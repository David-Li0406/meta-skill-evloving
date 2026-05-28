# EVE Development Portfolio - Complete Setup

Execute ALL tasks autonomously. This is a comprehensive update of ARETE's EVE Online development projects including asset downloads, ESI integration, tools, and compliance updates.

## Project Paths
- EVE_Ships: ~/projects/EVE_Ships
- EVE_Rebellion: ~/projects/EVE_Rebellion  
- EVE_Gatekeeper: ~/projects/EVE_Gatekeeper

If paths differ, ask once then continue.

---

# PHASE 1: EVE_Ships - Complete Rebuild with Official Renders

## Task: Delete existing content and rebuild with official EVE Image Server assets

### Step 1: Backup and clean
```bash
cd ~/projects
mv EVE_Ships EVE_Ships_backup_$(date +%Y%m%d) 2>/dev/null || true
mkdir -p EVE_Ships/{renders/{256,512},icons/{32,64},by_faction,by_class}
cd EVE_Ships
```

### Step 2: Download ALL ships from images.evetech.net

Image URL pattern: `https://images.evetech.net/types/{type_id}/render?size={size}`

**COMPLETE SHIP DATABASE - Download ALL of these:**

```python
SHIPS = {
    # FRIGATES (24 ships)
    "rifter": 587, "slasher": 585, "breacher": 598, "probe": 586, "burst": 599, "vigil": 3766,
    "tristan": 593, "atron": 608, "incursus": 594, "imicus": 607, "navitas": 592, "maulus": 609,
    "merlin": 603, "kestrel": 602, "condor": 583, "heron": 605, "bantam": 582, "griffin": 584,
    "punisher": 597, "executioner": 589, "tormentor": 591, "magnate": 29248, "inquisitor": 590, "crucifier": 2161,
    
    # DESTROYERS (8 ships)
    "thrasher": 16242, "talwar": 32872,
    "catalyst": 16240, "algos": 32875,
    "cormorant": 16238, "corax": 32876,
    "coercer": 16236, "dragoon": 32874,
    
    # CRUISERS (16 ships)
    "stabber": 622, "rupture": 629, "bellicose": 630, "scythe": 631,
    "thorax": 627, "vexor": 626, "celestis": 633, "exequror": 634,
    "caracal": 621, "moa": 623, "blackbird": 632, "osprey": 620,
    "maller": 624, "omen": 625, "arbitrator": 628, "augoror": 619,
    
    # BATTLECRUISERS (12 ships)
    "hurricane": 24702, "cyclone": 24700, "tornado": 4310,
    "brutix": 16229, "myrmidon": 24698, "talos": 4308,
    "drake": 24690, "ferox": 24688, "naga": 4306,
    "harbinger": 24696, "prophecy": 24692, "oracle": 4302,
    
    # BATTLESHIPS (12 ships)
    "tempest": 639, "typhoon": 644, "maelstrom": 24694,
    "megathron": 641, "dominix": 645, "hyperion": 24690,
    "raven": 638, "scorpion": 640, "rokh": 24688,
    "apocalypse": 642, "armageddon": 643, "abaddon": 24692,
    
    # FACTION/PIRATE (18 ships)
    "dramiel": 17703, "cynabal": 17715, "machariel": 17738,
    "succubus": 17924, "phantasm": 17718, "nightmare": 17736,
    "daredevil": 17928, "vigilant": 17720, "vindicator": 17740,
    "cruor": 17926, "ashimmu": 17922, "bhaalgorn": 17920,
    "worm": 17930, "gila": 17715, "rattlesnake": 17918,
    "astero": 33468, "stratios": 33470, "nestor": 33472,
    
    # CAPITALS (16 ships)
    "naglfar": 19724, "moros": 19720, "phoenix": 19726, "revelation": 19722,
    "nidhoggur": 24483, "thanatos": 23911, "chimera": 23915, "archon": 23757,
    "lif": 37605, "ninazu": 37607, "minokawa": 37606, "apostle": 37604,
    "hel": 22852, "nyx": 23913, "wyvern": 23917, "aeon": 23919,
    
    # TITANS (4 ships)
    "ragnarok": 11568, "erebus": 671, "leviathan": 3764, "avatar": 11567,
    
    # INDUSTRIAL (12 ships)
    "mammoth": 652, "iteron_v": 657, "badger": 648, "bestower": 1944,
    "venture": 32880, "procurer": 17480, "retriever": 17478, "covetor": 17476,
    "hulk": 22544, "skiff": 22546, "mackinaw": 22548,
    "orca": 28606, "rorqual": 28352,
    "fenrir": 20189, "obelisk": 20187, "charon": 20185, "providence": 20183,
}

FACTIONS = {
    "minmatar": ["rifter", "slasher", "breacher", "probe", "burst", "vigil", "thrasher", "talwar", "stabber", "rupture", "bellicose", "scythe", "hurricane", "cyclone", "tornado", "tempest", "typhoon", "maelstrom", "naglfar", "nidhoggur", "lif", "hel", "ragnarok", "fenrir", "mammoth"],
    "gallente": ["tristan", "atron", "incursus", "imicus", "navitas", "maulus", "catalyst", "algos", "thorax", "vexor", "celestis", "exequror", "brutix", "myrmidon", "talos", "megathron", "dominix", "hyperion", "moros", "thanatos", "ninazu", "nyx", "erebus", "obelisk", "iteron_v"],
    "caldari": ["merlin", "kestrel", "condor", "heron", "bantam", "griffin", "cormorant", "corax", "caracal", "moa", "blackbird", "osprey", "drake", "ferox", "naga", "raven", "scorpion", "rokh", "phoenix", "chimera", "minokawa", "wyvern", "leviathan", "charon", "badger"],
    "amarr": ["punisher", "executioner", "tormentor", "magnate", "inquisitor", "crucifier", "coercer", "dragoon", "maller", "omen", "arbitrator", "augoror", "harbinger", "prophecy", "oracle", "apocalypse", "armageddon", "abaddon", "revelation", "archon", "apostle", "aeon", "avatar", "providence", "bestower"],
    "pirate": ["dramiel", "cynabal", "machariel", "succubus", "phantasm", "nightmare", "daredevil", "vigilant", "vindicator", "cruor", "ashimmu", "bhaalgorn", "worm", "gila", "rattlesnake", "astero", "stratios", "nestor"],
    "ore": ["venture", "procurer", "retriever", "covetor", "hulk", "skiff", "mackinaw", "orca", "rorqual"],
}
```

