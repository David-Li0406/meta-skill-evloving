---
name: client-prediction
description: Client-side prediction and server reconciliation for responsive multiplayer controls
category: architectural
depends-on: [backend-multiplayer]
---

# Client-Side Prediction Skill

> "Client prediction makes multiplayer feel responsive. Server reconciliation keeps it honest."

## When to Use This Skill

Use for **EVERY server-authoritative gameplay feature** that needs responsive feel:
- Movement (WASD, jump, sprint)
- Shooting (aim, fire, ammo)
- Interactions (vault, mantle, crouch)

## Critical Architecture Pattern

```
┌─────────────────────────────────────────────────────────────────┐
│                    CLIENT PREDICTION FLOW                       │
│                                                                  │
│  INPUT                                                           │
│    │                                                             │
│    ├───► LOCAL PREDICTION (immediate visual feedback)            │
│    │      │                                                       │
│    │      └───► Display updates instantly (feels responsive)     │
│    │                                                             │
│    └───► SEND TO SERVER (validation)                            │
│           │                                                       │
│           │    NETWORK LATENCY (~100ms)                          │
│           │                                                       │
│           ▼                                                       │
│        SERVER PROCESSES                                          │
│           │                                                       │
│           └───► SERVER STATE (authoritative)                     │
│                  │                                                │
│                  │    NETWORK LATENCY                            │
│                  │                                                │
│                  ▼                                                │
│             CLIENT RECONCILES                                     │
│                  │                                                │
│                  ├───► Discard confirmed inputs                   │
│                  ├───► Re-apply pending inputs                    │
│                  └───► Smooth correction                         │
│                                                                  │
│  Result: Responsive feel + cheat prevention                      │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Start: Movement with Prediction

### Client Side (PlayerController.tsx)

```typescript
// src/components/game/player/PlayerController.tsx
import { useRef, useEffect } from '@react-three/fiber';
import { useNetworkManager } from '../../services/NetworkManager';

interface PendingInput {
  input: PlayerInput;
  sequence: number;
  timestamp: number;
}

export function PlayerController() {
  const networkManager = useNetworkManager();
  const meshRef = useRef<RapierRigidBody>(null);

  // Prediction state
  const localStateRef = useRef({
    position: { x: 0, y: 0, z: 0 },
    velocity: { x: 0, y: 0, z: 0 },
    rotation: 0,
  });

  const pendingInputsRef = useRef<PendingInput[]>([]);
  const inputSequenceRef = useRef(0);

  // Server state (for reconciliation)
  const serverStateRef = useRef({
    position: { x: 0, y: 0, z: 0 },
    lastProcessedSequence: 0,
  });

  // Listen for server state updates
  useEffect(() => {
    const unsubscribe = networkManager.onStateChange((serverState) => {
      const localPlayer = serverState.players.get(networkManager.sessionId);
      if (localPlayer) {
        reconcileWithServer(localPlayer);
      }
    });

    return unsubscribe;
  }, [networkManager]);

  // Reconcile local prediction with server state
  function reconcileWithServer(serverPlayer: any) {
    const serverState = serverStateRef.current;
    const localState = localStateRef.current;

    // Remove inputs that server has processed
    pendingInputsRef.current = pendingInputsRef.current.filter(
      p => p.sequence > serverPlayer.lastProcessedSequence
    );

    // Start from server position (authoritative)
    let reconciledPosition = { ...serverPlayer.position };

    // Re-apply all pending inputs
    for (const pending of pendingInputsRef.current) {
      reconciledPosition = applyInput(
        reconciledPosition,
        pending.input,
        0.016 // Assume ~60fps for prediction
      );
    }

    // Smoothly interpolate display to reconciled position
    const smoothingFactor = 0.3;
    localState.position.x = lerp(
      localState.position.x,
      reconciledPosition.x,
      smoothingFactor
    );
    localState.position.y = lerp(
      localState.position.y,
      reconciledPosition.y,
      smoothingFactor
    );
    localState.position.z = lerp(
      localState.position.z,
      reconciledPosition.z,
      smoothingFactor
    );
  }

  // Apply input to position (local prediction)
  function applyInput(position: Vector3, input: PlayerInput, dt: number): Vector3 {
    const speed = 10; // m/s
    const result = { ...position };

    if (input.forward) result.z -= speed * dt;
    if (input.backward) result.z += speed * dt;
    if (input.left) result.x -= speed * dt;
    if (input.right) result.x += speed * dt;

    return result;
  }

  // Handle input frame update
  useFrame((state, dt) => {
    const input = getCurrentInput();

    if (hasInput(input)) {
      // 1. Store for prediction
      const sequence = ++inputSequenceRef.current;
      pendingInputsRef.current.push({
        input,
        sequence,
        timestamp: Date.now(),
      });

      // 2. Apply locally (immediate feedback)
      const predictedPosition = applyInput(localStateRef.current.position, input, dt);
      localStateRef.current.position = predictedPosition;

      // Update display immediately
      if (meshRef.current) {
        meshRef.current.setTranslation(predictedPosition);
      }

      // 3. Send to server (for validation)
      networkManager.send({
        type: 'player_input',
        input,
        sequence,
      });
    }
  });

  return (
    <RigidBody ref={meshRef} colliders="ball" type="kinematicPosition">
      <mesh>
        <sphereGeometry args={[0.5]} />
        <meshStandardMaterial color="orange" />
      </mesh>
    </RigidBody>
  );
}
```

### Server Side (GameRoom.ts)

```typescript
// server/rooms/GameRoom.ts
import { Room, Client } from "colyseus";
import { Schema, type } from "@colyseus/schema";

