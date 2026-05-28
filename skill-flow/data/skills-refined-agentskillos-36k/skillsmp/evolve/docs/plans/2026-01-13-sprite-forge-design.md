# SpriteForge - 2D 轉 2.5D 遊戲素材工具

> 設計文件 v1.0 | 2026-01-13

## 專案概述

**目標**：上傳一張角色圖片，自動生成 8 方向 sprite，並在 Flame 引擎中即時預覽。

**技術棧**：
- **後端**：Python FastAPI + Celery + Redis
- **前端**：Flutter + Flame
- **AI 模型**：Qwen-Image-Edit-2511 + Multiple-Angles LoRA（透過 HF API）
- **儲存**：S3/R2/MinIO + CDN

**定位**：Side project，但保留可靠、可擴展、可維護的架構。

---

## 系統架構

```
┌─────────────────────────────────────────────────────────────────┐
│                    SpriteForge 架構圖                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                 Flutter App (全平台)                      │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────────────┐  │   │
│  │  │ 圖片上傳   │  │ 參數設定   │  │ Flame 預覽引擎    │  │   │
│  │  │ → S3直傳   │  │ (preset/   │  │ (即時顯示每張     │  │   │
│  │  │ presigned  │  │  seed/bg)  │  │  透過 SSE 推送)   │  │   │
│  │  └────────────┘  └────────────┘  └────────────────────┘  │   │
│  │              │                       ▲                    │   │
│  │              │         SSE: job.partial_result            │   │
│  │              ▼                       │                    │   │
│  │        ┌─────────────────────────────┴──┐                 │   │
│  │        │   JobRepository + SSEClient    │                 │   │
│  │        └─────────────────┬──────────────┘                 │   │
│  └──────────────────────────┼────────────────────────────────┘   │
│                             │                                    │
│  ┌──────────────────────────▼────────────────────────────────┐   │
│  │            Python Backend (FastAPI) - Stateless           │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │   │
│  │  │ POST /jobs   │  │ GET /jobs/id │  │ SSE /events  │     │   │
│  │  │ 建立任務     │  │ 查狀態/進度  │  │ Redis Stream │     │   │
│  │  └──────┬───────┘  └──────┬───────┘  └──────▲───────┘     │   │
│  │         │                 │                 │             │   │
│  │         ▼                 ▼                 │             │   │
│  │  ┌────────────────────────────────────────────────────┐   │   │
│  │  │                    Redis                           │   │   │
│  │  │  • job:{id}:meta (Hash)     - 任務元資料           │   │   │
│  │  │  • job:{id}:results (Hash)  - 各方向結果           │   │   │
│  │  │  • job:{id}:events (Stream) - 事件序列（可回放）   │   │   │
│  │  │  • job:queue (List)         - 任務佇列             │   │   │
│  │  └────────────────────────┬───────────────────────────┘   │   │
│  └───────────────────────────┼───────────────────────────────┘   │
│                              │                                   │
│  ┌───────────────────────────▼───────────────────────────────┐   │
│  │              Worker (Celery + asyncio)                    │   │
│  │  ┌────────────────────────────────────────────────────┐   │   │
│  │  │  1. 從 Queue 取任務                                │   │   │
│  │  │  2. 下載原圖 (s3.download(source_key))             │   │   │
│  │  │  3. 併發調用 HF API (Semaphore=3)                  │   │   │
│  │  │  4. 每完成一張 → 上傳 S3 + XADD 事件               │   │   │
│  │  │  5. 全部完成 → 打包 ZIP + 更新狀態                 │   │   │
│  │  └────────────────────────────────────────────────────┘   │   │
│  └───────────────────────────────────────────────────────────┘   │
│                              │                                   │
│         ┌────────────────────┼────────────────────┐              │
│         ▼                    ▼                    ▼              │
│  ┌─────────────┐   ┌─────────────────────┐   ┌─────────────┐     │
│  │  S3 / R2    │   │  Hugging Face API   │   │  CDN        │     │
│  │  (MinIO)    │   │  Qwen-Image-Edit    │   │  (圖片快取) │     │
│  └─────────────┘   └─────────────────────┘   └─────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

---

## API 設計

### Endpoints

```yaml
# GET /api/upload/presign
# 取得上傳用 presigned URL
Response:
  upload_url: string        # S3 presigned PUT URL
  source_key: string        # 給 POST /jobs 用
  expires_at: string