### Step 3: Create download script and run it

Create `download_ships.py`:
```python
#!/usr/bin/env python3
import asyncio
import json
from pathlib import Path
from datetime import datetime

try:
    import httpx
except ImportError:
    import subprocess
    subprocess.run(["pip", "install", "httpx"])
    import httpx

SHIPS = {
    "rifter": 587, "slasher": 585, "breacher": 598, "probe": 586, "burst": 599, "vigil": 3766,
    "tristan": 593, "atron": 608, "incursus": 594, "imicus": 607, "navitas": 592, "maulus": 609,
    "merlin": 603, "kestrel": 602, "condor": 583, "heron": 605, "bantam": 582, "griffin": 584,
    "punisher": 597, "executioner": 589, "tormentor": 591, "magnate": 29248, "inquisitor": 590, "crucifier": 2161,
    "thrasher": 16242, "talwar": 32872, "catalyst": 16240, "algos": 32875,
    "cormorant": 16238, "corax": 32876, "coercer": 16236, "dragoon": 32874,
    "stabber": 622, "rupture": 629, "bellicose": 630, "scythe": 631,
    "thorax": 627, "vexor": 626, "celestis": 633, "exequror": 634,
    "caracal": 621, "moa": 623, "blackbird": 632, "osprey": 620,
    "maller": 624, "omen": 625, "arbitrator": 628, "augoror": 619,
    "hurricane": 24702, "cyclone": 24700, "tornado": 4310,
    "brutix": 16229, "myrmidon": 24698, "talos": 4308,
    "drake": 24690, "ferox": 24688, "naga": 4306,
    "harbinger": 24696, "prophecy": 24692, "oracle": 4302,
    "tempest": 639, "typhoon": 644, "maelstrom": 24694,
    "megathron": 641, "dominix": 645, "hyperion": 24690,
    "raven": 638, "scorpion": 640, "rokh": 24688,
    "apocalypse": 642, "armageddon": 643, "abaddon": 24692,
    "dramiel": 17703, "cynabal": 17715, "machariel": 17738,
    "succubus": 17924, "phantasm": 17718, "nightmare": 17736,
    "daredevil": 17928, "vigilant": 17720, "vindicator": 17740,
    "cruor": 17926, "ashimmu": 17922, "bhaalgorn": 17920,
    "worm": 17930, "gila": 17715, "rattlesnake": 17918,
    "astero": 33468, "stratios": 33470, "nestor": 33472,
    "naglfar": 19724, "moros": 19720, "phoenix": 19726, "revelation": 19722,
    "nidhoggur": 24483, "thanatos": 23911, "chimera": 23915, "archon": 23757,
    "lif": 37605, "ninazu": 37607, "minokawa": 37606, "apostle": 37604,
    "hel": 22852, "nyx": 23913, "wyvern": 23917, "aeon": 23919,
    "ragnarok": 11568, "erebus": 671, "leviathan": 3764, "avatar": 11567,
    "mammoth": 652, "iteron_v": 657, "badger": 648, "bestower": 1944,
    "venture": 32880, "procurer": 17480, "retriever": 17478, "covetor": 17476,
    "hulk": 22544, "skiff": 22546, "mackinaw": 22548,
    "orca": 28606, "rorqual": 28352,
    "fenrir": 20189, "obelisk": 20187, "charon": 20185, "providence": 20183,
}

IMAGE_URL = "https://images.evetech.net/types/{type_id}/render?size={size}"

async def download(client, name, type_id, size, out_dir):
    path = out_dir / f"{name}_{type_id}.png"
    if path.exists():
        return True
    try:
        r = await client.get(IMAGE_URL.format(type_id=type_id, size=size), follow_redirects=True)
        if r.status_code == 200:
            path.write_bytes(r.content)
            return True
    except:
        pass
    return False

async def main():
    base = Path(".")
    for size in [256, 512]:
        (base / "renders" / str(size)).mkdir(parents=True, exist_ok=True)
    
    async with httpx.AsyncClient(timeout=30) as client:
        for size in [256, 512]:
            print(f"Downloading {len(SHIPS)} ships @ {size}px...")
            tasks = [download(client, n, t, size, base/"renders"/str(size)) for n, t in SHIPS.items()]
            results = await asyncio.gather(*tasks)
            print(f"  ✓ {sum(results)}/{len(results)} successful")
    
    # Create manifest
    manifest = {"generated": datetime.now().isoformat(), "ships": SHIPS, "total": len(SHIPS)}
    (base / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print("✓ Created manifest.json")

if __name__ == "__main__":
    asyncio.run(main())
```

