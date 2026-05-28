#!/usr/bin/env python3
"""
EVE_Ships Repository Rebuilder

Downloads ALL ship renders from the official EVE Image Server and creates
a properly organized, attributed repository.

Usage:
    python rebuild_eve_ships.py ~/projects/EVE_Ships
    python rebuild_eve_ships.py ~/projects/EVE_Ships --sizes 256,512
    python rebuild_eve_ships.py ~/projects/EVE_Ships --include-icons
"""

import argparse
import asyncio
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import List

import httpx

# ============================================================================
# COMPLETE EVE SHIP DATABASE
# Organized by class with type IDs, factions, and metadata
# ============================================================================

SHIP_DATABASE = {
    # ========== EMPIRE FRIGATES ==========
    "frigates": {
        # Minmatar
        "rifter": {"type_id": 587, "faction": "minmatar", "role": "combat"},
        "slasher": {"type_id": 585, "faction": "minmatar", "role": "combat"},
        "breacher": {"type_id": 598, "faction": "minmatar", "role": "combat"},
        "probe": {"type_id": 586, "faction": "minmatar", "role": "exploration"},
        "burst": {"type_id": 599, "faction": "minmatar", "role": "logistics"},
        "vigil": {"type_id": 3766, "faction": "minmatar", "role": "ewar"},

        # Gallente
        "tristan": {"type_id": 593, "faction": "gallente", "role": "combat"},
        "atron": {"type_id": 608, "faction": "gallente", "role": "combat"},
        "incursus": {"type_id": 594, "faction": "gallente", "role": "combat"},
        "imicus": {"type_id": 607, "faction": "gallente", "role": "exploration"},
        "navitas": {"type_id": 592, "faction": "gallente", "role": "logistics"},
        "maulus": {"type_id": 609, "faction": "gallente", "role": "ewar"},

        # Caldari
        "merlin": {"type_id": 603, "faction": "caldari", "role": "combat"},
        "kestrel": {"type_id": 602, "faction": "caldari", "role": "combat"},
        "condor": {"type_id": 583, "faction": "caldari", "role": "combat"},
        "heron": {"type_id": 605, "faction": "caldari", "role": "exploration"},
        "bantam": {"type_id": 582, "faction": "caldari", "role": "logistics"},
        "griffin": {"type_id": 584, "faction": "caldari", "role": "ewar"},

        # Amarr
        "punisher": {"type_id": 597, "faction": "amarr", "role": "combat"},
        "executioner": {"type_id": 589, "faction": "amarr", "role": "combat"},
        "tormentor": {"type_id": 591, "faction": "amarr", "role": "combat"},
        "magnate": {"type_id": 29248, "faction": "amarr", "role": "exploration"},
        "inquisitor": {"type_id": 590, "faction": "amarr", "role": "logistics"},
        "crucifier": {"type_id": 2161, "faction": "amarr", "role": "ewar"},
    },

    # ========== DESTROYERS ==========
    "destroyers": {
        # Minmatar
        "thrasher": {"type_id": 16242, "faction": "minmatar", "role": "combat"},
        "talwar": {"type_id": 32872, "faction": "minmatar", "role": "combat"},

        # Gallente
        "catalyst": {"type_id": 16240, "faction": "gallente", "role": "combat"},
        "algos": {"type_id": 32875, "faction": "gallente", "role": "combat"},

        # Caldari
        "cormorant": {"type_id": 16238, "faction": "caldari", "role": "combat"},
        "corax": {"type_id": 32876, "faction": "caldari", "role": "combat"},

        # Amarr
        "coercer": {"type_id": 16236, "faction": "amarr", "role": "combat"},
        "dragoon": {"type_id": 32874, "faction": "amarr", "role": "combat"},
    },

    # ========== CRUISERS ==========
    "cruisers": {
        # Minmatar
        "stabber": {"type_id": 622, "faction": "minmatar", "role": "combat"},
        "rupture": {"type_id": 629, "faction": "minmatar", "role": "combat"},
        "bellicose": {"type_id": 630, "faction": "minmatar", "role": "combat"},
        "scythe": {"type_id": 631, "faction": "minmatar", "role": "logistics"},

        # Gallente
        "thorax": {"type_id": 627, "faction": "gallente", "role": "combat"},
        "vexor": {"type_id": 626, "faction": "gallente", "role": "combat"},
        "celestis": {"type_id": 633, "faction": "gallente", "role": "ewar"},
        "exequror": {"type_id": 634, "faction": "gallente", "role": "logistics"},

        # Caldari
        "caracal": {"type_id": 621, "faction": "caldari", "role": "combat"},
        "moa": {"type_id": 623, "faction": "caldari", "role": "combat"},
        "blackbird": {"type_id": 632, "faction": "caldari", "role": "ewar"},
        "osprey": {"type_id": 620, "faction": "caldari", "role": "logistics"},

        # Amarr
        "maller": {"type_id": 624, "faction": "amarr", "role": "combat"},
        "omen": {"type_id": 625, "faction": "amarr", "role": "combat"},
        "arbitrator": {"type_id": 628, "faction": "amarr", "role": "ewar"},
        "augoror": {"type_id": 619, "faction": "amarr", "role": "logistics"},
    },

    # ========== BATTLECRUISERS ==========
    "battlecruisers": {
        # Minmatar
        "hurricane": {"type_id": 24702, "faction": "minmatar", "role": "combat"},
        "cyclone": {"type_id": 24700, "faction": "minmatar", "role": "combat"},
        "tornado": {"type_id": 4310, "faction": "minmatar", "role": "attack"},

        # Gallente
        "brutix": {"type_id": 16229, "faction": "gallente", "role": "combat"},
        "myrmidon": {"type_id": 24698, "faction": "gallente", "role": "combat"},
        "talos": {"type_id": 4308, "faction": "gallente", "role": "attack"},

        # Caldari
        "drake": {"type_id": 24690, "faction": "caldari", "role": "combat"},
        "ferox": {"type_id": 24688, "faction": "caldari", "role": "combat"},
        "naga": {"type_id": 4306, "faction": "caldari", "role": "attack"},

        # Amarr
        "harbinger": {"type_id": 24696, "faction": "amarr", "role": "combat"},
        "prophecy": {"type_id": 24692, "faction": "amarr", "role": "combat"},
        "oracle": {"type_id": 4302, "faction": "amarr", "role": "attack"},
    },

    # ========== BATTLESHIPS ==========
    "battleships": {
        # Minmatar
        "tempest": {"type_id": 639, "faction": "minmatar", "role": "combat"},
        "typhoon": {"type_id": 644, "faction": "minmatar", "role": "combat"},
        "maelstrom": {"type_id": 24694, "faction": "minmatar", "role": "combat"},

        # Gallente
        "megathron": {"type_id": 641, "faction": "gallente", "role": "combat"},
        "dominix": {"type_id": 645, "faction": "gallente", "role": "combat"},
        "hyperion": {"type_id": 24690, "faction": "gallente", "role": "combat"},

        # Caldari
        "raven": {"type_id": 638, "faction": "caldari", "role": "combat"},
        "scorpion": {"type_id": 640, "faction": "caldari", "role": "ewar"},
        "rokh": {"type_id": 24688, "faction": "caldari", "role": "combat"},

        # Amarr
        "apocalypse": {"type_id": 642, "faction": "amarr", "role": "combat"},
        "armageddon": {"type_id": 643, "faction": "amarr", "role": "combat"},
        "abaddon": {"type_id": 24692, "faction": "amarr", "role": "combat"},
    },

    # ========== FACTION/PIRATE SHIPS ==========
    "faction": {
        # Angel Cartel
        "dramiel": {"type_id": 17703, "faction": "angel", "role": "frigate"},
        "cynabal": {"type_id": 17715, "faction": "angel", "role": "cruiser"},
        "machariel": {"type_id": 17738, "faction": "angel", "role": "battleship"},

        # Sansha's Nation
        "succubus": {"type_id": 17924, "faction": "sansha", "role": "frigate"},
        "phantasm": {"type_id": 17718, "faction": "sansha", "role": "cruiser"},
        "nightmare": {"type_id": 17736, "faction": "sansha", "role": "battleship"},

        # Serpentis
        "daredevil": {"type_id": 17928, "faction": "serpentis", "role": "frigate"},
        "vigilant": {"type_id": 17720, "faction": "serpentis", "role": "cruiser"},
        "vindicator": {"type_id": 17740, "faction": "serpentis", "role": "battleship"},

        # Blood Raiders
        "cruor": {"type_id": 17926, "faction": "blood", "role": "frigate"},
        "ashimmu": {"type_id": 17922, "faction": "blood", "role": "cruiser"},
        "bhaalgorn": {"type_id": 17920, "faction": "blood", "role": "battleship"},

        # Guristas
        "worm": {"type_id": 17930, "faction": "guristas", "role": "frigate"},
        "gila": {"type_id": 17715, "faction": "guristas", "role": "cruiser"},
        "rattlesnake": {"type_id": 17918, "faction": "guristas", "role": "battleship"},

        # Sisters of EVE
        "astero": {"type_id": 33468, "faction": "soe", "role": "frigate"},
        "stratios": {"type_id": 33470, "faction": "soe", "role": "cruiser"},
        "nestor": {"type_id": 33472, "faction": "soe", "role": "battleship"},
    },

    # ========== CAPITAL SHIPS ==========
    "capitals": {
        # Dreadnoughts
        "naglfar": {"type_id": 19724, "faction": "minmatar", "role": "dreadnought"},
        "moros": {"type_id": 19720, "faction": "gallente", "role": "dreadnought"},
        "phoenix": {"type_id": 19726, "faction": "caldari", "role": "dreadnought"},
        "revelation": {"type_id": 19722, "faction": "amarr", "role": "dreadnought"},

        # Carriers
        "nidhoggur": {"type_id": 24483, "faction": "minmatar", "role": "carrier"},
        "thanatos": {"type_id": 23911, "faction": "gallente", "role": "carrier"},
        "chimera": {"type_id": 23915, "faction": "caldari", "role": "carrier"},
        "archon": {"type_id": 23757, "faction": "amarr", "role": "carrier"},

        # Force Auxiliaries
        "lif": {"type_id": 37605, "faction": "minmatar", "role": "fax"},
        "ninazu": {"type_id": 37607, "faction": "gallente", "role": "fax"},
        "minokawa": {"type_id": 37606, "faction": "caldari", "role": "fax"},
        "apostle": {"type_id": 37604, "faction": "amarr", "role": "fax"},
    },

    # ========== SUPERCAPITALS ==========
    "supercapitals": {
        # Supercarriers
        "hel": {"type_id": 22852, "faction": "minmatar", "role": "supercarrier"},
        "nyx": {"type_id": 23913, "faction": "gallente", "role": "supercarrier"},
        "wyvern": {"type_id": 23917, "faction": "caldari", "role": "supercarrier"},
        "aeon": {"type_id": 23919, "faction": "amarr", "role": "supercarrier"},

        # Titans
        "ragnarok": {"type_id": 11568, "faction": "minmatar", "role": "titan"},
        "erebus": {"type_id": 671, "faction": "gallente", "role": "titan"},
        "leviathan": {"type_id": 3764, "faction": "caldari", "role": "titan"},
        "avatar": {"type_id": 11567, "faction": "amarr", "role": "titan"},
    },

    # ========== INDUSTRIAL & SPECIALTY ==========
    "industrial": {
        # Haulers
        "mammoth": {"type_id": 652, "faction": "minmatar", "role": "hauler"},
        "iteron_v": {"type_id": 657, "faction": "gallente", "role": "hauler"},
        "badger": {"type_id": 648, "faction": "caldari", "role": "hauler"},
        "bestower": {"type_id": 1944, "faction": "amarr", "role": "hauler"},

        # Mining
        "venture": {"type_id": 32880, "faction": "ore", "role": "mining"},
        "procurer": {"type_id": 17480, "faction": "ore", "role": "mining"},
        "retriever": {"type_id": 17478, "faction": "ore", "role": "mining"},
        "covetor": {"type_id": 17476, "faction": "ore", "role": "mining"},
        "hulk": {"type_id": 22544, "faction": "ore", "role": "mining"},
        "skiff": {"type_id": 22546, "faction": "ore", "role": "mining"},
        "mackinaw": {"type_id": 22548, "faction": "ore", "role": "mining"},

        # Orca/Rorqual
        "orca": {"type_id": 28606, "faction": "ore", "role": "command"},
        "rorqual": {"type_id": 28352, "faction": "ore", "role": "capital_industrial"},

        # Freighters
        "fenrir": {"type_id": 20189, "faction": "minmatar", "role": "freighter"},
        "obelisk": {"type_id": 20187, "faction": "gallente", "role": "freighter"},
        "charon": {"type_id": 20185, "faction": "caldari", "role": "freighter"},
        "providence": {"type_id": 20183, "faction": "amarr", "role": "freighter"},
    },
}

