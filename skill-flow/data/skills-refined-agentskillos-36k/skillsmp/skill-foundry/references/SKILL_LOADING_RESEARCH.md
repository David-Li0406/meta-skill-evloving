# How VS Code / GitHub Copilot Agent Skills are discovered and loaded (Jan 2026)

This document answers the five "what actually happens?" questions about **Agent Skills** in VS Code / GitHub Copilot, based on current public documentation + the Agent Skills open standard.

Based on research conducted January 2026 using Claude Sonnet 4.5 and ChatGPT 5.2 against official documentation.

---

## TL;DR (what's actually documented)

- **Skills are discovered from specific folders**:
  - **Project (repo) skills:** `.github/skills/` (recommended) or `.claude/skills/` (legacy/back-compat)
  - **Personal (user) skills:** `~/.copilot/skills/` (recommended) or `~/.claude/skills/` (legacy/back-compat)  
  Source: VS Code docs + GitHub Docs
  - VS Code: https://code.visualstudio.com/docs/copilot/customization/agent-skills
  - GitHub Docs: https://docs.github.com/en/copilot/concepts/agents/about-agent-skills

- **Enablement is a setting:** `chat.useAgentSkills` (Experimental)  
  Source: VS Code release notes + settings reference  
  - Release notes: https://code.visualstudio.com/updates
  - Settings reference: https://code.visualstudio.com/docs/copilot/reference/copilot-settings

- **Loading is on-demand via "match to description"**:
  - Copilot "always reads" each skill's **name + description** (frontmatter)
  - When your request **matches the description**, Copilot **loads the SKILL.md instructions into the agent context**  
  Source: GitHub Docs ("How Copilot uses skills")  
  - https://docs.github.com/en/copilot/concepts/agents/about-agent-skills

- **Progressive disclosure is the core design**:
  - **Level 1:** name+description (discovery)
  - **Level 2:** full SKILL.md body (only when activated)
  - **Level 3:** references/assets/scripts (only when explicitly needed / requested by the skill instructions)  
  Source: Agent Skills specification  
  - https://agentskills.io/specification

---

## 1) How does "description matching" work?

### What's explicitly documented
GitHub's documentation describes the matching behavior at a **product level**, not the exact algorithm:

- Copilot "always reads" each skill's **name + description** (frontmatter)
- It activates a skill when your request **matches the description** and then injects the skill's instructions into context  
Source: https://docs.github.com/en/copilot/concepts/agents/about-agent-skills

### What's *not* explicitly documented (and what that implies)
Public docs **do not specify** whether matching is:
- pure keyword match,
- embedding similarity,
- LLM-based reasoning over descriptions,
- or a hybrid.

Given how the open standard is written, you should assume **implementation-specific matching** (different agents can choose different retrieval strategies), and treat **the description field as the primary "trigger surface"**.

### Practical guidance (how to make matching reliable)

