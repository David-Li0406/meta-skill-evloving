# Skill Creation Checklist

Step-by-step guide for creating new agent skills with validation at each stage.

## Phase 1: Planning

### 1.1 Define Purpose
- [ ] Identify the primary capability this skill provides
- [ ] List specific tasks the skill should handle
- [ ] Determine target users or use cases
- [ ] Verify this is a skill, not a slash command (see Decision Matrix below)

### 1.2 Assess Complexity
- [ ] Count number of distinct steps in workflow (1-3: simple, 4-8: medium, 9+: complex)
- [ ] Identify supporting resources needed (scripts, templates, references)
- [ ] Determine if progressive disclosure is needed (>500 lines suggests yes)
- [ ] List dependencies (packages, tools, external resources)

### 1.3 Research Existing Solutions
- [ ] Search for similar existing skills in project and personal directories
- [ ] Check if functionality can be added to existing skill vs. creating new one
- [ ] Review related skills for naming and structure patterns
- [ ] Identify opportunities to reference existing resources

## Phase 2: Design

### 2.1 Name Selection
- [ ] Choose verb in gerund form (verb + -ing)
- [ ] Verify lowercase-with-hyphens format only
- [ ] Confirm name is under 64 characters
- [ ] Ensure name is descriptive and specific (avoid "helper", "utils")
- [ ] Check name doesn't conflict with existing skills

**Validation**: Name matches pattern `^[a-z0-9-]+$` and length <= 64

### 2.2 Description Writing
- [ ] Write what the skill does (core functionality)
- [ ] Add when to use it (contexts and scenarios)
- [ ] Include trigger keywords (task types, data formats, domains)
- [ ] Include informational triggers for the domain: "how [X] works", "explaining [X]", "understanding [X]"
- [ ] Include action triggers ONLY for what the skill actually does (match verbs to capabilities)
- [ ] Verify action triggers don't include unrelated verbs (no "creating" if skill only analyzes)
- [ ] Verify under 1024 characters
- [ ] Test discoverability: Is it clear when to use this among 100+ skills?
- [ ] Use third-person voice

**Template**:
```
[Core functionality description]. Use when [scenarios/contexts], or when user mentions [trigger keywords/phrases].
```

**Validation**:
- Length <= 1024 characters
- Contains both "what" and "when" information
- Includes specific triggers
- Not empty

### 2.3 Structure Planning
- [ ] Decide on single SKILL.md vs. multiple files
- [ ] Plan progressive disclosure if complex:
  - [ ] SKILL.md contains high-level workflow
  - [ ] Supporting files contain detailed guidance
  - [ ] References are one level deep (no file-to-file-to-file chains)
- [ ] Identify sections needed in SKILL.md
- [ ] Plan supporting file names and purposes
- [ ] Design directory structure

### 2.4 Tool Restrictions (Optional)
- [ ] Determine if skill should restrict available tools
- [ ] List allowed tools if restrictions needed
- [ ] Document rationale for restrictions (security, read-only, etc.)

## Phase 3: Implementation

### 3.1 Create Directory Structure
- [ ] Choose location (personal: `~/.claude/skills/` or project: `.claude/skills/`)
- [ ] Create skill directory: `mkdir -p .claude/skills/skill-name`
- [ ] Create subdirectories if needed (templates/, scripts/, etc.)
- [ ] Verify paths use forward slashes (cross-platform compatibility)

### 3.2 Write YAML Frontmatter
- [ ] Create SKILL.md file
- [ ] Add opening delimiter: `---`
- [ ] Add name field: `name: skill-name`
- [ ] Add description field: `description: [your description]`
- [ ] Add allowed-tools if needed: `allowed-tools: Read, Grep, Glob`
- [ ] Add closing delimiter: `---`
- [ ] Verify no tabs in YAML (use spaces)
- [ ] Validate YAML syntax

**Template**:
```yaml
---
name: skill-name
description: Skill description with triggers and usage context
---
```

**Validation**:
- Delimiters `---` present at start and end
- name and description fields present
- No syntax errors
- No tab characters

### 3.3 Write Core Content in SKILL.md

#### Header Section
- [ ] Add main heading: `# Skill Name`
- [ ] Add brief overview paragraph
- [ ] Add "When to Use This Skill" section with trigger list

#### Workflow Section
- [ ] Structure workflows with clear headings
- [ ] Break into numbered steps
- [ ] Use subsections for complex steps
- [ ] Include decision points where applicable
- [ ] Add validation checkpoints

#### Progressive Disclosure Section (if applicable)
- [ ] List supporting files with brief descriptions
- [ ] Explain when to reference each file
- [ ] Keep references one level deep

#### Supporting Information
- [ ] Document dependencies
- [ ] Add usage examples if helpful
- [ ] Include troubleshooting guidance
- [ ] List limitations or constraints

#### Final Validation Section
- [ ] Add checklist for task completion
- [ ] Include verification steps
- [ ] List output requirements

