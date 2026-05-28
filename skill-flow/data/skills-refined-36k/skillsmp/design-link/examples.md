# Cross-Reference Graph Examples

Complete usage examples for design-link skill in different scenarios.

## Example 1: Full Graph for All Modules

**User request:**

> Show me the design doc relationships across all modules

**Execution:**

1. Load all modules from config
2. Find all design docs (12 found)
3. Parse frontmatter and content links
4. Build graph (12 nodes, 28 edges)
5. Analyze (2 orphans, 1 circular dependency)
6. Generate Mermaid diagram

**Output:**

```markdown
# Design Documentation Cross-Reference Graph

**Generated:** 2026-01-17
**Modules:** 3 (effect-type-registry, rspress-plugin-api-extractor,
design-doc-system)
**Documents:** 12
**References:** 28

## Graph Visualization

```mermaid
graph LR
  subgraph effect-type-registry
    ETR_obs[observability<br/>current]
    ETR_arch[architecture<br/>current]
    ETR_cache[cache-optimization<br/>draft]
    ETR_type[type-system<br/>stub]
  end

  subgraph rspress-plugin
    RP_type[type-loading-vfs<br/>current]
    RP_snap[snapshot-tracking<br/>current]
    RP_perf[performance-obs<br/>current]
  end

  ETR_obs -.-> ETR_arch
  ETR_obs --> ETR_cache
  RP_type --> RP_snap
  RP_perf -.-> ETR_obs

  classDef current fill:#90EE90
  classDef draft fill:#FFD700
  classDef stub fill:#D3D3D3
  classDef orphan stroke:#FF0000,stroke-width:3px

  class ETR_obs,ETR_arch,RP_type,RP_snap,RP_perf current
  class ETR_cache draft
  class ETR_type stub,orphan

**Legend:**

- Solid line (→): Dependency
- Dashed line (-.->): Related
- Dotted line (...>): Content link
- Green: Current status
- Yellow: Draft status
- Gray: Stub status
- Red border: Orphaned document

## Analysis Summary

### Strengths

- 5 bidirectional relationships (good cross-referencing)
- No isolated clusters (all docs connected)
- Most docs have multiple relationships

### Issues

- 2 orphaned documents need cross-references
- 1 circular dependency needs resolution
- 8 one-way references could be bidirectional

### Orphaned Documents

1. **effect-type-registry/type-system.md** (stub, 0 refs)
   - Recommendation: Add to architecture.md related docs
   - Or: Complete implementation and add references

2. **rspress-plugin-api-extractor/legacy-api.md** (archived, 0 refs)
   - Recommendation: Already archived, status is correct

### Circular Dependencies

1. **cache-optimization → observability → cache-optimization**
   - Issue: Both docs depend on each other
   - Fix: Change one relationship from dependency to related
   - Suggested: observability depends on cache-optimization, but
     cache-optimization only relates to observability

### Recommendations

1. Add type-system.md to architecture.md related docs
2. Resolve cache-optimization ↔ observability circular dependency
3. Review 8 one-way references for potential bidirectional upgrades
4. Verify legacy-api.md archival is complete


## Example 2: Orphaned Docs Only

**User request:**

> Find orphaned design docs

**Execution:**

1. Load all modules
2. Find all design docs
3. Build graph
4. Filter for orphans (nodes with degree 0)
5. Report findings

**Output:**

