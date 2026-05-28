---
id: feature-flags
name: "Feature Flags"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Feature Flags

## Overview

Feature flags (feature toggles) allow you to modify system behavior without deploying new code. They enable trunk-based development, progressive rollouts, A/B testing, and instant rollback of features.

## When to Use

- Progressive feature rollouts
- A/B testing and experimentation
- Canary deployments
- Kill switches for risky features
- Customer-specific features
- Trunk-based development (hide incomplete features)

## Key Principles

- **Keep flags short-lived**: Remove after full rollout
- **Track flag state**: Log which flags are active for debugging
- **Test all paths**: Both enabled and disabled code paths
- **Clean up**: Remove flag code when no longer needed
- **Minimize flag scope**: Flags at decision points, not scattered

## Best Practices

### Flag Types

```markdown
## Feature Flag Categories

### Release Flags
- Purpose: Hide incomplete features in production
- Lifespan: Short (days to weeks)
- Example: New checkout flow being developed

### Experiment Flags
- Purpose: A/B testing and data collection
- Lifespan: Medium (weeks to months)
- Example: Testing new pricing page design

### Ops Flags
- Purpose: Control operational aspects
- Lifespan: Medium to long
- Example: Circuit breaker, maintenance mode

### Permission Flags
- Purpose: Feature access control
- Lifespan: Long (permanent)
- Example: Premium features, beta access

### Kill Switches
- Purpose: Emergency feature disable
- Lifespan: Permanent (always available)
- Example: Disable payments during issues
```

### Simple Feature Flag Implementation

```python
from enum import Enum
from typing import Optional, Callable
from dataclasses import dataclass
import os
import json

class FlagType(Enum):
    RELEASE = "release"
    EXPERIMENT = "experiment"
    OPS = "ops"
    PERMISSION = "permission"


@dataclass
class FeatureFlag:
    name: str
    flag_type: FlagType
    default: bool = False
    description: str = ""
    owner: str = ""


class FeatureFlagManager:
    """Simple feature flag manager."""

    def __init__(self):
        self._flags: dict[str, FeatureFlag] = {}
        self._overrides: dict[str, bool] = {}
        self._load_overrides()

    def _load_overrides(self):
        """Load flag overrides from environment or config."""
        # From environment
        for key, value in os.environ.items():
            if key.startswith("FF_"):
                flag_name = key[3:].lower()
                self._overrides[flag_name] = value.lower() in ("true", "1", "yes")

        # From config file
        config_path = os.getenv("FEATURE_FLAGS_CONFIG")
        if config_path and os.path.exists(config_path):
            with open(config_path) as f:
                self._overrides.update(json.load(f))

    def register(self, flag: FeatureFlag):
        """Register a feature flag."""
        self._flags[flag.name] = flag

    def is_enabled(
        self,
        flag_name: str,
        user_id: Optional[str] = None,
        attributes: Optional[dict] = None
    ) -> bool:
        """Check if a feature flag is enabled."""
        # Check overrides first
        if flag_name in self._overrides:
            return self._overrides[flag_name]

        # Get flag definition
        flag = self._flags.get(flag_name)
        if not flag:
            return False

        return flag.default

    def get_all_flags(self, user_id: Optional[str] = None) -> dict[str, bool]:
        """Get all flag states for a user."""
        return {
            name: self.is_enabled(name, user_id)
            for name in self._flags
        }


# Global instance
feature_flags = FeatureFlagManager()

# Register flags
feature_flags.register(FeatureFlag(
    name="new_checkout",
    flag_type=FlagType.RELEASE,
    default=False,
    description="New checkout flow",
    owner="payments-team"
))

feature_flags.register(FeatureFlag(
    name="maintenance_mode",
    flag_type=FlagType.OPS,
    default=False,
    description="Enable maintenance mode",
    owner="platform-team"
))

# Usage
if feature_flags.is_enabled("new_checkout", user_id=user.id):
    return render_new_checkout(cart)
else:
    return render_old_checkout(cart)
```

### Percentage Rollout

