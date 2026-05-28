# Wan2.1/2.2 Model Specifications

Wan I2V モデルの詳細仕様リファレンス。

## Model Variants Overview

### Wan2.1 Models

| モデル名 | パラメータ数 | 解像度 | VRAM (fp16) | VRAM (fp8) |
|----------|-------------|--------|-------------|------------|
| wan2.1_i2v_720p_14B | 14B | 720p | 40GB+ | 24GB |
| wan2.1_i2v_480p_14B | 14B | 480p | 32GB+ | 20GB |
| wan2.1_i2v_1.3B | 1.3B | 480p | 8GB | 6GB |

### Wan2.2 Models

| モデル名 | パラメータ数 | 解像度 | 機能 | VRAM (fp16) |
|----------|-------------|--------|------|-------------|
| wan2.2_i2v_14B | 14B | 720p | I2V | 40GB+ |
| wan2.2_t2v_14B | 14B | 720p | T2V | 40GB+ |
| wan2.2_ti2v_5B | 5B | 720p | I2V, TI2V | 12-16GB |

## Precision Formats

### 利用可能な精度

| 精度 | サイズ削減 | 品質影響 | 推奨用途 |
|------|-----------|----------|----------|
| bf16/fp16 | 0% | なし | ハイエンドGPU |
| fp8 | ~50% | 微小 | 中〜高VRAM |
| GGUF Q5_K_S | ~75% | 小 | 中VRAM |
| GGUF Q4_K_S | ~80% | 中小 | 低VRAM（推奨） |
| GGUF Q3_K_S | ~85% | 中 | 極低VRAM |
| GGUF Q2_K | ~90% | 大 | 最低VRAM |

## Download Sources

### HuggingFace Official

**Wan2.1:**
- `Wan-Video/Wan2.1-I2V-14B-720P`
- `Wan-Video/Wan2.1-I2V-14B-480P`

**Wan2.2:**
- `Wan-Video/Wan2.2`

### GGUF Quantized Models

- `QuantStack/Wan2.2-I2V-A14B-GGUF`
- `city96/Wan2.2-I2V-5B-GGUF`

## Model File Sizes

### Wan2.1

| ファイル | サイズ |
|----------|--------|
| wan2.1_i2v_720p_14B_fp16.safetensors | ~28GB |
| wan2.1_i2v_720p_14B_fp8_e4m3fn.safetensors | ~14GB |
| wan2.1_i2v_1.3B_fp16.safetensors | ~2.6GB |

### Wan2.2

| ファイル | サイズ |
|----------|--------|
| wan2.2_i2v_14B_fp16.safetensors | ~28GB |
| wan2.2_ti2v_5B_fp16.safetensors | ~10GB |
| Wan2.2-I2V-A14B-Q4_K_S.gguf | ~8.2GB |
| Wan2.2-I2V-A14B-Q3_K_S.gguf | ~6.3GB |

## Supporting Models

### Text Encoder

| モデル | サイズ | 用途 |
|--------|--------|------|
| umt5_xxl_fp16.safetensors | ~9GB | 最高品質 |
| umt5_xxl_fp8_e4m3fn_scaled.safetensors | ~4.5GB | 推奨（品質/サイズバランス） |

### VAE

| モデル | サイズ | 互換性 |
|--------|--------|--------|
| wan2.1_vae.safetensors | ~330MB | Wan2.1/2.2両対応 |
| wan2.2_vae.safetensors | ~330MB | Wan2.2専用 |

### CLIP Vision

| モデル | サイズ | 用途 |
|--------|--------|------|
| clip_vision_h.safetensors | ~3.9GB | I2V必須 |

## Hardware Requirements

### Minimum Requirements（GGUF Q4使用時）

- GPU: NVIDIA RTX 3060 12GB 以上
- RAM: 32GB以上推奨
- Storage: 50GB以上の空き容量

### Recommended Requirements（fp16使用時）

- GPU: NVIDIA RTX 4090 24GB または A100 40GB
- RAM: 64GB以上
- Storage: 100GB以上のSSD

## Performance Characteristics

### 生成時間（81フレーム @ 576×1024）

| GPU | Wan2.2 5B fp16 | Wan2.2 14B GGUF Q4 | Wan2.2 14B fp8 |
|-----|----------------|-------------------|----------------|
| RTX 4090 | 22-30秒 | 45-60秒 | 40-50秒 |
| RTX 4080 | 35-45秒 | 70-90秒 | 60-75秒 |
| RTX 4070 | 55-70秒 | 90-120秒 | 80-100秒 |
| RTX 3090 | 45-60秒 | 80-100秒 | 70-90秒 |
| RTX 3080 | 90-120秒 | 150-180秒 | 130-160秒 |

### VRAM使用量目安

| 設定 | Wan2.2 5B | Wan2.2 14B GGUF Q4 |
|------|-----------|-------------------|
| 480×840, 41f | 6GB | 8GB |
| 576×1024, 81f | 10GB | 12GB |
| 720×1280, 81f | 14GB | 16GB |

## Model Architecture

### Diffusion Backbone

- ベースアーキテクチャ: Diffusion Transformer (DiT)
- 時間的モデリング: 3D Attention + Temporal Convolution
- ノイズスケジューラ: Flow Matching

### Conditioning

- テキスト: UMT5-XXL Encoder
- 画像: CLIP Vision Encoder (ViT-H)
- 時間埋め込み: Sinusoidal + Learned

## License

- **ライセンス**: Apache 2.0
- **商用利用**: 可
- **改変**: 可
- **再配布**: 可（ライセンス明記必須）
