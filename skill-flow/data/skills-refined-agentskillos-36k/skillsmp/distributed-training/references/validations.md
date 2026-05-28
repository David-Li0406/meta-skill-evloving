# Distributed Training - Validations

## DataLoader Without DistributedSampler

### **Id**
no-distributed-sampler
### **Severity**
error
### **Type**
regex
### **Pattern**
  - DataLoader\((?!.*DistributedSampler|.*sampler)
  - DataLoader\(.*shuffle\s*=\s*True(?!.*DistributedSampler)
### **Message**
Distributed training requires DistributedSampler for proper data splitting.
### **Fix Action**
Add: sampler=DistributedSampler(dataset)
### **Applies To**
  - **/*train*.py

## DistributedSampler Without set_epoch()

### **Id**
missing-set-epoch
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - DistributedSampler(?!.*set_epoch)
### **Message**
Call set_epoch() each epoch for proper shuffling.
### **Fix Action**
Add: train_sampler.set_epoch(epoch)
### **Applies To**
  - **/*train*.py

## Large Model Without Gradient Checkpointing

### **Id**
no-gradient-checkpointing
### **Severity**
info
### **Type**
regex
### **Pattern**
  - FSDP\((?!.*gradient_checkpointing)
  - AutoModelForCausalLM(?!.*gradient_checkpointing_enable)
### **Message**
Large models benefit from gradient checkpointing for memory efficiency.
### **Fix Action**
Add: model.gradient_checkpointing_enable()
### **Applies To**
  - **/*.py

## Distributed Training Without Mixed Precision

### **Id**
no-mixed-precision
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - DDP\((?!.*MixedPrecision|.*autocast)
  - FSDP\((?!.*mixed_precision)
### **Message**
Mixed precision (bf16/fp16) provides 2x memory savings.
### **Fix Action**
Add: mixed_precision=MixedPrecision(param_dtype=torch.bfloat16)
### **Applies To**
  - **/*train*.py

## DataLoader Without pin_memory

### **Id**
no-pin-memory
### **Severity**
info
### **Type**
regex
### **Pattern**
  - DataLoader\((?!.*pin_memory\s*=\s*True)
### **Message**
pin_memory=True speeds up CPU to GPU data transfer.
### **Fix Action**
Add: pin_memory=True
### **Applies To**
  - **/*train*.py

## Using Gloo Backend for GPU Training

### **Id**
gloo-backend-gpu
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - init_process_group.*backend\s*=\s*['"]gloo['"].*cuda
### **Message**
Use NCCL backend for GPU training (faster collectives).
### **Fix Action**
Change: backend='nccl'
### **Applies To**
  - **/*.py

## Using DataParallel Instead of DDP

### **Id**
dataparallel-not-ddp
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - nn\.DataParallel\(
  - torch\.nn\.DataParallel
### **Message**
DDP is faster and more scalable than DataParallel.
### **Fix Action**
Use: DistributedDataParallel instead
### **Applies To**
  - **/*.py