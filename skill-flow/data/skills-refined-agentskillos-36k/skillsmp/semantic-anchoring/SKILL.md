---
name: semantic-anchoring
description: Validate and enrich semantic references (ConceptIds) against the Knowledge Graph. Use when linking artifacts, specs, or code to ontology concepts, validating SHACL constraints, or discovering related concepts from DomainForge™.
license: Complete terms in LICENSE.txt
---

# Semantic Anchoring

Validate, enrich, and link content to the SEA-Forge™ Knowledge Graph using semantic references (ConceptIds).

**For reference:** [DomainForge Handbook](../../../docs/handbooks/DomainForge_Handbook/README.md) | [SDS-009: Knowledge Graph Service](../../../docs/specs/semantic-core/sds/009-knowledge-graph-service.md)

---

## When to Use This Skill

Use semantic-anchoring when:

1. **Linking to Concepts**: Adding `semanticRefs` to CADSL artifacts, specs, or code
2. **Validating References**: Checking if ConceptIds exist in the Knowledge Graph
3. **Discovering Concepts**: Finding related concepts for suggestions
4. **Enforcing Constraints**: Validating SHACL shapes on artifact structures
5. **Building Traceability**: Connecting specs → code → artifacts semantically

---

## ConceptId Format

ConceptIds follow this format:

```
<namespace>:<ConceptName>
```

**Examples:**
- `sea:BoundedContext` - SEA-Forge core ontology
- `sea:CognitiveArtifact` - Cognitive Extension
- `cmmn:Case` - CMMN primitives
- `domain:Customer` - Domain-specific concepts

**Reserved Namespaces:**
| Namespace | Ontology | Description |
|-----------|----------|-------------|
| `sea` | SEA-Forge Core | Core platform concepts |
| `cmmn` | CMMN | Case management primitives |
| `otel` | OpenTelemetry | Observability concepts |
| `domain` | Domain | Project-specific concepts |

---

## Validation Workflow

### Step 1: Extract ConceptIds

From CADSL artifact:
```yaml
semanticRefs:
  - conceptId: "sea:BoundedContext"
  - conceptId: "domain:Customer"
```

From code annotation:
```python
# @sea:Entity
class Customer:
    pass
```

### Step 2: Query Knowledge Graph

Use SPARQL to validate:

```sparql
ASK {
  <http://sea-forge.org/ontology#BoundedContext> a owl:Class .
}
```

Or use the Knowledge Graph Service API:

```bash
curl -X GET "http://localhost:7200/repositories/sea/concepts/sea:BoundedContext"
```

### Step 3: Report Results

**Valid ConceptId:**
```
✅ sea:BoundedContext - Found in SEA Core Ontology
   URI: http://sea-forge.org/ontology#BoundedContext
   Type: owl:Class
   Related: [sea:Domain, sea:Entity, sea:Flow]
```

**Invalid ConceptId:**
```
❌ sea:UnknownConcept - Not found in Knowledge Graph
   Suggestions:
   - sea:Concept (similarity: 0.85)
   - sea:Entity (similarity: 0.72)
```

---

## SHACL Constraint Validation

Validate artifact structures against SHACL shapes:

```turtle
sea:ChecklistShape a sh:NodeShape ;
  sh:targetClass sea:Checklist ;
  sh:property [
    sh:path sea:title ;
    sh:minCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path sea:semanticRefs ;
    sh:minCount 1 ;
    sh:message "Artifacts must have at least one semantic reference" ;
  ] .
```

**Validation Command:**
```bash
just validate-shacl artifact.yaml
```

---

## Enrichment Suggestions

When creating new content, suggest semantic anchors:

### Input
```markdown
# API Design Document

We're building a customer management API that handles orders and payments.
```

### Output
```yaml
suggestedAnchors:
  - text: "customer management"
    concepts:
      - conceptId: "domain:Customer"
        confidence: 0.95
      - conceptId: "sea:BoundedContext"
        confidence: 0.75
        
  - text: "orders"
    concepts:
      - conceptId: "domain:Order"
        confidence: 0.92
      - conceptId: "sea:Aggregate"
        confidence: 0.70
        
  - text: "payments"
    concepts:
      - conceptId: "domain:Payment"
        confidence: 0.88
```

---

## Integration Points

### Cognitive Artifacts Builder

When generating CADSL artifacts, validate all `semanticRefs`:

```yaml
# Before generation
validation:
  - conceptId: "sea:Deployment"
    status: "valid"
  - conceptId: "sea:QualityGate"
    status: "valid"
```

### Spec Pipeline

Validate ADR/PRD/SDS references to ontology:

```yaml
# In SDS header
semanticRefs:
  - conceptId: "sea:Service"
    validated: true
  - conceptId: "sea:API"
    validated: true
```

### Case Management

Link cases to domain concepts:

```yaml
case:
  conceptId: "cmmn:Case"
  domainRef: "domain:ProjectDelivery"
```

---

## Quality Guidelines

### 1. Prefer Specific Concepts

❌ **Too Generic:**
```yaml
semanticRefs:
  - conceptId: "sea:Thing"
```

✅ **Specific:**
```yaml
semanticRefs:
  - conceptId: "sea:BoundedContext"
  - conceptId: "domain:CustomerOnboarding"
```

### 2. Include Domain Context

Always include at least one domain-specific concept along with core ontology concepts:

```yaml
semanticRefs:
  - conceptId: "sea:Flow"        # Core ontology
  - conceptId: "domain:Checkout" # Domain specific
```

### 3. Validate Before Publishing

Never publish artifacts with unvalidated ConceptIds. Use:

```bash
just semantic-validate <artifact.yaml>
```

---

## References

- [DomainForge Handbook](../../../docs/handbooks/DomainForge_Handbook/README.md)
- [SDS-009: Knowledge Graph Service](../../../docs/specs/semantic-core/sds/009-knowledge-graph-service.md)
- [SEA Core Ontology](../../../ontology/sea-core.ttl)
- [Cognitive Architecture Handbook](../../../docs/handbooks/Cognitive_Architecture_Handbook/README.md)
