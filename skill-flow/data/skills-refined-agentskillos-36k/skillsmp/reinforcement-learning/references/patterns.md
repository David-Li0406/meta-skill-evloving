# Reinforcement Learning

## Patterns

### **Golden Rules**
  
---
    ##### **Rule**
Reward shaping is critical
    ##### **Reason**
Sparse rewards make learning nearly impossible
  
---
    ##### **Rule**
Start simple, scale up
    ##### **Reason**
Debug on toy environments before complex ones
  
---
    ##### **Rule**
Monitor training metrics obsessively
    ##### **Reason**
RL training is notoriously unstable
  
---
    ##### **Rule**
Use appropriate baselines
    ##### **Reason**
Reduces variance in policy gradients
  
---
    ##### **Rule**
Clip/constrain policy updates
    ##### **Reason**
Prevents catastrophic policy collapse
  
---
    ##### **Rule**
Separate exploration from exploitation
    ##### **Reason**
Ensures sufficient state-space coverage
### **Algorithm Taxonomy**
  #### **Value Based**
    ##### **Algorithms**
      - Q-Learning
      - DQN
      - Double DQN
      - Dueling DQN
    ##### **Learns**
Q(s,a) - Value of state-action pairs
    ##### **Best For**
      - Discrete actions
      - Atari games
  #### **Policy Based**
    ##### **Algorithms**
      - REINFORCE
      - Policy Gradient
    ##### **Learns**
pi(a|s) - Policy directly
    ##### **Best For**
      - Continuous actions
      - Robotics
  #### **Actor Critic**
    ##### **Algorithms**
      - A2C/A3C
      - PPO
      - SAC
      - TRPO
    ##### **Learns**
Both V and pi
    ##### **Best For**
      - Most tasks
      - LLM alignment
### **On Vs Off Policy**
  #### **On Policy**
    ##### **Algorithms**
      - PPO
      - A2C
    ##### **Property**
Learn from current policy samples
    ##### **Pros**
More stable
    ##### **Cons**
Fresh data required
  #### **Off Policy**
    ##### **Algorithms**
      - DQN
      - SAC
    ##### **Property**
Learn from any policy samples
    ##### **Pros**
More sample efficient
    ##### **Cons**
Requires replay buffer
### **Discount Factor**
  #### **Short Horizon**

  #### **Medium Horizon**

  #### **Long Horizon**

  #### **Infinite Horizon**

### **Ppo Config**
  #### **Clip Epsilon**
0.1-0.3 (typically 0.2)
  #### **Entropy Coef**
0.01 (encourages exploration)
  #### **Value Coef**
0.5
  #### **Max Grad Norm**
0.5
  #### **N Epochs**
3-10 per batch
### **Rlhf Pipeline**
  #### **Step1 Sft**
    ##### **Description**
Supervised Fine-Tuning
    ##### **Purpose**
Establish baseline helpful behavior
  #### **Step2 Reward Model**
    ##### **Description**
Train on human preference comparisons
    ##### **Output**
Reward(prompt, response) = scalar
    ##### **Loss**
Bradley-Terry: -log(sigmoid(r_chosen - r_rejected))
  #### **Step3 Ppo**
    ##### **Description**
Optimize policy with KL penalty
    ##### **Formula**
reward = r(x,y) - beta * KL(pi || pi_ref)

## Anti-Patterns


---
  #### **Pattern**
Sparse rewards
  #### **Problem**
Agent learns nothing
  #### **Solution**
Reward shaping, dense rewards

---
  #### **Pattern**
No baseline/advantage
  #### **Problem**
High variance gradients
  #### **Solution**
Use GAE, value baseline

---
  #### **Pattern**
Large policy updates
  #### **Problem**
Training collapse
  #### **Solution**
PPO clipping, KL penalty

---
  #### **Pattern**
No replay buffer (off-policy)
  #### **Problem**
Sample inefficiency
  #### **Solution**
Experience replay

---
  #### **Pattern**
Same network for Q and target
  #### **Problem**
Unstable learning
  #### **Solution**
Separate target network

---
  #### **Pattern**
Ignoring KL in RLHF
  #### **Problem**
Model drift, reward hacking
  #### **Solution**
KL penalty to reference model