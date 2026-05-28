// Marker Clusterer Component
// マーカークラスタリングコンポーネント
// TypeScript + React 18+ + Tailwind CSS

'use client';

import { GoogleMap, Marker, MarkerClusterer, InfoWindow } from '@react-google-maps/api';
import { useState, useCallback, useMemo, CSSProperties } from 'react';

// --------------------------------------------------
// 型定義
// --------------------------------------------------

export interface ClusterLocation {
  id: string;
  position: google.maps.LatLngLiteral;
  title: string;
  description?: string;
  category?: string;
}

interface ClusteredMapProps {
  /** マーカーのリスト */
  locations: ClusterLocation[];
  /** 地図の中心座標 */
  center?: google.maps.LatLngLiteral;
  /** ズームレベル */
  zoom?: number;
  /** コンテナのスタイル */
  containerStyle?: CSSProperties;
  /** マーカークリック時のコールバック */
  onMarkerClick?: (location: ClusterLocation) => void;
  /** クラスタリングのグリッドサイズ */
  gridSize?: number;
  /** クラスタリングが無効になるズームレベル */
  maxZoom?: number;
  /** 最小クラスターサイズ */
  minimumClusterSize?: number;
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

// サンプルデータ（100件のランダム位置）
export function generateSampleLocations(count: number = 100): ClusterLocation[] {
  const locations: ClusterLocation[] = [];
  const categories = ['restaurant', 'cafe', 'shop', 'hotel', 'park'];

  for (let i = 0; i < count; i++) {
    locations.push({
      id: `loc-${i}`,
      position: {
        lat: 35.6812 + (Math.random() - 0.5) * 0.1,
        lng: 139.7671 + (Math.random() - 0.5) * 0.1,
      },
      title: `場所 ${i + 1}`,
      description: `説明文 ${i + 1}`,
      category: categories[Math.floor(Math.random() * categories.length)],
    });
  }

  return locations;
}

// --------------------------------------------------
// メインコンポーネント
// --------------------------------------------------

/**
 * マーカークラスタリング付き地図
 *
 * @example
 * <ClusteredMap
 *   locations={locations}
 *   gridSize={60}
 *   maxZoom={15}
 * />
 */
export function ClusteredMap({
  locations,
  center = DEFAULT_CENTER,
  zoom = 11,
  containerStyle = DEFAULT_CONTAINER_STYLE,
  onMarkerClick,
  gridSize = 60,
  maxZoom = 15,
  minimumClusterSize = 2,
}: ClusteredMapProps) {
  const [selectedLocation, setSelectedLocation] = useState<ClusterLocation | null>(null);

  const handleMarkerClick = useCallback(
    (location: ClusterLocation) => {
      setSelectedLocation(location);
      onMarkerClick?.(location);
    },
    [onMarkerClick]
  );

  const handleInfoWindowClose = useCallback(() => {
    setSelectedLocation(null);
  }, []);

  return (
    <GoogleMap
      mapContainerStyle={containerStyle}
      center={center}
      zoom={zoom}
    >
      <MarkerClusterer
        options={{
          gridSize,
          maxZoom,
          minimumClusterSize,
          averageCenter: true,
          zoomOnClick: true,
        }}
      >
        {(clusterer) =>
          locations.map((location) => (
            <Marker
              key={location.id}
              position={location.position}
              title={location.title}
              clusterer={clusterer}
              onClick={() => handleMarkerClick(location)}
            />
          ))
        }
      </MarkerClusterer>

      {selectedLocation && (
        <InfoWindow
          position={selectedLocation.position}
          onCloseClick={handleInfoWindowClose}
        >
          <div className="p-2">
            <h3 className="font-bold">{selectedLocation.title}</h3>
            {selectedLocation.description && (
              <p className="text-sm text-gray-600 mt-1">
                {selectedLocation.description}
              </p>
            )}
            {selectedLocation.category && (
              <span className="inline-block mt-2 px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded">
                {selectedLocation.category}
              </span>
            )}
          </div>
        </InfoWindow>
      )}
    </GoogleMap>
  );
}

// --------------------------------------------------
// カテゴリ別カラーマーカー
// --------------------------------------------------

interface CategoryClusteredMapProps extends ClusteredMapProps {
  categoryColors?: Record<string, string>;
}

/**
 * カテゴリごとに色分けされたクラスタリングマップ
 */
export function CategoryClusteredMap({
  locations,
  categoryColors = {
    restaurant: '#FF5722',
    cafe: '#795548',
    shop: '#2196F3',
    hotel: '#9C27B0',
    park: '#4CAF50',
  },
  ...props
}: CategoryClusteredMapProps) {
  const [selectedLocation, setSelectedLocation] = useState<ClusterLocation | null>(null);

  // カテゴリごとにグループ化
  const groupedLocations = useMemo(() => {
    const groups: Record<string, ClusterLocation[]> = {};

    locations.forEach((location) => {
      const category = location.category || 'other';
      if (!groups[category]) {
        groups[category] = [];
      }
      groups[category].push(location);
    });

    return groups;
  }, [locations]);

  // カテゴリ別マーカーアイコン
  const getCategoryIcon = useCallback(
    (category: string): google.maps.Icon => {
      const color = categoryColors[category] || '#757575';
      return {
        url: `data:image/svg+xml,${encodeURIComponent(`
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="32" height="32">
            <path fill="${color}" d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
          </svg>
        `)}`,
        scaledSize: new google.maps.Size(32, 32),
        anchor: new google.maps.Point(16, 32),
      };
    },
    [categoryColors]
  );

  return (
    <div>
      {/* 凡例 */}
      <div className="mb-2 flex gap-2 flex-wrap">
        {Object.entries(categoryColors).map(([category, color]) => (
          <div key={category} className="flex items-center gap-1">
            <div
              className="w-3 h-3 rounded-full"
              style={{ backgroundColor: color }}
            />
            <span className="text-sm">{category}</span>
          </div>
        ))}
      </div>

      <GoogleMap
        mapContainerStyle={props.containerStyle || DEFAULT_CONTAINER_STYLE}
        center={props.center || DEFAULT_CENTER}
        zoom={props.zoom || 11}
      >
        {Object.entries(groupedLocations).map(([category, locs]) => (
          <MarkerClusterer
            key={category}
            options={{
              gridSize: props.gridSize || 60,
              maxZoom: props.maxZoom || 15,
            }}
          >
            {(clusterer) =>
              locs.map((location) => (
                <Marker
                  key={location.id}
                  position={location.position}
                  title={location.title}
                  icon={getCategoryIcon(category)}
                  clusterer={clusterer}
                  onClick={() => setSelectedLocation(location)}
                />
              ))
            }
          </MarkerClusterer>
        ))}

        {selectedLocation && (
          <InfoWindow
            position={selectedLocation.position}
            onCloseClick={() => setSelectedLocation(null)}
          >
            <div className="p-2">
              <h3 className="font-bold">{selectedLocation.title}</h3>
              <p className="text-sm">{selectedLocation.description}</p>
            </div>
          </InfoWindow>
        )}
      </GoogleMap>
    </div>
  );
}

// --------------------------------------------------
// 統計情報付きクラスタリング
// --------------------------------------------------

interface ClusterStats {
  total: number;
  byCategory: Record<string, number>;
}

interface StatsClusteredMapProps extends ClusteredMapProps {
  onStatsChange?: (stats: ClusterStats) => void;
}

/**
 * 統計情報を表示するクラスタリングマップ
 */
export function StatsClusteredMap({
  locations,
  onStatsChange,
  ...props
}: StatsClusteredMapProps) {
  // 統計情報を計算
  const stats = useMemo(() => {
    const byCategory: Record<string, number> = {};

    locations.forEach((location) => {
      const category = location.category || 'other';
      byCategory[category] = (byCategory[category] || 0) + 1;
    });

    return {
      total: locations.length,
      byCategory,
    };
  }, [locations]);

  // コールバックで通知
  useMemo(() => {
    onStatsChange?.(stats);
  }, [stats, onStatsChange]);

  return (
    <div>
      {/* 統計情報 */}
      <div className="mb-4 p-4 bg-gray-50 rounded-lg">
        <h3 className="font-bold mb-2">統計情報</h3>
        <p className="text-sm">合計: {stats.total} 件</p>
        <div className="mt-2 flex gap-4 flex-wrap">
          {Object.entries(stats.byCategory).map(([category, count]) => (
            <div key={category} className="text-sm">
              <span className="font-medium">{category}:</span> {count}
            </div>
          ))}
        </div>
      </div>

      <ClusteredMap locations={locations} {...props} />
    </div>
  );
}

// --------------------------------------------------
// フィルタリング付きクラスタリング
// --------------------------------------------------

interface FilterableClusteredMapProps extends ClusteredMapProps {
  categories: string[];
}

/**
 * カテゴリでフィルタリング可能なクラスタリングマップ
 */
export function FilterableClusteredMap({
  locations,
  categories,
  ...props
}: FilterableClusteredMapProps) {
  const [selectedCategories, setSelectedCategories] = useState<Set<string>>(
    new Set(categories)
  );

  const toggleCategory = useCallback((category: string) => {
    setSelectedCategories((prev) => {
      const next = new Set(prev);
      if (next.has(category)) {
        next.delete(category);
      } else {
        next.add(category);
      }
      return next;
    });
  }, []);

  const filteredLocations = useMemo(() => {
    return locations.filter((location) => {
      const category = location.category || 'other';
      return selectedCategories.has(category);
    });
  }, [locations, selectedCategories]);

  return (
    <div>
      {/* フィルター */}
      <div className="mb-4 flex gap-2 flex-wrap">
        {categories.map((category) => (
          <button
            key={category}
            onClick={() => toggleCategory(category)}
            className={`px-3 py-1 text-sm rounded-full transition-colors ${
              selectedCategories.has(category)
                ? 'bg-blue-500 text-white'
                : 'bg-gray-200 text-gray-600'
            }`}
          >
            {category}
          </button>
        ))}
      </div>

      <p className="text-sm text-gray-500 mb-2">
        {filteredLocations.length} / {locations.length} 件を表示
      </p>

      <ClusteredMap locations={filteredLocations} {...props} />
    </div>
  );
}

// --------------------------------------------------
// 使用例
// --------------------------------------------------

/*
// 基本的な使用法
import { ClusteredMap, generateSampleLocations } from '@/components/marker-clusterer';

export default function ClusterPage() {
  const locations = useMemo(() => generateSampleLocations(200), []);

  return (
    <ClusteredMap
      locations={locations}
      gridSize={60}
      maxZoom={15}
    />
  );
}

// カテゴリ別
import { CategoryClusteredMap, generateSampleLocations } from '@/components/marker-clusterer';

export default function CategoryPage() {
  const locations = useMemo(() => generateSampleLocations(100), []);

  return (
    <CategoryClusteredMap
      locations={locations}
      categoryColors={{
        restaurant: '#FF5722',
        cafe: '#795548',
        shop: '#2196F3',
      }}
    />
  );
}

// フィルタリング付き
import { FilterableClusteredMap, generateSampleLocations } from '@/components/marker-clusterer';

export default function FilterablePage() {
  const locations = useMemo(() => generateSampleLocations(100), []);
  const categories = ['restaurant', 'cafe', 'shop', 'hotel', 'park'];

  return (
    <FilterableClusteredMap
      locations={locations}
      categories={categories}
    />
  );
}

// 統計情報付き
import { StatsClusteredMap, generateSampleLocations } from '@/components/marker-clusterer';

export default function StatsPage() {
  const locations = useMemo(() => generateSampleLocations(100), []);

  const handleStatsChange = (stats: ClusterStats) => {
    console.log('Stats updated:', stats);
  };

  return (
    <StatsClusteredMap
      locations={locations}
      onStatsChange={handleStatsChange}
    />
  );
}
*/
