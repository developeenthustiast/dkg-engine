"""
Agent Planner for TruthGraph Autonomous Agent
Handles decision making using LLM (OpenAI/Anthropic)
"""

import logging
import json
import os
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

# Simple LLM client wrapper (replace with langchain/pydantic-ai in production)
# For hackathon, we'll use a direct HTTP call or a placeholder if no key
import aiohttp

logger = logging.getLogger(__name__)

class PlanStep(BaseModel):
    """A single step in the plan"""
    thought: str
    tool_name: Optional[str]
    tool_args: Optional[Dict[str, Any]]
    is_final: bool = False
    final_answer: Optional[str] = None

class AgentPlanner:
    """
    Enterprise-grade planner using ReAct pattern
    """
    
    def __init__(self, model: str = "gpt-4o"):
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY")
        
    async def plan_next_step(
        self, 
        history: List[Dict[str, str]], 
        tools: List[Dict[str, Any]]
    ) -> PlanStep:
        """
        Decide the next step based on history and available tools
        """
        if not self.api_key:
            logger.warning("No OpenAI API key found. Using mock planner.")
            return self._mock_plan(history)
            
        try:
            # Construct prompt
            system_prompt = self._build_system_prompt(tools)
            messages = [{"role": "system", "content": system_prompt}] + history
            
            # Call LLM (Simulated for this environment, but structure is real)
            # In a real run, this would make an API call
            # response = await self._call_llm(messages)
            
            # For the purpose of this environment where we might not have live API access
            # We will use a rule-based fallback if the API call fails or is mocked
            return self._mock_plan(history)
            
        except Exception as e:
            logger.error(f"Planning failed: {e}")
            return PlanStep(
                thought="Error in planning, stopping.",
                tool_name=None,
                tool_args=None,
                is_final=True,
                final_answer="I encountered an error while planning."
            )

    def _build_system_prompt(self, tools: List[Dict[str, Any]]) -> str:
        """Build the system prompt for the LLM"""
        tool_desc = json.dumps(tools, indent=2)
        return f"""
You are the TruthGraph Autonomous Agent.
Your goal is to verify claims, detect hallucinations, and ensure knowledge integrity using the Decentralized Knowledge Graph (DKG) and NeuroWeb.

You have access to the following tools:
{tool_desc}

Follow this pattern:
1. THOUGHT: Analyze the current situation and previous steps.
2. ACTION: Select a tool to use (if needed).
3. ARGS: Provide arguments for the tool.

If you have sufficient information to answer the user's request or have completed the goal, output a FINAL ANSWER.

Response Format (JSON):
{{
    "thought": "reasoning here",
    "tool_name": "name_of_tool_or_null",
    "tool_args": {{ "arg": "value" }},
    "is_final": boolean,
    "final_answer": "answer if is_final is true"
}}
"""

    def _mock_plan(self, history: List[Dict[str, str]]) -> PlanStep:
        """
        Simple rule-based planner for testing/demo without API key
        Detects intent from the last user message
        """
        last_msg = history[-1]['content'].lower() if history else ""
        
        if "compare" in last_msg:
            # Extract claims roughly (very naive)
            parts = last_msg.replace("compare", "").split("and")
            if len(parts) == 2:
                return PlanStep(
                    thought="User wants to compare two claims. I should use the comparison tool.",
                    tool_name="compare_claims",
                    tool_args={
                        "claim1": parts[0].strip(),
                        "claim2": parts[1].strip()
                    }
                )
        
        if "hallucination" in last_msg or "verify" in last_msg:
             return PlanStep(
                thought="User wants to check for hallucinations. I should use the detector.",
                tool_name="detect_hallucinations",
                tool_args={"text": last_msg}
            )
            
        if "search" in last_msg:
             return PlanStep(
                thought="User wants to search the DKG.",
                tool_name="search_dkg",
                tool_args={"query": last_msg.replace("search", "").strip()}
            )

        return PlanStep(
            thought="I have finished the task.",
            tool_name=None,
            tool_args=None,
            is_final=True,
            final_answer="Task completed (Mock Planner)."
        )

    async def _call_llm(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """Actual LLM call (placeholder implementation)"""
        # Implementation would use aiohttp to call OpenAI API
        pass
