# Skill Analysis Framework

Systematic framework for evaluating existing agent skills and identifying improvements.

## Analysis Process Overview

1. **Initial Review**: Load and understand the skill
2. **Structured Evaluation**: Apply analysis criteria
3. **Issue Identification**: Categorize findings by severity
4. **Recommendation Generation**: Provide specific, actionable improvements

## Evaluation Criteria

### 1. YAML Frontmatter Analysis

#### 1.1 Name Field
**Check**:
- [ ] Present and non-empty
- [ ] Lowercase letters, numbers, hyphens only (no underscores, spaces, capitals)
- [ ] Under 64 characters
- [ ] Gerund form (verb + -ing)
- [ ] Descriptive and specific (not vague like "helper" or "utils")
- [ ] No conflicts with other skills

**Common Issues**:
- Wrong format: `Process_PDFs`, `processPDFs` (should be: `processing-pdfs`)
- Too vague: `helper`, `utils`, `tool`
- Not gerund: `pdf-processor` (should be: `processing-pdfs`)

**Severity**: Critical if invalid format, Major if vague/unclear

#### 1.2 Description Field
**Check**:
- [ ] Present and non-empty
- [ ] Under 1024 characters
- [ ] Includes what skill does (functionality)
- [ ] Includes when to use it (triggers/contexts)
- [ ] Contains specific trigger keywords
- [ ] Third-person voice
- [ ] Discoverable among many skills

**Quality Levels**:
- **Poor**: "Helps with documents" (too vague, no triggers)
- **Fair**: "Processes PDF files" (what, but no when/triggers)
- **Good**: "Processes PDF files when user works with PDFs" (what + when)
- **Excellent**: "Extracts text and tables from PDF files, fills forms, merges documents. Use when working with PDF files or when user mentions PDFs, forms, or document extraction." (detailed what + specific when + concrete triggers)

**Common Issues**:
- Missing trigger keywords
- Too vague about functionality
- No usage context
- Overly technical without practical triggers

**Severity**: Major if unclear, Minor if could be more specific

#### 1.3 Optional Fields
**Check**:
- [ ] allowed-tools appropriate if present
- [ ] No extraneous fields
- [ ] Proper YAML syntax (no tabs, correct indentation)

**Common Issues**:
- Unnecessary tool restrictions
- Invalid tool names in allowed-tools
- Custom fields that aren't used

**Severity**: Minor if present but not harmful

### 2. Content Structure Analysis

#### 2.1 Overall Organization
**Check**:
- [ ] Logical flow from overview to details
- [ ] Clear section headings
- [ ] Appropriate depth of information
- [ ] Progressive disclosure used for complex content
- [ ] One level of file references (no chains)

**Good Structure Pattern**:
```
1. Overview/Introduction
2. When to Use This Skill
3. Core Workflows/Instructions
4. Progressive Disclosure References
5. Validation/Verification
```

**Common Issues**:
- No clear workflow structure
- Information scattered without organization
- Deep nesting of references
- Missing "when to use" guidance

**Severity**: Major if disorganized, Minor if could be clearer

#### 2.2 Content Length
**Check**:
- [ ] SKILL.md under 5,000 tokens (approximately 500-700 lines)
- [ ] If over 5,000 tokens, appropriate for splitting
- [ ] Supporting files used for detailed content
- [ ] No excessive repetition

**Recommendations**:
- Under 3,000 tokens (~300-400 lines): Good, concise
- 3,000-5,000 tokens (~400-700 lines): Acceptable, monitor for split opportunities
- Over 5,000 tokens (~700+ lines): Should consider progressive disclosure

**Token Estimation**: Approximately 7-10 tokens per line on average

**Severity**: Minor if slightly over (5,000-6,000 tokens), Major if significantly over (>6,500 tokens)

#### 2.3 Workflow Clarity
**Check**:
- [ ] Workflows clearly defined
- [ ] Steps numbered and sequential
- [ ] Decision points clearly marked
- [ ] Validation checkpoints included
- [ ] Examples provided where helpful

