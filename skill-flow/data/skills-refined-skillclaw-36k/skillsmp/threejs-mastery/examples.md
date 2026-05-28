# Three.js Code Examples

Practical, copy-paste ready examples for common Three.js tasks.

## Basic Scene Setup

```typescript
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

// Scene
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x1a1a1a);

// Camera
const camera = new THREE.PerspectiveCamera(
  75,
  window.innerWidth / window.innerHeight,
  0.1,
  1000
);
camera.position.set(0, 2, 5);

// Renderer
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
document.body.appendChild(renderer.domElement);

// Lighting
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(5, 10, 5);
directionalLight.castShadow = true;
scene.add(directionalLight);

// Controls
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

// Resize handler
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

// Animation loop
function animate() {
  controls.update();
  renderer.render(scene, camera);
  requestAnimationFrame(animate);
}

animate();
```

## Loading GLTF Model

```typescript
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader.js';

class ModelLoader {
  private gltfLoader: GLTFLoader;
  
  constructor() {
    // Setup DRACO compression
    const dracoLoader = new DRACOLoader();
    dracoLoader.setDecoderPath('/draco/');
    
    this.gltfLoader = new GLTFLoader();
    this.gltfLoader.setDRACOLoader(dracoLoader);
  }
  
  async load(url: string): Promise<THREE.Group> {
    return new Promise((resolve, reject) => {
      this.gltfLoader.load(
        url,
        (gltf) => {
          // Enable shadows
          gltf.scene.traverse((child) => {
            if (child instanceof THREE.Mesh) {
              child.castShadow = true;
              child.receiveShadow = true;
            }
          });
          
          resolve(gltf.scene);
        },
        (progress) => {
          const percent = (progress.loaded / progress.total) * 100;
          console.log(`Loading: ${percent.toFixed(0)}%`);
        },
        reject
      );
    });
  }
}

// Usage
const loader = new ModelLoader();
const model = await loader.load('/models/scene.glb');
scene.add(model);
```

## Particle System

```typescript
class ParticleSystem {
  private particles: THREE.Points;
  private velocities: Float32Array;
  
  constructor(count: number = 10000) {
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(count * 3);
    this.velocities = new Float32Array(count * 3);
    
    for (let i = 0; i < count; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 10;
      positions[i * 3 + 1] = (Math.random() - 0.5) * 10;
      positions[i * 3 + 2] = (Math.random() - 0.5) * 10;
      
      this.velocities[i * 3] = (Math.random() - 0.5) * 0.01;
      this.velocities[i * 3 + 1] = (Math.random() - 0.5) * 0.01;
      this.velocities[i * 3 + 2] = (Math.random() - 0.5) * 0.01;
    }
    
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    
    const material = new THREE.PointsMaterial({
      size: 0.05,
      color: 0xff6600,
      transparent: true,
      opacity: 0.8,
      sizeAttenuation: true
    });
    
    this.particles = new THREE.Points(geometry, material);
  }
  
  update() {
    const positions = this.particles.geometry.attributes.position.array as Float32Array;
    
    for (let i = 0; i < positions.length; i += 3) {
      positions[i] += this.velocities[i];
      positions[i + 1] += this.velocities[i + 1];
      positions[i + 2] += this.velocities[i + 2];
      
      // Boundary check
      if (Math.abs(positions[i]) > 5) this.velocities[i] *= -1;
      if (Math.abs(positions[i + 1]) > 5) this.velocities[i + 1] *= -1;
      if (Math.abs(positions[i + 2]) > 5) this.velocities[i + 2] *= -1;
    }
    
    this.particles.geometry.attributes.position.needsUpdate = true;
  }
  
  getParticles() {
    return this.particles;
  }
}

// Usage
const particleSystem = new ParticleSystem(10000);
scene.add(particleSystem.getParticles());

function animate() {
  particleSystem.update();
  renderer.render(scene, camera);
  requestAnimationFrame(animate);
}
```

## Post-Processing

```typescript
import { EffectComposer } from 'three/examples/jsm/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/examples/jsm/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass.js';

// Create composer
const composer = new EffectComposer(renderer);

// Render pass
const renderPass = new RenderPass(scene, camera);
composer.addPass(renderPass);

// Bloom pass
const bloomPass = new UnrealBloomPass(
  new THREE.Vector2(window.innerWidth, window.innerHeight),
  1.5,  // strength
  0.4,  // radius
  0.85  // threshold
);
composer.addPass(bloomPass);

// Render with composer instead of renderer
function animate() {
  controls.update();
  composer.render();
  requestAnimationFrame(animate);
}

// Update on resize
window.addEventListener('resize', () => {
  composer.setSize(window.innerWidth, window.innerHeight);
});
```

## Raycasting for Mouse Interaction