IMAGE_SERVER = "https://images.evetech.net"
VALID_SIZES = [32, 64, 128, 256, 512, 1024]


README_TEMPLATE = '''# EVE Ships - Official Render Collection

A complete collection of EVE Online ship renders from the official [EVE Image Server](https://images.evetech.net/).

![Ships Banner](renders/512/machariel_17738.png)

## 📊 Collection Stats

- **Total Ships:** {total_ships}
- **Ship Classes:** {ship_classes}
- **Render Sizes:** {sizes}
- **Last Updated:** {date}

## 📁 Directory Structure

```
EVE_Ships/
├── renders/
│   ├── 64/           # Small thumbnails
│   ├── 256/          # Medium (default)
│   └── 512/          # Large/HD
├── icons/
│   ├── 32/           # Inventory icons
│   └── 64/           # Large icons
├── by_faction/       # Symlinks organized by faction
├── by_class/         # Symlinks organized by ship class
├── manifest.json     # Complete ship database
└── README.md
```

## 🚀 Quick Usage

### Python
```python
from pathlib import Path

def get_ship_render(name: str, size: int = 256) -> Path:
    return Path(f"renders/{size}/{name}.png")

# Get Machariel render
machariel = get_ship_render("machariel_17738", 512)
```

### Web/React
```jsx
const ShipImage = ({ name, size = 256 }) => (
  <img src={`/eve_ships/renders/${size}/${name}.png`} alt={name} />
);
```

### Direct from EVE Image Server
```
https://images.evetech.net/types/{type_id}/render?size={size}
```

## 📋 Ship Manifest

See `manifest.json` for complete ship database with:
- Type IDs
- Factions
- Ship classes
- Roles

## 🔗 Links

- [EVE Image Server](https://images.evetech.net/)
- [EVE Developers](https://developers.eveonline.com/)
- [ESI API](https://esi.evetech.net/)

## ⚖️ Attribution

EVE Online and the EVE logo are registered trademarks of [CCP hf](https://www.ccpgames.com/).

All ship images are property of CCP and are used in accordance with the
[EVE Online Content Creation Terms of Use](https://community.eveonline.com/support/policies/content-creation-terms-of-use/).

This repository is not affiliated with or endorsed by CCP hf.

## 📄 License

Ship images: © CCP hf. Used under Content Creation Terms.
Repository structure and scripts: MIT License
'''


