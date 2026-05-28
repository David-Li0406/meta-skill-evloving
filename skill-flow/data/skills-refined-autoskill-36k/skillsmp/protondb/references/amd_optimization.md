# AMD GPU + Wayland Optimization

Comprehensive guide for optimizing gaming performance on AMD GPUs with Wayland on Arch Linux.

## Hardware Context

This guide is optimized for:
- **GPU:** AMD Radeon RX 6000/7000 series (RDNA 2/3)
- **CPU:** AMD Ryzen 5000/7000/9000 series
- **Display Server:** Wayland (Hyprland, Sway, GNOME Wayland, KDE Wayland)
- **Distribution:** Arch Linux (also applies to Manjaro, EndeavourOS)

## Core Environment Variables

### AMD GPU Configuration

**Force RADV Driver:**
```bash
AMD_VULKAN_ICD=RADV
```
- Uses Mesa's RADV Vulkan driver (open-source)
- Default for AMD GPUs on Linux
- Better performance than AMDVLK (proprietary alternative)

**Enable ACO Shader Compiler:**
```bash
RADV_PERFTEST=aco
```
- ACO (AMD Compiler) for faster shader compilation
- Significantly reduces shader stutter
- Improves frame times
- Now default in recent Mesa versions, but explicit is safe

**Ray Tracing Support:**
```bash
VKD3D_CONFIG=dxr11
```
- Enables DirectX Raytracing (DXR) support
- Required for games with ray tracing
- Works on RDNA 2+ (RX 6000/7000 series)

### DXVK/VKD3D Configuration

**Async Shader Compilation:**
```bash
DXVK_ASYNC=1
```
- Compiles shaders asynchronously in background
- Dramatically reduces stutter during gameplay
- May cause brief visual artifacts initially (worth the trade-off)
- Essential for smooth experience on first launch

**Memory Management:**
```bash
VKD3D_CONFIG=upload_hvv
```
- Use when game has memory allocation issues
- Helps with DirectX 12 games via VKD3D-Proton
- Not needed for most games

**DXVK State Cache:**
```bash
DXVK_STATE_CACHE_PATH=$HOME/.cache/dxvk-state-cache
```
- Saves compiled shader state cache
- Speeds up subsequent launches
- Reduces stutter on replays

### Wayland-Specific Settings

**Force Wayland for SDL2:**
```bash
SDL_VIDEODRIVER=wayland
```
- Uses native Wayland for SDL2 games
- Better performance than XWayland
- Proper fractional scaling
- Reduced input latency

**Qt Applications:**
```bash
QT_QPA_PLATFORM=wayland
```
- Forces Qt apps to use Wayland
- Needed for some game launchers

**Wayland EGL:**
```bash
EGL_PLATFORM=wayland
```
- Forces EGL to use Wayland backend
- Helps with some OpenGL games

### NVAPI Translation

**Enable NVAPI for AMD:**
```bash
PROTON_ENABLE_NVAPI=1
PROTON_HIDE_NVIDIA_GPU=0
```
- Translates NVIDIA-specific API calls
- Needed for games checking for NVIDIA features
- Allows games to detect GPU properly
- Enables features like DLSS alternatives (FSR)

## Complete Launch Option Presets

### Default (Balanced)

Recommended starting point for most games:
```bash
AMD_VULKAN_ICD=RADV RADV_PERFTEST=aco VKD3D_CONFIG=dxr11 DXVK_ASYNC=1 SDL_VIDEODRIVER=wayland gamemoderun mangohud %command%
```

**Use for:** Most modern games with good Proton support

### Performance (Maximum FPS)

Optimized for competitive gaming and high frame rates:
```bash
AMD_VULKAN_ICD=RADV RADV_PERFTEST=aco,nggc DXVK_ASYNC=1 RADV_DEBUG=nohiz,novrsflatshading mesa_glthread=true vblank_mode=0 SDL_VIDEODRIVER=wayland gamemoderun %command%
```

**Use for:** Competitive multiplayer, games where FPS matters most

**Additional flags:**
- `RADV_PERFTEST=nggc` - NGG culling for better geometry performance
- `RADV_DEBUG=nohiz,novrsflatshading` - Disable features for max FPS
- `mesa_glthread=true` - Multi-threaded GL driver
- `vblank_mode=0` - Disable VSync

### Compatibility (Maximum Stability)

