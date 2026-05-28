---
name: context-management
description: Use this skill for advanced context management, including saving and restoring project context across AI workflows.
---

# Context Management: Intelligent Context Capture and Restoration

## Role Statement

Expert Context Management Specialist focused on comprehensive, semantic-aware context preservation and intelligent retrieval across complex multi-agent AI workflows. This skill orchestrates advanced context capture, serialization, and rehydration strategies to maintain institutional knowledge and enable seamless multi-session collaboration.

## Context Overview

The Context Management tool is a sophisticated memory management system designed to:
- Capture and reconstruct project context across distributed AI workflows
- Enable seamless continuity in complex, long-running projects
- Provide intelligent, semantically-aware context retrieval and preservation
- Maintain historical knowledge integrity and decision traceability

## Core Requirements and Arguments

### Input Parameters
- `context_source`: Primary context storage location (vector database, file system)
- `project_identifier`: Unique project namespace
- `context_type`: Granularity of context capture (minimal, standard, comprehensive)
- `restoration_mode`:
  - `full`: Complete context restoration
  - `incremental`: Partial context update
  - `diff`: Compare and merge context versions
- `token_budget`: Maximum context tokens to restore (default: 8192)
- `relevance_threshold`: Semantic similarity cutoff for context components (default: 0.75)
- `$PROJECT_ROOT`: Absolute path to project root
- `$STORAGE_FORMAT`: Preferred storage format (json, markdown, vector)
- `$TAGS`: Optional semantic tags for context categorization

## Context Capture and Restoration Strategies

### 1. Semantic Information Identification
- Extract high-level architectural patterns and decision-making rationales
- Identify cross-cutting concerns and dependencies
- Map implicit knowledge structures

### 2. Context Serialization and Compression
- Use JSON Schema for structured representation and implement type-safe serialization
- Support advanced compression algorithms for efficient storage

### 3. Semantic Vector Search
- Utilize multi-dimensional embedding models for context retrieval
- Employ cosine similarity and vector clustering techniques

### 4. Relevance Filtering and Ranking
- Implement multi-stage relevance scoring considering temporal decay and historical impact

### 5. Context Rehydration Patterns
- Implement incremental context loading and support partial and full context reconstruction

### 6. Session State Reconstruction
- Reconstruct agent workflow state and preserve decision trails

### 7. Context Merging and Conflict Resolution
- Implement three-way merge strategies and detect semantic conflicts

### 8. Performance Optimization
- Implement efficient caching mechanisms and optimize vector search algorithms

## Reference Workflows

### Workflow 1: Project Onboarding Context Capture
1. Analyze project structure
2. Extract architectural decisions
3. Generate semantic embeddings
4. Store in vector database
5. Create markdown summary

### Workflow 2: Project Resumption
1. Retrieve most recent project context
2. Validate context against current codebase
3. Selectively restore relevant components
4. Generate resumption summary

### Workflow 3: Long-Running Session Context Management
1. Periodically capture context snapshots
2. Detect significant architectural changes
3. Version and archive context
4. Enable selective context restoration

## Usage Examples

```bash
# Full context restoration
context-restore project:ai-assistant --mode full

# Incremental context update
context-restore project:web-platform --mode incremental

# Context extraction
extract-context project_root:/path/to/project --context_type standard --storage_format json
```

## Advanced Integration Capabilities
- Real-time context synchronization
- Cross-platform context portability
- Compliance with enterprise knowledge management standards

## Future Roadmap
- Enhanced multi-modal embedding support
- Improved ML-driven context compression
- Real-time collaborative context editing
- Predictive context recommendation systems

## Limitations and Considerations
- Sensitive information must be explicitly excluded
- Context capture has computational overhead
- Requires careful configuration for optimal performance