// Map with Markers Component
// マーカーと InfoWindow を表示する地図コンポーネント
// TypeScript + React 18+ + Tailwind CSS

'use client';

import { GoogleMap, Marker, InfoWindow } from '@react-google-maps/api';
import { useCallback, useState, CSSProperties } from 'react';

// --------------------------------------------------
// 型定義
// --------------------------------------------------

export interface MapLocation {
  id: string;
  position: google.maps.LatLngLiteral;
  title: string;
  description?: string;
  icon?: string | google.maps.Icon;
}

interface MapWithMarkersProps {
  /** マーカーのリスト */
  locations: MapLocation[];
  /** 地図の中心座標（指定しない場合は最初のマーカーの位置） */
  center?: google.maps.LatLngLiteral;
  /** ズームレベル */
  zoom?: number;
  /** コンテナのスタイル */
  containerStyle?: CSSProperties;
  /** マーカークリック時のコールバック */
  onMarkerClick?: (location: MapLocation) => void;
  /** InfoWindow のカスタムレンダラー */
  renderInfoWindow?: (location: MapLocation) => React.ReactNode;
  /** マーカーアイコンのカスタマイズ */
  markerIcon?: string | google.maps.Icon;
  /** クラスタリングを有効にするか */
  enableClustering?: boolean;
}

// --------------------------------------------------
// デフォルト値
// --------------------------------------------------

const DEFAULT_CONTAINER_STYLE: CSSProperties = {
  width: '100%',
  height: '400px',
};

const DEFAULT_ZOOM = 13;

// サンプルデータ
export const SAMPLE_LOCATIONS: MapLocation[] = [
  {
    id: '1',
    position: { lat: 35.6812, lng: 139.7671 },
    title: '東京駅',
    description: '日本最大のターミナル駅',
  },
  {
    id: '2',
    position: { lat: 35.6586, lng: 139.7454 },
    title: '東京タワー',
    description: '高さ333mの電波塔',
  },
  {
    id: '3',
    position: { lat: 35.7100, lng: 139.8107 },
    title: '浅草寺',
    description: '東京最古の寺院',
  },
  {
    id: '4',
    position: { lat: 35.6762, lng: 139.6503 },
    title: '新宿駅',
    description: '世界一利用者数の多い駅',
  },
];

// --------------------------------------------------
// コンポーネント
// --------------------------------------------------

/**
 * マーカー付きの Google Map コンポーネント
 *
 * @example
 * // 基本的な使用法
 * <MapWithMarkers locations={locations} />
 *
 * @example
 * // カスタム InfoWindow
 * <MapWithMarkers
 *   locations={locations}
 *   renderInfoWindow={(location) => (
 *     <div>
 *       <h3>{location.title}</h3>
 *       <p>{location.description}</p>
 *     </div>
 *   )}
 * />
 */
export function MapWithMarkers({
  locations,
  center,
  zoom = DEFAULT_ZOOM,
  containerStyle = DEFAULT_CONTAINER_STYLE,
  onMarkerClick,
  renderInfoWindow,
  markerIcon,
}: MapWithMarkersProps) {
  // 選択されたマーカーの ID
  const [selectedId, setSelectedId] = useState<string | null>(null);

  // 地図インスタンス
  const [map, setMap] = useState<google.maps.Map | null>(null);

  // 中心座標を計算（指定がなければ最初のマーカーの位置）
  const mapCenter = center || locations[0]?.position || { lat: 35.6812, lng: 139.7671 };

  // 選択されたマーカーを取得
  const selectedLocation = locations.find((loc) => loc.id === selectedId);

  // マーカークリックハンドラ
  const handleMarkerClick = useCallback(
    (location: MapLocation) => {
      setSelectedId(location.id);
      onMarkerClick?.(location);
    },
    [onMarkerClick]
  );

  // InfoWindow を閉じる
  const handleInfoWindowClose = useCallback(() => {
    setSelectedId(null);
  }, []);

  // 地図読み込み完了時
  const handleLoad = useCallback((map: google.maps.Map) => {
    setMap(map);

    // すべてのマーカーが表示されるように bounds を調整
    if (locations.length > 1) {
      const bounds = new google.maps.LatLngBounds();
      locations.forEach((loc) => {
        bounds.extend(loc.position);
      });
      map.fitBounds(bounds);
    }
  }, [locations]);

  return (
    <GoogleMap
      mapContainerStyle={containerStyle}
      center={mapCenter}
      zoom={zoom}
      onLoad={handleLoad}
    >
      {locations.map((location) => (
        <Marker
          key={location.id}
          position={location.position}
          title={location.title}
          icon={location.icon || markerIcon}
          onClick={() => handleMarkerClick(location)}
          animation={
            selectedId === location.id
              ? google.maps.Animation.BOUNCE
              : undefined
          }
        />
      ))}

      {selectedLocation && (
        <InfoWindow
          position={selectedLocation.position}
          onCloseClick={handleInfoWindowClose}
          options={{
            pixelOffset: new google.maps.Size(0, -30),
          }}
        >
          {renderInfoWindow ? (
            <>{renderInfoWindow(selectedLocation)}</>
          ) : (
            <DefaultInfoWindowContent location={selectedLocation} />
          )}
        </InfoWindow>
      )}
    </GoogleMap>
  );
}

// --------------------------------------------------
// デフォルト InfoWindow コンテンツ
// --------------------------------------------------

