---
name: nextjs-google-maps
description: |
  This skill should be used when the user asks to "add Google Maps",
  "integrate maps", "show location on map", "implement place search",
  "add route calculation", "geocode address", "display markers",
  "create heatmap", "add Street View", "implement drawing tools",
  "Google Maps を追加", "地図を表示", "位置情報を表示",
  "場所検索を実装", "ルート計算", "住所から座標を取得",
  "マーカーを表示", "ヒートマップを作成", "ストリートビュー",
  "描画ツールを追加", "@react-google-maps/api の使い方",
  or needs guidance on Google Maps Platform integration with Next.js
  App Router, including Places API, Directions API, Geocoding API,
  visualization features, and performance optimization.
version: 1.0.0
---

# Next.js Google Maps Integration

Next.js App Router で `@react-google-maps/api` を使用した Google Maps 統合ガイド。

## 対象スタック

- Next.js 14+ (App Router)
- React 18+
- TypeScript
- `@react-google-maps/api` v2.x

## クイックスタート チェックリスト

1. [ ] Google Cloud Platform でプロジェクトを作成
2. [ ] 必要な API を有効化（Maps JavaScript API, Places API, Directions API, Geocoding API）
3. [ ] API キーを作成し、リファラー制限を設定
4. [ ] `npm install @react-google-maps/api` でライブラリをインストール
5. [ ] `.env.local` に `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY` を設定
6. [ ] Provider コンポーネントを作成
7. [ ] Map コンポーネントを実装

## インストール

```bash
npm install @react-google-maps/api
# または
yarn add @react-google-maps/api
# または
pnpm add @react-google-maps/api
```

## 環境変数の設定

`.env.local` ファイルを作成:

```
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_api_key_here
```

> **注意**: `NEXT_PUBLIC_` プレフィックスが必要です。これによりクライアントサイドで使用可能になります。

## Google Cloud Platform セットアップ

### 1. プロジェクト作成

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. 新しいプロジェクトを作成
3. 請求先アカウントをリンク（無料枠あり）

### 2. API の有効化

必要に応じて以下の API を有効化:

| API | 用途 |
|-----|------|
| Maps JavaScript API | 地図の表示（必須） |
| Places API | 場所検索・オートコンプリート |
| Directions API | ルート計算 |
| Geocoding API | 住所⇔座標変換 |

### 3. API キーの作成と制限

1. 「認証情報」→「認証情報を作成」→「API キー」
2. アプリケーションの制限:
   - 種類: HTTP リファラー
   - 許可するリファラー: `localhost:*`, `your-domain.com/*`
3. API の制限: 使用する API のみに制限

## コアコンポーネント

### Provider パターン（SSR 対応）

```tsx
// components/google-maps-provider.tsx
'use client';

import { Libraries, useLoadScript } from '@react-google-maps/api';
import { createContext, useContext, ReactNode } from 'react';

const libraries: Libraries = ['places', 'drawing', 'visualization'];

interface GoogleMapsContextType {
  isLoaded: boolean;
}

const GoogleMapsContext = createContext<GoogleMapsContextType>({ isLoaded: false });

export function GoogleMapsProvider({ children }: { children: ReactNode }) {
  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY!,
    libraries,
  });

  if (loadError) {
    return <div className="p-4 text-red-500">Google Maps の読み込みに失敗しました</div>;
  }

  if (!isLoaded) {
    return <div className="p-4">地図を読み込み中...</div>;
  }

  return (
    <GoogleMapsContext.Provider value={{ isLoaded }}>
      {children}
    </GoogleMapsContext.Provider>
  );
}

export function useGoogleMapsContext() {
  return useContext(GoogleMapsContext);
}
```

詳細: [examples/google-maps-provider.tsx](examples/google-maps-provider.tsx)

### 基本的な Map コンポーネント

