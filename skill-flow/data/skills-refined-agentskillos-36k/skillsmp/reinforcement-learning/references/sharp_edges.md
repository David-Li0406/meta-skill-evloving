# Reinforcement Learning - Sharp Edges

## Reward Hacking in RLHF

### **Id**
reward-hacking
### **Severity**
critical
### **Summary**
Model finds exploits in reward model instead of being helpful
### **Symptoms**
  - Reward score increases but quality decreases
  - Model produces verbose but unhelpful responses
  - Responses game the reward model's biases
  - Human evaluators disagree with high reward scores
### **Why**
  The reward model is an imperfect proxy for human preferences.
  Given enough optimization pressure, the policy finds reward model exploits.
  Common exploits: verbosity, sycophancy, specific phrases reward model likes.
  
### **Gotcha**
  # Optimizing reward too aggressively
  for step in range(1000000):
      reward = reward_model(response)
      loss = -reward  # Pure reward maximization
      loss.backward()
      # Model learns to game reward model
  
### **Solution**
  # 1. KL penalty to stay close to reference
  reward = reward_model(response) - kl_coef * kl_divergence(policy, reference)
  
  # 2. Periodically refresh reward model on new data
  # 3. Ensemble multiple reward models
  # 4. Human evaluation checkpoints
  
  # 5. Early stopping based on held-out evaluation
  if eval_score < best_score - tolerance:
      break  # Stop before overfitting to reward model
  

## Catastrophic Policy Collapse

### **Id**
policy-collapse
### **Severity**
critical
### **Summary**
Policy suddenly degenerates after seeming stable
### **Symptoms**
  - Entropy drops to near zero
  - Policy outputs become deterministic/repetitive
  - Reward suddenly crashes
  - All samples look identical
### **Why**
  Without proper constraints, policy gradient updates can be too large.
  A large bad update can push the policy into a degenerate state.
  From there, all samples reinforce the bad behavior.
  
### **Gotcha**
  # REINFORCE without clipping
  ratio = new_prob / old_prob
  loss = -ratio * advantage  # No limit on ratio!
  # If ratio >> 1, can destroy the policy
  
### **Solution**
  # PPO clipping prevents catastrophic updates
  ratio = torch.exp(new_log_prob - old_log_prob)
  
  surr1 = ratio * advantage
  surr2 = torch.clamp(ratio, 1 - clip_epsilon, 1 + clip_epsilon) * advantage
  
  loss = -torch.min(surr1, surr2).mean()
  
  # Also: monitor entropy, add entropy bonus
  entropy_bonus = -entropy_coef * entropy.mean()
  total_loss = loss + entropy_bonus
  

## Agent Never Learns Due to Sparse Rewards

### **Id**
sparse-reward-failure
### **Severity**
high
### **Summary**
Reward signal too rare for learning to occur
### **Symptoms**
  - Agent takes random actions indefinitely
  - No improvement over random baseline
  - Policy gradient has near-zero signal
### **Why**
  If reward only comes at episode end (or rarely), the agent gets no
  feedback about which intermediate actions were good.
  Credit assignment becomes impossible.
  
### **Gotcha**
  # Sparse reward environment
  def step(action):
      # Only reward at the very end
      if is_goal_reached():
          return observation, 1.0, True, {}  # Reward only here
      return observation, 0.0, False, {}  # No intermediate signal
  
### **Solution**
  # 1. Reward shaping - add intermediate rewards
  def shaped_reward(state, action, next_state):
      sparse = 1.0 if is_goal_reached(next_state) else 0.0
  
      # Potential-based shaping (preserves optimal policy)
      potential_diff = gamma * potential(next_state) - potential(state)
  
      return sparse + shaping_coef * potential_diff
  
  # 2. Curiosity-driven exploration
  # 3. Hierarchical RL with subgoals
  # 4. Curriculum learning - start with easier tasks
  

## Q-Value Overestimation in DQN

### **Id**
value-function-overestimation
### **Severity**
high
### **Summary**
Q-learning systematically overestimates values
### **Symptoms**
  - Q-values grow unrealistically large
  - Agent is overconfident about bad actions
  - Performance is worse than expected from Q-values
### **Why**
  max_a Q(s,a) takes the maximum over noisy estimates.
  This systematically picks the action with the highest positive noise.
  Over many updates, this bias compounds.
  
### **Gotcha**
  # Standard DQN - has overestimation bias
  target_q = reward + gamma * target_net(next_state).max()
  # max() selects the noisiest high estimate
  
### **Solution**
  # Double DQN - use online net to select, target net to evaluate
  next_actions = online_net(next_state).argmax(dim=1)
  target_q = reward + gamma * target_net(next_state).gather(1, next_actions)
  
  # The action selection and value estimation use different networks
  # This breaks the overestimation cycle
  

## KL Divergence Explodes During RLHF

### **Id**
kl-divergence-explosion
### **Severity**
high
### **Summary**
Policy drifts too far from reference model
### **Symptoms**
  - KL penalty term dominates the loss
  - Model forgets base capabilities
  - Responses become incoherent
  - Generation quality degrades
### **Why**
  Without proper KL constraint, the policy can drift arbitrarily far.
  The reference model represents the base capabilities we want to preserve.
  Drifting too far means catastrophic forgetting.
  
### **Gotcha**
  # KL coefficient too low
  kl_coef = 0.001  # Too weak!
  reward = reward_score - kl_coef * kl  # Barely constrains
  
### **Solution**
  # 1. Appropriate KL coefficient (0.1 - 0.5 typical)
  kl_coef = 0.1
  
  # 2. Adaptive KL penalty
  if kl > target_kl * 1.5:
      kl_coef *= 1.5
  elif kl < target_kl / 1.5:
      kl_coef /= 1.5
  
  # 3. Hard KL constraint (TRPO-style)
  if kl > max_kl:
      reject_update()
  