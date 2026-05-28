---
name: explore-internal-codebase
description: Use this skill when you need to explore an internal codebase at varying depths, whether for a quick overview, a deep dive, or architectural mapping.
---

# Explore - Internal Codebase Exploration

Meta-skill for exploring an internal codebase at varying depths. This is a READ-ONLY workflow, meaning no code changes will be made.

## Usage

```
/explore <depth> [options]
```

## Question Flow (No Arguments)

If the user types just `/explore` with no or partial arguments, guide them through this question flow. Use AskUserQuestion for each phase.

### Phase 0: Workflow Selection

```yaml
question: "How would you like to explore?"
header: "Explore"
options:
  - label: "Help me choose (Recommended)"
    description: "I'll ask questions to pick the right exploration depth"
  - label: "Quick - fast overview"
    description: "Chain: tldr tree → tldr structure (~1 min)"
  - label: "Deep - comprehensive analysis"
    description: "Chain: onboard → tldr → research → document (~5 min)"
  - label: "Architecture - layers & dependencies"
    description: "Chain: tldr arch → call graph → layer mapping (~3 min)"
```

**Mapping:**
- "Help me choose" → Continue to Phase 1-4 questions
- "Quick" → Set depth=quick, skip to Phase 2 (scope)
- "Deep" → Set depth=deep, skip to Phase 2 (scope)
- "Architecture" → Set depth=architecture, skip to Phase 2 (scope)

**If Answer is Unclear (via "Other"):**
```yaml
question: "I want to understand how deep you want to explore. Did you mean..."
header: "Clarify"
options:
  - label: "Help me choose"
    description: "Not sure - guide me through questions"
  - label: "Quick - fast overview"
    description: "Just want to see what's here"
  - label: "Deep - comprehensive analysis"
    description: "Need thorough understanding"
  - label: "Neither - let me explain differently"
    description: "I'll describe what I need"
```

### Phase 1: Exploration Goal

```yaml
question: "What are you trying to understand?"
header: "Goal"
options:
  - label: "Get oriented in the codebase"
    description: "Quick overview of structure"
  - label: "Understand how something works"
    description: "Deep dive into specific area"
  - label: "Map the architecture"
    description: "Layers, dependencies, patterns"
  - label: "Find where something is"
    description: "Locate specific code/functionality"
```

**Mapping:**
- "Get oriented" → quick depth
- "Understand how" → deep