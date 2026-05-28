# Technology Detection Confidence Configuration

Global confidence scores for technology detection methods.

## Detection Tiers

| Tier | Name | Description |
|------|------|-------------|
| 1 | Quick Detection (SBOM-based) | Fast detection using SBOM package analysis |
| 2 | Deep Detection (File-based) | Slower detection requiring file system scanning |

## Confidence Scores

| Detection Method | Tier | Confidence | Level | Description |
|------------------|------|------------|-------|-------------|
| Package | 1 | 95% | HIGH | Package found in SBOM (npm, pypi, go, maven, rubygems, etc.) |
| File Extension | 2 | 95% | HIGH | Known file extension detected (e.g., .tf, .py, .jsx) |
| Config File | 2 | 90% | HIGH | Known configuration file detected (e.g., terraform.lock.hcl, .eslintrc) |
| Config Directory | 2 | 90% | HIGH | Known configuration directory detected (e.g., .github/workflows, .terraform) |
| Import Statement | 2 | 85% | MEDIUM | Import statement detected in source code |
| Code Pattern | 2 | 80% | MEDIUM | Specific code pattern detected (e.g., API client instantiation) |
| Environment Variable | 2 | 70% | MEDIUM | Environment variable pattern detected in code or config |
| Shebang | 2 | 90% | HIGH | Shebang line indicating language/runtime |

## Confidence Levels

| Level | Range | Description |
|-------|-------|-------------|
| HIGH | 85-100% | Strong indicator - unique to the technology |
| MEDIUM | 70-84% | Moderate indicator - common but not unique |
| LOW | 50-69% | Weak indicator - may have false positives |

## Score Aggregation

When multiple detection methods find the same technology:

**Default Method**: `max` - Use the highest confidence score

**Available Methods**:
- `max` - Use highest score (default)
- `average` - Average all scores
- `bayesian` - Bayesian combination

## Usage Guidelines

### High Confidence Detection

- Package presence in SBOM is most reliable
- File extensions are reliable for language detection
- Config files are reliable for framework detection

### Medium Confidence Detection

- Import statements may be conditional or unused
- Code patterns can have false positives
- Environment variables may be templated

### Low Confidence Detection

- Single weak signals should be combined
- Require multiple indicators before reporting
- Flag as "possible" rather than "detected"
