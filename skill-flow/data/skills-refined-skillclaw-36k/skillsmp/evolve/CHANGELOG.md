# Changelog

All notable changes to this project will be documented in this file.

## [5.11.0] - 2026-01-21

### Added
- **GitHub → Skill 封裝策略文檔**
  - 新增 `skills/05-integration/_base/github-to-skill.md`
  - 六維度快速判斷框架（效率、專業、完整、品質、體驗、學習）
  - 分解重組進階策略（大型項目拆解為元件再重組）
  - 「封裝即學習」章節（封裝過程即知識內化過程）
  - UX 改善封裝技巧（自然語言介面取代參數地獄）
  - 決策流程圖與實戰案例
  - 與 evolve skill-acquisition 流程整合說明

### Documentation
- 更新 `skills/05-integration/README.md` 加入新文檔連結

---

## [5.10.1] - 2026-01-20

### Fixed
- **發布 SOP 完善**
  - 新增 Step 6: 同步 plugin cache
  - 新增 Step 7: 同步 `.claude/skills/evolve/` 目錄
  - 新增發布後版本驗證命令
  - 更新自動化腳本加入同步步驟
  - 修復發布後 skill 版本未更新的問題

---

## [5.10.0] - 2026-01-20

### Added
- **CP6.5 Worktree 完成流程增強**
  - 新增 PR 合併策略選擇表（Rebase/Squash/Merge）
  - 推薦使用 `gh pr merge --rebase` 取得線性歷史
  - 視覺化說明 rebase vs merge 的歷史差異
  - 保留直接合併選項給不需 PR 的專案

- **版本發布工具改進**
  - 新增 `sync-plugin-cache.sh` 自動同步腳本
  - 修復 `update-version.sh` macOS sed 相容性

### Documentation
- 記錄 SDD 規格驅動開發學習筆記
- 記錄版本發布工作流教訓

---

## [5.9.2] - 2026-01-20

### Added
- **測試覆蓋率提升**
  - 新增 `tests/test_checkpoints.bats` (16 tests) - 檢查點系統測試
  - 新增 `tests/test_scripts.bats` (19 tests) - Shell 腳本測試
  - 新增 `tests/test_memory.bats` (17 tests) - 記憶系統測試
  - 測試總數：73 tests（100% 通過）

- **Hooks 配置文檔**
  - 新增 `hooks/README.md` 說明兩種 hook 機制

- **失敗經驗記錄**
  - 新增 `.claude/memory/failures/2026-01-20-false-test-pass-claim.md`

### Changed
- **Token 優化**
  - SKILL.md 精簡 17%（185 → 154 行）
  - 版本歷史改用動態摘要 + 連結

### Fixed
- 修復 `skills/02-checkpoints/README.md` 缺少 CP0、CP0.5、CP6、CP6.5
- 修復 4 個 learning 文件的 YAML frontmatter 格式
- 修復 `test_skills.bats` markdown 連結驗證邏輯

### Removed
- 移除已棄用的 `skillpkg.json` 和 `.skillpkg/` 目錄

---

## [5.9.1] - 2026-01-19

### Added
- **Release Hooks 強制執行**
  - 新增 `pre-release`、`post-git-tag`、`post-version-update` hooks
  - 版本相關文件變更時自動提醒檢查版本一致性
  - 第四條鐵律：NO RELEASE WITHOUT VERSION CONSISTENCY CHECK

- **版本發布檢查清單**
  - 新增 `skills/99-evolution/_base/release-checklist.md`
  - 完整的發布前/後檢查流程
  - 緊急回滾指南

### Fixed
- 修復版本不一致問題（plugin.json、README.md badge 未同步）
- 更新 `update-version.sh` 支援 README.md badge 更新

---

## [5.9.0] - 2026-01-19

### Added
- **Superpowers 工作流整合**
  - 新增 `skills/05-integration/_base/superpowers-integration.md` 整合模組
  - 將 superpowers 執行紀律強制整合進 evolve 流程
  - 6 個強制整合點確保執行品質

- **Claude Code Hooks 強制執行腳本**
  - 新增 `scripts/evolve-hooks.sh` 統一管理所有 hook 提醒
  - PreToolUse: 北極星檢查 (CP0)、Memory 搜尋 (CP1)、程式碼前檢查 (CP1.5)
  - PostToolUse: TDD 提醒、失敗診斷、測試驗證
  - Stop: 完成驗證提醒、Memory 記錄提醒
  - 更新 `hooks.md` 提供完整配置範例（腳本版 + 內嵌版）

