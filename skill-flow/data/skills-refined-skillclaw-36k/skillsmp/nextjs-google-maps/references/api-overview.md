# Google Maps Platform API 概要

## Google Maps Platform とは

Google Maps Platform は、地図、ルート、場所に関する機能を提供する Google のサービス群です。

## 利用可能な API

### Maps JavaScript API（必須）

地図をウェブページに埋め込むための基本 API。

```tsx
import { GoogleMap } from '@react-google-maps/api';

<GoogleMap
  mapContainerStyle={{ width: '100%', height: '400px' }}
  center={{ lat: 35.6812, lng: 139.7671 }}
  zoom={15}
/>
```

**主な機能:**
- 地図の表示とカスタマイズ
- マーカー、ポリゴン、ポリラインの描画
- 地図タイプの切り替え（ロードマップ、衛星写真、地形など）
- イベントハンドリング

### Places API

場所の検索、詳細情報の取得、オートコンプリートを提供。

**主な機能:**
- テキスト検索
- 近隣検索
- Place Details（詳細情報）
- オートコンプリート
- Place Photos

### Directions API

2点間または複数地点間のルート計算。

**主な機能:**
- ルート計算（車、徒歩、自転車、公共交通機関）
- 経由地（ウェイポイント）対応
- 代替ルートの取得
- 距離・所要時間の取得

### Geocoding API

住所と座標の相互変換。

**主な機能:**
- ジオコーディング（住所 → 座標）
- 逆ジオコーディング（座標 → 住所）
- コンポーネントフィルタリング

## 料金体系

Google Maps Platform は従量課金制です。

### 無料枠（月額）

| API | 無料リクエスト数 |
|-----|-----------------|
| Maps JavaScript API | 28,000 回の読み込み |
| Places API | $200 相当のクレジット |
| Directions API | $200 相当のクレジット |
| Geocoding API | $200 相当のクレジット |

### 料金例（2024年時点）

| API | 料金（1,000リクエストあたり） |
|-----|------------------------------|
| Dynamic Maps | $7.00 |
| Places Autocomplete | $2.83 |
| Directions | $5.00 |
| Geocoding | $5.00 |

> **注意**: 最新の料金は [Google Maps Platform 料金ページ](https://cloud.google.com/maps-platform/pricing) を確認してください。

## レート制限とクォータ

### デフォルトのクォータ

| API | QPM (1分あたり) | QPD (1日あたり) |
|-----|-----------------|-----------------|
| Maps JavaScript API | 無制限 | 無制限 |
| Places API | 6,000 | - |
| Directions API | 3,000 | - |
| Geocoding API | 3,000 | - |

### クォータの管理

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. 「API とサービス」→「ダッシュボード」
3. 対象の API を選択
4. 「クォータ」タブで確認・変更

## API キー管理

### ベストプラクティス

1. **環境ごとに別のキーを使用**
   - 開発用、ステージング用、本番用

2. **リファラー制限を設定**
   ```
   開発: localhost:*
   本番: https://your-domain.com/*
   ```

3. **API 制限を設定**
   - 使用する API のみを許可

4. **キーのローテーション**
   - 定期的にキーを更新

### キーの制限設定

```bash
# Google Cloud Console で設定
# 1. 「認証情報」ページへ移動
# 2. API キーを選択
# 3. 「アプリケーションの制限」で「HTTP リファラー」を選択
# 4. 許可するドメインを追加
# 5. 「API の制限」で使用する API のみを選択
```

## 必要なライブラリ

`@react-google-maps/api` で使用するライブラリを指定:

```tsx
const libraries: Libraries = ['places', 'drawing', 'visualization', 'geometry'];
```

| ライブラリ | 用途 |
|-----------|------|
| `places` | Places API（オートコンプリート、場所検索） |
| `drawing` | 描画ツール（ポリゴン、円など） |
| `visualization` | ヒートマップ |
| `geometry` | 距離計算、ポリゴン内判定など |

## エラーコード一覧

| エラー | 原因 | 解決策 |
|--------|------|--------|
| `InvalidKeyMapError` | API キーが無効 | キーを再確認・再生成 |
| `RefererNotAllowedMapError` | リファラー制限に違反 | 許可リストにドメインを追加 |
| `ApiNotActivatedMapError` | API が有効化されていない | Cloud Console で API を有効化 |
| `OverQueryLimitMapError` | クォータ超過 | クォータを増やすか、リクエストを削減 |
| `RequestDeniedMapError` | リクエスト拒否 | API キーの制限を確認 |

## セキュリティ考慮事項

### クライアントサイド API キーの保護

1. **リファラー制限は必須**
   - 本番ドメインのみを許可

2. **API キーの公開範囲を理解する**
   - `NEXT_PUBLIC_` プレフィックスのキーはクライアントに公開される
   - サーバーサイドのみで使用する場合は別のキーを使用

3. **使用量の監視**
   - 異常な使用量を検知するアラートを設定

### サーバーサイド API 呼び出し

機密性の高い操作はサーバーサイドで実行:

```tsx
// app/api/geocode/route.ts
export async function POST(request: Request) {
  const { address } = await request.json();

  const response = await fetch(
    `https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(address)}&key=${process.env.GOOGLE_MAPS_SERVER_KEY}`
  );

  return Response.json(await response.json());
}
```

## 関連リソース

- [Google Maps Platform ドキュメント](https://developers.google.com/maps/documentation)
- [Google Cloud Console](https://console.cloud.google.com/)
- [料金計算ツール](https://cloud.google.com/maps-platform/pricing)
- [@react-google-maps/api リファレンス](react-google-maps-api.md)
