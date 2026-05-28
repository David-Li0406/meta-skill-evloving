# ComfyUI Setup for Wan I2V

Wan I2V モデルを ComfyUI で使用するためのセットアップガイド。

## Prerequisites

### システム要件

- Python 3.10 以上
- CUDA 11.8 以上（NVIDIA GPU使用時）
- Git
- 十分なストレージ容量（最低50GB）

### GPU要件

| 用途 | 最小VRAM | 推奨VRAM |
|------|----------|----------|
| GGUF Q4 | 8GB | 10GB |
| Wan2.2 5B | 12GB | 16GB |
| Wan2.2 14B fp8 | 20GB | 24GB |
| Wan2.2 14B fp16 | 40GB | 48GB |

## Installation Steps

### 1. ComfyUI のインストール

```bash
# リポジトリをクローン
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI

# 仮想環境を作成（推奨）
python -m venv venv
source venv/bin/activate  # Linux/macOS
# または
.\venv\Scripts\activate  # Windows

# 依存関係をインストール
pip install -r requirements.txt

# PyTorch（CUDA対応版）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### 2. ComfyUI-GGUF のインストール（低VRAM向け）

```bash
cd custom_nodes
git clone https://github.com/city96/ComfyUI-GGUF
cd ComfyUI-GGUF
pip install -r requirements.txt
```

### 3. モデルファイルのダウンロード

#### Diffusion Models

**Wan2.2 5B（推奨、バランス型）:**
```bash
# HuggingFaceからダウンロード
huggingface-cli download Wan-Video/Wan2.2 wan2.2_ti2v_5B_fp16.safetensors \
  --local-dir models/diffusion_models/
```

**Wan2.2 14B GGUF（低VRAM向け）:**
```bash
huggingface-cli download QuantStack/Wan2.2-I2V-A14B-GGUF Wan2.2-I2V-A14B-Q4_K_S.gguf \
  --local-dir models/diffusion_models/
```

#### Text Encoder

```bash
huggingface-cli download Comfy-Org/Wan_2.1_ComfyUI_models \
  split_files/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors \
  --local-dir models/text_encoders/
```

#### VAE

```bash
huggingface-cli download Comfy-Org/Wan_2.1_ComfyUI_models \
  split_files/vae/wan2.1_vae.safetensors \
  --local-dir models/vae/
```

#### CLIP Vision

```bash
huggingface-cli download Comfy-Org/Wan_2.1_ComfyUI_models \
  split_files/clip_vision/clip_vision_h.safetensors \
  --local-dir models/clip_vision/
```

## Directory Structure Verification

インストール後、以下の構造になっていることを確認：

```
ComfyUI/
├── main.py
├── models/
│   ├── diffusion_models/
│   │   ├── wan2.2_ti2v_5B_fp16.safetensors      # または
│   │   └── Wan2.2-I2V-A14B-Q4_K_S.gguf          # GGUF版
│   ├── text_encoders/
│   │   └── umt5_xxl_fp8_e4m3fn_scaled.safetensors
│   ├── vae/
│   │   └── wan2.1_vae.safetensors
│   └── clip_vision/
│       └── clip_vision_h.safetensors
├── custom_nodes/
│   └── ComfyUI-GGUF/                            # 低VRAM用
└── input/
    └── (your_input_images.png)
```

## Starting ComfyUI

### 基本起動

```bash
python main.py
```

### 低VRAMモード起動

```bash
python main.py --lowvram
```

### CPU オフロード有効

```bash
python main.py --cpu-vae
```

### ポート指定

```bash
python main.py --port 8188
```

## Loading Workflow Templates

1. ComfyUI を起動
2. ブラウザで `http://localhost:8188` を開く
3. Menu → Workflow → Browse Templates → Video
4. 「Wan2.2 14B I2V」または「Wan2.2 5B TI2V」を選択

## First Run Verification

### チェックリスト

- [ ] すべてのモデルファイルが正しいディレクトリに配置されている
- [ ] ComfyUI が正常に起動する
- [ ] ワークフローテンプレートが読み込める
- [ ] 各ノードでモデルが選択できる
- [ ] テスト画像で動画生成が成功する

### テスト生成設定

初回テストには以下の低負荷設定を推奨：

```
解像度: 480×840
フレーム数: 41
CFG: 5.0
Steps: 20
```

## Troubleshooting Installation

### よくある問題

| 問題 | 原因 | 解決策 |
|------|------|--------|
| ModuleNotFoundError | 依存関係未インストール | `pip install -r requirements.txt` |
| CUDA out of memory | VRAM不足 | `--lowvram` オプション使用 |
| Model not found | パス不正 | ディレクトリ構造を確認 |
| safetensors error | ファイル破損 | 再ダウンロード |

### ログ確認

```bash
# 詳細ログを有効化
python main.py --verbose
```

## Update ComfyUI

```bash
cd ComfyUI
git pull
pip install -r requirements.txt --upgrade
```

## Update Custom Nodes

```bash
cd custom_nodes/ComfyUI-GGUF
git pull
pip install -r requirements.txt --upgrade
```
