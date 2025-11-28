"""
NeuroWeb (OriginTrail Parachain) Configuration
"""

import os
from typing import Dict, Any

class ChainConfig:
    """Configuration for NeuroWeb connection"""
    
    # Network Details
    NETWORK_NAME = "NeuroWeb Testnet"
    CHAIN_ID = 20430
    TOKEN_SYMBOL = "NEURO"
    
    # RPC Endpoints
    # Primary WebSocket endpoint for Substrate interaction
    RPC_ENDPOINT_WS = os.getenv(
        "NEUROWEB_RPC_WS", 
        "wss://lofar-testnet.origin-trail.network"
    )
    
    # HTTP Endpoint for standard RPC calls
    RPC_ENDPOINT_HTTP = os.getenv(
        "NEUROWEB_RPC_HTTP", 
        "https://lofar-testnet.origin-trail.network"
    )
    
    # Block Explorer
    EXPLORER_URL = "https://neuroweb-testnet.subscan.io"
    
    # Account Configuration
    # Private key/seed for the account creating attestations
    # WARNING: Must be set in environment variables for security
    OPERATOR_SEED = os.getenv("NEUROWEB_OPERATOR_SEED")
    
    # Contract Addresses (if applicable in future)
    ATTESTATION_REGISTRY_ADDRESS = os.getenv("ATTESTATION_REGISTRY_ADDRESS")

    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Get configuration as dictionary"""
        return {
            "network": cls.NETWORK_NAME,
            "chain_id": cls.CHAIN_ID,
            "rpc_ws": cls.RPC_ENDPOINT_WS,
            "rpc_http": cls.RPC_ENDPOINT_HTTP,
            "has_seed": bool(cls.OPERATOR_SEED)
        }
