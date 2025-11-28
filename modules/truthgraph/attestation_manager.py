"""
Attestation Manager for TruthGraph
Handles creation and verification of on-chain attestations on NeuroWeb
"""

import logging
import hashlib
import json
from datetime import datetime
from typing import Dict, Any, Optional

from truthgraph.neuroweb_client import NeuroWebClient
from truthgraph.exceptions import AttestationException, ValidationException
from truthgraph.logging_config import get_correlation_id

logger = logging.getLogger(__name__)

class AttestationManager:
    """
    Manages the lifecycle of on-chain attestations
    """
    
    def __init__(self, client: Optional[NeuroWebClient] = None):
        self.client = client or NeuroWebClient()
        
    def create_attestation(self, ual: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create and submit an attestation for a Knowledge Asset
        
        Args:
            ual: Uniform Asset Locator
            data: Data content to attest (will be hashed)
            
        Returns:
            Dict containing attestation details and transaction hash
        """
        correlation_id = get_correlation_id()
        logger.info(f"Creating attestation for {ual} - correlation_id: {correlation_id}")
        
        try:
            # 1. Compute content hash
            content_hash = self._compute_hash(data)
            
            # 2. Submit to NeuroWeb
            tx_hash = self.client.submit_attestation(ual, content_hash)
            
            # 3. Construct attestation record
            attestation = {
                "ual": ual,
                "content_hash": content_hash,
                "tx_hash": tx_hash,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "chain": self.client.config.NETWORK_NAME,
                "chain_id": self.client.config.CHAIN_ID
            }
            
            logger.info(f"Attestation created successfully: {tx_hash}")
            return attestation
            
        except Exception as e:
            logger.error(f"Failed to create attestation: {e}")
            raise AttestationException(f"Attestation creation failed: {str(e)}", cause=e)

    def verify_attestation(self, ual: str, data: Dict[str, Any], tx_hash: str) -> Dict[str, Any]:
        """
        Verify an attestation against on-chain data
        
        Args:
            ual: UAL to verify
            data: Original data to verify against
            tx_hash: Transaction hash of the attestation
            
        Returns:
            Verification result
        """
        try:
            # 1. Recompute hash
            expected_hash = self._compute_hash(data)
            
            # 2. Verify on-chain
            is_valid = self.client.verify_attestation(tx_hash, ual, expected_hash)
            
            return {
                "valid": is_valid,
                "ual": ual,
                "tx_hash": tx_hash,
                "verified_at": datetime.utcnow().isoformat() + "Z"
            }
            
        except Exception as e:
            logger.error(f"Attestation verification failed: {e}")
            raise AttestationException("Verification failed", cause=e)

    def _compute_hash(self, data: Dict[str, Any]) -> str:
        """Compute SHA-256 hash of data dictionary"""
        # Sort keys for consistent hashing
        serialized = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(serialized.encode('utf-8')).hexdigest()
