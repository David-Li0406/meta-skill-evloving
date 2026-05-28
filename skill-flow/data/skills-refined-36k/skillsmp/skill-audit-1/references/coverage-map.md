# Coverage Map

workflow-to-skill mapping for gap analysis.

## luke's workflow activities

### daily coding

| activity | skill | status |
|----------|-------|--------|
| linear issue work | issue-context, loop | covered |
| code review | pr-audit | covered |
| slack communication | slack | covered |
| agent delegation | agent-pair | covered |
| design work | emil-kowalski | covered |

### skill management

| activity | skill | status |
|----------|-------|--------|
| create new skill | skill-create | covered |
| improve existing skill | skill-improve | covered |
| audit all skills | skill-audit | covered |
| compose skills | skill-compose | covered |
| route to skill | skill-chain | covered |
| generate prompts | metaprompt-factory | covered |

### communication

| activity | skill | status |
|----------|-------|--------|
| slack messages | slack | covered |
| imessages | imessage | covered |

### validation

| activity | skill | status |
|----------|-------|--------|
| quick check | consult-light | covered |
| deep review | consult-deep | covered |
| pr review | pr-audit | covered |

### clarification

| activity | skill | status |
|----------|-------|--------|
| gather requirements | deep-ask | covered |

### scaffolding

| activity | skill | status |
|----------|-------|--------|
| admin dashboard | dashboard | covered |

## gap detection template

when auditing, check each category:

```
Category: [name]
├── Activity 1 → skill? [✓ or gap]
├── Activity 2 → skill? [✓ or gap]
└── Activity 3 → skill? [✓ or gap]
```

## common gap patterns

### missing orchestration

```
gap: no skill for long-running autonomous work
solution: loop skill
```

### missing validation tier

```
gap: only one level of review
solution: consult-light + consult-deep (two tiers)
```

### missing communication channel

```
gap: can't notify user
solution: slack, imessage skills
```

### missing clarification

```
gap: jumping into work without requirements
solution: deep-ask skill
```

## coverage health

| coverage | meaning |
|----------|---------|
| 100% | all activities have skills |
| 80-99% | minor gaps, likely acceptable |
| 60-79% | notable gaps, consider new skills |
| <60% | significant gaps, prioritize skill creation |

## mapping new activities

when user develops new workflow patterns:

1. identify the activity
2. check if existing skill covers it
3. if partial coverage → extend existing skill
4. if no coverage → create new skill via skill-create
5. verify coverage in next audit

## skill consolidation signals

opposite of gaps - too many skills for one activity:

| signal | action |
|--------|--------|
| 2 skills, same trigger | merge into one |
| skill A always calls skill B | absorb B into A |
| >50% content overlap | deduplicate |
| same domain, different scope | may be valid (keep light + deep) |
