// Google Maps Provider Component
// Next.js App Router 対応の SSR セーフなプロバイダー
// TypeScript + React 18+

'use client';

import { Libraries, useLoadScript } from '@react-google-maps/api';
import { createContext, useContext, ReactNode, useMemo } from 'react';

// ライブラリはコンポーネント外で定数として定義（再レンダリング防止）
const libraries: Libraries = ['places', 'drawing', 'visualization'];

// コンテキストの型定義
interface GoogleMapsContextType {
  isLoaded: boolean;
}

// デフォルト値でコンテキストを作成
const GoogleMapsContext = createContext<GoogleMapsContextType>({
  isLoaded: false
});

// Provider Props の型定義
interface GoogleMapsProviderProps {
  children: ReactNode;
  loadingComponent?: ReactNode;
  errorComponent?: ReactNode;
}

/**
 * Google Maps API をロードし、子コンポーネントに提供する Provider
 *
 * @example
 * // app/map/layout.tsx
 * import { GoogleMapsProvider } from '@/components/google-maps-provider';
 *
 * export default function MapLayout({ children }) {
 *   return (
 *     <GoogleMapsProvider>
 *       {children}
 *     </GoogleMapsProvider>
 *   );
 * }
 */
export function GoogleMapsProvider({
  children,
  loadingComponent,
  errorComponent,
}: GoogleMapsProviderProps) {
  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY!,
    libraries,
  });

  // コンテキスト値をメモ化
  const contextValue = useMemo(() => ({ isLoaded }), [isLoaded]);

  // エラー時の表示
  if (loadError) {
    if (errorComponent) {
      return <>{errorComponent}</>;
    }

    return (
      <div className="flex items-center justify-center p-4 bg-red-50 text-red-600 rounded-lg">
        <svg
          className="w-5 h-5 mr-2"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <span>Google Maps の読み込みに失敗しました</span>
      </div>
    );
  }

  // ローディング中の表示
  if (!isLoaded) {
    if (loadingComponent) {
      return <>{loadingComponent}</>;
    }

    return (
      <div className="flex items-center justify-center p-4 bg-gray-50 rounded-lg">
        <svg
          className="animate-spin w-5 h-5 mr-2 text-blue-500"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
          />
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          />
        </svg>
        <span className="text-gray-600">地図を読み込み中...</span>
      </div>
    );
  }

  return (
    <GoogleMapsContext.Provider value={contextValue}>
      {children}
    </GoogleMapsContext.Provider>
  );
}

/**
 * Google Maps のロード状態を取得する Hook
 *
 * @example
 * function MapComponent() {
 *   const { isLoaded } = useGoogleMapsContext();
 *
 *   if (!isLoaded) {
 *     return <div>Loading...</div>;
 *   }
 *
 *   return <GoogleMap ... />;
 * }
 */
export function useGoogleMapsContext() {
  const context = useContext(GoogleMapsContext);

  if (context === undefined) {
    throw new Error('useGoogleMapsContext must be used within a GoogleMapsProvider');
  }

  return context;
}

// --------------------------------------------------
// カスタムローディング/エラーコンポーネントの使用例
// --------------------------------------------------

/**
 * カスタムローディングコンポーネントの例
 */
export function MapLoadingSkeleton() {
  return (
    <div className="w-full h-[400px] bg-gray-200 animate-pulse rounded-lg flex items-center justify-center">
      <div className="text-gray-400">
        <svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1.5}
            d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"
          />
        </svg>
      </div>
    </div>
  );
}

/**
 * カスタムエラーコンポーネントの例
 */
export function MapLoadError({ onRetry }: { onRetry?: () => void }) {
  return (
    <div className="w-full h-[400px] bg-red-50 rounded-lg flex flex-col items-center justify-center p-4">
      <svg className="w-12 h-12 text-red-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={1.5}
          d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
        />
      </svg>
      <h3 className="text-lg font-semibold text-red-700 mb-2">地図の読み込みに失敗しました</h3>
      <p className="text-red-600 text-sm mb-4 text-center">
        ネットワーク接続を確認するか、しばらく待ってから再試行してください
      </p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
        >
          再試行
        </button>
      )}
    </div>
  );
}

// --------------------------------------------------
// 使用例
// --------------------------------------------------

/*
// app/map/layout.tsx
import { GoogleMapsProvider, MapLoadingSkeleton, MapLoadError } from '@/components/google-maps-provider';

export default function MapLayout({ children }: { children: React.ReactNode }) {
  return (
    <GoogleMapsProvider
      loadingComponent={<MapLoadingSkeleton />}
      errorComponent={<MapLoadError onRetry={() => window.location.reload()} />}
    >
      {children}
    </GoogleMapsProvider>
  );
}

// app/map/page.tsx
'use client';

import { GoogleMap } from '@react-google-maps/api';

export default function MapPage() {
  return (
    <GoogleMap
      mapContainerStyle={{ width: '100%', height: '400px' }}
      center={{ lat: 35.6812, lng: 139.7671 }}
      zoom={15}
    />
  );
}
*/
