# Stakeholder Research Workflow

Gather insights from stakeholders, conduct user interviews, and document requirements and feedback.

## When to Use

- During PDLC Stakeholder_Alignment node
- After vision and market research are complete
- Before epic or feature design begins
- When validating solution approaches with users
- During feature refinement for user feedback

## Prerequisites

**Required artifacts**:
- D01-vision-statement.md - Product vision

**Optional context**:
- D02-market-research.md - Market and competitive analysis
- D03-solution-candidates.md - Solution ideas to validate
- F01-feature-prd.md - Feature spec (if doing feature-level research)

## Workflow Steps

### 1. Identify Stakeholder Groups

Categorize stakeholders:

**Primary Users**:
- End users who will use the product daily
- Power users with advanced needs
- Occasional users with basic needs

**Business Stakeholders**:
- Executives and decision-makers
- Product owners
- Operations teams

**Technical Stakeholders**:
- Development team
- Infrastructure and DevOps
- Security and compliance

**External Stakeholders**:
- Partners and integrators
- Customer success teams
- Support teams

### 2. Prepare Research Questions

Design questions for each stakeholder group:

**For End Users**:
- Current pain points and workflows
- Desired outcomes and goals
- Feature priorities and preferences
- Usability and experience expectations

**For Business Stakeholders**:
- Business objectives and KPIs
- Budget and timeline constraints
- Compliance and regulatory requirements
- Success metrics and ROI expectations

**For Technical Stakeholders**:
- Technical constraints and dependencies
- Integration requirements
- Performance and scalability needs
- Security and data privacy requirements

### 3. Conduct Stakeholder Interviews

For each stakeholder group:

**Interview Structure**:
1. Introduction and context setting
2. Current state exploration
3. Pain points and challenges
4. Desired outcomes and priorities
5. Feedback on proposed solutions (if applicable)
6. Open-ended questions and discussion

**Documentation During Interview**:
- Record key quotes verbatim
- Note emotional responses and emphasis
- Capture specific examples and stories
- Identify conflicting needs across stakeholders

### 4. Analyze and Synthesize Findings

Review all interviews to identify:

**Common Themes**:
- Repeated pain points across stakeholders
- Shared priorities and goals
- Consistent feedback patterns

**Divergent Needs**:
- Conflicting requirements
- Different priorities between groups
- Trade-offs that need resolution

**Key Insights**:
- Unexpected findings
- Hidden assumptions challenged
- Opportunities discovered

**Requirements**:
- Must-have capabilities
- Nice-to-have features
- Non-negotiable constraints

### 5. Prioritize Requirements

Categorize findings using MoSCoW method:

- **Must Have**: Critical requirements for MVP
- **Should Have**: Important but not critical
- **Could Have**: Desirable if time/budget allows
- **Won't Have**: Out of scope for this phase

### 6. Identify Conflicts and Resolutions

Document any:
- Conflicting requirements between stakeholder groups
- Trade-offs that need ProductManager decision
- Assumptions that need validation
- Questions requiring further research

### 7. Document Findings

Create D06-stakeholder-insights.md with structure:

