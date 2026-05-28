# Mutation Testing for Python

A Claude Code skill that applies mutation testing analysis to Python codebases using mutmut.

## What is Mutation Testing?

Mutation testing evaluates the quality of your tests by introducing small bugs (mutations) into your code and checking if your tests catch them. A high mutation score means your tests are effective at detecting real bugs.

**The key question:** "If I introduced a bug here, would my tests catch it?"

## When to Use This Skill

This skill helps you:

- **Analyze branch changes**: Review code on a feature branch to identify weak tests
- **Verify TDD effectiveness**: Ensure your tests actually verify behavior, not just execution
- **Strengthen test suites**: Find gaps in test coverage that code coverage metrics miss
- **Validate refactoring**: Confirm that refactoring didn't weaken your test suite
- **Find edge cases**: Identify missing boundary value tests and edge case handling

## Installation

### Project-Level (Shared with Team)

```bash
mkdir -p .claude/skills
cp -r path/to/mutation-testing-python .claude/skills/
```

Add to your project's `.gitignore` if you don't want to commit skills:
```
.claude/skills/
```

Or commit to share with your team:
```bash
git add .claude/skills/mutation-testing-python
git commit -m "Add mutation testing skill"
```

### Personal (Across All Projects)

```bash
mkdir -p ~/.claude/skills
cp -r path/to/mutation-testing-python ~/.claude/skills/
```

## Usage

### Manual Invocation

```bash
claude code
> /mutation-testing-python
```

### Automatic Activation

Claude Code will automatically activate this skill when you:

- Review Python files on a branch
- Discuss test effectiveness in Python projects
- Ask about strengthening Python tests
- Mention mutation testing for Python code

### Example Workflow

**1. After implementing a feature:**

```
You: I've just implemented a calculate_discount function. Can you review the tests?

Claude: [Activates mutation-testing-python skill]
        Let me analyze the tests for potential surviving mutants...

        Found potential weak test:
        - The test uses identity value (discount_rate=0) which makes
          multiplication and division indistinguishable.

        Suggested strengthening:
        def test_calculate_discount():
            assert calculate_discount(100, 0.2) == 20  # 100 * 0.2 != 100 / 0.2
```

**2. Reviewing a branch:**

```
You: Review the changes on my feature branch

Claude: [Activates mutation-testing-python skill]
        Analyzing changed files: src/auth.py, src/validators.py

        In auth.py:42 - Boundary condition in age >= 18:
        - Missing test for exactly age=18 (boundary value)
        - Would survive mutant: age > 18

        Recommended test:
        def test_is_adult_at_boundary():
            assert is_adult(18) is True  # Would catch >= → > mutation
```

## Integration with mutmut

This skill teaches mutation testing concepts and can guide integration with mutmut:

### Install mutmut

```bash
pip install mutmut
```

### Configure (pyproject.toml)

```toml
[tool.mutmut]
paths_to_mutate = "src/"
backup = false
runner = "pytest -x"
tests_dir = "tests/"
```

### Run mutation testing

```bash
# Run all mutations
mutmut run

# View results
mutmut results

# Show surviving mutants
mutmut show survived

# Generate HTML report
mutmut html
```

### Workflow with Claude Code

1. Run `mutmut run` to generate mutation report
2. Ask Claude Code to analyze surviving mutants:
   ```
   You: mutmut found 5 surviving mutants in src/auth.py.
        Can you help me strengthen the tests?

   Claude: [Uses mutation-testing-python skill to analyze and suggest improvements]
   ```

## What This Skill Provides

### Mental Mutation Analysis

The skill teaches you to mentally apply mutations without running mutmut:

- **Arithmetic mutations**: +, -, *, /, //, %, **
- **Comparison mutations**: <, <=, >, >=, ==, !=
- **Boolean mutations**: and, or, not
- **Identity mutations**: is, is not
- **Membership mutations**: in, not in
- **Collection mutations**: Empty lists, dicts, sets

### Systematic Review Process

1. Identify changed code on branch
2. Generate mental mutants for each function
3. Verify tests would catch each mutant
4. Document findings and strengthen weak tests

### Python-Specific Patterns

- Dictionary operations (`.get()` vs `[]`)
- None handling (`is None` vs `== None`)
- List comprehensions with filters
- Exception handling
- Context managers
- Type-specific mutations (str, list, dict, set)

### Concrete Examples

The skill includes 10+ concrete Python examples showing:

- Weak tests that would miss mutants
- Strong tests that would catch mutants
- Why specific test values matter
- How to avoid common pitfalls

## Key Concepts

### Mutation Operators

The skill covers all major Python mutation operators:

| Category | Examples |
|----------|----------|
| Arithmetic | `+` → `-`, `*` → `/`, `//` → `/`, `%` → `*`, `**` → `*` |
| Comparison | `<` → `<=`, `>=` → `>` |
| Boolean | `and` → `or`, `not a` → `a` |
| Identity | `is` → `==`, `is None` → `== None` |
| Membership | `in` → `not in` |
| Collections | `[1, 2]` → `[]`, `{}` → `{None: None}` |

### Test Strengthening Patterns

1. **Boundary value testing**: Test exact boundary conditions
2. **Avoid identity values**: Use values that distinguish operators (0, 1)
3. **Test both branches**: Verify all logical branches
4. **Verify side effects**: Use mock assertions
5. **Test None explicitly**: Cover None and non-None paths
6. **Test empty collections**: Verify behavior with empty lists/dicts

## Attribution

This skill is based on mutation testing concepts and patterns pioneered by Paul Hammond and the mutation testing community. Adapted for Python and mutmut by the Claude Code community.

## Related Skills

- `test-desiderata`: Analyze test quality using Kent Beck's framework
- `g-plt-increase-coverage`: Increase test coverage systematically
- `g-plt-plan-untested-code`: Plan tests for untested code

## Learn More

- [mutmut documentation](https://mutmut.readthedocs.io/)
- [Mutation Testing: A Tale of Two Suites](https://buttondown.com/hillelwayne/archive/mutation-testing-a-tale-of-two-suites/)
- [Are your tests actually testing anything?](https://blog.sulami.xyz/posts/mutation-testing/) by Paul Hammond

## License

See [LICENSE.txt](LICENSE.txt) for attribution and license information.
