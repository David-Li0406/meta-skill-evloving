---
name: gutters-system-integration
description: Critical checklist for any new feature/module in GUTTERS. Ensures all integration points are wired - Genesis, StateTracker, EventBus, Observability. Use BEFORE starting any implementation.
---

# GUTTERS System Integration Checklist

Every feature in GUTTERS must integrate with these systems. This is NOT optional.

## Integration Matrix

| System | When to Integrate | Files to Touch |
|--------|-------------------|----------------|
| **ModuleRegistry** | Any module that calculates or synthesizes | Auto-registered via `BaseModule` |
| **Genesis** | Any data that may be uncertain/incomplete | `genesis/declarations/`, engine subscriptions |
| **Active Memory** | Performance-critical data (synthesis, outputs) | `core/memory/active_memory.py` |
| **StateTracker** | Any data that affects profile completion | `core/state/tracker.py` |
| **EventBus** | Any action other modules might react to | `protocol/events.py`, `protocol/payloads.py` |
| **ActivityLogger** | Any LLM call or significant operation | `log_activity()` calls |
| **Chat System** | Any feature needing conversation presence | `SessionManager`, `ChatSession` |
| **Vector Index** | Any module with searchable history | `vector/embedding_service.py` |
| **Observability** | Any dashboard visibility | `api/v1/observability.py` |
| **Generative UI** | Any custom user interaction | `generative_ui/models.py`, `chat.py` |

---

## 1. Chat System Integration (The Cognitive Interface)

**Ask:** Does this feature involve user interaction, data gathering via dialogue, or automated status reporting?

**If YES, you MUST coordinate with the Master/Branch architecture:**

1.  **Master Chat Presence:** High-level status updates or refinement probes (Genesis) should target the user's singleton Master Chat.
2.  **Workspaces (Branches):** Intensive, topic-specific work (Deep Journaling, Nutrition Planning) should occur in a dedicated Branch session.
3.  **Memory Toggles:** Decide if the session should contribute to the user's permanent profile (`contribute_to_memory=True`).
4.  **Trace Metadata:** Store thinking steps, tool outputs, and LLM internal reasoning in `ChatMessage.meta` for Phase 7b observability.

```python
from src.app.modules.features.chat.session_manager import SessionManager

manager = SessionManager()

# Get the persistent UI presence
master = await manager.get_or_create_master_session(user_id, db)

# Or create a dedicated topic branch
branch = await manager.create_branch_session(
    user_id=user_id,
    session_type="nutrition",
    name="Meal Planning Week 4",
    contribute_to_memory=True,
    db=db
)
```

---

## 1. Genesis Integration (Uncertainty Handling)

**Ask:** Does this feature produce data that could be uncertain (missing birth time, incomplete input)?

**If YES, you MUST:**
```python
# 1. Create uncertainty extractor
# File: modules/intelligence/genesis/declarations/{module}.py
class {Module}UncertaintyExtractor:
    module_name = "{module}"
    
    async def extract(self, results: dict, user_id: int) -> UncertaintyDeclaration | None:
        if results.get("accuracy") == "probabilistic":
            return UncertaintyDeclaration(
                module=self.module_name,
                fields=[UncertaintyField(
                    field="{field_name}",
                    candidates=results["probabilities"],
                    refinement_strategies=["{strategy1}", "{strategy2}"]
                )]
            )

# 2. Register extractor
# File: modules/intelligence/genesis/registry.py
UncertaintyRegistry.register_extractor({Module}UncertaintyExtractor())

# 3. Create refinement strategies
# File: modules/intelligence/genesis/strategies/{module}.py
class {Strategy}Strategy:
    strategy_name = "{strategy_name}"
    applicable_fields = ["{field}"]
    probe_type = ProbeType.BINARY_CHOICE
    
    def generate_prompt(self, hypothesis: Hypothesis) -> str:
        ...

# 4. Register strategies
# File: modules/intelligence/genesis/strategies/__init__.py
StrategyRegistry.register({Strategy}Strategy())

# 5. Create refinement handler
# File: modules/calculation/{module}/refinement/__init__.py
async def handle_{field}_confirmed(user_id: int, confirmed_value: str, confidence: float):
    # Recalculate with confirmed value
    ...
```

---

## 2. ModuleRegistry Integration (Auto-Discovery)

**Ask:** Is this a module that calculates or synthesizes user data?

**If YES, auto-registration happens automatically:**
```python
# In BaseModule.__init__ (already implemented):
if self.name:
    from src.app.modules.registry import ModuleRegistry
    ModuleRegistry.register(self)
```

**Intelligence modules consume registry:**
```python
from src.app.modules.registry import ModuleRegistry

# Get modules with calculated data for user
calculated = await ModuleRegistry.get_calculated_modules_for_user(user_id, db)

# Get specific module data
astro_data = await ModuleRegistry.get_user_profile_data(user_id, db, "astrology")

# Filter by layer
calc_modules = ModuleRegistry.get_all_calculation_modules()
intel_modules = ModuleRegistry.get_all_intelligence_modules()
```

---

## 3. StateTracker Integration (Profile State)

**Ask:** Does this feature affect what the user's profile "completeness" looks like?

**If YES, you MUST:**
```python
# 1. Add to domain tracking
# File: core/state/tracker.py - PROFILE_DOMAINS dict
PROFILE_DOMAINS = {
    "{module_name}": {
        "required_fields": ["{field1}", "{field2}"],
        "weight": 0.6,  # Importance relative to other domains
    },
}

# 2. Add custom tracking methods if needed
class StateTracker:
    async def update_{feature}_status(self, user_id: int, ...):
        # Custom tracking logic
```

