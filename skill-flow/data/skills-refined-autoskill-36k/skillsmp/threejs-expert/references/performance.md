# Performance & Optimization (Three.js 2026)

To build elite 3D applications, performance must be a first-class citizen. This guide covers the essential techniques for maintaining 120fps on modern hardware.

## 1. Geometry Optimization

### Draco Compression
Always compress your `.glb` files. Draco reduces geometry size by up to 90%.
```bash
# Using gltf-pipeline (standard for 2026)
bun x gltf-pipeline -i scene.gltf -o scene.glb -d
```

### InstancedMesh (The Gold Standard)
If you have 1000 identical trees, use ONE `InstancedMesh`.
```tsx
function Forest() {
  const count = 1000;
  const meshRef = useRef<THREE.InstancedMesh>(null!);
  const tempObject = new THREE.Object3D();

  useEffect(() => {
    for (let i = 0; i < count; i++) {
      tempObject.position.set(Math.random() * 100, 0, Math.random() * 100);
      tempObject.updateMatrix();
      meshRef.current.setMatrixAt(i, tempObject.matrix);
    }
    meshRef.current.instanceMatrix.needsUpdate = true;
  }, []);

  return (
    <instancedMesh ref={meshRef} args={[null!, null!, count]}>
      <coneGeometry args={[1, 5, 8]} />
      <meshStandardMaterial color="green" />
    </instancedMesh>
  );
}
```

### BatchedMesh (r156+)
Use `BatchedMesh` when you have different geometries that share the same material. It allows drawing them in a single draw call.

## 2. Texture Optimization (KTX2)
Avoid PNG/JPG for large textures. They are decompressed into VRAM in their raw form.
- **KTX2/Basis**: Keeps textures compressed in VRAM.
- **Tools**: Use `toktx` or online converters to generate KTX2 files.

## 3. Render Loop Efficiency

### Frame-rate Independence
Always use the `delta` from `useFrame` or `clock.getDelta()`.
```javascript
// WRONG: Speed depends on FPS
mesh.rotation.x += 0.01;

// CORRECT: Speed is constant (units per second)
mesh.rotation.x += delta * 1.0;
```

### Throttling On-Demand
If the scene is static, don't waste energy.
```tsx
<Canvas frameloop="demand">
  {/* The scene will only render when something changes */}
</Canvas>
```

---
*Updated: January 23, 2026*
