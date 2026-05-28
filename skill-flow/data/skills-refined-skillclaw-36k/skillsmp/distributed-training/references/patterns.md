# Distributed Training

## Patterns

### **Golden Rules**
  
---
    ##### **Rule**
Profile before parallelizing
    ##### **Reason**
Know if you're memory or compute bound
  
---
    ##### **Rule**
Start with DDP, scale to FSDP/DeepSpeed
    ##### **Reason**
DDP is simpler and faster for small models
  
---
    ##### **Rule**
Gradient checkpointing trades compute for memory
    ##### **Reason**
30% slower but 60%+ memory savings
  
---
    ##### **Rule**
Mixed precision is almost free
    ##### **Reason**
bf16/fp16 = 2x memory savings, minimal accuracy loss
  
---
    ##### **Rule**
Communication is the bottleneck
    ##### **Reason**
Minimize gradient sync frequency
  
---
    ##### **Rule**
Use NCCL for multi-GPU
    ##### **Reason**
Purpose-built for GPU collective ops
### **Parallelism Types**
  #### **Data Parallelism**
    ##### **Description**
Same model on each GPU, different data batches
    ##### **Memory**
Full model per GPU
    ##### **Communication**
Sync gradients
    ##### **Implementations**
      - DDP
      - DataParallel
  #### **Model Parallelism**
    ##### **Description**
Model split across GPUs
    ##### **Types**
      ###### **Tensor**
Split individual layers
      ###### **Pipeline**
Split layers into stages
    ##### **Best For**
Models too large for single GPU
  #### **Zero Redundancy**
    ##### **Description**
Shard optimizer, gradients, parameters
    ##### **Stages**
      ###### **Zero1**
Shard optimizer state (4x memory savings)
      ###### **Zero2**
Shard gradients (8x memory savings)
      ###### **Zero3**
Shard parameters (linear scaling)
    ##### **Implementations**
      - FSDP
      - DeepSpeed ZeRO
### **Memory Requirements**
  #### **7B Model**
    ##### **Fp32**
28GB
    ##### **Fp16**
14GB
    ##### **With Optimizer**
84GB (Adam)
    ##### **Fsdp Full Shard**
14GB per GPU (8 GPUs)
  #### **70B Model**
    ##### **Fp32**
280GB
    ##### **Fp16**
140GB
    ##### **Qlora**
~48GB
### **Fsdp Vs Deepspeed**
  #### **Fsdp**
    ##### **Pros**
      - Native PyTorch
      - torch.compile support
      - Lower learning curve
    ##### **Cons**
      - No NVMe offload
      - All-or-nothing CPU offload
  #### **Deepspeed**
    ##### **Pros**
      - NVMe offload
      - More config options
      - Trillion-scale tested
    ##### **Cons**
      - External dependency
      - More complex setup

## Anti-Patterns


---
  #### **Pattern**
DDP for large models
  #### **Problem**
OOM
  #### **Solution**
Use FSDP or DeepSpeed ZeRO

---
  #### **Pattern**
No gradient checkpointing
  #### **Problem**
OOM on long sequences
  #### **Solution**
Enable for transformer layers

---
  #### **Pattern**
fp32 training
  #### **Problem**
2x memory waste
  #### **Solution**
Use bf16/fp16 mixed precision

---
  #### **Pattern**
Small batch with many GPUs
  #### **Problem**
Communication overhead
  #### **Solution**
Gradient accumulation

---
  #### **Pattern**
Sync on every step
  #### **Problem**
Slow training
  #### **Solution**
Reduce sync frequency

---
  #### **Pattern**
Not pinning memory
  #### **Problem**
Slow data loading
  #### **Solution**
pin_memory=True in DataLoader