# 可視化（ヒートマップ・クラスタリング）リファレンス

## 概要

Google Maps の可視化機能を使用して、大量のデータポイントを効果的に表示します。

- **ヒートマップ**: データの密度を色で表現
- **マーカークラスタリング**: 近接するマーカーをグループ化

## 必要なライブラリ

```tsx
const libraries: Libraries = ['visualization'];

const { isLoaded } = useLoadScript({
  googleMapsApiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY!,
  libraries,
});
```

## ヒートマップ（HeatmapLayer）

### 基本的な使用法

```tsx
import { HeatmapLayer } from '@react-google-maps/api';

const heatmapData = [
  new google.maps.LatLng(35.6812, 139.7671),
  new google.maps.LatLng(35.6586, 139.7454),
  new google.maps.LatLng(35.7100, 139.8107),
];

<GoogleMap ...>
  <HeatmapLayer data={heatmapData} />
</GoogleMap>
```

### 重み付きデータポイント

```tsx
interface WeightedLocation {
  location: google.maps.LatLng;
  weight: number;
}

const weightedData: WeightedLocation[] = [
  { location: new google.maps.LatLng(35.6812, 139.7671), weight: 10 },
  { location: new google.maps.LatLng(35.6586, 139.7454), weight: 5 },
  { location: new google.maps.LatLng(35.7100, 139.8107), weight: 8 },
];

<HeatmapLayer
  data={weightedData}
  options={{
    radius: 30,
    opacity: 0.8,
  }}
/>
```

### HeatmapLayer オプション

```tsx
interface HeatmapLayerOptions {
  // データポイント
  data: google.maps.LatLng[] | WeightedLocation[];

  // 各ポイントの影響半径（ピクセル）
  radius?: number;

  // 不透明度 (0.0 - 1.0)
  opacity?: number;

  // 色のグラデーション
  gradient?: string[];

  // 最大強度
  maxIntensity?: number;

  // ズームに応じて半径を変更
  dissipating?: boolean;
}
```

### カスタムグラデーション

```tsx
// クールカラー（青 → 緑 → 黄）
const coolGradient = [
  'rgba(0, 255, 255, 0)',
  'rgba(0, 255, 255, 1)',
  'rgba(0, 191, 255, 1)',
  'rgba(0, 127, 255, 1)',
  'rgba(0, 63, 255, 1)',
  'rgba(0, 0, 255, 1)',
  'rgba(0, 0, 223, 1)',
  'rgba(0, 0, 191, 1)',
  'rgba(0, 0, 159, 1)',
  'rgba(0, 0, 127, 1)',
  'rgba(63, 0, 91, 1)',
  'rgba(127, 0, 63, 1)',
  'rgba(191, 0, 31, 1)',
  'rgba(255, 0, 0, 1)',
];

// ウォームカラー（緑 → 黄 → 赤）
const warmGradient = [
  'rgba(0, 255, 0, 0)',
  'rgba(0, 255, 0, 0.5)',
  'rgba(128, 255, 0, 0.7)',
  'rgba(255, 255, 0, 0.8)',
  'rgba(255, 128, 0, 0.9)',
  'rgba(255, 0, 0, 1)',
];

<HeatmapLayer
  data={heatmapData}
  options={{
    gradient: warmGradient,
  }}
/>
```

### 動的データ更新

```tsx
function DynamicHeatmap() {
  const [data, setData] = useState<google.maps.LatLng[]>([]);

  useEffect(() => {
    // データの取得と更新
    const fetchData = async () => {
      const response = await fetch('/api/heatmap-data');
      const points = await response.json();
      setData(
        points.map((p: { lat: number; lng: number }) =>
          new google.maps.LatLng(p.lat, p.lng)
        )
      );
    };

    fetchData();
    const interval = setInterval(fetchData, 30000); // 30秒ごとに更新

    return () => clearInterval(interval);
  }, []);

  return (
    <GoogleMap ...>
      <HeatmapLayer data={data} />
    </GoogleMap>
  );
}
```

## マーカークラスタリング（MarkerClusterer）

### 基本的な使用法

```tsx
import { MarkerClusterer, Marker } from '@react-google-maps/api';

const locations = [
  { id: '1', position: { lat: 35.6812, lng: 139.7671 } },
  { id: '2', position: { lat: 35.6586, lng: 139.7454 } },
  // ... 多数のマーカー
];

<GoogleMap ...>
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
```

### MarkerClusterer オプション

```tsx
interface MarkerClustererOptions {
  // クラスターアイコンの画像パス
  imagePath?: string;

  // グリッドサイズ（ピクセル）
  gridSize?: number;

  // クラスタリングが無効になるズームレベル
  maxZoom?: number;

  // クラスタリングが開始される最小マーカー数
  minimumClusterSize?: number;

  // クラスターのスタイル
  styles?: ClusterIconStyle[];

  // クラスターをクリックしたときズームするか
  zoomOnClick?: boolean;

  // 平均中心を使用
  averageCenter?: boolean;
}

// 使用例
<MarkerClusterer
  options={{
    gridSize: 60,
    maxZoom: 15,
    minimumClusterSize: 3,
    averageCenter: true,
    zoomOnClick: true,
  }}
>
  {(clusterer) => /* ... */}
</MarkerClusterer>
```

