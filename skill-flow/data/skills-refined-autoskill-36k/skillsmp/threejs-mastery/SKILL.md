---
name: threejs-mastery
description: Ultimate Three.js development with WebGPU, React Three Fiber, performance optimization, and production-ready patterns. Use for building 3D web apps, optimizing rendering, implementing shaders, integrating physics, and following 2026 best practices.
---

# Three.js Mastery 2026

Production-grade Three.js development with WebGPU, modern patterns, and performance optimization.

## 📚 Essential Resources

**Official Documentation:**
- Three.js Docs: https://threejs.org/docs/
- Three.js Examples: https://threejs.org/examples/
- WebGPU Fundamentals: https://webgpufundamentals.org/

**Learning:**
- Three.js Journey (Bruno Simon): https://threejs-journey.com/
- Three.js Fundamentals: https://threejs.org/manual/
- Discover Three.js: https://discoverthreejs.com/

**Community:**
- Three.js Discourse: https://discourse.threejs.org/
- React Three Fiber: https://docs.pmnd.rs/react-three-fiber/

## 🏗️ Modern Architecture (2026)

### Project Structure
```
src/
├── core/              # Scene, renderer, camera management
├── entities/          # 3D objects and components
├── materials/         # Custom materials and shaders
├── physics/           # Physics integration (Rapier)
├── ui/               # 3D UI and overlays
└── utils/            # Performance, geometry, math utils
```

### Key Principles
1. **WebGPU First**: Use WebGPU with WebGL2 fallback
2. **TypeScript**: Full type safety
3. **Performance**: LOD, instancing, object pooling
4. **Memory Management**: Proper disposal patterns
5. **React Integration**: Use React Three Fiber for UI-heavy apps

## 🚀 WebGPU Setup (2026 Standard)

```typescript
// Modern renderer with feature detection
async function initializeRenderer(canvas: HTMLCanvasElement) {
  // Try WebGPU first
  if ('gpu' in navigator) {
    const adapter = await navigator.gpu.requestAdapter({
      powerPreference: 'high-performance'
    });
    
    if (adapter) {
      const renderer = new THREE.WebGPURenderer({
        canvas,
        antialias: true,
        powerPreference: 'high-performance'
      });
      
      await renderer.init();
      renderer.toneMapping = THREE.ACESFilmicToneMapping;
      renderer.toneMappingExposure = 1.0;
      
      return renderer;
    }
  }
  
  // Fallback to WebGL2
  const renderer = new THREE.WebGLRenderer({
    canvas,
    antialias: true,
    powerPreference: 'high-performance'
  });
  
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  
  return renderer;
}
```

## 🎨 Material Best Practices

### PBR Materials (2026)
```typescript
// Use MeshPhysicalMaterial for realistic rendering
const material = new THREE.MeshPhysicalMaterial({
  // Base properties
  map: colorTexture,
  normalMap: normalTexture,
  roughnessMap: roughnessTexture,
  metalnessMap: metalnessTexture,
  aoMap: aoTexture,
  
  // Physical properties
  roughness: 0.8,
  metalness: 0.0,
  
  // Advanced features (2026)
  clearcoat: 0.1,
  clearcoatRoughness: 0.3,
  transmission: 0,      // For glass
  thickness: 0.5,       // Subsurface
  ior: 1.5,
  
  // Environment
  envMapIntensity: 1.0
});
```

### Texture Optimization
```typescript
// Load with proper settings
const texture = textureLoader.load('/texture.jpg');
texture.colorSpace = THREE.SRGBColorSpace;  // CRITICAL for color
texture.anisotropy = 16;                    // Max quality
texture.minFilter = THREE.LinearMipmapLinearFilter;
texture.magFilter = THREE.LinearFilter;

// Use compressed textures (KTX2/Basis)
import { KTX2Loader } from 'three/examples/jsm/loaders/KTX2Loader.js';

const ktx2Loader = new KTX2Loader();
ktx2Loader.setTranscoderPath('/basis/');
ktx2Loader.detectSupport(renderer);

const compressedTexture = await ktx2Loader.loadAsync('/texture.ktx2');
```

## ⚡ Performance Optimization

### 1. Level of Detail (LOD)
```typescript
const lod = new THREE.LOD();

// High detail (close)
lod.addLevel(highPolyMesh, 0);

// Medium detail
lod.addLevel(mediumPolyMesh, 50);

// Low detail (far)
lod.addLevel(lowPolyMesh, 100);

scene.add(lod);

// Update in render loop
function animate() {
  lod.update(camera);
  renderer.render(scene, camera);
}
```

