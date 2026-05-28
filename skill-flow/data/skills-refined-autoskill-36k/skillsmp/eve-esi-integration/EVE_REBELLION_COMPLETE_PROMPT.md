# EVE REBELLION — Complete Implementation Prompt
## Comprehensive Claude Code Setup Guide

---

# CONTEXT

You are building **EVE Rebellion**, a top-down arcade space shooter platform set in the EVE Online universe. This is a proof-of-concept demo designed to pitch a licensed mobile game to CCP Games. The project is being rewritten from Python/pygame to **Rust** for cross-platform deployment (Linux, Windows, macOS, iOS, Android, WebAssembly).

**Repository**: `https://github.com/AreteDriver/EVE_Rebellion`
**Asset Library**: `https://github.com/AreteDriver/EVE_Ships`

---

# VISION

EVE Rebellion is not a single game—it's a **platform** with multiple campaigns exploring different eras and factions of the EVE universe. All chapters share core mechanics, visual language, and progression systems.

**Core Design Philosophy**:
- Devil Blade Reboot-inspired gameplay: methodical pacing, point-blank scoring, proximity-based risk/reward
- Controller-first input with formation switching (spread ↔ focused)
- Heat system that rewards aggression but punishes recklessness
- Berserk System: proximity kills = higher score multipliers
- Config-driven architecture: chapters are JSON, not code

---

# ARCHITECTURE

## Tech Stack (Rust Migration)

```
eve_rebellion/
├── Cargo.toml                      # Workspace configuration
├── crates/
│   ├── eve_core/                   # Shared game systems
│   │   ├── src/
│   │   │   ├── lib.rs
│   │   │   ├── heat.rs             # Heat/Berserk system
│   │   │   ├── scoring.rs          # Combo multipliers, point-blank bonuses
│   │   │   ├── weapons.rs          # Projectile systems
│   │   │   ├── ship.rs             # Ship stats, factions
│   │   │   ├── enemy_ai.rs         # 6 AI behaviors
│   │   │   ├── wave_patterns.rs    # 6 wave formations
│   │   │   └── audio.rs            # Procedural audio generation
│   │   └── Cargo.toml
│   │
│   ├── eve_render/                 # Rendering systems
│   │   ├── src/
│   │   │   ├── lib.rs
│   │   │   ├── sprites.rs          # Ship rendering, CCP asset loading
│   │   │   ├── particles.rs        # Particle effects
│   │   │   ├── parallax.rs         # Background layers
│   │   │   ├── hud.rs              # HUD elements
│   │   │   └── effects.rs          # Visual effects (explosions, trails)
│   │   └── Cargo.toml
│   │
│   ├── eve_chapters/               # Chapter-specific logic
│   │   ├── src/
│   │   │   ├── lib.rs
│   │   │   ├── minmatar_rebellion.rs
│   │   │   ├── the_last_stand.rs   # Caldari/Gallente
│   │   │   ├── abyssal_depths.rs   # Triglavian roguelike
│   │   │   ├── sansha_incursion.rs
│   │   │   └── elder_fleet.rs
│   │   └── Cargo.toml
│   │
│   └── eve_game/                   # Main game binary
│       ├── src/
│       │   ├── main.rs
│       │   ├── menu.rs             # Menu system
│       │   ├── faction_select.rs   # Empire/faction selection
│       │   ├── ship_select.rs      # Ship selection filtered by faction
│       │   ├── game_loop.rs        # Core game loop
│       │   └── save.rs             # Save/load system
│       └── Cargo.toml
│
├── assets/
│   ├── ships/                      # Cached CCP ship renders
│   ├── audio/                      # Procedural audio cache
│   ├── fonts/
│   └── ui/
│
└── config/
    ├── menu_system.json            # All menu flows
    ├── ship_roster.json            # All ships, all factions
    ├── weapons.json                # Weapon definitions
    ├── enemies.json                # Enemy definitions
    ├── chapters/
    │   ├── minmatar_rebellion.json
    │   ├── the_last_stand.json
    │   ├── abyssal_depths.json
    │   └── sansha_incursion.json
    └── factions/
        ├── caldari.json
        ├── gallente.json
        ├── minmatar.json
        ├── amarr.json
        └── triglavian.json
```

