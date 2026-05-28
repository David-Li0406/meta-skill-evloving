# Proton Version Selection Guide

Guide for choosing the right Proton version for different games and scenarios.

## Proton Version Types

### Official Valve Proton

**Proton Stable (e.g., Proton 9.0)**
- Latest stable release from Valve
- Thoroughly tested
- Recommended for most games
- Updated less frequently

**Proton Experimental**
- Bleeding edge features
- Latest fixes and improvements
- Updated frequently (weekly/bi-weekly)
- May have occasional regressions
- Recommended for: New releases, recently broken games

**Proton Hotfix**
- Emergency fixes for major issues
- Based on latest stable
- Rarely released

### Proton-GE (GloriousEggroll)

Community-built Proton with extra patches and fixes.

**Features:**
- Additional game-specific fixes
- Codec support (video cutscenes)
- Extra compatibility patches
- Faster updates for new games
- Alternative to waiting for official Proton updates

**Download:** https://github.com/GloriousEggroll/proton-ge-custom/releases

**Installation (via ProtonUp-Qt):**
```bash
sudo pacman -S protonup-qt
```

Then use GUI to install latest Proton-GE.

**Manual installation:**
```bash
cd ~/.steam/steam/compatdata/
wget <latest-proton-ge-release.tar.gz>
tar -xf proton-ge-*.tar.gz
mv GE-Proton* ~/.steam/steam/compatdata/
```

### Automated Management with manage_proton_ge.sh

The ProtonDB skill includes a comprehensive Proton-GE manager for automated installation and version management.

#### Quick Start

**List installed versions:**
```bash
scripts/manage_proton_ge.sh list
```

**Install latest version:**
```bash
scripts/manage_proton_ge.sh install
```

**Install specific version:**
```bash
scripts/manage_proton_ge.sh install GE-Proton9-1
```

**Get game-specific recommendation:**
```bash
scripts/manage_proton_ge.sh get-recommended <app_id>
```

#### All Available Commands

| Command | Description |
|---------|-------------|
| `list` | Show installed Proton-GE versions with dates and sizes |
| `list-available` | Show latest releases available on GitHub |
| `install [version]` | Install specific version or latest if none specified |
| `remove <version>` | Remove installed version (with confirmation) |
| `check-updates` | Check if newer version available |
| `get-recommended <app_id>` | Extract recommended version from ProtonDB reports |

#### Features

- **Auto-detection:** Automatically detects native Steam or Flatpak installation
- **Checksum verification:** SHA512 verification ensures download integrity
- **Update notifications:** Check for and install newer releases
- **Game recommendations:** Analyzes ProtonDB reports to suggest best version
- **Safe removal:** Confirmation prompts prevent accidental deletion
- **Progress feedback:** Clear status updates during operations

#### Integration with Game Analysis

The manager integrates automatically with other ProtonDB scripts:

```bash
# check_game.sh will suggest Proton-GE for Silver-rated games
scripts/check_game.sh 1245620

# generate_launch_options.sh highlights GE version usage
scripts/generate_launch_options.sh 1245620 --amd-only
```

### Proton Versions Comparison

| Version | Update Frequency | Stability | Game Support | Use Case |
|---------|-----------------|-----------|--------------|----------|
| Stable | Quarterly | Very High | Established games | Default choice |
| Experimental | Weekly | High | Latest games | New releases |
| GE | Weekly | High | Broadest | Problem games |

## Selection Strategy

### By Game Age

**Brand new games (< 1 month):**
1. Try Proton Experimental first
2. If issues, try latest Proton-GE
3. Fallback to stable if both fail

**Recent games (1-6 months):**
1. Try Proton Stable
2. If issues, try Experimental
3. Try Proton-GE as last resort

**Established games (> 6 months):**
1. Use Proton Stable
2. Only change if specific issues

**Old games (> 3 years):**
1. Use Proton Stable
2. Try older Proton versions if issues
3. May need PROTON_USE_WINED3D=1

