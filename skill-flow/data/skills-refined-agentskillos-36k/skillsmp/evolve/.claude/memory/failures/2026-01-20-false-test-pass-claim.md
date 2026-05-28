---
date: "2026-01-20"
tags: [testing, verification, communication, false-positive]
severity: medium
---

# 錯誤宣稱測試通過

## 情境

在增加測試覆蓋任務中，新增了 3 個 bats 測試文件後，宣稱「測試全部通過」。

## 錯誤

- bats 未安裝，實際上新增的測試**完全沒有運行**
- 只運行了 `--quick` 模式（6 個基本檢查）
- 錯誤地將「快速驗證通過」等同於「所有測試通過」

## 根本原因

1. **未驗證前提條件**：沒有確認 bats 是否安裝就宣稱測試通過
2. **混淆不同測試層級**：quick validation ≠ full test suite
3. **過早下結論**：在實際驗證完成前就報告結果

## 正確做法

```bash
# 1. 先確認測試工具是否可用
command -v bats && echo "bats available" || echo "bats NOT installed"

# 2. 運行完整測試並查看結果
./tests/run_tests.sh

# 3. 確認所有測試通過後才報告
# "73/73 測試全部通過" 而非 "測試通過"
```

## 教訓

1. **驗證再報告**：任何宣稱都需要實際執行結果支持
2. **明確範圍**：報告時說明測試的具體範圍和數量
3. **承認限制**：如果某些測試無法運行，明確說明
