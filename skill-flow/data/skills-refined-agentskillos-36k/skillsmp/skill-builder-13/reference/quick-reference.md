# Agent Skills Best Practices - Quick Reference

> **Quick access guide** for building efficient, maintainable Claude Code skills. For detailed architectural patterns, see [philosophy.md](./philosophy.md).

**📑 Navigation**: [quick-reference.md](./quick-reference.md) | [philosophy.md](./philosophy.md) | [Skill Creation Process](./skill-creation-process.md)

---

## 🎯 Progressive Disclosure: Core Principle

**Progressive disclosure is the core design principle that makes Agent Skills flexible and scalable.** Like a well-organized manual that starts with a table of contents, then specific chapters, and finally a detailed appendix, skills let Claude load information only as needed:

| Level | File | Context Window | # Tokens |
|-------|------|----------------|----------|
| **1** | SKILL.md Metadata (YAML) | Always loaded | ~100 |
| **2** | SKILL.md Body (Markdown) | Loaded when Skill triggers | <5k |
| **3+** | Bundled files (text files, scripts, data) | Loaded as-needed by Claude | unlimited* |

**Key takeaways:**
- **Level 1 (Metadata)**: ~100 tokens, always in context - make it count!
- **Level 2 (Body)**: <5k tokens, loaded on trigger - keep focused
- **Level 3+ (Bundled)**: Unlimited, loaded as needed - reference from Level 2

**This means:** Your SKILL.md should be a **table of contents and quick reference**, not a comprehensive manual. Link to detailed files that Claude loads only when needed.

---

## 📑 Navigation

- **[philosophy.md](./philosophy.md)** - Comprehensive guide with architectural patterns
- **[Progressive Disclosure](./progressive-disclosure.md)** - Design philosophy & UX patterns
- **[Dynamic Manifests](./dynamic-manifests.md)** - Runtime capability discovery
- **[Deferred Loading](./deferred-loading.md)** - Lazy initialization & optimization

---

## ⚡ Quick Start Checklist

Building a new skill? Follow this checklist:

- [ ] **Metadata (Level 1)**: Clear `name` and `description` (~100 tokens total)
- [ ] **Body (Level 2)**: Core instructions under 5k tokens (aim for <2k)
- [ ] **Bundled files (Level 3+)**: Complex details in separate files
- [ ] Move deterministic logic to executable scripts (not generated code)
- [ ] Extract shared utilities to reusable modules
- [ ] Add environment variable support for credentials
- [ ] Include error messages with troubleshooting steps
- [ ] Test with actual Claude usage

---

## 🎯 Core Principles (Summary)

### 1. Progressive Disclosure
Structure in layers:
- **Metadata** (always loaded) → **SKILL.md body** (on trigger) → **Linked files** (as needed)

### 2. Code > Tokens
Use scripts for deterministic tasks (API calls, data processing, calculations)

### 3. Keep SKILL.md Focused
<5k tokens (<2k recommended), scannable, action-oriented

### 4. Reusable Components
Extract shared logic to prevent duplication

### 5. Clear Metadata
Specific description helps Claude know when to trigger

### 6. Error Handling
Provide actionable feedback and troubleshooting steps

### 7. Logical Structure (Respecting Token Limits)

**⚠️ CRITICAL: Reference files MUST be in `/reference/` folder, NOT in root!**

```
skill-name/
├── SKILL.md              # Level 1+2: Metadata (~100) + Body (<5k tokens)
├── reference/            # ✅ REQUIRED: Level 3 detailed docs (loaded as-needed)
│   ├── detail1.md        #    ✅ All .md reference files go HERE
│   └── detail2.md        #    ✅ NOT in root directory
├── scripts/              # Level 3: Executable code
└── shared/               # Level 3: Reusable utilities
```

**❌ WRONG - Reference files in root:**
```
skill-name/
├── SKILL.md
├── detail1.md            # ❌ WRONG! Should be in reference/
├── detail2.md            # ❌ WRONG! Should be in reference/
└── scripts/
```

