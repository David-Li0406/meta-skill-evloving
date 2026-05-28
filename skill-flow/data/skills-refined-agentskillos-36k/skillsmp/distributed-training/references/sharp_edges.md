# Distributed Training - Sharp Edges

## Distributed Training Hangs on Gradient Sync

### **Id**
gradient-sync-deadlock
### **Severity**
critical
### **Summary**
One process waits forever for others that diverged
### **Symptoms**
  - Training hangs indefinitely
  - No error message, just frozen
  - GPU utilization drops to 0%
  - NCCL timeout errors after long wait
### **Why**
  All processes must call the same operations in the same order.
  If one process takes a different code path (e.g., skips a batch),
  other processes wait forever for a synchronization that never comes.
  
### **Gotcha**
  for batch in dataloader:
      if batch['size'] < min_batch_size:
          continue  # WRONG: Other processes don't skip!
  
      loss = model(batch)
      loss.backward()  # Hangs - other processes at different batch
  
### **Solution**
  # All processes must make same decisions
  # Use distributed-aware filtering
  
  # Option 1: Filter before distributed sampler
  filtered_dataset = [x for x in dataset if valid(x)]
  
  # Option 2: Pad/mask instead of skip
  if batch['size'] < min_batch_size:
      # Pad to min_batch_size instead of skipping
      batch = pad_batch(batch)
  
  # Option 3: Collective decision
  should_skip = batch['size'] < min_batch_size
  all_should_skip = dist.all_reduce(should_skip, op=dist.ReduceOp.MAX)
  if all_should_skip:
      continue  # All processes skip together
  

## FSDP CPU Offload Still OOMs

### **Id**
fsdp-cpu-offload-oom
### **Severity**
high
### **Summary**
CPU offload doesn't help if params don't fit during forward
### **Symptoms**
  - OOM during forward pass despite CPU offload
  - Memory spikes when gathering parameters
  - Offload seems to have no effect
### **Why**
  FSDP CPU offload stores parameters on CPU between forward/backward.
  But during forward, parameters must be gathered to GPU.
  If the full layer doesn't fit, you still OOM.
  
### **Gotcha**
  # CPU offload enabled but model still OOMs
  fsdp_model = FSDP(
      model,
      cpu_offload=CPUOffload(offload_params=True),
  )
  # OOM on first forward - layer too large!
  
### **Solution**
  # 1. Use finer-grained wrapping
  # Wrap individual layers, not whole model
  for layer in model.layers:
      FSDP(layer, cpu_offload=CPUOffload(offload_params=True))
  
  # 2. Combine with activation checkpointing
  model.gradient_checkpointing_enable()
  
  # 3. Consider DeepSpeed with NVMe offload
  # For truly massive models
  
  # 4. Use model parallelism for huge layers
  # Some layers must be split across GPUs
  

## fp16 Training Produces NaN/Inf

### **Id**
mixed-precision-loss-scaling
### **Severity**
high
### **Summary**
Gradient underflow/overflow without proper loss scaling
### **Symptoms**
  - Loss becomes NaN after some steps
  - Gradients are all zeros
  - Model parameters become inf
### **Why**
  fp16 has limited dynamic range (5.96e-8 to 65504).
  Small gradients underflow to zero.
  Without loss scaling, training fails silently.
  
### **Gotcha**
  # fp16 without loss scaling
  with torch.autocast(dtype=torch.float16):
      loss = model(batch)
  
  loss.backward()  # Gradients may underflow!
  optimizer.step()
  
### **Solution**
  # Option 1: Use bf16 (no scaling needed, wider range)
  with torch.autocast(dtype=torch.bfloat16):
      loss = model(batch)
  loss.backward()
  optimizer.step()
  
  # Option 2: fp16 with GradScaler
  from torch.cuda.amp import GradScaler
  scaler = GradScaler()
  
  with torch.autocast(dtype=torch.float16):
      loss = model(batch)
  
  scaler.scale(loss).backward()
  scaler.step(optimizer)
  scaler.update()
  

## Same Data Order Every Epoch

### **Id**
distributed-sampler-shuffle
### **Severity**
medium
### **Summary**
Forgetting set_epoch() on DistributedSampler
### **Symptoms**
  - Model sees same batch order every epoch
  - Validation metrics oscillate without improving
  - Training seems to plateau early
### **Why**
  DistributedSampler uses epoch as random seed.
  Without set_epoch(), same shuffling every epoch.
  Model overfits to the order, not the data.
  
### **Gotcha**
  train_sampler = DistributedSampler(dataset)
  train_loader = DataLoader(dataset, sampler=train_sampler)
  
  for epoch in range(epochs):
      for batch in train_loader:  # Same order every epoch!
          train(batch)
  
### **Solution**
  train_sampler = DistributedSampler(dataset)
  train_loader = DataLoader(dataset, sampler=train_sampler)
  
  for epoch in range(epochs):
      train_sampler.set_epoch(epoch)  # Different shuffle each epoch!
  
      for batch in train_loader:
          train(batch)
  

## Loading Checkpoint on Wrong Number of GPUs

### **Id**
checkpoint-rank-mismatch
### **Severity**
medium
### **Summary**
Sharded checkpoint doesn't match current world size
### **Symptoms**
  - Checkpoint loading fails
  - Shape mismatch errors
  - Missing or extra keys in state dict
### **Why**
  FSDP/DeepSpeed shard checkpoints across processes.
  Loading on different number of GPUs requires resharding.
  Naive torch.load() doesn't handle this.
  
### **Gotcha**
  # Saved on 8 GPUs, loading on 4
  state_dict = torch.load("checkpoint.pt")
  model.load_state_dict(state_dict)  # Shape mismatch!
  
### **Solution**
  # Use FSDP's checkpoint utilities
  from torch.distributed.checkpoint import load_state_dict, FileSystemReader
  
  # Load with resharding
  state_dict = {"model": model.state_dict()}
  load_state_dict(
      state_dict=state_dict,
      storage_reader=FileSystemReader("checkpoint_dir"),
  )
  model.load_state_dict(state_dict["model"])
  
  # Or: Save full state dict for portability
  # FSDP: use_orig_params=True, state_dict_type=FULL_STATE_DICT
  