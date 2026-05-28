// Drawing Manager Component
// 描画ツールコンポーネント
// TypeScript + React 18+ + Tailwind CSS

'use client';

import { GoogleMap, DrawingManager } from '@react-google-maps/api';
import { useState, useCallback, CSSProperties } from 'react';

// --------------------------------------------------
// 型定義
// --------------------------------------------------

type DrawingOverlayType = google.maps.drawing.OverlayType;

interface ShapeData {
  id: string;
  type: 'polygon' | 'circle' | 'rectangle' | 'polyline' | 'marker';
  overlay: google.maps.MVCObject;
  data: unknown;
}

interface DrawingMapProps {
  /** 地図の中心座標 */
  center?: google.maps.LatLngLiteral;
  /** ズームレベル */
  zoom?: number;
  /** コンテナのスタイル */
  containerStyle?: CSSProperties;
  /** 図形描画完了時のコールバック */
  onShapeComplete?: (shape: ShapeData) => void;
  /** 利用可能な描画モード */
  drawingModes?: DrawingOverlayType[];
  /** 編集可能にするか */
  editable?: boolean;
}

// --------------------------------------------------
// デフォルト値
// --------------------------------------------------

const DEFAULT_CONTAINER_STYLE: CSSProperties = {
  width: '100%',
  height: '400px',
};

const DEFAULT_CENTER: google.maps.LatLngLiteral = {
  lat: 35.6812,
  lng: 139.7671,
};

// 図形のデフォルトスタイル
const DEFAULT_POLYGON_OPTIONS: google.maps.PolygonOptions = {
  fillColor: '#4285F4',
  fillOpacity: 0.3,
  strokeColor: '#4285F4',
  strokeWeight: 2,
  editable: true,
  draggable: true,
};

const DEFAULT_CIRCLE_OPTIONS: google.maps.CircleOptions = {
  fillColor: '#34A853',
  fillOpacity: 0.3,
  strokeColor: '#34A853',
  strokeWeight: 2,
  editable: true,
  draggable: true,
};

const DEFAULT_RECTANGLE_OPTIONS: google.maps.RectangleOptions = {
  fillColor: '#FBBC05',
  fillOpacity: 0.3,
  strokeColor: '#FBBC05',
  strokeWeight: 2,
  editable: true,
  draggable: true,
};

const DEFAULT_POLYLINE_OPTIONS: google.maps.PolylineOptions = {
  strokeColor: '#EA4335',
  strokeWeight: 3,
  editable: true,
};

// --------------------------------------------------
// ユーティリティ関数
// --------------------------------------------------

let shapeIdCounter = 0;

function generateShapeId(): string {
  return `shape-${Date.now()}-${shapeIdCounter++}`;
}

function getPolygonCoordinates(polygon: google.maps.Polygon): google.maps.LatLngLiteral[] {
  const path = polygon.getPath();
  return path.getArray().map((latLng) => ({
    lat: latLng.lat(),
    lng: latLng.lng(),
  }));
}

function getCircleData(circle: google.maps.Circle): { center: google.maps.LatLngLiteral; radius: number } {
  return {
    center: circle.getCenter()?.toJSON() || { lat: 0, lng: 0 },
    radius: circle.getRadius(),
  };
}

function getRectangleData(rectangle: google.maps.Rectangle): google.maps.LatLngBoundsLiteral | null {
  return rectangle.getBounds()?.toJSON() || null;
}

/**
 * ポリゴンの面積を計算（平方メートル）
 */
export function calculatePolygonArea(polygon: google.maps.Polygon): number {
  return google.maps.geometry.spherical.computeArea(polygon.getPath());
}

/**
 * ポリラインの長さを計算（メートル）
 */
export function calculatePolylineLength(polyline: google.maps.Polyline): number {
  return google.maps.geometry.spherical.computeLength(polyline.getPath());
}

// --------------------------------------------------
// メインコンポーネント
// --------------------------------------------------

/**
 * 描画ツール付き地図コンポーネント
 *
 * @example
 * <DrawingMap
 *   onShapeComplete={(shape) => console.log('Shape created:', shape)}
 * />
 */
