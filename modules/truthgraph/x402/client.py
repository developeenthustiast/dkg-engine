"""
x402 Client for TruthGraph
Handles HTTP 402 Payment Required responses and executes micropayments
"""

import logging
import aiohttp
from typing import Dict, Any, Optional, Union

from truthgraph.x402.strategies import PaymentStrategy, MockPaymentStrategy

logger = logging.getLogger(__name__)

class X402Client:
    """
    Client for handling x402 protocol (HTTP 402 Payment Required)
    """
    
    def __init__(self, strategy: PaymentStrategy = None, budget_limit: float = 10.0):
        self.strategy = strategy or MockPaymentStrategy()
        self.budget_limit = budget_limit
        self.spent_total = 0.0
        self.token_cache: Dict[str, str] = {} # URL -> Token
        
    async def request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """
        Make an HTTP request with automatic x402 handling
        
        Args:
            method: HTTP method (GET, POST, etc.)
            url: Target URL
            **kwargs: Additional arguments for aiohttp
            
        Returns:
            Response JSON or text
        """
        # Check cache for existing token
        if url in self.token_cache:
            headers = kwargs.get('headers', {})
            headers['Authorization'] = f"Bearer {self.token_cache[url]}"
            kwargs['headers'] = headers
            
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, **kwargs) as response:
                
                # Handle 402 Payment Required
                if response.status == 402:
                    logger.info(f"Encountered 402 Payment Required at {url}")
                    return await self._handle_payment(response, method, url, **kwargs)
                
                # Handle success
                if 200 <= response.status < 300:
                    try:
                        return await response.json()
                    except:
                        return await response.text()
                        
                # Handle other errors
                logger.warning(f"Request failed with status {response.status}")
                response.raise_for_status()
                
    async def _handle_payment(self, response: aiohttp.ClientResponse, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """Handle the payment flow"""
        
        # 1. Parse WWW-Authenticate header
        auth_header = response.headers.get('WWW-Authenticate')
        if not auth_header:
            raise Exception("402 response missing WWW-Authenticate header")
            
        # Example header: L402 invoice="lnbc...", amount=100, currency="SAT"
        # Simplified parsing for demo
        details = self._parse_auth_header(auth_header)
        
        invoice = details.get('invoice')
        amount = float(details.get('amount', 0))
        currency = details.get('currency', 'UNK')
        
        if not invoice:
            raise Exception("Could not extract invoice from 402 response")
            
        # 2. Check budget
        if self.spent_total + amount > self.budget_limit:
            raise Exception(f"Payment of {amount} {currency} exceeds budget limit")
            
        # 3. Pay
        logger.info(f"Paying {amount} {currency}...")
        proof = await self.strategy.pay(invoice, int(amount), currency)
        self.spent_total += amount
        
        # 4. Cache token/proof
        # In L402, the proof is often the preimage, used to sign or as a bearer token
        # For simplicity, we'll treat the proof as a Bearer token
        self.token_cache[url] = proof
        
        # 5. Retry request
        logger.info("Retrying request with payment proof")
        headers = kwargs.get('headers', {})
        headers['Authorization'] = f"Bearer {proof}" # Or L402 <credential>
        kwargs['headers'] = headers
        
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, **kwargs) as retry_response:
                if retry_response.status == 402:
                    raise Exception("Payment failed or proof rejected")
                    
                try:
                    return await retry_response.json()
                except:
                    return await retry_response.text()

    def _parse_auth_header(self, header: str) -> Dict[str, str]:
        """
        Parse WWW-Authenticate header
        Format: Scheme param1="value1", param2="value2"
        """
        parts = header.split(' ', 1)
        if len(parts) < 2:
            return {}
            
        params = parts[1]
        result = {}
        for pair in params.split(','):
            kv = pair.strip().split('=')
            if len(kv) == 2:
                key = kv[0].strip()
                val = kv[1].strip().strip('"')
                result[key] = val
        return result