Run it: `python download_ships.py`

### Step 4: Create README.md

```markdown
# EVE Ships - Official Render Collection

Complete collection of EVE Online ship renders from the official EVE Image Server.

## Stats
- **Ships:** 120+
- **Sizes:** 256px, 512px
- **Source:** images.evetech.net

## Usage

```python
# Get ship render path
def get_ship(name, type_id, size=256):
    return f"renders/{size}/{name}_{type_id}.png"

# Example
machariel = get_ship("machariel", 17738, 512)
```

## Direct from EVE Image Server

```
https://images.evetech.net/types/{type_id}/render?size={size}
```

## Attribution

EVE Online and the EVE logo are registered trademarks of [CCP hf](https://www.ccpgames.com/).
All ship images are property of CCP and used in accordance with the [EVE Online Content Creation Terms of Use](https://community.eveonline.com/support/policies/content-creation-terms-of-use/).

This project is not affiliated with or endorsed by CCP hf.
```

### Step 5: Create .gitignore

```
__pycache__/
*.pyc
.DS_Store
*.tmp
.env
```

### Step 6: Git commit
```bash
git init
git add .
git commit -m "Official EVE ship renders from Image Server"
```

---

# PHASE 2: EVE_Rebellion - ESI Integration + Sprites

## Task: Add compliant ESI client and ship sprite system

