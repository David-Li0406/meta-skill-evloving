<!--
Copyright (c) 2025 Crash Override Inc. - https://crashoverride.com

SPDX-License-Identifier: GPL-3.0
-->

# COCOMO Models Reference

Comprehensive reference for Constructive Cost Model (COCOMO) software estimation models.

## Overview

**COCOMO** (Constructive Cost Model) is a family of algorithmic software cost estimation models developed by Barry Boehm. It estimates effort, schedule, and cost for software projects based on code size and various cost drivers.

**Versions**:
- **COCOMO 81**: Original model (1981)
- **COCOMO II**: Current model (1997-2000)
- **COCOMO Suite**: Extensions and tools

## COCOMO II Model

### Basic Model Hierarchy

1. **Application Composition Model**
   - For prototyping and early-stage estimation
   - Uses Object Points (screens, reports, components)
   - Productivity rates based on ICASE tool maturity

2. **Early Design Model**
   - For initial project planning
   - Uses Unadjusted Function Points (UFP)
   - 7 cost drivers (aggregate from detailed model)

3. **Post-Architecture Model**
   - Most detailed, for after architecture defined
   - Uses Source Lines of Code (SLOC) or Function Points
   - 17 cost drivers across 4 categories
   - 5 scale factors

### Effort Equation

**Basic Formula**:
```
Effort (Person-Months) = A × Size^B × ∏EM_i
```

Where:
- **A**: Calibration constant (typically 2.94 for COCOMO II)
- **Size**: Software size in KSLOC (thousands of source lines of code)
- **B**: Scale factor exponent
- **EM_i**: Effort multipliers from cost drivers

**Scale Factor Exponent**:
```
B = 0.91 + 0.01 × Σ SF_j
```

Where SF_j are 5 scale factors (0-5 rating each)

### Scale Factors

Scale factors affect the economy/diseconomy of scale:

1. **Precedentedness (PREC)**
   - Project familiarity and precedent
   - Very Low (4): Thoroughly unprecedented
   - Very High (0): Thoroughly familiar

2. **Development Flexibility (FLEX)**
   - Conformity to requirements and external interface
   - Very Low (5): Rigorous requirements
   - Very High (0): General goals

3. **Architecture/Risk Resolution (RESL)**
   - Risk management and architecture definition
   - Very Low (7): Little analysis, weak architecture
   - Very High (0): Thorough risk analysis, strong architecture

4. **Team Cohesion (TEAM)**
   - Stakeholder teamwork and collaboration
   - Very Low (5.5): Difficult interactions
   - Very High (0): Seamless interactions

5. **Process Maturity (PMAT)**
   - Capability Maturity Model (CMM) level
   - Very Low (7): CMM Level 1 (Initial)
   - Very High (0): CMM Level 5 (Optimizing)

### Cost Drivers (17 factors)

#### Product Factors

1. **Required Software Reliability (RELY)**
   - Impact of software failure
   - Very Low (0.82): Slight inconvenience
   - Very High (1.26): Risk to human life

2. **Database Size (DATA)**
   - Size relative to program size
   - Low (0.90): DB bytes/SLOC < 10
   - Very High (1.28): DB bytes/SLOC > 1000

3. **Product Complexity (CPLX)**
   - Control, computation, device, data management operations
   - Very Low (0.73): Straightforward
   - Extra High (1.74): Very difficult operations

4. **Developed for Reusability (RUSE)**
   - Extra effort for reusable components
   - None (0.95): No reuse
   - Extra High (1.24): Across product lines

5. **Documentation Match to Lifecycle Needs (DOCU)**
   - Documentation level vs needs
   - Very Low (0.81): Many gaps
   - Very High (1.23): Excessive documentation

#### Platform Factors

6. **Execution Time Constraint (TIME)**
   - % of available execution time used
   - Nominal (1.00): ≤ 50%
   - Extra High (1.63): ≥ 95%

