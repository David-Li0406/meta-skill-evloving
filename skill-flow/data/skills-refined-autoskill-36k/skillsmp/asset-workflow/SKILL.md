---
name: asset-workflow
description: Asset creation pipeline and integration workflow for Tech Artist
category: development
depends-on: []
---

# Asset Workflow Skill

> "A well-organized asset pipeline saves hours of frustration."

## When to Use This Skill

Use when:

- Creating new 3D/2D assets
- Importing external models
- Organizing project assets
- Setting up asset pipelines

## Asset Directory Structure

```
src/
├── assets/
│   ├── models/          # 3D models (.glb, .gltf)
│   │   ├── characters/
│   │   ├── vehicles/
│   │   ├── props/
│   │   └── environment/
│   ├── textures/        # Texture maps
│   │   ├── color/       # Albedo/diffuse
│   │   ├── normal/      # Normal maps
│   │   ├── roughness/   # Roughness/metalness
│   │   └── emission/    # Emissive/glow
│   ├── audio/           # Sound effects and music
│   │   ├── sfx/
│   │   └── music/
│   ├── shaders/         # GLSL shader files
│   └── fonts/           # Typefaces
└── components/
    └── assets/          # Asset wrapper components
```

## Asset Integration Workflow

### 1. Receive Task

```json
// From PM via current-task.json
{
  "taskId": "vis-002",
  "assetType": "material",
  "title": "Vehicle PBR materials",
  "description": "Create realistic car paint materials",
  "references": ["docs/design/gdd.md#visual-style"]
}
```

### 2. Read GDD for Art Direction

```markdown
# Visual Style Reference

## Color Palette
- Primary: #FF6B35 (sunset orange)
- Secondary: #004E89 (deep blue)
- Accent: #F77F00 (amber)

## Material Guidelines
- Vehicles: Metallic, 60-70% roughness
- Environment: Matte, 80% roughness
- UI elements: Emissive, glowing
```

### 3. Request Additional References (if needed)

```json
// Send to Game Designer via message queue
{
  "type": "reference_request",
  "from": "techartist",
  "to": "gamedesigner",
  "payload": {
    "question": "What specific car paint finish? (matte, gloss, metallic)",
    "taskId": "vis-002",
    "assetType": "material"
  }
}
```

### 4. Create Asset

```tsx
// src/components/assets/VehiclePaint.tsx
import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

export function VehiclePaint({ color = '#FF6B35' }: { color?: string }) {
  const materialRef = useRef<THREE.MeshPhysicalMaterial>(null!);

  useFrame(({ clock }) => {
    // Subtle clearcoat animation
    if (materialRef.current) {
      materialRef.current.clearcoat = 0.8 + Math.sin(clock.elapsedTime * 0.5) * 0.1;
    }
  });

  return (
    <meshPhysicalMaterial
      ref={materialRef}
      color={color}
      metalness={0.9}
      roughness={0.3}
      clearcoat={1.0}
      clearcoatRoughness={0.1}
      envMapIntensity={1.5}
    />
  );
}
```

### 5. Test in Scene

```tsx
// Test component for development
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { VehiclePaint } from './components/assets/VehiclePaint';

function TestScene() {
  return (
    <Canvas camera={{ position: [0, 2, 5] }}>
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} intensity={1} />
      <mesh>
        <boxGeometry args={[2, 1, 4]} />
        <VehiclePaint />
      </mesh>
      <OrbitControls />
    </Canvas>
  );
}
```

### 6. Run Feedback Loops

```bash
npm run type-check  # Must pass
npm run lint        # Must pass
npm run build       # Must pass
```

### 7. Commit Work

```bash
git add .
git commit -m "[ralph] [techartist] vis-002: Vehicle PBR materials

- Added metallic paint material with animated clearcoat
- Created reusable VehiclePaint component
- Material follows GDD color palette

PRD: vis-002 | Agent: techartist | Iteration: 1"
```

