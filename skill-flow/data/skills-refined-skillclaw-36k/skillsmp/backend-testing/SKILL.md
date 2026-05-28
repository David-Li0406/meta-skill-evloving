---
name: backend-testing
description: >-
  執行與除錯 KCardSwap 後端測試（pytest）：支援快速跑全套、只跑 unit/integration、單一檔案或單一測試、失敗重跑、最慢測試統計、coverage 報告，以及 gcs_smoke（RUN_GCS_SMOKE=1）等情境。也包含本機 Poetry 與 Makefile 的推薦指令與注意事項。
---

# Backend Testing Skill (pytest)

## 何時使用

- 你改了後端 use case / repository / router / schema，想快速確認沒壞
- CI 報測試失敗，你想在本機快速重現與縮小範圍
- 想針對單一模組或單一測試用例跑迭代（TDD）
- 想跑 coverage 或找出最慢的測試

## 預設策略（推薦）

- **優先用 Poetry 環境跑測試**（`poetry run pytest`）
  - 原因：後端 Docker container 的啟動腳本只安裝 main dependencies（不含 pytest/ruff 等 dev deps），因此「直接在目前的 backend 容器內跑 pytest」通常不可行。
- 測試 root 位置：`apps/backend`

## 最常用指令

> 下列命令都假設你在 repo 根目錄；若你已在 `apps/backend`，可省略 `cd apps/backend`。

### 1) 跑全套（最常用）

```bash
cd apps/backend
poetry run pytest -v
```

### 2) 只跑 unit 或 integration

```bash
# Unit
cd apps/backend
poetry run pytest -v tests/unit

# Integration
cd apps/backend
poetry run pytest -v tests/integration
```

### 3) 跑單一檔案 / 單一測試

```bash
# 單一檔案
cd apps/backend
poetry run pytest -v tests/unit/posts/test_create_post_use_case.py

# 單一測試（用節點表示法）
cd apps/backend
poetry run pytest -v tests/test_main.py::test_api_health_check
```

### 4) 以關鍵字篩選（快速縮小範圍）

```bash
cd apps/backend
poetry run pytest -v -k "profile or login"
```

### 5) 失敗重跑 / 快速迭代

```bash
# 只跑上次失敗的測試
cd apps/backend
poetry run pytest -v --lf

# 先跑上次失敗的，再跑其他（適合修完後確認）
cd apps/backend
poetry run pytest -v --ff
```

### 6) 看到最慢的測試（效能排查）

```bash
cd apps/backend
poetry run pytest -v --durations=10
```

### 7) 快速 fail-fast（縮短回饋時間）

```bash
cd apps/backend
poetry run pytest -v -x
# 或：poetry run pytest -v --maxfail=1
```

## Coverage（pytest-cov）

此專案已安裝 `pytest-cov`（dev dependencies）。常用命令：

```bash
cd apps/backend
poetry run pytest -v --cov=app --cov-report=term-missing
```

需要 HTML 報告：

```bash
cd apps/backend
poetry run pytest -v --cov=app --cov-report=html
```

成功判準：終端機出現 coverage summary，或生成 `htmlcov/`。

## 特殊情境：GCS smoke tests

- 專案定義了 `gcs_smoke` marker，並建議只在設定 `RUN_GCS_SMOKE=1` 時執行。
- 一般開發/CI 的 unit/integration 測試應使用 Mock GCS。

執行方式：

```bash
cd apps/backend
RUN_GCS_SMOKE=1 poetry run pytest -v -m gcs_smoke
```

注意：如果沒有任何測試實際標記 `@pytest.mark.gcs_smoke`，上述命令會跑不到測試；此時應以目前既有測試為準。

## Makefile 對應指令

- 你也可以用 repo 根目錄的 Makefile：

```bash
make test
```

注意：`make test` 目前是直接呼叫 `pytest -v`（不經 `poetry run`）。若你不是在已啟用 dev venv 的環境，可能會找不到 pytest；此時請改用本 skill 的 Poetry 指令。

## 已知限制 / 待改善點（如需可再做成另一個 skill）

- `apps/backend/tests/conftest.py` 內的 testcontainers fixture 目前是 `pytest.skip("Testcontainers not yet configured")`。
  - 若你想讓「需要資料庫容器的整合測試」真正跑起來，需要補上 `testcontainers[postgres]` 並解除註解。

## 觸發本 skill 的建議提問方式（範例）

- 「請用 Poetry 跑後端全套測試，失敗就用 --lf 重跑」
- 「只跑 posts 模組的 unit tests，並列出最慢 10 個」
- 「幫我跑這個單一測試並用 -x fail-fast」
- 「我要跑 coverage（term-missing + html）」
