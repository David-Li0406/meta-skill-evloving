# Other Diagram Types

Quick reference for additional Mermaid diagram types.

## Gantt Chart

Project timelines and scheduling.

```mermaid
gantt
    title Project Schedule
    dateFormat YYYY-MM-DD

    section Planning
    Requirements    :a1, 2024-01-01, 7d
    Design          :a2, after a1, 5d

    section Development
    Backend         :b1, after a2, 14d
    Frontend        :b2, after a2, 14d

    section Testing
    QA              :c1, after b1, 7d
```

Key syntax:
- `dateFormat YYYY-MM-DD`
- `section Name`
- `Task :id, start, duration` or `Task :id, after other_id, duration`
- Modifiers: `done`, `active`, `crit`

## Timeline

Chronological events.

```mermaid
timeline
    title Company History
    2020 : Founded
         : First product
    2021 : Series A
         : Team expansion
    2022 : International launch
    2023 : Acquisition
```

## User Journey

User experience flows.

```mermaid
journey
    title User Checkout Experience
    section Browse
        View products: 5: User
        Add to cart: 4: User
    section Checkout
        Enter details: 3: User
        Payment: 2: User, System
        Confirmation: 5: System
```

Format: `Task: score: actors` (score 1-5, 5 is best)

## Pie Chart

```mermaid
pie title Browser Usage
    "Chrome" : 65
    "Firefox" : 15
    "Safari" : 12
    "Other" : 8
```

## Quadrant Chart

2x2 matrix for analysis.

```mermaid
quadrantChart
    title Technology Assessment
    x-axis Low Complexity --> High Complexity
    y-axis Low Impact --> High Impact
    quadrant-1 Strategic
    quadrant-2 Quick Wins
    quadrant-3 Fill-ins
    quadrant-4 Major Projects
    Feature A: [0.8, 0.9]
    Feature B: [0.3, 0.7]
    Feature C: [0.6, 0.4]
```

## Git Graph

Visualize git history.

```mermaid
gitGraph
    commit
    commit
    branch feature
    checkout feature
    commit
    commit
    checkout main
    merge feature
    commit
```

## XY Chart

Data visualization.

```mermaid
xychart-beta
    title "Sales Over Time"
    x-axis [Jan, Feb, Mar, Apr, May]
    y-axis "Revenue ($K)" 0 --> 100
    bar [30, 45, 60, 55, 80]
    line [30, 45, 60, 55, 80]
```

## Sankey

Flow/distribution diagrams.

```mermaid
sankey-beta
    Source A,Target X,50
    Source A,Target Y,30
    Source B,Target X,20
    Source B,Target Z,40
```
