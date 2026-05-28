# Streamer Bait Design - Sharp Edges

## DMCA Takedowns Kill Streamer Adoption

### **Id**
dmca-takedown-risk
### **Severity**
critical
### **Description**
  Licensed music in your game = muted VODs, deleted videos, banned accounts. Streamers will avoid your game entirely if DMCA risk exists. One strike can ruin a creator's livelihood.
  
### **Detection Pattern**
music|soundtrack|audio|licensed
### **Symptoms**
  - Streamers decline keys
  - "Is this DMCA safe?" in every review
  - Muted sections in VODs
### **Solution**
  1. Ship with Streamer Mode toggle
  2. Include royalty-free alternative soundtrack
  3. Use StreamBeats, Pretzel, or commission original
  4. Test with actual streamers before launch
  5. CD Projekt RED approach: make ALL audio safe
  
### **References**
  - https://www.twitch.tv/p/en/legal/dmca-guidelines/

## Stream Sniping Ruins Multiplayer Experiences

### **Id**
stream-sniping-destroys-experience
### **Severity**
high
### **Description**
  Viewers join streamer's games to grief, cheat, or troll. Adds 5+ minute stream delay = kills chat interaction. Streamers abandon games with sniping problems.
  
### **Detection Pattern**
multiplayer|lobby|matchmaking|public
### **Symptoms**
  - Streamers complaining about snipers
  - Needing 5-minute stream delay
  - Griefers ruining content
### **Solution**
  1. Private lobby support with hidden codes
  2. Delay-reveal lobby system (code shows after game starts)
  3. Anonymous player names option
  4. Invite-only matchmaking
  5. Report and temporary ban system
  
### **Technical Detail**
  Among Us solved this with private rooms and friend codes rather than public matchmaking
  

## UI Unreadable at 720p/1080p Stream Compression

### **Id**
ui-unreadable-at-compression
### **Severity**
high
### **Description**
  Twitch compresses to ~6Mbps. YouTube to ~8Mbps. Your beautiful 12px fonts become blurry blobs. Viewers can't follow gameplay.
  
### **Detection Pattern**
font.*size|ui.*text|interface
### **Symptoms**
  - Chat asking "what does that say?"
  - Streamers manually explaining UI
  - Important information missed
### **Solution**
  1. Minimum 26px font size (Xbox guideline)
  2. High contrast: 4.5:1 ratio minimum, 7:1 optimal
  3. Test at 720p compressed preview
  4. Bold outlines on important text
  5. UI scaling options in settings
  
### **References**
  - https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/101

## Game Audio Drowns Out Commentary

### **Id**
audio-ducking-nightmare
### **Severity**
medium
### **Description**
  Streamers need to be heard. Constant loud game audio forces awkward manual volume balancing or inaudible commentary.
  
### **Detection Pattern**
voice.*chat|audio|sound|volume
### **Symptoms**
  - Streamers manually lowering game volume
  - Commentary hard to hear
  - Viewers complaining in chat
### **Solution**
  1. Implement audio ducking (lower game during voice)
  2. Provide separate music/SFX/voice volume sliders
  3. "Commentary mode" preset with lower audio
  4. Don't add extreme audio effects (flashbang, jammer noise)
  5. Test with OBS audio ducking setup
  
### **Code Example**
  // Audio ducking implementation
  const voiceDetector = new VoiceActivityDetector();
  voiceDetector.onSpeechStart = () => {
    gameAudio.volume = 0.3;  // Duck to 30%
  };
  voiceDetector.onSpeechEnd = () => {
    gameAudio.volume = 1.0;  // Restore
  };
  

## Session Length Doesn't Match Stream Format

### **Id**
session-length-mismatch
### **Severity**
high
### **Description**
  Streamers prefer 15-30 minute sessions for variety and clips. 2-hour sessions mean one game per stream, less exposure, and viewer drop-off. Match session to stream format.
  
### **Detection Pattern**
session|match|round|game.*length
### **Symptoms**
  - Streamers only play once per stream
  - Cutting mid-run to switch games
  - Viewer count drops during long sessions
### **Solution**
  1. Design 15-20 minute core loops
  2. Natural break points every 15-20 minutes
  3. Quick restart after death/failure
  4. Satisfying micro-conclusions
  5. "Just one more run" hooks
  
### **Examples**
  
