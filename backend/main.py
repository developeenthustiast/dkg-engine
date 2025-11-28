"""
TruthGraph Web API Server
FastAPI backend for the TruthGraph web interface
"""

from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import sys
import os
from typing import List, Dict, Any
import json
import logging

# Add parent directory to path - FIXED PATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'modules'))

from modules.truthgraph.agent.agent_core import AgentCore
from modules.truthgraph.dkg_client import DKGQueryClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TruthGraph-API")

app = FastAPI(title="TruthGraph API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
agent_running = False
recent_results = []

class AgentGoalRequest(BaseModel):
    goal: str
    max_steps: int = 10

class AgentResponse(BaseModel):
    status: str
    result: str
    history: List[Dict[str, Any]]

@app.get("/")
async def root():
    return {
        "message": "TruthGraph API Server",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "agent_running": agent_running
    }

@app.post("/agent/run", response_model=AgentResponse)
async def run_agent(request: AgentGoalRequest):
    global agent_running, recent_results
    
    if agent_running:
        raise HTTPException(status_code=409, detail="Agent is already running")
    
    try:
        agent_running = True
        logger.info(f"Starting agent with goal: {request.goal}")
        
        # Initialize agent
        agent = AgentCore()
        
        # Run agent
        result = await agent.run(request.goal, max_steps=request.max_steps)
        
        # Get history
        history = agent.memory.get_history()
        
        # Store result
        result_data = {
            "goal": request.goal,
            "result": result,
            "timestamp": "now",
            "history_length": len(history)
        }
        recent_results.insert(0, result_data)
        if len(recent_results) > 10:
            recent_results.pop()
        
        agent_running = False
        
        return AgentResponse(
            status="success",
            result=result,
            history=history
        )
    
    except Exception as e:
        agent_running = False
        logger.error(f"Agent execution failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agent/status")
async def get_agent_status():
    return {
        "running": agent_running,
        "recent_runs": len(recent_results)
    }

@app.get("/knowledge/recent")
async def get_recent_knowledge():
    return {
        "results": recent_results
    }

@app.websocket("/ws/agent")
async def websocket_agent(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Send status updates
            await websocket.send_json({
                "type": "status",
                "running": agent_running
            })
            await asyncio.sleep(1)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
