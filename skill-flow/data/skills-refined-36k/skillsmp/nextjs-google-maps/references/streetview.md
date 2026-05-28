# ストリートビュー リファレンス

## 概要

Google ストリートビューは、360度のパノラマ画像を表示し、
ユーザーが仮想的に場所を探索できる機能を提供します。

## 基本コンポーネント

### StreetViewPanorama

ストリートビューを表示するコンポーネント。

```tsx
import { StreetViewPanorama } from '@react-google-maps/api';

<GoogleMap ...>
  <StreetViewPanorama
    position={{ lat: 35.6812, lng: 139.7671 }}
    visible={true}
  />
</GoogleMap>
```

### スタンドアロン使用

地図なしでストリートビューのみを表示:

```tsx
import { StreetViewPanorama } from '@react-google-maps/api';

function StandaloneStreetView() {
  return (
    <div style={{ width: '100%', height: '400px' }}>
      <StreetViewPanorama
        containerElement={<div style={{ height: '100%' }} />}
        position={{ lat: 35.6812, lng: 139.7671 }}
        visible={true}
      />
    </div>
  );
}
```

## StreetViewPanorama オプション

```tsx
interface StreetViewPanoramaOptions {
  // 位置
  position: google.maps.LatLngLiteral;

  // 視点（POV: Point of View）
  pov?: {
    heading: number; // 0-360度（北が0）
    pitch: number;   // -90から90度（水平が0）
  };

  // ズームレベル（0-5）
  zoom?: number;

  // 表示状態
  visible?: boolean;

  // コントロールの表示
  addressControl?: boolean;
  fullscreenControl?: boolean;
  linksControl?: boolean;
  panControl?: boolean;
  zoomControl?: boolean;
  enableCloseButton?: boolean;
  motionTracking?: boolean;
  motionTrackingControl?: boolean;

  // コントロールの位置
  addressControlOptions?: {
    position: google.maps.ControlPosition;
  };
}
```

## 視点（POV）の制御

### heading（方角）

```
  0° = 北
 90° = 東
180° = 南
270° = 西
```

### pitch（傾き）

```
-90° = 真下
  0° = 水平
 90° = 真上
```

### 使用例

```tsx
<StreetViewPanorama
  position={{ lat: 35.6812, lng: 139.7671 }}
  visible={true}
  options={{
    pov: {
      heading: 90,  // 東向き
      pitch: 10,    // やや上向き
    },
    zoom: 1,
  }}
/>
```

## イベントハンドリング

```tsx
<StreetViewPanorama
  position={position}
  visible={true}
  onPositionChanged={() => {
    // 位置が変わった
    console.log('Position changed');
  }}
  onPovChanged={() => {
    // 視点が変わった
    console.log('POV changed');
  }}
  onVisibleChanged={() => {
    // 表示/非表示が切り替わった
    console.log('Visibility changed');
  }}
  onZoomChanged={() => {
    // ズームが変わった
    console.log('Zoom changed');
  }}
  onLoad={(panorama) => {
    console.log('Panorama loaded', panorama);
  }}
/>
```

## ストリートビューの可用性チェック

ストリートビューがその場所で利用可能かどうかを確認:

```tsx
async function checkStreetViewAvailability(
  position: google.maps.LatLngLiteral,
  radius: number = 50
): Promise<boolean> {
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
        resolve(status === google.maps.StreetViewStatus.OK);
      }
    );
  });
}

// 使用例
const isAvailable = await checkStreetViewAvailability({ lat: 35.6812, lng: 139.7671 });
if (isAvailable) {
  // ストリートビューを表示
}
```

## 最も近いパノラマを取得

```tsx
async function getNearestPanorama(
  position: google.maps.LatLngLiteral
): Promise<google.maps.StreetViewPanoramaData | null> {
  const streetViewService = new google.maps.StreetViewService();

  return new Promise((resolve) => {
    streetViewService.getPanorama(
      {
        location: position,
        radius: 100,
        preference: google.maps.StreetViewPreference.NEAREST,
      },
      (data, status) => {
        if (status === google.maps.StreetViewStatus.OK && data) {
          resolve(data);
        } else {
          resolve(null);
        }
      }
    );
  });
}

// 使用例
const panorama = await getNearestPanorama({ lat: 35.6812, lng: 139.7671 });
if (panorama) {
  console.log('Panorama ID:', panorama.location?.pano);
  console.log('Description:', panorama.location?.description);
}
```

