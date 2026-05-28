---
name: local-resources
description: 本地模型和数据集资源管理。在使用 HuggingFace 模型或 datasets 库加载数据时，优先使用本地资源。
---

# 本地模型和数据集资源

## 重要原则

**所有模型和数据集均已本地可用，无需联网下载**。在使用 HuggingFace 或 datasets 库时，直接指定本地路径。

## 本地资源路径

| 资源类型 | 路径 | 说明 |
|---------|------|------|
| 模型库 | `/home/share/models/` | 316+ 个预训练模型 |
| 数据集 | `~/datasets/` | 常用 NLP 基准数据集 |

---

## 可用模型列表

### MoE 模型 (与本项目相关)

| 模型名称 | 路径 | 备注 |
|---------|------|------|
| DeepSeek-MoE-16B | `/home/share/models/deepseek-moe-16b-base` | 有共享专家 |
| Mixtral-8x7B | `/home/share/models/Mixtral-8x7B-v0.1` | 无共享专家 |
| Mixtral-8x22B | `/home/share/models/Mixtral-8x22B-v0.1` | |
| Qwen2-57B-A14B | `/home/share/models/Qwen2-57B-A14B` | 有共享专家 |
| Qwen3-30B-A3B | `/home/share/models/Qwen3-30B-A3B` | 无共享专家 |
| Qwen1.5-MoE-A2.7B | `/home/share/models/Qwen1.5-MoE-A2.7B` | |
| Phi-3.5-MoE | `/home/share/models/Phi-3.5-MoE-instruct` | |
| MiniCPM-MoE-8x2B | `/home/share/models/MiniCPM-MoE-8x2B` | |
| OLMoE-1B-7B | `/home/share/models/OLMoE-1B-7B-0924` | |
| JetMoE-8B | `/home/share/models/jetmoe-8b` | |
| Chinese-Mixtral-8x7B | `/home/share/models/Chinese-Mixtral-8x7B` | |

### Qwen 系列

| 模型名称 | 路径 |
|---------|------|
| Qwen3-30B-A3B | `/home/share/models/Qwen3-30B-A3B` |
| Qwen3-235B-A22B | `/home/share/models/Qwen3-235B-A22B` |
| Qwen2-57B-A14B | `/home/share/models/Qwen2-57B-A14B` |
| Qwen2.5-72B | `/home/share/models/Qwen2.5-72B` |
| Qwen2.5-32B | `/home/share/models/Qwen2.5-32B` |
| Qwen2.5-14B | `/home/share/models/Qwen2.5-14B` |
| Qwen2.5-7B | `/home/share/models/Qwen2.5-7B` |
| Qwen2.5-3B | `/home/share/models/Qwen2.5-3B` |
| Qwen2.5-1.5B | `/home/share/models/Qwen2.5-1.5B` |
| Qwen2.5-0.5B | `/home/share/models/Qwen2.5-0.5B` |

### DeepSeek 系列

| 模型名称 | 路径 |
|---------|------|
| DeepSeek-Coder-V2-Lite-Instruct | `/home/share/models/DeepSeek-Coder-V2-Lite-Instruct` |
| DeepSeek-Coder-V2-Lite-Base | `/home/share/models/DeepSeek-Coder-V2-Lite-Base` |
| DeepSeek-Coder-V2-Instruct | `/home/share/models/DeepSeek-Coder-V2-Instruct` |
| DeepSeek-Coder-V2-Base | `/home/share/models/DeepSeek-Coder-V2-Base` |
| deepseek-coder-33b-instruct | `/home/share/models/deepseek-coder-33b-instruct` |
| deepseek-coder-6.7b-instruct | `/home/share/models/deepseek-coder-6.7b-instruct` |

### Code/LLaMA 系列

| 模型名称 | 路径 |
|---------|------|
| CodeLlama-70b-Python-hf | `/home/share/models/CodeLlama-70b-Python-hf` |
| CodeLlama-34b-Python-hf | `/home/share/models/CodeLlama-34b-Python-hf` |
| CodeLlama-13b-Python-hf | `/home/share/models/CodeLlama-13b-Python-hf` |
| CodeLlama-7b-Python-hf | `/home/share/models/CodeLlama-7b-Python-hf` |

### 其他模型

使用 `ls /home/share/models/` 查看完整列表（316+ 个模型）。

---

## 可用数据集列表

| 数据集名称 | 路径 | splits |
|-----------|------|--------|
| wikitext-2 | `~/datasets/wikitext-2/` | train, test, validation |
| c4 | `~/datasets/c4/` | train, test, validation |
| gsm8k | `~/datasets/gsm8k/` | train, test |
| hellaswag | `~/datasets/hellaswag/` | train, test, validation |
| arc-easy | `~/datasets/arc-easy/` | train, test, validation |
| arc-challenge | `~/datasets/arc-challenge/` | train, test, validation |
| boolq | `~/datasets/boolq/` | train, test, validation |
| piqa | `~/datasets/piqa/` | train, test, validation |
| winogrande | `~/datasets/winogrande/` | train, test, validation |
| rte | `~/datasets/rte/` | train, test, validation |
| obqa | `~/datasets/obqa/` | train, test, validation |
| humaneval | `~/datasets/humaneval/` | test |
| math_qa | `~/datasets/math_qa/` | train, test, validation |
| cnn_dailymail | `~/datasets/cnn_dailymail/` | train, test, validation |

---

## 代码中使用方法

### 加载本地模型

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

# 直接使用本地路径
model_path = "/home/share/models/Qwen3-30B-A3B"
model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(model_path)
```

### 加载本地数据集

```python
from datasets import load_from_disk

# 直接从本地路径加载
dataset = load_from_disk("~/datasets/wikitext-2")
train_data = dataset["train"]
test_data = dataset["test"]
```

### 本项目中的使用示例

```python
# 在 d16b.py, qwen3.py 等脚本中
model_path = "/home/share/models/deepseek-moe-16b-base"
model = get_deepeekmoe_model(model_path)  # 使用本地模型

# 在 datautils.py 中
def get_wikitext2():
    # 修改为使用本地路径
    data = load_from_disk("~/datasets/wikitext-2")
    return data["train"], data["validation"]
```

---

## 快速参考命令

```bash
# 查看所有模型
ls /home/share/models/

# 搜索特定模型 (如 MoE)
ls /home/share/models/ | grep -i moe

# 搜索 Qwen 模型
ls /home/share/models/ | grep -i qwen

# 查看数据集
ls ~/datasets/

# 查看数据集内容
ls ~/datasets/wikitext-2/
```

---

## 注意事项

1. **不要使用 `download=True`**：所有资源均已在本地
2. **路径使用绝对路径**：`/home/share/models/xxx` 或 `~/datasets/xxx`
3. **MoE 模型较大**：注意 GPU 内存限制
4. **数据集格式**：均为 HuggingFace Arrow 格式，使用 `load_from_disk()` 加载