---

# POST /api/jobs
# 建立生成任務
Request:
  source_key: string        # 從 /upload/presign 取得（不接受任意 URL）
  preset: "rpgmaker_8dir" | "rpgmaker_4dir" | "custom"
  angles: number[]          # 僅 preset=custom 時使用
  seed: number | null       # 可重現（null = random）
  bg: "transparent" | "keep"
  output_format: "frames" | "sheet" | "atlas"
  rig_version: "v1"         # 相機參數版本
  camera_rig:               # 可選
    distance: number
    elevation: number
    fov: number

Response:
  job_id: string
  status: "queued"
  event_url: string         # /api/events?job_id=...
  job_url: string           # /api/jobs/{id}
  export_url: string        # /api/jobs/{id}/export
  created_at: string

---

# GET /api/jobs/{job_id}
Response:
  job_id: string
  status: "queued" | "processing" | "completed" | "completed_with_errors" | "failed" | "canceled"
  stage: "uploading" | "generating" | "packing" | "done"
  progress:
    done: number
    total: number
    percent: number
  results:
    - index: number
      direction: string     # "F", "FR", ...
      angle: number
      state: "pending" | "processing" | "success" | "failed"
      image_url: string | null
      thumb_url: string | null
      error: string | null
  failed_directions: string[]
  has_errors: boolean
  error: { code: string, message: string } | null

---

# GET /api/jobs/{job_id}/export
Response:
  download_url: string      # ZIP 下載 URL
  metadata_url: string      # atlas.json URL
  expires_at: string

---

# POST /api/jobs/{job_id}/retry
# 只重試失敗的方向
Request:
  directions: string[] | null  # null = 全部失敗的
Response:
  status: "queued"
  retrying_directions: string[]

---

# POST /api/jobs/{job_id}/cancel
Response:
  status: "canceled" | "cancel_requested"
```

### SSE 事件流

```yaml
# GET /api/events?job_id=xxx
# Server-Sent Events (Redis Streams 可回放)

id: 1705123456789-0
event: job.created
data: { job_id, status, event_url, job_url, export_url }

id: 1705123456790-0
event: job.started
data: { job_id, stage: "generating" }

id: 1705123456791-0
event: job.progress
data: { job_id, done: 3, total: 8, percent: 37.5, current_direction: "R" }

id: 1705123456792-0
event: job.partial_result
data: { job_id, index: 2, direction: "R", angle: 90, thumb_url: "..." }

id: 1705123456800-0
event: job.completed
data: { job_id, status: "completed", download_url: "...", has_errors: false }

# 或
event: job.completed_with_errors
data: { job_id, status: "completed_with_errors", failed_directions: ["BR"], ... }

event: job.failed
data: { job_id, status: "failed", error: { code, message } }
```

### 方向定義

| 方向 | 代碼 | Azimuth | 說明 |
|------|------|---------|------|
| Front | F | 0° | 面向鏡頭 |
| Front-Right | FR | 45° | |
| Right | R | 90° | |
| Back-Right | BR | 135° | |
| Back | B | 180° | 背對鏡頭 |
| Back-Left | BL | 225° | |
| Left | L | 270° | |
| Front-Left | FL | 315° | |

**Presets**:
- `rpgmaker_8dir`: F, FR, R, BR, B, BL, L, FL
- `rpgmaker_4dir`: F, R, B, L

---

## Redis Schema

```
job:{id}:meta (Hash, TTL: 30d)
  status        : string
  stage         : string
  preset        : string
  seed          : number
  rig_version   : string
  source_key    : string
  created_at    : timestamp
  updated_at    : timestamp
  cancel_requested : bool

