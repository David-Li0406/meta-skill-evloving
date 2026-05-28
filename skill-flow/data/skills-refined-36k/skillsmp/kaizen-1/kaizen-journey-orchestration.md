# Journey Orchestration (Layer 5)

> **Version**: v0.9.0
> **Priority**: HIGH
> **Status**: Production-Ready

## Overview

Journey Orchestration is Kaizen's Layer 5 capability for declarative user journey management. It enables multi-pathway navigation with intent-driven transitions and cross-pathway context accumulation.

## Key Concepts

### 5-Layer Kaizen Architecture

```
Layer 5: Journey Orchestration  ← THIS LAYER
         ↓ orchestrates
Layer 4: Multi-Agent Pipelines (Ensemble, Router, Supervisor-Worker)
         ↓ coordinates
Layer 3: BaseAgent (single agent execution)
         ↓ uses
Layer 2: Signature (type-safe I/O with __intent__, __guidelines__)
         ↓ runs on
Layer 1: Kailash Core SDK (workflows, nodes, runtime)
```

### Journey vs Pathway

- **Journey**: Complete user flow (e.g., healthcare referral journey)
- **Pathway**: Single phase within a journey (e.g., intake, booking, confirmation)
- **Transition**: Rule for switching between pathways (e.g., FAQ intent triggers FAQ pathway)

## Quick Start

### Define a Journey

```python
from kaizen.journey import (
    Journey, Pathway, Transition, IntentTrigger,
    JourneyConfig, ReturnToPrevious
)
from kaizen.signatures import Signature, InputField, OutputField


# 1. Define Signatures with Layer 2 enhancements
class IntakeSignature(Signature):
    """Collect patient information."""

    __intent__ = "Gather symptoms and preferences for specialist referral"
    __guidelines__ = [
        "Ask about symptoms before demographics",
        "Use empathetic, non-clinical language"
    ]

    message: str = InputField(desc="Patient message")
    symptoms: list = OutputField(desc="Extracted symptoms")
    preferences: dict = OutputField(desc="Patient preferences")


class BookingSignature(Signature):
    """Handle doctor booking."""

    __intent__ = "Match patients with appropriate specialists"
    __guidelines__ = [
        "Present at most 3 options",
        "Never suggest rejected doctors"
    ]

    message: str = InputField(desc="Booking message")
    selected_doctor: dict = OutputField(desc="Selected doctor")


# 2. Define Journey with nested Pathways
class PatientJourney(Journey):
    __entry_pathway__ = "intake"

    # Global transitions (checked from any pathway)
    __transitions__ = [
        Transition(
            trigger=IntentTrigger(
                intents=["faq", "question", "help"],
                description="User has a question"
            ),
            to_pathway="faq",
            preserve_context=True
        )
    ]

    # Nested Pathway classes
    class IntakePath(Pathway):
        __signature__ = IntakeSignature
        __agents__ = ["intake_agent"]
        __accumulate__ = ["symptoms", "preferences"]
        __next__ = "booking"

    class BookingPath(Pathway):
        __signature__ = BookingSignature
        __agents__ = ["booking_agent"]
        __accumulate__ = ["selected_doctor", "rejected_doctors"]
        __next__ = "confirmation"

    class FAQPath(Pathway):
        __signature__ = FAQSignature
        __agents__ = ["faq_agent"]
        __return_behavior__ = ReturnToPrevious()  # Returns to previous pathway


# 3. Run the Journey
async def main():
    config = JourneyConfig(
        intent_detection_model="gpt-4o-mini",
        intent_confidence_threshold=0.75
    )

    journey = PatientJourney(session_id="patient-123", config=config)

    # Register agents
    journey.manager.register_agent("intake_agent", intake_agent)
    journey.manager.register_agent("booking_agent", booking_agent)
    journey.manager.register_agent("faq_agent", faq_agent)

    # Start session
    session = await journey.start()

    # Process messages
    response = await journey.process_message("I have back pain")
    print(f"Response: {response.message}")
    print(f"Pathway: {response.pathway_id}")
    print(f"Context: {response.accumulated_context}")
```

## Core Components

### Journey Class

