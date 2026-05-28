# Audit Logging

Track enumerator behavior during form completion.

## Overview

Audit logging captures:
- Navigation patterns
- Time spent on questions
- Location data
- Answer changes
- Enumerator identity

Useful for:
- Data quality assurance
- Performance monitoring
- Fraud detection
- Training needs assessment

---

## Enabling Audit Logging

Add to survey sheet:

| type | name |
|------|------|
| audit | audit |

**Note:** Only one audit row per form.

---

## Configuration Parameters

Add parameters column:

| type | name | parameters |
|------|------|------------|
| audit | audit | location-priority=balanced location-min-interval=60 location-max-age=120 |

### Location Tracking

| Parameter | Description |
|-----------|-------------|
| `location-priority` | Accuracy level |
| `location-min-interval` | Seconds between updates |
| `location-max-age` | Max seconds for cached locations |

### Location Priority Options

| Value | Description |
|-------|-------------|
| `high-accuracy` | Best GPS accuracy |
| `balanced` | ~100 meters accuracy |
| `low-power` | ~10 kilometers accuracy |
| `no-power` | Cached locations only |

### Change Tracking

| Parameter | Description |
|-----------|-------------|
| `track-changes=true` | Record old/new values |
| `track-changes-reasons=on-form-edit` | Require justification for edits |
| `identify-user=true` | Prompt for enumerator identity |

---

## Full Configuration Example

| type | name | parameters |
|------|------|------------|
| audit | audit | location-priority=balanced location-min-interval=60 location-max-age=120 track-changes=true track-changes-reasons=on-form-edit identify-user=true |

---

## Audit Log Contents

Generated `audit.csv` file contains:

| Column | Description |
|--------|-------------|
| `event` | Event type |
| `node` | Question reference |
| `start` | Event start (ms since epoch) |
| `end` | Event end (ms since epoch) |
| `latitude` | GPS latitude (if enabled) |
| `longitude` | GPS longitude (if enabled) |
| `accuracy` | GPS accuracy in meters |
| `old-value` | Previous answer (if track-changes) |
| `new-value` | New answer (if track-changes) |

### Event Types

| Event | Description |
|-------|-------------|
| `form start` | Form opened |
| `form exit` | Form closed |
| `form save` | Form saved |
| `form finalize` | Form marked complete |
| `question` | Question viewed |
| `group questions` | Group displayed |
| `jump` | Navigation jump |
| `add repeat` | Repeat instance added |
| `delete repeat` | Repeat instance deleted |
| `end screen` | End of form reached |
| `constraint error` | Validation failed |
| `location permissions granted` | GPS permission given |
| `location providers enabled` | GPS enabled |

---

## Timestamp Security

- Initial timestamp uses device time
- Subsequent timestamps calculated from elapsed time
- Prevents timestamp manipulation within session

---

## Example Analysis Use Cases

### Time per Question

Calculate `end - start` for question events to identify:
- Questions taking too long (confusion)
- Questions answered too quickly (skipping)

### Navigation Patterns

Track `jump` events to identify:
- Form sections being skipped
- Unusual navigation patterns

### Location Verification

Compare audit locations with captured geopoints:
- Verify enumerator was at claimed location
- Detect fabricated data

### Change Analysis

Review `old-value` and `new-value` to identify:
- Frequent corrections (training needs)
- Suspicious changes (data manipulation)

---

## Best Practices

### Balance Accuracy and Battery

- Use `balanced` for most cases
- Use `high-accuracy` only when needed
- Set reasonable intervals (60+ seconds)

### Storage Considerations

- Audit logs can be large
- More parameters = larger files
- Plan for storage and bandwidth

### Privacy

- Audit logs contain sensitive data
- Restrict access appropriately
- Consider data retention policies

### Analysis Planning

- Define analysis goals before enabling
- Not all parameters needed for all projects
- Test with sample data first
