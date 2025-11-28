"""
Agent Core for TruthGraph Autonomous Agent
Main execution loop integrating Memory, Planner, and Tools
"""

import logging
import asyncio
from typing import Optional, Dict, Any

from truthgraph.agent.agent_memory import AgentMemory
from truthgraph.agent.agent_planner import AgentPlanner
from truthgraph.agent.agent_tools import AgentTools

logger = logging.getLogger(__name__)

class AgentCore:
    """
    Autonomous Agent Core
    Executes the ReAct loop: Observe -> Think -> Act
    """
    
    def __init__(self):
        self.memory = AgentMemory()
        self.planner = AgentPlanner()
        self.tools = AgentTools()
        
    async def run(self, goal: str, max_steps: int = 10) -> str:
        """
        Run the agent to achieve a specific goal
        
        Args:
            goal: The objective (e.g., "Verify the claim that X is Y")
            max_steps: Safety limit to prevent infinite loops
            
        Returns:
            Final answer or result summary
        """
        logger.info(f"Starting agent run with goal: {goal}")
        self.memory.initialize_context(goal, max_steps)
        self.memory.add_message("user", goal)
        
        step = 0
        while step < max_steps:
            step += 1
            logger.info(f"Agent Step {step}/{max_steps}")
            
            # 1. Plan
            history = self.memory.get_history()
            tool_defs = self.tools.get_tool_definitions()
            
            plan = await self.planner.plan_next_step(history, tool_defs)
            
            # Log thought
            logger.info(f"Thought: {plan.thought}")
            self.memory.add_message("assistant", f"Thought: {plan.thought}")
            
            # 2. Check for completion
            if plan.is_final:
                logger.info("Agent reached final answer")
                self.memory.add_message("assistant", f"Final Answer: {plan.final_answer}")
                return plan.final_answer
            
            # 3. Act (Execute Tool)
            if plan.tool_name:
                logger.info(f"Action: {plan.tool_name} {plan.tool_args}")
                self.memory.add_message(
                    "assistant", 
                    f"Action: {plan.tool_name}\nArgs: {plan.tool_args}"
                )
                
                tool_result = await self.tools.execute_tool(plan.tool_name, plan.tool_args)
                
                # 4. Observe (Record Result)
                logger.info(f"Observation: {tool_result[:100]}...")
                self.memory.add_message("tool", tool_result)
            else:
                logger.warning("Planner returned no tool and no final answer. Stopping.")
                return "Agent stopped (uncertainty)."
                
        return "Max steps reached without final answer."

    async def run_autonomous_loop(self, interval_seconds: int = 300):
        """
        Run in continuous autonomous mode
        Periodically checks for new tasks or monitors topics
        """
        logger.info("Starting autonomous loop")
        while True:
            try:
                # Example: Pick a trending topic from DKG or Web and verify it
                # For now, just a placeholder action
                logger.info("Autonomous heartbeat: Checking for new claims...")
                
                # await self.run("Check recent crypto news for hallucinations")
                
                await asyncio.sleep(interval_seconds)
            except Exception as e:
                logger.error(f"Error in autonomous loop: {e}")
                await asyncio.sleep(60) # Wait before retry
