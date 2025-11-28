"""
Agent Tools for TruthGraph Autonomous Agent
Standardized interfaces for the agent to interact with DKG, NeuroWeb, and Analysis Engines
"""

import logging
import json
from typing import Dict, Any, List, Optional, Callable
from pydantic import BaseModel, Field

from truthgraph.dkg_client import DKGQueryClient
from truthgraph.dkg_publisher import DKGPublisher
from truthgraph.comparison_engine import ComparisonEngine
from truthgraph.hallucination_detector import HallucinationDetector
from truthgraph.bias_analyzer import BiasAnalyzer
from truthgraph.data_sources.wikipedia import WikipediaClient

logger = logging.getLogger(__name__)

class ToolDefinition(BaseModel):
    """Definition of a tool available to the agent"""
    name: str
    description: str
    parameters: Dict[str, Any]

class AgentTools:
    """
    Registry of tools available to the autonomous agent
    Wraps existing engines and clients into agent-callable functions
    """
    
    def __init__(self):
        # Initialize underlying components
        self.dkg_client = DKGQueryClient()
        self.dkg_publisher = DKGPublisher()
        self.comparison_engine = ComparisonEngine(publish_to_dkg=True, enable_attestations=True)
        self.hallucination_detector = HallucinationDetector(publish_to_dkg=True, enable_attestations=True)
        self.bias_analyzer = BiasAnalyzer(publish_to_dkg=True, enable_attestations=True)
        self.wikipedia_client = WikipediaClient()
        
        # Registry of callable tools
        self.tools: Dict[str, Callable] = {}
        self.definitions: List[ToolDefinition] = []
        
        self._register_tools()
        
    def _register_tools(self):
        """Register all available tools"""
        
        # 1. Search DKG
        self._register(
            name="search_dkg",
            description="Search the Decentralized Knowledge Graph for existing knowledge assets.",
            func=self._search_dkg,
            parameters={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query keywords"}
                },
                "required": ["query"]
            }
        )
        
        # 2. Compare Claims
        self._register(
            name="compare_claims",
            description="Compare two claims to check for conflicts or consistency. Automatically publishes result to DKG and creates NeuroWeb attestation.",
            func=self._compare_claims,
            parameters={
                "type": "object",
                "properties": {
                    "claim1": {"type": "string", "description": "First claim"},
                    "claim2": {"type": "string", "description": "Second claim"}
                },
                "required": ["claim1", "claim2"]
            }
        )
        
        # 3. Detect Hallucinations
        self._register(
            name="detect_hallucinations",
            description="Analyze text to detect AI hallucinations or unsupported claims. Automatically publishes result to DKG and creates NeuroWeb attestation.",
            func=self._detect_hallucinations,
            parameters={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to analyze"}
                },
                "required": ["text"]
            }
        )
        
        # 4. Search Web (Wikipedia)
        self._register(
            name="search_web",
            description="Search Wikipedia for factual information to verify claims.",
            func=self._search_web,
            parameters={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search topic"}
                },
                "required": ["query"]
            }
        )

    def _register(self, name: str, description: str, func: Callable, parameters: Dict[str, Any]):
        """Helper to register a tool"""
        self.tools[name] = func
        self.definitions.append(ToolDefinition(
            name=name,
            description=description,
            parameters=parameters
        ))
        logger.debug(f"Registered agent tool: {name}")

    # --- Tool Implementations ---

    async def _search_dkg(self, query: str) -> str:
        """Tool implementation for DKG search"""
        try:
            results = await self.dkg_client.search_assets(query)
            return json.dumps(results[:3], default=str) # Limit to top 3
        except Exception as e:
            return f"Error searching DKG: {str(e)}"

    async def _compare_claims(self, claim1: str, claim2: str) -> str:
        """Tool implementation for claim comparison"""
        try:
            result = await self.comparison_engine.compare(claim1, claim2)
            # Return concise summary
            summary = {
                "similarity": result.get("similarity_score"),
                "conflict": result.get("conflict"),
                "explanation": result.get("explanation"),
                "ual": result.get("dkg", {}).get("ual"),
                "attestation": result.get("attestation", {}).get("tx_hash")
            }
            return json.dumps(summary, default=str)
        except Exception as e:
            return f"Error comparing claims: {str(e)}"

    async def _detect_hallucinations(self, text: str) -> str:
        """Tool implementation for hallucination detection"""
        try:
            result = await self.hallucination_detector.detect(text)
            summary = {
                "is_hallucination": result.get("is_hallucination"),
                "score": result.get("score"),
                "ual": result.get("dkg", {}).get("ual"),
                "attestation": result.get("attestation", {}).get("tx_hash")
            }
            return json.dumps(summary, default=str)
        except Exception as e:
            return f"Error detecting hallucinations: {str(e)}"

    async def _search_web(self, query: str) -> str:
        """Tool implementation for web search"""
        try:
            article = await self.wikipedia_client.fetch_article(query)
            if not article:
                return "No information found."
            # Return summary
            return f"Found article '{article.get('title')}': {article.get('summary')[:500]}..."
        except Exception as e:
            return f"Error searching web: {str(e)}"

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Get definitions in format suitable for LLM function calling"""
        return [tool.dict() for tool in self.definitions]

    async def execute_tool(self, name: str, arguments: Dict[str, Any]) -> str:
        """Execute a tool by name"""
        if name not in self.tools:
            return f"Error: Tool '{name}' not found."
        
        try:
            logger.info(f"Agent executing tool: {name} with args: {arguments}")
            result = await self.tools[name](**arguments)
            return result
        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            return f"Error executing tool '{name}': {str(e)}"