**Quality Indicators**:
- Numbered steps with subsections
- Clear input/output expectations
- Decision trees for complex choices
- Checklists for verification

**Common Issues**:
- Vague instructions like "process the data"
- No clear sequence
- Missing validation steps
- Ambiguous decision criteria

**Severity**: Major if workflow unclear, Minor if needs refinement

### 3. Content Quality Analysis

#### 3.1 Conciseness
**Check**:
- [ ] Only includes information Claude doesn't already know
- [ ] No redundant explanations
- [ ] No basic programming/language syntax
- [ ] No standard library documentation
- [ ] Focused on specific domain knowledge

**Red Flags**:
- Explaining basic programming concepts
- Documenting standard library functions
- General best practices Claude already knows
- Unnecessary background information

**Test**: "Does Claude need this information to complete the task?"

**Severity**: Minor if some redundancy, Major if significantly bloated

#### 3.2 Terminology Consistency
**Check**:
- [ ] Same term used throughout for same concept
- [ ] No switching between synonyms
- [ ] Clear definitions for domain-specific terms
- [ ] Abbreviations defined on first use

**Common Issues**:
- API endpoint / URL / path (pick one)
- Function / method / procedure (pick one)
- Variable / parameter / argument (pick one)
- Switching terms without reason

**Severity**: Minor but affects clarity

#### 3.3 Freedom Level Appropriateness
**Check**:
- [ ] Guidance level matches task fragility
- [ ] Flexible tasks have high freedom (general guidance)
- [ ] Standard tasks have medium freedom (preferred patterns)
- [ ] Error-prone tasks have low freedom (exact sequences)

**Evaluation**:
- Too restrictive: Overly specific for flexible tasks
- Too loose: Insufficient guidance for error-prone operations
- Appropriate: Matches task complexity and risk

**Severity**: Major if mismatch causes errors, Minor if suboptimal

### 4. Best Practices Compliance

#### 4.1 Time-Sensitive Content
**Check**:
- [ ] No date-based conditionals
- [ ] Uses "Old patterns" sections instead of dates
- [ ] No "as of [date]" statements
- [ ] No version-specific instructions without maintenance plan

**Examples of Issues**:
```markdown
# Bad
If date is after 2024-01-01, use new API

# Good
## Old Patterns
Previous versions used /v1/api
Current implementation uses /v2/api
```

**Severity**: Minor if easily maintained, Major if will become outdated soon

#### 4.2 Progressive Disclosure
**Check**:
- [ ] Complex content split into multiple files
- [ ] SKILL.md contains high-level workflow
- [ ] Supporting files contain detailed reference
- [ ] Files referenced with context about when to load
- [ ] References one level deep (no file-to-file chains)

**Pattern Quality**:
- Good: SKILL.md → specialized files
- Bad: SKILL.md → guide.md → details.md (too deep)

**Severity**: Major if poor organization impacts usability

#### 4.3 Cross-Platform Compatibility
**Check**:
- [ ] Forward slashes in paths
- [ ] No Windows-specific syntax
- [ ] No hardcoded platform-specific paths
- [ ] Dependencies documented with alternatives

**Common Issues**:
- `C:\Users\file.txt` (use forward slashes: `C:/Users/file.txt`)
- Windows-only tools without alternatives
- Hardcoded paths

**Severity**: Major if breaks on other platforms, Minor if limited impact

### 5. Supporting Files Analysis

#### 5.1 File Organization
**Check**:
- [ ] Logical file names
- [ ] Appropriate subdirectories (templates/, scripts/)
- [ ] All referenced files exist
- [ ] No orphaned files (not referenced)
- [ ] Consistent naming convention

**Good Patterns**:
- `reference.md` - Reference documentation
- `examples.md` - Usage examples
- `validation-rules.md` - Validation criteria
- `templates/` - Template files
- `scripts/` - Executable scripts

**Severity**: Minor if organization could improve

