---
name: grpo-rewards
description: Implement token-level rewards in TRL's GRPOTrainer. Use when modifying reward computation or debugging reward tensor shapes.
---

## TRL Reward Integration

TRL's GRPOTrainer expects rewards from a function. To inject token-level penalties:

```python
def steganography_reward(completions: list[str], prompts: list[str], **kwargs) -> list[float]:
    """
    Reward function for GRPOTrainer.
    
    Returns list of scalar rewards (one per completion).
    For token-level penalties, we aggregate within this function.
    
    Args:
        completions: Generated texts (batch_size,)
        prompts: Original prompts (batch_size,)
        **kwargs: Additional context from trainer
        
    Returns:
        List of scalar rewards, length = batch_size
    """
    rewards = []
    for completion, prompt in zip(completions, prompts):
        # Parse CoT and answer
        cot = extract_between_tags(completion, "think")
        answer = extract_between_tags(completion, "answer")
        
        # Task reward (asymmetric weighting - correct answers worth more)
        correct = check_answer(answer, get_ground_truth(prompt))
        r_task = 2.0 if correct else 0.0
        
        # Token penalty (dense but aggregated to scalar)
        penalty = compute_token_penalty(cot, banned_tokens, tokenizer)
        
        rewards.append(r_task + penalty)
    return rewards
```

## Token Penalty Computation

```python
def compute_token_penalty(
    cot_text: str,
    banned_tokens: set[int],
    tokenizer,
    penalty_per_token: float = -0.1
) -> float:
    """
    Compute aggregated penalty for banned tokens in CoT.
    
    Args:
        cot_text: Chain-of-thought text (content inside <think>)
        banned_tokens: Set of token IDs that trigger penalties
        tokenizer: HuggingFace tokenizer
        penalty_per_token: Penalty magnitude per banned token occurrence
        
    Returns:
        Aggregated scalar penalty (negative value)
    """
    if not cot_text:
        return 0.0
    
    token_ids = tokenizer.encode(cot_text, add_special_tokens=False)
    penalty = sum(
        penalty_per_token 
        for tid in token_ids 
        if tid in banned_tokens
    )
    return penalty
```

## Key Configuration

```python
from trl import GRPOConfig, GRPOTrainer

config = GRPOConfig(
    # GRPO-specific
    num_generations=8,          # Group size for variance estimation (G in paper)
    
    # Regularization
    kl_coef=0.05,               # Moderate KL penalty to prevent drift
    entropy_coef=0.02,          # Small entropy bonus to prevent collapse
    
    # Training
    learning_rate=1e-5,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    max_steps=1000,
    
    # Generation
    max_new_tokens=512,
    temperature=0.7,
    
    # LoRA (if using PEFT)
    use_peft=True,
)

trainer = GRPOTrainer(
    model=model,
    args=config,
    train_dataset=dataset,
    reward_funcs=[steganography_reward],  # List of reward functions
    tokenizer=tokenizer,
)
```

## Shape Requirements

| Variable | Shape/Type | Description |
|----------|------------|-------------|
| `completions` | `List[str]` length B | Generated texts |
| `prompts` | `List[str]` length B | Input prompts |
| Return value | `List[float]` length B | Scalar rewards |

TRL handles the RL math internally - you just provide the scalar reward per completion.

## Curriculum Strategy

```python
def curriculum_reward(completions, prompts, step: int, **kwargs):
    """Reward with curriculum-based penalty scaling."""
    
    # Ramp up penalty strength over training
    warmup_steps = 500
    penalty_scale = min(1.0, step / warmup_steps)
    
    rewards = []
    for completion, prompt in zip(completions, prompts):
        cot = extract_between_tags(completion, "think")
        answer = extract_between_tags(completion, "answer")
        
        r_task = 2.0 if check_answer(answer, get_ground_truth(prompt)) else 0.0
        penalty = compute_token_penalty(cot, banned_tokens, tokenizer)
        
        # Scale penalty by curriculum
        scaled_penalty = penalty * penalty_scale
        
        rewards.append(r_task + scaled_penalty)
    return rewards
```

## Debugging Rewards

```python
# Add to reward function for debugging
import wandb

def steganography_reward_debug(completions, prompts, **kwargs):
    rewards = []
    penalties = []
    task_rewards = []
    
    for completion, prompt in zip(completions, prompts):
        cot = extract_between_tags(completion, "think")
        answer = extract_between_tags(completion, "answer")
        
        r_task = 2.0 if check_answer(answer, get_ground_truth(prompt)) else 0.0
        penalty = compute_token_penalty(cot, banned_tokens, tokenizer)
        
        task_rewards.append(r_task)
        penalties.append(penalty)
        rewards.append(r_task + penalty)
    
    # Log to W&B
    wandb.log({
        "reward/mean": sum(rewards) / len(rewards),
        "reward/task_mean": sum(task_rewards) / len(task_rewards),
        "reward/penalty_mean": sum(penalties) / len(penalties),
        "reward/accuracy": sum(1 for r in task_rewards if r > 0) / len(task_rewards),
    })
    
    return rewards
```

## Common Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| Rewards all zero | CoT extraction failing | Check tag parsing regex |
| Accuracy collapse | Penalty too strong | Reduce `penalty_per_token` or use curriculum |
| Reward explosion | No normalization | Clip rewards to `[-5, 5]` range |
| NaN losses | Empty completions | Add length check and default reward |