### By ProtonDB Rating

**Platinum/Gold ratings:**
- Use Proton Stable
- Should work out of box

**Silver rating:**
- Check ProtonDB for recommended version
- May need Proton-GE
- Likely needs custom launch options

**Bronze rating:**
- Try multiple Proton versions
- Check ProtonDB for specific version that works
- May need significant workarounds

**Borked rating:**
- Check if recently updated
- Try all available Proton versions
- Look for anti-cheat issues (may be unfixable)

### By Game Engine

**Unreal Engine 4/5:**
- Usually works well on Proton Stable
- Some UE5 games need Experimental
- Shader compilation stutter common (use DXVK_ASYNC=1)

**Unity:**
- Generally excellent compatibility
- Proton Stable sufficient
- Older Unity games may need PROTON_USE_WINED3D=1

**Source Engine:**
- Native Linux versions available for most
- If using Windows version, any Proton works

**Creation Engine (Bethesda):**
- Proton-GE often recommended
- Better mod support than official Proton
- Check community recommendations per game

**REDengine (CD Projekt Red):**
- Excellent compatibility
- Proton Stable works well
- RT features may need Experimental

**id Tech (id Software):**
- Many have native Linux ports (use those)
- Windows versions work on any Proton

### By DRM/Anti-Cheat

**Steam DRM only:**
- Any Proton version
- Choose based on game age

**Denuvo:**
- May cause issues with frequent Proton changes
- Stick to one Proton version
- Activation limits may trigger

**EasyAntiCheat (EAC):**
- Check ProtonDB for EAC status
- Some games whitelisted, most blocked
- If whitelisted, use Proton Stable or Experimental

**BattleEye:**
- Similar to EAC
- Game-by-game basis
- Check ProtonDB compatibility

**No DRM:**
- Any Proton version
- Most flexible

## Version-Specific Known Issues

### Proton 9.0

**Strengths:**
- Excellent DX11/DX12 support
- Strong VKD3D-Proton integration
- AMD ray tracing working well

**Known issues:**
- Some older DirectX 9 games have regressions
- Specific Unity games may have audio issues

**Best for:** Modern AAA games (2020+)

### Proton Experimental

**Strengths:**
- Latest DXVK and VKD3D-Proton
- Cutting-edge game support
- Quick fixes for new releases

**Known issues:**
- Occasional regressions
- May break previously working games
- Less tested

**Best for:** Latest releases, broken games on stable

### Proton-GE

**Strengths:**
- Extra codec support (video cutscenes)
- Additional game-specific patches
- Broader compatibility
- Faster community bug fixes

**Known issues:**
- Not officially supported by Valve
- May have conflicts with Steam updates
- More frequent version churn

**Best for:** Problem games, need video codec support

## Switching Proton Versions

### In Steam

1. Right-click game in library
2. Properties → Compatibility
3. Force the use of a specific Steam Play compatibility tool
4. Select desired Proton version
5. Close properties
6. Launch game

### Testing Multiple Versions

Keep notes on what works:
```bash
# Create a testing log
echo "Game: Elden Ring (1245620)" > ~/proton-test.log
echo "Test 1: Proton 9.0 - Works, 60 FPS" >> ~/proton-test.log
echo "Test 2: Experimental - Shader stutter" >> ~/proton-test.log
echo "Test 3: GE-Proton9-1 - Best performance, 75 FPS" >> ~/proton-test.log
```

## Proton Version Compatibility Database

### Games Known to Need Specific Versions

**Proton-GE Recommended:**
- Cyberpunk 2077 (video cutscenes)
- Red Dead Redemption 2 (codec support)
- Fall Guys (EAC support)
- Dead by Daylight (EAC support)

**Proton Experimental Recommended:**
- Latest Call of Duty (if supported)
- New Unreal Engine 5 games
- Games with very recent updates

**Older Proton Recommended:**
- Some legacy DirectX 9 games
- Games broken in recent Proton versions
- Check ProtonDB for specific version