job:{id}:results (Hash, TTL: 30d)
  F   : { state, image_url, thumb_url, error }
  FR  : { ... }
  ...

job:{id}:events (Stream, TTL: 7d)
  用於 SSE 回放

job:queue (List)
  待處理 job_id
```

---

## Export ZIP 結構

```
sprite-{job_id}.zip
├── frames/
│   ├── F.png
│   ├── FR.png
│   ├── R.png
│   ├── BR.png      # 如果失敗則不存在
│   ├── B.png
│   ├── BL.png
│   ├── L.png
│   └── FL.png
├── sheet.png       # 橫排或 grid
├── atlas.json
└── errors.json     # 如果有失敗方向
```

### atlas.json

```json
{
  "schema_version": 1,
  "job_id": "...",
  "preset": "rpgmaker_8dir",
  "seed": 12345,
  "rig_version": "v1",
  "frame_size": { "width": 512, "height": 512 },
  "frames": [
    {
      "index": 0,
      "direction": "F",
      "angle": 0,
      "state": "success",
      "rect": { "x": 0, "y": 0, "w": 512, "h": 512 },
      "pivot": { "x": 0.5, "y": 0.9 },
      "baseline_y": 500,
      "padding": 2,
      "extrude": 1
    },
    ...
  ],
  "failed_directions": ["BR"],
  "created_at": "..."
}
```

---

## Flutter 前端架構

```
app/lib/
├── main.dart
├── core/
│   ├── api/
│   │   ├── api_client.dart
│   │   ├── sse_client.dart          # 斷線重連 + Last-Event-ID
│   │   └── models/
│   │       ├── job.dart
│   │       ├── job_event.dart       # sealed class
│   │       └── atlas.dart
│   ├── repositories/
│   │   └── job_repository.dart
│   ├── services/
│   │   └── job_service.dart         # JobEvent → JobState reduce
│   └── utils/
│       ├── asset_cache.dart         # flutter_cache_manager + Flame
│       └── sprite_sheet_parser.dart
│
├── features/
│   ├── upload/
│   ├── generate/
│   └── export/
│
├── game/
│   ├── preview_game.dart
│   ├── components/
│   │   ├── character_sprite.dart    # SpriteGroupComponent<Direction>
│   │   └── joystick.dart
│   └── utils/
│       └── direction_resolver.dart
│
└── shared/
    ├── widgets/
    └── theme/
```

### JobState

```dart
enum JobStatus {
  idle, uploading, queued, processing, packing,
  completed, completedWithErrors, failed, canceled, retrying
}

enum JobStage { uploading, generating, packing, done }

@freezed
class JobState with _$JobState {
  const factory JobState({
    required String? jobId,
    required JobStatus status,
    required JobStage? stage,
    required int done,
    required int total,
    required List<PartialResult> results,
    required List<String> failedDirections,
    required String? eventUrl,
    required String? jobUrl,
    required String? exportUrl,
    required String? errorCode,
    required String? errorMessage,
  }) = _JobState;

  double get progress => total > 0 ? done / total : 0.0;
  bool get hasErrors => failedDirections.isNotEmpty;
}
```

### JobEvent sealed class

```dart
sealed class JobEvent {}

