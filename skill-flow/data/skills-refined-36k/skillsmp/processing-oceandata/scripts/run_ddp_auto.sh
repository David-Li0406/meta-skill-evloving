#!/bin/bash

# Auto DDP Training Script for Ocean Prediction
# 自动检测GPU数量并启动DDP训练
# Usage: bash scripts/run_ddp_auto.sh --config configs/mid_config.yaml

# Default configuration
CONFIG_FILE="configs/mid_config.yaml"
MASTER_ADDR="localhost"
MASTER_PORT="12355"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --config)
            CONFIG_FILE="$2"
            shift 2
            ;;
        --master_addr)
            MASTER_ADDR="$2"
            shift 2
            ;;
        --master_port)
            MASTER_PORT="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# 自动检测可用GPU数量
NUM_GPUS=$(nvidia-smi --list-gpus | wc -l)
echo "检测到 $NUM_GPUS 个GPU"

# 验证配置文件中的device_ids
if [ -f "$CONFIG_FILE" ]; then
    echo "检查配置文件: $CONFIG_FILE"
    # 这里可以添加配置验证逻辑
else
    echo "错误: 配置文件 $CONFIG_FILE 不存在"
    exit 1
fi

echo "======================================"
echo "DDP Training for Ocean Prediction"
echo "======================================"
echo "Config: $CONFIG_FILE"
echo "Number of GPUs: $NUM_GPUS"
echo "Master Address: $MASTER_ADDR"
echo "Master Port: $MASTER_PORT"
echo "======================================"

# 检查torchrun是否可用
if ! command -v torchrun &> /dev/null; then
    echo "错误: torchrun 命令不可用，请确保PyTorch已正确安装"
    exit 1
fi

# Run DDP training using torchrun
echo "启动DDP训练..."
torchrun \
    --nproc_per_node=$NUM_GPUS \
    --master_addr=$MASTER_ADDR \
    --master_port=$MASTER_PORT \
    main.py \
    --config $CONFIG_FILE \
    --mode train

echo "======================================"
echo "DDP Training completed!"
echo "======================================"