async def download_image(
    client: httpx.AsyncClient,
    type_id: int,
    name: str,
    size: int,
    variation: str,
    output_dir: Path
) -> bool:
    """Download a single image."""
    url = f"{IMAGE_SERVER}/types/{type_id}/{variation}?size={size}"
    filename = f"{name}_{type_id}.png"
    output_path = output_dir / filename

    if output_path.exists():
        return True  # Already have it

    try:
        response = await client.get(url, follow_redirects=True)
        if response.status_code == 200:
            output_path.write_bytes(response.content)
            return True
    except Exception as e:
        print(f"  ❌ Failed: {name} - {e}")

    return False


async def download_all_ships(
    output_dir: Path,
    sizes: List[int] = [256, 512],
    include_icons: bool = False,
    progress_callback=None
):
    """Download all ships."""
    renders_dir = output_dir / "renders"
    icons_dir = output_dir / "icons"

    # Create size directories
    for size in sizes:
        (renders_dir / str(size)).mkdir(parents=True, exist_ok=True)
        if include_icons:
            (icons_dir / str(size)).mkdir(parents=True, exist_ok=True)

    # Count total downloads
    total_ships = sum(len(ships) for ships in SHIP_DATABASE.values())
    total_downloads = total_ships * len(sizes) * (2 if include_icons else 1)

    print(f"\n📥 Downloading {total_ships} ships in {len(sizes)} sizes...")
    print(f"   Total images: {total_downloads}")
    print("-" * 50)

    completed = 0
    failed = 0

    semaphore = asyncio.Semaphore(10)  # Limit concurrent downloads

    async def bounded_download(client, type_id, name, size, variation, out_dir):
        async with semaphore:
            return await download_image(client, type_id, name, size, variation, out_dir)

    async with httpx.AsyncClient(timeout=30.0) as client:
        for ship_class, ships in SHIP_DATABASE.items():
            print(f"\n🚀 {ship_class.upper()} ({len(ships)} ships)")

            tasks = []
            for name, info in ships.items():
                type_id = info["type_id"]

                for size in sizes:
                    # Render
                    tasks.append((
                        bounded_download(
                            client, type_id, name, size, "render",
                            renders_dir / str(size)
                        ),
                        name, "render"
                    ))

                    # Icon
                    if include_icons and size <= 64:
                        tasks.append((
                            bounded_download(
                                client, type_id, name, size, "icon",
                                icons_dir / str(size)
                            ),
                            name, "icon"
                        ))

            # Execute tasks
            results = await asyncio.gather(*[t[0] for t in tasks])

            for result, (_, name, var) in zip(results, tasks):
                if result:
                    completed += 1
                else:
                    failed += 1

            success_rate = (completed / (completed + failed)) * 100 if (completed + failed) > 0 else 0
            print(f"   ✅ {completed} downloaded, ❌ {failed} failed ({success_rate:.0f}%)")

    return completed, failed


