---
id: ab-testing
name: "A/B Testing"
domain: DEV
skill: faion-software-developer
category: "development"
---

# A/B Testing

## Overview

A/B testing (split testing) compares two or more variants of a feature to determine which performs better based on defined metrics. It enables data-driven decisions about product changes while minimizing risk.

## When to Use

- Testing UI/UX changes (button colors, layouts, copy)
- Evaluating new features before full rollout
- Optimizing conversion funnels
- Pricing experiments
- Algorithm improvements (search, recommendations)

## Key Principles

- **Statistical significance**: Don't conclude until you have enough data
- **One variable at a time**: Isolate what you're testing
- **Clear hypothesis**: Define expected outcomes before testing
- **Minimize experiment interactions**: Avoid users in multiple conflicting tests
- **Document everything**: Results, learnings, decisions made

## Best Practices

### Experiment Design

```python
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import uuid

class ExperimentStatus(Enum):
    DRAFT = "draft"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


@dataclass
class Variant:
    name: str
    allocation: float  # 0.0 to 1.0
    description: str = ""


@dataclass
class Metric:
    name: str
    type: str  # "conversion", "continuous", "count"
    primary: bool = False
    direction: str = "increase"  # "increase" or "decrease"


@dataclass
class Experiment:
    id: str
    name: str
    hypothesis: str
    variants: list[Variant]
    metrics: list[Metric]
    status: ExperimentStatus = ExperimentStatus.DRAFT
    target_sample_size: int = 1000
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    owner: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)

    def validate(self) -> list[str]:
        """Validate experiment configuration."""
        errors = []

        # Check variant allocations sum to 1
        total_allocation = sum(v.allocation for v in self.variants)
        if abs(total_allocation - 1.0) > 0.001:
            errors.append(f"Variant allocations must sum to 1.0, got {total_allocation}")

        # Check at least 2 variants
        if len(self.variants) < 2:
            errors.append("Experiment must have at least 2 variants")

        # Check at least one metric
        if not self.metrics:
            errors.append("Experiment must have at least one metric")

        # Check exactly one primary metric
        primary_count = sum(1 for m in self.metrics if m.primary)
        if primary_count != 1:
            errors.append(f"Must have exactly one primary metric, got {primary_count}")

        return errors


# Example experiment definition
checkout_experiment = Experiment(
    id="exp-checkout-v2-2024",
    name="New Checkout Flow",
    hypothesis="The simplified checkout flow will increase conversion rate by 15%",
    variants=[
        Variant("control", 0.5, "Current checkout flow"),
        Variant("treatment", 0.5, "Simplified single-page checkout"),
    ],
    metrics=[
        Metric("checkout_conversion", "conversion", primary=True),
        Metric("cart_abandonment", "conversion", direction="decrease"),
        Metric("time_to_complete", "continuous", direction="decrease"),
        Metric("revenue_per_visitor", "continuous"),
    ],
    target_sample_size=10000,
    owner="checkout-team",
)
```

### Experiment Assignment

```python
import hashlib
from typing import Optional

class ExperimentAssigner:
    """Assigns users to experiment variants deterministically."""

    def __init__(self, experiments: dict[str, Experiment]):
        self.experiments = experiments

    def get_variant(
        self,
        experiment_id: str,
        user_id: str,
        override: Optional[str] = None
    ) -> Optional[str]:
        """Get assigned variant for a user in an experiment."""
        experiment = self.experiments.get(experiment_id)
        if not experiment:
            return None

        if experiment.status != ExperimentStatus.RUNNING:
            return None

        # Allow overrides for testing
        if override and any(v.name == override for v in experiment.variants):
            return override

        # Deterministic assignment using hash
        hash_key = f"{experiment_id}:{user_id}"
        hash_value = int(hashlib.md5(hash_key.encode()).hexdigest(), 16)
        bucket = (hash_value % 10000) / 10000.0

        # Assign to variant based on allocation
        cumulative = 0.0
        for variant in experiment.variants:
            cumulative += variant.allocation
            if bucket < cumulative:
                return variant.name

        return experiment.variants[-1].name

    def get_all_assignments(self, user_id: str) -> dict[str, str]:
        """Get all experiment assignments for a user."""
        assignments = {}
        for exp_id, experiment in self.experiments.items():
            variant = self.get_variant(exp_id, user_id)
            if variant:
                assignments[exp_id] = variant
        return assignments


# Usage
assigner = ExperimentAssigner({"checkout-v2": checkout_experiment})

# Get user's variant
variant = assigner.get_variant("checkout-v2", user_id="user-123")

if variant == "treatment":
    render_new_checkout()
else:
    render_old_checkout()
```

