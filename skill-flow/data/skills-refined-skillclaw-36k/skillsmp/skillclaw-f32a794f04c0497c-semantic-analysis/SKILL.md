---
name: semantic-analysis
description: Use this skill when you need to perform semantic code analysis and manipulation to enhance navigation and editing in large or complex codebases.
---

# Skill body

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
serena find_symbols --type authentication
```