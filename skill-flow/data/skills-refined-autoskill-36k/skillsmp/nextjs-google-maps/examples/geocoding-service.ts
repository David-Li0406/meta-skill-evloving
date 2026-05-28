// Geocoding Service
// ジオコーディングユーティリティ
// TypeScript

// --------------------------------------------------
// 型定義
// --------------------------------------------------

export interface GeocodingResult {
  position: google.maps.LatLngLiteral;
  formattedAddress: string;
  placeId: string;
  locationType: google.maps.GeocoderLocationType;
  addressComponents: google.maps.GeocoderAddressComponent[];
}

export interface JapaneseAddress {
  postalCode?: string;
  country?: string;
  prefecture?: string;
  city?: string;
  ward?: string;
  town?: string;
  chome?: string;
  building?: string;
  fullAddress: string;
}

export interface ReverseGeocodingResult {
  address: string;
  placeId: string;
  japaneseAddress: JapaneseAddress;
}

// --------------------------------------------------
// ジオコーディング関数
// --------------------------------------------------

/**
 * 住所を座標に変換（ジオコーディング）
 *
 * @example
 * const result = await geocodeAddress('東京都千代田区丸の内1-9-1');
 * console.log(result.position); // { lat: 35.6812, lng: 139.7671 }
 */
export async function geocodeAddress(
  address: string,
  options?: {
    country?: string;
    region?: string;
  }
): Promise<GeocodingResult | null> {
  const geocoder = new google.maps.Geocoder();

  return new Promise((resolve, reject) => {
    geocoder.geocode(
      {
        address,
        componentRestrictions: options?.country
          ? { country: options.country }
          : undefined,
        region: options?.region,
      },
      (results, status) => {
        if (status === google.maps.GeocoderStatus.OK && results?.[0]) {
          const result = results[0];
          resolve({
            position: {
              lat: result.geometry.location.lat(),
              lng: result.geometry.location.lng(),
            },
            formattedAddress: result.formatted_address,
            placeId: result.place_id,
            locationType: result.geometry.location_type,
            addressComponents: result.address_components,
          });
        } else if (status === google.maps.GeocoderStatus.ZERO_RESULTS) {
          resolve(null);
        } else {
          reject(new Error(`Geocoding failed: ${status}`));
        }
      }
    );
  });
}

/**
 * 座標を住所に変換（逆ジオコーディング）
 *
 * @example
 * const result = await reverseGeocode({ lat: 35.6812, lng: 139.7671 });
 * console.log(result.address); // "日本、〒100-0005 東京都千代田区..."
 */
export async function reverseGeocode(
  location: google.maps.LatLngLiteral
): Promise<ReverseGeocodingResult | null> {
  const geocoder = new google.maps.Geocoder();

  return new Promise((resolve, reject) => {
    geocoder.geocode({ location }, (results, status) => {
      if (status === google.maps.GeocoderStatus.OK && results?.[0]) {
        const result = results[0];
        resolve({
          address: result.formatted_address,
          placeId: result.place_id,
          japaneseAddress: parseJapaneseAddress(result.address_components, result.formatted_address),
        });
      } else if (status === google.maps.GeocoderStatus.ZERO_RESULTS) {
        resolve(null);
      } else {
        reject(new Error(`Reverse geocoding failed: ${status}`));
      }
    });
  });
}

/**
 * 日本の住所コンポーネントを解析
 */
export function parseJapaneseAddress(
  components: google.maps.GeocoderAddressComponent[],
  fullAddress: string
): JapaneseAddress {
  const find = (types: string[]) =>
    components.find((c) => types.some((t) => c.types.includes(t)));

  return {
    postalCode: find(['postal_code'])?.long_name,
    country: find(['country'])?.long_name,
    prefecture: find(['administrative_area_level_1'])?.long_name,
    city: find(['locality'])?.long_name,
    ward: find(['sublocality_level_1'])?.long_name,
    town: find(['sublocality_level_2'])?.long_name,
    chome: find(['sublocality_level_3'])?.long_name,
    building: find(['premise'])?.long_name,
    fullAddress,
  };
}

