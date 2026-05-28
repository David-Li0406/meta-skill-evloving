---
name: probabilistic-data-handling
description: Pattern for handling incomplete data (especially unknown birth times) with probabilistic calculations. Use when implementing modules that need to provide intelligent estimates instead of "Unknown" when data is missing.
---

# Probabilistic Data Handling

Pattern for intelligent handling of incomplete input data. Instead of returning "Unknown" when data is missing, sample possible values and return probability distributions.

## When to Use

- Module requires data that may not be provided (e.g., birth time)
- Output varies significantly based on missing data
- Users benefit from seeing possible outcomes with confidence levels
- Want to show "what you know" vs "what requires exact data"

## Core Pattern

### 1. Schema - Add Probability Type
```python
from pydantic import BaseModel
from typing import Literal

class ThingProbability(BaseModel):
    """Probability of a specific outcome."""
    value: str  # The outcome (e.g., "Projector", "Virgo Rising")
    probability: float  # 0.0 to 1.0
    sample_count: int  # Number of samples showing this outcome
    confidence: Literal["certain", "high", "medium", "low"]
```

### 2. Schema - Add Stability Type (optional)
```python
class DataPointStability(BaseModel):
    """Tracks if a data point is stable across all samples."""
    name: str  # e.g., "Sun", "Moon"
    value: str  # Most common value
    stable: bool  # True if same in ALL samples
    variation: str | None  # Description if varies
```

### 3. Calculator - Sample Across Possibilities
```python
def _calculate_probabilistic(
    date: date,
    location_lat: float,
    location_lng: float,
    timezone: str
) -> dict:
    """Sample 24 hours to determine probability distribution."""
    from collections import Counter
    
    outcome_counts = Counter()
    
    for hour in range(24):
        result = calculate_for_time(date, time(hour, 0), ...)
        outcome_counts[result.key_value] += 1
    
    total_samples = sum(outcome_counts.values())
    
    probabilities = []
    for value, count in outcome_counts.most_common():
        prob = count / total_samples
        confidence = "certain" if prob >= 1.0 else \
                    "high" if prob >= 0.75 else \
                    "medium" if prob >= 0.5 else "low"
        
        probabilities.append({
            "value": value,
            "probability": round(prob, 3),
            "sample_count": count,
            "confidence": confidence
        })
    
    most_likely = outcome_counts.most_common(1)[0]
    return {
        "most_likely": most_likely[0],
        "confidence": most_likely[1] / total_samples,
        "probabilities": probabilities
    }
```

### 4. Main Function - Handle Missing Data
```python
def calculate_something(
    name: str,
    date: date,
    time: time | None,  # May be None!
    location: Location
) -> Result:
    if time is None:
        # Use probabilistic calculation
        prob_data = _calculate_probabilistic(date, location.lat, ...)
        return Result(
            value=prob_data["most_likely"],
            accuracy="probabilistic",
            confidence=prob_data["confidence"],
            probabilities=prob_data["probabilities"],
            note=f"Most likely {prob_data['most_likely']} with {prob_data['confidence']:.0%} confidence"
        )
    else:
        # Full calculation
        return _calculate_full(name, date, time, location)
```

## Accuracy Levels

Always return `accuracy` field:
- `"full"` - All data provided, result is certain
- `"probabilistic"` - Key data missing, result is most likely outcome
- `"partial"` - Some data missing, limited analysis possible

## Confidence Thresholds

Use consistent thresholds:
| Confidence | Probability Range |
|------------|-------------------|
| `certain` | 100% |
| `high` | 75-99% |
| `medium` | 50-74% |
| `low` | <50% |

## Critical Checklist

- [ ] Added `ThingProbability` schema for probability data
- [ ] Made optional fields `Optional` in main result schema
- [ ] Added `accuracy: Literal["full", "probabilistic", "partial"]`
- [ ] Added `confidence: Optional[float]` to result
- [ ] Added `probabilities: Optional[list[ThingProbability]]`
- [ ] Implemented `_calculate_probabilistic` sampling function
- [ ] Handle edge case where all samples fail
- [ ] Include human-readable `note` explaining confidence

## GUTTERS Modules Using This Pattern

- **Human Design** - Type probabilities when birth time unknown
- **Astrology** - Rising sign, house, aspect stability
- **Future: Transits** - Event timing windows

## Gotchas

- Sample 24 hours minimum (one per hour)
- Handle cases where calculation fails for some hours
- Counter-based aggregation is efficient for categorical data
- For continuous data (degrees), consider ranges instead
