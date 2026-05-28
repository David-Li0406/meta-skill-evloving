# TDD Skill for Ziku

A comprehensive Test-Driven Development skill for the Ziku programming language project.

## Skill Structure

```
tdd/
├── SKILL.md                          # Main skill content (1,949 words)
├── README.md                         # This file
├── scripts/                          # Utility scripts
│   ├── create_test_file.sh          # Create test files with templates
│   ├── add_golden_test.sh           # Add tests to GoldenTest.lean
│   └── check_test_status.sh         # Quick test status (red/green)
├── references/                       # Detailed documentation
│   └── tdd-patterns.md              # Comprehensive TDD patterns (8,800+ words)
└── examples/                         # Example workflows
    ├── workflow-new-feature.md      # Adding a new language feature
    └── workflow-bug-fix.md          # Fixing bugs with regression tests
```

## Trigger Phrases

This skill activates when users ask to:
- "use TDD"
- "write tests first"
- "test-driven"
- "add a test for"
- "fix bug with TDD"
- "implement using TDD"
- "red-green-refactor"
- Or mention developing features test-first

## What This Skill Provides

### Core TDD Guidance
- Red-Green-Refactor cycle for Ziku
- Test-first feature development workflow
- Regression testing for bug fixes
- Integration with Ziku's golden test infrastructure

### Utility Scripts
- **create_test_file.sh**: Create `.ziku` test files with templates (lambda, let, match, codata, label)
- **add_golden_test.sh**: Automatically add test names to `GoldenTest.lean` lists
- **check_test_status.sh**: Quick red/green status check with visual feedback

### Detailed Patterns (references/)
- Complete red-green-refactor cycle explanation
- Test-first feature development strategies
- Regression testing workflows
- Test organization best practices
- Advanced techniques (triangulation, property-based testing)
- Ziku-specific patterns (codata testing, label/goto testing)
- Common TDD mistakes and solutions

### Example Workflows (examples/)
- **workflow-new-feature.md**: Complete example of adding a `for` loop construct
  - Shows all three phases: parser → inference → evaluation
  - Demonstrates red-green-refactor at each phase
- **workflow-bug-fix.md**: Complete example of fixing a nested label/goto bug
  - Shows reproduction, debugging, fixing, and regression prevention

## Quick Start

### Using Scripts

First, ensure scripts are executable:
```bash
chmod +x .claude/skills/tdd/scripts/*.sh
```

Then use them from the project root:
```bash
# Create a new test
.claude/skills/tdd/scripts/create_test_file.sh parser my_test lambda

# Add to test list
.claude/skills/tdd/scripts/add_golden_test.sh parser my_test

# Check test status
.claude/skills/tdd/scripts/check_test_status.sh

# Check specific category with custom timeout
.claude/skills/tdd/scripts/check_test_status.sh parser 60
```

### Basic TDD Cycle

1. **Red**: Write failing test
   ```bash
   create_test_file.sh ir-eval new_feature
   # Edit tests/golden/ir-eval/new_feature.ziku
   add_golden_test.sh ir-eval new_feature
   lake test  # Should fail
   ```

2. **Green**: Make it pass
   ```bash
   # Edit implementation files
   lake test  # Should pass
   ```

3. **Refactor**: Improve code
   ```bash
   # Improve code quality
   lake test  # Should still pass
   ```

## Progressive Disclosure

The skill uses progressive disclosure for efficient context management:

1. **Metadata**: Always loaded, provides skill triggering
2. **SKILL.md**: Loaded when skill triggers, covers essential workflow
3. **References**: Loaded as needed, provides deep patterns and techniques
4. **Examples**: Loaded as needed for specific workflow guidance

## Design Philosophy

- **Imperative/infinitive form**: All instructions use verb-first language
- **Third-person description**: Frontmatter uses "This skill should be used when..."
- **Lean main content**: SKILL.md stays focused, details in references
- **Practical utilities**: Scripts automate repetitive tasks
- **Real examples**: Complete workflows show actual usage

## Integration with Ziku

This skill is specifically tailored for Ziku's infrastructure:
- **Golden tests**: Leverages automatic `.golden` file generation
- **Three test categories**: Parser, inference, and IR evaluation
- **Test organization**: Follows `tests/GoldenTest.lean` structure
- **Build system**: Integrates with `lake test` and `lake build`
- **Conventions**: Follows Ziku's commit message format and testing patterns

## Validation Status

- [x] Frontmatter has name and description
- [x] Description uses third person with specific triggers
- [x] SKILL.md body uses imperative form
- [x] Scripts are cross-platform (macOS/Linux)
- [x] References provide detailed patterns
- [x] Examples show complete workflows
- [x] Progressive disclosure implemented
- [x] All referenced files exist

## Version

**v1.1.0** - Cross-platform improvements
- Fixed sed portability for macOS/Linux
- Improved check_test_status.sh with configurable timeout
- Removed time estimates from examples

## Maintenance

To update this skill:
1. Keep SKILL.md lean and focused
2. Add detailed patterns to references/tdd-patterns.md
3. Add new example workflows to examples/
4. Update scripts as Ziku's test infrastructure evolves
5. Increment version in SKILL.md frontmatter

## Testing the Skill

To verify the skill works:
1. Ask Claude: "Help me add a test for X using TDD"
2. Ask Claude: "Let's implement Y test-first"
3. Ask Claude: "I found a bug, let's fix it with TDD"

The skill should activate and guide through the appropriate workflow.
