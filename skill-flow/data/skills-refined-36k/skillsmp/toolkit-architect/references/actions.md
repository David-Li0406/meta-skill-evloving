# Action Types

## create

**Creates new plugin components** with best practices

**Steps**:
1. Load relevant knowledge base
2. Gather requirements
3. Generate component structure
4. Apply best practices
5. Validate compliance
6. Document workflow

**Knowledge Base Integration**:
- `/skills-knowledge` for skill components
- `/commands-knowledge` for command components
- `/subagents-knowledge` for subagent components
- `/hooks-knowledge` for hook components
- `/mcp-knowledge` for MCP components

**Dynamic Context**:
- Current project structure
- Git status and history
- Existing component inventory
- Plugin manifest configuration

## audit

**Audits existing components** for quality and compliance

**Steps**:
1. Load relevant knowledge base
2. Analyze component structure
3. Check compliance
4. Generate audit report
5. Provide recommendations

**Audit Checklist**:
- ✅ YAML frontmatter validity
- ✅ Directory structure compliance
- ✅ URL currency (2026)
- ✅ Best practices adherence
- ✅ Security considerations
- ✅ Progressive disclosure implementation
- ✅ Auto-discovery optimization

**Output**:
- Quality score (0-10)
- Compliance report
- Improvement recommendations
- Priority action items

## refine

**Improves existing components** based on audit findings

**Steps**:
1. Load relevant knowledge base
2. Review current state
3. Identify improvements
4. Apply enhancements
5. Validate changes
6. Document updates

**Refinement Priorities**:
- **High**: Security, critical bugs, architecture violations
- **Medium**: Performance, documentation, best practices
- **Low**: Styling, minor optimizations

**Safety Measures**:
- Create backup before changes
- Validate at each step
- Document all modifications
- Test after refinements
