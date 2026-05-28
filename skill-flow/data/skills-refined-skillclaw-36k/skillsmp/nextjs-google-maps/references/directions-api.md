# Directions API リファレンス

## 概要

Directions API は、2点間または複数地点間のルート計算を提供します。
経由地（ウェイポイント）、交通手段、リアルタイム交通状況にも対応。

## 有効化が必要な API

- Directions API

## 基本コンポーネント

### DirectionsService

ルート計算を実行するコンポーネント。

```tsx
import { DirectionsService } from '@react-google-maps/api';

<DirectionsService
  options={{
    origin: { lat: 35.6812, lng: 139.7671 },
    destination: { lat: 35.6586, lng: 139.7454 },
    travelMode: google.maps.TravelMode.DRIVING,
  }}
  callback={(result, status) => {
    if (status === 'OK' && result) {
      setDirections(result);
    }
  }}
/>
```

### DirectionsRenderer

計算されたルートを地図上に表示。

```tsx
import { DirectionsRenderer } from '@react-google-maps/api';

<DirectionsRenderer
  directions={directions}
  options={{
    polylineOptions: {
      strokeColor: '#4285F4',
      strokeWeight: 5,
    },
  }}
/>
```

## DirectionsRequest オプション

```tsx
interface DirectionsRequest {
  // 出発地（必須）
  origin: google.maps.LatLng | google.maps.LatLngLiteral | string | google.maps.Place;

  // 目的地（必須）
  destination: google.maps.LatLng | google.maps.LatLngLiteral | string | google.maps.Place;

  // 交通手段（必須）
  travelMode: google.maps.TravelMode;

  // 経由地
  waypoints?: google.maps.DirectionsWaypoint[];

  // 経由地の順序を最適化
  optimizeWaypoints?: boolean;

  // 代替ルートを取得
  provideRouteAlternatives?: boolean;

  // 出発時刻（交通状況を考慮）
  departureTime?: Date;

  // 到着時刻
  arrivalTime?: Date;

  // 避けるもの
  avoidFerries?: boolean;
  avoidHighways?: boolean;
  avoidTolls?: boolean;

  // 地域
  region?: string;

  // 単位系
  unitSystem?: google.maps.UnitSystem;

  // 公共交通機関のオプション
  transitOptions?: {
    arrivalTime?: Date;
    departureTime?: Date;
    modes?: google.maps.TransitMode[];
    routingPreference?: google.maps.TransitRoutePreference;
  };

  // ドライブのオプション
  drivingOptions?: {
    departureTime: Date;
    trafficModel?: google.maps.TrafficModel;
  };
}
```

## 交通手段（TravelMode）

| 値 | 説明 |
|-----|------|
| `DRIVING` | 自動車 |
| `WALKING` | 徒歩 |
| `BICYCLING` | 自転車 |
| `TRANSIT` | 公共交通機関 |

```tsx
// 使用例
<DirectionsService
  options={{
    origin: '東京駅',
    destination: '渋谷駅',
    travelMode: google.maps.TravelMode.TRANSIT,
    transitOptions: {
      departureTime: new Date(),
      modes: [
        google.maps.TransitMode.TRAIN,
        google.maps.TransitMode.SUBWAY,
      ],
    },
  }}
  callback={directionsCallback}
/>
```

## 経由地（Waypoints）

```tsx
const waypoints: google.maps.DirectionsWaypoint[] = [
  {
    location: '新宿駅',
    stopover: true, // 経由地点で停車するか
  },
  {
    location: { lat: 35.6586, lng: 139.7454 },
    stopover: false,
  },
];

<DirectionsService
  options={{
    origin: '東京駅',
    destination: '渋谷駅',
    waypoints,
    optimizeWaypoints: true, // 最適な順序に並べ替え
    travelMode: google.maps.TravelMode.DRIVING,
  }}
  callback={directionsCallback}
/>
```

## DirectionsResult の構造

