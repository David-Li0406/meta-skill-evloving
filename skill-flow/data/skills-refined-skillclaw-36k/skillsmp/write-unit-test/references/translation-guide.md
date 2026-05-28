# Functional Specification Reference

This document provides detailed examples of the functional specification format used to generate unit tests with the PreDB/PostDB pattern.

## Specification Format

Functional specifications follow this three-part structure:

### 1. PreDB
Define the initial state of the database before the test runs. Uses a CSV-like format where the first line is column headers and subsequent lines are data rows.

### 2. Workflow
A bullet-point list describing the sequence of actions and expected behavior. The first bullet typically indicates the public method being tested.

### 3. PostDB
Define the expected state of the database after the test runs. Includes both pre-existing rows and new rows created during the test.

## Placeholder Values

Use these placeholders for runtime-generated values:

- `<uuid>` - Auto-generated unique identifier
- `<timestamp>` - Auto-generated timestamp
- `<timestamp-1>`, `<timestamp-2>` - Multiple distinct timestamps
- `<vector>` - Embedding vector (dimension inferred from context)
- `<1536-dim vector>` - Explicit dimension specification
- `<3072-dim vector>` - Different dimension specification

## Complete Examples

### Example 1: Empty Database (Seed Case)

```markdown
## Create new idea with empty archive

### PreDB
idea:
(empty table)

### Workflow
* Call `dreamer.create()`
* LLM generates initial seed idea
* Idea description is embedded using text-embedding-3-small
* Idea is saved to database with embedding
* Returns Idea object

### PostDB
idea:
id, description, embedding, status, createdAt
<uuid>, "A simple task management app", <1536-dim vector>, pending, <timestamp>
```

**Key Characteristics:**
- Uses `(empty table)` to indicate no pre-existing data
- PostDB show only the newly created row
- Status defaults to 'pending'
- Placeholders indicate values generated at runtime

### Example 2: Single Pre-existing Row

```markdown
## Create new idea with successful products in archive

### PreDB
idea:
id, description, embedding, status, createdAt
idea-1, "Todo list app", <vector-1>, complete, <timestamp-1>
idea-2, "Blog platform", <vector-2>, complete, <timestamp-2>

### Workflow
* Call `dreamer.create()`
* Dreamer queries archive for successful products
* LLM receives successful product ideas as context
* LLM generates new idea building on successful patterns
* New idea is embedded using text-embedding-3-small
* Idea is saved to database
* Returns Idea object

### PostDB
idea:
id, description, embedding, status, createdAt
idea-1, "Todo list app", <vector-1>, complete, <timestamp-1>
idea-2, "Blog platform", <vector-2>, complete, <timestamp-2>
idea-3, "Collaborative kanban board", <vector-3>, pending, <timestamp-3>
```

**Key Characteristics:**
- PreDB show multiple pre-existing rows
- Each row uses hardcoded IDs for test data (idea-1, idea-2)
- Placeholders use suffixes to distinguish different values (<timestamp-1>, <timestamp-2>)
- PostDB include both pre-existing AND new rows
- New row gets a new placeholder ID (idea-3)

### Example 3: Filtering by Status

```markdown
## Create new idea with failed products in archive

### PreDB
idea:
id, description, embedding, status, createdAt
idea-1, "Complex real-time game engine", <vector-1>, failed, <timestamp-1>

### Workflow
* Call `dreamer.create()`
* Dreamer queries archive for failed products
* LLM receives failed product ideas as context
* LLM generates new idea avoiding overly complex patterns
* New idea is more learnable given current skill level
* Idea is embedded and saved
* Returns Idea object

### PostDB
idea:
id, description, embedding, status, createdAt
idea-1, "Complex real-time game engine", <vector-1>, failed, <timestamp-1>
idea-2, "Simple note-taking app", <vector-2>, pending, <timestamp-2>
```

**Key Characteristics:**
- Uses status='failed' to test specific filtering logic
- Workflow describes the business logic (avoiding complexity)
- New idea has status='pending' (different from pre-existing)

### Example 4: Mixed Data Scenario