### Event Tracking

```python
from datetime import datetime
from dataclasses import dataclass
import json

@dataclass
class ExperimentEvent:
    """Event for experiment analytics."""
    experiment_id: str
    variant: str
    user_id: str
    event_type: str  # "exposure", "conversion", "metric"
    metric_name: Optional[str] = None
    metric_value: Optional[float] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    properties: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "experiment_id": self.experiment_id,
            "variant": self.variant,
            "user_id": self.user_id,
            "event_type": self.event_type,
            "metric_name": self.metric_name,
            "metric_value": self.metric_value,
            "timestamp": self.timestamp.isoformat(),
            "properties": self.properties,
        }


class ExperimentTracker:
    """Track experiment events and exposures."""

    def __init__(self, analytics_client, assigner: ExperimentAssigner):
        self.analytics = analytics_client
        self.assigner = assigner
        self._exposures: set[tuple[str, str]] = set()

    def track_exposure(self, experiment_id: str, user_id: str):
        """Track that a user was exposed to an experiment."""
        # Deduplicate exposures
        key = (experiment_id, user_id)
        if key in self._exposures:
            return

        variant = self.assigner.get_variant(experiment_id, user_id)
        if not variant:
            return

        self._exposures.add(key)

        event = ExperimentEvent(
            experiment_id=experiment_id,
            variant=variant,
            user_id=user_id,
            event_type="exposure",
        )
        self.analytics.track("experiment_exposure", event.to_dict())

    def track_conversion(
        self,
        experiment_id: str,
        user_id: str,
        metric_name: str,
        value: float = 1.0,
        properties: dict = None
    ):
        """Track a conversion event for an experiment."""
        variant = self.assigner.get_variant(experiment_id, user_id)
        if not variant:
            return

        event = ExperimentEvent(
            experiment_id=experiment_id,
            variant=variant,
            user_id=user_id,
            event_type="conversion",
            metric_name=metric_name,
            metric_value=value,
            properties=properties or {},
        )
        self.analytics.track("experiment_conversion", event.to_dict())


# Usage
tracker = ExperimentTracker(analytics_client, assigner)

# Track exposure when showing variant
@app.get("/checkout")
async def checkout(user_id: str):
    variant = assigner.get_variant("checkout-v2", user_id)
    tracker.track_exposure("checkout-v2", user_id)

    if variant == "treatment":
        return render_new_checkout()
    return render_old_checkout()


# Track conversion
@app.post("/checkout/complete")
async def complete_checkout(user_id: str, order: Order):
    # Process order...

    # Track conversion
    tracker.track_conversion(
        "checkout-v2",
        user_id,
        "checkout_conversion",
        value=1.0,
        properties={"order_value": float(order.total)}
    )
```

### Statistical Analysis

