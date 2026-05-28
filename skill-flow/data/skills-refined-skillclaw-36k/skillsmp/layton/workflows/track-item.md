<workflow name="track-item">
<required_reading>
**Read if unfamiliar with bd commands:**
1. references/beads-commands.md - bd CLI reference
</required_reading>

<objective>Add an item to Layton's attention list.</objective>

<steps>
1. Parse user request for: item ID, source system, context
2. Create bead using: `bd create "<ID>: <context>" -t task -p 2 -l watching,<source>,layton --json`
   where `<ID>` is external identifier (e.g., JIRA-1234), `<context>` is user context, and `<source>` is source system label
3. Confirm to user with bead ID for future reference
</steps>

<examples>
User: "Track JIRA-1234, it's blocking the release"
```bash
bd create "JIRA-1234: blocking release" -t task -p 2 -l watching,jira,layton --json
```

User: "Keep an eye on PR 847"

```bash
bd create "PR-847: user wants to monitor" -t task -p 2 -l watching,github,layton --json
```

</examples>

<success_criteria>

- Bead created with `watching` and `layton` labels
- User received confirmation with bead ID
</success_criteria>
</workflow>