**✅ CORRECT - Reference files in /reference/ folder:**
```
skill-name/
├── SKILL.md
├── reference/
│   ├── detail1.md        # ✅ CORRECT!
│   └── detail2.md        # ✅ CORRECT!
└── scripts/
```

### 8. Iterate
Test → Monitor → Refine based on actual usage

### 9. Security
No hardcoded secrets, audit third-party skills

### 10. Test
Smoke test scripts, verify with Claude, check error messages

---

## 📝 SKILL.md Template (Token-Aware)

```markdown
---
# Level 1: Metadata (~100 tokens) - Always loaded
name: skill-name
description: Specific description of what this does (triggers skill selection)
version: 1.0.0
---

# Level 2: Body (<5k tokens, <2k recommended) - Loaded on trigger

## When to Use
- Trigger condition 1
- Trigger condition 2

## Quick Start
1. Run `scripts/main.py --arg value`
2. Review output

## Advanced Usage
For complex scenarios, see [reference/advanced.md](./reference/advanced.md)
For API details, see [reference/api-spec.md](./reference/api-spec.md)

# Level 3: Bundled files - Loaded as-needed by Claude
# (Don't embed large content here - link to it!)
```

**Token budget guide:**
- Metadata: ~100 tokens
- Body target: <2k tokens (max 5k)
- If approaching 2k, move details to bundled files

---

## 🚫 Common Pitfalls

| ❌ Don't | ✅ Do |
|----------|-------|
| **Put reference files in root** | **Put reference files in /reference/ folder** |
| Put everything in SKILL.md | Split into focused files (Level 3) |
| Generate code via tokens | Write executable scripts |
| Vague names ("helper-skill") | Specific names ("pdf-form-filler") |
| Hardcode credentials | Use environment variables |
| >5k token SKILL.md body | Keep under 2k tokens (max 5k) |
| >100 token metadata | Concise name + description (~100) |
| Duplicate logic | Extract to shared modules |
| Generic descriptions | Specific trigger keywords |

---

## 🔧 Recommended Structure (Token-Optimized)

**⚠️ MANDATORY: All reference .md files MUST be in `/reference/` folder!**

```
my-skill/
├── SKILL.md                 # Level 1+2: Metadata (~100) + Body (<2k tokens)
│                            # Quick reference + links to Level 3
│
├── README.md                # Human documentation (optional, not loaded)
│
├── reference/               # ✅ REQUIRED: Level 3 detailed docs (loaded as-needed)
│   ├── api_spec.md          #    ✅ All detailed .md files go HERE
│   ├── examples.md          #    ✅ NOT in root directory!
│   └── advanced.md          #    ✅ Link from SKILL.md as ./reference/file.md
│
├── scripts/                 # Level 3: Executable tools (loaded as-needed)
│   ├── main_tool.py
│   └── helper.py
│
└── shared/                  # Level 3: Reusable components
    ├── __init__.py
    ├── config.py            # Centralized config
    ├── api_client.py        # API wrapper
    └── formatters.py        # Output formatting
```

**Key principles:**
1. SKILL.md is the table of contents. Details go in Level 3 files.
2. **ALL reference .md files MUST be in `/reference/` folder**
3. Link to them as `./reference/filename.md` from SKILL.md

---

## 🎨 Metadata Best Practices

### Good Metadata
```yaml
---
name: pdf-form-filler
description: Fill out PDF forms by extracting fields and inserting values
---
```
- Specific about function
- Contains keywords Claude might see
- Clear trigger conditions

### Poor Metadata
```yaml
---
name: pdf-skill
description: A skill for working with PDFs
---
```
- Too generic
- Vague purpose
- Unclear when to trigger

---

## 🛡️ Error Handling Pattern

```python
class AuthenticationError(Exception):
    """Raised when API authentication fails"""
    pass

try:
    client.authenticate()
except AuthenticationError:
    print("❌ Authentication failed")
    print("\nTroubleshooting:")
    print("1. Verify API_KEY environment variable is set")
    print("2. Check API endpoint is accessible")
    print("3. Ensure network connectivity")
```

