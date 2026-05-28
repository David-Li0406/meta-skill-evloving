---
name: work-type-classifier
description: >
  This skill should be used when the user initiates autonomous development
  with /auto, /auto-lite, or similar commands to classify the type of work.
  Semantic work type classification with multi-layer detection.
  Analyzes user request using keywords, intent, output type, and confidence scoring.
  Automatically triggers ASK_USER if confidence is below threshold.
  Outputs skill activation plan to .claude/auto-context.yaml.
---

# Work Type Classifier v3.0

Multi-layer semantic classification for autonomous development requests.

## Classification Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  SEMANTIC CLASSIFIER v3.0                                       │
├─────────────────────────────────────────────────────────────────┤
│  Layer 1: Keyword Detection (base score)                        │
│  Layer 2: Intent Analysis (modifier)                            │
│  Layer 3: Output Type Detection (modifier)                      │
│  Layer 4: Confidence Calculation + User Fallback                │
└─────────────────────────────────────────────────────────────────┘
```

## Layer 1: Keyword Detection

Scan for explicit work type indicators:

### FRONTEND Keywords (score: +1 each)
```
English: "UI", "component", "page", "design", "frontend", "React", "Vue",
         "CSS", "Tailwind", "button", "form", "modal", "layout", "style",
         "responsive", "mobile", "animation", "theme", "dark mode", "UX"

Croatian: "dizajn", "komponenta", "stranica", "sučelje", "gumb", "obrazac",
          "izgled", "tema", "animacija", "responzivan"

Frameworks: "Next.js", "Nuxt", "Svelte", "Astro", "Remix", "Vite"
```

### BACKEND Keywords (score: +1 each)
```
English: "API", "endpoint", "backend", "database", "server", "REST",
         "GraphQL", "authentication", "middleware", "microservice",
         "queue", "worker", "cron", "webhook", "migration"

Croatian: "baza podataka", "autentikacija", "server", "pozadina"

Frameworks: "Express", "FastAPI", "Django", "Rails", "Nest.js"
```

### RESEARCH Keywords (score: +1 each)
```
English: "audit", "analyze", "review", "explore", "investigate", "check",
         "find", "search", "assess", "evaluate", "security", "performance",
         "vulnerability", "bottleneck", "report"

Croatian: "provjeri", "analiziraj", "istraži", "pregledaj", "sigurnost",
          "audit", "ranjivost", "procijeni"
```

### DOCUMENTATION Keywords (score: +1 each)
```
English: "docs", "documentation", "README", "spec", "proposal", "guide"
Croatian: "dokumentacija", "upute", "specifikacija"
```

### CREATIVE Keywords (score: +1 each)
```
English: "art", "visual", "poster", "GIF", "animation", "graphic", "logo"
Croatian: "umjetnost", "vizualno", "plakat", "grafika"
```

## Layer 2: Intent Analysis

Detect user's underlying intent beyond explicit keywords:

### DESIGN_QUALITY Intent
```
Triggers: "beautiful", "stunning", "impressive", "wow", "amazing",
          "perfect", "professional", "polished", "elegant"
Croatian:  "lijep", "impresivan", "savršen", "profesionalan", "ocarati",
           "oduševiti", "elegantan", "moderan"

Effect: If FRONTEND detected, adds DESIGN_QUALITY focus
        → Forces frontend-design skill invocation
```

### SECURITY Intent
```
Triggers: "secure", "safe", "vulnerability", "attack", "hack", "protect",
          "OWASP", "injection", "XSS", "CSRF"
Croatian:  "siguran", "zaštita", "napad", "ranjivost"

Effect: Adds SECURITY focus to any work type
        → Forces security-focused code review
```

### PERFORMANCE Intent
```
Triggers: "fast", "quick", "optimize", "speed", "slow", "performance",
          "efficient", "bottleneck", "scale"
Croatian:  "brzo", "optimiziraj", "sporo", "performanse", "efikasno"

Effect: Adds PERFORMANCE focus
        → Forces performance analysis patterns
