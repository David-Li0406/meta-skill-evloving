# PROBE Methodology Examples

This document contains detailed examples for the PROBE (PROxy-Based Estimation) methodology used in calibrate-sizing.

## Historical Analysis Example

```yaml
historical_analysis:
  stories_analyzed: N
  date_range: "YYYY-MM-DD to YYYY-MM-DD"

  size_distribution:
    very_small:
      count: N
      estimated_avg: X hours
      actual_avg: Y hours
      variance: (Y-X)/X * 100%

    small:
      count: N
      estimated_avg: X hours
      actual_avg: Y hours
      variance: %

    medium:
      count: N
      estimated_avg: X hours
      actual_avg: Y hours
      variance: %

    large:
      count: N
      estimated_avg: X hours
      actual_avg: Y hours
      variance: %

    very_large:
      count: N
      estimated_avg: X hours
      actual_avg: Y hours
      variance: %
      flag: "Consider breaking down VL stories"
```

## Pattern Analysis Example

```yaml
pattern_analysis:
  overestimation_patterns:
    - pattern: "Backend CRUD operations"
      frequency: "8 of 10 stories"
      typical_variance: "-30%"
      cause: "Reusable patterns established"
      action: "Reduce backend CRUD estimates by 25%"

  underestimation_patterns:
    - pattern: "Third-party integrations"
      frequency: "5 of 6 stories"
      typical_variance: "+45%"
      cause: "Unexpected API complexity"
      action: "Add 40% buffer to integration stories"

  accurate_patterns:
    - pattern: "UI components without API"
      frequency: "90% within 10%"
      cause: "Well understood, good templates"
      action: "Keep current estimation approach"

  technology_factors:
    new_tech_multiplier: 1.5 (actual data)
    familiar_tech_multiplier: 0.9 (actual data)

  complexity_factors:
    high_integration: "+40% actual vs estimated"
    standalone: "-10% actual vs estimated"
```

## Size Calibration Example

```yaml
size_calibration:
  current_definitions:
    very_small:
      old_range: "2-4 hours"
      actual_avg: 3.2 hours
      new_range: "2-4 hours" # No change needed

    small:
      old_range: "4-8 hours"
      actual_avg: 7.8 hours
      new_range: "6-10 hours" # Adjust up

    medium:
      old_range: "8-16 hours"
      actual_avg: 14.5 hours
      new_range: "10-18 hours" # Adjust up

    large:
      old_range: "16-24 hours"
      actual_avg: 22.0 hours
      new_range: "18-26 hours" # Slight adjust

    very_large:
      recommendation: "Split these - too variable"

  story_point_mapping:
    1_point:
      old: "2-4 hours"
      new: "2-4 hours"
    2_points:
      old: "4-8 hours"
      new: "6-10 hours"
    3_points:
      old: "8-16 hours"
      new: "10-18 hours"
    5_points:
      old: "16-24 hours"
      new: "18-26 hours"
    8_points:
      old: ">24 hours"
      new: "SPLIT REQUIRED"
```

## Proxy Updates Example

```yaml
proxy_updates:
  retire_proxies:
    - story: "1.2 - Old login (12h)"
      reason: "Outdated, before auth refactor"

    - story: "2.3 - Legacy API (20h)"
      reason: "No longer representative"

  add_proxies:
    - story: "5.4 - User Profile (14h)"
      category: "medium_ui_with_api"
      characteristics: "Form, validation, API calls"

    - story: "6.2 - Data Export (8h)"
      category: "small_backend"
      characteristics: "Query, transform, return"

  proxy_categories:
    ui_simple:
      proxies: ["4.1 (6h)", "5.2 (7h)"]
      avg: 6.5 hours

    ui_with_api:
      proxies: ["3.4 (14h)", "5.4 (14h)", "6.1 (16h)"]
      avg: 14.7 hours

    backend_crud:
      proxies: ["2.5 (8h)", "3.2 (9h)", "4.3 (7h)"]
      avg: 8.0 hours

    integration:
      proxies: ["3.6 (22h)", "5.7 (26h)"]
      avg: 24.0 hours
```

## Regression Model Example

Use when sufficient data (>30 stories) is available:

```yaml
regression_analysis:
  model_parameters:
    intercept: 2.5 hours (base overhead)

    factors:
      acceptance_criteria: 1.2 hours per AC
      api_endpoints: 2.5 hours per endpoint
      ui_components: 3.0 hours per component
      database_tables: 1.5 hours per table
      integration_points: 4.0 hours per integration

  formula: |
    estimated_hours = 2.5
      + (1.2 * num_acs)
      + (2.5 * num_endpoints)
      + (3.0 * num_components)
      + (1.5 * num_tables)
      + (4.0 * num_integrations)

  model_accuracy:
    r_squared: 0.78
    mean_error: 2.1 hours
    confidence: "Use as guidance, not absolute"
```

## Calibration Record Example

```yaml
calibration_record:
  date: "YYYY-MM-DD"
  stories_analyzed: N

  adjustments_made:
    size_ranges:
      - category: "small"
        old: "4-8h"
        new: "6-10h"

    proxy_changes:
      added: N
      retired: M

    patterns_identified: P

  accuracy_improvement:
    before_calibration: X%
    after_calibration: Y% (projected)

  next_calibration: "After 10 more stories"
```

## Recommendations Structure

```yaml
recommendations:
  immediate_actions:
    - action: "Update size category definitions in PROBE task"
      impact: "Better size alignment"

    - action: "Add 40% buffer to integration stories"
      impact: "Reduce underestimation"

    - action: "Reduce backend CRUD estimates by 25%"
      impact: "Avoid overestimation"

  process_improvements:
    - action: "Flag VL stories for automatic split review"
      impact: "Maintain flow efficiency"

    - action: "Require integration checklist for external APIs"
      impact: "Better risk assessment"

  training_needs:
    - topic: "New framework requires 50% more time"
      audience: "All estimators"

    - topic: "UI complexity factors"
      audience: "Frontend team"
```

## Calibration Report Template

```markdown
# Sizing Calibration Report

## Executive Summary
- Stories Analyzed: N
- Overall Accuracy: X%
- Key Finding: {main pattern}
- Action: {primary change}

## Size Category Performance

| Category | Count | Est Avg | Actual Avg | Variance |
|----------|-------|---------|------------|----------|
| VS       | N     | X hrs   | Y hrs      | Z%       |
| S        | N     | X hrs   | Y hrs      | Z%       |
| M        | N     | X hrs   | Y hrs      | Z%       |
| L        | N     | X hrs   | Y hrs      | Z%       |

## Pattern Analysis

### Overestimation
- Backend CRUD: -30% consistently
- Action: Reduce estimates by 25%

### Underestimation
- Integrations: +45% consistently
- Action: Add 40% buffer

## Updated Sizing Guide

### New Ranges
- Very Small: 2-4 hours (unchanged)
- Small: 6-10 hours (was 4-8)
- Medium: 10-18 hours (was 8-16)
- Large: 18-26 hours (was 16-24)
- Very Large: SPLIT REQUIRED

## Recommendations

1. Update PROBE task with new ranges
2. Train team on integration complexity
3. Flag all 8-point stories for split review
4. Use regression model for complex stories

## Next Steps
- Apply calibrations immediately
- Monitor next 10 stories closely
- Recalibrate after 10 completions
```
