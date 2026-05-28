// Directions Route Component
// ルート計算・表示コンポーネント
// TypeScript + React 18+ + Tailwind CSS

'use client';

import {
  GoogleMap,
  DirectionsService,
  DirectionsRenderer,
} from '@react-google-maps/api';
import { useCallback, useState, CSSProperties } from 'react';

// --------------------------------------------------
// 型定義
// --------------------------------------------------

interface DirectionsMapProps {
  /** 出発地 */
  origin: google.maps.LatLngLiteral | string;
  /** 目的地 */
  destination: google.maps.LatLngLiteral | string;
  /** 経由地 */
  waypoints?: google.maps.DirectionsWaypoint[];
  /** 交通手段 */
  travelMode?: google.maps.TravelMode;
  /** コンテナのスタイル */
  containerStyle?: CSSProperties;
  /** ルート計算完了時のコールバック */
  onDirectionsChange?: (result: google.maps.DirectionsResult | null) => void;
  /** 代替ルートを表示するか */
  showAlternatives?: boolean;
  /** ルート情報パネルを表示するか */
  showRouteInfo?: boolean;
}

interface RouteInfoProps {
  directions: google.maps.DirectionsResult;
  selectedRouteIndex: number;
  onRouteSelect: (index: number) => void;
}

// --------------------------------------------------
// デフォルト値
// --------------------------------------------------

const DEFAULT_CONTAINER_STYLE: CSSProperties = {
  width: '100%',
  height: '400px',
};

// ポリラインのスタイル
const ROUTE_COLORS = {
  primary: '#4285F4',
  alternative: '#9E9E9E',
};

// --------------------------------------------------
// HTML サニタイズ関数
// --------------------------------------------------

/**
 * Google Directions API の instructions をサニタイズ
 * 本番環境では DOMPurify の使用を推奨
 *
 * @example
 * npm install dompurify
 * import DOMPurify from 'dompurify';
 * const clean = DOMPurify.sanitize(html);
 */
function sanitizeInstructions(html: string): string {
  // 基本的なタグのみ許可（b, div, wbr は Directions API で使用される）
  // 本番環境では DOMPurify を使用してください
  return html
    .replace(/<(?!\/?(b|div|wbr)\b)[^>]*>/gi, '')
    .replace(/on\w+="[^"]*"/gi, '');
}

// --------------------------------------------------
// メインコンポーネント
// --------------------------------------------------

/**
 * ルート計算・表示コンポーネント
 *
 * @example
 * <DirectionsMap
 *   origin="東京駅"
 *   destination="渋谷駅"
 *   travelMode={google.maps.TravelMode.DRIVING}
 * />
 */
export function DirectionsMap({
  origin,
  destination,
  waypoints = [],
  travelMode = google.maps.TravelMode.DRIVING,
  containerStyle = DEFAULT_CONTAINER_STYLE,
  onDirectionsChange,
  showAlternatives = false,
  showRouteInfo = true,
}: DirectionsMapProps) {
  const [directions, setDirections] = useState<google.maps.DirectionsResult | null>(null);
  const [selectedRouteIndex, setSelectedRouteIndex] = useState(0);
  const [error, setError] = useState<string | null>(null);

  // ルート計算コールバック
  const directionsCallback = useCallback(
    (
      result: google.maps.DirectionsResult | null,
      status: google.maps.DirectionsStatus
    ) => {
      if (status === google.maps.DirectionsStatus.OK && result) {
        setDirections(result);
        setError(null);
        onDirectionsChange?.(result);
      } else if (status === google.maps.DirectionsStatus.ZERO_RESULTS) {
        setError('この区間のルートが見つかりませんでした');
        setDirections(null);
        onDirectionsChange?.(null);
      } else {
        setError(`ルート計算に失敗しました: ${status}`);
        setDirections(null);
        onDirectionsChange?.(null);
      }
    },
    [onDirectionsChange]
  );

  // デフォルトの中心（東京）
  const defaultCenter = { lat: 35.6812, lng: 139.7671 };

  return (
    <div>
      <GoogleMap
        mapContainerStyle={containerStyle}
        center={defaultCenter}
        zoom={12}
      >
        {/* ルート計算サービス（結果がない場合のみ実行） */}
        {!directions && (
          <DirectionsService
            options={{
              origin,
              destination,
              waypoints,
              travelMode,
              provideRouteAlternatives: showAlternatives,
              optimizeWaypoints: waypoints.length > 0,
            }}
            callback={directionsCallback}
          />
        )}

        {/* ルート表示 */}
        {directions && (
          <DirectionsRenderer
            directions={directions}
            routeIndex={selectedRouteIndex}
            options={{
              polylineOptions: {
                strokeColor: ROUTE_COLORS.primary,
                strokeWeight: 5,
                strokeOpacity: 0.8,
              },
              suppressMarkers: false,
            }}
          />
        )}
      </GoogleMap>

      {/* エラー表示 */}
      {error && (
        <div className="mt-4 p-4 bg-red-50 text-red-700 rounded-lg">
          {error}
        </div>
      )}

      {/* ルート情報パネル */}
      {showRouteInfo && directions && (
        <RouteInfo
          directions={directions}
          selectedRouteIndex={selectedRouteIndex}
          onRouteSelect={setSelectedRouteIndex}
        />
      )}
    </div>
  );
}

