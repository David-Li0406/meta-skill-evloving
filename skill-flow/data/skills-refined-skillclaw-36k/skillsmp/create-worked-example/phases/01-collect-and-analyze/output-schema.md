# Output Schema for Problem Analysis

**This file defines the JSON structure that must be returned by the analyze-problem phase.**

## Required Output Format

Return ONLY valid JSON matching this exact structure (no markdown, no explanation):

```json
{
  "problemAnalysis": {
    "problemTranscription": "EXACT verbatim transcription of everything in the image - all text, numbers, diagrams described, tables, etc. Be thorough and precise.",
    "problemType": "specific type (e.g., 'solving two-step equations with variables on both sides')",
    "mathematicalStructure": "description of relationships",
    "solution": [
      { "step": 1, "description": "what you do", "reasoning": "why you do it" }
    ],
    "answer": "final answer",
    "keyChallenge": "what makes this hard for students",
    "commonMistakes": ["mistake 1", "mistake 2"],
    "requiredPriorKnowledge": ["prereq 1", "prereq 2"],
    "answerFormat": "how answer should be presented",
    "visualType": "text-only | html-table | svg-visual",
    "svgSubtype": "coordinate-graph | diagram | shape | number-line | other",
    "diagramEvolution": {
      "initialState": "ASCII showing the initial diagram state (Problem Setup slide)",
      "keyElements": [
        { "element": "element name", "represents": "what it represents mathematically" }
      ],
      "steps": [
        {
          "header": "STEP 1: VERB",
          "ascii": "ASCII showing diagram after step 1 (builds on initial state)",
          "changes": ["What was added or modified in this step"]
        },
        {
          "header": "STEP 2: VERB",
          "ascii": "ASCII showing diagram after step 2 (builds on step 1)",
          "changes": ["What was added or modified in this step"]
        },
        {
          "header": "STEP 3: VERB",
          "ascii": "ASCII showing final diagram state with solution",
          "changes": ["What was added or modified in this step"]
        }
      ]
    },
    "graphPlan": {
      "equations": [
        {
          "label": "Line 1",
          "equation": "y = mx + b",
          "slope": 5,
          "yIntercept": 0,
          "color": "#60a5fa",
          "startPoint": { "x": 0, "y": 0 },
          "endPoint": { "x": 8, "y": 40 }
        }
      ],
      "scale": {
        "xMax": 8,
        "yMax": 50,
        "xAxisLabels": [0, 2, 4, 6, 8],
        "yAxisLabels": [0, 10, 20, 30, 40, 50]
      },
      "keyPoints": [
        { "label": "y-intercept Line 1", "x": 0, "y": 0, "dataX": 0, "dataY": 0 }
      ],
      "annotations": [
        { "type": "y-intercept-shift | parallel-label | slope-comparison | intersection-point | slope-triangle | point-label", "from": 0, "to": 20, "label": "+20" }
      ]
    }
  },
  "strategyDefinition": {
    "name": "Clear Strategy Name (e.g., 'Balance and Isolate')",
    "oneSentenceSummary": "To solve this, we [VERB] the [OBJECT] to find [GOAL]",
    "bigIdea": "The core mathematical concept in one sentence",
    "moves": [
      { "verb": "VERB1", "description": "what this step does", "result": "what it accomplishes" }
    ],
    "slideHeaders": ["STEP 1: VERB1", "STEP 2: VERB2"],
    "cfuQuestionTemplates": ["Why did I [VERB] first?", "How does [VERB]ing help?"]
  },
  "scenarios": [
    {
      "name": "Scenario name (different context from mastery check)",
      "context": "Real-world context description",
      "themeIcon": "🎮",
      "numbers": "specific numbers used",
      "description": "Full problem statement",
      "problemReminder": "≤15 word summary for slides",
      "visualPlan": { "type": "appropriate-visual-type", "...": "..." },
      "graphPlan": { "...": "only if coordinate-graph" },
      "diagramEvolution": {
        "initialState": "ASCII showing Problem Setup for THIS scenario's numbers",
        "keyElements": [{ "element": "...", "represents": "..." }],
        "steps": [
          {
            "header": "STEP 1: VERB",
            "ascii": "ASCII showing this scenario's values after step 1",
            "changes": ["What changed using this scenario's numbers"]
          }
        ]
      }
    }
  ]
}
```

## Field Requirements

### ⚠️ ALWAYS REQUIRED (no exceptions):

| Field | Description |
|-------|-------------|
| `strategyDefinition.moves` | 2-3 moves with verb, description, result |
| `scenarios` | Exactly 3 scenarios with different contexts |
| `scenarios[0].diagramEvolution` | Scenario 1 (worked example) needs its own diagramEvolution with its specific numbers in the ASCII art |

### Conditional Fields:

| Field | When Required |
|-------|---------------|
| `problemAnalysis.svgSubtype` | When `visualType` is `"svg-visual"` |
| `problemAnalysis.graphPlan` | When `svgSubtype` is `"coordinate-graph"` |
| `scenario[].graphPlan` | When `svgSubtype` is `"coordinate-graph"` |
| `scenario[].visualPlan` | When `svgSubtype` is NOT `"coordinate-graph"` |

## diagramEvolution Structure

The `diagramEvolution` field is **CRITICAL** for teacher preview. It shows exactly how the diagram will evolve across slides.

**Rules:**
- `initialState`: Shows Problem Setup slide (empty axes, blank diagram, etc.)
- `steps.length` MUST equal `strategyDefinition.moves.length`
- Each step builds cumulatively on the previous
- `header` must match the slide header ("STEP N: VERB")
- `changes` lists what was added/modified in that step

**Example for tape diagram:**
```json
"diagramEvolution": {
  "initialState": "┌────────────────────┐\n│        24          │\n└────────────────────┘\nTotal: 24, Groups: 4, Find: ?",
  "steps": [
    {
      "header": "STEP 1: PARTITION",
      "ascii": "┌─────┬─────┬─────┬─────┐\n│  ?  │  ?  │  ?  │  ?  │ = 24\n└─────┴─────┴─────┴─────┘",
      "changes": ["Divide into 4 equal parts", "Mark each with ?"]
    },
    {
      "header": "STEP 2: CALCULATE",
      "ascii": "┌─────┬─────┬─────┬─────┐\n│  6  │  6  │  6  │  6  │ = 24 ✓\n└─────┴─────┴─────┴─────┘",
      "changes": ["Calculate: 24 ÷ 4 = 6", "Fill in values"]
    }
  ]
}
```