```python
import numpy as np
from scipy import stats
from dataclasses import dataclass
from typing import Optional

@dataclass
class VariantStats:
    """Statistics for a single variant."""
    name: str
    sample_size: int
    conversions: int = 0
    conversion_rate: float = 0.0
    mean: float = 0.0
    std: float = 0.0
    confidence_interval: tuple[float, float] = (0.0, 0.0)


@dataclass
class ExperimentResults:
    """Results of an A/B test analysis."""
    experiment_id: str
    metric_name: str
    control: VariantStats
    treatment: VariantStats
    relative_lift: float
    p_value: float
    is_significant: bool
    confidence_level: float
    power: float
    sample_size_needed: int


class ExperimentAnalyzer:
    """Analyze A/B test results."""

    def __init__(self, confidence_level: float = 0.95):
        self.confidence_level = confidence_level
        self.alpha = 1 - confidence_level

    def analyze_conversion(
        self,
        experiment_id: str,
        metric_name: str,
        control_conversions: int,
        control_total: int,
        treatment_conversions: int,
        treatment_total: int,
    ) -> ExperimentResults:
        """Analyze conversion rate experiment."""
        # Calculate rates
        control_rate = control_conversions / control_total if control_total > 0 else 0
        treatment_rate = treatment_conversions / treatment_total if treatment_total > 0 else 0

        # Relative lift
        lift = (treatment_rate - control_rate) / control_rate if control_rate > 0 else 0

        # Z-test for proportions
        pooled_rate = (control_conversions + treatment_conversions) / (control_total + treatment_total)
        pooled_se = np.sqrt(pooled_rate * (1 - pooled_rate) * (1/control_total + 1/treatment_total))

        if pooled_se > 0:
            z_score = (treatment_rate - control_rate) / pooled_se
            p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
        else:
            p_value = 1.0

        # Confidence intervals
        control_ci = self._proportion_ci(control_conversions, control_total)
        treatment_ci = self._proportion_ci(treatment_conversions, treatment_total)

        # Power calculation
        power = self._calculate_power(
            control_rate, treatment_rate, control_total, treatment_total
        )

        # Sample size for 80% power
        min_sample = self._sample_size_for_power(
            control_rate, lift, power=0.80
        )

        return ExperimentResults(
            experiment_id=experiment_id,
            metric_name=metric_name,
            control=VariantStats(
                name="control",
                sample_size=control_total,
                conversions=control_conversions,
                conversion_rate=control_rate,
                confidence_interval=control_ci,
            ),
            treatment=VariantStats(
                name="treatment",
                sample_size=treatment_total,
                conversions=treatment_conversions,
                conversion_rate=treatment_rate,
                confidence_interval=treatment_ci,
            ),
            relative_lift=lift,
            p_value=p_value,
            is_significant=p_value < self.alpha,
            confidence_level=self.confidence_level,
            power=power,
            sample_size_needed=min_sample,
        )

    def _proportion_ci(
        self,
        successes: int,
        total: int
    ) -> tuple[float, float]:
        """Calculate Wilson confidence interval for proportion."""
        if total == 0:
            return (0.0, 0.0)

        z = stats.norm.ppf(1 - self.alpha / 2)
        p = successes / total
        n = total

        denominator = 1 + z**2 / n
        center = (p + z**2 / (2*n)) / denominator
        margin = z * np.sqrt((p * (1-p) + z**2 / (4*n)) / n) / denominator

        return (max(0, center - margin), min(1, center + margin))

    def _calculate_power(
        self,
        p1: float,
        p2: float,
        n1: int,
        n2: int
    ) -> float:
        """Calculate statistical power."""
        if n1 == 0 or n2 == 0:
            return 0.0

        effect_size = abs(p2 - p1) / np.sqrt(p1 * (1 - p1))
        pooled_n = 2 / (1/n1 + 1/n2)

        z_alpha = stats.norm.ppf(1 - self.alpha / 2)
        z_power = effect_size * np.sqrt(pooled_n / 2) - z_alpha

        return stats.norm.cdf(z_power)

    def _sample_size_for_power(
        self,
        baseline_rate: float,
        minimum_detectable_effect: float,
        power: float = 0.80
    ) -> int:
        """Calculate required sample size per variant."""
        if baseline_rate == 0 or minimum_detectable_effect == 0:
            return 0

        effect_rate = baseline_rate * (1 + minimum_detectable_effect)

        z_alpha = stats.norm.ppf(1 - self.alpha / 2)
        z_beta = stats.norm.ppf(power)

        p_avg = (baseline_rate + effect_rate) / 2
        n = 2 * ((z_alpha + z_beta) ** 2) * p_avg * (1 - p_avg) / (effect_rate - baseline_rate) ** 2

        return int(np.ceil(n))


# Usage
analyzer = ExperimentAnalyzer(confidence_level=0.95)

results = analyzer.analyze_conversion(
    experiment_id="checkout-v2",
    metric_name="checkout_conversion",
    control_conversions=245,
    control_total=5000,
    treatment_conversions=290,
    treatment_total=5000,
)

print(f"Control conversion rate: {results.control.conversion_rate:.2%}")
print(f"Treatment conversion rate: {results.treatment.conversion_rate:.2%}")
print(f"Relative lift: {results.relative_lift:.2%}")
print(f"P-value: {results.p_value:.4f}")
print(f"Statistically significant: {results.is_significant}")
print(f"Power: {results.power:.2%}")
```