class PlayerState extends Schema {
  @type("number") x = 0;
  @type("number") y = 0;
  @type("number") z = 0;
  @type("number") rotation = 0;
  @type("number") lastProcessedSequence = 0; // For reconciliation
}

export class GameRoom extends Room<GameRoomState> {
  private inputBuffers: Map<string, PlayerInput[]> = new Map();

  onCreate() {
    this.setState(new GameRoomState());
    this.setSimulationInterval((dt) => this.update(dt));
  }

  onJoin(client: Client) {
    const player = new PlayerState();
    player.x = 0;
    player.z = 0;
    this.state.players.set(client.sessionId, player);
    this.inputBuffers.set(client.sessionId, []);
  }

  onMessage(client: Client, data: any) {
    if (data.type === 'player_input') {
      const player = this.state.players.get(client.sessionId);
      if (!player) return;

      // Store input with sequence number
      this.inputBuffers.get(client.sessionId)?.push({
        ...data.input,
        sequence: data.sequence,
      });

      // Track last processed sequence for reconciliation
      player.lastProcessedSequence = data.sequence;
    }
  }

  update(dt: number) {
    const deltaTime = dt / 1000;

    for (const [sessionId, player] of this.state.players) {
      const inputs = this.inputBuffers.get(sessionId) || [];

      // Process all pending inputs
      for (const input of inputs) {
        this.processPlayerInput(player, input, deltaTime);
      }

      // Clear processed inputs
      this.inputBuffers.set(sessionId, []);
    }
  }

  processPlayerInput(player: PlayerState, input: PlayerInput, dt: number) {
    const speed = 10; // Must match client!

    // Apply movement SERVER-SIDE
    if (input.forward) player.z -= speed * dt;
    if (input.backward) player.z += speed * dt;
    if (input.left) player.x -= speed * dt;
    if (input.right) player.x += speed * dt;

    // Validate bounds (anti-cheat)
    player.x = Math.max(-50, Math.min(50, player.x));
    player.z = Math.max(-50, Math.min(50, player.z));

    // Server state automatically syncs to clients via Colyseus
  }
}
```

## Shooting Prediction with Rollback

### Client Side (PaintGun.tsx)

```typescript
// src/components/game/weapons/PaintGun.tsx
interface PendingShot {
  id: string;
  direction: Vector3;
  timestamp: number;
  sequence: number;
}

export function PaintGun() {
  const networkManager = useNetworkManager();
  const pendingShotsRef = useRef<PendingShot[]>([]);

  // Optimistic shooting
  function shoot(direction: Vector3) {
    const shotId = `${Date.now()}-${Math.random()}`;
    const sequence = ++shotSequenceRef.current;

    // 1. Spawn paint immediately (optimistic)
    spawnOptimisticDecal(shotId, direction);

    // 2. Store for rollback
    pendingShotsRef.current.push({
      id: shotId,
      direction,
      timestamp: Date.now(),
      sequence,
    });

    // 3. Send to server
    networkManager.send({
      type: 'paint_fire',
      direction,
      sequence,
    });
  }

  // Listen for server confirmation/rollback
  useEffect(() => {
    const unsubscribe = networkManager.onMessage('paint_result', (result) => {
      handlePaintResult(result);
    });
    return unsubscribe;
  }, []);

  function handlePaintResult(result: PaintResult) {
    const pendingIndex = pendingShotsRef.current.findIndex(
      s => s.sequence === result.sequence
    );

    if (pendingIndex === -1) return;

    const pending = pendingShotsRef.current[pendingIndex];

    if (result.confirmed) {
      // Server confirmed - mark optimistic decal as permanent
      confirmDecal(pending.id);
    } else {
      // Server rejected - rollback (remove optimistic decal)
      rollbackDecal(pending.id);
    }

    pendingShotsRef.current.splice(pendingIndex, 1);
  }

  function spawnOptimisticDecal(id: string, direction: Vector3) {
    // Create temporary decal with "optimistic" flag
    decalManager.spawn({
      id,
      position: calculateImpact(direction),
      team: localTeam,
      optimistic: true, // Mark for potential rollback
    });
  }

  function rollbackDecal(id: string) {
    decalManager.remove(id);
  }

  function confirmDecal(id: string) {
    decalManager.markPermanent(id);
  }
}
```

### Server Side (ProjectileSystem.ts)

```typescript
// server/systems/ProjectileSystem.ts
export class ProjectileSystem {
  private projectiles: PaintProjectile[] = [];

