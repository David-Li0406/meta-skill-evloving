# 描画ツール リファレンス

## 概要

Google Maps の描画ツールを使用すると、ユーザーが地図上にマーカー、ポリライン、
ポリゴン、円、矩形などの図形を描画できます。

## 必要なライブラリ

```tsx
const libraries: Libraries = ['drawing'];

const { isLoaded } = useLoadScript({
  googleMapsApiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY!,
  libraries,
});
```

## DrawingManager コンポーネント

### 基本的な使用法

```tsx
import { DrawingManager } from '@react-google-maps/api';

<GoogleMap ...>
  <DrawingManager
    drawingMode={google.maps.drawing.OverlayType.POLYGON}
    onPolygonComplete={(polygon) => {
      console.log('Polygon complete', polygon);
    }}
  />
</GoogleMap>
```

### DrawingManager オプション

```tsx
interface DrawingManagerOptions {
  // 描画モード
  drawingMode?: google.maps.drawing.OverlayType | null;

  // 描画コントロールを表示
  drawingControl?: boolean;

  // 描画コントロールのオプション
  drawingControlOptions?: {
    position: google.maps.ControlPosition;
    drawingModes: google.maps.drawing.OverlayType[];
  };

  // 各図形のデフォルトオプション
  circleOptions?: google.maps.CircleOptions;
  markerOptions?: google.maps.MarkerOptions;
  polygonOptions?: google.maps.PolygonOptions;
  polylineOptions?: google.maps.PolylineOptions;
  rectangleOptions?: google.maps.RectangleOptions;
}
```

### 描画モード（OverlayType）

| 値 | 説明 |
|-----|------|
| `MARKER` | マーカー（点） |
| `CIRCLE` | 円 |
| `POLYGON` | 多角形 |
| `POLYLINE` | 線 |
| `RECTANGLE` | 矩形 |

## 図形描画完了イベント

```tsx
<DrawingManager
  onMarkerComplete={(marker) => {
    console.log('Marker position:', marker.getPosition()?.toJSON());
  }}
  onCircleComplete={(circle) => {
    console.log('Circle center:', circle.getCenter()?.toJSON());
    console.log('Circle radius:', circle.getRadius());
  }}
  onPolygonComplete={(polygon) => {
    const path = polygon.getPath();
    const coordinates = path.getArray().map((latLng) => ({
      lat: latLng.lat(),
      lng: latLng.lng(),
    }));
    console.log('Polygon coordinates:', coordinates);
  }}
  onPolylineComplete={(polyline) => {
    const path = polyline.getPath();
    const coordinates = path.getArray().map((latLng) => ({
      lat: latLng.lat(),
      lng: latLng.lng(),
    }));
    console.log('Polyline coordinates:', coordinates);
  }}
  onRectangleComplete={(rectangle) => {
    const bounds = rectangle.getBounds();
    console.log('Rectangle bounds:', bounds?.toJSON());
  }}
  onOverlayComplete={(e) => {
    console.log('Overlay type:', e.type);
    console.log('Overlay object:', e.overlay);
  }}
/>
```

## 図形のスタイル設定

### ポリゴン

```tsx
<DrawingManager
  options={{
    polygonOptions: {
      fillColor: '#FF0000',
      fillOpacity: 0.3,
      strokeColor: '#FF0000',
      strokeWeight: 2,
      strokeOpacity: 0.8,
      editable: true,
      draggable: true,
    },
  }}
/>
```

### 円

```tsx
<DrawingManager
  options={{
    circleOptions: {
      fillColor: '#00FF00',
      fillOpacity: 0.2,
      strokeColor: '#00FF00',
      strokeWeight: 2,
      editable: true,
      draggable: true,
    },
  }}
/>
```

### ポリライン

```tsx
<DrawingManager
  options={{
    polylineOptions: {
      strokeColor: '#0000FF',
      strokeWeight: 3,
      strokeOpacity: 1,
      editable: true,
    },
  }}
/>
```

## 描画コントロールの位置

```tsx
<DrawingManager
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
  }}
/>
```

### ControlPosition の値

| 値 | 説明 |
|-----|------|
| `TOP_LEFT` | 左上 |
| `TOP_CENTER` | 上中央 |
| `TOP_RIGHT` | 右上 |
| `LEFT_CENTER` | 左中央 |
| `RIGHT_CENTER` | 右中央 |
| `BOTTOM_LEFT` | 左下 |
| `BOTTOM_CENTER` | 下中央 |
| `BOTTOM_RIGHT` | 右下 |

## 図形の編集と削除

### 編集可能な図形

```tsx
const [shapes, setShapes] = useState<google.maps.Polygon[]>([]);

const onPolygonComplete = (polygon: google.maps.Polygon) => {
  // 編集可能に設定
  polygon.setEditable(true);
  polygon.setDraggable(true);

  // 編集イベントをリッスン
  polygon.addListener('set_at', () => {
    console.log('Vertex moved');
  });

  polygon.addListener('insert_at', () => {
    console.log('Vertex inserted');
  });

  polygon.addListener('remove_at', () => {
    console.log('Vertex removed');
  });

  setShapes((prev) => [...prev, polygon]);
};

// 図形の削除
const deleteShape = (index: number) => {
  const shape = shapes[index];
  shape.setMap(null); // 地図から削除
  setShapes((prev) => prev.filter((_, i) => i !== index));
};
```

