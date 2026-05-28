# agents integration

Connecting epub CLI with the agents workspace for work capture.

## workspace structure

```
~/.agents/
├── AGENTS.md           # global agent instructions
├── references/         # design references, audits
│   ├── web/
│   │   └── {project}/
│   │       └── AUDIT.md
│   └── ios/
├── plans/              # implementation plans
├── sessions/           # session logs
├── hooks/              # automation scripts
└── skills/             # skill definitions

~/Developer/{project}/.agents/
├── AGENTS.md           # project-specific instructions
├── references/         # project references
└── plans/              # project plans
```

## digest command

convert workspace content to epub:

```bash
# digest all .agents content from last week
epub agents digest --since 7d

# digest specific project
epub agents digest --project ~/Developer/arbor-xyz

# filter by type
epub agents digest --type references
epub agents digest --type plans

# dry run (list without creating)
epub agents digest --dry-run
```

## artifact types

| type | source | epub grouping |
|------|--------|---------------|
| reference | `references/**/*.md` | `agents/{source}/references.epub` |
| plan | `plans/**/*.md` | `agents/{source}/plans.epub` |
| audit | `**/AUDIT.md` | `agents/{source}/audits.epub` |
| other | `*.md` (misc) | `agents/{source}/misc.epub` |

## hooks integration

### session-end hook

automatically digest work when session ends:

```bash
#!/bin/bash
# ~/.agents/hooks/session-end.sh

# digest recent work
cd ~/Developer/utils/epub
./bin/run.js agents digest --since 24h --quiet

# sync if device available
./bin/run.js device sync --ip 10.0.0.61 2>/dev/null || true
```

### daily digest hook

aggregate daily work:

```bash
#!/bin/bash
# run via cron at end of day

cd ~/Developer/utils/epub
./bin/run.js agents digest --since 24h
./bin/run.js device sync --ip 10.0.0.61 2>/dev/null || \
  echo "X4 not available - sync manually"
```

## cron setup

```bash
# edit crontab
crontab -e

# add daily digest at 6pm
0 18 * * * cd ~/Developer/utils/epub && ./bin/run.js agents digest --since 24h

# add morning feed sync at 6am
0 6 * * * cd ~/Developer/utils/epub && ./bin/run.js feed sync
```

## x4 folder mapping

| source | x4 path |
|--------|---------|
| ~/.agents/references | `/agents/global/references.epub` |
| ~/.agents/plans | `/agents/global/plans.epub` |
| ~/Developer/arbor-xyz/.agents | `/agents/arbor-xyz/` |

## content filtering

### by recency

```bash
# last 24 hours
epub agents digest --since 24h

# last week
epub agents digest --since 7d

# since specific date
epub agents digest --since 2025-01-01
```

### by type

```bash
# only references and audits
epub agents digest --type references

# only plans
epub agents digest --type plans
```

### by project

```bash
# specific project only
epub agents digest --project ~/Developer/arbor-xyz

# multiple projects
epub agents digest \
  --project ~/Developer/arbor-xyz \
  --project ~/Developer/koto-xyz
```

## session-summary.sh integration

the existing `~/.agents/hooks/session-summary.sh` generates:
- semantic summary of work done
- git diff stats
- recent commits
- linear issue context

epub agents digest can consume this output for richer digests.

## troubleshooting

| issue | cause | fix |
|-------|-------|-----|
| no artifacts found | wrong path or filter | check --project path |
| empty epub | markdown conversion failed | check file encoding |
| missing project | .agents dir doesn't exist | create .agents/ in project |
| hook not running | not executable | `chmod +x hook.sh` |
