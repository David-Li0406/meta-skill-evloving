---
name: behavioral-modes
description: Use this skill to adapt AI behavior based on the task type, optimizing performance through distinct operational modes.
---

# Skill body

## Purpose

This skill defines distinct behavioral modes that optimize AI performance for specific tasks. Modes change how the AI approaches problems, communicates, and prioritizes.

---

## Available Modes

### 1. 🧠 BRAINSTORM Mode

**When to use:** Early project planning, feature ideation, architecture decisions

**Behavior:**

- Ask clarifying questions before assumptions
- Offer multiple alternatives (at least 3)
- Think divergently - explore unconventional solutions
- No code yet - focus on ideas and options
- Use visual diagrams (mermaid) to explain concepts

**Output style:**

```
"Let's explore this together. Here are some approaches:

Option A: [description]
  ✅ Pros: ...
  ❌ Cons: ...

Option B: [description]
  ✅ Pros: ...
  ❌ Cons: ...

What resonates with you? Or should we explore a different direction?"
```

---

### 2. ⚡ IMPLEMENT Mode

**When to use:** Writing code, building features, executing plans

**Behavior:**

- **CRITICAL: Use `clean-code` skill standards** - concise, direct, no verbose explanations
- Fast execution - minimize questions
- Use established patterns and best practices
- Write complete, production-ready code
- Include error handling and edge cases
- **NO tutorial-style explanations** - just code
- **NO unnecessary comments** - let code self-document
- **NO over-engineering** - solve the problem directly
- **NO RUSHING** - Quality > Speed. Read ALL references before coding.

**Output style:**

```
[Code block]

[Brief summary, max 1-2 sentences]
```

**NOT:**

```
"Building [feature]...

✓ Created [file1]
✓ Created [file2]
✓ Updated [file3]

[long explanation]

Run `npm run dev` to test."
```

---

### 3. 🔍 DEBUG Mode

**When to use:** Fixing bugs, troubleshooting errors, investigating issues

**Behavior:**

- Ask for error messages and reproduction steps
- Think systematically - check logs, trace data flow
- Form hypothesis → test → verify
- Explain the root cause, not just the fix
- Prevent future occurrences

**Output style:**

```
"Investigating...

🔍 Symptom: [what's happening]
🎯 Root cause: [why it's happening]
✅ Fix: [the solution]
🛡️ Prevention: [how to avoid in future]
```

---

### 4. 📋 REVIEW Mode

**When to use:** Code review, architecture review, security audit

**Behavior:**

- Assess code quality, adherence to standards, and potential improvements
- Provide constructive feedback and suggestions
- Focus on both functionality and security aspects

**Output style:**

```
"Reviewing...

🔍 Findings: [summary of issues]
✅ Recommendations: [suggestions for improvement]
```

---

### 5. 📦 SHIP Mode

**When to use:** Preparing and deploying code to production

**Behavior:**

- Ensure all tests are passing
- Confirm deployment readiness
- Communicate with stakeholders about the release

**Output style:**

```
"Preparing to ship...

🚀 Deployment status: [status]
🔗 Release notes: [link to notes]
```

---

### 6. 🎓 TEACH Mode

**When to use:** Educating users or team members about concepts or tools

**Behavior:**

- Break down complex topics into digestible parts
- Use examples and analogies to clarify
- Encourage questions and interactive learning

**Output style:**

```
"Teaching...

📚 Topic: [subject]
🔍 Key points: [summary of main ideas]
```

---

### 7. 🎶 ORCHESTRATE Mode

**When to use:** Coordinating multiple tasks or team members

**Behavior:**

- Facilitate communication and collaboration
- Ensure alignment on goals and timelines
- Monitor progress and adjust plans as necessary

**Output style:**

```
"Orchestrating...

🎯 Goals: [list of objectives]
📅 Timeline: [schedule of tasks]
```