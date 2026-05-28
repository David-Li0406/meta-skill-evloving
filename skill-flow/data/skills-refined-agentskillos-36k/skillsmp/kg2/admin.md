# Administration

GraphDB REST API administration for the `kg2` repository.

## Initial Setup Order

After creating repository (see Repository Setup below): Schema → SHACL → Data

```bash
# 1. Load schema (OWL ontology)
curl -X POST 'https://kg.corca.ai/repositories/kg2/statements' \
  -H 'Content-Type: text/turtle' \
  --data-binary @data/schema.ttl

# 2. Load SHACL shapes
curl -X POST 'https://kg.corca.ai/repositories/kg2/rdf-graphs/service?graph=http://rdf4j.org/schema/rdf4j%23SHACLShapeGraph' \
  -H 'Content-Type: text/turtle' \
  --data-binary @data/shacl.ttl

# 3. Insert data (will be validated)
curl -X POST 'https://kg.corca.ai/repositories/kg2/statements' \
  -H 'Content-Type: text/turtle' \
  --data-binary @your-data.ttl
```

## SHACL Validation

Invalid data is rejected with HTTP 500. SHACL must be enabled at repository creation.

### Reloading Shapes

Clear existing shapes, then reload using Initial Setup step 2:

```bash
curl -X DELETE 'https://kg.corca.ai/repositories/kg2/rdf-graphs/service?graph=http://rdf4j.org/schema/rdf4j%23SHACLShapeGraph'
```

### Verifying SHACL

```bash
# Should return HTTP 500 (Paper missing rdfs:label and primaryAuthor)
curl -s -w "\nHTTP: %{http_code}\n" -X POST \
  'https://kg.corca.ai/repositories/kg2/statements' \
  -H 'Content-Type: text/turtle' \
  --data-binary @- <<'EOF'
@prefix paper: <https://kg.corca.ai/paper#> .
paper:shacl_test a paper:Paper .
EOF
```

If HTTP 204 instead of 500, SHACL is not enforcing. Check for existing violations:

```bash
curl -X POST 'https://kg.corca.ai/rest/repositories/kg2/validate/text' \
  -H 'Content-Type: text/turtle' \
  --data-binary @data/shacl.ttl
```

## Data Operations

```bash
# Export
curl -s 'https://kg.corca.ai/repositories/kg2/statements' \
  -H 'Accept: application/x-trig' -o backup.trig

# Clear
curl -X DELETE 'https://kg.corca.ai/repositories/kg2/statements'
```

## Repository Setup

Config: [data/repo-config.ttl](data/repo-config.ttl)

### Create/Recreate

```bash
# Create new repository
curl -X POST 'https://kg.corca.ai/rest/repositories' \
  -H 'Content-Type: multipart/form-data' \
  -F 'config=@data/repo-config.ttl'

# Delete repository
curl -X DELETE 'https://kg.corca.ai/rest/repositories/kg2'

# Restore from backup (after create)
curl -X POST 'https://kg.corca.ai/repositories/kg2/statements' \
  -H 'Content-Type: application/x-trig' \
  --data-binary @backup.trig
```

For full recreation: Export → Delete → Create → Restore → Load shapes. (SHACL shapes are stored in a separate named graph, not included in the default export.)
