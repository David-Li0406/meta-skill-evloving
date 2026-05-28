# Background Expansion Module

Automatically expand PC backgrounds into linked documents.

## Expansion Rules

### Always Expand (PC)
| Background | Module | Output |
|------------|--------|--------|
| Fetish | `fetish.md` | Fetish document per item |
| Rites | `rite.md` | Rite document per rite |
| Totem | `totem.md` | Pack totem (pooled) |
| Allies | NPC or `kinfolk.md` | Companion documents |
| Kinfolk | `kinfolk.md` | Kinfolk documents |
| Mentor | NPC document | Mentor document |

### Scale by Rating

**Fetish**
| Rating | Fetishes |
|--------|----------|
| 1 | 1 Level 1 |
| 2 | 1 Level 2 or 2 Level 1 |
| 3-5 | Combination up to rating |

**Rites**
| Rating | Rites |
|--------|-------|
| 1 | 1 Level 1 |
| 2 | 2 rites (max Level 2) |
| 3-5 | Rating rites (max = rating) |

**Allies/Kinfolk**
| Rating | NPCs |
|--------|------|
| 1-2 | 1 |
| 3 | 2 |
| 4-5 | 2-3 |

**Mentor**
| Rating | Mentor Rank |
|--------|-------------|
| 1 | Fostern |
| 2 | Adren |
| 3 | Athro |
| 4-5 | Elder |

## File Structure

```
[character]/
├── [character].md
├── fetishes/
├── rites/
├── companions/
└── totem/
```

## Linking Format

```markdown
| Background | Rating | Details |
|------------|--------|---------|
| Fetish | ●●● | [Fang Dagger](./fetishes/fang_dagger.md) |
| Rites | ●● | [Binding](./rites/binding.md) |
```

## Validation

- [ ] All Fetishes have documents
- [ ] All Rites have documents
- [ ] Rituals Knowledge ≥ highest rite level
- [ ] Pack totem documented
- [ ] Key Allies/Kinfolk documented
- [ ] Mentor documented with appropriate rank
