---
name: jira-task-init
description: "Generate initial overview comment for Jira tasks with structured risk and impact analysis. Use when assigned a new Jira task that requires initial planning and risk assessment. Triggers on: jira init, jira-initial, risk analysis, initial jira comment."
agent: project-manager
tools: read, glob, grep, bash, jira_search_issues, jira_get_issue, jira_list_projects, jira_get_project, jira_get_issue_transitions, task
---

# Jira Task Initial Overview Generator

Generates comprehensive initial overview comments for Jira tasks with structured risk and impact analysis. Creates the foundational assessment needed before work begins.

---

## Validation Schema

```yaml
validation_schema:
  required_fields: [Risk_Impact_Analysis, Dependencies, Potentially_Impacted_Areas, Known_Risks, Unknowns_Assumptions]
  format_requirements:
    format_pattern: "Field: Content"
    no_markdown: true
  field_validations:
    Risk_Impact_Analysis:
      required: true
      min_length: 50
      validation_rules:
        - Must contain both technical and business considerations
        - Technical keywords: performance, security, integration, compatibility
        - Business keywords: timeline, budget, user impact, business risk
        - Validation: Check for presence of both technical and business keywords
    Dependencies:
      required: true
      min_length: 30
      validation_rules:
        - Must include actionable dependency information
        - Internal dependencies: JIRA tickets, blocked tasks
        - External dependencies: APIs, third-party services
        - Resource dependencies: team availability, environment setup
    Potentially_Impacted_Areas:
      required: true
      min_length: 30
      validation_rules:
        - Must identify specific systems or user flows
        - Service impact: backend services, databases, APIs
        - User impact: frontend components, user workflows, performance
    Known_Risks:
      required: true
      min_length: 30
      validation_rules:
        - Must identify specific, assessable risks
        - Technical risks: performance, security, integration
        - Project risks: timeline, resource availability
        - Each risk should have potential impact level
    Unknowns_Assumptions:
      required: true
      min_length: 20
      validation_rules:
        - Must clearly state unknowns or working assumptions
        - Technical unknowns: performance characteristics, data volume
        - Business unknowns: user behavior, regulatory requirements
        - Scope assumptions: clear boundaries and exclusions
```

---

## Process Flow

1. **Initial Validation**: Checks if Jira task ID follows correct format (PROJECT-123)
2. **Ticket Existence Verification**: Uses `jira_get_issue` to confirm ticket exists and is accessible
3. **Data Gathering**: 
    - JIRA MCP server for ticket details, context, and related tickets
    - Coordinate with fullstack-developer subagent for comprehensive technical assessment
    - Fullstack-developer analysis includes:
      - Codebase complexity and technical debt evaluation
      - Implementation approach recommendations
      - Dependency identification at code level
      - Integration points and API contract analysis
      - Development effort estimation based on actual code
    - GitHub CLI for related PRs, review status, and code activity
    - Git commands for current branch status, recent commits, and changes analysis
4. **Content Analysis**: Generates content for each of the five overview fields enhanced with technical insights from fullstack-developer analysis
5. **Format Generation**: Creates overview comment following Output Format specification
6. **Enhanced Validation**: Applies enhanced validation rules for content quality and compliance
7. **Preview**: Shows formatted output ready for Jira
8. **User Confirmation**: Requires explicit approval
9. **Posting**: Uses `jira_add_comment` to add comment if confirmed

---

## Enhanced Validation Rules

### **Technical and Business Keyword Validation:**
- ✅ Risk & Impact Analysis must contain both technical AND business keywords
- ✅ Technical keywords: performance, security, integration, compatibility, scalability, database, API
- ✅ Business keywords: timeline, budget, user impact, business risk, ROI, stakeholders, requirements
- ❌ Validation fails if only one type of keyword is present

### **Cross-field Validation:**
- ✅ Dependencies should align with Potentially Impacted Areas
- ✅ Known Risks should be reflected in Risk & Impact Analysis
- ✅ Unknowns/Assumptions should relate to dependencies and risks
- ❌ Validation fails if fields conflict or are inconsistent

### **Content Quality Validation:**
- ✅ Risk assessments should include specific impact levels (high/medium/low)
- ✅ Dependencies should include actionable contact information or next steps
- ✅ Impacted areas should specify systems, users, or business processes
- ✅ Known risks should include probability and potential mitigation strategies
- ❌ Validation fails if content is too generic or lacks specificity

