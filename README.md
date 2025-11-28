# TruthGraph 🕸️🧠🛡️

> **The Trust Layer for the AI Era.**

I built **TruthGraph** to address a critical problem in the age of Generative AI: **Hallucinations and Misinformation**.

As AI agents become more autonomous, they need a way to verify information and establish trust without relying on centralized authorities. TruthGraph provides this by integrating three powerful technologies:

1.  **Autonomous AI Agents** (The Brain)
2.  **Decentralized Knowledge Graphs** (The Memory)
3.  **Blockchain Trust Layers** (The Anchor)

This project was developed for the **OriginTrail DKG Global Hackathon 2025**.

![Architecture](docs/images/architecture_diagram.png)

## 🚀 Key Features

-   **🧠 Autonomous Verification**: My agent doesn't just chat; it actively verifies claims, detects hallucinations, and cross-references data against the DKG.
-   **🕸️ structured Knowledge**: Instead of ephemeral text, analysis results are published as permanent, interoperable Knowledge Assets on the OriginTrail DKG.
-   **🛡️ On-Chain Trust**: Every piece of knowledge is cryptographically attested on the NeuroWeb parachain. If the data changes, the hash won't match.
-   **💰 Knowledge Economy**: I've implemented the **x402** protocol, allowing the agent to autonomously pay for premium data and monetize its own high-quality insights.

## 🏆 Hackathon Challenge: Decentralized Community Notes

**This project is submitted for the "Decentralized Community Notes" challenge.**

### How It Addresses the Challenge
-   **AI-Powered Fact-Checking**: Extends the concept of community notes by using an Autonomous Agent to instantly verify claims against the DKG and external sources.
-   **Verifiable Provenance**: Every "Note" (Analysis Result) is published as a DKG Knowledge Asset with an on-chain NeuroWeb attestation.
-   **Structured Knowledge**: We use strict JSON-LD schemas to ensure our notes are interoperable and machine-readable.

### Bonus Features
-   **✅ x402 Micropayments Implemented**: We have fully implemented the **x402 (HTTP 402)** protocol. The agent can autonomously pay for premium data or monetize its own fact-checking reports. (See `modules/truthgraph/x402/` and `examples/3_run_agent.py`).
-   **✅ Tokenomics Ready**: The system is designed to support staking/slashing based on the Trust Score calculated by the agent.

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
-   [**JSON-LD Example**](examples/example_note.jsonld): See a sample Knowledge Asset structure.
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
