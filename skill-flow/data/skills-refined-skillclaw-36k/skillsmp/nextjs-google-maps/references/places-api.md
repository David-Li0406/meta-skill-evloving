# Places API リファレンス

## 概要

Places API は、場所の検索、詳細情報の取得、オートコンプリートを提供する Google Maps Platform の API です。

## 有効化が必要な API

- Places API
- Places API (New) - 新しい機能を使用する場合

## Autocomplete コンポーネント

場所検索のオートコンプリート入力を提供。

### 基本的な使用法

```tsx
import { Autocomplete } from '@react-google-maps/api';
import { useState, useCallback } from 'react';

function PlaceAutocomplete() {
  const [autocomplete, setAutocomplete] = useState<google.maps.places.Autocomplete | null>(null);

  const onLoad = useCallback((ac: google.maps.places.Autocomplete) => {
    setAutocomplete(ac);
  }, []);

  const onPlaceChanged = useCallback(() => {
    if (autocomplete) {
      const place = autocomplete.getPlace();
      console.log('Selected place:', place);
    }
  }, [autocomplete]);

  return (
    <Autocomplete onLoad={onLoad} onPlaceChanged={onPlaceChanged}>
      <input type="text" placeholder="場所を検索..." />
    </Autocomplete>
  );
}
```

### Autocomplete オプション

```tsx
<Autocomplete
  onLoad={onLoad}
  onPlaceChanged={onPlaceChanged}
  options={{
    // 検索対象の国を制限
    componentRestrictions: { country: 'jp' },

    // 検索タイプを制限
    types: ['establishment'],

    // 検索範囲を制限
    bounds: {
      north: 35.9,
      south: 35.5,
      east: 140.0,
      west: 139.5,
    },

    // 検索範囲を厳密に制限
    strictBounds: true,

    // 取得するフィールドを指定（料金に影響）
    fields: ['place_id', 'geometry', 'name', 'formatted_address'],
  }}
>
  <input type="text" />
</Autocomplete>
```

### types オプションの値

| 値 | 説明 |
|-----|------|
| `establishment` | 店舗・施設 |
| `geocode` | 住所 |
| `address` | 正確な住所 |
| `(regions)` | 地域（市区町村など） |
| `(cities)` | 都市 |

### fields オプションの値と料金

| カテゴリ | フィールド | 料金 |
|---------|----------|------|
| Basic | `address_components`, `formatted_address`, `geometry`, `name`, `place_id`, `types` | $0 |
| Contact | `formatted_phone_number`, `international_phone_number`, `opening_hours`, `website` | $3/1000 |
| Atmosphere | `price_level`, `rating`, `reviews`, `user_ratings_total` | $5/1000 |

## PlaceResult オブジェクト

Autocomplete や PlaceService から返される場所情報。

```tsx
interface PlaceResult {
  // 基本情報
  place_id?: string;
  name?: string;
  formatted_address?: string;
  types?: string[];

  // 位置情報
  geometry?: {
    location: google.maps.LatLng;
    viewport?: google.maps.LatLngBounds;
  };

  // 住所コンポーネント
  address_components?: Array<{
    long_name: string;
    short_name: string;
    types: string[];
  }>;

  // 連絡先情報
  formatted_phone_number?: string;
  international_phone_number?: string;
  website?: string;

  // 営業時間
  opening_hours?: {
    isOpen: () => boolean;
    weekday_text: string[];
    periods: Array<{
      open: { day: number; time: string };
      close?: { day: number; time: string };
    }>;
  };

  // 評価情報
  rating?: number;
  user_ratings_total?: number;
  reviews?: Array<{
    author_name: string;
    rating: number;
    text: string;
    time: number;
  }>;

  // 写真
  photos?: Array<{
    getUrl: (opts?: { maxWidth?: number; maxHeight?: number }) => string;
    height: number;
    width: number;
  }>;
}
```

## PlacesService

Places API をプログラムから呼び出す。

### 場所の詳細を取得

```tsx
function getPlaceDetails(placeId: string): Promise<google.maps.places.PlaceResult | null> {
  return new Promise((resolve) => {
    const service = new google.maps.places.PlacesService(
      document.createElement('div')
    );

    service.getDetails(
      {
        placeId,
        fields: ['name', 'formatted_address', 'geometry', 'photos', 'rating'],
      },
      (result, status) => {
        if (status === google.maps.places.PlacesServiceStatus.OK && result) {
          resolve(result);
        } else {
          resolve(null);
        }
      }
    );
  });
}
```

### 近隣検索

```tsx
function searchNearby(
  location: google.maps.LatLngLiteral,
  radius: number,
  type: string
): Promise<google.maps.places.PlaceResult[]> {
  return new Promise((resolve) => {
    const service = new google.maps.places.PlacesService(
      document.createElement('div')
    );

    service.nearbySearch(
      {
        location,
        radius,
        type,
      },
      (results, status) => {
        if (status === google.maps.places.PlacesServiceStatus.OK && results) {
          resolve(results);
        } else {
          resolve([]);
        }
      }
    );
  });
}

// 使用例
const restaurants = await searchNearby(
  { lat: 35.6812, lng: 139.7671 },
  500,
  'restaurant'
);
```