### Reporting Dashboard Data

```python
from datetime import datetime, timedelta

class ExperimentReporter:
    """Generate experiment reports and dashboards."""

    def __init__(self, db, analyzer: ExperimentAnalyzer):
        self.db = db
        self.analyzer = analyzer

    def get_experiment_summary(self, experiment_id: str) -> dict:
        """Get summary data for an experiment."""
        # Get exposure and conversion data
        exposures = self._get_exposures(experiment_id)
        conversions = self._get_conversions(experiment_id)

        # Calculate metrics per variant
        variants_data = {}
        for variant, data in exposures.items():
            variant_conversions = conversions.get(variant, {})
            variants_data[variant] = {
                "exposures": data["count"],
                "unique_users": data["unique_users"],
                "conversions": variant_conversions.get("count", 0),
                "conversion_rate": (
                    variant_conversions.get("count", 0) / data["unique_users"]
                    if data["unique_users"] > 0 else 0
                ),
            }

        # Run statistical analysis
        if "control" in variants_data and "treatment" in variants_data:
            results = self.analyzer.analyze_conversion(
                experiment_id=experiment_id,
                metric_name="primary",
                control_conversions=variants_data["control"]["conversions"],
                control_total=variants_data["control"]["unique_users"],
                treatment_conversions=variants_data["treatment"]["conversions"],
                treatment_total=variants_data["treatment"]["unique_users"],
            )
        else:
            results = None

        return {
            "experiment_id": experiment_id,
            "variants": variants_data,
            "analysis": {
                "lift": results.relative_lift if results else None,
                "p_value": results.p_value if results else None,
                "is_significant": results.is_significant if results else False,
                "power": results.power if results else None,
            } if results else None,
            "generated_at": datetime.utcnow().isoformat(),
        }

    def get_daily_metrics(
        self,
        experiment_id: str,
        days: int = 14
    ) -> list[dict]:
        """Get daily metrics for trend analysis."""
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=days)

        daily_data = []
        current = start_date

        while current <= end_date:
            day_data = self._get_day_metrics(experiment_id, current)
            daily_data.append({
                "date": current.isoformat(),
                **day_data
            })
            current += timedelta(days=1)

        return daily_data
```

## Anti-patterns

- **Peeking at results**: Checking significance before enough data
- **Multiple testing**: Running many tests without correction
- **Changing experiment mid-run**: Modifying allocation or variants
- **No hypothesis**: Testing without expected outcomes
- **Ignoring segments**: Missing important subgroup differences
- **Too small sample**: Underpowered experiments

## References

- [Trustworthy Online Controlled Experiments](https://www.cambridge.org/core/books/trustworthy-online-controlled-experiments/D97B26382EB0EB2DC2019A7A7B518F59)
- [Optimizely Stats Engine](https://www.optimizely.com/optimization-glossary/statistical-significance/)
- [Evan Miller A/B Testing Calculator](https://www.evanmiller.org/ab-testing/)
- [Google Analytics Experiments](https://support.google.com/analytics/answer/1745147)
