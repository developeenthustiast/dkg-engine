# Architecture Overview

TruthGraph is built on a three-layer architecture designed to ensure the integrity, verifiability, and autonomy of AI-generated knowledge.

## The Triad

```mermaid
graph TD
    A[Autonomous Agent] -->|Publishes| K[Knowledge Layer (DKG)]
    A -->|Attests| T[Trust Layer (NeuroWeb)]
    K -->|Provides Context| A
    T -->|Verifies| A
    K <-->|Linked| T
```

### 1. Agent Layer (The Brain) 🧠
-   **Role**: Autonomous decision making, planning, and execution.
-   **Components**:
    -   `AgentCore`: Main ReAct loop.
    -   `AgentPlanner`: LLM-based reasoning engine.
    -   `AgentTools`: Interfaces for DKG, NeuroWeb, and Analysis Engines.
-   **Function**: It observes the world (Web/DKG), thinks about what needs verification, and acts (analyzes, publishes, attests).

### 2. Knowledge Layer (The Memory) 🕸️
-   **Role**: Decentralized storage of structured knowledge.
-   **Technology**: OriginTrail Decentralized Knowledge Graph (DKG).
-   **Components**:
    -   `DKGPublisher`: Publishes JSON-LD assets.
    -   `DKGQueryClient`: Retrieves assets via SPARQL/Graph queries.
-   **Function**: Stores the *content* of the analysis (e.g., "Claim X is 80% likely a hallucination") in a way that is machine-readable and interoperable.

### 3. Trust Layer (The Anchor) 🛡️
-   **Role**: Immutable verification and provenance.
-   **Technology**: NeuroWeb (Polkadot Parachain).
-   **Components**:
    -   `NeuroWebClient`: Submits transactions to the chain.
    -   `AttestationManager`: Creates cryptographic proofs (hashes).
-   **Function**: Stores the *proof* that the analysis happened at a specific time and hasn't been tampered with. It links the DKG UAL to a Blockchain Transaction Hash.

## Data Flow

1.  **Ingest**: Agent receives a claim (e.g., from a user or by monitoring the web).
2.  **Analyze**: Agent runs `HallucinationDetector` or `ComparisonEngine`.
3.  **Publish**: Result is published to DKG -> Returns `UAL`.
4.  **Attest**: `UAL` + `ResultHash` is submitted to NeuroWeb -> Returns `TxHash`.
5.  **Verify**: A third party can take the `UAL`, fetch the data, hash it, and check the `TxHash` on-chain to verify integrity.
