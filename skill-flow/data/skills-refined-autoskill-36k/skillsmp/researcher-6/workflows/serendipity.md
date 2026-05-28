# Workflow: Serendipity

Engineering unexpected discoveries through lateral search and anomaly hunting.

## Purpose

> "Chance favors the prepared mind." — Louis Pasteur

Standard search finds what you're looking for. Serendipity search finds what you didn't know you needed.

## When to Use

- Research feels "too clean" or predictable
- Need a fresh angle on a stale topic
- Looking for unexpected connections
- Want to differentiate from obvious sources
- Stuck in a research rut

## Serendipity Strategies

### 1. Relational Queries

Search for unexpected connections:

```
web_search("How is [concept A] related to [unrelated concept B]")
web_search("[your topic] AND [surprising field]")
web_search("[your topic] unexpected OR surprising OR counterintuitive")
```

**Examples:**
- "How is friction related to trust"
- "cognitive load AND architecture"
- "decision making unexpected biology"

### 2. Temporal Displacement

Search in unexpected time periods:

```
web_search("[topic] history OR origins OR 19th century")
web_search("[topic] ancient OR classical")
web_search("[topic] before:2000")
```

Old ideas often contain wisdom that was forgotten or rediscovered.

### 3. Domain Hopping

Search how other fields solved similar problems:

| Your Domain | Try Searching |
|-------------|---------------|
| AI safety | Aviation safety, nuclear safety, medical errors |
| Decision-making | Poker strategy, military tactics, judicial reasoning |
| System design | Biology, ecology, urban planning |
| Friction mechanisms | Speedbump design, circuit breakers, immune systems |

```
web_search("[analogous field] [your core concept]")
```

### 4. Failure Mining

Successes are over-studied. Failures are under-mined.

```
web_search("[topic] failure OR disaster OR mistake")
web_search("[topic] what went wrong")
web_search("[topic] postmortem OR retrospective")
```

### 5. Contrarian Sources

Find who disagrees with the mainstream:

```
web_search("[topic] skeptic OR critic")
web_search("[topic] overrated OR myth")
web_search("[mainstream claim] wrong OR incorrect")
```

### 6. Bibliographic Serendipity

In a good paper's references:
- Look for the ONE citation that seems out of place
- Follow it—it might reveal a connection others missed

### 7. Random Walk

From any interesting source:
1. Pick a random citation (not the obvious one)
2. Read that paper
3. Pick another random citation
4. Repeat 3x

Where you end up is often surprising.

### 8. Anomaly Hunting

In your existing evidence, look for:
- The one data point that doesn't fit
- The finding that contradicts the pattern
- The source that reaches different conclusions

**Investigate the anomaly.** It might be:
- An error (fine, rule it out)
- A boundary condition (valuable!)
- A completely different frame (potentially transformative)

## Recording Serendipitous Finds

When you find something unexpected:

```json
{
  "id": "ev_025",
  "claim": "Medieval monastery scheduling practices anticipated modern cognitive forcing",
  "source": {...},
  "confidence": 0.5,
  "serendipitous": true,
  "serendipity_path": "domain_hop: searched 'deliberation rituals history'",
  "connection_to_main_topic": "Benedictine Rule required 'stopping points' before major decisions—structural friction in decision-making",
  "potential_value": "Historical precedent; narrative hook; shows concept is ancient",
  "follow_up_needed": "Verify historical accuracy; find primary sources on monastic decision practices"
}
```

## Serendipity Evaluation

Not all surprises are valuable. Evaluate finds:

| Question | Good Sign | Bad Sign |
|----------|-----------|----------|
| Does it connect to your core argument? | Yes, even indirectly | No connection visible |
| Is it genuinely novel? | Not in your other sources | Already well-known |
| Does it add a new dimension? | New angle or evidence type | More of the same |
| Is it defensible? | Can find supporting evidence | One-off claim |
| Would it surprise readers? | Yes, productively | Yes, confusingly |

## Integration

Serendipitous finds can become:
- **The Turn**: A surprising insight that reframes the whole piece
- **A compelling example**: Concrete instance that makes abstract ideas vivid
- **Historical context**: "This problem isn't new—here's precedent"
- **A section hook**: Opens a section with something unexpected
- **The P.S.**: A parting insight that rewards readers who finish

## Time-Boxing

Serendipity is valuable but can be endless. Time-box it:

- **5 minutes**: Quick scan for anomalies in existing evidence
- **15 minutes**: One domain hop or temporal displacement search
- **30 minutes**: Full serendipity session with multiple strategies

If nothing emerges, move on. Serendipity can't be forced.

## Output

After serendipity session:
- Add any valuable finds to evidence.json with `serendipitous: true`
- Note potential uses in outline.md
- Flag any that need verification before use
