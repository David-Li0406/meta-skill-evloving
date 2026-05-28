---
id: fine-tuning-lora
name: "Fine-tuning (LoRA)"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Fine-tuning (LoRA)

## Overview

LoRA (Low-Rank Adaptation) is a parameter-efficient fine-tuning technique that trains small adapter layers instead of updating all model weights. This dramatically reduces memory requirements and training time while achieving comparable results to full fine-tuning.

## When to Use

- Limited GPU memory (consumer hardware)
- Quick iteration on fine-tuning experiments
- Need to maintain multiple task-specific adapters
- Training on smaller datasets
- When full fine-tuning is computationally prohibitive

## Key Concepts

### How LoRA Works

```
Original: W (d × k matrix)

LoRA adds: W' = W + BA
  Where: B (d × r), A (r × k), r << min(d, k)

Instead of training d × k parameters,
train only (d × r) + (r × k) parameters

Example: d=4096, k=4096, r=8
  Original: 16.7M parameters
  LoRA: 65K parameters (250x reduction)
```

### Key Parameters

| Parameter | Description | Typical Value |
|-----------|-------------|---------------|
| r (rank) | Dimension of low-rank matrices | 8-64 |
| alpha | Scaling factor | 16-32 |
| dropout | Dropout for LoRA layers | 0.05-0.1 |
| target_modules | Which layers to adapt | q_proj, v_proj, k_proj, o_proj |

## Implementation

### Basic LoRA Fine-tuning

```python
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer
)
from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
    TaskType
)
from datasets import load_dataset
import torch

# Load base model
model_name = "meta-llama/Llama-2-7b-hf"
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto"
)

# Configure LoRA
lora_config = LoraConfig(
    r=8,                           # Rank
    lora_alpha=32,                 # Scaling factor
    target_modules=[               # Layers to adapt
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
    ],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)

# Apply LoRA
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# Output: trainable params: 4,194,304 || all params: 6,742,609,920 || trainable%: 0.06%
```

### QLoRA (4-bit Quantization + LoRA)

```python
from transformers import BitsAndBytesConfig
import bitsandbytes as bnb

# 4-bit quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

# Load quantized model
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto"
)

# Prepare for training
model = prepare_model_for_kbit_training(model)

# Apply LoRA
model = get_peft_model(model, lora_config)
```

### Data Preparation

```python
from datasets import Dataset
from typing import List, Dict

def format_instruction(example: Dict) -> str:
    """Format example for instruction fine-tuning."""
    return f"""### Instruction:
{example['instruction']}

### Input:
{example.get('input', '')}

### Response:
{example['output']}"""

def prepare_dataset(
    examples: List[Dict],
    tokenizer,
    max_length: int = 512
) -> Dataset:
    """Prepare dataset for LoRA fine-tuning."""

    def tokenize(example):
        text = format_instruction(example)
        tokens = tokenizer(
            text,
            truncation=True,
            max_length=max_length,
            padding="max_length"
        )
        tokens["labels"] = tokens["input_ids"].copy()
        return tokens

    dataset = Dataset.from_list(examples)
    return dataset.map(tokenize, remove_columns=dataset.column_names)

# Example data
training_data = [
    {
        "instruction": "Summarize the following text",
        "input": "The quick brown fox jumps over the lazy dog...",
        "output": "A fox jumps over a dog."
    },
    # ... more examples
]

train_dataset = prepare_dataset(training_data, tokenizer)
```

### Training

```python
from transformers import TrainingArguments, Trainer, DataCollatorForLanguageModeling

# Training arguments
training_args = TrainingArguments(
    output_dir="./lora-output",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    save_strategy="epoch",
    warmup_ratio=0.03,
    lr_scheduler_type="cosine",
    optim="paged_adamw_8bit",  # Memory efficient optimizer
)

# Data collator
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    data_collator=data_collator
)

# Train
trainer.train()

# Save adapter
model.save_pretrained("./lora-adapter")
```

### Loading and Using LoRA Adapter

```python
from peft import PeftModel

def load_lora_model(base_model_name: str, adapter_path: str):
    """Load base model with LoRA adapter."""
    # Load base model
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        torch_dtype=torch.float16,
        device_map="auto"
    )

    # Load LoRA adapter
    model = PeftModel.from_pretrained(base_model, adapter_path)

    return model

def merge_and_save(model, output_path: str):
    """Merge LoRA weights into base model and save."""
    merged_model = model.merge_and_unload()
    merged_model.save_pretrained(output_path)
    return merged_model

# Usage
model = load_lora_model(
    "meta-llama/Llama-2-7b-hf",
    "./lora-adapter"
)

# Inference
def generate(model, tokenizer, prompt: str, max_new_tokens: int = 256):
    """Generate text with LoRA model."""
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        temperature=0.7,
        top_p=0.9,
        do_sample=True
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)
```

