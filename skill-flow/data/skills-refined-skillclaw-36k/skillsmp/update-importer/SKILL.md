---
name: update-importer
description: Update importer code when provider resource schemas change
tags: [importer, schema, terraform, maintenance]
---

# Update Importer Skill

When resource schemas in the provider are modified, the corresponding importer code must be updated to match. This skill guides you through the process.

## When to Use This Skill

Use this skill when:
- A provider resource schema is modified (fields added, removed, or renamed)
- The API response structure changes
- You're reviewing changes that touch resource definitions in `/provider/resource_*.go`

## Steps to Update Importer

### 1. Identify Changed Resource

Determine which resource(s) were modified. Common resources:
- `resource_bulk_sync.go` → `/importer/bulk_syncs.go`
- `resource_sync.go` → `/importer/syncs.go`
- `resource_connection_*.go` → `/importer/connections.go`
- `resource_model.go` → `/importer/models.go`

### 2. Check for Schema Validation

Each importer should use the schema validation pattern. Verify the importer has:

```go
// At the start of GenerateTerraformFiles
validator, err := NewSchemaValidator(ctx, provider.New{Resource}ResourceForSchemaIntrospection())
if err != nil {
    return fmt.Errorf("failed to create schema validator: %w", err)
}
```

If not present, add it following the pattern in `/importer/bulk_syncs.go`.

### 3. Update Field Mapping

In the `buildFieldMapping()` function, add any new fields:

```go
// Required fields
mapping := map[string]interface{}{
    "field_name": value,
    // ... existing fields
}

// Optional fields
if response.NewField != nil {
    mapping["new_field"] = response.NewField
}
```

**Important**: The mapping keys must exactly match the `tfsdk` tag names in the provider's resource data struct.

### 4. Update HCL Generation

In the `GenerateTerraformFiles()` function, add code to generate HCL for new fields:

```go
// For simple fields
if response.NewField != nil {
    resourceBlock.Body().SetAttributeValue("new_field",
        cty.StringVal(pointer.GetString(response.NewField)))
}

// For nested objects
if response.NewNested != nil {
    resourceBlock.Body().SetAttributeValue("new_nested",
        typeConverter(response.NewNested))
}

// For jsonencoded strings
tokens := wrapJSONEncode(response.NewConfig)
resourceBlock.Body().SetAttributeRaw("new_config", tokens)
```

### 5. Handle Field Renames

When fields are renamed in the schema:

1. Update the schema validator's suggestion map in `/importer/schema_validator.go`:

```go
suggestions := map[string]string{
    "old_field_name": "new_field_name",
}
```

2. Update both the mapping and HCL generation to use the new field name

### 6. Add Introspection Function

If the provider resource doesn't have an introspection function, add one:

```go
// In /provider/resource_{name}.go
func New{Resource}ResourceForSchemaIntrospection() resource.Resource {
    return &{resource}Resource{}
}
```

### 7. Verify with Tests

Build and test:

```bash
# Build importer
go build ./importer/...

# Run roundtrip tests
POLYTOMIC_API_KEY=$API_KEY POLYTOMIC_DEPLOYMENT_URL=$URL \
  TF_ACC=1 go test ./tests/... -v -timeout 120m
```

## Common Patterns

### Nested Objects (SingleNestedAttribute)

```go
// Build tokens manually for proper HCL structure
tokens := hclwrite.Tokens{
    &hclwrite.Token{Bytes: []byte("{\n")},
    &hclwrite.Token{Bytes: []byte("    field = ")},
    &hclwrite.Token{Bytes: []byte(fmt.Sprintf(`"%s"`, value))},
    &hclwrite.Token{Bytes: []byte("\n  }")},
}
resourceBlock.Body().SetAttributeRaw("nested_field", tokens)
```

### Set/List of Objects

```go
// Convert to array of maps
objects := make([]map[string]interface{}, 0, len(items))
for _, item := range items {
    objects = append(objects, map[string]interface{}{
        "id":      item.Id,
        "enabled": item.Enabled,
    })
}
resourceBlock.Body().SetAttributeValue("items", typeConverter(objects))
```

### Optional Fields

Always check if optional fields are present before adding to mapping or HCL:

```go
if response.OptionalField != nil {
    // Add to mapping and generate HCL
}
```

## Schema Drift Detection

The schema validator will fail with helpful errors if fields don't match:

```
schema validation failed for resource 'my-resource':
field 'old_field_name' not found in schema, did you mean 'new_field_name'?
```

This prevents drift by failing fast during import rather than at terraform plan time.

## Checklist

- [ ] Identified which importer file needs updates
- [ ] Added/verified schema validator is present
- [ ] Updated `buildFieldMapping()` with new/changed fields
- [ ] Updated `GenerateTerraformFiles()` HCL generation
- [ ] Handled renamed fields in validator suggestions
- [ ] Added introspection function to provider resource (if needed)
- [ ] Built importer successfully
- [ ] Verified with roundtrip tests (or documented why not possible)

## Notes

- The schema validator acts as the "source of truth" - provider schema changes are automatically caught
- Always prefer using `typeConverter()` for complex types rather than manual token construction
- Keep field names in sync between mapping keys and HCL generation
- Optional fields should gracefully handle nil values
