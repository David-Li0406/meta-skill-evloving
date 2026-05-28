---
name: slurm
description: SLURM 集群使用规范。在任何需要运行 Python 脚本或实验代码时使用。
---

# SLURM 集群使用规范

## 重要原则

**绝对不要尝试请求或分配 GPU 资源**。资源已由用户预先分配。

## 运行脚本的标准流程

### Step 1: 检查已分配的计算资源

使用 `sq` 命令查看当前已分配的作业：

```bash
sq
```

输出会显示 JOBID，例如：
```
JOBID     NAME    ST  TIME  NODES
65975     bash    R   1:00  node01
```

### Step 2: 使用 srun 运行脚本

使用已分配的 JOBID 运行脚本：

```bash
srun --jobid <JOBID> python <script.py> [args...]
```

## 示例

### 运行训练脚本

```bash
# 先检查作业
sq

# 运行脚本（假设 JOBID 是 65975）
srun --jobid 65975 python d16b.py /path/to/model wikitext2 \
  --seed 1234 --nsamples 128 --calib-length 2048 \
  --save /output/path --func prune --pratio 0.21 \
  --chunk-size 32 --reduce_ratio 0.95
```

### 运行评估脚本

```bash
srun --jobid 65975 python eval_ppl.py
```

## 环境信息

- **GPU**: 80GB A100/A800
- **CUDA**: cu118

## 环境准备

如果需要 CUDA，在运行前加载模块：

```bash
module load cuda/11.8
```

## 常见错误

| 错误 | 原因 | 正确做法 |
|------|------|----------|
| 使用 `sbatch` | 不应提交新作业 | 使用 `srun --jobid` |
| 使用 `--gpus` 参数 | 尝试分配资源 | 直接使用预分配资源 |
| 直接 `python xxx.py` | 未通过 SLURM 运行 | 使用 `srun --jobid` |

## 快速命令参考

| 命令 | 用途 |
|------|------|
| `sq` | 查看已分配的作业 |
| `srun --jobid <ID> <cmd>` | 在已分配资源上运行命令 |
