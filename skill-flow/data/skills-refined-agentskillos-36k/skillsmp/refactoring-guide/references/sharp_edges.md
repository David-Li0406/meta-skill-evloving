# Refactoring Guide - Sharp Edges

## Second System Syndrome - The Ambitious Rewrite

### **Id**
second-system-syndrome
### **Severity**
critical
### **Situation**
  Team decides to rewrite the legacy system "properly this time." Version 2 will
  have better architecture, cleaner code, all the features. Two years later,
  the rewrite is still not done, while the legacy system is still running and
  accumulating more fixes the rewrite doesn't have.
  
### **Why**
  Fred Brooks identified this in 1975. Developers who build a successful first
  system are tempted to add all the features they "wish they'd had" in version 2.
  The result is over-engineered, late, and often never ships. Meanwhile, the
  original system keeps accumulating value the rewrite lacks.
  
### **Solution**
  1. Never rewrite from scratch:
     - Use Strangler Fig pattern instead
     - Replace pieces incrementally
     - Keep the system running throughout
  
  2. If you must rebuild a component:
     - Feature freeze the old version first
     - Build new version alongside old
     - Migrate gradually
     - Keep new scope minimal
  
  3. Resist the temptation to "do it right":
     - Copy the quirks that users depend on
     - Maintain backward compatibility
     - Add improvements incrementally after migration
  
### **Symptoms**
  - We'll rewrite it properly this time
  - Rewrite has been ongoing for months/years
  - Legacy system keeps getting patches rewrite lacks
  - Scope keeps expanding
### **Detection Pattern**
rewrite|from scratch|version 2|v2|rebuild|new architecture

## Refactoring Without Tests - Flying Blind

### **Id**
refactoring-without-tests
### **Severity**
critical
### **Situation**
  Developer wants to clean up messy code. There are no tests. They refactor
  anyway, carefully reading the code to understand what it does. They ship.
  A week later, production breaks because an edge case they didn't notice
  was silently changed.
  
### **Why**
  Refactoring means changing structure while preserving behavior. Without tests,
  "preserving behavior" is just hope. You can't be sure the code works the same
  way. Manual testing catches obvious breaks but misses subtle behavior changes.
  
### **Solution**
  1. Write characterization tests first:
     ```python
     # Capture what the code DOES, not what it SHOULD do
     def test_characterization():
         result = legacy_function(input)
         assert result == captured_output  # Whatever it returned
     ```
  
  2. If tests are truly impossible:
     - Use IDE automated refactorings only (proven safe)
     - Make only mechanical, reversible changes
     - Review diff obsessively
     - Have multiple reviewers
  
  3. Consider the risk/reward:
     - Is this refactoring worth the risk?
     - Can you add tests first?
     - Is the code stable enough to leave alone?
  
### **Symptoms**
  - There are no tests but I'll be careful
  - Large refactoring PRs without test changes
  - Bugs appearing in "unchanged" code
  - Fear of touching certain modules
### **Detection Pattern**
no tests|without tests|can't test|untestable

## Mixed Commits - Refactoring + Features Together

### **Id**
mixed-refactoring-features
### **Severity**
high
### **Situation**
  Developer is adding a feature. "While I'm here," they clean up some code,
  rename variables, extract methods. The PR has the feature AND refactoring
  mixed together. Something breaks. Was it the feature? The refactoring?
  Nobody knows without hours of debugging.
  
### **Why**
  Mixing behavior changes (features) with structural changes (refactoring)
  creates debugging nightmares. Git blame becomes useless. Rollback is
  all-or-nothing. Code review is harder because reviewers must track both
  intent and structural changes.
  
### **Solution**
  1. Separate commits always:
     - Commit 1: Refactoring only (no behavior change)
     - Commit 2: Feature only (on clean code)
  
  2. For larger refactoring:
     - Separate PR entirely
     - Merge refactoring first
     - Then feature PR on clean base
  
  3. The test: Would tests change?
     - Refactoring: Tests should NOT change (behavior preserved)
     - Feature: Tests SHOULD change (new behavior)
     - If both happen, you're mixing concerns
  
