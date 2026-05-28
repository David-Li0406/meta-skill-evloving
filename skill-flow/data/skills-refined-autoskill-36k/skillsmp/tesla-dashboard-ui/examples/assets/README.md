# Tesla Dashboard UI - Custom Assets

カスタムSVGアイコンをAsset Catalogに追加する手順。

## Overview / 概要

Tesla Dashboard UIでは、SF Symbolsに加えて、Tesla固有のカスタムアイコンを使用できます。
このディレクトリには、カスタムSVGアイコンとその使用方法を記載しています。

## Directory Structure / ディレクトリ構造

```
assets/
├── README.md           # このファイル
├── icons/              # カスタムSVGアイコン
│   ├── tesla-logo.svg
│   ├── battery-charging.svg
│   ├── door-open.svg
│   └── ...
└── images/             # その他の画像アセット
    └── ...
```

## Adding Icons to Xcode / Xcodeへの追加手順

### 1. Asset Catalogを開く

1. Xcodeでプロジェクトを開く
2. `Assets.xcassets` を選択
3. 新しい Image Set を作成（右クリック → New Image Set）

### 2. SVGアイコンを追加

1. SVGファイルをImage Setにドラッグ＆ドロップ
2. 「Preserve Vector Data」をオンにする
3. 「Render As」を「Template Image」に設定（色を動的に変更する場合）

### 3. コードで使用

```swift
// Asset Catalogのアイコンを使用
Image("tesla-logo")
    .foregroundStyle(TeslaColors.accent)

// または TeslaIcon enumを拡張
extension TeslaIcon {
    static let teslaLogo = TeslaIcon(customName: "tesla-logo")
}
```

## Custom Icon Guidelines / カスタムアイコンのガイドライン

### サイズ

- 推奨サイズ: 24×24pt（@1x）
- ベクターデータとして保存（スケーラブル）

### カラー

- 単色で作成（Template Imageとして使用）
- 線の太さ: 2pt（SF Symbolsとの一貫性）

### ファイル形式

- SVG（推奨）
- PDF（ベクター）
- PNG（@1x, @2x, @3x が必要）

## Included Icons / 含まれるアイコン

現在、以下のカスタムアイコンが利用可能です：

| Icon | Name | Usage |
|------|------|-------|
| 🚗 | tesla-logo | Teslaブランドロゴ |
| 🔋 | battery-wave | 充電中のアニメーション用 |
| 🚪 | door-ajar | ドア半開き警告 |

## Creating Custom Icons / カスタムアイコンの作成

### Figmaでの作成

1. 24×24pxのフレームを作成
2. ストローク幅: 2px
3. 角丸: 2px（小さい要素）/ 4px（大きい要素）
4. SVGとしてエクスポート

### Illustratorでの作成

1. 24×24ptのアートボードを作成
2. ストローク幅: 2pt
3. 角丸: 2pt / 4pt
4. ファイル → 書き出し → SVG

## Code Usage Example / コード使用例

```swift
import SwiftUI

// カスタムアイコンを含むビュー
struct CustomIconView: View {
    var body: some View {
        HStack(spacing: 16) {
            // SF Symbol
            TeslaIconView(icon: .car, size: 24)

            // カスタムアイコン（Asset Catalog）
            Image("tesla-logo")
                .resizable()
                .scaledToFit()
                .frame(width: 24, height: 24)
                .foregroundStyle(TeslaColors.accent)
        }
    }
}

// TeslaIcon enumの拡張（カスタムアイコン対応）
enum TeslaCustomIcon: String {
    case teslaLogo = "tesla-logo"
    case batteryWave = "battery-wave"
    case doorAjar = "door-ajar"

    var image: Image {
        Image(rawValue)
    }
}

struct TeslaCustomIconView: View {
    let icon: TeslaCustomIcon
    var size: CGFloat = 24
    var color: Color = TeslaColors.textPrimary

    var body: some View {
        icon.image
            .resizable()
            .scaledToFit()
            .frame(width: size, height: size)
            .foregroundStyle(color)
    }
}
```

## Notes / 注意事項

- SF Symbolsで対応できる場合は、カスタムアイコンよりSF Symbolsを優先
- カスタムアイコンはプロジェクト固有の要素のみに使用
- アイコンの著作権・ライセンスに注意

## Resources / リソース

- [SF Symbols App](https://developer.apple.com/sf-symbols/)
- [Human Interface Guidelines - Icons](https://developer.apple.com/design/human-interface-guidelines/icons)
- [Figma Tesla UI Kit](https://www.figma.com/community/file/1382192547846546595)