```markdown
## Create new idea with both successful and failed products

### PreDB
idea:
id, description, embedding, status, createdAt
idea-1, "Todo list app", <vector-1>, complete, <timestamp-1>
idea-2, "Complex real-time game", <vector-2>, failed, <timestamp-2>

### Workflow
* Call `dreamer.create()`
* Dreamer queries archive for both successful and failed products
* LLM receives both as context (successful as stepping stones, failed to avoid)
* LLM generates new idea that:
  - Builds on successful patterns
  - Avoids complexity that led to failures
  - Progresses toward more challenging tasks appropriately
* Idea is embedded using text-embedding-3-small (1536 dimensions)
* Idea is saved to database
* Returns Idea object

### PostDB
idea:
id, description, embedding, status, createdAt
idea-1, "Todo list app", <vector-1>, complete, <timestamp-1>
idea-2, "Complex real-time game", <vector-2>, failed, <timestamp-2>
idea-3, "Todo app with real-time sync", <vector-3>, pending, <timestamp-3>
```

**Key Characteristics:**
- Tests complex business logic with mixed status values
- Workflow uses sub-bullets to describe detailed expectations
- Explicitly states vector dimensions in Workflow (1536)
- Generated test name would be: "should create new idea with both successful and failed products"

## Multiple Table Examples

### Example 5: Foreign Key Relationships

```markdown
## Create specification from idea

### PreDB
idea:
id, description, embedding, status, createdAt
idea-1, "Todo list app", <vector>, complete, <timestamp-1>

spec:
(empty table)

### Workflow
* Call `judge.createSpec(ideaId: 'idea-1')`
* Judge retrieves idea description
* LLM generates detailed functional specification
* Spec is saved with foreign key to idea
* Returns Spec object

### PostDB
idea:
id, description, embedding, status, createdAt
idea-1, "Todo list app", <vector>, complete, <timestamp-1>

spec:
id, ideaId, content, createdAt
<uuid>, idea-1, "Functional spec content...", <timestamp-2>
```

**Key Characteristics:**
- Multiple tables defined separately in PreDB
- Each table section starts with `table_name:`
- Foreign keys use hardcoded IDs (ideaId: idea-1)
- Empty tables use `(empty table)` notation
- PostDB show state of ALL relevant tables

### Example 6: Cascade Updates

```markdown
## Update product status after completion

### PreDB
idea:
id, description, embedding, status, createdAt
idea-1, "Todo app", <vector>, pending, <timestamp-1>

product:
id, ideaId, status, createdAt
prod-1, idea-1, in_progress, <timestamp-2>

### Workflow
* Call `product.complete(productId: 'prod-1')`
* Product status is updated to 'complete'
* Idea status is updated to 'complete' (cascade effect)
* Returns updated Product object

### PostDB
idea:
id, description, embedding, status, createdAt
idea-1, "Todo app", <vector>, complete, <timestamp-1>

product:
id, ideaId, status, createdAt
prod-1, idea-1, complete, <timestamp-2>
```

**Key Characteristics:**
- Shows state changes across related tables
- Notice status changes in both idea and product
- Demonstrates business logic that spans multiple tables

## Translation to Tests

### PreDB � PreDB

```typescript
// Empty table
await PreDB(db, schema, {
  idea: [],
});

// Table with data
const now = new Date();
await PreDB(db, schema, {
  idea: [
    {
      id: 'idea-1',
      description: 'Todo list app',
      embedding: new Array(1536).fill(0.1),
      status: 'complete',
      createdAt: now,
    },
  ],
});

// Multiple tables
await PreDB(db, schema, {
  idea: [
    { id: 'idea-1', description: 'Todo app', embedding: new Array(1536).fill(0.1), status: 'pending', createdAt: now },
  ],
  spec: [
    { id: 'spec-1', ideaId: 'idea-1', createdAt: now },
  ],
});
```

### Workflow � Test Execution

```typescript
// From: Call `dreamer.create()`
const result = await dreamer.create();

// From: Call `judge.createSpec(ideaId: 'idea-1')`
const result = await judge.createSpec('idea-1');
```

### PostDB � Assertions + PostDB