### カスタムクラスターアイコン

```tsx
const clusterStyles: ClusterIconStyle[] = [
  {
    url: '/cluster-small.png',
    height: 40,
    width: 40,
    textColor: '#ffffff',
    textSize: 12,
  },
  {
    url: '/cluster-medium.png',
    height: 50,
    width: 50,
    textColor: '#ffffff',
    textSize: 14,
  },
  {
    url: '/cluster-large.png',
    height: 60,
    width: 60,
    textColor: '#ffffff',
    textSize: 16,
  },
];

<MarkerClusterer
  options={{
    styles: clusterStyles,
    calculator: (markers, numStyles) => {
      // マーカー数に基づいてスタイルインデックスを計算
      let index = 0;
      const count = markers.length;

      if (count >= 100) {
        index = 2;
      } else if (count >= 10) {
        index = 1;
      }

      return {
        text: String(count),
        index: Math.min(index, numStyles),
      };
    },
  }}
>
  {(clusterer) => /* ... */}
</MarkerClusterer>
```

### SVG カスタムクラスター

```tsx
function createClusterIcon(count: number, color: string): string {
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50">
      <circle cx="25" cy="25" r="20" fill="${color}" />
      <text x="25" y="30" text-anchor="middle" fill="white" font-size="14">
        ${count}
      </text>
    </svg>
  `;
  return `data:image/svg+xml,${encodeURIComponent(svg)}`;
}

// カスタムレンダラーを使用
<MarkerClusterer
  options={{
    renderer: {
      render: ({ count, position }) => {
        const color = count >= 100 ? '#FF0000' : count >= 10 ? '#FFA500' : '#00FF00';
        return new google.maps.Marker({
          position,
          icon: {
            url: createClusterIcon(count, color),
            scaledSize: new google.maps.Size(50, 50),
          },
        });
      },
    },
  }}
>
```

### パフォーマンス最適化

```tsx
function OptimizedClusterMap({ locations }: { locations: Location[] }) {
  const [visibleMarkers, setVisibleMarkers] = useState<Location[]>([]);
  const mapRef = useRef<google.maps.Map | null>(null);

  // ビューポート内のマーカーのみをレンダリング
  const updateVisibleMarkers = useCallback(() => {
    if (!mapRef.current) return;

    const bounds = mapRef.current.getBounds();
    if (!bounds) return;

    const visible = locations.filter((loc) =>
      bounds.contains(loc.position)
    );
    setVisibleMarkers(visible);
  }, [locations]);

  const onLoad = useCallback((map: google.maps.Map) => {
    mapRef.current = map;
    updateVisibleMarkers();
  }, [updateVisibleMarkers]);

  return (
    <GoogleMap
      onLoad={onLoad}
      onBoundsChanged={updateVisibleMarkers}
    >
      <MarkerClusterer>
        {(clusterer) =>
          visibleMarkers.map((location) => (
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

## データ密度表現の選択

| ユースケース | 推奨 |
|------------|------|
| 位置の概観が重要 | マーカークラスタリング |
| 密度パターンの可視化 | ヒートマップ |
| 10,000+ ポイント | ヒートマップ |
| 個別マーカーへのアクセスが必要 | マーカークラスタリング |
| リアルタイムデータ | ヒートマップ |
| 詳細情報の表示が必要 | マーカークラスタリング |

## 組み合わせ使用

```tsx
function CombinedVisualization({ data }: { data: Location[] }) {
  const [showHeatmap, setShowHeatmap] = useState(false);

  const heatmapData = useMemo(
    () => data.map((d) => new google.maps.LatLng(d.position.lat, d.position.lng)),
    [data]
  );

  return (
    <div>
      <button onClick={() => setShowHeatmap(!showHeatmap)}>
        {showHeatmap ? 'クラスター表示' : 'ヒートマップ表示'}
      </button>

      <GoogleMap ...>
        {showHeatmap ? (
          <HeatmapLayer data={heatmapData} />
        ) : (
          <MarkerClusterer>
            {(clusterer) =>
              data.map((location) => (
                <Marker
                  key={location.id}
                  position={location.position}
                  clusterer={clusterer}
                />
              ))
            }
          </MarkerClusterer>
        )}
      </GoogleMap>
    </div>
  );
}
```

## 関連リソース

- [ヒートマップコード例](../examples/heatmap-layer.tsx)
- [マーカークラスタリングコード例](../examples/marker-clusterer.tsx)
- [パフォーマンス最適化](performance.md)