### 8. Send to QA

```json
// Update coordinator-state.json
{
  "currentTask": {
    "id": "vis-002",
    "status": "ready_for_qa",
    "assignedAgent": "techartist"
  }
}
```

## Asset Naming Conventions

| Asset Type     | Format                        | Example                     |
| -------------- | ----------------------------- | --------------------------- |
| Models         | `{Name}_lod{0-3}.glb`         | `sportsCar_lod0.glb`        |
| Textures       | `{name}_{type}.{ext}`         | `vehicle_color.png`         |
| Materials      | `{Name}Material.tsx`          | `CarPaintMaterial.tsx`      |
| Shaders        | `{name}.{vert|frag}`          | `water.vert`                |
| Components     | `{Name}.tsx`                  | `VehicleMesh.tsx`           |

## Import Guidelines

```tsx
// ✅ DO: Use lazy loading for large assets
import { useGLTF } from '@react-three/drei';

function Vehicle() {
  const { scene } = useGLTF('/assets/models/vehicles/sportsCar.glb');
  return <primitive object={scene} />;
}

// ✅ DO: Use Suspense for asset loading
import { Suspense } from 'react';

function Scene() {
  return (
    <Suspense fallback={<LoadingIndicator />}>
      <Vehicle />
    </Suspense>
  );
}

// ❌ DON'T: Import large assets at module level
import vehicleModel from './assets/models/vehicle.glb'; // Bad!
```

## Texture Optimization

```bash
# Optimize textures before importing
# Resize to power-of-2 dimensions
convert input.jpg -resize 512x512 output.png

# Compress to WebP
convert input.png -quality 80 output.webp

# Or use basis universal for GPU compression
basisu -q 1 input.png -output output.basis
```

## GLTF Export Settings (Blender)

```
Export Settings:
- Format: glTF Binary (.glb)
- Include: Selected Objects
- Mesh: + Apply Modifiers
- Mesh: - Tangents (compute at runtime)
- Mesh: - Blending: Obsolete
- LoD: Simplify disabled
- Armature: + Only Keyframes
- Animation: - Limit to Selected
- Geometry: - UV Map
- Geometry: - Normals
- Geometry: + Tangents
- Geometry: + Vertex Colors
- Objects: - PBR Ext
```

## Asset Component Template

```tsx
/**
 * {Asset Name}
 *
 * {Description of asset}
 *
 * @example
 * ```tsx
 * <MyAsset />
 * ```
 */
import { forwardRef, useMemo } from 'react';
import * as THREE from 'three';

export interface MyAssetProps {
  /** Description of prop */
  variant?: 'a' | 'b' | 'c';
  /** Another prop */
  intensity?: number;
}

export const MyAsset = forwardRef<THREE.Group, MyAssetProps>(
  ({ variant = 'a', intensity = 1.0 }, ref) => {
    // Create or load asset here
    const material = useMemo(
      () => new THREE.MeshStandardMaterial({
        color: variant === 'a' ? 0xff0000 : 0x0000ff,
      }),
      [variant]
    );

    return (
      <group ref={ref}>
        <mesh>
          <boxGeometry />
          <meshStandardMaterial {...material} />
        </mesh>
      </group>
    );
  }
);

MyAsset.displayName = 'MyAsset';
```

## Checklist

Before marking asset ready:

- [ ] Asset follows naming conventions
- [ ] File is in correct directory
- [ ] textures are optimized (compressed, power-of-2)
- [ ] Component has TypeScript types
- [ ] Props documented with JSDoc
- [ ] Example usage in comments
- [ ] Tested in browser
- [ ] Feedback loops all pass

## Reference

- [GLTF Best Practices](https://github.com/KhronosGroup/glTF-Sample-Models)
- [skills/r3f-materials.md](r3f-materials.md) — Material setup
- [AGENT.md](../AGENT.md) — Full techartist workflow