### 3.4 Content Quality Checks
- [ ] Remove information Claude already knows (programming basics, standard libraries)
- [ ] Eliminate redundant content
- [ ] Use consistent terminology throughout
- [ ] Verify conciseness (challenge every sentence)
- [ ] Check token count (target under 5,000 tokens for SKILL.md, approximately 500-700 lines)
- [ ] Verify all file paths use forward slashes (cross-platform compatibility)
- [ ] Ensure no absolute paths with usernames (use relative or tilde paths)
- [ ] Ensure appropriate freedom level:
  - High: General guidance for flexible tasks
  - Medium: Preferred patterns with some flexibility
  - Low: Exact sequences for error-prone operations

### 3.5 Create Supporting Files

For each supporting file:
- [ ] Create file in appropriate location (same directory or subdirectory)
- [ ] Add clear heading and purpose statement
- [ ] Organize content logically
- [ ] Keep focused on single topic
- [ ] Reference from SKILL.md with context

#### Common Supporting Files:
- **reference.md**: Reference documentation, specifications, standards
- **examples.md**: Usage examples, sample inputs/outputs
- **validation-rules.md**: Criteria for validation, quality checks
- **error-handling.md**: Error scenarios and resolution steps
- **templates/**: Template files for outputs

### 3.6 Add Scripts (if applicable)
- [ ] Create scripts in scripts/ subdirectory or skill root
- [ ] Use descriptive verb-noun names (calculate_ratios.py, validate_format.py)
- [ ] Include error handling
- [ ] Add documentation comments
- [ ] Make configuration values self-documenting with comments
- [ ] Document dependencies in script header
- [ ] Test scripts independently

**Script Header Template**:
```python
"""
Script Purpose: [What it does]
Dependencies: [Required packages]
Usage: [How to call it]
"""
```

## Phase 4: Validation

### 4.1 YAML Validation
- [ ] Open SKILL.md and verify frontmatter
- [ ] Check delimiter syntax: `---` at start and end
- [ ] Verify required fields present (name, description)
- [ ] Confirm no tabs (only spaces)
- [ ] Test with YAML validator if available

**Common Errors**:
- Missing delimiters
- Tabs instead of spaces
- Missing name or description
- Special characters in name

### 4.2 Name Validation
- [ ] Format: lowercase letters, numbers, hyphens only
- [ ] Length: under 64 characters
- [ ] Form: gerund (verb + -ing)
- [ ] Descriptive: clear purpose from name
- [ ] Unique: no conflicts with existing skills

**Regex Test**: `^[a-z0-9-]{1,64}$`

### 4.3 Description Validation
- [ ] Length: under 1024 characters
- [ ] Non-empty
- [ ] Includes what skill does
- [ ] Includes when to use it
- [ ] Contains trigger keywords
- [ ] Third-person voice
- [ ] Specific and discoverable

**Test**: Would this description help Claude find this skill among 100+ available skills?

### 4.4 Content Validation
- [ ] SKILL.md under 5,000 tokens (approximately 500-700 lines)
- [ ] Clear section structure
- [ ] Workflows have numbered steps
- [ ] Progressive disclosure used appropriately (multiple .md files if needed)
- [ ] All .md files in root directory are documented (all are loaded automatically)
- [ ] No redundant information
- [ ] Consistent terminology
- [ ] No time-sensitive content (no date conditionals)
- [ ] Cross-platform paths (forward slashes, even on Windows)
- [ ] No absolute paths with usernames (use relative or tilde paths)
- [ ] No Windows-specific syntax

### 4.5 Security Validation
- [ ] No hardcoded API keys, credentials, or secrets
- [ ] No sensitive data in skill files
- [ ] Scripts validate and sanitize inputs
- [ ] allowed-tools field appropriate (not overly permissive)
- [ ] File operations justified and documented
- [ ] Network calls documented (if any)
- [ ] Environment variable access documented (if any)
- [ ] Security considerations section added if skill handles sensitive operations

### 4.5 Best Practices Validation
- [ ] Conciseness: Only necessary information included
- [ ] Specificity: Clear and concrete guidance
- [ ] Focus: Single capability, not multiple unrelated features
- [ ] Organization: Logical flow and structure
- [ ] Completeness: All necessary information present
- [ ] References: One level deep maximum
- [ ] Examples: Provided where helpful
- [ ] Dependencies: Documented completely

### 4.6 File Structure Validation
- [ ] All referenced files exist
- [ ] File paths are correct
- [ ] Directory structure is logical
- [ ] No broken references
- [ ] Supporting files are appropriately named
- [ ] Scripts are in consistent location

## Phase 5: Testing

### 5.1 Syntax Testing
- [ ] Restart Claude Code to load skill
- [ ] Check for loading errors with `claude --debug` (if available)
- [ ] Verify skill appears in available skills
- [ ] Confirm no YAML parsing errors

### 5.2 Functional Testing
- [ ] Create 3-5 test scenarios representing typical use cases
- [ ] Test skill activation with various prompts:
  - Direct request: "Use [skill name] to..."
  - Implicit trigger: Use trigger keywords from description
  - Context-based: Provide context that should activate skill
- [ ] Verify skill loads correctly
- [ ] Confirm instructions are followed accurately
- [ ] Check that supporting files are loaded when needed

### 5.3 Cross-Model Testing (if possible)
- [ ] Test with Haiku (if available)
- [ ] Test with Sonnet
- [ ] Test with Opus (if available)
- [ ] Verify skill works effectively across models
- [ ] Adjust clarity if needed for different models

### 5.4 Edge Case Testing
- [ ] Test with incomplete inputs
- [ ] Test with edge case scenarios
- [ ] Verify error handling
- [ ] Check behavior with missing dependencies
- [ ] Confirm graceful degradation

### 5.5 Team Testing (for project skills)
- [ ] Have teammate test skill without context
- [ ] Observe activation patterns
- [ ] Gather feedback on clarity
- [ ] Identify confusion points
- [ ] Iterate based on feedback

## Phase 6: Documentation and Deployment

### 6.1 Internal Documentation
- [ ] Add comments to complex sections
- [ ] Document any non-obvious decisions
- [ ] Include version history if applicable
- [ ] Add "Last Updated" date if relevant

### 6.2 Usage Documentation (if needed)
- [ ] Create examples.md with usage examples
- [ ] Document common scenarios
- [ ] Show sample inputs and outputs
- [ ] Include troubleshooting tips

### 6.3 Deployment
For personal skills:
- [ ] Placed in `~/.claude/skills/skill-name/`
- [ ] Restart Claude Code to load

For project skills:
- [ ] Placed in `.claude/skills/skill-name/`
- [ ] Commit to git with descriptive commit message
- [ ] Push to repository
- [ ] Notify team members
- [ ] Document in project README or documentation (if applicable)

### 6.4 Maintenance Planning
- [ ] Identify areas that may need updates
- [ ] Plan for dependency updates
- [ ] Consider version tracking approach
- [ ] Establish review schedule if needed

## Decision Matrix: Skill vs Slash Command

Use this matrix to decide between creating a skill or slash command:

| Criteria | Skill | Slash Command |
|----------|-------|---------------|
| **Complexity** | Multi-step workflow, validation loops | Simple prompt |
| **Files** | Multiple files, scripts, templates | Single markdown file |
| **Discovery** | Should activate automatically | User explicitly invokes |
| **Reusability** | Across many conversations | Repeated in specific contexts |
| **Structure** | Needs organization and resources | Straightforward instruction |
| **Team Use** | Standardized workflow needed | Quick reminder or template |

**Choose Skill If**:
- 3+ distinct steps
- Supporting files/scripts needed
- Should activate automatically based on context
- Complex domain knowledge required
- Validation/verification loops needed

**Choose Slash Command If**:
- Simple, single prompt
- No supporting resources
- User wants explicit control
- Quick template or reminder
- One file is sufficient

## Troubleshooting Guide

### Skill Not Loading
1. Check YAML syntax (delimiters, no tabs)
2. Verify file location (correct skills directory)
3. Confirm file named exactly SKILL.md
4. Restart Claude Code
5. Run with --debug flag to see errors

### Skill Not Activating
1. Review description specificity (add more triggers)
2. Test with explicit "use [skill-name]" request
3. Verify trigger keywords are relevant
4. Check if description is too vague
5. Consider if task actually matches skill capability

### Skill Activating Incorrectly
1. Review description for overly broad triggers
2. Make description more specific to intended use cases
3. Remove ambiguous trigger keywords
4. Test with various prompts to identify false positives

### File Not Found Errors
1. Verify all referenced files exist
2. Check file paths and names are correct
3. Ensure references are relative from SKILL.md location
4. Confirm no typos in file references

### Script Execution Failures
1. Check script dependencies are installed
2. Verify script has execution permissions
3. Test script independently outside skill
4. Review error messages in script output
5. Confirm script paths are correct

## Quick Reference

### Minimal Valid SKILL.md
```markdown
---
name: example-skill
description: Does X when user asks for Y or mentions Z keywords
---

# Example Skill

[Core instructions here]
```

### Standard SKILL.md Structure
```markdown
---
name: skill-name
description: Full description with triggers
---

# Skill Name

Brief overview.

## When to Use This Skill

- Trigger 1
- Trigger 2
- Trigger 3

## Workflow

### Step 1: [Name]
Instructions

### Step 2: [Name]
Instructions

## References

- file1.md: Description
- file2.md: Description

## Validation

- [ ] Checklist item
- [ ] Checklist item
```

### File Structure Examples

**Simple Skill**:
```
skill-name/
└── SKILL.md
```

**Medium Complexity**:
```
skill-name/
├── SKILL.md
├── reference.md
└── examples.md
```

**Complex Skill**:
```
skill-name/
├── SKILL.md
├── reference.md
├── examples.md
├── validation-rules.md
├── scripts/
│   ├── process.py
│   └── validate.py
└── templates/
    └── output-template.md
```

## Completion Criteria

Skill is ready for use when:
- [ ] All Phase 1-4 checklists completed
- [ ] Testing shows consistent activation
- [ ] Instructions are clear and followed correctly
- [ ] No errors in loading or execution
- [ ] Team members (if applicable) can use successfully
- [ ] Documentation is complete
- [ ] Deployed to appropriate location
