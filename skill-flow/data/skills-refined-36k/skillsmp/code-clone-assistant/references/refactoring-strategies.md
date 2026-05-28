**Skill**: [Code Clone Assistant](../SKILL.md)


______________________________________________________________________

## Security

**Allowed Tools**: `Read, Grep, Bash, Edit, Write`

**Safe Refactoring**:

- Only refactor after user approval
- Run tests before marking complete
- Never use destructive commands
- Preserve git history
- Validate file paths before editing

______________________________________________________________________

## Detailed Documentation

For comprehensive details, see:

- **PMD CPD Reference**: `reference-pmd.md` - Commands, options, exclusions, error handling
- **Semgrep Reference**: `reference-semgrep.md` - Rules, patterns, advanced features
- **Examples**: `examples.md` - Real-world examples, complementary detection scenarios
- **Sample Rules**: `clone-rules.yaml` - Ready-to-use Semgrep patterns

______________________________________________________________________

## Installation

```bash
# Check installation
which pmd      # Should be /opt/homebrew/bin/pmd
which semgrep  # Should be /opt/homebrew/bin/semgrep

# Install if missing
brew install pmd      # PMD v7.17.0+
brew install semgrep  # Semgrep v1.140.0+
```

______________________________________________________________________

## Testing Results

**Test Date**: October 26, 2025
**Files Tested**: 3 files (sample1.py, sample2.py, sample.js)

**Results**:

- PMD CPD: 9 exact duplications
- Semgrep: 21 pattern violations
- Total Unique: ~27 DRY violations
- Coverage: 3x more than either tool alone

______________________________________________________________________

**This skill uses only tested commands validated in October 2025 with PMD CPD and Semgrep**
