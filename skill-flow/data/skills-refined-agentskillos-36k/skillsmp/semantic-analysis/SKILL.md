---
name: semantic-analysis
description: Semantic Code Analysis Workflow
---

# Semantic Code Analysis Workflow

This workflow enhances AG4ONE capabilities by integrating Serena's semantic code analysis and manipulation tools.

## Purpose

Provide IDE-like capabilities to AI agents through semantic understanding of code structure, enabling efficient navigation and precise editing operations.

## When to Use

- **Large codebases** where grep/file reading is inefficient
- **Complex projects** with many interconnected components
- **Precise editing** needed at symbol/function level
- **Dependency analysis** for understanding code relationships
- **Token optimization** for cost-effective AI coding

## Required Reading

- `@ag4one/serena/README.md` - Serena integration overview
- `@AG4-STYLE.md` - AG4ONE style and conventions
- `@.planning/STATE.md` - Current project state

## Process

### Phase 1: Semantic Discovery
```
<step name="semantic_codebase_analysis" priority="first">
1. Use Serena to discover codebase structure:
   - Find all symbols (classes, functions, methods)
   - Map relationships and dependencies
   - Identify architectural patterns
2. Create semantic index of key components
3. Store analysis results in `SERENA-ANALYSIS.md`
</step>
```

### Phase 2: Targeted Search
```
<step name="semantic_pattern_search">
1. Use Serena semantic search instead of grep:
   - Find symbols by name patterns
   - Locate code by functionality
   - Search within specific scopes (files, directories)
2. Apply filters for language, type, accessibility
3. Retrieve only relevant code sections
</step>
```

### Phase 3: Precise Editing
```
<step name="symbol_level_editing">
1. Use Serena symbol manipulation for changes:
   - Insert code at specific symbol locations
   - Replace function bodies while preserving signatures
   - Add methods to classes precisely
   - Modify imports and dependencies accurately
2. Validate edits with Serena's understanding
3. Verify surrounding code context remains intact
</step>
```

### Phase 4: Dependency Management
```
<step name="relationship_analysis">
1. Use Serena to understand code relationships:
   - Find all references to modified symbols
   - Update dependent components automatically
   - Validate no broken references remain
2. Map impact of changes across codebase
3. Document dependencies for future iterations
</step>
```

## Serena Tool Integration

### Symbol Discovery
```bash
# Find all authentication-related symbols
serena find_symbol --pattern "auth*" --type function,class
```

### Semantic Search
```bash
# Search for database connection patterns
serena semantic_search --query "database connection" --language typescript
```

### Precise Editing
```bash
# Add new method to UserService class
serena insert_after_symbol --class UserService --after_method --name validateEmail
```

### Relationship Analysis
```bash
# Find all code using PaymentProcessor
serena find_referencing_symbols --symbol PaymentProcessor
```

## Success Criteria

- [ ] Semantic index created for codebase
- [ ] Token usage reduced compared to file-based approaches
- [ ] Precise symbol-level edits completed
- [ ] All code relationships understood and maintained
- [ ] No broken references or dependencies
- [ ] Documentation updated with semantic findings

## AG4ONE Enhancement

This workflow transforms AG4ONE from file-based to semantic-based operations:

**Before**: Read entire files, grep for patterns, string replacements
**After**: Symbol discovery, semantic search, precise editing, relationship analysis

Result: More efficient AI coding with better context understanding and reduced token consumption.

---

**AG4ONE Semantic Analysis** - IDE-level capabilities for AI pair programming.