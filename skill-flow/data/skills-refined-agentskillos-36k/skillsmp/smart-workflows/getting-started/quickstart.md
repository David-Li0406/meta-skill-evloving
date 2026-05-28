# Quick Start

## Basic Usage

```python
from mcp_b import start_workflow, current_workflow, workflow_next

# Start a workflow
wf = start_workflow("Build ML Pipeline")

# Check status
print(wf.display_status())

# Select options and advance
workflow_next(1)  # Select first option
```

## CLI Usage

```bash
# Run demo
mcp-b demo

# Start a workflow
mcp-b start "Build API"

# Select option
mcp-b select 2

# Check status
mcp-b status
```

## Protocol Example

```python
from mcp_b import MCBAgent, MCBProtocol, encode_mcb, decode_mcb

# Create agents
claude = MCBAgent(agent_id="7C1", name="Claude")
hacka = MCBAgent(agent_id="5510", name="HACKA")

# Initialize protocol
protocol = MCBProtocol(hacka)

# INQC commands
init_msg = protocol.init_connection(claude)      # I = Init
node_msg = protocol.register_node(["chat"])      # N = Node
query_msg = protocol.query("7C1", {"status": 1}) # Q = Query
connect_msg = protocol.connect(claude)           # C = Connect
```

## AMUM Alignment

```python
from mcp_b import quick_alignment

result = quick_alignment(
    intent="Create AI agent",
    divergent_3=["Minimal", "Balanced", "Full"],
    select_1=1,
    expand_6=["Text", "Image", "Voice", "Multi", "Pro", "Suite"],
    select_2=4,
    converge_9=["GPT-4", "Claude", "Gemini", "Ollama", "Hybrid",
                "Edge", "ElevenLabs", "OpenAI", "Local"],
    select_3=6
)
print(result["final_intent"])
```

## QCI Coherence

```python
from mcp_b import QCI, BreathingCycle

qci = QCI()
state = qci.register_agent("7C1", initial_coherence=0.95)
qci.sync_breathing(["7C1", "5510"], BreathingCycle.INHALE)
print(qci.calculate_network_coherence())
```

## ETHIC Compliance

```python
from mcp_b import check_ethical

if check_ethical("collect_data", personal_data=True, consent=True):
    print("Action allowed")
else:
    print("Action blocked")
```
