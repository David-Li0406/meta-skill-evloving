---
name: fluid-model
description: 获得预测管网的调度能力。在 Windows 环境下按算例(001-264,默认001)修改控制CSV(Boundary等)、就地patch批量job-config、运行 real_predict 并汇总/对比输出。
dependencies:
  - python>=3.9
---

# 最关键的两个绝对路径前缀-请务必记住！！重要
[PROJECT-PATH-PREFIX]: "D:/ml_pro_master/chroes/fluid_model" 
比如python -m real_predict.main ... 整个流体模型项目的代码都是在这个项目路径下面，后续的都是相对路径，如果你使用 WorkspaceTools 的 `run_command`：**real_predict 必须传 `cwd=<项目根目录绝对路径>`，但是scripts是属于SKILL里面的路径，就是之前的项目路径，可以不用cwd。只有real_predict或者mock_data需要到fluid_model的根目录下面去执行。当遇到路径的脚本不存在的时候反复思考是不是路径写错了，再结束对话。**

[SKILL-PATH-PREFIX]: "D:/ml_pro_master/gis_pipeline_llm/backend/agent/skills/fluid-model" 这个是关于这个预制SKILL的脚本的代码都放在这里。也支持自定义脚本在 `[SKILL-PATH-PREFIX]/temporary_scripts` 目录下创建。

# real_predict 批量预测工作流

这个 Skill 专注于一个可重复的流程：  
**选算例 →（按场景）修改控制 CSV → patch job-config → 执行 `python -m real_predict.main ...` → 阅读输出 →（可选）对比“修改前/后”差异。**

> 设计目标：低自由度、少手工编辑、可反复迭代多个“特殊变化”场景。

---

## 强制规则（必须照做）

### 0) 预测算例选择规则（001–264）
- **允许范围**：第001个算例 ～ 第264个算例  
- **默认**：用户没说 / 说错 / 超范围 → **默认使用第001个算例**

### 1) 路径与工作目录规则
- **所有关键路径都建议使用绝对路径**（尤其是 job-config 的 `sample_dir` / `output`）。因为现在有多个路径的文件还需要考虑。

### 2) output 必须写到“新文件夹”
- 每次运行都必须把 `jobs[x].output` 指到一个**新的输出目录**，避免覆盖旧结果。
- 本 Skill 默认把输出放到：  
  `[PROJECT-PATH-PREFIX]/real_predict/examples/_runs/<run_tag>/<原output最后一级目录名>/`


## 两种使用方式

### A. 一次性快速改 Boundary.csv（你给的命令形式）
适用：你只想改某一列（默认整列全改），并希望能对比“改前/改后”。

#### 1) 修改（会自动生成备份）
> 默认：不指定行/时间范围时，会修改 **该列的所有数据行**。

```bash
python [SKILL-PATH-PREFIX]/scripts/modify_boundary.py \
  --boundary-file "[PROJECT-PATH-PREFIX]/data/dataset/mock_test/第001个算例/Boundary.csv" \
  --column "T_001:SNQ" \
  --value 1200
```

可选：只改某一段时间（需要 CSV 有 TIME 列）：
```bash
python [SKILL-PATH-PREFIX]/scripts/modify_boundary.py \
  --boundary-file "[PROJECT-PATH-PREFIX]/data/dataset/mock_test/第001个算例/Boundary.csv" \
  --column "T_001:SNQ" \
  --value 1200 \
  --start-time "2025/1/1 6:00" \
  --end-time "2025/1/1 12:00"
```

#### 2) 对比修改前后到底哪些数据不一样（自动找“最新备份”）
```bash
python [SKILL-PATH-PREFIX]/scripts/diff_boundary.py \
  --boundary-file "[PROJECT-PATH-PREFIX]/data/dataset/mock_test/第001个算例/Boundary.csv" \
  --column "T_001:SNQ"
```

输出：
- 控制台打印差异统计
- 同目录生成：
  - `diff_Boundary_YYYYMMDD_HHMMSS.md`
  - `diff_Boundary_YYYYMMDD_HHMMSS.csv`

> Windows 说明：  
> - 如果你用 CMD / PowerShell，不支持 `\` 续行，请把命令写成一行，或者用 PowerShell 的反引号续行。  
> - 脚本本身不依赖 bash / bin / shebang。

---

### B. 完整批量预测工作流（0→4，可反复迭代）

#### Step 0：写 plan.json（推荐用于多次迭代）
把 plan 放到（示例）：
`[PROJECT-PATH-PREFIX]/real_predict/examples/_runs/<run_tag>/plan.json`

plan 模板见：`[SKILL-PATH-PREFIX]/reference/plan_schema.md` 与 `[SKILL-PATH-PREFIX]/examples/plan_example_001.json`

#### Step 1：校验 plan（避免跑到一半才发现路径/列名错）
```bash
python [SKILL-PATH-PREFIX]/scripts/validate_plan.py --plan "[PROJECT-PATH-PREFIX]/real_predict/examples/_runs/<run_tag>/plan.json"
```

#### Step 2：按 plan 修改控制 CSV（可多条 change）
```bash
python [SKILL-PATH-PREFIX]/scripts/apply_csv_changes.py --plan "[PROJECT-PATH-PREFIX]/real_predict/examples/_runs/<run_tag>/plan.json"
```

#### Step 3：就地 patch job-config（修改 sample_dir/output 指向新目录）
```bash
python [SKILL-PATH-PREFIX]/scripts/patch_job_config_inplace.py --plan "[PROJECT-PATH-PREFIX]/real_predict/examples/_runs/<run_tag>/plan.json"
```

#### Step 4：执行预测（严格按要求）
```bash
python -m real_predict.main --job-config "[PROJECT-PATH-PREFIX]/real_predict/examples/batch_jobs_full_value_projection_small.json"
cwd=[PROJECT-PATH-PREFIX]
```

#### Step 5：汇总输出目录
```bash
python [SKILL-PATH-PREFIX]/scripts/summarize_output.py --plan "[PROJECT-PATH-PREFIX]/real_predict/examples/_runs/<run_tag>/plan.json"
```

然后读取：
`[PROJECT-PATH-PREFIX]/real_predict/examples/_runs/<run_tag>/summary.md`

---

## 迭代多个“特殊变化”的推荐做法

- 每个变化场景一个新的 `run_tag`
- 只改 `plan.json` 里的 `csv_changes`（或者用 modify_boundary 快速修改）
- 每次都生成新 output 文件夹
- 每次都跑完：validate → apply → patch → predict → summarize
- 如果需要临时定义Scripts自定义修改的模式，可以在 `[SKILL-PATH-PREFIX]/temporary_scripts` 目录下创建脚本。

