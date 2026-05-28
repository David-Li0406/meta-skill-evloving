# Mining Industry Scheduling Standards

Best practices and standards specific to mining and resources projects, including BHP-specific conventions.

## Mining Project Phases

### 1. Study Phase (Pre-Feasibility / Feasibility)
**Duration**: 12-36 months
**Schedule Level**: High-level milestone schedule
**Update Frequency**: Monthly
**Key Milestones**:
- Trade-off studies complete
- Geological model finalized
- Process design complete
- Environmental approvals
- Financial investment decision (FID)

**Scheduling Characteristics**:
- Activity durations: 1-4 weeks typical
- Focus on decision gates and approvals
- Resource loading: Generally not required at this phase
- Contingency: 20-30% schedule contingency typical

### 2. Engineering & Procurement (EPCM/EPC)
**Duration**: 18-36 months
**Schedule Level**: Detailed engineering schedule
**Update Frequency**: Weekly for active areas, monthly for long-lead
**Key Milestones**:
- Engineering data releases (30%, 60%, 90%, IFC)
- Long-lead equipment orders
- Bulk material procurement
- Construction work packages ready

**Scheduling Characteristics**:
- Activity durations: 5-20 working days for detail activities
- Extensive use of finish-to-finish relationships for engineering deliverables
- Resource loading by discipline (structural, mechanical, electrical, etc.)
- Track drawing issuance and approval cycles

### 3. Construction & Commissioning
**Duration**: 24-48 months (major projects)
**Schedule Level**: Very detailed construction schedule (Level 4/5)
**Update Frequency**: Weekly
**Key Milestones**:
- Beneficial occupancy dates
- Mechanical completion by area
- Pre-commissioning complete
- Commissioning activities
- Performance testing
- Handover to operations

**Scheduling Characteristics**:
- Activity durations: 1-10 working days typical, max 20 days
- High logic density (≥2.0 relationships per activity)
- Full resource loading (labor, equipment, materials)
- Weather and seasonal constraints critical
- Multiple shift work common

### 4. Ramp-Up to Production
**Duration**: 6-18 months
**Schedule Level**: Operations-focused schedule
**Update Frequency**: Weekly initially, then monthly
**Key Milestones**:
- First ore/product
- Nameplate capacity achieved
- Sustained production rate
- Final acceptance

## Activity Duration Standards

### Maximum Duration Limits

| Project Phase | Activity Type | Max Duration | Rationale |
|--------------|--------------|--------------|-----------|
| Construction | Detail work | 20 working days | Maintain schedule control |
| Engineering | Design tasks | 15 working days | Align with drawing cycles |
| Procurement | Ordering activities | 30 working days | Long-lead items |
| Commissioning | System testing | 10 working days | Maintain momentum |
| Any | Summary/WBS | No limit | Rollup activities |
| Any | Level of Effort | Project duration | Continuous activities |

**Enforcement**:
- >95% of detail activities should comply
- Exceptions require justification and approval
- Long activities should be broken down into measurable increments

## Logic Density Requirements

**Standard**: Minimum 1.8 relationships per activity (construction phase)

**Calculation**:
```
Logic Density = (Total Predecessors + Total Successors) / Total Activities
```

**Phase-Specific Targets**:
- Study Phase: ≥1.2 (high-level schedule)
- Engineering: ≥1.5 (deliverable-focused)
- Construction: ≥1.8 (detailed execution)
- Commissioning: ≥1.6 (sequential systems)

**Quality Indicators**:
- <1.5: Poor logic, schedule not reliable
- 1.5-1.8: Acceptable for early phases
- 1.8-2.5: Good logic density
- >3.0: May indicate over-complexity

## Float Management

### Float Thresholds

| Float Range | Classification | Action Required |
|-------------|----------------|-----------------|
| ≤0 days | Critical | Daily monitoring, mitigation plans |
| 1-10 days | Near-critical | Weekly monitoring, watch list |
| 11-30 days | Low float | Bi-weekly review |
| 31-60 days | Moderate float | Monthly review |
| >60 days | High float | Review logic, may indicate detachment |

### Float Consumption Monitoring

**Rule**: Track float consumption rate, not just absolute float.

**Calculation**:
```
Float Consumption Rate = (Baseline Float - Current Float) / Weeks Elapsed
```

**Thresholds**:
- >2 days/week: High risk, immediate action
- 1-2 days/week: Moderate risk, mitigation required
- <1 day/week: Normal variance

## Critical Path Management

### Critical Path Requirements

1. **Single Longest Path**: Critical path must represent the true longest path to completion
2. **Logic-Driven**: Critical activities should be critical due to logic, not constraints
3. **Continuous**: No gaps in critical path
4. **Realistic**: Critical path should align with experienced team's expectations

