# Neural Architecture Search - Sharp Edges

## Search Space Too Large to Explore

### **Id**
search-space-explosion
### **Severity**
high
### **Summary**
Combinatorial explosion makes finding good architectures unlikely
### **Symptoms**
  - Search never converges
  - Best found architecture is mediocre
  - Huge variance between runs
  - Compute budget exhausted quickly
### **Why**
  A search space with n choices per layer and L layers has n^L configurations.
  Even 5 choices over 12 layers = 244 million configurations.
  Random sampling will miss good regions entirely.
  
### **Gotcha**
  # Overly broad search space
  search_space = {
      'num_layers': (1, 100),
      'hidden_dim': (16, 4096),
      'num_heads': (1, 64),
      'activation': ['relu', 'gelu', 'swish', 'mish', 'selu', ...],
      'dropout': (0.0, 0.9),
      ...
  }
  # Too many combinations to explore meaningfully
  
### **Solution**
  # Constrained search space based on domain knowledge
  search_space = {
      'num_layers': [6, 8, 12],  # Known good values
      'hidden_dim': [256, 512, 768],  # Reasonable range
      'num_heads': [4, 8, 12],  # Must divide hidden_dim
      'activation': ['gelu', 'swish'],  # Best performers
      'dropout': [0.1, 0.2, 0.3],  # Typical range
  }
  
  # Or use cell-based search (DARTS-style)
  # Search for cell structure, then stack cells
  

## Proxy Task Doesn't Predict Full Task Performance

### **Id**
proxy-task-mismatch
### **Severity**
high
### **Summary**
Architecture ranked best on proxy fails on real task
### **Symptoms**
  - Top proxy architecture underperforms baseline on full task
  - Rankings don't correlate between proxy and full
  - Small models favored on proxy but don't scale
### **Why**
  Proxy tasks (small data, few epochs) can have different optima
  than the full task. What works at small scale may not scale.
  Regularization needs differ between small and large data.
  
### **Gotcha**
  # Proxy: 10% of data, 10 epochs
  def evaluate_on_proxy(architecture):
      model = build_model(architecture)
      score = train(model, data[:1000], epochs=10)
      return score
  
  # Best proxy architecture may not be best at full scale
  # Overfit architectures look good on small data
  
### **Solution**
  # 1. Validate periodically on full task
  if trial % 50 == 0:
      full_score = train(best_so_far, full_data, full_epochs)
      if full_score < baseline:
          adjust_search_space()
  
  # 2. Use fidelity-aware methods (Hyperband)
  # Train promising configs longer
  
  # 3. Rank correlation check
  # Sample configs, evaluate on both proxy and full
  # Ensure Spearman correlation > 0.7
  

## Weight Sharing Leads to Wrong Architecture Rankings

### **Id**
weight-sharing-collapse
### **Severity**
medium
### **Summary**
Supernet weights don't transfer to standalone training
### **Symptoms**
  - Top supernet paths perform poorly when trained independently
  - All paths have similar performance
  - Extracted architecture significantly underperforms
### **Why**
  In weight-sharing NAS, all architectures share the same weights.
  This creates coupling: improving one path can hurt another.
  The optimal weights for the supernet differ from optimal for any subnet.
  
### **Gotcha**
  # One-shot NAS with heavy weight sharing
  supernet.train(data)
  rankings = [(arch, supernet.evaluate(arch)) for arch in candidates]
  best_arch = max(rankings, key=lambda x: x[1])
  
  # Standalone training may give very different results!
  
### **Solution**
  # 1. Fair sampling during supernet training
  for batch in dataloader:
      # Random architecture each batch
      arch = sample_random_architecture()
      loss = supernet.forward_with_arch(batch, arch)
      loss.backward()
  
  # 2. Longer standalone retraining
  # Don't trust supernet rankings directly
  # Retrain top-10 from scratch, pick best
  
  # 3. Few-shot NAS
  # Partially inherit weights, fine-tune for a few epochs
  

## NAS Results Not Reproducible

### **Id**
reproducibility-failure
### **Severity**
medium
### **Summary**
Can't replicate found architecture or its performance
### **Symptoms**
  - Rerunning search finds different architecture
  - Same architecture gives different scores
  - Published results can't be reproduced
### **Why**
  NAS involves many sources of randomness:
  - Search algorithm randomness
  - Weight initialization
  - Data shuffling
  - GPU non-determinism
  Without proper seeding and logging, results are irreproducible.
  
### **Gotcha**
  # No seed setting or experiment tracking
  study = optuna.create_study()
  study.optimize(objective, n_trials=100)
  best = study.best_params
  # Can't reproduce this run!
  
### **Solution**
  # 1. Set all seeds
  import random
  import numpy as np
  import torch
  
  def set_seed(seed):
      random.seed(seed)
      np.random.seed(seed)
      torch.manual_seed(seed)
      torch.cuda.manual_seed_all(seed)
      torch.backends.cudnn.deterministic = True
  
  # 2. Log everything
  study = optuna.create_study(
      study_name="nas_experiment_001",
      storage="sqlite:///optuna.db",
  )
  
  # 3. Save search state for resume
  study.optimize(objective, n_trials=100,
                 callbacks=[SaveStateCallback()])
  