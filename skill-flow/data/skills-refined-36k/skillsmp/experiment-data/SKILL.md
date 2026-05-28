---
name: experiment-data
description: Guidance for working with the experiment_data.py data object - hierarchical navigation, chat messages, sentiment analysis, and DataFrame exports
---

# Experiment Data Skill

Use this skill when working with experimental data in `analysis/experiment_data.py`. This skill provides guidance on navigating the hierarchical data structure, accessing player/group/session data, and performing analysis.

## Data Hierarchy

```
Experiment
  └─ Session (session_code, treatment)
      └─ Segment (introduction, supergame1-5, finalresults)
          └─ Round (round_number)
              └─ Group (group_id 1-4)
                  └─ Player (label A-R)
```

## Loading Data

```python
from experiment_data import load_experiment_data

# Load multi-session experiment
# Format: (data_csv_path, chat_csv_path, treatment)
file_pairs = [
    ('01_t1_data.csv', '01_t1_chat.csv', 1),
    ('02_t2_data.csv', '02_t2_chat.csv', 2),
]
experiment = load_experiment_data(file_pairs, name="My Experiment")
```

## Navigating the Hierarchy

### Experiment Level
```python
experiment.sessions                    # Dict[session_code, Session]
experiment.get_session('abc123')       # Get specific session
experiment.list_session_codes()        # List all session codes
```

### Session Level
```python
session = experiment.get_session('abc123')
session.session_code                   # str: Session identifier
session.treatment                      # int: Treatment condition (1 or 2)
session.segments                       # Dict[name, Segment]
session.participant_labels             # Dict[participant_id, label]
session.get_segment('supergame1')      # Get segment by name
session.get_supergame(1)               # Shortcut for get_segment('supergame1')
```

### Segment Level
```python
segment = session.get_supergame(1)
segment.name                           # str: 'supergame1', 'introduction', etc.
segment.rounds                         # Dict[round_number, Round]
segment.get_round(1)                   # Get specific round
segment.get_player_across_rounds('A')  # Dict[round_num, Player] for player A
```

### Round Level
```python
round_obj = segment.get_round(1)
round_obj.round_number                 # int: Round number within segment
round_obj.groups                       # Dict[group_id, Group]
round_obj.players                      # Dict[label, Player] - all players
round_obj.get_group(1)                 # Get specific group
round_obj.get_player('A')              # Get player by label
round_obj.get_player_by_id(5)          # Get player by participant ID
```

### Group Level
```python
group = round_obj.get_group(1)
group.group_id                         # int: Group ID (1-4)
group.players                          # Dict[label, Player]
group.total_contribution               # float: Sum of player contributions
group.individual_share                 # float: round(total_contribution * 0.4)
group.get_player('A')                  # Get player by label
group.chat_messages                    # List[ChatMessage] for this group
```

### Player Level
```python
player = group.get_player('A')
player.label                           # str: 'A', 'B', etc.
player.participant_id                  # int: ID in session
player.id_in_group                     # int: Position in group (1-4)
player.contribution                    # float: Amount contributed (0-25)
player.payoff                          # float: Round payoff
player.group_id                        # int: Group they belong to
player.chat_messages                   # List[ChatMessage] from this player
player.data                            # Dict: Additional player attributes
```

## Chat Messages

### ChatMessage Attributes
```python
msg.nickname                           # str: Player label
msg.body                               # str: Message content
msg.timestamp                          # float: Unix timestamp
msg.datetime                           # datetime: Converted timestamp
msg.sentiment                          # float: Compound score (-1 to 1)
msg.positive_sentiment                 # float: Positive score (0-1)
msg.negative_sentiment                 # float: Negative score (0-1)
```

### Access Patterns
```python
player.chat_messages                   # Player's messages in round
group.chat_messages                    # All group messages in round
round_obj.get_all_chat_messages()      # All messages in round
segment.get_all_chat_messages()        # All messages in supergame
session.get_all_chat_messages()        # All messages in session
experiment.get_all_chat_messages()     # All messages across sessions
```

## Sentiment Analysis (VADER)

```python
# Returns SentimentAnalysis object or None
sentiment = player.get_chat_sentiment()
sentiment.compound                     # float: Overall score (-1 to 1)
sentiment.positive                     # float: Positive component (0-1)
sentiment.negative                     # float: Negative component (0-1)
sentiment.neutral                      # float: Neutral component (0-1)
sentiment.message_count                # int: Messages analyzed
sentiment.dominant_sentiment           # str: 'positive', 'negative', 'neutral'
sentiment.sentiment_intensity          # str: 'strong', 'moderate', 'weak'

# Available at all levels
player.get_chat_sentiment()
group.get_chat_sentiment()
round_obj.get_chat_sentiment()
segment.get_chat_sentiment()
session.get_overall_sentiment()
experiment.get_overall_sentiment()
```

## DataFrame Exports

```python
# Contributions (one row per player-round)
df = experiment.to_dataframe_contributions()
# Columns: session_code, treatment, segment, round, group, label,
#          participant_id, contribution, payoff, role

# Chat messages (one row per message)
df = experiment.to_dataframe_chat()
# Columns: session, segment, round, group, player, timestamp, message
```

## Common Access Patterns

### Get Single Value
```python
# Get player A's contribution in supergame 1, round 1
contrib = experiment.get_session('abc123') \
    .get_supergame(1) \
    .get_round(1) \
    .get_player('A').contribution
```

### Track Player Across Rounds
```python
for round_num, player in segment.get_player_across_rounds('A').items():
    print(f"Round {round_num}: {player.contribution}")
```

### Iterate Through Groups
```python
for group_id, group in round_obj.groups.items():
    print(f"Group {group_id}: total={group.total_contribution}")
    for label, player in group.players.items():
        print(f"  {label}: {player.contribution}")
```

### Treatment Comparisons
```python
for session in experiment.sessions.values():
    if session.treatment == 1:
        # Treatment 1 analysis
        pass
```

### Calculate Group Statistics
```python
for group_id, group in round_obj.groups.items():
    contributions = [p.contribution for p in group.players.values()]
    avg = sum(contributions) / len(contributions)
    print(f"Group {group_id} avg contribution: {avg}")
```

## Key Constants

- **MPCR (Multiplier)**: 0.4
- **Endowment**: 25 points per round
- **Players per group**: 4
- **Participant labels**: A-R (skips I and O)
- **Payoff formula**: `payoff = (25 - contribution) + (group_total * 0.4)`
- **Individual share**: `round(group_total * 0.4)`

## Supergame Round Counts

| Supergame | Rounds |
|-----------|--------|
| supergame1 | 3 |
| supergame2 | 4 |
| supergame3 | 4 |
| supergame4 | 4 |
| supergame5 | 5 |

## Data File Naming Convention

- Data files: `{session_num}_t{treatment}_data.csv`
- Chat files: `{session_num}_t{treatment}_chat.csv`
- Example: `01_t1_data.csv`, `01_t1_chat.csv`

## Testing

Run tests to verify data integrity:
```bash
uv run pytest analysis/tests/ -v
```

Tests are located in `analysis/tests/` and verify:
- Contribution values match raw CSV
- Chat messages load correctly
- Group totals equal sum of player contributions
- Payoff calculations are correct
- Segment/round structure is preserved