```markdown
# Orphaned Design Documents

**Total orphaned:** 2 of 12 documents (17%)

## Orphaned Documents

### effect-type-registry/type-system.md

**Status:** stub
**Category:** architecture
**Created:** 2026-01-10
**Completeness:** 5%

**Why orphaned:**

- No outgoing references (related, dependencies, content links)
- No incoming references from other docs
- Not linked from CLAUDE.md

**Recommendations:**

1. Add to related docs in:
   - architecture.md (same category)
   - observability.md (may use type system)

2. Or: Delete if this was experimental/abandoned

3. Or: Complete implementation and add proper cross-references

### rspress-plugin-api-extractor/legacy-api.md

**Status:** archived
**Category:** architecture
**Created:** 2025-11-20
**Archived:** 2026-01-05

**Why orphaned:**

- Archived document
- Superseded by current-api.md
- References were removed during archival

**Recommendations:**

- No action needed (archived status is appropriate)
- Verify current-api.md covers all legacy-api topics

## Summary

**Action required:** 1 document
**No action needed:** 1 document (archived)

**Next steps:**

1. Review effect-type-registry/type-system.md
2. Decide: complete, cross-reference, or delete
3. Update frontmatter if keeping

## Example 3: Dependency Graph Only

**User request:**

> Show only dependency relationships in JSON

**Execution:**

1. Load all modules
2. Find all design docs
3. Extract only 'dependencies' from frontmatter
4. Build dependency-only graph
5. Output as JSON

**Output:**

```json
{
  "metadata": {
    "generated": "2026-01-17T10:45:00Z",
    "filter": "dependencies",
    "modules": 3,
    "documents": 12,
    "dependency_edges": 8
  },
  "nodes": [
    {
      "id": "effect-type-registry/observability",
      "path": ".claude/design/effect-type-registry/observability.md",
      "module": "effect-type-registry",
      "status": "current",
      "dependencies_out": 1,
      "dependencies_in": 2
    },
    {
      "id": "effect-type-registry/cache-optimization",
      "path": ".claude/design/effect-type-registry/cache-optimization.md",
      "module": "effect-type-registry",
      "status": "draft",
      "dependencies_out": 1,
      "dependencies_in": 0
    }
  ],
  "edges": [
    {
      "from": "effect-type-registry/cache-optimization",
      "to": "effect-type-registry/observability",
      "type": "dependency"
    },
    {
      "from": "effect-type-registry/observability",
      "to": "effect-type-registry/cache-optimization",
      "type": "dependency"
    }
  ],
  "analysis": {
    "circular_dependencies": [
      [
        "effect-type-registry/cache-optimization",
        "effect-type-registry/observability",
        "effect-type-registry/cache-optimization"
      ]
    ],
    "dependency_depth": {
      "max": 2,
      "average": 1.2
    }
  }
}

## Example 4: Module-Specific Graph

**User request:**

> Show cross-reference graph for effect-type-registry only

**Execution:**

1. Filter to effect-type-registry module
2. Find design docs (4 found)
3. Build graph
4. Generate Mermaid

**Output:**

```markdown
# Design Documentation Cross-Reference Graph

**Module:** effect-type-registry
**Documents:** 4
**References:** 7

```mermaid
graph LR
  obs[observability<br/>current]
  arch[architecture<br/>current]
  cache(cache-optimization<br/>draft)
  type([type-system<br/>stub])

  obs -.-> arch
  obs --> cache
  arch -.-> cache

  classDef current fill:#90EE90
  classDef draft fill:#FFD700
  classDef stub fill:#D3D3D3
  classDef orphan stroke:#FF0000,stroke-width:3px

  class obs,arch current
  class cache draft
  class type stub,orphan

## Analysis

**Strengths:**

- Well-connected core docs (obs, arch, cache)
- 2 bidirectional relationships

**Issues:**

- 1 orphaned stub (type-system)
- 1 circular dependency (obs ↔ cache)

**Recommendations:**

1. Connect type-system to architecture
2. Resolve circular dependency between observability and cache-optimization


## Example 5: Cross-Module References

**User request:**

> Show relationships that cross module boundaries

**Execution:**

1. Load all modules
2. Find all design docs
3. Build full graph
4. Filter for cross-module edges
5. Report

**Output:**

