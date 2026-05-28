# API Reference

## Core Modules

### Protocol (`mcp_b.protocol`)

- `MCBMessage` - Message container
- `MCBAgent` - Agent representation
- `MCBProtocol` - Protocol handler
- `encode_mcb()` - Encode messages
- `decode_mcb()` - Decode messages

### AMUM (`mcp_b.amum`)

- `AMUM` - Alignment manager
- `AMUMSession` - Session state
- `quick_alignment()` - One-liner alignment

### QCI (`mcp_b.qci`)

- `QCI` - Coherence tracker
- `QCIState` - Agent state
- `BreathingCycle` - Sync states

### ETHIC (`mcp_b.ethic`)

- `ETHIC` - Ethics enforcer
- `EthicPrinciple` - Principle definition
- `check_ethical()` - Compliance check

### Workflow (`mcp_b.workflow`)

- `Workflow` - Workflow instance
- `WorkflowTemplate` - Template definition
- `WorkflowEngine` - Engine manager
- `start_workflow()` - Start new workflow

### Utils (`mcp_b.utils`)

- `timed_cache` - TTL cache decorator
- `memoize_method` - Method memoization
- `batch_operation` - Batch processing
- `lazy_property` - Lazy evaluation

## Full API

For complete API documentation, see the source code docstrings or run:

```bash
pip install sphinx sphinx-autodoc-typehints
sphinx-apidoc -o docs/api src/mcp_b
```
