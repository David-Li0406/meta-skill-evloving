---
id: trunk-based-development
name: "Trunk-Based Development"
domain: DEV
skill: faion-software-developer
category: "development-practices"
---

# Trunk-Based Development

## Overview

Trunk-Based Development (TBD) is a source-control branching model where developers collaborate on code in a single branch called "trunk" (or "main/master"), resisting any pressure to create long-lived development branches. Small, frequent commits to trunk enable Continuous Integration and reduce merge conflicts.

## When to Use

- Teams practicing CI/CD
- Projects requiring fast iteration
- When merge conflicts are a problem
- High-performing DevOps teams
- Feature flag infrastructure exists
- Strong automated testing in place

## When to Avoid

- Weak test coverage
- No CI/CD pipeline
- Regulatory compliance requiring branch isolation
- Open-source projects with external contributors

## Key Principles

### Single Source of Truth

```markdown
## Rules
- One main branch ("trunk" / "main")
- All developers commit to trunk
- Trunk is always releasable
- No long-lived feature branches (> 1-2 days max)

## Benefits
- Everyone sees latest code
- No merge hell
- Faster feedback
- Simpler mental model
```

### Small, Frequent Commits

```markdown
## Commit Patterns
- At least once per day
- Smaller changes = easier review
- Each commit builds and tests pass
- Ideally < 200 lines changed

## Anti-patterns
- Commits once a week
- "WIP" commits to trunk
- Large refactoring in one commit
```

### Trunk is Always Releasable

```markdown
## Enforced By
- Automated tests (must pass to merge)
- Feature flags (hide incomplete work)
- Code review (short turnaround)
- CI pipeline (fast feedback)

## If Trunk Breaks
- Stop everything
- Fix immediately
- Root cause analysis
- Improve tests/gates
```

## Branching Strategies

### Pure Trunk (Commit Directly)

```bash
# For small teams (2-3) with high trust
# and strong local testing

# Work on trunk directly
git checkout main
git pull

# Make changes
vim src/feature.py

# Test locally
pytest

# Commit directly to trunk
git add .
git commit -m "feat: add user validation"
git push origin main
```

### Short-Lived Feature Branches

```bash
# For most teams (recommended)
# Branches live < 1-2 days

# Create short-lived branch
git checkout -b feat/user-validation
git push -u origin feat/user-validation

# Work in small increments
vim src/feature.py
git add . && git commit -m "add email validator"

# Frequently integrate from main
git fetch origin main
git rebase origin/main

# Open PR same day
gh pr create --title "Add user validation" --body "..."

# Merge same day (after review)
gh pr merge --squash

# Delete branch immediately
git checkout main
git pull
git branch -d feat/user-validation
```

### Release Branches (Optional)

```markdown
## When Needed
- Long release testing cycles
- Regulatory requirements
- Multiple versions in production

## Rules
- Branch from trunk for release
- Only hotfixes go to release branch
- Cherry-pick fixes back to trunk
- Never develop on release branch

## Flow
main → release/v2.1 → production
         ↓ hotfix
       release/v2.1 → cherry-pick to main
```

## Best Practices

### Feature Flags

```python
# Hide incomplete features behind flags
# Deploy to production without exposing

from feature_flags import is_enabled

def get_user_profile(user_id: str):
    profile = fetch_profile(user_id)

    # New feature behind flag
    if is_enabled("show_activity_feed", user_id):
        profile["activity"] = fetch_activity(user_id)

    return profile

# Feature flag service
class FeatureFlags:
    def __init__(self, provider: FlagProvider):
        self.provider = provider

    def is_enabled(self, flag: str, user_id: str = None) -> bool:
        """
        Check if feature is enabled.
        Supports:
        - Global on/off
        - Percentage rollout
        - User-specific targeting
        """
        return self.provider.evaluate(flag, {"user_id": user_id})
```

### Branch by Abstraction

```python
# Large refactoring without feature branches
# Create abstraction layer, swap implementation

# Step 1: Create abstraction
class PaymentProcessor(Protocol):
    def process(self, amount: Decimal) -> PaymentResult: ...

# Step 2: Old implementation
class LegacyPaymentProcessor:
    def process(self, amount: Decimal) -> PaymentResult:
        return self.old_gateway.charge(amount)

# Step 3: New implementation (behind flag)
class NewPaymentProcessor:
    def process(self, amount: Decimal) -> PaymentResult:
        return self.stripe.create_charge(amount)

# Step 4: Router (use flag to switch)
def get_payment_processor() -> PaymentProcessor:
    if feature_flags.is_enabled("new_payment"):
        return NewPaymentProcessor()
    return LegacyPaymentProcessor()

# Step 5: After validation, remove old code
# Delete LegacyPaymentProcessor
# Remove feature flag
# Direct instantiation of NewPaymentProcessor
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
# Ensure quality before pushing to trunk

repos:
  - repo: local
    hooks:
      - id: tests
        name: Run tests
        entry: pytest --tb=short -q
        language: system
        pass_filenames: false

      - id: lint
        name: Lint code
        entry: ruff check .
        language: system
        pass_filenames: false

      - id: type-check
        name: Type check
        entry: mypy src/
        language: system
        pass_filenames: false
```

### CI Pipeline for TBD