### Changed
- **Goal Analysis 階段強化**
  - Level 1+ 任務強制使用 `superpowers:brainstorming`
  - 深度訪談與 brainstorming 協作流程

- **PDCA Plan 階段強化**
  - Level 2 任務強制使用 `superpowers:writing-plans`
  - 計畫文件格式規範

- **PDCA Do 階段強化**
  - 強制使用 `superpowers:test-driven-development`
  - 鐵律：NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST

- **PDCA Check 階段強化**
  - 強制使用 `superpowers:verification-before-completion`
  - 鐵律：NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
  - 禁止用語清單（should work now, probably fixed, looks correct）

- **CP5 失敗驗屍強化**
  - 強制使用 `superpowers:systematic-debugging`
  - 鐵律：NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
  - 四階段流程：根因調查 → 模式分析 → 假設測試 → 實作
  - 3+ 次修復失敗時強制質疑架構

### Philosophy
- **Superpowers 是 evolve 的「執行紀律層」**
- 核心洞察：有紀律的執行 > 隨機嘗試
- 解決方案：在各關鍵階段強制調用相應的 superpowers skill

### Integration Points
| 情境 | 必須調用的 Skill |
|------|------------------|
| Level 1+ 目標分析 | `superpowers:brainstorming` |
| Level 2 計畫撰寫 | `superpowers:writing-plans` |
| 任何程式碼變更 | `superpowers:test-driven-development` |
| 任何完成宣告 | `superpowers:verification-before-completion` |
| 任何失敗/錯誤 | `superpowers:systematic-debugging` |
| 分支完成 | `superpowers:finishing-a-development-branch` |

---

## [5.8.0] - 2026-01-19

### Added
- **Skill 缺口處理流程**
  - 當 Skill Discovery 找不到適合的 skill（相關度 < 0.5）時，自動詢問使用者
  - 提供三個選項：研究並建立新 Skill、組合現有 Skill、直接開始
  - 整合 skill-creator 和 4C 知識習得法

### Changed
- **CP1 檢查點更新**
  - 新增「找不到適合 Skill」處理流程
  - 明確的決策樹和選項說明
- **skill-acquisition.md 更新**
  - 更新 Step 3.5 的選項，加入「研究並建立」選項

---

## [5.7.0] - 2026-01-19

### Added
- **LEANN Skill Discovery 整合**
  - 新增 `scripts/setup-skill-index.sh` 設定 LEANN 語義搜尋環境
  - 新增 `skills/05-integration/_base/leann-skill-discovery.md` 整合指南
  - 支援 79 個 skills 的向量語義索引

### Changed
- **CP1 強化**：加入 LEANN 語義搜尋 Skill 推薦
  - 從任務描述理解概念，而非關鍵字匹配
  - 搜尋「卡牌遊戲」→ 也找到 "deckbuilder", "roguelike" 相關 skill
  - 自動降級到 FTS5 當 LEANN 不可用時

### Features
- 語義理解：理解任務概念而非關鍵字匹配
- 向量索引：LEANN HNSW 後端，本地運行
- 自動推薦：CP1 自動顯示相關度分數

---

## [5.6.0] - 2026-01-17

### Changed
- **Plugin 架構簡化**
  - 整合 `evolve-plugin/` 子目錄到根目錄
  - `.claude-plugin/` 現在直接在 repo 根目錄
  - 安裝方式簡化為 `/plugin marketplace add miles990/self-evolving-agent`

### Updated
- **Marketplace 名稱變更**
  - 舊：`/plugin marketplace add miles990/self-evolving-agent#evolve-plugin`
  - 新：`/plugin marketplace add miles990/self-evolving-agent`
  - 舊：`/plugin install evolve@evolve-plugin`
  - 新：`/plugin install evolve@self-evolving-agent`

### Fixed
- 更新所有文檔中的 marketplace 引用
- 更新版本腳本 (update-version.sh, check-version.sh) 指向正確路徑

---

## [5.5.0] - 2026-01-16

### Added
- **智能 Skill 生態系 MVP**
  - 新增 `scripts/sync-skills.sh` 從 GitHub 同步 skill 索引到 sqlite-memory
  - 新增 `skills/03-memory/_base/scope-detection.md` Scope 自動判斷指南
  - 新增 `skills/05-integration/_base/skill-ecosystem.md` 生態系整合文檔
  - 支援 78 個 skills（54 software + 24 domain）自動索引

