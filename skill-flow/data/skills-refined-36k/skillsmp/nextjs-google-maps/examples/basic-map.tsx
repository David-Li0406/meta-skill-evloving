// Basic Map Component
// Next.js App Router 対応の基本的な地図コンポーネント
// TypeScript + React 18+ + Tailwind CSS

'use client';

import { GoogleMap } from '@react-google-maps/api';
import { useCallback, useState, CSSProperties } from 'react';

// --------------------------------------------------
// 型定義
// --------------------------------------------------

interface MapProps {
  /** 地図の中心座標 */
  center?: google.maps.LatLngLiteral;
  /** ズームレベル (0-21) */
  zoom?: number;
  /** コンテナのスタイル */
  containerStyle?: CSSProperties;
  /** コンテナの CSS クラス */
  containerClassName?: string;
  /** 地図オプション */
  options?: google.maps.MapOptions;
  /** 地図読み込み完了時のコールバック */
  onLoad?: (map: google.maps.Map) => void;
  /** クリック時のコールバック */
  onClick?: (e: google.maps.MapMouseEvent) => void;
  /** 子要素（マーカーなど） */
  children?: React.ReactNode;
}

// --------------------------------------------------
// デフォルト値
// --------------------------------------------------

// 東京駅をデフォルトの中心に
const DEFAULT_CENTER: google.maps.LatLngLiteral = {
  lat: 35.6812,
  lng: 139.7671,
};

const DEFAULT_ZOOM = 15;

// デフォルトのコンテナスタイル
const DEFAULT_CONTAINER_STYLE: CSSProperties = {
  width: '100%',
  height: '400px',
};

// デフォルトの地図オプション
const DEFAULT_OPTIONS: google.maps.MapOptions = {
  disableDefaultUI: false,
  zoomControl: true,
  mapTypeControl: false,
  scaleControl: true,
  streetViewControl: false,
  rotateControl: false,
  fullscreenControl: true,
  // 地図のスタイル（オプション）
  // styles: [...],
};

// --------------------------------------------------
// コンポーネント
// --------------------------------------------------

/**
 * 基本的な Google Map コンポーネント
 *
 * @example
 * // シンプルな使用法
 * <Map />
 *
 * @example
 * // カスタム設定
 * <Map
 *   center={{ lat: 35.6812, lng: 139.7671 }}
 *   zoom={12}
 *   onClick={(e) => console.log('Clicked:', e.latLng)}
 * />
 *
 * @example
 * // マーカー付き
 * <Map center={{ lat: 35.6812, lng: 139.7671 }}>
 *   <Marker position={{ lat: 35.6812, lng: 139.7671 }} />
 * </Map>
 */
export function Map({
  center = DEFAULT_CENTER,
  zoom = DEFAULT_ZOOM,
  containerStyle = DEFAULT_CONTAINER_STYLE,
  containerClassName,
  options = DEFAULT_OPTIONS,
  onLoad,
  onClick,
  children,
}: MapProps) {
  // 地図インスタンスの状態管理
  const [map, setMap] = useState<google.maps.Map | null>(null);

  // 読み込み完了時のハンドラ
  const handleLoad = useCallback(
    (map: google.maps.Map) => {
      setMap(map);
      onLoad?.(map);
    },
    [onLoad]
  );

  // アンマウント時のハンドラ
  const handleUnmount = useCallback(() => {
    setMap(null);
  }, []);

  return (
    <GoogleMap
      mapContainerStyle={containerStyle}
      mapContainerClassName={containerClassName}
      center={center}
      zoom={zoom}
      options={options}
      onLoad={handleLoad}
      onUnmount={handleUnmount}
      onClick={onClick}
    >
      {children}
    </GoogleMap>
  );
}

// --------------------------------------------------
// プリセットバリアント
// --------------------------------------------------

/**
 * フルスクリーン地図
 */
export function FullscreenMap(props: Omit<MapProps, 'containerStyle'>) {
  return (
    <Map
      {...props}
      containerStyle={{
        width: '100vw',
        height: '100vh',
      }}
    />
  );
}

/**
 * 固定高さの地図
 */
export function FixedHeightMap({
  height = 400,
  ...props
}: MapProps & { height?: number }) {
  return (
    <Map
      {...props}
      containerStyle={{
        width: '100%',
        height: `${height}px`,
      }}
    />
  );
}

/**
 * アスペクト比を維持する地図
 */