### **Symptoms**
  - Large PRs with "cleaned up while I was there"
  - Mixed test additions and refactoring
  - Hard-to-review diffs
  - Bugs of unclear origin
### **Detection Pattern**
while I was here|also cleaned up|and refactored

## Phantom Interface - Abstraction Without Need

### **Id**
phantom-interface
### **Severity**
medium
### **Situation**
  During refactoring, developer creates interfaces for everything "for
  testability" or "flexibility." Now there's IUserService with one
  UserServiceImpl. The code is longer, harder to navigate, and the
  flexibility is never used.
  
### **Why**
  Interfaces add indirection. Every time you read the code, you have to
  find the implementation. This is worth it when you have multiple
  implementations or genuine dependency injection needs. It's not worth
  it "just in case."
  
### **Solution**
  1. Don't extract interface until you need it:
     - Multiple implementations? Interface.
     - Test mocking painful? Consider interface.
     - "Might need it someday"? Don't.
  
  2. YAGNI applies to refactoring too:
     - Refactor toward simplicity, not "proper architecture"
     - Add abstraction when you feel pain
     - One implementation = no interface needed
  
  3. If you must have interfaces:
     - Use language features that don't require explicit interfaces
     - Python: duck typing
     - TypeScript: structural typing
     - Go: implicit interfaces
  
### **Symptoms**
  - IFoo + FooImpl everywhere
  - Interfaces with single implementations
  - Factory classes that just call constructors
  - "For testability" interfaces never mocked
### **Detection Pattern**
interface I|Impl|Factory|Provider

## Big Bang Refactoring - The Massive PR

### **Id**
big-bang-refactoring
### **Severity**
high
### **Situation**
  Developer decides to "properly refactor" a module. Three weeks later, they
  have a 3,000-line PR touching 50 files. Review is cursory because nobody
  can truly review that much change. It merges. Bugs trickle in for weeks.
  
### **Why**
  Large changes are impossible to review well. They're impossible to test
  completely. They're hard to roll back because so much is intertwined.
  Each line has a small probability of error; multiply by thousands and
  errors are guaranteed.
  
### **Solution**
  1. Break into many small PRs:
     - One refactoring type per PR (all renames, then all extractions)
     - Or one area per PR (all OrderService changes, then PaymentService)
     - Each PR reviewable in one sitting (< 400 lines)
  
  2. Ship incrementally:
     - Merge each small PR immediately
     - Get feedback on each before continuing
     - Catch problems early
  
  3. Track with Mikado Method:
     - Draw dependency graph of needed changes
     - Work from leaves to root
     - Each leaf is a small, independent PR
  
### **Symptoms**
  - PRs with 1000+ lines
  - "This is part 1 of 5" multi-week refactoring
  - Review comments like "LGTM" on huge diffs
  - Long-lived feature branches
### **Detection Pattern**
large refactoring|big cleanup|refactoring PR

## Refactoring During Crisis - Wrong Time

### **Id**
refactoring-in-production-crisis
### **Severity**
high
### **Situation**
  Production is on fire. Bug is urgent. Developer traces it to messy code.
  "I'll just clean this up while I'm fixing the bug - that'll prevent
  future issues." The fix takes longer. The refactoring introduces a new bug.
  Now there are two fires.
  
### **Why**
  Crisis mode requires focus. Refactoring requires attention to detail and
  thorough testing. These are incompatible. Under pressure, refactoring
  quality drops while risk increases. The minimal fix is the safe fix.
  
### **Solution**
  1. During crisis: Minimal fix only
     - Fix the bug with smallest possible change
     - Add test proving it's fixed
     - Ship immediately
  
  2. After crisis: Refactor properly
     - Schedule refactoring as follow-up
     - Do it with full attention, not under pressure
     - Thorough review and testing
  
  3. The rule:
     - Urgent? Minimal fix.
     - Important but not urgent? Refactor.
     - Never both at once.
  