```tsx
// components/map.tsx
'use client';

import { GoogleMap } from '@react-google-maps/api';
import { useCallback, useState } from 'react';

const containerStyle = {
  width: '100%',
  height: '400px',
};

const defaultCenter = {
  lat: 35.6812,
  lng: 139.7671,
};

export function Map() {
  const [map, setMap] = useState<google.maps.Map | null>(null);

  const onLoad = useCallback((map: google.maps.Map) => {
    setMap(map);
  }, []);

  const onUnmount = useCallback(() => {
    setMap(null);
  }, []);

  return (
    <GoogleMap
      mapContainerStyle={containerStyle}
      center={defaultCenter}
      zoom={15}
      onLoad={onLoad}
      onUnmount={onUnmount}
    />
  );
}
```

詳細: [examples/basic-map.tsx](examples/basic-map.tsx)

### Layout での統合

```tsx
// app/map/layout.tsx
import { GoogleMapsProvider } from '@/components/google-maps-provider';

export default function MapLayout({ children }: { children: React.ReactNode }) {
  return (
    <GoogleMapsProvider>
      {children}
    </GoogleMapsProvider>
  );
}
```

## マーカーと InfoWindow

```tsx
import { GoogleMap, Marker, InfoWindow } from '@react-google-maps/api';
import { useState } from 'react';

interface Location {
  id: string;
  position: google.maps.LatLngLiteral;
  title: string;
}

const locations: Location[] = [
  { id: '1', position: { lat: 35.6812, lng: 139.7671 }, title: '東京駅' },
  { id: '2', position: { lat: 35.6586, lng: 139.7454 }, title: '東京タワー' },
];

export function MapWithMarkers() {
  const [selectedId, setSelectedId] = useState<string | null>(null);

  return (
    <GoogleMap mapContainerStyle={containerStyle} center={locations[0].position} zoom={13}>
      {locations.map((location) => (
        <Marker
          key={location.id}
          position={location.position}
          onClick={() => setSelectedId(location.id)}
        >
          {selectedId === location.id && (
            <InfoWindow onCloseClick={() => setSelectedId(null)}>
              <div className="p-2">{location.title}</div>
            </InfoWindow>
          )}
        </Marker>
      ))}
    </GoogleMap>
  );
}
```

詳細: [examples/map-with-markers.tsx](examples/map-with-markers.tsx)

## Places API（場所検索）

### オートコンプリート

```tsx
import { Autocomplete } from '@react-google-maps/api';
import { useCallback, useState } from 'react';

export function PlaceAutocomplete({
  onPlaceSelect
}: {
  onPlaceSelect: (place: google.maps.places.PlaceResult) => void
}) {
  const [autocomplete, setAutocomplete] = useState<google.maps.places.Autocomplete | null>(null);

  const onLoad = useCallback((ac: google.maps.places.Autocomplete) => {
    setAutocomplete(ac);
  }, []);

  const onPlaceChanged = useCallback(() => {
    if (autocomplete) {
      const place = autocomplete.getPlace();
      if (place.geometry?.location) {
        onPlaceSelect(place);
      }
    }
  }, [autocomplete, onPlaceSelect]);

  return (
    <Autocomplete
      onLoad={onLoad}
      onPlaceChanged={onPlaceChanged}
      options={{
        componentRestrictions: { country: 'jp' },
        types: ['establishment'],
      }}
    >
      <input
        type="text"
        placeholder="場所を検索..."
        className="w-full px-4 py-2 border rounded-lg"
      />
    </Autocomplete>
  );
}
```

詳細: [examples/places-autocomplete.tsx](examples/places-autocomplete.tsx), [references/places-api.md](references/places-api.md)

## Directions API（ルート計算）

```tsx
import { DirectionsRenderer, DirectionsService } from '@react-google-maps/api';
import { useCallback, useState } from 'react';

export function DirectionsMap({
  origin,
  destination,
}: {
  origin: google.maps.LatLngLiteral;
  destination: google.maps.LatLngLiteral;
}) {
  const [directions, setDirections] = useState<google.maps.DirectionsResult | null>(null);

  const directionsCallback = useCallback(
    (result: google.maps.DirectionsResult | null, status: google.maps.DirectionsStatus) => {
      if (status === 'OK' && result) {
        setDirections(result);
      }
    },
    []
  );

  return (
    <GoogleMap mapContainerStyle={containerStyle} center={origin} zoom={12}>
      {!directions && (
        <DirectionsService
          options={{
            origin,
            destination,
            travelMode: google.maps.TravelMode.DRIVING,
          }}
          callback={directionsCallback}
        />
      )}
      {directions && <DirectionsRenderer directions={directions} />}
    </GoogleMap>
  );
}
```

