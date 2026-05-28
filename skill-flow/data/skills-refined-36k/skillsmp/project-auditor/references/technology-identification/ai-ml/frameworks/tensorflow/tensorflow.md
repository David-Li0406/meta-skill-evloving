# TensorFlow

**Category**: ai-ml/frameworks
**Description**: Open source machine learning framework developed by Google
**Homepage**: https://www.tensorflow.org

## Package Detection

### PYPI
*TensorFlow Python packages*

- `tensorflow`
- `tensorflow-gpu`
- `tf-nightly`
- `tensorflow-hub`
- `tensorflow-datasets`
- `tensorflow-probability`
- `tensorflow-addons`
- `tensorflow-io`
- `tensorflow-text`

### NPM
*TensorFlow.js packages*

- `@tensorflow/tfjs`
- `@tensorflow/tfjs-node`
- `@tensorflow/tfjs-node-gpu`
- `@tensorflow/tfjs-core`
- `@tensorflow/tfjs-layers`

### Related Packages
- `keras`
- `tensorboard`
- `tf-keras`

## Import Detection

### Python
File extensions: .py

**Pattern**: `import tensorflow`
- TensorFlow import
- Example: `import tensorflow as tf`

**Pattern**: `from tensorflow import`
- TensorFlow from import
- Example: `from tensorflow import keras`

**Pattern**: `tf\.keras`
- Keras via TensorFlow
- Example: `model = tf.keras.Sequential()`

### Javascript
File extensions: .js, .ts

**Pattern**: `from ['"]@tensorflow/tfjs`
- TensorFlow.js import
- Example: `import * as tf from '@tensorflow/tfjs';`

**Pattern**: `require\(['"]@tensorflow/tfjs`
- TensorFlow.js CommonJS
- Example: `const tf = require('@tensorflow/tfjs');`

### Common Imports
- `tensorflow`
- `@tensorflow/tfjs`

## Environment Variables

*TensorFlow configuration*

- `TF_CPP_MIN_LOG_LEVEL`
- `CUDA_VISIBLE_DEVICES`
- `TF_FORCE_GPU_ALLOW_GROWTH`
- `TF_GPU_ALLOCATOR`

## Detection Notes

- TensorFlow 2.x includes Keras as tf.keras
- Can run on CPU or GPU
- TensorFlow.js for browser/Node.js
- Often paired with NumPy and Pandas

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 70% (MEDIUM)
