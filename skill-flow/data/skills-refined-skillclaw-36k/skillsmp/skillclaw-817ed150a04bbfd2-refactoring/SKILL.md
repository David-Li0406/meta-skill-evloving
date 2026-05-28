---
name: refactoring
description: Use this skill when you need to safely refactor code, reduce complexity, or improve maintainability through established patterns and strategies.
---

# Refactoring Skill

## Golden Rules

1. **Never refactor without tests** - Tests are your safety net.
2. **Small steps** - One change at a time; test after each.
3. **Keep it working** - Code should pass tests at every step.
4. **Commit often** - Easy to revert if something breaks.

## Code Smells to Address

### Bloaters
| Smell | Symptom | Refactoring |
|-------|---------|-------------|
| Long Method | >20 lines | Extract Method |
| Large Class | >200 lines | Extract Class |
| Long Parameter List | >3 params | Introduce Parameter Object |
| Data Clumps | Same fields appear together | Extract Class |

### Object-Orientation Abusers
| Smell | Symptom | Refactoring |
|-------|---------|-------------|
| Switch Statements | Multiple type checks | Replace with Polymorphism |
| Parallel Inheritance | Every subclass needs partner | Merge Hierarchies |
| Refused Bequest | Subclass doesn't use parent | Replace Inheritance with Delegation |

### Change Preventers
| Smell | Symptom | Refactoring |
|-------|---------|-------------|
| Divergent Change | One class changed for multiple reasons | Extract Class |
| Shotgun Surgery | One change affects many classes | Move Method/Field |
| Feature Envy | Method uses other class's data | Move Method |

### Dispensables
| Smell | Symptom | Refactoring |
|-------|---------|-------------|
| Dead Code | Unused code | Delete |
| Duplicate Code | Same logic repeated | Extract Method |
| Speculative Generality | Unused abstraction | Collapse Hierarchy |
| Comments | Explaining bad code | Refactor until self-explanatory |

## Common Refactorings

### Extract Method
```python
# Before
def process_order(order):
    # Validate order
    if not order.items:
        raise ValueError("Empty order")
    if order.total < 0:
        raise ValueError("Invalid total")
    # ... more validation ...

    # Calculate shipping
    shipping = 0
    if order.total > 100:
        shipping = 0
    elif order.weight < 1:
        shipping = 5
    else:
        shipping = 10
    # ... continue

# After
def process_order(order):
    validate_order(order)
    shipping = calculate_shipping(order)
    # ... continue

def validate_order(order):
    if not order.items:
        raise ValueError("Empty order")
    if order.total < 0:
        raise ValueError("Invalid total")
```