**Include:**
- Custom exception types
- Clear error messages with context
- Numbered troubleshooting steps
- Graceful degradation when possible

---

## 🔍 When to Use Each Pattern

### Use Progressive Disclosure When:
- Skill has optional advanced features
- Documentation is extensive
- Users have varying expertise levels
- See: [topics/progressive-disclosure.md](./progressive-disclosure.md)

### Use Dynamic Manifests When:
- Capabilities change based on context
- Features depend on user permissions
- Tools should appear/disappear dynamically
- See: [topics/dynamic-manifests.md](./dynamic-manifests.md)

### Use Deferred Loading When:
- Skill has heavy dependencies
- Not all features used every time
- Startup time matters
- See: [topics/deferred-loading.md](./deferred-loading.md)

---

## ✅ Skill Structure Validation Checklist

**Run this checklist BEFORE considering a skill complete:**

- [ ] **Folder Structure**:
  - [ ] `/reference/` folder exists
  - [ ] ALL .md reference files are IN `/reference/` folder
  - [ ] NO .md files in root (except SKILL.md and optional README.md)
  - [ ] `/scripts/` folder exists (if scripts needed)
  - [ ] `/shared/` folder exists (if shared utilities needed)
- [ ] **SKILL.md Structure**:
  - [ ] Metadata section exists (~100 tokens)
  - [ ] Body is <2k tokens (max 5k)
  - [ ] Links to reference files use `./reference/filename.md` format
  - [ ] No large content blocks embedded (moved to /reference/)
- [ ] **Progressive Disclosure**:
  - [ ] Level 1 (metadata) is concise
  - [ ] Level 2 (body) is a table of contents
  - [ ] Level 3 (reference files) contains details

## 📊 Optimization Checklist

- [ ] **Token Efficiency**:
  - Metadata ~100 tokens
  - Body <2k tokens (max 5k)
  - Detailed content in Level 3 files IN `/reference/` folder
- [ ] **Code Execution**: Deterministic tasks in scripts
- [ ] **Lazy Loading**: Heavy imports deferred (Level 3)
- [ ] **Caching**: Results cached when appropriate
- [ ] **Shared Utilities**: Common code extracted
- [ ] **Environment Config**: Credentials via env vars
- [ ] **Error Recovery**: Graceful failure handling
- [ ] **Progressive Disclosure**: SKILL.md links to details in `/reference/`, doesn't embed them
- [ ] **Folder Hierarchy**: All reference .md files in `/reference/` folder

---

## 🧪 Testing Workflow

```bash
# 1. Manual smoke test
cd skill-name/scripts
python main_tool.py --test-mode

# 2. Test with Claude
"Use the my-skill to process test data"

# 3. Verify checklist
✓ Works on first try?
✓ Error messages helpful?
✓ Claude understands how to use it?
✓ No credentials in code?
```

---

## 🛠️ Step-by-Step Process

**Building a new skill?** Follow the systematic process:

→ **[Skill Creation Process Guide](./skill-creation-process.md)** - Complete walkthrough from planning to deployment

Includes:
- 5-phase process (Planning → Structure → Implementation → Testing → Refinement)
- Full working example: `incident-triage` skill
- Copy-paste templates for all components
- Token optimization at every step
- Adaptation checklist for your use case

---

## 📚 Additional Resources

- [Skill Creation Process](./skill-creation-process.md) - Step-by-step guide with example
- [Anthropic: Equipping Agents with Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Skills Documentation](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
- [Skills Cookbook](https://github.com/anthropics/claude-cookbooks/tree/main/skills)
- [MCP Official Spec](https://spec.modelcontextprotocol.io/)

---

## 🗺️ Full Documentation

For comprehensive guides on architectural patterns, implementation details, and advanced techniques, see:

→ **[philosophy.md](./philosophy.md)** - Start here for the complete best practices guide

**Last Updated**: 2025-10-20