## ProtonDB Version Notation

When reading ProtonDB reports:

**Format examples:**
- `Proton 9.0-1` - Official Stable
- `Proton Experimental` - Latest experimental
- `GE-Proton9-1` - Proton-GE version 9-1
- `Proton 8.0-5` - Older stable version

**How to match:**
- Steam shows: "Proton 9.0" → Report means "Proton 9.0-x"
- Steam shows: "Proton Experimental" → Report means current Experimental
- Proton-GE versions are distinct, check exact version number

## Installing Specific Proton-GE Versions

### Via ProtonUp-Qt (Recommended)

```bash
# Install tool
sudo pacman -S protonup-qt

# Launch GUI
protonup-qt
```

Select specific GE version from list, install.

### Manual Installation

```bash
# Download specific version
cd ~/.steam/steam/compatdata
wget https://github.com/GloriousEggroll/proton-ge-custom/releases/download/GE-Proton9-1/GE-Proton9-1.tar.gz

# Extract
tar -xf GE-Proton9-1.tar.gz

# Move to compatibility tools directory
mkdir -p ~/.steam/steam/compatibilitytools.d
mv GE-Proton9-1 ~/.steam/steam/compatibilitytools.d/

# Restart Steam
```

## Downgrading to Older Official Proton

Older Proton versions available via Steam Beta branches:

1. Right-click game → Properties → Betas
2. Select older Proton version if available
3. Or use ProtonUp-Qt to install older versions

**Note:** Not all old versions available this way.

## Keeping Proton Updated

### Official Proton

Auto-updates via Steam:
- Stable: Updates with major releases
- Experimental: Updates automatically (weekly-ish)

**Disable auto-update for specific game:**
Properties → Automatic Updates → Only update this game when I launch it

### Proton-GE

Check for updates via ProtonUp-Qt or manually:

```bash
# Check current version
ls ~/.steam/steam/compatibilitytools.d/

# Check latest release
curl -s https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases/latest | jq -r '.tag_name'
```

## Best Practices

1. **Start with Proton Stable** - works for most games
2. **Check ProtonDB first** - see what others use successfully
3. **Try Experimental for new games** - better support for latest releases
4. **Use Proton-GE for problem games** - extra patches help compatibility
5. **Document what works** - keep notes on successful configs
6. **Don't change if it works** - if game runs well, leave Proton version alone
7. **Test after major updates** - game updates may need Proton version change
8. **Clear shader cache when switching** - prevents issues: `rm -rf ~/.steam/steam/steamapps/shadercache/<APP_ID>`

## Version Selection Flowchart

```
Game just released (< 1 week)?
├─ Yes: Proton Experimental
│   ├─ Works? Keep it
│   └─ Broken? Try Proton-GE latest
└─ No: Continue

Game has Platinum/Gold on ProtonDB?
├─ Yes: Proton Stable
│   ├─ Works? Keep it
│   └─ Issues? Check ProtonDB comments for version
└─ No: Continue

ProtonDB shows specific version working?
├─ Yes: Use that version (install via ProtonUp-Qt if GE)
└─ No: Continue

Game has video cutscene issues?
└─ Yes: Try Proton-GE (has codecs)

Still not working?
└─ Try all versions systematically:
    1. Proton Stable
    2. Proton Experimental
    3. Latest Proton-GE
    4. Proton Stable - 1 version
    5. Older Proton-GE
```

## Community Resources

**Where to find version recommendations:**
- ProtonDB reports: https://www.protondb.com
- Proton GitHub: https://github.com/ValveSoftware/Proton/issues
- Reddit /r/linux_gaming: Community discussion
- ProtonGE GitHub: https://github.com/GloriousEggroll/proton-ge-custom

**Stay updated:**
- Watch ProtonGE releases: https://github.com/GloriousEggroll/proton-ge-custom/releases
- Follow @Plagman (Proton developer) on social media
- Check Steam announcements for Proton updates
