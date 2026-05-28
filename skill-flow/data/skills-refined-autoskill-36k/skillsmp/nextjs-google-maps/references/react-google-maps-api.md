# @react-google-maps/api リファレンス

## 概要

`@react-google-maps/api` は Google Maps JavaScript API の React ラッパーライブラリです。
TypeScript をフルサポートし、React の Hooks パターンに対応しています。

## インストール

```bash
npm install @react-google-maps/api
```

## 基本アーキテクチャ

```
useLoadScript / LoadScript
        ↓
   GoogleMap
        ↓
┌───────┴───────┐
Marker    InfoWindow    Polyline    Polygon    ...
```

## API ローディング

### useLoadScript Hook（推奨）

```tsx
import { useLoadScript, Libraries } from '@react-google-maps/api';

const libraries: Libraries = ['places', 'drawing', 'visualization'];

function App() {
  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY!,
    libraries,
  });

  if (loadError) return <div>Error loading maps</div>;
  if (!isLoaded) return <div>Loading...</div>;

  return <Map />;
}
```

### LoadScript コンポーネント

```tsx
import { LoadScript, GoogleMap } from '@react-google-maps/api';

function App() {
  return (
    <LoadScript
      googleMapsApiKey={process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY!}
      libraries={['places']}
    >
      <GoogleMap ... />
    </LoadScript>
  );
}
```

### 比較

| 特徴 | useLoadScript | LoadScript |
|------|--------------|------------|
| 使用場所 | 関数コンポーネント内 | JSX 内 |
| 柔軟性 | 高い | 中程度 |
| エラーハンドリング | 容易 | やや複雑 |
| SSR 対応 | `'use client'` が必要 | 同様 |

## コアコンポーネント

### GoogleMap

地図のコンテナコンポーネント。

```tsx
import { GoogleMap } from '@react-google-maps/api';

<GoogleMap
  mapContainerStyle={{ width: '100%', height: '400px' }}
  center={{ lat: 35.6812, lng: 139.7671 }}
  zoom={15}
  options={{
    disableDefaultUI: false,
    zoomControl: true,
    mapTypeControl: false,
  }}
  onLoad={(map) => console.log('Map loaded', map)}
  onUnmount={() => console.log('Map unmounted')}
  onClick={(e) => console.log('Clicked', e.latLng)}
/>
```

**主な Props:**

| Prop | 型 | 説明 |
|------|-----|------|
| `mapContainerStyle` | `CSSProperties` | コンテナのスタイル |
| `mapContainerClassName` | `string` | コンテナの CSS クラス |
| `center` | `LatLngLiteral` | 地図の中心座標 |
| `zoom` | `number` | ズームレベル（0-21） |
| `options` | `MapOptions` | 地図オプション |
| `onLoad` | `(map: Map) => void` | 読み込み完了時のコールバック |
| `onUnmount` | `() => void` | アンマウント時のコールバック |
| `onClick` | `(e: MapMouseEvent) => void` | クリック時のコールバック |

### Marker

地図上にマーカーを表示。

```tsx
import { Marker } from '@react-google-maps/api';

<Marker
  position={{ lat: 35.6812, lng: 139.7671 }}
  title="東京駅"
  label="A"
  icon={{
    url: '/custom-marker.png',
    scaledSize: new google.maps.Size(40, 40),
  }}
  onClick={() => console.log('Marker clicked')}
  draggable={false}
  animation={google.maps.Animation.DROP}
/>
```

**主な Props:**

| Prop | 型 | 説明 |
|------|-----|------|
| `position` | `LatLngLiteral` | マーカーの位置 |
| `title` | `string` | ホバー時のタイトル |
| `label` | `string \| MarkerLabel` | マーカー上のラベル |
| `icon` | `string \| Icon` | カスタムアイコン |
| `draggable` | `boolean` | ドラッグ可能か |
| `animation` | `Animation` | アニメーション |
| `onClick` | `() => void` | クリック時のコールバック |

### InfoWindow

情報ウィンドウを表示。

```tsx
import { InfoWindow } from '@react-google-maps/api';

<InfoWindow
  position={{ lat: 35.6812, lng: 139.7671 }}
  onCloseClick={() => setIsOpen(false)}
  options={{
    maxWidth: 300,
    pixelOffset: new google.maps.Size(0, -30),
  }}
>
  <div className="p-2">
    <h3 className="font-bold">東京駅</h3>
    <p>日本最大のターミナル駅</p>
  </div>
</InfoWindow>
```

