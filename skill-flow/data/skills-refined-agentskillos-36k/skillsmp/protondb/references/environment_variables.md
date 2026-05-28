# Environment Variables Reference

Complete reference of environment variables for Linux gaming with Proton.

## AMD GPU Variables

### AMD_VULKAN_ICD
**Values:** `RADV` | `AMDVLK`
**Default:** System default (usually RADV)
**Description:** Force specific Vulkan driver

```bash
AMD_VULKAN_ICD=RADV         # Mesa's open-source driver (recommended)
AMD_VULKAN_ICD=AMDVLK       # AMD's proprietary driver
```

**Use RADV when:** Most games (better performance, more features)
**Use AMDVLK when:** Specific compatibility issues with RADV

### RADV_PERFTEST
**Values:** Comma-separated list of features
**Default:** None
**Description:** Enable experimental RADV performance features

```bash
RADV_PERFTEST=aco                  # ACO shader compiler (now default)
RADV_PERFTEST=aco,nggc             # ACO + NGG culling
RADV_PERFTEST=aco,nggc,rt          # ACO + NGG + Ray tracing
```

**Features:**
- `aco` - AMD Compiler for faster shaders
- `nggc` - NGG culling for better geometry performance
- `rt` - Ray tracing optimizations
- `tccompat` - Texture compression compatibility

### RADV_DEBUG
**Values:** Comma-separated debug options
**Default:** None
**Description:** Debug options and performance tweaks

```bash
RADV_DEBUG=nohiz                   # Disable hierarchical Z-buffer
RADV_DEBUG=novrsflatshading        # Disable VRS flat shading
```

**Use for:** Troubleshooting rendering issues or squeezing max FPS

## DXVK Variables

### DXVK_ASYNC
**Values:** `1` | `0`
**Default:** `0`
**Description:** Enable asynchronous shader compilation

```bash
DXVK_ASYNC=1                       # Enable (recommended)
```

**Effect:** Dramatically reduces stutter, may cause brief visual glitches initially

### DXVK_STATE_CACHE_PATH
**Values:** Directory path
**Default:** `~/.cache/dxvk`
**Description:** Location for shader state cache

```bash
DXVK_STATE_CACHE_PATH=$HOME/.cache/dxvk-state-cache
```

**Effect:** Faster subsequent launches, reduced stutter

### DXVK_HUD
**Values:** Comma-separated HUD options
**Default:** None
**Description:** DXVK performance overlay

```bash
DXVK_HUD=fps                       # Show FPS only
DXVK_HUD=fps,devinfo               # FPS + device info
DXVK_HUD=full                      # All information
```

**Options:**
- `fps` - Frame rate
- `frametimes` - Frame time graph
- `submissions` - GPU submission count
- `drawcalls` - Draw call count
- `pipelines` - Pipeline statistics
- `descriptors` - Descriptor statistics
- `memory` - Memory usage
- `version` - DXVK version
- `api` - D3D API version
- `compiler` - Shader compiler activity
- `devinfo` - Device information

### DXVK_CONFIG_FILE
**Values:** File path
**Default:** None
**Description:** Load DXVK config from file

```bash
DXVK_CONFIG_FILE=$HOME/.config/dxvk.conf
```

**Config format:**
```ini
dxgi.maxFrameLatency = 1
d3d9.maxFrameLatency = 1
```

### DXVK_LOG_LEVEL
**Values:** `none` | `error` | `warn` | `info` | `debug`
**Default:** `info`
**Description:** DXVK logging verbosity

```bash
DXVK_LOG_LEVEL=none                # Disable logging
DXVK_LOG_LEVEL=debug               # Maximum verbosity
```

## VKD3D-Proton Variables

### VKD3D_CONFIG
**Values:** Comma-separated options
**Default:** None
**Description:** VKD3D-Proton configuration

```bash
VKD3D_CONFIG=dxr11                 # DirectX Raytracing 1.1
VKD3D_CONFIG=upload_hvv            # Memory allocation method
```

**Options:**
- `dxr` - Enable DXR (ray tracing)
- `dxr11` - Enable DXR 1.1
- `upload_hvv` - Use host-visible VRAM for uploads

### VKD3D_DEBUG
**Values:** Comma-separated debug options
**Default:** None
**Description:** VKD3D debugging options

