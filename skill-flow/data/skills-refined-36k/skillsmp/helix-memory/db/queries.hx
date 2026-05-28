// Enhanced Queries for Graph-based Memory System
// Time-windows, reasoning chains, hybrid search

// ============================================================================
// STORAGE QUERIES
// ============================================================================

// Store a new memory with full metadata including timestamp
QUERY StoreMemory(
    content: String,
    category: String,
    importance: U32,
    tags: String,
    source: String,
    created_at: String
) =>
    memory <- AddN<Memory>({
        content: content,
        category: category,
        importance: importance,
        tags: tags,
        source: source,
        created_at: created_at
    })
    RETURN memory

// Store embedding for a memory
QUERY StoreMemoryEmbedding(
    memory_id: ID,
    vector: [F64],
    content: String,
    model: String
) =>
    memory <- N<Memory>(memory_id)
    embedding_node <- AddV<MemoryEmbedding>(vector, {content: content, model: model})
    AddE<HasEmbedding>::From(memory)::To(embedding_node)
    RETURN embedding_node

// ============================================================================
// REASONING CHAIN QUERIES
// ============================================================================

// Create IMPLIES relationship
QUERY CreateImplication(
    from_id: ID,
    to_id: ID,
    confidence: U32,
    reason: String
) =>
    from_mem <- N<Memory>(from_id)
    to_mem <- N<Memory>(to_id)
    edge <- AddE<Implies>::From(from_mem)::To(to_mem)
    RETURN edge

// Create CONTRADICTS relationship
QUERY CreateContradiction(
    from_id: ID,
    to_id: ID,
    severity: U32,
    resolution: String
) =>
    from_mem <- N<Memory>(from_id)
    to_mem <- N<Memory>(to_id)
    edge <- AddE<Contradicts>::From(from_mem)::To(to_mem)
    RETURN edge

// Create BECAUSE relationship (causal chain)
QUERY CreateCausalLink(
    from_id: ID,
    to_id: ID,
    strength: U32
) =>
    from_mem <- N<Memory>(from_id)
    to_mem <- N<Memory>(to_id)
    edge <- AddE<Because>::From(from_mem)::To(to_mem)
    RETURN edge

// Create SUPERSEDES relationship (version history)
QUERY CreateSupersedes(
    new_id: ID,
    old_id: ID
) =>
    new_mem <- N<Memory>(new_id)
    old_mem <- N<Memory>(old_id)
    edge <- AddE<Supersedes>::From(new_mem)::To(old_mem)
    RETURN edge

// Get what a memory implies (forward reasoning)
QUERY GetImplications(memory_id: ID) =>
    implied <- N<Memory>(memory_id)::Out<Implies>
    RETURN implied

// Get why a memory exists (backward reasoning)
QUERY GetReasons(memory_id: ID) =>
    reasons <- N<Memory>(memory_id)::Out<Because>
    RETURN reasons

// Get contradictions for a memory
QUERY GetContradictions(memory_id: ID) =>
    conflicts <- N<Memory>(memory_id)::Out<Contradicts>
    RETURN conflicts

// Get superseded memories
QUERY GetSupersededBy(memory_id: ID) =>
    superseded <- N<Memory>(memory_id)::Out<Supersedes>
    RETURN superseded

// ============================================================================
// RETRIEVAL QUERIES
// ============================================================================

// Get all memories (filtering done in Python)
QUERY GetAllMemories() =>
    memories <- N<Memory>
    RETURN memories

// ============================================================================
// VECTOR SEARCH QUERIES
// ============================================================================

// Semantic search via embeddings
QUERY SearchBySimilarity(
    query_vector: [F64],
    k: I64
) =>
    embeddings <- SearchV<MemoryEmbedding>(query_vector, k)
    memories <- embeddings::In<HasEmbedding>
    RETURN memories

// ============================================================================
// TEXT SEARCH QUERIES
// ============================================================================

// Full-text search on content
QUERY SearchByText(query: String) =>
    memories <- N<Memory>::WHERE(_::{content}::CONTAINS(query))
    RETURN memories

