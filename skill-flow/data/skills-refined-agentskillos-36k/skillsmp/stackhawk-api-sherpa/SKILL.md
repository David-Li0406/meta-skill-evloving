---
name: stackhawk-api-sherpa
description: Use when designing new hawkop commands, exploring StackHawk API capabilities, or working with API features. Guides through endpoint selection, CLI design, and implementation.
---

# StackHawk API Sherpa

Your guide to navigating the StackHawk API and building great HawkOp commands.

---

## Step 1: Check Freshness

### OpenAPI Spec
The spec should be refreshed periodically. Check the file date:
```bash
ls -la stackhawk-openapi.json
```

If older than 30 days, refresh:
```bash
curl -o stackhawk-openapi.json https://download.stackhawk.com/openapi/stackhawk-openapi.json
```

### API Reference
Check the `Last Updated` timestamp in `.claude/context/stackhawk-api.md`. If the reference is outdated compared to the spec, note which sections need updating.

---

## Step 2: Read the API Reference

Before designing any command:
1. **Read** `.claude/context/stackhawk-api.md`
2. **Check** implementation status - is this endpoint already wrapped?
3. **Review** the data model relationships diagram
4. **Note:** Check [api-quirks.md](api-quirks.md) for API behaviors that don't match the OpenAPI spec

---

## Step 3: User Value Assessment

Answer these questions before touching code:

- [ ] **What user problem does this solve?**
  - What question does the user want answered?
  - What action do they want to take?

- [ ] **Who is the user?**
  - Developer checking their scans?
  - Security engineer reviewing findings?
  - DevOps automating pipelines?

- [ ] **How often will this be used?**
  - Daily workflow? → Optimize for speed
  - Occasional admin task? → Optimize for clarity

---

## Step 4: Endpoint Selection

### Find the Right Endpoint(s)
1. Check the API reference by category
2. Consider: Does one endpoint give all needed data, or do we need multiple?
3. Check if v2 endpoint exists (prefer v2 for better pagination)

### Pagination Considerations
- Will the response be large? (100+ items) → Use parallel pagination
- Check if `totalCount` is available in response
- Max page size is 1000

### Rate Limiting
- Which category? Scan (80/sec), User (80/sec), AppList (80/sec), Default (6/sec)
- For bulk operations, consider caching

---

## Step 5: CLI UX Design

### Invoke the CLI Designer
For command UX decisions, also invoke `/cli-designer` to ensure we follow clig.dev principles.

### Command Structure Decision Tree

**Is this a new resource type or extending existing?**
```
Same resource type? → Extend existing command
  Example: `scan get` extends `scan`

New resource type? → New top-level command
  Example: `finding` as new command

Cross-resource query? → Consider which resource is primary
  Example: "findings for app X" → `app findings` or `finding list --app`?
```

**What operation is this?**
```
Retrieving multiple items → `list` subcommand
  Example: `scan list`, `app list`

Retrieving single item by ID → `get` subcommand
  Example: `scan get <ID>`, `app get <ID>`

Modifying state → Verb subcommand
  Example: `scan start`, `app create`, `config upload`
```

### Naming Conventions
- Commands: lowercase, singular nouns (`scan`, `app`, `team`)
- Subcommands: verbs or `list`/`get` (`list`, `get`, `create`, `delete`)
- Flags: `--long-name` with `-s` short form for common ones
- Match existing patterns in hawkop

### Standard Flags
```
--org <ID>        # Organization context
--format <FMT>    # table|json
--limit <N>       # Pagination limit
--debug           # Verbose output
--no-cache        # Bypass cache
```

---

## Step 6: Implementation Planning

### Files to Create/Modify

```
src/client/models/<resource>.rs   # API model
src/client/mod.rs                 # Trait method
src/client/api/<category>.rs      # Implementation
src/models/display/<resource>.rs  # Display model
src/cli/<command>.rs              # CLI handler
src/cli/mod.rs                    # Command enum
src/main.rs                       # Routing
```

### Implementation Checklist

- [ ] **API Model** - Matches OpenAPI schema?
- [ ] **Serde attributes** - `rename_all`, aliases for quirks?
- [ ] **Trait method** - Pagination params if needed?
- [ ] **Error handling** - Descriptive error messages?
- [ ] **Display model** - Key fields for table output?
- [ ] **CLI handler** - Follows existing patterns?
- [ ] **Help text** - Clear, actionable descriptions?
- [ ] **Tests** - Unit + integration tests?

---

## Step 7: Verify with Live API

If the OpenAPI spec is unclear:
1. Use `hawkop` CLI to test (if endpoint implemented)
2. Use StackHawk MCP tools for unimplemented endpoints
3. Document any discrepancies

```bash
# Test with hawkop
hawkop <command> --format json | jq .

# Check actual response shape
cargo run -- <command> --format json --debug 2>&1
```

---

## Step 8: Update Documentation

After implementing:
1. **Update API reference** - Mark endpoint as ✅ implemented
2. **Update CLAUDE.md** - Add command to list if new
3. **Add tests** - Unit and integration

---

## Quick Reference Links

- **API Reference**: `.claude/context/stackhawk-api.md`
- **API Quirks**: [api-quirks.md](api-quirks.md) - API behaviors that differ from the OpenAPI spec
- **CLI Design Principles**: `docs/CLI_DESIGN_PRINCIPLES.md`
- **Implementation Patterns**: `CLAUDE.md` → "Adding New Commands"
- **OpenAPI Spec**: `stackhawk-openapi.json`
- **Existing Commands**: `src/cli/` (follow these patterns)

---

## Common Scenarios

### "I want to add a list command for X"
1. Check API reference for list endpoint
2. Check if v2 endpoint exists
3. Follow `src/cli/app.rs` or `src/cli/scan.rs` as template
4. Add pagination support if large datasets expected

### "I want to add a detail/get command"
1. Check API reference for get-by-ID endpoint
2. Consider drill-down (like `scan get` → alerts → messages)
3. Follow `src/cli/scan.rs` `get()` as template

### "I want to add an action command (create/delete/start)"
1. Check API reference for POST/DELETE endpoint
2. Design confirmation prompts for destructive actions
3. Consider `--yes` flag to skip confirmation
4. Return actionable success/error messages

### "User wants data that spans multiple endpoints"
1. Identify primary resource
2. Consider if we should make multiple API calls
3. Cache where appropriate
4. Present unified output
