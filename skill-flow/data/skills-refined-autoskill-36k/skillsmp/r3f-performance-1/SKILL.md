---
name: r3f-performance
description: Performance optimization techniques for R3F and Three.js
category: optimization
depends-on: [r3f-fundamentals]
---

# R3F Performance Skill

> "Optimize for mobile, scale up for desktop – 60 FPS is the goal."

## When to Use This Skill

Use when:

- FPS drops below 60
- Targeting mobile devices
- Rendering many objects
- Implementing LOD systems
- Debugging performance issues

## Quick Start

```tsx
// Performance-optimized Canvas
<Canvas
  dpr={[1, 2]} // Limit pixel ratio
  performance={{ min: 0.5 }} // Auto-reduce quality
  gl={{ antialias: false }} // Disable for mobile
>
  <Suspense fallback={null}>
    <Scene />
  </Suspense>
</Canvas>
```

## The 16ms Budget (60 FPS)

| System     | Budget      | Notes                 |
| ---------- | ----------- | --------------------- |
| Input      | ~1ms        | Event handling        |
| Physics    | ~3ms        | Rapier/Cannon updates |
| Game Logic | ~4ms        | State, AI, animations |
| Render     | ~5ms        | Three.js draw calls   |
| Buffer     | ~3ms        | Safety margin         |
| **Total**  | **16.67ms** | 60 FPS target         |

## Decision Framework

| Symptom            | Likely Cause        | Solution            |
| ------------------ | ------------------- | ------------------- |
| Low FPS everywhere | Too many draw calls | Instancing, merging |
| FPS drops on zoom  | LOD not implemented | Add LOD system      |
| Mobile slow        | DPR too high        | Limit to 1.5        |
| Memory grows       | Dispose missing     | Add cleanup         |
| Stuttering         | GC pressure         | Object pooling      |

## Progressive Guide

### Level 1: Basic Optimizations

```tsx
// Limit device pixel ratio
<Canvas dpr={Math.min(window.devicePixelRatio, 2)}>

// Disable expensive features on mobile
const isMobile = /iPhone|iPad|Android/i.test(navigator.userAgent);

<Canvas
  shadows={!isMobile}
  gl={{
    antialias: !isMobile,
    powerPreference: 'high-performance',
  }}
>
```

### Level 2: Instanced Rendering

```tsx
import { Instances, Instance } from '@react-three/drei';

// Instead of 1000 separate meshes
function OptimizedTrees({ positions }) {
  return (
    <Instances limit={positions.length}>
      <cylinderGeometry args={[0.1, 0.3, 2]} />
      <meshStandardMaterial color="brown" />
      {positions.map((pos, i) => (
        <Instance key={i} position={pos} />
      ))}
    </Instances>
  );
}
```

### Level 3: Level of Detail (LOD)

```tsx
import { Detailed } from '@react-three/drei';

function LODTree({ position }) {
  return (
    <Detailed distances={[0, 20, 50, 100]} position={position}>
      {/* Closest - high detail */}
      <HighDetailTree />
      {/* Medium distance */}
      <MediumDetailTree />
      {/* Far - low detail */}
      <LowDetailTree />
      {/* Very far - billboard or nothing */}
      <mesh>
        <planeGeometry args={[1, 2]} />
        <meshBasicMaterial map={treeBillboard} transparent />
      </mesh>
    </Detailed>
  );
}
```

### Level 4: Frustum Culling & BVH

```tsx
import { useBVH } from '@react-three/drei';

function OptimizedMesh() {
  const meshRef = useRef();

  // Enable BVH for faster raycasting
  useBVH(meshRef);

  return (
    <mesh ref={meshRef} frustumCulled>
      <complexGeometry />
      <meshStandardMaterial />
    </mesh>
  );
}
```

### Level 5: Object Pooling

```tsx
// Pool for frequently created/destroyed objects
const bulletPool = useMemo(() => {
  const pool = [];
  for (let i = 0; i < 100; i++) {
    pool.push({
      active: false,
      position: new THREE.Vector3(),
      velocity: new THREE.Vector3(),
    });
  }
  return pool;
}, []);

function getBullet() {
  return bulletPool.find((b) => !b.active);
}

function releaseBullet(bullet) {
  bullet.active = false;
}
```

## Mobile Optimization

| Feature         | Desktop | Mobile  |
| --------------- | ------- | ------- |
| Pixel Ratio     | 2.0     | 1.0-1.5 |
| Shadows         | On      | Off     |
| Anti-aliasing   | MSAA    | Off     |
| Post-processing | Full    | Minimal |
| Draw calls      | < 200   | < 50    |
| Polygons        | < 1M    | < 100K  |