def create_manifest(output_dir: Path):
    """Create manifest.json with all ship data."""
    manifest = {
        "generated": datetime.now().isoformat(),
        "source": "EVE Image Server (images.evetech.net)",
        "total_ships": sum(len(ships) for ships in SHIP_DATABASE.values()),
        "ships": {},
        "by_type_id": {},
        "by_faction": {},
        "by_class": {}
    }

    for ship_class, ships in SHIP_DATABASE.items():
        manifest["by_class"][ship_class] = []

        for name, info in ships.items():
            type_id = info["type_id"]
            faction = info["faction"]

            ship_entry = {
                "name": name,
                "type_id": type_id,
                "faction": faction,
                "class": ship_class,
                "role": info.get("role", "combat"),
                "render_url": f"https://images.evetech.net/types/{type_id}/render",
                "icon_url": f"https://images.evetech.net/types/{type_id}/icon"
            }

            manifest["ships"][name] = ship_entry
            manifest["by_type_id"][str(type_id)] = name
            manifest["by_class"][ship_class].append(name)

            if faction not in manifest["by_faction"]:
                manifest["by_faction"][faction] = []
            manifest["by_faction"][faction].append(name)

    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print("✅ Created manifest.json")

    return manifest


def create_readme(output_dir: Path, sizes: List[int]):
    """Create README.md."""
    total_ships = sum(len(ships) for ships in SHIP_DATABASE.values())
    ship_classes = len(SHIP_DATABASE)

    readme = README_TEMPLATE.format(
        total_ships=total_ships,
        ship_classes=ship_classes,
        sizes=", ".join(str(s) for s in sizes),
        date=datetime.now().strftime("%Y-%m-%d")
    )

    readme_path = output_dir / "README.md"
    readme_path.write_text(readme)
    print("✅ Created README.md")


