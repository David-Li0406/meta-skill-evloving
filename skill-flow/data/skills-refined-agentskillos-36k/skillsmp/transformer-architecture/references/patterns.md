# Transformer Architecture

## Patterns

### **Golden Rules**
  
---
    ##### **Rule**
Attention is O(n^2) in sequence length
    ##### **Reason**
Long contexts need efficient attention (FlashAttention, sparse)
  
---
    ##### **Rule**
Position info must be injected
    ##### **Reason**
Transformers have no inherent order awareness
  
---
    ##### **Rule**
Layer norm placement matters
    ##### **Reason**
Pre-norm (before attention) is more stable for training
  
---
    ##### **Rule**
Masking determines causality
    ##### **Reason**
Wrong masks cause data leakage in training
  
---
    ##### **Rule**
Mixed precision is free performance
    ##### **Reason**
bf16/fp16 on modern GPUs with negligible quality loss
### **Architecture Variants**
  #### **Encoder Only**
    ##### **Models**
      - BERT
      - RoBERTa
    ##### **Attention**
Bidirectional self-attention
    ##### **Use Cases**
      - Classification
      - NER/tagging
      - Embeddings
      - Retrieval
  #### **Decoder Only**
    ##### **Models**
      - GPT
      - LLaMA
    ##### **Attention**
Causal (left-to-right) self-attention
    ##### **Use Cases**
      - Text generation
      - Code completion
      - Chat/dialogue
      - Reasoning
  #### **Encoder Decoder**
    ##### **Models**
      - T5
      - BART
    ##### **Attention**
Cross-attention between enc/dec
    ##### **Use Cases**
      - Translation
      - Summarization
      - Seq2seq tasks
### **Positional Encoding**
  #### **Sinusoidal**
    ##### **Pros**
      - Deterministic
      - Generalizes to longer sequences
    ##### **Cons**
      - Moderate length extrapolation
    ##### **Best For**
Short sequences
  #### **Learned**
    ##### **Pros**
      - Simple
      - Stable training
    ##### **Cons**
      - Poor length generalization
    ##### **Best For**
Fixed-length tasks
  #### **Rope**
    ##### **Pros**
      - Excellent length extrapolation
      - Relative position encoded naturally
    ##### **Cons**
      - Slightly more compute
    ##### **Best For**
Long-context LLMs
  #### **Alibi**
    ##### **Pros**
      - Excellent extrapolation
      - Very low memory
    ##### **Cons**
      - May underperform on short contexts
    ##### **Best For**
Very long sequences
### **Efficient Attention**
  #### **Flash Attention**
    ##### **Memory**
O(n) instead of O(n^2)
    ##### **Speedup**
2-4x for long sequences
    ##### **Note**
Exact same results, not approximate
  #### **Grouped Query Attention**
    ##### **Description**
Fewer KV heads than query heads
    ##### **Models**
      - LLaMA 2
      - Mistral
    ##### **Benefit**
Memory efficiency during inference

## Anti-Patterns


---
  #### **Pattern**
Wrong mask type
  #### **Problem**
Data leakage in training
  #### **Solution**
Causal for decoders, bidirectional for encoders

---
  #### **Pattern**
No scaling in attention
  #### **Problem**
Gradients vanish/explode
  #### **Solution**
Always divide by sqrt(d_k)

---
  #### **Pattern**
Post-norm for deep nets
  #### **Problem**
Training instability
  #### **Solution**
Use pre-norm (LayerNorm before attention)

---
  #### **Pattern**
Ignoring mixed precision
  #### **Problem**
2x slower training
  #### **Solution**
Use bf16/fp16 on modern GPUs

---
  #### **Pattern**
O(n^2) attention for long seqs
  #### **Problem**
OOM errors
  #### **Solution**
FlashAttention, sparse attention

---
  #### **Pattern**
Fixed positional embeddings
  #### **Problem**
Poor length generalization
  #### **Solution**
RoPE or ALiBi for long contexts