For problematic games that need extra compatibility:
```bash
AMD_VULKAN_ICD=RADV DXVK_ASYNC=1 PROTON_USE_WINED3D=1 PROTON_NO_ESYNC=1 PROTON_NO_FSYNC=1 SDL_VIDEODRIVER=x11 %command%
```

**Use for:** Old games, games with known issues, broken Vulkan support

**Additional flags:**
- `PROTON_USE_WINED3D=1` - Use OpenGL instead of Vulkan
- `PROTON_NO_ESYNC=1` - Disable eventfd-based sync
- `PROTON_NO_FSYNC=1` - Disable futex-based sync
- `SDL_VIDEODRIVER=x11` - Fallback to XWayland

### Wayland Native (Full Wayland)

For games with excellent Wayland support:
```bash
AMD_VULKAN_ICD=RADV RADV_PERFTEST=aco VKD3D_CONFIG=dxr11 DXVK_ASYNC=1 SDL_VIDEODRIVER=wayland EGL_PLATFORM=wayland QT_QPA_PLATFORM=wayland gamescope -f -W 2560 -H 1440 -- gamemoderun mangohud %command%
```

**Use for:** Games that work perfectly on Wayland, want native experience

**Includes gamescope:**
- `-f` - Fullscreen
- `-W 2560 -H 1440` - Your native resolution
- Provides better alt-tab, fractional scaling, VRR control

### Ray Tracing (RDNA 2+)

For games with ray tracing support:
```bash
AMD_VULKAN_ICD=RADV RADV_PERFTEST=aco,rt VKD3D_CONFIG=dxr11 DXVK_ASYNC=1 PROTON_ENABLE_NVAPI=1 SDL_VIDEODRIVER=wayland gamemoderun mangohud %command%
```

**Use for:** Games with DXR/ray tracing (RX 6000/7000 series)

**Additional flags:**
- `RADV_PERFTEST=rt` - Enable ray tracing optimizations
- `VKD3D_CONFIG=dxr11` - DXR 1.1 support
- `PROTON_ENABLE_NVAPI=1` - For RT feature detection

## Performance Tools

### GameMode

CPU governor and process priority optimization.

**Installation:**
```bash
sudo pacman -S gamemode lib32-gamemode
systemctl --user enable --now gamemoded.service
```

**Usage in launch options:**
```bash
gamemoderun %command%
```

**Configuration:** `~/.config/gamemode.ini`
```ini
[general]
renice=10

[gpu]
apply_gpu_optimisations=accept_responsibility
gpu_device=0
amd_performance_level=high
```

### MangoHud

Performance overlay for monitoring FPS, temps, CPU/GPU usage.

**Installation:**
```bash
sudo pacman -S mangohud lib32-mangohud
```

**Usage in launch options:**
```bash
mangohud %command%
```

**Configuration:** `~/.config/MangoHud/MangoHud.conf`
```ini
fps
gpu_stats
cpu_stats
gpu_temp
cpu_temp
vram
ram
frame_timing=1
engine_version
vulkan_driver
```

**Keybinds:**
- `Shift+F12` - Toggle overlay
- `Shift+F2` - Change position
- `Shift+F4` - Reload config

### GameScope

Wayland compositor specifically for gaming.

**Installation:**
```bash
sudo pacman -S gamescope
```

**Common usage patterns:**

**Fullscreen at native resolution:**
```bash
gamescope -f -W 2560 -H 1440 -- %command%
```

**Windowed mode:**
```bash
gamescope -W 1920 -H 1080 -w 1920 -h 1080 -- %command%
```

**With frame rate limit:**
```bash
gamescope -f -W 2560 -H 1440 -r 144 -- %command%
```

**With upscaling (FSR):**
```bash
gamescope -f -W 2560 -H 1440 -w 1920 -h 1080 -F fsr -- %command%
```

**Flags:**
- `-f` - Fullscreen
- `-W/-H` - Output resolution
- `-w/-h` - Game resolution
- `-r` - Frame rate limit
- `-F fsr` - Enable FSR upscaling
- `-U` - Unlock refresh rate (VRR)

### Combination Example

Complete launch option with all tools:
```bash
gamescope -f -W 2560 -H 1440 -r 165 -U -- AMD_VULKAN_ICD=RADV RADV_PERFTEST=aco VKD3D_CONFIG=dxr11 DXVK_ASYNC=1 SDL_VIDEODRIVER=wayland gamemoderun mangohud %command%
```

## AMD-Specific Features

### FidelityFX Super Resolution (FSR)

AMD's upscaling technology (works on any GPU).

