---
name: openapi-sdk-generation
description: >-
  當後端 API 有變更或 mobile SDK 型別不一致時，更新 repo 內的 OpenAPI snapshot（openapi/openapi.json），並在 apps/mobile 重新生成 hey-api/openapi-ts SDK、清理舊產物、進行 type-check 驗證。也適用於 CI/雲端 agent 需要用 repo snapshot 穩定 codegen 的情境。
---

# OpenAPI / Mobile SDK 生成 Skill

## 何時使用

在出現以下任一情況時使用本 skill：

- 你修改了後端 FastAPI router / request / response schema（新增/刪除/改參數、改 envelope 型別等）
- Mobile 端 SDK 型別看起來落後（例如缺少新 endpoint、型別不一致、IDE 自動完成不對）
- CI/雲端 agent 無法依賴 `localhost` 或內網取得 OpenAPI，需要使用 repo 內 snapshot 做 codegen

## 目標

- 更新 repo snapshot：`openapi/openapi.json`
- 以 snapshot 重新生成 mobile SDK（hey-api/openapi-ts）
- 以 `npm run type-check` 驗證型別

## 核心原則（務必遵守）

- OpenAPI codegen 的輸入來源一律使用 repo snapshot：`openapi/openapi.json`
- 變更後端 API 時，先更新 snapshot 再動前端（避免前端以過期型別開發）
- `generated/` 產物不要手動修改；若需修正，以「修改後端 → regenerate snapshot → regenerate SDK」為準
- Git 提交時：只提交 `openapi/openapi.json`；SDK 生成輸出目錄不要 commit（已在 `.gitignore`）

## Step-by-step 流程

### Step 0：前置確認

- 你已完成後端 API 修改（或你正在修復 SDK/型別不一致問題）
- 若你只是要重生 SDK（沒改後端）：仍建議先確認 `openapi/openapi.json` 是最新（必要時先 regenerate）

### Step 1：更新 OpenAPI snapshot（推薦路徑）

在 repo 根目錄執行：

```bash
make generate-openapi
```

可選替代方案（在 apps/backend）：

```bash
cd apps/backend
poetry run python scripts/generate_openapi.py
```

最小依賴 fallback（不需要 Poetry；適合自動化/agent 環境）：

```bash
cd apps/backend
pip3 install fastapi pydantic sqlalchemy injector asyncpg python-jose passlib bcrypt email-validator google-auth google-cloud-storage firebase-admin httpx python-multipart
python3 scripts/generate_openapi.py
```

成功判準：`openapi/openapi.json` 的內容已更新，且是有效 JSON。

### Step 2：在 mobile 端清理並重新生成 SDK

```bash
cd apps/mobile
npm run sdk:clean
npm run sdk:generate
```

成功判準：SDK 生成流程完成且沒有錯誤。

### Step 3：驗證型別

```bash
cd apps/mobile
npm run type-check
```

成功判準：type-check 通過。

### Step 4：提交規則（重要）

只提交 snapshot：

```bash
git add openapi/openapi.json
```

不要提交 SDK 生成輸出（通常是 `apps/mobile/generated/` 之類的目錄，且已被忽略）。

## 常見問題 / 排錯

### 1) `/api/v1/api/v1/...` 路徑重複

後端 OpenAPI paths 已包含 `/api/v1`，因此 mobile 端的 `baseUrl` 應使用 host-only（例如 `http://localhost:8080`），不要把 `/api/v1` 再加進 baseUrl。

### 2) OpenAPI snapshot 看起來沒變、但後端明明改了

- 確認你修改的是被 FastAPI app 掛載到 OpenAPI 的 router
- 重新跑一次 `make generate-openapi`
- 檢查是否有條件式路由/設定導致該端點沒有被載入

### 3) 生成失敗：`ModuleNotFoundError: No module named 'fastapi'`

- 推薦：使用 Poetry 方法（`cd apps/backend && poetry install` 後再跑 generate script）
- 或使用最小依賴 pip 安裝的 fallback

## 觸發本 skill 的建議提問方式（範例）

- 「我剛改了後端 API，請更新 openapi snapshot 並重生 mobile SDK，最後跑 type-check」
- 「CI 報 SDK 型別不一致，請用 repo 的 openapi/openapi.json 重新 generate SDK 並驗證」
- 「請依照專案規範：先 make generate-openapi，再在 apps/mobile 跑 sdk:clean / sdk:generate / type-check」
