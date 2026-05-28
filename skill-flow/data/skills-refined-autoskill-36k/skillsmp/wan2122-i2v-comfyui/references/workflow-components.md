# Workflow Components Reference

Wan I2V ワークフローを構成するノードとコンポーネントの詳細リファレンス。

## Basic I2V Workflow Structure

```
┌─────────────────┐
│   Load Image    │──────────────────────────────┐
└─────────────────┘                              │
                                                 ▼
┌─────────────────┐    ┌─────────────────┐    ┌──────────────────┐
│ Load CLIP Vision│───▶│CLIP Vision Encode│───▶│                  │
└─────────────────┘    └─────────────────┘    │                  │
                                               │                  │
┌─────────────────┐    ┌─────────────────┐    │  WanVideo I2V    │
│   Load CLIP     │───▶│  CLIP Encode    │───▶│    Sampler       │
└─────────────────┘    └─────────────────┘    │                  │
                                               │                  │
┌─────────────────┐                            │                  │
│ Load Diffusion  │───────────────────────────▶│                  │
│     Model       │                            │                  │
└─────────────────┘                            └────────┬─────────┘
                                                        │
┌─────────────────┐                                     ▼
│    Load VAE     │───────────────────────────▶┌──────────────────┐
└─────────────────┘                            │   VAE Decode     │
                                               └────────┬─────────┘
                                                        │
                                                        ▼
                                               ┌──────────────────┐
                                               │   Save Video     │
                                               └──────────────────┘
```

## Core Nodes

### Load Diffusion Model

Wan拡散モデルを読み込むノード。

**入力:**
- `model_name`: 使用するモデルファイル名

**出力:**
- `MODEL`: 拡散モデルオブジェクト

**設定例:**
```
model_name: wan2.2_ti2v_5B_fp16.safetensors
```

### Load GGUF Model（低VRAM用）

GGUF量子化モデルを読み込むノード（ComfyUI-GGUF必須）。

**入力:**
- `gguf_name`: GGUFファイル名

**出力:**
- `MODEL`: 量子化モデルオブジェクト

**設定例:**
```
gguf_name: Wan2.2-I2V-A14B-Q4_K_S.gguf
```

### Load CLIP

テキストエンコーダを読み込むノード。

**入力:**
- `clip_name`: CLIPモデルファイル名
- `type`: エンコーダタイプ（`wan`を指定）

**出力:**
- `CLIP`: テキストエンコーダオブジェクト

**設定例:**
```
clip_name: umt5_xxl_fp8_e4m3fn_scaled.safetensors
type: wan
```

### Load CLIP Vision

画像エンコーダを読み込むノード。

**入力:**
- `clip_name`: CLIP Visionファイル名

**出力:**
- `CLIP_VISION`: 画像エンコーダオブジェクト

**設定例:**
```
clip_name: clip_vision_h.safetensors
```

### Load VAE

VAEモデルを読み込むノード。

**入力:**
- `vae_name`: VAEファイル名

**出力:**
- `VAE`: VAEオブジェクト

**設定例:**
```
vae_name: wan2.1_vae.safetensors
```

### Load Image

入力画像を読み込むノード。

**入力:**
- `image`: 画像ファイルパス

**出力:**
- `IMAGE`: 画像テンソル

### CLIP Text Encode

テキストプロンプトをエンコードするノード。

**入力:**
- `text`: プロンプト文字列
- `clip`: CLIPオブジェクト

**出力:**
- `CONDITIONING`: コンディショニングテンソル

**プロンプト例:**
```
A woman slowly turns her head and smiles, soft natural lighting, cinematic quality
```

### CLIP Vision Encode

入力画像をエンコードするノード。

**入力:**
- `clip_vision`: CLIP Visionオブジェクト
- `image`: 画像テンソル

**出力:**
- `CLIP_VISION_OUTPUT`: 画像特徴量

## Sampler Nodes

### WanVideo I2V Sampler

Wan I2V の主要サンプリングノード。

**入力:**
| パラメータ | タイプ | 説明 |
|-----------|--------|------|
| model | MODEL | 拡散モデル |
| positive | CONDITIONING | ポジティブプロンプト |
| negative | CONDITIONING | ネガティブプロンプト |
| clip_vision_output | CLIP_VISION_OUTPUT | 画像特徴量 |
| width | INT | 出力幅 |
| height | INT | 出力高さ |
| length | INT | フレーム数 |
| cfg | FLOAT | CFGスケール |
| steps | INT | サンプリングステップ数 |
| seed | INT | ランダムシード |

**出力:**
- `LATENT`: 生成された潜在表現

**推奨設定:**

| 設定 | 低VRAM | 標準 | 高品質 |
|------|--------|------|--------|
| width | 480 | 576 | 720 |
| height | 840 | 1024 | 1280 |
| length | 41 | 81 | 121 |
| cfg | 5.0 | 5.5 | 6.0 |
| steps | 20 | 25 | 30 |

### EmptyWanLatent

空の潜在表現を生成するノード。

**入力:**
- `width`: 幅
- `height`: 高さ
- `length`: フレーム数
- `batch_size`: バッチサイズ

**出力:**
- `LATENT`: 空の潜在表現

## Decoder Nodes

### VAE Decode Video

潜在表現を動画フレームにデコードするノード。

**入力:**
- `vae`: VAEオブジェクト
- `samples`: 潜在表現

**出力:**
- `IMAGE`: デコードされた動画フレーム

## Output Nodes

### Save Video

動画ファイルとして保存するノード。

**入力:**
- `images`: 動画フレーム
- `fps`: フレームレート
- `filename_prefix`: ファイル名プレフィックス

**設定例:**
```
fps: 24
filename_prefix: wan_output
format: mp4
```

### Preview Video

プレビュー表示用ノード。

**入力:**
- `images`: 動画フレーム
- `fps`: フレームレート

## TI2V (Text + Image to Video) Additional Nodes

Wan2.2 5B TI2V 専用ノード。

### WanVideo TI2V Sampler

テキストと画像を組み合わせて動画生成。

**追加入力:**
- `image`: 入力画像（オプショナル）
- `image_strength`: 画像の影響度（0.0-1.0）

**設定例:**
```
image_strength: 0.7  # 画像を強く参照
image_strength: 0.3  # テキストを強く反映
```

## Utility Nodes

### ImageResize

画像をリサイズするノード。

**入力:**
- `image`: 入力画像
- `width`: 目標幅
- `height`: 目標高さ
- `method`: リサイズ方法

**推奨設定:**
```
method: lanczos
```

### Seed (ランダム)

再現可能なシードを生成。

**入力:**
- `seed`: シード値（-1でランダム）

## Node Connections Summary

| 出力ノード | 出力タイプ | 入力ノード |
|-----------|-----------|-----------|
| Load Diffusion Model | MODEL | WanVideo Sampler |
| Load CLIP | CLIP | CLIP Text Encode |
| Load CLIP Vision | CLIP_VISION | CLIP Vision Encode |
| Load VAE | VAE | VAE Decode Video |
| Load Image | IMAGE | CLIP Vision Encode |
| CLIP Text Encode | CONDITIONING | WanVideo Sampler (positive/negative) |
| CLIP Vision Encode | CLIP_VISION_OUTPUT | WanVideo Sampler |
| WanVideo Sampler | LATENT | VAE Decode Video |
| VAE Decode Video | IMAGE | Save Video |
