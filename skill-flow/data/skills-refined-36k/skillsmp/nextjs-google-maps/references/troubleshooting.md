# トラブルシューティング

## よくあるエラーと解決策

### 1. RefererNotAllowedMapError

**症状**: 地図が表示されず、コンソールに `RefererNotAllowedMapError` が表示される

**原因**: API キーのリファラー制限に、現在のドメインが含まれていない

**解決策**:
1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. 「認証情報」→ API キーを選択
3. 「アプリケーションの制限」→「HTTP リファラー」
4. 以下を追加:
   ```
   localhost:*
   http://localhost:*
   https://localhost:*
   https://your-domain.com/*
   ```

### 2. InvalidKeyMapError

**症状**: 地図が表示されず、`InvalidKeyMapError` が表示される

**原因**: API キーが無効、または期限切れ

**解決策**:
1. API キーが正しくコピーされているか確認
2. 環境変数の設定を確認:
   ```bash
   echo $NEXT_PUBLIC_GOOGLE_MAPS_API_KEY
   ```
3. 必要に応じて新しい API キーを生成

### 3. ApiNotActivatedMapError

**症状**: 特定の機能が動作しない

**原因**: 必要な API が有効化されていない

**解決策**:
1. Google Cloud Console で以下の API を有効化:
   - Maps JavaScript API（必須）
   - Places API（オートコンプリート使用時）
   - Directions API（ルート計算使用時）
   - Geocoding API（住所変換使用時）

### 4. OverQueryLimitMapError

**症状**: 一定回数のリクエスト後にエラー

**原因**: API の使用量制限を超過

**解決策**:
1. 請求先アカウントがリンクされているか確認
2. クォータを増やす（Cloud Console で設定）
3. リクエストをキャッシュして重複を減らす

### 5. SSR/ハイドレーションエラー

**症状**: `window is not defined` または `google is not defined`

**原因**: サーバーサイドで Google Maps API にアクセスしている

**解決策**:

1. コンポーネントに `'use client'` を追加:
   ```tsx
   'use client';

   import { GoogleMap } from '@react-google-maps/api';
   ```

2. Dynamic import を使用:
   ```tsx
   import dynamic from 'next/dynamic';

   const Map = dynamic(
     () => import('@/components/map').then((mod) => mod.Map),
     { ssr: false }
   );
   ```

3. `useEffect` 内で Google オブジェクトを使用:
   ```tsx
   useEffect(() => {
     if (typeof window !== 'undefined' && window.google) {
       // Google Maps API を使用
     }
   }, []);
   ```

### 6. TypeScript エラー: google is not defined

**症状**: TypeScript が `google` 型を認識しない

**解決策**:

1. `@types/google.maps` をインストール:
   ```bash
   npm install -D @types/google.maps
   ```

2. `tsconfig.json` で型を追加:
   ```json
   {
     "compilerOptions": {
       "types": ["google.maps"]
     }
   }
   ```

3. または、グローバル型定義を作成:
   ```tsx
   // types/google-maps.d.ts
   /// <reference types="google.maps" />

   declare global {
     interface Window {
       google: typeof google;
     }
   }

   export {};
   ```

### 7. 地図が正しいサイズで表示されない

**症状**: 地図が小さすぎる、または表示されない

**原因**: コンテナのサイズが設定されていない

**解決策**:

1. 明示的なサイズを設定:
   ```tsx
   <GoogleMap
     mapContainerStyle={{ width: '100%', height: '400px' }}
     ...
   />
   ```

2. CSS クラスを使用:
   ```tsx
   <GoogleMap
     mapContainerClassName="w-full h-[400px]"
     ...
   />
   ```

### 8. マーカーがちらつく/再レンダリングされる

**症状**: マーカーが不必要に再描画される

**原因**: コンポーネントの再レンダリング時に新しいオブジェクトが作成される

**解決策**:

1. 位置情報をメモ化:
   ```tsx
   const center = useMemo(() => ({ lat: 35.6812, lng: 139.7671 }), []);
   ```

2. コールバックをメモ化:
   ```tsx
   const onLoad = useCallback((map: google.maps.Map) => {
     mapRef.current = map;
   }, []);
   ```

3. マーカーのキーを安定させる:
   ```tsx
   {locations.map((loc) => (
     <Marker key={loc.id} position={loc.position} /> // loc.id を使用
   ))}
   ```

### 9. ライブラリが読み込まれない

**症状**: `places` や `drawing` が undefined

**原因**: ライブラリがロードスクリプトで指定されていない

**解決策**:

```tsx
const libraries: Libraries = ['places', 'drawing', 'visualization'];

// コンポーネント外で定義することが重要
const { isLoaded } = useLoadScript({
  googleMapsApiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY!,
  libraries,
});
```

### 10. メモリリーク警告

**症状**: コンソールに「can't perform a React state update on an unmounted component」

**原因**: コンポーネントのアンマウント後に状態を更新している

**解決策**:

```tsx
useEffect(() => {
  let isMounted = true;

  async function fetchData() {
    const result = await someAsyncOperation();
    if (isMounted) {
      setData(result);
    }
  }

  fetchData();

  return () => {
    isMounted = false;
  };
}, []);
```

### 11. Autocomplete の候補が表示されない

**症状**: 入力しても候補が出ない

**原因**: Places API が有効化されていない、または制限が厳しすぎる

**解決策**:

1. Places API が有効か確認
2. 制限を緩和:
   ```tsx
   <Autocomplete
     options={{
       componentRestrictions: { country: 'jp' },
       types: [], // 空配列ですべてのタイプを許可
     }}
   >
   ```

### 12. ビルドエラー: Cannot find module '@react-google-maps/api'

**症状**: ビルド時にモジュールが見つからない

**解決策**:

1. パッケージを再インストール:
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

2. TypeScript のキャッシュをクリア:
   ```bash
   rm -rf .next
   npm run build
   ```

## デバッグ Tips

### API ローディングの確認

```tsx
const { isLoaded, loadError } = useLoadScript({...});

console.log('isLoaded:', isLoaded);
console.log('loadError:', loadError);
```

### Map インスタンスの確認

```tsx
const onLoad = (map: google.maps.Map) => {
  console.log('Map instance:', map);
  console.log('Map center:', map.getCenter()?.toJSON());
  console.log('Map zoom:', map.getZoom());
};
```

### API キーのテスト

```bash
curl "https://maps.googleapis.com/maps/api/geocode/json?address=Tokyo&key=YOUR_API_KEY"
```

## パフォーマンス問題

### 地図が遅い

1. **マーカーの数を減らす**
   - MarkerClusterer を使用
   - ビューポート内のマーカーのみ表示

2. **ポリラインを単純化**
   ```tsx
   // ポイント数を減らす
   const simplifiedPath = google.maps.geometry.encoding.decodePath(
     google.maps.geometry.encoding.encodePath(path)
   );
   ```

3. **イベントリスナーを最適化**
   ```tsx
   // デバウンスを使用
   const handleBoundsChanged = useDebouncedCallback(() => {
     // 処理
   }, 300);
   ```

## 関連リソース

- [Google Maps API エラーコード](https://developers.google.com/maps/documentation/javascript/error-messages)
- [@react-google-maps/api GitHub Issues](https://github.com/JustFly1984/react-google-maps-api/issues)
- [パフォーマンス最適化](performance.md)
