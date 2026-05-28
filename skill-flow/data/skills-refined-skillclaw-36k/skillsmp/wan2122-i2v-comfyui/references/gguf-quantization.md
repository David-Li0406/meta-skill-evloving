# GGUF Quantization Guide

低VRAM環境でWan I2Vを実行するためのGGUF量子化ガイド。

## GGUF概要

GGUF（GPT-Generated Unified Format）は、大規模モデルを効率的に量子化・圧縮するフォーマット。元のfp16/bf16モデルを2-8ビットに量子化し、VRAM使用量を大幅に削減する。

## 利点と欠点

### 利点

- **VRAM削減**: 最大80-90%のメモリ削減
- **コンシューマーGPU対応**: 8GB VRAMでも14Bモデルを実行可能
- **段階的オフロード**: GPU/CPU間の自動メモリ管理

### 欠点

- **品質低下**: 量子化レベルに応じた品質劣化
- **生成速度**: CPU オフロード時は速度低下
- **カスタムノード必要**: ComfyUI-GGUF が必須

## 量子化レベル比較

| 量子化 | モデルサイズ | VRAM目安 | 品質 | 推奨度 |
|--------|-------------|----------|------|--------|
| Q2_K | ~1.85GB | 6GB | ★★☆☆☆ | 極限環境のみ |
| Q3_K_S | ~2.29GB | 8GB | ★★★☆☆ | 低VRAM |
| Q4_K_S | ~3.12GB | 10GB | ★★★★☆ | **推奨** |
| Q4_K_M | ~3.31GB | 10GB | ★★★★☆ | 推奨 |
| Q5_K_S | ~3.56GB | 12GB | ★★★★★ | 品質重視 |
| Q5_K_M | ~3.80GB | 12GB | ★★★★★ | 最高品質量子化 |
| Q6_K | ~4.53GB | 14GB | ★★★★★ | ほぼ無損失 |
| Q8_0 | ~5.00GB | 16GB | ★★★★★ | 事実上無損失 |

## インストール手順

### 1. ComfyUI-GGUF のインストール

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/city96/ComfyUI-GGUF
cd ComfyUI-GGUF
pip install -r requirements.txt
```

### 2. GGUFモデルのダウンロード

**Wan2.2 14B I2V（推奨: Q4_K_S）:**
```bash
huggingface-cli download QuantStack/Wan2.2-I2V-A14B-GGUF \
  Wan2.2-I2V-A14B-Q4_K_S.gguf \
  --local-dir ComfyUI/models/diffusion_models/
```

**他の量子化レベル:**
```bash
# Q3_K_S（より低VRAM）
huggingface-cli download QuantStack/Wan2.2-I2V-A14B-GGUF \
  Wan2.2-I2V-A14B-Q3_K_S.gguf \
  --local-dir ComfyUI/models/diffusion_models/

# Q5_K_S（より高品質）
huggingface-cli download QuantStack/Wan2.2-I2V-A14B-GGUF \
  Wan2.2-I2V-A14B-Q5_K_S.gguf \
  --local-dir ComfyUI/models/diffusion_models/
```

### 3. ディレクトリ確認

```
ComfyUI/
├── models/
│   └── diffusion_models/
│       └── Wan2.2-I2V-A14B-Q4_K_S.gguf
└── custom_nodes/
    └── ComfyUI-GGUF/
```

## ワークフロー設定

### 通常ノード vs GGUFノード

| 用途 | 通常 | GGUF |
|------|------|------|
| モデル読み込み | Load Diffusion Model | Load GGUF |
| 対応形式 | .safetensors, .pt | .gguf |
| VRAM使用 | 高 | 低 |

### GGUFワークフロー構成

```
[Load GGUF] ──────────────────────────────────┐
                                              │
[Load CLIP] → [CLIP Text Encode] ─────────────┤
                                              ├→ [WanVideo Sampler]
[Load CLIP Vision] → [CLIP Vision Encode] ────┤
                                              │
[Load VAE] ───────────────────────────────────┘
```

### Load GGUF ノードの設定

```
Node: Load GGUF
├── gguf_name: Wan2.2-I2V-A14B-Q4_K_S.gguf
└── (自動的にモデルを検出)
```

## メモリ最適化設定

### ComfyUI起動オプション

```bash
# 低VRAMモード（推奨）
python main.py --lowvram

# VAEをCPUで処理
python main.py --cpu-vae

# 積極的なVRAM解放
python main.py --lowvram --cpu-vae
```

### ワークフロー内での最適化

1. **解像度を下げる**: 576×1024 → 480×840
2. **フレーム数を減らす**: 81 → 41
3. **バッチサイズを1に**: batch_size = 1

## VRAM使用量ガイド

### Q4_K_S使用時の目安

| 設定 | VRAM使用量 |
|------|-----------|
| 480×840, 41f | ~6-7GB |
| 576×1024, 41f | ~8-9GB |
| 576×1024, 81f | ~10-11GB |
| 720×1280, 41f | ~11-12GB |

### Q3_K_S使用時の目安

| 設定 | VRAM使用量 |
|------|-----------|
| 480×840, 41f | ~5-6GB |
| 576×1024, 41f | ~7-8GB |
| 576×1024, 81f | ~8-9GB |

## 品質比較

### 各量子化レベルの出力品質

```
fp16 (参照)  ████████████████████ 100%
Q8_0         ████████████████████ ~99%
Q6_K         ███████████████████░ ~97%
Q5_K_M       ██████████████████░░ ~95%
Q5_K_S       █████████████████░░░ ~93%
Q4_K_M       ████████████████░░░░ ~90%
Q4_K_S       ███████████████░░░░░ ~88%
Q3_K_S       █████████████░░░░░░░ ~80%
Q2_K         ███████████░░░░░░░░░ ~70%
```

### 品質維持のコツ

1. **Q4_K_S以上を使用**: Q3以下は目立つ劣化
2. **CFGを調整**: 量子化モデルでは低めのCFG（4.0-5.0）が効果的
3. **Stepsを増やす**: 品質補填のため25-30推奨

## トラブルシューティング

### よくある問題

| 問題 | 原因 | 解決策 |
|------|------|--------|
| GGUFノードが見つからない | カスタムノード未インストール | ComfyUI-GGUFをインストール |
| モデルが読み込めない | パスが不正 | diffusion_modelsディレクトリを確認 |
| OOMエラー | 設定が高すぎ | 解像度/フレーム数を下げる |
| 品質が低い | 量子化レベル | Q4_K_S以上を使用 |
| 生成が遅い | CPUオフロード | 解像度を下げてGPUのみで処理 |

### GGUFモデルの検証

```bash
# ファイルサイズ確認
ls -lh ComfyUI/models/diffusion_models/Wan2.2-I2V-A14B-Q4_K_S.gguf
# 期待: ~3.1GB

# ハッシュ検証（オプション）
sha256sum Wan2.2-I2V-A14B-Q4_K_S.gguf
```

## 推奨設定まとめ

### 8GB VRAM

```yaml
model: Wan2.2-I2V-A14B-Q3_K_S.gguf
resolution: 480×840
frames: 41
cfg: 4.5
steps: 25
起動オプション: --lowvram --cpu-vae
```

### 10-12GB VRAM

```yaml
model: Wan2.2-I2V-A14B-Q4_K_S.gguf
resolution: 576×1024
frames: 81
cfg: 5.0
steps: 25
起動オプション: --lowvram
```

### 16GB VRAM

```yaml
model: Wan2.2-I2V-A14B-Q5_K_S.gguf
resolution: 720×1280
frames: 81
cfg: 5.5
steps: 30
起動オプション: (なし)
```
