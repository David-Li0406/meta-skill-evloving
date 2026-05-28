# Game Programming Patterns Reference

Advanced patterns for building production-quality game systems.

## Finite State Machines (FSM)

```typescript
type GamePhase = 'morning' | 'action' | 'resolution' | 'night';

class GamePhaseMachine {
  private phase: GamePhase = 'morning';
  private transitions: Record<GamePhase, GamePhase> = {
    morning: 'action',
    action: 'resolution',
    resolution: 'night',
    night: 'morning',
  };
  
  transition(): void {
    this.phase = this.transitions[this.phase];
    this.onPhaseEnter(this.phase);
  }
  
  private onPhaseEnter(phase: GamePhase): void {
    // Phase-specific initialization
  }
}
```

## Command Pattern (Undo/Redo)

```typescript
interface Command {
  execute(): void;
  undo(): void;
}

class CommandHistory {
  private history: Command[] = [];
  private pointer = -1;
  
  execute(command: Command): void {
    this.history = this.history.slice(0, this.pointer + 1);
    command.execute();
    this.history.push(command);
    this.pointer++;
  }
  
  undo(): void {
    if (this.pointer >= 0) {
      this.history[this.pointer--].undo();
    }
  }
}
```

## Observer Pattern (Event Bus)

```typescript
type GameEvent = 
  | { type: 'POT_THRESHOLD_REACHED'; potId: string }
  | { type: 'TRIGGER_EARNED'; trigger: TriggerType }
  | { type: 'DAY_COMPLETED'; dayNumber: number };

class GameEventBus {
  private handlers = new Map<string, Set<Function>>();
  
  on(type: string, handler: Function): () => void {
    if (!this.handlers.has(type)) this.handlers.set(type, new Set());
    this.handlers.get(type)!.add(handler);
    return () => this.handlers.get(type)?.delete(handler);
  }
  
  emit(event: GameEvent): void {
    this.handlers.get(event.type)?.forEach(h => h(event));
  }
}
```

## Object Pool (Performance)

```typescript
class ObjectPool<T> {
  private pool: T[] = [];
  private activeCount = 0;
  
  constructor(private factory: () => T, private reset: (obj: T) => void, size = 10) {
    for (let i = 0; i < size; i++) this.pool.push(factory());
  }
  
  acquire(): T {
    if (this.activeCount >= this.pool.length) this.pool.push(this.factory());
    return this.pool[this.activeCount++];
  }
  
  release(obj: T): void {
    const index = this.pool.indexOf(obj);
    if (index !== -1 && index < this.activeCount) {
      this.reset(obj);
      [this.pool[index], this.pool[--this.activeCount]] = [this.pool[this.activeCount], this.pool[index]];
    }
  }
}
```

## Strategy Pattern

```typescript
interface ScoringStrategy {
  calculateScore(results: DayResults): number;
}

class StandardScoring implements ScoringStrategy {
  calculateScore(results: DayResults): number {
    return results.potsWon * 100 + results.troubleCleared * 50;
  }
}

class HarvestPhaseScoring implements ScoringStrategy {
  calculateScore(results: DayResults): number {
    return (results.potsWon * 100 + results.troubleCleared * 50) * 3;
  }
}
```

---

*Game Patterns Reference - Game Engineering Team*