### Step 1: Create core/esi_client.py

```python
"""
ESI Client for EVE_Rebellion
Compliant with CCP's API requirements.
"""
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, Optional
import httpx

class ESIClient:
    """EVE Online ESI API Client with compliance features."""
    
    BASE_URL = "https://esi.evetech.net/latest"
    IMAGE_URL = "https://images.evetech.net"
    
    def __init__(self, app_name: str = "EVE_Rebellion", contact: str = "developer@example.com"):
        self.headers = {
            "User-Agent": f"{app_name}/1.0 ({contact})",
            "Accept": "application/json"
        }
        self._cache: Dict[str, Dict] = {}
        self._error_count = 0
    
    def _check_cache(self, key: str) -> Optional[Any]:
        """Check if we have valid cached data."""
        if key in self._cache:
            if datetime.now(timezone.utc) < self._cache[key]["expires"]:
                return self._cache[key]["data"]
        return None
    
    async def get(self, endpoint: str, params: dict = None) -> Any:
        """Make GET request with caching and error monitoring."""
        cache_key = f"{endpoint}:{params}"
        
        cached = self._check_cache(cache_key)
        if cached:
            return cached
        
        url = f"{self.BASE_URL}{endpoint}"
        if not url.endswith("/"):
            url += "/"
        
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(url, headers=self.headers, params=params)
            
            # Monitor error budget
            if "X-ESI-Error-Limit-Remain" in r.headers:
                remain = int(r.headers["X-ESI-Error-Limit-Remain"])
                if remain < 10:
                    print(f"⚠️ ESI error budget critical: {remain}")
                    await asyncio.sleep(30)
            
            r.raise_for_status()
            data = r.json()
            
            # Cache based on Expires header
            if "Expires" in r.headers:
                try:
                    exp = datetime.strptime(r.headers["Expires"], "%a, %d %b %Y %H:%M:%S %Z")
                    self._cache[cache_key] = {"data": data, "expires": exp.replace(tzinfo=timezone.utc)}
                except:
                    pass
            
            return data
    
    async def get_type(self, type_id: int) -> Dict:
        """Get type info (ship stats)."""
        return await self.get(f"/universe/types/{type_id}")
    
    def get_render_url(self, type_id: int, size: int = 256) -> str:
        """Get ship render URL."""
        return f"{self.IMAGE_URL}/types/{type_id}/render?size={size}"
    
    def get_icon_url(self, type_id: int, size: int = 64) -> str:
        """Get ship icon URL."""
        return f"{self.IMAGE_URL}/types/{type_id}/icon?size={size}"


# Default client
_client: Optional[ESIClient] = None

def get_esi() -> ESIClient:
    global _client
    if not _client:
        _client = ESIClient()
    return _client
```

### Step 2: Create core/ship_sprites.py

