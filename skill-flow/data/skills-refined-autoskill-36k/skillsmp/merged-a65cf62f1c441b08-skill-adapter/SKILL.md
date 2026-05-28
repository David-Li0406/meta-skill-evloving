---
name: skill-adapter
description: Use this skill to analyze existing plugins, extract their capabilities, and adapt those skills to solve current tasks effectively.
---

# Skill Adapter - Universal Plugin Capability Extractor

## Purpose
Analyzes plugins in the marketplace to understand their capabilities, extracts core patterns and approaches, and adapts those skills to solve the current user's task. Acts as a "skill chameleon" that can adopt any plugin's capabilities.

## How It Works

### 1. Task Analysis
When a user presents a task:
- Identify the core capability needed (e.g., "analyze code quality", "generate documentation", "automate deployment").
- Determine the domain (security, devops, testing, etc.).
- Extract key requirements and constraints.

### 2. Plugin Discovery
Search existing plugins for relevant capabilities:

```bash
# Find plugins in relevant category
ls plugins/community/ plugins/packages/ plugins/examples/

# Search for keywords in plugin descriptions
grep -r "keyword" --include="plugin.json" plugins/

# Find similar commands/agents
grep -r "capability-name" --include="*.md" plugins/
```

### 3. Capability Extraction
For each relevant plugin found, analyze:

**Commands (commands/*.md):**
- Read the markdown content.
- Extract the approach/methodology.
- Identify input/output patterns.
- Note any scripts or tools used.

**Agents (agents/*.md):**
- Understand the agent's role.
- Extract problem-solving approach.
- Note decision-making patterns.
- Identify expertise areas.

**Skills (skills/*/SKILL.md):**
- Read the skill instructions.
- Extract core capability.
- Note trigger conditions.
- Understand tool usage patterns.

**Scripts (scripts/*.sh, *.py):**
- Analyze script logic.
- Extract reusable patterns.
- Identify best practices.
- Note error handling approaches.

### 4. Pattern Synthesis
Combine learned patterns:
- Merge multiple approaches if beneficial.
- Adapt to current context and constraints.
- Simplify or enhance based on user needs.
- Ensure compatibility with the current environment.

### 5. Skill Application
Apply the adapted skill:
- Use the learned approach.
- Follow the extracted patterns.
- Apply best practices discovered.
- Adapt syntax/tools to the current context.

## Example Workflows

### Example 1: Learning Code Analysis from Security Plugins
**User task:** "Analyze this codebase for issues"
1. Search for security and code-analysis plugins.
2. Extract patterns from relevant plugins.
3. Synthesize approach and apply to the user's codebase.

### Example 2: Adopting Documentation Skills
**User task:** "Generate API documentation"
1. Find documentation plugins.
2. Extract approaches and synthesize.
3. Apply combined approach to the user's API.

### Example 3: Learning Automation from DevOps Plugins
**User task:** "Automate deployment process"
1. Search DevOps category.
2. Extract patterns and synthesize deployment workflow.
3. Apply to the user's specific tech stack.

## Reasoning Process

### When to Use Skill Adapter
Trigger when:
- User needs capability that might exist in the marketplace.
- Task could benefit from existing plugin patterns.
- User asks: "Is there a plugin for this?"

### Plugin Selection Criteria
Choose plugins based on:
1. **Relevance**: Matches task domain/requirements.
2. **Quality**: Well-documented, clear approach.
3. **Simplicity**: Not overly complex for the task.

### Adaptation Strategy
When adapting skills:
- **Keep**: Core logic and proven patterns.
- **Adapt**: Syntax, tool names, specific commands.
- **Enhance**: Add error handling, user feedback.
- **Simplify**: Remove unnecessary complexity.

## Limitations and Boundaries

### What Skill Adapter CAN Do:
✅ Read and analyze plugin source code.  
✅ Extract patterns and approaches.  
✅ Adapt methodologies to new contexts.  
✅ Combine multiple plugin capabilities.  

### What Skill Adapter CANNOT Do:
❌ Execute compiled code (MCP servers).  
❌ Access external APIs without credentials.  
❌ Modify original plugins.  

## Success Criteria
Skill adaptation is successful when:
1. User's task is completed effectively.
2. Adapted skill is properly contextualized.
3. Result quality matches or exceeds original plugin.

## Transparency
Always inform the user:
- Which plugins were analyzed.
- What patterns were extracted.
- How the skill was adapted.

## Example Usage
```
User: "I need to validate JSON schemas in my project"
Skill Adapter Process:
1. Searches plugins for JSON validation.
2. Extracts patterns and adapts.
3. Applies validation to the user's schemas.
```

## Meta-Learning
Skill Adapter improves by:
- Tracking which plugins solve which tasks best.
- Learning which patterns are most reusable.

---

**In essence:** Skill Adapter is a meta-skill that makes the entire plugin marketplace available as a learning resource, extracting and applying capabilities on-demand to solve user tasks efficiently.