---
name: shader-development
description: GLSL shader creation process and patterns for R3F
category: development
depends-on: [r3f-materials]
---

# Shader Development Skill

> "Shaders unlock visual effects impossible with standard materials."

## When to Use This Skill

Use when:

- Creating custom visual effects
- Implementing procedural patterns
- Optimizing material performance
- Building GPU-accelerated effects

## Shader Structure

```tsx
import { shaderMaterial } from '@react-three/drei';
import { extend } from '@react-three/fiber';

const CustomShaderMaterial = shaderMaterial(
  // Uniforms (variables passed from JS)
  {
    uTime: { value: 0 },
    uColor: { value: new THREE.Color(0.0, 0.5, 1.0) },
    uTexture: { value: null },
  },
  // Vertex shader
  vertexShader,
  // Fragment shader
  fragmentShader
);

extend({ CustomShaderMaterial });
```

## Vertex Shader Patterns

### Basic Vertex Shader

```glsl
uniform float uTime;
uniform mat4 modelViewMatrix;
uniform mat4 projectionMatrix;

attribute vec3 position;
attribute vec2 uv;
attribute vec3 normal;

varying vec2 vUv;
varying vec3 vNormal;
varying vec3 vPosition;

void main() {
  vUv = uv;
  vNormal = normal;
  vPosition = position;

  // Basic displacement
  vec3 pos = position;
  pos.y += sin(pos.x * 4.0 + uTime) * 0.1;

  gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
}
```

### SDF-based Displacement

```glsl
// Sphere SDF
float sdSphere(vec3 p, float r) {
  return length(p) - r;
}

void main() {
  vec3 pos = position;

  // Animated SDF displacement
  float d = sdSphere(pos * 2.0, 1.0);
  pos += normal * d * 0.1;

  vUv = uv;
  gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
}
```

### Vertex Animation

```glsl
uniform float uTime;
varying vec2 vUv;

// Simple noise function
float hash(vec2 p) {
  return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

void main() {
  vUv = uv;
  vec3 pos = position;

  // Wave displacement
  pos.z += sin(pos.x * 2.0 + uTime) * cos(pos.y * 2.0 + uTime) * 0.2;

  gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
}
```

## Fragment Shader Patterns

### Color Gradient

```glsl
uniform float uTime;
varying vec2 vUv;

void main() {
  // UV gradient
  vec3 color = vec3(vUv.x, vUv.y, 0.5);

  // Add time-based animation
  color.r += sin(uTime) * 0.2;

  gl_FragColor = vec4(color, 1.0);
}
```

### Circle/Shape Drawing

```glsl
varying vec2 vUv;

float sdCircle(vec2 p, float r) {
  return length(p) - r;
}

float sdBox(vec2 p, vec2 b) {
  vec2 d = abs(p) - b;
  return length(max(d, 0.0)) + min(max(d.x, d.y), 0.0);
}

void main() {
  vec2 uv = vUv * 2.0 - 1.0;

  // Draw circle
  float circle = sdCircle(uv, 0.5);
  vec3 color = vec3(smoothstep(0.0, 0.01, circle));

  // Draw box border
  float box = sdBox(uv, vec2(0.4));
  float border = abs(box) - 0.05;
  color = mix(color, vec3(1.0, 0.0, 0.0), 1.0 - smoothstep(0.0, 0.01, border));

  gl_FragColor = vec4(color, 1.0);
}
```

### Noise Patterns

```glsl
// Simple noise
float hash(vec2 p) {
  return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

float noise(vec2 p) {
  vec2 i = floor(p);
  vec2 f = fract(p);
  f = f * f * (3.0 - 2.0 * f);

  float a = hash(i);
  float b = hash(i + vec2(1.0, 0.0));
  float c = hash(i + vec2(0.0, 1.0));
  float d = hash(i + vec2(1.0, 1.0));

  return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
}

float fbm(vec2 p) {
  float value = 0.0;
  float amplitude = 0.5;
  for (int i = 0; i < 5; i++) {
    value += amplitude * noise(p);
    p *= 2.0;
    amplitude *= 0.5;
  }
  return value;
}

void main() {
  vec2 uv = vUv * 3.0;
  float n = fbm(uv);
  vec3 color = vec3(n);

  gl_FragColor = vec4(color, 1.0);
}
```

### Fresnel Effect (Rim Lighting)

```glsl
varying vec3 vNormal;
varying vec3 vViewPosition;

void main() {
  // Calculate view direction
  vec3 viewDir = normalize(-vViewPosition);

  // Fresnel calculation
  float fresnel = pow(1.0 - dot(viewDir, vNormal), 3.0);

  // Apply fresnel
  vec3 color = vec3(0.0, 0.5, 1.0);
  color = mix(color, vec3(1.0), fresnel);

  gl_FragColor = vec4(color, 1.0);
}
```