// --------------------------------------------------
// バッチ処理
// --------------------------------------------------

export interface BatchGeocodingResult {
  address: string;
  result: GeocodingResult | null;
  error?: string;
}

/**
 * 複数の住所を一括でジオコーディング
 *
 * @example
 * const results = await batchGeocode([
 *   '東京都渋谷区渋谷1-1-1',
 *   '東京都新宿区新宿1-1-1',
 * ]);
 */
export async function batchGeocode(
  addresses: string[],
  options?: {
    delayMs?: number;
    country?: string;
    onProgress?: (current: number, total: number) => void;
  }
): Promise<BatchGeocodingResult[]> {
  const { delayMs = 100, country, onProgress } = options || {};
  const results: BatchGeocodingResult[] = [];

  for (let i = 0; i < addresses.length; i++) {
    const address = addresses[i];

    try {
      const result = await geocodeAddress(address, { country });
      results.push({ address, result });
    } catch (error) {
      results.push({
        address,
        result: null,
        error: error instanceof Error ? error.message : '不明なエラー',
      });
    }

    onProgress?.(i + 1, addresses.length);

    // レート制限を避けるための遅延
    if (i < addresses.length - 1) {
      await new Promise((resolve) => setTimeout(resolve, delayMs));
    }
  }

  return results;
}

// --------------------------------------------------
// ユーティリティ
// --------------------------------------------------

/**
 * 2点間の距離を計算（メートル）
 */
export function calculateDistance(
  from: google.maps.LatLngLiteral,
  to: google.maps.LatLngLiteral
): number {
  const fromLatLng = new google.maps.LatLng(from.lat, from.lng);
  const toLatLng = new google.maps.LatLng(to.lat, to.lng);

  return google.maps.geometry.spherical.computeDistanceBetween(fromLatLng, toLatLng);
}

/**
 * 距離を人間が読みやすい形式に変換
 */
export function formatDistance(meters: number): string {
  if (meters < 1000) {
    return `${Math.round(meters)}m`;
  }
  return `${(meters / 1000).toFixed(1)}km`;
}

/**
 * 住所が有効かどうかを検証
 */
export async function validateAddress(
  address: string,
  options?: {
    country?: string;
    requiredLocationType?: google.maps.GeocoderLocationType;
  }
): Promise<{
  isValid: boolean;
  result: GeocodingResult | null;
  message: string;
}> {
  try {
    const result = await geocodeAddress(address, { country: options?.country });

    if (!result) {
      return {
        isValid: false,
        result: null,
        message: '住所が見つかりませんでした',
      };
    }

    // 位置精度のチェック
    if (options?.requiredLocationType) {
      const locationTypes: google.maps.GeocoderLocationType[] = [
        'ROOFTOP',
        'RANGE_INTERPOLATED',
        'GEOMETRIC_CENTER',
        'APPROXIMATE',
      ];

      const requiredIndex = locationTypes.indexOf(options.requiredLocationType);
      const resultIndex = locationTypes.indexOf(result.locationType);

      if (resultIndex > requiredIndex) {
        return {
          isValid: false,
          result,
          message: `住所の精度が不十分です（${result.locationType}）`,
        };
      }
    }

    return {
      isValid: true,
      result,
      message: '有効な住所です',
    };
  } catch (error) {
    return {
      isValid: false,
      result: null,
      message: error instanceof Error ? error.message : '検証に失敗しました',
    };
  }
}

// --------------------------------------------------
// キャッシュ付きジオコーダー
// --------------------------------------------------

class CachedGeocoder {
  private cache = new Map<string, GeocodingResult | null>();
  private maxCacheSize: number;

  constructor(maxCacheSize: number = 100) {
    this.maxCacheSize = maxCacheSize;
  }