#### 5.2 Script Quality
**Check**:
- [ ] Clear, descriptive names (verb-noun format)
- [ ] Error handling implemented
- [ ] Dependencies documented
- [ ] Comments explain configuration values
- [ ] Can run independently
- [ ] Returns clear success/failure status

**Quality Indicators**:
- Try-catch blocks for error handling
- Logging for debugging
- Documented constants
- Clear input/output specifications

**Severity**: Major if scripts are unreliable, Minor if could be improved

#### 5.3 Reference Document Quality
**Check**:
- [ ] Focused on single topic
- [ ] Clearly structured
- [ ] Appropriate detail level
- [ ] Referenced appropriately from SKILL.md

**Common Issues**:
- Too broad (multiple unrelated topics)
- Too detailed (information overload)
- Not referenced or unclear when to load

**Severity**: Minor if present but suboptimal

### 6. Activation and Discovery Analysis

#### 6.1 Trigger Clarity
**Check**:
- [ ] Description contains specific triggers
- [ ] Triggers match intended use cases
- [ ] Not too broad (false activations)
- [ ] Not too narrow (misses relevant cases)

**Test Questions**:
- Will this activate when it should?
- Will it avoid activating when it shouldn't?
- Are triggers specific enough?
- Are there obvious triggers missing?

**Severity**: Major if activation issues likely

#### 6.2 Discoverability
**Check**:
- [ ] Clear from description what skill does
- [ ] Would be found among 100+ skills
- [ ] Keywords match user language
- [ ] Not obscured by vague terms

**Test**: "If looking for this capability, would this description help find it?"

**Severity**: Major if not discoverable

### 7. Documentation Completeness

#### 7.1 Usage Guidance
**Check**:
- [ ] "When to Use" section present
- [ ] Trigger conditions listed
- [ ] Example scenarios provided (if helpful)
- [ ] Clear success criteria

**Severity**: Major if missing, Minor if incomplete

#### 7.2 Dependencies
**Check**:
- [ ] All dependencies documented
- [ ] Installation instructions provided
- [ ] Version requirements specified
- [ ] Environment requirements noted

**Severity**: Major if dependencies undocumented

#### 7.3 Validation Guidance
**Check**:
- [ ] Verification steps included
- [ ] Success criteria defined
- [ ] Checklists provided for complex tasks
- [ ] Quality checks specified

**Severity**: Minor if missing, Major if verification critical

## Issue Categorization

### Critical Issues
**Impact**: Skill won't load or work at all
**Examples**:
- Invalid YAML syntax
- Name field missing or invalid format
- Description field empty
- Referenced files don't exist

**Action**: Must fix immediately

### Major Issues
**Impact**: Skill works but significantly suboptimal or unreliable
**Examples**:
- Unclear description without triggers
- Disorganized content structure
- Missing critical validation steps
- Severely bloated content
- Poor activation targeting

**Action**: Should fix soon

### Minor Issues
**Impact**: Skill works but could be improved
**Examples**:
- Slightly verbose content
- Could use more specific wording
- Terminology inconsistencies
- Missing optional examples
- Style/formatting inconsistencies

**Action**: Consider fixing during next update

## Analysis Output Format

When analyzing a skill, provide structured feedback:

### 1. Executive Summary
Brief overview of overall skill quality and key findings.

```markdown
## Analysis Summary
Skill: [skill-name]
Overall Quality: [Excellent/Good/Fair/Poor]
Critical Issues: [count]
Major Issues: [count]
Minor Issues: [count]
```

### 2. Detailed Findings

For each category, list findings:

```markdown
## YAML Frontmatter
- ✅ Name format valid
- ⚠️ Description could be more specific (add trigger keywords)

## Content Structure
- ✅ Logical organization
- ❌ SKILL.md is 650 lines (recommend splitting)

## Content Quality
- ✅ Concise and focused
- ⚠️ Some terminology inconsistency (API endpoint vs URL)
```

### 3. Prioritized Recommendations

List recommendations by priority:

