# PFAS Community Modeling: Functional Roles in Microbial Degradation

This document captures the ongoing discussion about modeling how individual organisms contribute to PFAS (per- and polyfluoroalkyl substances) degradation in microbial communities.

## Background

Marcin is developing a representation for PFAS degradation communities in the `PFASCommunityAgents` repo (CultureBotAI, private). The goal is to model:
- Which organisms are in a community
- What functional role each organism plays
- How the community as a whole degrades PFAS

## Functional Role Enumeration

Marcin proposed the following `FunctionalRoleEnum` (Jan 12, 2026):

| Role | Description |
|------|-------------|
| `primary_degrader` | Primary organism responsible for PFAS degradation |
| `synergist` | Supports degrader via metabolite exchange or growth factors |
| `detoxifier` | Degrades toxic intermediates from primary degradation |
| `electron_shuttle` | Facilitates electron transfer in community metabolism |
| `biotransformer` | Transforms PFAS structure without complete degradation |
| `oxidative_degrader` | Degrades PFAS via oxidative pathways |
| `reductive_degrader` | Degrades PFAS via reductive defluorination |
| `support` | Provides general metabolic support to community |

## Modeling Challenges

### The Ternary Relationship Problem

The relationship between community, organism, and role is inherently ternary:
- An **organism** (NCBITaxon)
- Has a **role** (FunctionalRole)
- In a **community** (BIOSAMPLE or similar)

Standard S-P-O triples cannot directly represent this.

### Proposed Reification Approach

Mark proposed (Jan 13, 2026) using reification:

```
R rdf:type RoleAssertion
R concerns_community BIOSAMPLE:1234
R concerns_organism NCBITaxon:5555
R demonstrates_role oxidative_degrader
```

This creates an intermediate node (R) that connects all three concepts.

### Marcin's Target Model

Marcin outlined the modeling goals:

```
# Community membership
taxon_X biolink:member_of community_A

# Taxon roles
taxon_X has_role R1

# Community composition (inferred)
community_A composed_of_role R1, R2, R3

# Community location
community occurs_in location
community prefers ENVO_term
```

**Prediction targets**:
- taxon → role edges
- taxon → community edges
- community composition

### Domain/Range Issues

Mark identified issues with Biolink predicate usage:

> "A community cannot occur anywhere. Only processes can `occur_in`."

This suggests:
- `biolink:occurs_in` has wrong domain/range for community-location
- May need `community_growth` or `live_community` process node
- Or new METPO predicates

## Biolink Limitations

Marcin noted:
> "Unfortunately this is where biolink may not give the detail we need. It may be that we need more precise predicates in METPO again, eg `assesses`, `is_assessed_by`."

### Potential METPO Additions

For PFAS community modeling:
- `has_functional_role` - organism → role
- `demonstrates_role_in` - organism → community (with role context)
- `is_composed_of_roles` - community → role set

## Related Work

### Enzyme-Assay Modeling (Precedent)

Similar challenges arose modeling enzyme-assay relationships:

```
# Current (problematic)
CHEBI:16828 biolink:occurs_in assay:API_20A_IND
```

Issue: Chemicals cannot "occur in" processes.

Marcin suggested `is_related_to_at_instance_level` from RO:0000056 (participates_in).

### CMM Community Modeling

This PFAS work parallels CMM (Critical Mineral Metabolism) community modeling:
- Same need for organism → role → community representation
- Similar functional role enumerations (but for mineral metabolism)
- Shared infrastructure in cmm-ai-automation

## Implementation Options

### Option 1: Reification (RDF/OWL Style)

```turtle
:assertion_123 a :RoleAssertion ;
    :concerns_community :BIOSAMPLE_1234 ;
    :concerns_organism NCBITaxon:5555 ;
    :demonstrates_role :oxidative_degrader .
```

**Pros**: Semantically clean, extensible
**Cons**: More complex queries, more nodes

### Option 2: Qualified Edges (Biolink Style)

Use edge properties/qualifiers:

```json
{
  "subject": "NCBITaxon:5555",
  "predicate": "biolink:member_of",
  "object": "BIOSAMPLE:1234",
  "qualifiers": {
    "functional_role": "oxidative_degrader"
  }
}
```

**Pros**: Simpler graph structure
**Cons**: Qualifier support varies across tools

### Option 3: Role-Specific Predicates

Create predicates per role:

```
NCBITaxon:5555 METPO:is_primary_degrader_in BIOSAMPLE:1234
NCBITaxon:5556 METPO:is_synergist_in BIOSAMPLE:1234
```

**Pros**: Direct querying
**Cons**: Predicate proliferation, less flexible

### Option 4: Intermediate Role Nodes

```
NCBITaxon:5555 biolink:has_role :role_instance_789
:role_instance_789 rdf:type :oxidative_degrader
:role_instance_789 biolink:occurs_in BIOSAMPLE:1234
```

**Pros**: Balances reification and simplicity
**Cons**: Still adds nodes

## Next Steps

1. **Decide on representation**: Which option best fits kg-microbe patterns?
2. **Define METPO predicates**: If needed for the chosen approach
3. **Prototype in PFASCommunityAgents**: Test with real PFAS data
4. **Coordinate with CMM work**: Ensure compatible patterns

## Relevant Repositories

| Repo | Role |
|------|------|
| [CultureBotAI/PFASCommunityAgents](https://github.com/CultureBotAI/PFASCommunityAgents) | Main PFAS community modeling (private) |
| [CultureBotAI/PFAS-AI](https://github.com/CultureBotAI/PFAS-AI) | PFAS literature/data (public) |
| [berkeleybop/metpo](https://github.com/berkeleybop/metpo) | METPO ontology for predicates |
| [Knowledge-Graph-Hub/kg-microbe](https://github.com/Knowledge-Graph-Hub/kg-microbe) | Integration target |
| [turbomam/cmm-ai-automation](https://github.com/turbomam/cmm-ai-automation) | CMM parallel work (this repo) |

## Discussion References

- Slack #kg-microbe-ldrd: Jan 12-13, 2026 discussion on functional roles
- Slack #culturebot: Dec 4, 2025 - Mark asking for guidance on contributing
- kg-microbe Issue #458: METPO predicates for Madin and BactoTraits

---

*Last updated: 2026-01-14*
*Based on Slack discussions in #kg-microbe-ldrd*
