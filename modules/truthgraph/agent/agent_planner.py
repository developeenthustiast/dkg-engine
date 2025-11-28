"""
Agent Planner for TruthGraph Autonomous Agent
Handles decision making using LLM (Google Gemini)
"""

import logging
import json
import os
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
    Enterprise-grade planner using ReAct pattern with Google Gemini
    """
    
    def __init__(self, model: str = "models/gemini-2.0-flash"):
        self.model_name = model
        self.api_key = os.getenv("GOOGLE_API_KEY")
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(model)
            logger.info(f"Google Gemini initialized: {model}")
        else:
            self.model = None
            logger.warning("No Google API key found. Using mock planner.")
        
    async def plan_next_step(
        self, 
        history: List[Dict[str, str]], 
        tools: List[Dict[str, Any]]
    ) -> PlanStep:
        """
        Decide the next step based on history and available tools
        """
        if not self.model:
            logger.warning("No Gemini API key found. Using mock planner.")
            return self._mock_plan(history)
            
        try:
            # Construct prompt
            system_prompt = self._build_system_prompt(tools)
            
            # Format conversation history
            conversation = system_prompt + "\n\nConversation history:\n"
            for msg in history:
                conversation += f"{msg['role']}: {msg['content']}\n"
            
            conversation += "\nRespond with JSON following the format specified above."
            
            # Call Gemini
            response = self.model.generate_content(conversation)
            response_text = response.text
            
            # Parse JSON response
            # Remove markdown code blocks if present
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]
            
            result = json.loads(response_text.strip())
            
            return PlanStep(**result)
            
        except Exception as e:
            logger.error(f"Planning with Gemini failed: {e}")
            logger.info("Falling back to mock planner")
            return self._mock_plan(history)

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

Response Format (JSON only, no other text):
{{
    "thought": "your reasoning here",
    "tool_name": "name_of_tool_or_null",
    "tool_args": {{"arg": "value"}},
    "is_final": false,
    "final_answer": null
}}

OR when finished:
{{
    "thought": "I have completed the verification",
    "tool_name": null,
    "tool_args": null,
    "is_final": true,
    "final_answer": "your final answer here"
}}
"""

    def _mock_plan(self, history: List[Dict[str, str]]) -> PlanStep:
        """
        Simple rule-based planner for testing/demo without API key
        """
        last_msg = history[-1]['content'].lower() if history else ""
        
        if "flat" in last_msg or "round" in last_msg:
            return PlanStep(
                thought="User is asking about Earth's shape. I should verify this claim.",
                tool_name="detect_hallucinations",
                tool_args={"text": last_msg}
            )
        
        if "compare" in last_msg:
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
