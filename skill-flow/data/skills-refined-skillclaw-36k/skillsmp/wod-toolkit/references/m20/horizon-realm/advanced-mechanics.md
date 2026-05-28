# Advanced Mechanics

## Quintessence Accounting

### Sources for Realm Maintenance

| Source | Q/mo Provided |
|--------|---------------|
| **Node Background** | 1 per dot |
| **Quintessence Wellspring** | As purchased (10 pts = 1 Q/mo, max = Rank) |
| **Personal Stores** | Mages pool personal Q |
| **Tass Harvesting** | Convert physical Q |
| **Anchor to Node** | Node rating directly to maintenance |

### Key Distinctions

- **Horizon Realm Background** provides ACCESS, NOT Quintessence
- **Node Background** is primary maintenance source
- **Wellspring** makes Realm partially/fully self-sustaining

### Example

Rank 4 Realm (4 Q/mo maintenance):
- Node 3: provides 3 Q/mo
- Wellspring 1: generates 1 Q/mo (cost 10 build pts)
- Total: 4 Q/mo covers maintenance ✓

## Node Within Realm

A Node can exist INSIDE a Horizon Realm, separate from the Realm itself.

**Mechanics:**
- Node is distinct from Quintessence Wellspring
- Has own rating, Resonance, Reality Zone
- Create separately using **node-creator**
- Node's Q CAN be used for Realm maintenance
- Follows all normal Node rules

**Build Points:** Node inside Realm doesn't cost Realm build points—it's a separate Background purchase.

**Anchor to Node Merit:** If taking this, Node must exist and be specified. Node rating = Q/mo directly to maintenance. If Node destroyed, Realm becomes unstable.

## Background vs Rank

**Horizon Realm Background**: Measures ACCESS and ownership
- Rating 1-5: Access only (visit, use facilities)
- Rating 6-10: Ownership (access + 5, can modify, control)
- **Costs double normal Background points**

**Realm Rank**: Measures POWER and size
- Rank 1-10: Determines build points and base maintenance
- Independent of Background rating

**Examples:**
- Background 2 (4 bg pts) = Access to ANY Rank Realm, even Rank 10
- Background 7 (14 bg pts) = Ownership of Realm up to Rank 7
- Character with Background 3 has access to chantry's Rank 8 Realm
- Character with Background 9 owns Rank 4 Realm (chose smaller)

## Merit/Flaw Stacking

### General Rule
Merits and Flaws stack unless specifically incompatible.

### Quintessence Efficient Stacking
Can be purchased multiple times. Each halves (round down) CURRENT maintenance.

| Application | Rank 5 Example |
|-------------|----------------|
| Base | 5 Q/mo |
| First | 2 Q/mo |
| Second | 1 Q/mo |
| Third | 0 Q/mo |

### Quintessence Efficient + Bleeding Out

**Order of Operations:** Apply Bleeding Out first, THEN Quintessence Efficient.

Example: Rank 5 with both:
- Base: 5 Q/mo
- After Bleeding Out (×2): 10 Q/mo
- After Quintessence Efficient (÷2): 5 Q/mo (net zero effect)

### Incompatible Combinations

| Combination | Reason |
|-------------|--------|
| Bountiful + Environment 1 | Environment 1 is barren (unless specifically lush) |
| Inaccessible + Access Points | Inaccessible removes free access point |
| Has Subrealm + Rank ≤ 2 | Subrealm must be lower rank, need 3+ |
| Subrealm (Flaw) + Rank ≥ 8 | Larger Realm must be higher rank, none above 10 |

## Mobile Realm Mechanics

### Movement (with Mobile Merit, 5 pts)

**Within Same Umbral Region** (High/Middle/Low/Deep):
- Pilot roll: Intelligence + Cosmology, difficulty 8
- Success: Move up to Size rating in "zones" per day
- With Genius Locus: Self-directs, automatic success

**Between Umbral Regions:**
- Pilot roll: Intelligence + Cosmology, difficulty 9
- Requires Arete roll (difficulty 7) to navigate boundaries
- Failure: Stuck at boundary 1d10 days
- With Genius Locus: Self-directs but still needs 1d10 days transit

### Speed by Size

| Size | Zones/Day |
|------|-----------|
| 1 | 1 (very slow) |
| 4 | 4 (modest) |
| 6 | 6 (fast) |

### Restrictions
- Cannot move during rituals or major magical workings
- Access Points remain at original locations unless Realm returns
- Inhabitants feel unsettling sensation during movement

### Genius Locus Self-Direction
- Realm decides where to go based on intelligence
- Owner can negotiate but not command (unless pact)
- Rebellion possible if Realm disagrees

## Genius Locus Capabilities

### Building the Intelligence

| Component | Cost |
|-----------|------|
| Genius Locus Merit | 5 pts (base) |
| Attributes | 3 pts each (start at 0) |
| Abilities | 1 pt each (start at 0) |

Cannot make rolls at 0.

**Typical Investment:**
- Basic: 10-20 build pts
- Moderate: 20-30 build pts
- Highly intelligent: 30-50 build pts

### Communication Methods
- Environmental changes (weather, temperature, sounds)
- Dreams and visions
- Speaking through inhabitants or guardians
- Direct mental contact (if Mind affinity)
- Perception + Awareness to notice events within itself

### Magical Capability

**Genius Locus does NOT have:**
- Avatar (by default)
- Sphere magic (unless bound with Awakened spirit)
- Arete

**Genius Locus CAN:**
- Control Special Phenomena (on/off)
- Reshape environment (if Morphic Merit)
- Direct Guardians
- Seal/open Access Points
- Perceive threats
- Communicate needs
- Form relationships with inhabitants

### Personality and Agency
- Has goals, desires, fears based on origin
- May cooperate, resist, or pursue own agenda
- Can refuse movement (if Mobile)
- Can close Access Points
- Can become antagonist if corrupted

### Example Intelligent Realm

```
Genius Locus base: 5 pts
Intelligence 3: 9 pts
Wits 2: 6 pts
Perception 4: 12 pts
Awareness 3: 3 pts
Cosmology 2: 2 pts
Enigmas 3: 3 pts
Total: 40 build pts

Result: Can perceive threats, communicate needs, understand 
Umbral geography. Cannot cast magic but extremely aware.
```

## Maintenance Failure Consequences

If maintenance not paid:

| Duration | Effect |
|----------|--------|
| 1 month | Realm becomes unstable (random effects) |
| 2-3 months | Size decreases by 1 |
| 4-6 months | Environment degrades one level |
| 6+ months | Realm begins collapsing (Dying Flaw effects) |

With Dying Flaw, these effects occur at triple speed.

## Realm Stability Ratings

| Stability | Description |
|-----------|-------------|
| **Solid** | Normal operation, no issues |
| **Mutable** | Minor shifts, occasional anomalies |
| **Unstable** | Significant reality fluctuations |
| **Collapsing** | Active degradation, requires intervention |

Anchor to Node loss → Mutable for 1 year
Maintenance failure → Progresses through stages
Paradox Scarred → Permanently Unstable unless healed