**主な Props:**

| Prop | 型 | 説明 |
|------|-----|------|
| `position` | `LatLngLiteral` | 表示位置 |
| `anchor` | `MVCObject` | アンカー要素（Marker など） |
| `onCloseClick` | `() => void` | 閉じるボタンクリック時 |
| `options` | `InfoWindowOptions` | オプション |

### Polyline

線を描画。

```tsx
import { Polyline } from '@react-google-maps/api';

const path = [
  { lat: 35.6812, lng: 139.7671 },
  { lat: 35.6586, lng: 139.7454 },
  { lat: 35.7100, lng: 139.8107 },
];

<Polyline
  path={path}
  options={{
    strokeColor: '#FF0000',
    strokeOpacity: 0.8,
    strokeWeight: 3,
  }}
/>
```

### Polygon

多角形を描画。

```tsx
import { Polygon } from '@react-google-maps/api';

const paths = [
  { lat: 35.6812, lng: 139.7671 },
  { lat: 35.6586, lng: 139.7454 },
  { lat: 35.6900, lng: 139.7000 },
];

<Polygon
  paths={paths}
  options={{
    fillColor: '#0000FF',
    fillOpacity: 0.3,
    strokeColor: '#0000FF',
    strokeWeight: 2,
  }}
/>
```

### Circle

円を描画。

```tsx
import { Circle } from '@react-google-maps/api';

<Circle
  center={{ lat: 35.6812, lng: 139.7671 }}
  radius={1000} // メートル
  options={{
    fillColor: '#FF0000',
    fillOpacity: 0.2,
    strokeColor: '#FF0000',
    strokeWeight: 1,
  }}
/>
```

## Places API コンポーネント

### Autocomplete

場所検索のオートコンプリート。

```tsx
import { Autocomplete } from '@react-google-maps/api';

const [autocomplete, setAutocomplete] = useState<google.maps.places.Autocomplete | null>(null);

<Autocomplete
  onLoad={(ac) => setAutocomplete(ac)}
  onPlaceChanged={() => {
    if (autocomplete) {
      const place = autocomplete.getPlace();
      console.log(place);
    }
  }}
  options={{
    types: ['establishment'],
    componentRestrictions: { country: 'jp' },
    fields: ['place_id', 'geometry', 'name', 'formatted_address'],
  }}
>
  <input type="text" placeholder="場所を検索..." />
</Autocomplete>
```

### StandaloneSearchBox

独立した検索ボックス。

```tsx
import { StandaloneSearchBox } from '@react-google-maps/api';

<StandaloneSearchBox
  onLoad={(ref) => setSearchBox(ref)}
  onPlacesChanged={() => {
    const places = searchBox?.getPlaces();
    console.log(places);
  }}
>
  <input type="text" placeholder="検索..." />
</StandaloneSearchBox>
```

## Directions API コンポーネント

### DirectionsService

ルート計算を実行。

```tsx
import { DirectionsService } from '@react-google-maps/api';

<DirectionsService
  options={{
    origin: { lat: 35.6812, lng: 139.7671 },
    destination: { lat: 35.6586, lng: 139.7454 },
    travelMode: google.maps.TravelMode.DRIVING,
    waypoints: [
      { location: '渋谷駅', stopover: true },
    ],
  }}
  callback={(result, status) => {
    if (status === 'OK') {
      setDirections(result);
    }
  }}
/>
```

### DirectionsRenderer

計算されたルートを表示。

```tsx
import { DirectionsRenderer } from '@react-google-maps/api';

<DirectionsRenderer
  directions={directions}
  options={{
    polylineOptions: {
      strokeColor: '#0066FF',
      strokeWeight: 4,
    },
    suppressMarkers: false,
  }}
/>
```

## 可視化コンポーネント

### HeatmapLayer

ヒートマップを表示。

```tsx
import { HeatmapLayer } from '@react-google-maps/api';

const data = [
  new google.maps.LatLng(35.6812, 139.7671),
  new google.maps.LatLng(35.6586, 139.7454),
];

<HeatmapLayer
  data={data}
  options={{
    radius: 20,
    opacity: 0.7,
    gradient: [
      'rgba(0, 255, 255, 0)',
      'rgba(0, 255, 255, 1)',
      'rgba(0, 191, 255, 1)',
      'rgba(0, 127, 255, 1)',
      'rgba(0, 63, 255, 1)',
      'rgba(0, 0, 255, 1)',
    ],
  }}
/>
```

