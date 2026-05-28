# Builders API Reference

**CRITICAL**: This document covers the high-level Builder APIs that MUST be used in this project.
DO NOT create custom implementations of these patterns.

---

## Official Builder Imports

```python
from agent_framework import (
    # High-level Builders (MUST USE THESE)
    ConcurrentBuilder,       # Parallel execution
    GroupChatBuilder,        # Group chat orchestration
    HandoffBuilder,          # Agent handoff patterns
    MagenticBuilder,         # Magentic One style orchestration

    # WorkflowExecutor (MUST USE THIS)
    WorkflowExecutor,           # Nested workflow execution
    SubWorkflowRequestMessage,  # Sub-workflow requests
    SubWorkflowResponseMessage, # Sub-workflow responses

    # GroupChat Components
    GroupChatDirective,         # Group chat control
    ManagerSelectionResponse,   # Manager selection

    # Magentic Components
    MagenticManagerBase,        # Abstract manager base
    StandardMagenticManager,    # Default manager implementation
    MagenticContext,            # Manager context
)
```

---

## ConcurrentBuilder

For parallel agent execution with result aggregation.

```python
from agent_framework import ConcurrentBuilder

# CORRECT: Use official ConcurrentBuilder
workflow = (
    ConcurrentBuilder()
    .participants([agent1, agent2, agent3])
    .with_aggregator(summarizer_agent)
    .with_checkpointing(checkpoint_storage)
    .build()
)

# Execute
async for result in workflow.run("Analyze from multiple perspectives"):
    print(result)
```

**WRONG:**
```python
# ❌ DO NOT create custom concurrent execution
class MyConcurrentRunner:
    async def run_parallel(self, agents, input):
        tasks = [a.run(input) for a in agents]
        return await asyncio.gather(*tasks)
```

---

## GroupChatBuilder

For manager-directed multi-agent conversations.

```python
from agent_framework import GroupChatBuilder, ManagerSelectionResponse

# CORRECT: Use official GroupChatBuilder
workflow = (
    GroupChatBuilder()
    .participants(
        researcher=research_agent,
        writer=writer_agent,
        reviewer=reviewer_agent
    )
    .set_manager(manager_agent, display_name="Coordinator")
    .with_max_rounds(10)
    .with_termination_condition(my_condition)
    .with_checkpointing(storage)
    .build()
)

# Or with selection function
workflow = (
    GroupChatBuilder()
    .participants(researcher=agent1, writer=agent2)
    .set_select_speakers_func(my_selector_function)
    .build()
)
```

**WRONG:**
```python
# ❌ DO NOT create custom group chat orchestration
class _MockGroupChatWorkflow:
    def __init__(self, participants):
        self.participants = participants

    async def run(self, input):
        # Custom implementation...
```

---

## HandoffBuilder

For agent-to-agent handoff patterns.

```python
from agent_framework import HandoffBuilder

# CORRECT: Use official HandoffBuilder
workflow = (
    HandoffBuilder(name="support-handoff")
    .participants([triage_agent, billing_agent, technical_agent])
    .set_coordinator(coordinator_agent)
    .add_handoff(
        source="triage",
        targets=["billing", "technical"],
        condition=lambda ctx: ctx.category
    )
    .with_interaction_mode("human_in_loop")
    .build()
)
```

**WRONG:**
```python
# ❌ DO NOT create custom handoff logic
class HandoffController:
    def __init__(self):
        self.policies = {}

    async def execute_handoff(self, from_agent, to_agent):
        # Custom implementation...
```

---

## MagenticBuilder

For Magentic One style orchestration with planning and progress tracking.

```python
from agent_framework import (
    MagenticBuilder,
    MagenticManagerBase,
    StandardMagenticManager,
)

# CORRECT: Use official MagenticBuilder with StandardMagenticManager
workflow = (
    MagenticBuilder()
    .participants(
        researcher=research_agent,
        coder=coding_agent,
        writer=writing_agent
    )
    .with_standard_manager(
        agent=manager_agent,
        max_round_count=20,
        max_stall_count=3
    )
    .with_plan_review(enable=True)
    .with_checkpointing(storage)
    .build()
)

# Or extend official MagenticManagerBase
class CustomManager(MagenticManagerBase):  # ✅ Extend official base
    async def plan(self, context: MagenticContext) -> ChatMessage:
        # Custom planning logic
        ...
```

**WRONG:**
```python
# ❌ DO NOT create custom manager base classes
class MagenticManagerBase(ABC):  # Custom implementation
    @abstractmethod
    async def plan(self, context):
        ...

class StandardMagenticManager(MagenticManagerBase):  # Custom implementation
    ...
```

---

## WorkflowExecutor

For nested workflow execution (sub-workflows).

```python
from agent_framework import (
    WorkflowExecutor,
    SubWorkflowRequestMessage,
    SubWorkflowResponseMessage,
)

# CORRECT: Use or extend official WorkflowExecutor
executor = WorkflowExecutor(
    workflow=my_sub_workflow,
    id="sub-workflow-executor",
    allow_direct_output=False
)

# In parent workflow
workflow = Workflow(
    executors=[main_executor, executor],
    edges=[
        Edge(source="main", target=executor),
        Edge(source=executor, target="output"),
    ]
)

# Or extend for custom behavior
class ExtendedWorkflowExecutor(WorkflowExecutor):  # ✅ Extend official
    def __init__(self, workflow, id, **kwargs):
        super().__init__(workflow=workflow, id=id, **kwargs)
        # Add custom configuration
```

**WRONG:**
```python
# ❌ DO NOT create custom workflow executor
class WorkflowExecutorAdapter:
    def __init__(self, workflow, id):
        self.workflow = workflow  # Missing super().__init__
        self.id = id

    async def process_workflow(self, input):
        # Custom implementation without using official API
```

---

## Adapter Pattern (IPA Platform)

When extending official builders for IPA Platform, use this pattern:

```python
from agent_framework import OfficialBuilder

class BuilderAdapter:
    """IPA Platform adapter for OfficialBuilder."""

    def __init__(self, **kwargs):
        # MUST: Create official builder instance
        self._builder = OfficialBuilder()

        # OK: Add IPA-specific configuration
        self._ipa_config = kwargs

    def participants(self, agents):
        # MUST: Delegate to official builder
        self._builder.participants(agents)
        return self

    def build(self):
        # MUST: Call official builder's build()
        workflow = self._builder.build()

        # OK: Wrap with IPA-specific enhancements
        return self._wrap_workflow(workflow)
```

---

## Verification

Always run the verification script after implementing builders:

```bash
cd backend
python scripts/verify_official_api_usage.py
```

Expected output: `5/5 checks passed`

### What the script checks:

1. ✅ `from agent_framework import ConcurrentBuilder`
2. ✅ `from agent_framework import HandoffBuilder`
3. ✅ `from agent_framework import GroupChatBuilder`
4. ✅ `from agent_framework import MagenticBuilder`
5. ✅ `from agent_framework import WorkflowExecutor`

---

## Quick Reference

| Need | Use This | NOT This |
|------|----------|----------|
| Parallel execution | `ConcurrentBuilder` | Custom parallel runner |
| Group conversation | `GroupChatBuilder` | Custom group chat class |
| Agent handoff | `HandoffBuilder` | Custom handoff controller |
| Magentic orchestration | `MagenticBuilder` | Custom magentic manager |
| Nested workflows | `WorkflowExecutor` | Custom workflow executor |
| Manager base class | `MagenticManagerBase` (import) | Custom ABC definition |
| Standard manager | `StandardMagenticManager` (import) | Custom implementation |
