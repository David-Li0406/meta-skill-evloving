# Character Module

Create mechanically valid Garou (werewolf) characters for W20.

## PC vs NPC

| Type | Linked Documents | When |
|------|------------------|------|
| **PC** (default) | REQUIRED | Standard creation |
| **NPC** | Not required | "NPC", "quick", "simple", "stat block" |

## Dependencies (PC Only)

**Read `modules/background-expansion.md` for the complete background → module mapping.**

| Background | Action |
|------------|--------|
| Fetish | Read `modules/fetish.md`, create fetish document(s) |
| Rites | Read `modules/rite.md`, create rite documents |
| Totem | Read `modules/totem.md`, create pack totem |
| Allies/Kinfolk | Read `modules/kinfolk.md` or create NPC |
| Mentor | Create NPC document |

## Creation Steps

1. **PC/NPC** — Default PC
2. **Concept** — Name, core idea, history hook
3. **Breed** — Homid (Gnosis 1), Metis (Gnosis 3), or Lupus (Gnosis 5)
4. **Auspice** — Moon phase determines Rage, Renown, role
5. **Tribe** — Social group determines Willpower, restrictions
6. **Nature & Demeanor** — From `lookup.py character.archetypes archetypes`
7. **Attributes** — 7/5/3 across Physical/Social/Mental
8. **Abilities** — 13/9/5 across Talents/Skills/Knowledges (cap 3)
9. **Backgrounds** — 5 dots. Note which need sub-documents
10. **Gifts** — 1 breed + 1 auspice + 1 tribe (Level 1 only)
11. **Renown** — Set by auspice
12. **Rage/Gnosis/Willpower** — Set by auspice/breed/tribe
13. **Merits & Flaws** — Optional
14. **⛔ BACKGROUNDS (PC)** — Create documents for Fetish/Totem/Rites/Allies
15. **Freebies** — 15 + Flaws - Merits. Spend exactly.
16. **Derived** — Rank 1, Health 7
17. **Specialties** — Required for 4+ traits
18. **Description** — Appearance in all forms, history
19. **Document** — Link all sub-documents
20. **Validate**

---

## Quick Reference Tables

### Breed
| Breed | Gnosis | Restrictions |
|-------|--------|--------------|
| Homid | 1 | Cannot start with Rituals |
| Metis | 3 | Must have deformity |
| Lupus | 5 | Many Knowledge restrictions |

### Auspice
| Auspice | Rage | Renown (G/H/W) |
|---------|------|----------------|
| Ragabash | 1 | 2/1/0 |
| Theurge | 2 | 0/1/2 |
| Philodox | 3 | 0/2/1 |
| Galliard | 4 | 2/0/1 |
| Ahroun | 5 | 2/1/0 |

### Tribe Willpower
Black Furies 3, Bone Gnawers 4, Children of Gaia 4, Fianna 3, Get of Fenris 3, Glass Walkers 3, Red Talons 3, Shadow Lords 3, Silent Striders 3, Silver Fangs 3, Stargazers 4, Uktena 3, Wendigo 4

---

## Freebie Costs

| Trait | Cost |
|-------|------|
| Attribute | 5 |
| Ability | 2 |
| Background | 1 |
| Gift (Level 1) | 7 |
| Rage | 1 |
| Gnosis | 2 |
| Willpower | 1 |

---

## Validation

- [ ] Attributes: 15 dots (+ 9 base)
- [ ] Abilities: 27 dots, none > 3
- [ ] Backgrounds: 5 dots
- [ ] Gifts: 3 total (1 breed, 1 auspice, 1 tribe)
- [ ] Breed/tribe restrictions honored
- [ ] Metis has deformity (if applicable)
- [ ] Rage = auspice, Gnosis = breed, Willpower = tribe
- [ ] Freebies spent exactly
- [ ] (PC) All relevant backgrounds have documents
