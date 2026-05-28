// Heatmap Layer Component
// ヒートマップ表示コンポーネント
// TypeScript + React 18+ + Tailwind CSS

'use client';

import { GoogleMap, HeatmapLayer } from '@react-google-maps/api';
import { useState, useMemo, useCallback, CSSProperties } from 'react';

// --------------------------------------------------
// 型定義
// --------------------------------------------------

interface HeatmapPoint {
  lat: number;
  lng: number;
  weight?: number;
}

interface HeatmapMapProps {
  /** データポイント */
  data: HeatmapPoint[];
  /** 地図の中心座標 */
  center?: google.maps.LatLngLiteral;
  /** ズームレベル */
  zoom?: number;
  /** コンテナのスタイル */
  containerStyle?: CSSProperties;
  /** ヒートマップの半径 */
  radius?: number;
  /** 不透明度 */
  opacity?: number;
  /** カスタムグラデーション */
  gradient?: string[];
  /** コントロールを表示するか */
  showControls?: boolean;
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

// プリセットグラデーション
export const GRADIENT_PRESETS = {
  default: undefined, // Google Maps のデフォルト
  cool: [
    'rgba(0, 255, 255, 0)',
    'rgba(0, 255, 255, 1)',
    'rgba(0, 191, 255, 1)',
    'rgba(0, 127, 255, 1)',
    'rgba(0, 63, 255, 1)',
    'rgba(0, 0, 255, 1)',
  ],
  warm: [
    'rgba(0, 255, 0, 0)',
    'rgba(128, 255, 0, 0.5)',
    'rgba(255, 255, 0, 0.7)',
    'rgba(255, 128, 0, 0.9)',
    'rgba(255, 0, 0, 1)',
  ],
  grayscale: [
    'rgba(128, 128, 128, 0)',
    'rgba(128, 128, 128, 0.5)',
    'rgba(64, 64, 64, 0.8)',
    'rgba(0, 0, 0, 1)',
  ],
  rainbow: [
    'rgba(0, 0, 255, 0)',
    'rgba(0, 255, 255, 0.5)',
    'rgba(0, 255, 0, 0.6)',
    'rgba(255, 255, 0, 0.7)',
    'rgba(255, 128, 0, 0.8)',
    'rgba(255, 0, 0, 1)',
  ],
};

// サンプルデータ
export const SAMPLE_HEATMAP_DATA: HeatmapPoint[] = [
  // 東京駅周辺（高密度）
  { lat: 35.6812, lng: 139.7671, weight: 10 },
  { lat: 35.6815, lng: 139.7675, weight: 8 },
  { lat: 35.6808, lng: 139.7668, weight: 9 },
  { lat: 35.6820, lng: 139.7680, weight: 7 },
  // 渋谷周辺（中密度）
  { lat: 35.6580, lng: 139.7016, weight: 6 },
  { lat: 35.6590, lng: 139.7020, weight: 5 },
  { lat: 35.6575, lng: 139.7010, weight: 4 },
  // 新宿周辺（高密度）
  { lat: 35.6896, lng: 139.7006, weight: 9 },
  { lat: 35.6900, lng: 139.7010, weight: 8 },
  { lat: 35.6892, lng: 139.6998, weight: 7 },
  // 品川周辺（低密度）
  { lat: 35.6284, lng: 139.7387, weight: 3 },
  { lat: 35.6290, lng: 139.7390, weight: 2 },
];

// --------------------------------------------------
// コンポーネント
// --------------------------------------------------

/**
 * ヒートマップ表示コンポーネント
 *
 * @example
 * <HeatmapMap data={heatmapData} radius={30} opacity={0.8} />
 */
export function HeatmapMap({
  data,
  center = DEFAULT_CENTER,
  zoom = 12,
  containerStyle = DEFAULT_CONTAINER_STYLE,
  radius = 20,
  opacity = 0.7,
  gradient,
  showControls = false,
}: HeatmapMapProps) {
  // コントロール用の状態
  const [currentRadius, setCurrentRadius] = useState(radius);
  const [currentOpacity, setCurrentOpacity] = useState(opacity);
  const [currentGradient, setCurrentGradient] = useState<string[] | undefined>(gradient);

  // データを google.maps.LatLng に変換
  const heatmapData = useMemo(() => {
    return data.map((point) => {
      if (point.weight !== undefined) {
        return {
          location: new google.maps.LatLng(point.lat, point.lng),
          weight: point.weight,
        };
      }
      return new google.maps.LatLng(point.lat, point.lng);
    });
  }, [data]);

  return (
    <div>
      <GoogleMap
        mapContainerStyle={containerStyle}
        center={center}
        zoom={zoom}
      >
        <HeatmapLayer
          data={heatmapData}
          options={{
            radius: currentRadius,
            opacity: currentOpacity,
            gradient: currentGradient,
          }}
        />
      </GoogleMap>

      {/* コントロールパネル */}
      {showControls && (
        <HeatmapControls
          radius={currentRadius}
          opacity={currentOpacity}
          onRadiusChange={setCurrentRadius}
          onOpacityChange={setCurrentOpacity}
          onGradientChange={setCurrentGradient}
        />
      )}
    </div>
  );
}

// --------------------------------------------------
// コントロールパネル
// --------------------------------------------------

interface HeatmapControlsProps {
  radius: number;
  opacity: number;
  onRadiusChange: (radius: number) => void;
  onOpacityChange: (opacity: number) => void;
  onGradientChange: (gradient: string[] | undefined) => void;
}

function HeatmapControls({
  radius,
  opacity,
  onRadiusChange,
  onOpacityChange,
  onGradientChange,
}: HeatmapControlsProps) {
  return (
    <div className="mt-4 p-4 bg-white rounded-lg shadow space-y-4">
      {/* 半径 */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          半径: {radius}px
        </label>
        <input
          type="range"
          min="5"
          max="50"
          value={radius}
          onChange={(e) => onRadiusChange(Number(e.target.value))}
          className="w-full"
        />
      </div>

      {/* 不透明度 */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          不透明度: {Math.round(opacity * 100)}%
        </label>
        <input
          type="range"
          min="0"
          max="100"
          value={opacity * 100}
          onChange={(e) => onOpacityChange(Number(e.target.value) / 100)}
          className="w-full"
        />
      </div>

      {/* グラデーション */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          グラデーション
        </label>
        <div className="flex gap-2 flex-wrap">
          {Object.entries(GRADIENT_PRESETS).map(([name, gradient]) => (
            <button
              key={name}
              onClick={() => onGradientChange(gradient)}
              className="px-3 py-1 text-sm bg-gray-100 rounded hover:bg-gray-200"
            >
              {name}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

// --------------------------------------------------
// リアルタイム更新ヒートマップ
// --------------------------------------------------

interface RealTimeHeatmapProps {
  fetchUrl: string;
  refreshInterval?: number;
  containerStyle?: CSSProperties;
}

/**
 * リアルタイム更新ヒートマップ
 */
export function RealTimeHeatmap({
  fetchUrl,
  refreshInterval = 30000,
  containerStyle = DEFAULT_CONTAINER_STYLE,
}: RealTimeHeatmapProps) {
  const [data, setData] = useState<HeatmapPoint[]>([]);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchData = useCallback(async () => {
    try {
      const response = await fetch(fetchUrl);
      const points = await response.json();
      setData(points);
      setLastUpdated(new Date());
    } catch (error) {
      console.error('Failed to fetch heatmap data:', error);
    } finally {
      setIsLoading(false);
    }
  }, [fetchUrl]);

  // 初回読み込みと定期更新
  useState(() => {
    fetchData();
    const interval = setInterval(fetchData, refreshInterval);
    return () => clearInterval(interval);
  });

  if (isLoading) {
    return (
      <div
        style={containerStyle}
        className="flex items-center justify-center bg-gray-100"
      >
        <div className="text-gray-500">データを読み込み中...</div>
      </div>
    );
  }

  return (
    <div>
      <HeatmapMap data={data} containerStyle={containerStyle} />
      {lastUpdated && (
        <p className="text-sm text-gray-500 mt-2">
          最終更新: {lastUpdated.toLocaleTimeString()}
        </p>
      )}
    </div>
  );
}

// --------------------------------------------------
// 時系列ヒートマップ
// --------------------------------------------------

interface TimeSeriesHeatmapProps {
  dataByTime: Record<string, HeatmapPoint[]>;
  containerStyle?: CSSProperties;
}

/**
 * 時系列でデータを切り替えられるヒートマップ
 */
export function TimeSeriesHeatmap({
  dataByTime,
  containerStyle = DEFAULT_CONTAINER_STYLE,
}: TimeSeriesHeatmapProps) {
  const times = Object.keys(dataByTime).sort();
  const [selectedTime, setSelectedTime] = useState(times[0] || '');
  const [isPlaying, setIsPlaying] = useState(false);

  // 自動再生
  useState(() => {
    if (!isPlaying) return;

    const interval = setInterval(() => {
      setSelectedTime((current) => {
        const currentIndex = times.indexOf(current);
        const nextIndex = (currentIndex + 1) % times.length;
        return times[nextIndex];
      });
    }, 1000);

    return () => clearInterval(interval);
  });

  const currentData = dataByTime[selectedTime] || [];

  return (
    <div>
      <HeatmapMap data={currentData} containerStyle={containerStyle} />

      {/* 時間コントロール */}
      <div className="mt-4 flex items-center gap-4">
        <button
          onClick={() => setIsPlaying(!isPlaying)}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          {isPlaying ? '停止' : '再生'}
        </button>

        <select
          value={selectedTime}
          onChange={(e) => setSelectedTime(e.target.value)}
          className="px-3 py-2 border rounded"
        >
          {times.map((time) => (
            <option key={time} value={time}>
              {time}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}

// --------------------------------------------------
// 使用例
// --------------------------------------------------

/*
// 基本的な使用法
import { HeatmapMap, SAMPLE_HEATMAP_DATA } from '@/components/heatmap-layer';

export default function HeatmapPage() {
  return (
    <HeatmapMap
      data={SAMPLE_HEATMAP_DATA}
      radius={25}
      opacity={0.8}
      showControls={true}
    />
  );
}

// カスタムグラデーション
import { HeatmapMap, GRADIENT_PRESETS } from '@/components/heatmap-layer';

export default function CustomGradientPage() {
  return (
    <HeatmapMap
      data={SAMPLE_HEATMAP_DATA}
      gradient={GRADIENT_PRESETS.warm}
    />
  );
}

// リアルタイム更新
import { RealTimeHeatmap } from '@/components/heatmap-layer';

export default function RealTimePage() {
  return (
    <RealTimeHeatmap
      fetchUrl="/api/heatmap-data"
      refreshInterval={10000}
    />
  );
}

// 時系列データ
import { TimeSeriesHeatmap } from '@/components/heatmap-layer';

export default function TimeSeriesPage() {
  const dataByTime = {
    '09:00': [{ lat: 35.6812, lng: 139.7671, weight: 5 }],
    '12:00': [{ lat: 35.6812, lng: 139.7671, weight: 10 }],
    '15:00': [{ lat: 35.6812, lng: 139.7671, weight: 8 }],
    '18:00': [{ lat: 35.6812, lng: 139.7671, weight: 15 }],
  };

  return <TimeSeriesHeatmap dataByTime={dataByTime} />;
}
*/
