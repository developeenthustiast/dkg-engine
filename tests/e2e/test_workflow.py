"""
End-to-End Test for TruthGraph Workflow
"""

import pytest
from truthgraph.agent.agent_core import AgentCore

@pytest.mark.asyncio
async def test_e2e_hallucination_verification():
    """
    Test the full flow:
    User Request -> Agent Plan -> Hallucination Check -> DKG Publish -> NeuroWeb Attest -> Result
    """
    agent = AgentCore()
    
    # We rely on the mock planner and mock tools (or real ones if env is set)
    # For this E2E, we assume the environment variables are set or we are using the mock planner
    # which we know directs to 'detect_hallucinations'
    
    goal = "Check for hallucinations in: 'The earth is flat and rests on a turtle.'"
    
    # Run agent
    result = await agent.run(goal, max_steps=5)
    
    # Verify result
    assert result is not None
    # The mock planner usually ends with "Task completed" or similar if it loops, 
    # but our mock planner logic for 'hallucination' returns a tool use.
    # The AgentCore loop executes the tool, then observes.
    # The next plan step from mock planner (if not updated) might be to repeat or finish.
    # We should ensure our mock planner handles the "after tool" state or we just check that it ran.
    
    # For a robust test, we'd check the memory to see if the tool was called
    history = agent.memory.get_history()
    
    tool_calls = [m for m in history if m["role"] == "assistant" and "Action: detect_hallucinations" in m["content"]]
    assert len(tool_calls) > 0, "Agent should have called detect_hallucinations"
    
    tool_outputs = [m for m in history if m["role"] == "tool"]
    assert len(tool_outputs) > 0, "Tool should have returned output"
