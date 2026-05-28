---
name: Poker Near Me
description: Location-based poker room discovery and live game tracking
---

# Poker Near Me Skill

## Overview
Help users find live poker games near them using geolocation and a comprehensive venue database.

## Database Schema
```sql
CREATE TABLE poker_venues (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  address TEXT,
  city TEXT,
  state TEXT,
  country TEXT,
  latitude DECIMAL(10, 8),
  longitude DECIMAL(11, 8),
  phone TEXT,
  website TEXT,
  hours JSONB, -- {"mon": "10:00-02:00", ...}
  games_offered TEXT[], -- ['NLH', 'PLO', 'Mixed']
  stakes_available TEXT[], -- ['1/2', '2/5', '5/10']
  has_tournaments BOOLEAN DEFAULT TRUE,
  rating DECIMAL(2, 1),
  review_count INTEGER DEFAULT 0,
  image_url TEXT,
  is_verified BOOLEAN DEFAULT FALSE
);

CREATE TABLE live_games (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  venue_id UUID REFERENCES poker_venues(id),
  game_type TEXT,
  stakes TEXT,
  seats_available INTEGER,
  waiting_list INTEGER,
  reported_at TIMESTAMPTZ DEFAULT NOW(),
  reported_by UUID REFERENCES auth.users(id)
);

-- PostGIS for location queries
CREATE EXTENSION IF NOT EXISTS postgis;
ALTER TABLE poker_venues ADD COLUMN location GEOGRAPHY(POINT, 4326);
UPDATE poker_venues SET location = ST_MakePoint(longitude, latitude);
```

## Nearby Search
```javascript
async function findNearbyPokerRooms(lat, lng, radiusMiles = 50) {
  const radiusMeters = radiusMiles * 1609.34;
  
  const { data } = await supabase.rpc('find_nearby_venues', {
    lat,
    lng,
    radius: radiusMeters
  });
  
  return data;
}

// SQL Function
CREATE OR REPLACE FUNCTION find_nearby_venues(lat FLOAT, lng FLOAT, radius FLOAT)
RETURNS TABLE (
  id UUID,
  name TEXT,
  address TEXT,
  distance_miles FLOAT,
  games_offered TEXT[],
  stakes_available TEXT[]
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    pv.id,
    pv.name,
    pv.address,
    ST_Distance(pv.location, ST_MakePoint(lng, lat)::geography) / 1609.34 as distance_miles,
    pv.games_offered,
    pv.stakes_available
  FROM poker_venues pv
  WHERE ST_DWithin(pv.location, ST_MakePoint(lng, lat)::geography, radius)
  ORDER BY distance_miles;
END;
$$ LANGUAGE plpgsql;
```

## Live Game Reporting
```javascript
async function reportLiveGame(venueId, userId, gameInfo) {
  await supabase.from('live_games').insert({
    venue_id: venueId,
    game_type: gameInfo.gameType,
    stakes: gameInfo.stakes,
    seats_available: gameInfo.seats,
    waiting_list: gameInfo.waitlist,
    reported_by: userId
  });
}
```

## Map Integration
```jsx
import { GoogleMap, Marker, InfoWindow } from '@react-google-maps/api';

function PokerMap({ venues, center }) {
  const [selected, setSelected] = useState(null);
  
  return (
    <GoogleMap
      center={center}
      zoom={10}
      mapContainerStyle={{ width: '100%', height: '400px' }}
    >
      {venues.map(venue => (
        <Marker
          key={venue.id}
          position={{ lat: venue.latitude, lng: venue.longitude }}
          onClick={() => setSelected(venue)}
          icon="/icons/poker-chip-marker.png"
        />
      ))}
      
      {selected && (
        <InfoWindow
          position={{ lat: selected.latitude, lng: selected.longitude }}
          onCloseClick={() => setSelected(null)}
        >
          <VenueCard venue={selected} />
        </InfoWindow>
      )}
    </GoogleMap>
  );
}
```

## Components
- `PokerNearMe.jsx` - Main page with map + list
- `VenueCard.jsx` - Venue summary
- `VenueDetail.jsx` - Full venue page
- `LiveGamesFeed.jsx` - Real-time game reports
- `ReportGameModal.jsx` - Submit game info
- `FilterPanel.jsx` - Filter by stakes/game type