```python
from kaizen.journey import Journey, Pathway

class MyJourney(Journey):
    __entry_pathway__ = "start"       # Required: First pathway
    __transitions__ = [...]           # Optional: Global transitions

    class StartPath(Pathway):
        __signature__ = StartSignature
        __agents__ = ["start_agent"]
        __next__ = "finish"           # Next pathway

    class FinishPath(Pathway):
        __signature__ = FinishSignature
        __agents__ = ["finish_agent"]
        # No __next__ = terminal pathway
```

### Pathway Configuration

| Attribute | Type | Description |
|-----------|------|-------------|
| `__signature__` | Type[Signature] | Type-safe I/O contract |
| `__agents__` | List[str] | Agent IDs to execute |
| `__pipeline__` | str | Pipeline pattern: "sequential", "parallel", "router", "ensemble" |
| `__accumulate__` | List[str] | Fields to persist across pathways |
| `__next__` | str | Default next pathway |
| `__guidelines__` | List[str] | Additional guidelines (merged with signature) |
| `__return_behavior__` | ReturnBehavior | ReturnToPrevious or ReturnToSpecific |

### Transitions

```python
from kaizen.journey import Transition, IntentTrigger, ConditionTrigger

# Intent-based (LLM-powered)
Transition(
    trigger=IntentTrigger(
        intents=["help", "faq", "question"],
        description="User needs help"
    ),
    to_pathway="faq"
)

# Condition-based (context check)
Transition(
    trigger=ConditionTrigger(
        condition=lambda ctx: ctx.get("retry_count", 0) >= 3,
        description="Too many retries"
    ),
    to_pathway="escalation"
)
```

### Context Accumulation

```python
from kaizen.journey import ContextAccumulator, MergeStrategy

# Configure merge strategies per field
accumulator = ContextAccumulator(config)
accumulator.configure_field("rejected_doctors", MergeStrategy.APPEND)
accumulator.configure_field("preferences", MergeStrategy.MERGE_DICT)
accumulator.configure_field("total_attempts", MergeStrategy.SUM)
```

**Available Strategies:**
- `REPLACE` (default): New value replaces old
- `APPEND`: Append to list
- `MERGE_DICT`: Merge dictionaries
- `MAX`/`MIN`: Keep maximum/minimum value
- `SUM`: Sum numeric values
- `UNION`: Set union for lists

### Return Behaviors

```python
from kaizen.journey import ReturnToPrevious, ReturnToSpecific

# FAQ detour - returns to previous pathway
class FAQPath(Pathway):
    __return_behavior__ = ReturnToPrevious(preserve_context=True)

# Error handling - returns to specific pathway
class ErrorPath(Pathway):
    __return_behavior__ = ReturnToSpecific(target_pathway="intake")
```

## Nexus Deployment

Deploy journeys via Nexus for API/CLI/MCP access:

```python
from kaizen.journey.nexus import JourneyNexusAdapter, deploy_journey_to_nexus
from nexus import Nexus

# Create adapter
adapter = JourneyNexusAdapter(
    journey_class=PatientJourney,
    agents={
        "intake_agent": intake_agent,
        "booking_agent": booking_agent,
        "faq_agent": faq_agent
    }
)

# Deploy to Nexus
nexus = Nexus(title="Healthcare Platform", enable_api=True)
deploy_journey_to_nexus(nexus, adapter, "patient_journey")
nexus.run()

# Access via:
# - API: POST /workflows/patient_journey {"session_id": "...", "message": "..."}
# - CLI: nexus run patient_journey --session-id=... --message="..."
```

## Hooks System

```python
from kaizen.journey import PathwayManager, JourneyHookEvent

manager = PathwayManager(journey, session_id, config)

# Register hooks
@manager.register_hook(JourneyHookEvent.POST_PATHWAY_EXECUTE)
async def log_pathway(context):
    print(f"Executed: {context.pathway_id}")
    return {"logged": True}

@manager.register_hook(JourneyHookEvent.POST_TRANSITION)
async def track_transition(context):
    print(f"Transitioned to: {context.to_pathway}")
```

