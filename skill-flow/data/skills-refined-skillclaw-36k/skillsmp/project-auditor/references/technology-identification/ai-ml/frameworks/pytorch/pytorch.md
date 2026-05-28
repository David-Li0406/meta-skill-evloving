# PyTorch

**Category**: ai-ml/frameworks
**Description**: Open source machine learning framework developed by Meta/Facebook
**Homepage**: https://pytorch.org

## Package Detection

### PYPI
*PyTorch Python packages*

- `torch`
- `torchvision`
- `torchaudio`
- `pytorch`
- `pytorch-lightning`
- `torch-geometric`
- `torchtext`
- `torchmetrics`

### NPM
*PyTorch JavaScript bindings*

- `@aspect-analytics/torch-js`

### Related Packages
- `numpy`
- `lightning`
- `transformers`
- `accelerate`

## Import Detection

### Python
File extensions: .py

**Pattern**: `import torch`
- PyTorch import
- Example: `import torch`

**Pattern**: `from torch import`
- PyTorch from import
- Example: `from torch import nn`

**Pattern**: `torch\.nn`
- PyTorch neural networks
- Example: `model = torch.nn.Sequential()`

**Pattern**: `import torchvision`
- TorchVision import
- Example: `import torchvision.transforms as transforms`

### Common Imports
- `torch`
- `torchvision`
- `torchaudio`

## Environment Variables

*PyTorch configuration*

- `TORCH_HOME`
- `CUDA_VISIBLE_DEVICES`
- `PYTORCH_CUDA_ALLOC_CONF`
- `TORCH_DISTRIBUTED_DEBUG`

## Detection Notes

- Primary deep learning framework alongside TensorFlow
- Strong in research and computer vision
- Dynamic computational graphs
- Often paired with HuggingFace Transformers

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 70% (MEDIUM)