### MarkerClusterer

マーカーのクラスタリング。

```tsx
import { MarkerClusterer } from '@react-google-maps/api';

<MarkerClusterer
  options={{
    imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m',
    gridSize: 60,
    maxZoom: 15,
  }}
>
  {(clusterer) =>
    locations.map((loc) => (
      <Marker key={loc.id} position={loc.position} clusterer={clusterer} />
    ))
  }
</MarkerClusterer>
```

## ストリートビューコンポーネント

### StreetViewPanorama

ストリートビューを表示。

```tsx
import { StreetViewPanorama } from '@react-google-maps/api';

<StreetViewPanorama
  position={{ lat: 35.6812, lng: 139.7671 }}
  visible={true}
  options={{
    pov: { heading: 100, pitch: 0 },
    zoom: 1,
    addressControl: true,
    fullscreenControl: true,
  }}
  onPovChanged={() => console.log('POV changed')}
/>
```

## 描画コンポーネント

### DrawingManager

図形描画ツール。

```tsx
import { DrawingManager } from '@react-google-maps/api';

<DrawingManager
  drawingMode={google.maps.drawing.OverlayType.POLYGON}
  options={{
    drawingControl: true,
    drawingControlOptions: {
      position: google.maps.ControlPosition.TOP_CENTER,
      drawingModes: [
        google.maps.drawing.OverlayType.POLYGON,
        google.maps.drawing.OverlayType.POLYLINE,
        google.maps.drawing.OverlayType.CIRCLE,
        google.maps.drawing.OverlayType.RECTANGLE,
      ],
    },
    polygonOptions: {
      fillColor: '#FF0000',
      fillOpacity: 0.3,
      strokeWeight: 2,
      editable: true,
    },
  }}
  onPolygonComplete={(polygon) => console.log('Polygon complete', polygon)}
  onCircleComplete={(circle) => console.log('Circle complete', circle)}
/>
```

## Hooks

### useGoogleMap

現在の Map インスタンスを取得。

```tsx
import { useGoogleMap } from '@react-google-maps/api';

function MapControls() {
  const map = useGoogleMap();

  const panTo = (position: google.maps.LatLngLiteral) => {
    map?.panTo(position);
  };

  return <button onClick={() => panTo({ lat: 35.6812, lng: 139.7671 })}>東京へ移動</button>;
}
```

## TypeScript 型定義

### よく使う型

```tsx
import type {
  GoogleMap,
  Marker,
  Libraries,
} from '@react-google-maps/api';

// 座標
type LatLngLiteral = google.maps.LatLngLiteral;

// マップオプション
type MapOptions = google.maps.MapOptions;

// マーカーオプション
type MarkerOptions = google.maps.MarkerOptions;

// ライブラリ
type Libraries = ('places' | 'drawing' | 'visualization' | 'geometry')[];
```

### カスタム型定義

```tsx
// types/google-maps.d.ts
declare global {
  interface Window {
    google: typeof google;
  }
}

export interface MapLocation {
  id: string;
  position: google.maps.LatLngLiteral;
  title: string;
  description?: string;
}
```

## パフォーマンス Tips

1. **libraries は定数として定義**
   ```tsx
   // コンポーネント外で定義
   const libraries: Libraries = ['places'];
   ```

2. **onLoad で map を ref に保存**
   ```tsx
   const mapRef = useRef<google.maps.Map | null>(null);
   const onLoad = useCallback((map: google.maps.Map) => {
     mapRef.current = map;
   }, []);
   ```

3. **Marker の key を安定させる**
   ```tsx
   // ID を使用
   <Marker key={location.id} ... />
   ```

## 他ライブラリとの比較

| ライブラリ | 特徴 |
|-----------|------|
| `@react-google-maps/api` | 最も人気、メンテナンスが活発 |
| `@vis.gl/react-google-maps` | Google 公式、新しい |
| `google-map-react` | 軽量、シンプル |

## 関連リソース

- [GitHub リポジトリ](https://github.com/JustFly1984/react-google-maps-api)
- [公式ドキュメント](https://react-google-maps-api-docs.netlify.app/)
- [API 概要](api-overview.md)