export function DrawingMap({
  center = DEFAULT_CENTER,
  zoom = 15,
  containerStyle = DEFAULT_CONTAINER_STYLE,
  onShapeComplete,
  drawingModes,
  editable = true,
}: DrawingMapProps) {
  const [shapes, setShapes] = useState<ShapeData[]>([]);
  const [selectedShape, setSelectedShape] = useState<ShapeData | null>(null);
  const [drawingMode, setDrawingMode] = useState<DrawingOverlayType | null>(null);

  // 図形を選択
  const selectShape = useCallback((shape: ShapeData | null) => {
    // 前の選択を解除
    if (selectedShape && selectedShape.overlay instanceof google.maps.Polygon) {
      selectedShape.overlay.setOptions({ strokeWeight: 2 });
    }

    // 新しい図形を選択
    if (shape && shape.overlay instanceof google.maps.Polygon) {
      shape.overlay.setOptions({ strokeWeight: 4 });
    }

    setSelectedShape(shape);
  }, [selectedShape]);

  // 図形削除
  const deleteShape = useCallback((shapeId: string) => {
    const shape = shapes.find((s) => s.id === shapeId);
    if (shape) {
      // 地図から削除
      if ('setMap' in shape.overlay) {
        (shape.overlay as google.maps.Polygon).setMap(null);
      }
      setShapes((prev) => prev.filter((s) => s.id !== shapeId));
      if (selectedShape?.id === shapeId) {
        setSelectedShape(null);
      }
    }
  }, [shapes, selectedShape]);

  // すべての図形を削除
  const clearAllShapes = useCallback(() => {
    shapes.forEach((shape) => {
      if ('setMap' in shape.overlay) {
        (shape.overlay as google.maps.Polygon).setMap(null);
      }
    });
    setShapes([]);
    setSelectedShape(null);
  }, [shapes]);

  // 図形作成時の共通処理
  const handleShapeComplete = useCallback(
    (type: ShapeData['type'], overlay: google.maps.MVCObject, data: unknown) => {
      const shape: ShapeData = {
        id: generateShapeId(),
        type,
        overlay,
        data,
      };

      // クリックイベントを追加
      if ('addListener' in overlay) {
        (overlay as google.maps.Polygon).addListener('click', () => {
          selectShape(shape);
        });
      }

      setShapes((prev) => [...prev, shape]);
      onShapeComplete?.(shape);
      setDrawingMode(null); // 描画モードをリセット
    },
    [onShapeComplete, selectShape]
  );

  // ポリゴン完了
  const onPolygonComplete = useCallback(
    (polygon: google.maps.Polygon) => {
      polygon.setEditable(editable);
      polygon.setDraggable(editable);
      handleShapeComplete('polygon', polygon, getPolygonCoordinates(polygon));
    },
    [editable, handleShapeComplete]
  );

  // 円完了
  const onCircleComplete = useCallback(
    (circle: google.maps.Circle) => {
      circle.setEditable(editable);
      circle.setDraggable(editable);
      handleShapeComplete('circle', circle, getCircleData(circle));
    },
    [editable, handleShapeComplete]
  );

  // 矩形完了
  const onRectangleComplete = useCallback(
    (rectangle: google.maps.Rectangle) => {
      rectangle.setEditable(editable);
      rectangle.setDraggable(editable);
      handleShapeComplete('rectangle', rectangle, getRectangleData(rectangle));
    },
    [editable, handleShapeComplete]
  );

  // ポリライン完了
  const onPolylineComplete = useCallback(
    (polyline: google.maps.Polyline) => {
      polyline.setEditable(editable);
      const path = polyline.getPath().getArray().map((latLng) => ({
        lat: latLng.lat(),
        lng: latLng.lng(),
      }));
      handleShapeComplete('polyline', polyline, path);
    },
    [editable, handleShapeComplete]
  );

  // マーカー完了
  const onMarkerComplete = useCallback(
    (marker: google.maps.Marker) => {
      marker.setDraggable(editable);
      handleShapeComplete('marker', marker, marker.getPosition()?.toJSON());
    },
    [editable, handleShapeComplete]
  );

  return (
    <div>
      {/* ツールバー */}
      <div className="mb-2 flex gap-2 flex-wrap">
        <button
          onClick={() => setDrawingMode(google.maps.drawing.OverlayType.POLYGON)}
          className={`px-3 py-1.5 rounded text-sm ${
            drawingMode === google.maps.drawing.OverlayType.POLYGON
              ? 'bg-blue-500 text-white'
              : 'bg-gray-200 text-gray-700'
          }`}
        >
          ポリゴン
        </button>
        <button
          onClick={() => setDrawingMode(google.maps.drawing.OverlayType.CIRCLE)}
          className={`px-3 py-1.5 rounded text-sm ${
            drawingMode === google.maps.drawing.OverlayType.CIRCLE
              ? 'bg-green-500 text-white'
              : 'bg-gray-200 text-gray-700'
          }`}
        >
          円
        </button>
        <button
          onClick={() => setDrawingMode(google.maps.drawing.OverlayType.RECTANGLE)}
          className={`px-3 py-1.5 rounded text-sm ${
            drawingMode === google.maps.drawing.OverlayType.RECTANGLE
              ? 'bg-yellow-500 text-white'
              : 'bg-gray-200 text-gray-700'
          }`}
        >
          矩形
        </button>
        <button
          onClick={() => setDrawingMode(google.maps.drawing.OverlayType.POLYLINE)}
          className={`px-3 py-1.5 rounded text-sm ${
            drawingMode === google.maps.drawing.OverlayType.POLYLINE
              ? 'bg-red-500 text-white'
              : 'bg-gray-200 text-gray-700'
          }`}
        >
          線
        </button>
        <button
          onClick={() => setDrawingMode(null)}
          className="px-3 py-1.5 bg-gray-500 text-white rounded text-sm"
        >
          選択モード
        </button>

        <div className="flex-1" />

        {selectedShape && (
          <button
            onClick={() => deleteShape(selectedShape.id)}
            className="px-3 py-1.5 bg-red-500 text-white rounded text-sm"
          >
            選択を削除
          </button>
        )}
        {shapes.length > 0 && (
          <button
            onClick={clearAllShapes}
            className="px-3 py-1.5 bg-gray-700 text-white rounded text-sm"
          >
            すべて削除
          </button>
        )}
      </div>

      {/* 地図 */}
      <GoogleMap
        mapContainerStyle={containerStyle}
        center={center}
        zoom={zoom}
        onClick={() => selectShape(null)}
      >
        <DrawingManager
          drawingMode={drawingMode}
          onPolygonComplete={onPolygonComplete}
          onCircleComplete={onCircleComplete}
          onRectangleComplete={onRectangleComplete}
          onPolylineComplete={onPolylineComplete}
          onMarkerComplete={onMarkerComplete}
          options={{
            drawingControl: false, // カスタムツールバーを使用
            polygonOptions: DEFAULT_POLYGON_OPTIONS,
            circleOptions: DEFAULT_CIRCLE_OPTIONS,
            rectangleOptions: DEFAULT_RECTANGLE_OPTIONS,
            polylineOptions: DEFAULT_POLYLINE_OPTIONS,
          }}
        />
      </GoogleMap>

      {/* 図形リスト */}
      {shapes.length > 0 && (
        <div className="mt-4 p-4 bg-white rounded-lg shadow">
          <h3 className="font-bold mb-2">描画された図形 ({shapes.length})</h3>
          <ul className="space-y-2">
            {shapes.map((shape) => (
              <li
                key={shape.id}
                className={`flex items-center justify-between p-2 rounded cursor-pointer ${
                  selectedShape?.id === shape.id ? 'bg-blue-50' : 'hover:bg-gray-50'
                }`}
                onClick={() => selectShape(shape)}
              >
                <div className="flex items-center gap-2">
                  <ShapeIcon type={shape.type} />
                  <span className="capitalize">{shape.type}</span>
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    deleteShape(shape.id);
                  }}
                  className="text-red-500 hover:text-red-700"
                >
                  削除
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

// --------------------------------------------------
// 図形アイコン
// --------------------------------------------------

function ShapeIcon({ type }: { type: ShapeData['type'] }) {
  const iconClass = 'w-4 h-4';

  switch (type) {
    case 'polygon':
      return (
        <svg className={iconClass} fill="#4285F4" viewBox="0 0 24 24">
          <path d="M2 2h20v20H2z" fillOpacity="0.3" />
          <path d="M2 2h20v20H2z" fill="none" stroke="#4285F4" strokeWidth="2" />
        </svg>
      );
    case 'circle':
      return (
        <svg className={iconClass} fill="#34A853" viewBox="0 0 24 24">
          <circle cx="12" cy="12" r="10" fillOpacity="0.3" />
          <circle cx="12" cy="12" r="10" fill="none" stroke="#34A853" strokeWidth="2" />
        </svg>
      );
    case 'rectangle':
      return (
        <svg className={iconClass} fill="#FBBC05" viewBox="0 0 24 24">
          <rect x="2" y="4" width="20" height="16" fillOpacity="0.3" />
          <rect x="2" y="4" width="20" height="16" fill="none" stroke="#FBBC05" strokeWidth="2" />
        </svg>
      );
    case 'polyline':
      return (
        <svg className={iconClass} viewBox="0 0 24 24">
          <path d="M2 18l7-7 4 4 9-9" fill="none" stroke="#EA4335" strokeWidth="2" />
        </svg>
      );
    case 'marker':
      return (
        <svg className={iconClass} fill="#4285F4" viewBox="0 0 24 24">
          <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z" />
        </svg>
      );
    default:
      return null;
  }
}

// --------------------------------------------------
// エクスポート用データ取得
// --------------------------------------------------

/**
 * 図形データを JSON 形式でエクスポート
 */
export function exportShapesToJSON(shapes: ShapeData[]): string {
  const exportData = shapes.map((shape) => {
    let data: unknown = null;

    switch (shape.type) {
      case 'polygon':
        data = getPolygonCoordinates(shape.overlay as google.maps.Polygon);
        break;
      case 'circle':
        data = getCircleData(shape.overlay as google.maps.Circle);
        break;
      case 'rectangle':
        data = getRectangleData(shape.overlay as google.maps.Rectangle);
        break;
      case 'polyline':
        const polyline = shape.overlay as google.maps.Polyline;
        data = polyline.getPath().getArray().map((latLng) => ({
          lat: latLng.lat(),
          lng: latLng.lng(),
        }));
        break;
      case 'marker':
        const marker = shape.overlay as google.maps.Marker;
        data = marker.getPosition()?.toJSON();
        break;
    }

    return {
      id: shape.id,
      type: shape.type,
      data,
    };
  });

  return JSON.stringify(exportData, null, 2);
}

// --------------------------------------------------
// 使用例
// --------------------------------------------------

/*
// 基本的な使用法
import { DrawingMap } from '@/components/drawing-manager';

export default function DrawingPage() {
  const handleShapeComplete = (shape: ShapeData) => {
    console.log('Shape created:', shape);
  };

  return (
    <DrawingMap
      onShapeComplete={handleShapeComplete}
      editable={true}
    />
  );
}

// 面積計算
import { DrawingMap, calculatePolygonArea } from '@/components/drawing-manager';

export default function AreaCalculationPage() {
  const handleShapeComplete = (shape: ShapeData) => {
    if (shape.type === 'polygon') {
      const area = calculatePolygonArea(shape.overlay as google.maps.Polygon);
      console.log(`面積: ${(area / 1000000).toFixed(4)} km²`);
    }
  };

  return <DrawingMap onShapeComplete={handleShapeComplete} />;
}

// データのエクスポート
import { DrawingMap, exportShapesToJSON } from '@/components/drawing-manager';

export default function ExportPage() {
  const [shapes, setShapes] = useState<ShapeData[]>([]);

  const handleExport = () => {
    const json = exportShapesToJSON(shapes);
    console.log(json);

    // ダウンロード
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'shapes.json';
    a.click();
  };

  return (
    <div>
      <DrawingMap
        onShapeComplete={(shape) => setShapes((prev) => [...prev, shape])}
      />
      <button onClick={handleExport}>エクスポート</button>
    </div>
  );
}
*/