## Rust Dependencies

```toml
# Cargo.toml (workspace)
[workspace]
members = ["crates/*"]

[workspace.dependencies]
bevy = "0.12"                    # Game engine (or macroquad for simpler approach)
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
tokio = { version = "1.0", features = ["full"] }
reqwest = { version = "0.11", features = ["json"] }
image = "0.24"
rodio = "0.17"                   # Audio
gilrs = "0.10"                   # Controller input
```

---

# MENU FLOW ARCHITECTURE

## Main Flow

```
TITLE SCREEN
    ↓
CHAPTER SELECT
    ├── "Minmatar Rebellion"    → Empire Select → Tribe Select → Difficulty → Ship → Play
    ├── "The Last Stand"        → Faction Select (Caldari vs Gallente) → Difficulty → Ship → Play
    ├── "Abyssal Depths"        → Filament Select → Ship → Play
    ├── "Sansha Incursion"      → Difficulty → Ship → Play
    └── "Elder Fleet"           → Difficulty → Ship → Play
```

## Empire Selection (Minmatar Rebellion Rework)

The Minmatar Rebellion chapter now starts with **Empire Selection** before tribe selection. This determines which empire you fight FOR (as Minmatar) and which you fight AGAINST.

```json
{
    "empire_select": {
        "chapter": "minmatar_rebellion",
        "layout": "horizontal_scroll",
        "title": "THE REBELLION BURNS ACROSS NEW EDEN",
        "subtitle": "Choose your battleground",
        
        "empires": [
            {
                "id": "amarr_front",
                "name": "AMARR FRONT",
                "description": "Break the chains. Free our people from the Golden Fleet.",
                "enemy_faction": "amarr",
                "player_faction": "minmatar",
                "narrative": "The Amarr Empire has enslaved our people for centuries. Today, we take them back.",
                "color_primary": "#8B0000",
                "color_secondary": "#4A0000"
            },
            {
                "id": "caldari_front", 
                "name": "CALDARI FRONT",
                "description": "Mercenary contract. Corporate war for the highest bidder.",
                "enemy_faction": "caldari",
                "player_faction": "minmatar",
                "narrative": "The State pays well. Their corporate enemies pay better. War is profit.",
                "color_primary": "#1E3A5F",
                "color_secondary": "#0D1F33"
            },
            {
                "id": "gallente_front",
                "name": "GALLENTE FRONT", 
                "description": "Freedom fighters supporting Federation expansion.",
                "enemy_faction": "gallente",
                "player_faction": "minmatar",
                "narrative": "The Federation claims to love liberty. Let them prove it in blood.",
                "color_primary": "#2E5D2E",
                "color_secondary": "#1A3A1A"
            }
        ]
    }
}
```

After empire selection, the existing tribe selection (Sebiestor, Brutor, Vherokior, Krusual) remains unchanged.

## Faction Selection (The Last Stand)

Two flags side-by-side. Player chooses which side of the Caldari-Gallente conflict to experience.

```json
{
    "faction_select": {
        "chapter": "the_last_stand",
        "layout": "versus_split",
        "title": "CHOOSE YOUR SIDE",
        
        "factions": [
            {
                "id": "caldari",
                "name": "CALDARI STATE",
                "position": "left",
                "flag": "caldari_flag",
                "description": "Hold the line while your people escape. Earn the fall.",
                "narrative": "The evacuation fleet needs forty minutes. You are the only thing between them and the Gallente armada.",
                "ships_available": ["phoenix", "wyvern", "leviathan"],
                "default_ship": "leviathan",
                "enemy_faction": "gallente",
                "comm_style": "terse_professional"
            },
            {
                "id": "gallente",
                "name": "GALLENTE FEDERATION",
                "position": "right", 
                "flag": "gallente_flag",
                "description": "Stop the Caldari titan. Protect your homeworld.",
                "narrative": "A Caldari titan is on collision course with Gallente Prime. Millions will die if it reaches atmosphere.",
                "ships_available": ["moros", "thanatos", "erebus"],
                "default_ship": "erebus",
                "enemy_faction": "caldari",
                "comm_style": "passionate_righteous"
            }
        ]
    }
}
```