```typescript
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

function onMouseClick(event: MouseEvent) {
  // Calculate mouse position in normalized device coordinates
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
  
  // Update raycaster
  raycaster.setFromCamera(mouse, camera);
  
  // Calculate objects intersecting the ray
  const intersects = raycaster.intersectObjects(scene.children, true);
  
  if (intersects.length > 0) {
    const object = intersects[0].object;
    
    // Change color on click
    if (object instanceof THREE.Mesh) {
      (object.material as THREE.MeshStandardMaterial).color.set(0xff0000);
    }
  }
}

window.addEventListener('click', onMouseClick);
```

## Environment Map

```typescript
import { RGBELoader } from 'three/examples/jsm/loaders/RGBELoader.js';

async function setupEnvironment() {
  const rgbeLoader = new RGBELoader();
  const envMap = await rgbeLoader.loadAsync('/hdr/studio.hdr');
  
  envMap.mapping = THREE.EquirectangularReflectionMapping;
  
  scene.environment = envMap;
  scene.background = envMap;
  
  // Apply to materials
  scene.traverse((child) => {
    if (child instanceof THREE.Mesh) {
      const material = child.material as THREE.MeshStandardMaterial;
      if (material) {
        material.envMap = envMap;
        material.needsUpdate = true;
      }
    }
  });
}

setupEnvironment();
```

## Skybox

```typescript
const loader = new THREE.CubeTextureLoader();
const skybox = loader.load([
  '/skybox/px.jpg',  // positive x
  '/skybox/nx.jpg',  // negative x
  '/skybox/py.jpg',  // positive y
  '/skybox/ny.jpg',  // negative y
  '/skybox/pz.jpg',  // positive z
  '/skybox/nz.jpg',  // negative z
]);

scene.background = skybox;
```

## Text in 3D

```typescript
import { FontLoader } from 'three/examples/jsm/loaders/FontLoader.js';
import { TextGeometry } from 'three/examples/jsm/geometries/TextGeometry.js';

async function create3DText(text: string): Promise<THREE.Mesh> {
  const fontLoader = new FontLoader();
  
  return new Promise((resolve, reject) => {
    fontLoader.load(
      '/fonts/helvetiker_regular.typeface.json',
      (font) => {
        const geometry = new TextGeometry(text, {
          font: font,
          size: 1,
          height: 0.2,
          curveSegments: 12,
          bevelEnabled: true,
          bevelThickness: 0.03,
          bevelSize: 0.02,
          bevelOffset: 0,
          bevelSegments: 5
        });
        
        geometry.center();
        
        const material = new THREE.MeshStandardMaterial({
          color: 0xff6600,
          metalness: 0.5,
          roughness: 0.3
        });
        
        resolve(new THREE.Mesh(geometry, material));
      },
      undefined,
      reject
    );
  });
}

// Usage
const text = await create3DText('Hello Three.js!');
scene.add(text);
```

## Camera Animation

```typescript
import { gsap } from 'gsap';

function animateCamera(targetPosition: THREE.Vector3, duration: number = 2) {
  gsap.to(camera.position, {
    x: targetPosition.x,
    y: targetPosition.y,
    z: targetPosition.z,
    duration: duration,
    ease: 'power2.inOut',
    onUpdate: () => {
      camera.lookAt(0, 0, 0);
    }
  });
}

// Usage
animateCamera(new THREE.Vector3(5, 5, 5), 2);
```

## Simple Physics

```typescript
class PhysicsObject {
  mesh: THREE.Mesh;
  velocity: THREE.Vector3;
  acceleration: THREE.Vector3;
  
  constructor(geometry: THREE.BufferGeometry, material: THREE.Material) {
    this.mesh = new THREE.Mesh(geometry, material);
    this.velocity = new THREE.Vector3();
    this.acceleration = new THREE.Vector3();
  }
  
  applyForce(force: THREE.Vector3) {
    this.acceleration.add(force);
  }
  
  update(deltaTime: number) {
    // Update velocity
    this.velocity.add(this.acceleration.clone().multiplyScalar(deltaTime));
    
    // Update position
    this.mesh.position.add(this.velocity.clone().multiplyScalar(deltaTime));
    
    // Reset acceleration
    this.acceleration.set(0, 0, 0);
    
    // Apply gravity
    this.applyForce(new THREE.Vector3(0, -9.81, 0));
    
    // Ground collision
    if (this.mesh.position.y < 0) {
      this.mesh.position.y = 0;
      this.velocity.y *= -0.8;  // Bounce with dampening
    }
  }
}

// Usage
const ball = new PhysicsObject(
  new THREE.SphereGeometry(0.5),
  new THREE.MeshStandardMaterial({ color: 0xff0000 })
);
scene.add(ball.mesh);

function animate() {
  ball.update(0.016);  // ~60fps
  renderer.render(scene, camera);
  requestAnimationFrame(animate);
}
```
