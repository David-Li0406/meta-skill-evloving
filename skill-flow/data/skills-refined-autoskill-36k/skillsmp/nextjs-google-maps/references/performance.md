# パフォーマンス最適化 リファレンス

## 概要

Google Maps を使用するアプリケーションのパフォーマンスを最適化するための
テクニックとベストプラクティス。

## バンドルサイズの最適化

### Dynamic Import

Next.js の Dynamic Import を使用して、地図コンポーネントを遅延読み込み:

```tsx
import dynamic from 'next/dynamic';

const Map = dynamic(
  () => import('@/components/map').then((mod) => mod.Map),
  {
    ssr: false,
    loading: () => (
      <div className="h-[400px] bg-gray-100 animate-pulse flex items-center justify-center">
        <span className="text-gray-400">地図を読み込み中...</span>
      </div>
    ),
  }
);

export default function MapPage() {
  return <Map />;
}
```

### 必要なライブラリのみ読み込む

```tsx
// 悪い例：すべてのライブラリを読み込む
const libraries: Libraries = ['places', 'drawing', 'visualization', 'geometry'];

// 良い例：必要なものだけを読み込む
const libraries: Libraries = ['places']; // Places API のみ使用する場合
```

## コンポーネントの最適化

### ライブラリの定数化

ライブラリ配列をコンポーネント外で定義して、再レンダリングを防止:

```tsx
// コンポーネント外で定義
const libraries: Libraries = ['places'];

function MapComponent() {
  // コンポーネント内で定義すると、毎回新しい配列が作成される
  const { isLoaded } = useLoadScript({
    googleMapsApiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY!,
    libraries, // 外部で定義した配列を参照
  });
  // ...
}
```

### Map インスタンスの保持

```tsx
function OptimizedMap() {
  const mapRef = useRef<google.maps.Map | null>(null);

  const onLoad = useCallback((map: google.maps.Map) => {
    // ref に保存して再利用
    mapRef.current = map;
  }, []);

  const onUnmount = useCallback(() => {
    mapRef.current = null;
  }, []);

  return (
    <GoogleMap
      onLoad={onLoad}
      onUnmount={onUnmount}
      // ... other props
    />
  );
}
```

### コールバックのメモ化

```tsx
function MapWithMarkers({ markers }: { markers: Marker[] }) {
  // useCallback でメモ化
  const handleMarkerClick = useCallback((markerId: string) => {
    console.log('Clicked:', markerId);
  }, []);

  // useMemo で値をメモ化
  const center = useMemo(() => {
    if (markers.length === 0) return { lat: 35.6812, lng: 139.7671 };
    return markers[0].position;
  }, [markers]);

  return (
    <GoogleMap center={center}>
      {markers.map((marker) => (
        <Marker
          key={marker.id}
          position={marker.position}
          onClick={() => handleMarkerClick(marker.id)}
        />
      ))}
    </GoogleMap>
  );
}
```

## マーカーの最適化

### マーカークラスタリング

大量のマーカーがある場合は、クラスタリングを使用:

```tsx
import { MarkerClusterer } from '@react-google-maps/api';

function ClusteredMarkers({ locations }: { locations: Location[] }) {
  return (
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
  );
}
```

### ビューポート内のマーカーのみ表示

```tsx
function ViewportOptimizedMap({ allMarkers }: { allMarkers: Marker[] }) {
  const [visibleMarkers, setVisibleMarkers] = useState<Marker[]>([]);
  const mapRef = useRef<google.maps.Map | null>(null);

  const updateVisibleMarkers = useCallback(() => {
    if (!mapRef.current) return;

    const bounds = mapRef.current.getBounds();
    if (!bounds) return;

    // ビューポート内のマーカーのみをフィルタリング
    const visible = allMarkers.filter((marker) =>
      bounds.contains(marker.position)
    );
    setVisibleMarkers(visible);
  }, [allMarkers]);

  const onBoundsChanged = useDebouncedCallback(updateVisibleMarkers, 100);

  return (
    <GoogleMap
      onLoad={(map) => {
        mapRef.current = map;
        updateVisibleMarkers();
      }}
      onBoundsChanged={onBoundsChanged}
    >
      {visibleMarkers.map((marker) => (
        <Marker key={marker.id} position={marker.position} />
      ))}
    </GoogleMap>
  );
}
```

### マーカーのキーを安定させる

```tsx
// 悪い例：インデックスをキーに使用
{markers.map((marker, index) => (
  <Marker key={index} position={marker.position} />
))}

// 良い例：一意の ID をキーに使用
{markers.map((marker) => (
  <Marker key={marker.id} position={marker.position} />
))}
```

## イベントハンドリングの最適化

### デバウンス

```tsx
import { useDebouncedCallback } from 'use-debounce';

function MapWithSearch() {
  const [bounds, setBounds] = useState<google.maps.LatLngBounds | null>(null);

  // 100ms のデバウンス
  const handleBoundsChanged = useDebouncedCallback(() => {
    if (mapRef.current) {
      setBounds(mapRef.current.getBounds() || null);
    }
  }, 100);

  return (
    <GoogleMap onBoundsChanged={handleBoundsChanged}>
      {/* ... */}
    </GoogleMap>
  );
}
```

