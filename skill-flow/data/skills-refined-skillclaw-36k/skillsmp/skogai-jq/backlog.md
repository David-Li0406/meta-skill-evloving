# backlog

items roughly prioritized. top = more urgent/important.

## foundation (must have)

### crud operations
- [x] crud-get - get value at path
- [x] crud-set - set value at path
- [x] crud-delete - remove value at path
- [x] crud-query - filter/select using jq expression
- [x] crud-has - check if path exists
- [x] crud-merge - deep merge objects

### schema validation
- [ ] validate input against schema before transform
- [ ] validate output against schema after transform
- [ ] generate useful error messages
- [ ] test with ajv to ensure it works

### testing infrastructure
- [x] direct jq file testing
- [x] schema validation in tests
- [x] test generator from schema
- [ ] assertion helpers for common checks

## extraction from chat-history

### existing transformations to migrate
these already exist in ~/dev/chat-history/jq-utils/, need to:
1. extract transformation
2. add schema
3. add tests
4. generalize if needed

#### message operations
- [x] extract-role-content - get role and content from message
- [x] format-message - format message to standard shape
- [x] validate-message-schema - check message structure
- [x] normalize-timestamp - standardize timestamp formats
- [x] generate-message-id - create unique id

#### filtering
- [x] filter-by-date-range - messages in time window
- [x] filter-by-role - messages from specific role
- [x] filter-by-pattern - content matching regex
- [x] deduplicate-by-content - remove duplicate messages

#### extraction
- [x] extract-urls - find all urls in content
- [x] extract-mentions - find @mentions
- [x] extract-code-blocks - pull out code
- [x] extract-first-line - get first line of content

#### predicates
- [x] has-field - check field exists
- [x] has-code-block - check for code
- [x] has-url - check for urls
- [x] is-empty-string - check if string empty
- [x] is-timestamp - validate timestamp format
- [x] is-uuid - validate uuid format

#### transformation
- [x] add-field - add field to object
- [x] remove-field - remove field from object
- [x] rename-field - change field name
- [x] copy-field - duplicate field
- [x] pick-fields - select subset of fields

#### aggregation
- [x] group-by-field - group objects by field value
- [x] sort-by-field - sort by field
- [x] count-by-field - count occurrences
- [x] generate-stats - compute statistics

## common patterns (high value)

### array operations
- [x] array-append - add item to array
- [x] array-prepend - add item to start
- [x] array-filter - filter items by predicate
- [x] array-map - transform each item
- [x] array-reduce - reduce to single value
- [x] array-unique - remove duplicates
- [x] array-flatten - flatten nested arrays
- [x] array-chunk - split into chunks

### string operations
- [x] string-split - split by delimiter
- [x] string-join - join array with delimiter
- [x] string-trim - remove whitespace
- [x] string-replace - replace pattern
- [x] string-match - extract matches
- [x] string-truncate - limit length

### validation
- [x] validate-required - check required fields exist
- [x] validate-types - check field types
- [x] validate-format - check string format (email, url, etc)
- [x] validate-range - check numeric range

### type coercion
- [x] to-string - convert to string
- [x] to-number - convert to number
- [x] to-boolean - convert to boolean
- [x] to-array - ensure value is array
- [x] to-object - ensure value is object

### composition helpers
- [x] pipe - chain transformations
- [x] map-transform - apply transformation to array items
- [x] try-transform - apply with fallback on error

## meta/tooling

### transformation development
- [ ] transformation template generator
- [ ] schema generator from example i/o
- [ ] test generator from schema
- [ ] documentation generator

### discovery
- [ ] list all transformations with descriptions
- [ ] search transformations by keyword
- [ ] show transformation dependencies
- [ ] generate usage examples

### quality
- [ ] lint schemas for consistency
- [ ] validate all tests pass
- [ ] check transformation naming conventions
- [ ] ensure documentation is complete

## experiments (maybe)

### performance
- [ ] benchmark transformations
- [ ] identify slow operations
- [ ] streaming mode for large files

### advanced composition
- [ ] transformation pipelines as config
- [ ] conditional transformations
- [ ] parallel transformation execution

### integration
- [ ] github action to run tests
- [ ] pre-commit hook for validation
- [ ] mcp server for transformations

## questions to answer

### about schemas
- what schema format? json-schema vs custom
- how detailed should schemas be?
- document args in schema or comments?

### about testing
- test each transformation in isolation only?
- also test common compositions?
- how to test error cases?

### about organization
- flat directory or categorize by type?
- one big test.sh or per-transformation tests?
- documentation in separate files or inline?

### about usage
- do we need a cli wrapper?
- how to handle transformation discovery?
- version transformations or keep breaking changes?

## done

- [x] establish directory structure
- [x] create crud-get, crud-set, and crud-delete
- [x] direct jq file testing working
- [x] basic schemas for transformations
- [x] comprehensive test suites (600+ tests, all passing)
- [x] test-all.sh runner script
- [x] README.md with full documentation
- [x] project documentation (CLAUDE.md)
- [x] vision and backlog (this file)
- [x] library implemented at src/jq-transforms/
- [x] 62 transformations implemented across 14 categories
- [x] all CRUD operations (6)
- [x] all array operations (8)
- [x] all string operations (6)
- [x] all validation operations (5)
- [x] all type coercion (5)
- [x] all extraction operations (5)
- [x] all filtering operations (3)
- [x] all predicates (6)
- [x] all field operations (5)
- [x] all aggregation operations (4)
- [x] all message operations (3)
- [x] all composition helpers (3)
- [x] schema-validation and test-generator meta tools (2)
