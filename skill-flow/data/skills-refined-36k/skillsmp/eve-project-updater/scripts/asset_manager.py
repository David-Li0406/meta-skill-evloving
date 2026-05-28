#!/usr/bin/env python3
"""
EVE Asset Manager

Centralized asset management for all EVE projects.
Downloads and syncs ship renders, icons, and other assets.

Usage:
    python asset_manager.py --sync-all
    python asset_manager.py --download-ships --output ~/eve_assets
    python asset_manager.py --link-to-project ~/projects/EVE_Rebellion
"""

import argparse
import asyncio
import json
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import httpx

# ============================================================================
# SHIP DATABASE
# ============================================================================

SHIP_DATABASE = {
    "frigates": {
        "rifter": {"type_id": 587, "faction": "minmatar"},
        "slasher": {"type_id": 585, "faction": "minmatar"},
        "breacher": {"type_id": 598, "faction": "minmatar"},
        "probe": {"type_id": 586, "faction": "minmatar"},
        "burst": {"type_id": 599, "faction": "minmatar"},
        "vigil": {"type_id": 3766, "faction": "minmatar"},

        "tristan": {"type_id": 593, "faction": "gallente"},
        "atron": {"type_id": 608, "faction": "gallente"},
        "incursus": {"type_id": 594, "faction": "gallente"},
        "imicus": {"type_id": 605, "faction": "gallente"},
        "navitas": {"type_id": 592, "faction": "gallente"},
        "maulus": {"type_id": 609, "faction": "gallente"},

        "merlin": {"type_id": 603, "faction": "caldari"},
        "kestrel": {"type_id": 602, "faction": "caldari"},
        "condor": {"type_id": 583, "faction": "caldari"},
        "heron": {"type_id": 605, "faction": "caldari"},
        "bantam": {"type_id": 582, "faction": "caldari"},
        "griffin": {"type_id": 584, "faction": "caldari"},

        "punisher": {"type_id": 597, "faction": "amarr"},
        "executioner": {"type_id": 589, "faction": "amarr"},
        "tormentor": {"type_id": 591, "faction": "amarr"},
        "magnate": {"type_id": 29248, "faction": "amarr"},
        "inquisitor": {"type_id": 590, "faction": "amarr"},
        "crucifier": {"type_id": 2161, "faction": "amarr"},
    },
    "cruisers": {
        "stabber": {"type_id": 622, "faction": "minmatar"},
        "rupture": {"type_id": 629, "faction": "minmatar"},
        "bellicose": {"type_id": 630, "faction": "minmatar"},
        "scythe": {"type_id": 631, "faction": "minmatar"},

        "thorax": {"type_id": 627, "faction": "gallente"},
        "vexor": {"type_id": 626, "faction": "gallente"},
        "celestis": {"type_id": 633, "faction": "gallente"},
        "exequror": {"type_id": 634, "faction": "gallente"},

        "caracal": {"type_id": 621, "faction": "caldari"},
        "moa": {"type_id": 623, "faction": "caldari"},
        "blackbird": {"type_id": 632, "faction": "caldari"},
        "osprey": {"type_id": 620, "faction": "caldari"},

        "maller": {"type_id": 624, "faction": "amarr"},
        "omen": {"type_id": 625, "faction": "amarr"},
        "arbitrator": {"type_id": 628, "faction": "amarr"},
        "augoror": {"type_id": 625, "faction": "amarr"},
    },
    "battlecruisers": {
        "hurricane": {"type_id": 24702, "faction": "minmatar"},
        "cyclone": {"type_id": 24700, "faction": "minmatar"},

        "brutix": {"type_id": 16229, "faction": "gallente"},
        "myrmidon": {"type_id": 24690, "faction": "gallente"},

        "drake": {"type_id": 24690, "faction": "caldari"},
        "ferox": {"type_id": 24688, "faction": "caldari"},

        "harbinger": {"type_id": 24696, "faction": "amarr"},
        "prophecy": {"type_id": 24692, "faction": "amarr"},
    },
    "battleships": {
        "tempest": {"type_id": 639, "faction": "minmatar"},
        "typhoon": {"type_id": 644, "faction": "minmatar"},
        "maelstrom": {"type_id": 24694, "faction": "minmatar"},

        "megathron": {"type_id": 641, "faction": "gallente"},
        "dominix": {"type_id": 645, "faction": "gallente"},
        "hyperion": {"type_id": 24690, "faction": "gallente"},

        "raven": {"type_id": 638, "faction": "caldari"},
        "scorpion": {"type_id": 640, "faction": "caldari"},
        "rokh": {"type_id": 24688, "faction": "caldari"},

        "apocalypse": {"type_id": 642, "faction": "amarr"},
        "armageddon": {"type_id": 643, "faction": "amarr"},
        "abaddon": {"type_id": 24692, "faction": "amarr"},
    },
    "faction": {
        "machariel": {"type_id": 17738, "faction": "angel"},
        "nightmare": {"type_id": 17736, "faction": "sansha"},
        "vindicator": {"type_id": 17740, "faction": "serpentis"},
        "bhaalgorn": {"type_id": 17920, "faction": "blood"},
        "rattlesnake": {"type_id": 17918, "faction": "guristas"},
        "phantasm": {"type_id": 17703, "faction": "sansha"},
        "vigilant": {"type_id": 17720, "faction": "serpentis"},
        "cynabal": {"type_id": 17715, "faction": "angel"},
    },
    "capitals": {
        "naglfar": {"type_id": 19724, "faction": "minmatar"},
        "moros": {"type_id": 19720, "faction": "gallente"},
        "phoenix": {"type_id": 19726, "faction": "caldari"},
        "revelation": {"type_id": 19722, "faction": "amarr"},

        "nidhoggur": {"type_id": 24483, "faction": "minmatar"},
        "thanatos": {"type_id": 23911, "faction": "gallente"},
        "chimera": {"type_id": 23915, "faction": "caldari"},
        "archon": {"type_id": 23757, "faction": "amarr"},
    },
    "supercapitals": {
        "hel": {"type_id": 22852, "faction": "minmatar"},
        "nyx": {"type_id": 23913, "faction": "gallente"},
        "wyvern": {"type_id": 23917, "faction": "caldari"},
        "aeon": {"type_id": 23919, "faction": "amarr"},

        "ragnarok": {"type_id": 11568, "faction": "minmatar"},
        "erebus": {"type_id": 671, "faction": "gallente"},
        "leviathan": {"type_id": 3764, "faction": "caldari"},
        "avatar": {"type_id": 11567, "faction": "amarr"},
    },
}