Write descriptions that:
1. **Explicitly state "Use when..."** (don't be subtle)
2. **Include synonyms + key nouns + verbs** (words appearing in user prompts)
3. **List 2-4 concrete trigger phrases** (direct examples)

This aligns with Agent Skills standard: descriptions communicate "what it does and when to use it", and the body should include instructions/examples.

**Example description that triggers reliably:**
```yaml
---
name: viewcomponent-design-system
description: >
  Building Rails ViewComponents, shadcn-rails UI kits, design systems, or Stimulus/Hotwire views.
  Use when: implementing ViewComponents, designing component libraries, styling with shadcn-rails,
  connecting Stimulus controllers, managing modal/portal dialogs, or defining component slots.
  Keywords: ViewComponent, component, shadcn-rails, design system, UI kit, form, modal.
---
```

**Key insight:** Better descriptions = more reliable skill loading across different LLM backends.

---

## 2) When does skill loading happen?

### Documented behavior
VS Code and GitHub both describe **on-demand loading**:
- Skills are **detected** (discovered) from the folder(s)
- They are **loaded into chat context when relevant**  
Sources:
- VS Code docs: https://code.visualstudio.com/docs/copilot/customization/agent-skills
- VS Code release notes: https://code.visualstudio.com/updates
- GitHub Docs: https://docs.github.com/en/copilot/concepts/agents/about-agent-skills

### Practical interpretation
The pipeline is:

1. **Discovery phase:** Build internal list of skills (Level 1: name+description from frontmatter)
2. **Request phase:** When you send a message, system evaluates which skills match using request text + context
3. **Context assembly:** Activated skills' SKILL.md content is attached to model request **before** response generation

**Important:** Loading happens "upfront" before response generation, not mid-response. It's a pre-request assembly step.

---

## 3) What's the loading process—SKILL.md vs references/?

### Progressive disclosure (the real architecture)
The Agent Skills spec formalizes **progressive disclosure levels**:

- **Level 1:** name + description in frontmatter (always available for discovery)
- **Level 2:** SKILL.md body (loaded when skill is activated/selected)
- **Level 3:** references/, assets/, scripts/ (NOT loaded unless skill instructions explicitly request them)

Source: https://agentskills.io/specification

### What the model actually sees
When activated, the system loads the **SKILL.md body** into the agent's context.

**Token efficiency best practice:**
- Keep SKILL.md concise (150-300 lines ideal)
- Put bulk material (deep guides, catalogs, indexes) in Level 3 references/
- This optimizes token use while keeping detailed resources available

---

## 4) Why don't "app-level" skills work?

### Supported locations (official VS Code docs)
VS Code's "Use Agent Skills" documentation lists:
- **Project skills:** `.github/skills/` (recommended) or `.claude/skills/` (legacy)
- **Personal skills:** `~/.copilot/skills/` (recommended) or `~/.claude/skills/` (legacy)

Source: https://code.visualstudio.com/docs/copilot/customization/agent-skills

### Common mistake: `.copilot/skills` (repo-local)
Many users create `.copilot/skills/` inside the repo, but:
- `.copilot/skills/` **is NOT a documented project skill directory**
- The documented personal directory is `~/.copilot/skills/` (user home, not repo)
- If you used `.copilot/skills/` (repo-local), discovery **will fail**

**Fix:** Use `.github/skills/` for project-level skills.

### Another gotcha: VS Code versions and rollout timing
Agent Skills landed as experimental in VS Code 1.108 (December 2025).  
Early/insiders builds may have only scanned `.claude/` paths during rollout.

Current stable (Jan 2026+): `.github/skills/` is the primary location.

---

## 5) Skill scope / precedence / disabling

### Scope (documented)
VS Code supports:
- **Project skills** in repo-level `.github/skills/` or `.claude/skills/`
- **Personal skills** in user-home `~/.copilot/skills/` or `~/.claude/skills/`

Source: https://code.visualstudio.com/docs/copilot/customization/agent-skills

### Precedence (NOT formally documented)
Official docs don't define rules like:
- "Project overrides personal if names collide"
- "Only top N skills load"
- "Tie-breakers by folder location"

**Best practice to avoid surprises:**
- Keep skill names globally unique (across personal + project)
- Keep skills single-purpose (one workflow each)
- If two skills might match the same query, include "When NOT to use" section
- Include explicit deferral instructions if one skill should delegate to another

### Disabling skills
No per-skill disable toggle is documented yet.

**Current options:**
1. Delete/rename the skill folder (discovery stops immediately)
2. Disable all skills: `chat.useAgentSkills = false` in VS Code settings

Sources:
- VS Code release notes: https://code.visualstudio.com/updates
- Settings reference: https://code.visualstudio.com/docs/copilot/reference/copilot-settings

---

## How to debug: "Did my skill load?"

### Method 1: Use the Chat Debug view
VS Code recommends the **Chat Debug view** to inspect what was sent to the model.

Source: VS Code debugging docs: https://code.visualstudio.com/docs/copilot/customization/custom-instructions

### Method 2: Controlled trigger tests
Create a test skill with a *very specific* trigger phrase:

```yaml
name: test-skill
description: TRIGGER_PHRASE_9Q3X (use only for debugging)
```

Then prompt: "TRIGGER_PHRASE_9Q3X - answer X"

- If skill loads: relevance matching is working ✅
- If skill doesn't load: discovery/config/path problem ❌

### Method 3: Confirm discovery (sanity checks)
1. Is `chat.useAgentSkills: true` set in User AND Workspace settings?
2. Skill path is exactly: `.github/skills/<skill-name>/SKILL.md` ?
3. File name is exactly `SKILL.md` (case-sensitive)?
4. Run discovery test: Ask "List all available skills" and verify skill name appears

Sources:
- VS Code docs: https://code.visualstudio.com/docs/copilot/customization/agent-skills
- GitHub Docs: https://docs.github.com/en/copilot/concepts/agents/about-agent-skills

---

## Summary: What to rely on, what to assume

### ✅ Reliable (documented)
- Skills discovered from `.github/skills/`
- On-demand loading via description matching
- Progressive disclosure (Level 1 → 2 → 3)
- Requires `chat.useAgentSkills: true` setting

### ⚠️ Implementation-specific (not documented)
- Exact matching algorithm (keywords vs embeddings vs reasoning)
- Precedence when multiple skills match
- Per-skill disable mechanism
- Token budgets per skill

### 🎯 Best practice
Focus on what's documented and controllable:
- Write **crystal-clear descriptions** with explicit "Use when..." language
- Keep **SKILL.md concise** (use Level 3 references for bulk material)
- Test with **controlled prompts** to verify loading
- Keep skills **non-overlapping** to avoid precedence confusion

---

## Research sources

- VS Code "Use Agent Skills": https://code.visualstudio.com/docs/copilot/customization/agent-skills
- VS Code Release Notes (Agent Skills in 1.108): https://code.visualstudio.com/updates
- GitHub Docs "About Agent Skills": https://docs.github.com/en/copilot/concepts/agents/about-agent-skills
- Agent Skills open standard: https://agentskills.io/specification
- VS Code settings reference: https://code.visualstudio.com/docs/copilot/reference/copilot-settings
- VS Code debugging guidance: https://code.visualstudio.com/docs/copilot/customization/custom-instructions

---

**Document version:** 1.0  
**Last updated:** January 2026  
**Status:** Based on publicly available documentation as of Jan 2026  
