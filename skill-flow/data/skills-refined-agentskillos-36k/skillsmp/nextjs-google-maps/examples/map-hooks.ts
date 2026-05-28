// Map Hooks
// Google Maps 用カスタムフック集
// TypeScript + React 18+

'use client';

import { useState, useEffect, useCallback, useRef } from 'react';

// --------------------------------------------------
// 現在地取得フック
// --------------------------------------------------

interface UseCurrentLocationResult {
  position: google.maps.LatLngLiteral | null;
  error: string | null;
  isLoading: boolean;
  refresh: () => void;
}

interface UseCurrentLocationOptions {
  enableHighAccuracy?: boolean;
  timeout?: number;
  maximumAge?: number;
}

/**
 * 現在地を取得するフック
 *
 * @example
 * const { position, error, isLoading, refresh } = useCurrentLocation();
 *
 * if (isLoading) return <div>位置情報を取得中...</div>;
 * if (error) return <div>エラー: {error}</div>;
 * if (position) return <div>現在地: {position.lat}, {position.lng}</div>;
 */
export function useCurrentLocation(
  options?: UseCurrentLocationOptions
): UseCurrentLocationResult {
  const [position, setPosition] = useState<google.maps.LatLngLiteral | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const getPosition = useCallback(() => {
    if (!navigator.geolocation) {
      setError('お使いのブラウザは位置情報をサポートしていません');
      return;
    }

    setIsLoading(true);
    setError(null);

    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setPosition({
          lat: pos.coords.latitude,
          lng: pos.coords.longitude,
        });
        setIsLoading(false);
      },
      (err) => {
        let message = '位置情報の取得に失敗しました';
        switch (err.code) {
          case err.PERMISSION_DENIED:
            message = '位置情報の許可が拒否されました';
            break;
          case err.POSITION_UNAVAILABLE:
            message = '位置情報を取得できませんでした';
            break;
          case err.TIMEOUT:
            message = '位置情報の取得がタイムアウトしました';
            break;
        }
        setError(message);
        setIsLoading(false);
      },
      {
        enableHighAccuracy: options?.enableHighAccuracy ?? true,
        timeout: options?.timeout ?? 10000,
        maximumAge: options?.maximumAge ?? 0,
      }
    );
  }, [options?.enableHighAccuracy, options?.timeout, options?.maximumAge]);

  useEffect(() => {
    getPosition();
  }, [getPosition]);

  return { position, error, isLoading, refresh: getPosition };
}

// --------------------------------------------------
// 位置追跡フック
// --------------------------------------------------

interface UseWatchPositionResult {
  position: google.maps.LatLngLiteral | null;
  error: string | null;
  isTracking: boolean;
  startTracking: () => void;
  stopTracking: () => void;
}

/**
 * 位置情報を継続的に追跡するフック
 *
 * @example
 * const { position, isTracking, startTracking, stopTracking } = useWatchPosition();
 */
export function useWatchPosition(): UseWatchPositionResult {
  const [position, setPosition] = useState<google.maps.LatLngLiteral | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isTracking, setIsTracking] = useState(false);
  const watchIdRef = useRef<number | null>(null);

  const startTracking = useCallback(() => {
    if (!navigator.geolocation) {
      setError('お使いのブラウザは位置情報をサポートしていません');
      return;
    }

    setIsTracking(true);
    setError(null);

    watchIdRef.current = navigator.geolocation.watchPosition(
      (pos) => {
        setPosition({
          lat: pos.coords.latitude,
          lng: pos.coords.longitude,
        });
      },
      (err) => {
        setError(`位置情報エラー: ${err.message}`);
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 1000,
      }
    );
  }, []);

  const stopTracking = useCallback(() => {
    if (watchIdRef.current !== null) {
      navigator.geolocation.clearWatch(watchIdRef.current);
      watchIdRef.current = null;
    }
    setIsTracking(false);
  }, []);

  useEffect(() => {
    return () => {
      stopTracking();
    };
  }, [stopTracking]);

  return { position, error, isTracking, startTracking, stopTracking };
}

