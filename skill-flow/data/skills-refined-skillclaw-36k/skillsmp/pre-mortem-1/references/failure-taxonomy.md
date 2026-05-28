# Failure Taxonomy for Spec Simulation

Comprehensive catalog of failure modes to check during simulation.

---

## Category 1: Interface Mismatch

**Description**: What the spec says vs what the system actually does.

| Failure Mode | Detection Question | Enhancement Pattern |
|--------------|-------------------|---------------------|
| Wrong JSON schema | "What does the actual output look like?" | Extract schema from code |
| Missing fields | "What fields are we assuming exist?" | Document all expected fields |
| Different types | "Is this a string or enum?" | Add type constraints |
| Versioning issues | "What if API version changes?" | Add version handling |

**Simulation Prompt**: "What if I actually run this command right now and compare output to spec?"

---

## Category 2: Timing & Performance

**Description**: Operations take longer or behave differently under load.

| Failure Mode | Detection Question | Enhancement Pattern |
|--------------|-------------------|---------------------|
| Timeout | "What if this takes 10x longer?" | Per-operation timeouts |
| Race condition | "What if two requests overlap?" | Add locking/ordering |
| Resource exhaustion | "What if we hit rate limits?" | Add backoff/retry |
| Cascading delays | "What if dependency is slow?" | Add circuit breakers |

**Simulation Prompt**: "What happens if I run this during peak load with degraded network?"

---

## Category 3: Error Handling

**Description**: What happens when things go wrong.

| Failure Mode | Detection Question | Enhancement Pattern |
|--------------|-------------------|---------------------|
| Unclear error message | "Can user understand this?" | Add actionable messages |
| Missing recovery | "What does user do after error?" | Add recovery steps |
| Silent failure | "How do we know this failed?" | Add explicit error states |
| Partial failure | "What if step 3 of 5 fails?" | Add checkpoint/resume |

**Simulation Prompt**: "What if every external call fails? What does the user see?"

---

## Category 4: Safety & Security

**Description**: Dangerous operations without adequate protection.

| Failure Mode | Detection Question | Enhancement Pattern |
|--------------|-------------------|---------------------|
| Missing confirmation | "Can this delete prod data?" | Add explicit confirm gate |
| Unclear severity | "Does user know this is dangerous?" | Add visual safety levels |
| No rollback | "What if we need to undo?" | Document rollback procedure |
| Privilege escalation | "Can this exceed permissions?" | Add permission checks |

**Simulation Prompt**: "What's the worst thing a user could do by accident?"

---

## Category 5: User Experience

**Description**: How users interact with the system.

| Failure Mode | Detection Question | Enhancement Pattern |
|--------------|-------------------|---------------------|
| Skipped instructions | "What if user doesn't read?" | Put warnings before actions |
| Confusing flow | "Is the next step obvious?" | Add explicit next actions |
| Missing feedback | "Does user know it's working?" | Add progress indicators |
| Information overload | "Is this scannable?" | Limit to 2-3 sentences |

**Simulation Prompt**: "What if the user is stressed and just wants to copy-paste?"

---

## Category 6: Integration Points

**Description**: Interactions with external systems.

| Failure Mode | Detection Question | Enhancement Pattern |
|--------------|-------------------|---------------------|
| Dependency unavailable | "What if API is down?" | Add fallback behavior |
| Changed behavior | "What if upstream updates?" | Version pin dependencies |
| Auth failure | "What if token expires?" | Add re-auth flow |
| Data format change | "What if schema evolves?" | Add schema validation |

**Simulation Prompt**: "What if every external system is having a bad day?"

---

## Category 7: State Management

**Description**: Keeping track of where we are.

| Failure Mode | Detection Question | Enhancement Pattern |
|--------------|-------------------|---------------------|
| Lost state | "What if session ends mid-operation?" | Add checkpointing |
| Inconsistent state | "What if DB and cache differ?" | Add reconciliation |
| Stale state | "What if data changed since read?" | Add refresh/optimistic locking |
| Orphaned resources | "What if create succeeds but record fails?" | Add cleanup procedures |

**Simulation Prompt**: "What if power goes out halfway through?"

---

## Category 8: Documentation Gap

**Description**: Spec doesn't match reality.

| Failure Mode | Detection Question | Enhancement Pattern |
|--------------|-------------------|---------------------|
| Outdated example | "Does this actually work?" | Test all examples |
| Missing prerequisite | "What else needs to be true?" | Document prerequisites |
| Implicit assumption | "What am I assuming is already done?" | Make assumptions explicit |
| Wrong version | "Does this work on current version?" | Add version requirements |

**Simulation Prompt**: "Could a new team member follow this spec from scratch?"

---

## Category 9: Tooling & CLI

**Description**: Command-line and tool behavior.

| Failure Mode | Detection Question | Enhancement Pattern |
|--------------|-------------------|---------------------|
| Different flags | "Are these the actual flags?" | Verify against --help |
| Path issues | "What if running from different dir?" | Use absolute paths |
| Missing tools | "Is this tool installed?" | Add tool prerequisites |
| Output format varies | "Is output consistent?" | Parse defensively |

**Simulation Prompt**: "What if I run this on a fresh machine?"

---

## Category 10: Operational

**Description**: Running in production.

| Failure Mode | Detection Question | Enhancement Pattern |
|--------------|-------------------|---------------------|
| No audit trail | "Can we investigate later?" | Add structured logging |
| Missing metrics | "How do we know it's healthy?" | Add observability |
| No runbook | "What do we do at 2 AM?" | Add troubleshooting guide |
| Unclear ownership | "Who gets paged?" | Add escalation path |

**Simulation Prompt**: "What if this breaks on Sunday at 3 AM?"

---

## Using This Taxonomy

During simulation, walk through each category:

```markdown
## Iteration N: [Category Name]

**Failure mode checked**: [Specific mode from table]
**Question asked**: [Detection question]
**Finding**: [What we discovered]
**Enhancement**: [Concrete spec change]
```

Not every category will yield findings for every spec. Focus on categories relevant to your spec's domain.
