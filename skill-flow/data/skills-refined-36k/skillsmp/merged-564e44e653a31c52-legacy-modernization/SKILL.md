---
name: legacy-modernization
description: Use this skill for safe, incremental upgrades of legacy codebases, framework migrations, and technical debt reduction.
---

# Legacy Modernization

Safely upgrade and modernize legacy systems.

## When to Use

- Framework migrations (e.g., jQuery to React, Python 2 to 3)
- Database modernization (e.g., stored procedures to ORMs)
- Monolith decomposition into microservices
- Technical debt reduction
- Dependency updates and security patches
- API versioning and backward compatibility

## Migration Strategies

### Strangler Fig Pattern

```
┌─────────────────────────────────────┐
│           Load Balancer             │
└──────────────┬──────────────────────┘
               │
       ┌───────┴───────┐
       │               │
┌──────▼──────┐ ┌──────▼──────┐
│   Legacy    │ │    New      │
│   System    │ │   Service   │
└─────────────┘ └─────────────┘

1. Route new features to new service
2. Gradually migrate existing features
3. Eventually retire legacy system
```

### Branch by Abstraction

```python
# 1. Create abstraction layer
class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, amount: float) -> bool:
        pass

# 2. Wrap legacy implementation
class LegacyPaymentProcessor(PaymentProcessor):
    def __init__(self, legacy_system):
        self.legacy = legacy_system

    def process(self, amount: float) -> bool:
        return self.legacy.old_process_method(amount)

# 3. Create new implementation
class ModernPaymentProcessor(PaymentProcessor):
    def process(self, amount: float) -> bool:
        # New implementation
        pass

# 4. Use feature flag to switch
processor = (ModernPaymentProcessor() if feature_flag("new_payment")
             else LegacyPaymentProcessor(legacy))
```

## Migration Checklist

### Before Starting

- [ ] Document current behavior
- [ ] Add tests for existing functionality
- [ ] Set up monitoring and alerts
- [ ] Create rollback plan
- [ ] Communicate with stakeholders

### During Migration

- [ ] Make incremental changes
- [ ] Test after each change
- [ ] Monitor error rates
- [ ] Keep legacy running in parallel
- [ ] Document breaking changes

### After Migration

- [ ] Remove feature flags
- [ ] Clean up legacy code
- [ ] Update documentation
- [ ] Archive old codebase
- [ ] Post-mortem lessons learned

## Output

- Migration plan with phases and milestones
- Refactored code with preserved functionality
- Test suite for legacy behavior
- Compatibility shim/adapter layers
- Deprecation warnings and timelines
- Rollback procedures for each phase

## Examples

**Input:** "Migrate from Express to Fastify"  
**Action:** Create adapter layer, migrate routes incrementally, test each step.

**Input:** "Reduce technical debt in this module"  
**Action:** Add tests first, refactor incrementally, maintain compatibility.

Focus on risk mitigation. Never break existing functionality without a migration path.