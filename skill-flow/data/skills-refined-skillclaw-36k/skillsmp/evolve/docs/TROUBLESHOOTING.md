# 故障排除指南 (Troubleshooting)

> 常見問題及解決方案

## 目錄

- [安裝問題](#安裝問題)
- [執行問題](#執行問題)
- [Memory 問題](#memory-問題)
- [整合問題](#整合問題)

---

## 安裝問題

### `/evolve` 命令沒有反應

**症狀**: 輸入 `/evolve` 後沒有任何回應

**可能原因與解決方案**:

1. **Skill 未安裝**
   ```bash
   # 檢查安裝
   ls -la .claude/skills/evolve/SKILL.md

   # 重新安裝
   curl -fsSL https://raw.githubusercontent.com/miles990/self-evolving-agent/main/install.sh | bash
   ```

2. **Skill 未被載入**
   - 確認 Claude Code 有啟用 skills 功能
   - 重新啟動 Claude Code session

3. **路徑問題**
   ```bash
   # 驗證安裝
   ./scripts/verify-install.sh
   ```

### 安裝腳本失敗

**症狀**: `curl | bash` 執行失敗

**解決方案**:

1. **網路問題**
   ```bash
   # 測試連線
   curl -I https://raw.githubusercontent.com/miles990/self-evolving-agent/main/install.sh
   ```

2. **權限問題**
   ```bash
   # 手動下載並執行
   curl -fsSL https://raw.githubusercontent.com/miles990/self-evolving-agent/main/install.sh -o install.sh
   chmod +x install.sh
   ./install.sh --with-memory
   ```

3. **手動安裝**
   ```bash
   git clone https://github.com/miles990/self-evolving-agent.git
   cp -r self-evolving-agent/skills .claude/skills/evolve
   ```

---

## 執行問題

### 卡在某個步驟不動

**症狀**: 執行中停滯，沒有進度

**解決方案**:

1. **檢查是否等待輸入**
   - 某些操作需要用戶確認
   - 查看是否有 `⏸️ NEED HUMAN` 提示

2. **Context 限制**
   - 長時間執行可能達到 context 上限
   - 嘗試減少 `--max-iterations` 數量

3. **重新開始**
   ```bash
   # 清除狀態後重試
   /evolve [目標] --max-iterations 5
   ```

### 重複執行相同操作

**症狀**: 陷入迴圈，重複嘗試失敗的方法

**解決方案**:

1. **停止條件已達成**
   - 連續 3 次相同錯誤會自動停止
   - 若沒有停止，手動中斷

2. **記憶系統問題**
   ```bash
   # 檢查失敗記錄
   ls -la .claude/memory/failures/

   # 驗證 memory 完整性
   ./scripts/validate-memory.sh
   ```

3. **策略池耗盡**
   - 所有策略都失敗時會停止
   - 考慮簡化目標或尋求幫助

### 編譯/測試失敗無法繼續

**症狀**: CP2 檢查點阻擋繼續執行

**這是預期行為** - CP2 是強制檢查點。

**解決方案**:

1. **修復編譯錯誤**
   - 查看錯誤訊息
   - 修復後重新執行

2. **修復測試失敗**
   - 確認測試本身是否正確
   - 修復程式碼或調整測試

3. **跳過測試（不建議）**
   - 如果確定測試不相關，可手動繼續
   - 但這違反 PDCA 驗證原則

---

## Memory 問題

### index.md 與實際文件不同步

**症狀**: 搜尋找不到已存在的記憶

**解決方案**:

1. **驗證同步狀態**
   ```bash
   ./scripts/validate-memory.sh
   ```

2. **手動同步**
   ```bash
   # 列出所有 memory 文件
   find .claude/memory -name "*.md" -type f

   # 手動更新 index.md
   ```

3. **預防**
   - 創建 memory 後**立即**更新 index.md（CP3.5）
   - 使用標準操作流程

### Memory 文件格式錯誤

**症狀**: 搜尋結果異常或解析失敗

**解決方案**:

1. **檢查 frontmatter**
   ```yaml
   ---
   date: YYYY-MM-DD
   tags: [tag1, tag2]
   status: resolved | unresolved
   ---
   ```

2. **修復格式**
   - 確保 YAML frontmatter 正確
   - 確保使用 UTF-8 編碼

### Memory 目錄不存在

**症狀**: 找不到 `.claude/memory/`

**解決方案**:

```bash
# 初始化 memory 系統
mkdir -p .claude/memory/{learnings,failures,decisions,patterns,strategies,discoveries}

# 創建 index.md
cat > .claude/memory/index.md << 'EOF'
# 專案記憶索引

> Last curated: $(date +%Y-%m-%d)

## 最近學習
<!-- LEARNINGS_START -->
<!-- LEARNINGS_END -->

## 失敗經驗
<!-- FAILURES_START -->
<!-- FAILURES_END -->
EOF
```

---

## 整合問題

### Plugin 安裝失敗

**症狀**: `/plugin install` 失敗

**解決方案**:

1. **確認 marketplace 已添加**
   ```bash
   # 先添加 marketplace
   /plugin marketplace add miles990/self-evolving-agent

   # 再安裝
   /plugin install evolve@self-evolving-agent
   ```

2. **檢查網路**
   ```bash
   curl -I https://github.com/miles990/self-evolving-agent
   ```

### MCP 工具無法使用

**症狀**: PAL、spec-workflow 工具不可用

**解決方案**:

1. **確認 MCP 配置**
   - 檢查 Claude Code 的 MCP 設定
   - 確認對應的 MCP server 已啟用

2. **重新配置**
   - 參考各 MCP 的官方文檔
   - 確認 API key 或憑證設定

### Hooks 沒有觸發

**症狀**: PostToolUse 或 Stop hooks 不執行

**解決方案**:

1. **檢查 hooks 配置**
   ```bash
   cat .claude/settings.local.json
   ```

2. **重新設定**
   ```bash
   ./scripts/setup-hooks.sh
   ```

3. **確認 hook 命令可執行**
   - 測試 hook 中的命令是否能獨立執行

---

## 取得更多幫助

如果以上方案都無法解決問題：

1. **查看詳細文檔**
   - [USAGE.md](./USAGE.md)
   - [skills/SKILL.md](../skills/SKILL.md)

2. **搜尋相關經驗**
   ```bash
   grep -r "錯誤關鍵字" .claude/memory/
   ```

3. **提交 Issue**
   - [GitHub Issues](https://github.com/miles990/self-evolving-agent/issues)
   - 請附上錯誤訊息和執行環境資訊

4. **社群討論**
   - 查看其他用戶的經驗分享
