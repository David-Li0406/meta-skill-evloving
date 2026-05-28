# Spec Assistant - Quick Start

## 🚀 One-Minute Guide

### How to Activate

Just say any of these in Cursor:

```
"Help me spec out a new authentication feature"
"I need to build a specification for user notifications"
"Let's gather requirements for the reporting system"
"Can you help me plan this feature before coding?"
```

**No slash command needed!** The skill activates automatically.

### What Happens Next

1. You'll see: "🔍 **Entering Spec-Building Mode**..."
2. The agent asks 5 initial discovery questions
3. You answer one at a time
4. Together you build a complete spec through 4 phases

### The 4 Phases

```
Phase 1: SPECIFY → High-level vision
Phase 2: PLAN    → Technical blueprint  
Phase 3: TASKS   → Implementation breakdown
Phase 4: IMPLEMENT → Code generation
```

### Six Core Areas

Every spec covers:

1. **Commands**: Full commands with flags
2. **Testing**: Framework, location, coverage
3. **Structure**: Folder organization
4. **Style**: Code examples
5. **Git**: Branch/commit/PR format
6. **Boundaries**: Always/Ask/Never tiers

### Three-Tier Boundaries

- ✅ **Always**: Actions that don't need approval
- ⚠️ **Ask First**: Changes needing review
- 🚫 **Never**: Hard stops

## 💡 Pro Tips

1. **Be specific**: "JWT auth with refresh tokens" beats "authentication"
2. **Show examples**: One code snippet beats paragraphs of description
3. **Define success**: Make every criterion testable
4. **Trust the process**: Don't skip phases - each builds on the last

## 🎯 Example Session

```
You: "Help me spec out user authentication"

Agent: "🔍 Entering Spec-Building Mode - I'll help you build 
        a complete spec before any code is written. Let me ask 
        some clarifying questions...
        
        In one sentence: what outcome do you want from this feature?"

You: "Users can securely log in with email/password and stay 
      logged in across sessions"

Agent: "Who will use this? What problem does it solve for them?"

[... continues through discovery questions ...]
```

## 📋 Output Format

You'll get a structured specification:

```markdown
# Feature Name Specification

## Objective
[Problem, users, outcome]

## User Stories
- As a [user], I want [goal] so that [benefit]

## Technical Requirements
- Tech Stack: [specific versions]
- Architecture: [how it connects]
- Constraints: [performance, security]

## Acceptance Criteria
- [ ] Given [state], When [action], Then [outcome]

## Implementation Tasks
1. [Specific, testable task]

## Boundaries
- ✅ Always: [...]
- ⚠️ Ask First: [...]
- 🚫 Never: [...]
```

## ❓ Common Questions

**"Will this activate every time?"**
No - only when you mention spec-related keywords.

**"Can I use the old command?"**
Yes - `/spec-assistant` still works from `commands/`.

**"How do I disable it?"**
Rename the directory to `spec-assistant.disabled`.

**"Can I customize it?"**
Yes - edit `SKILL.md` to match your workflow.

---

**Ready?** Just say "help me spec out [your feature]" in Cursor!
