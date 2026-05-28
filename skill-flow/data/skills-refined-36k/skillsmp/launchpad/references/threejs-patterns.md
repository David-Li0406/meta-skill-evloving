# Three.js Patterns for Landing Pages

React Three Fiber (R3F) patterns for immersive landing pages and portfolios.

---

## Stack

```bash
npm install three @react-three/fiber @react-three/drei
```

**@react-three/fiber** — React renderer for Three.js
**@react-three/drei** — Useful helpers (controls, loaders, abstractions)

---

## When to Use

### Use Three.js

- Portfolio sites showcasing creative/3D work
- Product showcases (3D product viewer)
- Tech/gaming landing pages where immersion matters
- Creative agency pages
- Interactive data visualizations
- Generative art backgrounds

### Don't Use Three.js

- Content-focused SaaS landing pages
- Waitlist/email capture pages
- Mobile-first experiences without fallbacks
- When Framer Motion or CSS can achieve the effect
- When it's decoration, not experience

---

## Setup

### Basic Canvas

```tsx
import { Canvas } from '@react-three/fiber'

function Scene() {
  return (
    <Canvas
      camera={{ position: [0, 0, 5], fov: 50 }}
      style={{ position: 'absolute', inset: 0 }}
    >
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} />
      {/* Your 3D content */}
    </Canvas>
  )
}
```

### With Suspense (for loading models)

```tsx
import { Suspense } from 'react'
import { Canvas } from '@react-three/fiber'
import { Loader } from '@react-three/drei'

function Scene() {
  return (
    <>
      <Canvas>
        <Suspense fallback={null}>
          <Model />
        </Suspense>
      </Canvas>
      <Loader />
    </>
  )
}
```

---

## Hero Background Patterns

### Floating Geometry

```tsx
import { Canvas } from '@react-three/fiber'
import { Float, MeshDistortMaterial } from '@react-three/drei'

function FloatingHero() {
  return (
    <div className="absolute inset-0 -z-10">
      <Canvas camera={{ position: [0, 0, 5] }}>
        <ambientLight intensity={0.5} />
        <directionalLight position={[10, 10, 5]} intensity={1} />

        <Float
          speed={2}
          rotationIntensity={0.5}
          floatIntensity={1}
        >
          <mesh scale={2}>
            <icosahedronGeometry args={[1, 4]} />
            <MeshDistortMaterial
              color="#ff6b35"
              distort={0.3}
              speed={2}
              roughness={0.2}
            />
          </mesh>
        </Float>
      </Canvas>
    </div>
  )
}
```

### Particle Field

```tsx
import { useRef, useMemo } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import * as THREE from 'three'

function Particles({ count = 1000 }) {
  const mesh = useRef<THREE.Points>(null)

  const particles = useMemo(() => {
    const positions = new Float32Array(count * 3)
    for (let i = 0; i < count; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 10
      positions[i * 3 + 1] = (Math.random() - 0.5) * 10
      positions[i * 3 + 2] = (Math.random() - 0.5) * 10
    }
    return positions
  }, [count])

  useFrame((state) => {
    if (mesh.current) {
      mesh.current.rotation.y = state.clock.elapsedTime * 0.05
    }
  })

  return (
    <points ref={mesh}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={particles.length / 3}
          array={particles}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial size={0.02} color="#4ECDC4" transparent opacity={0.6} />
    </points>
  )
}

function ParticleHero() {
  return (
    <div className="absolute inset-0 -z-10">
      <Canvas camera={{ position: [0, 0, 5] }}>
        <Particles count={2000} />
      </Canvas>
    </div>
  )
}
```

### Gradient Sphere

```tsx
import { Canvas } from '@react-three/fiber'
import { MeshGradientMaterial, Float } from '@react-three/drei'

function GradientHero() {
  return (
    <div className="absolute inset-0 -z-10 overflow-hidden">
      <Canvas camera={{ position: [0, 0, 4] }}>
        <Float speed={1} rotationIntensity={0.2}>
          <mesh scale={3}>
            <sphereGeometry args={[1, 64, 64]} />
            <meshBasicMaterial color="#ff6b35" wireframe />
          </mesh>
        </Float>
      </Canvas>
    </div>
  )
}
```

---

## Interactive Patterns

### Mouse-Following Element

```tsx
import { useRef } from 'react'
import { Canvas, useFrame, useThree } from '@react-three/fiber'
import * as THREE from 'three'

function FollowMouse() {
  const mesh = useRef<THREE.Mesh>(null)
  const { viewport } = useThree()

  useFrame(({ mouse }) => {
    if (mesh.current) {
      mesh.current.position.x = THREE.MathUtils.lerp(
        mesh.current.position.x,
        (mouse.x * viewport.width) / 2,
        0.1
      )
      mesh.current.position.y = THREE.MathUtils.lerp(
        mesh.current.position.y,
        (mouse.y * viewport.height) / 2,
        0.1
      )
    }
  })

  return (
    <mesh ref={mesh}>
      <sphereGeometry args={[0.5, 32, 32]} />
      <meshStandardMaterial color="#ff6b35" />
    </mesh>
  )
}
```

### Scroll-Linked Camera