---

## 4. EventBus Integration (Module Communication)

**Ask:** Should other modules react when this feature does something?

**If YES, you MUST:**
```python
# 1. Define event constant
# File: protocol/events.py
{MODULE}_{ACTION} = "{module}.{entity}.{action}"

# 2. Create typed payload
# File: protocol/payloads.py
class {Module}{Action}Payload(BaseModel):
    user_id: int
    # Specific fields

# 3. Publish event
await event_bus.publish(
    event_type={MODULE}_{ACTION},
    payload=payload.model_dump(),
    source="{module}.{component}",
    user_id=str(user_id),
)

# 4. Subscribe where needed
# In other modules' initialize():
event_bus.subscribe({MODULE}_{ACTION}, self.handle_{action})
```

---

## 5. ActivityLogger Integration (Observability)

**Ask:** Does this feature make LLM calls or do significant operations users should see?

**If YES, you MUST:**
```python
from app.core.activity.logger import get_activity_logger

# For LLM calls
logger = get_activity_logger()
await logger.log_llm_call(
    trace_id=trace_id,
    model_id=model_id,
    prompt=prompt,
    response=response,
    cost_aud=cost_aud, # 🆕 MANDATORY: Log AUD cost for user transparency
)

# For general activities
await logger.log_activity(
    trace_id=trace_id,
    agent="{module}.{component}",
    activity_type="{action}",
    details={...}
)
```

# 6. Active Memory Integration (Caching)

**Ask:** Does this module produce data needed for real-time conversation or dashboard display?

**If YES, you MUST:**
```python
from app.core.memory.active_memory import get_active_memory

memory = get_active_memory()

# 1. Warm Memory: Cache module output immediately after calculation
await memory.set_module_output(user_id, "{module}", data)

# 2. Hot Memory: Trigger synthesis if this changes the user's core profile
from app.core.memory.synthesis_orchestrator import get_orchestrator, SynthesisTrigger
orchestrator = get_orchestrator()
await orchestrator.trigger_synthesis(user_id, SynthesisTrigger.MODULE_DATA_UPDATED)
```

---

## 7. API Endpoint Integration

**Ask:** Does this feature need user-facing endpoints?

**If YES, you MUST:**
```python
# 1. Create router
# File: api/v1/{feature}.py
router = APIRouter(prefix="/{feature}", tags=["{feature}"])

# 2. Register in api/v1/__init__.py
from .{feature} import router as {feature}_router
router.include_router({feature}_router)

# 3. Add observability endpoint if tracking data
# File: api/v1/observability.py
@router.get("/{feature}-activity/{user_id}")
async def get_{feature}_activity(user_id: int):
    ...
```

---

## 8. Generative UI Integration (Interactive Components)

**Ask:** Does this feature need structured input from the user beyond text?

**If YES, you MUST:**
```python
# 1. Define Component Model
# File: modules/intelligence/generative_ui/models.py
class {My}ComponentSpec(BaseModel):
    options: List[str]

# 2. Add to ComponentType
# File: modules/intelligence/generative_ui/models.py - ComponentType Enum
MY_COMPONENT = "my_component"

# 3. Add Generation Logic
# File: modules/intelligence/generative_ui/generator.py
async def generate_my_component(...):
    return ComponentSpec(component_type=ComponentType.MY_COMPONENT, ...)

# 4. Handle Submission in API
# File: api/v1/chat.py - submit_component_response
elif response.component_type == ComponentType.MY_COMPONENT:
    # Store data
    # Publish event
    await event_bus.publish("my.component.submitted", ...)
```

---

## Pre-Implementation Checklist

Before writing any code, answer these:

- [ ] **Genesis:** Will any output be uncertain? → Create extractor + strategies
- [ ] **StateTracker:** Does this affect profile completion? → Update domains
- [ ] **EventBus:** Should other modules react? → Define events + payloads
- [ ] **ActivityLogger:** Are there LLM calls? → Set tier (Premium/Standard) + Log AUD cost
- [ ] **Observability:** Should users see this in dashboard? → Add endpoints
- [ ] **Active Memory:** Is data pushed to warm/hot layers? → Update cache
- [ ] **Vector Index:** Should this content be semantically searchable? → Seed embeddings
- [ ] **High-Fidelity Tests:** Real DB + Redis test created? → No mocks!

---

## Common Integration Patterns

### New Calculation Module
1. Inherit `BaseModule`
2. Load config from database
3. Subscribe to `USER_BIRTH_DATA_UPDATED`
4. Publish `MODULE_PROFILE_CALCULATED`
5. Create Genesis uncertainty extractor
6. Add to StateTracker domains
7. Contribute to synthesis

### New Intelligence Module
1. Inherit `BaseModule`
2. Subscribe to relevant events
3. Add activity logging for LLM calls
4. Create observability endpoint
5. Integrate with Genesis if produces uncertainties

### New API Feature
1. Create router + register in `src/app/api/v1/__init__.py`
2. Use existing auth dependencies (`get_current_user` from `src.app.api.dependencies`)
3. Add observability if significant
4. Test with authentication and properly awaited fixtures
5. Ensure `manifest.json` is present for modules

---

❌ "I'll add Genesis integration later" → NO, do it now. Genesis is the "soul" of the system.
❌ "Events aren't needed" → Decoupling is mandatory.
❌ "Mocking the database in tests" → NO. See `high-fidelity-testing` skill. All tests must verify actual persistence.
❌ "Leaving it in PG, I'll cache later" → NO, push to Active Memory Warm Layer immediately.