**In-Game FSR:**
- Enable in game settings if available
- Quality modes: Ultra Quality > Quality > Balanced > Performance
- Better than running at lower native resolution

**GameScope FSR:**
```bash
gamescope -F fsr -w 1920 -h 1080 -W 2560 -H 1440 -- %command%
```
- Render at 1920×1080, upscale to 2560×1440
- Significant performance boost with minimal quality loss

### Variable Refresh Rate (VRR)

Enable FreeSync/Adaptive Sync for smooth gameplay.

**Hyprland configuration:**
```
monitor=DP-1,2560x1440@165,0x0,1,vrr,1
```

**GameScope with VRR:**
```bash
gamescope -f -U -- %command%
```
- `-U` unlocks refresh rate
- Uses VRR if monitor supports it

### RADV Performance Levels

Set GPU performance mode for gaming.

**Temporary (per-game):**
```bash
echo "high" | sudo tee /sys/class/drm/card0/device/power_dpm_force_performance_level
```

**Via GameMode:** Configure in `gamemode.ini` (recommended)

**Levels:**
- `auto` - Default balanced mode
- `high` - Maximum performance
- `low` - Power saving

## Wayland Compositor-Specific Settings

### Hyprland

**Configuration for gaming:**
```
# Reduce latency
misc {
    vrr = 1
    vfr = false
}

# Disable effects for games
windowrulev2 = immediate, class:^(steam_app_.*)$
windowrulev2 = noborder, class:^(steam_app_.*)$
windowrulev2 = noblur, class:^(steam_app_.*)$
windowrulev2 = noshadow, class:^(steam_app_.*)$
```

### Sway

**Configuration for gaming:**
```
# Full performance for Steam games
for_window [class="steam_app_.*"] {
    border none
    fullscreen enable
}

# VRR
output DP-1 adaptive_sync on
```

### GNOME Wayland

Enable VRR in settings:
```bash
gsettings set org.gnome.mutter experimental-features "['variable-refresh-rate']"
```

### KDE Plasma Wayland

VRR available in System Settings → Display Configuration → Enable Adaptive Sync

## Troubleshooting AMD + Wayland

### Window Focus Issues

**Problem:** Game loses focus, can't capture input

**Solution 1:** Use GameScope
```bash
gamescope -f -- %command%
```

**Solution 2:** Fallback to XWayland
```bash
SDL_VIDEODRIVER=x11 %command%
```

### Performance Lower Than Expected

**Check GPU performance level:**
```bash
cat /sys/class/drm/card0/device/power_dpm_force_performance_level
```

**Should be `high` during gaming**

**Verify GameMode is active:**
```bash
gamemoded -s
```

**Check CPU governor:**
```bash
cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```

**Should be `performance` during gaming**

### Stuttering Issues

**Enable DXVK_ASYNC:**
```bash
DXVK_ASYNC=1 %command%
```

**Check shader cache:**
```bash
ls ~/.steam/steam/steamapps/shadercache/
```

**First launch always stutters** - wait for shader compilation

### Screen Tearing

**Enable VRR in compositor config**

**Or force VSync:**
```bash
vblank_mode=1 %command%
```

### Missing Ray Tracing

**Verify GPU supports it:**
- RX 6000/7000 series only

**Enable in launch options:**
```bash
VKD3D_CONFIG=dxr11 RADV_PERFTEST=rt PROTON_ENABLE_NVAPI=1 %command%
```

**Check in-game settings** - may need to enable separately

## Monitoring and Benchmarking

### Check FPS in Real-Time

Use MangoHud:
```bash
mangohud %command%
```

### Log Performance Data

```bash
MANGOHUD_OUTPUT=fps.log MANGOHUD_LOG_DURATION=60 mangohud %command%
```

Logs FPS data for 60 seconds to `fps.log`

### Compare Configurations

Benchmark with different launch options:
```bash
# Test 1: Default
mangohud %command%

# Test 2: Performance
RADV_PERFTEST=aco,nggc mangohud %command%

# Check mangohud logs for average FPS
```

## Best Practices Summary

1. **Start with default preset** - works for most games
2. **Enable GameMode and MangoHud** - always beneficial
3. **Use DXVK_ASYNC=1** - essential for smooth experience
4. **Try GameScope for problematic games** - solves many Wayland issues
5. **Keep Mesa updated** - `sudo pacman -Syu mesa`
6. **Monitor performance** - use MangoHud to identify bottlenecks
7. **Check ProtonDB** - others may have better configs for specific games
8. **Test incrementally** - add optimizations one at a time
