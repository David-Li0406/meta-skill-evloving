<!--
Copyright (c) 2025 Crash Override Inc. - https://crashoverride.com

SPDX-License-Identifier: GPL-3.0
-->

# Code Ownership RAG Documentation

**Retrieval-Augmented Generation** (RAG) reference materials for code ownership analysis, providing comprehensive knowledge base for AI-enhanced analysis and recommendations.

## Overview

This directory contains curated research, best practices, and methodologies for code ownership analysis. These documents serve as reference material for:
- AI-powered code ownership analysis
- CODEOWNERS file generation and validation
- Bus factor risk assessment
- Knowledge transfer planning
- Team health evaluation

## Documents

### 📚 [Code Ownership Fundamentals](code-ownership-fundamentals.md)

Foundation concepts and types of code ownership.

**Contents**:
- Strong, weak, and collective ownership models
- Benefits and drawbacks of each approach
- Martin Fowler's perspective and critiques
- Psychological vs. corporeal ownership
- Modern context with AI (2025)
- Guidance for choosing ownership models

**Key Insights**:
- Strong ownership creates bottlenecks (Fowler's critique)
- Weak and collective ownership depend on team social dynamics
- Hybrid approaches often work best
- AI is changing knowledge distribution dynamics

**Use Cases**:
- Understanding ownership philosophy
- Choosing appropriate ownership model
- Explaining ownership trade-offs
- Training team members

---

### 📋 [CODEOWNERS Best Practices](codeowners-best-practices.md)

Comprehensive guide to CODEOWNERS files across Git platforms.

**Contents**:
- Core syntax and patterns
- Strategic implementation models
- Platform-specific features (GitHub, GitLab, Bitbucket)
- 10 critical mistakes to avoid
- Testing and validation approaches
- Maintenance schedules

**Key Insights**:
- Last-match-wins rule for pattern precedence
- Teams are better than individuals (reduces bus factor)
- Stale ownership is a common anti-pattern
- Regular audits (quarterly) are essential
- Balance granularity vs. maintainability

**Use Cases**:
- Creating new CODEOWNERS files
- Validating existing CODEOWNERS
- Troubleshooting ownership issues
- Planning CODEOWNERS structure

---

### 📊 [Ownership Metrics](ownership-metrics.md)

Quantitative measurement and analysis methodologies.

**Contents**:
- Commit-based vs. line-based ownership
- Weighted ownership scores
- Coverage metrics
- Distribution metrics (Gini coefficient)
- Staleness and freshness metrics
- Health score calculation
- Review and engagement metrics

**Key Insights**:
- Commit-based metrics stronger for defect prediction (97% accuracy)
- Line-based metrics better for authorship/IP
- Only 0-40% of developers identified by both methods
- Gini coefficient >0.7 indicates dangerous concentration
- Freshness >75% active owners is healthy

**Use Cases**:
- Measuring code ownership health
- Predictive defect modeling
- Tracking improvement trends
- Benchmarking against standards

---

### 🚌 [Bus Factor Analysis](bus-factor-analysis.md)

Risk assessment and succession planning.

**Contents**:
- Bus factor definition and calculation
- Single point of failure (SPOF) detection
- Risk assessment framework
- Succession planning methodology
- Mitigation strategies
- Case studies

**Key Insights**:
- Bus factor = 1 is critical risk
- SPOF has 6 criteria (owner, criticality, complexity, tests, docs)
- Knowledge transfer takes 1-8 weeks depending on complexity
- Preventive measures more effective than reactive
- Documentation + backup ownership essential

**Use Cases**:
- Identifying critical risks
- Planning team transitions
- Succession planning
- Knowledge transfer estimation

---

## How to Use This Documentation

### For AI Analysis

These documents provide context for AI-powered code ownership analysis:

1. **Load relevant documents** based on analysis type:
   - Repository audit → All documents
   - CODEOWNERS validation → Best Practices + Fundamentals
   - Bus factor analysis → Bus Factor + Metrics
   - Knowledge transfer → Bus Factor + Fundamentals

2. **Reference specific sections** for targeted insights:
   - Metrics calculations → Ownership Metrics formulas
   - Risk assessment → Bus Factor risk frameworks
   - Recommendations → Best Practices patterns

3. **Ground recommendations** in research:
   - Cite specific metrics and thresholds
   - Reference best practices
   - Use proven methodologies

### For Human Reference

Quick navigation by use case:

**"How do I measure code ownership?"**
→ [Ownership Metrics](ownership-metrics.md)

**"What should my CODEOWNERS file look like?"**
→ [CODEOWNERS Best Practices](codeowners-best-practices.md)

**"How do I calculate bus factor?"**
→ [Bus Factor Analysis](bus-factor-analysis.md)

**"What ownership model should we use?"**
→ [Code Ownership Fundamentals](code-ownership-fundamentals.md)

**"Someone is leaving, what do I do?"**
→ [Bus Factor Analysis - Succession Planning](bus-factor-analysis.md#succession-planning)

## Key Concepts Summary

### Ownership Models

| Model | Control | Flexibility | Best For |
|-------|---------|-------------|----------|
| **Strong** | Single owner approves all changes | Low | Security-critical, specialized domains |
| **Weak** | Designated owner, anyone can modify | Medium | Most enterprise teams |
| **Collective** | Everyone owns everything | High | Small XP teams, startups |

### Critical Thresholds

```
Ownership Coverage: >70% good, >90% excellent
Gini Coefficient: <0.5 good, <0.3 excellent
Bus Factor: ≥3 healthy, 1-2 risky
Active Owners: >60% acceptable, >75% excellent
Review Turnaround: <24 hours target
```

### Risk Indicators

```
🚨 Critical:
- Bus factor = 1 for critical component
- Top 1 person owns >20% of codebase
- Critical code abandoned (>180 days inactive)

⚠️ Warning:
- Bus factor = 2 for important component
- Gini coefficient >0.7
- >30% files with stale owners

ℹ️ Monitor:
- Coverage <80%
- Review turnaround >48 hours
- Active owners <70%
```

## Research Sources

This documentation synthesizes research from:

- **Martin Fowler** - Code Ownership philosophy and critiques
- **arXiv:2408.12807v1** (2024) - Empirical research on ownership and quality
- **Microsoft Research** - Code ownership and defect correlation
- **Aviator.co** - Modern CODEOWNERS practices
- **GitHub/GitLab Documentation** - Platform-specific features
- **Various 2024-2025** - Software engineering best practices

## Integration with Tools

### Code Ownership Analyser Scripts

The RAG documentation informs:
- `ownership-analyser.sh` - Basic ownership calculation
- `ownership-analyser-claude.sh` - AI-enhanced analysis with RAG context

Scripts use these documents to:
- Calculate metrics using proven formulas
- Assess risk using established thresholds
- Generate recommendations based on best practices
- Validate CODEOWNERS against patterns

### Claude Code Skill

The [Code Ownership Analysis Skill](../../skills/code-ownership/code-ownership-analyser.skill) leverages this RAG documentation to provide expert analysis and recommendations.

### Prompts

The [Code Ownership Prompts](../../prompts/code-ownership/) reference this documentation for consistent, research-backed guidance.

## Maintenance

### Update Schedule

- **Quarterly**: Review metrics and thresholds against industry trends
- **Annually**: Comprehensive update with latest research
- **As Needed**: New platform features, major research publications

### Contributing

To contribute or update documentation:

1. Research new sources thoroughly
2. Maintain consistent format and structure
3. Add citations and references
4. Update this README with new insights
5. Test with ownership analyser scripts
6. Submit PR with rationale

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

## Version History

- **v1.0.0** (2024-11): Initial comprehensive RAG documentation
  - Code ownership fundamentals
  - CODEOWNERS best practices
  - Ownership metrics
  - Bus factor analysis

## Related Resources

### Within Repository

- [Code Ownership Skill](../../skills/code-ownership/)
- [Code Ownership Prompts](../../prompts/code-ownership/)
- [Ownership Analyser Scripts](../../utils/code-ownership/)

### External Resources

- [Martin Fowler: Code Ownership](https://martinfowler.com/bliki/CodeOwnership.html)
- [GitHub CODEOWNERS Documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [GitLab Code Owners](https://docs.gitlab.com/ee/user/project/codeowners/)
- [arXiv: Code Ownership Research](https://arxiv.org/abs/2408.12807)

## License

GPL-3.0 - See [LICENSE](../../LICENSE) for details.

---

**Build better code ownership practices with research-backed guidance!**