```tsx
import { useRef } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { ScrollControls, useScroll } from '@react-three/drei'

function ScrollScene() {
  const scroll = useScroll()

  useFrame((state) => {
    // Move camera based on scroll
    state.camera.position.z = 5 - scroll.offset * 3
    state.camera.position.y = scroll.offset * 2
  })

  return (
    <mesh>
      <torusKnotGeometry args={[1, 0.3, 128, 16]} />
      <meshStandardMaterial color="#ff6b35" />
    </mesh>
  )
}

function ScrollHero() {
  return (
    <Canvas>
      <ScrollControls pages={3}>
        <ambientLight />
        <ScrollScene />
      </ScrollControls>
    </Canvas>
  )
}
```

---

## Product Viewer

### Basic Product Showcase

```tsx
import { Suspense } from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, useGLTF, Environment, ContactShadows } from '@react-three/drei'

function Product({ url }: { url: string }) {
  const { scene } = useGLTF(url)
  return <primitive object={scene} scale={1} />
}

function ProductViewer({ modelUrl }: { modelUrl: string }) {
  return (
    <div className="w-full h-[500px] bg-surface rounded-2xl overflow-hidden">
      <Canvas camera={{ position: [0, 0, 5], fov: 50 }}>
        <ambientLight intensity={0.5} />
        <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} />

        <Suspense fallback={null}>
          <Product url={modelUrl} />
          <Environment preset="city" />
          <ContactShadows position={[0, -1.5, 0]} opacity={0.4} blur={2} />
        </Suspense>

        <OrbitControls
          enablePan={false}
          enableZoom={false}
          minPolarAngle={Math.PI / 4}
          maxPolarAngle={Math.PI / 2}
        />
      </Canvas>
    </div>
  )
}
```

---

## Performance

### Lazy Loading

```tsx
import { lazy, Suspense } from 'react'

const ThreeScene = lazy(() => import('./ThreeScene'))

function Hero() {
  return (
    <div className="relative min-h-screen">
      {/* Static content loads immediately */}
      <div className="relative z-10">
        <h1>Your Headline</h1>
      </div>

      {/* 3D scene lazy loads */}
      <Suspense fallback={<div className="absolute inset-0 bg-void" />}>
        <ThreeScene />
      </Suspense>
    </div>
  )
}
```

### Reduced Motion

```tsx
import { useReducedMotion } from 'framer-motion'

function AnimatedScene() {
  const prefersReducedMotion = useReducedMotion()

  if (prefersReducedMotion) {
    return <StaticFallback />
  }

  return <ThreeJSScene />
}
```

### WebGL Detection

```tsx
import { useState, useEffect } from 'react'

function useWebGLSupport() {
  const [supported, setSupported] = useState(true)

  useEffect(() => {
    try {
      const canvas = document.createElement('canvas')
      const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl')
      setSupported(!!gl)
    } catch {
      setSupported(false)
    }
  }, [])

  return supported
}

function Hero() {
  const webglSupported = useWebGLSupport()

  if (!webglSupported) {
    return <StaticHero />
  }

  return <ThreeJSHero />
}
```

### Performance Optimization

```tsx
import { Canvas } from '@react-three/fiber'
import { PerformanceMonitor, AdaptiveDpr } from '@react-three/drei'

function OptimizedScene() {
  return (
    <Canvas>
      <PerformanceMonitor
        onDecline={() => {
          // Reduce quality when performance drops
        }}
      >
        <AdaptiveDpr pixelated />
        {/* Scene content */}
      </PerformanceMonitor>
    </Canvas>
  )
}
```

---

## Mobile Considerations

### Touch-Friendly Controls

```tsx
import { OrbitControls } from '@react-three/drei'

// Enable touch on mobile
<OrbitControls
  enablePan={false}
  enableZoom={true}
  touches={{
    ONE: THREE.TOUCH.ROTATE,
    TWO: THREE.TOUCH.DOLLY_PAN
  }}
/>
```

### Responsive Canvas

```tsx
function ResponsiveScene() {
  const isMobile = useMediaQuery('(max-width: 768px)')

  return (
    <Canvas
      camera={{
        position: isMobile ? [0, 0, 7] : [0, 0, 5],
        fov: isMobile ? 60 : 50
      }}
      dpr={isMobile ? 1 : [1, 2]} // Lower DPR on mobile
    >
      {/* Scene */}
    </Canvas>
  )
}
```

---

## Integration with Page

### Behind Content

```tsx
<section className="relative min-h-screen">
  {/* 3D background */}
  <div className="absolute inset-0 -z-10">
    <Canvas>
      <Scene />
    </Canvas>
  </div>

  {/* Content on top */}
  <div className="relative z-10 flex items-center justify-center min-h-screen">
    <div className="text-center">
      <h1 className="text-6xl font-bold">Your Headline</h1>
    </div>
  </div>
</section>
```

### Split Layout

```tsx
<section className="grid grid-cols-1 lg:grid-cols-2 min-h-screen">
  {/* Content */}
  <div className="flex items-center p-12">
    <div>
      <h1>Product Name</h1>
      <p>Description</p>
    </div>
  </div>

  {/* 3D Viewer */}
  <div className="relative h-[50vh] lg:h-auto">
    <Canvas>
      <ProductScene />
    </Canvas>
  </div>
</section>
```

---

## Resources

- [React Three Fiber docs](https://docs.pmnd.rs/react-three-fiber)
- [Drei helpers](https://github.com/pmndrs/drei)
- [Three.js docs](https://threejs.org/docs/)
- [Bruno Simon's Three.js Journey](https://threejs-journey.com/)
