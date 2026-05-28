---
name: pytorch-deep-learning
description: Use this skill for deep learning development with PyTorch, including model training, GPU optimization, and advanced architectures like transformers and diffusion models.
---

# PyTorch Deep Learning Skill

This skill provides a comprehensive environment for deep learning development using PyTorch, including model training, GPU acceleration, and advanced architectures.

## Capabilities

- Neural network definition and training
- CUDA GPU acceleration and mixed precision training
- Data loading and preprocessing with efficient DataLoaders
- Model checkpointing and inference
- TensorBoard visualization
- Distributed training support
- Integration with NumPy, Pandas, scikit-learn, and Hugging Face Transformers
- Pretrained models (torchvision, torchtext, torchaudio)
- Implementation of custom `nn.Module` classes and autograd functions
- Support for diffusion models and attention mechanisms

## When to Use

- Deep learning model development
- Computer vision tasks
- Natural language processing
- Audio processing
- Transfer learning
- Research experiments
- Production model deployment
- Interactive demos for inference

## Environment Setup

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import torchvision.models as models
import torchvision.transforms as transforms

# Check GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")
```

## Model Definition

```python
class SimpleNN(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out

model = SimpleNN(784, 256, 10).to(device)
```

## Training Loop

```python
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(num_epochs):
    for batch_idx, (data, targets) in enumerate(train_loader):
        data, targets = data.to(device), targets.to(device)

        # Forward pass
        scores = model(data)
        loss = criterion(scores, targets)

        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if batch_idx % 100 == 0:
            print(f'Epoch [{epoch}/{num_epochs}] Loss: {loss.item():.4f}')
```

## Data Loading

```python
class CustomDataset(Dataset):
    def __init__(self, data, labels):
        self.data = data
        self.labels = labels

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]

# DataLoader
dataset = CustomDataset(train_data, train_labels)
train_loader = DataLoader(dataset, batch_size=64, shuffle=True, num_workers=4)
```

## Pretrained Models and Fine-tuning

```python
# Load pretrained ResNet
model = models.resnet50(pretrained=True)

# Fine-tune last layer
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, num_classes)
model = model.to(device)

# Freeze early layers
for param in model.parameters():
    param.requires_grad = False
for param in model.fc.parameters():
    param.requires_grad = True
```

## Model Saving/Loading

```python
# Save checkpoint
torch.save({
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss,
}, 'checkpoint.pth')

# Load checkpoint
checkpoint = torch.load('checkpoint.pth')
model.load_state_dict(checkpoint['model_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
```

## Performance Optimization

- Use DataParallel/DistributedDataParallel for multi-GPU training
- Implement gradient accumulation for large batches
- Profile code to identify bottlenecks
- Use `torch.cuda.amp` for mixed precision training

## Best Practices

1. Always move model and data to the same device.
2. Use DataLoader for efficient batching and data augmentation.
3. Enable cuDNN benchmarking for performance.
4. Clear CUDA cache periodically.
5. Implement early stopping and learning rate scheduling.

## Related Skills

- jupyter-notebooks - Interactive ML development
- cuda-development - Custom CUDA kernels
- data-visualization - Plot training metrics
- gradio - Create interactive demos for inference

## Notes

- Ensure CUDA and cuDNN are properly installed.
- Use gradient clipping for stability in training.
- Handle NaN/Inf values properly during training.