```yaml
# .github/workflows/trunk.yml
name: Trunk CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run tests
        run: pytest --cov=src --cov-fail-under=80

      - name: Lint
        run: ruff check .

      - name: Type check
        run: mypy src/

      # Fast feedback is crucial
      # Total time should be < 10 minutes

  deploy-to-staging:
    needs: build-and-test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to staging
        run: ./deploy.sh staging

  # Optional: auto-deploy to production
  # deploy-to-production:
  #   needs: deploy-to-staging
  #   ...
```

### Code Review in TBD

```markdown
## Fast Reviews Required
- Review within 4 hours (ideally 1 hour)
- Small PRs = fast reviews
- Async review or pair on complex changes

## Review Checklist
- [ ] Tests pass
- [ ] Feature flag if needed
- [ ] Backward compatible
- [ ] No breaking changes to trunk

## Pair Programming Alternative
- Write code together = no review needed
- Pair = instant review
- Good for complex changes
```

## Common Patterns

### Keystone Interface Pattern

```python
# Build complete feature in parts
# Only enable when all parts ready

# Part 1: Add endpoint (returns 404)
@app.get("/api/v2/users/{user_id}/activity")
async def get_activity(user_id: str):
    raise HTTPException(status_code=404, detail="Coming soon")

# Part 2: Add backend logic (not called yet)
class ActivityService:
    def get_recent_activity(self, user_id: str):
        return self.repo.get_activity(user_id, limit=50)

# Part 3: Connect (behind flag)
@app.get("/api/v2/users/{user_id}/activity")
async def get_activity(user_id: str):
    if not feature_flags.is_enabled("activity_api"):
        raise HTTPException(status_code=404)
    return activity_service.get_recent_activity(user_id)

# Part 4: Enable flag, monitor, remove flag
```

### Dark Launching

```python
# Deploy to production, but don't expose
# Test with production traffic

async def process_order(order: Order):
    # Current implementation
    result = await current_processor.process(order)

    # Dark launch: run new implementation in parallel
    if feature_flags.is_enabled("dark_launch_new_processor"):
        try:
            new_result = await new_processor.process(order)
            # Compare results, log differences
            if result != new_result:
                logger.warning(f"Result mismatch: {result} vs {new_result}")
        except Exception as e:
            logger.error(f"Dark launch error: {e}")

    # Always return current result
    return result
```

## TBD vs GitFlow

| Aspect | Trunk-Based | GitFlow |
|--------|-------------|---------|
| Main branches | 1 (trunk) | 5+ (main, develop, feature/, release/, hotfix/) |
| Branch lifetime | Hours to 1-2 days | Days to weeks |
| Merge conflicts | Rare, small | Common, large |
| Deployment | Continuous | Scheduled releases |
| Complexity | Simple | Complex |
| Best for | Web apps, SaaS | Mobile apps, packaged software |

## Challenges and Solutions

### "Trunk is Always Broken"

```markdown
## Cause
- Insufficient automated tests
- No pre-commit checks
- Slow CI feedback

## Solutions
1. Gate merges on passing tests
2. Add pre-commit hooks
3. Speed up CI (< 10 min)
4. Use feature flags for incomplete work
5. Smaller commits
```

### "Need Long-Lived Branches"

```markdown
## Cause
- Large features taking weeks
- No feature flag infrastructure
- Compliance requirements

## Solutions
1. Break feature into smaller parts
2. Implement feature flags
3. Use Branch by Abstraction
4. For compliance: release branches only
```

### "Code Review Bottleneck"

```markdown
## Cause
- Large PRs
- Few reviewers
- Async-only review

## Solutions
1. Smaller PRs (< 200 lines)
2. Pair programming (instant review)
3. Fast review SLA (< 4 hours)
4. Rotate reviewers
```

## Metrics

```markdown
## Leading Indicators
- Branch lifetime (target: < 1 day)
- PR size (target: < 200 lines)
- CI time (target: < 10 minutes)
- Review time (target: < 4 hours)

## Lagging Indicators
- Deployment frequency
- Lead time for changes
- Change failure rate
- Time to restore service

## DORA Metrics
TBD correlates with elite DORA performers:
- Deploy on demand (multiple times per day)
- Lead time < 1 hour
- Change failure rate < 15%
- Time to restore < 1 hour
```

## Implementation Roadmap

```markdown
## Phase 1: Foundation (2-4 weeks)
- [ ] Improve test coverage (> 70%)
- [ ] Speed up CI (< 10 min)
- [ ] Add pre-commit hooks
- [ ] Define branch naming conventions

## Phase 2: Short-Lived Branches (2-4 weeks)
- [ ] Set branch lifetime limit (2 days)
- [ ] Implement feature flags
- [ ] Fast code review SLA
- [ ] Monitor branch lifetime

## Phase 3: Continuous Deployment (4-8 weeks)
- [ ] Auto-deploy to staging
- [ ] Implement dark launching
- [ ] Add production monitoring
- [ ] Optional: auto-deploy to prod

## Phase 4: Optimization (ongoing)
- [ ] Track DORA metrics
- [ ] Optimize CI further
- [ ] Reduce feature flag debt
- [ ] Continuous improvement
```

## References

- [Trunk Based Development](https://trunkbaseddevelopment.com/)
- [Accelerate - Nicole Forsgren et al.](https://itrevolution.com/accelerate-book/)
- [Continuous Delivery - Jez Humble](https://continuousdelivery.com/)
- [Feature Flags - Martin Fowler](https://martinfowler.com/articles/feature-toggles.html)
