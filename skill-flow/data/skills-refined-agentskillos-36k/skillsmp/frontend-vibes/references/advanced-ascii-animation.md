# Advanced ASCII Animation: 2D Video/Image to ASCII Grid

Comprehensive guide to creating performant animated ASCII art effects using WebGL-based rendering. This reference covers multiple implementation approaches, complete code examples, performance optimization, and troubleshooting.

## Why WebGL for ASCII Animation?

**DOM Manipulation Limitations:**
Rendering ASCII art by manipulating individual DOM elements (creating a `<span>` for each character) becomes prohibitively expensive at scale. A typical 80x40 character grid requires 3,200 DOM elements. At 60fps, updating positions, colors, or content creates severe performance bottlenecks.

**WebGL Advantages:**
- Render entire grid as single texture operation
- GPU handles parallel pixel processing
- Achieve 60fps even with complex effects
- Scales to large character grids (100x60+)
- Enables video-rate ASCII conversion

## Approach 1: PixiJS + @pixi/react (Recommended)

PixiJS provides a production-ready 2D WebGL renderer with React bindings. This is the most accessible approach for React developers.

### Complete Implementation

**1. Install Dependencies**

```bash
npm install pixi.js @pixi/react
```

**2. Create ASCII Filter (Custom Fragment Shader)**

```typescript
// asciiFilter.ts
import { Filter } from "pixi.js";

const ASCII_CHARS = " .:-=+*#%@";

export function createAsciiFilter(cellSize = 8, charSet = ASCII_CHARS) {
  const fragmentShader = `
    precision mediump float;

    varying vec2 vTextureCoord;
    uniform sampler2D uSampler;
    uniform vec2 resolution;
    uniform float cellSize;
    uniform float time;
    uniform float charCount;

    // Luminance calculation (ITU-R BT.709)
    float luminance(vec3 color) {
      return dot(color, vec3(0.2126, 0.7152, 0.0722));
    }

    void main() {
      // Calculate cell coordinates
      vec2 uv = vTextureCoord * resolution;
      vec2 cell = floor(uv / cellSize) * cellSize;
      vec2 cellCenter = cell + cellSize * 0.5;
      vec2 sampleUV = cellCenter / resolution;

      // Sample source texture at cell center
      vec3 color = texture2D(uSampler, sampleUV).rgb;
      float lum = luminance(color);

      // Add animated flicker for CRT effect
      float flicker = 0.05 * sin(time * 2.0 + cellCenter.x * 0.1 + cellCenter.y * 0.05);
      lum = clamp(lum + flicker, 0.0, 1.0);

      // Quantize luminance to character levels
      float charIndex = floor(lum * charCount);
      float quantized = charIndex / charCount;

      // Apply color (maintain original hue, adjust brightness)
      vec3 asciiColor = color * (quantized / lum);

      gl_FragColor = vec4(asciiColor, 1.0);
    }
  `;

  return new Filter(undefined, fragmentShader, {
    resolution: { x: 1, y: 1 },
    cellSize,
    time: 0,
    charCount: charSet.length,
  });
}
```

**3. Create React Component**

```typescript
// AsciiImage.tsx
import { Stage, Sprite, useTick } from "@pixi/react";
import { Texture } from "pixi.js";
import { useEffect, useRef } from "react";
import { createAsciiFilter } from "./asciiFilter";

interface AsciiImageProps {
  src: string;
  width?: number;
  height?: number;
  cellSize?: number;
  animated?: boolean;
}

export function AsciiImage({
  src,
  width = 600,
  height = 400,
  cellSize = 8,
  animated = true,
}: AsciiImageProps) {
  const filterRef = useRef(createAsciiFilter(cellSize));

  useEffect(() => {
    filterRef.current.uniforms.resolution = { x: width, y: height };
  }, [width, height]);

  useTick((delta) => {
    if (animated) {
      filterRef.current.uniforms.time += delta * 0.05;
    }
  });

  return (
    <Stage
      width={width}
      height={height}
      options={{
        background: "#131313", // Warm black background
        antialias: false, // Sharp pixels for ASCII aesthetic
      }}
    >
      <Sprite
        texture={Texture.from(src)}
        width={width}
        height={height}
        filters={[filterRef.current]}
      />
    </Stage>
  );
}
```