```bash
VKD3D_DEBUG=none                   # Disable debugging
VKD3D_DEBUG=warn                   # Show warnings
```

## SDL Variables

### SDL_VIDEODRIVER
**Values:** `wayland` | `x11` | `auto`
**Default:** `auto`
**Description:** Force SDL2 video backend

```bash
SDL_VIDEODRIVER=wayland            # Native Wayland (recommended on Wayland)
SDL_VIDEODRIVER=x11                # XWayland fallback
```

**Use Wayland when:** On Wayland compositor for better performance
**Use X11 when:** Compatibility issues with Wayland

### SDL_AUDIODRIVER
**Values:** `pulseaudio` | `pipewire` | `alsa`
**Default:** `auto`
**Description:** Force SDL2 audio backend

```bash
SDL_AUDIODRIVER=pipewire           # PipeWire (modern)
SDL_AUDIODRIVER=pulseaudio         # PulseAudio
```

## Wayland Variables

### EGL_PLATFORM
**Values:** `wayland` | `x11`
**Default:** Auto-detect
**Description:** Force EGL platform

```bash
EGL_PLATFORM=wayland               # Native Wayland EGL
```

### QT_QPA_PLATFORM
**Values:** `wayland` | `xcb`
**Default:** Auto-detect
**Description:** Qt platform abstraction

```bash
QT_QPA_PLATFORM=wayland            # Qt apps on Wayland
```

### GDK_BACKEND
**Values:** `wayland` | `x11`
**Default:** Auto-detect
**Description:** GTK backend selection

```bash
GDK_BACKEND=wayland                # GTK apps on Wayland
```

## Proton Variables

### PROTON_USE_WINED3D
**Values:** `1` | `0`
**Default:** `0`
**Description:** Use OpenGL instead of Vulkan

```bash
PROTON_USE_WINED3D=1               # Fallback to OpenGL
```

**Use when:** Vulkan issues, very old games, debugging

### PROTON_NO_ESYNC
**Values:** `1` | `0`
**Default:** `0`
**Description:** Disable eventfd-based synchronization

```bash
PROTON_NO_ESYNC=1                  # Disable esync
```

**Use when:** Compatibility issues, file descriptor limits

### PROTON_NO_FSYNC
**Values:** `1` | `0`
**Default:** `0`
**Description:** Disable futex-based synchronization

```bash
PROTON_NO_FSYNC=1                  # Disable fsync
```

**Use when:** Kernel doesn't support fsync, compatibility issues

### PROTON_ENABLE_NVAPI
**Values:** `1` | `0`
**Default:** `0`
**Description:** Enable NVAPI translation for non-NVIDIA GPUs

```bash
PROTON_ENABLE_NVAPI=1              # Enable NVAPI (needed for some games)
```

**Use for:** Games checking NVIDIA-specific features, AMD ray tracing

### PROTON_HIDE_NVIDIA_GPU
**Values:** `1` | `0`
**Default:** `1`
**Description:** Hide GPU from NVAPI

```bash
PROTON_HIDE_NVIDIA_GPU=0           # Don't hide GPU (allow detection)
```

**Use with:** `PROTON_ENABLE_NVAPI=1` on AMD GPUs

### PROTON_LOG
**Values:** `1` | `0`
**Default:** `0`
**Description:** Enable verbose Proton logging

```bash
PROTON_LOG=1                       # Enable logging
```

**Log location:** `$STEAM_DIR/steamapps/compatdata/<APP_ID>/pfx/drive_c/`

### PROTON_DUMP_DEBUG_COMMANDS
**Values:** `1` | `0`
**Default:** `0`
**Description:** Dump debug commands to file

```bash
PROTON_DUMP_DEBUG_COMMANDS=1       # Dump debug info
```

## Mesa Variables

### mesa_glthread
**Values:** `true` | `false`
**Default:** `false`
**Description:** Multi-threaded OpenGL driver

```bash
mesa_glthread=true                 # Enable (better performance)
```

**Use for:** OpenGL games, extra performance on multi-core CPUs

### MESA_VK_WSI_PRESENT_MODE
**Values:** `immediate` | `mailbox` | `fifo` | `fifo_relaxed`
**Default:** `fifo`
**Description:** Vulkan present mode