### Glow Effect

```glsl
uniform float uTime;
varying vec2 vUv;

void main() {
  vec2 uv = vUv * 2.0 - 1.0;
  float dist = length(uv);

  // Glow calculation
  float glow = 0.02 / dist;
  glow = pow(glow, 1.5);

  // Animated color
  vec3 color = vec3(
    0.5 + 0.5 * sin(uTime),
    0.5 + 0.5 * sin(uTime + 2.0),
    0.5 + 0.5 * sin(uTime + 4.0)
  );

  color *= glow;

  gl_FragColor = vec4(color, 1.0);
}
```

## Complete Shader Example

```tsx
import { shaderMaterial } from '@react-three/drei';
import { extend, useFrame } from '@react-three/fiber';
import { useRef } from 'react';

const HologramMaterial = shaderMaterial(
  {
    uTime: 0,
    uColor: new THREE.Color(0.0, 1.0, 0.5),
    uScanLineDensity: 100.0,
    uScanLineSpeed: 2.0,
  },
  // Vertex shader
  `
    uniform float uTime;
    varying vec2 vUv;
    varying vec3 vPosition;
    varying vec3 vNormal;

    void main() {
      vUv = uv;
      vPosition = position;
      vNormal = normalize(normalMatrix * normal);

      // Holographic wobble
      vec3 pos = position;
      float wobble = sin(pos.y * 2.0 + uTime * 3.0) * 0.02;
      pos.x += wobble;

      gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
    }
  `,
  // Fragment shader
  `
    uniform float uTime;
    uniform vec3 uColor;
    uniform float uScanLineDensity;
    uniform float uScanLineSpeed;
    varying vec2 vUv;
    varying vec3 vPosition;
    varying vec3 vNormal;

    void main() {
      // Scan lines
      float scanLine = sin(vPosition.y * uScanLineDensity + uTime * uScanLineSpeed);
      scanLine = smoothstep(-0.5, 0.5, scanLine);

      // Fresnel effect
      vec3 viewDir = normalize(cameraPosition - vPosition);
      float fresnel = pow(1.0 - abs(dot(viewDir, vNormal)), 2.0);

      // Combine effects
      vec3 color = uColor;
      color *= 0.5 + scanLine * 0.5;
      color += fresnel * 0.5;

      // Add grid pattern
      float grid = step(0.95, fract(vPosition.x * 10.0)) +
                   step(0.95, fract(vPosition.y * 10.0));
      color += grid * 0.2;

      gl_FragColor = vec4(color, 0.3 + fresnel * 0.5);
    }
  `
);

extend({ HologramMaterial });

function HologramMesh() {
  const materialRef = useRef();

  useFrame((state) => {
    if (materialRef.current) {
      materialRef.current.uTime = state.clock.elapsedTime;
    }
  });

  return (
    <mesh>
      <boxGeometry args={[2, 2, 2]} />
      <hologramMaterial ref={materialRef} />
    </mesh>
  );
}
```

## Shader Debugging

```glsl
// Debug UVs
gl_FragColor = vec4(vUv, 0.0, 1.0);

// Debug normals
gl_FragColor = vec4(vNormal * 0.5 + 0.5, 1.0);

// Debug position (normalized)
gl_FragColor = vec4(vPosition * 0.5 + 0.5, 1.0);

// Visualize value as grayscale
float value = /* your calculation */;
gl_FragColor = vec4(vec3(value), 1.0);

// Heat map visualization
vec3 heatmap(float t) {
  return mix(vec3(0.0, 0.0, 1.0),
             mix(vec3(0.0, 1.0, 0.0), vec3(1.0, 0.0, 0.0), t),
             t);
}
```

## Anti-Patterns

❌ **DON'T:**

- Create complex shaders without testing incrementally
- Use if/else for dynamic branching in shaders
- Forget to normalize vectors before dot products
- Use uniforms for static values (use const)

✅ **DO:**

- Build shaders step by step, test each addition
- Use mix() instead of if/else when possible
- Test on mobile hardware
- Add comments to complex shader math

## Checklist

Before finalizing shader:

- [ ] Shader compiles without errors
- [ ] Uniforms properly typed
- [ ] Varyings match between vertex/fragment
- [ ] Performance tested on target hardware
- [ ] Fallback considered for low-end devices
- [ ] Complex shader sections documented

## Reference

- [Book of Shaders](https://thebookofshaders.com/)
- [Shadertoy](https://www.shadertoy.com/) — Shader gallery
- [skills/shader-sdf.md](shader-sdf.md) — SDF functions
- [skills/r3f-materials.md](r3f-materials.md) — Material basics
