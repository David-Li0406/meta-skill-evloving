# Tasks: Boris Tips Integration

## 任務總覽

| ID | 任務 | 優先級 | 狀態 |
|----|------|--------|------|
| 1 | 更新 psb-setup.md 加入 permissions 配置 | P0 | [ ] |
| 2 | 建立 06-scaling 模組結構 | P1 | [ ] |
| 3 | 建立 large-codebase.md | P1 | [ ] |
| 4 | 更新 SKILL.md 模組列表 | P1 | [ ] |

---

## Task 1: 更新 psb-setup.md 加入 permissions 配置

- [x] **Task 1: Permissions 配置**

**檔案：** `skills/00-getting-started/_base/psb-setup.md`

**變更內容：**
1. 在 Setup 階段 7 步驟清單後新增第 8 步：Claude Code 權限配置
2. 添加 `settings.local.json` 配置範例
3. 說明 `/permissions` vs `--dangerously-skip-permissions`

**_Prompt:**
```
Role: Documentation Writer for Claude Code Skills
Task: Update psb-setup.md to include Claude Code permissions configuration guidance. Add step 8 to the PSB checklist covering /permissions setup. Include JSON config examples and best practices.
Restrictions:
- Do not modify existing steps 1-7
- Keep formatting consistent with existing style
- Use traditional Chinese
_Leverage:
- .claude/memory/learnings/2025-01-07-boris-cherny-claude-code-tips.md (Boris Tip #6)
_Requirements: US-1
Success: psb-setup.md contains permissions section with config example and /permissions guidance
Instructions: Mark task as [-] in progress, implement, use log-implementation after completion, then mark [x] complete
```

---

## Task 2: 建立 06-scaling 模組結構

- [x] **Task 2: Scaling 模組結構**

**檔案：**
- `skills/06-scaling/README.md`
- `skills/06-scaling/_base/` 目錄

**變更內容：**
1. 建立 `06-scaling` 目錄
2. 建立 `_base` 子目錄
3. 建立 README.md 說明模組用途

**_Prompt:**
```
Role: Skill Architect
Task: Create the 06-scaling module directory structure following the atomic architecture pattern used by other modules.
Restrictions:
- Follow existing module structure (see 05-integration as reference)
- README should be concise
- Use traditional Chinese
_Leverage: skills/05-integration/README.md (structure reference)
_Requirements: AD-2
Success: 06-scaling directory exists with README.md and _base/ subdirectory
Instructions: Mark task as [-] in progress, implement, use log-implementation after completion, then mark [x] complete
```

---

## Task 3: 建立 large-codebase.md

- [x] **Task 3: Large Codebase 文檔**

**檔案：** `skills/06-scaling/_base/large-codebase.md`

**變更內容：**
1. 問題診斷章節
2. fileSuggestion 配置說明
3. 索引腳本模板
4. 適用場景說明

**_Prompt:**
```
Role: Performance Optimization Expert
Task: Create large-codebase.md documenting how to optimize Claude Code file search for large codebases using fileSuggestion configuration.
Restrictions:
- Include problem diagnosis criteria
- Provide working script template
- Document limitations
- Use traditional Chinese
_Leverage:
- .claude/memory/learnings/2025-01-07-boris-cherny-claude-code-tips.md (大型 Codebase 優化段落)
- Design document fileSuggestion configuration section
_Requirements: US-2
Success: large-codebase.md is complete with config examples, script template, and usage scenarios
Instructions: Mark task as [-] in progress, implement, use log-implementation after completion, then mark [x] complete
```

---

## Task 4: 更新 SKILL.md 模組列表

- [x] **Task 4: SKILL.md 更新**

**檔案：** `skills/SKILL.md`

**變更內容：**
1. 快速導覽表格加入 06-scaling
2. 目錄結構加入 06-scaling
3. 添加 large-codebase.md 到模組內容

**_Prompt:**
```
Role: Documentation Maintainer
Task: Update SKILL.md to include the new 06-scaling module in the quick navigation table and directory structure.
Restrictions:
- Only add 06-scaling module entries
- Do not modify other content
- Maintain consistent formatting
_Leverage: Existing module entries in SKILL.md
_Requirements: Design integration points
Success: SKILL.md includes 06-scaling in both navigation table and directory structure
Instructions: Mark task as [-] in progress, implement, use log-implementation after completion, then mark [x] complete
```

---

## 驗證清單

完成所有任務後：

- [x] `psb-setup.md` 包含 permissions 配置段落
- [x] `06-scaling/` 目錄結構正確
- [x] `large-codebase.md` 內容完整
- [x] `SKILL.md` 已更新
- [x] 所有文檔使用繁體中文
- [x] 格式與現有文檔一致