### Changed
- **CP1 強化**：加入 Skill 推薦功能（自動搜尋並推薦相關 skill）

### Features
- 自動發現：從 GitHub repos 同步 skill metadata
- 智能推薦：根據任務關鍵字推薦相關 skill
- 經驗共享：透過 scope（global/project:xxx）實現跨專案學習

---

## [5.4.0] - 2026-01-16

### Added
- **Memory MCP 整合**
  - 新增 `skills/05-integration/_base/memory-mcp.md` 整合指南
  - 整合 SQLite FTS5 全文搜尋到 evolve 流程
  - 支援 Skill 使用追蹤（成功率統計）
  - 支援失敗經驗跨專案索引

### Changed
- **CP1 強化**：加入 `memory_search` + `failure_search`（FTS5 搜尋）
- **CP3.5 強化**：加入 `memory_write`（雙重記錄：Git + SQLite）
- **CP5 強化**：加入 `failure_record`（跨專案失敗經驗共享）

### Performance
- 搜尋速度：~20ms → ~3.5ms（5.7x 提升）
- Token/搜尋：~2300 → ~200（91% 節省）

---

## [5.3.0] - 2026-01-15

### Added
- **智能 Plugin 安裝流程**
  - 自動檢查已安裝 plugins (`~/.claude/plugins/installed_plugins.json`)
  - 自動檢查已添加 marketplaces (`~/.claude/plugins/known_marketplaces.json`)
  - 版本比對：已安裝版本 vs marketplace 最新版本
  - 過期時建議執行 `/plugin update`

- **Skills → Plugin 轉換工具**
  - 新增 `scripts/convert-to-plugin.sh` 腳本
  - 支援 `--marketplace` 和 `--category` 模式
  - 自動生成 marketplace.json 和各分類 plugin.json

### Changed
- **skillpkg → Plugin Marketplace 遷移**
  - 移除所有 skillpkg MCP 依賴
  - 重命名 `skillpkg.md` → `skill-integration.md`
  - 更新安裝方式為 `/plugin marketplace add` + `/plugin install`

### Removed
- skillpkg MCP 工具呼叫（`mcp__skillpkg__*`）

---

## [5.2.0] - 2026-01-14

### Added
- **版本檢查與自動更新**
  - 啟動時檢查 evolve 版本
  - 建議用戶更新到最新版本

- **Skill Creator Token 優化**
  - 新增 Stage 3.5 Token 優化步驟
  - 整合 skill-optimizer 方法論

---

## [5.1.0] - 2026-01-14

### Added
- **Git Worktree 隔離環境**
  - 新增 Worktree 工作流程
  - 支援功能隔離開發
  - 自動清理完成的 worktree

---

## [5.0.0] - 2026-01-14

### Added
- **Plugin 格式支援**
  - 新增 `evolve-plugin/` 目錄，支援 Claude Code Plugin 安裝
  - 安裝方式：`/plugin install miles990/self-evolving-agent#evolve-plugin`
  - 新增 `.claude-plugin/plugin.json` 配置

- **Skill Creator 工作流**
  - 新增 `/new-skill` 命令和 `--new-skill` 參數
  - 四階段流程：引導式訪談 → 分析生成 → 驗證 → 發布
  - 新增 `skill-creator/` 模組（含範本和腳本）
  - 整合 `knowledge-acquisition-4c` 作為研究 fallback

- **Hooks 自動提醒**
  - `checkpoint-reminder.sh`：Edit/Write 後提醒 CP1.5、CP2
  - `memory-sync.sh`：Memory 文件創建後提醒 CP3.5

- **Commands 定義**
  - `commands/evolve/COMMAND.md`：正式 /evolve 命令
  - `commands/new-skill/COMMAND.md`：正式 /new-skill 命令

### Changed
- **Repo 整合**
  - 從雙 repo（self-evolving-agent + evolve-plugin）合併為單一 repo
  - `evolve-plugin/` 現為子目錄，不再是獨立 repo
  - 統一 `skills/` 和 `evolve-plugin/skills/` 內容

- **安裝路徑更新**
  - 舊：`/plugin install miles990/evolve-plugin`
  - 新：`/plugin install miles990/self-evolving-agent#evolve-plugin`