---

# SHIP LOADING SYNC

Ships load dynamically based on selected faction/empire. The ship roster is filtered by chapter and faction.

```rust
// src/ship_select.rs

pub struct ShipRoster {
    pub ships: HashMap<String, ShipDefinition>,
}

impl ShipRoster {
    pub fn filter_by_chapter_and_faction(
        &self,
        chapter: &str,
        player_faction: &str,
        enemy_faction: &str,
    ) -> FilteredRoster {
        let player_ships: Vec<_> = self.ships.values()
            .filter(|s| s.faction == player_faction)
            .filter(|s| s.available_in_chapter(chapter))
            .cloned()
            .collect();
            
        let enemy_ships: Vec<_> = self.ships.values()
            .filter(|s| s.faction == enemy_faction)
            .cloned()
            .collect();
            
        FilteredRoster { player_ships, enemy_ships }
    }
}
```

## Ship Type IDs (CCP Image Server)

```json
{
    "ships": {
        "minmatar": {
            "rifter": { "type_id": 587, "class": "frigate" },
            "wolf": { "type_id": 11396, "class": "assault_frigate" },
            "jaguar": { "type_id": 11196, "class": "assault_frigate" },
            "thrasher": { "type_id": 594, "class": "destroyer" },
            "stabber": { "type_id": 620, "class": "cruiser" },
            "tempest": { "type_id": 639, "class": "battleship" },
            "ragnarok": { "type_id": 24693, "class": "titan" }
        },
        "amarr": {
            "executioner": { "type_id": 589, "class": "frigate" },
            "punisher": { "type_id": 597, "class": "frigate" },
            "retribution": { "type_id": 11393, "class": "assault_frigate" },
            "omen": { "type_id": 628, "class": "cruiser" },
            "apocalypse": { "type_id": 642, "class": "battleship" },
            "archon": { "type_id": 23757, "class": "carrier" },
            "aeon": { "type_id": 23919, "class": "supercarrier" },
            "avatar": { "type_id": 11567, "class": "titan" }
        },
        "caldari": {
            "kestrel": { "type_id": 602, "class": "frigate" },
            "hawk": { "type_id": 11377, "class": "assault_frigate" },
            "corax": { "type_id": 16236, "class": "destroyer" },
            "caracal": { "type_id": 621, "class": "cruiser" },
            "phoenix": { "type_id": 19724, "class": "dreadnought" },
            "wyvern": { "type_id": 23915, "class": "supercarrier" },
            "leviathan": { "type_id": 3764, "class": "titan" }
        },
        "gallente": {
            "tristan": { "type_id": 598, "class": "frigate" },
            "enyo": { "type_id": 11373, "class": "assault_frigate" },
            "catalyst": { "type_id": 16238, "class": "destroyer" },
            "thorax": { "type_id": 622, "class": "cruiser" },
            "moros": { "type_id": 19722, "class": "dreadnought" },
            "thanatos": { "type_id": 23911, "class": "carrier" },
            "erebus": { "type_id": 3764, "class": "titan" }
        },
        "triglavian": {
            "damavik": { "type_id": 47269, "class": "frigate" },
            "kikimora": { "type_id": 49710, "class": "destroyer" },
            "vedmak": { "type_id": 47271, "class": "cruiser" },
            "drekavac": { "type_id": 49711, "class": "battlecruiser" },
            "zirnitra": { "type_id": 52907, "class": "dreadnought" }
        }
    }
}
```

Ship images loaded from: `https://images.evetech.net/types/{type_id}/render?size=512`

---

# CHAPTER SPECIFICATIONS

## 1. Minmatar Rebellion

**Emotional Target**: Liberation, defiance, growth
**Pilot Catchphrase Evolution**:
- Rifter: "In Rust We Trust!"
- Wolf: "No more rust - just steel!"
- Jaguar: "From rust to legend!"

