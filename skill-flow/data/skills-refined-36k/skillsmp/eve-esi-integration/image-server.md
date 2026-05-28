# EVE Image Server Reference

The image server provides renders, icons, portraits, and logos for EVE Online entities.

## Base URL

```
https://images.evetech.net/
```

## URL Format

```
https://images.evetech.net/{category}/{id}/{variation}?size={size}
```

## Categories

### Types (Ships, Modules, Items)

| Variation | Description | Best For |
|-----------|-------------|----------|
| `render` | 3D render with transparency | Game sprites, previews |
| `icon` | Inventory icon | UI elements, lists |
| `bp` | Blueprint icon | Industry apps |
| `bpc` | Blueprint copy icon | Industry apps |
| `relicicon` | Relic variation | Exploration apps |

Examples:
```
https://images.evetech.net/types/587/render?size=512     # Rifter 3D render
https://images.evetech.net/types/587/icon?size=64        # Rifter inventory icon
https://images.evetech.net/types/587/bp?size=64          # Rifter blueprint
```

### Characters

| Variation | Description |
|-----------|-------------|
| `portrait` | Character portrait (JPEG) |

Example:
```
https://images.evetech.net/characters/123456/portrait?size=256
```

### Corporations

| Variation | Description |
|-----------|-------------|
| `logo` | Corporation logo (PNG with transparency) |

Example:
```
https://images.evetech.net/corporations/98000001/logo?size=128
```

### Alliances

| Variation | Description |
|-----------|-------------|
| `logo` | Alliance logo (PNG with transparency) |

Example:
```
https://images.evetech.net/alliances/99000001/logo?size=128
```

## Sizes

Valid sizes: `32`, `64`, `128`, `256`, `512`, `1024`

If size is omitted, native resolution is returned.

## Discovering Available Variations

```
GET https://images.evetech.net/{category}/{id}
```

Returns JSON array of available variations:
```json
["render", "icon", "bp", "bpc"]
```

## Common Ship Type IDs

| Ship | Type ID | Class |
|------|---------|-------|
| Rifter | 587 | Frigate |
| Tristan | 593 | Frigate |
| Merlin | 603 | Frigate |
| Punisher | 597 | Frigate |
| Caracal | 621 | Cruiser |
| Thorax | 627 | Cruiser |
| Maller | 624 | Cruiser |
| Stabber | 622 | Cruiser |
| Drake | 24690 | Battlecruiser |
| Hurricane | 24702 | Battlecruiser |
| Raven | 638 | Battleship |
| Megathron | 641 | Battleship |
| Machariel | 17738 | Faction BS |
| Nyx | 23913 | Supercarrier |
| Avatar | 11567 | Titan |

## Bulk Download Script

```python
import httpx
import asyncio
from pathlib import Path

SHIP_IDS = [587, 593, 621, 24690, 17738]  # Add more as needed
SIZES = [64, 256, 512]
OUTPUT_DIR = Path("assets/ships")

async def download_ship(client: httpx.AsyncClient, type_id: int, size: int):
    url = f"https://images.evetech.net/types/{type_id}/render?size={size}"
    output = OUTPUT_DIR / f"{type_id}_{size}.png"
    
    if output.exists():
        return  # Skip existing
    
    response = await client.get(url)
    if response.status_code == 200:
        output.write_bytes(response.content)
        print(f"Downloaded: {type_id} @ {size}px")
    else:
        print(f"Failed: {type_id} - {response.status_code}")

async def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    async with httpx.AsyncClient() as client:
        tasks = [
            download_ship(client, ship_id, size)
            for ship_id in SHIP_IDS
            for size in SIZES
        ]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
```

## Error Handling

| Status | Meaning | Action |
|--------|---------|--------|
| 200 | Success | Image returned |
| 302 | Not found | Redirects to generic placeholder |
| 404 | Invalid size | Use valid size (32/64/128/256/512/1024) |

## Image Formats

- **Types (render/icon/bp)**: PNG with transparency
- **Character portraits**: JPEG (no transparency)
- **Corp/Alliance logos**: PNG with transparency

## Caching

- Images are heavily cached by CDN
- No rate limiting on image server
- Safe to prefetch and cache locally

## Integration Tips

### For Games (EVE_Rebellion)

```python
def get_enemy_sprite(type_id: int, size: int = 256) -> str:
    """Get URL for enemy ship render."""
    return f"https://images.evetech.net/types/{type_id}/render?size={size}"

# In your sprite loading code
enemy_types = {
    "frigate": 587,    # Rifter
    "cruiser": 621,    # Caracal
    "battleship": 638, # Raven
    "boss": 23913      # Nyx supercarrier
}

for name, type_id in enemy_types.items():
    url = get_enemy_sprite(type_id)
    # Download and convert to pygame surface
```

### For React/Web Apps

```jsx
const ShipImage = ({ typeId, size = 256, variation = "render" }) => (
  <img
    src={`https://images.evetech.net/types/${typeId}/${variation}?size=${size}`}
    alt={`Ship ${typeId}`}
    loading="lazy"
    onError={(e) => {
      e.target.src = "/placeholder-ship.png";
    }}
  />
);

// Usage
<ShipImage typeId={587} size={128} />
```

### Preloading Strategy

```javascript
const preloadShipImages = (typeIds, sizes = [64, 256]) => {
  typeIds.forEach(id => {
    sizes.forEach(size => {
      const img = new Image();
      img.src = `https://images.evetech.net/types/${id}/render?size=${size}`;
    });
  });
};

// Preload common ships on app init
preloadShipImages([587, 593, 621, 24690]);
```
