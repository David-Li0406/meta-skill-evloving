<!--
Copyright (c) 2025 Crash Override Inc. - https://crashoverride.com

SPDX-License-Identifier: GPL-3.0
-->

# DORA Metrics Complete Guide

Comprehensive guide to DevOps Research and Assessment (DORA) metrics for measuring and improving software delivery performance.

## Overview

**DORA** (DevOps Research and Assessment) is a research program that has investigated software delivery performance since 2014. The program identified four key metrics that indicate the performance of software delivery and operations teams.

**Source**: Google Cloud's DORA team, based on 10+ years of research surveying 36,000+ professionals worldwide.

**Purpose**: Provide evidence-based capabilities and practices that drive high performance in software delivery and organizational outcomes.

## The Four Key Metrics

### 1. Deployment Frequency

**Definition**: How often an organization successfully releases to production.

**What it Measures**:
- Velocity of software delivery
- Batch size (inversely)
- Release automation maturity
- Team confidence in releases

**Calculation**:
```
Deployment Frequency = Number of Deployments / Time Period

Examples:
- Multiple deployments per day
- Daily
- Weekly
- Monthly
- Quarterly
```

**Why It Matters**:
- Faster feedback loops
- Reduced time to market
- Smaller, safer changes
- Improved customer responsiveness
- Lower deployment risk (smaller batches)

**Performance Levels** (2023):
```
Elite:     Multiple deployments per day
High:      Between once per day and once per week
Medium:    Between once per week and once per month
Low:       Between once per month and once every 6 months
```

**How to Improve**:
1. **Automate deployment pipeline**
   - CI/CD implementation
   - Automated testing
   - Infrastructure as Code

2. **Reduce batch size**
   - Feature flags
   - Branch by abstraction
   - Smaller pull requests

3. **Improve testing**
   - Test automation
   - Test-driven development
   - Shift-left testing

4. **Empower teams**
   - Team autonomy
   - Ownership of releases
   - Blameless postmortems

**Common Pitfalls**:
- Measuring deployments without production impact
- Counting failed deployments
- Gaming the metric (deployments without value)
- Not distinguishing between deployment types

### 2. Lead Time for Changes

**Definition**: The time it takes for a commit to get into production.

**What it Measures**:
- Development efficiency
- Deployment automation
- Process bottlenecks
- Organizational agility

**Calculation**:
```
Lead Time = Time from Code Commit to Production Deploy

Measured as:
- Hours
- Days
- Weeks
- Months
```

**Components**:
```
Total Lead Time =
  Code Review Time +
  Build Time +
  Test Time +
  Deployment Time +
  Approval/Waiting Time
```

**Performance Levels** (2023):
```
Elite:     Less than one hour
High:      Between one day and one week
Medium:    Between one week and one month
Low:       Between one month and six months
```

**Why It Matters**:
- Faster time to value
- Rapid feedback on changes
- Improved competitive advantage
- Better developer experience
- Reduced context switching

**How to Improve**:
1. **Automate the pipeline**
   - Continuous Integration
   - Automated testing
   - Automated deployment
   - Eliminate manual approvals

2. **Reduce work in progress**
   - Smaller changes
   - Feature flags
   - Trunk-based development

3. **Optimize review process**
   - Pair programming
   - Mob programming
   - Async code review
   - Clear review guidelines

4. **Parallelize activities**
   - Parallel test execution
   - Independent deployments
   - Microservices architecture