```markdown
# Cross-Module Design Documentation References

**Total cross-module references:** 3

## Cross-Module Relationships

### rspress-plugin-api-extractor → effect-type-registry

**1. performance-observability → observability**

- **Type:** content-link
- **Context:** Performance metrics refer to registry observability events
- **Reason:** Plugin uses registry's event system
- **Status:** Documented integration pattern

**2. type-loading-vfs → architecture**

- **Type:** dependency
- **Context:** VFS implementation depends on registry architecture
- **Reason:** Deep integration with registry internals
- **Status:** Critical dependency

### effect-type-registry → design-doc-system

**3. observability → event-patterns**

- **Type:** related
- **Context:** Registry observability follows standard event patterns
- **Reason:** Reuses design decisions
- **Status:** Shared pattern

## Analysis

**Integration Points:** 2 modules tightly coupled
(rspress-plugin + registry)

**Shared Patterns:** 1 reference to design-doc-system patterns

**Recommendations:**

1. Document rspress-plugin → registry integration in both modules
2. Add bidirectional reference for performance-observability ↔ observability
3. Consider creating integration-patterns doc

## Example 6: Bidirectional vs One-Way

**User request:**

> Show me which references are bidirectional and which are one-way

**Execution:**

1. Build graph
2. Classify each edge as bidirectional or one-way
3. Report both categories

**Output:**

```markdown
# Reference Direction Analysis

## Bidirectional Relationships (5)

Healthy cross-referencing where both docs reference each other:

1. **effect-type-registry/observability ↔ architecture**
   - Type: related
   - Status: Good - improves discoverability

2. **rspress-plugin-api-extractor/type-loading-vfs ↔ snapshot-tracking**
   - Type: related
   - Status: Good - documents integration

3. **effect-type-registry/cache-optimization ↔ observability**
   - Type: dependency
   - Status: ⚠️ Circular dependency - needs fixing

4. **rspress-plugin-api-extractor/build-architecture ↔ type-loading-vfs**
   - Type: content-link
   - Status: Good - architectural relationship

5. **effect-type-registry/architecture ↔ cache-optimization**
   - Type: related
   - Status: Good - related concepts

**Summary:** 4 healthy, 1 needs fixing

## One-Way References (8)

References that are not reciprocated:

1. **cache-optimization → architecture** (related)
   - Currently: One-way
   - Suggestion: Already exists! This is duplicate of #5 above
   - Action: Verify frontmatter is correct

2. **performance-observability → observability** (content-link)
   - Currently: Cross-module, one-way
   - Suggestion: Add cross-module reference in registry/observability
   - Action: Document integration pattern

3. **snapshot-tracking → build-architecture** (dependency)
   - Currently: One-way dependency
   - Status: Appropriate - implementation depends on architecture
   - Action: No change needed

[... 5 more ...]

**Summary:**

- 3 should add back-references (improve discoverability)
- 5 are appropriately one-way (dependencies, content-links)

## Example 6 Recommendations

**High Priority:**

1. Add back-reference: observability → performance-observability

**Low Priority:**

2. Review other one-way references for bidirectional opportunities

## Example 7: No Design Docs Found

**User request:**

> Show design doc graph for new-module

**Execution:**

1. Load config
2. Check for new-module
3. No docs found in `.claude/design/new-module/`

**Output:**

```text
INFO: No design documents found

**Module:** new-module
**Path:** .claude/design/new-module/

This is normal for new modules.

**Next steps:**

1. Run `/design-init new-module {topic}` to create your first design doc
2. Add cross-references as you create more docs
3. Run `/design-link new-module` to see relationships

**Example:**

/design-init new-module architecture

## Example 8: Broken References

**User request:**

> Analyze design doc graph

**Execution:**

1. Build graph
2. Detect broken references (docs that no longer exist)
3. Report with recommendations

**Output:**

```text
WARNING: Broken references detected

## Broken References (2)

### effect-type-registry/observability.md

**Broken reference:** ../deleted-module/deleted-doc.md
**Reference type:** dependency (frontmatter)
**Impact:** Document structure shows dependency that doesn't exist

**Fix:**

1. Remove from frontmatter:
   ```yaml
   dependencies:
     # - ../deleted-module/deleted-doc.md  # REMOVE THIS
   ```

1. Or: Create the missing document if still needed

### rspress-plugin-api-extractor/build-architecture.md

**Broken reference:** [Old API](./old-api.md)
**Reference type:** content-link
**Impact:** Broken markdown link in document

**Fix:**

1. Update link to point to current-api.md:

   ```markdown
   [API Documentation](./current-api.md)
   ```

2. Or: Remove link if no longer relevant

## Example 8 Recommendations

1. Fix 2 broken references
2. Run `/design-validate` to check for other issues
3. Re-run `/design-link` to verify graph health