```python
import hashlib
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class RolloutConfig:
    """Configuration for gradual rollout."""
    percentage: int = 0  # 0-100
    user_ids: set[str] = field(default_factory=set)  # Always enabled
    groups: set[str] = field(default_factory=set)  # Enabled groups


class FeatureFlagManagerWithRollout:
    def __init__(self):
        self._flags: dict[str, FeatureFlag] = {}
        self._rollouts: dict[str, RolloutConfig] = {}

    def set_rollout(self, flag_name: str, config: RolloutConfig):
        """Set rollout configuration for a flag."""
        self._rollouts[flag_name] = config

    def is_enabled(
        self,
        flag_name: str,
        user_id: Optional[str] = None,
        groups: Optional[set[str]] = None
    ) -> bool:
        """Check if flag is enabled for user."""
        flag = self._flags.get(flag_name)
        if not flag:
            return False

        rollout = self._rollouts.get(flag_name)
        if not rollout:
            return flag.default

        # Check explicit user list
        if user_id and user_id in rollout.user_ids:
            return True

        # Check group membership
        if groups and rollout.groups & groups:
            return True

        # Check percentage rollout
        if rollout.percentage > 0 and user_id:
            return self._is_in_percentage(flag_name, user_id, rollout.percentage)

        return flag.default

    def _is_in_percentage(
        self,
        flag_name: str,
        user_id: str,
        percentage: int
    ) -> bool:
        """Deterministic percentage check using hash."""
        # Combine flag name and user ID for consistent bucketing
        key = f"{flag_name}:{user_id}"
        hash_value = int(hashlib.md5(key.encode()).hexdigest(), 16)
        bucket = hash_value % 100
        return bucket < percentage


# Usage
flags = FeatureFlagManagerWithRollout()

# Gradual rollout to 25% of users
flags.set_rollout("new_search", RolloutConfig(
    percentage=25,
    user_ids={"admin-1", "test-user"},  # Always enabled
    groups={"beta_testers", "employees"}  # Groups enabled
))

# Check with user context
if flags.is_enabled("new_search", user_id=current_user.id, groups=current_user.groups):
    return new_search(query)
else:
    return old_search(query)
```

### Feature Flag Decorator

```python
from functools import wraps
from typing import Callable, Optional

def feature_flag(
    flag_name: str,
    fallback: Optional[Callable] = None,
    default_return=None
):
    """Decorator to conditionally execute function based on flag."""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Try to get user_id from kwargs or first arg
            user_id = kwargs.get("user_id") or (args[0] if args else None)

            if feature_flags.is_enabled(flag_name, user_id=user_id):
                return func(*args, **kwargs)
            elif fallback:
                return fallback(*args, **kwargs)
            else:
                return default_return

        return wrapper
    return decorator


# Usage
@feature_flag("new_recommendation_engine", fallback=get_recommendations_v1)
def get_recommendations_v2(user_id: str, limit: int = 10):
    """New ML-based recommendations."""
    return ml_service.get_recommendations(user_id, limit)


def get_recommendations_v1(user_id: str, limit: int = 10):
    """Legacy rule-based recommendations."""
    return rule_engine.get_recommendations(user_id, limit)
```

### Context Manager for Flags

```python
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Optional
import structlog

logger = structlog.get_logger()

# Store enabled flags in context
enabled_flags_var: ContextVar[set] = ContextVar("enabled_flags", default=set())


@contextmanager
def feature_flag_context(user_id: Optional[str] = None, attributes: dict = None):
    """Context manager that evaluates and stores flag state."""
    # Evaluate all flags once at request start
    enabled = set()
    for flag_name in feature_flags._flags:
        if feature_flags.is_enabled(flag_name, user_id, attributes):
            enabled.add(flag_name)

    # Store in context
    token = enabled_flags_var.set(enabled)

    # Log enabled flags
    logger.info("Feature flags evaluated", enabled_flags=list(enabled), user_id=user_id)

    try:
        yield enabled
    finally:
        enabled_flags_var.reset(token)


def is_flag_enabled(flag_name: str) -> bool:
    """Quick check using pre-evaluated context."""
    return flag_name in enabled_flags_var.get()


# FastAPI middleware
@app.middleware("http")
async def feature_flag_middleware(request: Request, call_next):
    user_id = getattr(request.state, "user_id", None)

    with feature_flag_context(user_id=user_id):
        response = await call_next(request)
        return response


# Usage in endpoint
@app.get("/products")
async def list_products():
    if is_flag_enabled("new_product_page"):
        return await get_products_v2()
    return await get_products_v1()
```

### LaunchDarkly Integration

```python
import ldclient
from ldclient.config import Config
from ldclient import Context

# Initialize LaunchDarkly client
ldclient.set_config(Config(os.getenv("LAUNCHDARKLY_SDK_KEY")))
ld_client = ldclient.get()


def is_enabled(
    flag_key: str,
    user_id: str,
    email: Optional[str] = None,
    custom_attributes: dict = None
) -> bool:
    """Check feature flag using LaunchDarkly."""
    context_builder = Context.builder(user_id)
    context_builder.kind("user")

    if email:
        context_builder.set("email", email)

    if custom_attributes:
        for key, value in custom_attributes.items():
            context_builder.set(key, value)

    context = context_builder.build()

    return ld_client.variation(flag_key, context, False)


def get_variation(
    flag_key: str,
    user_id: str,
    default: str = "control"
) -> str:
    """Get string variation for A/B testing."""
    context = Context.builder(user_id).kind("user").build()
    return ld_client.variation(flag_key, context, default)


# Usage
if is_enabled("new_pricing_page", user.id, email=user.email):
    return render_new_pricing()
else:
    return render_old_pricing()

# A/B test variant
variant = get_variation("checkout_button_color", user.id)
if variant == "blue":
    button_class = "btn-blue"
elif variant == "green":
    button_class = "btn-green"
else:
    button_class = "btn-default"
```