def create_symlink_structure(output_dir: Path):
    """Create organized symlink directories."""
    renders_dir = output_dir / "renders"
    by_faction = output_dir / "by_faction"
    by_class = output_dir / "by_class"

    # Clean existing
    if by_faction.exists():
        shutil.rmtree(by_faction)
    if by_class.exists():
        shutil.rmtree(by_class)

    by_faction.mkdir()
    by_class.mkdir()

    # Find a valid size directory
    size_dirs = [d for d in renders_dir.iterdir() if d.is_dir()]
    if not size_dirs:
        return

    default_size = size_dirs[0].name

    for ship_class, ships in SHIP_DATABASE.items():
        class_dir = by_class / ship_class
        class_dir.mkdir(exist_ok=True)

        for name, info in ships.items():
            faction = info["faction"]
            type_id = info["type_id"]
            filename = f"{name}_{type_id}.png"

            # By class
            source = Path("..") / "renders" / default_size / filename
            target = class_dir / filename
            try:
                target.symlink_to(source)
            except Exception:
                pass

            # By faction
            faction_dir = by_faction / faction
            faction_dir.mkdir(exist_ok=True)
            source = Path("..") / "renders" / default_size / filename
            target = faction_dir / filename
            try:
                target.symlink_to(source)
            except Exception:
                pass

    print("✅ Created symlink structure")


