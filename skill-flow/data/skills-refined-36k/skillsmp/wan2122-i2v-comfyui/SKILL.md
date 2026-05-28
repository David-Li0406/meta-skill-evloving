---
name: Wan2.1/2.2 I2V ComfyUI
description: This skill should be used when the user asks to "implement Wan I2V", "set up Wan2.1", "configure Wan2.2", "image to video with Wan", "ComfyUI video generation", "low VRAM video generation", "GGUF Wan model", "setup video diffusion model", "Wan I2Vを実装", "Wan2.1をセットアップ", "Wan2.2を設定", "画像から動画生成", "ComfyUIで動画生成", "低VRAMで動画生成", "GGUFモデルを使用", "動画生成モデルのセットアップ", or needs guidance on Wan2.1/2.2 image-to-video model setup, ComfyUI workflow configuration, GGUF quantization for low VRAM, video generation parameters, or troubleshooting Wan model issues.
version: 0.1.0
---

# Wan2.1/2.2 I2V ComfyUI Implementation

Alibabaがオープンソース化したWan2.1/2.2 I2V（Image-to-Video）モデルをComfyUIで使用するための包括的ガイド。画像から動画を生成する機能の実装をサポートする。

## Quick Start Checklist

Wan I2Vを実装する際の必須手順：

1. **ComfyUI セットアップ確認**
   - ComfyUI最新版をインストール
   - `git pull` で更新を確認

2. **カスタムノードのインストール（低VRAM向け）**
   ```bash
   cd ComfyUI/custom_nodes
   git clone https://github.com/city96/ComfyUI-GGUF
   ```

3. **モデルファイルの配置**
   - Diffusion Model → `models/diffusion_models/`
   - Text Encoder → `models/text_encoders/`
   - VAE → `models/vae/`
   - CLIP Vision → `models/clip_vision/`

4. **ワークフローの読み込み**
   - Menu → Workflow → Browse Templates → Video → Wan2.2

## Model Overview

### Wan2.1 vs Wan2.2 比較

| 特性 | Wan2.1 | Wan2.2 |
|------|--------|--------|
| リリース | 2025年2月 | 2025年7月 |
| モデルサイズ | 14B, 1.3B | 14B, 5B |
| I2V対応 | ✓ | ✓ |
| TI2V対応 | - | ✓（5B） |
| 推奨VRAM | 40GB+ (14B fp16) | 8GB+ (5Bオフロード) |
| ライセンス | Apache 2.0 | Apache 2.0 |

### モデル選択ガイド

**高品質重視（ハイエンドGPU）:**
- Wan2.2 14B fp16 - 最高品質
- VRAM: 40GB以上推奨

**バランス重視（ミドルレンジGPU）:**
- Wan2.2 5B - 品質とVRAMのバランス
- VRAM: 12-16GB

**低VRAM環境（コンシューマーGPU）:**
- Wan2.2 GGUF Q4_K_S - 量子化版
- VRAM: 8-10GB

## Directory Structure

モデルファイルの配置構造：

```
ComfyUI/
├── models/
│   ├── diffusion_models/
│   │   ├── wan2.1_i2v_720p_14B_fp8_e4m3fn.safetensors
│   │   ├── wan2.2_i2v_14B_fp16.safetensors
│   │   ├── wan2.2_ti2v_5B_fp16.safetensors
│   │   └── Wan2.2-I2V-A14B-Q4_K_S.gguf  # 低VRAM用
│   ├── text_encoders/
│   │   └── umt5_xxl_fp8_e4m3fn_scaled.safetensors
│   ├── vae/
│   │   ├── wan2.1_vae.safetensors
│   │   └── wan2.2_vae.safetensors
│   └── clip_vision/
│       └── clip_vision_h.safetensors
└── custom_nodes/
    └── ComfyUI-GGUF/  # 低VRAM用カスタムノード
```

## Core Workflow Components

### 基本的なI2Vワークフロー構成

```
[Load Image] → [CLIP Vision Encode] ─┐
                                      │
[Load Text Encoder] → [Text Encode] ──┤
                                      ├→ [WanVideo Sampler] → [VAE Decode] → [Save Video]
[Load Diffusion Model] ───────────────┤
                                      │
[Load VAE] ───────────────────────────┘
```

### 必須ノード一覧

| ノード | 用途 | 設定 |
|--------|------|------|
| Load Diffusion Model | Wanモデル読み込み | `wan2.2_i2v_*.safetensors` |
| Load CLIP | テキストエンコーダ読み込み | `umt5_xxl_*.safetensors` |
| Load VAE | VAE読み込み | `wan2.1_vae.safetensors` |
| Load CLIP Vision | 画像エンコーダ読み込み | `clip_vision_h.safetensors` |
| WanVideo Sampler | 動画生成サンプラー | CFG, Steps等を設定 |

