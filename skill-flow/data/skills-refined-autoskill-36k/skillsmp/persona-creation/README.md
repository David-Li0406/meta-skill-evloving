# Persona Creation Skill

Master the art of creating effective AI agent personas for Jules.

## What This Skill Teaches

This skill provides a comprehensive framework for designing role-specific prompts that guide Jules to execute tasks with precision, following best practices and maintaining project standards.

## Key Concepts

### What is a Persona?

A **persona** is a specialized prompt that:
- Defines a specific role and mission for Jules
- Establishes clear boundaries and constraints
- Provides decision-making frameworks
- Includes project-specific context and conventions
- Documents learnings from previous executions

### Why Use Personas?

Personas help Jules:
- ✅ **Consistency**: Execute tasks the same way every time
- ✅ **Quality**: Follow best practices automatically
- ✅ **Autonomy**: Make good decisions without constant guidance
- ✅ **Learning**: Build on past experiences through journals
- ✅ **Specialization**: Excel at specific types of tasks

## What You'll Learn

1. **Anatomy of Effective Personas**
   - Identity, methodology, toolchain, examples, boundaries

2. **Persona Archetypes**
   - Builder (TDD/Engineering)
   - Sentinel (Security/Quality)
   - Scribe (Documentation)
   - Artisan (Polish/UX)
   - Weaver (Integration)
   - Janitor (Cleanup)
   - Bolt (Performance)

3. **Creation Workflow**
   - 10-step process from concept to tested persona

4. **Advanced Techniques**
   - Persona inheritance
   - Context injection with Jinja2
   - Conditional behavior
   - Multi-phase workflows

5. **Real-World Examples**
   - Privacy-first data processor
   - Performance optimizer
   - TDD builder
   - Security sentinel

## Quick Start

### Creating Your First Persona

1. **Choose an archetype** (Builder, Sentinel, etc.)
2. **Define the role** (name, emoji, mission)
3. **Create the methodology** (step-by-step process)
4. **Add examples** (good vs bad)
5. **Set boundaries** (always/sometimes/never)
6. **Save to `.team/`** directory
7. **Test with a real task**

### Example: Creating a "Janitor" Persona

```markdown
You are "Janitor" 🧹 - a meticulous cleanup specialist who removes technical debt safely.

Your mission is to clean up the codebase using dead code analysis and safe refactoring.

## The Cleanup Protocol

1. 🔍 SCAN - Find unused code with vulture
2. ✅ VERIFY - Confirm with coverage reports
3. 🗑️ REMOVE - Delete safely with tests
4. 📝 DOCUMENT - Log what was removed and why
```

## File Organization

### Where to Save Personas

**Active personas** (with journals):
- `.team/{persona_name}.md`

**Prompt templates**:
- `.team/personas/{persona_name}.md`
- `.team/personas/{persona_name}.md.jinja2` (with dynamic context)

## Common Use Cases

### Use Case 1: TDD Development
Create a "Builder" persona that enforces Red-Green-Refactor cycle.

### Use Case 2: Security Audits
Create a "Sentinel" persona that hunts for vulnerabilities.

### Use Case 3: Documentation Updates
Create a "Scribe" persona that maintains accurate docs.

### Use Case 4: Performance Optimization
Create a "Bolt" persona that profiles and optimizes code.

### Use Case 5: Code Cleanup
Create a "Janitor" persona that removes dead code safely.

## Best Practices

### DO:
- ✅ Start with a clear, memorable identity
- ✅ Define a systematic, repeatable process
- ✅ Include concrete code examples
- ✅ Specify exact commands and tools
- ✅ Set clear boundaries
- ✅ Test with real tasks

### DON'T:
- ❌ Be vague or philosophical
- ❌ Create conflicting instructions
- ❌ Skip verification steps
- ❌ Use generic examples
- ❌ Forget project context

## Resources

- **SKILL.md**: Complete guide to persona creation
- **examples.md**: Multiple ready-to-use persona templates
- **Existing personas**: See `.team/` directory for real examples

## When to Use This Skill

Invoke this skill when:
- Creating a new persona for Jules
- Improving an existing persona
- Standardizing task execution
- Teaching Jules project-specific workflows
- Documenting best practices in executable form

## Examples in This Repository

See these existing personas for inspiration:
- `.team/builder.md` - TDD-driven development (implied from user's example)
- `.team/sentinel.md` - Security vulnerability tracking
- `.team/scribe.md` - Documentation maintenance
- `.team/artisan.md` - UX polish and improvements
- `.team/bolt.md` - Performance optimization

## Quick Reference

| Archetype | Best For | Key Trait |
|-----------|----------|-----------|
| **Builder** | Features, bugs, refactoring | Systematic TDD |
| **Sentinel** | Security, quality audits | Threat modeling |
| **Scribe** | Documentation, knowledge | Accuracy & clarity |
| **Artisan** | UX, polish, details | User empathy |
| **Weaver** | Integration, pipelines | Data flow |
| **Janitor** | Cleanup, tech debt | Safe refactoring |
| **Bolt** | Performance, optimization | Measurement |

## Getting Started

1. Read `SKILL.md` for comprehensive guidance
2. Review `examples.md` for ready-to-use templates
3. Study existing personas in `.team/`
4. Create your first persona using the template
5. Test it with a real Jules session
6. Iterate based on results

---

**Remember**: A good persona is specific, systematic, and testable. If Jules can't understand what to do, the persona needs more clarity.
