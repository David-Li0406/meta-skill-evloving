# Research Agent - Worked Example

This example demonstrates converting the research framework into a deployed Mastra agent.

## Framework Analysis

The research skill has:

### Diagnostic States (10)
| ID | Name | Key Symptom |
|----|------|-------------|
| R1 | No Analysis | Jumping to searching without topic analysis |
| R1.5 | No Vocabulary Map | Using outsider terminology |
| R2 | Single-Perspective Search | All queries support one viewpoint |
| R3 | Domain Blindness | Searching only in familiar field |
| R4 | Recency Bias | Only recent sources |
| R5 | Breadth Without Depth | Many tabs, no synthesis |
| R6 | Completion Uncertainty | Unsure when to stop |
| R7 | Research Complete | Can explain and act |
| R8 | No Persistence | Starting from scratch each session |
| R9 | Scope Mismatch | Over/under-researching relative to stakes |
| R10 | No Confidence Signaling | Hedging everywhere |

### Process Phases
1. **Phase 0**: Topic Analysis (concepts, stakeholders, temporal, domains, controversies)
2. **Phase 1.5**: Vocabulary Mapping (expert vs. outsider terms, cross-domain synonyms)
3. **Phase 2**: Query Construction (foundational, historical, current, competing, evidence)
4. **Synthesis**: Confidence-calibrated output

### Key Vocabulary
- Phase 0 Analysis
- Vocabulary Map
- Core Terms
- Depth Levels (introductory, working, expert)
- Diminishing Returns
- Single-Shot Research
- Scope Calibration
- Confidence Markers

## Agent Architecture

```
research-agent/
├── src/
│   ├── mastra/
│   │   ├── agents/
│   │   │   └── research-agent.ts       # Main agent with framework instructions
│   │   ├── tools/
│   │   │   ├── assess-state.ts         # Diagnose research state (R1-R10)
│   │   │   ├── run-phase0.ts           # Execute Phase 0 analysis
│   │   │   ├── build-vocabulary.ts     # Build vocabulary map
│   │   │   ├── expand-queries.ts       # Generate search queries
│   │   │   ├── retrieve-prior.ts       # Get prior research/vocabulary
│   │   │   └── synthesize.ts           # Create synthesis with confidence
│   │   ├── workflows/
│   │   │   ├── full-research.ts        # Complete research workflow
│   │   │   └── single-shot.ts          # Time-boxed research workflow
│   │   └── index.ts                    # Mastra instance
│   ├── schemas/
│   │   ├── vocabulary.ts
│   │   ├── analysis.ts
│   │   ├── synthesis.ts
│   │   └── states.ts
│   └── index.ts                        # Hono server
├── package.json
├── tsconfig.json
└── Dockerfile
```

## Tool Mapping

| Framework Element | Tool |
|-------------------|------|
| Diagnostic states R1-R10 | `assess-research-state` |
| Phase 0 Analysis | `run-phase0-analysis` |
| Vocabulary Mapping | `build-vocabulary-map` |
| Query Construction | `expand-queries` |
| Prior Research Check | `retrieve-prior-research` |
| Synthesis | `synthesize-research` |

## Workflow Design

### Full Research Workflow
```
Input: { topic, depth, decisionContext }
    ↓
[check-prior-research] → Has prior vocabulary?
    ↓                         ↓
    No                       Yes
    ↓                         ↓
[phase-0-analysis]    [load-vocabulary]
    ↓                         ↓
[vocabulary-mapping] ←────────┘
    ↓
[query-expansion]
    ↓
[synthesize-findings]
    ↓
Output: { synthesis, vocabularyMap, confidence, gaps }
```

### Single-Shot Workflow
```
Input: { topic, timeBox, stakes }
    ↓
[calibrate-scope]
    ↓
[quick-analysis] (compressed Phase 0)
    ↓
[targeted-search]
    ↓
[synthesize-with-confidence]
    ↓
Output: { synthesis, confidence, caveats }
```

## API Endpoints

```
POST /api/diagnose
  → Assess research state, recommend intervention

POST /api/intervene
  → Apply intervention for specific state

POST /api/process/start
  → Start full research workflow

GET /api/process/:runId/status
  → Check workflow progress

POST /api/chat
  → Conversational interaction with research agent

GET /api/vocabulary/:topic
  → Retrieve prior vocabulary maps
```

## Memory Configuration

```typescript
// Thread per research topic
const thread = `research-${userId}-${topic}`;

// Vocabulary maps in vector store
indexName: "vocabulary-maps"
filter: { userId, topic }

// Research findings in vector store
indexName: "research-findings"
filter: { userId }
```

## Deployment

```bash
# Build
npm run build

# Run locally
npm run dev

# Docker
docker build -t research-agent .
docker run -p 3000:3000 -e OPENAI_API_KEY=sk-... research-agent

# Deploy to Railway/Fly.io
fly deploy
```

## Usage Example

```bash
# Diagnose current research state
curl -X POST http://localhost:3000/api/diagnose \
  -H "Content-Type: application/json" \
  -d '{
    "situation": "I am researching the gentrification of workwear but keep finding surface-level fashion articles",
    "topic": "gentrification of workwear"
  }'

# Response:
{
  "state": "R1.5",
  "stateName": "No Vocabulary Map",
  "confidence": 0.85,
  "symptomsMatched": ["Using outsider terminology", "Finding only surface-level material"],
  "intervention": "Build vocabulary map. Hunt for expert terms in early sources.",
  "nextActions": [
    "Search for 'technically called' and 'also known as' in current sources",
    "Map terms by domain using vocabulary template"
  ]
}
```

## Files in This Example

- `analysis.json` - Framework analysis output
- `src/` - Full agent implementation (reference)

To generate your own research agent:
```bash
deno run --allow-read scripts/analyze-framework.ts skills/research/SKILL.md --output analysis.json
```