7. **Main Storage Constraint (STOR)**
   - % of available storage used
   - Nominal (1.00): ≤ 50%
   - Extra High (1.46): ≥ 95%

8. **Platform Volatility (PVOL)**
   - Frequency of platform changes
   - Low (0.87): Major change every 12 months
   - Very High (1.30): Major change every 2 weeks

#### Personnel Factors

9. **Analyst Capability (ACAP)**
   - Analysis and design ability
   - Very Low (1.42): 15th percentile
   - Very High (0.71): 90th percentile

10. **Programmer Capability (PCAP)**
    - Programming ability and efficiency
    - Very Low (1.34): 15th percentile
    - Very High (0.76): 90th percentile

11. **Personnel Continuity (PCON)**
    - Annual personnel turnover
    - Very Low (1.29): > 48% turnover
    - Very High (0.81): ≤ 3% turnover

12. **Applications Experience (APEX)**
    - Experience with application type
    - Very Low (1.22): ≤ 2 months
    - Very High (0.81): ≥ 6 years

13. **Platform Experience (PLEX)**
    - Experience with platform
    - Very Low (1.19): ≤ 2 months
    - Very High (0.85): ≥ 6 years

14. **Language and Tool Experience (LTEX)**
    - Programming language and tool experience
    - Very Low (1.20): ≤ 2 months
    - Very High (0.84): ≥ 6 years

#### Project Factors

15. **Use of Software Tools (TOOL)**
    - Tool support: editors, debuggers, CASE
    - Very Low (1.17): Edit, code, debug
    - Very High (0.78): Strong, mature tools

16. **Multisite Development (SITE)**
    - Degree of multisite working
    - Very Low (1.22): International, no collocation
    - Extra High (0.80): Fully collocated

17. **Required Development Schedule (SCED)**
    - Schedule constraint vs nominal
    - Very Low (1.43): 75% of nominal
    - Very High (1.00): 160% of nominal

### Schedule Equation

**Development Time** (months):
```
TDEV = C × Effort^D

Where:
C = 3.67
D = 0.28 + 0.2 × (B - 0.91)
```

### Maintenance Effort

**Annual Maintenance Effort**:
```
MAF (Maintenance Adjustment Factor) =
  1.0 + (SU / 100) × MCF

Where:
SU = Software Understanding rating
MCF = Maintenance Change Factor
```

## Lines of Code (LOC) Counting

### What to Count

**Include**:
- Executable statements
- Data declarations
- Job control statements (if significant)
- Format statements
- Comments (optional, document choice)

**Exclude**:
- Blank lines
- Compiler directives (optional)
- Auto-generated code (optional)

### Language Conversion

**Average Lines per Function Point**:
```
Assembly: 320 LOC/FP
C: 128 LOC/FP
C++: 64 LOC/FP
Java: 53 LOC/FP
Python: 38 LOC/FP
JavaScript: 47 LOC/FP
SQL: 40 LOC/FP
```

**Function Points to SLOC**:
```
SLOC = FP × Language_Factor
```

## Estimation Process

### Step-by-Step Estimation

1. **Size Estimation**
   - Determine software size (KSLOC or Function Points)
   - Consider reused, modified, and new code
   - Apply sizing uncertainty

2. **Scale Factor Assessment**
   - Rate 5 scale factors (0-5 each)
   - Calculate B exponent
   - Determines economy/diseconomy of scale

3. **Cost Driver Rating**
   - Rate 17 cost drivers
   - Determine effort multipliers
   - Calculate product of all EMs

4. **Effort Calculation**
   - Apply effort equation
   - Get person-months estimate
   - Includes all project activities

5. **Schedule Calculation**
   - Apply schedule equation
   - Get calendar months
   - Optimal team size = Effort / Schedule

6. **Resource Distribution**
   - Allocate across phases
   - Waterfall: Requirements (7%), Design (16%), Code (26%), Test (31%), Management (20%)
   - Adjust for lifecycle model

