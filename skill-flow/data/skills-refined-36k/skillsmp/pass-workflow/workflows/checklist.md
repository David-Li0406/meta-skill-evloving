# Pass Development Checklist

Universal checklists for ensuring pass development completeness.

## Create New Pass Checklist

### Design Phase
- [ ] Identify target obfuscation pattern
- [ ] Determine AST node types
- [ ] Plan transformation logic
- [ ] Evaluate if transformation affects scope

### Implementation Phase
- [ ] Create `src/passes/<name>.ts`
- [ ] Implement Pass interface (name, description, pre/visitor/post)
- [ ] Add statistics tracking
- [ ] Add logging
- [ ] Mark dirty flags

### Testing Phase
- [ ] Create `tests/passes/<name>.test.ts`
- [ ] Cover basic transformations
- [ ] Cover all operators/variants
- [ ] Cover edge cases (NaN, Infinity, null, undefined)
- [ ] Cover type coercion
- [ ] Cover nested patterns
- [ ] Include negative cases (non-matching code unchanged)

### Examples Phase
- [ ] Create `examples/<name>.js`
- [ ] Include obfuscated input examples
- [ ] Add comments showing expected output
- [ ] Verify with CLI: `./bin/unmanglejs.js examples/<name>.js -p`

### Documentation Phase
- [ ] Create `docs/en/passes/<name>.md`
- [ ] Include overview
- [ ] List all features with examples
- [ ] Add edge case notes
- [ ] Translate to Chinese: `docs/zh-CN/passes/<name>.md`

### Registration Phase
- [ ] Add to `src/passes/registry.ts`
- [ ] Export from `src/passes/index.ts`
- [ ] Verify: `./bin/unmanglejs.js --list-passes | grep <name>`

### Final Validation
- [ ] `npm test` - All tests pass
- [ ] `npm run lint` - No lint errors
- [ ] `npm run format:check` - Code properly formatted
- [ ] `npm run build` - Build succeeds

---

## Modify Existing Pass Checklist

### Understand Phase
- [ ] Read existing implementation
- [ ] Read existing tests
- [ ] Read existing documentation
- [ ] Understand current behavior

### Modify Phase
- [ ] Add tests first (TDD)
- [ ] Modify implementation
- [ ] Update examples
- [ ] Update English documentation
- [ ] Update Chinese documentation

### Validation Phase
- [ ] New tests pass
- [ ] Old tests still pass
- [ ] CLI validation passes
- [ ] Five-file sync check

---

## Debug Pass Checklist

### Isolate Issue
- [ ] Create minimal reproduction
- [ ] Run with `-d` flag
- [ ] Test target pass in isolation

### Check Common Issues
- [ ] `ctx.markAstDirty()` marked?
- [ ] `path.skip()` added (after replacement)?
- [ ] Transformation logic correct?
- [ ] Scope handling correct? (see babel-api-gotchas.md)

### Verify Fix
- [ ] Minimal reproduction passes
- [ ] Original tests still pass
- [ ] Edge case tests added

---

## Documentation Update Checklist

### Sync Check
- [ ] Implementation code matches docs
- [ ] Examples match docs
- [ ] English and Chinese docs structure match
- [ ] All features documented

### Quality Check
- [ ] Each feature has example
- [ ] Edge cases documented
- [ ] Code examples runnable
- [ ] Cross-references correct
