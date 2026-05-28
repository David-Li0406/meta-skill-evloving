---
name: map-feature
description: Guide for the Map page feature (Kakao Maps integration, location search, store category filtering). Use when working on map components, search bar, bottom sheet, detail sheet, store/pickup filters, or Kakao Map API integration. Triggers on "map", "kakao map", "location search", "store category", "bottom sheet", "map marker", "nearby", "autocomplete", "suggest".
---

# Map Feature Guide

## File Structure

```
src/
├── pages/Map/
│   └── Map.tsx                      # Main map page (state management)
│
├── components/map/
│   ├── MapSearchBar.tsx             # Search input + autocomplete dropdown
│   ├── MapCard.tsx                  # Location card in bottom sheet
│   ├── MapDetailSheet.tsx           # Location detail bottom sheet
│   ├── MapView.tsx                  # Kakao Map markers + overlays
│   ├── MapFloatingView.tsx          # Source toggle (keco/zerowaste/all)
│   └── bottomSheet/
│       ├── MapBottomSheet.tsx       # Bottom sheet container
│       ├── StoreCategoryFilter.tsx  # Store category filter UI
│       └── FilterContent.tsx        # Pickup category filter
│
├── api/services/map/
│   ├── map.service.ts               # API client (MapService class)
│   ├── map.type.ts                  # TypeScript types + STORE_CATEGORIES
│   └── map.queries.ts               # React Query options
│
└── hooks/
    └── useKakaoLoaderOrigin.tsx      # Kakao Maps SDK loader
```

## Data Flow

```
Map.tsx (state owner)
  ├── useQuery(MapQueries.getLocations) → MapService.getLocations()
  ├── MapSearchBar → MapService.suggestPlaces() / searchLocations()
  ├── MapBottomSheet → MapCard[] → handleSetSelectedId()
  ├── MapDetailSheet → MapService.getLocationDetail()
  ├── MapView → kakao.maps.Map + MapMarker[]
  └── StoreCategoryFilter → selectedStoreCategories state
```

## Key State

```typescript
// Map.tsx
const [center, setCenter] = useState({ lat, lng });     // Map center
const [mapZoom, setMapZoom] = useState(3);               // Zoom level
const [selectedId, setSelectedId] = useState<number | null>(null);
const [selectedStoreCategories, setSelectedStoreCategories] = useState<string[]>([]);
const [searchResults, setSearchResults] = useState<LocationListResponse | null>(null);
const [toggle, setToggle] = useState<ToggleType>('all'); // Source filter
```

## API Types

```typescript
// LocationListRequest
{ lat, lon, radius?, zoom?, store_category?, pickup_category? }

// LocationListItemResponse
{ id, name, source, road_address?, latitude, longitude, distance_km?,
  distance_text?, store_category?, is_open?, is_holiday?,
  start_time?, end_time?, phone?, pickup_categories?, place_url?, kakao_place_id? }

// SuggestEntry
{ place_name, address, latitude, longitude, place_url? }

// LocationDetailResponse
{ id, name, source, road_address?, lot_address?, latitude?, longitude?,
  store_category, pickup_categories, phone?, place_url?, kakao_place_id?,
  collection_items?, introduction? }
```

## Store Categories

```typescript
const STORE_CATEGORIES = [
  { key: 'refill_zero', label: '제로웨이스트' },
  { key: 'cafe_bakery', label: '카페/베이커리' },
  { key: 'vegan_dining', label: '비건/식당' },
  { key: 'upcycle_recycle', label: '업사이클/재활용' },
  { key: 'book_workshop', label: '도서관/공방' },
  { key: 'market_mart', label: '마트/시장' },
  { key: 'lodging', label: '숙박' },
  { key: 'public_dropbox', label: '무인 수거함' },
  { key: 'general', label: '기타' },
];
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `VITE_KAKAO_MAP_API_KEY` | Kakao Maps JavaScript SDK key |
| `VITE_API_BASE_URL` | Backend API base URL |

## Kakao Map Integration

- SDK loader: `useKakaoLoaderOrigin` hook (loads `react-kakao-maps-sdk`)
- Map component: `<Map>` from `react-kakao-maps-sdk`
- Markers: `<MapMarker>` with custom overlay
- Pan/zoom events: `onCenterChanged`, `onZoomChanged`

## Common Patterns

### Search flow
1. User types in MapSearchBar
2. Debounce (300ms) → `MapService.suggestPlaces(q)`
3. Show dropdown with SuggestEntry[]
4. User selects → pan map to coordinates + `MapService.searchLocations()`

### Filter flow
1. User opens StoreCategoryFilter
2. Toggle categories → temporary state
3. "결과보기" button → `setSelectedStoreCategories()`
4. useEffect triggers `refetch()` with new `store_category` param

### Detail flow
1. User taps MapCard
2. `setSelectedId(id)` → MapDetailSheet opens
3. `MapService.getLocationDetail(id)` → show detail

### Directions
```typescript
// Opens Kakao Map directions in new tab
window.open(`https://map.kakao.com/link/to/${name},${lat},${lng}`)
```

## Known Issues

1. **Query key caching**: `MapQueries.getLocations` uses static query key — different map positions return cached data
2. **Multiple refetch effects**: Three `useEffect` hooks call `refetch()` with different conditions
3. **MapView marker key**: Uses array index instead of item ID
4. **Silent error handling**: MapDetailSheet/MapSearchBar swallow API errors
