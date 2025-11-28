"""
Example 2: Verifying Trust via NeuroWeb
---------------------------------------
This script demonstrates how to:
1. Verify an on-chain attestation on the NeuroWeb parachain.
2. Ensure the data in the DKG matches the immutable proof on the blockchain.
"""

import asyncio
import logging
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from truthgraph.neuroweb_client import NeuroWebClient
from truthgraph.attestation_manager import AttestationManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Example2")

async def main():
    logger.info("Initializing Trust Layer components...")
    
    # Initialize clients (Mocked if no env vars, or real if configured)
    nw_client = NeuroWebClient()
    attestation_mgr = AttestationManager()
    
    # Sample Data (Simulating a result that was previously published)
    sample_ual = "did:dkg:otp:2043/0x5c3.../12345"
    sample_data = {"claim": "TruthGraph is awesome", "score": 1.0}
    
    # 1. Create Attestation (Simulating the publishing step)
    logger.info("Creating attestation for sample data...")
    try:
        attestation = attestation_mgr.create_attestation(sample_ual, sample_data)
        tx_hash = attestation['tx_hash']
        logger.info(f"Attestation submitted. Tx Hash: {tx_hash}")
        
        # 2. Verify Attestation
        logger.info("Verifying attestation on-chain...")
        
        # Re-compute hash locally to verify integrity
        local_hash = attestation_mgr.compute_hash(sample_data)
        logger.info(f"Local Content Hash: {local_hash}")
        
        # Verify against chain
        is_valid = nw_client.verify_attestation(tx_hash, sample_ual, local_hash)
        
        if is_valid:
            logger.info("✅ TRUST VERIFIED: On-chain proof matches local data.")
        else:
            logger.error("❌ TRUST FAILED: On-chain proof does not match.")
            
    except Exception as e:
        logger.error(f"Error in example: {e}")

if __name__ == "__main__":
    asyncio.run(main())
