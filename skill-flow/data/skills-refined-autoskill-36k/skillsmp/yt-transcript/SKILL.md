---
name: yt-transcript
description: 產生 YouTube 逐字稿並依 NotebookLM 來源上限自動合併/分檔，支援 CSV 與直接 URL，包含續跑/補跑與重試。適用於要把多支 YouTube 影片整理成 NotebookLM 來源檔的場景。
license: MIT. LICENSE.txt has complete terms
---

# yt-transcript

## Overview

從 YouTube 影片產生逐字稿，並依 NotebookLM 單一來源上限自動合併/續接成
`transcript/<NotebookSource>.md` 與 `_partN`。

## Quick Start

`<skill-root>` 指包含本 `SKILL.md` 的資料夾。

### CSV 模式

1. `cd` 到輸出資料夾（含 `youtube_videos.csv`）  
2. 執行：`./.venv/bin/python <skill-root>/scripts/get_transcripts.py`

### URL 模式

`SOURCE_NAME="LLM" URLS="https://youtu.be/AAA https://youtu.be/BBB" ./.venv/bin/python <skill-root>/scripts/get_transcripts.py`

## Requirements

- Python 3
- `pandas`、`requests`
- API key（擇一）  
  - 環境變數：`GEMINI_API_KEY=...`  
  - 檔案：`scripts/` 同層放 `.gemini_key_paid` / `.gemini_key_free`
- 只支援公開影片（private / unlisted 不可用）

## Outputs

- `transcript/<NotebookSource>.md`
- `transcript/<NotebookSource>_partN.md`

## Advanced

完整設定、環境變數與進階用法請看 `reference.md`。
