#!/usr/bin/env python3
"""
EVE Project Updater

Applies ESI integration templates and compliance fixes to EVE projects.

Usage:
    python project_updater.py ~/projects/EVE_Rebellion --plan
    python project_updater.py ~/projects/EVE_Rebellion --apply
    python project_updater.py ~/projects/EVE_Starmap --apply --component sso
"""

import argparse
import sys
from enum import Enum
from pathlib import Path
from typing import Dict, List


class UpdateAction(Enum):
    ADD_FILE = "add_file"
    MODIFY_FILE = "modify_file"
    ADD_DEPENDENCY = "add_dependency"
    CREATE_DIR = "create_dir"
    DOWNLOAD_ASSETS = "download_assets"


# ============================================================================
# TEMPLATES
# ============================================================================

ESI_CLIENT_TEMPLATE = '''"""
ESI Client for {project_name}

A compliant ESI API client following CCP's best practices.
"""

import asyncio
from datetime import datetime, timezone
from typing import Dict, Optional, Any
import httpx

class ESIClient:
    """
    EVE Online ESI API Client

    Features:
    - User-Agent header (required by CCP)
    - Response caching based on Expires header
    - Error limit monitoring (100 errors/60s = ban)
    - Rate limiting for bulk operations
    """

    BASE_URL = "https://esi.evetech.net/latest"
    IMAGE_URL = "https://images.evetech.net"

    def __init__(
        self,
        app_name: str = "{project_name}",
        contact_email: str = "developer@example.com",
        datasource: str = "tranquility"
    ):
        self.app_name = app_name
        self.contact_email = contact_email
        self.datasource = datasource

        self.headers = {{
            "User-Agent": f"{{app_name}}/1.0 ({{contact_email}})",
            "Accept": "application/json"
        }}

        self._cache: Dict[str, Dict] = {{}}
        self._error_count = 0
        self._error_reset: Optional[datetime] = None

    def _check_error_budget(self, headers: Dict) -> None:
        """Monitor error limit headers."""
        if "X-ESI-Error-Limit-Remain" in headers:
            remain = int(headers["X-ESI-Error-Limit-Remain"])
            reset = int(headers.get("X-ESI-Error-Limit-Reset", 60))

            if remain < 20:
                print(f"⚠️ ESI error budget low: {{remain}} remaining, resets in {{reset}}s")

            if remain < 5:
                raise Exception(f"ESI error budget critical: {{remain}} remaining. Pausing requests.")

    def _get_cache_key(self, endpoint: str, params: Optional[Dict]) -> str:
        """Generate cache key for request."""
        param_str = json.dumps(params, sort_keys=True) if params else ""
        return f"{{endpoint}}:{{param_str}}"

    def _is_cached(self, cache_key: str) -> bool:
        """Check if response is cached and valid."""
        if cache_key not in self._cache:
            return False

        cached = self._cache[cache_key]
        return datetime.now(timezone.utc) < cached["expires"]

    async def get(
        self,
        endpoint: str,
        params: Optional[Dict] = None,
        skip_cache: bool = False
    ) -> Any:
        """
        Make a GET request to ESI.

        Args:
            endpoint: API endpoint (e.g., "/universe/systems/30000142/")
            params: Query parameters
            skip_cache: Force fresh request

        Returns:
            JSON response data
        """
        cache_key = self._get_cache_key(endpoint, params)

        # Check cache first
        if not skip_cache and self._is_cached(cache_key):
            return self._cache[cache_key]["data"]

        # Build request
        url = f"{{self.BASE_URL}}{{endpoint}}"
        if not url.endswith("/"):
            url += "/"

        request_params = {{"datasource": self.datasource}}
        if params:
            request_params.update(params)

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                url,
                headers=self.headers,
                params=request_params
            )

            # Check error budget
            self._check_error_budget(dict(response.headers))

            # Handle errors
            if response.status_code >= 400:
                self._error_count += 1
                response.raise_for_status()

            # Parse response
            data = response.json()

            # Cache based on Expires header
            if "Expires" in response.headers:
                try:
                    expires = datetime.strptime(
                        response.headers["Expires"],
                        "%a, %d %b %Y %H:%M:%S %Z"
                    ).replace(tzinfo=timezone.utc)

                    self._cache[cache_key] = {{
                        "data": data,
                        "expires": expires
                    }}
                except ValueError:
                    pass  # Ignore invalid date format

            return data

    async def get_system(self, system_id: int) -> Dict:
        """Get solar system information."""
        return await self.get(f"/universe/systems/{{system_id}}")

    async def get_type(self, type_id: int) -> Dict:
        """Get type information (ships, modules, etc.)."""
        return await self.get(f"/universe/types/{{type_id}}")

    async def get_route(
        self,
        origin: int,
        destination: int,
        flag: str = "shortest",
        avoid: Optional[List[int]] = None
    ) -> List[int]:
        """
        Calculate route between systems.

        Args:
            origin: Origin system ID
            destination: Destination system ID
            flag: "shortest", "secure", or "insecure"
            avoid: List of system IDs to avoid

        Returns:
            List of system IDs representing the route
        """
        params = {{"flag": flag}}
        if avoid:
            params["avoid"] = avoid

        return await self.get(f"/route/{{origin}}/{{destination}}", params)

    def get_ship_render_url(self, type_id: int, size: int = 256) -> str:
        """Get URL for ship render image."""
        return f"{{self.IMAGE_URL}}/types/{{type_id}}/render?size={{size}}"

    def get_ship_icon_url(self, type_id: int, size: int = 64) -> str:
        """Get URL for ship icon."""
        return f"{{self.IMAGE_URL}}/types/{{type_id}}/icon?size={{size}}"

    def get_character_portrait_url(self, character_id: int, size: int = 256) -> str:
        """Get URL for character portrait."""
        return f"{{self.IMAGE_URL}}/characters/{{character_id}}/portrait?size={{size}}"


# Convenience instance
_default_client: Optional[ESIClient] = None

def get_client() -> ESIClient:
    """Get default ESI client instance."""
    global _default_client
    if _default_client is None:
        _default_client = ESIClient()
    return _default_client
'''

