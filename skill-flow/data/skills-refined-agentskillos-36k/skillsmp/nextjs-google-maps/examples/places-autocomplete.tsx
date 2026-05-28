// Places Autocomplete Component
// 場所検索オートコンプリートコンポーネント
// TypeScript + React 18+ + Tailwind CSS

'use client';

import { Autocomplete, GoogleMap, Marker } from '@react-google-maps/api';
import { useCallback, useState, useRef, CSSProperties } from 'react';

// --------------------------------------------------
// 型定義
// --------------------------------------------------

interface PlaceAutocompleteProps {
  /** 場所選択時のコールバック */
  onPlaceSelect?: (place: google.maps.places.PlaceResult) => void;
  /** プレースホルダーテキスト */
  placeholder?: string;
  /** 検索対象の国コード */
  countryRestriction?: string | string[];
  /** 検索タイプ */
  types?: string[];
  /** 入力のスタイル */
  inputClassName?: string;
  /** コンテナのスタイル */
  containerClassName?: string;
  /** 地図を表示するか */
  showMap?: boolean;
  /** 地図のスタイル */
  mapContainerStyle?: CSSProperties;
}

interface SelectedPlace {
  placeId: string;
  name: string;
  address: string;
  position: google.maps.LatLngLiteral;
}

// --------------------------------------------------
// デフォルト値
// --------------------------------------------------

const DEFAULT_MAP_CONTAINER_STYLE: CSSProperties = {
  width: '100%',
  height: '300px',
};

// 東京をデフォルトの中心に
const DEFAULT_CENTER: google.maps.LatLngLiteral = {
  lat: 35.6812,
  lng: 139.7671,
};

// --------------------------------------------------
// コンポーネント
// --------------------------------------------------

/**
 * 場所検索オートコンプリートコンポーネント
 *
 * @example
 * // 基本的な使用法
 * <PlaceAutocomplete
 *   onPlaceSelect={(place) => console.log('Selected:', place)}
 * />
 *
 * @example
 * // 地図付き
 * <PlaceAutocomplete
 *   showMap={true}
 *   countryRestriction="jp"
 *   onPlaceSelect={(place) => console.log('Selected:', place)}
 * />
 */
export function PlaceAutocomplete({
  onPlaceSelect,
  placeholder = '場所を検索...',
  countryRestriction = 'jp',
  types = ['establishment'],
  inputClassName,
  containerClassName,
  showMap = false,
  mapContainerStyle = DEFAULT_MAP_CONTAINER_STYLE,
}: PlaceAutocompleteProps) {
  const [autocomplete, setAutocomplete] = useState<google.maps.places.Autocomplete | null>(null);
  const [selectedPlace, setSelectedPlace] = useState<SelectedPlace | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Autocomplete 読み込み完了時
  const onLoad = useCallback((ac: google.maps.places.Autocomplete) => {
    setAutocomplete(ac);
  }, []);

  // 場所選択時
  const onPlaceChanged = useCallback(() => {
    if (!autocomplete) return;

    const place = autocomplete.getPlace();

    if (place.geometry?.location) {
      const position = {
        lat: place.geometry.location.lat(),
        lng: place.geometry.location.lng(),
      };

      const selected: SelectedPlace = {
        placeId: place.place_id || '',
        name: place.name || '',
        address: place.formatted_address || '',
        position,
      };

      setSelectedPlace(selected);
      onPlaceSelect?.(place);
    }
  }, [autocomplete, onPlaceSelect]);

  // 入力クリア
  const handleClear = useCallback(() => {
    if (inputRef.current) {
      inputRef.current.value = '';
    }
    setSelectedPlace(null);
  }, []);

  return (
    <div className={containerClassName}>
      <div className="relative">
        <Autocomplete
          onLoad={onLoad}
          onPlaceChanged={onPlaceChanged}
          options={{
            componentRestrictions: countryRestriction
              ? { country: countryRestriction }
              : undefined,
            types,
            fields: [
              'place_id',
              'name',
              'formatted_address',
              'geometry',
              'photos',
            ],
          }}
        >
          <input
            ref={inputRef}
            type="text"
            placeholder={placeholder}
            className={
              inputClassName ||
              'w-full px-4 py-2 pr-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none'
            }
          />
        </Autocomplete>

        {/* クリアボタン */}
        {selectedPlace && (
          <button
            onClick={handleClear}
            className="absolute right-2 top-1/2 -translate-y-1/2 p-1 text-gray-400 hover:text-gray-600"
            type="button"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        )}
      </div>

      {/* 選択された場所の情報 */}
      {selectedPlace && (
        <div className="mt-2 p-3 bg-gray-50 rounded-lg">
          <p className="font-medium text-gray-900">{selectedPlace.name}</p>
          <p className="text-sm text-gray-500 mt-1">{selectedPlace.address}</p>
        </div>
      )}

      {/* 地図 */}
      {showMap && (
        <div className="mt-4">
          <GoogleMap
            mapContainerStyle={mapContainerStyle}
            center={selectedPlace?.position || DEFAULT_CENTER}
            zoom={selectedPlace ? 16 : 12}
          >
            {selectedPlace && (
              <Marker
                position={selectedPlace.position}
                title={selectedPlace.name}
              />
            )}
          </GoogleMap>
        </div>
      )}
    </div>
  );
}

