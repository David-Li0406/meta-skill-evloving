#!/bin/bash

# Ocean Velocity Prediction Test Script
# Usage: bash scripts/test.sh --model_path logs/ocean/01_15/OceanCNN_12_34_56

# Default configuration
MODEL_PATH=""
NUM_VISUALIZE=10

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --model_path)
            MODEL_PATH="$2"
            shift 2
            ;;
        --num_visualize)
            NUM_VISUALIZE="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Check if model path is provided
if [ -z "$MODEL_PATH" ]; then
    echo "Error: --model_path is required"
    echo "Usage: bash scripts/test.sh --model_path logs/ocean/01_15/OceanCNN_12_34_56"
    exit 1
fi

echo "======================================"
echo "Ocean Velocity Prediction Testing"
echo "======================================"
echo "Model Path: $MODEL_PATH"
echo "Number of Visualizations: $NUM_VISUALIZE"
echo "======================================"

# Run testing
python test_ocean.py \
    --model_path $MODEL_PATH \
    --num_visualize $NUM_VISUALIZE

echo "======================================"
echo "Testing completed!"
echo "Results saved to: ${MODEL_PATH}/test_results"
echo "======================================"
