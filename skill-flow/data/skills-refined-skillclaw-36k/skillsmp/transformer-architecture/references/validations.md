# Transformer Architecture - Validations

## Attention Without Scaling Factor

### **Id**
missing-attention-scaling
### **Severity**
error
### **Type**
regex
### **Pattern**
  - softmax.*matmul.*query.*key(?!.*/.*sqrt)
  - torch\.matmul\(.*query.*key(?!.*math\.sqrt|/.*d_k)
### **Message**
Attention scores must be scaled by sqrt(d_k) to prevent gradient issues.
### **Fix Action**
Add: scores = scores / math.sqrt(d_k)
### **Applies To**
  - **/*.py

## Potentially Wrong Causal Mask

### **Id**
hardcoded-mask-direction
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - torch\.triu\(.*ones(?!.*transpose)
  - np\.triu\(.*ones
### **Message**
Upper triangular mask may be wrong for causal attention. Verify mask direction.
### **Fix Action**
Use torch.tril for causal (decoder) masks, torch.triu for encoder padding masks.
### **Applies To**
  - **/*.py

## Attention Block Without Residual

### **Id**
missing-residual-connection
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - self\.attention\(.*\)\s*$(?!.*\+.*x|.*residual)
### **Message**
Transformer blocks require residual connections for gradient flow.
### **Fix Action**
Add: output = residual + self.attention(x)
### **Applies To**
  - **/*.py

## Training Without Mixed Precision

### **Id**
no-mixed-precision
### **Severity**
info
### **Type**
regex
### **Pattern**
  - model\.train\(\)(?!.*autocast|.*amp|.*bf16|.*fp16)
### **Message**
Consider using mixed precision (bf16/fp16) for 2x memory savings and faster training.
### **Fix Action**
Add: with torch.autocast(device_type='cuda', dtype=torch.bfloat16)
### **Applies To**
  - **/*train*.py

## Fixed Position Embedding Limit

### **Id**
fixed-position-limit
### **Severity**
info
### **Type**
regex
### **Pattern**
  - nn\.Embedding\(\s*\d{3,4}\s*,.*position
  - max_position_embeddings\s*=\s*\d{3,4}
### **Message**
Fixed position embeddings may limit sequence length. Consider RoPE for longer contexts.
### **Fix Action**
Use RoPE or ALiBi for better length extrapolation.
### **Applies To**
  - **/*.py

## Large Model Without Gradient Checkpointing

### **Id**
no-gradient-checkpointing
### **Severity**
info
### **Type**
regex
### **Pattern**
  - num_layers\s*=\s*(?:[2-9]\d|\d{3,})(?!.*checkpoint)
  - n_layer\s*=\s*(?:[2-9]\d|\d{3,})
### **Message**
Large models benefit from gradient checkpointing for memory efficiency.
### **Fix Action**
Add: model.gradient_checkpointing_enable()
### **Applies To**
  - **/*.py

## FlashAttention Not Enabled

### **Id**
flash-attention-not-enabled
### **Severity**
info
### **Type**
regex
### **Pattern**
  - scaled_dot_product_attention(?!.*enable_flash)
### **Message**
Enable FlashAttention for better memory efficiency and speed.
### **Fix Action**
Use: with torch.backends.cuda.sdp_kernel(enable_flash=True)
### **Applies To**
  - **/*.py