# Skill Creation Examples

Examples for creating new skills including naming, descriptions, and structure patterns.

## Official Skill Examples

These examples from the Claude cookbooks demonstrate best practices:

### 1. analyzing-financial-statements

**Strength: Clear domain focus and specific triggers**

```yaml
---
name: analyzing-financial-statements
description: Calculates key financial ratios and metrics from financial statement data for investment analysis. Use when analyzing company performance, evaluating investments, or when user provides income statements, balance sheets, or cash flow statements.
---
```

**Why it works:**
- ✅ Specific capability: "calculates key financial ratios"
- ✅ Clear triggers: "analyzing company performance", "evaluating investments"
- ✅ Data format triggers: "income statements, balance sheets, cash flow statements"
- ✅ Includes Python scripts for calculations
- ✅ Focused on single domain (financial analysis)

### 2. applying-brand-guidelines

**Strength: Progressive disclosure with REFERENCE.md**

```yaml
---
name: applying-brand-guidelines
description: Ensures documents maintain Acme Corporation's brand standards including colors, fonts, logos, and formatting. Use when creating or reviewing corporate documents, presentations, reports, or when user mentions brand compliance or style guidelines.
---
```

**Why it works:**
- ✅ Clear purpose: "ensures documents maintain brand standards"
- ✅ Specific elements: "colors, fonts, logos, formatting"
- ✅ Multiple triggers: "creating or reviewing corporate documents", "brand compliance"
- ✅ Uses REFERENCE.md for detailed specs (progressive disclosure)
- ✅ Company-specific knowledge that Claude doesn't have

### 3. creating-financial-models

**Strength: Multiple related capabilities in single domain**

```yaml
---
name: creating-financial-models
description: Builds advanced financial models including DCF analysis, sensitivity testing, Monte Carlo simulations, and scenario planning for investment analysis. Use when valuing companies, analyzing investments, or when user mentions DCF, financial projections, or valuation models.
---
```

**Why it works:**
- ✅ Lists specific capabilities: "DCF analysis, sensitivity testing, Monte Carlo"
- ✅ Clear use case: "valuing companies, analyzing investments"
- ✅ Technical triggers: "DCF", "financial projections", "valuation models"
- ✅ Includes specialized Python scripts
- ✅ Appropriate complexity for specialized domain

---

## Skill Name Examples

### ❌ Poor Names

```yaml
name: helper
```
**Problem:** Too vague, doesn't describe what it helps with

```yaml
name: document_processor
```
**Problem:** Underscores not allowed, not gerund form

```yaml
name: ProcessingDocuments
```
**Problem:** Not lowercase, capital letters not allowed

```yaml
name: pdf
```
**Problem:** Not gerund form, too generic

```yaml
name: financial-analysis-and-reporting-and-visualization-tool
```
**Problem:** Too long, tries to do too much

---

### ✅ Good Names

```yaml
name: processing-pdfs
```
**Good:** Gerund form, specific about what it processes

```yaml
name: analyzing-financial-statements
```
**Good:** Clear action (analyzing) and object (financial statements)

```yaml
name: validating-api-responses
```
**Good:** Specific task and domain

```yaml
name: generating-technical-documentation
```
**Good:** Clear capability, appropriate scope

```yaml
name: applying-brand-guidelines
```
**Good:** Action-oriented, clear purpose

---

## Description Examples

### ❌ Poor Descriptions

#### Example 1: Too Vague
```yaml
description: Helps with documents
```
**Problems:**
- No specific functionality
- No triggers
- No context for activation
- Could mean anything

---

#### Example 2: What Without When
```yaml
description: Processes PDF files and extracts text content.
```
**Problems:**
- Describes functionality but no usage triggers
- Missing contexts where it should activate
- No data format or task triggers

---

#### Example 3: Too Technical Without Context
```yaml
description: Implements DCF valuation methodology using WACC and terminal value calculations.
```
**Problems:**
- Technical but missing practical triggers
- No mention of when to use it
- Assumes user will say exact technical terms

---

### ✅ Good Descriptions

#### Fair (Minimum Acceptable)
```yaml
description: Processes PDF files to extract text and tables. Use when working with PDF documents.
```
**Improvements over poor:**
- ✅ Has "what" (processes PDF files)
- ✅ Has "when" (working with PDF documents)
- ⚠️ Could use more specific triggers

---

#### Good (Solid Quality)
```yaml
description: Processes PDF files to extract text, tables, and forms. Use when working with PDF documents or when user mentions document extraction, form filling, or PDF manipulation.
```
**Why better:**
- ✅ Specific capabilities listed
- ✅ Multiple triggers: "document extraction", "form filling", "PDF manipulation"
- ✅ Clear activation contexts

---

