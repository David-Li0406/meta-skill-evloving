# Narrative Ghost Hunting Module

Source: **Paranormal Investigator's Handbook**

Alternative rules for running structured ghost hunts. Use instead of normal investigation rolls.

---

## Overview

1. **Team selects Lead Investigator** who makes final decisions on actions
2. **Goal**: Determine nature of ghost before accruing 5 Malice points
3. **Success**: Identify ghost type → Choose Finale action
4. **Failure**: Reach 5 Malice → Catastrophic result

---

## Investigation Actions

| Action | Description | Malice if Negative |
|--------|-------------|-------------------|
| **Spirit Box** | Ask questions via spirit box. Tone matters. | 1 |
| **EMF** | Detect electromagnetic energy | 1 |
| **Motion Sensors** | Detect unseen presence | 1 |
| **Thermal Cameras** | Detect cold spots/heat blooms | 1 |
| **Cleansing** | Use incense to calm spirit | 2 |
| **Confront** | Present information about ghost's life/death | 2 |
| **Force Manifestation** | Cajole or force ghost to appear | 3 |
| **Seek Fetter** | Determine what holds ghost to place | 3 |
| **Research** | Uncover details (for Confront action) | 0 |
| **Passive Action** | Repair equipment, recover from mishap | 0 |

---

## Ghost Types

### The Passive
**Description**: Not angry or sorrowful. Cause disturbances by accident.

| Positive Actions | Negative Actions | Clues |
|------------------|------------------|-------|
| Cleansing, EMF, Thermal, Spirit Box, Seek Fetter | Manifestation, Confront | Neutral aura, random disturbances, cold spots |

### The Mourner
**Description**: Gripped by deep sorrow. Lingers near death site.

| Positive Actions | Negative Actions | Clues |
|------------------|------------------|-------|
| Cleansing, Thermal, EMF, Seek Fetter | Manifestation, Confront, Spirit Box | Sorrow, cold spots, distant murmurs |

### The Grim
**Description**: Ghost hounds protecting sacred ground.

| Positive Actions | Negative Actions | Clues |
|------------------|------------------|-------|
| Showing deference to territory | Destruction, aggression, trespass, Spirit Box, Manifestation, Confront | Hounds baying, feeling watched |

### Harlequins
**Description**: Manipulative, charismatic wraiths.

| Positive Actions | Negative Actions | Clues |
|------------------|------------------|-------|
| Questions, Spirit Box, Manifestation, Seek Fetter (will lie!) | Confront, refusing possession, cleansing | Charming, pleasant aura |

### Nightriders
**Description**: Nightmare-inducing wraiths.

| Positive Actions | Negative Actions | Clues |
|------------------|------------------|-------|
| Cleansing, Thermal, EMF, Confront | Manifestation, Spirit Box, Seek Fetter | Distant screams, chill, TV static |

### Poltergeists
**Description**: Indistinct masses of anger and frustration.

| Positive Actions | Negative Actions | Clues |
|------------------|------------------|-------|
| Motion Sensors, EMF, Thermal | Manifestation, Spirit Box, Cleansing, Confront, Seek Fetter | Anger, objects moved/thrown |

---

## Setbacks (Negative Results)

| Setback | Effect |
|---------|--------|
| **Equipment Malfunction** | Device breaks, battery dies, card full. Passive action to restore. |
| **Prank** | Ghost hinders progress through trickery. |
| **False Clue** | Ghost lies about their nature. May lead to wrong actions. |
| **Ectoplasm** | Disgusting residue on gear. Passive action to clean. |
| **Changing Nature** | Mood shift. One action switches from positive to negative or vice versa. |
| **Pitfall** | Terrain used against investigators. Passive action to clear. |

---

## Malice Levels

| Level | Description |
|-------|-------------|
| **1** | Slightly disturbed. General unease, slight temperature dip. |
| **2** | More agitated. Breath visible, mild static, small objects move. |
| **3** | First anger. Lights flicker, frost on surfaces, larger objects rattle. |
| **4** | Lights out. Glass shatters. Large furniture moves. Wind in enclosed space. |
| **5** | **END**. Rage. Walls weep blood, audible wails, equipment fails, ghost manifests and attacks. |

---

## Finale Actions

Choose when ghost type is determined (before reaching 5 Malice):

| Action | Description | Best For |
|--------|-------------|----------|
| **Find Peace** | Help ghost pass on quietly | Non-malevolent spirits |
| **Exorcism** | Forcefully separate ghost from tether | Trickster/malevolent spirits |
| **Seal** | Trap spirit in place or object | Too powerful to exorcise |
| **Destroy Fetter** | Destroy binding object (causes ghost trauma) | Malicious spirits |

**Wrong Action**: If Storyteller believes chosen action wouldn't work, Malice +1 and choose again. If this brings Malice to 5, investigation ends in failure.

---

## Catastrophic Results (Malice 5)

| Result | Effect |
|--------|--------|
| **Cursed** | One investigator gains Hanger-on-like curse. Buy off with XP. |
| **Injury** | 3 bashing damage. Injured, cannot hunt until medical attention. |
| **Broken Gear** | Most important/expensive item destroyed beyond repair. |
| **Brink of Death** | *Malice 6+ only*. Near-fatal injury. Give chances to save. |
| **Possession** | Most susceptible character possessed. Willpower roll (Diff 6) each scene to break free. Storyteller provides ghost's goal. |

---

## Try, Try Again

Failure doesn't mean end of story. Can approach again through:
- Normal rules of play
- Second Narrative Hunt attempt

**If returning too soon**: Ghost still agitated. Start Malice at 2+. May receive false clues or have actions switched.

**After catastrophe**: Resolve results (especially possession) before trying again. Failure can seed new stories.

---

## Data Lookup

```bash
python scripts/lookup.py wr20.mortals narrative-ghost-hunting
python scripts/lookup.py wr20.mortals creatures
```
