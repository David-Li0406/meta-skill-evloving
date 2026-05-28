# COSTAR Framework

**C**ontext, **O**bjective, **S**tyle, **T**one, **A**udience, **R**esponse Format

Best for well-defined tasks with clear structure.

## Template

```xml
<context>
[Background information and situation]
[Why this task exists]
[Relevant constraints or history]
</context>

<objective>
[Clear, specific goal statement]
[What success looks like]
</objective>

<style>
[Writing approach: analytical, creative, technical, conversational]
[Level of detail: high-level vs. deep dive]
</style>

<tone>
[Emotional quality: professional, friendly, formal, urgent]
[Voice characteristics]
</tone>

<audience>
[Who will receive this output]
[Their expertise level]
[What they care about]
</audience>

<response_format>
[Exact structure expected]
[Include example if complex]
</response_format>
```

## Example

```xml
<context>
B2B SaaS company launching new API versioning feature.
Engineering complete, marketing needs documentation.
API serves 500+ enterprise customers via REST.
</context>

<objective>
Create API docs enabling v1→v2 migration with zero downtime.
Success: Developer can migrate in under 1 hour.
</objective>

<style>
Technical but accessible. Code examples for every endpoint.
Follow Stripe documentation style.
</style>

<tone>
Professional, helpful, confident.
Acknowledge migration challenges without being apologetic.
</tone>

<audience>
Backend developers at enterprise companies.
Familiar with REST, not our specific API.
Time-constrained, need quick answers.
</audience>

<response_format>
## Overview
[1 paragraph summary]

## Migration Guide
### Step 1: [Title]
[Description + code example]

## Breaking Changes
| v1 | v2 | Action |

## FAQ
[3-5 common questions]
</response_format>
```

## When to Use

- Documentation
- Reports
- Structured analysis
- Any task with clear deliverable format

## When NOT to Use

- Creative/exploratory tasks → Use CRISPE
- Complex workflows → Use 5C
- Quick subagent spawns → Use minimal template
