# Decision Trees

Reference guide for key decisions during Unit Work execution.

## When to Checkpoint

```
After completing a unit of work:
                    |
+-----------------------------------------------+
| Did all automated verification pass?           |
|   NO  -> Fix issues, do NOT checkpoint         |
|   YES |                                        |
+-----------------------------------------------+
                    |
+-----------------------------------------------+
| What type of code was changed?                 |
|   Backend/API only -> High confidence possible |
|   UI involved      -> Lower confidence ceiling |
|   Data migration   -> Requires extra scrutiny  |
+-----------------------------------------------+
                    |
+-----------------------------------------------+
| Calculate confidence:                          |
|   Start at 100%                               |
|   - Subtract 5% for each untested edge case   |
|   - Subtract 20% if UI layout changes         |
|   - Subtract 10% if complex state management  |
|   - Subtract 15% if external API integration  |
+-----------------------------------------------+
                    |
+-----------------------------------------------+
| Confidence >= 95%?                             |
|   YES -> Checkpoint and continue to next unit  |
|   NO  -> Checkpoint and PAUSE for human review |
+-----------------------------------------------+
```

## When to Ask User vs Decide Autonomously

```
During implementation, agent encounters a decision:
                    |
+-----------------------------------------------+
| Is this decision covered by the spec?          |
|   YES -> Follow spec, decide autonomously      |
|   NO  |                                        |
+-----------------------------------------------+
                    |
+-----------------------------------------------+
| Is this a pure implementation detail?          |
| (variable naming, loop vs map, file org)       |
|   YES -> Decide autonomously, follow codebase  |
|   NO  |                                        |
+-----------------------------------------------+
                    |
+-----------------------------------------------+
| Does this affect architecture or UX?           |
|   YES -> STOP and ask user                     |
|   NO  |                                        |
+-----------------------------------------------+
                    |
+-----------------------------------------------+
| Could this decision be wrong and hard to fix?  |
|   YES -> STOP and ask user                     |
|   NO  -> Decide autonomously, note in checkpoint|
+-----------------------------------------------+
```

## When to Use Each Memory Operation

### Agent Needs Information

```
+-----------------------------------------------+
| What do you need?                              |
+-----------------------------------------------+
| "Where is X located?"                          |
|   -> recall --budget low                       |
+-----------------------------------------------+
| "How does X work?"                             |
|   -> recall --budget mid --include-chunks      |
+-----------------------------------------------+
| "How do X and Y interact?"                     |
|   -> recall --budget high --include-chunks     |
+-----------------------------------------------+
| "Why was X designed this way?"                 |
|   -> reflect (uses disposition for reasoning)  |
+-----------------------------------------------+
| "Should I do X or Y for this new feature?"     |
|   -> reflect with --context describing decision|
+-----------------------------------------------+
```

### Agent Discovered Something

```
+-----------------------------------------------+
| What did you discover?                         |
+-----------------------------------------------+
| File location/purpose                          |
|   -> retain --async --doc-id "feature-name"    |
+-----------------------------------------------+
| Gotcha/quirk that caused issues                |
|   -> retain --async (high priority narrative)  |
+-----------------------------------------------+
| Architectural pattern                          |
|   -> retain --async                            |
+-----------------------------------------------+
| Decision rationale                             |
|   -> retain --async with PR/discussion ref     |
+-----------------------------------------------+
| Verification blind spot (human found bug)      |
|   -> retain --async (CRITICAL for future)      |
+-----------------------------------------------+
```

## Which Verification Subagent to Use

See [verification-flow.md](./verification-flow.md#which-verification-subagent-to-use) for the complete decision tree.

## Bug Discovery Decision

```
Bug discovered during implementation:
                    |
+-----------------------------------------------+
| Is this bug critical and blocking?             |
|   YES -> Auto-fix, create checkpoint           |
+-----------------------------------------------+
                    |
+-----------------------------------------------+
| Is this a medium-severity bug?                 |
|   YES -> Note in checkpoint, don't fix         |
|         (Avoid drive-by fixes)                 |
+-----------------------------------------------+
                    |
+-----------------------------------------------+
| Is this a minor bug or code smell?             |
|   YES -> Ignore, stay focused on spec          |
+-----------------------------------------------+
```

## Refactor Discovery Decision

```
Refactoring opportunity discovered:
                    |
+-----------------------------------------------+
| Does this refactor block the current work?     |
|   YES -> Minimal fix only, note for future     |
+-----------------------------------------------+
                    |
+-----------------------------------------------+
| Is this unrelated to current feature?          |
|   YES -> Note as tech debt, do not execute     |
+-----------------------------------------------+
```
