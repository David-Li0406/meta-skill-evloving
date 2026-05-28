---
name: mahjong-ui-components
description: UI component patterns for Fujian Mahjong game. Use when building tile displays, hand layouts, call prompts, score screens, or any visual game elements.
---

# Mahjong UI Components

Patterns for building consistent UI components for the Mahjong game.

## When to Use

- Building tile display components
- Laying out player hands
- Creating call prompt overlays
- Designing score breakdown screens
- Implementing game board layout
- Styling exposed melds and bonus tiles

## Component Hierarchy

```
GameScreen
├── Header
│   ├── RoomCode
│   ├── GoldTileIndicator
│   └── WallCount
├── GameBoard
│   ├── OpponentArea (×3)
│   │   ├── PlayerName
│   │   ├── ExposedMelds
│   │   ├── BonusTiles
│   │   └── ConnectionStatus
│   ├── DiscardPile
│   └── CenterInfo
├── PlayerHand
│   ├── ConcealedTiles
│   ├── ExposedMelds
│   ├── BonusTiles
│   └── ActionButtons
└── Overlays
    ├── CallPrompt
    ├── WinScreen
    └── DrawScreen
```

## Tile Components

### Base Tile

```jsx
// React component
function Tile({ tileId, size = 'medium', onClick, disabled, selected, isGold }) {
  const tileType = getTileType(tileId);
  const [category, value] = parseTileType(tileType);

  const sizeClasses = {
    small: 'w-8 h-12',
    medium: 'w-12 h-16',
    large: 'w-16 h-24'
  };

  return (
    <div
      className={`
        ${sizeClasses[size]}
        rounded-md border-2 bg-white
        flex items-center justify-center
        cursor-pointer transition-all
        ${selected ? 'border-blue-500 -translate-y-2' : 'border-gray-300'}
        ${disabled ? 'opacity-50 cursor-not-allowed' : 'hover:border-blue-300'}
        ${isGold ? 'ring-2 ring-yellow-400' : ''}
      `}
      onClick={disabled ? undefined : onClick}
    >
      <TileContent category={category} value={value} />
      {isGold && <GoldIndicator />}
    </div>
  );
}

function TileContent({ category, value }) {
  if (category === 'dots') {
    return <DotsIcon count={value} />;
  }
  if (category === 'bamboo') {
    return <BambooIcon count={value} />;
  }
  if (category === 'characters') {
    return <CharacterIcon number={value} />;
  }
  if (category === 'wind') {
    return <WindIcon direction={value} />;
  }
  if (category === 'dragon') {
    return <DragonIcon type={value} />;
  }
}

function GoldIndicator() {
  return (
    <div className="absolute -top-1 -right-1 w-4 h-4 bg-yellow-400 rounded-full flex items-center justify-center">
      <span className="text-xs">金</span>
    </div>
  );
}
```

### Tile Back (Hidden)

```jsx
function TileBack({ size = 'medium' }) {
  const sizeClasses = {
    small: 'w-8 h-12',
    medium: 'w-12 h-16',
    large: 'w-16 h-24'
  };

  return (
    <div className={`
      ${sizeClasses[size]}
      rounded-md border-2 border-gray-400
      bg-gradient-to-br from-green-700 to-green-900
    `}>
      <div className="w-full h-full flex items-center justify-center">
        <span className="text-white text-opacity-30 text-2xl">麻</span>
      </div>
    </div>
  );
}
```

## Hand Components

### Player's Own Hand

