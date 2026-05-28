// Street View Component
// ストリートビューコンポーネント
// TypeScript + React 18+ + Tailwind CSS

'use client';

import { GoogleMap, StreetViewPanorama, Marker } from '@react-google-maps/api';
import { useState, useCallback, useEffect, CSSProperties } from 'react';

// --------------------------------------------------
// 型定義
// --------------------------------------------------

interface StreetViewMapProps {
  /** 表示位置 */
  position: google.maps.LatLngLiteral;
  /** 初期の視点（POV） */
  pov?: {
    heading: number;
    pitch: number;
  };
  /** 初期ズームレベル */
  zoom?: number;
  /** コンテナのスタイル */
  containerStyle?: CSSProperties;
  /** ストリートビューを初期表示するか */
  initiallyVisible?: boolean;
  /** 位置変更時のコールバック */
  onPositionChange?: (position: google.maps.LatLngLiteral) => void;
  /** 視点変更時のコールバック */
  onPovChange?: (pov: { heading: number; pitch: number }) => void;
}

interface StreetViewAvailability {
  isAvailable: boolean;
  nearestPosition?: google.maps.LatLngLiteral;
  description?: string;
}

// --------------------------------------------------
// デフォルト値
// --------------------------------------------------

const DEFAULT_CONTAINER_STYLE: CSSProperties = {
  width: '100%',
  height: '400px',
};

const DEFAULT_POV = {
  heading: 0,
  pitch: 0,
};

// --------------------------------------------------
// メインコンポーネント
// --------------------------------------------------

/**
 * ストリートビュー付き地図コンポーネント
 *
 * @example
 * <StreetViewMap
 *   position={{ lat: 35.6812, lng: 139.7671 }}
 *   initiallyVisible={true}
 * />
 */
export function StreetViewMap({
  position,
  pov = DEFAULT_POV,
  zoom = 1,
  containerStyle = DEFAULT_CONTAINER_STYLE,
  initiallyVisible = false,
  onPositionChange,
  onPovChange,
}: StreetViewMapProps) {
  const [showStreetView, setShowStreetView] = useState(initiallyVisible);
  const [currentPosition, setCurrentPosition] = useState(position);
  const [panorama, setPanorama] = useState<google.maps.StreetViewPanorama | null>(null);

  // パノラマの読み込み完了時
  const onLoad = useCallback((pano: google.maps.StreetViewPanorama) => {
    setPanorama(pano);
  }, []);

  // 位置変更時
  const handlePositionChanged = useCallback(() => {
    if (panorama) {
      const pos = panorama.getPosition();
      if (pos) {
        const newPosition = { lat: pos.lat(), lng: pos.lng() };
        setCurrentPosition(newPosition);
        onPositionChange?.(newPosition);
      }
    }
  }, [panorama, onPositionChange]);

  // 視点変更時
  const handlePovChanged = useCallback(() => {
    if (panorama) {
      const newPov = panorama.getPov();
      onPovChange?.({
        heading: newPov.heading,
        pitch: newPov.pitch,
      });
    }
  }, [panorama, onPovChange]);

  // 地図クリック時
  const handleMapClick = useCallback((e: google.maps.MapMouseEvent) => {
    if (e.latLng) {
      const newPosition = {
        lat: e.latLng.lat(),
        lng: e.latLng.lng(),
      };
      setCurrentPosition(newPosition);
    }
  }, []);

  return (
    <div>
      {/* 表示切り替えボタン */}
      <div className="mb-2 flex gap-2">
        <button
          onClick={() => setShowStreetView(false)}
          className={`px-4 py-2 rounded transition-colors ${
            !showStreetView
              ? 'bg-blue-500 text-white'
              : 'bg-gray-200 text-gray-700'
          }`}
        >
          地図
        </button>
        <button
          onClick={() => setShowStreetView(true)}
          className={`px-4 py-2 rounded transition-colors ${
            showStreetView
              ? 'bg-blue-500 text-white'
              : 'bg-gray-200 text-gray-700'
          }`}
        >
          ストリートビュー
        </button>
      </div>

      <GoogleMap
        mapContainerStyle={containerStyle}
        center={currentPosition}
        zoom={15}
        onClick={handleMapClick}
        options={{
          streetViewControl: true,
        }}
      >
        <StreetViewPanorama
          position={currentPosition}
          visible={showStreetView}
          onLoad={onLoad}
          onPositionChanged={handlePositionChanged}
          onPovChanged={handlePovChanged}
          options={{
            pov,
            zoom,
            addressControl: true,
            fullscreenControl: true,
            linksControl: true,
            panControl: true,
            zoomControl: true,
          }}
        />

        {!showStreetView && (
          <Marker position={currentPosition} />
        )}
      </GoogleMap>

      {/* 現在位置の表示 */}
      <div className="mt-2 text-sm text-gray-500">
        現在位置: {currentPosition.lat.toFixed(6)}, {currentPosition.lng.toFixed(6)}
      </div>
    </div>
  );
}

