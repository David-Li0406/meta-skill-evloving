# Fidelity Assessment Categories

## Exact Match
Implementation precisely matches specification requirements. No deviations detected.

## Minor Deviation
Small differences from spec with no functional impact:
- Different variable names (but consistent with codebase style)
- Minor refactoring for code quality
- Improved error messages
- Additional logging or comments

## Major Deviation
Significant differences affecting functionality or architecture:
- Different API signatures than specified
- Missing required features
- Different data structures
- Changed control flow or logic

## Missing Functionality
Specified features not implemented:
- Required functions missing
- Incomplete implementation
- Skipped acceptance criteria

---

## Success Criteria

A successful fidelity review:
- Compares all specified requirements against implementation
- Identifies and categorizes deviations accurately
- Assesses impact of deviations
- Provides actionable recommendations
- Generates clear, structured report
- Automatically saves to `specs/.fidelity-reviews/` directory
- Documents findings for future reference
