---
name: camera-pruning
description: Camera 微专家剪枝方法。基于微专家能量估计的 MoE 模型结构化剪枝。
---

# Camera 微专家剪枝方法

> 基于 Camera 论文 (arXiv:2508.02322) 的 MoE 模型剪枝复现

## 核心概念：微专家 (Micro-Expert)

### 什么是微专家？

传统 MoE 模型以 **Expert** 为压缩单元（每个 Expert 包含 up_proj, gate_proj, down_proj 三个矩阵）。

**Camera 提出更细粒度的视角**：将每个 Expert 沿中间维度分解为 **Micro-Expert**。

```
Expert (传统视角):          Micro-Expert (Camera 视角):
┌─────────────┐             ┌─────────────────────────┐
│ up_proj     │             │ up_proj[0, :]    ←─┐    │
│ gate_proj   │             │ gate_proj[0, :]  ←─┤    │
│ down_proj   │             │ down_proj[:, 0]  ←─┘ Micro-Expert 0
└─────────────┘             │ up_proj[1, :]    ←─┐    │
                            │ gate_proj[1, :]  ←─┤ Micro-Expert 1
                            │ down_proj[:, 1]  ←─┘    │
                            │         ...              │
                            └─────────────────────────┘

微专家数量 = Expert 数量 × 中间维度 (d_ff)
```

### 跨矩阵完整性

一个微专家横跨三个矩阵，**必须同步处理**：

```
Micro-Expert i = {
    W_up[i, :]      (第 i 行)
    W_gate[i, :]    (第 i 行)
    W_down[:, i]    (第 i 列)
}
```

剪枝时，三个矩阵的对应位置**同时置零**，保持功能完整性。

---

## Camera 算法

### 微专家能量

Camera 定义微专家的**解码时能量**来衡量重要性：

$$\mathcal{E}_i = \left[(1-\alpha) \| \Phi_{:,i} \|_2^2 + \alpha \| \Phi_{:,i} \|_\infty^2 \right] \cdot \| w_i \|_2^2$$

其中：
- $\Phi_{:,i}$ = 第 i 个微专家在校准数据上的激活系数向量
- $\alpha$ = 平衡系数（实验中取 0.95 ~ 1.0）
- **能量越低 → 微专家越冗余 → 优先剪枝**

### 代码参数对应

| 论文参数 | 代码参数 | 典型值 |
|---------|---------|--------|
| $\alpha$ | `1 - reduce_ratio` | 0.95 ~ 1.0 |
| $\lambda$ (剪枝比例) | `--pratio` | 0.2, 0.4, 0.6 |

---

## Camera-P：结构化剪枝

### 剪枝流程

```
┌─────────────────────────────────────────────────────────┐
│  Step 1: 校准 (收集隐藏状态)                             │
│  - 用校准数据 (如 wikitext2) 前向传播                    │
│  - 收集每层 MoE 的输入输出隐藏状态                       │
├─────────────────────────────────────────────────────────┤
│  Step 2: 能量估计 (计算微专家重要性)                     │
│  - 对每个微专家计算能量 E_i                              │
│  - 按能量降序排序                                        │
├─────────────────────────────────────────────────────────┤
│  Step 3: 剪枝 (置零低能量微专家)                         │
│  - 保留 Top (1-λ)% 高能量微专家                         │
│  - 将其余微专家在三个矩阵中对应位置置零                  │
└─────────────────────────────────────────────────────────┘
```

### 运行示例

```bash
# DeepSeek-MoE-16B，20% 剪枝
srun --jobid <JOBID> python d16b.py /home/share/models/deepseek-moe-16b-base wikitext2 \
  --seed 1234 --nsamples 128 --calib-length 2048 \
  --save /output/path --func prune --pratio 0.21 \
  --chunk-size 32 --reduce_ratio 0.05

# Qwen3-30B-A3B，40% 剪枝
srun --jobid <JOBID> python qwen3.py /home/share/models/Qwen3-30B-A3B wikitext2 \
  --seed 1234 --nsamples 128 --calib-length 2048 \
  --save /output/path --func prune --pratio 0.4 \
  --chunk-size 32 --reduce_ratio 0.00
```