```tsx
// Mobile detection and config
const config = useMemo(() => {
  const isMobile = /iPhone|iPad|Android/i.test(navigator.userAgent);
  return {
    dpr: isMobile ? 1 : Math.min(window.devicePixelRatio, 2),
    shadows: !isMobile,
    antialias: !isMobile,
    maxDrawCalls: isMobile ? 50 : 200,
  };
}, []);
```

## Memory Management

```tsx
// CRITICAL: Dispose of Three.js objects
useEffect(() => {
  const geometry = new THREE.BoxGeometry();
  const material = new THREE.MeshStandardMaterial();

  return () => {
    geometry.dispose();
    material.dispose();
    // Also dispose textures
    if (material.map) material.map.dispose();
  };
}, []);
```

## Anti-Patterns

❌ **DON'T:**

- Create objects inside useFrame
- Use high polygon models without LOD
- Skip dispose() calls
- Use shadows on mobile without testing
- Render invisible objects
- Use uncompressed textures

✅ **DO:**

- Reuse Vector3, Quaternion instances
- Implement LOD for complex scenes
- Always dispose geometries and materials
- Profile before and after optimizations
- Use Instances for repeated objects
- Compress textures (WebP, Basis)

## Performance Monitoring

```tsx
import { useFrame } from '@react-three/fiber';
import { useRef } from 'react';

function PerformanceMonitor() {
  const frameCount = useRef(0);
  const lastTime = useRef(performance.now());

  useFrame(() => {
    frameCount.current++;

    const now = performance.now();
    if (now - lastTime.current >= 1000) {
      console.log(`FPS: ${frameCount.current}`);
      frameCount.current = 0;
      lastTime.current = now;
    }
  });

  return null;
}
```

## Checklist

Performance review:

- [ ] DPR limited appropriately
- [ ] Instancing used for repeated objects
- [ ] LOD implemented for complex models
- [ ] Dispose called on cleanup
- [ ] No object creation in useFrame
- [ ] Shadows disabled on mobile
- [ ] Textures compressed
- [ ] Draw calls under budget
- [ ] FPS stable at 60

## Common Performance Killers

1. **Too many draw calls** → Use Instances
2. **High polygon count** → Use LOD
3. **Unoptimized textures** → Compress, resize
4. **No frustum culling** → Enable frustumCulled
5. **Memory leaks** → Call dispose()
6. **GC pressure** → Object pooling
7. **Expensive shaders** → Simplify, use mobile variants
8. **Post-processing** → Limit on mobile

## Client-Side Prediction for Multiplayer

> "Client-side prediction hides network latency by simulating actions locally before server confirmation."

### When to Use

Use client-side prediction when:
- Building multiplayer games with Colyseus/Socket.io
- Network latency causes noticeable input delay (>50ms)
- Players need instant feedback on movement/actions
- Fast-paced gameplay (shooters, platformers, action games)

### Core Concept

```
1. Player presses W key
2. Client immediately updates local position (prediction)
3. Client sends input to server
4. Server processes and sends back authoritative state
5. Client reconciles if server state differs (correction)
```

### Basic Prediction Pattern

```tsx
import { useFrame } from '@react-three/fiber';
import { useRef, useState } from 'react';
import * as THREE from 'three';

interface PredictedState {
  position: THREE.Vector3;
  rotation: THREE.Quaternion;
  sequence: number; // For ordering
}

function PlayerWithPrediction() {
  const meshRef = useRef<THREE.Mesh>(null);
  const [serverState, setServerState] = useState<PredictedState | null>(null);
  const pendingInputs = useRef<Array<{ input: PlayerInput; sequence: number }>>([]);
  const currentSequence = useRef(0);

  // Local physics update (runs every frame)
  useFrame((_, delta) => {
    if (!meshRef.current) return;

    // Apply local physics for instant feedback
    const input = getCurrentInput(); // From keyboard/mouse state
    const state = applyPhysics(meshRef.current, input, delta);

    // Send input to server (throttled)
    if (shouldSendInput()) {
      currentSequence.current++;
      pendingInputs.current.push({
        input: { ...input },
        sequence: currentSequence.current,
      });
      networkManager.send({
        type: 'player_input',
        input,
        sequence: currentSequence.current,
      });
    }
  });

  // Server reconciliation (when server update arrives)
  useEffect(() => {
    if (!serverState || !meshRef.current) return;

    // Remove confirmed inputs from pending
    pendingInputs.current = pendingInputs.current.filter(
      (p) => p.sequence > serverState.sequence
    );

    // Start from server position
    let reconciledPosition = serverState.position.clone();
    let reconciledRotation = serverState.rotation.clone();

    // Re-apply all pending inputs
    for (const pending of pendingInputs.current) {
      const result = applyPhysicsToState(
        reconciledPosition,
        reconciledRotation,
        pending.input,
        1/60 // Fixed timestep
      );
      reconciledPosition = result.position;
      reconciledRotation = result.rotation;
    }

    // Smoothly interpolate to reconciled state
    meshRef.current.position.lerp(reconciledPosition, 0.3);
    meshRef.current.quaternion.slerp(reconciledRotation, 0.3);
  }, [serverState]);

  return <mesh ref={meshRef} />;
}
```