```jsx
function PlayerHand({
  concealedTiles,
  exposedMelds,
  bonusTiles,
  goldTileType,
  drawnTile,
  onTileClick,
  selectedTile,
  canDiscard
}) {
  return (
    <div className="flex flex-col items-center gap-4 p-4 bg-gray-100 rounded-lg">
      {/* Bonus Tiles */}
      {bonusTiles.length > 0 && (
        <div className="flex gap-1">
          <span className="text-sm text-gray-500 mr-2">Bonus:</span>
          {bonusTiles.map(tile => (
            <Tile
              key={tile}
              tileId={tile}
              size="small"
              disabled
            />
          ))}
        </div>
      )}

      {/* Exposed Melds */}
      {exposedMelds.length > 0 && (
        <div className="flex gap-4">
          {exposedMelds.map((meld, i) => (
            <Meld key={i} meld={meld} goldTileType={goldTileType} />
          ))}
        </div>
      )}

      {/* Concealed Hand */}
      <div className="flex gap-1">
        {concealedTiles.map(tile => (
          <Tile
            key={tile}
            tileId={tile}
            size="large"
            isGold={getTileType(tile) === goldTileType}
            selected={selectedTile === tile}
            onClick={() => onTileClick(tile)}
            disabled={!canDiscard}
          />
        ))}

        {/* Drawn tile (separated) */}
        {drawnTile && (
          <>
            <div className="w-2" /> {/* Spacer */}
            <Tile
              tileId={drawnTile}
              size="large"
              isGold={getTileType(drawnTile) === goldTileType}
              selected={selectedTile === drawnTile}
              onClick={() => onTileClick(drawnTile)}
              disabled={!canDiscard}
            />
          </>
        )}
      </div>

      {/* Action Buttons */}
      {canDiscard && selectedTile && (
        <button
          className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
          onClick={() => onDiscard(selectedTile)}
        >
          Discard
        </button>
      )}
    </div>
  );
}
```

### Opponent Hand (Hidden)

```jsx
function OpponentHand({
  tileCount,
  exposedMelds,
  bonusTiles,
  goldTileType,
  playerName,
  isCurrentTurn,
  isConnected
}) {
  return (
    <div className={`
      flex flex-col items-center gap-2 p-2
      ${isCurrentTurn ? 'bg-yellow-100 rounded-lg' : ''}
    `}>
      <div className="flex items-center gap-2">
        <span className="font-medium">{playerName}</span>
        {!isConnected && <span className="text-red-500 text-sm">●</span>}
        {isCurrentTurn && <span className="text-yellow-600 text-sm">⟵ Turn</span>}
      </div>

      {/* Bonus Tiles */}
      {bonusTiles.length > 0 && (
        <div className="flex gap-1">
          {bonusTiles.map(tile => (
            <Tile key={tile} tileId={tile} size="small" disabled />
          ))}
        </div>
      )}

      {/* Exposed Melds */}
      {exposedMelds.length > 0 && (
        <div className="flex gap-2">
          {exposedMelds.map((meld, i) => (
            <Meld key={i} meld={meld} size="small" goldTileType={goldTileType} />
          ))}
        </div>
      )}

      {/* Hidden tiles */}
      <div className="flex gap-0.5">
        {Array(tileCount).fill(0).map((_, i) => (
          <TileBack key={i} size="small" />
        ))}
      </div>
    </div>
  );
}
```

### Meld Display

```jsx
function Meld({ meld, size = 'medium', goldTileType }) {
  return (
    <div className="flex gap-0.5 p-1 bg-gray-200 rounded">
      {meld.tiles.map(tile => (
        <Tile
          key={tile}
          tileId={tile}
          size={size}
          isGold={getTileType(tile) === goldTileType}
          disabled
        />
      ))}
      <span className="text-xs text-gray-500 self-end ml-1">
        {meld.type === 'chow' ? '吃' : '碰'}
      </span>
    </div>
  );
}
```

## Game Board Components

### Discard Pile

```jsx
function DiscardPile({ tiles, lastDiscard, goldTileType }) {
  return (
    <div className="p-4 bg-gray-50 rounded-lg min-h-[200px]">
      <h3 className="text-sm text-gray-500 mb-2">Discards</h3>
      <div className="flex flex-wrap gap-1 max-w-[300px]">
        {tiles.map((tile, i) => (
          <Tile
            key={tile}
            tileId={tile}
            size="small"
            isGold={getTileType(tile) === goldTileType}
            disabled
            className={tile === lastDiscard ? 'ring-2 ring-red-500' : ''}
          />
        ))}
      </div>
    </div>
  );
}
```

### Gold Tile Indicator

```jsx
function GoldTileIndicator({ goldTileType, exposedGold }) {
  return (
    <div className="flex items-center gap-2 p-2 bg-yellow-100 rounded-lg">
      <span className="text-sm font-medium text-yellow-800">Gold:</span>
      <Tile tileId={exposedGold} size="small" disabled />
      <span className="text-xs text-yellow-600">(Wild Card)</span>
    </div>
  );
}
```

### Wall Count

```jsx
function WallCount({ count }) {
  return (
    <div className="flex items-center gap-2 px-3 py-1 bg-gray-200 rounded">
      <span className="text-sm text-gray-600">Wall:</span>
      <span className="font-mono font-bold">{count}</span>
    </div>
  );
}
```