// Search by tag
QUERY SearchByTag(tag: String) =>
    memories <- N<Memory>::WHERE(_::{tags}::CONTAINS(tag))
    RETURN memories

// ============================================================================
// CONCEPT QUERIES
// ============================================================================

// Create a concept
QUERY CreateConcept(
    name: String,
    concept_type: String,
    description: String
) =>
    concept <- AddN<Concept>({name: name, concept_type: concept_type, description: description})
    RETURN concept

// Link memory to concept
QUERY LinkToConcept(
    memory_id: ID,
    concept_id: ID,
    strength: U32
) =>
    memory <- N<Memory>(memory_id)
    concept <- N<Concept>(concept_id)
    edge <- AddE<RelatedToConcept>::From(memory)::To(concept)
    RETURN edge

// Get memories for a concept
QUERY GetMemoriesForConcept(concept_id: ID) =>
    memories <- N<Concept>(concept_id)::In<RelatedToConcept>
    RETURN memories

// Get all concepts
QUERY GetAllConcepts() =>
    concepts <- N<Concept>
    RETURN concepts

// ============================================================================
// CONTEXT QUERIES
// ============================================================================

// Create a context
QUERY CreateContext(
    name: String,
    description: String,
    context_type: String
) =>
    context <- AddN<Context>({name: name, description: description, context_type: context_type})
    RETURN context

// Link memory to context
QUERY LinkMemoryToContext(
    memory_id: ID,
    context_id: ID,
    relevance: U32
) =>
    memory <- N<Memory>(memory_id)
    context <- N<Context>(context_id)
    AddE<BelongsTo>::From(memory)::To(context)
    RETURN "success"

// Get memories in context
QUERY GetMemoriesInContext(context_id: ID) =>
    memories <- N<Context>(context_id)::In<BelongsTo>
    RETURN memories

// Get all contexts
QUERY GetAllContexts() =>
    contexts <- N<Context>
    RETURN contexts

// Delete context (for cleanup)
QUERY DeleteContext(context_id: ID) =>
    DROP N<Context>(context_id)
    RETURN "deleted"

// ============================================================================
// BASIC CRUD
// ============================================================================

// Get memory by ID
QUERY GetMemory(id: ID) =>
    memory <- N<Memory>(id)
    RETURN memory

// Delete memory (hard delete)
QUERY DeleteMemory(id: ID) =>
    DROP N<Memory>(id)
    RETURN "deleted"

// Link related memories (generic)
QUERY LinkRelatedMemories(
    from_id: ID,
    to_id: ID,
    relationship: String,
    strength: U32
) =>
    from_memory <- N<Memory>(from_id)
    to_memory <- N<Memory>(to_id)
    edge <- AddE<RelatesTo>::From(from_memory)::To(to_memory)
    RETURN edge

// Get related memories
QUERY GetRelatedMemories(memory_id: ID) =>
    related <- N<Memory>(memory_id)::Out<RelatesTo>
    RETURN related

// Get memory with embedding
QUERY GetMemoryEmbedding(memory_id: ID) =>
    embedding <- N<Memory>(memory_id)::Out<HasEmbedding>
    RETURN embedding

// ============================================================================
// PROBLEM-SOLUTION EDGES (Solves relationship)
// ============================================================================

// Create SOLVES relationship (solution -> problem)
QUERY CreateSolvesLink(
    solution_id: ID,
    problem_id: ID,
    strength: U32
) =>
    solution <- N<Memory>(solution_id)
    problem <- N<Memory>(problem_id)
    edge <- AddE<Solves>::From(solution)::To(problem)
    RETURN edge

// Get problems that a solution solves (outgoing Solves edges)
QUERY GetSolvedProblems(solution_id: ID) =>
    problems <- N<Memory>(solution_id)::Out<Solves>
    RETURN problems

// Get solutions that solve a problem (incoming Solves edges)
QUERY GetSolutionsFor(problem_id: ID) =>
    solutions <- N<Memory>(problem_id)::In<Solves>
    RETURN solutions
