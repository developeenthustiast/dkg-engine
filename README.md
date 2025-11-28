# TruthGraph 🕸️🧠🛡️

> **The Trust Layer for the AI Era.**
> *Winner of the OriginTrail DKG Global Hackathon 2025 (Target)*

TruthGraph is a decentralized system that integrates **AI Agents**, **Knowledge Graphs**, and **Blockchain Trust** to fight hallucinations and misinformation.

![Architecture](docs/images/architecture_diagram.png)

## 🚀 Key Features

-   **🧠 Autonomous AI Agent**: A "Brain" that independently verifies claims, detects hallucinations, and analyzes bias.
-   **🕸️ Knowledge Layer (DKG)**: Publishes analysis results as structured, interoperable Knowledge Assets on the OriginTrail DKG.
-   **🛡️ Trust Layer (NeuroWeb)**: Secures every analysis with an on-chain cryptographic attestation, ensuring provenance and immutability.
-   **💰 x402 Economy**: Built-in micropayments allow the agent to pay for premium data and monetize its own insights.

## 🏆 Hackathon Tracks

TruthGraph addresses multiple tracks:
-   **Grokpedia vs Wikipedia**: Real-time verification of AI knowledge.
-   **Decentralized Community Notes**: Automated, verifiable fact-checking.
-   **Social Graph Reputation**: Trust scores for information sources.

## ⚡ Quick Start

### Prerequisites
-   Python 3.9+
-   Node.js 16+ (for DKG Node)
-   OriginTrail DKG Node (running locally or remote)

### Installation

1.  **Clone the repo**
    ```bash
    git clone https://github.com/developeenthustiast/dkg-engine.git
    cd dkg-engine
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment**
    ```bash
    cp .env.example .env
    # Edit .env with your API keys and DKG config
    ```

4.  **Run the Agent**
    ```bash
    python examples/3_run_agent.py
    ```

## 📚 Documentation

-   [**Architecture**](docs/ARCHITECTURE.md): Deep dive into the Agent-Knowledge-Trust triad.
-   [**Setup Guide**](docs/SETUP.md): Detailed installation and configuration instructions.
-   [**User Guide**](docs/USER_GUIDE.md): How to use the CLI and Agent tools.
-   [**API Reference**](docs/API.md): Technical reference for developers.

## 🧪 Testing

Run the comprehensive test suite to verify system integrity:

```bash
pytest tests/
```

## 🏗️ Architecture Overview

TruthGraph operates on three layers:

1.  **Agent Layer**: The decision maker (Python/LLM).
2.  **Knowledge Layer**: The storage and query engine (OriginTrail DKG).
3.  **Trust Layer**: The verification anchor (NeuroWeb Parachain).

## 📜 License

MIT License. See [LICENSE](LICENSE) for details.
