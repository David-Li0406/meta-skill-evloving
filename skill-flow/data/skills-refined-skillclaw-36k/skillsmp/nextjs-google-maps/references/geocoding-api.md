# Geocoding API リファレンス

## 概要

Geocoding API は、住所と地理座標（緯度・経度）の相互変換を提供します。

- **ジオコーディング**: 住所 → 座標
- **逆ジオコーディング**: 座標 → 住所

## 有効化が必要な API

- Geocoding API

## 基本的な使用法

### ジオコーディング（住所 → 座標）

```tsx
function geocodeAddress(address: string): Promise<google.maps.LatLngLiteral | null> {
  const geocoder = new google.maps.Geocoder();

  return new Promise((resolve, reject) => {
    geocoder.geocode({ address }, (results, status) => {
      if (status === 'OK' && results?.[0]) {
        const location = results[0].geometry.location;
        resolve({
          lat: location.lat(),
          lng: location.lng(),
        });
      } else if (status === 'ZERO_RESULTS') {
        resolve(null);
      } else {
        reject(new Error(`Geocoding failed: ${status}`));
      }
    });
  });
}

// 使用例
const position = await geocodeAddress('東京都千代田区丸の内1-9-1');
console.log(position); // { lat: 35.6812, lng: 139.7671 }
```

### 逆ジオコーディング（座標 → 住所）

```tsx
function reverseGeocode(
  location: google.maps.LatLngLiteral
): Promise<string | null> {
  const geocoder = new google.maps.Geocoder();

  return new Promise((resolve, reject) => {
    geocoder.geocode({ location }, (results, status) => {
      if (status === 'OK' && results?.[0]) {
        resolve(results[0].formatted_address);
      } else if (status === 'ZERO_RESULTS') {
        resolve(null);
      } else {
        reject(new Error(`Reverse geocoding failed: ${status}`));
      }
    });
  });
}

// 使用例
const address = await reverseGeocode({ lat: 35.6812, lng: 139.7671 });
console.log(address); // "日本、〒100-0005 東京都千代田区丸の内..."
```

## GeocoderRequest オプション

```tsx
interface GeocoderRequest {
  // 住所文字列（ジオコーディング用）
  address?: string;

  // 座標（逆ジオコーディング用）
  location?: google.maps.LatLng | google.maps.LatLngLiteral;

  // Place ID（特定の場所を指定）
  placeId?: string;

  // 検索範囲の境界
  bounds?: google.maps.LatLngBounds | google.maps.LatLngBoundsLiteral;

  // 検索対象の地域コード
  region?: string;

  // コンポーネントフィルタ
  componentRestrictions?: {
    country?: string | string[];
    postalCode?: string;
    administrativeArea?: string;
    locality?: string;
    route?: string;
  };

  // 言語
  language?: string;
}
```

## GeocoderResult の構造

```tsx
interface GeocoderResult {
  // 住所コンポーネント
  address_components: Array<{
    long_name: string;
    short_name: string;
    types: string[];
  }>;

  // フォーマット済み住所
  formatted_address: string;

  // 位置情報
  geometry: {
    location: google.maps.LatLng;
    location_type: 'ROOFTOP' | 'RANGE_INTERPOLATED' | 'GEOMETRIC_CENTER' | 'APPROXIMATE';
    viewport: google.maps.LatLngBounds;
    bounds?: google.maps.LatLngBounds;
  };

  // Place ID
  place_id: string;

  // 住所タイプ
  types: string[];

  // 結果の一部がマッチしたかどうか
  partial_match?: boolean;

  // plus_code（オプション）
  plus_code?: {
    compound_code: string;
    global_code: string;
  };
}
```

## 住所コンポーネントの解析

日本の住所を解析するユーティリティ:

```tsx
interface JapaneseAddress {
  postalCode?: string;
  country?: string;
  prefecture?: string;
  city?: string;
  ward?: string;
  town?: string;
  chome?: string;
  banchi?: string;
  building?: string;
}

function parseJapaneseAddress(
  components: google.maps.GeocoderAddressComponent[] | undefined
): JapaneseAddress {
  if (!components) return {};

  const find = (types: string[]) =>
    components.find((c) => types.some((t) => c.types.includes(t)));

  return {
    postalCode: find(['postal_code'])?.long_name,
    country: find(['country'])?.long_name,
    prefecture: find(['administrative_area_level_1'])?.long_name,
    city: find(['locality'])?.long_name,
    ward: find(['sublocality_level_1', 'political'])?.long_name,
    town: find(['sublocality_level_2'])?.long_name,
    chome: find(['sublocality_level_3'])?.long_name,
    banchi: find(['sublocality_level_4', 'premise'])?.long_name,
  };
}
```

## 地域バイアス

検索結果を特定の地域に偏らせる:

