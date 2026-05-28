# plan.json 字段说明（Schema）

## 最小示例
```json
{
  "project_root": "D:\\ml_pro_master\\chroes\\fluid_model",
  "sample_id": "001",
  "run_tag": "run_20260105_153000_case001",
  "job_config_path": "D:\\ml_pro_master\\chroes\\fluid_model\\real_predict\\examples\\batch_jobs_full_value_projection_small.json",
  "job_index": 0,
  "csv_changes": [
    {
      "file": "Boundary.csv",
      "column": "T_001:SNQ",
      "value": 1200
    }
  ],
  "overrides": {
    "device": "auto",
    "output_mode": "split",
    "prediction_minutes": 10
  }
}
```

## 字段说明

- project_root（必填）：项目根目录（绝对路径）
- sample_id（可选）：001–264（缺失/越界默认 001）
- run_tag（必填）：本次运行标签（建议纯 ASCII）
- job_config_path（可选）：默认指向 batch_jobs_full_value_projection_small.json
- job_index（可选）：默认 0
- csv_changes（可选）：多个 CSV 修改
  - file：相对 sample_dir 的文件名，默认 Boundary.csv
  - column：列名（必须精确匹配表头）
  - value：新值（数字或字符串）
  - start_time/end_time（可选）：按 TIME 时间范围修改
  - match_time（可选）：精确修改某个 TIME 点（字符串或数组）
  - row_index（可选）：按数据行序号修改（1 表示第一行数据，不含表头；可数组）
- overrides（可选）：写入 job-config 的 defaults（device/output_mode/prediction_minutes 等）
