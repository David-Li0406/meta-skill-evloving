# Error Handling Reference

| Error | Cause | Solution |
|-------|-------|----------|
| Schema validation failed | Invalid OpenAPI spec | Fix schema errors, validate with tool |
| Type generation error | Unsupported schema construct | Simplify schema or add custom handler |
| Client compile error | Generated code invalid | Review template, fix generation config |
| Doc generation incomplete | Missing descriptions | Add descriptions to OpenAPI spec |
| Contract test failed | Implementation mismatch | Update implementation to match spec |