// --------------------------------------------------
// ルート情報パネル
// --------------------------------------------------

function RouteInfo({ directions, selectedRouteIndex, onRouteSelect }: RouteInfoProps) {
  const routes = directions.routes;
  const selectedRoute = routes[selectedRouteIndex];
  const leg = selectedRoute.legs[0];

  return (
    <div className="mt-4 bg-white rounded-lg shadow p-4">
      {/* ルート選択（代替ルートがある場合） */}
      {routes.length > 1 && (
        <div className="mb-4">
          <h4 className="text-sm font-medium text-gray-700 mb-2">ルートを選択</h4>
          <div className="flex gap-2 flex-wrap">
            {routes.map((route, index) => (
              <button
                key={index}
                onClick={() => onRouteSelect(index)}
                className={`px-3 py-1.5 text-sm rounded-full transition-colors ${
                  selectedRouteIndex === index
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {route.summary || `ルート ${index + 1}`}
                <span className="ml-1 opacity-75">
                  ({route.legs[0].duration.text})
                </span>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* ルート概要 */}
      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <p className="text-sm text-gray-500">距離</p>
          <p className="text-lg font-semibold">{leg.distance.text}</p>
        </div>
        <div>
          <p className="text-sm text-gray-500">所要時間</p>
          <p className="text-lg font-semibold">{leg.duration.text}</p>
        </div>
      </div>

      {/* 出発地・目的地 */}
      <div className="space-y-2 mb-4">
        <div className="flex items-start">
          <div className="w-6 h-6 rounded-full bg-green-500 flex items-center justify-center text-white text-xs mt-0.5 mr-2">
            A
          </div>
          <div>
            <p className="text-sm font-medium">出発</p>
            <p className="text-sm text-gray-600">{leg.start_address}</p>
          </div>
        </div>
        <div className="flex items-start">
          <div className="w-6 h-6 rounded-full bg-red-500 flex items-center justify-center text-white text-xs mt-0.5 mr-2">
            B
          </div>
          <div>
            <p className="text-sm font-medium">到着</p>
            <p className="text-sm text-gray-600">{leg.end_address}</p>
          </div>
        </div>
      </div>

      {/* 道順（折りたたみ可能） */}
      <details className="group">
        <summary className="cursor-pointer text-sm font-medium text-blue-600 hover:text-blue-700">
          道順を表示
        </summary>
        <ol className="mt-3 space-y-3">
          {leg.steps.map((step, index) => (
            <li key={index} className="flex items-start">
              <span className="w-6 h-6 rounded-full bg-gray-200 flex items-center justify-center text-xs mr-3 mt-0.5">
                {index + 1}
              </span>
              <div>
                {/*
                  Google API からの HTML を表示
                  セキュリティ: 本番環境では DOMPurify でサニタイズを推奨
                */}
                <p
                  className="text-sm"
                  dangerouslySetInnerHTML={{
                    __html: sanitizeInstructions(step.instructions)
                  }}
                />
                <p className="text-xs text-gray-500 mt-1">
                  {step.distance.text} · {step.duration.text}
                </p>
              </div>
            </li>
          ))}
        </ol>
      </details>
    </div>
  );
}

// --------------------------------------------------
// 交通手段選択付きコンポーネント
// --------------------------------------------------

interface DirectionsWithModeSelectProps {
  origin: google.maps.LatLngLiteral | string;
  destination: google.maps.LatLngLiteral | string;
}

export function DirectionsWithModeSelect({
  origin,
  destination,
}: DirectionsWithModeSelectProps) {
  const [travelMode, setTravelMode] = useState<google.maps.TravelMode>(
    google.maps.TravelMode.DRIVING
  );
  const [key, setKey] = useState(0);

  const handleModeChange = (mode: google.maps.TravelMode) => {
    setTravelMode(mode);
    // DirectionsService を再実行するためにキーを更新
    setKey((prev) => prev + 1);
  };

  const modes = [
    { mode: google.maps.TravelMode.DRIVING, icon: '🚗', label: '車' },
    { mode: google.maps.TravelMode.TRANSIT, icon: '🚃', label: '電車' },
    { mode: google.maps.TravelMode.WALKING, icon: '🚶', label: '徒歩' },
    { mode: google.maps.TravelMode.BICYCLING, icon: '🚴', label: '自転車' },
  ];

  return (
    <div>
      {/* 交通手段選択 */}
      <div className="flex gap-2 mb-4">
        {modes.map(({ mode, icon, label }) => (
          <button
            key={mode}
            onClick={() => handleModeChange(mode)}
            className={`flex items-center gap-1 px-4 py-2 rounded-lg transition-colors ${
              travelMode === mode
                ? 'bg-blue-500 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            <span>{icon}</span>
            <span>{label}</span>
          </button>
        ))}
      </div>

      {/* 地図 */}
      <DirectionsMap
        key={key}
        origin={origin}
        destination={destination}
        travelMode={travelMode}
        showAlternatives={true}
      />
    </div>
  );
}

// --------------------------------------------------
// 入力フォーム付きコンポーネント
// --------------------------------------------------

interface DirectionsWithInputProps {
  defaultOrigin?: string;
  defaultDestination?: string;
}

export function DirectionsWithInput({
  defaultOrigin = '',
  defaultDestination = '',
}: DirectionsWithInputProps) {
  const [origin, setOrigin] = useState(defaultOrigin);
  const [destination, setDestination] = useState(defaultDestination);
  const [submittedRoute, setSubmittedRoute] = useState<{
    origin: string;
    destination: string;
  } | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (origin && destination) {
      setSubmittedRoute({ origin, destination });
    }
  };

  return (
    <div>
      {/* 入力フォーム */}
      <form onSubmit={handleSubmit} className="mb-4 space-y-3">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            出発地
          </label>
          <input
            type="text"
            value={origin}
            onChange={(e) => setOrigin(e.target.value)}
            placeholder="例: 東京駅"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            目的地
          </label>
          <input
            type="text"
            value={destination}
            onChange={(e) => setDestination(e.target.value)}
            placeholder="例: 渋谷駅"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <button
          type="submit"
          className="w-full px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
        >
          ルートを検索
        </button>
      </form>

      {/* 地図 */}
      {submittedRoute && (
        <DirectionsWithModeSelect
          origin={submittedRoute.origin}
          destination={submittedRoute.destination}
        />
      )}
    </div>
  );
}

// --------------------------------------------------
// マルチルートコンポーネント
// --------------------------------------------------

interface MultiStopRouteProps {
  stops: string[];
  travelMode?: google.maps.TravelMode;
}

/**
 * 複数の経由地を含むルート
 */
export function MultiStopRoute({
  stops,
  travelMode = google.maps.TravelMode.DRIVING,
}: MultiStopRouteProps) {
  if (stops.length < 2) {
    return <div className="p-4 text-gray-500">2つ以上の地点を指定してください</div>;
  }

  const origin = stops[0];
  const destination = stops[stops.length - 1];
  const waypoints: google.maps.DirectionsWaypoint[] = stops
    .slice(1, -1)
    .map((location) => ({
      location,
      stopover: true,
    }));

  return (
    <DirectionsMap
      origin={origin}
      destination={destination}
      waypoints={waypoints}
      travelMode={travelMode}
    />
  );
}

// --------------------------------------------------
// 使用例
// --------------------------------------------------

/*
// 基本的な使用法
import { DirectionsMap } from '@/components/directions-route';

export default function RoutePage() {
  return (
    <DirectionsMap
      origin="東京駅"
      destination="渋谷駅"
      travelMode={google.maps.TravelMode.DRIVING}
    />
  );
}

// 交通手段選択付き
import { DirectionsWithModeSelect } from '@/components/directions-route';

export default function RouteWithModePage() {
  return (
    <DirectionsWithModeSelect
      origin={{ lat: 35.6812, lng: 139.7671 }}
      destination={{ lat: 35.6586, lng: 139.7454 }}
    />
  );
}

// 入力フォーム付き
import { DirectionsWithInput } from '@/components/directions-route';

export default function RouteInputPage() {
  return (
    <div className="max-w-lg mx-auto p-4">
      <h1 className="text-xl font-bold mb-4">ルート検索</h1>
      <DirectionsWithInput
        defaultOrigin="東京駅"
        defaultDestination="新宿駅"
      />
    </div>
  );
}

// 複数経由地
import { MultiStopRoute } from '@/components/directions-route';

export default function MultiStopPage() {
  const stops = [
    '東京駅',
    '品川駅',
    '渋谷駅',
    '新宿駅',
  ];

  return <MultiStopRoute stops={stops} />;
}
*/