// --------------------------------------------------
// 複数地点選択コンポーネント
// --------------------------------------------------

interface MultiPlaceAutocompleteProps {
  /** 場所選択時のコールバック */
  onPlacesChange?: (places: SelectedPlace[]) => void;
  /** 最大選択数 */
  maxPlaces?: number;
  /** プレースホルダーテキスト */
  placeholder?: string;
}

/**
 * 複数の場所を選択できるオートコンプリート
 */
export function MultiPlaceAutocomplete({
  onPlacesChange,
  maxPlaces = 5,
  placeholder = '場所を追加...',
}: MultiPlaceAutocompleteProps) {
  const [places, setPlaces] = useState<SelectedPlace[]>([]);
  const [autocomplete, setAutocomplete] = useState<google.maps.places.Autocomplete | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const onLoad = useCallback((ac: google.maps.places.Autocomplete) => {
    setAutocomplete(ac);
  }, []);

  const onPlaceChanged = useCallback(() => {
    if (!autocomplete) return;

    const place = autocomplete.getPlace();

    if (place.geometry?.location && places.length < maxPlaces) {
      const newPlace: SelectedPlace = {
        placeId: place.place_id || '',
        name: place.name || '',
        address: place.formatted_address || '',
        position: {
          lat: place.geometry.location.lat(),
          lng: place.geometry.location.lng(),
        },
      };

      // 重複チェック
      if (!places.some((p) => p.placeId === newPlace.placeId)) {
        const newPlaces = [...places, newPlace];
        setPlaces(newPlaces);
        onPlacesChange?.(newPlaces);
      }

      // 入力をクリア
      if (inputRef.current) {
        inputRef.current.value = '';
      }
    }
  }, [autocomplete, places, maxPlaces, onPlacesChange]);

  const removePlace = useCallback(
    (placeId: string) => {
      const newPlaces = places.filter((p) => p.placeId !== placeId);
      setPlaces(newPlaces);
      onPlacesChange?.(newPlaces);
    },
    [places, onPlacesChange]
  );

  return (
    <div className="space-y-3">
      {/* 選択された場所のリスト */}
      {places.length > 0 && (
        <ul className="space-y-2">
          {places.map((place, index) => (
            <li
              key={place.placeId}
              className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
            >
              <div className="flex items-center">
                <span className="w-6 h-6 flex items-center justify-center bg-blue-500 text-white text-sm rounded-full mr-3">
                  {index + 1}
                </span>
                <div>
                  <p className="font-medium text-gray-900">{place.name}</p>
                  <p className="text-sm text-gray-500">{place.address}</p>
                </div>
              </div>
              <button
                onClick={() => removePlace(place.placeId)}
                className="p-1 text-gray-400 hover:text-red-500"
                type="button"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </li>
          ))}
        </ul>
      )}

      {/* 入力フィールド */}
      {places.length < maxPlaces && (
        <Autocomplete
          onLoad={onLoad}
          onPlaceChanged={onPlaceChanged}
          options={{
            componentRestrictions: { country: 'jp' },
            types: ['establishment'],
            fields: ['place_id', 'name', 'formatted_address', 'geometry'],
          }}
        >
          <input
            ref={inputRef}
            type="text"
            placeholder={placeholder}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
          />
        </Autocomplete>
      )}

      {places.length >= maxPlaces && (
        <p className="text-sm text-gray-500">
          最大 {maxPlaces} 件まで選択できます
        </p>
      )}
    </div>
  );
}