ATTRIBUTION_TEMPLATE = '''
## Attribution

EVE Online and the EVE logo are registered trademarks of [CCP hf](https://www.ccpgames.com/).
All EVE Online assets, including ship images and game data, are property of CCP and are used in accordance with the [EVE Online Content Creation Terms of Use](https://community.eveonline.com/support/policies/content-creation-terms-of-use/).

This project is not affiliated with or endorsed by CCP hf.

Data provided via:
- [EVE Online ESI API](https://esi.evetech.net/)
- [EVE Image Server](https://images.evetech.net/)
'''

SHIP_SPRITES_TEMPLATE = '''"""
Ship Sprites Manager for {project_name}

Loads ship sprites from EVE Image Server with caching.
"""

import asyncio
from pathlib import Path
from typing import Dict, Optional
import pygame
import httpx

class ShipSprites:
    """
    Manages ship sprite loading from EVE Image Server.

    Features:
    - Async downloading
    - Local caching
    - Pygame surface conversion
    """

    IMAGE_SERVER = "https://images.evetech.net"

    # Common ship type IDs
    SHIPS = {{
        "rifter": 587,
        "tristan": 593,
        "merlin": 603,
        "punisher": 597,
        "caracal": 621,
        "thorax": 627,
        "moa": 623,
        "maller": 624,
        "drake": 24690,
        "hurricane": 24702,
        "raven": 638,
        "megathron": 641,
        "machariel": 17738,
        "nyx": 23913,
    }}

    def __init__(self, cache_dir: str = "assets/ships"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._surfaces: Dict[int, pygame.Surface] = {{}}

    def _get_cache_path(self, type_id: int, size: int) -> Path:
        """Get local cache path for sprite."""
        return self.cache_dir / f"{{type_id}}_{{size}}.png"

    async def _download_sprite(self, type_id: int, size: int) -> bytes:
        """Download sprite from Image Server."""
        url = f"{{self.IMAGE_SERVER}}/types/{{type_id}}/render?size={{size}}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()
            return response.content

    async def load_sprite(
        self,
        type_id: int,
        size: int = 256,
        use_cache: bool = True
    ) -> pygame.Surface:
        """
        Load ship sprite as Pygame surface.

        Args:
            type_id: EVE type ID for the ship
            size: Image size (32, 64, 128, 256, 512)
            use_cache: Whether to use local file cache

        Returns:
            Pygame Surface with ship render
        """
        cache_key = (type_id, size)

        # Check memory cache
        if cache_key in self._surfaces:
            return self._surfaces[cache_key]

        cache_path = self._get_cache_path(type_id, size)

        # Check file cache
        if use_cache and cache_path.exists():
            surface = pygame.image.load(str(cache_path)).convert_alpha()
            self._surfaces[cache_key] = surface
            return surface

        # Download
        print(f"Downloading ship sprite: {{type_id}} @ {{size}}px")
        image_data = await self._download_sprite(type_id, size)

        # Save to cache
        cache_path.write_bytes(image_data)

        # Convert to surface
        import io
        surface = pygame.image.load(io.BytesIO(image_data)).convert_alpha()
        self._surfaces[cache_key] = surface

        return surface

    def load_sprite_sync(self, type_id: int, size: int = 256) -> pygame.Surface:
        """Synchronous sprite loading (uses asyncio.run internally)."""
        return asyncio.run(self.load_sprite(type_id, size))

    async def preload_common_ships(self, size: int = 256) -> None:
        """Preload all common ship sprites."""
        tasks = [
            self.load_sprite(type_id, size)
            for type_id in self.SHIPS.values()
        ]
        await asyncio.gather(*tasks)
        print(f"Preloaded {{len(self.SHIPS)}} ship sprites")

    def get_by_name(self, name: str, size: int = 256) -> Optional[pygame.Surface]:
        """Get sprite by ship name."""
        type_id = self.SHIPS.get(name.lower())
        if type_id:
            return self.load_sprite_sync(type_id, size)
        return None


# Usage example:
# sprites = ShipSprites()
# await sprites.preload_common_ships()
# rifter_surface = sprites.get_by_name("rifter")
'''

