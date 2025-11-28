"""
Agent Memory for TruthGraph Autonomous Agent
Manages short-term context and long-term history for the agent
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class AgentMessage(BaseModel):
    """Represents a message in the agent's memory"""
    role: str  # 'system', 'user', 'assistant', 'tool'
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class AgentContext(BaseModel):
    """Current execution context"""
    goal: str
    steps_taken: int = 0
    max_steps: int = 10
    messages: List[AgentMessage] = Field(default_factory=list)
    variables: Dict[str, Any] = Field(default_factory=dict)

class AgentMemory:
    """
    Enterprise-grade memory management for the agent
    """
    
    def __init__(self):
        self.current_context: Optional[AgentContext] = None
        self.long_term_history: List[Dict[str, Any]] = []
        
    def initialize_context(self, goal: str, max_steps: int = 10):
        """Start a new execution context"""
        self.current_context = AgentContext(
            goal=goal,
            max_steps=max_steps
        )
        # Add system prompt/initial instruction
        self.add_message("system", f"You are TruthGraph Agent. Your goal is: {goal}")
        logger.info(f"Agent memory initialized with goal: {goal}")

    def add_message(self, role: str, content: str, metadata: Dict[str, Any] = None):
        """Add a message to the current context"""
        if not self.current_context:
            raise ValueError("Context not initialized")
            
        message = AgentMessage(
            role=role,
            content=content,
            metadata=metadata or {}
        )
        self.current_context.messages.append(message)
        logger.debug(f"Added message to memory: [{role}] {content[:50]}...")

    def get_history(self) -> List[Dict[str, Any]]:
        """Get formatted history for the LLM"""
        if not self.current_context:
            return []
            
        return [
            {
                "role": msg.role,
                "content": msg.content
            }
            for msg in self.current_context.messages
        ]

    def clear_context(self):
        """Archive and clear current context"""
        if self.current_context:
            # Save summary to long-term history (simplified)
            self.long_term_history.append({
                "goal": self.current_context.goal,
                "timestamp": datetime.utcnow().isoformat(),
                "steps": self.current_context.steps_taken
            })
            self.current_context = None
            logger.info("Agent context cleared and archived")