```tsx
interface DirectionsResult {
  // ルート配列（代替ルートを含む場合は複数）
  routes: DirectionsRoute[];

  // ジオコーディングされた経由地
  geocoded_waypoints?: DirectionsGeocodedWaypoint[];

  // リクエスト情報
  request: DirectionsRequest;
}

interface DirectionsRoute {
  // 区間（脚）
  legs: DirectionsLeg[];

  // 概要のポリライン
  overview_polyline: string;

  // 概要のパス
  overview_path: google.maps.LatLng[];

  // 境界
  bounds: google.maps.LatLngBounds;

  // 著作権表示
  copyrights: string;

  // 警告
  warnings: string[];

  // 経由地の順序（最適化された場合）
  waypoint_order: number[];

  // 運賃情報（公共交通機関の場合）
  fare?: {
    currency: string;
    text: string;
    value: number;
  };
}

interface DirectionsLeg {
  // 開始地点
  start_location: google.maps.LatLng;
  start_address: string;

  // 終了地点
  end_location: google.maps.LatLng;
  end_address: string;

  // 距離
  distance: {
    text: string;  // "5.2 km"
    value: number; // 5200 (メートル)
  };

  // 所要時間
  duration: {
    text: string;  // "15分"
    value: number; // 900 (秒)
  };

  // 交通状況を考慮した所要時間
  duration_in_traffic?: {
    text: string;
    value: number;
  };

  // ステップ（道順）
  steps: DirectionsStep[];
}

interface DirectionsStep {
  // 指示（HTML形式）
  instructions: string;

  // 距離
  distance: { text: string; value: number };

  // 所要時間
  duration: { text: string; value: number };

  // 開始・終了地点
  start_location: google.maps.LatLng;
  end_location: google.maps.LatLng;

  // パス
  path: google.maps.LatLng[];

  // 移動手段
  travel_mode: google.maps.TravelMode;

  // 公共交通機関の詳細
  transit?: DirectionsTransitDetails;

  // サブステップ
  steps?: DirectionsStep[];
}
```

## ルート情報の表示

> **セキュリティ注意**: `step.instructions` は Google API から返される HTML です。
> 信頼できるソースですが、本番環境では DOMPurify 等でサニタイズすることを推奨します。

```tsx
import DOMPurify from 'dompurify';

function RouteInfo({ directions }: { directions: google.maps.DirectionsResult }) {
  const route = directions.routes[0];
  const leg = route.legs[0];

  // HTML をサニタイズする関数
  const sanitizeHtml = (html: string) => {
    return DOMPurify.sanitize(html, { ALLOWED_TAGS: ['b', 'div', 'wbr'] });
  };

  return (
    <div className="p-4 bg-white rounded-lg shadow">
      <h3 className="font-bold text-lg mb-2">ルート情報</h3>

      <div className="space-y-2">
        <p>
          <span className="font-medium">出発:</span> {leg.start_address}
        </p>
        <p>
          <span className="font-medium">到着:</span> {leg.end_address}
        </p>
        <p>
          <span className="font-medium">距離:</span> {leg.distance.text}
        </p>
        <p>
          <span className="font-medium">所要時間:</span> {leg.duration.text}
        </p>
      </div>

      <div className="mt-4">
        <h4 className="font-medium mb-2">道順</h4>
        <ol className="list-decimal list-inside space-y-1">
          {leg.steps.map((step, index) => (
            <li
              key={index}
              className="text-sm"
            >
              {/* サニタイズした HTML を使用 */}
              <span dangerouslySetInnerHTML={{ __html: sanitizeHtml(step.instructions) }} />
            </li>
          ))}
        </ol>
      </div>
    </div>
  );
}
```

## 複数ルートの表示

```tsx
function MultiRouteMap({
  origin,
  destination,
}: {
  origin: google.maps.LatLngLiteral;
  destination: google.maps.LatLngLiteral;
}) {
  const [directions, setDirections] = useState<google.maps.DirectionsResult | null>(null);
  const [selectedRouteIndex, setSelectedRouteIndex] = useState(0);

  const directionsCallback = useCallback(
    (result: google.maps.DirectionsResult | null, status: google.maps.DirectionsStatus) => {
      if (status === 'OK' && result) {
        setDirections(result);
      }
    },
    []
  );

  return (
    <>
      <GoogleMap {...mapProps}>
        {!directions && (
          <DirectionsService
            options={{
              origin,
              destination,
              travelMode: google.maps.TravelMode.DRIVING,
              provideRouteAlternatives: true,
            }}
            callback={directionsCallback}
          />
        )}

        {directions && (
          <DirectionsRenderer
            directions={directions}
            routeIndex={selectedRouteIndex}
          />
        )}
      </GoogleMap>

      {/* ルート選択 */}
      {directions && (
        <div className="flex gap-2 mt-4">
          {directions.routes.map((route, index) => (
            <button
              key={index}
              onClick={() => setSelectedRouteIndex(index)}
              className={`px-4 py-2 rounded ${
                selectedRouteIndex === index
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200'
              }`}
            >
              ルート {index + 1} ({route.legs[0].duration.text})
            </button>
          ))}
        </div>
      )}
    </>
  );
}
```

