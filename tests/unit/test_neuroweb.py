"""
Unit Tests for NeuroWeb Client
"""

import pytest
from unittest.mock import MagicMock, patch
from truthgraph.neuroweb_client import NeuroWebClient

def test_neuroweb_initialization():
    with patch('truthgraph.neuroweb_client.SubstrateInterface') as mock_substrate:
        client = NeuroWebClient()
        assert client is not None
        # Verify it didn't connect immediately if auto_connect is False (default)
        # or if it did, that it used the mock

@pytest.mark.asyncio
async def test_submit_attestation_mock():
    # Test the logic without hitting the chain
    with patch('truthgraph.neuroweb_client.SubstrateInterface') as mock_substrate:
        client = NeuroWebClient()
        client.substrate = mock_substrate
        client.keypair = MagicMock()
        
        # Mock receipt
        mock_receipt = {'extrinsic_hash': '0xhash'}
        client.substrate.submit_extrinsic.return_value = mock_receipt
        
        tx_hash = client.submit_attestation("did:dkg:123", "hash123")
        assert tx_hash == "0xhash"
