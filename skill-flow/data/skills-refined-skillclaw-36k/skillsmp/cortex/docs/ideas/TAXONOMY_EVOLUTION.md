# Taxonomy Evolution — Future Exploration

**Status:** Idea / Not Started  
**Last Updated:** January 21, 2026  
**Related:** `MEMORY_SYSTEM_SPEC.md`

---

## The Problem

Entity types are static but should evolve:

```
Initial:     {type: "Company"}
After 100 companies: {type: "Company", subtype: "Startup|Enterprise|Agency", industry: "..."}
```

This problem appears across multiple domains:

| Domain | Example |
|--------|---------|
| **Entity types** | Company → Startup / Enterprise / Agency |
| **Capability taxonomy** | "file_edit" vs "edit_file" vs "modify_file" → canonical form |
| **PII categories** | Person → Customer / Employee / Contact |
| **Relationship types** | KNOWS → FRIENDS_WITH / COLLEAGUES_WITH / ACQUAINTANCE |

---

## Why Inline Resolution Isn't Enough

Graphiti's inline entity resolution handles **identity**:
- "Tyler" = "Tyler Brandt" ✓

But not **category refinement**:
- "Should 'Company' split into subtypes?" ✗
- "This was 'Vendor' but now acts like 'Partner'" ✗

---

## Possible Approaches

### 1. Periodic Clustering + Human Review

```
1. Get all entities of type "Company"
2. Embed their names + summaries
3. Cluster by similarity (k-means, HDBSCAN)
4. For each cluster, LLM proposes a subtype name
5. Human reviews proposed taxonomy
6. Apply: update entity types
```

**Pros:** Human oversight, controllable  
**Cons:** Requires human intervention, batch process

### 2. Confidence-Based Promotion

```
1. During extraction, track type confidence
2. When type is ambiguous (confidence < threshold):
   - Create entity with best-guess type
   - Add to "needs review" queue
3. Periodically, analyze ambiguous entities
4. Propose new types or subtype splits
```

**Pros:** Identifies weak spots automatically  
**Cons:** Still needs batch review

### 3. Emergent Subtyping from Relationships

```
1. Analyze relationship patterns
2. Companies that have EMPLOYS edges → likely larger
3. Companies that only have WORKS_WITH edges → likely vendors
4. Propose subtypes based on relationship signatures
```

**Pros:** Uses structural info, not just names  
**Cons:** Requires sufficient relationship data

### 4. LLM-Assisted Ontology Refinement

```
1. Periodically show LLM all entities of a type
2. Ask: "Should this type be split? How?"
3. LLM proposes: "Split 'Company' into: Employer, Client, Vendor"
4. Apply or defer
```

**Pros:** Leverages LLM reasoning  
**Cons:** Token-expensive, may hallucinate

---

## Relationship to Community Detection

| Community Detection | Taxonomy Evolution |
|--------------------|--------------------|
| Groups related entities | Refines entity types |
| "These people work together" | "These are 'Colleagues'" |
| Emergent, per-instance | Structural, affects schema |
| Run frequently | Run occasionally |

Community detection can **inform** taxonomy evolution:
- If community "Tyler's Work Contacts" always contains Person entities
- And they all have WORKS_WITH edges to Tyler
- Propose subtype: Person → Colleague

---

## Implementation Ideas

### Schema Support

```sql
-- Track type history
CREATE TABLE entity_type_history (
    entity_id TEXT,
    old_type TEXT,
    new_type TEXT,
    reason TEXT,
    changed_at TEXT
);

-- Track proposed types
CREATE TABLE proposed_types (
    id TEXT PRIMARY KEY,
    base_type TEXT,
    proposed_subtype TEXT,
    evidence TEXT,  -- JSON: cluster members, relationship patterns
    confidence REAL,
    status TEXT,  -- 'pending', 'accepted', 'rejected'
    created_at TEXT
);
```

### Batch Job Skeleton

```go
func EvolveTypeTaxonomy(ctx context.Context, baseType string) error {
    // 1. Get all entities of type
    entities, _ := store.GetEntitiesByType(baseType)
    
    // 2. Cluster by embedding
    clusters := ClusterEntities(entities)
    
    // 3. For each cluster, propose subtype
    proposals := []TypeProposal{}
    for _, cluster := range clusters {
        name, confidence := ProposeSubtypeName(cluster)
        proposals = append(proposals, TypeProposal{
            BaseType:     baseType,
            ProposedType: name,
            Members:      cluster.EntityIDs,
            Confidence:   confidence,
        })
    }
    
    // 4. Store for review (or auto-apply if confidence high)
    return store.SaveTypeProposals(proposals)
}
```

---

## Questions to Explore

1. **When to run?** After N new entities? On schedule? On demand?

2. **Auto-apply threshold?** What confidence level allows automatic type updates?

3. **Type hierarchy depth?** Company → Startup → YC_Startup? How deep?

4. **Cross-type relationships?** Can relationship patterns inform type changes?

5. **Rollback?** How to undo a bad taxonomy change?

---

## Deferred Until

This exploration should happen **after** the core memory system is working:
- [ ] Entity extraction working
- [ ] Entity resolution working
- [ ] Relationships extraction working
- [ ] Community detection working

Then we can build taxonomy evolution on top.

---

*This is an idea document for future exploration. Not part of current implementation.*