**Core Mechanics**:
- 13-boss progression
- Refugee rescue (upgrade currency)
- Tribal bonuses based on selection
- Ship upgrades: Rifter → Wolf → Jaguar
- Berserk System (proximity kills = multiplier)
- Heat system (doubles multiplier when maxed)

**Tribal Bonuses**:
```json
{
    "tribes": [
        { "id": "sebiestor", "bonus": "+10% Shield Capacity", "voice_style": "analytical" },
        { "id": "brutor", "bonus": "+15% Weapon Damage", "voice_style": "fierce" },
        { "id": "vherokior", "bonus": "+20% Healing Received", "voice_style": "spiritual" },
        { "id": "krusual", "bonus": "+15% Score Multiplier", "voice_style": "cunning" }
    ]
}
```

**Enemy Wave Patterns** (6 types):
1. **Linear Rush** - Single file approach
2. **Sine Wave** - Oscillating entry
3. **Spiral** - Rotating formation
4. **Ambush** - Spawn from screen edges
5. **Pincer** - Two groups converging
6. **Screen Clear** - Full screen assault

**Enemy AI Behaviors** (6 types):
1. **Kamikaze** - Direct collision course
2. **Weaver** - Erratic movement
3. **Sniper** - Long range, stationary
4. **Spawner** - Creates additional enemies
5. **Tank** - High HP, slow
6. **Basic** - Standard attack patterns

---

## 2. The Last Stand (Caldari vs Gallente)

**Emotional Target**: Sacrifice, tragedy, earned death
**Core Narrative**: CNS Kairiola's final hours defending evacuation

**Caldari Side**:
- Play as Admiral Yakiya Tovil-Toba
- Defend evacuation fleet for 40 minutes
- Titan cannot move—weapons platform only
- Thermal collapse mechanic (ship dying regardless)
- Victory = 100% evacuation, then crash into Gallente Prime

**Gallente Side**:
- Stop the Caldari titan
- Prevent atmospheric entry
- Different emotional experience—you're the "villain"

**Titan Control Scheme** (No movement):
- **RT**: Fighter Launch (sustained fire, heat generation)
- **LB**: ECM Burst (screen clear, long cooldown, high heat)
- **RB**: Shield Booster (emergency repair, heat spike)
- **Y**: Doomsday Weapon (massive damage, near-fatal heat)

**Thermal Collapse System**:
- Heat rises constantly
- All actions generate heat
- Overheat = systems fail
- No way to cool permanently—only delay
- Ship dies when thermal threshold exceeded

**Evacuation Milestones**:
```json
{
    "milestones": [
        { "percent": 0, "comm": "Kairiola, all channels open. They're coming." },
        { "percent": 15, "comm": "First transports away. Gallente repositioning to you." },
        { "percent": 30, "comm": "They're committed. You have their attention." },
        { "percent": 50, "comm": "Halfway. We see your thermals, Admiral." },
        { "percent": 70, "comm": "Navigation locked. Coordinates confirmed." },
        { "percent": 85, "comm": "Last transports spinning up. Hold." },
        { "percent": 95, "comm": "Fleet away. Kairiola... the path is yours." }
    ]
}
```

---

## 3. Abyssal Depths (Triglavian Roguelike)

**Emotional Target**: Tension, greed vs survival, "one more room"
**Core Loop**: Enter filament → Clear 3 rooms → Extract before timer expires

**Filament Types** (Environment modifiers):
| Filament | Effect |
|----------|--------|
| Exotic | Balanced, no modifiers |
| Firestorm | +50% Armor, -50% Shield, +Thermal damage |
| Electrical | +50% Shield, -50% Armor, +EM damage |
| Dark Matter | -30% Signature, -50% Range, +Kinetic |
| Gamma | +50% Shield Boost, -30% Explosive Resist |

**Tier System** (Difficulty scaling):
| Tier | Timer | Enemy Scaling | Loot Mult |
|------|-------|---------------|-----------|
| T1 Calm | 20:00 | 1.0× | 1.0× |
| T2 Agitated | 18:00 | 1.3× | 1.5× |
| T3 Fierce | 15:00 | 1.6× | 2.0× |
| T4 Raging | 12:00 | 2.0× | 3.0× |
| T5 Chaotic | 10:00 | 2.5× | 4.5× |
| T6 Cataclysmic | 8:00 | 3.0× | 7.0× |

