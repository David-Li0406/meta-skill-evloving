# Totem Module

Create pack totems for W20.

## References
- `lookup.py totem.totems totems` — All totems by type
- `lookup.py totem.totem-creation-guide totem-creation-guide` — **Creation rules and power scaling**

## Totem Types

| Type | Focus | Typical Renown | Typical Abilities |
|------|-------|----------------|-------------------|
| Respect | Leadership, nobility | Honor | Leadership, Empathy, Medicine |
| War | Combat, strength | Glory | Brawl, Melee, Intimidation |
| Wisdom | Knowledge, mysticism | Wisdom | Enigmas, Occult, Stealth |
| Cunning | Trickery, survival | Mixed | Stealth, Subterfuge, Survival |

---

## Individual Traits (All Pack Members)

Individual Traits are benefits that **every pack member** receives simultaneously. They should be thematically linked to the totem spirit and scaled appropriately to the Background Cost.

### What Individual Traits Can Include

| Trait Type | Examples | Notes |
|------------|----------|-------|
| Attributes | +1 Stamina, +2 Perception | Modest bonuses; see Combat Caution below |
| Abilities | +2 Survival, +1 Stealth | Thematically appropriate to totem |
| Unique Abilities | Perfect direction sense, immunity to a specific effect | Situational or narrow in scope |
| Difficulty Modifiers | -1 difficulty to tracking rolls, -2 difficulty to resist fear | Applied to specific rolls/powers |
| **Permanent Renown** | +2 Glory, +1 Honor, +3 Wisdom | **Key benefit—see below** |

### Permanent Renown: The Hidden Power

Permanent Renown is one of the most valuable Individual Traits. In W20, climbing Rank is a long, difficult process:
1. Earn Temporary Renown through deeds
2. Qualify Temporary Renown into Permanent Renown (often requiring Rites, challenges, or ST approval)
3. Accumulate enough Permanent Renown across categories to advance in Rank

**Receiving Permanent Renown from a Totem is a vast boon**—it represents the spirits themselves recognizing the pack's worth, accelerating their path to higher Rank.

### Combat Trait Caution

When designing Individual Traits that enhance combat (Strength, Brawl, Melee, Firearms, damage bonuses, etc.), remember that **Garou already possess a substantial combat advantage**:

- Crinos form grants **+4 Strength**, **+1 Dexterity**, **+3 Stamina**
- Hispo grants **+3 Strength**, **+2 Stamina**
- Garou have Rage for extra actions, regeneration, and natural weapons

This doesn't mean War totems can't grant combat bonuses—they absolutely can and should. But those bonuses should be **considered carefully** and kept proportionate. A +1 to Brawl is meaningful; a +3 to Strength on top of Crinos might unbalance the game.

**Good combat Individual Traits**: +1-2 to an Ability, difficulty modifiers for specific combat situations, bonuses that apply in narrow circumstances (vs. Wyrm creatures, when defending packmates, etc.)

---

## Pack Traits (Shared Pool, One at a Time)

Pack Traits are **more powerful** than Individual Traits, but they come with a key limitation: **only one pack member can benefit at a time**, and usage is typically capped per story or session.

### What Pack Traits Can Include

| Trait Type | Examples | Notes |
|------------|----------|-------|
| **Willpower Pool** | 3-5 Willpower per story | Most common Pack Trait; represents totem "pushing" for the pack |
| Attributes | +3 Strength, +2 Wits | Higher than Individual; one member at a time |
| Abilities | +4 Brawl, +3 Intimidation | Can exceed normal caps; one member at a time |
| Gifts | Access to a specific Gift | Often a Level 1-2 Gift usable by any pack member |
| Unique Powers | Berserker without frenzy, perfect tracking | Signature abilities that define the totem |
| Spirit Interaction | Respected by spirits of X type, can communicate with Y | Social/Umbral benefits |

### Pack Willpower: The Totem's Influence

A common and impactful Pack Trait is a pool of Willpower points (typically 3-5 per story). This represents the **totem spirit pushing its influence** in a pack member's favor during high-stakes moments.

