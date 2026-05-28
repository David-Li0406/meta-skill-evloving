# YARA-Forge

YARA-Forge provides open-source YARA rule bundles from multiple community projects, curated by Nextron Systems.

**Project**: https://yarahq.github.io/

## Overview

YARA-Forge rules supplement THOR's commercial signatures with community-contributed detections. They're maintained separately and can be added/removed independently.

## Available Rulesets

| Ruleset | False Positive Rate | Detection Coverage | Use Case |
|---------|--------------------|--------------------|----------|
| `core` | Minimal | Good | Production environments |
| `extended` | Balanced | Better | General use |
| `full` | Higher | Maximum | Lab/research |

## Commands

### Download Ruleset

```bash
# Download core ruleset (recommended for production)
thor-util yara-forge download --ruleset core

# Download extended ruleset (balanced)
thor-util yara-forge download --ruleset extended

# Download full ruleset (maximum coverage)
thor-util yara-forge download --ruleset full
```

### Remove YARA-Forge Rules

```bash
thor-util yara-forge remove
```

## Behavior

- Only **one ruleset** active at a time
- New download overwrites previous ruleset
- Rules stored in: `./custom-signatures/yara-forge/`
- Auto-updated with `thor-util update`
- Does not affect commercial THOR signatures

## Choosing a Ruleset

### core (Recommended for Production)

- Minimal false positive rate
- Rules thoroughly tested
- Good detection for known threats
- Safe for automated/unattended scans

### extended (General Use)

- Balanced FP vs detection tradeoff
- Includes more experimental rules
- Good for investigations with manual review
- Default recommendation for most users

### full (Lab/Research Only)

- Maximum detection coverage
- Higher false positive rate
- Includes aggressive/experimental rules
- Requires manual review of findings
- Not recommended for production sweeps

## Integration with THOR Signatures

YARA-Forge rules are stored in `custom-signatures/yara-forge/` and loaded alongside:
- Commercial THOR signatures (`./signatures/`)
- Your custom signatures (`./custom-signatures/`)

The three sources combine for maximum coverage.

## Update Behavior

When you run `thor-util update`:
1. Commercial signatures updated
2. YARA-Forge rules updated (if installed)
3. Custom signatures unchanged

## Troubleshooting

### Too Many False Positives

```bash
# Switch to more conservative ruleset
thor-util yara-forge download --ruleset core

# Or remove YARA-Forge entirely
thor-util yara-forge remove
```

### Missing Recent Threats

```bash
# Switch to broader ruleset
thor-util yara-forge download --ruleset extended

# Or full for maximum coverage (expect FPs)
thor-util yara-forge download --ruleset full
```

### Rules Not Loading

1. Check `./custom-signatures/yara-forge/` exists
2. Run `thor-util update` to refresh
3. Verify no syntax errors in THOR startup log

## Best Practices

1. **Production environments**: Use `core` ruleset
2. **Incident response**: Use `extended` for broader coverage
3. **Threat hunting/research**: Consider `full` with manual review
4. **Keep updated**: Rules auto-update with `thor-util update`
5. **Review findings**: YARA-Forge rules may need more context than commercial signatures

## Filtering YARA-Forge Detections

If specific YARA-Forge rules cause issues:

```bash
# Filter at runtime
thor64.exe --init-filter YARA_FORGE_RuleName -p C:\

# Or add to false_positive_filters.cfg
echo "YARA_FORGE_RuleName;.*" >> ./config/false_positive_filters.cfg
```
