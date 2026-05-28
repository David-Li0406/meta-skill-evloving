# Kinfolk Module

Create Kinfolk characters (human or wolf relatives of Garou) using W20 Kinfolk: A Breed Apart.

## Quick Reference: Kinfolk vs Garou

| Aspect | Kinfolk | Garou |
|--------|---------|-------|
| Attributes | 6/4/3 | 7/5/3 |
| Abilities | 11/7/4 (no cap) | 13/9/5 (cap 3) |
| Backgrounds | 5 | 5 |
| Freebies | 21 | 15 |
| Willpower | 3 | By tribe |
| Rage/Gnosis | No (see Gnosis Merit) | Yes |
| Delirium | Immune | Cause it |
| Gifts | Via roleplay only (max 1-3) | At creation |

## Dependencies

| Feature | Reference |
|---------|-----------|
| Abilities | `lookup.py kinfolk.abilities abilities` |
| Backgrounds | `lookup.py kinfolk.backgrounds backgrounds` |
| Merits/Flaws | `lookup.py kinfolk.merits-flaws merits-flaws` |
| Gifts | `lookup.py kinfolk.gifts gifts` |
| Rites | `lookup.py kinfolk.rites rites` |
| Fetishes/Talens | `lookup.py kinfolk.fetishes-talens fetishes-talens` |
| Numina | `lookup.py kinfolk.numina numina` |
| Kin-Fetches | `lookup.py kinfolk.kin-fetches kin-fetches` |
| Organizations | `lookup.py kinfolk.organizations organizations` |
| Antagonists | `lookup.py kinfolk.skin-dancers skin-dancers` |

---

## Creation Steps

1. **Concept** — Name, tribe affiliation, kenning/callow status
2. **Breed** — Human (typical) or Wolf (rare, limited play)
3. **Relation Type** — Role in Garou society:
   - Protector, Provider, Spy, Support, Warrior
4. **Attributes** — 6/4/3 (+ 9 base = 1 in each)
5. **Abilities** — 11/7/4 (Talents/Skills/Knowledges, no cap)
   - New options: Intuition (Talent); Bureaucracy, Herbalism, Veterinary Medicine, Rituals (Knowledges)
6. **Backgrounds** — 5 dots
   - Standard: Allies, Contacts, Mentor, Pure Breed, Resources
   - Kinfolk-specific: Equipment, Garou Favor, Renown, Rites
   - **Restricted**: No Ancestors, Past Life, Totem, Fetish (Background)
7. **Willpower** — 3
8. **Merits & Flaws** — Optional (up to 7 pts Flaws)
9. **Gnosis Merit** — Optional (5/6/7 pts for 1/2/3 dots)
10. **Numina** — Optional (7 pts per dot first type, 14 pts second)
11. **Freebies** — 21 + Flaws - Merits. Spend exactly.
12. **Description** — Appearance, history, relation to Garou family

---

## Freebie Costs

| Trait | Cost |
|-------|------|
| Attribute | 5 |
| Ability | 2 |
| Background | 1 |
| Willpower | 1 |
| Gnosis (Merit required) | 2 |
| Numina (1st type) | 7/dot |
| Numina (2nd type) | 14/dot |

---

## Gnosis Merit

Allows Kinfolk to possess Gnosis and use Gnosis-requiring Gifts, fetishes, and talens.

| Dots | Cost |
|------|------|
| 1 | 5 pts |
| 2 | 6 pts |
| 3 | 7 pts |

**Note**: Even with Gnosis, Kinfolk cannot learn Gifts requiring Rage.

---

## Kinfolk Gifts

**Acquisition**: Through roleplay + experience points only. Cannot purchase at creation.
**Limit**: Most have 1 Gift; max 2-3 under exceptional circumstances.
**Level Cap**: Level 1 only.

| Cost | Type |
|------|------|
| 15 XP | Breed or tribe Gift |
| +5 XP | Outside breed/tribe |
| +5 XP | Taught by Garou (not spirit) |

**Without Gnosis**: Can only learn Gifts not requiring Gnosis expenditure.
**Teaching**: Usually requires Theurge to summon spirit teacher. Kinfolk negotiates directly with spirit.

---

## Kinfolk Rites

