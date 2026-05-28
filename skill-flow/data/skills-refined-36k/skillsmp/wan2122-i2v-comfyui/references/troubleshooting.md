# Troubleshooting Guide

Wan I2V 使用時の問題解決ガイド。

## エラー一覧

### メモリ関連エラー

#### CUDA out of memory

**症状:**
```
RuntimeError: CUDA out of memory. Tried to allocate X.XX GiB
```

**原因:**
- VRAM不足
- 解像度/フレーム数が高すぎる
- 他のアプリがVRAMを占有

**解決策:**

1. **解像度を下げる:**
   ```
   576×1024 → 480×840
   ```

2. **フレーム数を減らす:**
   ```
   81 → 41
   ```

3. **GGUFモデルを使用:**
   ```
   fp16 → Q4_K_S GGUF
   ```

4. **起動オプションを追加:**
   ```bash
   python main.py --lowvram --cpu-vae
   ```

5. **他のアプリを終了:**
   - ブラウザ（特にChrome）
   - 画像編集ソフト
   - 他のPythonプロセス

---

#### Memory allocation failed

**症状:**
```
torch.cuda.OutOfMemoryError: CUDA memory allocation failed
```

**解決策:**
上記「CUDA out of memory」と同様の対処を実施。

---

### モデル読み込みエラー

#### Model not found

**症状:**
```
FileNotFoundError: Model 'xxx.safetensors' not found
```

**原因:**
- ファイルパスが不正
- ファイル名のtypo
- ディレクトリが間違っている

**解決策:**

1. **ディレクトリ構造を確認:**
   ```
   ComfyUI/models/
   ├── diffusion_models/  ← Wanモデルはここ
   ├── text_encoders/     ← umt5はここ
   ├── vae/               ← VAEはここ
   └── clip_vision/       ← CLIP Visionはここ
   ```

2. **ファイル名を確認:**
   - 大文字/小文字を正確に
   - 拡張子を確認（.safetensors, .gguf）

3. **ComfyUIを再起動:**
   新しくダウンロードしたモデルは再起動で認識

---

#### Invalid safetensors file

**症状:**
```
safetensors_rust.SafetensorError: Invalid safetensors file
```

**原因:**
- ダウンロードが途中で失敗
- ファイルが破損

**解決策:**

1. **ファイルサイズを確認:**
   ```bash
   ls -lh models/diffusion_models/
   ```
   期待されるサイズと比較

2. **再ダウンロード:**
   ```bash
   rm models/diffusion_models/corrupted_file.safetensors
   huggingface-cli download ... --force-download
   ```

---

### 生成品質問題

#### 時間的不整合（フリッカー、ちらつき）

**症状:**
- フレーム間で急激な変化
- オブジェクトがちらつく
- 色が不安定

**原因:**
- CFGが高すぎる
- Stepsが極端

**解決策:**

1. **CFGを下げる:**
   ```
   7.0 → 5.0
   ```

2. **Stepsを調整:**
   ```
   40 → 25
   ```

3. **シードを固定:**
   ランダムシードではなく固定値を使用

---

#### 動きが少ない/静止画のよう

**症状:**
- ほとんど動かない
- 微妙な動きのみ

**原因:**
- CFGが高すぎる
- Motion Strengthが低すぎる

**解決策:**

1. **CFGを下げる:**
   ```
   6.0 → 4.0
   ```

2. **Motion Strengthを上げる（TI2V）:**
   ```
   0.5 → 0.7
   ```

3. **プロンプトに動きの記述を追加:**
   ```
   "slowly walking", "gently moving", "wind blowing"
   ```

---

#### 品質が低い/ぼやける

**症状:**
- 細部がぼやける
- ノイズが多い
- シャープさに欠ける

**原因:**
- 量子化レベルが低すぎる
- Stepsが少なすぎる
- 解像度が低すぎる

**解決策:**

1. **量子化レベルを上げる:**
   ```
   Q3_K_S → Q4_K_S → Q5_K_S
   ```

2. **Stepsを増やす:**
   ```
   20 → 25 → 30
   ```

3. **ネガティブプロンプトを追加:**
   ```
   blurry, low quality, noise, pixelated
   ```

---

### ワークフローエラー

#### Node not found

**症状:**
```
Node type 'XXX' not found
```

**原因:**
- カスタムノードがインストールされていない
- ノード名が変更された

**解決策:**

1. **カスタムノードをインストール:**
   ```bash
   cd custom_nodes
   git clone https://github.com/city96/ComfyUI-GGUF
   ```

2. **ComfyUIを更新:**
   ```bash
   cd ComfyUI
   git pull
   ```

---

#### Connection error

**症状:**
- ノード間の接続が赤くなる
- 型の不一致エラー

**原因:**
- 出力と入力の型が合わない
- ノードの順序が不正

**解決策:**

1. **接続を確認:**
   - MODEL → MODEL
   - CLIP → CLIP
   - VAE → VAE
   - CONDITIONING → CONDITIONING

2. **ワークフローテンプレートを使用:**
   Menu → Workflow → Browse Templates → Video

---

### パフォーマンス問題

#### 生成が遅すぎる

**症状:**
- 予想より大幅に時間がかかる
- 進捗が止まる

**原因:**
- CPUオフロードが発生
- 設定が高すぎる
- GPUドライバが古い

**解決策:**

1. **VRAM使用量を確認:**
   ```bash
   nvidia-smi
   ```

2. **設定を下げる:**
   - 解像度を下げる
   - フレーム数を減らす

3. **GPUドライバを更新:**
   最新のNVIDIAドライバをインストール

---

#### ComfyUIがフリーズ

**症状:**
- UIが応答しなくなる
- プログレスバーが更新されない

**原因:**
- メモリ不足
- 処理に時間がかかっている

**解決策:**

1. **待つ:**
   初回実行時は特に時間がかかる場合がある

2. **ターミナルを確認:**
   エラーが出ていないか確認

3. **強制終了して再起動:**
   ```
   Ctrl+C（ターミナル）
   python main.py --lowvram
   ```

---

## デバッグ手順

### ログ出力の有効化

```bash
python main.py --verbose
```

### VRAM監視

```bash
# リアルタイム監視
watch -n 1 nvidia-smi

# または
nvidia-smi -l 1
```

### Python依存関係の確認

```bash
pip list | grep torch
pip list | grep safetensors
pip list | grep gguf
```

### モデルファイルの検証

```bash
# ファイル一覧
ls -la models/diffusion_models/
ls -la models/text_encoders/
ls -la models/vae/
ls -la models/clip_vision/

# サイズ確認
du -sh models/*
```

## サポートリソース

### 公式ドキュメント

- [ComfyUI Wiki](https://github.com/comfyanonymous/ComfyUI/wiki)
- [Wan-Video GitHub](https://github.com/Wan-Video/Wan2.2)
- [ComfyUI-GGUF](https://github.com/city96/ComfyUI-GGUF)

### コミュニティ

- ComfyUI Discord
- Reddit r/StableDiffusion
- HuggingFace Discussions

## 問題報告テンプレート

問題を報告する際は以下の情報を含めてください：

```
## 環境
- OS:
- GPU:
- VRAM:
- ComfyUI version:
- Python version:

## 使用モデル
- Diffusion:
- Text Encoder:
- VAE:
- CLIP Vision:

## 設定
- 解像度:
- フレーム数:
- CFG:
- Steps:

## エラーメッセージ
（完全なエラーログをペースト）

## 再現手順
1.
2.
3.
```