```python
"""
Ship Sprite Manager for EVE_Rebellion
Loads ship renders from EVE Image Server.
"""
import asyncio
from pathlib import Path
from typing import Dict, Optional
import io

try:
    import pygame
except ImportError:
    pygame = None

try:
    import httpx
except ImportError:
    httpx = None

class ShipSprites:
    """Manages ship sprite loading with caching."""
    
    IMAGE_URL = "https://images.evetech.net/types/{type_id}/render?size={size}"
    
    # Ship type IDs for game enemies
    ENEMY_SHIPS = {
        "frigate": 587,       # Rifter
        "destroyer": 16242,   # Thrasher
        "cruiser": 621,       # Caracal
        "battlecruiser": 24702,  # Hurricane
        "battleship": 638,    # Raven
        "carrier": 23911,     # Thanatos
        "boss": 23913,        # Nyx
        "titan": 11567,       # Avatar
    }
    
    def __init__(self, cache_dir: str = "assets/ships"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._surfaces: Dict[tuple, pygame.Surface] = {} if pygame else {}
    
    def _cache_path(self, type_id: int, size: int) -> Path:
        return self.cache_dir / f"{type_id}_{size}.png"
    
    async def _download(self, type_id: int, size: int) -> bytes:
        """Download sprite from Image Server."""
        url = self.IMAGE_URL.format(type_id=type_id, size=size)
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(url, follow_redirects=True)
            r.raise_for_status()
            return r.content
    
    async def load(self, type_id: int, size: int = 256) -> Optional[pygame.Surface]:
        """Load ship sprite as Pygame surface."""
        if not pygame:
            return None
        
        key = (type_id, size)
        if key in self._surfaces:
            return self._surfaces[key]
        
        cache_path = self._cache_path(type_id, size)
        
        # Try cache first
        if cache_path.exists():
            surface = pygame.image.load(str(cache_path)).convert_alpha()
            self._surfaces[key] = surface
            return surface
        
        # Download
        try:
            data = await self._download(type_id, size)
            cache_path.write_bytes(data)
            surface = pygame.image.load(io.BytesIO(data)).convert_alpha()
            self._surfaces[key] = surface
            return surface
        except Exception as e:
            print(f"Failed to load sprite {type_id}: {e}")
            return None
    
    def load_sync(self, type_id: int, size: int = 256) -> Optional[pygame.Surface]:
        """Synchronous sprite loading."""
        return asyncio.run(self.load(type_id, size))
    
    async def preload_enemies(self, size: int = 256):
        """Preload all enemy ship sprites."""
        tasks = [self.load(tid, size) for tid in self.ENEMY_SHIPS.values()]
        await asyncio.gather(*tasks)
        print(f"✓ Preloaded {len(self.ENEMY_SHIPS)} enemy sprites")
    
    def get_enemy_sprite(self, enemy_type: str, size: int = 256) -> Optional[pygame.Surface]:
        """Get sprite for enemy type."""
        type_id = self.ENEMY_SHIPS.get(enemy_type)
        if type_id:
            return self.load_sync(type_id, size)
        return None


# Default instance
sprites = ShipSprites()
```

### Step 3: Update constants.py - Add enemy type mapping

Add this to constants.py:
```python
# EVE Ship Type IDs for enemies
ENEMY_TYPE_IDS = {
    "frigate": 587,       # Rifter
    "destroyer": 16242,   # Thrasher  
    "cruiser": 621,       # Caracal
    "battlecruiser": 24702,  # Hurricane
    "battleship": 638,    # Raven
    "carrier": 23911,     # Thanatos
    "supercarrier": 23913,  # Nyx
    "titan": 11567,       # Avatar
}

# Image Server URL pattern
EVE_IMAGE_URL = "https://images.evetech.net/types/{type_id}/render?size={size}"
```

### Step 4: Add attribution to README.md

Append to README.md:
```markdown

## Attribution

EVE Online and the EVE logo are registered trademarks of [CCP hf](https://www.ccpgames.com/).
Ship images and game data from [EVE Image Server](https://images.evetech.net/) and [ESI API](https://esi.evetech.net/).
Used in accordance with the [EVE Online Content Creation Terms of Use](https://community.eveonline.com/support/policies/content-creation-terms-of-use/).

This project is not affiliated with or endorsed by CCP hf.
```

### Step 5: Git commit
```bash
git add .
git commit -m "Add ESI client and ship sprite system"
```

---

# PHASE 3: EVE_Gatekeeper - ESI Foundation + SDE Prep

## Task: Set up ESI client, auth scaffolding, and SDE importer stub

### Step 1: Create app/esi_client.py