**Common Pitfalls**:
- Only measuring coding time
- Not including all wait states
- Measuring from ticket creation (that's cycle time, not lead time)
- Ignoring blocked/paused time

### 3. Change Failure Rate

**Definition**: The percentage of deployments causing a failure in production.

**What it Measures**:
- Quality of deployments
- Testing effectiveness
- Release process reliability
- System stability

**Calculation**:
```
Change Failure Rate = (Failed Deployments / Total Deployments) × 100%

Where "Failed" means:
- Caused service degradation
- Required immediate remediation (hotfix, rollback, patch)
- Resulted in service outage
- Required manual intervention
```

**Performance Levels** (2023):
```
Elite:     0-15% (less than 15% of changes fail)
High:      16-30%
Medium:    16-30%
Low:       16-30%
```

**Note**: Research shows elite performers have similar failure rates to others, but recover much faster (see MTTR).

**Why It Matters**:
- Customer experience impact
- Engineering efficiency
- Team morale
- Innovation capacity
- Risk tolerance

**What NOT to Include**:
- Changes caught in staging/pre-prod
- Issues found in automated tests
- Planned maintenance
- Known limitations
- Configuration changes that are immediately reverted

**How to Improve**:
1. **Improve testing**
   - Comprehensive test coverage
   - Production-like test environments
   - Automated integration tests
   - Chaos engineering

2. **Better monitoring**
   - Real-time alerting
   - Synthetic monitoring
   - User experience monitoring
   - Error tracking

3. **Quality gates**
   - Code review requirements
   - Automated quality checks
   - Security scanning
   - Performance testing

4. **Progressive delivery**
   - Feature flags
   - Canary deployments
   - Blue-green deployments
   - A/B testing

**Common Pitfalls**:
- Only counting catastrophic failures
- Not counting degraded performance
- Gaming by avoiding risky changes
- Blame culture preventing honest reporting

### 4. Mean Time to Recovery (MTTR)

**Definition**: How long it takes to restore service when a service incident occurs.

**Alternative Name**: Time to Restore Service

**What it Measures**:
- Incident response capability
- System resilience
- Monitoring effectiveness
- Team preparedness

**Calculation**:
```
MTTR = Total Downtime / Number of Incidents

Measured from:
Start: When incident starts/detected
End: When service fully restored

Examples:
- Less than 1 hour
- Less than 1 day
- Between 1 day and 1 week
- More than 1 week
```

**Performance Levels** (2023):
```
Elite:     Less than one hour
High:      Less than one day
Medium:    Between one day and one week
Low:       More than one week
```

**Why It Matters**:
- Customer impact minimization
- Revenue protection
- Team stress reduction
- Competitive advantage
- Organizational resilience

**Components of Recovery Time**:
```
MTTR =
  Time to Detect +
  Time to Diagnose +
  Time to Decide on Fix +
  Time to Implement Fix +
  Time to Deploy Fix +
  Time to Verify Fix
```

**How to Improve**:
1. **Faster detection**
   - Real-time monitoring
   - Automated alerting
   - User error reporting
   - Synthetic monitoring

2. **Faster diagnosis**
   - Centralized logging
   - Distributed tracing
   - Debugging tools
   - Runbooks and playbooks

3. **Faster remediation**
   - Automated rollback
   - Feature flags (kill switch)
   - Self-healing systems
   - Rapid deployment pipeline

4. **Better preparation**
   - Incident response training
   - Regular game days
   - Postmortem reviews
   - Documentation

**Common Pitfalls**:
- Only measuring detection time
- Not including diagnosis time
- Counting time to workaround, not full resolution
- Using mean instead of median (outliers skew mean)

## Performance Profiles

### Elite Performers (2023 Data)

```
Deployment Frequency:  Multiple per day
Lead Time:             < 1 hour
Change Failure Rate:   0-15%
MTTR:                  < 1 hour
```

**Characteristics**:
- Highly automated pipelines
- Strong testing culture
- Loosely coupled architecture
- High team autonomy
- Continuous improvement mindset

### High Performers

```
Deployment Frequency:  Daily to weekly
Lead Time:             1 day to 1 week
Change Failure Rate:   0-15%
MTTR:                  < 1 day
```

**Characteristics**:
- Good automation
- Regular deployments
- Effective monitoring
- Clear processes

### Medium Performers

```
Deployment Frequency:  Weekly to monthly
Lead Time:             1 week to 1 month
Change Failure Rate:   16-30%
MTTR:                  1 day to 1 week
```

**Characteristics**:
- Partial automation
- Some manual processes
- Improving practices

### Low Performers

```
Deployment Frequency:  Monthly to semi-annually
Lead Time:             1 month to 6 months
Change Failure Rate:   16-30%
MTTR:                  > 1 week
```

**Characteristics**:
- Manual processes
- Batch releases
- Limited automation
- Improvement needed

## Using DORA Metrics

### Getting Started

1. **Establish Baseline**
   - Measure current state
   - Document measurement methods
   - Set realistic initial goals
   - Communicate to team

2. **Start Simple**
   - Pick one metric to focus on
   - Use manual tracking if needed
   - Build measurement habits
   - Iterate on process

3. **Automate Measurement**
   - Integrate with CI/CD
   - Use existing tools
   - Dashboard creation
   - Regular reporting

4. **Act on Insights**
   - Identify bottlenecks
   - Experiment with solutions
   - Measure improvements
   - Celebrate wins

### Common Measurement Approaches

**Deployment Frequency**:
```bash
# From CI/CD logs
SELECT COUNT(*)
FROM deployments
WHERE status = 'success'
  AND environment = 'production'
  AND timestamp >= DATE_SUB(NOW(), INTERVAL 30 DAY)
```

**Lead Time**:
```bash
# From Git and deployment data
SELECT AVG(TIMESTAMPDIFF(HOUR, commit_time, deploy_time))
FROM commits c
JOIN deployments d ON c.sha = d.commit_sha
WHERE d.environment = 'production'
  AND d.timestamp >= DATE_SUB(NOW(), INTERVAL 30 DAY)
```

**Change Failure Rate**:
```bash
# From incident tracking
SELECT
  (COUNT(CASE WHEN caused_incident = 1 THEN 1 END) * 100.0 / COUNT(*))
    AS failure_rate
FROM deployments
WHERE environment = 'production'
  AND timestamp >= DATE_SUB(NOW(), INTERVAL 30 DAY)
```

**MTTR**:
```bash
# From incident management
SELECT AVG(TIMESTAMPDIFF(MINUTE, detected_at, resolved_at)) / 60.0
FROM incidents
WHERE severity IN ('critical', 'high')
  AND detected_at >= DATE_SUB(NOW(), INTERVAL 90 DAY)
```

### Anti-Patterns

**DON'T**:
- ❌ Use metrics for individual performance evaluation
- ❌ Create incentives that game the metrics
- ❌ Focus on one metric in isolation
- ❌ Compare teams without context
- ❌ Set arbitrary targets without understanding
- ❌ Blame teams for poor metrics
- ❌ Measure without taking action

**DO**:
- ✅ Use for team improvement
- ✅ Look at trends over time
- ✅ Consider all four metrics together
- ✅ Understand team context
- ✅ Set goals collaboratively
- ✅ Create psychological safety
- ✅ Act on insights

## Integration with Other Frameworks

### Relationship to Business Outcomes

Research shows high DORA performers have:
- **2x more likely** to exceed business goals
- **2x more likely** to exceed profitability goals
- **Higher customer satisfaction**
- **Better employee retention**
- **Lower burnout rates**

### Complementary Metrics

**Team Health**:
- Developer satisfaction
- Burnout indicators
- Psychological safety
- Team stability

**Business Metrics**:
- Customer satisfaction (NPS, CSAT)
- Revenue impact
- User engagement
- Feature adoption

**Quality Metrics**:
- Test coverage
- Code quality
- Security vulnerabilities
- Technical debt

### DevOps Capabilities

DORA research identified 24 capabilities that drive performance:

**Technical**:
1. Use version control
2. Automate deployments
3. Implement CI/CD
4. Use trunk-based development
5. Implement test automation
6. Support test data management
7. Shift left on security
8. Implement continuous delivery
9. Use loosely coupled architecture
10. Empower teams

**Process**:
11. Work in small batches
12. Make flow visible
13. Gather customer feedback
14. Team experimentation

**Cultural**:
15. Support generative culture
16. Encourage learning
17. Support collaboration
18. Provide work-life balance
19. Enable job satisfaction

**Management**:
20. Have lightweight approval process
21. Monitor to inform decisions
22. Check system health proactively
23. Improve processes
24. Use cloud effectively

## Tools and Automation

### Data Collection Tools

**Git Analytics**:
- GitHub Insights
- GitLab Analytics
- Bitbucket Analytics

**CI/CD Metrics**:
- Jenkins metrics
- GitLab CI insights
- GitHub Actions analytics
- CircleCI insights

**Incident Management**:
- PagerDuty analytics
- Opsgenie reports
- Incident.io
- StatusPage metrics

**All-in-One**:
- Jellyfish
- LinearB
- Sleuth
- Haystack

### Custom Dashboards

**Grafana Example**:
```yaml
dashboards:
  - title: "DORA Metrics"
    panels:
      - deployment_frequency
      - lead_time_trend
      - change_failure_rate
      - mttr_by_severity
```

**DataDog Example**:
```yaml
metrics:
  - deployment.frequency
  - deployment.lead_time
  - incident.failure_rate
  - incident.mttr
```

## Best Practices

### Measurement Best Practices

1. **Be Consistent**
   - Same definition over time
   - Same data sources
   - Same calculation method
   - Document methodology

2. **Use Automation**
   - Minimize manual tracking
   - Integrate with existing tools
   - Real-time dashboards
   - Automated reporting

3. **Focus on Trends**
   - Week-over-week changes
   - Month-over-month improvements
   - Quarterly goals
   - Long-term trajectory

4. **Provide Context**
   - Team size changes
   - Technology changes
   - Organizational changes
   - External factors

### Improvement Best Practices

1. **Start Where You Are**
   - Accept current state
   - No judgment
   - Incremental improvement
   - Celebrate progress

2. **Focus on Constraints**
   - Theory of Constraints
   - Identify bottlenecks
   - Optimize the bottleneck
   - Repeat

3. **Experiment**
   - Small changes
   - Measure impact
   - Learn and iterate
   - Share learnings

4. **Build Culture**
   - Psychological safety
   - Blameless postmortems
   - Continuous learning
   - Collaborative problem-solving

## References

- DORA State of DevOps Reports: https://dora.dev/research/
- DORA Quick Check: https://dora.dev/quickcheck/
- Google Cloud DORA: https://cloud.google.com/blog/products/devops-sre/dora-2022-accelerate-state-of-devops-report-now-out
- Accelerate Book: https://itrevolution.com/product/accelerate/
- DORA Guides: https://dora.dev/guides/
