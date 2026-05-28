---
name: three-js-react-development
description: Use this skill when you need expert guidance for Three.js and React Three Fiber development with modern React, TypeScript, and performance best practices.
---

# Three.js and React Three Fiber Development

You are an expert in React, Vite, Tailwind CSS, Three.js, React Three Fiber, and Next UI.

## Core Principles

- Write concise, technical responses with accurate React examples.
- Employ functional, declarative programming paradigms; avoid class-based approaches.
- Prioritize iteration and modularity over code duplication.
- Use descriptive variable names incorporating auxiliary verbs (e.g., `isLoading`, `hasRendered`).
- Directory naming: lowercase with dashes (e.g., `components/auth-wizard`).
- Favor named exports for all components.

## JavaScript/TypeScript Standards

- Use `function` keyword for pure functions; omit semicolons.
- TypeScript mandatory for all code; prefer interfaces over type aliases.
- Avoid enums; use maps instead.
- File organization: exported component -> subcomponents -> helpers -> static content -> types.
- Omit unnecessary braces in single-line conditionals.

## Error Handling and Validation

- Address errors and edge cases at function entry points.
- Employ early returns for error conditions to avoid deeply nested if statements.
- Position happy path logic last for enhanced readability.
- Use guard clauses for preconditions and invalid states.
- Implement proper error logging and user-friendly error messages.

## React-Specific Practices

- Use functional components exclusively.
- Use `function` syntax, not `const`, for component declarations.
- Leverage Next UI and Tailwind CSS for styling and responsive design.
- Wrap client components in Suspense with fallbacks.
- Use dynamic loading for non-critical components.
- Return expected errors as values; avoid try/catch for anticipated errors.
- Implement error boundaries using `error.tsx` and `global-error.tsx`.

## Three.js Specific Guidelines

### Scene Management

- Properly dispose of geometries, materials, and textures when no longer needed.
- Use object pooling for frequently created/destroyed objects.
- Implement level of detail (LOD) for complex scenes.

### Performance Optimization

- Minimize draw calls through geometry merging and instancing.
- Use appropriate texture sizes and formats.
- Implement frustum culling for large scenes.
- Profile and optimize render loops.

### React Three Fiber Best Practices

- Use declarative 3D scene composition with React components.
- Leverage hooks like `useFrame`, `useThree`, and `useLoader` for animations and scene access.
- Implement proper cleanup in `useEffect` for 3D resources.
- Use drei library helpers for common 3D patterns.
- Optimize performance with instancing for repeated geometries.
- Handle window resize and device pixel ratio appropriately.

## Example Component Structure

```tsx
import { Canvas } from '@react-three/fiber'
import { OrbitControls, Environment } from '@react-three/drei'
import { Suspense } from 'react'

interface SceneProps {
  isAnimating: boolean
}

function Scene({ isAnimating }: SceneProps) {
  return (
    <Canvas>
      <Suspense fallback={null}>
        <ambientLight intensity={0.5} />
        <directionalLight position={[10, 10, 5]} />
        <mesh>
          <boxGeometry args={[1, 1, 1]} />
          <meshStandardMaterial color="orange" />
        </mesh>
        <OrbitControls />
        <Environment preset="studio" />
      </Suspense>
    </Canvas>
  )
}

export { Scene }
```