# Project Claude Initializer Skill

快速為專案建立標準化的 `.claude` 配置目錄。

## 🚀 快速開始

### 觸發關鍵字
- 「初始化 Claude 配置」
- 「設定專案 Claude」
- 「為這個專案建立 .claude 目錄」
- 「幫我設定專案的 Claude Code」

### 功能
✅ 自動掃描專案資訊（package.json, pyproject.toml 等）
✅ 智慧生成 CLAUDE.md 專案指引
✅ 建立標準 .gitignore
✅ 支援技術棧自動偵測
✅ 安全處理現有配置

## 🔒 安全保證

### 絕對不會做的事
- ❌ 覆蓋現有 settings.json
- ❌ 刪除或修改現有技能
- ❌ 未經詢問覆蓋 CLAUDE.md
- ❌ 刪除任何使用者資料

### 會做的事
- ✅ 檢查現有配置
- ✅ 詢問使用者意見
- ✅ 提供備份選項
- ✅ 保留所有自訂內容

## 📋 支援的專案類型

| 類型 | 偵測檔案 | 自動提取 |
|------|---------|---------|
| Node.js/React/Vue | package.json | 名稱、依賴、指令 |
| Python/FastAPI/Django | pyproject.toml, requirements.txt | 框架、依賴 |
| Go | go.mod | 模組資訊 |
| Rust | Cargo.toml | 專案資訊 |
| Java | pom.xml, build.gradle | 專案配置 |

## 🎯 使用場景

### 場景 1：全新專案
```bash
cd ~/new-project
claude
```
> 「初始化 Claude 配置」

結果：
- ✅ 建立完整 .claude 目錄
- ✅ 生成 CLAUDE.md
- ✅ 建立 .gitignore

### 場景 2：現有專案（無配置）
```bash
cd ~/existing-project
claude
```
> 「設定專案 Claude」

結果：
- ✅ 掃描專案資訊
- ✅ 自動填充技術棧
- ✅ 提取常用指令

### 場景 3：已有部分配置
```bash
cd ~/project-with-partial-config
claude
```
> 「初始化 Claude 配置」

結果：
- ✅ 保留現有檔案
- ✅ 只建立缺失部分
- ✅ 告知保留了什麼

### 場景 4：團隊專案
```bash
cd ~/team-project
claude
```
> 「初始化 Claude 配置」

結果：
- ⚠️  偵測為團隊專案
- 💡 提示謹慎操作
- ✅ 提供「唯讀檢視」選項

## 📦 產出結構

```
.claude/
├── .gitignore           # 排除運行時檔案
├── CLAUDE.md            # 專案指引（自動生成）
├── skills/              # 空目錄（可選）
└── plans/               # 空目錄（可選）
```

## 🎨 CLAUDE.md 內容

自動生成的專案指引包含：

```markdown
# [專案名稱]

## 專案簡介
[自動提取或使用者輸入]

## 技術棧
[自動偵測]
- 前端：React 18 + TypeScript
- 建置工具：Vite
- 測試：Vitest

## 專案結構
[自動掃描]

## 開發規範
[根據技術棧提供建議]

## 常用指令
[從 package.json 自動提取]

## 特殊注意事項
[預留給使用者填寫]
```

## 🔄 處理流程

```
1. 檢查當前目錄
   ↓
2. 檢查現有配置 ← 🔒 安全關鍵
   ↓
3. 掃描專案資訊
   ↓
4. 詢問使用者確認
   ↓
5. 建立配置檔案
   ↓
6. 提供後續步驟
```

## 💡 智慧功能

### 技術棧自動偵測
根據依賴自動識別：
- React, Vue, Next.js, Nuxt
- Express, Fastify, NestJS
- FastAPI, Django, Flask
- 測試框架、UI 庫等

### 指令自動提取
從 `package.json` scripts 提取：
```json
{
  "scripts": {
    "dev": "vite",      → npm run dev
    "build": "vite build",  → npm run build
    "test": "vitest"    → npm test
  }
}
```

### 規範智慧建議
根據技術棧提供相應規範：
- React → TypeScript strict mode, 元件規範
- Python → PEP 8, type hints
- Go → gofmt, golint

## 🤝 團隊共享

### 方式 1：專案配置（推薦）
配置會加入專案 git，團隊成員 clone 後自動獲得。

```bash
git add .claude/
git commit -m "docs: 初始化 Claude Code 配置"
git push
```

### 方式 2：複製此 skill
團隊成員可複製這個 skill 到自己的環境：

```bash
# 複製 skill 資料夾
cp -r ~/.claude/skills/project-claude-initializer ~/.claude/skills/

# 或 clone 整個配置倉庫
git clone https://github.com/Jimmy1987s/.claude.git ~/.claude
```

### 方式 3：手動分享
直接傳送 `SKILL.md` 檔案給團隊成員。

## ⚠️ 注意事項

1. **檢查後再執行**
   - 先檢查現有配置
   - 詢問使用者意見
   - 提供預覽和取消選項

2. **保守策略**
   - 有疑問時保留現有內容
   - 不確定時詢問使用者
   - 提供備份選項

3. **透明操作**
   - 明確告知每個步驟
   - 顯示將要修改的內容
   - 確認操作結果

4. **團隊友善**
   - 偵測團隊專案時特別謹慎
   - 提醒與團隊討論
   - 提供唯讀檢視選項

## 🐛 故障排除

### Q: Skill 沒有執行？
A: 確認觸發關鍵字是否正確，或直接說「使用 project-claude-initializer skill」

### Q: 自動偵測失敗？
A: Skill 會詢問你手動輸入專案資訊，使用通用模板

### Q: 擔心覆蓋現有配置？
A: 不用擔心！Skill 會先檢查並詢問你，預設選項是「保留現有」

### Q: 如何更新現有配置？
A: 說「更新專案 Claude 配置」，Skill 會提供更新選項

## 📚 相關資源

- [完整 Skill 說明](SKILL.md)
- [多工作區指南](../../docs/workspace/WORKSPACE_GUIDE.md)
- [專案模板](../../docs/workspace/templates/project-claude-template/)

## 🎉 範例輸出

```
✓ 已檢查專案資訊
  專案名稱：my-web-app
  技術棧：React 18 + TypeScript + Vite

✓ 已建立 .claude 目錄結構
✓ 已建立 .claude/.gitignore
✓ 已建立 .claude/CLAUDE.md（自動填充）
✓ 已建立 .claude/skills/（空目錄）

專案配置已完成！

下一步：
1. 檢視 .claude/CLAUDE.md 並調整
2. 提交：git add .claude/ && git commit -m "docs: 初始化 Claude Code 配置"
3. 開始使用：claude（自動讀取配置）

團隊共享：
- 配置已加入專案 git
- 團隊成員 clone 後自動獲得
- 個人設定可用 settings.local.json
```

## 版本

- v1.0.0 (2026-01-10) - 初始版本
- v1.1.0 (2026-01-10) - 增強安全性，詳細情況處理