**4. Usage Example**

```typescript
// App.tsx
import { AsciiImage } from "./AsciiImage";

export default function App() {
  return (
    <div className="min-h-screen bg-[#131313] flex items-center justify-center">
      <AsciiImage
        src="/images/portrait.jpg"
        width={800}
        height={600}
        cellSize={10}
        animated={true}
      />
    </div>
  );
}
```

### Video Source Example

```typescript
// AsciiVideo.tsx
import { Stage, Sprite, useTick } from "@pixi/react";
import { Texture, VideoResource } from "pixi.js";
import { useEffect, useRef, useState } from "react";
import { createAsciiFilter } from "./asciiFilter";

interface AsciiVideoProps {
  src: string;
  width?: number;
  height?: number;
  cellSize?: number;
}

export function AsciiVideo({
  src,
  width = 640,
  height = 480,
  cellSize = 8,
}: AsciiVideoProps) {
  const [texture, setTexture] = useState<Texture | null>(null);
  const filterRef = useRef(createAsciiFilter(cellSize));

  useEffect(() => {
    // Create video element
    const video = document.createElement("video");
    video.src = src;
    video.loop = true;
    video.muted = true;
    video.playsInline = true;

    // Create texture from video
    const videoResource = new VideoResource(video, {
      autoPlay: true,
      updateFPS: 30, // Match video framerate
    });
    const videoTexture = Texture.from(videoResource);

    setTexture(videoTexture);
    filterRef.current.uniforms.resolution = { x: width, y: height };

    return () => {
      videoTexture.destroy(true);
      video.remove();
    };
  }, [src, width, height]);

  useTick((delta) => {
    filterRef.current.uniforms.time += delta * 0.05;
  });

  if (!texture) return null;

  return (
    <Stage
      width={width}
      height={height}
      options={{ background: "#131313", antialias: false }}
    >
      <Sprite
        texture={texture}
        width={width}
        height={height}
        filters={[filterRef.current]}
      />
    </Stage>
  );
}
```

## Approach 2: Three.js with ShaderMaterial

For 3D scenes or more complex shader effects, use Three.js. This approach offers more control but higher complexity.

### Implementation Outline

