# Transformer Architecture - Sharp Edges

## Attention Without sqrt(d_k) Scaling

### **Id**
attention-without-scaling
### **Severity**
critical
### **Summary**
Dot products grow large, pushing softmax into saturated regions
### **Symptoms**
  - Vanishing gradients during training
  - Attention weights become very peaky (near one-hot)
  - Training diverges or stalls
### **Why**
  For large d_k, the dot products q·k can grow large in magnitude.
  When passed through softmax, large values push gradients to near-zero.
  The scaling factor 1/sqrt(d_k) keeps the variance of dot products ≈ 1.
  
### **Gotcha**
  scores = torch.matmul(query, key.transpose(-2, -1))
  # Missing: / math.sqrt(d_k)
  attention_weights = F.softmax(scores, dim=-1)
  
### **Solution**
  d_k = query.size(-1)
  scores = torch.matmul(query, key.transpose(-2, -1)) / math.sqrt(d_k)
  attention_weights = F.softmax(scores, dim=-1)
  

## Causal Mask Leaks Future Tokens

### **Id**
wrong-causal-mask
### **Severity**
critical
### **Summary**
Decoder sees future tokens during training, fails at inference
### **Symptoms**
  - Perfect training loss but poor generation
  - Model generates repetitive or nonsensical text
  - Validation loss much higher than training
### **Why**
  Decoder-only models must not see future tokens during training.
  If the mask allows future token access, the model learns to cheat.
  At inference, future tokens don't exist, so the model fails.
  
### **Gotcha**
  # Wrong: No mask or wrong mask direction
  output = self_attention(x)  # Sees all tokens
  
  # Wrong mask direction
  mask = torch.triu(torch.ones(seq_len, seq_len))  # Upper triangular - wrong!
  
### **Solution**
  # Correct: Lower triangular mask (each position sees only previous)
  mask = torch.tril(torch.ones(seq_len, seq_len))  # Lower triangular
  
  # Apply mask
  scores = scores.masked_fill(mask == 0, float('-inf'))
  attention_weights = F.softmax(scores, dim=-1)
  

## Post-LayerNorm Causes Training Instability

### **Id**
post-norm-deep-networks
### **Severity**
high
### **Summary**
Original transformer used post-norm, but pre-norm is more stable
### **Symptoms**
  - Training becomes unstable with more layers
  - Requires very careful learning rate tuning
  - Gradient explosion in deep networks
### **Why**
  Post-norm: x + LayerNorm(Attention(x))
  Pre-norm: x + Attention(LayerNorm(x))
  
  Pre-norm keeps residual path clean, gradients flow more easily.
  Modern LLMs (GPT-3, LLaMA) all use pre-norm.
  
### **Gotcha**
  # Post-norm (original transformer, less stable)
  x = self.attention(x)
  x = self.norm1(x + residual)
  
### **Solution**
  # Pre-norm (modern, more stable)
  residual = x
  x = self.norm1(x)
  x = self.attention(x)
  x = residual + x
  

## KV Cache Memory Explosion with Long Contexts

### **Id**
kv-cache-memory-explosion
### **Severity**
high
### **Summary**
KV cache grows linearly with sequence length
### **Symptoms**
  - OOM during generation with long prompts
  - Memory usage grows unexpectedly
  - Batch size must decrease for longer sequences
### **Why**
  KV cache stores key/value tensors for all previous tokens.
  For a 7B model with 32 layers, 32 heads, 128 head_dim:
  KV cache per token = 2 * 32 * 32 * 128 * 2 bytes = 512KB
  4K context = 2GB just for KV cache
  
### **Gotcha**
  # Naive generation without KV cache management
  for i in range(max_new_tokens):
      output = model(full_sequence)  # Recomputes everything!
  
### **Solution**
  # Use KV cache with proper memory management
  past_key_values = None
  for i in range(max_new_tokens):
      output = model(new_token_only, past_key_values=past_key_values)
      past_key_values = output.past_key_values
  
  # For very long sequences: sliding window attention
  # Or: quantize KV cache to int8
  

## Model Fails on Sequences Longer Than Training

### **Id**
position-encoding-length-limit
### **Severity**
medium
### **Summary**
Learned/sinusoidal positions don't extrapolate well
### **Symptoms**
  - Quality degrades on longer sequences
  - Model produces garbage after position limit
  - Perplexity spikes at certain positions
### **Why**
  Learned positions: Only trained up to max_position_embeddings.
  Sinusoidal: Frequencies may not extrapolate well.
  
  RoPE and ALiBi are designed for length extrapolation.
  
### **Gotcha**
  # Learned positions with fixed limit
  self.position_embeddings = nn.Embedding(512, d_model)  # Max 512 tokens
  
  # At inference with 1000 tokens: Index out of bounds!
  
### **Solution**
  # Use RoPE or ALiBi for length extrapolation
  class RotaryPositionalEmbedding(nn.Module):
      def __init__(self, dim, max_seq_len=4096, base=10000):
          # RoPE naturally extrapolates beyond training length
          ...
  
  # Or dynamically extend positions
  # LLaMA uses RoPE with NTK-aware scaling for longer contexts
  