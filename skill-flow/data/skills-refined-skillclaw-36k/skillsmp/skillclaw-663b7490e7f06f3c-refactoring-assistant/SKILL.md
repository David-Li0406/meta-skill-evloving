---
name: refactoring-assistant
description: Use this skill when you need to guide refactoring decisions and large-scale code improvements, especially in legacy systems and technical debt management.
---

# Skill body

## Purpose

This skill provides a decision framework for refactoring and rewriting, along with patterns for large-scale refactoring and technical debt management. Strategies are divided into three levels: tactical (daily), strategic (architecture), and safety (legacy code).

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
  favor_refactor: [large codebase, good tests, business critical, team familiarity, sound architecture, time constraints, low risk]
  favor_rewrite: [small standalone, no tests, downtime tolerable, unfamiliar, flawed architecture, ample time, higher risk]

# === Warning: Second System Effect ===
rewrite_antipatterns:
  - "Adding features that weren't originally present"
  - "Over-abstracting for future flexibility"
  - "Ignoring lessons learned from the existing system"
quote: "The second system is the most dangerous system a person will ever design. — Fred Brooks"

# === Tactical Strategies: Daily Refactoring ===
tactical:
  preparatory_refactoring:
    definition: "Adjust the structure before adding new features to make changes easier"
    quote: "Make the change easy (this may be hard), then do that easy change. — Kent Beck"
    when: [feature is blocked, reduce friction, upcoming changes]
    workflow:
      1: "Identify the change to be made"
      2: "Identify what makes the change difficult"
      3: "Refactor to make the change easier"
      4: "Make that (now easier) change"
    principles:
      - "Separate preparatory refactoring from feature commits"
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
      - "Extract a few lines of code into a well-named method"
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
      2_migrate: "Request → Facade → [New System (functionality), Old System (remaining)]"
      3_complete: "Request → New System (100%) [Old System decommissioned]"
    checklist:
      - "Identify interception points"
      - "Establish an event capture layer"
      - "Implement the first feature in the new system"
      - "Gradually route traffic"
      - "Monitor and compare"
      - "Decommission the old system"

  anti_corruption_layer:
    definition: "Prevent legacy system corruption by isolating new systems from old"
```