"""
Trust Verifier for TruthGraph
Integrates DKG Knowledge Assets with NeuroWeb Attestations for full trust verification
"""

import logging
from typing import Dict, Any, Optional

from truthgraph.dkg_client import DKGQueryClient
from truthgraph.attestation_manager import AttestationManager
from truthgraph.exceptions import VerificationException
from truthgraph.logging_config import get_correlation_id

logger = logging.getLogger(__name__)

class TrustVerifier:
    """
    High-level verifier for the Trust Layer
    Verifies data integrity across Agent, Knowledge, and Trust layers
    """
    
    def __init__(self):
        self.dkg_client = DKGQueryClient()
        self.attestation_manager = AttestationManager()
        
    async def verify_asset_trust(self, ual: str, tx_hash: Optional[str] = None) -> Dict[str, Any]:
        """
        Perform comprehensive trust verification for a Knowledge Asset
        
        Args:
            ual: UAL of the asset
            tx_hash: Optional transaction hash (if known, otherwise searches)
            
        Returns:
            Trust verification report
        """
        correlation_id = get_correlation_id()
        logger.info(f"Verifying trust for {ual} - correlation_id: {correlation_id}")
        
        report = {
            "ual": ual,
            "trust_score": 0.0,
            "checks": {
                "dkg_integrity": False,
                "neuroweb_attestation": False
            },
            "details": {}
        }
        
        try:
            # 1. Retrieve from DKG
            asset = await self.dkg_client.get_asset(ual)
            report['checks']['dkg_integrity'] = True
            report['details']['dkg_asset'] = asset
            
            # 2. Verify NeuroWeb Attestation
            if tx_hash:
                # If we have the tx hash, verify directly
                verification = self.attestation_manager.verify_attestation(ual, asset, tx_hash)
                report['checks']['neuroweb_attestation'] = verification['valid']
                report['details']['attestation'] = verification
            else:
                # TODO: Implement lookup of attestation by UAL if tx_hash not provided
                # This would require an indexer or queryable storage on the chain side
                report['details']['attestation'] = "Transaction hash not provided, skipping on-chain check"
            
            # 3. Compute Trust Score
            score = 0.0
            if report['checks']['dkg_integrity']:
                score += 0.5
            if report['checks']['neuroweb_attestation']:
                score += 0.5
                
            report['trust_score'] = score
            
            logger.info(f"Trust verification complete. Score: {score}")
            return report
            
        except Exception as e:
            logger.error(f"Trust verification failed: {e}")
            raise VerificationException(f"Trust verification failed: {str(e)}", cause=e)
