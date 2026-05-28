---
name: allocate-file
description: This file instructs how to allocate files in the cyber security vault
version: 2.1
lastUpdated: 2026-01-19
---

# Allocate File Skill

This skill guides the process of properly organizing and allocating files in the cyber security knowledge vault following the Zettelkasten method.

## Overview

When new files are added to the vault (typically in root or 0-inbox/), they must be:
1. Renamed to follow the standardized naming convention
2. Updated with complete YAML frontmatter
3. Moved to the appropriate folder (1-concepts, 2-areas, 3-resources, or 4-archives)
4. Linked to related notes with bidirectional references
5. Update INDEX.md to include the new note in appropriate sections

---

## Step 1: Rename File

### Naming Convention
All files must follow: `YYYYMMDDhhmmss-descriptive-title.md`

- **ID (YYYYMMDDhhmmss)**: 14-digit timestamp
  - YYYY: Year (e.g., 2026)
  - MM: Month (01-12)
  - DD: Day (01-31)
  - hh: Hour (00-23)
  - mm: Minute (00-59)
  - ss: Second (00-59)
- **Title**: Lowercase, hyphen-separated, descriptive
  - Use hyphens (-) not underscores (_)
  - Keep concise but clear (3-6 words ideal)
  - Avoid special characters

### Examples
- ❌ Bad: `Explore debugging techniques.md`
- ❌ Bad: `test.md`
- ✅ Good: `20260114100000-python-debugging-techniques.md`
- ✅ Good: `20260107070934-python-file-handling.md`

### Command
```bash
mv "Old File Name.md" "YYYYMMDDhhmmss-new-descriptive-name.md"
```

---

## Step 2: Update YAML Front Matter

### Required Fields

Every note must include complete YAML frontmatter at the top:

```yaml
---
id: YYYYMMDDhhmmss
title: Descriptive Note Title
tags:
  - primary-tag
  - secondary-tag
  - category-tag
  - source-tag
createdAt: YYYY-MM-DD
updatedAt: YYYY-MM-DD
related:
  - "[[YYYYMMDDhhmmss-related-note-1]]"
  - "[[YYYYMMDDhhmmss-related-note-2]]"
---
```

### Field Guidelines

#### `id`
- Must match the timestamp in filename
- 14-digit format: YYYYMMDDhhmmss
- Example: `20260114100000`

#### `title`
- Clear, descriptive title (can include spaces and capitals)
- Should be readable and searchable
- Example: `Python debugging techniques`

#### `tags`
- Use 3-7 tags per note
- Include both general and specific tags
- Tag hierarchy:
  1. **Core Domain**: `#incident-response`, `#network-security`, `#web-security`
  2. **Specific Tools**: `#wireshark`, `#python`, `#siem`
  3. **Protocols**: `#tcp`, `#tls`, `#ipv4`
  4. **Frameworks**: `#nist`, `#csf`
  5. **Source**: `#Coursera`, `#Course6`, `#Course7`
- Examples: `python`, `debugging`, `error-handling`, `automation`, `Coursera`, `Course7`