class JobCreated extends JobEvent { ... }
class JobStarted extends JobEvent { ... }
class JobProgress extends JobEvent { ... }
class JobPartialResult extends JobEvent { ... }
class JobCompleted extends JobEvent { ... }
class JobCompletedWithErrors extends JobEvent { ... }
class JobFailed extends JobEvent { ... }
```

---

## Python 後端架構

```
backend/
├── main.py
├── config.py
│
├── api/
│   ├── routes/
│   │   ├── jobs.py
│   │   ├── upload.py
│   │   └── events.py
│   ├── deps.py
│   ├── middleware/
│   │   └── rate_limit.py
│   └── schemas/
│
├── core/
│   ├── services/
│   │   ├── job_service.py
│   │   ├── qwen_service.py          # + backoff + 熔斷
│   │   └── export_service.py
│   ├── models/
│   │   ├── job.py
│   │   └── direction.py
│   └── events/
│       ├── publisher.py             # Redis Streams XADD
│       └── subscriber.py            # XREAD + Last-Event-ID
│
├── worker/
│   ├── celery_app.py
│   ├── tasks/
│   │   └── generate_task.py         # 冪等 + 併發控制
│   └── handlers/
│       └── direction_handler.py
│
├── infra/
│   ├── redis.py
│   ├── s3.py
│   └── hf_client.py                 # + circuit breaker
│
└── tests/
```

### Worker 核心邏輯

```python
@celery_app.task(bind=True, max_retries=3)
async def generate_sprite_task(self, job_id: str):
    job = await job_repo.get(job_id)

    if job.cancel_requested:
        await job_repo.update_status(job_id, "canceled")
        return

    await publisher.emit(job_id, JobStarted(stage="generating"))

    # 有限併發
    semaphore = asyncio.Semaphore(3)

    async def process_direction(i: int, direction: Direction):
        async with semaphore:
            # 冪等檢查
            existing = await job_repo.get_result(job_id, direction.code)
            if existing and existing.state == "success":
                return  # 跳過已成功

            if await s3.exists(f"{job_id}/{direction.code}.png"):
                return  # S3 已存在

            # 檢查取消
            if await job_repo.is_cancel_requested(job_id):
                return

            try:
                image = await qwen_service.generate(...)
                # 上傳 + 發事件
                ...
            except HFTimeoutError as e:
                await job_repo.mark_direction_failed(job_id, direction, str(e))

    await asyncio.gather(*[
        process_direction(i, d) for i, d in enumerate(job.directions)
    ])

    # 打包
    await publisher.emit(job_id, JobStarted(stage="packing"))
    await export_service.pack_zip(job_id)

    # 判斷最終狀態
    failed = await job_repo.get_failed_directions(job_id)
    if failed:
        await job_repo.update_status(job_id, "completed_with_errors")
        await publisher.emit(job_id, JobCompletedWithErrors(...))
    else:
        await job_repo.update_status(job_id, "completed")
        await publisher.emit(job_id, JobCompleted(...))
```

---

## 安全與營運

| 項目 | 措施 |
|------|------|
| **SSRF 防護** | source_key 只接受自己 bucket 的 key |
| **Rate Limit** | per IP: 10 req/min, per user: 50 req/min |
| **HF 熔斷** | 連續 5 次 timeout → 暫停 60s |
| **source_key 綁定** | 綁定 session/user，防止盜用 |
| **TTL 清理** | completed/failed job 保留 30 天 |

---

## MVP 範圍

**Phase 1（本次實作）**:
- [x] 設計文件
- [ ] Python 後端（FastAPI + Celery + Redis）
- [ ] Flutter 前端（上傳 + 生成 + SSE 進度）
- [ ] Flame 預覽（靜態 8 方向 + joystick）
- [ ] 導出 ZIP

**Phase 2（未來）**:
- [ ] 走路動畫（每方向 3 幀）
- [ ] 自訂角度
- [ ] 去背優化
- [ ] 用戶系統
- [ ] 付費方案

---

## 專案結構

```
sprite-forge/
├── backend/           # Python FastAPI
├── app/               # Flutter + Flame
├── shared/            # JSON Schema
├── docker-compose.yml
├── README.md
└── docs/
    └── plans/
        └── 2026-01-13-sprite-forge-design.md
```
