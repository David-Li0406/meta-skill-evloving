# 06-parallel

多 Session 預設並行模組。

## 內容

| 文件 | 說明 |
|------|------|
| [session-management.md](./_base/session-management.md) | Session 管理與任務鎖機制 |

## 核心功能

1. **預設並行** — 新 Session 自動認領任務
2. **任務鎖** — 防止重複認領
3. **衝突處理** — 檔案衝突自動/手動解決
4. **負載均衡** — 智能任務分配