// --------------------------------------------------
// ストリートビューの可用性チェック
// --------------------------------------------------

/**
 * ストリートビューの可用性をチェック
 */
export async function checkStreetViewAvailability(
  position: google.maps.LatLngLiteral,
  radius: number = 50
): Promise<StreetViewAvailability> {
  const streetViewService = new google.maps.StreetViewService();

  return new Promise((resolve) => {
    streetViewService.getPanorama(
      {
        location: position,
        radius,
        preference: google.maps.StreetViewPreference.NEAREST,
        source: google.maps.StreetViewSource.OUTDOOR,
      },
      (data, status) => {
        if (status === google.maps.StreetViewStatus.OK && data?.location) {
          resolve({
            isAvailable: true,
            nearestPosition: {
              lat: data.location.latLng?.lat() || position.lat,
              lng: data.location.latLng?.lng() || position.lng,
            },
            description: data.location.description || undefined,
          });
        } else {
          resolve({ isAvailable: false });
        }
      }
    );
  });
}

// --------------------------------------------------
// 可用性チェック付きストリートビュー
// --------------------------------------------------

interface SafeStreetViewProps extends Omit<StreetViewMapProps, 'initiallyVisible'> {
  fallbackContent?: React.ReactNode;
}

/**
 * 可用性をチェックしてからストリートビューを表示
 */
export function SafeStreetView({
  position,
  fallbackContent,
  ...props
}: SafeStreetViewProps) {
  const [availability, setAvailability] = useState<StreetViewAvailability | null>(null);
  const [isChecking, setIsChecking] = useState(true);

  useEffect(() => {
    setIsChecking(true);
    checkStreetViewAvailability(position).then((result) => {
      setAvailability(result);
      setIsChecking(false);
    });
  }, [position]);

  if (isChecking) {
    return (
      <div
        style={props.containerStyle || DEFAULT_CONTAINER_STYLE}
        className="flex items-center justify-center bg-gray-100"
      >
        <div className="text-gray-500">ストリートビューを確認中...</div>
      </div>
    );
  }

  if (!availability?.isAvailable) {
    return fallbackContent || (
      <div
        style={props.containerStyle || DEFAULT_CONTAINER_STYLE}
        className="flex items-center justify-center bg-gray-100"
      >
        <div className="text-center">
          <p className="text-gray-500">この場所ではストリートビューを利用できません</p>
          <p className="text-sm text-gray-400 mt-1">
            別の場所を選択してください
          </p>
        </div>
      </div>
    );
  }

  return (
    <StreetViewMap
      {...props}
      position={availability.nearestPosition || position}
      initiallyVisible={true}
    />
  );
}

// --------------------------------------------------
// スプリットビュー（地図とストリートビュー並列表示）
// --------------------------------------------------

interface SplitViewProps {
  position: google.maps.LatLngLiteral;
  containerStyle?: CSSProperties;
}

/**
 * 地図とストリートビューを並べて表示
 */
export function SplitView({ position, containerStyle }: SplitViewProps) {
  const [currentPosition, setCurrentPosition] = useState(position);

  const halfStyle: CSSProperties = {
    width: '50%',
    height: containerStyle?.height || '400px',
  };

  const handleMapClick = useCallback((e: google.maps.MapMouseEvent) => {
    if (e.latLng) {
      setCurrentPosition({
        lat: e.latLng.lat(),
        lng: e.latLng.lng(),
      });
    }
  }, []);

  return (
    <div className="flex" style={containerStyle}>
      {/* 地図 */}
      <GoogleMap
        mapContainerStyle={halfStyle}
        center={currentPosition}
        zoom={15}
        onClick={handleMapClick}
        options={{
          streetViewControl: false,
        }}
      >
        <Marker position={currentPosition} />
      </GoogleMap>

      {/* ストリートビュー */}
      <GoogleMap
        mapContainerStyle={halfStyle}
        center={currentPosition}
        zoom={15}
      >
        <StreetViewPanorama
          position={currentPosition}
          visible={true}
          options={{
            addressControl: true,
            fullscreenControl: true,
          }}
        />
      </GoogleMap>
    </div>
  );
}

