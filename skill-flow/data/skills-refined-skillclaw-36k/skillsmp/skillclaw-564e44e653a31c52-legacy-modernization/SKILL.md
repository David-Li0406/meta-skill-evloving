---
name: legacy-modernization
description: Use this skill when you need to safely upgrade and modernize legacy systems, migrate frameworks, and reduce technical debt through incremental and structured approaches.
---

# Legacy Modernization

Safely upgrade and modernize legacy systems.

## When to Use

- Framework migrations (e.g., jQuery to React, Java 8 to 17, Python 2 to 3)
- Language version upgrades
- Monolith decomposition to microservices
- Technical debt reduction
- Dependency updates and security patches
- Database modernization (e.g., stored procedures to ORMs)
- API versioning and maintaining backward compatibility

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

Focus on risk mitigation. Never break existing functionality without a migration path.