### **Risk Assessment Validation:**
- ✅ Must include both technical and business risk perspectives
- ✅ Should consider short-term and long-term impacts
- ✅ Include dependency risks and external factors
- ✅ Consider resource availability and timeline implications
- ❌ Validation fails if risk assessment is incomplete or one-sided

---

## Output Format

The generated overview comment follows this exact format:

The generated overview comment must follow this exact format:

```
Risk & Impact Analysis: `[Comprehensive risk and impact analysis text]`
Dependencies: `[List of dependencies with details]`
Potentially Impacted Areas: `[Areas potentially affected by this work]`
Known Risks: `[Identified risks with assessments]`
Unknowns / Assumptions: `[Unknowns and assumptions being made]`
```

### **Key Requirements:**
- Each line follows the exact pattern: `Field: Content`
- Content should be comprehensive but concise
- No additional markdown formatting or bullet points
- All five fields must be present

### **Field-Specific Requirements:**

**Risk & Impact Analysis:**
- Minimum 50 characters
- Comprehensive overview of risks and impacts
- Business and technical considerations
- Clear assessment of overall project impact

**Dependencies:**
      - Minimum 30 characters
      - Covers technical, resource, and external dependencies
      - Enhanced with code-level dependencies from fullstack-developer analysis
      - Specific and actionable information with technical implementation details
      - Includes JIRA tickets, PRs, external systems, and code contracts

**Potentially Impacted Areas:**
      - Minimum 30 characters
      - Enhanced with component-level analysis from fullstack-developer
      - Identifies affected systems/services and specific code modules
      - Includes user-facing impacts where relevant
      - Mentions performance or scalability implications with technical basis

**Known Risks:**
      - Minimum 30 characters
      - Enhanced with technical risk assessment from fullstack-developer
      - Identifies specific risks with potential impact and technical basis
      - Covers technical complexity risks and implementation challenges
      - Includes probability/impact where possible with code analysis backing

**Unknowns / Assumptions:**
- Minimum 20 characters
- Clearly states unknowns or assumptions
- Relevant to the work being performed
- Identifies scope boundaries

---

## Validation Rules

### **Format Validation:**
- ✅ Field name exactly as specified
- ✅ Colon followed by space
- ✅ No additional formatting or bullet points
- ❌ Validation fails if format deviates

### **Content Validation:**
- ✅ All fields meet minimum character requirements
- ✅ Content is relevant and specific
- ✅ Technical details are accurate
- ✅ Dependencies are actionable
- ❌ Validation fails if content is too brief or irrelevant

---

## Error Handling

If any data source is unavailable:
- Note the missing data source clearly
- Proceed with available information
- Indicate which sections may have incomplete information
- Suggest manual verification steps

If JIRA task ID format is invalid:
- Provide clear error message with correct format example (PROJECT-123)
- Suggest verifying task ID before proceeding

If ticket existence verification fails:
- Clearly indicate ticket not found or access denied
- Suggest verifying ticket ID and permissions
- Provide option to proceed with manual input if appropriate

If content generation fails:
- Provide templates for each field type
- Offer manual input options
- Include guidance on meeting content requirements

### **Enhanced Validation Error Handling:**

**Keyword Validation Errors:**
- Missing business keywords: Suggest adding timeline, budget, user impact, or business risk
- Missing technical keywords: Recommend adding performance, security, integration, or compatibility
- Provide comprehensive keyword lists for both categories

**Cross-field Validation Errors:**
- Dependencies vs Impact areas misaligned: Suggest reviewing dependency scope
- Risks not reflected in analysis: Recommend updating Risk & Impact Analysis
- Inconsistent assumptions: Request clarification on scope boundaries

**Content Quality Errors:**
- Vague risk assessments: Provide templates with specific impact level examples
- Generic dependencies: Suggest including specific contact information or next steps
- Unclear impacted areas: Request specific systems, users, or business processes
- Incomplete risk analysis: Recommend adding probability and mitigation strategies

**Risk Assessment Errors:**
- One-sided perspective: Suggest adding missing technical or business view
- Missing timeframe: Recommend including short-term and long-term impacts
- Incomplete consideration: Request dependency risks and external factors
- Resource implications missing: Suggest adding timeline and resource considerations