**Abyssal Enemy Factions**:

1. **Triglavian Collective**
   - Damavik swarms (light, ramping damage)
   - Vedmak cruisers (heavy, spooling weapons)
   - Drekavak battlecruisers (boss tier)
   - **Unique**: Disintegrators ramp damage over time on target

2. **Rogue Drones**
   - Tessera (light)
   - Phorus (medium, spawner)
   - Tyrannos (heavy)

3. **Sleepers**
   - Circadian Seeker (light, fast)
   - Sleeper Sentinel (medium)
   - Sleeper Warden (heavy, EWAR)

4. **Drifters** (T5-6 only)
   - Drifter Battleship (boss)
   - Doomsday weapon (visible charge, must interrupt)

**Room Progression**:
```
ROOM 1 "Pockets" → ROOM 2 "Escalation" → ROOM 3 "Extraction"
   Light enemies      Medium + hazards       Boss + extract gate
```

**Environmental Hazards**:
- Deviant Automata (AoE damage pulse)
- Ephialtes Cloud (tracking disruption)
- Tachyon Cloud (speed reduction)
- Triglavian Pylon (buffs enemies)

---

## 4. Sansha Incursion

**Emotional Target**: Dread, holding until rescue arrives
**Core Mechanic**: Wave defense against zombie fleet

**Unique Elements**:
- True Slaves (mind-controlled pilots) behave erratically
- CONCORD backup arrives... eventually
- Boss: Sansha Supercarrier with fighter spam
- Incursion site types (Vanguard, Assault, HQ)

**Sansha Ships**:
- Centii (frigate swarm)
- Centum (cruiser)
- Centus (battleship)
- True Slave variants (erratic AI)
- Revenant (supercarrier boss)

---

## 5. Elder Fleet (Liberation Day)

**Emotional Target**: Hope, defiance, rescue
**Connection**: Direct sequel to Minmatar Rebellion

**Core Mechanic**:
- Escort transports
- Rescue slaves from Amarr space
- Refugee count matters (like evacuation %)
- Boss: Amarr Titan attempting to stop fleet

**Unlocks**: Elder Fleet skins for Minmatar ships

---

# SCORING SYSTEM

Based on Devil Blade Reboot:

```rust
pub struct ScoringSystem {
    pub combo_count: u32,
    pub combo_multiplier: f32,  // 1x to 5x
    pub heat_bonus: bool,       // 2x when heat maxed
    pub berserk_active: bool,   // Proximity kills boost
}

impl ScoringSystem {
    pub fn calculate_kill_score(&self, base_points: u32, distance: f32) -> u32 {
        let distance_bonus = if distance < 50.0 { 3.0 }      // Point-blank
                            else if distance < 100.0 { 2.0 } // Close
                            else if distance < 200.0 { 1.5 } // Medium
                            else { 1.0 };                    // Far
        
        let heat_mult = if self.heat_bonus { 2.0 } else { 1.0 };
        let berserk_mult = if self.berserk_active { 1.5 } else { 1.0 };
        
        (base_points as f32 * self.combo_multiplier * distance_bonus * heat_mult * berserk_mult) as u32
    }
}
```

---

# AUDIO SYSTEM

Procedural audio generation (no external assets required):

```rust
pub struct AudioSystem {
    pub sample_rate: u32,      // 44100
    pub channels: u32,         // 2 (stereo)
}

impl AudioSystem {
    pub fn generate_laser(&self, frequency: f32, duration: f32) -> Vec<f32>;
    pub fn generate_explosion(&self, intensity: f32) -> Vec<f32>;
    pub fn generate_engine_hum(&self, throttle: f32) -> Vec<f32>;
    pub fn generate_shield_hit(&self) -> Vec<f32>;
    pub fn generate_alarm(&self, urgency: f32) -> Vec<f32>;
}
```