### テキスト検索

```tsx
function textSearch(query: string): Promise<google.maps.places.PlaceResult[]> {
  return new Promise((resolve) => {
    const service = new google.maps.places.PlacesService(
      document.createElement('div')
    );

    service.textSearch(
      {
        query,
        location: { lat: 35.6812, lng: 139.7671 },
        radius: 5000,
      },
      (results, status) => {
        if (status === google.maps.places.PlacesServiceStatus.OK && results) {
          resolve(results);
        } else {
          resolve([]);
        }
      }
    );
  });
}

// 使用例
const results = await textSearch('東京駅 カフェ');
```

## セッショントークン

Autocomplete のリクエストをセッションとしてグループ化し、料金を最適化。

```tsx
import { useRef, useCallback } from 'react';

function PlaceAutocompleteWithSession() {
  const sessionToken = useRef<google.maps.places.AutocompleteSessionToken | null>(null);

  // セッショントークンを生成
  const getSessionToken = useCallback(() => {
    if (!sessionToken.current) {
      sessionToken.current = new google.maps.places.AutocompleteSessionToken();
    }
    return sessionToken.current;
  }, []);

  // セッションをリセット
  const resetSession = useCallback(() => {
    sessionToken.current = null;
  }, []);

  const onPlaceChanged = useCallback(() => {
    // 場所が選択されたらセッションをリセット
    resetSession();
  }, [resetSession]);

  // ...
}
```

## 写真の取得

```tsx
function getPlacePhotos(place: google.maps.places.PlaceResult, maxWidth: number = 400) {
  if (!place.photos || place.photos.length === 0) {
    return [];
  }

  return place.photos.map((photo) => ({
    url: photo.getUrl({ maxWidth }),
    width: photo.width,
    height: photo.height,
  }));
}

// 使用例
const photos = getPlacePhotos(place, 600);
```

## 住所コンポーネントの解析

```tsx
interface ParsedAddress {
  postalCode?: string;
  country?: string;
  prefecture?: string;
  city?: string;
  ward?: string;
  street?: string;
}

function parseAddressComponents(
  components: google.maps.GeocoderAddressComponent[] | undefined
): ParsedAddress {
  if (!components) return {};

  const findComponent = (type: string) =>
    components.find((c) => c.types.includes(type));

  return {
    postalCode: findComponent('postal_code')?.long_name,
    country: findComponent('country')?.long_name,
    prefecture: findComponent('administrative_area_level_1')?.long_name,
    city: findComponent('locality')?.long_name,
    ward: findComponent('sublocality_level_1')?.long_name,
    street: findComponent('route')?.long_name,
  };
}
```

## StandaloneSearchBox

複数の場所を検索できる検索ボックス。

```tsx
import { StandaloneSearchBox } from '@react-google-maps/api';

function SearchBox() {
  const [searchBox, setSearchBox] = useState<google.maps.places.SearchBox | null>(null);

  const onLoad = useCallback((ref: google.maps.places.SearchBox) => {
    setSearchBox(ref);
  }, []);

  const onPlacesChanged = useCallback(() => {
    if (searchBox) {
      const places = searchBox.getPlaces();
      console.log('Found places:', places);
    }
  }, [searchBox]);

  return (
    <StandaloneSearchBox onLoad={onLoad} onPlacesChanged={onPlacesChanged}>
      <input type="text" placeholder="検索..." className="w-full px-4 py-2 border rounded" />
    </StandaloneSearchBox>
  );
}
```

## エラーハンドリング

```tsx
const PlacesServiceStatus = google.maps.places.PlacesServiceStatus;

function handlePlacesError(status: google.maps.places.PlacesServiceStatus): string {
  switch (status) {
    case PlacesServiceStatus.OK:
      return '';
    case PlacesServiceStatus.ZERO_RESULTS:
      return '検索結果がありません';
    case PlacesServiceStatus.INVALID_REQUEST:
      return 'リクエストが無効です';
    case PlacesServiceStatus.OVER_QUERY_LIMIT:
      return 'API制限を超えました';
    case PlacesServiceStatus.REQUEST_DENIED:
      return 'リクエストが拒否されました';
    case PlacesServiceStatus.UNKNOWN_ERROR:
      return '不明なエラーが発生しました';
    default:
      return 'エラーが発生しました';
  }
}
```

## 料金最適化のヒント

1. **必要なフィールドのみを指定**
   ```tsx
   fields: ['place_id', 'geometry', 'name'] // Basic フィールドは無料
   ```

2. **セッショントークンを使用**
   - Autocomplete のリクエストをグループ化

3. **キャッシュを活用**
   - 同じ場所の詳細を何度も取得しない

4. **Autocomplete の代わりに Geocoding を検討**
   - 単純な住所検索なら Geocoding API の方が安い場合がある

## 関連リソース

- [Places API 公式ドキュメント](https://developers.google.com/maps/documentation/places/web-service)
- [Places Autocomplete コード例](../examples/places-autocomplete.tsx)
- [Geocoding API](geocoding-api.md)
