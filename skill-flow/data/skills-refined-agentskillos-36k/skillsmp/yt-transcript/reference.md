# yt-transcript reference

## 快速開始

在「要輸出結果的資料夾」執行：

```bash
./.venv/bin/python <skill-root>/scripts/get_transcripts.py
```

`<skill-root>` 指的是包含 `SKILL.md` 的資料夾。

## 輸入格式

### CSV 模式

檔名：`youtube_videos.csv`

必要欄位：
- `Title`
- `URL`
- `NotebookSource`（若整份 CSV 都同一來源，可改用 `SOURCE_NAME`）

腳本會自動新增：
- `Checked`（✔ 已完成 / △ MAX_TOKENS / ✖ 失敗）
- `序號`

批次只會略過 `✔`；`△` 與 `✖` 會再跑。

### URL 模式

直接用環境變數帶入：

```bash
SOURCE_NAME="LLM" URLS="https://youtu.be/AAA https://youtu.be/BBB" \
  ./.venv/bin/python <skill-root>/scripts/get_transcripts.py
```

或用純文字檔：

```bash
SOURCE_NAME="LLM" URLS_FILE="/path/to/urls.txt" \
  ./.venv/bin/python <skill-root>/scripts/get_transcripts.py
```

## 輸出規則

- 主要輸出：`transcript/<NotebookSource>.md`
- 超出上限：`transcript/<NotebookSource>_partN.md`
- 上限計算：`NOTEBOOKLM_MAX_WORDS × NOTEBOOKLM_TARGET_RATIO`

## API Key 與安全

- 建議用環境變數：`GEMINI_API_KEY=...`
- 或在 `scripts/` 同層放 `.gemini_key_paid` / `.gemini_key_free`
- 這些 key 不應提交到 Git

## 常用環境變數（說人話）

- `SOURCE_NAME`：URL 模式時的來源名稱
- `NOTEBOOK_SOURCE_COLUMN`：CSV 裡的來源欄位名稱（預設 `NotebookSource`）
- `NOTEBOOKLM_MAX_WORDS`：單一來源上限（預設 500000 words）
- `NOTEBOOKLM_TARGET_RATIO`：保守比例（預設 0.6）
- `MAX_VIDEOS`：這次只跑 N 支
- `SINGLE_INDEX`：單支處理（CSV 的序號）
- `GEMINI_MODEL`：指定模型（預設 `gemini-2.5-flash`）
- `GEMINI_MEDIA_RESOLUTION`：影片解析度（LOW/MEDIUM/HIGH）
- `MERGE_LINES`：合併短行（1=開）
- `INPUT_PRICE_PER_M`：每 1M tokens 的輸入成本估算（USD）
- `OUTPUT_PRICE_PER_M`：每 1M tokens 的輸出成本估算（USD）

## 常見問題

- **只有 .skill 沒有 repo 能不能跑？**
  可以。skill 內含 `scripts/get_transcripts.py` 與 `prompt.txt`，只要本機有 Python + 相依套件即可。

- **要換 key？**
  用 `GEMINI_API_KEY` 或改 `scripts/` 同層的 `.gemini_key_*`。
