---
name: icp-batch-skill
description: "批量处理 domains.xlsx：提取域名，优先命中本地缓存，缺失时调用 ICP 备案查询 API（AppCode 模式），生成/更新缓存与结果文件，并将备案主体/备案号写回 Excel 末两列。"
---

# ICP 批处理工作流

此技能封装了整套批量查询流程，适用于类似 `domains.xlsx` 的表格：
- 从表头含“链接”的列提取域名（保留去重，非标准值也保留）。
- 优先使用本地缓存 `icp_results.csv`；仅对缺失或失败记录调用 API。
- 写回/更新：
  - `icp_results.csv`：完整原始响应缓存（domain,status_code,error_header,body）。
  - `icp_success.csv`：解析后的成功条目（code=1）。
  - 原始 Excel 在末尾追加两列：备案主体、备案号。

## 运行前准备
- Python 3.9+，依赖：`pip install openpyxl requests`。
- 环境变量：`APP_CODE=<你的AppCode>`（勿写入脚本/仓库）。
- 默认文件：`domains.xlsx` 位于工作目录，表头含“链接”列。

## 快速使用
```bash
python icp-batch-skill/scripts/run_icp_batch.py \
  --workbook domains.xlsx \
  --cache icp_results.csv \
  --success icp_success.csv
```
参数说明（均有默认，可省略）：
- `--workbook`：待处理 Excel（默认 domains.xlsx）。
- `--cache`：缓存文件（默认 icp_results.csv）。
- `--success`：成功解析输出（默认 icp_success.csv）。

## 过程要点
1) 提取域名：优先匹配表头等于“链接”的列，否则使用首列。对每行提取正则域名；无匹配则使用原文本。
2) 缓存策略：
   - 命中且 `status_code=200` 且响应 `code=1` → 直接复用。
   - 其他情况 → 调用 API `GET https://domainicp.market.alicloudapi.com/do?domain=...`，头 `Authorization: APPCODE <APP_CODE>`。
3) 写回：
   - 追加两列表头：`备案主体`、`备案号`，按行填充命中数据（无则留空）。
   - `icp_results.csv` 覆盖写入完整域名顺序。
   - `icp_success.csv` 写入成功解析条目，便于后续复用。

## 常见问题
- 403/鉴权失败：检查 APP_CODE 是否有效、套餐授权正常。
- 非标准域名：脚本保留并尝试查询，若返回 code=0 / 字段为空，输出空。
- 如需更换 API Host/Path，可用参数 `--host`、`--path`（见脚本）。

## 资源
- 脚本：`scripts/run_icp_batch.py`
