# Architecture Layer Model

## The Six Layers

| Layer      | Location              | Purpose                                      |
| ---------- | --------------------- | -------------------------------------------- |
| **Data**   | `Core/Data/`          | Immutable data structures, ScriptableObjects |
| **State**  | `Core/State/`         | Mutable runtime game state                   |
| **Logic**  | `Core/GameManager.cs` | Game rules, orchestration                    |
| **View**   | `View/`               | Visual representation, Unity components      |
| **Input**  | `Input/`              | Board SDK abstraction                        |
| **Config** | `Config/`             | Static layout constants                      |

## Layer Dependencies

```text
Config ← (all layers read constants)
         ↓
Data ← State ← Logic
                ↓
            View ← Input
```

- **Config**: No dependencies (pure constants)
- **Data**: No dependencies (pure data)
- **State**: References Data types
- **Logic**: References State and Data
- **View**: References Logic, State, Data
- **Input**: Only Board SDK, fires events

## Namespace Mapping

| Layer  | Namespace                  |
| ------ | -------------------------- |
| Data   | `ZeroDayAttack.Core.Data`  |
| State  | `ZeroDayAttack.Core.State` |
| Logic  | `ZeroDayAttack.Core`       |
| View   | `ZeroDayAttack.View`       |
| Input  | `ZeroDayAttack.Input`      |
| Config | `ZeroDayAttack.Config`     |
