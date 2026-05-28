# Pact Module

Create formal agreements between demons and mortals.

## Overview

Pacts are supernatural contracts that bind mortals to demons in exchange for favors, powers, or knowledge. They are the primary mechanism for demons to gain Faith.

---

## Types of Pacts

### Soul Pact
The mortal's soul is claimed upon death.
- **Demon Gains**: Permanent claim to soul; maximum Faith potential
- **Mortal Gains**: Significant supernatural benefits
- **Breaking**: Nearly impossible; requires divine intervention

### Service Pact
The mortal serves the demon for a specified period.
- **Demon Gains**: Regular Faith; mortal services
- **Mortal Gains**: Specific benefit for duration
- **Breaking**: Possible with significant cost

### Exchange Pact
A single transaction: one favor for one favor.
- **Demon Gains**: Single Faith boost; specific service
- **Mortal Gains**: One-time benefit
- **Breaking**: Typically ends naturally when fulfilled

### Worship Pact
The mortal provides ongoing devotion and worship.
- **Demon Gains**: Steady Faith income
- **Mortal Gains**: Ongoing minor benefits; sense of purpose
- **Breaking**: Fades if worship stops

---

## Creating a Pact

### Step 1: The Mortal's Desire

What does the mortal want badly enough to deal with a demon?

| Desire Category | Examples |
|-----------------|----------|
| Health | Cure disease, heal injury, extend life |
| Wealth | Money, success, business advantage |
| Love | Win someone's heart, save relationship |
| Power | Authority, influence, political position |
| Knowledge | Secrets, skills, understanding |
| Revenge | Punish enemy, destroy rival |
| Protection | Safety from threat, rescue loved one |
| Beauty | Physical perfection, eternal youth |

### Step 2: What the Demon Offers

Demons can provide supernatural aid within their capabilities:

| Offer Type | Limitations |
|------------|-------------|
| **Healing** | Can cure almost anything; resurrection is difficult |
| **Wealth** | Usually through manipulation, not creation |
| **Love** | Can compel attraction; true love is harder |
| **Power** | Can grant temporary abilities or arrange circumstances |
| **Knowledge** | Can share vast ancient wisdom |
| **Revenge** | Destruction is easy; elegant revenge takes finesse |
| **Protection** | Can ward, guard, or eliminate threats |
| **Beauty** | Transfiguration powers excel here |

### Step 3: What the Mortal Owes

The demon's price for services rendered:

| Price Category | Description | Faith Value |
|----------------|-------------|-------------|
| **Worship** | Regular prayer and devotion | Low but steady |
| **Service** | Tasks and missions | Moderate per task |
| **Recruitment** | Bring other mortals to demon | Moderate to high |
| **Sacrifice** | Give up something valuable | Based on value |
| **Soul** | Claim upon death | Maximum |

### Step 4: Terms and Conditions

Every pact should specify:

1. **Duration**: How long does the pact last?
2. **Trigger**: When does the pact take effect?
3. **Obligations**: What must each party do?
4. **Limitations**: What cannot be demanded?
5. **Termination**: How can the pact end?
6. **Consequences**: What happens if terms are broken?

---

## Pact Mechanics

### Forming the Pact

- **Requirement**: Mortal must agree freely (coercion weakens pact)
- **Ritual**: Verbal agreement is sufficient; written strengthens
- **Witness**: True Name invocation seals the pact
- **Effect**: Supernatural bond forms; detectable by other supernaturals

### Faith from Pacts

| Pact Type | Faith/Month | Notes |
|-----------|-------------|-------|
| Soul Pact | 2-3 | Highest yield; mortal becomes invested |
| Service Pact | 1-2 | Depends on activity level |
| Exchange Pact | 1-5 (one time) | Based on favor magnitude |
| Worship Pact | 1 | Reliable but modest |

### Breaking Pacts

| Method | Difficulty | Consequences |
|--------|------------|--------------|
| Mutual agreement | Easy | None |
| Mortal's death | N/A | Soul collected (if soul pact) |
| Fulfill all terms | N/A | Pact ends naturally |
| Breach of terms | Varies | Supernatural punishment |
| Divine intervention | Very hard | Demon may be weakened |
| Another demon | Hard | Creates new obligations |

**Breach Consequences**:
- Demon's curse activates
- Faith bond becomes painful
- Mortal suffers bad fortune
- Soul claim may activate early

---

## Common Pact Patterns

### The Classic Deal
*Mortal wants something; demon provides in exchange for soul*

**Structure**:
- Demon grants significant one-time benefit
- Mortal's soul is claimed at death
- Mortal may serve demon in interim

**Variations**:
- Time-limited soul claim (e.g., 10 years of service, then soul)
- Conditional soul claim (e.g., only if mortal dies unrepentant)

### The Patron Relationship
*Demon provides ongoing support; mortal serves and worships*

**Structure**:
- Demon grants regular minor benefits
- Mortal worships and serves
- Either party can end with notice

**Variations**:
- Demon "adopts" mortal, becoming patron saint
- Mortal joins cult serving the demon
- Exclusive vs. non-exclusive worship

### The Single Favor
*One-time exchange with no ongoing relationship*

**Structure**:
- Demon does one thing for mortal
- Mortal does one thing for demon
- Pact ends when both fulfilled

**Variations**:
- Immediate exchange vs. deferred payment
- Specific action vs. "favor to be named later"

### The Empowerment
*Demon invests power in mortal for ongoing service*

**Structure**:
- Demon grants supernatural abilities (via invested Faith)
- Mortal becomes enhanced thrall
- Abilities lost if pact ends

**Variations**:
- Combat enhancement (bodyguard thrall)
- Social enhancement (infiltrator thrall)
- Psychic abilities (seer thrall)

---

## Pact Complications

### Loopholes
- Mortals may try to fulfill letter while violating spirit
- Demons are master contract lawyers; usually prepared
- Clever mortals may still find escape clauses

### Third Parties
- Other demons may try to steal thralls
- Angels or hunters may try to break pacts
- Family members may bargain for release

### Torment Effects
- High-Torment demons make crueler pacts
- May demand more suffering
- Less concerned with mortal wellbeing
- Pacts may have hidden punishment clauses

---

## Data Lookup

```bash
# Get pact templates
python scripts/lookup.py d20.rules pacts "soul-pact"

# Search by desire type
python scripts/lookup.py d20.rules pacts --find "wealth"
```

---

## Output Template

```markdown
# Pact: [Mortal Name] and [Demon Name]

**Pact Type**: [Soul/Service/Exchange/Worship]
**Date Formed**: [When]
**Duration**: [How long]

## The Mortal's Desire

[What did they want?]

## The Offer

[What did the demon promise?]

### Specific Terms
- [Term 1]
- [Term 2]
- [Term 3]

## The Price

[What does the mortal owe?]

### Specific Obligations
- [Obligation 1]
- [Obligation 2]
- [Obligation 3]

## Conditions

### Duration
[How long the pact lasts]

### Limitations
[What the demon cannot demand]
[What the mortal cannot request]

### Termination Conditions
- [Condition 1]
- [Condition 2]

### Breach Consequences
[What happens if either party breaks terms]

## Current Status

**Faith Generated**: [Amount per period]
**Empowerments**: [If any Faith invested]
**Relationship**: [Current state of demon-mortal relationship]

## Notes

[Any special circumstances or ongoing developments]
```
