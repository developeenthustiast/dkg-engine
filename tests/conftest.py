"""
Pytest Fixtures for TruthGraph Tests
"""

import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock

from truthgraph.dkg_client import DKGQueryClient
from truthgraph.dkg_publisher import DKGPublisher
from truthgraph.neuroweb_client import NeuroWebClient
from truthgraph.agent.agent_core import AgentCore
from truthgraph.x402.client import X402Client

@pytest.fixture
def mock_dkg_client():
    client = MagicMock(spec=DKGQueryClient)
    client.search_assets = AsyncMock(return_value=[{"ual": "did:dkg:123", "data": "test"}])
    client.get_asset = AsyncMock(return_value={"data": "test"})
    return client

@pytest.fixture
def mock_dkg_publisher():
    publisher = MagicMock(spec=DKGPublisher)
    publisher.publish_asset = AsyncMock(return_value={"ual": "did:dkg:new123"})
    publisher.publish_comparison = AsyncMock(return_value={"ual": "did:dkg:comp123"})
    publisher.publish_hallucination = AsyncMock(return_value={"ual": "did:dkg:hal123"})
    return publisher

@pytest.fixture
def mock_neuroweb_client():
    client = MagicMock(spec=NeuroWebClient)
    client.connect = MagicMock()
    client.submit_attestation = MagicMock(return_value="0x123abc")
    client.verify_attestation = MagicMock(return_value=True)
    return client

@pytest.fixture
def mock_x402_client():
    client = MagicMock(spec=X402Client)
    client.request = AsyncMock(return_value={"data": "premium_content"})
    return client

@pytest.fixture
def agent(mock_dkg_client, mock_dkg_publisher, mock_neuroweb_client):
    # In a real test we might inject these mocks if the Agent allowed dependency injection
    # For now we'll just instantiate a standard agent
    agent = AgentCore()
    # Monkey patch for testing if needed, or use as is for integration
    return agent
