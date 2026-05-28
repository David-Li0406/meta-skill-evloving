# Bane Module

Create Banes (Wyrm-spirits) for W20 - from minor Gafflings to the terrifying Maeljin Incarna.

## Bane Basics

Banes are corrupted spirits serving the Wyrm. All Banes have:
- **Corruption** charm (always)
- Often **Possession** charm
- Feed on negative emotions/concepts
- Register as Wyrm-tainted to detection Gifts

## The Triatic Wyrm

The Wyrm has three aspects, and Banes may serve any:

| Aspect | Domain | Banes Serve Through |
|--------|--------|---------------------|
| **Beast-of-War** | Destruction, violence | Rage, pain, slaughter |
| **Eater-of-Souls** | Consumption, entropy | Addiction, hunger, decay |
| **Defiler** | Corruption, perversion | Pollution, madness, taint |

## Urge Wyrms

Twelve great spirits embodying primal corruptions. Banes often serve one:

| Urge Wyrm | Domain | Manifestation |
|-----------|--------|---------------|
| **Foebok** | Fear | Terror, paralysis |
| **Vorus** | Greed | Hoarding, theft |
| **Mahsstrac** | Power | Domination, tyranny |
| **Karnala** | Desire | Lust, obsession |
| **Abhorra** | Hatred | Bigotry, violence |
| **Angu** | Cruelty | Torture, sadism |
| **Ba'ashkai** | Violence | Murder, war |
| **Khaaloobh** | Consumption | Gluttony, addiction |
| **Pseulak** | Lies | Deception, betrayal |
| **Sykora** | Paranoia | Suspicion, isolation |
| **Gree** | Despair | Depression, suicide |
| **Lethargg** | Apathy | Sloth, entropy |

## Maeljin Incarna (Dark Lords)

The most powerful Banes - once-human entities who transcended to become Incarna serving the Urge Wyrms. Each rules a duchy in Malfeas.

### The Nine Maeljin

| Maeljin | Serves | Domain | Destruction Method |
|---------|--------|--------|-------------------|
| **Aliara** | Karnala (Desire) | Seduction, obsession | Must be killed by someone she desires |
| **Lord Steel** | Abhorra (Hatred) | Rage, genocide | Remove mask, imprison in mirrored room for lunar month |
| **Lady Aife** | Angu (Cruelty) | Torture, suffering | Only Nameless Angel, Pattern Spiders, or pain-indifferent entities can slay her |
| **Hellbringer** | Ba'ashkai (Violence) | War, slaughter | Must stab self with own crossbow bolt away from battle |
| **Knight Entropy** | Khaaloobh (Consumption) | Decay, addiction | Exposure to pure Wyld energies |
| **Maine duBois** | Pseulak (Lies) | Deception, contracts | Sign contract requiring forfeit if failed, with no profit to anyone |
| **Doge Klypse** | Sykora (Paranoia) | Suspicion, isolation | Find brass box containing memory of last person he trusted |
| **Nameless Angel** | Gree (Despair) | Depression, suicide | Concolation ritual (lost to time) |
| **Thurifuge** | Lethargg (Apathy/Disease) | Plague, entropy | Drown in purest healing spring |

### Elemental Maeljin

Four Maeljin embody corrupted elements:

| Maeljin | Element | Destruction Method |
|---------|---------|-------------------|
| **Lord Choke** | Smog/Air | Four greatest air elementals working together |
| **Lord Kerne** | Balefire/Fire | Freeze solid, encase in lead |
| **Lord Collum** | Sludge/Water | Plant five rare purifying plant seeds in body |
| **Lady Yul** | Toxin/Earth | Ingest Moly herb from Pangaea |

## Common Bane Breeds

| Breed | Feeds On | Typical Rank |
|-------|----------|--------------|
| Bitter Rages | Rage, anger | Jaggling |
| Psychomachiae | Psychological flaws | Jaggling |
| Scrags | Pain, violence | Gaffling-Jaggling |
| Hoglings | Gluttony, excess | Gaffling |
| Drattosi | Despair, apathy | Gaffling |
| Nexus Crawlers | Blighted places | Incarna |
| Kalus | Cold, isolation | Jaggling |
| Mara | Nightmares | Jaggling |
| Furmlings | Rage/shame | Gaffling |
| Wakshaani | Addiction | Jaggling |
| H'rugglings | Violence | Gaffling |
| Nihilachs | Entropy | Jaggling-Incarna |
| Nocturnae | Fear of dark | Gaffling |
| Harpies | Spite, jealousy | Jaggling |
| Abliphets | Memories | Jaggling |

## Creation Steps

1. **Concept**: Define the negative emotion/concept it embodies
2. **Rank**: Gaffling (minor), Jaggling (moderate), Incarna (major)
3. **Allegiance**: Which Urge Wyrm or Triatic aspect?
4. **Statistics**: Assign Rage, Gnosis, Willpower, Essence by rank
5. **Charms**: All have Corruption; add others appropriate to concept
6. **Appearance**: Describe horrific/seductive form
7. **Behavior**: How does it hunt/feed/corrupt?
8. **Weakness**: What harms or banishes it?

## Stat Ranges by Rank

| Rank | Rage | Gnosis | Willpower | Essence |
|------|------|--------|-----------|---------|
| Gaffling | 2-4 | 2-4 | 2-4 | 5-15 |
| Jaggling | 5-7 | 5-7 | 5-7 | 20-40 |
| Incarna | 8-10 | 8-10 | 8-10 | 50-100+ |
| Maeljin | 10+ | 10+ | 10+ | 200+ |

## Output Format

```markdown
# [Bane Name]

**Rank**: [Gaffling/Jaggling/Incarna]
**Serves**: [Urge Wyrm or Triatic Aspect]
**Feeds On**: [Emotion/concept]

## Statistics
| Trait | Rating |
|-------|--------|
| Rage | [X] |
| Gnosis | [X] |
| Willpower | [X] |
| Essence | [X] |

## Charms
- **Corruption**: [How it corrupts]
- [Other charms as appropriate]

## Image
[Horrific or deceptively beautiful appearance]

## Behavior
[How it hunts/feeds/corrupts]

## Weakness
[What can harm or banish it]
```

## Reference Files

- `lookup.py spirit.bane-breeds bane-breeds` - Common Bane types
- `lookup.py spirit.maeljin-incarna maeljin-incarna` - Dark Lords with full stats
- `lookup.py spirit.urge-wyrms urge-wyrms` - The twelve Urge Wyrms
- `lookup.py spirit.elemental-maeljin elemental-maeljin` - Elemental Dark Lords