```typescript
// Assertions based on expected values
expect(idea.description.length).toBeGreaterThan(10);
expect(idea.embedding).toHaveLength(1536);
expect(idea.status).toBe('pending');

// PostDB verification (using allowExtraRows when pre-existing data exists)
await PostDB(db, schema, {
  idea: [
    {
      id: idea.id,
      description: idea.description,
      embedding: idea.embedding,
      status: idea.status,
      createdAt: idea.createdAt,
    },
  ],
}, { allowExtraRows: true });
```

## Common Patterns

### Pattern 1: Testing with No Pre-existing Data

```markdown
### PreDB
tableName:
(empty table)
```

Maps to:
```typescript
await PreDB(db, schema, {
  tableName: [],
});
```

### Pattern 2: Using Multiple Distinct Placeholders

```markdown
### PreDB
idea:
id, description, embedding, status, createdAt
idea-1, "First idea", <vector-1>, complete, <timestamp-1>
idea-2, "Second idea", <vector-2>, complete, <timestamp-2>
```

Maps to:
```typescript
const now = new Date();
await PreDB(db, schema, {
  idea: [
    { id: 'idea-1', description: 'First idea', embedding: new Array(1536).fill(0.1), status: 'complete', createdAt: now },
    { id: 'idea-2', description: 'Second idea', embedding: new Array(1536).fill(0.2), status: 'complete', createdAt: now },
  ],
});
```

**Note:** Use different fill values for distinct vectors (0.1 vs 0.2) but same timestamp constant is acceptable for test data.

### Pattern 3: Quoted String Values

When values contain spaces or special characters, use quotes:

```markdown
idea:
id, description
idea-1, "Todo list with real-time collaboration"
```

Maps to:
```typescript
{ id: 'idea-1', description: 'Todo list with real-time collaboration' }
```

### Pattern 4: Enum Values

```markdown
idea:
id, status
idea-1, complete
idea-2, failed
idea-3, pending
```

Maps to:
```typescript
{ id: 'idea-1', status: 'complete' }
{ id: 'idea-2', status: 'failed' }
{ id: 'idea-3', status: 'pending' }
```

**Note:** No quotes in spec, but translated to string literals in code.

## Best Practices

### DO:
- Use descriptive scenario names that explain the test case
- Keep workflows focused on behavior, not implementation
- Use placeholders for runtime-generated values
- Include both pre-existing and new rows in PostDB
- Use hardcoded IDs for test data (idea-1, spec-1, etc.)
- Use `(empty table)` notation for tables with no data

### DON'T:
- Include implementation details in Workflow (focus on what happens, not how)
- Use actual UUIDs or timestamps in specs (use placeholders)
- Omit pre-existing rows from PostDB (show complete state)
- Mix concerns - each scenario should test one logical case
- Add unnecessary complexity - keep specs simple and focused

## Spec Writing Checklist

When writing a new functional specification:

- [ ] Scenario has clear, descriptive name
- [ ] PreDB define ALL relevant table states
- [ ] Workflow starts with method call (e.g., "Call `class.method(args)`")
- [ ] Workflow describes behavior, not implementation
- [ ] Placeholders used for generated values
- [ ] PostDB show complete expected database state
- [ ] PostDB include both pre-existing and new rows
- [ ] Column names match database schema exactly
- [ ] Enum values match schema definitions
- [ ] Foreign key relationships are correctly specified

## Example Scenario Names

Good scenario names that translate to clear test names:

- "Create new idea with empty archive" � "should create new idea when archive is empty"
- "Create new idea with successful products" � "should create new idea with successful products in archive"
- "Update product status after completion" � "should update product status after completion"
- "Generate spec from idea" � "should generate spec from idea"
- "Reject invalid input" � "should reject invalid input"

## Notes

- Specs are written BEFORE implementation (TDD approach)
- Tests generated from specs will fail until implementation exists
- Specs define the contract that implementation must satisfy
- Focus on WHAT the system does, not HOW it works
- PreDB/PostDB pattern makes database state verification explicit
- Use `allowExtraRows: true` in PostDB when you only care about changes
