<overview>
本文件定義 WASDE Ingestor 可能遇到的失敗模式及其緩解策略。
</overview>

<failure_categories>
**失敗模式分類**

| 類別 | 說明 | 嚴重程度 |
|------|------|----------|
| Network | 網路連線問題 | Low |
| Parse | PDF/HTML 解析失敗 | Medium |
| Schema | 表格結構變化 | High |
| Validation | 數據驗證失敗 | Medium |
| System | 系統資源問題 | Low |
</failure_categories>

<network_failures>
**Network 失敗模式**

**F001: Connection Timeout**
```yaml
id: F001
symptom: "連線 USDA 網站超時"
causes:
  - USDA 伺服器負載過高（發布日當天）
  - 網路不穩定
  - 防火牆阻擋

mitigation:
  - retry:
      max_attempts: 5
      backoff: [1, 2, 4, 8, 16]  # exponential backoff
  - alternative_source:
      - "https://usda.library.cornell.edu/"
      - "https://esmis.nal.usda.gov/"

recovery:
  - "等待 5-10 分鐘後重試"
  - "使用備用數據源"
```

**F002: HTTP 404 Not Found**
```yaml
id: F002
symptom: "報告 URL 返回 404"
causes:
  - URL 結構變更
  - 報告尚未發布
  - 檔案名稱格式改變

mitigation:
  - discover_url:
      description: "重新發現報告 URL"
      pattern: "/wasde/wasde{YYMM}.pdf"
  - check_release_calendar:
      url: "https://www.usda.gov/oce/commodity/wasde"

recovery:
  - "確認發布日期是否正確"
  - "嘗試不同的 URL pattern"
```

**F003: SSL Certificate Error**
```yaml
id: F003
symptom: "SSL 憑證驗證失敗"
causes:
  - 憑證過期
  - 中間人攻擊（罕見）
  - 本地時間錯誤

mitigation:
  - verify_ssl: true  # 不要關閉 SSL 驗證
  - check_system_time: true
  - use_alternative_source: true

recovery:
  - "檢查系統時間是否正確"
  - "更新 CA 憑證"
```
</network_failures>

<parse_failures>
**Parse 失敗模式**

**F101: PDF Layout Break**
```yaml
id: F101
symptom: "PDF 解析返回斷裂欄位或合併列"
causes:
  - PDF 生成工具變更
  - 表格跨頁
  - 特殊字元

mitigation:
  - fallback_parser:
      order: ["pdfplumber", "camelot", "tabula"]
  - html_fallback:
      enabled: true
      url_pattern: "https://www.usda.gov/oce/commodity/wasde/"
  - row_reconstruction:
      description: "啟發式列重建"
      enabled: true

recovery:
  - "嘗試不同的 PDF 解析器"
  - "切換到 HTML 解析"
  - "人工檢查並標記異常"

diagnostics:
  output:
    - "raw_extraction.json"
    - "problematic_pages.txt"
```

**F102: Table Not Found**
```yaml
id: F102
symptom: "找不到指定的表格"
causes:
  - 表格標題變更
  - 表格被移除
  - 頁碼變化

mitigation:
  - fuzzy_match:
      enabled: true
      threshold: 0.8  # 80% 相似度
      aliases:
        - "U.S. Soybeans Supply and Use"
        - "Soybeans: U.S. Supply and Use"
        - "US SOYBEANS SUPPLY AND USE"
  - page_scan:
      description: "掃描所有頁面尋找表格"
      enabled: true

recovery:
  - "使用模糊匹配搜尋"
  - "記錄失敗並通知維護者"

diagnostics:
  output:
    - "available_tables.json"
    - "search_log.txt"
```

**F103: Column Mismatch**
```yaml
id: F103
symptom: "欄位數量或名稱與預期不符"
causes:
  - USDA 新增或刪除欄位
  - 欄位重命名
  - 表格格式調整

mitigation:
  - flexible_mapping:
      enabled: true
      strategy: "best_effort"
  - column_aliases:
      use_aliases: true
      warn_on_missing: true

recovery:
  - "使用欄位別名映射"
  - "記錄新增/刪除的欄位"
  - "更新欄位映射配置"

diagnostics:
  output:
    - "column_diff.json"
    - "mapping_result.json"
```

**F104: Numeric Parse Error**
```yaml
id: F104
symptom: "數值解析失敗"
causes:
  - 千分位符號（1,234 vs 1234）
  - 負數表示法（(100) vs -100）
  - 特殊值（N/A, -, *)

mitigation:
  - number_patterns:
      thousands_sep: [",", " "]
      decimal_sep: ["."]
      negative_formats: ["()", "-", "−"]
      null_values: ["N/A", "-", "*", "--", "n.a."]

recovery:
  - "嘗試多種數值格式"
  - "將無法解析的值標記為 null"
```
</parse_failures>

<schema_failures>
**Schema 失敗模式**