### Critical Activity Characteristics

**Monitoring Frequency**:
- Daily for construction critical activities
- Weekly for engineering/procurement critical activities

**Required Mitigation**:
- All critical activities must have risk mitigation plans
- Regular critical path reviews (weekly minimum)
- Fast-tracking/crash options identified

### Near-Critical Paths

**Definition**: Activities with ≤10 days total float

**Importance**: In mining projects, multiple near-critical paths are common due to:
- Parallel construction areas
- Multiple commissioning systems
- Weather-dependent outdoor work

**Management**: Track top 3-5 near-critical paths as potential critical paths.

## Constraints and Milestones

### Constraint Usage Limits

**Target**: <5% of activities constrained (excluding milestones)

**Allowed Constraint Types**:
1. **Mandatory Start On (MSO)** / **Mandatory Finish On (MFO)**:
   - Regulatory dates (environmental windows)
   - Contractual milestones
   - Interface dates with other projects

2. **Start No Earlier Than (SNET)** / **Finish No Earlier Than (FNET)**:
   - Resource availability (e.g., specialized equipment arrival)
   - Seasonal work windows (wet/dry season in mining regions)
   - Permit approval minimum timeframes

**Discouraged Constraints**:
- As Late As Possible (ALAP) - use sparingly
- Start/Finish No Later Than - indicates schedule pressure, use logic instead

### Milestone Definitions

**Project Milestones** (zero duration):
- Major decision gates (FID, construction start)
- Regulatory approvals received
- Contractual deliverables
- First ore/product milestones
- Beneficial occupancy dates
- Final acceptance

**Milestone Naming Convention** (BHP Standard):
```
[Phase Code]-[Area]-[Milestone Type]-[Description]
Example: CONST-CRU-BOD-Crusher Beneficial Occupancy
```

## Resource Management

### Resource Categories - Mining Projects

1. **Labor Resources**:
   - Construction labor (by trade: pipefitters, electricians, etc.)
   - Engineering disciplines (structural, mechanical, electrical, civil)
   - Commissioning teams
   - Owner's team

2. **Equipment Resources**:
   - Heavy equipment (cranes, dozers, excavators)
   - Specialized equipment (piling rigs, mining equipment)
   - Construction equipment (concrete pumps, welders)

3. **Material Resources** (tracking only, not scheduling):
   - Bulk materials (concrete, steel, piping)
   - Equipment (pumps, motors, crushers, conveyors)
   - Consumables

### Resource Loading Requirements

**When Required**:
- Construction phase: Mandatory
- Engineering phase: By discipline (recommended)
- Procurement: Not typically resource-loaded
- Commissioning: By system/team (recommended)

**Resource Histogram Review**:
- Weekly review during peak construction
- Identify ramp-up and ramp-down periods
- Smooth resource profiles to avoid demobilization/remobilization
- Peak resource levels should align with site capacity (camps, facilities)

### Resource Over-Allocation Limits

**Acceptable Thresholds**:
- <10% over-allocation: Acceptable, can be managed with overtime
- 10-20% over-allocation: Requires leveling or justification
- >20% over-allocation: Not acceptable, must be resolved

## Progress Measurement

### Earned Value Integration

Mining projects typically integrate P6 with earned value management:

**Physical % Complete Methods**:
1. **0/100 Rule**: Activity earns credit only when complete (milestones, short activities)
2. **50/50 Rule**: 50% at start, 50% at finish (medium activities)
3. **Weighted Milestones**: Credit at defined milestones (long activities)
4. **Percent Complete**: Based on quantity installed (bulk work)

**Activity Coding for EV**:
- Cost Account Code
- Work Breakdown Structure (WBS) alignment
- Control Account Manager (CAM) assignment

### Progress Update Frequency

| Project Phase | Update Frequency | Data Cut-Off | Distribution |
|--------------|------------------|--------------|--------------|
| Study | Monthly | Last Friday | Following Monday |
| Engineering | Bi-weekly | Thursday | Friday |
| Construction | Weekly | Friday | Monday |
| Commissioning | Weekly | Friday | Monday |

### Progress Update Quality Checks

**Pre-Publication Validation**:
1. All in-progress activities have actual start dates
2. All completed activities have actual finish dates
3. No future actual dates
4. Remaining duration is reasonable
5. Physical % aligns with actual dates
6. Critical path reviewed and validated
7. Out-of-sequence work identified and justified

## Weather and Seasonal Constraints

### Mining Regions - Weather Considerations

**Tropical/Monsoon Regions** (Northern Australia, Southeast Asia):
- Wet season: Nov-Apr (limited outdoor work)
- Dry season: May-Oct (peak construction)
- Schedule activities requiring dry conditions in dry season
- Plan for wet season delays (15-25% productivity loss)