```markdown
# Stakeholder Research Report

## Executive Summary
[Key findings and insights in 3-5 bullet points]

## Stakeholder Groups

### Primary Users ([n] interviewed)
- [User segment 1]: [brief description]
- [User segment 2]: [brief description]

### Business Stakeholders ([n] interviewed)
- [Role/team]: [brief description]

### Technical Stakeholders ([n] interviewed)
- [Role/team]: [brief description]

## Research Methodology
- Interview format: [structured/semi-structured/survey]
- Duration: [date range]
- Sample size: [total participants]

## Key Findings

### Pain Points and Challenges
1. **[Pain point theme]**
   - Frequency: [how often mentioned]
   - Severity: [impact level]
   - Quote: "[representative quote]"
   - Implication: [what this means for design]

2. **[Another pain point]**
   [Same structure]

### User Goals and Desired Outcomes
1. **[Goal theme]**
   - Stakeholder group: [who mentioned this]
   - Priority: [High/Medium/Low]
   - Success metric: [how they measure this]

### Feature Priorities

#### Must Have (MVP Blockers)
1. [Feature/capability]: [rationale from stakeholders]
2. [Feature/capability]: [rationale]

#### Should Have (High Priority)
1. [Feature/capability]: [rationale]

#### Could Have (If Time Permits)
1. [Feature/capability]: [rationale]

#### Won't Have (Out of Scope)
1. [Feature/capability]: [reason for exclusion]

### Usability and Experience Expectations
- [Key expectation 1]
- [Key expectation 2]
- Reference products: [products users mentioned as examples]

## Requirements Summary

### Functional Requirements
1. [Requirement]: [source stakeholder group]
2. [Requirement]: [source]

### Non-Functional Requirements
1. Performance: [specific expectations]
2. Security: [specific requirements]
3. Scalability: [specific needs]
4. Compliance: [regulatory requirements]

### Technical Constraints
- [Constraint 1]: [description]
- [Constraint 2]: [description]

## Conflicts and Trade-offs

### [Conflict 1]
- **Stakeholders**: [Group A] vs [Group B]
- **Issue**: [description of conflict]
- **Options**:
  - Option 1: [favor Group A approach]
  - Option 2: [favor Group B approach]
  - Option 3: [compromise approach]
- **Recommendation**: [suggested resolution]

### [Conflict 2]
[Same structure]

## User Personas (if applicable)

### [Persona 1 Name]
- **Role**: [job title/role]
- **Goals**: [primary objectives]
- **Pain Points**: [key frustrations]
- **Tech Savviness**: [skill level]
- **Quote**: "[representative quote]"

### [Persona 2 Name]
[Same structure]

## Recommendations

1. [Actionable recommendation based on findings]
   - Rationale: [why]
   - Impact: [expected outcome]

2. [Another recommendation]
   [Same structure]

## Open Questions

1. [Question requiring further research or validation]
2. [Another question]

## Appendix

### Interview Questions Used
[List of questions for reference]

### Stakeholder List
[Non-sensitive list of stakeholder groups and counts]
```

### 8. Store Artifact

Save the completed stakeholder insights:
```bash
/home/jwwelbor/projects/ai-dev-team/docs/workflow/artifacts/D06-stakeholder-insights.md
```

## Success Criteria

Research is complete when:
- All major stakeholder groups are represented
- Common themes and patterns are identified
- Requirements are prioritized using MoSCoW
- Conflicts are documented with resolution options
- Findings are specific and actionable
- Recommendations are tied to stakeholder feedback
- User personas capture key user segments (if applicable)

## Interview Templates

### User Interview Template

```markdown
## Interview with [Name/Role] - [Date]

### Current Workflow
Q: Walk me through how you currently [solve this problem]
A: [notes]

### Pain Points
Q: What are the biggest frustrations with your current approach?
A: [notes]

### Goals
Q: What would an ideal solution enable you to do?
A: [notes]

### Priorities
Q: If you could only have 3 features, what would they be?
A: [notes]

### Context
Q: How often do you [perform this task]? Who else is involved?
A: [notes]
```

### Business Stakeholder Template

```markdown
## Interview with [Name/Role] - [Date]

### Business Objectives
Q: What business goals does this product need to achieve?
A: [notes]

### Success Metrics
Q: How will you measure success?
A: [notes]

### Constraints
Q: What are the budget, timeline, and resource constraints?
A: [notes]

### Requirements
Q: What are the non-negotiable requirements?
A: [notes]
```

## Next Steps

After stakeholder research:
- ProductManager reviews findings for scope decisions
- Conflicts escalated for resolution
- Requirements inform epic and feature PRD creation
- User personas guide UX/CX design
- Workflow advances to Epic_Creation or Feature_PRD_Writing

## Related Workflows

- `market-research.md` - Market and competitive insights
- `feasibility-analysis.md` - Technical viability assessment
- `specification-writing/workflows/write-prd.md` - Feature PRD creation
- `design/workflows/journey-mapping.md` - Customer journey design