```tsx
// 日本に限定
geocoder.geocode({
  address: '渋谷',
  componentRestrictions: {
    country: 'jp',
  },
});

// 東京周辺を優先
geocoder.geocode({
  address: '渋谷',
  bounds: {
    north: 35.9,
    south: 35.5,
    east: 140.0,
    west: 139.5,
  },
});

// 地域コードで指定
geocoder.geocode({
  address: 'Shibuya',
  region: 'jp',
});
```

## 位置精度（location_type）

| 値 | 説明 |
|-----|------|
| `ROOFTOP` | 正確な位置（建物レベル） |
| `RANGE_INTERPOLATED` | 推定位置（道路上の補間） |
| `GEOMETRIC_CENTER` | 幾何学的中心（ポリゴンの中心など） |
| `APPROXIMATE` | おおよその位置 |

```tsx
// 精度でフィルタリング
async function getExactLocation(address: string) {
  const geocoder = new google.maps.Geocoder();

  return new Promise((resolve) => {
    geocoder.geocode({ address }, (results, status) => {
      if (status === 'OK' && results) {
        // ROOFTOP 精度の結果のみを使用
        const exact = results.find(
          (r) => r.geometry.location_type === 'ROOFTOP'
        );
        resolve(exact || results[0]);
      } else {
        resolve(null);
      }
    });
  });
}
```

## バッチ処理

複数の住所を一度に処理:

```tsx
async function batchGeocode(
  addresses: string[],
  delayMs: number = 100
): Promise<Map<string, google.maps.LatLngLiteral | null>> {
  const results = new Map<string, google.maps.LatLngLiteral | null>();

  for (const address of addresses) {
    try {
      const position = await geocodeAddress(address);
      results.set(address, position);
    } catch (error) {
      console.error(`Failed to geocode: ${address}`, error);
      results.set(address, null);
    }

    // レート制限を避けるための遅延
    await new Promise((resolve) => setTimeout(resolve, delayMs));
  }

  return results;
}

// 使用例
const addresses = [
  '東京都渋谷区渋谷1-1-1',
  '東京都新宿区新宿1-1-1',
  '東京都港区六本木1-1-1',
];

const positions = await batchGeocode(addresses);
```

## エラーハンドリング

```tsx
const GeocoderStatus = google.maps.GeocoderStatus;

function handleGeocoderError(status: google.maps.GeocoderStatus): string {
  switch (status) {
    case GeocoderStatus.OK:
      return '';
    case GeocoderStatus.ZERO_RESULTS:
      return '住所が見つかりませんでした';
    case GeocoderStatus.OVER_QUERY_LIMIT:
      return 'API 制限を超えました。しばらく待ってから再試行してください';
    case GeocoderStatus.REQUEST_DENIED:
      return 'リクエストが拒否されました。API キーを確認してください';
    case GeocoderStatus.INVALID_REQUEST:
      return '無効なリクエストです';
    case GeocoderStatus.UNKNOWN_ERROR:
      return 'サーバーエラーが発生しました';
    default:
      return '不明なエラーが発生しました';
  }
}
```

## React Hook

```tsx
import { useState, useCallback } from 'react';

interface UseGeocoderResult {
  geocode: (address: string) => Promise<google.maps.LatLngLiteral | null>;
  reverseGeocode: (position: google.maps.LatLngLiteral) => Promise<string | null>;
  isLoading: boolean;
  error: string | null;
}

export function useGeocoder(): UseGeocoderResult {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const geocode = useCallback(async (address: string) => {
    setIsLoading(true);
    setError(null);

    try {
      const result = await geocodeAddress(address);
      return result;
    } catch (err) {
      setError(err instanceof Error ? err.message : '不明なエラー');
      return null;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const reverseGeocode = useCallback(async (position: google.maps.LatLngLiteral) => {
    setIsLoading(true);
    setError(null);

    try {
      const result = await reverseGeocodeAddress(position);
      return result;
    } catch (err) {
      setError(err instanceof Error ? err.message : '不明なエラー');
      return null;
    } finally {
      setIsLoading(false);
    }
  }, []);

  return { geocode, reverseGeocode, isLoading, error };
}
```

## 料金

| 操作 | 料金（1,000リクエストあたり） |
|------|------------------------------|
| ジオコーディング | $5.00 |
| 逆ジオコーディング | $5.00 |

**無料枠**: 毎月 $200 のクレジット（約 40,000 リクエスト）

## ベストプラクティス

1. **キャッシュを活用**
   - 同じ住所の結果をキャッシュして重複リクエストを避ける

2. **バッチ処理時はレート制限に注意**
   - リクエスト間に適切な遅延を設ける

3. **地域制限を使用**
   - 検索精度向上と料金最適化のため

4. **エラーハンドリングを適切に**
   - ユーザーに分かりやすいエラーメッセージを表示

5. **位置精度を確認**
   - 重要な操作では `ROOFTOP` 精度を確認

## 関連リソース

- [Geocoding API 公式ドキュメント](https://developers.google.com/maps/documentation/geocoding)
- [ジオコーディングコード例](../examples/geocoding-service.ts)
- [Places API](places-api.md)