// --------------------------------------------------
// 地図中心座標フック
// --------------------------------------------------

interface UseMapCenterResult {
  center: google.maps.LatLngLiteral;
  setCenter: (center: google.maps.LatLngLiteral) => void;
  panTo: (position: google.maps.LatLngLiteral) => void;
}

/**
 * 地図の中心座標を管理するフック
 *
 * @example
 * const { center, setCenter, panTo } = useMapCenter(map);
 */
export function useMapCenter(
  map: google.maps.Map | null,
  initialCenter: google.maps.LatLngLiteral = { lat: 35.6812, lng: 139.7671 }
): UseMapCenterResult {
  const [center, setCenter] = useState(initialCenter);

  const panTo = useCallback(
    (position: google.maps.LatLngLiteral) => {
      if (map) {
        map.panTo(position);
        setCenter(position);
      }
    },
    [map]
  );

  // 地図の中心が変わったときに状態を更新
  useEffect(() => {
    if (!map) return;

    const listener = map.addListener('center_changed', () => {
      const newCenter = map.getCenter();
      if (newCenter) {
        setCenter({
          lat: newCenter.lat(),
          lng: newCenter.lng(),
        });
      }
    });

    return () => {
      google.maps.event.removeListener(listener);
    };
  }, [map]);

  return { center, setCenter, panTo };
}

// --------------------------------------------------
// 地図境界フック
// --------------------------------------------------

interface UseMapBoundsResult {
  bounds: google.maps.LatLngBounds | null;
  contains: (position: google.maps.LatLngLiteral) => boolean;
  fitBounds: (bounds: google.maps.LatLngBounds | google.maps.LatLngBoundsLiteral) => void;
}

/**
 * 地図の表示範囲（境界）を管理するフック
 *
 * @example
 * const { bounds, contains, fitBounds } = useMapBounds(map);
 */
export function useMapBounds(map: google.maps.Map | null): UseMapBoundsResult {
  const [bounds, setBounds] = useState<google.maps.LatLngBounds | null>(null);

  useEffect(() => {
    if (!map) return;

    const listener = map.addListener('bounds_changed', () => {
      setBounds(map.getBounds() || null);
    });

    return () => {
      google.maps.event.removeListener(listener);
    };
  }, [map]);

  const contains = useCallback(
    (position: google.maps.LatLngLiteral) => {
      return bounds?.contains(position) ?? false;
    },
    [bounds]
  );

  const fitBounds = useCallback(
    (newBounds: google.maps.LatLngBounds | google.maps.LatLngBoundsLiteral) => {
      map?.fitBounds(newBounds);
    },
    [map]
  );

  return { bounds, contains, fitBounds };
}

// --------------------------------------------------
// ズームレベルフック
// --------------------------------------------------

interface UseMapZoomResult {
  zoom: number;
  setZoom: (zoom: number) => void;
  zoomIn: () => void;
  zoomOut: () => void;
}

/**
 * 地図のズームレベルを管理するフック
 *
 * @example
 * const { zoom, setZoom, zoomIn, zoomOut } = useMapZoom(map);
 */
export function useMapZoom(
  map: google.maps.Map | null,
  initialZoom: number = 15
): UseMapZoomResult {
  const [zoom, setZoomState] = useState(initialZoom);

  useEffect(() => {
    if (!map) return;

    const listener = map.addListener('zoom_changed', () => {
      setZoomState(map.getZoom() || initialZoom);
    });

    return () => {
      google.maps.event.removeListener(listener);
    };
  }, [map, initialZoom]);

  const setZoom = useCallback(
    (newZoom: number) => {
      if (map) {
        map.setZoom(newZoom);
        setZoomState(newZoom);
      }
    },
    [map]
  );

  const zoomIn = useCallback(() => {
    setZoom(zoom + 1);
  }, [setZoom, zoom]);

  const zoomOut = useCallback(() => {
    setZoom(zoom - 1);
  }, [setZoom, zoom]);

  return { zoom, setZoom, zoomIn, zoomOut };
}