#### `createdAt` / `updatedAt`
- Format: YYYY-MM-DD
- createdAt: Original creation date (don't change)
- updatedAt: Last modification date (update when editing)

#### `related`
- List related notes using Wikilinks
- Format: `"[[YYYYMMDDhhmmss-note-title]]"`
- Include 2-5 related notes when applicable
- Create bidirectional links (update both files)

### Example: Complete Frontmatter

```yaml
---
id: 20260114100000
title: Python debugging techniques
tags:
  - python
  - debugging
  - error-handling
  - automation
  - Coursera
  - Course7
createdAt: 2026-01-14
updatedAt: 2026-01-14
related:
  - "[[20260106183102-Essential Python components for automation]]"
  - "[[20260107070934-python-file-handling]]"
  - "[[20260107080000-python-file-parsing-split-join]]"
---
```

---

## Step 3: Move to Appropriate Folder

### Folder Structure

- **0-inbox/** - Temporary location for new/unprocessed notes
  - Use for initial file placement
  - Should be emptied regularly during maintenance
  
- **1-concepts/** - Permanent notes with fundamental concepts
  - Core cybersecurity concepts
  - Tool documentation and theory
  - Process explanations
  - Examples: NIST frameworks, protocol explanations, security concepts
  
- **2-areas/** - Ongoing projects and responsibilities
  - Active projects
  - Work in progress
  - Ongoing learning tracks
  
- **3-resources/** - Reference materials and quick guides
  - Command cheatsheets
  - Playbook examples
  - Quick reference guides
  - Examples: tcpdump commands, wireshark filters
  
- **4-archives/** - Completed or deprecated content
  - Old course materials
  - Outdated information
  - Completed projects
  - Historical references

### Decision Matrix

| Content Type | Destination | Examples |
|--------------|-------------|----------|
| Conceptual knowledge | 1-concepts/ | Frameworks, protocols, theories |
| Active project | 2-areas/ | Current research, ongoing work |
| Quick reference | 3-resources/ | Command guides, cheatsheets |
| Completed/outdated | 4-archives/ | Old notes, deprecated info |
| Unprocessed | 0-inbox/ | Temporary holding only |

### Command
```bash
mv "0-inbox/YYYYMMDDhhmmss-note-title.md" "1-concepts/"
```

---

## Step 4: Update Links

### Bidirectional Linking

When adding a new note, update related notes to link back:

1. **Identify related notes** - Find 2-5 closely related notes
2. **Add forward links** - Add links in new note's `related` field
3. **Add backward links** - Add new note's link to related notes
4. **Update dates** - Update `updatedAt` field in all modified notes

### Example Workflow

**New note created:**
- `20260114100000-python-debugging-techniques.md`

**Related notes identified:**
- `20260106183102-Essential Python components for automation.md`
- `20260107070934-python-file-handling.md`
- `20260107080000-python-file-parsing-split-join.md`

**Actions:**
1. ✅ Add links in new note's frontmatter
2. ✅ Add new note's link to each related note's frontmatter
3. ✅ Update `updatedAt` to current date in all modified notes
4. ✅ Fix any broken links (incorrect IDs)

### Link Format
- Use Wikilinks: `[[YYYYMMDDhhmmss-note-title]]`
- Include full ID and title
- Use quotes in YAML: `"[[20260114100000-python-debugging-techniques]]"`

### Obsidian Link Behavior

**Important:** For Obsidian (and VS Code with Markdown extensions) to properly resolve links:

1. **Links within the same folder** - Can use just the ID-title:
   ```markdown
   [[20260114100000-python-debugging-techniques]]
   ```

2. **Links across folders** - Should include relative path:
   ```markdown
   [[1-concepts/20260114100000-python-debugging-techniques]]
   [[3-resources/20250926100000-tcpdump-usage-guide]]
   ```

3. **In YAML frontmatter** - Always use quotes and consider folder structure:
   ```yaml
   related:
     - "[[20260106183102-Essential Python components for automation]]"
     - "[[3-resources/20250926100000-tcpdump-usage-guide]]"
   ```

4. **INDEX.md links** - Use folder-relative paths for navigation:
   ```markdown
   - [[20250825110100-NIST-CSF-incident-response]] - NIST CSF概要
   - [[1-concepts/20260119100000-disaster-recovery-business-continuity]] - 災害復旧
   ```

**Best Practices:**
- Test links after creation (Cmd/Ctrl + Click in Obsidian)
- Use consistent path format throughout the vault
- Prefer short links within same folder, explicit paths across folders
- Update links when moving files between folders

### Common Link Issues to Fix
- ❌ Missing links (one-way references)
- ❌ Incorrect IDs (wrong timestamp)
- ❌ Broken links (file doesn't exist)
- ❌ Duplicate entries in related field
- ❌ Missing folder paths in cross-folder links
- ❌ Incorrect relative paths

---

## Step 5: Update INDEX.md

### Why Update INDEX.md

INDEX.md serves as the main navigation hub for the entire vault. When adding significant notes (especially to 1-concepts/), update INDEX.md to maintain discoverability.

### When to Update

**Always update for:**
- New conceptual notes in 1-concepts/
- New major topics or categories
- New tags that represent significant areas
- New course materials (Course6, Course7, Course8, etc.)

**Optional for:**
- Minor updates to existing notes
- Files in 0-inbox/ (temporary)
- Reference materials in 3-resources/ (unless major)

### What to Update

1. **Main Topic Sections** - Add new notes under appropriate headings:
   ```markdown
   ### セキュリティフレームワーク
   - [[20250825110100-NIST-CSF-incident-response]] - NIST CSF概要
   - [[20260119100000-disaster-recovery-business-continuity]] - 災害復旧と事業継続計画
   ```

2. **Tag List** - Add new tags when introducing new categories:
   ```markdown
   ### 分野別
   - #incident-response - インシデント対応
   - #disaster-recovery - 災害復旧
   - #business-continuity - 事業継続
   ```

3. **Course Tags** - Add new course identifiers:
   ```markdown
   ### コース関連
   - #Course6 - Coursera コース6
   - #Course7 - Coursera コース7
   - #Course8 - Coursera コース8
   ```

### Update Workflow

1. **Determine section** - Where does this note fit?
   - Security frameworks?
   - Network security?
   - Tools?
   - Programming/automation?

2. **Add link with description** - Use format:
   ```markdown
   - [[note-id-and-title]] - Brief description in Japanese
   ```

3. **Update tags section** - If new tags were created:
   - Add to appropriate tag category
   - Include brief Japanese description

4. **Maintain consistency** - Follow existing patterns:
   - Same bullet format
   - Same link style
   - Same description style
   - Alphabetical or chronological order within sections

### Example: Adding New Notes to INDEX.md

**New notes created:**
- `20260119100000-disaster-recovery-business-continuity.md`
- `20260117100000-data-asset-classification.md`

**INDEX.md updates:**

```markdown
### セキュリティフレームワーク
- [[20250825110100-NIST-CSF-incident-response]] - NIST CSF概要
- [[20250905100000-incident-response-plan]] - インシデント対応計画
- [[20251022100000-incident-documentation]] - インシデントドキュメンテーション
+ - [[20260119100000-disaster-recovery-business-continuity]] - 災害復旧と事業継続計画
+ - [[20260117100000-data-asset-classification]] - データと資産の分類
```

```markdown
### 分野別
- #incident-response - インシデント対応
- #network-security - ネットワークセキュリティ
+ - #data-classification - データ分類
+ - #disaster-recovery - 災害復旧
+ - #business-continuity - 事業継続
```

### INDEX.md Structure Reference

```markdown
# Cyber Security Vault Index

## フォルダ構造
[Folder descriptions]

## 主要トピック
### セキュリティフレームワーク
### チーム・組織
### ネットワークセキュリティ
### Webセキュリティ
### 脅威モデリング
### セキュリティツール
### 自動化とプログラミング
### パケット解析
### ログ管理
### 脅威検知・分析

## タグ一覧
### コース関連
### 分野別
### ツール
### プロトコル

## ファイル命名規則
## YAMLフロントマター形式
## リンク方法
```

---

## Checklist

Use this checklist when allocating a file:

- [ ] File renamed to `YYYYMMDDhhmmss-descriptive-title.md` format
- [ ] YAML frontmatter includes all required fields:
  - [ ] `id` matches filename timestamp
  - [ ] `title` is clear and descriptive
  - [ ] `tags` includes 3-7 relevant tags
  - [ ] `createdAt` set to creation date
  - [ ] `updatedAt` set to current date
  - [ ] `related` includes 2-5 related notes
- [ ] File moved to appropriate folder (1-concepts, 2-areas, 3-resources, or 4-archives)
- [ ] Related notes updated with bidirectional links
- [ ] All related notes have `updatedAt` refreshed
- [ ] No broken links or incorrect IDs
- [ ] Links include folder paths when crossing directories
- [ ] Links tested in Obsidian (Cmd/Ctrl + Click)
- [ ] INDEX.md updated with new note (if 1-concepts/)
- [ ] INDEX.md tags section updated (if new tags)
- [ ] Inbox folder is clean (file removed from 0-inbox/)

---

## Common Scenarios

### Scenario 1: Unprocessed file in root directory
```bash
# File: "Explore debugging techniques.md" in root
# 1. Move to inbox
mv "Explore debugging techniques.md" 0-inbox/

# 2. Review content, add frontmatter
# 3. Rename
cd 0-inbox/
mv "Explore debugging techniques.md" "20260114100000-python-debugging-techniques.md"

# 4. Move to concepts
mv "20260114100000-python-debugging-techniques.md" ../1-concepts/

# 5. Update links in related files

# 6. Update INDEX.md
# - Add to "自動化とプログラミング" section
# - Add any new tags to tag sections
```

### Scenario 2: Duplicate file detected
```bash
# Check differences
diff "old-file.md" "1-concepts/new-file.md"

# If new version is better, remove old
rm "old-file.md"

# If old has unique content, merge manually then remove
```

### Scenario 3: File with no frontmatter
```markdown
# Add complete YAML block at top of file
---
id: 20260114100000
title: [Add descriptive title]
tags:
  - [add relevant tags]
createdAt: 2026-01-14
updatedAt: 2026-01-14
related:
  - "[[link-to-related-note]]"
---
[Original content starts here]
```

---

## Maintenance Tasks

### Weekly
- [ ] Process all files in 0-inbox/
- [ ] Update broken links
- [ ] Add missing frontmatter fields
- [ ] Verify file naming consistency

### Monthly
- [ ] Review and consolidate related notes
- [ ] Archive outdated content to 4-archives/
- [ ] Update INDEX.md with new major topics
- [ ] Check for duplicate content

### Quarterly
- [ ] Major vault reorganization if needed
- [ ] Tag system review and optimization
- [ ] Relationship graph analysis
- [ ] Documentation quality review

---

## Tips

1. **Always start with inbox** - New files should go to 0-inbox first
2. **ID uniqueness** - Each note must have unique timestamp ID
3. **Link as you go** - Add related links immediately when creating notes
4. **Update dates** - Always update `updatedAt` when modifying files
5. **Consistent tagging** - Use existing tags when possible, create new ones sparingly
6. **Bidirectional links** - Every link should be reciprocated
7. **Clear titles** - Titles should be searchable and descriptive
8. **Regular reviews** - Schedule weekly inbox processing
9. **Test in Obsidian** - Always test links work correctly (Cmd/Ctrl + Click)
10. **Update INDEX.md** - Add significant notes to INDEX.md for discoverability
11. **Use folder paths** - Include folder paths in links when crossing directories
12. **Maintain INDEX.md** - Keep INDEX.md organized and up-to-date with new topics

---

## Summary

When allocating files in the cyber security vault:
1. ✅ Rename with timestamp ID format
2. ✅ Add complete YAML frontmatter
3. ✅ Move to appropriate folder
4. ✅ Create bidirectional links
5. ✅ Update INDEX.md for discoverability
6. ✅ Test all links in Obsidian

This process ensures:
- **Organization** - Files in correct locations
- **Discoverability** - Easy to find via INDEX.md
- **Connectivity** - Proper link relationships
- **Consistency** - Standardized format throughout
- **Maintainability** - Easy to update and reorganize

---

Last updated: 2026-01-19