| Type | Roll | Diff |
|------|------|------|
| Accord | Cha + Rituals | 7 |
| Milestones | Cha + Rituals | 7 |
| Homestead | Varies | 7 |
| Punishment | Cha + Rituals | 7 |
| Renown | Cha + Rituals | 6 |
| Seasonal | Sta + Rituals | Varies |
| Minor | None | None |

**Key Rites**: Rite of Apology, Rite of Exile, Rite of Intervention, Rite of the Morning Song (grants Sense Wyrm after 9 days), Rite of Evening Chant (+1 Social die with matching auspice Garou).

---

## Numina

Three categories of mortal supernatural abilities:

| Type | Description |
|------|-------------|
| **Hedge Magic** | Folk wizardry: Conjuration, Divination, Healing, Herbalism/Brewing, Spirit Chasing |
| **Psychic** | Mental powers: Empathic Healing, Soulstealing |
| **True Faith** | Spiritual devotion (1-10 rating). Adds to Willpower rolls; may repel vampires/wraiths/Wyrm |

**Cost**: 7 freebie/dot (first Numen), 14/dot (second). XP cost = current rating × 7.
**Rarity**: Having more than one type is extremely rare.

---

## Equipment Options

With Equipment Background, Kinfolk may start with:
- Silver bullets, healing herbs, gas masks (1-2 dots)
- Wiretaps, surgical kits, white noise generators, talens with Gnosis Merit (3-4 dots)
- Unique items, powerful talens (5 dots)

---

## Tribal Kinfolk Notes

| Tribe | Kinfolk Character |
|-------|-------------------|
| Black Furies | Primarily female; strong women traditions |
| Bone Gnawers | Diverse urban survivors; resourceful |
| Children of Gaia | All walks of life; have counselors for transitions |
| Fianna | Celtic heritage; music, storytelling, revelry |
| Get of Fenris | Northern European; martial training expected |
| Glass Walkers | Urban professionals; corporate/tech integration |
| Red Talons | Almost entirely wolf Kin; human Kin extremely rare |
| Shadow Lords | Eastern European; political savvy encouraged |
| Silent Striders | Wandering, nomadic; spread globally |
| Silver Fangs | Aristocratic noble bloodlines; Pure Breed emphasis |
| Stargazers | Asian/philosophical; meditation and balance |
| Uktena | Indigenous peoples; ancient traditions and lore |
| Wendigo | Native American (northern); strong cultural identity |

---

## Kin-Fetches

Spirit guardians bound to Kinfolk at birth. Alert tribe when Kin undergoes First Change.
- **Kin-Fetch** (Gaffling): Basic guardian spirit
- **Blood Fetch** (Jaggling): Attached to old, prosperous families with high Pure Breed
- **Fetch Spider**: Glass Walker variant disguised as Weaver-spirit
- **Fetch-Hawk**: Black Spiral Dancer Bane that parasitizes Kin-Fetches

**Merits/Flaws**: Alert Kin-Fetch (2 pt Merit), Malingering Kin-Fetch (3 pt Flaw)

---

## Output Format

```markdown
# [Character Name]

**Breed**: [Human/Wolf]
**Tribe Affiliation**: [Tribe]
**Relation**: [Role type]
**Status**: [Kenning/Callow]

## Attributes
[Standard format - Physical/Social/Mental]

## Abilities
[Standard format - Talents/Skills/Knowledges]

## Backgrounds
[5 dots with descriptions]

## Pools
- Willpower: 3
- Gnosis: [If Merit purchased]

## Merits & Flaws
[If any]

## Numina
[If any - specify type and level]

## Equipment
[If Equipment Background]

## Role
[How they serve their Garou family]

## Description
[Appearance, personality, history, relationship to Garou kin]
```

---

## Validation

- [ ] Attributes: 13 dots (+ 9 base)
- [ ] Abilities: 22 dots total (11/7/4)
- [ ] Backgrounds: 5 dots (no Ancestors, Past Life, Totem, Fetish)
- [ ] Willpower: 3
- [ ] Freebies spent exactly
- [ ] Gnosis only with Merit
- [ ] No Gifts at creation
- [ ] Numina costs correct (7 or 14 per dot)