IMAGE_SERVER = "https://images.evetech.net"
VALID_SIZES = [32, 64, 128, 256, 512, 1024]


@dataclass
class DownloadResult:
    type_id: int
    name: str
    size: int
    success: bool
    path: Optional[Path] = None
    error: Optional[str] = None


class AssetManager:
    """Centralized asset management for EVE projects."""

    def __init__(self, asset_dir: Path):
        self.asset_dir = asset_dir
        self.ships_dir = asset_dir / "ships"
        self.icons_dir = asset_dir / "icons"
        self.manifest_path = asset_dir / "manifest.json"

        # Create directories
        self.ships_dir.mkdir(parents=True, exist_ok=True)
        self.icons_dir.mkdir(parents=True, exist_ok=True)

        # Load manifest
        self.manifest = self._load_manifest()

    def _load_manifest(self) -> Dict:
        """Load or create manifest."""
        if self.manifest_path.exists():
            return json.loads(self.manifest_path.read_text())
        return {
            "created": datetime.now().isoformat(),
            "updated": datetime.now().isoformat(),
            "ships": {},
            "downloads": []
        }

    def _save_manifest(self):
        """Save manifest to disk."""
        self.manifest["updated"] = datetime.now().isoformat()
        self.manifest_path.write_text(json.dumps(self.manifest, indent=2))

    async def download_ship(
        self,
        type_id: int,
        name: str,
        size: int = 256,
        variation: str = "render"
    ) -> DownloadResult:
        """Download a single ship image."""
        # Determine output path
        if variation == "render":
            output_dir = self.ships_dir / str(size)
        else:
            output_dir = self.icons_dir / str(size)

        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{name}_{type_id}.png"

        # Skip if exists
        if output_path.exists():
            return DownloadResult(type_id, name, size, True, output_path)

        # Download
        url = f"{IMAGE_SERVER}/types/{type_id}/{variation}?size={size}"

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, follow_redirects=True)

                if response.status_code == 200:
                    output_path.write_bytes(response.content)
                    return DownloadResult(type_id, name, size, True, output_path)
                else:
                    return DownloadResult(
                        type_id, name, size, False,
                        error=f"HTTP {response.status_code}"
                    )
        except Exception as e:
            return DownloadResult(type_id, name, size, False, error=str(e))

    async def download_all_ships(
        self,
        sizes: List[int] = [256],
        classes: Optional[List[str]] = None,
        factions: Optional[List[str]] = None
    ) -> List[DownloadResult]:
        """Download all ships matching criteria."""
        results = []
        tasks = []

        for ship_class, ships in SHIP_DATABASE.items():
            if classes and ship_class not in classes:
                continue

            for name, info in ships.items():
                if factions and info["faction"] not in factions:
                    continue

                for size in sizes:
                    tasks.append(self.download_ship(
                        info["type_id"],
                        name,
                        size
                    ))

        print(f"📥 Downloading {len(tasks)} images...")

        # Run with concurrency limit
        semaphore = asyncio.Semaphore(10)

        async def bounded_download(task):
            async with semaphore:
                return await task

        results = await asyncio.gather(*[bounded_download(t) for t in tasks])

        # Update manifest
        for result in results:
            if result.success:
                ship_key = f"{result.name}_{result.type_id}"
                if ship_key not in self.manifest["ships"]:
                    self.manifest["ships"][ship_key] = {
                        "type_id": result.type_id,
                        "name": result.name,
                        "sizes": []
                    }
                if result.size not in self.manifest["ships"][ship_key]["sizes"]:
                    self.manifest["ships"][ship_key]["sizes"].append(result.size)

        self._save_manifest()

        return results

    def link_to_project(self, project_path: Path, link_type: str = "symlink"):
        """Link assets to a project."""
        target_dir = project_path / "assets" / "eve_ships"

        if link_type == "symlink":
            # Create symlink
            if target_dir.exists():
                if target_dir.is_symlink():
                    target_dir.unlink()
                else:
                    shutil.rmtree(target_dir)

            target_dir.parent.mkdir(parents=True, exist_ok=True)
            target_dir.symlink_to(self.ships_dir.absolute())
            print(f"✅ Linked {self.ships_dir} → {target_dir}")

        elif link_type == "copy":
            # Copy files
            if target_dir.exists():
                shutil.rmtree(target_dir)
            shutil.copytree(self.ships_dir, target_dir)
            print(f"✅ Copied {self.ships_dir} → {target_dir}")

    def generate_type_mapping(self) -> Dict[str, int]:
        """Generate name to type_id mapping."""
        mapping = {}
        for ship_class, ships in SHIP_DATABASE.items():
            for name, info in ships.items():
                mapping[name] = info["type_id"]
        return mapping

    def get_stats(self) -> Dict:
        """Get asset statistics."""
        render_count = sum(1 for _ in self.ships_dir.rglob("*.png"))
        icon_count = sum(1 for _ in self.icons_dir.rglob("*.png"))
        total_size = sum(f.stat().st_size for f in self.asset_dir.rglob("*.png"))

        return {
            "renders": render_count,
            "icons": icon_count,
            "total_files": render_count + icon_count,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "ship_classes": len(SHIP_DATABASE),
            "unique_ships": sum(len(ships) for ships in SHIP_DATABASE.values())
        }


