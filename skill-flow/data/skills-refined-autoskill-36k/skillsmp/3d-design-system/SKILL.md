---
name: 3D Design System
description: Implement 3D elements and effects using Three.js and React Three Fiber
---

# 3D Design System Skill

## Overview
Create immersive 3D poker experiences using React Three Fiber, Three.js, and CSS 3D transforms.

## Setup

### Dependencies
```bash
npm install three @react-three/fiber @react-three/drei
```

### Basic Canvas Setup
```jsx
import { Canvas } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera } from '@react-three/drei';

function PokerScene() {
  return (
    <Canvas>
      <PerspectiveCamera makeDefault position={[0, 5, 10]} />
      <OrbitControls enablePan={false} maxPolarAngle={Math.PI / 2.5} />
      
      {/* Lighting */}
      <ambientLight intensity={0.4} />
      <spotLight position={[0, 10, 0]} intensity={0.8} castShadow />
      
      {/* Scene Objects */}
      <PokerTable3D />
      <Cards3D />
      <Chips3D />
    </Canvas>
  );
}
```

## 3D Poker Table

### Table Mesh
```jsx
import { useGLTF, MeshReflectorMaterial } from '@react-three/drei';

function PokerTable3D() {
  return (
    <group>
      {/* Felt surface */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]} receiveShadow>
        <planeGeometry args={[12, 6]} />
        <meshStandardMaterial 
          color="#0d4d33"
          roughness={0.9}
          metalness={0.1}
        />
      </mesh>
      
      {/* Rail */}
      <mesh position={[0, 0.2, 0]}>
        <torusGeometry args={[5, 0.3, 16, 100]} />
        <meshStandardMaterial 
          color="#8B4513"
          roughness={0.3}
          metalness={0.6}
        />
      </mesh>
      
      {/* Floor with reflections */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.5, 0]}>
        <planeGeometry args={[50, 50]} />
        <MeshReflectorMaterial
          blur={[300, 100]}
          resolution={1024}
          mixBlur={1}
          mixStrength={40}
          roughness={1}
          depthScale={1.2}
          color="#101010"
          metalness={0.4}
        />
      </mesh>
    </group>
  );
}
```

## 3D Cards

### Card Component
```jsx
import { useTexture } from '@react-three/drei';
import { useSpring, animated } from '@react-spring/three';

function Card3D({ card, position, rotation, isFlipped }) {
  const [frontTexture, backTexture] = useTexture([
    `/cards/${card}.png`,
    '/cards/back.png'
  ]);
  
  const { rotateY } = useSpring({
    rotateY: isFlipped ? Math.PI : 0,
    config: { mass: 1, tension: 180, friction: 12 }
  });
  
  return (
    <animated.group position={position} rotation-y={rotateY}>
      {/* Front face */}
      <mesh rotation={[0, 0, 0]}>
        <planeGeometry args={[0.7, 1]} />
        <meshStandardMaterial map={frontTexture} />
      </mesh>
      
      {/* Back face */}
      <mesh rotation={[0, Math.PI, 0]}>
        <planeGeometry args={[0.7, 1]} />
        <meshStandardMaterial map={backTexture} />
      </mesh>
    </animated.group>
  );
}
```

### Card Deal Animation
```jsx
import { useFrame } from '@react-three/fiber';
import { useRef } from 'react';

function DealingCard3D({ targetPosition, delay }) {
  const ref = useRef();
  const [isDealing, setIsDealing] = useState(false);
  
  useEffect(() => {
    const timer = setTimeout(() => setIsDealing(true), delay * 100);
    return () => clearTimeout(timer);
  }, [delay]);
  
  useFrame((state, delta) => {
    if (!ref.current || !isDealing) return;
    
    ref.current.position.lerp(targetPosition, 0.1);
    ref.current.rotation.y += delta * 2;
  });
  
  return (
    <mesh ref={ref} position={[0, 5, 0]}>
      <planeGeometry args={[0.7, 1]} />
      <meshStandardMaterial color="red" />
    </mesh>
  );
}
```

## 3D Chips