**Available Events:**
- `PRE_SESSION_START`, `POST_SESSION_START`
- `PRE_PATHWAY_EXECUTE`, `POST_PATHWAY_EXECUTE`
- `PRE_TRANSITION`, `POST_TRANSITION`
- `SESSION_RESTORED`, `SESSION_COMPLETE`
- `SESSION_ERROR`, `CONTEXT_ACCUMULATED`

## Healthcare Example

Complete reference implementation:

```
apps/kailash-kaizen/examples/journey/healthcare_referral/
├── journey.py          # 5 pathways, 3 transitions
├── signatures/         # 5 signatures with __intent__, __guidelines__
├── agents/             # 5 agents (intake, booking, faq, persuasion, confirmation)
├── tests/              # Unit, integration, E2E tests
└── README.md           # Usage guide
```

Run the demo:
```bash
cd apps/kailash-kaizen
python -m examples.journey.healthcare_referral.main --mode demo
```

## Testing

```python
import pytest
from kaizen.journey import Journey, Pathway, JourneyConfig


class TestMyJourney:
    def test_journey_extracts_pathways(self):
        assert "intake" in MyJourney._pathways
        assert "booking" in MyJourney._pathways

    def test_entry_pathway(self):
        assert MyJourney._entry_pathway == "intake"

    @pytest.mark.asyncio
    async def test_process_message(self, mock_agents):
        journey = MyJourney("test", JourneyConfig())
        journey.manager.register_agent("intake_agent", mock_agents["intake"])

        await journey.start()
        response = await journey.process_message("Hello")

        assert response.pathway_id == "intake"
```

## Configuration

```python
from kaizen.journey import JourneyConfig

config = JourneyConfig(
    # Intent Detection
    intent_detection_model="gpt-4o-mini",    # LLM for intent classification
    intent_confidence_threshold=0.75,         # Minimum confidence
    intent_cache_ttl_seconds=300,             # Cache TTL

    # Pathway Execution
    max_pathway_depth=15,                     # Max stack depth
    pathway_timeout_seconds=60.0,             # Timeout per pathway

    # Context
    max_context_size_bytes=512 * 1024,        # 512KB limit
    context_persistence="dataflow",           # "memory", "dataflow"

    # Error Handling
    error_recovery="graceful",                # "fail_fast", "graceful", "retry"
    max_retries=3
)
```

## Common Patterns

### Pattern 1: Detour and Return
```python
class MyJourney(Journey):
    __transitions__ = [
        Transition(
            trigger=IntentTrigger(["help"]),
            to_pathway="help"
        )
    ]

    class HelpPath(Pathway):
        __return_behavior__ = ReturnToPrevious()  # Back to previous
```

### Pattern 2: Conditional Escalation
```python
class MyJourney(Journey):
    __transitions__ = [
        Transition(
            trigger=ConditionTrigger(
                condition=lambda ctx: ctx.get("failures", 0) > 3
            ),
            to_pathway="human_handoff"
        )
    ]
```

### Pattern 3: Context-Aware Booking
```python
class BookingPath(Pathway):
    __accumulate__ = ["rejected_doctors"]  # Track rejections

    # Booking agent sees rejected_doctors in context
    # and excludes them from suggestions
```

## Related Skills

- **[kaizen-signatures.md](kaizen-signatures.md)** - Layer 2 Signatures with __intent__, __guidelines__
- **[kaizen-supervisor-worker.md](kaizen-supervisor-worker.md)** - Layer 4 multi-agent patterns
- **[kaizen-baseagent-quick.md](kaizen-baseagent-quick.md)** - Layer 3 BaseAgent

## Files Reference

| File | Description |
|------|-------------|
| `kaizen/journey/__init__.py` | Public exports |
| `kaizen/journey/core.py` | Journey, Pathway, metaclasses |
| `kaizen/journey/transitions.py` | Transition, triggers |
| `kaizen/journey/intent.py` | IntentDetector, caching |
| `kaizen/journey/manager.py` | PathwayManager |
| `kaizen/journey/context.py` | ContextAccumulator |
| `kaizen/journey/state.py` | StateManager, backends |
| `kaizen/journey/nexus.py` | Nexus integration |
| `kaizen/journey/behaviors.py` | Return behaviors |
| `kaizen/journey/errors.py` | Journey exceptions |