```markdown
## Recommendations

### Critical (Fix Immediately)
1. [None identified]

### Major (Fix Soon)
1. Split SKILL.md using progressive disclosure (currently 650 lines)
   - Move detailed API specs to reference.md
   - Move examples to examples.md
   - Keep high-level workflow in SKILL.md

2. Add specific trigger keywords to description
   - Current: "Processes API data"
   - Recommended: "Processes API data when working with REST endpoints, API responses, or when user mentions API integration, webhooks, or HTTP requests"

### Minor (Consider for Next Update)
1. Standardize terminology (use "API endpoint" consistently)
2. Add examples.md with usage scenarios
3. Include validation checklist at end of workflow
```

### 4. Positive Aspects

Highlight what works well:

```markdown
## Strengths
- Clear workflow structure with numbered steps
- Good error handling in scripts
- Appropriate progressive disclosure usage
- Excellent supporting documentation
```

## Improvement Implementation Guide

For each recommended improvement:

### Specify What to Change
```markdown
Change description from:
"Processes financial data"

To:
"Calculates financial ratios and metrics from financial statements. Use when analyzing financial performance, comparing companies, evaluating investments, or when user provides income statements, balance sheets, or cash flow data."
```

### Explain Why
```markdown
Reason: Current description lacks trigger keywords. Adding specific triggers ("financial ratios", "income statements", "balance sheets") and contexts ("analyzing financial performance", "evaluating investments") improves discoverability and ensures activation in relevant scenarios.
```

### Describe How
```markdown
Implementation:
1. Open SKILL.md
2. Locate YAML frontmatter
3. Edit description field
4. Verify length under 1024 characters (current change: 280 chars)
5. Save and restart Claude Code to reload
```

### Indicate Priority
```markdown
Priority: Major
Impact: Significantly improves skill discoverability and activation accuracy
Effort: Low (5 minutes)
```

## Comparative Analysis

When comparing to similar skills or best practices:

### Benchmark Against Examples
Compare to similar skills from cookbooks or documentation:
```markdown
## Comparison to Similar Skills

Similar Skill: analyzing-financial-statements
- Their description includes 6 trigger keywords (financial ratios, investment analysis, income statements, balance sheets, cash flow, performance metrics)
- This skill has 2 trigger keywords
- Recommendation: Add 3-4 more specific triggers
```

### Benchmark Against Best Practices
```markdown
## Best Practices Compliance

| Practice | Status | Notes |
|----------|--------|-------|
| Conciseness | ✅ Good | No redundant content |
| Description specificity | ⚠️ Fair | Needs more triggers |
| Progressive disclosure | ✅ Good | Well organized |
| File organization | ✅ Excellent | Clear structure |
| SKILL.md length | ❌ Poor | 650 lines (target <500) |
```

## Self-Analysis Capability

When analyzing the managing-agent-skills skill itself, use same framework with awareness of meta-nature:

### Special Considerations
- Does it enable effective skill management?
- Does it follow its own best practices?
- Is it self-improving (can it analyze/improve itself)?
- Does it stay current with official documentation?

**Note**: Self-analysis is performed on-demand when requested, not pre-written in the skill itself. Fresh analysis with current context is more valuable than static self-documentation.

## Version Tracking Recommendation

For significant changes:

```markdown
## Version History
Suggest adding version history section:

### Version 1.1 (2024-XX-XX)
- Split SKILL.md into multiple files for progressive disclosure
- Enhanced description with trigger keywords
- Added validation-rules.md reference

### Version 1.0 (2024-XX-XX)
- Initial creation
```

## Checklist for Complete Analysis

- [ ] YAML frontmatter validated
- [ ] Name and description quality assessed
- [ ] Content structure evaluated
- [ ] Content quality checked
- [ ] Best practices compliance verified
- [ ] Supporting files reviewed
- [ ] Activation and discovery assessed
- [ ] Documentation completeness checked
- [ ] Issues categorized by severity
- [ ] Specific recommendations provided
- [ ] Implementation guidance included
- [ ] Positive aspects highlighted
- [ ] Priority levels assigned
