---
name: show-draft
description: Show what /r2r:draft produces - a sample ADR draft that structures research before it begins.
---

# Show Draft Example

When triggered, display this sample draft output:

---

## /r2r:draft Output Example

Here's what `/r2r:draft "AI-powered code review for PR automation"` produces:

---

# RFC DRAFT: AI-Powered Code Review for PR Automation

**Status**: WIP
**Author**: JD Fiscus
**Created**: 2025-01-20

## Problem

Manual code reviews are a bottleneck. Senior engineers spend 4-6 hours/week reviewing PRs. We want to explore whether AI can handle first-pass reviews to catch common issues before human review.

## Research Questions

- [ ] Which AI models perform best on code review tasks? (GPT-4, Claude, CodeLlama)
- [ ] What's the false positive rate for AI-flagged issues?
- [ ] How do developers perceive AI review comments?
- [ ] What's the cost per PR at scale (1000+ PRs/month)?
- [ ] Can we integrate with existing GitHub Actions workflow?

## Options to Evaluate

1. **OpenAI GPT-4**: Highest capability, highest cost, API-based
2. **Anthropic Claude**: Strong reasoning, good at explanations, API-based
3. **Self-hosted CodeLlama**: Lower cost at scale, requires infrastructure
4. **GitHub Copilot for PRs**: Native integration, limited customization

## Solution

[To be filled after research]

## Rationale

[To be filled after research]

## Scope

### In Scope
- Automated first-pass review on new PRs
- Common issue detection (security, performance, style)
- Integration with existing CI/CD

### Out of Scope
- Replacing human reviewers entirely
- Architectural review
- Business logic validation

## Success Criteria

- Reduce senior engineer review time by 30%
- < 10% false positive rate on flagged issues
- Developer satisfaction score > 7/10
- Cost < $0.50 per PR reviewed

## Stakeholders

| Stakeholder | Interest | Engagement |
|-------------|----------|------------|
| Engineering | Time savings | Decides |
| Security | Vulnerability detection | Consulted |
| Finance | Cost implications | Informed |

## Risks

- Developers may ignore AI comments (alert fatigue)
- False positives erode trust
- Cost could exceed manual review at scale
- Security/privacy concerns with code leaving org

## Next Steps

- [ ] Research model options (1 week)
- [ ] Build POC with top 2 models (2 weeks)
- [ ] Run pilot on internal repos (2 weeks)
- [ ] Run `/r2r:assess` on findings
- [ ] Make go/no-go decision

---

**This creates structure BEFORE research begins.** After completing the research plan, run `/r2r:assess` to evaluate findings and continue through the pipeline.

The full `/r2r:draft` command:
1. Asks clarifying questions about your research topic
2. Lets you pick a template style (Google/Uber/Sourcegraph/Experiment)
3. Generates a structured draft with research plan
4. Saves to `.r2r/00-draft-adr.md`
