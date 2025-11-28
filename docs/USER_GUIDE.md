# User Guide

## Running the Autonomous Agent

The core of TruthGraph is the Autonomous Agent. You can run it using the provided example script.

### Command
```bash
python examples/3_run_agent.py
```

### What Happens
1.  The agent initializes its Memory, Planner, and Tools.
2.  It receives a goal (defined in the script, e.g., "Verify claim X").
3.  It enters the **ReAct Loop**:
    -   **Thought**: It reasons about what to do.
    -   **Action**: It calls a tool (e.g., `search_web`, `detect_hallucinations`).
    -   **Observation**: It sees the result.
4.  If it finds a result, it automatically:
    -   **Publishes** to DKG.
    -   **Attests** on NeuroWeb.
5.  It returns the final answer.

## Using CLI Tools

You can also use the components individually in your own scripts.

### Publishing Knowledge
```python
from truthgraph.dkg_publisher import DKGPublisher

publisher = DKGPublisher()
result = await publisher.publish_comparison({...})
print(result['ual'])
```

### Verifying Trust
```python
from truthgraph.neuroweb_client import NeuroWebClient

client = NeuroWebClient()
is_valid = client.verify_attestation(tx_hash, ual, content_hash)
print(f"Verified: {is_valid}")
```

## Interpreting Results

-   **UAL (Unique Asset Locator)**: The ID of the data on the DKG (e.g., `did:dkg:otp:2043/...`).
-   **Tx Hash**: The transaction ID on the NeuroWeb blockchain.
-   **Trust Score**: A composite score (0.0 - 1.0) indicating how reliable the information is based on verification.
