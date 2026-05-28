# Class Responsibilities

## Core Layer

| Class         | Responsibility                                                                                    |
| ------------- | ------------------------------------------------------------------------------------------------- |
| `GameManager` | Singleton. Initializes game, manages phases, orchestrates state changes. Does NOT handle visuals. |
| `GameState`   | Holds BoardState, TokenState[], current player, phase tracking, action counters                   |
| `BoardState`  | 5x5 grid (TileData[,]), reserve lists, draw pile stack, discard pile                              |
| `TokenState`  | Token identity (owner, type), position (tile, node), physical tracking state                      |

## Data Layer

| Class           | Responsibility                                                              |
| --------------- | --------------------------------------------------------------------------- |
| `TileData`      | Defines a tile: ID, sprite, path segments, rotation, grid position          |
| `TokenData`     | Defines a token: ID, sprite, owner, type, Board SDK glyph ID                |
| `PathSegment`   | Connects two EdgeNode values with a PathColor                               |
| `TileDatabase`  | ScriptableObject containing `List<TileData>` for all 25 tiles               |
| `TokenDatabase` | ScriptableObject with 6 named token slots (Red/Blue x Attack/Exploit/Ghost) |

## View Layer

| Class                 | Responsibility                                                                       |
| --------------------- | ------------------------------------------------------------------------------------ |
| `TileManager`         | Singleton. Spawns TileView, provides grid-to-world conversion, holds TileDatabase    |
| `TokenManager`        | Singleton. Spawns TokenView, handles glyph events, snaps tokens, holds TokenDatabase |
| `TileView`            | MonoBehaviour on tile GameObjects. Holds TileData, manages sprite                    |
| `TokenView`           | MonoBehaviour on token GameObjects. Holds TokenData and TokenState                   |
| `BackgroundRenderer`  | Renders board background as solid color or sprite                                    |
| `GridOverlayRenderer` | Draws 5x5 grid lines with glow effect                                                |
| `CameraController`    | Configures orthographic camera for 1920x1080                                         |

## Input Layer

| Class          | Responsibility                                                                         |
| -------------- | -------------------------------------------------------------------------------------- |
| `InputManager` | Singleton. Polls BoardInput.GetActiveContacts(), fires events. ONLY Board.Input import |
