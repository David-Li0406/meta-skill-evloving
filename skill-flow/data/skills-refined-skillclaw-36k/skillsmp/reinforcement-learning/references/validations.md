# Reinforcement Learning - Validations

## PPO Without Clipping

### **Id**
ppo-no-clipping
### **Severity**
error
### **Type**
regex
### **Pattern**
  - ratio.*advantage(?!.*clamp|clip)
  - policy_loss.*=.*-.*ratio.*advantage(?!.*min)
### **Message**
PPO requires clipping to prevent catastrophic policy updates.
### **Fix Action**
Add: torch.clamp(ratio, 1-eps, 1+eps) and use min of clipped/unclipped
### **Applies To**
  - **/*.py

## Advantages Not Normalized

### **Id**
no-advantage-normalization
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - advantage.*=(?!.*(mean|std|normalize))
### **Message**
Normalizing advantages reduces variance and improves training stability.
### **Fix Action**
Add: advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
### **Applies To**
  - **/*ppo*.py
  - **/*rl*.py

## Missing Entropy Bonus

### **Id**
no-entropy-bonus
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - policy_loss(?!.*entropy)
  - actor_loss(?!.*entropy)
### **Message**
Entropy bonus encourages exploration and prevents premature convergence.
### **Fix Action**
Add: total_loss = policy_loss - entropy_coef * entropy.mean()
### **Applies To**
  - **/*ppo*.py
  - **/*a2c*.py

## RLHF Without KL Penalty

### **Id**
rlhf-no-kl-penalty
### **Severity**
error
### **Type**
regex
### **Pattern**
  - reward_model.*response(?!.*kl|.*reference)
### **Message**
RLHF requires KL penalty to prevent model drift and reward hacking.
### **Fix Action**
Add: reward = reward_score - kl_coef * kl_divergence(policy, reference)
### **Applies To**
  - **/*rlhf*.py
  - **/*alignment*.py

## DQN Without Target Network

### **Id**
dqn-no-target-network
### **Severity**
error
### **Type**
regex
### **Pattern**
  - q_network.*max(?!.*target)
  - q_net.*next_state(?!.*target)
### **Message**
DQN requires separate target network for stable learning.
### **Fix Action**
Add target network and periodically update: target_net.load_state_dict(q_net.state_dict())
### **Applies To**
  - **/*dqn*.py
  - **/*q_learning*.py

## RL Training Without Gradient Clipping

### **Id**
no-gradient-clipping-rl
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - loss\.backward\(\)\s*\n\s*optimizer\.step(?!.*clip_grad)
### **Message**
RL training benefits from gradient clipping for stability.
### **Fix Action**
Add: nn.utils.clip_grad_norm_(parameters, max_grad_norm)
### **Applies To**
  - **/*rl*.py
  - **/*ppo*.py

## Training Without Reward Logging

### **Id**
no-reward-logging
### **Severity**
info
### **Type**
regex
### **Pattern**
  - for.*episode(?!.*log|.*print|.*wandb|.*writer)
### **Message**
RL training requires careful monitoring of reward and metrics.
### **Fix Action**
Log: episode_reward, policy_loss, value_loss, entropy, KL divergence
### **Applies To**
  - **/*train*.py
  - **/*rl*.py