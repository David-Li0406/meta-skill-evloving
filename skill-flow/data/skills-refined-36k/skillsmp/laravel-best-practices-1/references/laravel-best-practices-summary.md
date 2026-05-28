# Laravel Best Practices Skill Summary

This folder is designed for AI coding agents that operate inside a Laravel repository.
It provides a rule-backed workflow for:

- Code generation (Laravel idioms and layering)
- Code review (diff/file review with rule ids and patch outlines)
- Test planning and scaffolding (Pest preferred; PHPUnit supported)

## Primary patterns enforced
- FormRequest validation and authorization
- Thin controllers; orchestration only
- Service/Action classes for workflows
- Eloquent scopes/relationships for reusable query logic
- No DB queries in Blade; eager loading to prevent N+1
- Chunking/streaming for large dataset processing

See `references/rulebook.json` for rule ids and detection signals.