#### Excellent (Best Practice)
```yaml
description: Calculates key financial ratios and metrics from financial statement data for investment analysis. Use when analyzing company performance, evaluating investments, or when user provides income statements, balance sheets, or cash flow statements.
```
**Why excellent:**
- ✅ Precise functionality: "calculates key financial ratios"
- ✅ Clear purpose: "for investment analysis"
- ✅ Multiple task triggers: "analyzing company performance", "evaluating investments"
- ✅ Data format triggers: "income statements, balance sheets, cash flow statements"
- ✅ Would be discoverable among 100+ skills

---

#### Excellent with Informational + Action Triggers

**Example: Multi-Capability Skill**
```yaml
description: Creates, analyzes, and improves Claude Code hooks including configuration, scripts, and security validation. Use when user asks how hooks work, explaining hook concepts, understanding hook types and event lifecycle, describing hook configuration, creating new hooks, analyzing existing hooks for improvements, validating hook security, debugging hook activation, or when user mentions "PreToolUse", "PostToolUse", "SessionStart", or other hook event types.
```
**Why this is excellent:**
- ✅ **Informational triggers first**: "how hooks work", "explaining hook concepts", "understanding hook types"
- ✅ **Action triggers match capabilities**: "creating", "analyzing", "validating", "debugging" (all things this skill does)
- ✅ Activates for both learning questions AND action tasks
- ✅ Specific technical triggers: "PreToolUse", "PostToolUse", "SessionStart"
- ✅ Covers full scope: conceptual understanding + practical implementation

---

**Example: Formatting-Only Skill**
```yaml
description: Enforces Python coding standards (PEP 8), clean code principles, and maintainability patterns. Use when user asks about Python best practices, explaining PEP 8 standards, understanding clean code principles, describing Python code organization patterns, formatting Python files, applying code standards, or reviewing code style.
```
**Action triggers match capabilities:**
- ✅ "formatting" - skill formats code
- ✅ "applying" - skill applies standards
- ✅ "reviewing" - skill reviews style
- ❌ NO "creating" - skill doesn't create new files from scratch
- ❌ NO "generating" - not a code generation skill

---

**Example: Analysis-Only Skill**
```yaml
description: Analyzes existing skills for quality, organization, and best practices compliance. Use when user asks how skill analysis works, explaining skill evaluation criteria, understanding skill quality metrics, analyzing skills, evaluating skill effectiveness, reviewing skill structure, or assessing skill organization.
```
**Action triggers match capabilities:**
- ✅ "analyzing" - skill analyzes content
- ✅ "evaluating" - skill evaluates quality
- ✅ "reviewing" - skill reviews structure
- ✅ "assessing" - skill assesses organization
- ❌ NO "creating" - this skill doesn't create skills
- ❌ NO "formatting" - not a formatting skill

---

#### Comparison: Before and After

**Before (action-only):**
```yaml
description: Creates and manages plugins. Use when creating plugins, bundling skills/commands/hooks/MCPs, generating plugin.json, setting up marketplaces.
```
*Activates for: Action tasks only*
*Misses: "What are plugins?", "How do plugins work?", "Explain plugin structure"*

**After (informational + action triggers):**
```yaml
description: Create, pack, bundle, and manage Claude Code plugins. Use when user asks how plugins work, what plugins are, explaining plugin structure, understanding plugin.json manifest, creating plugins, bundling skills/commands/hooks/MCPs, generating plugin.json, setting up marketplaces.
```
*Activates for: Learning questions AND action tasks*
*Catches: "What are plugins?" → Provides context from skill content*
*Catches: "Create a plugin" → Executes workflow*

---

#### Anti-Pattern: Mismatched Capabilities

```yaml
description: Formats code to style guidelines. Use when creating files, analyzing code quality, generating documentation, or formatting code.
```

**Problems:**
- ❌ "creating files" - formatting skill doesn't create files
- ❌ "analyzing code quality" - formatting applies rules, doesn't analyze quality
- ❌ "generating documentation" - completely unrelated
- ✅ "formatting code" - only correct trigger

**Fixed version:**
```yaml
description: Formats code to style guidelines. Use when user asks about code formatting standards, explaining style rules, understanding formatting conventions, formatting code files, applying style guidelines, or structuring code layout.
```

**Pattern Template:**
```
Use when user asks [how/what/explain domain], [action verb 1 matching capability], [action verb 2 matching capability], or when user mentions [specific terms]
```

---

## Description Evolution: Step-by-Step Improvement

**Starting Point: Too Vague**
```yaml
description: Helps with API work
```
*Problem: No specifics, no triggers*

---

**Step 1: Add What**
```yaml
description: Validates API responses against expected schemas
```
*Better: Now has specific functionality*
*Still Missing: When to use it, triggers*

---

**Step 2: Add When**
```yaml
description: Validates API responses against expected schemas. Use when working with APIs.
```
*Better: Has basic trigger*
*Still Missing: Specific contexts, data formats*

