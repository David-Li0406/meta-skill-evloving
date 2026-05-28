---
name: React Patterns
description: Modern React patterns, hooks, and state management for the poker platform
---

# React Patterns Skill

## Overview
Modern React patterns optimized for real-time poker applications with performant rendering.

## Component Patterns

### 1. Compound Components
```jsx
// Flexible, composable API
<PokerTable>
  <PokerTable.Felt />
  <PokerTable.Seats>
    {players.map(p => <PokerTable.Seat key={p.id} player={p} />)}
  </PokerTable.Seats>
  <PokerTable.Board cards={communityCards} />
  <PokerTable.Pot amount={pot} />
  <PokerTable.Actions onAction={handleAction} />
</PokerTable>
```

### 2. Render Props
```jsx
<GameState>
  {({ state, dispatch, isLoading }) => (
    isLoading ? <LoadingSpinner /> : <GameBoard state={state} />
  )}
</GameState>
```

### 3. Custom Hooks
```javascript
// useGameState.js
function useGameState(tableId) {
  const [state, setState] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  
  useEffect(() => {
    const channel = supabase.channel(`table:${tableId}`)
      .on('broadcast', { event: 'state' }, ({ payload }) => {
        setState(payload);
      })
      .subscribe((status) => {
        setIsConnected(status === 'SUBSCRIBED');
      });
    
    return () => channel.unsubscribe();
  }, [tableId]);
  
  return { state, isConnected };
}
```

## State Management

### Context + Reducer Pattern
```javascript
// GameContext.js
const GameContext = createContext();

const gameReducer = (state, action) => {
  switch (action.type) {
    case 'DEAL_CARDS':
      return { ...state, phase: 'dealing', cards: action.cards };
    case 'PLAYER_ACTION':
      return { ...state, lastAction: action.payload };
    case 'NEXT_STREET':
      return { ...state, street: action.street, board: [...state.board, ...action.cards] };
    case 'SHOWDOWN':
      return { ...state, phase: 'showdown', winners: action.winners };
    default:
      return state;
  }
};

export function GameProvider({ children, tableId }) {
  const [state, dispatch] = useReducer(gameReducer, initialState);
  
  return (
    <GameContext.Provider value={{ state, dispatch }}>
      {children}
    </GameContext.Provider>
  );
}

export const useGame = () => useContext(GameContext);
```

### Zustand (Lightweight Alternative)
```javascript
import { create } from 'zustand';

const usePokerStore = create((set, get) => ({
  // State
  players: [],
  pot: 0,
  communityCards: [],
  currentTurn: null,
  
  // Actions
  setPlayers: (players) => set({ players }),
  addToPot: (amount) => set((s) => ({ pot: s.pot + amount })),
  dealCommunityCard: (card) => set((s) => ({ 
    communityCards: [...s.communityCards, card] 
  })),
  nextTurn: () => {
    const { players, currentTurn } = get();
    const nextIndex = (players.findIndex(p => p.id === currentTurn) + 1) % players.length;
    set({ currentTurn: players[nextIndex].id });
  }
}));
```

## Performance Patterns

### React.memo for Pure Components
```jsx
const PlayerCard = React.memo(function PlayerCard({ player, isActive }) {
  return (
    <div className={`player-card ${isActive ? 'active' : ''}`}>
      <img src={player.avatar} alt={player.name} />
      <span>{player.name}</span>
      <span className="stack">${player.stack}</span>
    </div>
  );
});
```

### useMemo for Expensive Calculations
```jsx
const rangeGrid = useMemo(() => {
  return calculateRangeGrid(selectedHands, position);
}, [selectedHands, position]);
```

### useCallback for Stable References
```jsx
const handleAction = useCallback((action, amount) => {
  dispatch({ type: 'PLAYER_ACTION', payload: { action, amount } });
  broadcastAction(tableId, action, amount);
}, [tableId, dispatch]);
```

### Virtualization for Long Lists
```jsx
import { FixedSizeList } from 'react-window';

function HandHistory({ hands }) {
  return (
    <FixedSizeList
      height={400}
      width="100%"
      itemCount={hands.length}
      itemSize={60}
    >
      {({ index, style }) => (
        <div style={style}>
          <HandHistoryRow hand={hands[index]} />
        </div>
      )}
    </FixedSizeList>
  );
}
```

## Animation Integration

### Framer Motion HOC
```jsx
import { motion, AnimatePresence } from 'framer-motion';

function AnimatedCard({ card, isVisible }) {
  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          initial={{ scale: 0, rotateY: 180 }}
          animate={{ scale: 1, rotateY: 0 }}
          exit={{ scale: 0, opacity: 0 }}
          transition={{ duration: 0.3 }}
        >
          <Card value={card} />
        </motion.div>
      )}
    </AnimatePresence>
  );
}
```

## Error Boundaries
```jsx
class GameErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Game error:', error, errorInfo);
    // Log to monitoring service
  }

  render() {
    if (this.state.hasError) {
      return <GameErrorFallback onRetry={() => this.setState({ hasError: false })} />;
    }
    return this.props.children;
  }
}
```

## File Structure
```
src/
├── components/
│   ├── poker/           # Poker-specific components
│   │   ├── PokerTable/
│   │   ├── Card/
│   │   ├── Chip/
│   │   └── ActionButtons/
│   └── shared/          # Reusable UI components
├── hooks/               # Custom hooks
│   ├── useGameState.js
│   ├── useTimer.js
│   └── useSound.js
├── context/             # React contexts
├── store/               # Zustand stores
└── utils/               # Helper functions
```