export function AspectRatioMap({
  aspectRatio = '16/9',
  ...props
}: MapProps & { aspectRatio?: string }) {
  return (
    <div style={{ aspectRatio, width: '100%' }}>
      <Map
        {...props}
        containerStyle={{
          width: '100%',
          height: '100%',
        }}
      />
    </div>
  );
}

// --------------------------------------------------
// 地図スタイルプリセット
// --------------------------------------------------

/**
 * ダークモード地図スタイル
 */
export const DARK_MODE_STYLE: google.maps.MapTypeStyle[] = [
  { elementType: 'geometry', stylers: [{ color: '#242f3e' }] },
  { elementType: 'labels.text.stroke', stylers: [{ color: '#242f3e' }] },
  { elementType: 'labels.text.fill', stylers: [{ color: '#746855' }] },
  {
    featureType: 'administrative.locality',
    elementType: 'labels.text.fill',
    stylers: [{ color: '#d59563' }],
  },
  {
    featureType: 'poi',
    elementType: 'labels.text.fill',
    stylers: [{ color: '#d59563' }],
  },
  {
    featureType: 'poi.park',
    elementType: 'geometry',
    stylers: [{ color: '#263c3f' }],
  },
  {
    featureType: 'poi.park',
    elementType: 'labels.text.fill',
    stylers: [{ color: '#6b9a76' }],
  },
  {
    featureType: 'road',
    elementType: 'geometry',
    stylers: [{ color: '#38414e' }],
  },
  {
    featureType: 'road',
    elementType: 'geometry.stroke',
    stylers: [{ color: '#212a37' }],
  },
  {
    featureType: 'road',
    elementType: 'labels.text.fill',
    stylers: [{ color: '#9ca5b3' }],
  },
  {
    featureType: 'road.highway',
    elementType: 'geometry',
    stylers: [{ color: '#746855' }],
  },
  {
    featureType: 'road.highway',
    elementType: 'geometry.stroke',
    stylers: [{ color: '#1f2835' }],
  },
  {
    featureType: 'road.highway',
    elementType: 'labels.text.fill',
    stylers: [{ color: '#f3d19c' }],
  },
  {
    featureType: 'transit',
    elementType: 'geometry',
    stylers: [{ color: '#2f3948' }],
  },
  {
    featureType: 'transit.station',
    elementType: 'labels.text.fill',
    stylers: [{ color: '#d59563' }],
  },
  {
    featureType: 'water',
    elementType: 'geometry',
    stylers: [{ color: '#17263c' }],
  },
  {
    featureType: 'water',
    elementType: 'labels.text.fill',
    stylers: [{ color: '#515c6d' }],
  },
  {
    featureType: 'water',
    elementType: 'labels.text.stroke',
    stylers: [{ color: '#17263c' }],
  },
];

/**
 * シンプル地図スタイル（POI を非表示）
 */
export const SIMPLE_STYLE: google.maps.MapTypeStyle[] = [
  {
    featureType: 'poi',
    stylers: [{ visibility: 'off' }],
  },
  {
    featureType: 'transit',
    elementType: 'labels.icon',
    stylers: [{ visibility: 'off' }],
  },
];

/**
 * ダークモード地図
 */
export function DarkModeMap(props: MapProps) {
  return (
    <Map
      {...props}
      options={{
        ...DEFAULT_OPTIONS,
        ...props.options,
        styles: DARK_MODE_STYLE,
      }}
    />
  );
}

/**
 * シンプル地図（POI 非表示）
 */
export function SimpleMap(props: MapProps) {
  return (
    <Map
      {...props}
      options={{
        ...DEFAULT_OPTIONS,
        ...props.options,
        styles: SIMPLE_STYLE,
      }}
    />
  );
}

// --------------------------------------------------
// 使用例
// --------------------------------------------------

/*
// 基本的な使用法
import { Map } from '@/components/basic-map';

export default function MapPage() {
  return (
    <Map
      center={{ lat: 35.6812, lng: 139.7671 }}
      zoom={15}
      onClick={(e) => {
        console.log('Clicked at:', e.latLng?.toJSON());
      }}
    />
  );
}

// ダークモード
import { DarkModeMap } from '@/components/basic-map';

export default function DarkMapPage() {
  return <DarkModeMap />;
}

// マーカー付き
import { Map } from '@/components/basic-map';
import { Marker } from '@react-google-maps/api';

export default function MapWithMarkerPage() {
  return (
    <Map center={{ lat: 35.6812, lng: 139.7671 }}>
      <Marker position={{ lat: 35.6812, lng: 139.7671 }} />
    </Map>
  );
}
*/