### 2. Instancing for Repeated Objects
```typescript
// Create instanced mesh
const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshStandardMaterial({ color: 0xff6600 });
const instancedMesh = new THREE.InstancedMesh(geometry, material, 1000);

// Set transforms for each instance
const matrix = new THREE.Matrix4();
const position = new THREE.Vector3();
const rotation = new THREE.Euler();
const quaternion = new THREE.Quaternion();
const scale = new THREE.Vector3(1, 1, 1);

for (let i = 0; i < 1000; i++) {
  position.set(
    (i % 10) * 2,
    Math.floor(i / 100) * 2,
    Math.floor((i % 100) / 10) * 2
  );
  
  quaternion.setFromEuler(rotation);
  matrix.compose(position, quaternion, scale);
  
  instancedMesh.setMatrixAt(i, matrix);
}

instancedMesh.instanceMatrix.needsUpdate = true;
scene.add(instancedMesh);
```

### 3. Object Pooling
```typescript
// Reuse objects instead of creating new ones
class ObjectPool<T extends THREE.Object3D> {
  private pool: T[] = [];
  private active = new Set<T>();
  
  constructor(
    private factory: () => T,
    initialSize: number = 100
  ) {
    for (let i = 0; i < initialSize; i++) {
      this.pool.push(this.factory());
    }
  }
  
  acquire(): T {
    const obj = this.pool.pop() || this.factory();
    this.active.add(obj);
    return obj;
  }
  
  release(obj: T): void {
    obj.position.set(0, 0, 0);
    obj.rotation.set(0, 0, 0);
    obj.scale.set(1, 1, 1);
    obj.visible = true;
    
    this.active.delete(obj);
    this.pool.push(obj);
  }
}
```

### 4. Frustum Culling
```typescript
// Automatically cull objects outside camera view
mesh.frustumCulled = true;  // Default is true

// Manual culling for optimization
const frustum = new THREE.Frustum();
const projScreenMatrix = new THREE.Matrix4();

function updateFrustum() {
  camera.updateMatrixWorld();
  projScreenMatrix.multiplyMatrices(
    camera.projectionMatrix,
    camera.matrixWorldInverse
  );
  frustum.setFromProjectionMatrix(projScreenMatrix);
}

function isVisible(object: THREE.Object3D): boolean {
  if (!object.geometry?.boundingSphere) return true;
  
  const sphere = object.geometry.boundingSphere.clone();
  sphere.applyMatrix4(object.matrixWorld);
  
  return frustum.intersectsSphere(sphere);
}
```

## 🎮 React Three Fiber Patterns

### Basic Setup
```tsx
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Environment } from '@react-three/drei';

function App() {
  return (
    <Canvas
      camera={{ position: [0, 0, 5], fov: 50 }}
      shadows
      dpr={[1, 2]}  // Adaptive pixel ratio
    >
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} castShadow />
      
      <Scene />
      
      <OrbitControls makeDefault />
      <Environment preset="sunset" />
    </Canvas>
  );
}
```

### Animation Hook
```tsx
import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

function RotatingBox() {
  const meshRef = useRef<THREE.Mesh>(null);
  
  // Use ref, not state for animations!
  useFrame((state, delta) => {
    if (!meshRef.current) return;
    
    meshRef.current.rotation.y += delta;
    meshRef.current.position.y = Math.sin(state.clock.elapsedTime) * 0.5;
  });
  
  return (
    <mesh ref={meshRef} castShadow>
      <boxGeometry />
      <meshStandardMaterial color="orange" />
    </mesh>
  );
}
```

### Performance Optimization in R3F
```tsx
import { memo } from 'react';
import { Instances, Instance } from '@react-three/drei';

// Memoize expensive components
const ExpensiveModel = memo(function ExpensiveModel() {
  return <primitive object={complexModel} />;
});

// Use instancing for many objects
function ManyBoxes() {
  return (
    <Instances limit={1000}>
      <boxGeometry />
      <meshStandardMaterial />
      {Array.from({ length: 1000 }).map((_, i) => (
        <Instance
          key={i}
          position={[
            (i % 10) * 2 - 10,
            Math.floor(i / 100) * 2,
            Math.floor((i % 100) / 10) * 2 - 10
          ]}
        />
      ))}
    </Instances>
  );
}
```

## 🎨 Shader Basics

### Custom Shader Material
```typescript
const material = new THREE.ShaderMaterial({
  uniforms: {
    time: { value: 0 },
    color: { value: new THREE.Color(0xff6600) }
  },
  
  vertexShader: `
    varying vec2 vUv;
    
    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  
  fragmentShader: `
    uniform float time;
    uniform vec3 color;
    varying vec2 vUv;
    
    void main() {
      vec3 finalColor = color;
      finalColor.r += sin(vUv.x * 10.0 + time) * 0.5;
      
      gl_FragColor = vec4(finalColor, 1.0);
    }
  `
});