function DefaultInfoWindowContent({ location }: { location: MapLocation }) {
  return (
    <div className="p-2 max-w-xs">
      <h3 className="font-bold text-gray-900 mb-1">{location.title}</h3>
      {location.description && (
        <p className="text-gray-600 text-sm">{location.description}</p>
      )}
    </div>
  );
}

// --------------------------------------------------
// カスタムマーカーアイコンの例
// --------------------------------------------------

/**
 * カスタム SVG マーカーを作成
 */
export function createCustomMarkerIcon(
  color: string = '#4285F4',
  size: number = 40
): google.maps.Icon {
  return {
    url: `data:image/svg+xml,${encodeURIComponent(`
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="${size}" height="${size}">
        <path fill="${color}" d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
      </svg>
    `)}`,
    scaledSize: new google.maps.Size(size, size),
    anchor: new google.maps.Point(size / 2, size),
  };
}

/**
 * 番号付きマーカーを作成
 */
export function createNumberedMarkerIcon(
  number: number,
  color: string = '#4285F4'
): google.maps.Icon {
  return {
    url: `data:image/svg+xml,${encodeURIComponent(`
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 50" width="40" height="50">
        <path fill="${color}" d="M20 0C9 0 0 9 0 20c0 15 20 30 20 30s20-15 20-30C40 9 31 0 20 0z"/>
        <circle fill="white" cx="20" cy="18" r="12"/>
        <text x="20" y="23" text-anchor="middle" font-size="14" font-weight="bold" fill="${color}">${number}</text>
      </svg>
    `)}`,
    scaledSize: new google.maps.Size(40, 50),
    anchor: new google.maps.Point(20, 50),
  };
}

// --------------------------------------------------
// 選択可能なマーカーリスト付き地図
// --------------------------------------------------

interface MapWithListProps extends MapWithMarkersProps {
  /** リストを表示するか */
  showList?: boolean;
  /** リストの位置 */
  listPosition?: 'left' | 'right' | 'bottom';
}

/**
 * マーカーリスト付き地図
 */
export function MapWithMarkerList({
  locations,
  showList = true,
  listPosition = 'right',
  ...props
}: MapWithListProps) {
  const [selectedId, setSelectedId] = useState<string | null>(null);

  const handleLocationSelect = (location: MapLocation) => {
    setSelectedId(location.id);
  };

  const containerClass =
    listPosition === 'bottom'
      ? 'flex flex-col'
      : 'flex flex-col md:flex-row';

  const listClass =
    listPosition === 'bottom'
      ? 'w-full max-h-48 overflow-y-auto'
      : listPosition === 'left'
        ? 'w-full md:w-64 order-first'
        : 'w-full md:w-64';

  return (
    <div className={containerClass}>
      <div className="flex-1">
        <MapWithMarkers
          {...props}
          locations={locations}
          onMarkerClick={handleLocationSelect}
        />
      </div>

      {showList && (
        <div className={`${listClass} bg-white border-l border-gray-200`}>
          <ul className="divide-y divide-gray-100">
            {locations.map((location) => (
              <li
                key={location.id}
                onClick={() => handleLocationSelect(location)}
                className={`p-3 cursor-pointer hover:bg-gray-50 transition-colors ${
                  selectedId === location.id ? 'bg-blue-50' : ''
                }`}
              >
                <h4 className="font-medium text-gray-900">{location.title}</h4>
                {location.description && (
                  <p className="text-sm text-gray-500 mt-1">
                    {location.description}
                  </p>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

// --------------------------------------------------
// 使用例
// --------------------------------------------------

/*
// 基本的な使用法
import { MapWithMarkers, SAMPLE_LOCATIONS } from '@/components/map-with-markers';

export default function MapPage() {
  return (
    <MapWithMarkers
      locations={SAMPLE_LOCATIONS}
      onMarkerClick={(location) => console.log('Selected:', location)}
    />
  );
}

// カスタム InfoWindow
import { MapWithMarkers, MapLocation } from '@/components/map-with-markers';

export default function CustomInfoWindowPage() {
  const renderInfoWindow = (location: MapLocation) => (
    <div className="p-4">
      <h3 className="text-lg font-bold">{location.title}</h3>
      <p className="mt-2">{location.description}</p>
      <button className="mt-3 px-4 py-2 bg-blue-500 text-white rounded">
        詳細を見る
      </button>
    </div>
  );

  return (
    <MapWithMarkers
      locations={SAMPLE_LOCATIONS}
      renderInfoWindow={renderInfoWindow}
    />
  );
}

// リスト付き地図
import { MapWithMarkerList, SAMPLE_LOCATIONS } from '@/components/map-with-markers';

export default function MapWithListPage() {
  return (
    <MapWithMarkerList
      locations={SAMPLE_LOCATIONS}
      showList={true}
      listPosition="right"
    />
  );
}

// カスタムマーカーアイコン
import {
  MapWithMarkers,
  SAMPLE_LOCATIONS,
  createNumberedMarkerIcon,
} from '@/components/map-with-markers';

export default function CustomMarkerPage() {
  const locationsWithIcons = SAMPLE_LOCATIONS.map((loc, index) => ({
    ...loc,
    icon: createNumberedMarkerIcon(index + 1, '#FF5722'),
  }));

  return <MapWithMarkers locations={locationsWithIcons} />;
}
*/
