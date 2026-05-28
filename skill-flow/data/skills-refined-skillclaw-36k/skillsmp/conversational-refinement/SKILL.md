---
name: conversational-refinement
description: Pattern for building conversational refinement systems (like Genesis). Use when a module needs to gather evidence through natural dialogue to resolve uncertainties or incomplete data.
---

# Conversational Refinement Pattern

Pattern for LLM-driven refinement through natural conversation. When data is uncertain/incomplete, conversationally refine it instead of asking direct questions.

## When to Use

- Module has probabilistic outputs that could be refined
- User interaction can provide evidence (without them knowing the technical goal)
- You need to confirm assumptions through behavioral observations
- System should feel like conversation, not questionnaire

## Architecture

```
uncertainty/       # What's unknown
├── declarations   # Module declares uncertain fields
├── registry       # Central uncertainty tracking

hypothesis/        # What we suspect
├── model          # Hypothesis with confidence, priority
├── evidence       # Supporting/contradicting observations

probes/            # How we ask
├── types          # binary_choice, slider, reflection, confirmation
├── generator      # LLM-powered, strategy-driven
├── strategies/    # Domain-specific probe templates

session/           # Conversation state
├── manager        # Track progress, limits, completion

engine/            # Orchestration
├── lifecycle      # uncertainty → hypothesis → probe → confirm
├── priority       # Which hypothesis to probe next
```

## Core Models

### 1. UncertaintyDeclaration
```python
class UncertaintyField(BaseModel):
    """Single uncertain field with candidates."""
    field: str  # "rising_sign"
    module: str
    candidates: dict[str, float]  # {"Virgo": 0.25, "Leo": 0.25}
    confidence_threshold: float = 0.80
    refinement_strategies: list[str]

class UncertaintyDeclaration(BaseModel):
    """Module declares uncertain outputs."""
    module: str
    user_id: int
    fields: list[UncertaintyField]
    source_accuracy: Literal["probabilistic", "partial"]
```

### 2. Hypothesis
```python
class Hypothesis(BaseModel):
    """Trackable belief about uncertain field."""
    id: str
    field: str
    suspected_value: str
    confidence: float
    initial_confidence: float
    evidence: list[str] = []
    contradictions: list[str] = []
    probes_attempted: int = 0
    max_probes: int = 3
    resolved: bool = False
    
    @property
    def priority(self) -> float:
        """High when close to threshold, core field, has evidence."""
        if self.resolved:
            return 0.0
        
        closeness = 1 - abs(0.80 - self.confidence)
        core_boost = 0.1 if self.field in CORE_FIELDS else 0
        evidence_ratio = len(self.evidence) / (len(self.contradictions) + 1)
        
        return closeness + core_boost + (evidence_ratio * 0.1)
    
    @property
    def needs_probing(self) -> bool:
        return (not self.resolved and 
                self.confidence < 0.80 and 
                self.probes_attempted < self.max_probes)
```

### 3. ProbePacket
```python
class ProbePacket(BaseModel):
    """Question to gather evidence."""
    id: str
    hypothesis_id: str
    probe_type: Literal["binary_choice", "slider", "reflection", "confirmation"]
    question: str
    options: list[str] | None  # For binary_choice
    strategy_used: str
    confidence_mappings: dict[str, dict[str, float]]  # {"0": {"Virgo": 0.15}}
```

## Strategy Pattern

Strategies convert hypotheses into natural questions:

```python
class MorningRoutineStrategy:
    strategy_name = "morning_routine"
    applicable_fields = ["rising_sign"]
    probe_type = ProbeType.BINARY_CHOICE
    
    def generate_prompt(self, hypothesis: Hypothesis) -> str:
        return f"""Generate a binary choice about morning routines.
        Testing if rising sign is {hypothesis.suspected_value}.
        Don't mention astrology.
        Return JSON: {{"question": "...", "options": ["...", "..."], "mappings": ...}}"""

# Registry pattern
StrategyRegistry.register(MorningRoutineStrategy())
strategies = StrategyRegistry.get_strategies_for_field("rising_sign")
```

## Session Management

```python
class GenesisSession(BaseModel):
    session_id: str
    user_id: int
    state: Literal["active", "paused", "complete"]
    total_probes_sent: int
    max_probes_per_session: int = 10
    max_probes_per_field: int = 3
    fields_probed: dict[str, int]  # {"rising_sign": 2}
    fields_confirmed: list[str]
    
    @property
    def should_continue(self) -> bool:
        return (self.state == "active" and 
                self.total_probes_sent < self.max_probes_per_session)
```

## API Pattern

Single conversational endpoint:

```python
@router.post("/conversation")
async def conversation(request: ConversationRequest):
    """
    - No session_id: Start new session, return first probe
    - session_id + response: Process response, return next probe
    - session_complete: Return summary
    """
    if not request.session_id:
        session = await manager.create_session(user_id, hypothesis_ids)
    
    if request.response:
        result = await manager.process_response(session, response, engine)
        if result["session_complete"]:
            return {"summary": result["summary"]}
    
    next_probe = await manager.get_next_probe(session, engine)
    return {"probe": next_probe, "progress": manager.get_progress(session)}
```

## Integration Points

### 1. Auto-Start (on uncertain data)
```python
# In birth_data.py after submission
if birth_time is None:
    hypotheses = await engine.initialize_from_uncertainties(declarations)
    session = await manager.create_session(user_id, [h.id for h in hypotheses])
    return {"genesis_session": {"session_id": session.id, "first_probe": ...}}
```

### 2. StateTracker (profile completion)
```python
# In engine after creating hypotheses
await tracker.update_genesis_status(user_id, len(hypotheses), fields)

# In engine after confirmation
await tracker.update_field_confirmed(user_id, field, confirmed_value)
```

### 3. Activity Logging (observability)
```python
# In probe generator
await logger.log_activity(
    agent="genesis.probe_generator",
    activity_type="probe_generated",
    details={"hypothesis_id": h.id, "question": probe.question}
)
```

## Lifecycle Flow

```
1. Module calculates (probabilistic) → emits uncertainty declaration
2. Engine creates hypotheses from candidates
3. Session manager starts conversation
4. Loop:
   a. Select highest priority hypothesis
   b. Generate probe via strategy + LLM
   c. Present to user
   d. Process response → update confidence
   e. Check confirmations
5. Confirmation → trigger module recalculation
6. Session complete → summary
```

## Checklist

- [ ] UncertaintyDeclaration with candidates + confidence_threshold
- [ ] Hypothesis with priority calculation
- [ ] ProbeGenerator with LLM + fallback templates
- [ ] Strategy registry with domain strategies
- [ ] Session manager tracking limits
- [ ] Single conversational API endpoint
- [ ] Auto-start integration where uncertainties occur
- [ ] StateTracker hooks for observability
- [ ] Activity logging for transparency
- [ ] 80%+ test coverage

## GUTTERS Example: Genesis

Genesis implements this pattern for:
- **Rising sign** (no birth time → 12 candidates)
- **HD type** (no birth time → 5 candidates)

Strategies: morning_routine, first_impression, energy_pattern, decision_style