## プログラムによるルート計算

```tsx
async function calculateRoute(
  origin: google.maps.LatLngLiteral,
  destination: google.maps.LatLngLiteral,
  options?: Partial<google.maps.DirectionsRequest>
): Promise<google.maps.DirectionsResult | null> {
  const directionsService = new google.maps.DirectionsService();

  return new Promise((resolve, reject) => {
    directionsService.route(
      {
        origin,
        destination,
        travelMode: google.maps.TravelMode.DRIVING,
        ...options,
      },
      (result, status) => {
        if (status === 'OK' && result) {
          resolve(result);
        } else if (status === 'ZERO_RESULTS') {
          resolve(null);
        } else {
          reject(new Error(`Directions request failed: ${status}`));
        }
      }
    );
  });
}
```

## 交通状況の考慮

```tsx
<DirectionsService
  options={{
    origin: '東京駅',
    destination: '渋谷駅',
    travelMode: google.maps.TravelMode.DRIVING,
    drivingOptions: {
      departureTime: new Date(), // 現在時刻
      trafficModel: google.maps.TrafficModel.BEST_GUESS,
    },
  }}
  callback={directionsCallback}
/>
```

### TrafficModel

| 値 | 説明 |
|-----|------|
| `BEST_GUESS` | 過去のデータに基づく最良推測 |
| `PESSIMISTIC` | 過去の最悪ケース |
| `OPTIMISTIC` | 過去の最良ケース |

## エラーハンドリング

```tsx
const DirectionsStatus = google.maps.DirectionsStatus;

function handleDirectionsError(status: google.maps.DirectionsStatus): string {
  switch (status) {
    case DirectionsStatus.OK:
      return '';
    case DirectionsStatus.NOT_FOUND:
      return '出発地または目的地が見つかりませんでした';
    case DirectionsStatus.ZERO_RESULTS:
      return 'この区間のルートが見つかりませんでした';
    case DirectionsStatus.MAX_WAYPOINTS_EXCEEDED:
      return '経由地が多すぎます（最大25箇所）';
    case DirectionsStatus.MAX_ROUTE_LENGTH_EXCEEDED:
      return 'ルートが長すぎます';
    case DirectionsStatus.INVALID_REQUEST:
      return '無効なリクエストです';
    case DirectionsStatus.OVER_QUERY_LIMIT:
      return 'API 制限を超えました';
    case DirectionsStatus.REQUEST_DENIED:
      return 'リクエストが拒否されました';
    case DirectionsStatus.UNKNOWN_ERROR:
      return 'サーバーエラーが発生しました';
    default:
      return '不明なエラーが発生しました';
  }
}
```

## 料金

| 操作 | 料金（1,000リクエストあたり） |
|------|------------------------------|
| Directions | $5.00 |
| Directions (Advanced) | $10.00 |

**Advanced の条件:**
- 交通状況を考慮する場合
- 10以上の経由地がある場合
- 経由地の最適化を使用する場合

## ベストプラクティス

1. **結果をキャッシュ**
   - 同じルートの結果をキャッシュして重複リクエストを避ける

2. **DirectionsService は一度だけ呼び出す**
   ```tsx
   // 結果が得られたら再リクエストしない
   {!directions && (
     <DirectionsService ... />
   )}
   ```

3. **経由地は最大25箇所**
   - 無料プランでは経由地は最大25箇所

4. **不要なフィールドを省略**
   - サブステップが不要な場合は steps を無視

## 関連リソース

- [Directions API 公式ドキュメント](https://developers.google.com/maps/documentation/directions)
- [ルート表示コード例](../examples/directions-route.tsx)
- [Geocoding API](geocoding-api.md)
