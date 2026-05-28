# Nano Banana 参照情報

公式ドキュメントとベストプラクティスの参照リンク・要点まとめ。

---

## 公式ドキュメント

### Google AI Developer Docs
- [Image Generation Overview](https://ai.google.dev/gemini-api/docs/image-generation)
  - モデル: `gemini-2.5-flash-image` / `gemini-3-pro-image-preview`
  - SynthID watermark が全生成画像に入る
  - `imageConfig.aspectRatio` でアスペクト比指定可能

### Nano Banana Pro Prompting Guide
- [dev.to - Nano Banana Pro Prompting Strategies](https://dev.to/googleai/nano-banana-pro-prompting-guide-strategies-1h9n)
  - Identity Locking のベストプラクティス
  - Structural Control & Layout Guidance
  - Edit, Don't Re-roll 戦略

---

## モデル比較

| 項目 | Flash (`gemini-2.5-flash-image`) | Pro (`gemini-3-pro-image-preview`) |
|------|----------------------------------|-----------------------------------|
| 速度 | 速い | 遅め |
| コスト | 低い | 高い |
| 文字精度 | 中程度 | 高い |
| 複雑な指示 | 中程度 | 高い |
| 参照画像枚数 | 3枚程度 | 5枚（最大14枚） |
| 推奨用途 | ラフ案量産、イテレーション | ロゴ、文字入り、最終仕上げ |

---

## プロンプティング原則（公式推奨）

### 1. Describe the Scene（シーンを説明）
タグ羅列ではなく、シーン全体を文章で説明する。

### 2. Be Hyper-Specific（具体的に）
曖昧な指示は避け、年齢/服/素材感/時間帯など詳細を入れる。

### 3. Control the Camera（撮影言語で制御）
shot type / angle / lens / DoF などカメラ用語で構図を指定。

### 4. Provide Context and Intent（文脈と意図）
用途（EC用、サムネ用、ポスター下地）を明示する。

### 5. Semantic Negative Prompts（意味的な否定）
`no xxx` ではなく「xxxが存在しない状態」「背景がクリーンで単色」のように書く。

### 6. Iterate and Refine（会話で微修正）
当たりが出たらリロールせず、差分指示で詰める。

---

## 用途別の推奨設定

### ロゴ/文字入り
- **モデル**: Pro 推奨
- **aspectRatio**: 1:1 または 16:9
- **注意**: 文字は引用符で固定、崩れる場合は2段階生成

### EC/物撮り
- **モデル**: Flash でラフ → Pro で仕上げ
- **aspectRatio**: 1:1（正方形）または 4:5（Instagram向け）
- **注意**: 背景は白/グラデ、余白でテキスト領域確保

### サムネ/ポスター下地
- **モデル**: Flash でラフ → Pro で仕上げ
- **aspectRatio**: 16:9（YouTube）または 9:16（縦型）
- **注意**: ネガティブスペースを明示的に指定

### ステッカー/アイコン
- **モデル**: Flash で十分
- **aspectRatio**: 1:1
- **注意**: 背景透明、線の太さ・塗りスタイルを明示

### 写実/シネマティック
- **モデル**: Flash でラフ → Pro で仕上げ
- **aspectRatio**: 16:9 または 21:9
- **注意**: レンズ/絞り/被写界深度を撮影言語で指定

---

## 編集時の注意事項

### 権利に関する注意
- **自分が権利を持つ画像のみ**を入力すること
- 他人の著作物、肖像権のある画像は使用しない
- 生成物の商用利用は利用規約を確認

### 編集の基本パターン
1. **追加（Add）**: 元画像に要素を追加
2. **削除（Remove）**: 元画像から要素を削除
3. **変更（Change）**: 元画像の一部を変更

### 編集プロンプトの書き方
```text
Keep everything the same as the input image except:
- Change: [変更内容]
- Add: [追加内容]
- Remove: [削除内容]
Maintain consistent lighting, perspective, and style with the original.
```

---

## 参照画像の活用

### Identity Locking（同一性固定）
- 「Image 1 と同じ顔を維持」と明示
- Pro モデル推奨
- 複数枚の同一人物画像で精度向上

### Structural Control（構造制御）
- ワイヤーフレーム/グリッド画像でレイアウト強制
- 「Image 2 の構図に従う」と明示

### Style Transfer（スタイル転送）
- 「Image 3 のレンダリングスタイルに合わせる」
- 色味/タッチ/雰囲気を参照画像から継承

---

## トラブルシューティング

### 文字が崩れる
1. Pro モデルに切り替える
2. 文字を引用符で明示: `Text to include (exact): "YOUR TEXT"`
3. 2段階生成: 文字のみ → 文字入り画像

### 同一性が維持されない
1. Pro モデルに切り替える
2. 参照画像を複数枚入力（同一人物の異なる角度）
3. 「keep the face identical to Image 1」と明示

### 構図が安定しない
1. 構図を詳細に指定（rule of thirds, centered, etc.）
2. ワイヤーフレーム参照画像を入力
3. 「place subject on left third」など位置を明示

### 背景がごちゃごちゃする
1. 「simple, clean, low-detail background」と明示
2. 「solid [color] background」と単色指定
3. 「negative space on [direction]」と余白を指示
