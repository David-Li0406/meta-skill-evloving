# Places Autocomplete & Geocoding

## Important: Deprecation Notice

As of **March 1st, 2025**, `google.maps.places.Autocomplete` (the widget) is **not available to new customers**. Use `AutocompleteService` with a custom UI instead.

---

## Custom Places Autocomplete (Recommended)

Build your own autocomplete UI using `AutocompleteService`:

```tsx
// components/place-autocomplete.tsx
import { useState, useEffect, useCallback, useRef } from 'react';
import { useMapsLibrary } from '@vis.gl/react-google-maps';

interface PlaceAutocompleteProps {
  onPlaceSelect: (place: google.maps.places.PlaceResult | null) => void;
  placeholder?: string;
}

export function PlaceAutocomplete({ onPlaceSelect, placeholder = 'Search places...' }: PlaceAutocompleteProps) {
  const placesLib = useMapsLibrary('places');
  const [inputValue, setInputValue] = useState('');
  const [suggestions, setSuggestions] = useState<google.maps.places.AutocompletePrediction[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  
  const autocompleteService = useRef<google.maps.places.AutocompleteService | null>(null);
  const placesService = useRef<google.maps.places.PlacesService | null>(null);
  const sessionToken = useRef<google.maps.places.AutocompleteSessionToken | null>(null);

  // Initialize services
  useEffect(() => {
    if (!placesLib) return;
    
    autocompleteService.current = new placesLib.AutocompleteService();
    // PlacesService needs an element or map - use a dummy div
    const div = document.createElement('div');
    placesService.current = new placesLib.PlacesService(div);
    sessionToken.current = new placesLib.AutocompleteSessionToken();
  }, [placesLib]);

  // Fetch suggestions
  const fetchSuggestions = useCallback(async (input: string) => {
    if (!autocompleteService.current || !input.trim()) {
      setSuggestions([]);
      return;
    }

    try {
      const response = await autocompleteService.current.getPlacePredictions({
        input,
        sessionToken: sessionToken.current!,
        // Optional: bias results
        // componentRestrictions: { country: 'us' },
        // types: ['address'], // or 'establishment', 'geocode', etc.
      });
      
      setSuggestions(response.predictions || []);
      setIsOpen(true);
    } catch (error) {
      console.error('Autocomplete error:', error);
      setSuggestions([]);
    }
  }, []);

  // Debounce input
  useEffect(() => {
    const timer = setTimeout(() => {
      fetchSuggestions(inputValue);
    }, 300);
    
    return () => clearTimeout(timer);
  }, [inputValue, fetchSuggestions]);

  // Handle suggestion selection
  const handleSelect = useCallback((prediction: google.maps.places.AutocompletePrediction) => {
    if (!placesService.current || !placesLib) return;

    // Get full place details
    placesService.current.getDetails(
      {
        placeId: prediction.place_id,
        fields: ['geometry', 'name', 'formatted_address', 'place_id'],
        sessionToken: sessionToken.current!,
      },
      (place, status) => {
        if (status === google.maps.places.PlacesServiceStatus.OK && place) {
          onPlaceSelect(place);
          setInputValue(place.formatted_address || place.name || '');
          setIsOpen(false);
          // Reset session token after selection
          sessionToken.current = new placesLib.AutocompleteSessionToken();
        }
      }
    );
  }, [placesLib, onPlaceSelect]);

  return (
    <div className="relative">
      <input
        type="text"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onFocus={() => suggestions.length > 0 && setIsOpen(true)}
        onBlur={() => setTimeout(() => setIsOpen(false), 200)}
        placeholder={placeholder}
        className="w-full px-4 py-2 border rounded-lg"
      />
      
      {isOpen && suggestions.length > 0 && (
        <ul className="absolute z-50 w-full mt-1 bg-white border rounded-lg shadow-lg max-h-60 overflow-auto">
          {suggestions.map((suggestion) => (
            <li
              key={suggestion.place_id}
              onClick={() => handleSelect(suggestion)}
              className="px-4 py-2 cursor-pointer hover:bg-gray-100"
            >
              <span className="font-medium">
                {suggestion.structured_formatting.main_text}
              </span>
              <span className="text-gray-500 text-sm ml-2">
                {suggestion.structured_formatting.secondary_text}
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

### Usage with Map

```tsx
function MapWithSearch() {
  const [selectedPlace, setSelectedPlace] = useState<google.maps.places.PlaceResult | null>(null);
  const [markerRef, marker] = useAdvancedMarkerRef();

  const position = selectedPlace?.geometry?.location
    ? { lat: selectedPlace.geometry.location.lat(), lng: selectedPlace.geometry.location.lng() }
    : null;

  return (
    <APIProvider apiKey={API_KEY}>
      <div className="flex flex-col gap-4">
        <PlaceAutocomplete onPlaceSelect={setSelectedPlace} />
        
        <Map
          defaultCenter={{ lat: 40.7128, lng: -74.006 }}
          defaultZoom={12}
          mapId="YOUR_MAP_ID"
          style={{ height: '400px' }}
        >
          {position && (
            <AdvancedMarker ref={markerRef} position={position}>
              <Pin />
            </AdvancedMarker>
          )}
        </Map>
      </div>
    </APIProvider>
  );
}
```

---

## Autocomplete with MapControl

Place the autocomplete inside the map:

```tsx
import { MapControl, ControlPosition } from '@vis.gl/react-google-maps';