### Chip Stack
```jsx
function ChipStack3D({ amount, position, color = '#ff4444' }) {
  const chipCount = Math.min(Math.ceil(amount / 100), 10);
  
  return (
    <group position={position}>
      {[...Array(chipCount)].map((_, i) => (
        <mesh key={i} position={[0, i * 0.05, 0]} castShadow>
          <cylinderGeometry args={[0.3, 0.3, 0.04, 32]} />
          <meshStandardMaterial 
            color={color}
            roughness={0.3}
            metalness={0.7}
          />
        </mesh>
      ))}
    </group>
  );
}
```

### Chip Throw Animation
```jsx
import { useSpring, animated } from '@react-spring/three';

function FlyingChip3D({ from, to, onComplete }) {
  const { position, rotation } = useSpring({
    from: { position: from, rotation: [0, 0, 0] },
    to: { position: to, rotation: [Math.PI * 2, Math.PI * 4, 0] },
    config: { mass: 1, tension: 200, friction: 20 },
    onRest: onComplete
  });
  
  return (
    <animated.mesh position={position} rotation={rotation}>
      <cylinderGeometry args={[0.3, 0.3, 0.04, 32]} />
      <meshStandardMaterial color="#ffd700" metalness={0.8} roughness={0.2} />
    </animated.mesh>
  );
}
```

## CSS 3D Effects

### 3D Card CSS
```css
.card-3d {
  perspective: 1000px;
  transform-style: preserve-3d;
}

.card-3d:hover {
  transform: rotateY(15deg) rotateX(-5deg);
}

.card-3d-inner {
  transition: transform 0.6s;
  transform-style: preserve-3d;
}

.card-3d.flipped .card-3d-inner {
  transform: rotateY(180deg);
}

.card-front, .card-back {
  position: absolute;
  backface-visibility: hidden;
}

.card-back {
  transform: rotateY(180deg);
}
```

### 3D Button Effect
```css
.btn-3d {
  transform: perspective(500px) translateZ(0);
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-3d:hover {
  transform: perspective(500px) translateZ(20px);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
}

.btn-3d:active {
  transform: perspective(500px) translateZ(-10px);
}
```

## Environment & Lighting

### HDR Environment
```jsx
import { Environment } from '@react-three/drei';

<Environment 
  preset="night"  // 'sunset', 'dawn', 'night', 'warehouse', 'forest', etc.
  background={false}
/>
```

### Custom Lighting Rig
```jsx
function PokerLighting() {
  return (
    <>
      {/* Main overhead light */}
      <spotLight
        position={[0, 10, 0]}
        angle={0.5}
        penumbra={0.5}
        intensity={1}
        castShadow
        shadow-mapSize={[2048, 2048]}
      />
      
      {/* Rim lights */}
      <pointLight position={[10, 5, 0]} intensity={0.3} color="#ff7700" />
      <pointLight position={[-10, 5, 0]} intensity={0.3} color="#0077ff" />
      
      {/* Ambient fill */}
      <ambientLight intensity={0.2} />
    </>
  );
}
```

## Performance

### 1. Use `instancedMesh` for many identical objects
```jsx
function ChipField({ chips }) {
  const meshRef = useRef();
  
  useEffect(() => {
    chips.forEach((chip, i) => {
      meshRef.current.setMatrixAt(i, new Matrix4().makeTranslation(...chip.position));
    });
    meshRef.current.instanceMatrix.needsUpdate = true;
  }, [chips]);
  
  return (
    <instancedMesh ref={meshRef} args={[null, null, chips.length]}>
      <cylinderGeometry args={[0.3, 0.3, 0.04, 16]} />
      <meshStandardMaterial color="#ffd700" />
    </instancedMesh>
  );
}
```

### 2. Use `useLoader` for async loading
```jsx
const texture = useLoader(TextureLoader, '/texture.jpg');
```

### 3. Lazy load 3D scenes
```jsx
const Poker3DScene = dynamic(() => import('./Poker3DScene'), {
  ssr: false,
  loading: () => <LoadingSpinner />
});
```

### 4. Use LOD (Level of Detail)
```jsx
import { LOD } from 'three';

// Simpler geometry at distance, detailed up close
```
