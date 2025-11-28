"""
NeuroWeb Client for TruthGraph Trust Layer
Handles connection and interaction with NeuroWeb (Polkadot Parachain)
"""

import logging
from typing import Optional, Dict, Any, List
from substrateinterface import SubstrateInterface, Keypair
from substrateinterface.exceptions import SubstrateRequestException

from truthgraph.chain_config import ChainConfig
from truthgraph.exceptions import ChainConnectionException, ChainTransactionException
from truthgraph.logging_config import get_correlation_id
from truthgraph.utils.retry import retry_with_backoff

logger = logging.getLogger(__name__)

class NeuroWebClient:
    """
    Enterprise-grade client for interacting with NeuroWeb
    """
    
    def __init__(self):
        self.config = ChainConfig
        self.interface: Optional[SubstrateInterface] = None
        self.keypair: Optional[Keypair] = None
        
        self._initialize_keypair()
        
    def _initialize_keypair(self):
        """Initialize account keypair from seed"""
        if self.config.OPERATOR_SEED:
            try:
                self.keypair = Keypair.create_from_uri(self.config.OPERATOR_SEED)
                logger.info(f"NeuroWeb operator account initialized: {self.keypair.ss58_address}")
            except Exception as e:
                logger.error(f"Failed to initialize NeuroWeb keypair: {e}")
                # Don't raise here, allow read-only mode
        else:
            logger.warning("No NeuroWeb operator seed provided. Client will be read-only.")

    def connect(self) -> bool:
        """
        Establish connection to NeuroWeb
        
        Returns:
            bool: True if connected successfully
        """
        try:
            logger.info(f"Connecting to NeuroWeb at {self.config.RPC_ENDPOINT_WS}...")
            self.interface = SubstrateInterface(
                url=self.config.RPC_ENDPOINT_WS,
                ss58_format=42,  # Standard Substrate format
                type_registry_preset='substrate-node-template' # Generic preset, adjust if specific types needed
            )
            
            # Verify connection by getting chain info
            chain_info = self.interface.rpc_request("system_chain", []).get('result')
            logger.info(f"Successfully connected to {chain_info}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to NeuroWeb: {e}")
            raise ChainConnectionException(f"Connection failed: {str(e)}", cause=e)

    @retry_with_backoff(max_retries=3)
    def get_block_number(self) -> int:
        """Get current block number"""
        if not self.interface:
            self.connect()
            
        try:
            result = self.interface.query("System", "Number")
            return result.value
        except Exception as e:
            logger.error(f"Failed to get block number: {e}")
            raise ChainConnectionException("Failed to query chain", cause=e)

    @retry_with_backoff(max_retries=3)
    def get_balance(self, address: Optional[str] = None) -> Dict[str, Any]:
        """
        Get account balance
        
        Args:
            address: Address to query (defaults to operator)
            
        Returns:
            Dict containing free and reserved balance
        """
        if not self.interface:
            self.connect()
            
        target_address = address or (self.keypair.ss58_address if self.keypair else None)
        if not target_address:
            raise ValueError("No address provided and no operator keypair available")
            
        try:
            result = self.interface.query("System", "Account", [target_address])
            data = result.value['data']
            return {
                "free": data['free'],
                "reserved": data['reserved'],
                "misc_frozen": data['misc_frozen'],
                "fee_frozen": data['fee_frozen']
            }
        except Exception as e:
            logger.error(f"Failed to get balance for {target_address}: {e}")
            raise ChainConnectionException("Failed to query balance", cause=e)

    @retry_with_backoff(max_retries=3)
    def submit_attestation(self, ual: str, content_hash: str) -> str:
        """
        Submit an on-chain attestation for a Knowledge Asset
        
        Args:
            ual: Uniform Asset Locator of the DKG asset
            content_hash: Hash of the content being attested
            
        Returns:
            str: Transaction hash
        """
        correlation_id = get_correlation_id()
        logger.info(f"Submitting attestation for {ual} - correlation_id: {correlation_id}")
        
        if not self.interface:
            self.connect()
            
        if not self.keypair:
            raise ChainTransactionException("Cannot sign transaction: No operator keypair")
            
        try:
            # Construct the remark extrinsic (simple on-chain storage)
            # Format: "TruthGraph:Attest:{ual}:{content_hash}"
            attestation_data = f"TruthGraph:Attest:{ual}:{content_hash}"
            
            call = self.interface.compose_call(
                call_module='System',
                call_function='remark',
                call_params={
                    'remark': attestation_data.encode('utf-8')
                }
            )
            
            extrinsic = self.interface.create_signed_extrinsic(
                call=call,
                keypair=self.keypair
            )
            
            receipt = self.interface.submit_extrinsic(
                extrinsic,
                wait_for_inclusion=True
            )
            
            if receipt.is_success:
                tx_hash = receipt.extrinsic_hash
                logger.info(f"Attestation submitted successfully. Tx Hash: {tx_hash}")
                return tx_hash
            else:
                raise ChainTransactionException(f"Transaction failed: {receipt.error_message}")
                
        except SubstrateRequestException as e:
            logger.error(f"Substrate request failed: {e}")
            raise ChainTransactionException("Failed to submit attestation", cause=e)
        except Exception as e:
            logger.error(f"Unexpected error submitting attestation: {e}")
            raise ChainTransactionException("Unexpected error", cause=e)

    def verify_attestation(self, tx_hash: str, expected_ual: str, expected_hash: str) -> bool:
        """
        Verify an on-chain attestation exists and matches
        
        Args:
            tx_hash: Transaction hash to check
            expected_ual: UAL expected in the attestation
            expected_hash: Content hash expected
            
        Returns:
            bool: True if valid attestation found
        """
        if not self.interface:
            self.connect()
            
        try:
            # Retrieve the extrinsic
            receipt = self.interface.retrieve_extrinsic_by_hash(tx_hash)
            if not receipt:
                logger.warning(f"Transaction {tx_hash} not found")
                return False
                
            # Check if it was successful (this might need block retrieval to be 100% sure of success event)
            # For simplicity, we check the call data
            
            call = receipt.call
            if call.call_module.name == 'System' and call.call_function.name == 'remark':
                remark_bytes = call.call_args[0]['value']
                # Handle different return types (bytes or hex string)
                if isinstance(remark_bytes, str) and remark_bytes.startswith('0x'):
                    remark_data = bytes.fromhex(remark_bytes[2:]).decode('utf-8')
                elif isinstance(remark_bytes, bytes):
                    remark_data = remark_bytes.decode('utf-8')
                else:
                    remark_data = str(remark_bytes)

                expected_data = f"TruthGraph:Attest:{expected_ual}:{expected_hash}"
                
                is_valid = remark_data == expected_data
                logger.info(f"Verification for {tx_hash}: {is_valid}")
                return is_valid
                
            return False
            
        except Exception as e:
            logger.error(f"Verification failed: {e}")
            return False