### Multiple LoRA Adapters

```python
from peft import PeftModel

def load_multiple_adapters(
    base_model_name: str,
    adapters: Dict[str, str]  # {"name": "path"}
) -> PeftModel:
    """Load base model with multiple adapters."""
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        torch_dtype=torch.float16,
        device_map="auto"
    )

    # Load first adapter
    first_name, first_path = next(iter(adapters.items()))
    model = PeftModel.from_pretrained(
        base_model,
        first_path,
        adapter_name=first_name
    )

    # Load additional adapters
    for name, path in list(adapters.items())[1:]:
        model.load_adapter(path, adapter_name=name)

    return model

def switch_adapter(model: PeftModel, adapter_name: str):
    """Switch to a different adapter."""
    model.set_adapter(adapter_name)

# Usage
model = load_multiple_adapters(
    "meta-llama/Llama-2-7b-hf",
    {
        "customer_support": "./adapters/customer-support",
        "code_generation": "./adapters/code-gen",
        "summarization": "./adapters/summary"
    }
)

# Switch between adapters
switch_adapter(model, "customer_support")
response = generate(model, tokenizer, "How do I reset my password?")

switch_adapter(model, "code_generation")
response = generate(model, tokenizer, "Write a Python function to sort a list")
```

### Hyperparameter Tuning

```python
from dataclasses import dataclass
from typing import List

@dataclass
class LoRAExperiment:
    rank: int
    alpha: int
    dropout: float
    target_modules: List[str]

def run_lora_experiment(
    base_model_name: str,
    train_dataset,
    experiment: LoRAExperiment,
    output_dir: str
):
    """Run a single LoRA experiment."""
    # Load model
    model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        torch_dtype=torch.float16,
        device_map="auto"
    )

    # Configure LoRA
    config = LoraConfig(
        r=experiment.rank,
        lora_alpha=experiment.alpha,
        lora_dropout=experiment.dropout,
        target_modules=experiment.target_modules,
        task_type=TaskType.CAUSAL_LM
    )

    model = get_peft_model(model, config)

    # Train
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=1,
        per_device_train_batch_size=4,
        learning_rate=2e-4,
        fp16=True,
        logging_steps=10,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
    )

    trainer.train()

    return trainer.state.log_history

# Experiment grid
experiments = [
    LoRAExperiment(rank=4, alpha=16, dropout=0.05, target_modules=["q_proj", "v_proj"]),
    LoRAExperiment(rank=8, alpha=32, dropout=0.05, target_modules=["q_proj", "v_proj"]),
    LoRAExperiment(rank=16, alpha=32, dropout=0.1, target_modules=["q_proj", "v_proj", "k_proj", "o_proj"]),
    LoRAExperiment(rank=32, alpha=64, dropout=0.1, target_modules=["q_proj", "v_proj", "k_proj", "o_proj"]),
]

for i, exp in enumerate(experiments):
    results = run_lora_experiment(
        "meta-llama/Llama-2-7b-hf",
        train_dataset,
        exp,
        f"./experiments/exp_{i}"
    )
    print(f"Experiment {i}: rank={exp.rank}, loss={results[-1]['loss']}")
```

### SFTTrainer with LoRA

```python
from trl import SFTTrainer

def train_with_sft_trainer(
    model_name: str,
    dataset,
    lora_config: LoraConfig,
    output_dir: str
):
    """Train using TRL's SFTTrainer (recommended approach)."""
    # Load model with quantization
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
    )

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map="auto"
    )

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token

    # Training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=3,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        fp16=True,
        logging_steps=10,
        save_strategy="epoch",
        warmup_ratio=0.03,
    )

    # SFTTrainer handles LoRA setup
    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        tokenizer=tokenizer,
        args=training_args,
        peft_config=lora_config,
        max_seq_length=512,
        formatting_func=format_instruction,  # Your formatting function
    )

    trainer.train()
    trainer.save_model()

    return trainer
```

### Production LoRA Pipeline