## Call Prompt

```jsx
function CallPrompt({
  discardedTile,
  discarderName,
  validCalls,  // ['win', 'pung', 'chow', 'pass']
  onCall,
  waitingFor,  // Number of players still deciding
  goldTileType
}) {
  const callLabels = {
    win: { text: '胡 Win', color: 'bg-red-500 hover:bg-red-600' },
    pung: { text: '碰 Pung', color: 'bg-blue-500 hover:bg-blue-600' },
    chow: { text: '吃 Chow', color: 'bg-green-500 hover:bg-green-600' },
    pass: { text: 'Pass', color: 'bg-gray-500 hover:bg-gray-600' }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl p-6 shadow-2xl max-w-md w-full mx-4">
        <h2 className="text-lg font-bold mb-4 text-center">
          {discarderName} discarded:
        </h2>

        <div className="flex justify-center mb-6">
          <Tile
            tileId={discardedTile}
            size="large"
            isGold={getTileType(discardedTile) === goldTileType}
            disabled
          />
        </div>

        <div className="grid grid-cols-2 gap-3 mb-4">
          {['win', 'pung', 'chow', 'pass'].map(call => {
            const isValid = validCalls.includes(call);
            const { text, color } = callLabels[call];

            return (
              <button
                key={call}
                className={`
                  py-3 px-4 rounded-lg text-white font-medium
                  transition-all
                  ${isValid ? color : 'bg-gray-300 cursor-not-allowed'}
                `}
                onClick={() => isValid && onCall(call)}
                disabled={!isValid}
              >
                {text}
              </button>
            );
          })}
        </div>

        <p className="text-center text-sm text-gray-500">
          Waiting for {waitingFor} player(s)...
        </p>
      </div>
    </div>
  );
}
```

## Win/End Screens

### Win Screen

```jsx
function WinScreen({ winner, scoreBreakdown, isThreeGolds, onPlayAgain }) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl p-8 shadow-2xl max-w-lg w-full mx-4">
        {isThreeGolds && (
          <div className="text-center mb-4">
            <span className="text-4xl">🏆</span>
            <h2 className="text-2xl font-bold text-yellow-600">Three Golds!</h2>
          </div>
        )}

        <h2 className="text-xl font-bold text-center mb-6">
          {winner.name} Wins!
        </h2>

        <div className="bg-gray-50 rounded-lg p-4 mb-6">
          <h3 className="font-medium mb-3">Score Breakdown</h3>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span>Base</span>
              <span>+1</span>
            </div>
            {scoreBreakdown.bonusTiles > 0 && (
              <div className="flex justify-between">
                <span>Bonus Tiles ({scoreBreakdown.bonusTileCount})</span>
                <span>+{scoreBreakdown.bonusTiles}</span>
              </div>
            )}
            {scoreBreakdown.golds > 0 && (
              <div className="flex justify-between">
                <span>Gold Tiles ({scoreBreakdown.goldCount})</span>
                <span>+{scoreBreakdown.golds}</span>
              </div>
            )}
            <div className="border-t pt-2 flex justify-between">
              <span>Subtotal</span>
              <span>{scoreBreakdown.subtotal}</span>
            </div>
            {scoreBreakdown.isSelfDraw && (
              <div className="flex justify-between text-blue-600">
                <span>Self-Draw (×2)</span>
                <span>×2</span>
              </div>
            )}
            {isThreeGolds && (
              <div className="flex justify-between text-yellow-600">
                <span>Three Golds Bonus</span>
                <span>+20</span>
              </div>
            )}
            <div className="border-t pt-2 flex justify-between font-bold text-lg">
              <span>Total</span>
              <span>{scoreBreakdown.total}</span>
            </div>
          </div>
        </div>

        <div className="text-center text-sm text-gray-600 mb-6">
          Each loser pays {scoreBreakdown.total} points
        </div>

        <button
          className="w-full py-3 bg-blue-500 text-white rounded-lg font-medium hover:bg-blue-600"
          onClick={onPlayAgain}
        >
          Play Again
        </button>
      </div>
    </div>
  );
}
```

### Draw Screen