def print_stats(manager: AssetManager):
    """Print asset statistics."""
    stats = manager.get_stats()
    print("\n📊 Asset Statistics:")
    print(f"   Ship renders: {stats['renders']}")
    print(f"   Icons: {stats['icons']}")
    print(f"   Total files: {stats['total_files']}")
    print(f"   Total size: {stats['total_size_mb']} MB")
    print(f"   Ship database: {stats['unique_ships']} ships in {stats['ship_classes']} classes")


async def main():
    parser = argparse.ArgumentParser(description="EVE Asset Manager")
    parser.add_argument("--asset-dir", "-d", type=Path,
                       default=Path.home() / ".eve_assets",
                       help="Central asset directory")
    parser.add_argument("--sync-all", action="store_true",
                       help="Download all ships in all sizes")
    parser.add_argument("--download-ships", action="store_true",
                       help="Download ship renders")
    parser.add_argument("--sizes", type=str, default="256,512",
                       help="Comma-separated sizes to download")
    parser.add_argument("--classes", type=str,
                       help="Ship classes to download (frigates,cruisers,etc)")
    parser.add_argument("--factions", type=str,
                       help="Factions to download (minmatar,gallente,etc)")
    parser.add_argument("--link-to-project", type=Path,
                       help="Link assets to a project")
    parser.add_argument("--copy-to-project", type=Path,
                       help="Copy assets to a project")
    parser.add_argument("--stats", action="store_true",
                       help="Show asset statistics")
    parser.add_argument("--generate-mapping", action="store_true",
                       help="Generate type ID mapping JSON")

    args = parser.parse_args()

    manager = AssetManager(args.asset_dir)

    if args.stats:
        print_stats(manager)
        return

    if args.generate_mapping:
        mapping = manager.generate_type_mapping()
        output = args.asset_dir / "type_mapping.json"
        output.write_text(json.dumps(mapping, indent=2))
        print(f"✅ Generated type mapping: {output}")
        return

    if args.sync_all:
        sizes = [64, 256, 512]
        print(f"🔄 Syncing all ships in sizes: {sizes}")
        results = await manager.download_all_ships(sizes=sizes)
        success = sum(1 for r in results if r.success)
        print(f"\n✅ Downloaded {success}/{len(results)} images")
        print_stats(manager)

    elif args.download_ships:
        sizes = [int(s) for s in args.sizes.split(",")]
        classes = args.classes.split(",") if args.classes else None
        factions = args.factions.split(",") if args.factions else None

        results = await manager.download_all_ships(
            sizes=sizes,
            classes=classes,
            factions=factions
        )
        success = sum(1 for r in results if r.success)
        print(f"\n✅ Downloaded {success}/{len(results)} images")

    if args.link_to_project:
        manager.link_to_project(args.link_to_project, "symlink")

    if args.copy_to_project:
        manager.link_to_project(args.copy_to_project, "copy")


if __name__ == "__main__":
    asyncio.run(main())