### Uncertainty and Risk

**Size Uncertainty**:
```
Pessimistic = Most Likely × 1.25
Optimistic = Most Likely × 0.80
```

**Effort Uncertainty**:
```
Based on scale factors and risk assessment
Higher B values = more uncertainty
```

## Project Phases

### Effort Distribution (Waterfall)

1. **Requirements & Planning**: 7-9%
2. **System Design**: 16-18%
3. **Detailed Design & Coding**: 26-28%
4. **Integration & Test**: 31-33%
5. **Management**: 18-20%

### Schedule Distribution

```
Design: 20-24% of TDEV
Coding: 45-50% of TDEV
Testing: 26-30% of TDEV
```

## Calibration

### Local Calibration

COCOMO models should be calibrated to local environment:

1. **Collect Historical Data**
   - Actual effort, schedule, size
   - Cost driver ratings
   - Project characteristics

2. **Regression Analysis**
   - Adjust A constant
   - Adjust cost driver multipliers
   - Validate with test set

3. **Iterative Refinement**
   - Track estimates vs actuals
   - Update calibration factors
   - Document lessons learned

## Modern Extensions

### Agile COCOMO

Adaptations for agile:
- Story points → SLOC conversion
- Velocity-based estimation
- Sprint-level estimation
- Continuous recalibration

### Cloud/DevOps Adjustments

**Infrastructure as Code**:
- Count config as code
- Tool complexity factors
- Automation multipliers

**Microservices**:
- Per-service estimation
- Integration complexity
- Deployment overhead

## Tools and Implementation

### COCOMO Calculators

1. **USC COCOMO Suite**
   - Official COCOMO II implementation
   - Extensive calibration options
   - Risk analysis tools

2. **Open Source Tools**
   - CocomoCalc
   - OpenCOCOMO
   - Web-based calculators

### Automation Approaches

**From Repository**:
```bash
# Count lines of code
cloc . --json > loc.json

# Analyze complexity
radon cc . --json > complexity.json

# Calculate COCOMO
cocomo-estimate --size <KSLOC> --complexity <rating>
```

**From Project Files**:
- Parse package.json dependencies
- Analyze code complexity
- Assess team size and experience
- Calculate scale factors from metrics

## Accuracy and Limitations

### Typical Accuracy

- **Within 20%**: 70% of projects
- **Within 30%**: 80% of projects
- **Best case**: 10-15% error

### Limitations

1. **Size Estimation Difficulty**
   - Most critical input
   - High uncertainty early
   - Requires experience

2. **Subjective Ratings**
   - Cost drivers require judgment
   - Team bias possible
   - Need calibration

3. **Model Assumptions**
   - Waterfall bias (adjustable)
   - Stable requirements
   - Experienced estimators

4. **Not Applicable For**
   - Very small projects (< 2 KSLOC)
   - Non-software work
   - Pure research/prototyping

## Best Practices

### Do ✓
- ✓ Calibrate to organization
- ✓ Use historical data
- ✓ Include uncertainty ranges
- ✓ Update estimates regularly
- ✓ Combine with other methods
- ✓ Document assumptions

### Don't ✗
- ✗ Use uncalibrated defaults
- ✗ Estimate too early
- ✗ Ignore uncertainty
- ✗ Treat as single-point estimate
- ✗ Use for contract negotiation only
- ✗ Ignore actuals vs estimates

## References

- Boehm, B. et al. (2000). "Software Cost Estimation with COCOMO II"
- COCOMO II Model Definition Manual: http://csse.usc.edu/tools/
- ISO/IEC 20926:2009 - IFPUG Function Point Counting
- COSMIC Function Points: https://cosmic-sizing.org/

## Related Metrics

- **Function Points**: Alternative size metric
- **Story Points**: Agile relative sizing
- **Feature Points**: Extension to FP
- **COSMIC**: ISO standard functional size