def create_gitignore(output_dir: Path):
    """Create .gitignore."""
    gitignore = """# OS files
.DS_Store
Thumbs.db

# Python
__pycache__/
*.pyc
.venv/

# IDE
.vscode/
.idea/

# Temp
*.tmp
*.bak
"""
    (output_dir / ".gitignore").write_text(gitignore)
    print("✅ Created .gitignore")


async def rebuild_repository(
    output_dir: Path,
    sizes: List[int] = [256, 512],
    include_icons: bool = False,
    backup: bool = True
):
    """Complete repository rebuild."""
    print("\n" + "=" * 60)
    print("  EVE_Ships Repository Rebuilder")
    print("=" * 60)

    # Backup existing
    if output_dir.exists() and backup:
        backup_dir = output_dir.parent / f"{output_dir.name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        print(f"\n📦 Backing up existing repo to: {backup_dir.name}")
        shutil.move(str(output_dir), str(backup_dir))

    # Create fresh directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Download all ships
    completed, failed = await download_all_ships(
        output_dir,
        sizes=sizes,
        include_icons=include_icons
    )

    # Create manifest
    print("\n📋 Creating manifest and documentation...")
    manifest = create_manifest(output_dir)
    create_readme(output_dir, sizes)
    create_gitignore(output_dir)

    # Create symlink structure
    print("\n🔗 Creating organized symlinks...")
    create_symlink_structure(output_dir)

    # Summary
    print("\n" + "=" * 60)
    print("  ✅ REBUILD COMPLETE")
    print("=" * 60)
    print("\n📊 Summary:")
    print(f"   Ships: {manifest['total_ships']}")
    print(f"   Classes: {len(SHIP_DATABASE)}")
    print(f"   Factions: {len(manifest['by_faction'])}")
    print(f"   Images downloaded: {completed}")
    print(f"   Failed: {failed}")
    print(f"   Sizes: {sizes}")
    print(f"\n📁 Output: {output_dir}")

    print("\n💡 Next steps:")
    print("   cd", output_dir)
    print("   git init")
    print("   git add .")
    print('   git commit -m "Initial commit: Official EVE ship renders"')
    print("   git remote add origin https://github.com/AreteDriver/EVE_Ships.git")
    print("   git push -u origin main --force")


def main():
    parser = argparse.ArgumentParser(
        description="Rebuild EVE_Ships with official Image Server renders",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s ~/projects/EVE_Ships
    %(prog)s ~/projects/EVE_Ships --sizes 64,256,512
    %(prog)s ~/projects/EVE_Ships --include-icons --no-backup
        """
    )

    parser.add_argument("output", type=Path, help="Output directory (e.g., ~/projects/EVE_Ships)")
    parser.add_argument("--sizes", type=str, default="256,512",
                       help="Comma-separated render sizes (default: 256,512)")
    parser.add_argument("--include-icons", action="store_true",
                       help="Also download inventory icons")
    parser.add_argument("--no-backup", action="store_true",
                       help="Don't backup existing directory")

    args = parser.parse_args()

    sizes = [int(s.strip()) for s in args.sizes.split(",")]
    sizes = [s for s in sizes if s in VALID_SIZES]

    if not sizes:
        print("Error: No valid sizes specified")
        print(f"Valid sizes: {VALID_SIZES}")
        return

    asyncio.run(rebuild_repository(
        args.output.expanduser(),
        sizes=sizes,
        include_icons=args.include_icons,
        backup=not args.no_backup
    ))


if __name__ == "__main__":
    main()