```jsx
function DrawScreen({ onPlayAgain }) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl p-8 shadow-2xl max-w-md w-full mx-4 text-center">
        <span className="text-4xl mb-4 block">🤝</span>
        <h2 className="text-xl font-bold mb-2">Draw Game</h2>
        <p className="text-gray-600 mb-6">The wall is exhausted. No winner this round.</p>

        <button
          className="w-full py-3 bg-blue-500 text-white rounded-lg font-medium hover:bg-blue-600"
          onClick={onPlayAgain}
        >
          Play Again
        </button>
      </div>
    </div>
  );
}
```

## Room/Lobby Components

### Room Code Display

```jsx
function RoomCodeDisplay({ code }) {
  const [copied, setCopied] = useState(false);

  const copyCode = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="flex items-center gap-2">
      <span className="text-sm text-gray-500">Room:</span>
      <code className="font-mono text-lg font-bold tracking-wider">{code}</code>
      <button
        onClick={copyCode}
        className="p-1 hover:bg-gray-100 rounded"
      >
        {copied ? '✓' : '📋'}
      </button>
    </div>
  );
}
```

### Player Slots

```jsx
function PlayerSlots({ players, currentUserId, onSelectDealer, selectedDealer, isHost }) {
  return (
    <div className="grid grid-cols-2 gap-4">
      {[0, 1, 2, 3].map(seat => {
        const player = players[`seat${seat}`];
        const isMe = player?.id === currentUserId;
        const isDealer = selectedDealer === seat;

        return (
          <div
            key={seat}
            className={`
              p-4 rounded-lg border-2
              ${player ? 'bg-white border-gray-200' : 'bg-gray-50 border-dashed border-gray-300'}
              ${isMe ? 'ring-2 ring-blue-500' : ''}
            `}
          >
            {player ? (
              <div className="flex items-center justify-between">
                <div>
                  <span className="font-medium">{player.name}</span>
                  {isMe && <span className="text-xs text-blue-500 ml-1">(You)</span>}
                </div>
                {isHost && (
                  <button
                    onClick={() => onSelectDealer(seat)}
                    className={`
                      px-2 py-1 text-xs rounded
                      ${isDealer
                        ? 'bg-yellow-400 text-yellow-900'
                        : 'bg-gray-200 hover:bg-gray-300'}
                    `}
                  >
                    {isDealer ? '庄 Dealer' : 'Set Dealer'}
                  </button>
                )}
                {!isHost && isDealer && (
                  <span className="px-2 py-1 text-xs bg-yellow-400 text-yellow-900 rounded">
                    庄 Dealer
                  </span>
                )}
              </div>
            ) : (
              <span className="text-gray-400">Waiting for player...</span>
            )}
          </div>
        );
      })}
    </div>
  );
}
```

## Utility Functions

```javascript
function getTileType(tileId) {
  // "dots_5_2" -> "dots_5"
  // "wind_east_0" -> "wind_east"
  // "dragon_red_0" -> "dragon_red"
  const parts = tileId.split('_');
  if (parts[0] === 'wind' || parts[0] === 'dragon') {
    return `${parts[0]}_${parts[1]}`;
  }
  return `${parts[0]}_${parts[1]}`;
}

function parseTileType(tileType) {
  // "dots_5" -> ["dots", 5]
  // "wind_east" -> ["wind", "east"]
  const parts = tileType.split('_');
  const value = parseInt(parts[1]) || parts[1];
  return [parts[0], value];
}

function sortTiles(tiles, goldTileType) {
  const order = { dots: 0, bamboo: 1, characters: 2, wind: 3, dragon: 4 };
  const windOrder = { east: 0, south: 1, west: 2, north: 3 };

  return [...tiles].sort((a, b) => {
    const [catA, valA] = parseTileType(getTileType(a));
    const [catB, valB] = parseTileType(getTileType(b));

    // Gold tiles first
    const aIsGold = getTileType(a) === goldTileType;
    const bIsGold = getTileType(b) === goldTileType;
    if (aIsGold && !bIsGold) return -1;
    if (!aIsGold && bIsGold) return 1;

    // Then by category
    if (order[catA] !== order[catB]) {
      return order[catA] - order[catB];
    }

    // Then by value
    if (catA === 'wind') {
      return windOrder[valA] - windOrder[valB];
    }
    return valA - valB;
  });
}
```

## Styling Notes

- Use Tailwind CSS for rapid development
- Gold tiles should have yellow highlight/ring
- Current player should have visual indicator
- Invalid buttons greyed out but visible
- Responsive design for different screen sizes
- Consider color-blind friendly palette for suits
