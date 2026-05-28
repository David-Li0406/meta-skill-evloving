#!/bin/bash

# Debug script for ocean prediction with memory optimization
# 海洋预测调试脚本 - 内存优化版本

echo "======================================"
echo "Debug Training for Ocean Prediction"
echo "======================================"

# 设置环境变量优化内存使用
export CUDA_LAUNCH_BLOCKING=1
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:128
export OMP_NUM_THREADS=1

# 检查GPU状态
echo "GPU状态:"
nvidia-smi --query-gpu=index,name,memory.total,memory.used,memory.free --format=csv,noheader,nounits

# 清理GPU缓存
python -c "import torch; torch.cuda.empty_cache()"

# 运行调试训练
echo "开始调试训练..."
python main.py \
    --config configs/surface_config_debug.yaml \
    --mode train

echo "======================================"
echo "Debug training completed!"
echo "======================================"