## 地図との連携

### 地図とストリートビューの切り替え

```tsx
function MapWithStreetViewToggle() {
  const [showStreetView, setShowStreetView] = useState(false);
  const [position, setPosition] = useState<google.maps.LatLngLiteral>({
    lat: 35.6812,
    lng: 139.7671,
  });

  return (
    <div>
      <button onClick={() => setShowStreetView(!showStreetView)}>
        {showStreetView ? '地図を表示' : 'ストリートビューを表示'}
      </button>

      <GoogleMap
        mapContainerStyle={{ width: '100%', height: '400px' }}
        center={position}
        zoom={15}
        onClick={(e) => {
          if (e.latLng) {
            setPosition({
              lat: e.latLng.lat(),
              lng: e.latLng.lng(),
            });
          }
        }}
      >
        <StreetViewPanorama
          position={position}
          visible={showStreetView}
        />

        {!showStreetView && <Marker position={position} />}
      </GoogleMap>
    </div>
  );
}
```

### ペグマン（ストリートビューアイコン）の制御

```tsx
<GoogleMap
  options={{
    streetViewControl: true, // ペグマンを表示
    streetViewControlOptions: {
      position: google.maps.ControlPosition.RIGHT_BOTTOM,
    },
  }}
>
```

## カスタムパノラマ

カスタム画像でストリートビューを作成:

```tsx
function registerCustomPanorama() {
  const customPano = {
    location: {
      pano: 'custom-pano-id',
      description: 'カスタムパノラマ',
      latLng: new google.maps.LatLng(35.6812, 139.7671),
    },
    tiles: {
      tileSize: new google.maps.Size(2048, 1024),
      worldSize: new google.maps.Size(2048, 1024),
      centerHeading: 0,
      getTileUrl: (pano: string, zoom: number, tileX: number, tileY: number) => {
        return `/custom-panorama/${zoom}_${tileX}_${tileY}.jpg`;
      },
    },
  };

  // カスタムパノラマプロバイダーを登録
  // ...
}
```

## StreetViewSource

ストリートビューの画像ソースを指定:

| 値 | 説明 |
|-----|------|
| `DEFAULT` | すべてのソース |
| `OUTDOOR` | 屋外のみ |
| `GOOGLE` | Google が撮影した画像のみ |

```tsx
streetViewService.getPanorama({
  location: position,
  source: google.maps.StreetViewSource.OUTDOOR,
});
```

## エラーハンドリング

```tsx
const StreetViewStatus = google.maps.StreetViewStatus;

function handleStreetViewError(status: google.maps.StreetViewStatus): string {
  switch (status) {
    case StreetViewStatus.OK:
      return '';
    case StreetViewStatus.ZERO_RESULTS:
      return 'この場所にストリートビューはありません';
    case StreetViewStatus.UNKNOWN_ERROR:
      return 'ストリートビューの読み込みに失敗しました';
    default:
      return '不明なエラーが発生しました';
  }
}
```

## モバイル対応

### タッチジェスチャー

```tsx
<StreetViewPanorama
  position={position}
  visible={true}
  options={{
    // モバイル向け設定
    motionTracking: true, // デバイスの動きに追従
    motionTrackingControl: true, // モーショントラッキングボタン
    panControl: true, // パンコントロール
    zoomControl: true, // ズームコントロール
  }}
/>
```

### モーショントラッキング

デバイスの傾きに応じて視点を変更:

```tsx
<StreetViewPanorama
  options={{
    motionTracking: true,
    motionTrackingControl: true,
    motionTrackingControlOptions: {
      position: google.maps.ControlPosition.LEFT_BOTTOM,
    },
  }}
/>
```

## パフォーマンス

1. **必要な時だけ読み込む**
   ```tsx
   {showStreetView && (
     <StreetViewPanorama position={position} visible={true} />
   )}
   ```

2. **可用性を事前にチェック**
   - ストリートビューが利用できない場所ではボタンを無効化

3. **適切な解像度を使用**
   - モバイルでは低解像度で十分な場合がある

## 関連リソース

- [ストリートビューコード例](../examples/street-view.tsx)
- [Google Maps Platform ドキュメント](https://developers.google.com/maps/documentation/javascript/streetview)