---
    ##### **Lethal Company**
15-20 minute expeditions
  
---
    ##### **Fall Guys**
15-minute shows
  
---
    ##### **Among Us**
10-15 minute rounds

## Content Violates Platform Guidelines

### **Id**
twitch-content-violations
### **Severity**
high
### **Description**
  Twitch/YouTube have content rules. Sexual content, extreme violence, hate symbols can get streamers banned even if it's "in the game."
  
### **Detection Pattern**
mature|adult|violence|content.*warning
### **Symptoms**
  - Streamers refusing to play
  - VODs deleted by platform
  - Bad press about game content
### **Solution**
  1. Research platform content guidelines
  2. Content labeling options in-game
  3. "Safe for streaming" mode that disables risky content
  4. Avoid user-generated content without moderation
  5. Historical/contextual violence is usually OK (Wolfenstein)
  
### **References**
  - https://www.twitch.tv/p/en/legal/community-guidelines/

## OBS Game Capture Doesn't Work

### **Id**
obs-game-capture-broken
### **Severity**
medium
### **Description**
  Some games don't work with OBS Game Capture due to anti-cheat, DX12 issues, or hooking problems. Streamers forced to use less efficient Display Capture.
  
### **Detection Pattern**
obs|streaming.*software|capture|directx|dx12
### **Symptoms**
  - Black screen in OBS preview
  - Performance issues during streaming
  - Streamers switching to Display Capture
### **Solution**
  1. Test with OBS Game Capture before shipping
  2. Provide DX11 fallback option
  3. Check anti-cheat compatibility with OBS
  4. Documentation for streaming setup
  5. Consider Vulkan issues on some systems
  
### **References**
  - https://obsproject.com/kb/game-capture-source

## No Quick Restart After Failures

### **Id**
no-emergency-restart
### **Severity**
medium
### **Description**
  Stream momentum dies during long restart sequences. Loading screens, cutscenes, and menus between attempts create dead air that loses viewers.
  
### **Detection Pattern**
restart|retry|death|failure
### **Symptoms**
  - Awkward silence during restarts
  - Streamers filling time with filler talk
  - Viewers leaving during loading
### **Solution**
  1. Instant restart option (skip intro/cutscenes)
  2. Minimal loading between attempts
  3. "Quick restart" keybind
  4. Skip tutorial after first playthrough
  5. Roguelike instant-loop design
  

## Price Too High for Group Purchases

### **Id**
pricing-kills-adoption
### **Severity**
high
### **Description**
  4-player co-op at $30 each = $120 for friend group. High friction for impulsive purchases after watching stream. Compare to Lethal Company's $10 = $40 for group.
  
### **Detection Pattern**
price|cost|purchase
### **Symptoms**
  - "I'll wait for a sale" comments
  - Solo play only despite co-op design
  - Low conversion from stream viewers
### **Solution**
  1. Sweet spot: $10-15 for streamer games
  2. 4-pack bundle discounts
  3. Free demo for try-before-buy
  4. Launch with 10-15% discount
  5. Among Us model: free base + cosmetics
  

## Game Has No Clip-Worthy Moments

### **Id**
no-clip-worthy-moments
### **Severity**
high
### **Description**
  Streamers need highlight material. If your game produces no memorable peaks - jump scares, dramatic reversals, comedic deaths - it won't get shared.
  
### **Detection Pattern**
clip|highlight|moment|viral
### **Symptoms**
  - No game clips on social media
  - Streamers describe game as "chill" (bad for discovery)
  - Low viewer engagement during streams
### **Solution**
  1. Design explicit peak moments
  2. Quick tension → release cycles
  3. Unpredictable outcomes for each play
  4. Reaction-worthy revelations
  5. Shareable failure states
  

## Solo Play Experience Is Broken/Boring

### **Id**
solo-experience-broken
### **Severity**
medium
### **Description**
  Content creators are 1% of players. If solo play sucks, your Steam reviews will tank from the other 99%.
  
### **Detection Pattern**
solo|single.*player|alone
### **Symptoms**
  - "Only fun with friends" reviews
  - Low player retention
  - Negative Steam reviews despite streamer success
### **Solution**
  1. Design solo-viable core loop
  2. AI companions for co-op designed games
  3. Procedural content for replayability
  4. Single-player-focused progression hooks
  5. Balance for 1-player AND 4-player
  