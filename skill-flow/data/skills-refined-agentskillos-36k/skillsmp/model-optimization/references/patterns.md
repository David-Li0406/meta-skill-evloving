# Model Optimization

## Patterns

### **Golden Rules**
  
---
    ##### **Rule**
Measure baseline first
    ##### **Reason**
Know what you're optimizing against
  
---
    ##### **Rule**
Quantization before pruning
    ##### **Reason**
Quantization is usually higher ROI
  
---
    ##### **Rule**
Validate on real data
    ##### **Reason**
Don't just check loss, check task metrics
  
---
    ##### **Rule**
Profile on target hardware
    ##### **Reason**
Desktop GPU ≠ mobile ≠ server
  
---
    ##### **Rule**
Combine techniques carefully
    ##### **Reason**
Order matters, some don't compose well
  
---
    ##### **Rule**
Keep the original model
    ##### **Reason**
You may need to retrain
### **Optimization Techniques**
  #### **Quantization**
    ##### **Description**
Reduce numerical precision
    ##### **Methods**
      - FP32 → FP16/BF16: 2x memory savings
      - INT8 Dynamic: Weights quantized, activations at runtime
      - INT8 Static: Both quantized, needs calibration
      - GPTQ/AWQ: 4-bit LLM quantization
    ##### **Tools**
      - torch.quantization
      - bitsandbytes
      - GPTQ
  #### **Pruning**
    ##### **Description**
Remove parameters
    ##### **Types**
      ###### **Unstructured**
Remove individual weights (needs sparse hardware)
      ###### **Structured**
Remove entire channels/filters (actual smaller model)
    ##### **Methods**
      - Magnitude pruning
      - Iterative pruning
      - Lottery ticket
  #### **Distillation**
    ##### **Description**
Train small model from large model outputs
    ##### **Components**
      - Hard labels: Standard cross-entropy
      - Soft labels: KL divergence with temperature
      - Feature distillation: Match intermediate representations
  #### **Export**
    ##### **Description**
Convert to optimized runtime
    ##### **Formats**
      - ONNX: Cross-framework compatibility
      - TensorRT: NVIDIA GPU optimization
      - OpenVINO: Intel optimization
### **Quantization Comparison**
  #### **Fp16 Bf16**
    ##### **Bits**

    ##### **Accuracy Loss**
~0%
    ##### **Speedup**
2x
    ##### **Use Case**
Training, inference
  #### **Int8 Dynamic**
    ##### **Bits**

    ##### **Accuracy Loss**
1-2%
    ##### **Speedup**
2x
    ##### **Use Case**
CPU inference
  #### **Int8 Static**
    ##### **Bits**

    ##### **Accuracy Loss**
1-3%
    ##### **Speedup**
2-4x
    ##### **Use Case**
Server inference
  #### **Gptq 4Bit**
    ##### **Bits**

    ##### **Accuracy Loss**
2-5%
    ##### **Speedup**
3-4x
    ##### **Use Case**
LLM inference

## Anti-Patterns


---
  #### **Pattern**
Quantizing untrained model
  #### **Problem**
Poor accuracy
  #### **Solution**
Train first, then quantize

---
  #### **Pattern**
Over-pruning without fine-tuning
  #### **Problem**
Accuracy collapse
  #### **Solution**
Iterative prune + fine-tune

---
  #### **Pattern**
Wrong quantization method
  #### **Problem**
Suboptimal results
  #### **Solution**
PTQ for inference, QAT for accuracy

---
  #### **Pattern**
Ignoring target hardware
  #### **Problem**
No speedup
  #### **Solution**
Profile on actual deployment target

---
  #### **Pattern**
Skipping calibration data
  #### **Problem**
Poor quantization
  #### **Solution**
Use representative dataset

---
  #### **Pattern**
Combining techniques blindly
  #### **Problem**
Degraded accuracy
  #### **Solution**
Test each step, validate task metrics