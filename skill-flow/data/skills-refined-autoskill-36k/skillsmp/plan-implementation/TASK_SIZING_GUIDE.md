# Task Sizing Guide

Quick reference for breaking down features into appropriately sized implementation tasks.

---

## The Goldilocks Principle

### Too Small 🐭
Tasks that are too granular create tracking overhead without value.

**Examples**:
- ❌ "Add getter for property X"
- ❌ "Write one test case"
- ❌ "Fix typo in comment"
- ❌ "Rename variable from x to y"

**Why avoid**: Time spent managing task > time to complete it

---

### Just Right 🐻
Tasks that deliver meaningful progress and are clearly testable.

**Examples**:
- ✅ "Implement Training.CalculateBonus() with unit tests"
- ✅ "Add Horse.Speed stat modifier with tests for edge cases"
- ✅ "Create TrainingService.AddTraining() with validation"
- ✅ "Wire up RaceService to use effective stats (base + training)"

**Why perfect**:
- Completable in 30-90 minutes
- Clear acceptance criteria
- Delivers testable functionality
- Meaningful progress visible

**Task Template**:
```
[Action] [Component].[Method/Feature] with [validation/tests/integration]
```

---

### Too Large 🐘
Tasks that are vague, multi-day, or impossible to test atomically.

**Examples**:
- ❌ "Implement entire training system"
- ❌ "Refactor RaceService"
- ❌ "Add all API endpoints"
- ❌ "Make everything work together"

**Why avoid**:
- Unclear when "done"
- Hard to test
- Risky (too many changes at once)
- Demotivating (never feels complete)

**Fix**: Break into vertical slices or phases

---

## Vertical Slice Sizing

A vertical slice delivers **end-to-end functionality** for **one capability**.

### Good Vertical Slice ✅
**Task**: "Add training for Speed stat"

**Includes**:
- Data: Training entity with Speed type
- Logic: Horse.CalculateEffectiveStats() applies Speed training
- Persistence: Can save/load Speed training from database
- Tests: Unit tests for calculation, integration test for persistence

**Demo**: Train a horse's Speed, save to DB, load it back, see improved Speed in races

**Size**: 1-2 hours of focused work

---

### Too Horizontal ❌
**Task**: "Create all training entities"

**Includes**:
- Training entity
- SpeedTraining entity
- StaminaTraining entity
- AgilityTraining entity

**Problem**:
- Doesn't deliver working feature
- Can't validate behavior
- Just busywork until something uses it

**Fix**: Do "Speed training end-to-end" first, then add Stamina, then Agility

---

## Sizing by Complexity

### Simple (30-45 min) 🟢
- Add one calculated property with tests
- Implement one validation rule
- Create one simple entity
- Write characterization tests for existing method

### Medium (45-90 min) 🟡
- Implement service method with multiple edge cases
- Add database integration with migration
- Refactor one subsystem with test coverage
- Wire up new component to existing system

### Complex (90+ min) 🔴
- Design and implement calculation algorithm
- Build new service with multiple methods
- Integrate complex third-party API
- Migrate/transform existing data

**If task is Complex**: Consider breaking into multiple Medium tasks

---

## Red-Green-Refactor Sizing

Each TDD cycle should be **one task**.

### Red Phase
**Size**: 10-20 minutes
- Write 3-5 test cases for one behavior
- Run tests, verify they fail
- Confirm failure is for the right reason

### Green Phase
**Size**: 20-45 minutes
- Write minimal code to pass tests
- Don't worry about perfection
- Make it work before making it pretty

### Refactor Phase
**Size**: 10-25 minutes
- Clean up while keeping tests green
- Extract methods, improve names
- Remove duplication

**Total Cycle**: 40-90 minutes = One task

---

## Task Breakdown Examples

### Example 1: Training System

❌ **Too Large**: "Implement training system"

✅ **Broken Down**:
1. Phase 1: Add Speed training (data + calculation) with tests
2. Phase 2: Wire Speed training into race simulation with integration tests
3. Phase 3: Add Stamina training following same pattern
4. Phase 4: Add Agility training following same pattern
5. Phase 5: Add TrainingService for business logic and validation

**Each phase**: Delivers working, testable functionality

---

### Example 2: Race Modifiers Refactor

❌ **Too Large**: "Refactor modifier system"

✅ **Broken Down**:
1. Phase 1: Create RaceModifierConfig with constants (tests for validation)
2. Phase 2: Implement stat modifiers (Speed, Agility) with unit tests
3. Phase 3: Implement environmental modifiers (Surface, Condition) with unit tests
4. Phase 4: Implement phase modifiers (LegType timing) with unit tests
5. Phase 5: Wire all modifiers into RaceService with integration tests
6. Phase 6: Delete old code, clean up, verify no regressions

**Each phase**: Independent, testable, builds on previous

---

### Example 3: New Game Feature