  async geocode(
    address: string,
    options?: { country?: string }
  ): Promise<GeocodingResult | null> {
    const cacheKey = `${address}:${options?.country || ''}`;

    if (this.cache.has(cacheKey)) {
      return this.cache.get(cacheKey) || null;
    }

    const result = await geocodeAddress(address, options);

    // キャッシュサイズを超えた場合、最も古いエントリを削除
    if (this.cache.size >= this.maxCacheSize) {
      const firstKey = this.cache.keys().next().value;
      if (firstKey) {
        this.cache.delete(firstKey);
      }
    }

    this.cache.set(cacheKey, result);
    return result;
  }

  clearCache(): void {
    this.cache.clear();
  }

  getCacheSize(): number {
    return this.cache.size;
  }
}

// シングルトンインスタンス
export const cachedGeocoder = new CachedGeocoder();

// --------------------------------------------------
// エラーハンドリング
// --------------------------------------------------

export function getGeocoderErrorMessage(status: google.maps.GeocoderStatus): string {
  const messages: Record<google.maps.GeocoderStatus, string> = {
    [google.maps.GeocoderStatus.OK]: '',
    [google.maps.GeocoderStatus.ZERO_RESULTS]: '住所が見つかりませんでした',
    [google.maps.GeocoderStatus.OVER_QUERY_LIMIT]: 'API 制限を超えました。しばらく待ってから再試行してください',
    [google.maps.GeocoderStatus.REQUEST_DENIED]: 'リクエストが拒否されました。API キーを確認してください',
    [google.maps.GeocoderStatus.INVALID_REQUEST]: '無効なリクエストです',
    [google.maps.GeocoderStatus.UNKNOWN_ERROR]: 'サーバーエラーが発生しました',
    [google.maps.GeocoderStatus.ERROR]: 'リクエストの処理中にエラーが発生しました',
  };

  return messages[status] || '不明なエラーが発生しました';
}

// --------------------------------------------------
// 使用例
// --------------------------------------------------

/*
// 基本的な使用法
import { geocodeAddress, reverseGeocode } from '@/utils/geocoding-service';

async function example() {
  // 住所 → 座標
  const result = await geocodeAddress('東京都千代田区丸の内1-9-1');
  if (result) {
    console.log('座標:', result.position);
    console.log('住所:', result.formattedAddress);
  }

  // 座標 → 住所
  const reverseResult = await reverseGeocode({ lat: 35.6812, lng: 139.7671 });
  if (reverseResult) {
    console.log('住所:', reverseResult.address);
    console.log('都道府県:', reverseResult.japaneseAddress.prefecture);
  }
}

// バッチ処理
import { batchGeocode } from '@/utils/geocoding-service';

async function batchExample() {
  const addresses = [
    '東京都渋谷区渋谷1-1-1',
    '東京都新宿区新宿1-1-1',
    '東京都港区六本木1-1-1',
  ];

  const results = await batchGeocode(addresses, {
    delayMs: 200,
    country: 'jp',
    onProgress: (current, total) => {
      console.log(`Progress: ${current}/${total}`);
    },
  });

  results.forEach(({ address, result, error }) => {
    if (result) {
      console.log(`${address}: ${JSON.stringify(result.position)}`);
    } else {
      console.log(`${address}: エラー - ${error}`);
    }
  });
}

// キャッシュ付き
import { cachedGeocoder } from '@/utils/geocoding-service';

async function cachedExample() {
  // 最初のリクエストは API を呼び出す
  const result1 = await cachedGeocoder.geocode('東京駅');

  // 2回目はキャッシュから取得
  const result2 = await cachedGeocoder.geocode('東京駅');

  console.log('キャッシュサイズ:', cachedGeocoder.getCacheSize());
}

// 住所検証
import { validateAddress } from '@/utils/geocoding-service';

async function validationExample() {
  const { isValid, result, message } = await validateAddress(
    '東京都千代田区丸の内1-9-1',
    {
      country: 'jp',
      requiredLocationType: 'ROOFTOP',
    }
  );

  if (isValid) {
    console.log('有効な住所です:', result?.formattedAddress);
  } else {
    console.log('無効:', message);
  }
}
*/