function MapWithEmbeddedSearch() {
  const map = useMap();
  const [selectedPlace, setSelectedPlace] = useState<google.maps.places.PlaceResult | null>(null);

  // Pan to selected place
  useEffect(() => {
    if (!map || !selectedPlace?.geometry?.location) return;
    map.panTo(selectedPlace.geometry.location);
    map.setZoom(15);
  }, [map, selectedPlace]);

  return (
    <Map {...mapProps}>
      <MapControl position={ControlPosition.TOP}>
        <div className="m-4">
          <PlaceAutocomplete onPlaceSelect={setSelectedPlace} />
        </div>
      </MapControl>
      
      {selectedPlace?.geometry?.location && (
        <AdvancedMarker
          position={{
            lat: selectedPlace.geometry.location.lat(),
            lng: selectedPlace.geometry.location.lng(),
          }}
        />
      )}
    </Map>
  );
}
```

---

## Geocoding

Convert addresses to coordinates and vice versa.

### Address to Coordinates (Geocoding)

```tsx
import { useMapsLibrary } from '@vis.gl/react-google-maps';

function useGeocoder() {
  const geocodingLib = useMapsLibrary('geocoding');
  const [geocoder, setGeocoder] = useState<google.maps.Geocoder | null>(null);

  useEffect(() => {
    if (!geocodingLib) return;
    setGeocoder(new geocodingLib.Geocoder());
  }, [geocodingLib]);

  const geocode = useCallback(async (address: string): Promise<google.maps.LatLngLiteral | null> => {
    if (!geocoder) return null;

    try {
      const response = await geocoder.geocode({ address });
      
      if (response.results.length > 0) {
        const location = response.results[0].geometry.location;
        return { lat: location.lat(), lng: location.lng() };
      }
    } catch (error) {
      console.error('Geocoding error:', error);
    }
    
    return null;
  }, [geocoder]);

  return { geocode, isReady: !!geocoder };
}

// Usage
function AddressSearch() {
  const { geocode, isReady } = useGeocoder();
  const [address, setAddress] = useState('');
  const [result, setResult] = useState<google.maps.LatLngLiteral | null>(null);

  const handleSearch = async () => {
    const coords = await geocode(address);
    if (coords) setResult(coords);
  };

  return (
    <div>
      <input value={address} onChange={(e) => setAddress(e.target.value)} />
      <button onClick={handleSearch} disabled={!isReady}>Search</button>
      {result && <p>Lat: {result.lat}, Lng: {result.lng}</p>}
    </div>
  );
}
```

### Coordinates to Address (Reverse Geocoding)

```tsx
function useReverseGeocoder() {
  const geocodingLib = useMapsLibrary('geocoding');
  const [geocoder, setGeocoder] = useState<google.maps.Geocoder | null>(null);

  useEffect(() => {
    if (!geocodingLib) return;
    setGeocoder(new geocodingLib.Geocoder());
  }, [geocodingLib]);

  const reverseGeocode = useCallback(async (
    latLng: google.maps.LatLngLiteral
  ): Promise<string | null> => {
    if (!geocoder) return null;

    try {
      const response = await geocoder.geocode({ location: latLng });
      
      if (response.results.length > 0) {
        return response.results[0].formatted_address;
      }
    } catch (error) {
      console.error('Reverse geocoding error:', error);
    }
    
    return null;
  }, [geocoder]);

  return { reverseGeocode, isReady: !!geocoder };
}