### Deprecated
- `miles990/evolve-plugin` 獨立 repo 已停用（建議 archive）

---

## [4.5.0] - 2026-01-12

### Changed
- **Token 優化 (Token Optimization)**
  - ASCII Box Art → Markdown 格式轉換，減少 token 消耗
  - SKILL.md: 14,727 bytes → 8,997 bytes (39% 減少)
  - 保持 100% 護欄效果與判斷力

### Optimized Files
- `skills/SKILL.md` - 主入口優化
  - 核心哲學區塊：ASCII box → table
  - 執行流程概覽：43 行 ASCII 圖 → 11 行編號清單
  - 架構考量三層設計：ASCII box → table
  - CP1.5 兩階段設計：ASCII box → bullet points
  - 停止條件/完成信號：ASCII box → table/list
- `skills/02-checkpoints/_base/cp1-memory-search.md` - ASCII box → checklist
- `skills/01-core/_base/pdca-cycle.md` - PDCA 流程圖和架構設計 ASCII → markdown
- `skills/00-getting-started/_base/psb-setup.md` - PSB 檢查清單 ASCII → markdown
- `skills/02-checkpoints/_base/cp1.5-consistency-check.md` - 多個 ASCII box → tables/checklists

### Philosophy
- 核心洞察：skillpkg 模組合併導致安裝後 7x 膨脹 (14.7KB → 106.8KB)
- 解決方案：移除裝飾性 ASCII 藝術，保留語意內容
- 原則：Token 效率 > 視覺美觀（在 CLI 環境中）

---

## [4.4.0] - 2026-01-12

### Added
- **北極星系統 (North Star System)**
  - 新增 `cp0-north-star.md` - 專案/任務開始前的方向錨定
  - 新增 `cp6-project-health-check.md` - 定期專案健檢（每 5 次迭代）
  - 北極星文件結構：一句話願景、完成標準、不做清單、當初為什麼開始
  - 北極星訪談流程：使用 AskUserQuestion 收集關鍵資訊
  - Memory 結構新增 `north-star/` 目錄

- **專案健檢機制 (CP6)**
  - Scope 檢查：有沒有做「不做清單」的東西？
  - 方向檢查：離北極星更近了嗎？
  - 終止檢查：這個專案還值得繼續嗎？
  - 健檢報告模板與偏離處理選項

### Changed
- **CP3 強化**：整合北極星方向校正
  - 對照北極星的「完成標準」和「不做清單」
  - 新增偏離處理選項（調整/更新/繼續/暫停）
- 更新執行流程圖，新增 CP0 和 CP6
- 更新強制檢查點表格，新增 CP0 和 CP6

### Philosophy
- 核心洞察：「做到後面，好像都迷失了方向」— 這是專案失敗的常見原因
- 解決方案：在開始時錨定方向，在過程中持續校正

---

## [4.3.0] - 2026-01-12

### Added
- **深度訪談模式 (Deep Interview)**
  - 新增 `goal-analysis.md` 深度訪談區塊
  - 觸發條件：Level 2 強制、Level 1+模糊建議
  - Ultrathink 4 問：隱藏假設、邊界情況、技術債務、二階效應
  - 訪談問題範本（4 大類深入問題）
  - 結束條件與產出格式（`goal_specification` YAML）

### Changed
- 更新執行流程圖，突出深度訪談步驟
- 流程簡述新增「深度訪談」標記

