# Feature Planning Template (TDD Approach)

## Feature Name
[Brief, descriptive name for the feature]

## Summary
[One paragraph explaining what this feature is and why it's being added to TripleDerby]

---

## Requirements

### Functional Requirements
What the feature must do:
- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3

### Acceptance Criteria
How we'll know the feature works (these become tests):
- [ ] Criterion 1: [e.g., "Given a horse with Speed=80, when training Speed, then Speed increases by X"]
- [ ] Criterion 2: [e.g., "Given max stat value, when training, then stat does not exceed cap"]
- [ ] Criterion 3: [e.g., "Given invalid training request, then returns validation error"]

### Non-Functional Requirements
- [ ] Performance: [e.g., training calculation completes in < 10ms]
- [ ] Security: [e.g., validate all inputs to prevent exploits]

---

## Technical Analysis

### Affected Systems
- **Entities**: [e.g., Horse, Race, RaceRunHorse]
- **Services**: [e.g., RaceService, TrainingService]
- **Data Layer**: [e.g., new Training table]
- **UI Components**: [e.g., training screen]

### Data Model Changes
```
Example:
- Add Training entity with properties: Id, HorseId, Stat, XP, Date
- Add TrainingLevel property to Horse
- Add CalculateEffectiveStats() method to Horse
```

### Integration Points
- [e.g., RaceService needs to use Horse.CalculateEffectiveStats() instead of raw stats]
- [e.g., UI needs to display training progress]

### Risks & Challenges
- [e.g., Complex stat calculations might be hard to test]
- [e.g., Database migration for existing horses]

---

## TDD Implementation Plan

### Red-Green-Refactor Cycles

Each cycle follows: Write failing test → Make it pass → Clean up code

#### Cycle 1: Core Domain Model
**RED - Write Failing Tests**
- [ ] Test: Training entity can be created with required properties
- [ ] Test: Horse can have associated Training records
- [ ] Test: Horse.CalculateEffectiveStats() returns base stats when no training

**GREEN - Make Tests Pass**
- [ ] Create Training entity class
- [ ] Add Training navigation property to Horse
- [ ] Implement Horse.CalculateEffectiveStats() method (simple version)

**REFACTOR**
- [ ] Clean up any duplicated code
- [ ] Ensure proper encapsulation
- [ ] Verify naming conventions

---

#### Cycle 2: Training Calculations
**RED - Write Failing Tests**
- [ ] Test: Training XP correctly increases stat values
- [ ] Test: Training bonuses apply correct formulas (linear, diminishing, etc.)
- [ ] Test: Stats respect maximum caps even with training
- [ ] Test: Multiple training records stack correctly

**GREEN - Make Tests Pass**
- [ ] Implement training bonus calculation in Horse.CalculateEffectiveStats()
- [ ] Add stat cap validation
- [ ] Handle multiple training records per stat

**REFACTOR**
- [ ] Extract calculation logic if complex
- [ ] Remove magic numbers (use constants)
- [ ] Simplify conditional logic

---

#### Cycle 3: Training Service - Add Training
**RED - Write Failing Tests**
- [ ] Test: Can add training XP to a horse's stat
- [ ] Test: Adding training creates Training entity
- [ ] Test: Adding training to invalid stat throws exception
- [ ] Test: Adding negative XP throws exception
- [ ] Test: Training respects cooldown rules (if applicable)

**GREEN - Make Tests Pass**
- [ ] Create TrainingService class
- [ ] Implement AddTraining(horseId, stat, xp) method
- [ ] Add validation for stat names and XP values
- [ ] Implement cooldown logic (if needed)

**REFACTOR**
- [ ] Extract validation to separate method
- [ ] Ensure single responsibility principle
- [ ] Consider using value objects for Stat/XP

---

#### Cycle 4: Integration with Race Service
**RED - Write Failing Tests**
- [ ] Test: RaceService uses effective stats (base + training) in simulation
- [ ] Test: Trained horse performs better than untrained in race
- [ ] Test: Race results reflect training bonuses accurately

**GREEN - Make Tests Pass**
- [ ] Update RaceService to call Horse.CalculateEffectiveStats()
- [ ] Ensure race simulation uses effective stats everywhere
- [ ] Verify race outcome calculations

**REFACTOR**
- [ ] Remove any direct stat access (use CalculateEffectiveStats() consistently)
- [ ] Simplify stat retrieval logic
- [ ] Ensure backward compatibility

---

#### Cycle 5: Data Persistence
**RED - Write Failing Tests**
- [ ] Test: Training entity can be saved to database
- [ ] Test: Training records are loaded with Horse entity
- [ ] Test: Can query horses by training level
- [ ] Test: Deleting horse cascades to training records

**GREEN - Make Tests Pass**
- [ ] Configure Training entity in ModelBuilderExtensions
- [ ] Set up relationships (Horse 1-to-many Training)
- [ ] Create database migration
- [ ] Update repository methods if needed

**REFACTOR**
- [ ] Optimize queries (eager loading vs lazy loading)
- [ ] Add indexes if needed for performance
- [ ] Clean up migration code

---

#### Cycle 6: Edge Cases & Validation
**RED - Write Failing Tests**
- [ ] Test: Training non-existent horse returns error
- [ ] Test: Training with null/invalid inputs throws proper exceptions
- [ ] Test: Concurrent training requests are handled safely
- [ ] Test: Training XP overflow is handled correctly

**GREEN - Make Tests Pass**
- [ ] Add null checks and validation
- [ ] Implement proper error handling
- [ ] Add concurrency safeguards if needed
- [ ] Handle edge cases (max int, etc.)

**REFACTOR**
- [ ] Consolidate validation logic
- [ ] Use guard clauses
- [ ] Ensure consistent error handling

---

#### Cycle 7: UI Integration (if applicable)
**RED - Write Failing Tests**
- [ ] Test: TrainingController returns training data for horse
- [ ] Test: TrainingController accepts training requests
- [ ] Test: Invalid training requests return proper error responses

**GREEN - Make Tests Pass**
- [ ] Create TrainingController/ViewModel
- [ ] Wire up UI to TrainingService
- [ ] Add API endpoints or UI bindings

**REFACTOR**
- [ ] Extract UI logic from business logic
- [ ] Ensure proper separation of concerns
- [ ] Optimize data transfer objects

---

## Test Categories

### Unit Tests
Focus on individual components in isolation:
- Training entity behavior
- Horse.CalculateEffectiveStats() logic
- TrainingService methods
- Validation rules

### Integration Tests
Test components working together:
- TrainingService + Database
- RaceService + Horse with training
- End-to-end training workflow

### Performance Tests (if needed)
- Race simulation with 20 trained horses completes in < 100ms
- Training calculation doesn't degrade with many records

---

## Success Criteria (Test-Driven)

All tests must pass:
- [ ] All unit tests pass (isolated component behavior)
- [ ] All integration tests pass (components working together)
- [ ] Code coverage > 80% for new code
- [ ] No regression in existing tests
- [ ] Performance benchmarks met

Feature works correctly:
- [ ] Can train horses and see stat improvements
- [ ] Training bonuses apply correctly in races
- [ ] Edge cases handled gracefully
- [ ] UI (if applicable) works intuitively

---

## Implementation Workflow

### For Each TDD Cycle:

1. **RED Phase**
   - Write test(s) that define the desired behavior
   - Run tests → They should FAIL (no implementation yet)
   - Confirm test failure is for the right reason

2. **GREEN Phase**
   - Write minimal code to make tests pass
   - Don't worry about perfection, just make it work
   - Run tests → They should PASS

3. **REFACTOR Phase**
   - Clean up code while keeping tests green
   - Remove duplication
   - Improve names, structure, readability
   - Run tests → They should still PASS

4. **Commit**
   - Commit after each complete cycle
   - Commit message: "Add [feature]: [what was added]"
   - Example: "Add training bonus calculation to Horse entity"

---

## Testing Patterns to Use

### Arrange-Act-Assert (AAA)
```csharp
[Fact]
public void AddTraining_IncreasesHorseStat()
{
    // Arrange
    var horse = new Horse { Speed = 80 };
    var service = new TrainingService();

    // Act
    service.AddTraining(horse.Id, "Speed", 100);

    // Assert
    Assert.Equal(85, horse.CalculateEffectiveStats().Speed);
}
```

### Test Naming Convention
`MethodName_Scenario_ExpectedBehavior`
- `CalculateEffectiveStats_WithNoTraining_ReturnsBaseStats`
- `AddTraining_WithNegativeXP_ThrowsArgumentException`
- `RaceSimulation_WithTrainedHorse_PerformsBetter`

### Test Data Builders (for complex objects)
```csharp
public class HorseBuilder
{
    public Horse WithSpeed(int speed) { ... }
    public Horse WithTraining(string stat, int xp) { ... }
    public Horse Build() { ... }
}
```

---

## Open Questions

Items needing clarification before starting:
- [ ] Question 1: [e.g., Linear or diminishing returns for training?]
- [ ] Question 2: [e.g., Should there be training cooldowns?]
- [ ] Question 3: [e.g., Cost for training (currency, resources)?]

---

## Files to Create (Test-First)

### Test Files (Created First)
- `TripleDerby.Tests/Entities/TrainingTests.cs`
- `TripleDerby.Tests/Entities/HorseTests.cs`
- `TripleDerby.Tests/Services/TrainingServiceTests.cs`
- `TripleDerby.Tests/Integration/TrainingIntegrationTests.cs`

### Implementation Files (Created to Make Tests Pass)
- `TripleDerby.Core/Entities/Training.cs`
- `TripleDerby.Core/Services/TrainingService.cs`
- `TripleDerby.Infrastructure/Data/Migrations/AddTrainingSystem.cs`
- `TripleDerby.Infrastructure/Data/ModelBuilderExtensions.cs` (update)

---

## Milestones

### Milestone 1: Core Domain Tests Green
All unit tests for Training and Horse pass

### Milestone 2: Service Layer Tests Green
All TrainingService tests pass

### Milestone 3: Integration Tests Green
End-to-end training workflow works

### Milestone 4: Race Integration Tests Green
Training bonuses correctly affect race outcomes

### Milestone 5: Production Ready
All tests pass, code coverage met, feature complete

---

## Notes

- **Test first, always**: No production code without a failing test first
- **Small steps**: Each cycle should be 15-30 minutes max
- **Keep tests green**: Never commit with failing tests
- **Refactor fearlessly**: Tests give you confidence to improve code
- **Listen to tests**: If tests are hard to write, design might need improvement
