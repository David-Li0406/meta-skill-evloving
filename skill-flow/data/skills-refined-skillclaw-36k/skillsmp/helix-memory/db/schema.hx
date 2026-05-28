// Enhanced Schema for Claude Code Long-Term Memory
// Graph-based with reasoning chains and vector search
// Inspired by Helixir architecture

// ============================================================================
// NODES
// ============================================================================

// Memory node - core storage unit
N::Memory {
    content: String,         // The actual memory content
    category: String,        // preference, fact, context, decision, task, solution
    created_at: String,      // ISO timestamp for time-window searches
    importance: U32,         // 1-10 priority scale
    tags: String,            // Comma-separated tags
    source: String,          // session_id or "manual"
}

// Vector embedding for semantic search
V::MemoryEmbedding {
    content: String,         // Original text for context
    model: String,           // Which embedding model was used
}

// Context groups related memories (project, session, topic)
N::Context {
    name: String,
    description: String,
    context_type: String,    // project, session, topic
    created_at: Date,
}

// Concept for categorical grouping (like Helixir's Skills/Preferences/Goals)
N::Concept {
    name: String,            // e.g., "python", "testing", "wordpress"
    concept_type: String,    // skill, preference, goal, domain
    description: String,
}

// ============================================================================
// REASONING EDGES (Graph Power!)
// ============================================================================

// Memory implies another (logical consequence)
// "prefers Python" IMPLIES "avoid Node.js suggestions"
E::Implies {
    From: Memory,
    To: Memory,
    Properties: {
        confidence: U32,     // 1-10 how certain is this implication
        reason: String,      // Why this implication exists
    }
}

// Memory contradicts another (conflict detection)
// "always use tabs" CONTRADICTS "always use spaces"
E::Contradicts {
    From: Memory,
    To: Memory,
    Properties: {
        severity: U32,       // 1-10 how severe the contradiction
        resolution: String,  // How to resolve (newer_wins, ask_user, etc)
    }
}

// Memory exists because of another (causal chain)
// "migrated to FastAPI" BECAUSE "Flask too slow for async"
E::Because {
    From: Memory,
    To: Memory,
    Properties: {
        strength: U32,       // 1-10 causal strength
    }
}

// Memory supersedes another (version history)
// New preference replaces old one
E::Supersedes {
    From: Memory,
    To: Memory,
    Properties: {
        superseded_at: Date,
    }
}

// ============================================================================
// STRUCTURAL EDGES
// ============================================================================

// Memory has vector embedding
E::HasEmbedding {
    From: Memory,
    To: MemoryEmbedding,
    Properties: {}
}

// Memory belongs to context
E::BelongsTo {
    From: Memory,
    To: Context,
    Properties: {
        relevance: U32,
    }
}

// Memory relates to concept (categorical)
E::RelatedToConcept {
    From: Memory,
    To: Concept,
    Properties: {
        strength: U32,
    }
}

// General relationship (fallback for misc relations)
E::RelatesTo {
    From: Memory,
    To: Memory,
    Properties: {
        relationship: String,
        strength: U32,
    }
}

// Solution solves a problem (causal fix relationship)
// "Fixed datastar signal" SOLVES "Cart count not updating"
E::Solves {
    From: Memory,
    To: Memory,
    Properties: {
        strength: U32,       // 1-10 how directly it solves the problem
    }
}
