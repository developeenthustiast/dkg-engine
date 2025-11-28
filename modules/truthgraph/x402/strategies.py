"""
Payment Strategies for x402 Client
Defines how payments are actually executed (Mock, Lightning, On-chain)
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class PaymentStrategy(ABC):
    """Abstract base class for payment strategies"""
    
    @abstractmethod
    async def pay(self, invoice: str, amount: int, currency: str) -> str:
        """
        Execute payment
        
        Args:
            invoice: Payment request/invoice string
            amount: Amount to pay
            currency: Currency code (e.g., 'SAT', 'NEURO')
            
        Returns:
            str: Payment proof (preimage or token)
        """
        pass

class MockPaymentStrategy(PaymentStrategy):
    """
    Mock payment strategy for testing/hackathon
    Always succeeds without real money
    """
    
    async def pay(self, invoice: str, amount: int, currency: str) -> str:
        logger.info(f"[MOCK] Paying {amount} {currency} for invoice: {invoice[:20]}...")
        # Return a fake preimage/token
        return f"mock_proof_{hash(invoice)}"

class LightningPaymentStrategy(PaymentStrategy):
    """
    Lightning Network payment strategy (Placeholder)
    """
    
    async def pay(self, invoice: str, amount: int, currency: str) -> str:
        logger.warning("Lightning payment not fully implemented yet.")
        # In production, connect to LND/CoreLightning node here
        return "ln_proof_placeholder"

class NeuroWebPaymentStrategy(PaymentStrategy):
    """
    NeuroWeb on-chain payment strategy (Placeholder)
    """
    
    async def pay(self, invoice: str, amount: int, currency: str) -> str:
        logger.warning("NeuroWeb payment not fully implemented yet.")
        # In production, submit transaction to NeuroWeb chain
        return "neuro_tx_hash_placeholder"