### Testing with Feature Flags

```python
import pytest
from unittest.mock import patch

@pytest.fixture
def feature_flags_enabled():
    """Fixture to enable specific flags in tests."""
    def _enable(*flags):
        original = feature_flags._overrides.copy()
        for flag in flags:
            feature_flags._overrides[flag] = True

        yield

        feature_flags._overrides = original

    return _enable


@pytest.fixture
def feature_flags_disabled():
    """Fixture to disable specific flags in tests."""
    def _disable(*flags):
        original = feature_flags._overrides.copy()
        for flag in flags:
            feature_flags._overrides[flag] = False

        yield

        feature_flags._overrides = original

    return _disable


# Test with flag enabled
def test_new_checkout_flow(feature_flags_enabled):
    with feature_flags_enabled("new_checkout"):
        result = process_checkout(cart)
        assert result.used_new_flow is True


# Test with flag disabled
def test_old_checkout_flow(feature_flags_disabled):
    with feature_flags_disabled("new_checkout"):
        result = process_checkout(cart)
        assert result.used_new_flow is False


# Parametrized tests for both paths
@pytest.mark.parametrize("flag_enabled", [True, False])
def test_checkout_both_paths(flag_enabled):
    with patch.object(feature_flags, "is_enabled", return_value=flag_enabled):
        result = process_checkout(cart)
        assert result.success is True
```

### Flag Cleanup

```python
"""
Flag Lifecycle Management

1. PLANNING
   - Define flag name, type, owner
   - Set expected lifespan
   - Document in flag registry

2. DEVELOPMENT
   - Implement with flag
   - Test both paths
   - Deploy with flag OFF

3. ROLLOUT
   - Enable for internal users
   - Gradual percentage increase
   - Monitor metrics

4. FULL ROLLOUT
   - Enable for all users
   - Monitor for issues

5. CLEANUP (Critical!)
   - Remove flag checks from code
   - Remove flag configuration
   - Deploy clean code
   - Delete flag definition
"""

# Flag registry with cleanup dates
FLAG_REGISTRY = {
    "new_checkout": {
        "type": "release",
        "owner": "payments-team",
        "created": "2024-01-15",
        "expected_cleanup": "2024-02-15",
        "status": "rolling_out",
        "rollout_percentage": 50,
    },
    "maintenance_mode": {
        "type": "ops",
        "owner": "platform-team",
        "created": "2023-06-01",
        "expected_cleanup": None,  # Permanent
        "status": "permanent",
    },
}


def audit_stale_flags():
    """Find flags that should be cleaned up."""
    from datetime import datetime, timedelta

    stale_flags = []
    now = datetime.now()

    for flag_name, info in FLAG_REGISTRY.items():
        cleanup_date = info.get("expected_cleanup")
        if cleanup_date:
            cleanup = datetime.strptime(cleanup_date, "%Y-%m-%d")
            if cleanup < now:
                stale_flags.append({
                    "flag": flag_name,
                    "owner": info["owner"],
                    "overdue_days": (now - cleanup).days,
                })

    return stale_flags


# CI check for stale flags
# scripts/check_stale_flags.py
if __name__ == "__main__":
    stale = audit_stale_flags()
    if stale:
        print("WARNING: Stale feature flags found!")
        for flag in stale:
            print(f"  - {flag['flag']}: {flag['overdue_days']} days overdue (owner: {flag['owner']})")
        # Optionally fail CI
        # sys.exit(1)
```

## Anti-patterns

- **Flag debt**: Never removing flags after rollout
- **Nested flags**: Multiple flags creating complex conditions
- **Flag dependencies**: One flag depending on another
- **Global flags**: Flags without user context
- **Testing only happy path**: Not testing disabled state
- **Using flags for config**: Flags aren't configuration management

## References

- [Feature Toggles - Martin Fowler](https://martinfowler.com/articles/feature-toggles.html)
- [LaunchDarkly Docs](https://docs.launchdarkly.com/)
- [Unleash Feature Flags](https://www.getunleash.io/)
- [Feature Flag Best Practices](https://featureflags.io/)