### Credits
- 靈感來源：[@BensonTWN](https://x.com/BensonTWN/status/2010319050099110270)
- 核心洞察：「寫 spec 最大的問題是你不知道自己漏了什麼」

---

## [4.1.0] - 2026-01-12

### Added
- **測試框架**
  - `tests/test_skills.bats` - Bats-core 測試套件
  - `tests/run_tests.sh` - 測試執行器（支援 `--quick` 和 `--bats` 模式）

- **自動化提升**
  - `Makefile` - 統一命令入口（`make help`, `make test`, `make validate`）
  - `scripts/quickstart.sh` - 一鍵快速設置新專案
  - CI 新增 quick-test job

- **智能化提升**
  - `skill-acquisition.md` 新增 **Fallback 機制**
    - Level 1: Skill + Memory（正常路徑）
    - Level 2: 外部知識源（context7, WebSearch, PAL）
    - Level 3: 結構化降級（分解任務、詢問用戶）
    - Level 4: 誠實失敗

### Changed
- CI 工作流程重構，新增 quick-test → validate → install-test 流程
- 更新能力評估框架，新增 `fallback_options` 欄位

---

## [4.0.1] - 2026-01-11

### Added
- **專業度提升**
  - `.gitignore` - 排除不必要的文件
  - `CLAUDE.md` - 專案約束文件，供 AI 理解專案規範
  - `docs/TROUBLESHOOTING.md` - 故障排除指南
  - `scripts/verify-install.sh` - 安裝驗證腳本
  - `.github/workflows/ci.yml` - GitHub Actions CI 自動化驗證

### Changed
- **移除 community/ 架構** - 簡化為單人使用模式
- 更新 `README.md` 貢獻指南，移除 community 引用
- 修復 `skillpkg.json` 硬編碼路徑問題

### Fixed
- `check-env.sh` 現在會正確檢測 `CLAUDE.md`

---

## [4.0.0] - 2026-01-11

### Breaking Changes
- **原子化架構重構** - 將 2000+ 行的 SKILL.md 拆分為模組化結構
- 路徑從根目錄 `SKILL.md` 改為 `skills/SKILL.md`

### Added
- **原子化模組結構**
  - `00-getting-started/` - 入門與環境設定
  - `01-core/` - 核心流程（PSB + PDCA）
  - `02-checkpoints/` - 強制檢查點（護欄）
  - `03-memory/` - 記憶系統操作
  - `04-emergence/` - 涌現機制
  - `05-integration/` - 外部工具整合
  - `99-evolution/` - 自我進化機制

- **`_base/` + `community/` 分離架構**
  - `_base/`: 官方內容（受保護，更新不會覆蓋）
  - `community/`: 社群貢獻（避免 merge conflict）

- **一鍵安裝**
  ```bash
  curl -fsSL https://raw.githubusercontent.com/miles990/self-evolving-agent/main/install.sh | bash
  ```

- **全域同步腳本**
  - `scripts/sync-global.sh` - 同步到 `~/.claude/skills/evolve/`
  - 支援 `--atomic` 參數保持原子化結構

### Changed
- SKILL.md 從 2027 行精簡為 192 行（主入口）
- 完整內容分散於各模組 `_base/` 目錄
- 全域整合版約 1769 行

### Benefits
- **更易維護**: 小文件 > 巨型文件
- **更易貢獻**: 社群可在 `community/` 自由添加
- **更易學習**: 模組化方便逐步閱讀
- **更易擴展**: 新功能加新模組，不影響既有內容

### Inspiration
- 借鑒 [makepad-skills](https://github.com/ZhangHanDong/makepad-skills) 的架構設計

---

## [3.7.1] - 2026-01-08

### Added - Checkpoint 3.5: Memory 同步

基於 evolve-trader 專案的實際失敗經驗，新增強制 Memory 同步檢查點：

- **Checkpoint 3.5: Memory 同步 - 即時更新 index.md**
  - 背景：創建多個 memory 文件（learnings, failures, decisions）後忘記更新 index.md
  - 用戶反饋：「我看.claude/memory沒有新的紀錄」
  - 原因：儲存與索引是兩個分離的動作，容易忽略後者
  - 解決：強制要求 Write memory → Edit index → 驗證 三步一體

### Changed
- 版本號從 3.7.0 更新至 3.7.1
- 強制檢查點從 3 個增至 3.5 個（新增 Memory 同步）

### Lessons Learned
- 從 evolve-trader 專案 ADR-043~045 優化過程中發現此模式
- 失敗記錄：`.claude/memory/failures/2026-01-08-forget-to-update-index.md`

---

## [3.5.1] - 2026-01-07

### Added - Auto Domain Detection
- **自動領域識別機制**
  - 從任務描述提取關鍵詞
  - 透過 skillpkg triggers 搜尋匹配的領域 skill
  - 自動載入相關領域知識
  - 支援多領域同時載入

- **領域 Skills 整合**
  - 支援 `claude-domain-skills` (非技術領域)
  - 支援 `claude-software-skills` (技術領域)
  - 16 個領域 skills 可用：
    - Finance: quant-trading, investment-analysis
    - Business: product-management, project-management, marketing, sales, strategy
    - Creative: game-design, ui-ux-design, brainstorming, storytelling, visual-media
    - Professional: research-analysis, knowledge-management
    - Lifestyle: personal-growth, side-income

- **新增範例文檔**
  - `examples/auto-domain-detection.md` - 自動領域識別使用範例

### Changed
- 核心流程新增 Auto Domain Detection 階段
- 更新 README 說明自動領域識別功能
- triggers 格式相容 skillpkg 1.0 schema

### Reference
- [claude-domain-skills](https://github.com/miles990/claude-domain-skills)
- [skillpkg](https://github.com/anthropics/skillpkg)

---

## [3.4.0] - 2026-01-07

### Added - Boris Cherny Tips 整合

基於 Claude Code 創作者 Boris Cherny 分享的 13 條使用技巧，新增以下功能：

- **強化驗證迴圈（Tip #13）**
  - PDCA Check 階段加入自動化驗證策略
  - 自動執行測試、構建、Lint、型別檢查
  - Boris: "給 Claude 驗證工作的方式，品質提升 2-3 倍"

- **Subagent 策略（Tip #8）**
  - `verify-app`: 驗證應用程式正確運作
  - `code-simplifier`: 簡化複雜程式碼
  - `build-validator`: 驗證構建流程
  - 新增 `.claude/memory/strategies/subagents.md` 策略定義

- **Hooks 整合（Tips #9, #12）**
  - PostToolUse hook: 自動格式化程式碼
  - Stop hook: 任務完成時執行驗證
  - 配置範例和使用建議

- **長時間任務處理（Tip #12）**
  - ralph-wiggum plugin 整合
  - Background Agent 使用指南
  - Permission 優化建議（/permissions vs --dangerously-skip-permissions）

### Reference
- [Boris Cherny Threads Post](https://www.threads.com/@boris_cherny/post/DTBVlMIkpcm)
- 學習記錄：`.claude/memory/learnings/2025-01-07-boris-cherny-claude-code-tips.md`

---

## [3.3.1] - 2026-01-06

### Added
- **標準化完成輸出格式**
  - `✅ GOAL ACHIEVED: [目標]` - 目標達成
  - `⏸️ NEED HUMAN: [原因]` - 需要人工介入
  - `❌ CANNOT COMPLETE: [原因]` - 無法完成
  - 方便識別和未來工具整合

### Cleanup
- 移除 `.claude/memory/` 範本（應在使用者專案）
- 移除 `drafts/` 目錄（屬於其他專案）
- 移除空的 `.github/` 目錄

---

## [3.3.0] - 2026-01-06

### Added
- **強制檢查點（Mandatory Checkpoints）**
  - Checkpoint 1: 任務開始前 - 主動查 Memory
  - Checkpoint 2: 程式碼變更後 - 編譯 + 測試必須通過
  - Checkpoint 3: Milestone 完成後 - 目標確認

- **Memory 生命週期管理**
  - 整理策略：合併、標註過時、加上下文、刪除
  - 觸發時機：Milestone 完成、條目超過 20 筆、新舊衝突、定期整理
  - Memory 整理 Checklist

- **index.md Metadata**
  - Last curated: 上次整理日期
  - Total entries: 總條目數
  - Next review: 下次整理日期
  - 統計區塊

### Changed
- 從「指南」變「護欄」：強制檢查點不可跳過
- Memory 不再只進不出，需要定期去蕪存菁

### Philosophy
- AI 的價值：0 → 60 分（基礎產出）
- 人類的價值：60 → 100 分（品質、判斷、細節）
- AI 是放大器，不是替代品

---

## [3.2.0] - 2026-01-06

### Added
- **核心哲學：AI 協作的抽象化範式**
  - MCP = 能力邊界（能做什麼）
  - Tools = 具體實作（怎麼做）
  - Skill = 領域知識（何時用什麼）— 封裝好的判斷力
  - CLAUDE.md = 上下文約束（專案規範）

- **PSB System 整合**
  - Plan-Setup-Build 環境準備流程
  - 在寫第一行程式碼前，先確保環境就緒
  - 7 步驟環境檢查清單

- **Phase -1: 環境準備**
  - Git Repo 檢查
  - CLAUDE.md 專案記憶
  - 記憶系統初始化
  - MCP 配置（可選）
  - Slash Commands 設定（可選）

- **設計原則**
  - 有主見的設計：合理預設值 > 讓 AI 選擇
  - 深且窄：專注 10% 高價值任務
  - 預期失敗：設計優雅降級
  - 增強回饋：執行中提醒目標和進度

### Changed
- 核心理念圖表更新為 PSB + PDCA 整合框架
- README 新增 Core Philosophy 區塊
- 流程從 `Goal → ...` 改為 `PSB Setup → Goal → ...`

### Reference
- [PSB System (HackMD)](https://hackmd.io/@eBrqaOowRWWfcAjhMNwlvg/HkNuCGcEZl)
- [Agent Design is Still Hard 2025](https://ihower.tw/blog/13513-agent-design-is-still-hard-2025)

---

## [3.1.0] - 2025-01-05

### Changed
- **Git-based Memory** - 記憶目錄從 `.claude/memory/` 改為 `.claude/memory/`
- 相容 GitHub Copilot Agent Skills（共用 `.github/` 目錄）
- 跨工具記憶共享：Claude Code, Copilot, Cursor

### New Memory Structure
```
📁 .claude/memory/
├── index.md          ← 快速索引（自動維護）
├── learnings/        ← 學習記錄
├── decisions/        ← 決策記錄 (ADR)
├── failures/         ← 失敗經驗
├── patterns/         ← 推理模式
└── strategies/       ← 策略記錄
```

### Added
- Phase 0: 初始化記憶系統
- 完整的記憶操作指南（Grep/Write/Edit 範例）
- index.md 索引機制
- 結構化經驗模板（frontmatter + markdown）

### Benefits
- Git 版本控制，可追溯歷史
- 團隊協作，PR 審核記憶變更
- 專案相關，隨 repo 遷移
- 離線可用，無需外部服務

---

## [3.0.0] - 2025-01-05

### Breaking Changes
- **Zero External Dependencies** - Removed all external MCP dependencies
- **Local File Memory** - Replaced Cipher MCP with local markdown files

### Changed
- Memory system: Cipher MCP → Local files (`.claude/memory/`)
- Skill acquisition: skillpkg → WebSearch + Context7
- All external tool references updated to use built-in tools only

### New Memory System
```
📁 .claude/memory/
├── experiences.md    ← Solutions, failures, lessons learned
├── strategies.md     ← Strategy tracking, success rates
└── learnings.md      ← New skills, discoveries, notes
```

### Benefits
- Works out of the box, no installation required
- Pure text format, Git-friendly
- Fast Grep search
- Copy to any project instantly

### Migration from v2.x
1. Export any existing Cipher memories manually
2. Paste into `.claude/memory/experiences.md` or `learnings.md`
3. No configuration changes needed

---

## [2.1.0] - 2025-01-03

### Added
- **Cipher MCP Integration** - Replaced claude-dev-memory with Cipher as the memory system
- **Dual Memory Architecture** - System 1 (Knowledge) + System 2 (Reflection)
- **New Memory Tools**:
  - `cipher_memory_search` - Search stored knowledge
  - `cipher_extract_and_operate_memory` - Store and retrieve experiences
  - `cipher_store_reasoning_memory` - Store reasoning patterns
  - `cipher_search_reasoning_patterns` - Search reasoning history

### Changed
- Memory system migration from claude-dev-memory to Cipher
- Updated all memory tool references in SKILL.md
- Updated README with Cipher installation instructions

### Benefits
- Cross-IDE memory sync (Cursor ↔ VS Code ↔ Claude Code)
- Team shared memory (Workspace Memory)
- Auto-learns development patterns
- Zero configuration setup

## [2.0.0] - 2025-01-02

### Added
- **Capability Boundary Assessment** - Self-evaluate skills before execution
- **Skill Auto-Acquisition** - Integration with skillpkg MCP for on-demand skill learning
- **Failure Mode Diagnosis** - Classify failures into 5 types (Knowledge Gap, Execution Error, Environment Issue, Strategy Error, Resource Limit)
- **Multi-Strategy Mechanism** - Strategy pool to avoid repeating failed approaches
- **Structured Experience Format** - Searchable experience storage for future retrieval
- **Learning Verification** - Verify newly acquired skills before applying

### Changed
- Enhanced PDCA loop with diagnostic feedback
- Improved goal clarity checking with user questionnaire
- Better progress reporting format

## [1.0.0] - 2024-12-31

### Added
- Initial Self-Evolving Agent implementation
- Basic PDCA (Plan-Do-Check-Act) loop
- Memory integration (Core + Archival)
- Goal decomposition and sub-goal tracking
- Reflexion-based learning mechanism
