# Three.js Mastery Skill for VS Code GitHub Copilot

Production-grade Three.js development with WebGPU, React Three Fiber, and 2026 best practices.

## 🚀 Installation

### Method 1: Clone to Skills Directory

```bash
# For user-level (all workspaces)
mkdir -p ~/.claude/skills
cd ~/.claude/skills
git clone <this-repo> threejs-mastery

# OR for workspace-level (current project only)
mkdir -p .claude/skills
cd .claude/skills
git clone <this-repo> threejs-mastery
```

### Method 2: Manual Installation

1. Download this repository
2. Copy `threejs-mastery` folder to:
   - **User-level**: `~/.claude/skills/` (all workspaces)
   - **Workspace-level**: `.claude/skills/` in your project root

### Method 3: VS Code Settings

1. Open VS Code Settings (⌘, or Ctrl+,)
2. Search for "chat.useAgentSkills"
3. Enable the setting
4. The skill will auto-activate when working with Three.js code

## 📋 Prerequisites

- VS Code 1.95+ (January 2025 or later)
- GitHub Copilot subscription
- Enable setting: `chat.useAgentSkills: true`

## ✅ Verify Installation

1. Open a JavaScript/TypeScript file
2. Open Copilot Chat (Ctrl+Alt+I or ⌘⌥I)
3. Ask: "Show me available skills"
4. You should see "threejs-mastery" in the list

## 💡 Usage Examples

The skill automatically activates when you:
- Work with Three.js code
- Ask about 3D graphics
- Mention WebGPU, shaders, or rendering
- Use React Three Fiber

### Example Prompts

**"Create a WebGPU renderer with fallback"**
```
Copilot will provide complete code with feature detection,
initialization, and WebGL2 fallback
```

**"Set up a particle system"**
```
Generates optimized particle system with proper geometry
and animation loop
```

**"Optimize my Three.js scene for mobile"**
```
Provides specific optimizations: pixel ratio, shadows,
LOD, texture compression
```

**"Create a React Three Fiber component"**
```
Generates R3F component with hooks, proper refs,
and performance patterns
```

**"Add post-processing bloom effect"**
```
Sets up EffectComposer with UnrealBloomPass and
proper configuration
```

## 📁 What's Included

```
threejs-mastery/
├── SKILL.md                      # Main skill definition
├── examples.md                   # Copy-paste code examples
├── performance-profiler.ts       # Real-time performance monitoring
└── asset-optimizer.js            # Texture/model optimization tool
```

### SKILL.md
Core skill containing:
- Essential learning resources (official docs, courses)
- Modern architecture patterns (2026)
- WebGPU setup with fallback
- Material best practices (PBR workflow)
- Performance optimization techniques
- React Three Fiber patterns
- Shader basics
- Memory management
- Production checklist

### examples.md
Ready-to-use code snippets:
- Basic scene setup
- GLTF model loading
- Particle systems
- Post-processing
- Raycasting/interaction
- Environment maps
- 3D text
- Camera animation
- Simple physics

### Scripts

**performance-profiler.ts** - Monitor your app:
```typescript
import { PerformanceProfiler } from './performance-profiler';

const profiler = new PerformanceProfiler(renderer, scene);

function animate() {
  profiler.begin();
  renderer.render(scene, camera);
  profiler.end();
  
  // Check stats
  const stats = profiler.getStats();
  console.log('FPS:', stats.fps);
}
```

**asset-optimizer.js** - Optimize assets:
```bash
node asset-optimizer.js --input ./public/assets --output ./dist/assets
```

## 🎯 Skill Features

### Automatic Activation
The skill triggers when you:
- Import Three.js (`import * as THREE`)
- Mention WebGPU, shaders, or 3D terms
- Work with .tsx/.jsx files using R3F
- Ask about performance optimization
- Request material or lighting setup

