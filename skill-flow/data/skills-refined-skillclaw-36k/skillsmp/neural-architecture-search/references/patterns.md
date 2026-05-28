# Neural Architecture Search

## Patterns

### **Golden Rules**
  
---
    ##### **Rule**
Define search space carefully
    ##### **Reason**
Too large = intractable, too small = miss optima
  
---
    ##### **Rule**
Use efficient evaluation strategies
    ##### **Reason**
Full training per candidate is prohibitively expensive
  
---
    ##### **Rule**
Start with proxy tasks
    ##### **Reason**
Smaller dataset, fewer epochs for quick filtering
  
---
    ##### **Rule**
Consider the deployment target
    ##### **Reason**
Best accuracy != best latency/memory tradeoff
  
---
    ##### **Rule**
Track all experiments
    ##### **Reason**
Reproducibility is critical for NAS
  
---
    ##### **Rule**
Set compute budgets upfront
    ##### **Reason**
NAS can consume unlimited resources
### **Three Pillars**
  #### **Search Space**
    ##### **Description**
What architectures are possible?
    ##### **Components**
      - Layer types
      - Number of layers
      - Connections
      - Hyperparameters
      - Operations
  #### **Search Strategy**
    ##### **Description**
How to explore the space?
    ##### **Methods**
      - Random search
      - Grid search
      - Bayesian optimization
      - Evolutionary algorithms
      - Reinforcement learning
      - Gradient-based (DARTS)
  #### **Performance Estimation**
    ##### **Description**
How to evaluate efficiently?
    ##### **Methods**
      - Full training (slow but accurate)
      - Early stopping (train partially)
      - Weight sharing (one-shot methods)
      - Surrogate models (predict performance)
      - Learning curve extrapolation
### **Search Strategies**
  #### **Random Search**
    ##### **Description**
Surprisingly effective baseline
    ##### **Note**
Often outperforms grid search for same compute
  #### **Bayesian Optimization**
    ##### **Description**
Model objective with surrogate (GP)
    ##### **Acquisition**
Expected Improvement balances explore/exploit
    ##### **Best For**
Expensive evaluations, continuous spaces
  #### **Darts**
    ##### **Description**
Differentiable architecture search
    ##### **Key Insight**
Continuous relaxation of discrete choices
    ##### **Formula**
mixed_op(x) = sum(softmax(alpha_i) * op_i(x))
  #### **Evolutionary**
    ##### **Description**
Population-based search
    ##### **Best For**
Large discrete search spaces
### **Efficient Evaluation**
  #### **Successive Halving**
    ##### **Description**
Start many configs, keep top 1/eta fraction
    ##### **Hyperband**
Multi-fidelity version
  #### **Weight Sharing**
    ##### **Description**
Train supernet, extract subnets
    ##### **Pros**
Train once, evaluate many
    ##### **Cons**
Weight coupling between architectures
  #### **Early Stopping**
    ##### **Description**
Stop unpromising trials early
    ##### **Tools**
Optuna pruning, Hyperband

## Anti-Patterns


---
  #### **Pattern**
Search space too large
  #### **Problem**
Never converges
  #### **Solution**
Constrain based on domain knowledge

---
  #### **Pattern**
No early stopping
  #### **Problem**
Wastes compute on bad configs
  #### **Solution**
Successive halving, Optuna pruning

---
  #### **Pattern**
Full training per trial
  #### **Problem**
Prohibitively expensive
  #### **Solution**
Weight sharing, proxy tasks

---
  #### **Pattern**
Ignoring transfer
  #### **Problem**
Starting from scratch each time
  #### **Solution**
Warm-start from similar tasks

---
  #### **Pattern**
No reproducibility
  #### **Problem**
Can't replicate results
  #### **Solution**
Log all configs, set seeds

---
  #### **Pattern**
Overfitting to proxy
  #### **Problem**
Best on proxy != best on target
  #### **Solution**
Validate on full task periodically