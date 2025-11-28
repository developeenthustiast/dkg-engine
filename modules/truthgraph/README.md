# TruthGraph - Decentralized Trust Layer for AI

> **Verifiable fact-checking powered by OriginTrail DKG, NeuroWeb, and autonomous AI agents**

[![DKG Global Hackathon 2025](https://img.shields.io/badge/DKG_Hackathon-2025-blue)](https://dorahacks.io/hackathon/origintrail-scaling-trust-ai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Node 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)

## 🎯 Overview

TruthGraph is an enterprise-grade autonomous AI agent system that verifies claims, detects hallucinations, and ensures knowledge integrity through the Decentralized Knowledge Graph (DKG) and NeuroWeb blockchain.

Built for the **DKG Global Hackathon 2025**, TruthGraph demonstrates the power of integrating:
- 🤖 **Agent Layer**: Autonomous AI agents (Google Gemini 2.0)
- 🕸️ **Knowledge Layer**: OriginTrail DKG with W3C-compliant Knowledge Assets
- 🛡️ **Trust Layer**: NeuroWeb parachain on Polkadot with on-chain attestations

---

## 🚀 Key Features

### Autonomous AI Agent
- **Google Gemini 2.0 Flash** integration for intelligent reasoning
- **ReAct pattern** implementation for transparent decision-making
- **Multi-tool orchestration** (hallucination detection, bias analysis, claim comparison)
- **Error recovery** and adaptive problem-solving

### Knowledge Graph Integration
- **OriginTrail DKG Edge Node** integration (✅ Hard Requirement)
- **JSON-LD Knowledge Assets** with W3C schema.org compliance
- **Verifiable provenance** with cryptographic signatures
- **Cross-chain discoverable** linked data

### Trust & Verification
- **NeuroWeb parachain** on Polkadot for immutable attestations
- **On-chain proof** of verification results
- **x402 micropayment** integration for sustainable monetization
- **Enterprise-grade security** with circuit breakers and retry logic

### Analysis Engines
- 🔍 **Hallucination Detector**: Identifies AI-generated false claims
- ⚖️ **Bias Analyzer**: Detects political and ideological bias
- 🔬 **Comparison Engine**: Cross-references claims for conflicts
- 📊 **Provenance Tracker**: Maintains verification chain

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      AGENT LAYER                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Autonomous AI Agent (Google Gemini 2.0)            │   │
│  │  • ReAct Pattern                                     │   │
│  │  • Multi-tool Orchestration                          │   │
│  │  • Adaptive Reasoning                                │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   KNOWLEDGE LAYER                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  OriginTrail DKG Edge Node                           │   │
│  │  • JSON-LD Knowledge Assets                          │   │
│  │  • W3C Semantic Web Standards                        │   │
│  │  • Verifiable Linked Data                            │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                     TRUST LAYER                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  NeuroWeb (Polkadot Parachain)                       │   │
│  │  • On-chain Attestations                             │   │
│  │  • Immutable Proof                                   │   │
│  │  • x402 Micropayments                                │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Tech Stack

### Backend
- **Python 3.11+** - Core application
- **FastAPI** - High-performance API framework
- **Uvicorn** - ASGI server
- **Google Generative AI** - Gemini 2.0 Flash integration
- **Pydantic 2.0** - Data validation
- **aiohttp** - Async HTTP client

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Vite** - Build tool

### Blockchain
- **OriginTrail DKG** - Decentralized Knowledge Graph
- **NeuroWeb** - Polkadot parachain
- **Substrate Interface** - Blockchain client
- **x402 Protocol** - Micropayments

---

## 🛠️ Installation

### Prerequisites
- Python 3.11 or higher
- Node.js 18 or higher
- Google AI API key ([Get it here](https://aistudio.google.com/app/api-keys))
- Git

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/dkg-engine.git
cd dkg-engine
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt
pip install -r modules/truthgraph/requirements.txt
pip install python-dotenv google-generativeai

# Create .env file
cat > .env << EOL
GOOGLE_API_KEY=your-google-api-key-here
DKG_NODE_ENDPOINT=http://localhost:8900
NEUROWEB_RPC_WS=wss://lofar-testnet.origin-trail.network
EOL

# Start backend server
python main.py
```

Backend will run on `http://localhost:8000`

### 3. Frontend Setup

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on `http://localhost:5173`

---

## 🎮 Usage

### Web Interface

1. Open `http://localhost:5173` in your browser
2. Enter a claim or question in the input field
3. Click "Run Verification"
4. Watch the agent reason through the verification process
5. View results with confidence scores and provenance

### Example Queries

**Claim Comparison:**
```
Compare: Earth is flat and Earth is spherical
```

**Hallucination Detection:**
```
Detect hallucinations in: The moon is made of cheese
```

**DKG Search:**
```
Search DKG for climate verification data
```

### API Endpoints

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Run Agent Verification
```bash
curl -X POST http://localhost:8000/agent/run \
  -H "Content-Type: application/json" \
  -d '{"goal": "Check if the earth is flat"}'
```

#### Compare Claims
```bash
curl -X POST http://localhost:8000/compare \
  -H "Content-Type: application/json" \
  -d '{
    "claim1": "Water boils at 100C",
    "claim2": "Water boils at 212F"
  }'
```

#### Detect Hallucinations
```bash
curl -X POST http://localhost:8000/hallucination \
  -H "Content-Type: application/json" \
  -d '{"text": "The Eiffel Tower is in London"}'
```

---

## 🏆 DKG Hackathon 2025 Requirements

### ✅ Completed Requirements

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| **DKG Edge Node** | ✅ Complete | Integrated via `dkg_client.py` and `dkg_publisher.py` |
| **Knowledge Assets** | ✅ Complete | JSON-LD with W3C schema.org in `knowledge_assets.py` |
| **NeuroWeb Integration** | ✅ Complete | On-chain attestations via `neuroweb_client.py` |
| **Polkadot Security** | ✅ Complete | NeuroWeb parachain integration |
| **x402 Micropayments** | ✅ Complete | Payment client in `x402/client.py` |
| **Agent Layer** | ✅ Complete | Autonomous AI agent with Gemini 2.0 |
| **Three-Layer Architecture** | ✅ Complete | Agent-Knowledge-Trust fully integrated |

### 📊 Judging Criteria Alignment

**Excellence & Innovation (20%)**
- First autonomous agent for DKG truth verification
- Novel three-layer integration
- Advanced multi-tool orchestration

**Technical Implementation (40%)**
- Enterprise-grade Python architecture
- Async/await patterns throughout
- Circuit breakers and retry logic
- Comprehensive error handling

**Impact & Relevance (20%)**
- Addresses AI misinformation crisis
- Real-world applications in journalism, governance, academia
- Scalable to multiple industries

**Ethics & Sustainability (10%)**
- Privacy-preserving design
- Open source (MIT License)
- x402 micropayments for sustainability
- Transparent decision-making

**Communication & Presentation (10%)**
- Clear documentation
- Interactive demo interface
- Comprehensive architecture diagrams

---

## 📁 Project Structure

```
dkg-engine/
├── backend/
│   ├── main.py                          # FastAPI application entry point
│   ├── requirements.txt                 # Python dependencies
│   ├── .env                             # Environment variables (create this)
│   └── modules/
│       └── truthgraph/
│           ├── agent/                   # Autonomous AI agent
│           │   ├── agent_core.py       # Main agent execution loop
│           │   ├── agent_planner.py    # Gemini 2.0 integration
│           │   ├── agent_memory.py     # Context management
│           │   └── agent_tools.py      # Tool orchestration
│           ├── dkg_client.py           # DKG query client
│           ├── dkg_publisher.py        # DKG publishing
│           ├── knowledge_assets.py     # JSON-LD schemas
│           ├── neuroweb_client.py      # NeuroWeb integration
│           ├── attestation_manager.py  # On-chain attestations
│           ├── comparison_engine.py    # Claim comparison
│           ├── hallucination_detector.py # AI hallucination detection
│           ├── bias_analyzer.py        # Bias detection
│           ├── x402/                   # Micropayment integration
│           │   ├── client.py
│           │   └── strategies.py
│           └── utils/                  # Utilities
│               ├── cache.py
│               ├── circuit_breaker.py
│               └── retry.py
├── frontend/
│   ├── src/
│   │   ├── App.tsx                     # Main React component
│   │   ├── components/                 # UI components
│   │   └── main.tsx                    # Entry point
│   ├── package.json
│   └── vite.config.ts
└── README.md                            # This file
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
# AI Configuration
GOOGLE_API_KEY=your-google-api-key-here

# DKG Configuration
DKG_NODE_ENDPOINT=http://localhost:8900
DKG_PRIVATE_KEY=your-dkg-private-key
DKG_PUBLISHER_ID=your-publisher-id

# NeuroWeb Configuration
NEUROWEB_RPC_WS=wss://lofar-testnet.origin-trail.network
NEUROWEB_RPC_HTTP=https://lofar-testnet.origin-trail.network
NEUROWEB_OPERATOR_SEED=your-seed-phrase

# Logging
LOG_LEVEL=INFO
LOG_JSON=true
```

### API Keys

**Google AI (Required):**
1. Visit [Google AI Studio](https://aistudio.google.com/app/api-keys)
2. Create a new API key
3. Add to `.env` as `GOOGLE_API_KEY`

**DKG Node (Optional for local testing):**
- Uses simulated responses if no DKG node is running
- Connect to real DKG node for production

---

## 🧪 Testing

### Run Backend Tests
```bash
cd backend
pytest modules/truthgraph/tests/
```

### Manual Testing
```bash
# Health check
curl http://localhost:8000/health

# Test agent
curl -X POST http://localhost:8000/agent/run \
  -H "Content-Type: application/json" \
  -d '{"goal": "Test verification"}'
```

---

## 📊 Knowledge Asset Example

Every verification creates a W3C-compliant Knowledge Asset:

```json
{
  "@context": {
    "@vocab": "https://schema.org/",
    "dkg": "https://dkg.origintrail.io/",
    "truthgraph": "https://truthgraph.ai/"
  },
  "@type": "truthgraph:ComparisonAsset",
  "@id": "dkg://comparison/uuid-abc123",
  "claim1": "The Earth is flat",
  "claim2": "The Earth is spherical",
  "similarity_score": 0.15,
  "conflict": true,
  "explanation": "Claims are contradictory",
  "confidence": 0.92,
  "creator": "TruthGraph Enterprise v1.0",
  "created": "2025-11-28T21:00:00Z",
  "verification_method": "Wikipedia + DKG cross-reference",
  "sources": [
    {
      "url": "https://en.wikipedia.org/wiki/Earth",
      "timestamp": "2025-11-28T21:00:00Z"
    }
  ]
}
```

---

## 🎬 Demo Video

Watch our 5-minute demo: [Link to YouTube/Vimeo]

**Demo Highlights:**
- Autonomous agent reasoning through complex claims
- Real-time tool orchestration
- Knowledge Asset creation
- NeuroWeb attestation flow
- x402 micropayment integration

---

## 🌟 Real-World Applications

### 📰 Journalism & Media
- Real-time fact-checking for news articles
- Automated source verification
- Combat misinformation at scale

### 🏛️ Governance & Policy
- Decentralized community notes
- Policy claim verification
- Transparent decision-making

### 🎓 Academic Research
- Automated peer review assistance
- Citation verification
- Research integrity protection

### 💼 Enterprise AI
- Corporate knowledge verification
- Compliance auditing
- AI output validation

---

## 🛣️ Roadmap

### Phase 1: Foundation (✅ Complete)
- [x] Core agent architecture
- [x] DKG integration
- [x] NeuroWeb attestations
- [x] Basic UI

### Phase 2: Enhancement (Q1 2025)
- [ ] Advanced NLP models
- [ ] Multi-language support
- [ ] Real-time collaboration
- [ ] Mobile app

### Phase 3: Scale (Q2 2025)
- [ ] Enterprise API
- [ ] Plugin ecosystem
- [ ] Cross-chain expansion
- [ ] Community governance

---

## 🤝 Contributing

We welcome contributions! This is an open-source project under MIT License.

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use TypeScript for frontend
- Write tests for new features
- Update documentation

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **OriginTrail** - For the Decentralized Knowledge Graph protocol
- **Polkadot** - For shared security infrastructure
- **NeuroWeb** - For the trust layer parachain
- **Google** - For Gemini AI models
- **DKG Hackathon 2025** - For the opportunity to build this solution

---

## 🔗 Links

- [DKG Global Hackathon 2025](https://dorahacks.io/hackathon/origintrail-scaling-trust-ai/)
- [OriginTrail Documentation](https://docs.origintrail.io/)
- [NeuroWeb Documentation](https://neuroweb.ai/)
- [Polkadot Documentation](https://wiki.polkadot.network/)
- [Google AI Studio](https://aistudio.google.com/)

---

<div align="center">


*Making AI trustworthy, one verification at a time.*

</div>
