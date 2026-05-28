---
name: threejs-3d-graphics
description: Use this skill when building immersive 3D web experiences with Three.js, covering scenes, cameras, geometries, materials, animations, and advanced rendering techniques.
---

# Three.js Development

Build high-performance 3D web applications using Three.js - a cross-browser WebGL/WebGPU library.

## When to Use This Skill

Use when working with:
- 3D scenes, models, animations, or visualizations
- WebGL/WebGPU rendering and graphics programming
- Interactive 3D experiences (games, configurators, data visualization)
- Camera controls, lighting, materials, or shaders
- Loading 3D assets (GLTF, FBX, OBJ) or textures
- Post-processing effects (bloom, depth of field, SSAO)
- Physics simulations, VR/XR experiences, or spatial audio
- Performance optimization (instancing, LOD, frustum culling)

## Progressive Learning Path

### Level 1: Getting Started
- Scene setup, basic geometries, materials, lights, rendering loop

### Level 2: Common Tasks
- **Asset Loading**: GLTF, FBX, OBJ, texture loaders
- **Textures**: Types, mapping, wrapping, filtering
- **Cameras**: Perspective, orthographic, controls
- **Lights**: Types, shadows, helpers
- **Animations**: Clips, mixer, keyframes
- **Math**: Vectors, matrices, quaternions, curves

### Level 3: Interactive & Effects
- **Interaction**: Raycasting, picking, transforms
- **Post-Processing**: Passes, bloom, SSAO, SSR
- **Controls (Addons)**: Orbit, transform, first-person

### Level 4: Advanced Rendering
- **Materials Advanced**: PBR, custom shaders
- **Performance**: Instancing, LOD, batching, culling
- **Node Materials (TSL)**: Shader graphs, compute

### Level 5: Specialized
- **Physics**: Ammo, Rapier, Jolt, VR/XR
- **Advanced Loaders**: SVG, VRML, domain-specific
- **WebGPU**: Modern backend, compute shaders

## Quick Start Pattern

```javascript
// 1. Scene, Camera, Renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// 2. Add Objects
const geometry = new THREE.BoxGeometry();
const material = new THREE.MeshStandardMaterial({ color: 0x00ff00 });
const cube = new THREE.Mesh(geometry, material);
scene.add(cube);

// 3. Add Lights
const light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(5, 5, 5);
scene.add(light);
scene.add(new THREE.AmbientLight(0x404040));

// 4. Animation Loop
function animate() {
  requestAnimationFrame(animate);
  cube.rotation.x += 0.01;
  cube.rotation.y += 0.01;
  renderer.render(scene, camera);
}
animate();
```

## External Resources

- Official Docs: [Three.js Documentation](https://threejs.org/docs/)
- Examples: [Three.js Examples](https://threejs.org/examples/)
- Editor: [Three.js Editor](https://threejs.org/editor/)
- Discord: [Three.js Discord](https://discord.gg/56GBJwAnUS)

## Task Planning Notes

- Always plan and break many small todo tasks.
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed.