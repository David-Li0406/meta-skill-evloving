# Context Network to Memory Conversion

Mapping operating-frameworks context network patterns to Mastra agent memory and RAG.

## Core Mapping

| Context Network Element | Mastra Memory Pattern |
|-------------------------|----------------------|
| status.md (current state) | Conversation thread metadata |
| decisions.md | Thread messages with decision metadata |
| glossary.md | Vector store for term lookup |
| Research findings | RAG with topic indexing |
| Prior vocabulary maps | Vector store with user/topic filtering |
| Session continuity | Thread-based memory |

## Conversation Memory for Sessions

Context network tracks session continuity in status.md. In Mastra:

```typescript
// Create thread for research session
const createResearchThread = async (userId: string, topic: string) => {
  const threadId = `research-${userId}-${topic.toLowerCase().replace(/\s+/g, "-")}`;

  const thread = await mastra.storage?.createThread({
    resourceId: userId,
    metadata: {
      type: "research-session",
      topic,
      status: "active",
      createdAt: new Date().toISOString(),
      frameworkId: "research",
    },
  });

  return threadId;
};

// Use thread in agent calls
const response = await researchAgent.generate(message, {
  memory: {
    thread: threadId,
    resource: userId,
  },
});
```

## Vocabulary Maps as RAG

Context network stores vocabulary maps for reuse. In Mastra:

```typescript
import { embed } from "@ai-sdk/openai";

// Store vocabulary map in vector store
const storeVocabularyMap = async (
  userId: string,
  topic: string,
  vocabularyMap: VocabularyMap
) => {
  // Create embedding from core terms
  const termsText = vocabularyMap.coreTerms
    .map(t => `${t.term}: ${t.definition}`)
    .join("\n");

  const { embedding } = await embed({
    model: openai.embedding("text-embedding-3-small"),
    value: `${topic}\n${termsText}`,
  });

  await mastra.vectors?.default.upsert({
    indexName: "vocabulary-maps",
    vectors: [{
      id: `vocab-${userId}-${topic}`,
      vector: embedding,
      metadata: {
        userId,
        topic,
        coreTerms: vocabularyMap.coreTerms,
        synonyms: vocabularyMap.synonyms,
        depthIndicators: vocabularyMap.depthIndicators,
        lastUpdated: new Date().toISOString(),
      },
    }],
  });
};

// Retrieve prior vocabulary for topic
const retrievePriorVocabulary = async (userId: string, topic: string) => {
  const { embedding } = await embed({
    model: openai.embedding("text-embedding-3-small"),
    value: topic,
  });

  const results = await mastra.vectors?.default.query({
    indexName: "vocabulary-maps",
    queryVector: embedding,
    filter: { userId },
    topK: 3,
  });

  return results?.map(r => r.metadata) || [];
};
```

## Research Findings as RAG

Prior research stored for retrieval:

```typescript
// Store research findings
const storeResearchFindings = async (
  userId: string,
  topic: string,
  synthesis: ResearchSynthesis
) => {
  // Chunk key findings
  const chunks = synthesis.keyFindings.map((finding, i) => ({
    id: `finding-${userId}-${topic}-${i}`,
    content: `${finding.claim}\n${finding.sources.map(s => s.title).join(", ")}`,
    metadata: {
      userId,
      topic,
      type: "finding",
      confidence: finding.confidence,
      claimText: finding.claim,
      sources: finding.sources,
      researchedAt: synthesis.synthesizedAt,
    },
  }));

  const { embeddings } = await embedMany({
    model: openai.embedding("text-embedding-3-small"),
    values: chunks.map(c => c.content),
  });

  await mastra.vectors?.default.upsert({
    indexName: "research-findings",
    vectors: chunks.map((chunk, i) => ({
      id: chunk.id,
      vector: embeddings[i],
      metadata: chunk.metadata,
    })),
  });
};

// Retrieve prior findings
const retrievePriorFindings = async (
  userId: string,
  query: string,
  limit = 5
) => {
  const { embedding } = await embed({
    model: openai.embedding("text-embedding-3-small"),
    value: query,
  });

  const results = await mastra.vectors?.default.query({
    indexName: "research-findings",
    queryVector: embedding,
    filter: { userId },
    topK: limit,
  });

  return results?.map(r => ({
    claim: r.metadata.claimText,
    confidence: r.metadata.confidence,
    sources: r.metadata.sources,
    relevanceScore: r.score,
  })) || [];
};
```

## Decision Logging

Context network decisions.md tracks key decisions. In Mastra:

```typescript
// Log decision to thread
const logDecision = async (
  threadId: string,
  decision: {
    question: string;
    choice: string;
    rationale: string;
    alternatives: string[];
  }
) => {
  await mastra.storage?.addMessage({
    threadId,
    role: "system",
    content: JSON.stringify(decision),
    metadata: {
      type: "decision",
      question: decision.question,
      choice: decision.choice,
      decidedAt: new Date().toISOString(),
    },
  });
};

// Retrieve decisions from thread
const getDecisions = async (threadId: string) => {
  const messages = await mastra.storage?.getMessages({
    threadId,
    page: 1,
    perPage: 100,
  });

  return messages
    ?.filter(m => m.metadata?.type === "decision")
    .map(m => JSON.parse(m.content));
};
```

## Framework Knowledge Indexing

Index framework content for agent self-awareness:

```typescript
// Index framework SKILL.md sections
const indexFrameworkKnowledge = async (
  frameworkId: string,
  skillContent: string
) => {
  // Parse into sections
  const sections = parseSkillSections(skillContent);

  const { embeddings } = await embedMany({
    model: openai.embedding("text-embedding-3-small"),
    values: sections.map(s => s.content),
  });

  await mastra.vectors?.default.upsert({
    indexName: "framework-knowledge",
    vectors: sections.map((section, i) => ({
      id: `${frameworkId}-${section.id}`,
      vector: embeddings[i],
      metadata: {
        frameworkId,
        sectionType: section.type,  // "state", "anti-pattern", "process"
        sectionId: section.id,
        content: section.content,
      },
    })),
  });
};

// Agent can query its own framework knowledge
export const queryFrameworkKnowledge = createTool({
  id: "query-framework",
  description: "Search framework knowledge for patterns and guidance",
  inputSchema: z.object({
    query: z.string(),
    sectionType: z.enum(["state", "anti-pattern", "process", "any"]).optional(),
  }),
  execute: async (inputData, context) => {
    const { query, sectionType } = inputData;
    const { mastra } = context;

    const { embedding } = await embed({
      model: openai.embedding("text-embedding-3-small"),
      value: query,
    });

    const filter = sectionType && sectionType !== "any"
      ? { sectionType }
      : undefined;

    const results = await mastra?.vectors?.default.query({
      indexName: "framework-knowledge",
      queryVector: embedding,
      filter,
      topK: 3,
    });

    return {
      sections: results?.map(r => ({
        type: r.metadata.sectionType,
        content: r.metadata.content,
        relevance: r.score,
      })),
    };
  },
});
```

## Session State Management

Track research session state (like context network status.md):

```typescript
// Session state schema
const SessionStateSchema = z.object({
  currentPhase: z.string(),
  completedPhases: z.array(z.string()),
  diagnosticState: z.string().optional(),
  vocabularyMapComplete: z.boolean(),
  findingsCount: z.number(),
  gaps: z.array(z.string()),
  lastActivity: z.string().datetime(),
});

// Store session state
const updateSessionState = async (
  threadId: string,
  state: z.infer<typeof SessionStateSchema>
) => {
  await mastra.storage?.updateThread(threadId, {
    metadata: {
      sessionState: state,
      updatedAt: new Date().toISOString(),
    },
  });
};

// Retrieve session state
const getSessionState = async (threadId: string) => {
  const thread = await mastra.storage?.getThread(threadId);
  return thread?.metadata?.sessionState;
};
```

## Cross-Session Continuity

Tool for checking prior work before starting:

```typescript
export const checkPriorResearch = createTool({
  id: "check-prior-research",
  description: "Check for prior research on topic before starting. " +
    "Prevents starting from scratch when vocabulary maps or findings exist.",
  inputSchema: z.object({
    topic: z.string(),
    userId: z.string(),
  }),
  outputSchema: z.object({
    hasPriorWork: z.boolean(),
    vocabularyMaps: z.array(VocabularyMapSummarySchema),
    recentFindings: z.array(FindingSummarySchema),
    lastSessionDate: z.string().optional(),
    recommendation: z.string(),
  }),
  execute: async (inputData, context) => {
    const { topic, userId } = inputData;
    const { mastra } = context;

    // Check for vocabulary maps
    const vocabMaps = await retrievePriorVocabulary(userId, topic);

    // Check for findings
    const findings = await retrievePriorFindings(userId, topic, 3);

    // Check for recent threads
    const threads = await mastra?.storage?.listThreads({
      resourceId: userId,
      filter: { "metadata.topic": topic },
    });

    const lastSession = threads?.[0]?.metadata?.updatedAt;
    const hasPriorWork = vocabMaps.length > 0 || findings.length > 0;

    let recommendation: string;
    if (!hasPriorWork) {
      recommendation = "No prior research found. Start with Phase 0 analysis.";
    } else if (vocabMaps.length > 0) {
      recommendation = `Found vocabulary map from ${vocabMaps[0].lastUpdated}. ` +
        "Load vocabulary and continue from last state.";
    } else {
      recommendation = `Found ${findings.length} prior findings. ` +
        "Review findings before expanding research.";
    }

    return {
      hasPriorWork,
      vocabularyMaps: vocabMaps.map(v => ({
        topic: v.topic,
        termCount: v.coreTerms?.length || 0,
        lastUpdated: v.lastUpdated,
      })),
      recentFindings: findings.map(f => ({
        claim: f.claim,
        confidence: f.confidence,
      })),
      lastSessionDate: lastSession,
      recommendation,
    };
  },
});
```

## Memory Cleanup and Consolidation

Prevent unbounded memory growth:

```typescript
// Summarize old conversations
const consolidateThread = async (threadId: string) => {
  const messages = await mastra.storage?.getMessages({
    threadId,
    page: 1,
    perPage: 100,
  });

  if (!messages || messages.length < 50) return;

  // Summarize with agent
  const summarizer = mastra.getAgent("summarizer");
  const conversation = messages.map(m => `${m.role}: ${m.content}`).join("\n");

  const summary = await summarizer?.generate(
    `Summarize this research session, preserving key findings and decisions:\n\n${conversation}`
  );

  // Store summary, archive old messages
  await mastra.storage?.addMessage({
    threadId,
    role: "system",
    content: `[SESSION SUMMARY]\n${summary?.text}`,
    metadata: {
      type: "summary",
      originalMessageCount: messages.length,
      consolidatedAt: new Date().toISOString(),
    },
  });
};
```

## Best Practices

1. **Thread per Topic**: Create separate threads for each research topic
2. **Filter by User**: Always include userId in vector queries
3. **Check Before Starting**: Use checkPriorResearch tool before new research
4. **Store Vocabulary**: Persist vocabulary maps for future sessions
5. **Log Decisions**: Record key decisions with rationale
6. **Consolidate Old Threads**: Summarize long conversations
7. **Index Framework**: Make framework knowledge searchable by agent