// --------------------------------------------------
// 住所入力コンポーネント
// --------------------------------------------------

interface AddressAutocompleteProps {
  /** 住所選択時のコールバック */
  onAddressSelect?: (address: ParsedAddress) => void;
  /** プレースホルダーテキスト */
  placeholder?: string;
}

interface ParsedAddress {
  fullAddress: string;
  postalCode?: string;
  prefecture?: string;
  city?: string;
  ward?: string;
  street?: string;
  position: google.maps.LatLngLiteral;
}

/**
 * 住所入力用オートコンプリート
 */
export function AddressAutocomplete({
  onAddressSelect,
  placeholder = '住所を入力...',
}: AddressAutocompleteProps) {
  const [autocomplete, setAutocomplete] = useState<google.maps.places.Autocomplete | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const onLoad = useCallback((ac: google.maps.places.Autocomplete) => {
    setAutocomplete(ac);
  }, []);

  const onPlaceChanged = useCallback(() => {
    if (!autocomplete) return;

    const place = autocomplete.getPlace();

    if (place.geometry?.location && place.address_components) {
      const findComponent = (type: string) =>
        place.address_components?.find((c) => c.types.includes(type));

      const parsed: ParsedAddress = {
        fullAddress: place.formatted_address || '',
        postalCode: findComponent('postal_code')?.long_name,
        prefecture: findComponent('administrative_area_level_1')?.long_name,
        city: findComponent('locality')?.long_name,
        ward: findComponent('sublocality_level_1')?.long_name,
        street: findComponent('route')?.long_name,
        position: {
          lat: place.geometry.location.lat(),
          lng: place.geometry.location.lng(),
        },
      };

      onAddressSelect?.(parsed);
    }
  }, [autocomplete, onAddressSelect]);

  return (
    <Autocomplete
      onLoad={onLoad}
      onPlaceChanged={onPlaceChanged}
      options={{
        componentRestrictions: { country: 'jp' },
        types: ['address'],
        fields: ['formatted_address', 'address_components', 'geometry'],
      }}
    >
      <input
        ref={inputRef}
        type="text"
        placeholder={placeholder}
        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
      />
    </Autocomplete>
  );
}

// --------------------------------------------------
// 使用例
// --------------------------------------------------

/*
// 基本的な使用法
import { PlaceAutocomplete } from '@/components/places-autocomplete';

export default function SearchPage() {
  const handlePlaceSelect = (place: google.maps.places.PlaceResult) => {
    console.log('Selected place:', {
      name: place.name,
      address: place.formatted_address,
      location: place.geometry?.location?.toJSON(),
    });
  };

  return (
    <div className="max-w-md mx-auto p-4">
      <PlaceAutocomplete
        onPlaceSelect={handlePlaceSelect}
        showMap={true}
        placeholder="店舗を検索..."
      />
    </div>
  );
}

// 複数地点選択
import { MultiPlaceAutocomplete } from '@/components/places-autocomplete';

export default function MultiSelectPage() {
  const handlePlacesChange = (places: SelectedPlace[]) => {
    console.log('Selected places:', places);
  };

  return (
    <div className="max-w-md mx-auto p-4">
      <h2 className="text-lg font-bold mb-4">訪問先を追加</h2>
      <MultiPlaceAutocomplete
        onPlacesChange={handlePlacesChange}
        maxPlaces={5}
      />
    </div>
  );
}

// 住所入力フォーム
import { AddressAutocomplete } from '@/components/places-autocomplete';

export default function AddressFormPage() {
  const [address, setAddress] = useState<ParsedAddress | null>(null);

  return (
    <div className="max-w-md mx-auto p-4">
      <label className="block text-sm font-medium mb-2">配送先住所</label>
      <AddressAutocomplete onAddressSelect={setAddress} />

      {address && (
        <div className="mt-4 p-4 bg-gray-50 rounded-lg">
          <p>〒{address.postalCode}</p>
          <p>{address.prefecture} {address.city} {address.ward}</p>
          <p>{address.street}</p>
        </div>
      )}
    </div>
  );
}
*/
