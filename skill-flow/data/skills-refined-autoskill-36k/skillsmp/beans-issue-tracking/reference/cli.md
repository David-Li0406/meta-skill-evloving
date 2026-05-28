# Beans CLI Reference

## Creating Beans

```bash
beans create "Title" -t task -s todo
beans create "Title" -t task -d "Description"
beans create "Title" -t task --parent <parent-id>
beans create "Title" --tag discovered -t task -s todo
```

## Updating Beans

```bash
beans update <id> -s in-progress
beans update <id> -s completed
beans update <id> -s scrapped
beans update <id> --parent <id>
beans update <id> --blocking <id>
```

## Listing & Filtering

```bash
beans list --ready                    # Not blocked, ready to start
beans list -s in-progress             # Currently active
beans list -p high,critical           # By priority
beans list -t bug,feature             # By type
beans list -S "search term"           # Search
beans list --tag security             # By tag
beans list --is-blocked               # Cannot start (blocked)
beans list --has-blocking             # Blocks others
```

## Viewing

```bash
beans show <id>                       # Full details
beans roadmap                         # High-level view
```

## Maintenance

```bash
beans check                           # Find issues (cycles, orphans)
beans check --fix                     # Auto-fix issues
beans archive                         # Clean up completed
```

## Recovery After Context Loss

1. Find active work: `beans list -s in-progress`
2. View details: `beans show <id>`
3. Resume from checklist in bean file