REQUIREMENTS_ADDITIONS = {
    "esi_client": ["httpx>=0.25.0"],
    "ship_sprites": ["httpx>=0.25.0", "pygame>=2.0.0"],
    "sso": ["httpx>=0.25.0", "pyjwt>=2.8.0"],
}


# ============================================================================
# UPDATE LOGIC
# ============================================================================

def detect_project_type(project_path: Path) -> str:
    """Detect project type."""
    for f in project_path.rglob("*.py"):
        try:
            content = f.read_text(errors='ignore')
            if 'pygame' in content:
                return 'game'
            if 'fastapi' in content or 'FastAPI' in content:
                return 'api'
        except Exception:
            pass

    if (project_path / 'package.json').exists():
        return 'web'

    if len(list(project_path.rglob('*.svg'))) > 5:
        return 'assets'

    return 'unknown'


def plan_updates(project_path: Path, components: List[str] = None) -> List[Dict]:
    """Generate update plan for project."""
    plan = []
    project_type = detect_project_type(project_path)

    # Check what already exists
    has_esi_client = any(
        'ESIClient' in f.read_text(errors='ignore')
        for f in project_path.rglob('*.py')
        if f.is_file()
    )

    readme_path = project_path / 'README.md'
    has_attribution = False
    if readme_path.exists():
        has_attribution = 'CCP' in readme_path.read_text(errors='ignore')

    # Plan ESI client
    if not components or 'esi' in components:
        if not has_esi_client:
            if project_type == 'game':
                dest = project_path / 'core' / 'esi_client.py'
            elif project_type == 'api':
                dest = project_path / 'app' / 'esi_client.py'
            else:
                dest = project_path / 'esi_client.py'

            plan.append({
                "action": UpdateAction.ADD_FILE,
                "path": str(dest),
                "template": "esi_client",
                "description": "Add ESI client with compliance features"
            })

    # Plan attribution
    if not has_attribution:
        plan.append({
            "action": UpdateAction.MODIFY_FILE,
            "path": str(readme_path),
            "template": "attribution",
            "description": "Add CCP attribution to README"
        })

    # Plan ship sprites for games
    if project_type == 'game' and (not components or 'sprites' in components):
        sprites_path = project_path / 'core' / 'ship_sprites.py'
        if not sprites_path.exists():
            plan.append({
                "action": UpdateAction.ADD_FILE,
                "path": str(sprites_path),
                "template": "ship_sprites",
                "description": "Add ship sprite manager with Image Server integration"
            })

    # Plan dependencies
    deps_to_add = set()
    for item in plan:
        template = item.get("template")
        if template in REQUIREMENTS_ADDITIONS:
            deps_to_add.update(REQUIREMENTS_ADDITIONS[template])

    if deps_to_add:
        plan.append({
            "action": UpdateAction.ADD_DEPENDENCY,
            "dependencies": list(deps_to_add),
            "description": f"Add dependencies: {', '.join(deps_to_add)}"
        })

    return plan


