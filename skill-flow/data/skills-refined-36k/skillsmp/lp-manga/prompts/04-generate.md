# Phase 4: 画像生成プロンプト（Gemini用）

## AI役割定義

あなたはプロの漫画家のアシスタントです。
以下の設定と指示に基づいて、LP漫画のコマ画像を生成してください。

## 前提条件

Phase 3で作成した以下が存在すること：

- キャラクターシート（特徴タグ含む）
- キャラクター三面図（画像）
- 絵コンテ

## Geminiへの依頼テンプレート

### 基本構造（XMLタグ形式）

Geminiに画像生成を依頼する際は、以下のXML形式で情報を提供します：

```xml
<image_generation_request>
  <role>
    あなたはプロの漫画家のアシスタントです。
    以下の設定と指示に基づいて、LP漫画の1コマを生成してください。
  </role>

  <style>
    <visual>{トーン＆マナー定義の画風スタイル}</visual>
    <color>{色彩設計}</color>
    <line>線画ははっきりとした黒</line>
    <effect>漫画的な表現（集中線、効果線）を適宜使用</effect>
  </style>

  <character>
    <name>{キャラクター名}</name>
    <tags>{キャラクターシートの特徴タグを貼り付け}</tags>
    <reference>
      [三面図画像を添付]
      ※この画像の人物の顔の造形、髪型、服装を維持してください。
    </reference>
  </character>

  <scene>
    <panel_number>{No.}</panel_number>
    <composition>{構図/カメラ}</composition>
    <expression>{キャラ/表情}</expression>
    <description>
      {絵コンテの生成指示を貼り付け}
    </description>
  </scene>

  <output_spec>
    <size>{デリバリー仕様の画像サイズ}</size>
    <aspect_ratio>{デリバリー仕様のアスペクト比}</aspect_ratio>
    <constraint>吹き出しは描かない（後で追加するため余白を確保）</constraint>
  </output_spec>
</image_generation_request>
```

### コマ生成ワークフロー

```text
1. 三面図を添付
    ↓
2. XMLテンプレートに沿ってプロンプトを作成
    ↓
3. 生成実行
    ↓
4. 結果確認
    ↓
5-A. OK → アセット管理表に記録、次のコマへ
5-B. NG → プロンプト調整して再生成
```

### プロンプト調整のコツ

| 問題 | 対策 | 追加指示 |
| :--- | :--- | :--- |
| キャラの顔が変わる | 三面図を毎回添付、特徴タグを冒頭に記載 | `<constraint>参照画像の人物と同一人物として描いてください</constraint>` |
| 指が6本になる | 手を描かない構図にする | `<constraint>手は画面外に配置</constraint>` |
| 背景が意図と違う | 背景の詳細を追記 | `<background>具体的な場所。具体的なオブジェクトが見える</background>` |
| スタイルがブレる | スタイル指定を強化 | `<visual>日本の商業漫画のような、クリーンな線画と明確な塗り分け</visual>` |

## 生成ログ・アセット管理表

生成した画像のバージョン管理と採用判定を記録します。

| No. | コマ番号 | 生成日時 | プロンプト調整内容 | 判定 | 修正必要箇所 | ファイルパス |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | 1 | YYYY-MM-DD HH:MM | 初回生成 | NG | 指が6本 | `assets/raw/01_v1.png` |
| 2 | 1 | YYYY-MM-DD HH:MM | 「手は描かず顔アップ」に変更 | OK | - | `assets/raw/01_v2.png` |

## 完了条件チェックリスト

- [ ] 全コマでOK判定の画像が存在する
- [ ] 全画像のファイルパスが記録されている
- [ ] 生成ログが記録されている
- [ ] キャラクターの一貫性が保たれている（目視確認）

## ファイル命名規則

```text
assets/
├── raw/                    # 生成した素材（未加工）
│   ├── 01_v1.png          # コマ01、バージョン1
│   ├── 01_v2.png          # コマ01、バージョン2（採用版）
│   ├── 02_v1.png
│   └── ...
├── processed/              # 加工済み素材
│   ├── 01_final.webp
│   └── ...
└── reference/              # 参照画像（三面図等）
    ├── character_a_sheet.png
    └── character_b_sheet.png
```