詳細: [examples/directions-route.tsx](examples/directions-route.tsx), [references/directions-api.md](references/directions-api.md)

## ジオコーディング

```tsx
// utils/geocoding.ts
export async function geocodeAddress(address: string): Promise<google.maps.LatLngLiteral | null> {
  const geocoder = new google.maps.Geocoder();

  return new Promise((resolve) => {
    geocoder.geocode({ address }, (results, status) => {
      if (status === 'OK' && results?.[0]) {
        const location = results[0].geometry.location;
        resolve({ lat: location.lat(), lng: location.lng() });
      } else {
        resolve(null);
      }
    });
  });
}

export async function reverseGeocode(
  location: google.maps.LatLngLiteral
): Promise<string | null> {
  const geocoder = new google.maps.Geocoder();

  return new Promise((resolve) => {
    geocoder.geocode({ location }, (results, status) => {
      if (status === 'OK' && results?.[0]) {
        resolve(results[0].formatted_address);
      } else {
        resolve(null);
      }
    });
  });
}
```

詳細: [examples/geocoding-service.ts](examples/geocoding-service.ts), [references/geocoding-api.md](references/geocoding-api.md)

## 高度な可視化

### ヒートマップ

```tsx
import { HeatmapLayer } from '@react-google-maps/api';

const heatmapData = [
  new google.maps.LatLng(35.6812, 139.7671),
  new google.maps.LatLng(35.6586, 139.7454),
  // ... more points
];

export function HeatmapMap() {
  return (
    <GoogleMap mapContainerStyle={containerStyle} center={defaultCenter} zoom={12}>
      <HeatmapLayer
        data={heatmapData}
        options={{
          radius: 20,
          opacity: 0.7,
        }}
      />
    </GoogleMap>
  );
}
```

詳細: [examples/heatmap-layer.tsx](examples/heatmap-layer.tsx), [references/visualization.md](references/visualization.md)

### マーカークラスタリング

```tsx
import { MarkerClusterer } from '@react-google-maps/api';

export function ClusteredMap({ locations }: { locations: Location[] }) {
  return (
    <GoogleMap mapContainerStyle={containerStyle} center={defaultCenter} zoom={10}>
      <MarkerClusterer>
        {(clusterer) =>
          locations.map((location) => (
            <Marker
              key={location.id}
              position={location.position}
              clusterer={clusterer}
            />
          ))
        }
      </MarkerClusterer>
    </GoogleMap>
  );
}
```

詳細: [examples/marker-clusterer.tsx](examples/marker-clusterer.tsx)

## ストリートビュー

```tsx
import { StreetViewPanorama } from '@react-google-maps/api';

export function StreetViewMap({ position }: { position: google.maps.LatLngLiteral }) {
  return (
    <GoogleMap mapContainerStyle={containerStyle} center={position} zoom={15}>
      <StreetViewPanorama
        position={position}
        visible={true}
        options={{
          addressControl: true,
          fullscreenControl: true,
        }}
      />
    </GoogleMap>
  );
}
```

詳細: [examples/street-view.tsx](examples/street-view.tsx), [references/streetview.md](references/streetview.md)

## 描画ツール

```tsx
import { DrawingManager } from '@react-google-maps/api';

export function DrawingMap() {
  const onPolygonComplete = (polygon: google.maps.Polygon) => {
    const path = polygon.getPath();
    const coordinates = path.getArray().map((latLng) => ({
      lat: latLng.lat(),
      lng: latLng.lng(),
    }));
    console.log('Polygon coordinates:', coordinates);
  };

  return (
    <GoogleMap mapContainerStyle={containerStyle} center={defaultCenter} zoom={15}>
      <DrawingManager
        drawingMode={google.maps.drawing.OverlayType.POLYGON}
        onPolygonComplete={onPolygonComplete}
        options={{
          drawingControl: true,
          drawingControlOptions: {
            position: google.maps.ControlPosition.TOP_CENTER,
            drawingModes: [
              google.maps.drawing.OverlayType.POLYGON,
              google.maps.drawing.OverlayType.POLYLINE,
              google.maps.drawing.OverlayType.CIRCLE,
            ],
          },
        }}
      />
    </GoogleMap>
  );
}
```

