# Framework Analysis

How to analyze an operating-frameworks skill for agent conversion.

## Overview

Before writing any code, systematically extract the framework's structure. This analysis becomes the blueprint for agent design.

## Analysis Template

### 1. Extract Diagnostic States

For each state in the framework's SKILL.md:

```json
{
  "states": [
    {
      "id": "R1",
      "name": "No Analysis",
      "symptoms": [
        "Jumping straight to searching without analyzing the topic"
      ],
      "test": "Can you articulate stakeholders, temporal scope, and domain mapping?",
      "intervention": "Run Phase 0 Analysis Template before generating queries",
      "precedingStates": [],
      "followingStates": ["R1.5", "R2"]
    }
  ]
}
```

**Key fields:**
- `id`: State identifier from framework (R1, D2, etc.)
- `name`: Human-readable state name
- `symptoms`: What user notices when in this state
- `test`: How to verify this state applies
- `intervention`: What framework recommends
- `precedingStates`: Which states typically lead here
- `followingStates`: Which states typically follow

### 2. Extract Vocabulary

Identify terms that need precise definitions:

```json
{
  "vocabulary": [
    {
      "term": "Phase 0 Analysis",
      "definition": "Structured analysis of topic before searching: concepts, stakeholders, temporal scope, domains, controversies",
      "domain": "research",
      "depth": "expert",
      "relatedTerms": ["Topic Analysis", "Pre-search Analysis"],
      "usedInStates": ["R1", "R1.5"]
    },
    {
      "term": "Vocabulary Map",
      "definition": "Primary research deliverable mapping expert vs. outsider terms, cross-domain synonyms, and depth indicators",
      "domain": "research",
      "depth": "expert",
      "relatedTerms": ["Term Map", "Terminology Mapping"],
      "usedInStates": ["R1.5", "R3"]
    }
  ]
}
```

**Depth levels:**
- `introductory`: Terms outsiders use
- `working`: Terms practitioners use
- `expert`: Technical/precise terminology

### 3. Extract Process Phases

Map the framework's workflow:

```json
{
  "processes": [
    {
      "phaseId": "0",
      "name": "Topic Analysis",
      "description": "Analyze topic through multiple lenses before searching",
      "inputs": ["topic", "decision_context"],
      "outputs": ["core_concepts", "stakeholders", "temporal_scope", "domains", "controversies"],
      "dependencies": [],
      "optional": false
    },
    {
      "phaseId": "1.5",
      "name": "Vocabulary Mapping",
      "description": "Build vocabulary map as primary deliverable",
      "inputs": ["core_concepts"],
      "outputs": ["vocabulary_map"],
      "dependencies": ["0"],
      "optional": false
    }
  ]
}
```

### 4. Extract Integration Points

Identify connections to other skills:

```json
{
  "integrations": [
    {
      "skill": "context-networks",
      "connectionType": "storage",
      "description": "Store vocabulary maps and research findings in context network",
      "states": ["R8"]
    },
    {
      "skill": "fact-check",
      "connectionType": "verification",
      "description": "Apply truth-check to research findings",
      "states": ["R10"]
    }
  ]
}
```

### 5. Extract Anti-Patterns

Document what to avoid:

```json
{
  "antiPatterns": [
    {
      "name": "Confirmation Trap",
      "symptom": "Searching for evidence that supports existing belief",
      "fix": "Explicitly search for strongest counterargument",
      "relatedStates": ["R2"]
    }
  ]
}
```

### 6. Extract Completion Criteria

Define when the process is done:

```json
{
  "completionCriteria": {
    "minimumViable": [
      "Can define core concepts in own words",
      "Know 2-3 major perspectives",
      "Found authoritative source per perspective"
    ],
    "workingKnowledge": [
      "Can explain historical context",
      "Understand stakeholder positions",
      "Encountered counterarguments"
    ],
    "deepExpertise": [
      "Traced claims to primary sources",
      "Can evaluate competing evidence"
    ]
  }
}
```

## Analysis Process

### Step 1: Read the Full Framework

Read the entire SKILL.md without extracting yet. Understand the overall purpose and flow.

### Step 2: Identify State Boundaries

Look for section headers like "Diagnostic States", "The States", or numbered/lettered items with symptoms/interventions.

### Step 3: Map Vocabulary

Highlight terms that:
- Have specific definitions in this framework
- Are used differently than common usage
- Connect to Zod schema needs

### Step 4: Trace Process Flow

Identify the ordered steps or phases. Note:
- What each phase produces
- What each phase requires
- Optional vs required phases

### Step 5: Find Integration Points

Look for:
- References to other skills
- "Integration with..." sections
- Cross-links or "see also" references

### Step 6: Validate Completeness

Check that you've captured:
- [ ] All diagnostic states
- [ ] Key vocabulary (10-20 terms minimum)
- [ ] Process phases with dependencies
- [ ] Integration points
- [ ] Anti-patterns
- [ ] Completion criteria

## Output Format

Save analysis as JSON:

```
analysis/
├── research-framework-analysis.json
├── story-sense-analysis.json
└── worldbuilding-analysis.json
```

## Example: Research Framework Analysis

See `examples/research-agent/analysis.json` for complete example.

Quick summary:
- **States**: 10 (R1-R10)
- **Vocabulary**: 15 key terms
- **Phases**: 4 (Phase 0, 1.5, 2, Synthesis)
- **Integrations**: 2 (context-networks, fact-check)
- **Anti-patterns**: 10 documented

## Using Analysis for Agent Design

Once analysis is complete:

1. **States → Tools**: Each state or state group becomes a diagnostic tool
2. **Vocabulary → Schemas**: Each term becomes a Zod type
3. **Phases → Workflow**: Process becomes workflow steps
4. **Integrations → Dependencies**: Connected skills inform tool design
5. **Anti-patterns → Validation**: Prevent known failure modes
