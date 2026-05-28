# Workflow: Testing Guidance

<required_reading>
**Read ALL references**:
1. references/data-layer-tests.md
2. references/biz-layer-tests.md
3. references/service-layer-tests.md
4. references/test-helpers.md
5. references/table-driven-tests.md
6. references/mock-patterns.md
</required_reading>

<process>
## Step 1: Determine Guidance Needed

Ask: "What aspect of testing would you like guidance on?"

Options:
1. **Overall testing strategy** - How to test Clean Architecture layers
2. **Data layer testing** - GORM, SQLite, entity transformations
3. **Biz layer testing** - Mocking repos, testing business logic
4. **Service layer testing** - Mocking use cases, proto mapping
5. **Table-driven tests** - Structure and patterns
6. **Mocking with testify** - Creating and using mocks
7. **Test helpers** - Setup functions, valid objects
8. **Running and validating tests** - make test, coverage

## Step 2: Provide Guidance

Based on selection, provide detailed explanation from the relevant reference file.

**Include:**
- Conceptual overview
- Code examples from symbol-service
- Common pitfalls
- Best practices
- Related references

## Step 3: Offer Examples

Show real examples from the workspace:
- Point to specific test files
- Highlight key patterns
- Explain why they work

## Step 4: Answer Follow-Up Questions

Allow user to ask follow-up questions about the guidance provided.
</process>

<success_criteria>
- [ ] Guidance request understood
- [ ] Appropriate references loaded
- [ ] Clear explanation provided
- [ ] Code examples included
- [ ] User understands the pattern
</success_criteria>