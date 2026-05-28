<overview>
Command reference for the `bd` (beads) CLI used by Layton for state operations.
</overview>

<creating_beads>
**Track external item:**

```bash
bd create "JIRA-1234: blocking release" -t task -p 2 -l watching,jira,layton --json
```

Output:

```json
{"id": "beads-abc", "title": "JIRA-1234: blocking release", "labels": ["watching", "jira", "layton"]}
```

</creating_beads>

<querying_beads>

| Query | Command |
| --- | --- |
| Watched items | `bd list --label watching --json` |
| Current focus | `bd list --label focus --json` |
| All Layton beads | `bd list --label layton --json` |
| Ready work | `bd ready --json` |

</querying_beads>

<updating_beads>
**Add label:**

```bash
bd update <id> --add-label <label> --json
```

**Remove label:**

```bash
bd update <id> --remove-label <label> --json
```

</updating_beads>

<closing_beads>

```bash
bd close <id> --reason "..." --json
```

</closing_beads>

<label_conventions>

| Label | Purpose |
| --- | --- |
| `layton` | Namespace - all Layton-managed beads |
| `watching` | Items user wants tracked |
| `focus` | Current work item (only one) |
| `jira`, `github`, etc. | Source system |

</label_conventions>
