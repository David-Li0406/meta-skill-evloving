# WebGPU & TSL (Three Shader Language)

In 2026, WebGL is considered a legacy fallback. WebGPU is the primary API, and TSL is the bridge that allows us to write shaders that run everywhere.

## 1. Why WebGPU?
- **Lower CPU Overhead**: WebGPU handles draw calls much faster than WebGL.
- **Compute Shaders**: Move complex math (physics, flocking, particles) to the GPU.
- **Modern GPU Features**: Access to bind groups, storage buffers, and more.

## 2. Transitioning to TSL
TSL (Three Shader Language) is a node-based shader system that looks like JavaScript but compiles to WGSL or GLSL.

### Example: A Wave Shader in TSL
```tsx
import { positionLocal, timerLocal, sin, float, vec3 } from 'three/tsl';

const material = new THREE.MeshStandardNodeMaterial();

const time = timerLocal();
const pos = positionLocal;

// Procedural wave logic
const wave = sin(pos.x.add(time)).mul(0.5);
const newPos = vec3(pos.x, pos.y.add(wave), pos.z);

material.positionNode = newPos; // Displace vertices
```

## 3. Compute Shaders
You can now run arbitrary calculations on the GPU without rendering anything.
```javascript
const computeInit = new THREE.ComputeNode( ( { storage } ) => {
    // Write your GPU logic here
} );
renderer.compute( computeInit );
```

## 4. Mandatory Async Init
WebGPU requires an asynchronous setup.
```javascript
const renderer = new THREE.WebGPURenderer();
await renderer.init(); // This is mandatory in v172+
```

---
*Updated: January 23, 2026*
