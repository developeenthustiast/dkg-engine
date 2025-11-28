# TruthGraph - Quick Demo Guide

This guide will help you demonstrate TruthGraph for the hackathon video.

## 🎯 Demo Flow (5 minutes)

### 1. Introduction (30 seconds)
**What to say:**
> "I built TruthGraph to solve AI hallucinations by combining autonomous agents, the OriginTrail DKG, and blockchain trust. Let me show you how it works."

**What to show:**
- Open the GitHub repo
- Briefly scroll through the code structure

### 2. Architecture Overview (1 minute)
**What to say:**
> "TruthGraph has three layers: The Agent Layer for autonomous reasoning, the Knowledge Layer using OriginTrail's DKG for storage, and the Trust Layer with NeuroWeb for on-chain attestations."

**What to show:**
- Open `docs/ARCHITECTURE.md`
- Show the mermaid diagram

### 3. Live Demo - Web Interface (2 minutes)
**What to say:**
> "Let me show you the web interface. I can give the agent any goal, and it autonomously verifies claims."

**What to do:**
1. Open http://localhost:5173
2. Type: "Check if 'The capital of Mars is Elonville' is a hallucination"
3. Click "Run Agent"
4. **Point out:**
   - Real-time thoughts appearing
   - The agent searching Wikipedia
   - Tool execution (detect_hallucinations)
   - Final result: "Hallucination detected"

**What to say:**
> "Notice how the agent autonomously decided to use the hallucination detector, found evidence on Wikipedia, and determined this is false."

### 4. Show the Code (1 minute)
**What to say:**
> "Behind the scenes, every result is published to the DKG as a JSON-LD Knowledge Asset and attested on the NeuroWeb blockchain."

**What to show:**
- Open `backend/main.py` - show the API
- Open `modules/truthgraph/agent/agent_core.py` - show the ReAct loop
- Open `modules/truthgraph/x402/client.py` - mention x402 implementation

### 5. Wrap Up (30 seconds)
**What to say:**
> "TruthGraph addresses the Decentralized Community Notes challenge by providing AI-powered, verifiable fact-checking. It's enterprise-grade, fully tested, and ready to scale. Thank you!"

**What to show:**
- Show `pytest` passing (if you ran tests)
- Show the GitHub repo one more time

## 📝 Key Points to Emphasize:
- ✅ Autonomous (no human intervention needed)
- ✅ Decentralized (DKG + NeuroWeb)
- ✅ Verifiable (on-chain attestations)
- ✅ Extensible (x402 for monetization)
- ✅ Enterprise-grade (tests, docs, modern UI)

## 🎬 Recording Tips:
- Use OBS or Loom for screen recording
- Record in 1080p
- Speak clearly and confidently
- Show your passion for the project
- Keep it under 5 minutes
- Add background music (optional)

Good luck! 🚀