```typescript
// AsciiThreeScene.tsx
import { useRef, useEffect } from "react";
import * as THREE from "three";

export function AsciiThreeScene() {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    // Setup scene, camera, renderer
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, 800 / 600, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: false });
    renderer.setSize(800, 600);
    containerRef.current.appendChild(renderer.domElement);

    // Create plane with ASCII shader material
    const geometry = new THREE.PlaneGeometry(2, 2);
    const material = new THREE.ShaderMaterial({
      uniforms: {
        tDiffuse: { value: null },
        resolution: { value: new THREE.Vector2(800, 600) },
        cellSize: { value: 8.0 },
        time: { value: 0.0 },
      },
      vertexShader: `
        varying vec2 vUv;
        void main() {
          vUv = uv;
          gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
      `,
      fragmentShader: `
        uniform sampler2D tDiffuse;
        uniform vec2 resolution;
        uniform float cellSize;
        uniform float time;
        varying vec2 vUv;

        float luminance(vec3 color) {
          return dot(color, vec3(0.2126, 0.7152, 0.0722));
        }

        void main() {
          vec2 uv = vUv * resolution;
          vec2 cell = floor(uv / cellSize) * cellSize;
          vec2 sampleUV = (cell + cellSize * 0.5) / resolution;

          vec3 color = texture2D(tDiffuse, sampleUV).rgb;
          float lum = luminance(color);

          float levels = 10.0;
          float quantized = floor(lum * levels) / levels;

          gl_FragColor = vec4(vec3(quantized), 1.0);
        }
      `,
    });

    const mesh = new THREE.Mesh(geometry, material);
    scene.add(mesh);

    camera.position.z = 1;

    // Animation loop
    function animate() {
      requestAnimationFrame(animate);
      material.uniforms.time.value += 0.01;
      renderer.render(scene, camera);
    }
    animate();

    return () => {
      renderer.dispose();
      containerRef.current?.removeChild(renderer.domElement);
    };
  }, []);

  return <div ref={containerRef} />;
}
```

## Approach 3: Regl (Functional WebGL)

For maximum control with minimal abstraction, use regl with react-regl.

### Installation

```bash
npm install regl react-regl
```

### Implementation

```typescript
// AsciiRegl.tsx
import { useEffect, useRef } from "react";
import createREGL from "regl";

export function AsciiRegl({ src }: { src: string }) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (!canvasRef.current) return;

    const regl = createREGL(canvasRef.current);
    const image = new Image();
    image.src = src;

    image.onload = () => {
      const texture = regl.texture(image);

      const drawAscii = regl({
        frag: `
          precision mediump float;
          uniform sampler2D texture;
          uniform vec2 resolution;
          uniform float cellSize;
          varying vec2 uv;

          float luminance(vec3 c) {
            return dot(c, vec3(0.2126, 0.7152, 0.0722));
          }

          void main() {
            vec2 cell = floor(uv * resolution / cellSize) * cellSize;
            vec2 sampleUV = (cell + cellSize * 0.5) / resolution;
            vec3 color = texture2D(texture, sampleUV).rgb;
            float lum = luminance(color);
            gl_FragColor = vec4(vec3(floor(lum * 10.0) / 10.0), 1.0);
          }
        `,
        vert: `
          precision mediump float;
          attribute vec2 position;
          varying vec2 uv;
          void main() {
            uv = position * 0.5 + 0.5;
            gl_Position = vec4(position, 0, 1);
          }
        `,
        attributes: {
          position: [-1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1],
        },
        uniforms: {
          texture,
          resolution: [800, 600],
          cellSize: 8,
        },
        count: 6,
      });

      regl.frame(() => {
        regl.clear({ color: [0.07, 0.07, 0.07, 1] });
        drawAscii();
      });
    };

    return () => {
      regl.destroy();
    };
  }, [src]);

  return <canvas ref={canvasRef} width={800} height={600} />;
}
```

## Advanced Effects

### Scanline Overlay

Add horizontal scanlines for CRT monitor aesthetic:

```glsl
// Add to fragment shader
float scanline = sin(uv.y * resolution.y * 0.5) * 0.1;
vec3 asciiColor = color * (quantized / lum) * (1.0 - scanline);
```

### Color Palette Mapping

Map luminance to custom color palette:

```glsl
uniform vec3 palette[4];
uniform int paletteSize;

void main() {
  // ... calculate lum ...

  int index = int(floor(lum * float(paletteSize)));
  vec3 paletteColor = palette[clamp(index, 0, paletteSize - 1)];

  gl_FragColor = vec4(paletteColor, 1.0);
}
```

### Dithering for More Detail

Apply Floyd-Steinberg dithering:

```glsl
// Requires multi-pass rendering or compute shader
// Simplified ordered dithering:
float dither = mod(uv.x + uv.y, 2.0) * 0.05;
float lum = luminance(color) + dither;
```

## Performance Optimization

### Cell Size Tuning

- **Large cells (12-16px)**: Lower GPU load, chunkier aesthetic, 60fps on mobile
- **Medium cells (8-10px)**: Balanced detail and performance, recommended default
- **Small cells (4-6px)**: High detail, higher GPU load, desktop only

### Resolution Scaling

Render at lower resolution, upscale with CSS:

```typescript
<Stage
  width={400}  // Render resolution
  height={300}
  options={{ background: "#131313" }}
  style={{
    width: "800px",  // Display size
    height: "600px",
    imageRendering: "pixelated", // Crisp upscaling
  }}
>
```

### Frame Rate Control

For video sources, match update FPS to video framerate (typically 24-30fps):

```typescript
const videoResource = new VideoResource(video, {
  autoPlay: true,
  updateFPS: 30, // Don't update faster than source
});
```

### Texture Caching

Cache created textures to avoid recreation:

```typescript
const textureCache = new Map<string, Texture>();

function getTexture(src: string): Texture {
  if (!textureCache.has(src)) {
    textureCache.set(src, Texture.from(src));
  }
  return textureCache.get(src)!;
}
```

## Troubleshooting

### Issue: Flickering or Tearing

**Cause:** Texture not synchronized with render loop

**Solution:** Use `useTick` hook properly, ensure video resource updates match frame rate

```typescript
useTick((delta) => {
  // Update time uniform consistently
  filterRef.current.uniforms.time += delta * 0.05;
}, true); // Priority true for consistent updates
```

### Issue: Poor Performance on Mobile

**Cause:** Too small cell size or too high resolution

**Solutions:**
- Increase cell size to 10-12px on mobile
- Reduce canvas resolution (render at 50-75% display size)
- Disable animation on low-end devices:

```typescript
const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
const cellSize = isMobile ? 12 : 8;
const animated = !isMobile;
```

### Issue: Colors Look Washed Out

**Cause:** Incorrect luminance calculation or quantization

**Solution:** Use ITU-R BT.709 luminance weights, preserve color ratio:

```glsl
// Good
vec3 asciiColor = color * (quantized / max(lum, 0.01));

// Bad - loses color information
vec3 asciiColor = vec3(quantized);
```

### Issue: Video Not Playing

**Cause:** Browser autoplay policies or missing video attributes

**Solution:** Ensure video is muted and has playsInline:

```typescript
video.muted = true;       // Required for autoplay
video.playsInline = true; // Required for iOS
video.loop = true;
```

### Issue: Memory Leak with Video

**Cause:** Video texture not properly destroyed

**Solution:** Clean up resources in useEffect return:

```typescript
useEffect(() => {
  const videoTexture = Texture.from(videoResource);

  return () => {
    videoTexture.destroy(true);  // Destroy base texture too
    video.pause();
    video.src = "";
    video.remove();
  };
}, [src]);
```

## Character Set Variations

Experiment with different character sets for varied aesthetics:

```typescript
// Classic ASCII (light to dark)
const CLASSIC = " .:-=+*#%@";

// Block characters (smooth gradients)
const BLOCKS = " ░▒▓█";

// Technical (cyberpunk aesthetic)
const TECHNICAL = " ·:;=+*#@";

// Binary aesthetic
const BINARY = " 01";

// Minimal (high contrast)
const MINIMAL = " .:@";
```

Pass to `createAsciiFilter(cellSize, charSet)` to customize appearance.

## Integration with React Spring

Animate ASCII parameters using react-spring:

```typescript
import { useSpring, animated } from "@react-spring/web";

const [spring, api] = useSpring(() => ({
  cellSize: 8,
  config: { tension: 300, friction: 25 },
}));

// Animate on hover
const handleMouseEnter = () => {
  api.start({ cellSize: 4 }); // Increase detail
};

const handleMouseLeave = () => {
  api.start({ cellSize: 8 }); // Reset
};

// Update filter uniforms with animated value
useEffect(() => {
  const unsubscribe = spring.cellSize.onChange((value) => {
    filterRef.current.uniforms.cellSize = value;
  });
  return unsubscribe;
}, [spring]);
```

## Resources

- **PixiJS Documentation**: https://pixijs.com/guides
- **PixiJS Filters Guide**: https://pixijs.io/guides/basics/filters.html
- **@pixi/react API**: https://react.pixijs.io
- **WebGL Shader Reference**: https://www.khronos.org/opengl/wiki/OpenGL_Shading_Language
- **Regl Documentation**: https://github.com/regl-project/regl/blob/gh-pages/API.md
- **ASCII Art Shader Examples**: https://www.shadertoy.com/results?query=ascii

## Next Steps

After implementing basic ASCII animation:
1. Experiment with different character sets and palettes
2. Add interactive controls (cell size slider, animation toggle)
3. Combine with other effects (scanlines, chromatic aberration, bloom)
4. Optimize for production (code splitting, lazy loading textures)
5. Consider accessibility (provide alternative views for users with visual impairments)