**Arid Regions** (Western Australia, Chile):
- Extreme heat: Dec-Feb (reduce outdoor work hours)
- Dust storms: Seasonal, impact concrete pours and electrical work
- Generally favorable for year-round construction

**Cold Regions** (Canada, Russia):
- Winter: Nov-Mar (limited outdoor work, frozen ground)
- Summer: Apr-Oct (peak construction window)
- Ice road access: Jan-Mar only (remote sites)
- Plan bulk material deliveries during access windows

**Implementation**:
- Use calendar exceptions for seasonal work restrictions
- Apply productivity factors for adverse weather periods
- Build weather contingency (5-15% depending on region)

## BHP-Specific Standards

### Activity Coding Structure

**Mandatory Activity Codes**:
1. **Area Code**: Physical location (plant area, infrastructure, mine area)
2. **Discipline**: Engineering or construction discipline
3. **Work Package**: Alignment with contract packages
4. **Responsible Party**: Contractor, owner, vendor
5. **Milestone Category**: If activity is a project milestone

**Example**:
```
Activity: Install Crusher Motor
Area: CRU (Crusher Plant)
Discipline: ELEC (Electrical)
Work Package: WP-005 (Electrical Installation)
Responsible: Contractor-A
```

### Baseline Management

**Baseline Types**:
1. **FID Baseline**: Approved at Financial Investment Decision
2. **Project Baseline**: Updated baseline reflecting approved changes
3. **Forecast Baseline**: Current project forecast
4. **Monthly Snapshots**: Archived monthly schedules for trend analysis

**Change Control**:
- All baseline changes require change request and approval
- Baseline updates: Quarterly or after major scope changes
- Maintain baseline integrity (no retroactive changes)

### Reporting Requirements

**Standard Reports** (BHP Mining Projects):
1. **Weekly Look-Ahead**: 4-week rolling window
2. **Critical Path Report**: All critical activities with status
3. **Milestone Report**: All project milestones with forecast dates
4. **Variance Report**: Baseline vs current (activities >5 days variance)
5. **Float Trend**: Top 20 activities with declining float
6. **Resource Histogram**: 12-week rolling resource forecast

**Dashboard KPIs**:
- Overall project % complete (planned vs actual)
- Critical path finish date (baseline vs forecast)
- Number of activities with negative float
- Number of critical activities
- Schedule Performance Index (SPI)
- Top 10 risks to schedule completion

## Risk and Opportunity Management

### Schedule Risk Analysis

**When Required**:
- Pre-FID: Probabilistic analysis to support project sanction
- Post-FID: Annual risk reviews, or after major changes
- Active Risk Management: Quarterly reviews during execution

**Methodology**:
- Monte Carlo simulation (min/most likely/max durations)
- P50 = Most likely completion
- P80 = Completion with high confidence (add contingency)
- P90 = Very high confidence (regulatory commitments)

**Risk Buffers**:
- Schedule contingency: 10-20% (depending on phase and complexity)
- Management reserve: Additional 5-10% (for unknown unknowns)

### Critical Schedule Risks - Mining Projects

**Common Schedule Risks**:
1. Regulatory approvals delayed (environmental, heritage)
2. Long-lead equipment delivery delays (crushers, mills, conveyors)
3. Weather worse than historical average
4. Geotechnical conditions worse than expected (foundations, underground)
5. Labor availability (remote locations, competitive market)
6. Industrial relations (strikes, work stoppages)
7. COVID-19 or health restrictions (ongoing consideration)
8. Supply chain disruptions (bulk materials, equipment)

**Mitigation in Schedule**:
- Build risk mitigation activities into schedule
- Identify float protection strategies
- Fast-track where possible (parallel vs sequential)
- Early procurement of long-lead items

## Quality Metrics Summary

High-quality mining project schedule should achieve:

| Metric | Target | Phase Applicability |
|--------|--------|---------------------|
| Logic density | ≥1.8 | Construction |
| Activities with constraints | <5% | All phases |
| Long activities (>20 days) | <5% | Construction |
| Critical activities monitored | 100% | All phases |
| Schedule updates | Weekly | Construction |
| Resource over-allocation | <10% | Construction |
| Baseline variance review | Monthly | All phases |
| Risk review frequency | Quarterly | All phases |

## Tools Integration

**Common Integration Points**:
- **Cost Management**: Integration with cost control systems (earned value)
- **Document Management**: Link schedules to drawing registers, specifications
- **Risk Register**: Link schedule risks to corporate risk registers
- **Reporting Tools**: Export data to BI tools (Power BI, Tableau)
- **Field Progress**: Integration with field data capture tools

**Data Exchange Formats**:
- XER files for P6-to-P6 transfers
- XML for cross-platform integration
- API calls for real-time data sync
- Database views for reporting tools