```python
"""
ESI Client for EVE_Gatekeeper (2D Starmap)
Full-featured client with SSO support.
"""
import asyncio
import os
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
import httpx

class ESIClient:
    """EVE ESI Client with full compliance and SSO support."""
    
    BASE_URL = "https://esi.evetech.net/latest"
    IMAGE_URL = "https://images.evetech.net"
    SSO_URL = "https://login.eveonline.com/v2/oauth"
    
    def __init__(
        self,
        app_name: str = "EVE_Gatekeeper",
        contact: str = "developer@example.com",
        client_id: str = None,
        client_secret: str = None
    ):
        self.app_name = app_name
        self.client_id = client_id or os.getenv("EVE_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("EVE_CLIENT_SECRET")
        
        self.headers = {
            "User-Agent": f"{app_name}/1.0 ({contact})",
            "Accept": "application/json"
        }
        self._cache: Dict[str, Dict] = {}
    
    # === PUBLIC ENDPOINTS (No Auth) ===
    
    async def get(self, endpoint: str, params: dict = None) -> Any:
        """Make cached GET request."""
        cache_key = f"{endpoint}:{params}"
        
        if cache_key in self._cache:
            if datetime.now(timezone.utc) < self._cache[cache_key]["expires"]:
                return self._cache[cache_key]["data"]
        
        url = f"{self.BASE_URL}{endpoint}"
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(url, headers=self.headers, params=params)
            
            # Error budget monitoring
            if "X-ESI-Error-Limit-Remain" in r.headers:
                remain = int(r.headers["X-ESI-Error-Limit-Remain"])
                if remain < 10:
                    print(f"⚠️ ESI error budget: {remain}")
                    await asyncio.sleep(30)
            
            r.raise_for_status()
            data = r.json()
            
            # Cache
            if "Expires" in r.headers:
                try:
                    exp = datetime.strptime(r.headers["Expires"], "%a, %d %b %Y %H:%M:%S %Z")
                    self._cache[cache_key] = {"data": data, "expires": exp.replace(tzinfo=timezone.utc)}
                except:
                    pass
            
            return data
    
    # === MAP ENDPOINTS ===
    
    async def get_systems(self) -> List[int]:
        """Get all system IDs."""
        return await self.get("/universe/systems/")
    
    async def get_system(self, system_id: int) -> Dict:
        """Get system info including stargates."""
        return await self.get(f"/universe/systems/{system_id}/")
    
    async def get_stargate(self, stargate_id: int) -> Dict:
        """Get stargate destination."""
        return await self.get(f"/universe/stargates/{stargate_id}/")
    
    async def get_route(self, origin: int, destination: int, flag: str = "shortest", avoid: List[int] = None) -> List[int]:
        """Calculate route between systems."""
        params = {"flag": flag}
        if avoid:
            params["avoid"] = avoid
        return await self.get(f"/route/{origin}/{destination}/", params)
    
    # === LIVE DATA ENDPOINTS ===
    
    async def get_system_kills(self) -> List[Dict]:
        """Get system kill counts (for heatmap)."""
        return await self.get("/universe/system_kills/")
    
    async def get_system_jumps(self) -> List[Dict]:
        """Get system jump counts (for heatmap)."""
        return await self.get("/universe/system_jumps/")
    
    async def get_incursions(self) -> List[Dict]:
        """Get active incursions."""
        return await self.get("/incursions/")
    
    async def get_sovereignty_map(self) -> List[Dict]:
        """Get sovereignty data."""
        return await self.get("/sovereignty/map/")
    
    # === SSO AUTH (Stub - implement with tokens) ===
    
    def get_auth_url(self, callback_url: str, scopes: List[str], state: str) -> str:
        """Generate SSO authorization URL."""
        from urllib.parse import urlencode
        params = {
            "response_type": "code",
            "redirect_uri": callback_url,
            "client_id": self.client_id,
            "scope": " ".join(scopes),
            "state": state
        }
        return f"{self.SSO_URL}/authorize?{urlencode(params)}"
    
    async def exchange_code(self, code: str) -> Dict:
        """Exchange auth code for tokens."""
        import base64
        creds = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        
        async with httpx.AsyncClient() as client:
            r = await client.post(
                f"{self.SSO_URL}/token",
                headers={
                    "Authorization": f"Basic {creds}",
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                data={"grant_type": "authorization_code", "code": code}
            )
            return r.json()
    
    # === AUTH ENDPOINTS (require token) ===
    
    async def get_character_location(self, character_id: int, token: str) -> Dict:
        """Get character's current location."""
        headers = {**self.headers, "Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{self.BASE_URL}/characters/{character_id}/location/",
                headers=headers
            )
            return r.json()
    
    async def set_waypoint(self, destination_id: int, token: str, clear: bool = False) -> bool:
        """Set autopilot waypoint in EVE client."""
        headers = {**self.headers, "Authorization": f"Bearer {token}"}
        params = {
            "destination_id": destination_id,
            "clear_other_waypoints": clear,
            "add_to_beginning": False
        }
        async with httpx.AsyncClient() as client:
            r = await client.post(
                f"{self.BASE_URL}/ui/autopilot/waypoint/",
                headers=headers,
                params=params
            )
            return r.status_code == 204


# Default instance
_client: Optional[ESIClient] = None

def get_esi() -> ESIClient:
    global _client
    if not _client:
        _client = ESIClient()
    return _client
```