// Update uniforms in render loop
function animate() {
  material.uniforms.time.value += 0.016;
  renderer.render(scene, camera);
}
```

## 🧹 Memory Management

### Proper Disposal
```typescript
function disposeObject(object: THREE.Object3D) {
  object.traverse((child) => {
    // Dispose geometry
    if (child.geometry) {
      child.geometry.dispose();
    }
    
    // Dispose material(s)
    if (child.material) {
      const materials = Array.isArray(child.material) 
        ? child.material 
        : [child.material];
      
      materials.forEach((material) => {
        // Dispose all textures
        Object.keys(material).forEach((key) => {
          const value = (material as any)[key];
          if (value instanceof THREE.Texture) {
            value.dispose();
          }
        });
        
        material.dispose();
      });
    }
    
    // Dispose skeleton
    if (child instanceof THREE.SkinnedMesh) {
      child.skeleton?.dispose();
    }
  });
  
  // Remove from parent
  object.parent?.remove(object);
}
```

## 🎯 Common Patterns

### Scene Management (Singleton)
```typescript
class SceneManager {
  private static instance: SceneManager;
  private scene: THREE.Scene;
  private renderer: THREE.WebGPURenderer | THREE.WebGLRenderer;
  private camera: THREE.PerspectiveCamera;
  
  private constructor() {}
  
  static getInstance(): SceneManager {
    if (!SceneManager.instance) {
      SceneManager.instance = new SceneManager();
    }
    return SceneManager.instance;
  }
  
  async initialize(canvas: HTMLCanvasElement) {
    this.scene = new THREE.Scene();
    this.renderer = await initializeRenderer(canvas);
    this.camera = new THREE.PerspectiveCamera(
      75,
      window.innerWidth / window.innerHeight,
      0.1,
      1000
    );
  }
  
  render() {
    this.renderer.render(this.scene, this.camera);
  }
}
```

### Loading Assets
```typescript
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader.js';

// Setup DRACO compression
const dracoLoader = new DRACOLoader();
dracoLoader.setDecoderPath('/draco/');

const gltfLoader = new GLTFLoader();
gltfLoader.setDRACOLoader(dracoLoader);

// Load model
async function loadModel(url: string): Promise<THREE.Group> {
  return new Promise((resolve, reject) => {
    gltfLoader.load(
      url,
      (gltf) => resolve(gltf.scene),
      undefined,
      reject
    );
  });
}

// Usage with error handling
try {
  const model = await loadModel('/models/car.glb');
  scene.add(model);
} catch (error) {
  console.error('Failed to load model:', error);
}
```

## 📊 Performance Monitoring

```typescript
// Track FPS and performance
class PerformanceMonitor {
  private frameCount = 0;
  private lastTime = performance.now();
  private fps = 60;
  
  update() {
    this.frameCount++;
    const now = performance.now();
    
    if (now >= this.lastTime + 1000) {
      this.fps = Math.round((this.frameCount * 1000) / (now - this.lastTime));
      this.frameCount = 0;
      this.lastTime = now;
      
      // Check performance
      if (this.fps < 30) {
        console.warn('⚠️ Low FPS detected:', this.fps);
      }
    }
  }
  
  getFPS(): number {
    return this.fps;
  }
}

const monitor = new PerformanceMonitor();

function animate() {
  monitor.update();
  renderer.render(scene, camera);
  requestAnimationFrame(animate);
}
```

## 📱 Mobile Optimization

```typescript
function optimizeForMobile(renderer: THREE.WebGPURenderer | THREE.WebGLRenderer) {
  const isMobile = /Android|iPhone|iPad/i.test(navigator.userAgent);
  
  if (isMobile) {
    // Reduce pixel ratio
    renderer.setPixelRatio(Math.min(1.5, window.devicePixelRatio));
    
    // Disable expensive features
    renderer.shadowMap.enabled = false;
    
    // Use simpler materials
    scene.traverse((object) => {
      if (object instanceof THREE.Mesh) {
        const material = object.material as THREE.MeshStandardMaterial;
        if (material) {
          material.envMapIntensity = 0.5;
        }
      }
    });
  }
}
```

## ✅ Production Checklist

Before deploying:

- [ ] WebGPU with WebGL2 fallback implemented
- [ ] All geometries and materials properly disposed
- [ ] LOD system for complex scenes
- [ ] Instancing used for repeated objects
- [ ] Textures compressed (WebP, KTX2)
- [ ] Shadow maps optimized (size, soft shadows)
- [ ] Mobile optimizations applied
- [ ] Performance monitoring in place
- [ ] Error handling for asset loading
- [ ] TypeScript types defined
- [ ] FPS stable at 60+ on target devices
- [ ] Memory usage under 500MB
- [ ] Draw calls under 100
- [ ] Triangle count optimized with LOD

## 🔗 Additional Resources

Detailed guides available in skill references:
- Performance optimization deep dive
- React Three Fiber complete guide
- WebGPU advanced techniques
- Shader library (20+ shaders)
- Physics integration (Rapier)
- Post-processing effects

**Tools:**
- Performance profiler script
- Asset optimizer script
- Bundle analyzer

Ready to build amazing 3D experiences! 🚀