// Usage: Get address when clicking on map
function ClickToAddress() {
  const { reverseGeocode, isReady } = useReverseGeocoder();
  const [address, setAddress] = useState<string | null>(null);

  const handleMapClick = async (e: google.maps.MapMouseEvent) => {
    if (!e.latLng || !isReady) return;
    
    const result = await reverseGeocode({
      lat: e.latLng.lat(),
      lng: e.latLng.lng(),
    });
    
    setAddress(result);
  };

  return (
    <>
      <Map onClick={handleMapClick} {...mapProps} />
      {address && <p>Address: {address}</p>}
    </>
  );
}
```

---

## Places Details

Get detailed information about a place:

```tsx
function usePlaceDetails() {
  const placesLib = useMapsLibrary('places');
  const serviceRef = useRef<google.maps.places.PlacesService | null>(null);

  useEffect(() => {
    if (!placesLib) return;
    const div = document.createElement('div');
    serviceRef.current = new placesLib.PlacesService(div);
  }, [placesLib]);

  const getPlaceDetails = useCallback(async (
    placeId: string,
    fields: string[] = ['name', 'formatted_address', 'geometry', 'photos', 'rating', 'reviews']
  ): Promise<google.maps.places.PlaceResult | null> => {
    if (!serviceRef.current) return null;

    return new Promise((resolve) => {
      serviceRef.current!.getDetails(
        { placeId, fields },
        (place, status) => {
          if (status === google.maps.places.PlacesServiceStatus.OK) {
            resolve(place);
          } else {
            resolve(null);
          }
        }
      );
    });
  }, []);

  return { getPlaceDetails, isReady: !!serviceRef.current };
}
```

---

## Nearby Search

Find places near a location:

```tsx
function useNearbySearch() {
  const placesLib = useMapsLibrary('places');
  const map = useMap();
  const serviceRef = useRef<google.maps.places.PlacesService | null>(null);

  useEffect(() => {
    if (!placesLib || !map) return;
    serviceRef.current = new placesLib.PlacesService(map);
  }, [placesLib, map]);

  const searchNearby = useCallback(async (
    location: google.maps.LatLngLiteral,
    radius: number,
    type?: string
  ): Promise<google.maps.places.PlaceResult[]> => {
    if (!serviceRef.current) return [];

    return new Promise((resolve) => {
      serviceRef.current!.nearbySearch(
        {
          location,
          radius,
          type: type as string,
        },
        (results, status) => {
          if (status === google.maps.places.PlacesServiceStatus.OK && results) {
            resolve(results);
          } else {
            resolve([]);
          }
        }
      );
    });
  }, []);

  return { searchNearby, isReady: !!serviceRef.current };
}

// Usage
function NearbyRestaurants() {
  const { searchNearby, isReady } = useNearbySearch();
  const [restaurants, setRestaurants] = useState<google.maps.places.PlaceResult[]>([]);

  const findRestaurants = async () => {
    const results = await searchNearby(
      { lat: 40.7128, lng: -74.006 },
      1500, // 1.5km radius
      'restaurant'
    );
    setRestaurants(results);
  };

  return (
    <button onClick={findRestaurants} disabled={!isReady}>
      Find Restaurants
    </button>
  );
}
```

---

## Autocomplete Options Reference

```tsx
const autocompleteOptions: google.maps.places.AutocompletionRequest = {
  input: 'pizza',
  
  // Bias to a location
  locationBias: {
    center: { lat: 40.7128, lng: -74.006 },
    radius: 5000,
  },
  
  // Or restrict to bounds
  locationRestriction: {
    east: -73.9,
    west: -74.1,
    north: 40.8,
    south: 40.6,
  },
  
  // Restrict to countries
  componentRestrictions: { country: ['us', 'ca'] },
  
  // Filter by type
  types: ['address'], // 'establishment', 'geocode', '(cities)', '(regions)'
  
  // Session token (for billing)
  sessionToken: new google.maps.places.AutocompleteSessionToken(),
};
```

### Place Types

- `'address'` - Street addresses
- `'establishment'` - Businesses
- `'geocode'` - Geographic areas
- `'(cities)'` - Cities only
- `'(regions)'` - Administrative regions