### Interpolation for Remote Players

```tsx
// Remote entities use interpolation (not prediction)
function RemotePlayer({ state }: { state: PlayerState }) {
  const meshRef = useRef<THREE.Mesh>(null);
  const targetPosition = useRef(new THREE.Vector3());
  const renderPosition = useRef(new THREE.Vector3());

  // Update target when new state arrives
  useEffect(() => {
    targetPosition.current.set(state.x, state.y, state.z);
  }, [state.x, state.y, state.z]);

  // Interpolate toward target each frame
  useFrame(() => {
    if (!meshRef.current) return;

    // 100ms delay for smooth interpolation
    const alpha = 0.15; // Adjust based on tick rate
    renderPosition.current.lerp(targetPosition.current, alpha);
    meshRef.current.position.copy(renderPosition.current);
  });

  return <mesh ref={meshRef} />;
}
```

### Snapshot Interpolation Buffer

```tsx
// Buffer multiple snapshots for smoother interpolation
function SnapshotBuffer() {
  const snapshots = useRef<PlayerState[]>([]);
  const INTERPOLATION_DELAY = 100; // ms

  const addSnapshot = (state: PlayerState) => {
    snapshots.current.push(state);
    // Remove old snapshots
    const cutoff = Date.now() - INTERPOLATION_DELAY * 2;
    snapshots.current = snapshots.current.filter((s) => s.timestamp > cutoff);
  };

  const getInterpolatedState = () => {
    const renderTime = Date.now() - INTERPOLATION_DELAY;
    // Find two snapshots around render time
    const sorted = [...snapshots.current].sort((a, b) => a.timestamp - b.timestamp);
    const before = sorted.filter((s) => s.timestamp <= renderTime).pop();
    const after = sorted.find((s) => s.timestamp > renderTime);

    if (!before || !after) return sorted[sorted.length - 1];

    // Linear interpolation between snapshots
    const t = (renderTime - before.timestamp) / (after.timestamp - before.timestamp);
    return {
      position: new THREE.Vector3().lerpVectors(
        new THREE.Vector3(before.x, before.y, before.z),
        new THREE.Vector3(after.x, after.y, after.z),
        t
      ),
      rotation: before.rotation.slerp(after.rotation, t),
    };
  };
}
```

### Prediction Error Correction

```tsx
// Smooth correction when prediction differs from server
function ReconcileWithSmoothing({
  clientPosition,
  serverPosition,
}: {
  clientPosition: THREE.Vector3;
  serverPosition: THREE.Vector3;
}) {
  const distance = clientPosition.distanceTo(serverPosition);

  // If error is small, smooth correct
  if (distance < 0.5) {
    // Visual only - snap server state, smooth render
    return {
      snap: false,
      correction: serverPosition.clone().sub(clientPosition).multiplyScalar(0.2),
    };
  }

  // If error is large, instant snap (rubber banding)
  return {
    snap: true,
    correction: serverPosition.clone().sub(clientPosition),
  };
}
```

### Prediction Best Practices

| Pattern | Use Case | Notes |
| ------- | -------- | ----- |
| **Client-authoritative** | Single player | No prediction needed |
| **Server-authoritative with prediction** | Multiplayer | Standard approach |
| **Hybrid** | Fast action, cosmetic only | Predict visuals, validate logic on server |
| **Lag compensation** | Hit detection | Server rewinds time for validation |

### Performance Tips

1. **Limit prediction scope**: Only predict local player
2. **Fixed timestep**: Use `1/60` for physics consistency
3. **Sequence numbers**: Track all inputs for proper replay
4. **Buffer size**: Keep 50-200ms of pending inputs
5. **Interpolation delay**: 100ms is standard for 20 tick rate

### Common Issues

| Issue | Cause | Solution |
| ----- | ----- | -------- |
| Rubber banding | Large prediction error | Increase interpolation delay |
| Input feel laggy | No client prediction | Implement prediction immediately |
| Jittery movement | Inconsistent interpolation | Use buffer-based interpolation |
| Desync over time | Floating point drift | Reconcile to server state every frame |

## Reference

- [Three.js Performance Tips](https://threejs.org/manual/#en/optimize-lots-of-objects)
- [agents/developer/skills/r3f-fundamentals.md](r3f-fundamentals.md) — R3F basics
- [agents/developer/skills/r3f-materials.md](r3f-materials.md) — Material optimization
- [Gaffer On Games - Networking](https://gafferongames.com/post/what_every_programmer_needs_to_know_about_game_networking/) — Game networking fundamentals
