# Subagent Prompts

## Model Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Initial analysis | `haiku` | Fast, cheap, good enough for categorization |
| Deep analysis (3 options) | `sonnet` | Smarter reasoning for nuanced interpretation |

## Analysis Prompt (Initial)

Use this prompt when spawning subagents for initial item analysis:

```
Task({
  subagent_type: "general-purpose",
  description: "Distill clipping: [title]",
  model: "haiku",
  prompt: `
    You are processing a single inbox item. Return a PROPOSAL, not a final note.

    ## Item
    File: 00 Inbox/[filename]
    Type: [clipping|transcription|attachment]

    ## Enriched Content
    [Full content from enrichment phase - transcript, article text, etc.]

    ## Your Task
    1. Read the note: para_read({ file: "...", response_format: "json" })
    2. Analyze the enriched content provided above
    3. Categorize and extract hints for organization
    4. Return a structured proposal (see format below)

    ## Proposal Format (JSON)
    {
      "file": "00 Inbox/[filename]",
      "type": "[clipping|transcription|attachment]",
      "proposed_title": "[meaningful title]",
      "proposed_template": "[resource|gift|booking|etc]",
      "summary": "[2-3 sentences]",
      "categorization_hints": ["...", "...", "..."],
      "suggested_areas": ["[[Area]]"],
      "suggested_projects": ["[[Project]]"],
      "resource_type": "[article|meeting|tutorial|etc]",
      "source_format": "[video|article|audio|etc]",
      "confidence": "[high|medium|low]",
      "notes": "[any special considerations]"
    }

    ## Available Areas
    [areas list]

    ## Available Projects
    [projects list]
  `
})
```

**CRITICAL**: Run 3 Task calls in a single message for parallel execution.

## Deep Analysis Prompt (3 Options)

When user chooses "3" (Deeper), spawn a subagent that returns **multiple options**:

```
Task({
  subagent_type: "general-purpose",
  description: "Deep analysis: [title]",
  model: "sonnet",
  prompt: `
    You are doing DEEP ANALYSIS of an inbox item.
    Return 3 DIFFERENT categorization options for the user to choose from.

    ## Item
    [Full content from original proposal]

    ## Your Task
    Analyze this content deeply and propose 3 DIFFERENT ways to categorize it:

    1. **Option A**: [Most likely interpretation]
    2. **Option B**: [Alternative framing]
    3. **Option C**: [Creative/unexpected angle]

    For voice memos especially, consider:
    - Is this a meeting? What type? (standup, 1:1, planning, retro)
    - Is this personal reflection? Journal entry?
    - Is this a brainstorm? Ideas to capture?
    - Is this task-related? Action items?

    ## Return Format (JSON)
    {
      "options": [
        {
          "label": "A",
          "interpretation": "[How you see this content]",
          "proposed_title": "...",
          "proposed_template": "...",
          "resource_type": "...",
          "summary": "...",
          "categorization_hints": [...],
          "suggested_areas": [...],
          "suggested_projects": [...],
          "rationale": "[Why this interpretation]"
        },
        { "label": "B", ... },
        { "label": "C", ... }
      ]
    }

    ## Available Areas
    [areas list]

    ## Available Projects
    [projects list]
  `
})
```

## Proposal JSON Schema

```typescript
interface Proposal {
  file: string;                    // Original inbox file path
  type: "clipping" | "transcription" | "attachment";
  proposed_title: string;          // Meaningful title for the note
  proposed_template: string;       // resource, gift, booking, etc.
  summary: string;                 // 2-3 sentence summary
  categorization_hints: string[];          // 3-5 bullet points
  suggested_areas: string[];       // Wikilinks like [[Area Name]]
  suggested_projects: string[];    // Wikilinks like [[Project Name]]
  resource_type: string;           // article, meeting, tutorial, etc.
  source_format: string;           // video, article, audio, etc.
  confidence: "high" | "medium" | "low";
  notes?: string;                  // Special considerations
}

interface DeepAnalysisOption extends Proposal {
  label: "A" | "B" | "C";
  interpretation: string;          // How this option interprets the content
  rationale: string;               // Why this interpretation makes sense
}

interface DeepAnalysisResponse {
  options: DeepAnalysisOption[];
}
```

## Best Practices

1. **Always include enriched content** - Don't make subagents fetch content again
2. **Provide vault context** - Areas and projects help with categorization
3. **Use haiku for speed** - Initial analysis doesn't need sonnet
4. **Use sonnet for depth** - Multiple interpretations benefit from reasoning
5. **Return JSON** - Structured output is easier to process
6. **Include confidence** - Helps user decide if deeper analysis is needed