### Step 2: Create .env.example

```bash
# EVE SSO Credentials
# Register at: https://developers.eveonline.com/applications
EVE_CLIENT_ID=your_client_id_here
EVE_CLIENT_SECRET=your_client_secret_here
EVE_CALLBACK_URL=http://localhost:8000/callback

# Database
DATABASE_URL=sqlite:///./data/gatekeeper.db

# Optional
DEBUG=true
```

### Step 3: Create app/sde_importer.py

```python
"""
SDE Importer for EVE_Gatekeeper

Downloads and imports EVE Static Data Export.

Source: https://www.fuzzwork.co.uk/dump/latest/sqlite-latest.sqlite.bz2

Usage:
    python -m app.sde_importer --download
    python -m app.sde_importer --import
"""
import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple
import json

SDE_URL = "https://www.fuzzwork.co.uk/dump/latest/sqlite-latest.sqlite.bz2"
SDE_PATH = Path("data/sde.sqlite")

class SDEImporter:
    """Imports universe data from EVE SDE."""
    
    def __init__(self, sde_path: Path = SDE_PATH):
        self.sde_path = sde_path
        self.conn = None
    
    def connect(self):
        """Connect to SDE database."""
        if not self.sde_path.exists():
            raise FileNotFoundError(
                f"SDE not found at {self.sde_path}\n"
                f"Download from: {SDE_URL}\n"
                f"Extract to: {self.sde_path}"
            )
        self.conn = sqlite3.connect(self.sde_path)
        self.conn.row_factory = sqlite3.Row
    
    def get_systems(self) -> List[Dict]:
        """Get all solar systems with coordinates."""
        cursor = self.conn.execute("""
            SELECT 
                solarSystemID as id,
                solarSystemName as name,
                constellationID as constellation_id,
                regionID as region_id,
                x, y, z,
                security
            FROM mapSolarSystems
        """)
        return [dict(row) for row in cursor.fetchall()]
    
    def get_stargates(self) -> List[Dict]:
        """Get all stargates with destinations."""
        cursor = self.conn.execute("""
            SELECT
                fromSolarSystemID as from_system,
                toSolarSystemID as to_system
            FROM mapSolarSystemJumps
        """)
        return [dict(row) for row in cursor.fetchall()]
    
    def get_regions(self) -> List[Dict]:
        """Get all regions."""
        cursor = self.conn.execute("""
            SELECT
                regionID as id,
                regionName as name,
                x, y, z
            FROM mapRegions
        """)
        return [dict(row) for row in cursor.fetchall()]
    
    def build_graph(self) -> Dict[int, List[int]]:
        """Build adjacency list for pathfinding."""
        gates = self.get_stargates()
        graph = {}
        for gate in gates:
            src, dst = gate["from_system"], gate["to_system"]
            graph.setdefault(src, []).append(dst)
            graph.setdefault(dst, []).append(src)
        return graph
    
    def export_json(self, output_dir: Path):
        """Export SDE data as JSON files."""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        systems = self.get_systems()
        (output_dir / "systems.json").write_text(json.dumps(systems))
        print(f"✓ Exported {len(systems)} systems")
        
        gates = self.get_stargates()
        (output_dir / "stargates.json").write_text(json.dumps(gates))
        print(f"✓ Exported {len(gates)} stargate connections")
        
        regions = self.get_regions()
        (output_dir / "regions.json").write_text(json.dumps(regions))
        print(f"✓ Exported {len(regions)} regions")
        
        graph = self.build_graph()
        (output_dir / "graph.json").write_text(json.dumps(graph))
        print(f"✓ Exported system graph")
    
    def close(self):
        if self.conn:
            self.conn.close()


def download_sde():
    """Download SDE from Fuzzwork."""
    import subprocess
    print(f"Downloading SDE from {SDE_URL}...")
    SDE_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    bz2_path = SDE_PATH.with_suffix(".sqlite.bz2")
    subprocess.run(["wget", "-O", str(bz2_path), SDE_URL], check=True)
    subprocess.run(["bunzip2", str(bz2_path)], check=True)
    print(f"✓ SDE saved to {SDE_PATH}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--download", action="store_true", help="Download SDE")
    parser.add_argument("--export", action="store_true", help="Export to JSON")
    args = parser.parse_args()
    
    if args.download:
        download_sde()
    
    if args.export:
        importer = SDEImporter()
        importer.connect()
        importer.export_json(Path("data/export"))
        importer.close()
```

