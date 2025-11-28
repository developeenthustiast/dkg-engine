# Setup Guide

## Prerequisites

Before running TruthGraph, ensure you have the following installed:

1.  **Python 3.9+**: [Download Python](https://www.python.org/downloads/)
2.  **Node.js 16+**: [Download Node.js](https://nodejs.org/) (Required for DKG Node)
3.  **Git**: [Download Git](https://git-scm.com/)

## Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/developeenthustiast/dkg-engine.git
    cd dkg-engine
    ```

2.  **Create Virtual Environment** (Recommended)
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Python Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  **Environment Variables**
    Copy the example file:
    ```bash
    cp .env.example .env
    ```

    Edit `.env` with your details:
    -   `OPENAI_API_KEY`: Required for the Agent Planner (LLM).
    -   `NEUROWEB_RPC_WS`: WebSocket endpoint for NeuroWeb (default provided).
    -   `NEUROWEB_OPERATOR_SEED`: Your wallet seed for signing attestations (Testnet).
    -   `DKG_ENVIRONMENT`: `testnet` or `mainnet`.

2.  **DKG Node**
    Ensure your local DKG node is running or you have access to a remote node.
    -   Default endpoint: `http://localhost:8900`

## Verification

Run the test suite to ensure everything is set up correctly:

```bash
pytest tests/
```

If all tests pass, you are ready to run the agent!
