# TruthGraph Enterprise Integration with OriginTrail DKG

This directory contains the TruthGraph enterprise-grade truth verification system integrated with OriginTrail's Decentralized Knowledge Graph.

## Architecture

```
modules/truthgraph/
├── validators.py          # Pydantic validation models
├── exceptions.py          # Custom exception hierarchy
├── logging_config.py      # Structured JSON logging
├── config.py              # Environment configuration
├── engines/               # Analysis engines
│   ├── comparison_engine.py
│   ├── hallucination_detector.py
│   └── bias_analyzer.py
├── data_sources/          # Data source integrations
│   ├── wikipedia.py
│   └── dkg_client.py      # DKG Knowledge Asset client
└── utils/                 # Utility modules
    ├── circuit_breaker.py
    ├── retry.py
    └── cache.py
```

## Three-Layer Integration

### Agent Layer
- Autonomous AI agent for truth verification
- Decision-making using analysis engines
- Publishing verified results to DKG

### Knowledge Layer (DKG)
- OriginTrail DKG Edge Node
- Knowledge Assets with JSON-LD
- Verifiable, discoverable linked data

### Trust Layer (NeuroWeb/Polkadot)
- NeuroWeb parachain integration
- Cross-chain verification
- Polkadot shared security
- x402 micropayments

## Setup

1. Install Python dependencies:
```bash
pip install -r modules/truthgraph/requirements.txt
```

2. Configure environment variables in `.env`

3. Run DKG Node (see main README.md)

## Usage

```python
from modules.truthgraph.engines.comparison_engine import ComparisonEngine

engine = ComparisonEngine()
result = await engine.compare("Claim 1", "Claim 2")
```

## DKG Hackathon 2025

This implementation is designed for the DKG Global Hackathon 2025, demonstrating:
- ✅ Agent-Knowledge-Trust layer integration
- ✅ DKG Edge Node usage
- ✅ Knowledge Assets with JSON-LD
- ✅ NeuroWeb/Polkadot trust verification
- ✅ x402 micropayment integration
- ✅ Enterprise security standards

## License

MIT License - see LICENSE file
