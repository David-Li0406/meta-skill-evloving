---
name: ml-optimization
description: Optimizes TensorFlow.js WebGPU backend, WebLLM offline inference, and implements memory safety for heavy ML models
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: development
---

## What I do

I optimize the ML pipeline for performance and memory efficiency. I manage TF.js WebGPU backend configuration, WebLLM offline inference, and ensure proper memory cleanup to prevent leaks.

## When to use me

Use this when:

- You're working with TF.js or WebLLM models
- You notice memory leaks or performance regressions
- You're updating model weights or configurations

## Key Concepts

- **TF.js WebGPU**: GPU acceleration for browser ML
- **WebLLM**: Browser-based LLM for offline inference
- **SmolLM2**: Efficient LLM model variant
- **Memory Safety**: Proper tensor cleanup
- **Manual Chunks**: Code splitting for model loading

## Source Files

- `services/vision.ts`: ML model integration
- `vite.config.ts`: Build configuration for chunks
- `plans/02_edge_ml_implementation.md`: ML optimization plan

## Code Patterns

- Use tf.tidy() for automatic tensor cleanup
- Lazy load heavy models on user interaction
- Expose unload() method for component unmount
- Manual chunks in Vite for model code splitting

## Operational Constraints

- All TF.js operations MUST use tf.tidy() or dispose()
- Heavy models must expose unload() method
- Clean up on component unmount
- Monitor memory usage in production
