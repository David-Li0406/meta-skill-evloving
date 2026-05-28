---
name: refactoring-assistant
description: Use this skill when you need to guide refactoring decisions and improve large-scale codebases, especially for legacy system modernization and technical debt management.
---

# Refactoring Assistant

> **Language**: [English](../../../../../skills/claude-code/refactoring-assistant/SKILL.md) | 简体中文 | 繁體中文

**Version**: 2.0.0  
**Last Updated**: 2026-01-21  
**Scope**: Claude Code Skills

---

## Purpose

This skill provides a decision framework for refactoring and rewriting, large-scale refactoring patterns, and technical debt management. Strategies are divided into three levels: tactical (day-to-day), strategic (architecture), and safety (legacy code).

---

## Quick Reference (YAML Compressed Format)

```yaml
# === Decision: Refactor vs Rewrite ===
decision_tree:
  - q: "Is the code running in production?"
    n: "→ Consider rewriting (lower risk)"
    y: next
  - q: "Do you understand the functionality of the code?"
    n: "→ Write feature tests first"
    y: next
  - q: "Is test coverage >60%?"
    n: "→ Add tests first"
    y: next
  - q: "Is the core architecture fixable?"
    n: "→ Strangler Fig pattern"
    y: "→ Incremental refactoring ✓"

comparison_matrix:
  favor_refactor: [large codebases, good tests, business critical, team familiarity, sound architecture, time constraints, low risk]
  favor_rewrite: [small standalone, no tests, tolerable downtime, unfamiliarity, flawed architecture, ample time, higher risk]

# === Warning: Second System Effect ===
rewrite_antipatterns:
  - "Adding features that weren't originally present"
  - "Over-abstracting for future flexibility"
  - "Ignoring lessons from the existing system"
quote: "The second system is the most dangerous system a person ever designs. — Fred Brooks"

# === Tactical Strategies: Everyday Refactoring ===
tactical:
  preparatory_refactoring:
    definition: "Adjust structure before adding features to make changes easier"
    quote: "Make the change easy (this may be hard), then do the easy change. — Kent Beck"
    when: [functionality is blocked, reduce friction, upcoming changes]
    workflow:
      1: "Identify the change to be made"
      2: "Identify what makes the change difficult"
      3: "Refactor to make the change easier"
      4: "Make that (now easier) change"
    principles:
      - "Separate preparatory refactoring from feature submissions"
      - "Maintain passing tests at every step"
      - "Do not mix refactoring with feature work"

  boy_scout_rule:
    definition: "Leave the code cleaner than you found it (opportunistic refactoring)"
    quote: "Leave the campground cleaner than you found it. — Robert C. Martin"
    when: [any maintenance, bug fixes, feature additions, combating entropy]
    guidelines:
      - "Make only small improvements (minutes, not hours)"
      - "Do not change behavior"
      - "Do not break existing tests"
      - "Keep the scope within the current task"
    examples:
      - "Rename confusing variables"
      - "Extract several lines of code into a well-named method"
      - "Remove dead code"
      - "Add clarifying comments"
    antipatterns:
      - "Turning bug fixes into large refactorings"
      - "Refactoring unrelated code"
      - "Modifying without test coverage"
      - "Scope creep beyond the original task"

  red_green_refactor:
    definition: "TDD refactoring phase"
    duration: "5-15 minutes per cycle"
    scope: "Single method/class"
    techniques: [extract method, rename, inline variable, replace magic numbers]
    reference: "→ See TDD standards"

# === Strategic Strategies: Architectural Refactoring ===
strategic:
  strangler_fig:
    definition: "Gradually route functionality to a new system, incrementally replacing the old system"
    origin: "Named after the strangler fig tree"
    phases:
      1_intercept: "Request → Facade → Old System (100%)"
      2_migrate: "Request → Facade → [New System (functionality), Old System (rest)]"
      3_complete: "Request → New System (100%) [Old System offline]"
    checklist:
      - "Identify interception points"
      - "Establish an event capture layer"
      - "Implement the first feature in the new system"
      - "Gradually route traffic"
      - "Monitor and compare"
      - "Take the old system offline"

  anti_corruption_layer:
    definition: "A translation layer to prevent legacy models from polluting the new system"
    origin: "Eric Evans, Domain-Driven Design (2003)"
    when:
      - "New and old systems must coexist and interact"
      - "Legacy systems have chaotic domain models"
      - "Protect the bounded context of the new system"
    components:
      facade: "Simplify complex legacy interfaces"
      adapter: "Transform legacy data into new domain models"
      translator: "Map legacy terms to a common language"
    checklist:
      - "Define clear ACL interfaces"
      - "Map legacy entities to new models"
      - "Handle data format transformations"
      - "Implement error translations"
      - "Add logging for debugging"
      - "Thoroughly test ACL isolation"
    vs_strangler:
      strangler: "Goal is to replace legacy"
      acl: "Goal is to coexist with legacy"

  branch_by_abstraction:
    steps:
      1: "Client → Abstraction (interface) → Old Implementation"
      2: "Client → Abstraction → [Old Implementation, New Implementation (switch)]"
      3: "Client → New Implementation [Old Implementation removed]"
    principles: [all changes in the main branch, feature toggles, coexistence during transition]

  parallel_change:
    aka: "Expand-Migrate-Contract"
    phases:
      expand: "Add new alongside old, new code uses new, old still operates"
      migrate: "Update all clients to use new, validate, data migration"
      contract: "Remove old, clean up, update documentation"

# === Safety Strategies: Legacy Code ===
safety:
  legacy:
    definition: "Code without tests (regardless of age)"
    dilemma: "Safe modifications require tests → Adding tests requires modifying code"
    solution: "Use safe techniques to add tests first"

  characterization_tests:
    purpose: "Capture existing behavior (not verifying correctness)"
    process:
      1: "Call the code to understand"
      2: "Write assertions that are expected to fail"
      3: "Execute, observe actual results"
      4: "Update assertions to match actual behavior"
      5: "Repeat until covering behaviors needing modification"
    principle: "Record what the code does, not what it should do"

  scratch_refactoring:
    definition: "Refactor for understanding, discard all changes"
    workflow:
      1: "Create a probe branch (or git stash)"
      2: "Refactor boldly to understand"
      3: "Document what you learn"
      4: "Discard changes (git reset --hard)"
      5: "Apply learning to write feature tests"
    when: [code is too complex, no documentation, need to quickly build a mental model]
    principle: "The goal is understanding, not clean code"

  seams:
    definition: "Places where behavior can be changed without editing code"
    object: "Through polymorphic overrides (injecting test doubles)"
    preprocessing: "Compile-time replacements (macros)"
    link: "Link-time replacements (DI, module replacements)"

  sprout_wrap:
    sprout_method: "New logic → Create new method, call from old"
    sprout_class: "New logic evolves independently → New class"
    wrap_method: "Add behavior before and after → Rename original method, create wrapper"
    wrap_class: "Decorate existing → Decorator pattern"
    principle: "New code uses TDD; legacy code remains unchanged until tested"

# === Database: Refactoring ===
db_expand_contract:
  expand: "Add new columns/tables, application writes to both, can safely roll back"
  migrate: "Copy data, validate consistency, application reads from new"
  contract: "Confirm old is unused, remove old, clean up dual writes"

db_scenarios:
  rename_column: {strategy: "Add→Migrate→Delete", risk: medium}
  split_table: {strategy: "New table + foreign key→Migrate→Adjust", risk: high}
  merge_tables: {strategy: "New table→Merge→Switch", risk: high}
  change_datatype: {strategy: "New column→Transform→Switch", risk: medium}
  add_not_null: {strategy: "Fill defaults→Add constraint", risk: low}

# === Workflow: Safe Refactoring ===
before: [define success criteria, "coverage >80%", clean working directory, create branch, communicate with team]
during: [one small change at a time, test after each change, revert on failure, commit frequently, no new features]
after: [all tests pass, measurably better, documentation updated, team reviewed, no new features]

# === Metrics ===
code_quality:
  cyclomatic_complexity: "Each function <10"
  cognitive_complexity: "Lower is better"
  coupling: "Reduce"
  cohesion: "Increase"
  duplication: "<3%"

test_quality:
  coverage: "≥80%, not reduced"
  speed: "Faster after refactoring"
  flaky_count: "Reduced"

# === Technical Debt Management ===
quadrant: # Martin Fowler
  prudent_deliberate: "We know this is debt"
  reckless_deliberate: "No time for design"
  prudent_inadvertent: "Now we know how to do it"
  reckless_inadvertent: "What is layering?"

priority:
  high: {criteria: "Blocking development, frequent errors", action: "Address immediately"}
  medium: {criteria: "Slowing development, increasing complexity", action: "Plan for next iteration"}
  low: {criteria: "Minor issues, localized impact", action: "Address when possible"}

tracking:
  fields: [description, impact, estimated workload, ignore risks, related code]

# === Decision Matrix Summary ===
decision_matrix:
  - {strategy: "Preparatory Refactoring", scale: "small", risk: "low", use: "Reduce friction in feature development"}
  - {strategy: "Boy Scout Rule", scale: "very small", risk: "low", use: "Continuous debt repayment"}
  - {strategy: "Red-Green Refactor", scale: "small", risk: "low", use: "TDD development cycle"}
  - {strategy: "Strangler Fig", scale: "large", risk: "medium", use: "System replacement"}
  - {strategy: "Anti-Corruption Layer", scale: "medium", risk: "low", use: "Coexistence of new and old"}
  - {strategy: "Branch by Abstraction", scale: "large", risk: "medium", use: "Main branch refactoring"}
  - {strategy: "Parallel Change", scale: "medium", risk: "low", use: "Interface/Schema migration"}
  - {strategy: "Characterization Tests", scale: "—", risk: "—", use: "Precondition for legacy refactoring"}
  - {strategy: "Scratch Refactoring", scale: "small", risk: "low", use: "Understanding black box code"}

# === Strategy Selection ===
selection_guide:
  functionality blocked by chaotic code: "Preparatory Refactoring"
  encountering code during bug fixes: "Boy Scout Rule"
  writing new code with TDD: "Red-Green Refactor"
  replacing an entire legacy system: "Strangler Fig"
  integrating legacy without pollution: "Anti-Corruption Layer"
  refactoring shared code in the main branch: "Branch by Abstraction"
  changing widely used interfaces: "Parallel Change"
  handling untested legacy: "Characterization Tests + Scratch Refactoring first"
```

---

## Configuration Detection

### Detection Order

1. Check the "Disabled Skills" section in `CONTRIBUTING.md`
2. Check the "Refactoring Standards" section in `CONTRIBUTING.md`
3. If not found, **default to standard refactoring practices**

---

## Detailed Guide

For complete standards, refer to:
- [Refactoring Standards](../../../core/refactoring-standards.md)

---

## Related Standards

- [Refactoring Standards](../../../core/refactoring-standards.md) - Core standards
- [Test-Driven Development](../../../core/test-driven-development.md) - TDD refactoring phase
- [Code Review Checklist](../../../core/code-review-checklist.md) - Refactoring PR review
- [Check-in Standards](../../../core/checkin-standards.md) - Pre-commit requirements
- [TDD Assistant](../tdd-assistant/SKILL.md) - TDD workflow

---

## Version History

| Version | Date       | Changes |
|---------|------------|---------|
| 2.0.0  | 2026-01-21 | Added tactical strategies (preparatory refactoring, boy scout rule), anti-corruption layer, decision matrix summary. Restructured into tactical/strategic/safety layers. |
| 1.0.0  | 2026-01-12 | Initial release |

---

## License

This skill is published under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

**Source**: [universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)