```

### MULTIPLE_OUTPUTS Intent
```
Triggers: Numbers + nouns: "5 pages", "3 components", "several", "multiple"
Croatian:  "5 stranica", "3 komponente", "nekoliko", "više"

Effect: Indicates multiple deliverables expected
        → Adjusts planning for parallel work
```

## Layer 3: Output Type Detection

Determine what the user expects as output:

### IMPLEMENTATION Output
```
Triggers: "build", "create", "implement", "add", "make", "develop", "code"
Croatian:  "napravi", "izradi", "implementiraj", "dodaj", "razvij"

Result: Standard implementation workflow (7 phases)
```

### RESEARCH Output
```
Triggers: "audit", "analyze", "review", "report", "findings", "assess"
Croatian:  "auditiraj", "analiziraj", "pregled", "izvještaj", "procjena"

Result: Research workflow (R1-R4)
        → Switches to /auto-audit flow
```

### DOCUMENTATION Output
```
Triggers: "document", "write docs", "explain", "describe"
Croatian:  "dokumentiraj", "objasni", "opiši"

Result: Documentation workflow
```

## Layer 4: Confidence Calculation

### Scoring Formula
```
base_score = sum(keyword_matches) * keyword_weight
intent_modifier = sum(intent_matches) * intent_weight
output_modifier = output_type_match * output_weight

total_score = base_score + intent_modifier + output_modifier

confidence = total_score / max_possible_score
```

### Weights
```yaml
keyword_weight: 1.0
intent_weight: 0.5
output_weight: 0.3
```

### Thresholds
```yaml
confident: >= 0.70      # Proceed without asking
uncertain: 0.40 - 0.69  # ASK USER to confirm
ambiguous: < 0.40       # ASK USER to specify
```

### Tie-Breaking Rules
When multiple work types score equally:
1. If RESEARCH keywords present → RESEARCH wins
2. If FRONTEND + BACKEND equal → FULLSTACK
3. If still tied → ASK USER

## Classification Process

### Step 1: Run All Layers
```python
# Pseudocode
keywords = detect_keywords(request)
intents = analyze_intent(request)
output_type = detect_output_type(request)

scores = calculate_scores(keywords, intents, output_type)
work_type = get_highest_score(scores)
confidence = calculate_confidence(scores)
```

### Step 2: Check Confidence
```python
if confidence >= 0.70:
    proceed_with_classification(work_type)
elif confidence >= 0.40:
    ask_user_to_confirm(work_type, confidence)
else:
    ask_user_to_specify()
```

### Step 3: User Confirmation (if needed)

When confidence < 0.70, use AskUserQuestion:
```
Detektiram [WORK_TYPE] task s [FOCUS] fokusom (confidence: [X]%).

Jesi li to točno?
- Da, nastavi
- Ne, ovo je [alternativa]
- Promijeni na: [custom]
```

### Step 4: Output Classification

Create `.claude/auto-context.yaml`:
```yaml
# Auto-generated by work-type-classifier v3.0
# Generated: <timestamp>

classification:
  work_type: FRONTEND | BACKEND | FULLSTACK | RESEARCH | DOCUMENTATION | CREATIVE
  confidence: 0.85
  user_confirmed: false | true

  # Layer 1 results
  detected_keywords:
    - "dizajn"
    - "prototip"
    - "UI"

  # Layer 2 results
  detected_intents:
    - DESIGN_QUALITY

  # Layer 3 results
  output_type: IMPLEMENTATION | RESEARCH | DOCUMENTATION

focus:
  - DESIGN_QUALITY   # If detected
  - SECURITY         # If detected
  - PERFORMANCE      # If detected
  - MULTIPLE_OUTPUTS # If detected

# Skill activation based on classification
skills_to_invoke:
  # Always invoked
  discipline:
    - superpowers:brainstorming
    - superpowers:writing-plans
    - superpowers:test-driven-development
    - superpowers:verification-before-completion
    - superpowers:requesting-code-review

  # Based on work_type
  domain_specific:
    - <skill-1>
    - <skill-2>

  # If focus detected
  focus_skills:
    - <focus-skill-1>