## Key Parameters

### 解像度設定

| 設定 | 解像度 | 用途 |
|------|--------|------|
| 標準（縦長） | 576×1024 | ポートレート動画 |
| 標準（横長） | 1024×576 | ランドスケープ動画 |
| 低VRAM | 840×480 | メモリ節約 |
| 高品質 | 720p (1280×720) | 14Bモデル向け |

### 生成パラメータ

| パラメータ | 推奨値 | 説明 |
|-----------|--------|------|
| **フレーム数** | 81 | 約3-4秒 @24fps |
| **CFG** | 4-7 | 低め=自然な動き、高め=プロンプト忠実 |
| **Steps** | 20-30 | 高め=細部改善、過度は不安定に |
| **Seed** | 任意 | 再現性のため固定推奨 |

### CFG (Classifier-Free Guidance) ガイド

```
CFG 3.5-4.5: 最大限の動きと変化、クリエイティブな出力
CFG 5.0-6.0: バランスの取れた動きとプロンプト忠実度
CFG 6.5-7.0: プロンプトに強く従う、動きは控えめ
```

## GGUF Quantization（低VRAM向け）

VRAM 8-12GB環境でWanモデルを実行するための量子化オプション：

| 量子化レベル | モデルサイズ | VRAM目安 | 品質 |
|-------------|-------------|----------|------|
| Q2_K | ~1.85GB | 6GB | 低 |
| Q3_K_S | ~2.29GB | 8GB | 中低 |
| Q4_K_S | ~3.12GB | 10GB | 中（推奨） |
| Q5_K_S | ~3.56GB | 12GB | 高 |

### GGUFセットアップ

1. ComfyUI-GGUFをインストール
2. 量子化モデルをダウンロード（HuggingFaceから）
3. `models/diffusion_models/` に配置
4. `Load GGUF Model` ノードを使用

## Performance Benchmarks

### 生成時間目安（81フレーム、576×1024）

| GPU | Wan2.2 5B | Wan2.2 14B GGUF Q4 |
|-----|-----------|-------------------|
| RTX 4090 | ~22-30秒 | ~45-60秒 |
| RTX 4070 | ~55-70秒 | ~90-120秒 |
| RTX 3080 | ~90-120秒 | ~150-180秒 |

## Common Issues & Solutions

| 問題 | 原因 | 解決策 |
|------|------|--------|
| OOM（メモリ不足） | VRAM不足 | 解像度↓、GGUF使用、フレーム数↓ |
| 時間的不整合 | CFG/Steps過大 | CFG 4-5、Steps 20-25に調整 |
| モデルロード失敗 | パス/名前不一致 | ディレクトリ構造を確認 |
| 生成が遅い | 高解像度/fp16 | GGUF量子化、解像度削減 |
| 動きが少ない | CFG高すぎ | CFG 3.5-4.5に下げる |
| 品質が低い | 量子化レベル | Q4_K_S以上を使用 |

詳細なトラブルシューティングは `references/troubleshooting.md` を参照。

## Quick Reference

| Component | Purpose | Key API/File |
|-----------|---------|--------------|
| Diffusion Model | 動画生成の核 | `wan2.2_i2v_*.safetensors` |
| Text Encoder | プロンプト処理 | `umt5_xxl_*.safetensors` |
| CLIP Vision | 画像理解 | `clip_vision_h.safetensors` |
| VAE | エンコード/デコード | `wan2.1_vae.safetensors` |
| ComfyUI-GGUF | 低VRAM対応 | カスタムノード |

## Additional Resources

### Reference Files

詳細な情報は以下を参照：

- **`references/model-specifications.md`** - モデル仕様の詳細（Wan2.1/2.2、パラメータ数、VRAM要件）
- **`references/comfyui-setup.md`** - ComfyUIセットアップ完全ガイド
- **`references/workflow-components.md`** - ワークフローコンポーネントの詳細
- **`references/parameters-guide.md`** - パラメータ設定の詳細ガイド
- **`references/gguf-quantization.md`** - GGUF量子化の詳細と設定
- **`references/troubleshooting.md`** - エラー一覧とデバッグ手法

### Example Files

実装サンプルは `examples/` ディレクトリを参照：

- **`examples/wan21-basic-i2v.json`** - Wan2.1基本I2Vワークフロー
- **`examples/wan22-i2v-workflow.json`** - Wan2.2 I2Vワークフロー
- **`examples/wan22-ti2v-workflow.json`** - Wan2.2 TI2V（Text+Image to Video）
- **`examples/low-vram-gguf.json`** - 低VRAM向けGGUFワークフロー
- **`examples/high-quality-14b.json`** - 高品質14B設定ワークフロー
