# Known Issues and Workarounds

Common problems when gaming on Linux with Proton and their solutions, focused on AMD + Wayland + Arch Linux.

## Anti-Cheat Issues

### EasyAntiCheat (EAC)

**Problem:** Many EAC games don't work on Linux

**Check Status:**
- Visit ProtonDB for specific game
- Check https://areweanticheatyet.com/

**Whitelisted Games Work:**
- Apex Legends
- Dead by Daylight
- Fall Guys
- Lost Ark
- War Thunder

**Most EAC Games Don't Work:**
- Fortnite (Epic's decision, not technical)
- Rust (no Linux support enabled)
- New World (no Linux support enabled)

**Solution:**
- No workaround if game not whitelisted
- Developer must enable Linux support
- Check game-specific news for updates

### BattleEye

**Problem:** Similar to EAC, most don't work

**Whitelisted Games:**
- Destiny 2
- Rainbow Six Siege

**Solution:**
- Same as EAC - developer decision
- No technical workaround

### Denuvo Anti-Tamper

**Problem:** Activation limits when switching Proton versions

**Symptoms:**
- "Too many activations" error
- Game won't launch after Proton switch

**Solution:**
```bash
# Stick to one Proton version once activated
# If you must switch:
# 1. Deactivate via game settings (if available)
# 2. Wait 24-48 hours
# 3. Switch Proton version
# 4. Reactivate
```

**Prevention:**
- Choose Proton version carefully before first launch
- Don't experiment with multiple versions
- Use Proton Stable for Denuvo games

**Games Affected:**
- Most AAA releases 2017-2023
- Check store page for Denuvo mention

## Wayland-Specific Issues

### Window Focus Lost

**Problem:** Game opens but can't receive input

**Symptoms:**
- Game window visible but unresponsive
- Keyboard/mouse don't work
- Can't click on game

**Solution 1 - GameScope:**
```bash
gamescope -f -- %command%
```

**Solution 2 - XWayland Fallback:**
```bash
SDL_VIDEODRIVER=x11 %command%
```

**Solution 3 - Compositor Settings:**
For Hyprland, add to config:
```
windowrulev2 = stayfocused, class:^(steam_app_.*)$
```

### Resolution Switching Broken

**Problem:** Game can't change resolution or goes black

**Solution - GameScope with Fixed Resolution:**
```bash
gamescope -f -W 2560 -H 1440 -w 1920 -h 1080 -- %command%
```

- `-W/-H` = output resolution (your monitor)
- `-w/-h` = game resolution

### Mouse Cursor Visible in Game

**Problem:** Desktop cursor shows over game

**Solution:**
```bash
# Try GameScope
gamescope -f -- %command%

# Or XWayland fallback
SDL_VIDEODRIVER=x11 %command%
```

### Screen Recording/Streaming Issues

**Problem:** OBS/streaming apps can't capture Wayland games

**Solution - Use XWayland for game:**
```bash
SDL_VIDEODRIVER=x11 %command%
```

**Or - Use PipeWire screen sharing:**
- Ensure OBS/streaming app supports Wayland + PipeWire
- Update to latest versions
- Use "PipeWire Screen Capture" source

## Performance Issues

### Shader Compilation Stutter

**Problem:** Severe stuttering when new effects appear

**Symptoms:**
- First playthrough stutters badly
- New areas/effects cause hitches
- Gets better over time

**Solution:**
```bash
DXVK_ASYNC=1 %command%
```

**Additional:**
```bash
# Let shaders compile first
# Play game for 30 minutes to build shader cache
# Performance improves dramatically after
```

**Check shader cache:**
```bash
ls ~/.steam/steam/steamapps/shadercache/<APP_ID>/
```

### Consistently Low FPS

**Problem:** Game runs slower than expected

**Check 1 - GPU Performance Level:**
```bash
cat /sys/class/drm/card0/device/power_dpm_force_performance_level
```

Should show `high` during gaming.

**Fix 1 - GameMode:**
```bash
# Ensure GameMode is active
systemctl --user status gamemoded

# Use in launch options
gamemoderun %command%
```

**Check 2 - CPU Governor:**
```bash
cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```

Should show `performance` during gaming (GameMode does this).

**Fix 2 - Mesa Performance:**
```bash
RADV_PERFTEST=aco,nggc DXVK_ASYNC=1 gamemoderun %command%
```

**Check 3 - VSync Enabled:**
```bash
# Disable VSync for testing
vblank_mode=0 %command%
```

### Memory Leaks

**Problem:** Game uses more RAM over time, eventually crashes

**Solution - VKD3D Memory Config:**
```bash
VKD3D_CONFIG=upload_hvv %command%
```

**Monitor memory:**
```bash
# Use MangoHud to watch VRAM/RAM
mangohud %command%
```

**Restart game periodically** if leak persists.

### CPU Bottleneck

**Problem:** GPU not fully utilized, low FPS

**Check:**
```bash
# Use MangoHud to see CPU/GPU usage
mangohud %command%

# If CPU at 100%, GPU at 50-70% → CPU bottleneck
```

**Solutions:**
```bash
# Enable mesa_glthread (OpenGL games)
mesa_glthread=true %command%

# Ensure GameMode active
gamemoderun %command%

# Close background apps
```

## Graphics Issues

### Screen Tearing

**Problem:** Horizontal tears across screen

**Solution 1 - Enable VRR/FreeSync:**
```
# Hyprland config
monitor=DP-1,2560x1440@165,0x0,1,vrr,1

# Sway config
output DP-1 adaptive_sync on
```

**Solution 2 - Force VSync:**
```bash
vblank_mode=1 %command%
```

**Solution 3 - GameScope:**
```bash
gamescope -f -r 165 -- %command%
```

### Black Screen on Launch

**Problem:** Game launches but shows black screen

**Solution 1 - Different Proton Version:**
- Try Proton Experimental
- Try Proton-GE
- Try older Proton Stable

**Solution 2 - Fallback to OpenGL:**
```bash
PROTON_USE_WINED3D=1 %command%
```

**Solution 3 - Disable Compositing:**
```bash
# For X11 compositors (not applicable on Wayland)
# Use GameScope instead:
gamescope -f -- %command%
```

**Check logs:**
```bash
# Enable Proton logging
PROTON_LOG=1 %command%

# Check log file in:
~/.steam/steam/steamapps/compatdata/<APP_ID>/pfx/drive_c/
```

### Graphical Glitches/Artifacts

**Problem:** Visual corruption, missing textures, flickering

**Solution 1 - Different Vulkan Driver:**
```bash
# If using RADV, try AMDVLK
AMD_VULKAN_ICD=AMDVLK %command%

# Or vice versa
AMD_VULKAN_ICD=RADV %command%
```

**Solution 2 - Disable Async:**
```bash
# Some games have issues with async
DXVK_ASYNC=0 %command%
```

**Solution 3 - Update Mesa:**
```bash
sudo pacman -Syu mesa lib32-mesa
```

### Missing Textures

**Problem:** Textures don't load, appear as pink/black

**Solution - Increase VRAM Allocation:**
Check game requirements vs your VRAM.

**Or - OpenGL Fallback:**
```bash
PROTON_USE_WINED3D=1 %command%
```

## Audio Issues

### No Sound

**Problem:** Game launches but no audio

**Check Audio Backend:**
```bash
# Check PipeWire is running
systemctl --user status pipewire pipewire-pulse

# Restart if needed
systemctl --user restart pipewire pipewire-pulse
```

**Solution - Force Audio Driver:**
```bash
SDL_AUDIODRIVER=pipewire %command%
```

**Or:**
```bash
SDL_AUDIODRIVER=pulseaudio %command%
```

### Audio Crackling/Stuttering

**Problem:** Audio pops, clicks, or breaks up

**Solution - Increase Buffer Size:**

Edit `~/.config/pipewire/pipewire.conf.d/custom.conf`:
```conf
context.properties = {
    default.clock.rate = 48000
    default.clock.quantum = 1024
    default.clock.min-quantum = 512
}
```

Restart PipeWire:
```bash
systemctl --user restart pipewire
```

### Surround Sound Not Working

**Problem:** Only stereo output on 5.1/7.1 setup

**Solution - PipeWire Configuration:**

Check PipeWire sees all channels:
```bash
pw-cli list-objects | grep -A 10 "node.name.*sink"
```

May need game-specific audio settings.

## Input Issues

### Controller Not Detected

**Problem:** Game doesn't recognize gamepad

**Solution 1 - Steam Input:**
- Steam Settings → Controller → Enable Steam Input
- Configure controller in Big Picture Mode

**Solution 2 - Verify Device:**
```bash
# Check controller visible
ls /dev/input/js*
evtest
```

**Solution 3 - Permissions:**
```bash
# Add user to input group
sudo usermod -a -G input $USER
# Log out and back in
```

### Mouse Sensitivity Wrong

**Problem:** Mouse too fast/slow in game

**Solution - Disable mouse acceleration:**
```bash
# For Wayland, use compositor settings
# Hyprland example:
input {
    accel_profile = flat
    sensitivity = 0
}
```

**In-game:** Adjust sensitivity settings, disable "enhance pointer precision"

### Keyboard Layout Issues

**Problem:** Keys mapped incorrectly

**Solution:**
```bash
# Ensure correct keyboard layout set in compositor
# Games usually use system layout

# For specific games, may need to change Steam locale
# Steam → Settings → Interface → Language
```

## Multiplayer/Network Issues

### Can't Connect to Multiplayer

**Problem:** Singleplayer works, multiplayer fails

**Check 1 - Firewall:**
```bash
sudo ufw status

# If enabled, may need to allow game ports
sudo ufw allow <port>/tcp
sudo ufw allow <port>/udp
```

**Check 2 - NAT/UPnP:**
- Router may need port forwarding
- Enable UPnP in router settings
- Check game-specific ports

**Check 3 - Anti-Cheat:**
- Verify game supports Linux multiplayer
- Check areweanticheatyet.com

### Voice Chat Not Working

**Problem:** Can't hear others or they can't hear you

**Solution - PipeWire Loopback:**
```bash
# Check microphone works
pw-record --list-targets
```

**Steam Voice Settings:**
- Steam → Settings → Voice
- Test microphone
- Select correct input device

## Installation/Update Issues

### Game Won't Download

**Problem:** Download stalls or fails

**Solution 1 - Clear Download Cache:**
- Steam → Settings → Downloads → Clear Download Cache
- Restart Steam

**Solution 2 - Change Download Region:**
- Steam → Settings → Downloads → Download Region
- Choose geographically close server

**Solution 3 - Check Disk Space:**
```bash
df -h ~
```

### Game Won't Update

**Problem:** Update fails repeatedly

**Solution - Verify Game Files:**
- Right-click game → Properties → Local Files → Verify integrity of game files
- Steam will redownload corrupted files

### Proton Prefix Corrupted

**Problem:** Game worked before, now broken after update

**Solution - Reset Prefix:**
```bash
# Backup saves first!
# Check game's save location (usually in compatdata or Steam Cloud)

# Delete prefix
rm -rf ~/.steam/steam/steamapps/compatdata/<APP_ID>/

# Launch game, Steam recreates prefix
```

## Debugging Steps

### Systematic Troubleshooting

**1. Check ProtonDB:**
- Search for game
- Check rating and reports
- Look for similar hardware configs

**2. Try Different Proton Versions:**
- Stable
- Experimental
- Latest Proton-GE

**3. Test with Minimal Launch Options:**
```bash
# Just the game, no extras
%command%
```

Add options one at a time to isolate issue.

**4. Enable Logging:**
```bash
PROTON_LOG=1 DXVK_LOG_LEVEL=debug %command%
```

Check logs for errors.

**5. Test on X11:**
If using Wayland, test on X11 session to rule out Wayland issues.

**6. Check System Logs:**
```bash
journalctl --user -u steam -f
dmesg | grep -i error
```

Look for GPU, driver, or system errors.

## Getting Help

### Information to Provide

When asking for help, include:

**System info:**
```bash
# GPU
lspci | grep -i vga

# Mesa version
glxinfo | grep "OpenGL version"

# Kernel version
uname -r

# Distribution
cat /etc/os-release | grep PRETTY_NAME
```

**Game info:**
- Steam App ID
- ProtonDB rating
- Proton version tried
- Launch options used

**Error messages:**
- Screenshots of errors
- Relevant log excerpts
- Steps to reproduce

### Community Resources

- **ProtonDB:** https://www.protondb.com
- **Reddit:** /r/linux_gaming, /r/archlinux
- **Steam Forums:** Community Discussions for game
- **Proton GitHub:** https://github.com/ValveSoftware/Proton/issues
- **Arch Wiki:** https://wiki.archlinux.org/title/Steam
- **Discord:** GloriousEggroll Discord, Linux Gaming Discord