  processFireMessage(client: Client, data: FireMessage) {
    const player = this.room.state.players.get(client.sessionId);
    if (!player) return;

    // Validate ammo
    if (player.ink <= 0) {
      this.sendReject(client, data.sequence, 'no_ink');
      return;
    }

    // Validate fire rate
    const now = Date.now();
    if (now - player.lastShotTime < 100) {
      this.sendReject(client, data.sequence, 'cooldown');
      return;
    }

    // Validate aim direction
    const aimLength = Math.sqrt(
      data.direction.x ** 2 +
      data.direction.y ** 2 +
      data.direction.z ** 2
    );
    if (aimLength > 1.1) {
      this.sendReject(client, data.sequence, 'invalid_aim');
      return;
    }

    // Create projectile SERVER-SIDE
    const projectile: PaintProjectile = {
      id: `proj-${client.sessionId}-${data.sequence}`,
      x: player.x,
      y: player.y + 1.5,
      z: player.z,
      dx: data.direction.x * 25, // 25 m/s
      dy: data.direction.y * 25,
      dz: data.direction.z * 25,
      owner: client.sessionId,
      team: player.team,
      sequence: data.sequence,
    };

    this.projectiles.push(projectile);
    player.ink -= 1;
    player.lastShotTime = now;

    // Notify client that shot was accepted
    this.sendConfirm(client, data.sequence);
  }

  update(dt: number) {
    const deltaTime = dt / 1000;

    for (let i = this.projectiles.length - 1; i >= 0; i--) {
      const proj = this.projectiles[i];

      // Move projectile
      proj.x += proj.dx * deltaTime;
      proj.y += proj.dy * deltaTime;
      proj.z += proj.dz * deltaTime;

      // Apply gravity
      proj.dy -= 9.8 * deltaTime;

      // Check collision
      if (this.checkCollision(proj)) {
        this.spawnPaintDecal(proj);
        this.broadcastPaintEvent(proj);
        this.projectiles.splice(i, 1);
      } else if (proj.y < 0) {
        // Below ground
        this.projectiles.splice(i, 1);
      }
    }
  }

  sendConfirm(client: Client, sequence: number) {
    client.send({
      type: 'paint_result',
      sequence,
      confirmed: true,
    });
  }

  sendReject(client: Client, sequence: number, reason: string) {
    client.send({
      type: 'paint_result',
      sequence,
      confirmed: false,
      reason,
    });
  }
}
```

## Reconciliation Smoothing

```typescript
// Smooth correction without "snapping"
function reconcilePosition(
  displayPosition: Vector3,
  serverPosition: Vector3,
  pendingInputs: PendingInput[]
): Vector3 {
  // Calculate reconciled position
  let reconciled = { ...serverPosition };

  for (const input of pendingInputs) {
    reconciled = applyInput(reconciled, input.input, 0.016);
  }

  // Smooth interpolation (not instant snap)
  const t = 0.2; // 20% correction per frame
  return {
    x: lerp(displayPosition.x, reconciled.x, t),
    y: lerp(displayPosition.y, reconciled.y, t),
    z: lerp(displayPosition.z, reconciled.z, t),
  };
}
```

## Testing Checklist

For each predicted feature:

- [ ] Input feels immediate (no perceived lag)
- [ ] Server rejection causes rollback
- [ ] Rollback is smooth (not jarring)
- [ ] Reconciliation completes within 200ms
- [ ] Multiple clients see same result
- [ ] No "rubber banding" under normal latency
- [ ] High latency (200ms+) still playable

## Common Mistakes

| ❌ Wrong | ✅ Right |
|----------|----------|
| No prediction, send input only | Predict locally, then send input |
| No reconciliation, just snap | Smooth interpolation to server state |
| Apply server state directly | Re-apply pending inputs first |
| Remove all optimistic effects | Only remove rejected effects |
| Fixed smoothing factor | Dynamic smoothing based on distance |

## Debugging Tips

```typescript
// Visualize prediction error
function drawPredictionDebug() {
  const serverPos = serverStateRef.current.position;
  const localPos = localStateRef.current.position;
  const error = Math.sqrt(
    (serverPos.x - localPos.x) ** 2 +
    (serverPos.y - localPos.y) ** 2 +
    (serverPos.z - localPos.z) ** 2
  );

  // Draw line from predicted to actual
  if (error > 0.5) {
    drawDebugLine(localPos, serverPos, 'red');
  }

  console.log(`Prediction error: ${error.toFixed(2)}m`);
}
```

## Performance Notes

- Limit pending inputs to ~100 entries
- Clean up old pending inputs (> 1 second)
- Use object pooling for input objects
- Batch reconciliation updates (not every frame)

## Reference

- [agents/developer/skills/backend-multiplayer.md](./backend-multiplayer.md) — Server-authoritative architecture
- [Valve Latency Compensation](https://developer.valvesoftware.com/wiki/Latency_Compensating_Methods_in_Client/Server_In-game_Protocol_Design_and_Optimization) — Original prediction patterns
- [Gaffer On Games - Networking](https://gafferongames.com/post/what_every_programmer_needs_to_know_about_game_networking/) — Game networking fundamentals
- [Colyseus Schema Documentation](https://docs.colyseus.io/colyseus/server/schema/) — State serialization