---

**Step 3: Add Specific Triggers**
```yaml
description: Validates API responses against expected schemas. Use when testing APIs, debugging integrations, or when user mentions API validation, response checking, or schema verification.
```
*Better: Multiple specific triggers*
*Still Missing: Data format triggers*

---

**Step 4: Add Data Format Triggers (Excellent)**
```yaml
description: Validates API responses against expected schemas including REST, GraphQL, and webhooks. Use when testing APIs, debugging integrations, verifying data contracts, or when user provides API responses, JSON schemas, or mentions API validation, response checking, or schema verification.
```
*Excellent: Comprehensive triggers across task types, data formats, and keywords*

---

## Progressive Disclosure Examples

### When to Keep Simple (Single File)

**Example: Simple validation skill**
```
validating-email-formats/
└── SKILL.md (120 lines)
```

**Why single file works:**
- Simple, focused task
- No supporting resources needed
- Under 500 lines
- No complex reference data

---

### When to Split (Progressive Disclosure)

#### Before: Bloated Single File
```
applying-brand-guidelines/
└── SKILL.md (850 lines including all color specs, font details, templates, etc.)
```
**Problem:** Too long, hard to navigate, information overload

---

#### After: Progressive Disclosure
```
applying-brand-guidelines/
├── SKILL.md (200 lines - workflow and when to reference REFERENCE.md)
└── REFERENCE.md (400 lines - detailed specs loaded on-demand)
```

**SKILL.md structure:**
```markdown
# Applying Brand Guidelines

## Workflow
1. Identify document type
2. Load brand specifications (see REFERENCE.md)
3. Apply colors, fonts, logos
4. Validate against checklist

## When to Load REFERENCE.md
Load REFERENCE.md when you need:
- Exact color codes and RGB values
- Detailed typography specifications
- Template formats for specific document types
- File naming conventions
```

**Why this works:**
- ✅ SKILL.md stays focused on workflow
- ✅ Details loaded only when needed
- ✅ Clear guidance on when to load supporting files
- ✅ One level deep (no file-to-file-to-file chains)

---

### Pattern: Domain-Specific Organization

**Complex skill with multiple domains:**
```
processing-api-data/
├── SKILL.md (300 lines - main workflow)
├── authentication.md (200 lines - auth details)
├── error-handling.md (150 lines - error scenarios)
└── data-formats.md (200 lines - format specs)
```

**SKILL.md references:**
```markdown
## Step 2: Authenticate
For authentication details, see authentication.md

## Step 4: Handle Errors
If errors occur, see error-handling.md

## Step 5: Parse Response
For format specifications, see data-formats.md
```

**Why this works:**
- Each file focused on one topic
- References give clear context
- Agent loads only what's needed for current step

---

## File Organization Patterns

### Pattern 1: Simple Skill (No Supporting Files)
```
skill-name/
└── SKILL.md
```
**When to use:** Under 500 lines, no scripts, no reference data needed

---

### Pattern 2: Skill with Scripts
```
skill-name/
├── SKILL.md
├── process_data.py
└── validate_output.py
```
**When to use:** Execution requires custom scripts, still under 500 lines total

---

### Pattern 3: Skill with Reference Data
```
skill-name/
├── SKILL.md (workflow)
└── REFERENCE.md (detailed specs)
```
**When to use:** Workflow simple but requires detailed reference information

---

### Pattern 4: Complex Skill with Organization
```
skill-name/
├── SKILL.md (main workflow, ~300 lines)
├── reference.md (specs)
├── examples.md (usage examples)
├── scripts/
│   ├── process.py
│   └── validate.py
└── templates/
    └── output-template.xlsx
```
**When to use:** Complex domain, multiple supporting resources, scripts and templates

---

## Summary: Key Patterns to Follow

### Names
- ✅ Use gerund form: `processing-`, `analyzing-`, `validating-`
- ✅ Be specific: `processing-pdfs` not `document-helper`
- ✅ Use hyphens: `analyzing-financial-statements`
- ❌ Avoid: underscores, capitals, vague terms like "helper", "utils"

### Descriptions
- ✅ Include what it does: "Calculates financial ratios..."
- ✅ Include when to use: "Use when analyzing investments..."
- ✅ Include triggers: "...or when user mentions DCF, valuations, financial statements"
- ❌ Avoid: Vague descriptions without specific triggers

### Content
- ✅ Only domain-specific knowledge Claude doesn't have
- ✅ Company policies, proprietary formats, internal tools
- ✅ Clear workflows with validation steps
- ❌ Avoid: Basic programming, standard libraries, general knowledge

### Structure
- ✅ SKILL.md under 500 lines
- ✅ Progressive disclosure for complex content
- ✅ One level of file references
- ✅ Clear guidance on when to load supporting files
- ❌ Avoid: Monolithic files, deep nesting, information overload