**F201: Schema Drift**
```yaml
id: F201
symptom: "表格結構與基準不同"
severity: high
causes:
  - USDA 調整報告格式
  - 新增商品或細分
  - 合併或刪除表格

detection:
  - schema_hash_check: true
  - column_count_check: true
  - column_name_check: true

mitigation:
  - on_minor_drift:  # 新增欄位
      action: "warn_and_continue"
      include_new_columns: true
  - on_major_drift:  # 刪除或重命名
      action: "fail_with_report"
      create_issue: true

recovery:
  - "檢查 USDA 公告是否有格式變更說明"
  - "更新欄位映射配置"
  - "開立 GitHub issue 追蹤"

diagnostics:
  output:
    - "schema_diff_report.json"
    - "migration_guide.md"
```

**F202: Marketing Year Format Change**
```yaml
id: F202
symptom: "行銷年度格式變更"
causes:
  - "2024/25" → "24/25"
  - "2024-25" → "2024/25"

mitigation:
  - flexible_parsing:
      patterns:
        - "\\d{4}/\\d{2}"   # 2024/25
        - "\\d{2}/\\d{2}"   # 24/25
        - "\\d{4}-\\d{2}"   # 2024-25
        - "\\d{4}"          # 2024

recovery:
  - "嘗試多種格式解析"
  - "標準化為 YYYY/YY 格式"
```
</schema_failures>

<validation_failures>
**Validation 失敗模式**

**F301: Balance Check Failed**
```yaml
id: F301
symptom: "供需平衡公式驗證失敗"
causes:
  - 解析錯誤
  - 統計殘差超出預期
  - 單位錯誤

mitigation:
  - tolerance_adjustment:
      default: 1.0
      allow_override: true
  - residual_handling:
      include_residual: true
      max_residual_pct: 5.0

recovery:
  - "檢查是否有遺漏的欄位"
  - "調整容許誤差"
  - "人工檢查原始報告"

diagnostics:
  output:
    - "balance_check_details.json"
```

**F302: Value Out of Range**
```yaml
id: F302
symptom: "數值超出合理範圍"
causes:
  - 解析錯誤（小數點位置）
  - 單位錯誤
  - 實際異常值

mitigation:
  - range_check:
      mode: "warn"  # warn | fail | skip
      log_anomalies: true
  - historical_comparison:
      enabled: true
      z_score_threshold: 3.0

recovery:
  - "與歷史數據比較"
  - "檢查單位是否正確"
  - "標記為待人工確認"
```

**F303: Partial Data**
```yaml
id: F303
symptom: "部分數據缺失"
causes:
  - 只找到 US 表格，缺少 World
  - 部分商品解析失敗

mitigation:
  - partial_output:
      enabled: true
      when: "scope_allows"  # 當配置允許部分輸出
  - fail_if_required:
      check_scope: true

recovery:
  - "輸出可用數據並標記缺失"
  - "或根據配置完全失敗"
```
</validation_failures>

<system_failures>
**System 失敗模式**

**F401: Disk Space**
```yaml
id: F401
symptom: "磁碟空間不足"
mitigation:
  - pre_check:
      min_free_space_mb: 500
  - cleanup:
      remove_temp_files: true
      compress_old_reports: true
```

**F402: Memory Error**
```yaml
id: F402
symptom: "記憶體不足"
mitigation:
  - streaming_parse:
      enabled: true
      chunk_size: 1000
  - gc_aggressive:
      enabled: true
```

**F403: Permission Denied**
```yaml
id: F403
symptom: "檔案寫入權限不足"
mitigation:
  - pre_check:
      test_write: true
  - fallback_dir:
      use_temp: true
```
</system_failures>

<error_handling_strategy>
**錯誤處理策略**

```python
class IngestError(Exception):
    def __init__(self, error_id, message, recoverable=True, diagnostics=None):
        self.error_id = error_id
        self.message = message
        self.recoverable = recoverable
        self.diagnostics = diagnostics or {}

def handle_error(error: IngestError, config):
    """統一錯誤處理"""

    # 記錄錯誤
    log_error(error)

    # 輸出診斷資訊
    if error.diagnostics:
        write_diagnostics(error.diagnostics, config.output_dir)

    # 根據可恢復性決定行為
    if error.recoverable and config.allow_partial:
        return {"status": "partial", "error": error}
    else:
        raise error
```

**重試配置：**
```yaml
retry_config:
  network_errors: [F001, F002, F003]
  max_retries: 5
  backoff_strategy: "exponential"
  initial_delay_seconds: 1

  parse_errors: [F101, F102, F103, F104]
  max_retries: 2
  fallback_enabled: true

  schema_errors: [F201, F202]
  max_retries: 0  # 不重試，直接報告
  create_issue: true

  validation_errors: [F301, F302, F303]
  max_retries: 0
  allow_partial: true
```
</error_handling_strategy>