### 図形のクリックで選択

```tsx
const [selectedShape, setSelectedShape] = useState<google.maps.Polygon | null>(null);

const onPolygonComplete = (polygon: google.maps.Polygon) => {
  polygon.addListener('click', () => {
    // 前の選択を解除
    if (selectedShape) {
      selectedShape.setOptions({ strokeWeight: 2 });
    }

    // 新しい選択をハイライト
    polygon.setOptions({ strokeWeight: 4 });
    setSelectedShape(polygon);
  });
};
```

## 図形データの保存

### 座標の抽出

```tsx
function getPolygonCoordinates(polygon: google.maps.Polygon) {
  const path = polygon.getPath();
  return path.getArray().map((latLng) => ({
    lat: latLng.lat(),
    lng: latLng.lng(),
  }));
}

function getCircleData(circle: google.maps.Circle) {
  return {
    center: circle.getCenter()?.toJSON(),
    radius: circle.getRadius(),
  };
}

function getRectangleData(rectangle: google.maps.Rectangle) {
  const bounds = rectangle.getBounds();
  return {
    north: bounds?.getNorthEast().lat(),
    east: bounds?.getNorthEast().lng(),
    south: bounds?.getSouthWest().lat(),
    west: bounds?.getSouthWest().lng(),
  };
}
```

### JSON への変換

```tsx
interface ShapeData {
  type: 'polygon' | 'circle' | 'rectangle' | 'polyline';
  data: unknown;
}

function saveShapes(shapes: google.maps.MVCObject[]): ShapeData[] {
  return shapes.map((shape) => {
    if (shape instanceof google.maps.Polygon) {
      return {
        type: 'polygon',
        data: getPolygonCoordinates(shape),
      };
    }
    if (shape instanceof google.maps.Circle) {
      return {
        type: 'circle',
        data: getCircleData(shape),
      };
    }
    // ... 他の形状
    return { type: 'polygon', data: null };
  });
}
```

## 図形の復元

```tsx
function restorePolygon(
  map: google.maps.Map,
  coordinates: google.maps.LatLngLiteral[]
): google.maps.Polygon {
  return new google.maps.Polygon({
    paths: coordinates,
    map,
    fillColor: '#FF0000',
    fillOpacity: 0.3,
    strokeColor: '#FF0000',
    strokeWeight: 2,
    editable: true,
  });
}

function restoreCircle(
  map: google.maps.Map,
  center: google.maps.LatLngLiteral,
  radius: number
): google.maps.Circle {
  return new google.maps.Circle({
    center,
    radius,
    map,
    fillColor: '#00FF00',
    fillOpacity: 0.2,
    strokeColor: '#00FF00',
    strokeWeight: 2,
    editable: true,
  });
}
```

## 面積と距離の計算

```tsx
// ポリゴンの面積（平方メートル）
function calculatePolygonArea(polygon: google.maps.Polygon): number {
  return google.maps.geometry.spherical.computeArea(polygon.getPath());
}

// ポリラインの長さ（メートル）
function calculatePolylineLength(polyline: google.maps.Polyline): number {
  return google.maps.geometry.spherical.computeLength(polyline.getPath());
}

// 円の面積（平方メートル）
function calculateCircleArea(circle: google.maps.Circle): number {
  const radius = circle.getRadius();
  return Math.PI * radius * radius;
}

// 使用例
const area = calculatePolygonArea(polygon);
console.log(`面積: ${(area / 1000000).toFixed(2)} km²`);
```

## 描画モードの動的切り替え

```tsx
function DynamicDrawingMode() {
  const [drawingMode, setDrawingMode] = useState<google.maps.drawing.OverlayType | null>(null);

  return (
    <div>
      <div className="mb-4 flex gap-2">
        <button
          onClick={() => setDrawingMode(google.maps.drawing.OverlayType.POLYGON)}
          className="px-4 py-2 bg-blue-500 text-white rounded"
        >
          ポリゴン
        </button>
        <button
          onClick={() => setDrawingMode(google.maps.drawing.OverlayType.CIRCLE)}
          className="px-4 py-2 bg-green-500 text-white rounded"
        >
          円
        </button>
        <button
          onClick={() => setDrawingMode(null)}
          className="px-4 py-2 bg-gray-500 text-white rounded"
        >
          選択モード
        </button>
      </div>

      <GoogleMap ...>
        <DrawingManager
          drawingMode={drawingMode}
          options={{
            drawingControl: false, // カスタムコントロールを使用
          }}
        />
      </GoogleMap>
    </div>
  );
}
```

## ベストプラクティス

1. **図形の管理**
   - 描画された図形を状態で管理
   - 削除時は `setMap(null)` を呼び出す

2. **編集機能**
   - `editable: true` で頂点の編集を許可
   - `draggable: true` で図形の移動を許可

3. **スタイルの一貫性**
   - 描画前にデフォルトオプションを設定

4. **データの永続化**
   - 座標データを JSON で保存
   - 復元時は同じオプションで再作成

## 関連リソース

- [描画ツールコード例](../examples/drawing-manager.tsx)
- [Google Maps API ドキュメント](https://developers.google.com/maps/documentation/javascript/drawinglayer)
