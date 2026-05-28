# workflow.md（Windows 友好）

## 总流程（固定顺序）

1. **确定算例**（001–264，默认 001）
2. **修改控制 CSV**
   - Boundary.csv 常用列：如 `B_081:FR`, `T_001:SNQ` 等
   - 默认可全列修改；也可按 TIME 时间范围修改
3. **patch job-config（就地修改）**
   - 文件：`real_predict/examples/batch_jobs_full_value_projection_small.json`
   - 修改：`jobs[job_index].sample_dir` / `jobs[job_index].output`
4. **执行预测**
   - 命令：`python -m real_predict.main --job-config real_predict/examples/batch_jobs_full_value_projection_small.json`
5. **阅读输出**
   - 汇总脚本会输出 `summary.md`

## 为什么 modify_boundary 不需要“指定哪一行”？
很多工况是“让一个控制量在整个预测区间都保持某个值”，因此：
- **默认行为**：修改该列的所有数据行（最直观、最常用）
- 如果你确实要指定行/时间段：
  - 用 `--start-time/--end-time`（按 TIME 范围过滤）
  - 或用 `--match-time`（精确点修改）
  - 或用 `--row-index`（按数据行序号修改，1 表示第一行数据，不含表头）

## 差异对比如何判断“是否满足”？
- `diff_boundary.py` 会输出：
  - 修改了多少行
  - 哪些 TIME（或行号）发生变化
  - before/after 的具体值
- 你可以用它来验证：
  - 是否只改了预期时间范围
  - 是否改成了预期的 value
