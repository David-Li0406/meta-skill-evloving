# Skill Quality Checklist

Before considering a skill complete, verify:

## Structure
- [ ] Correct archetype directory structure
- [ ] SKILL.md present and properly formatted
- [ ] YAML frontmatter with name and description
- [ ] workflows/ directory (if Standard or Complex)

## Routing
- [ ] Workflow Routing section present
- [ ] Workflow Routing section is FIRST (after YAML)
- [ ] Every workflow explicitly routed with examples
- [ ] File paths are absolute and correct

## Activation
- [ ] Comprehensive trigger patterns (8-category coverage)
- [ ] "When to Activate This Skill" section detailed
- [ ] USE WHEN in YAML description
- [ ] Natural language variations covered

## Documentation
- [ ] All files referenced in SKILL.md main body
- [ ] Clear purpose and when-to-use for each file
- [ ] Examples provided
- [ ] Related workflows linked

## Integration
- [ ] Registered in skills directory
- [ ] No duplication of CORE context
- [ ] Compatible with existing skills
- [ ] Tested activation with natural language

## Quality
- [ ] Follows naming conventions
- [ ] Progressive disclosure pattern
- [ ] Self-contained but inherits CORE
- [ ] Validated against skill-structure.md

---

## Quality Gates

Every created/updated skill must pass:

### 1. Structural Validation
- Correct archetype directory structure
- Proper file naming conventions
- Required files present

### 2. Routing Validation
- Workflow Routing section present and FIRST
- All workflows explicitly routed
- Activation triggers comprehensive (8-category pattern)

### 3. Documentation Validation
- All files referenced in SKILL.md
- Clear purpose and when-to-use guidance
- Examples provided

### 4. Integration Validation
- No duplication of CORE context
- Compatible with agent workflows
