# Skill Ingestion Protocol

> **CLI First, LLM for Intelligence Only**. Use this protocol to import external skills efficiently.

## Core Principle
Use CLI for heavy lifting (cloning, listing, moving, deleting). Use LLM only for analysis and registry generation.

---

## Phase 1: Git Clone (Zero Token)

**Action**: Clone the repo to a temp directory.

```powershell
# Windows PowerShell
$REPO_URL = "https://github.com/owner/repo"  # <--- REPLACE THIS
$TEMP_DIR = ".agent/skills/_import"

New-Item -ItemType Directory -Force -Path $TEMP_DIR | Out-Null
git clone --depth 1 $REPO_URL "$TEMP_DIR/repo-name"
tree /F "$TEMP_DIR/repo-name/skills" 2>$null || ls -R "$TEMP_DIR/repo-name/skills"
```

---

## Phase 2: Analysis & Selection

**Action**: List available skills and ask user to select.

```powershell
# List Skills
Get-ChildItem -Path ".agent/skills/_import/repo-name/skills" -Directory | Select-Object Name
```

**LLM Task**:
1. Read the `SKILL.md` frontmatter of selected skills (only first 50 lines).
2. Check if a skill with the same name already exists in `.agent/skills/`.

---

## Phase 3: De-branding (Optional)

**Action**: Bulk replace branding (e.g., "Claude" -> "Antigravity").

```powershell
$target = ".agent/skills/_import/repo-name/skills/skill-name"
Get-ChildItem -Path $target -Recurse -Include *.md,*.txt,*.json | ForEach-Object {
    (Get-Content $_.FullName -Raw) -replace 'Claude', 'Antigravity' | Set-Content $_.FullName -NoNewline
}
```

---

## Phase 4: Install & Register

**Action 1**: Move folder to production.
```powershell
Move-Item -Path ".agent/skills/_import/repo-name/skills/skill-name" -Destination ".agent/skills/skill-name" -Force
```

**Action 2 (LLM)**: Generate `registry.json` entry.
- Extract `name` and `description` from frontmatter.
- Generate specific `intent_keywords`.
- Append to `.agent/skills/registry.json`.

---

## Phase 5: Cleanup

**Action**: Remove temp files.
```powershell
Remove-Item -Path ".agent/skills/_import" -Recurse -Force
```