---

## 支持的模型

| 脚本 | 模型 | MoE 模块位置 | 特点 |
|------|------|-------------|------|
| `d16b.py` | DeepSeek-MoE-16B | `layer.mlp` | 有共享专家 |
| `qwen3.py` | Qwen3-30B-A3B | `layer.mlp` | 无共享专家 |
| `qwen2.py` | Qwen2-57B-A14B | `layer.mlp` | 有共享专家 |
| `mixtral.py` | Mixtral-8x7B | `layer.block_sparse_moe` | 无共享专家 |
| `phi.py` | Phi-3.5-MoE | `layer.block_sparse_moe` | 无共享专家 |

---

## 核心参数说明

| 参数 | 含义 | 典型值 | 说明 |
|------|------|--------|------|
| `--pratio` | 剪枝比例 | 0.2, 0.4, 0.6 | 剪掉的比例 |
| `--reduce_ratio` | L∞ 范数权重 | 0.05, 0.00 | 对应 α = 1 - reduce_ratio |
| `--chunk-size` | 批大小 | 32, 64, 128 | 显存不足时减小 |
| `--nsamples` | 校准样本数 | 128 | 通常 128 足够 |
| `--calib-length` | 序列长度 | 2048 | 校准数据长度 |
| `--save` | 输出路径 | - | 保存剪枝后的 checkpoint |

---

## 实验结果参考

### DeepSeek-MoE-16B (WikiText2 PPL)

| 剪枝比例 | Original | NAEE | D²-MoE | Camera-P |
|---------|----------|------|--------|----------|
| 20% | 6.51 | 6.77 | 7.29 | **6.57** |
| 40% | 6.51 | 8.01 | 8.38 | **6.93** |
| 60% | 6.51 | 15.47 | 12.13 | **8.68** |

### Qwen2-57B-A14B (平均准确率)

| 剪枝比例 | Original | NAEE | D²-MoE | Camera-P |
|---------|----------|------|--------|----------|
| 20% | 66.74 | 66.11 | 66.38 | **67.28** |
| 40% | 66.74 | 63.92 | 64.40 | **66.81** |
| 60% | 66.74 | 51.40 | 56.32 | **65.17** |

---

## 常见问题

### Q: reduce_ratio 如何选择？

- `reduce_ratio = 0.05` → α = 0.95，平衡 L2 和 L∞ 范数
- `reduce_ratio = 0.00` → α = 1.00，纯 L∞ 范数
- 论文中对 DeepSeek/Qwen2 使用 0.05，Qwen3 使用 0.00

### Q: 剪枝比例如何选择？

- 20%：保守剪枝，性能损失最小
- 40%：中等剪枝，性能与压缩平衡
- 60%：激进剪枝，适合推理加速优先的场景

### Q: 为什么比 D²-MoE 快？

- Camera-P：直接置零权重，5 分钟完成 50B 模型
- D²-MoE：需要 SVD 分解 + 低秩近似，耗时数小时

### Q: 有共享专家的模型需要特殊处理吗？

不需要。Camera 对所有微专家统一排序，共享专家的微专家会自动获得较高能量（通常被保留）。

---

## 快速命令参考

```bash
# 查看可用模型
ls /home/share/models/ | grep -i "moe\|mixtral"

# 查看数据集
ls ~/datasets/

# 检查 SLURM 作业
sq

# 运行剪枝
srun --jobid <JOBID> python <script>.py <model_path> <dataset> [args...]
```

---

## 相关文件

- 实验背景：`EXPERIMENT.md`
- 核心实现：`mei.py`
- 模型脚本：`d16b.py`, `qwen3.py`, `qwen2.py`, `mixtral.py`, `phi.py`
- 数据加载：`datautils.py`
