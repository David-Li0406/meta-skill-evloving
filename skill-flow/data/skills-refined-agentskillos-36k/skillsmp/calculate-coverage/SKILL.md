---
name: calculate-coverage
description: Calculate code coverage for .NET projects using local coverage scripts. Use when user asks to calculate coverage, check coverage, coverage metrics, test coverage. For NEW CODE coverage (what SonarCloud Quality Gate checks), use when user says "new code coverage", "coverage on new code", "changed code coverage", "feature branch coverage". For OVERALL coverage, use when user says "overall coverage", "total coverage", "full coverage", "complete coverage".
allowed-tools: Bash, Read
---

# Code Coverage Calculator

## Purpose
Calculate and report code coverage metrics for .NET projects using:
- `calculate-coverage.sh` - **Overall** coverage (all code in the project)
- `calculate-coverage-new-code.sh` - **New code** coverage (changed/modified code vs base branch)

Both scripts match the exact CI pipeline methodology.

## When to Activate
Activate this skill when the user mentions coverage-related keywords.

### Coverage Mode Detection
Determine which script to run based on user intent:

**NEW CODE Coverage (calculate-coverage-new-code.sh):**
- User explicitly says: "new code", "changed code", "modified code", "feature branch coverage"
- User is on a feature branch and says "calculate coverage" (smart default)

**OVERALL Coverage (calculate-coverage.sh):**
- User explicitly says: "overall", "total", "full", "complete", "all code"
- User is on main/master branch and says "calculate coverage" (smart default)

### Smart Default Detection
When user says just "calculate coverage" without specifying:
```bash
CURRENT_BRANCH=$(git branch --show-current)
if [[ "$CURRENT_BRANCH" == "main" || "$CURRENT_BRANCH" == "master" ]]; then
    # Run overall coverage
    ./calculate-coverage.sh
else
    # Run new code coverage (feature branch)
    ./calculate-coverage-new-code.sh
fi
```

## Instructions

### 1. Determine Which Script to Run

Follow the Coverage Mode Detection logic above to determine which script to run.

### 2. Locate the Coverage Scripts

Both scripts are typically in the project root:
- `./calculate-coverage.sh` - Overall coverage
- `./calculate-coverage-new-code.sh` - New code coverage

### 3. Execute Coverage Calculation

**For OVERALL Coverage:**
```bash
# Standard execution
./calculate-coverage.sh

# With HTML report auto-open
./calculate-coverage.sh --html

# Skip build if already built
./calculate-coverage.sh --no-build

# Verbose output for debugging
./calculate-coverage.sh --verbose
```

**For NEW CODE Coverage:**
```bash
# Standard execution (compares against main)
./calculate-coverage-new-code.sh

# Compare against different base branch
./calculate-coverage-new-code.sh --base develop

# With HTML report auto-open
./calculate-coverage-new-code.sh --html

# Skip build if already built
./calculate-coverage-new-code.sh --no-build

# Verbose output for debugging
./calculate-coverage-new-code.sh --verbose
```

**Timeout:** Allow up to 10 minutes (600000ms) for large projects.

### 4. Present Results

After execution, present the coverage results in a clear format:

**For OVERALL Coverage:**
```
=== Overall Code Coverage Report ===

Overall Metrics:
- Line Coverage:   XX.X% (covered/total)
- Branch Coverage: XX.X% (covered/total)

Coverage Status: [PASS/FAIL] (threshold: 80%)

Top Areas Needing Coverage:
1. ClassName - XX.X%
2. ClassName - XX.X%
3. ClassName - XX.X%

Generated Reports:
- HTML:      ./coverage/index.html
- SonarQube: ./coverage/SonarQube.xml
```

**For NEW CODE Coverage:**
```
=== New Code Coverage Report (vs main) ===

Changed Source Files:
- File1.cs
- File2.cs

Coverage by File:
  File1.cs    XX/XX lines (XX.X%)
  File2.cs    XX/XX lines (XX.X%)

Summary:
- Total new/modified lines: XX
- Covered lines:            XX
- NEW CODE COVERAGE:        XX.XX%

Quality Gate: [PASS/FAIL] (threshold: 80%)
```

### 5. Provide Recommendations

Based on coverage results:

**For OVERALL Coverage:**
- **If >= 80%:** Congratulate on good coverage, suggest maintaining as code evolves
- **If 60-79%:** Identify lowest coverage areas, focus on critical business logic
- **If < 60%:** Flag as needing immediate attention, list top 5-10 files with lowest coverage

**For NEW CODE Coverage:**
- **If >= 80%:** Pass Quality Gate - safe to merge
- **If < 80%:** Fail Quality Gate - show files needing more tests and how many lines need coverage

## Error Handling

### Script Not Found
If coverage scripts are not found:
1. Inform the user which script is missing
2. For overall coverage, suggest running:
   ```bash
   dotnet test --collect:"XPlat Code Coverage"
   ```
3. For new code coverage, suggest checking the project root for `calculate-coverage-new-code.sh`

### Prerequisites Missing
If reportgenerator is not installed:
```bash
dotnet tool install --global dotnet-reportgenerator-globaltool
```

### Build Failures
If tests fail during coverage:
1. Report the number of failed tests
2. Suggest fixing tests before measuring coverage
3. Offer to run tests with verbose output

### Permission Issues
If script is not executable:
```bash
chmod +x ./calculate-coverage.sh
```

## Output Files

After successful execution, these files are generated:
- `./coverage/index.html` - Interactive HTML report
- `./coverage/SonarQube.xml` - Format matching CI SonarCloud upload
- `./coverage/Cobertura.xml` - Standard coverage format
- `./coverage/Summary.txt` - Text summary

## Coverage Thresholds

**Overall Coverage Thresholds:**
- **Green (80%+):** Excellent coverage
- **Yellow (60-79%):** Acceptable but should improve
- **Red (<60%):** Needs immediate attention

**New Code Coverage Threshold:**
- SonarCloud Quality Gate requires **80% coverage on new code**
- This is enforced on pull requests before merging

## Integration with CI

Both coverage scripts use the exact same methodology as the CI pipeline:
1. Coverlet XPlat Code Coverage collector
2. OpenCover format output
3. ReportGenerator for Cobertura conversion
4. SonarQube XML format for cloud analysis

**Overall Coverage** (`calculate-coverage.sh`):
- Matches what SonarCloud reports for overall project health

**New Code Coverage** (`calculate-coverage-new-code.sh`):
- Uses `git diff` to identify changed lines (same as SonarCloud with `sonar.newCode.referenceBranch`)
- Cross-references with Cobertura coverage data
- Reports coverage only for new/modified lines
- Matches what SonarCloud Quality Gate checks on PRs