**Music Layers** (dynamic based on game state):
1. Bass pulse (heartbeat rhythm)
2. Synth pads (tension)
3. Lead melody (escalation)
4. Percussion (intensity)

---

# CROSS-PLATFORM DEPLOYMENT

## Build Targets

```bash
# Desktop
cargo build --release --target x86_64-unknown-linux-gnu     # Linux
cargo build --release --target x86_64-pc-windows-msvc       # Windows
cargo build --release --target x86_64-apple-darwin          # macOS

# Mobile
cargo build --release --target aarch64-linux-android        # Android
cargo build --release --target aarch64-apple-ios            # iOS

# Web
cargo build --release --target wasm32-unknown-unknown       # WebAssembly
```

## Mobile Touch Controls

```rust
pub enum TouchMode {
    Virtual Joystick,    // Left side: movement
    FireZone,           // Right side: auto-aim fire
    SwipeFormation,     // Two-finger: toggle spread/focused
    TapDoomsday,        // Three-finger: special weapon
}
```

---

# IMPLEMENTATION CHECKLIST

## Phase 1: Core Systems
- [ ] Rust project structure
- [ ] Bevy/macroquad setup
- [ ] Ship asset loader (CCP API)
- [ ] Basic rendering pipeline
- [ ] Input system (controller + touch)
- [ ] Heat system
- [ ] Scoring system
- [ ] Procedural audio

## Phase 2: Minmatar Rebellion
- [ ] Empire selection screen
- [ ] Tribe selection screen
- [ ] Ship selection (filtered by faction)
- [ ] 13-boss progression
- [ ] Wave patterns (6 types)
- [ ] Enemy AI (6 behaviors)
- [ ] Refugee rescue mechanic
- [ ] Ship upgrades

## Phase 3: The Last Stand
- [ ] Faction selection (Caldari vs Gallente)
- [ ] Titan control scheme
- [ ] Thermal collapse system
- [ ] Evacuation timer
- [ ] Milestone communications
- [ ] Endgame sequence

## Phase 4: Abyssal Depths
- [ ] Filament selection UI
- [ ] Tier system
- [ ] Room generation
- [ ] Room transitions
- [ ] Environmental hazards
- [ ] Triglavian enemies
- [ ] Disintegrator ramping damage
- [ ] Extraction mechanics
- [ ] Loot system

## Phase 5: Additional Chapters
- [ ] Sansha Incursion
- [ ] Elder Fleet
- [ ] Unlock system integration

## Phase 6: Polish & Deploy
- [ ] Parallax backgrounds
- [ ] Particle effects
- [ ] HUD polish
- [ ] Save/load system
- [ ] Cross-platform builds
- [ ] Performance optimization

---

# KEY REMINDERS

1. **Ships load based on faction selection** - Filter `ship_roster.json` by chapter + faction
2. **Empire selection precedes tribe selection** in Minmatar Rebellion
3. **The Last Stand has TWO playable sides** - Caldari AND Gallente perspectives
4. **Abyssal uses all faction ships** as selectable (frigate/destroyer/cruiser)
5. **Heat system is universal** - All chapters use the same heat mechanics
6. **Procedural audio** - No external sound files required
7. **CCP Image Server** - `https://images.evetech.net/types/{type_id}/render?size=512`
8. **Tribal elder thanks player after missions** with tribe-specific dialogue
9. **Devil Blade Reboot pacing** - Methodical, not chaotic; point-blank scoring rewards risk
10. **Controller-first design** - Formation toggle (spread ↔ focused) is core mechanic

---

# START HERE

```bash
# Clone repositories
git clone https://github.com/AreteDriver/EVE_Rebellion
git clone https://github.com/AreteDriver/EVE_Ships

# Create Rust project
cargo new eve_rebellion --name eve_game
cd eve_rebellion

# Add dependencies and begin implementation
```

Begin by implementing the core systems (heat, scoring, ship loading), then build Minmatar Rebellion first as the reference chapter. Other chapters layer on top of these shared systems.

---

*"In Rust We Trust!" → "No more rust - just steel!" → "From rust to legend!"*