```python
from dataclasses import dataclass
from typing import List, Dict, Optional
import logging
import os

@dataclass
class LoRAConfig:
    base_model: str
    rank: int = 8
    alpha: int = 32
    dropout: float = 0.05
    target_modules: List[str] = None
    use_4bit: bool = True
    max_length: int = 512
    batch_size: int = 4
    num_epochs: int = 3
    learning_rate: float = 2e-4

class LoRATrainingPipeline:
    """Production LoRA fine-tuning pipeline."""

    def __init__(self, config: LoRAConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)

        if config.target_modules is None:
            config.target_modules = ["q_proj", "k_proj", "v_proj", "o_proj"]

    def prepare_model(self):
        """Load and prepare model for training."""
        self.logger.info(f"Loading model: {self.config.base_model}")

        if self.config.use_4bit:
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16,
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                self.config.base_model,
                quantization_config=bnb_config,
                device_map="auto"
            )
            self.model = prepare_model_for_kbit_training(self.model)
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                self.config.base_model,
                torch_dtype=torch.float16,
                device_map="auto"
            )

        self.tokenizer = AutoTokenizer.from_pretrained(self.config.base_model)
        self.tokenizer.pad_token = self.tokenizer.eos_token

        # Apply LoRA
        lora_config = LoraConfig(
            r=self.config.rank,
            lora_alpha=self.config.alpha,
            lora_dropout=self.config.dropout,
            target_modules=self.config.target_modules,
            task_type=TaskType.CAUSAL_LM
        )

        self.model = get_peft_model(self.model, lora_config)
        self.model.print_trainable_parameters()

    def train(
        self,
        train_data: List[Dict],
        val_data: Optional[List[Dict]] = None,
        output_dir: str = "./lora-output"
    ) -> Dict:
        """Run training."""
        # Prepare datasets
        train_dataset = prepare_dataset(train_data, self.tokenizer, self.config.max_length)

        val_dataset = None
        if val_data:
            val_dataset = prepare_dataset(val_data, self.tokenizer, self.config.max_length)

        # Training args
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=self.config.num_epochs,
            per_device_train_batch_size=self.config.batch_size,
            gradient_accumulation_steps=4,
            learning_rate=self.config.learning_rate,
            fp16=True,
            logging_steps=10,
            save_strategy="epoch",
            evaluation_strategy="epoch" if val_dataset else "no",
            warmup_ratio=0.03,
            lr_scheduler_type="cosine",
            optim="paged_adamw_8bit" if self.config.use_4bit else "adamw_torch",
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            data_collator=DataCollatorForLanguageModeling(self.tokenizer, mlm=False)
        )

        self.logger.info("Starting training...")
        trainer.train()

        # Save
        self.model.save_pretrained(output_dir)
        self.tokenizer.save_pretrained(output_dir)

        return {
            "status": "completed",
            "output_dir": output_dir,
            "train_loss": trainer.state.log_history[-1].get("train_loss")
        }

    def evaluate(self, test_data: List[Dict]) -> Dict:
        """Evaluate model on test data."""
        self.model.eval()
        correct = 0
        total = len(test_data)

        for example in test_data:
            prompt = format_instruction({
                "instruction": example["instruction"],
                "input": example.get("input", ""),
                "output": ""
            }).split("### Response:")[0] + "### Response:"

            generated = generate(self.model, self.tokenizer, prompt)
            expected = example["output"]

            # Simple match check
            if expected.lower().strip() in generated.lower():
                correct += 1

        return {
            "accuracy": correct / total,
            "total": total,
            "correct": correct
        }
```

## Best Practices

1. **Rank Selection**
   - Start with r=8, increase if underfitting
   - Higher rank = more parameters = better fit but slower
   - r=4 often sufficient for simple tasks

2. **Target Modules**
   - At minimum: q_proj, v_proj
   - Better: add k_proj, o_proj
   - MLP layers for complex tasks

3. **Learning Rate**
   - Higher than full fine-tuning (1e-4 to 3e-4)
   - Use warmup (3-5% of steps)
   - Cosine scheduler works well

4. **Memory Optimization**
   - Use 4-bit quantization (QLoRA)
   - Gradient checkpointing
   - Gradient accumulation

5. **Data Quality**
   - Quality > quantity
   - Diverse examples
   - Consistent formatting

## Common Pitfalls

1. **Wrong Target Modules** - Not adapting important layers
2. **Rank Too Low** - Underfitting on complex tasks
3. **Learning Rate Too High** - Training instability
4. **No Warmup** - Loss spikes early in training
5. **Inconsistent Formatting** - Model confusion
6. **Forgetting Tokenizer** - Pad token not set

## References

- [LoRA Paper](https://arxiv.org/abs/2106.09685)
- [QLoRA Paper](https://arxiv.org/abs/2305.14314)
- [PEFT Library](https://huggingface.co/docs/peft)
- [TRL Library](https://huggingface.co/docs/trl)