### Code Quality
All generated code includes:
- ✅ TypeScript types
- ✅ Error handling
- ✅ Memory cleanup
- ✅ Performance optimization
- ✅ Mobile considerations
- ✅ WebGPU + WebGL2 fallback

### Best Practices (2026)
- WebGPU as default
- PBR materials (MeshPhysicalMaterial)
- Proper texture compression
- LOD systems
- Object pooling
- Instancing
- Proper disposal patterns

## 🎓 Learning Path

The skill teaches progressively:

1. **Setup** → WebGPU renderer, scene basics
2. **Materials** → PBR workflow, textures
3. **Performance** → LOD, instancing, optimization
4. **React** → R3F patterns, hooks
5. **Advanced** → Shaders, compute, physics

## 🔧 Configuration

### Enable Skill
In VS Code settings.json:
```json
{
  "chat.useAgentSkills": true
}
```

### Skill Locations
Copilot checks these locations:
1. `~/.claude/skills/` (user-level)
2. `.claude/skills/` (workspace-level)
3. `.github/skills/` (repository-level)

## 🌟 Tips for Best Results

### Be Specific
❌ "Make a 3D scene"
✅ "Create a Three.js scene with WebGPU renderer, orbital camera, and PBR materials"

### Mention Context
❌ "Optimize performance"
✅ "Optimize my Three.js scene for mobile devices using LOD and instancing"

### Use Code Context
Select existing code before asking questions - Copilot will use it as context

### Follow-up Questions
Ask for clarification or alternatives:
- "Show alternative using React Three Fiber"
- "Add error handling"
- "Optimize for mobile"

## 📊 What to Expect

### Code Quality
- Production-ready patterns
- TypeScript definitions
- Error boundaries
- Cleanup on disposal
- Performance optimizations

### Performance Targets
Generated code aims for:
- 60 FPS on target hardware
- <100 draw calls
- <500MB memory usage
- Proper LOD implementation
- Mobile-friendly defaults

## 🐛 Troubleshooting

### Skill Not Activating

1. Check setting: `chat.useAgentSkills: true`
2. Verify location: `~/.claude/skills/threejs-mastery/SKILL.md` exists
3. Restart VS Code
4. Try explicit prompt: "Using Three.js Mastery skill..."

### Outdated Code

1. Check Three.js version: `npm list three`
2. Update to latest: `npm install three@latest`
3. Skill targets Three.js r170+ (2026)

### Wrong Patterns

The skill teaches 2026 best practices:
- WebGPU (not WebGL1)
- MeshPhysicalMaterial (not MeshLambertMaterial)
- TypeScript (not plain JS)
- Modern bundlers (Vite, not Webpack 4)

## 🔄 Updates

The skill reflects Three.js state as of January 2026:
- Three.js r170+
- WebGPU stable
- React Three Fiber v9+
- Modern browser APIs

## 📚 Additional Resources

### Official Documentation
- Three.js Docs: https://threejs.org/docs/
- WebGPU Fundamentals: https://webgpufundamentals.org/
- React Three Fiber: https://docs.pmnd.rs/react-three-fiber/

### Courses
- Three.js Journey (Bruno Simon): https://threejs-journey.com/
- Discover Three.js: https://discoverthreejs.com/

### Community
- Three.js Discourse: https://discourse.threejs.org/
- GitHub Discussions: https://github.com/mrdoob/three.js/discussions

## 🤝 Contributing

Found improvements?
1. Fork the repository
2. Add to SKILL.md or examples.md
3. Test with Copilot
4. Submit pull request

## 📝 License

MIT License - Use freely in your projects

## 🆘 Support

Issues? Questions?
1. Check examples.md for code snippets
2. Review SKILL.md for patterns
3. Ask Copilot: "Explain this Three.js pattern"
4. Open GitHub issue

---

**Built for the Three.js community** 🚀

Version: 2026.1 | Three.js r170+ | WebGPU | React Three Fiber v9+