```bash
MESA_VK_WSI_PRESENT_MODE=mailbox   # Adaptive VSync
```

**Modes:**
- `immediate` - No VSync (tearing possible)
- `mailbox` - Adaptive VSync (best for VRR)
- `fifo` - Standard VSync
- `fifo_relaxed` - Relaxed VSync

### MESA_LOADER_DRIVER_OVERRIDE
**Values:** Driver name
**Default:** Auto-detect
**Description:** Override Mesa driver selection

```bash
MESA_LOADER_DRIVER_OVERRIDE=radeonsi  # Force radeonsi (OpenGL)
```

## VSync Variables

### vblank_mode
**Values:** `0` | `1` | `2` | `3`
**Default:** `1`
**Description:** OpenGL VSync mode

```bash
vblank_mode=0                      # VSync off
vblank_mode=1                      # VSync on
vblank_mode=2                      # Adaptive VSync
vblank_mode=3                      # Application-controlled
```

## Performance Variables

### __GL_THREADED_OPTIMIZATIONS
**Values:** `1` | `0`
**Default:** `0`
**Description:** Enable NVIDIA-style threaded optimizations on Mesa

```bash
__GL_THREADED_OPTIMIZATIONS=1      # Enable
```

**Note:** Use `mesa_glthread=true` instead for Mesa drivers

### __GL_YIELD
**Values:** `NOTHING` | `USLEEP`
**Default:** System default
**Description:** CPU yield behavior

```bash
__GL_YIELD=NOTHING                 # No yielding (better CPU utilization)
```

## Hybrid Graphics Variables

### DRI_PRIME
**Values:** `1` | `0`
**Default:** `0`
**Description:** Select dedicated GPU on hybrid systems

```bash
DRI_PRIME=1                        # Use dedicated GPU
```

**Use on:** Laptops with integrated + dedicated GPU

## Wine Variables

### WINEDEBUG
**Values:** Debug channels
**Default:** None
**Description:** Wine debug output

```bash
WINEDEBUG=-all                     # Disable all debug output (performance)
WINEDEBUG=+fps                     # Show FPS information
WINEDEBUG=+d3d,+vulkan            # Debug D3D and Vulkan
```

### WINEPREFIX
**Values:** Directory path
**Default:** `~/.wine`
**Description:** Wine prefix location

```bash
WINEPREFIX=$HOME/.local/share/wineprefixes/game
```

**Note:** Managed by Steam/Proton, usually don't need to set

## GameMode Variables

GameMode is controlled via config file, not environment variables.

**Config location:** `~/.config/gamemode.ini`

Launch with: `gamemoderun %command%`

## Complete Configuration Examples

### Maximum Performance
```bash
AMD_VULKAN_ICD=RADV \
RADV_PERFTEST=aco,nggc \
DXVK_ASYNC=1 \
RADV_DEBUG=nohiz,novrsflatshading \
mesa_glthread=true \
vblank_mode=0 \
SDL_VIDEODRIVER=wayland \
PROTON_ENABLE_NVAPI=1 \
gamemoderun mangohud %command%
```

### Maximum Compatibility
```bash
AMD_VULKAN_ICD=RADV \
DXVK_ASYNC=1 \
PROTON_USE_WINED3D=1 \
PROTON_NO_ESYNC=1 \
PROTON_NO_FSYNC=1 \
SDL_VIDEODRIVER=x11 \
WINEDEBUG=-all \
%command%
```

### Balanced (Recommended)
```bash
AMD_VULKAN_ICD=RADV \
RADV_PERFTEST=aco \
VKD3D_CONFIG=dxr11 \
DXVK_ASYNC=1 \
SDL_VIDEODRIVER=wayland \
PROTON_ENABLE_NVAPI=1 \
gamemoderun mangohud %command%
```

## Debugging Variables

When troubleshooting, enable logging:
```bash
PROTON_LOG=1 \
DXVK_LOG_LEVEL=debug \
VKD3D_DEBUG=warn \
WINEDEBUG=+fps,+d3d,+vulkan \
%command%
```

Check logs in:
- Proton: `~/.steam/steam/steamapps/compatdata/<APP_ID>/pfx/drive_c/`
- System: `journalctl --user -u steam`
