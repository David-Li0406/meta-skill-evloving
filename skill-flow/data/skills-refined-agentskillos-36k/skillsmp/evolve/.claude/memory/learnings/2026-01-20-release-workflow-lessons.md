---
date: "2026-01-20"
tags: [release, macos, sed, plugin-cache, bash, version-update]
---

# 版本發布工作流教訓

## 情境

執行 v5.9.2 發布時遇到多個技術問題。

## 教訓 1: macOS sed 正則表達式

**問題**: `sed -i '' "s/[0-9]\+/.../"` 在 macOS 上不工作

**原因**: macOS sed 預設使用 BRE (Basic Regular Expression)，`\+` 是 GNU sed 的 BRE 擴展，macOS 不支援

**解決方案**:
```bash
# ❌ 錯誤 - macOS 不支援
sed -i '' "s/[0-9]\+\.[0-9]\+/.../"

# ✅ 正確 - 使用 -E 啟用 ERE
sed -i '' -E "s/[0-9]+\.[0-9]+/.../"
```

**記住**: macOS sed 用 `-E`，Linux sed 用 `-r` 來啟用 ERE

## 教訓 2: cp 不複製隱藏目錄

**問題**: `cp -r source/* dest/` 不會複製 `.hidden` 目錄

**原因**: Shell glob `*` 預設不匹配以 `.` 開頭的檔案/目錄

**解決方案**:
```bash
# 方法 1: 分開複製
cp -r source/* dest/
cp -r source/.hidden dest/

# 方法 2: 使用 rsync
rsync -av source/ dest/

# 方法 3: 設定 shell 選項 (bash)
shopt -s dotglob
cp -r source/* dest/
```

## 教訓 3: Plugin Cache 更新流程

**正確流程**:
1. 清除舊 cache: `rm -rf ~/.claude/plugins/cache/<plugin-name>`
2. 建立版本目錄: `mkdir -p ~/.claude/plugins/cache/<plugin-name>/<skill>/<version>`
3. 複製所有檔案（包括隱藏目錄）
4. 驗證 `.claude-plugin/plugin.json` 存在且版本正確

**驗證命令**:
```bash
cat ~/.claude/plugins/cache/<plugin>/evolve/<version>/.claude-plugin/plugin.json
```

## 改進建議

考慮在 `install.sh` 中增加全域 plugin 安裝選項：
```bash
./install.sh --global  # 安裝到 ~/.claude/plugins/cache/
./install.sh           # 安裝到當前專案 .claude/skills/
```
