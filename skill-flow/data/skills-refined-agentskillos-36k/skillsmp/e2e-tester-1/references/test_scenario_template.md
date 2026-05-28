# Test Scenario: [Name]

## Objective

[Single sentence describing what this test verifies]

## Prerequisites

- **Game state:** [clean/existing save/specific slot]
- **Required data:** [character vault/specific dungeon/etc.]
- **Special setup:** [any other requirements]

## Setup Steps

1. [First setup step - be specific about commands]
2. [Second setup step - include expected outputs if relevant]
3. [Continue until ready to test]

## Test Actions

1. [Action to perform]
   - **Command:** `[exact command to type]`
   - **Expected:** [what should happen]

2. [Next action]
   - **Command:** `[exact command]`
   - **Expected:** [what should happen]

3. [Continue with all test steps]

## Expected Outcomes

- ✓ [Success criterion 1 - specific and testable]
- ✓ [Success criterion 2]
- ✓ [Success criterion 3]
- ✓ No exceptions or error messages appear
- ✓ [Additional success criteria]

## Failure Conditions

- ✗ [What would indicate test failure]
- ✗ [Another failure condition]
- ✗ Python exceptions or tracebacks appear
- ✗ Game crashes or exits unexpectedly
- ✗ [Additional failure conditions]

## Notes

- **Estimated duration:** [X minutes]
- **Edge cases:** [Any edge cases to watch for]
- **Future extensions:** [How this scenario could be expanded]
- **Related scenarios:** [Links to related test scenarios]

---

## Template Usage Guide

### Writing Good Test Actions

**Bad example:**
```
1. Attack an enemy
```

**Good example:**
```
1. Attack the first goblin
   - **Command:** `attack 1`
   - **Expected:** Damage is dealt, goblin HP decreases, turn advances
```

### Defining Clear Success Criteria

**Bad example:**
```
- ✓ Combat works
```

**Good example:**
```
- ✓ Combat initiates when entering room with enemies
- ✓ Turn order follows initiative rolls
- ✓ Damage calculations match D&D 5E rules
- ✓ Combat ends when all enemies defeated or party flees
```

### Common Prerequisites

**New game:**
```
- **Game state:** clean (no existing saves)
- **Required data:** none
```

**Existing save:**
```
- **Game state:** existing save in slot 1
- **Required data:** Party with Shadow, Bob, Tim in Goblin Warren
```

**Character testing:**
```
- **Game state:** clean
- **Required data:** Character vault with level 5 wizard
```

### Scenario Naming Conventions

- `basic_combat.md` - Fundamental combat mechanics
- `dungeon_exploration.md` - Navigation and room interaction
- `spell_casting.md` - Magic system testing
- `inventory_management.md` - Item handling
- `character_creation.md` - Character vault operations
- `edge_case_[feature].md` - Boundary conditions
- `bug_[issue_number].md` - Specific bug reproduction