### **Symptoms**
  - While fixing the bug I also...
  - Mixed bugfix + refactoring PRs under time pressure
  - Hotfixes that include "improvements"
  - New bugs appearing after "simple" fixes
### **Detection Pattern**
hotfix.*refactor|urgent.*clean|while fixing

## Rename Cascade - One Rename Breaks Everything

### **Id**
rename-cascade
### **Severity**
medium
### **Situation**
  Developer renames a function. But it's called from 47 places. Some through
  dynamic dispatch. Some through string references. Some in templates. Some in
  tests. The rename breaks things that the IDE didn't catch.
  
### **Why**
  IDE refactoring tools can't find all references, especially in dynamic
  languages or when names are constructed as strings. Renames that look safe
  can break runtime behavior that static analysis doesn't see.
  
### **Solution**
  1. Before renaming:
     - Search for string references: "functionName"
     - Search in configs, templates, and non-code files
     - Check dynamic calls: getattr, reflection, eval
  
  2. Use parallel change for public APIs:
     - Add new name
     - Mark old as deprecated
     - Migrate callers
     - Remove old after all migrated
  
  3. For internal renames:
     - IDE rename is usually safe
     - Run full test suite
     - Search for string usage
  
### **Symptoms**
  - Breaks that IDE didn't catch
  - Errors in templates or config files
  - Runtime errors from reflection
  - I just renamed it, why is it broken?
### **Detection Pattern**
rename|getattr|reflection|dynamically

## Behavior Change Disguised as Refactoring

### **Id**
behavior-change-as-refactoring
### **Severity**
high
### **Situation**
  Developer "refactors" a function. But the new version handles an edge case
  differently. The change is called "refactoring" but it's actually a behavior
  change. The bug it introduces is blamed on the refactoring, not the behavior
  change.
  
### **Why**
  Refactoring has a specific meaning: change structure, preserve behavior.
  Behavior changes need different scrutiny - new tests, product review,
  communication. Mislabeling lets behavior changes slip through without
  proper review.
  
### **Solution**
  1. Definition check:
     - Are you changing what the code does? → Not refactoring
     - Are you changing how it does it? → Refactoring
     - If tests change behavior assertions → Not refactoring
  
  2. Separate behavior changes explicitly:
     - Refactoring PR (tests unchanged)
     - Then behavior change PR (new tests)
     - Each reviewed appropriately
  
  3. If you find a bug during refactoring:
     - DON'T fix it in the same commit
     - File it, note it, fix it separately
     - Characterization test the bug if needed
  
### **Symptoms**
  - "Refactoring" PRs that add/change tests
  - Unexpected behavior after "simple refactoring"
  - "I just cleaned it up" introducing bugs
  - Edge case differences after refactoring
### **Detection Pattern**
refactor.*fix|clean up.*also|improve.*change

## Losing Institutional Knowledge - Why Was It Like That?

### **Id**
losing-institutional-knowledge
### **Severity**
medium
### **Situation**
  Developer cleans up "weird" code. It looked wrong. Now it's clean.
  A month later, a specific edge case breaks. Turns out the "weird" code
  was handling a vendor quirk, a regulatory requirement, or a customer-
  specific behavior that nobody documented.
  
### **Why**
  Legacy code often looks wrong but is right. It accumulated fixes for
  real-world problems over years. Without understanding WHY it was written
  that way, you can't know if your "improvement" breaks something important.
  
### **Solution**
  1. Before refactoring, ask:
     - Why might this have been written this way?
     - Is there a comment explaining it?
     - Who wrote it and can you ask them?
     - Are there related issues/tickets?
  
  2. Characterization tests capture behavior:
     - Even if you don't understand why, test what it does
     - Now refactoring is safer
  
  3. When you find out why:
     - Add a comment explaining the reason
     - Future developers will thank you
     - Or add a test that documents the edge case
  
### **Symptoms**
  - "This looks wrong" code being cleaned up
  - Bugs in edge cases after "obvious improvements"
  - Long-forgotten issues reappearing
  - Customer complaints after "internal cleanup"
### **Detection Pattern**
looks wrong|weird code|don't know why|strange