詳細: [examples/drawing-manager.tsx](examples/drawing-manager.tsx), [references/drawing-tools.md](references/drawing-tools.md)

## パフォーマンス最適化

### Dynamic Import（SSR 無効化）

```tsx
import dynamic from 'next/dynamic';

const MapComponent = dynamic(
  () => import('@/components/map').then((mod) => mod.Map),
  {
    ssr: false,
    loading: () => <div className="h-[400px] bg-gray-100 animate-pulse" />
  }
);
```

### Map インスタンスの再利用

```tsx
// Map インスタンスを ref で保持し、再レンダリング時の再生成を防ぐ
const mapRef = useRef<google.maps.Map | null>(null);

const onLoad = useCallback((map: google.maps.Map) => {
  mapRef.current = map;
}, []);
```

詳細: [references/performance.md](references/performance.md)

## エラーハンドリング

```tsx
export function handleGoogleMapsError(error: unknown): string {
  if (error instanceof Error) {
    const message = error.message;

    if (message.includes('RefererNotAllowedMapError')) {
      return 'API キーのリファラー制限を確認してください';
    }
    if (message.includes('InvalidKeyMapError')) {
      return 'API キーが無効です';
    }
    if (message.includes('ApiNotActivatedMapError')) {
      return '必要な API が有効化されていません';
    }
    if (message.includes('OverQueryLimitMapError')) {
      return 'API 呼び出し制限を超えました';
    }
  }

  return '不明なエラーが発生しました';
}
```

詳細: [references/troubleshooting.md](references/troubleshooting.md)

## TypeScript 型定義

```tsx
// types/google-maps.ts

export interface MapLocation {
  id: string;
  position: google.maps.LatLngLiteral;
  title: string;
  description?: string;
  icon?: string;
}

export interface DirectionsRequest {
  origin: google.maps.LatLngLiteral | string;
  destination: google.maps.LatLngLiteral | string;
  travelMode: google.maps.TravelMode;
  waypoints?: google.maps.DirectionsWaypoint[];
}

export interface GeocodingResult {
  address: string;
  location: google.maps.LatLngLiteral;
  placeId: string;
  formattedAddress: string;
}
```

## クイックリファレンス

| コンポーネント | 用途 |
|---------------|------|
| `GoogleMap` | 地図の表示 |
| `Marker` | マーカーの表示 |
| `InfoWindow` | 情報ウィンドウ |
| `Autocomplete` | 場所検索 |
| `DirectionsService` | ルート計算 |
| `DirectionsRenderer` | ルート表示 |
| `HeatmapLayer` | ヒートマップ |
| `MarkerClusterer` | マーカークラスタリング |
| `StreetViewPanorama` | ストリートビュー |
| `DrawingManager` | 描画ツール |

## 追加リソース

### リファレンス
- [API 概要](references/api-overview.md)
- [@react-google-maps/api リファレンス](references/react-google-maps-api.md)
- [Places API](references/places-api.md)
- [Directions API](references/directions-api.md)
- [Geocoding API](references/geocoding-api.md)
- [可視化（ヒートマップ・クラスタリング）](references/visualization.md)
- [ストリートビュー](references/streetview.md)
- [描画ツール](references/drawing-tools.md)
- [パフォーマンス最適化](references/performance.md)
- [トラブルシューティング](references/troubleshooting.md)

### コード例
- [Google Maps Provider](examples/google-maps-provider.tsx)
- [基本 Map](examples/basic-map.tsx)
- [マーカー付き Map](examples/map-with-markers.tsx)
- [場所検索オートコンプリート](examples/places-autocomplete.tsx)
- [ルート表示](examples/directions-route.tsx)
- [ジオコーディング](examples/geocoding-service.ts)
- [ヒートマップ](examples/heatmap-layer.tsx)
- [マーカークラスタリング](examples/marker-clusterer.tsx)
- [ストリートビュー](examples/street-view.tsx)
- [描画ツール](examples/drawing-manager.tsx)
- [カスタムフック](examples/map-hooks.ts)
