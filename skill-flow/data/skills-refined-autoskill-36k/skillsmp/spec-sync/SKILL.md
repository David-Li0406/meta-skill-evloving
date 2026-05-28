---
name: spec-sync
description: Synchronize DEV_SPEC.md and split it into chapter-specific files under specs/ directory. Run sync_spec.py to update, then read SPEC_INDEX.md for navigation. Foundation for all spec-based operations. Use when user says "同步规范", "sync spec", or before any spec-dependent task.
metadata:
  category: documentation
  triggers: "sync spec, update spec, 同步规范"
allowed-tools: Bash(python:*) Read
---

# Spec Sync

This skill synchronizes the master specification document (`DEV_SPEC.md`) and splits it into smaller, chapter-specific files stored in the `specs/` directory.

> **This is a prerequisite for all spec-based operations.** Other skills depend on the split spec files to perform their tasks.

---

## How to Use

### Used in dev-workflow (Automatic)

When you trigger dev-workflow (e.g., "下一阶段" or "继续开发"), **spec-sync runs automatically as Stage 1**. No manual action needed.

### Manual Sync (Edge Cases Only)

Only manually run if:
- You edited `DEV_SPEC.md` outside of workflow
- Spec files are corrupted or missing
- Testing a single skill in isolation

```bash
# Normal sync
python .github/skills/spec-sync/sync_spec.py

# Force regenerate (even if no changes detected)
python .github/skills/spec-sync/sync_spec.py --force
```

---

### What the Sync Script Does

The script performs these operations:
1. Read `DEV_SPEC.md` from project root
2. Calculate hash to detect changes 
3. Split the document into chapter files under `specs/`
4. Generate `SPEC_INDEX.md` as the navigation index

---

### After Sync: Navigate with SPEC_INDEX.md

**Use `SPEC_INDEX.md` as your entry point** to understand what each spec file contains:

```
Read: .github/skills/spec-sync/SPEC_INDEX.md
```

This index file provides:
- Summary of each chapter's content 
- Quick reference to locate the spec you need 

Then read the specific spec file you need from `specs/` directory:

```
Read: .github/skills/spec-sync/specs/05-architecture.md
```

---

## Directory Structure

```
.github/skills/spec-sync/
├── SKILL.md              ← This file
├── SPEC_INDEX.md         ← Auto-generated index (navigation index)
├── sync_spec.py          ← Sync script
├── .spec_hash            ← Hash file for change detection
└── specs/                ← Split spec files (chapter files)
    ├── 01-overview.md
    ├── 02-features.md
    ├── 03-tech-stack.md
    ├── 04-testing.md
    ├── 05-architecture.md
    ├── 06-schedule.md
    └── 07-future.md
```

---

## Important Notes

- **Never edit files in `specs/` directly** — they are auto-generated
- **Always edit `DEV_SPEC.md`** and re-run the sync script
- Use `--force` flag to regenerate even if no changes detected:
  ```bash
  python .github/skills/spec-sync/sync_spec.py --force
  ```