// --------------------------------------------------
// クリック位置フック
// --------------------------------------------------

interface UseMapClickResult {
  clickedPosition: google.maps.LatLngLiteral | null;
  clearClickedPosition: () => void;
}

/**
 * 地図上のクリック位置を取得するフック
 *
 * @example
 * const { clickedPosition, clearClickedPosition } = useMapClick(map);
 */
export function useMapClick(map: google.maps.Map | null): UseMapClickResult {
  const [clickedPosition, setClickedPosition] = useState<google.maps.LatLngLiteral | null>(null);

  useEffect(() => {
    if (!map) return;

    const listener = map.addListener('click', (e: google.maps.MapMouseEvent) => {
      if (e.latLng) {
        setClickedPosition({
          lat: e.latLng.lat(),
          lng: e.latLng.lng(),
        });
      }
    });

    return () => {
      google.maps.event.removeListener(listener);
    };
  }, [map]);

  const clearClickedPosition = useCallback(() => {
    setClickedPosition(null);
  }, []);

  return { clickedPosition, clearClickedPosition };
}

// --------------------------------------------------
// ジオコーディングフック
// --------------------------------------------------

interface UseGeocodingResult {
  geocode: (address: string) => Promise<google.maps.LatLngLiteral | null>;
  reverseGeocode: (position: google.maps.LatLngLiteral) => Promise<string | null>;
  isLoading: boolean;
  error: string | null;
}

/**
 * ジオコーディングフック
 *
 * @example
 * const { geocode, reverseGeocode, isLoading, error } = useGeocoding();
 * const position = await geocode('東京駅');
 */
export function useGeocoding(): UseGeocodingResult {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const geocoderRef = useRef<google.maps.Geocoder | null>(null);

  // Geocoder インスタンスの遅延初期化
  const getGeocoder = useCallback(() => {
    if (!geocoderRef.current) {
      geocoderRef.current = new google.maps.Geocoder();
    }
    return geocoderRef.current;
  }, []);

  const geocode = useCallback(
    async (address: string): Promise<google.maps.LatLngLiteral | null> => {
      setIsLoading(true);
      setError(null);

      return new Promise((resolve) => {
        getGeocoder().geocode({ address }, (results, status) => {
          setIsLoading(false);

          if (status === 'OK' && results?.[0]) {
            const location = results[0].geometry.location;
            resolve({
              lat: location.lat(),
              lng: location.lng(),
            });
          } else {
            setError(`ジオコーディング失敗: ${status}`);
            resolve(null);
          }
        });
      });
    },
    [getGeocoder]
  );

  const reverseGeocode = useCallback(
    async (position: google.maps.LatLngLiteral): Promise<string | null> => {
      setIsLoading(true);
      setError(null);

      return new Promise((resolve) => {
        getGeocoder().geocode({ location: position }, (results, status) => {
          setIsLoading(false);

          if (status === 'OK' && results?.[0]) {
            resolve(results[0].formatted_address);
          } else {
            setError(`逆ジオコーディング失敗: ${status}`);
            resolve(null);
          }
        });
      });
    },
    [getGeocoder]
  );

  return { geocode, reverseGeocode, isLoading, error };
}

// --------------------------------------------------
// ルート計算フック
// --------------------------------------------------

interface UseDirectionsResult {
  directions: google.maps.DirectionsResult | null;
  calculateRoute: (
    origin: google.maps.LatLngLiteral | string,
    destination: google.maps.LatLngLiteral | string,
    options?: Partial<google.maps.DirectionsRequest>
  ) => Promise<void>;
  clearRoute: () => void;
  isLoading: boolean;
  error: string | null;
}

/**
 * ルート計算フック
 *
 * @example
 * const { directions, calculateRoute, isLoading, error } = useDirections();
 * await calculateRoute('東京駅', '渋谷駅');
 */