# Phase-specific instructions
phase_instructions:
  phase_2:
    - "MANDATORY: Invoke skills from domain_specific list"
  phase_4:
    - "MANDATORY: Apply TDD"
    - "MANDATORY: Apply domain_specific skills during implementation"
  phase_6:
    - "MANDATORY: Run fresh verification"
```

## Skill Mapping by Work Type

### FRONTEND
```yaml
domain_specific:
  - frontend-design      # ALWAYS for FRONTEND
  - webapp-testing       # E2E testing
focus_skills:
  DESIGN_QUALITY:
    - frontend-design    # Double emphasis
```

### BACKEND
```yaml
domain_specific:
  - architecture-patterns
  - api-design-principles
focus_skills:
  SECURITY:
    - code-reviewer (security mode)
```

### FULLSTACK
```yaml
domain_specific:
  - frontend-design
  - architecture-patterns
```

### RESEARCH
```yaml
domain_specific: []      # No implementation skills
workflow: "research"     # Use R1-R4 workflow
output: "docs/audits/"
```

### DOCUMENTATION
```yaml
domain_specific:
  - doc-coauthoring
```

### CREATIVE
```yaml
domain_specific:
  - canvas-design
  - algorithmic-art
```

## Integration with State Machine

After classification, update state machine:
```bash
# scripts/state-transition.sh
state-transition.sh work-type "$WORK_TYPE" "$FOCUS" "$CONFIDENCE"
```

This ensures mandatory skills are enforced by the pre-phase hook.

## Examples

### Example 1: Croatian Frontend Request
```
Input: "ajde napravi 5 savršenih prototipova dizajna koji ce ocarati usere"

Layer 1 (Keywords):
  - "dizajna" → FRONTEND (+1)
  - "prototipova" → FRONTEND (+1)

Layer 2 (Intent):
  - "savršenih" → DESIGN_QUALITY
  - "ocarati" → DESIGN_QUALITY

Layer 3 (Output):
  - "napravi" → IMPLEMENTATION
  - "5" → MULTIPLE_OUTPUTS

Result:
  work_type: FRONTEND
  confidence: 0.85
  focus: [DESIGN_QUALITY, MULTIPLE_OUTPUTS]
  mandatory_skills: [frontend-design, webapp-testing]
```

### Example 2: Security Audit Request
```
Input: "audit auth feature and tell me if everything is secure"

Layer 1 (Keywords):
  - "audit" → RESEARCH (+1)
  - "auth" → BACKEND (+1)

Layer 2 (Intent):
  - "secure" → SECURITY

Layer 3 (Output):
  - "audit" → RESEARCH output
  - "tell me" → REPORT expected

Result:
  work_type: RESEARCH
  confidence: 0.90
  focus: [SECURITY]
  workflow: research (R1-R4)
  output: docs/audits/
```

### Example 3: Ambiguous Request
```
Input: "make the app better"

Layer 1 (Keywords):
  - "app" → FULLSTACK (+0.5)

Layer 2 (Intent):
  - "better" → (ambiguous)

Layer 3 (Output):
  - "make" → IMPLEMENTATION

Result:
  work_type: FULLSTACK
  confidence: 0.35
  ACTION: ASK_USER

Question: "Što točno želiš poboljšati?
- Frontend/UI dizajn
- Backend/API performanse
- Oboje
- Nešto drugo"
```

## Quality Standards

1. **ALWAYS** create `.claude/auto-context.yaml` before Phase 2
2. **NEVER** proceed with confidence < 0.40 without user input
3. **ALWAYS** include detected keywords and intents for transparency
4. **ALWAYS** update state machine with work_type and confidence
5. **PRIORITIZE** RESEARCH detection - audits should not run implementation workflow

## When NOT to Use This Skill

Do NOT use this skill when:

1. **User explicitly specifies work type** - Trust user's classification
2. **Resuming from checkpoint** - Use saved classification
3. **Sequential simple commands** - Direct requests like "run tests"
4. **Non-development tasks** - Questions, explanations, general queries
5. **Already classified** - Check `.claude/auto-context.yaml` first