### スロットリング

```tsx
import { useThrottledCallback } from 'use-debounce';

function MapWithTracking() {
  // 1秒に1回まで
  const handleDrag = useThrottledCallback((e: google.maps.MapMouseEvent) => {
    console.log('Dragging:', e.latLng?.toJSON());
  }, 1000);

  return <GoogleMap onDrag={handleDrag} />;
}
```

## メモリ管理

### 図形の適切な削除

```tsx
function ShapeManager() {
  const shapesRef = useRef<google.maps.Polygon[]>([]);

  const addShape = (polygon: google.maps.Polygon) => {
    shapesRef.current.push(polygon);
  };

  const removeShape = (index: number) => {
    const shape = shapesRef.current[index];
    shape.setMap(null); // 地図から削除
    google.maps.event.clearInstanceListeners(shape); // リスナーを削除
    shapesRef.current.splice(index, 1);
  };

  const clearAllShapes = () => {
    shapesRef.current.forEach((shape) => {
      shape.setMap(null);
      google.maps.event.clearInstanceListeners(shape);
    });
    shapesRef.current = [];
  };

  // クリーンアップ
  useEffect(() => {
    return () => {
      clearAllShapes();
    };
  }, []);

  // ...
}
```

### イベントリスナーのクリーンアップ

```tsx
useEffect(() => {
  if (!map) return;

  const listener = map.addListener('click', handleClick);

  return () => {
    google.maps.event.removeListener(listener);
  };
}, [map, handleClick]);
```

## データ読み込みの最適化

### API リクエストのキャッシュ

```tsx
class GeocodingCache {
  private cache = new Map<string, google.maps.LatLngLiteral>();
  private maxSize: number;

  constructor(maxSize = 100) {
    this.maxSize = maxSize;
  }

  async geocode(address: string): Promise<google.maps.LatLngLiteral | null> {
    // キャッシュを確認
    if (this.cache.has(address)) {
      return this.cache.get(address)!;
    }

    // API を呼び出し
    const result = await geocodeAddress(address);

    if (result) {
      // キャッシュサイズを管理
      if (this.cache.size >= this.maxSize) {
        const firstKey = this.cache.keys().next().value;
        this.cache.delete(firstKey);
      }
      this.cache.set(address, result);
    }

    return result;
  }
}
```

### バッチリクエスト

```tsx
async function batchGeocode(addresses: string[]): Promise<Map<string, google.maps.LatLngLiteral>> {
  const results = new Map<string, google.maps.LatLngLiteral>();

  // 並列処理（レート制限に注意）
  const batchSize = 10;
  for (let i = 0; i < addresses.length; i += batchSize) {
    const batch = addresses.slice(i, i + batchSize);
    const promises = batch.map((address) => geocodeAddress(address));

    const batchResults = await Promise.all(promises);

    batch.forEach((address, index) => {
      if (batchResults[index]) {
        results.set(address, batchResults[index]!);
      }
    });

    // レート制限対策
    if (i + batchSize < addresses.length) {
      await new Promise((resolve) => setTimeout(resolve, 200));
    }
  }

  return results;
}
```

## レンダリングの最適化

### React.memo の使用

```tsx
const MarkerComponent = React.memo(function MarkerComponent({
  position,
  onClick,
}: {
  position: google.maps.LatLngLiteral;
  onClick: () => void;
}) {
  return <Marker position={position} onClick={onClick} />;
});
```

### 仮想化（大量のリスト）

```tsx
import { FixedSizeList as List } from 'react-window';

function VirtualizedMarkerList({ markers }: { markers: Marker[] }) {
  return (
    <List
      height={400}
      itemCount={markers.length}
      itemSize={50}
      width="100%"
    >
      {({ index, style }) => (
        <div style={style}>
          {markers[index].title}
        </div>
      )}
    </List>
  );
}
```

## パフォーマンス計測

### 読み込み時間の計測

```tsx
function PerformanceTrackedMap() {
  const startTime = useRef(Date.now());

  const onLoad = useCallback(() => {
    const loadTime = Date.now() - startTime.current;
    console.log(`Map loaded in ${loadTime}ms`);

    // アナリティクスに送信
    // analytics.track('map_load_time', { duration: loadTime });
  }, []);

  return <GoogleMap onLoad={onLoad} />;
}
```

### React DevTools Profiler

1. React DevTools を開く
2. Profiler タブを選択
3. 記録を開始
4. 地図を操作
5. 記録を停止して結果を分析

## チェックリスト

- [ ] Dynamic Import を使用している
- [ ] 必要なライブラリのみを読み込んでいる
- [ ] ライブラリ配列がコンポーネント外で定義されている
- [ ] コールバックがメモ化されている
- [ ] 大量のマーカーにはクラスタリングを使用している
- [ ] イベントがデバウンス/スロットリングされている
- [ ] 図形のクリーンアップが適切に行われている
- [ ] API リクエストがキャッシュされている
- [ ] マーカーのキーが安定している

## 関連リソース

- [React Performance](https://react.dev/learn/render-and-commit)
- [Next.js Dynamic Imports](https://nextjs.org/docs/pages/building-your-application/optimizing/lazy-loading)
- [マーカークラスタリング](../examples/marker-clusterer.tsx)