def apply_updates(project_path: Path, plan: List[Dict], dry_run: bool = False) -> None:
    """Apply planned updates to project."""
    project_name = project_path.name

    for item in plan:
        action = item["action"]
        print(f"\n{'[DRY RUN] ' if dry_run else ''}Applying: {item['description']}")

        if dry_run:
            continue

        if action == UpdateAction.ADD_FILE:
            path = Path(item["path"])
            path.parent.mkdir(parents=True, exist_ok=True)

            template_name = item["template"]
            if template_name == "esi_client":
                content = ESI_CLIENT_TEMPLATE.format(project_name=project_name)
            elif template_name == "ship_sprites":
                content = SHIP_SPRITES_TEMPLATE.format(project_name=project_name)
            else:
                content = f"# Template: {template_name}"

            path.write_text(content)
            print(f"  ✅ Created: {path}")

        elif action == UpdateAction.MODIFY_FILE:
            path = Path(item["path"])
            template_name = item["template"]

            if template_name == "attribution":
                if path.exists():
                    content = path.read_text()
                    if "## Attribution" not in content:
                        content += "\n" + ATTRIBUTION_TEMPLATE
                        path.write_text(content)
                        print(f"  ✅ Updated: {path}")
                else:
                    path.write_text(f"# {project_name}\n" + ATTRIBUTION_TEMPLATE)
                    print(f"  ✅ Created: {path}")

        elif action == UpdateAction.ADD_DEPENDENCY:
            req_path = project_path / "requirements.txt"
            existing = set()
            if req_path.exists():
                existing = set(req_path.read_text().strip().split('\n'))

            new_deps = set(item["dependencies"]) - existing
            if new_deps:
                with open(req_path, 'a') as f:
                    f.write('\n' + '\n'.join(new_deps) + '\n')
                print(f"  ✅ Added to requirements.txt: {', '.join(new_deps)}")


def main():
    parser = argparse.ArgumentParser(description="Update EVE projects with ESI integration")
    parser.add_argument("project", type=Path, help="Project path to update")
    parser.add_argument("--plan", action="store_true", help="Show update plan only")
    parser.add_argument("--apply", action="store_true", help="Apply updates")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done")
    parser.add_argument("--component", "-c", action="append", dest="components",
                       choices=["esi", "sso", "sprites", "attribution"],
                       help="Specific components to update")

    args = parser.parse_args()

    if not args.project.exists():
        print(f"Error: Project not found: {args.project}")
        sys.exit(1)

    project_type = detect_project_type(args.project)
    print(f"\n📁 Project: {args.project.name}")
    print(f"   Type: {project_type}")

    plan = plan_updates(args.project, args.components)

    if not plan:
        print("\n✅ Project is already up to date!")
        return

    print(f"\n📋 Update Plan ({len(plan)} items):")
    for i, item in enumerate(plan, 1):
        print(f"   {i}. {item['description']}")

    if args.apply or args.dry_run:
        print("\n" + "─" * 50)
        apply_updates(args.project, plan, dry_run=args.dry_run)

        if not args.dry_run:
            print("\n✅ Updates applied successfully!")
            print("   Run your tests to verify everything works.")
    else:
        print("\n💡 Run with --apply to implement these updates")
        print("   Run with --dry-run to preview changes")


if __name__ == "__main__":
    main()