// --------------------------------------------------
// 360度ツアー
// --------------------------------------------------

interface TourStop {
  id: string;
  position: google.maps.LatLngLiteral;
  pov: { heading: number; pitch: number };
  title: string;
  description?: string;
}

interface StreetViewTourProps {
  stops: TourStop[];
  containerStyle?: CSSProperties;
  autoPlay?: boolean;
  autoPlayInterval?: number;
}

/**
 * ストリートビューツアー
 */
export function StreetViewTour({
  stops,
  containerStyle = DEFAULT_CONTAINER_STYLE,
  autoPlay = false,
  autoPlayInterval = 5000,
}: StreetViewTourProps) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(autoPlay);

  const currentStop = stops[currentIndex];

  // 自動再生
  useEffect(() => {
    if (!isPlaying) return;

    const timer = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % stops.length);
    }, autoPlayInterval);

    return () => clearInterval(timer);
  }, [isPlaying, stops.length, autoPlayInterval]);

  const goToNext = () => {
    setCurrentIndex((prev) => (prev + 1) % stops.length);
  };

  const goToPrev = () => {
    setCurrentIndex((prev) => (prev - 1 + stops.length) % stops.length);
  };

  return (
    <div>
      <GoogleMap
        mapContainerStyle={containerStyle}
        center={currentStop.position}
        zoom={15}
      >
        <StreetViewPanorama
          position={currentStop.position}
          visible={true}
          options={{
            pov: currentStop.pov,
            addressControl: false,
            linksControl: false,
          }}
        />
      </GoogleMap>

      {/* ツアーコントロール */}
      <div className="mt-4 p-4 bg-white rounded-lg shadow">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-bold text-lg">{currentStop.title}</h3>
          <span className="text-sm text-gray-500">
            {currentIndex + 1} / {stops.length}
          </span>
        </div>

        {currentStop.description && (
          <p className="text-gray-600 mb-4">{currentStop.description}</p>
        )}

        <div className="flex items-center justify-between">
          <button
            onClick={goToPrev}
            className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
          >
            前へ
          </button>

          <button
            onClick={() => setIsPlaying(!isPlaying)}
            className={`px-4 py-2 rounded ${
              isPlaying
                ? 'bg-red-500 text-white'
                : 'bg-green-500 text-white'
            }`}
          >
            {isPlaying ? '停止' : '自動再生'}
          </button>

          <button
            onClick={goToNext}
            className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
          >
            次へ
          </button>
        </div>

        {/* 進捗バー */}
        <div className="mt-4 flex gap-1">
          {stops.map((_, index) => (
            <button
              key={index}
              onClick={() => setCurrentIndex(index)}
              className={`flex-1 h-2 rounded ${
                index === currentIndex ? 'bg-blue-500' : 'bg-gray-200'
              }`}
            />
          ))}
        </div>
      </div>
    </div>
  );
}

// --------------------------------------------------
// 使用例
// --------------------------------------------------

/*
// 基本的な使用法
import { StreetViewMap } from '@/components/street-view';

export default function StreetViewPage() {
  return (
    <StreetViewMap
      position={{ lat: 35.6812, lng: 139.7671 }}
      pov={{ heading: 90, pitch: 0 }}
      initiallyVisible={true}
    />
  );
}

// 可用性チェック付き
import { SafeStreetView } from '@/components/street-view';

export default function SafeStreetViewPage() {
  return (
    <SafeStreetView
      position={{ lat: 35.6812, lng: 139.7671 }}
      fallbackContent={
        <div className="p-4 bg-yellow-50 text-yellow-800">
          ストリートビューは利用できません
        </div>
      }
    />
  );
}

// スプリットビュー
import { SplitView } from '@/components/street-view';

export default function SplitViewPage() {
  return (
    <SplitView
      position={{ lat: 35.6812, lng: 139.7671 }}
      containerStyle={{ height: '500px' }}
    />
  );
}

// ツアー
import { StreetViewTour } from '@/components/street-view';

export default function TourPage() {
  const stops: TourStop[] = [
    {
      id: '1',
      position: { lat: 35.6812, lng: 139.7671 },
      pov: { heading: 0, pitch: 0 },
      title: '東京駅',
      description: '日本最大のターミナル駅',
    },
    {
      id: '2',
      position: { lat: 35.6586, lng: 139.7454 },
      pov: { heading: 180, pitch: 20 },
      title: '東京タワー',
      description: '高さ333mの電波塔',
    },
  ];

  return <StreetViewTour stops={stops} autoPlay={false} />;
}
*/