❌ **Too Horizontal**:
- Phase 1: Create all entities
- Phase 2: Create all services
- Phase 3: Create all UI

✅ **Vertical Slices**:
- Phase 1: Basic betting (entity + service + UI) - can place bet, see result
- Phase 2: Bet validation (rules + tests) - invalid bets rejected
- Phase 3: Payout calculation (logic + tests) - winnings calculated correctly
- Phase 4: Betting history (persistence + UI) - view past bets

**Each phase**: Delivers working feature increment

---

## Checklist for Well-Sized Tasks

### ✅ Good Task Characteristics
- [ ] Concrete action verb (Implement, Create, Add, Refactor, Wire up)
- [ ] Specific component/method named
- [ ] Includes "with tests" or "with validation"
- [ ] Completable in 30-90 minutes
- [ ] Clear "done" criteria
- [ ] Independently testable
- [ ] Delivers visible progress

### ❌ Warning Signs
- [ ] Vague verbs (Fix, Update, Make, Do)
- [ ] No specific component mentioned
- [ ] No testing mentioned
- [ ] Would take multiple hours/days
- [ ] Unclear when it's done
- [ ] Can't test until other tasks complete
- [ ] Just infrastructure/setup work

---

## Task Naming Patterns

### Pattern 1: Create with Tests
```
Create [EntityName] with [properties] and unit tests for [scenarios]
```
**Example**: Create Training entity with HorseId, Stat, XP properties and unit tests for validation

### Pattern 2: Implement with Tests
```
Implement [ClassName].[MethodName] with tests for [edge cases]
```
**Example**: Implement Horse.CalculateEffectiveStats() with tests for zero training, max training, multiple stats

### Pattern 3: Wire Up with Integration
```
Wire up [Component] to use [OtherComponent] with integration test
```
**Example**: Wire up RaceService to use Horse.CalculateEffectiveStats() with integration test for race outcome

### Pattern 4: Refactor with Coverage
```
Refactor [component] to [improvement] while maintaining test coverage
```
**Example**: Refactor stat modifiers to use configuration constants while maintaining 100% test coverage

### Pattern 5: Add Validation
```
Add [validation type] to [component] with tests for [invalid scenarios]
```
**Example**: Add input validation to TrainingService.AddTraining() with tests for negative XP, invalid stat, null horse

---

## Phase Naming Patterns

Phases should be named by **what they deliver**, not what they do.

### ❌ Bad Phase Names (Task-Focused)
- "Create entities"
- "Write tests"
- "Update database"
- "Build services"

### ✅ Good Phase Names (Outcome-Focused)
- "Speed training calculation" (delivers working Speed bonus calculation)
- "Training persistence" (delivers ability to save/load training)
- "Race integration" (delivers training affecting race outcomes)
- "Validation and edge cases" (delivers robust error handling)

---

## Estimation Guide

### Time Estimates by Task Type

**Create Simple Entity**: 30 min
- Write class with properties
- Add 5-10 unit tests
- Validate required fields

**Implement Service Method**: 45-60 min
- Write method logic
- Add 10-15 unit tests
- Handle 3-5 edge cases

**Database Integration**: 60-75 min
- Create/update entity configuration
- Write migration
- Add integration tests
- Verify CRUD operations

**Refactor with Tests**: 45-60 min
- Extract method/class
- Move test coverage
- Verify no behavior change
- Clean up call sites

**Complex Algorithm**: 90-120 min
- Research approach
- Write characterization tests
- Implement algorithm
- Test edge cases
- Optimize if needed

---

## When to Split a Task

Split if any of these are true:

### Multiple Concerns
Task involves unrelated concepts
- ❌ "Add training and update UI and migrate database"
- ✅ Split into: Training logic, UI update, Database migration

### Multiple Test Suites
Task requires tests in multiple test files
- ❌ "Implement training across all entities"
- ✅ Split by entity: Horse training, then Jockey training, etc.

### Dependencies Create Waiting
Task can't start until multiple other tasks finish
- ❌ "Integrate everything"
- ✅ Split into: Integrate A→B, then Integrate B→C

### Unclear Acceptance Criteria
Can't easily define "done"
- ❌ "Improve performance"
- ✅ Split into: Profile bottlenecks, Optimize query N+1, Add caching

### Takes > 2 Hours
Task estimate exceeds one focused work session
- ❌ Any task > 2 hours
- ✅ Break into subtasks of 30-90 min each

---

## Quick Reference

| Aspect | Guideline |
|--------|-----------|
| **Time** | 30-90 minutes of focused work |
| **Tests** | Every task includes tests |
| **Demo** | Can show working result |
| **Scope** | One concept/behavior/integration |
| **Action** | Concrete verb + specific target |
| **Value** | Delivers testable functionality |
| **Risk** | Can be rolled back if needed |

---

**Remember**: The goal is **working software incrementally**, not perfectly organized tasks!