### Step 4: Create app/config.py

```python
"""Configuration for EVE_Gatekeeper."""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

# EVE SSO
EVE_CLIENT_ID = os.getenv("EVE_CLIENT_ID")
EVE_CLIENT_SECRET = os.getenv("EVE_CLIENT_SECRET")
EVE_CALLBACK_URL = os.getenv("EVE_CALLBACK_URL", "http://localhost:8000/callback")

# ESI Scopes needed
EVE_SCOPES = [
    "esi-location.read_location.v1",
    "esi-location.read_online.v1",
    "esi-ui.write_waypoint.v1",
    "esi-assets.read_assets.v1",
]

# Database
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR}/gatekeeper.db")

# Cache TTLs (seconds)
CACHE_TTL_SYSTEMS = 86400  # 24 hours
CACHE_TTL_KILLS = 300      # 5 minutes
CACHE_TTL_JUMPS = 300      # 5 minutes
CACHE_TTL_LOCATION = 5     # 5 seconds
```

### Step 5: Add attribution to README.md

Append to README.md:
```markdown

## Attribution

EVE Online and the EVE logo are registered trademarks of [CCP hf](https://www.ccpgames.com/).
Map data from [EVE SDE](https://developers.eveonline.com/resource/resources) and [ESI API](https://esi.evetech.net/).
Used in accordance with the [EVE Online Content Creation Terms of Use](https://community.eveonline.com/support/policies/content-creation-terms-of-use/).

This project is not affiliated with or endorsed by CCP hf.
```

### Step 6: Git commit
```bash
git add .
git commit -m "Add ESI client, SSO scaffolding, and SDE importer"
```

---

# PHASE 4: Final Git Push

```bash
# Push all projects
cd ~/projects/EVE_Ships && git push --force origin main
cd ~/projects/EVE_Rebellion && git push origin main
cd ~/projects/EVE_Gatekeeper && git push origin main
```

---

# COMPLETION CHECKLIST

After execution, verify:

- [ ] EVE_Ships has 100+ ship renders in renders/256/ and renders/512/
- [ ] EVE_Ships has manifest.json with type ID mapping
- [ ] EVE_Rebellion has core/esi_client.py
- [ ] EVE_Rebellion has core/ship_sprites.py  
- [ ] EVE_Rebellion has ENEMY_TYPE_IDS in constants.py
- [ ] EVE_Gatekeeper has app/esi_client.py with SSO support
- [ ] EVE_Gatekeeper has app/sde_importer.py
- [ ] EVE_Gatekeeper has .env.example
- [ ] ALL projects have CCP attribution in README.md
- [ ] ALL projects committed and pushed

---

# SUCCESS METRICS

| Project | Before | After |
|---------|--------|-------|
| EVE_Ships | C (50) | A (95) |
| EVE_Rebellion | A- (85) | A (95) |
| EVE_Gatekeeper | B- (70) | B+ (85) |

Total execution time: ~40 minutes

Report completion of each phase as you go.
