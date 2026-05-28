# AI Changelog Guide

> **TL;DR:** Add changelog entries after meaningful work. Use importance levels to highlight achievements.

## Quick Reference

### When to Add Entry

| Trigger | Level | Category |
|---------|-------|----------|
| Plan completed & implemented (big feature) | 1 (Saavutus) | feature |
| New admin page or major system | 1 | feature |
| Major refactoring (architectural) | 1 | refactor |
| Normal new feature | 3 | feature |
| Bug fix (any) | 3-4 | fix |
| Small UI tweak | 4 | fix |
| Database migration | 3-4 | feature/fix |
| Minor technical change | 4 | chore |

### Importance Levels

| Level | Label | When to Use |
|-------|-------|-------------|
| **1** | Saavutus | **Rare** - Only day's MAIN achievement, new system, major milestone |
| **2** | Tärkeä | **Sparingly** - Notable feature that deserves highlight |
| **3** | Normaali | **Default** - Most features, fixes, changes go here |
| **4** | Tekninen | Small detail, minor tweak, technical debt |

**Rule of thumb:** When in doubt, use level 3. Level 1-2 should be rare.

## SQL Insert Pattern

```sql
INSERT INTO admin.changelog_entries (description, category, importance)
VALUES (
  'Short description of what was done',
  'feature',  -- feature, fix, refactor, docs, chore
  2           -- 1-4 importance level
);
```

## Achievement Rules

### Level 1 (Saavutus) - RARE

Use only for:
- **New major system**: Entirely new capability (e.g., "Lean changelog system")
- **Big planned feature**: Multi-day implementation with planning phase
- **New admin page**: First-time creation of admin tool

### Level 2 (Tärkeä) - SPARINGLY

Use for:
- **Notable improvement**: Something worth mentioning in release notes
- **Important refactoring**: Significant code restructuring

### Level 3 (Normaali) - DEFAULT

**Most things go here:**
- Normal features
- Bug fixes
- Small improvements
- New components
- Database changes

### Level 4 (Tekninen)

- Minor tweaks
- Code cleanup
- Unused import removal
- Small styling changes

### Skip Changelog

- Typo fixes in code/docs
- Comment updates
- Failed attempts (only log success)

## Examples

### Level 1 (Achievement) - New system

```sql
-- New admin page or major system
INSERT INTO admin.changelog_entries (description, category, importance)
VALUES (
  'Admin i18n-sivu: käännöstiedostojen katselu ja hallinta',
  'feature',
  1  -- New admin page = level 1
);
```

### Level 3 (Normal) - Most fixes and features

```sql
-- Bug fix (most go to level 3)
INSERT INTO admin.changelog_entries (description, category, importance)
VALUES (
  'Korjattu infinite loop AdminTranslationsPage-sivulla',
  'fix',
  3  -- Normal fix
);

-- Small feature improvement
INSERT INTO admin.changelog_entries (description, category, importance)
VALUES (
  'Aiheet-sivun oletusajärjestys suomenkielisen nimen mukaan',
  'feature',
  3  -- Normal feature
);
```

### Level 4 (Technical) - Minor changes

```sql
-- Code cleanup, minor tweaks
INSERT INTO admin.changelog_entries (description, category, importance)
VALUES (
  'Poistettu käyttämättömät importit (CodeQL)',
  'fix',
  4  -- Technical cleanup
);
```

## Workflow

1. **Complete meaningful work** (not just reading/exploring)
2. **Determine importance**:
   - New admin page or major system? → Level 1
   - Most features and fixes → Level 3 (default)
   - Minor cleanup? → Level 4
3. **Write concise description** (Finnish, one line)
4. **Insert entry** via SQL
5. **Verify** entry appears in admin dashboard

## Categories

| Category | Finnish | Use For |
|----------|---------|---------|
| `feature` | Ominaisuus | New functionality |
| `fix` | Korjaus | Bug fixes |
| `refactor` | Refaktorointi | Code restructuring |
| `docs` | Dokumentaatio | Documentation changes |
| `chore` | Ylläpito | Maintenance, configs |

## Bundling Small Tasks

When completing multiple related small tasks, create ONE entry (still level 3):

```sql
-- Instead of 5 separate entries for small fixes
INSERT INTO admin.changelog_entries (description, category, importance)
VALUES (
  'Hakutermien käännösten hallinta: infinite loop korjaus, AI-käännösten näyttö, usage_count reset',
  'fix',
  3  -- Bundled but still normal level
);
```

## Admin UI

View and manage entries at `/admin/changelog` → "Muutokset" tab:
- Add entries via form (category + importance dropdowns)
- Toggle "Näytä kaikki" to see level 3-4 entries
- "Tee versio" bundles unreleased entries into release
