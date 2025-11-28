"""
Unit Tests for Autonomous Agent
"""

import pytest
from truthgraph.agent.agent_core import AgentCore
from truthgraph.agent.agent_planner import AgentPlanner
from truthgraph.agent.agent_memory import AgentMemory

@pytest.mark.asyncio
async def test_agent_initialization():
    agent = AgentCore()
    assert agent.memory is not None
    assert agent.planner is not None
    assert agent.tools is not None

@pytest.mark.asyncio
async def test_planner_mock_response():
    planner = AgentPlanner()
    # Test the mock planner logic
    history = [{"role": "user", "content": "verify hallucination in 'sky is green'"}]
    plan = await planner.plan_next_step(history, [])
    
    assert plan.tool_name == "detect_hallucinations"
    assert plan.tool_args["text"] == "'sky is green'"

def test_memory_management():
    memory = AgentMemory()
    memory.initialize_context("test goal")
    memory.add_message("user", "hello")
    
    history = memory.get_history()
    assert len(history) == 2 # System + User
    assert history[1]["content"] == "hello"