Mechanically, this Willpower can be spent like personal Willpower (automatic successes, activating certain powers, resisting effects). The key difference:
- It's a **shared pool**—once spent, it's gone for everyone until the next story
- It represents the **totem's direct intervention**, which should feel significant in narrative

### Usage Caps and Limitations

To prevent abuse, Pack Traits often include limitations:
- **Per story**: "The pack shares 4 Willpower per story"
- **Per scene**: "One pack member may add +3 Brawl per scene"
- **Per use**: "Once per story, a pack member may use the Gift: Sense Wyrm"
- **Circumstantial**: "Only when defending the caern" or "Only against Wyrm-tainted foes"

The more powerful the Pack Trait, the stricter the limitation should be.

---

## Power by Cost

| Cost | Label | Individual Traits | Pack Traits | Ban Severity |
|------|-------|-------------------|-------------|--------------|
| 4 | Minor | 2 pts Renown + minor bonus | 2-3 WP, modest ability | Moderate |
| 5 | Standard | 2-3 pts Renown + ability bonus | 3-5 WP, notable power | Significant |
| 6 | Powerful | 3 pts Renown + strong bonus | 3-4 WP, impressive power | Demanding |
| 7 | Mighty | 3-4 pts Renown + multiple bonuses | 4+ WP, unique power | Strict |
| 8+ | Legendary | 4-5 pts Renown + exceptional | Multiple strong powers | Extreme |

---

## Additional Point Costs

Pack members can pool extra Background dots beyond the base cost to enhance their totem:

| Enhancement | Cost |
|-------------|------|
| +1 Willpower pool | 1 |
| +1 to an Ability (Individual) | 1 |
| Totem can always find pack members | 1 |
| Totem can speak to all pack members | 1 |
| Totem is nearly always with the pack | 2 |
| Pack is respected by spirits of totem's type | 2 |
| Extra Charm for totem spirit | 2 |

---

## Ban Design

| Type | Description | Severity |
|------|-------------|----------|
| Protection | Must protect something (animals, places, people) | Low-Medium |
| Behavioral | Must/must not act certain ways | Medium-High |
| Ritual | Regular observances required | Medium |
| Obedience | Must obey totem's commands | High |
| Taboo | Specific prohibitions with consequences | Variable |

**Rule**: Ban severity should match totem cost. Higher power = stricter demands.

---

## Creation Steps

1. **Type** — Respect/War/Wisdom/Cunning
2. **Cost** — 4-8 typical (determines power level)
3. **Individual Traits** — Permanent Renown + Attributes/Abilities/Modifiers (all pack members)
4. **Pack Traits** — Willpower pool + powerful abilities (one at a time, capped usage)
5. **Ban** — Thematic restriction (severity matches cost)
6. **Avatar** — Physical description of the Jaggling
7. **Brood** — What lesser spirits serve this totem
8. **Validate** — Compare to existing totems at same cost

---

## Output Format

```markdown
# [Totem Name]

**Type**: [Respect/War/Wisdom/Cunning]
**Background Cost**: [X]

## Individual Traits (All Pack Members)

**Permanent Renown**: [Renown bonuses]

**Additional Benefits**:
- [Attribute/Ability bonuses, difficulty modifiers, unique abilities]

## Pack Traits (Shared, One at a Time)

**Willpower**: [X per story]

**Special Abilities**:
- [Powerful abilities with usage limitations]

## Ban

[What the pack must/must not do, with consequences for violation]

## Totem Avatar

[Physical description, personality, how it communicates with the pack]

## Brood

[What lesser spirits serve this totem]
```

---

## Design Philosophy

A well-designed totem should:

1. **Feel thematically coherent** — All traits flow from the totem's nature
2. **Offer meaningful choices** — Pack Traits require deciding who benefits when
3. **Create story hooks** — Bans should generate interesting situations, not just penalties
4. **Scale appropriately** — Higher cost = more power AND more demands
5. **Respect existing balance** — Garou are already powerful; totems enhance, not break
