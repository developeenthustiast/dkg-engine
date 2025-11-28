"""
Example 3: Running the Autonomous Agent
---------------------------------------
This script demonstrates the full power of TruthGraph:
1. An Autonomous AI Agent receives a high-level goal.
2. It plans a sequence of actions (ReAct pattern).
3. It uses tools to Search DKG, Verify Claims, and Publish Results.
4. It secures its findings on NeuroWeb.
"""

import asyncio
import logging
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from truthgraph.agent.agent_core import AgentCore

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Example3")

async def main():
    logger.info("Initializing Autonomous Agent...")
    agent = AgentCore()
    
    # Define a goal
    goal = "Verify if the following claim is a hallucination: 'The capital of Mars is Elonville.'"
    
    logger.info(f"🤖 Agent Goal: {goal}")
    logger.info("-" * 50)
    
    try:
        # Run the agent
        final_answer = await agent.run(goal, max_steps=10)
        
        logger.info("-" * 50)
        logger.info(f"✅ Agent Finished!")
        logger.info(f"Final Answer: {final_answer}")
        
        # Inspect Memory (Optional)
        logger.info("\nAgent Thought Process:")
        for msg in agent.memory.get_history():
            if msg['role'] == 'assistant':
                print(f"  {msg['content']}")
                
    except Exception as e:
        logger.error(f"❌ Agent Failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