export function useDirections(): UseDirectionsResult {
  const [directions, setDirections] = useState<google.maps.DirectionsResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const serviceRef = useRef<google.maps.DirectionsService | null>(null);

  const getService = useCallback(() => {
    if (!serviceRef.current) {
      serviceRef.current = new google.maps.DirectionsService();
    }
    return serviceRef.current;
  }, []);

  const calculateRoute = useCallback(
    async (
      origin: google.maps.LatLngLiteral | string,
      destination: google.maps.LatLngLiteral | string,
      options?: Partial<google.maps.DirectionsRequest>
    ) => {
      setIsLoading(true);
      setError(null);

      getService().route(
        {
          origin,
          destination,
          travelMode: google.maps.TravelMode.DRIVING,
          ...options,
        },
        (result, status) => {
          setIsLoading(false);

          if (status === 'OK' && result) {
            setDirections(result);
          } else {
            setError(`ルート計算失敗: ${status}`);
            setDirections(null);
          }
        }
      );
    },
    [getService]
  );

  const clearRoute = useCallback(() => {
    setDirections(null);
    setError(null);
  }, []);

  return { directions, calculateRoute, clearRoute, isLoading, error };
}

// --------------------------------------------------
// 距離計算フック
// --------------------------------------------------

interface UseDistanceResult {
  calculateDistance: (
    from: google.maps.LatLngLiteral,
    to: google.maps.LatLngLiteral
  ) => number;
  formatDistance: (meters: number) => string;
}

/**
 * 2点間の距離を計算するフック
 *
 * @example
 * const { calculateDistance, formatDistance } = useDistance();
 * const meters = calculateDistance(pointA, pointB);
 * console.log(formatDistance(meters)); // "1.5 km"
 */
export function useDistance(): UseDistanceResult {
  const calculateDistance = useCallback(
    (from: google.maps.LatLngLiteral, to: google.maps.LatLngLiteral) => {
      const fromLatLng = new google.maps.LatLng(from.lat, from.lng);
      const toLatLng = new google.maps.LatLng(to.lat, to.lng);

      return google.maps.geometry.spherical.computeDistanceBetween(fromLatLng, toLatLng);
    },
    []
  );

  const formatDistance = useCallback((meters: number) => {
    if (meters < 1000) {
      return `${Math.round(meters)} m`;
    }
    return `${(meters / 1000).toFixed(1)} km`;
  }, []);

  return { calculateDistance, formatDistance };
}

// --------------------------------------------------
// 使用例
// --------------------------------------------------

/*
// 現在地を表示
import { useCurrentLocation } from '@/hooks/map-hooks';
import { Map } from '@/components/basic-map';
import { Marker } from '@react-google-maps/api';

function CurrentLocationMap() {
  const { position, isLoading, error, refresh } = useCurrentLocation();

  if (isLoading) return <div>位置情報を取得中...</div>;
  if (error) return <div>エラー: {error}</div>;

  return (
    <div>
      <Map center={position || undefined}>
        {position && <Marker position={position} />}
      </Map>
      <button onClick={refresh}>現在地を更新</button>
    </div>
  );
}

// ジオコーディング
import { useGeocoding } from '@/hooks/map-hooks';

function GeocodingExample() {
  const { geocode, reverseGeocode, isLoading } = useGeocoding();
  const [position, setPosition] = useState<google.maps.LatLngLiteral | null>(null);

  const handleSearch = async () => {
    const result = await geocode('東京駅');
    if (result) {
      setPosition(result);
    }
  };

  return (
    <div>
      <button onClick={handleSearch} disabled={isLoading}>
        東京駅を検索
      </button>
      {position && <p>座標: {position.lat}, {position.lng}</p>}
    </div>
  );
}

// ルート計算
import { useDirections } from '@/hooks/map-hooks';
import { GoogleMap, DirectionsRenderer } from '@react-google-maps/api';

function DirectionsExample() {
  const { directions, calculateRoute, isLoading, error } = useDirections();

  useEffect(() => {
    calculateRoute('東京駅', '渋谷駅');
  }, [calculateRoute]);

  return (
    <GoogleMap ...>
      {directions && <DirectionsRenderer directions={directions} />}
    </GoogleMap>
  );
}
*/
