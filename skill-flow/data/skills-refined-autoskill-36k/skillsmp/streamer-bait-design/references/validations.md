# Streamer Bait Design - Validations

## Small Font Size

### **Id**
small-font-size
### **Pattern**
font-?size\s*[=:]\s*(?:[0-9]|1[0-9]|2[0-5])(?:px|pt)?[^0-9]
### **Severity**
warning
### **Message**
Font size below 26px may be unreadable at streaming compression
### **Fix**
Increase font-size to at least 26px for streaming readability
### **Applies To**
  - *.css
  - *.scss
  - *.less
### **Test Cases**
  #### **Should Match**
    - font-size: 14px
    - fontSize = 12
    - font-size: 20pt
  #### **Should Not Match**
    - font-size: 26px
    - fontSize = 32
    - font-size: 48px

## No Volume Control

### **Id**
no-volume-control
### **Pattern**
audio|music|sound(?!.*volume|.*slider|.*setting|.*control)
### **Severity**
info
### **Message**
Audio implementation without volume controls - streamers need adjustable levels
### **Fix**
Add separate volume sliders for music, SFX, and voice
### **Applies To**
  - *.js
  - *.ts
  - *.cs
### **Test Cases**
  #### **Should Match**
    - playAudio('bgm.mp3')
    - this.music.play()
  #### **Should Not Match**
    - playAudio('bgm.mp3', volume: musicVolume)
    - this.music.setVolume(settings.musicVolume)

## Hardcoded Session Length

### **Id**
hardcoded-session-length
### **Pattern**
session.*(?:length|duration|time).*=.*(?:60|90|120)
### **Severity**
warning
### **Message**
Session length >45 minutes may not fit stream format
### **Fix**
Consider shorter 15-20 minute sessions with natural break points
### **Applies To**
  - *.js
  - *.ts
  - *.cs
  - *.gd
### **Test Cases**
  #### **Should Match**
    - sessionLength = 60
    - match_duration: 90
  #### **Should Not Match**
    - sessionLength = 15
    - match_duration: 20

## No Streamer Mode

### **Id**
no-streamer-mode
### **Pattern**
settings|config|options(?!.*streamer|.*broadcast|.*stream)
### **Severity**
info
### **Message**
Settings without Streamer Mode - consider adding streaming-specific options
### **Fix**
Add Streamer Mode toggle with DMCA-safe audio and anti-snipe features
### **Applies To**
  - *.js
  - *.ts
  - *.cs
### **Test Cases**
  #### **Should Match**
    - const settings = {
    - class GameOptions {
  #### **Should Not Match**
    - settings.streamerMode
    - isStreaming: false

## Unskippable Cutscene

### **Id**
unskippable-cutscene
### **Pattern**
cutscene|intro|cinematic(?!.*skip|.*cancel)
### **Severity**
warning
### **Message**
Cutscene without skip option kills stream momentum on restarts
### **Fix**
Add skip option, especially for content seen before
### **Applies To**
  - *.js
  - *.ts
  - *.cs
  - *.gd
### **Test Cases**
  #### **Should Match**
    - playCutscene('intro')
    - showIntro()
  #### **Should Not Match**
    - playCutscene('intro', skippable: true)
    - if (!seenIntro) showIntro()

## Public Lobby Code

### **Id**
public-lobby-code
### **Pattern**
lobby.*code|room.*code(?!.*hidden|.*private|.*delay)
### **Severity**
warning
### **Message**
Visible lobby code enables stream sniping
### **Fix**
Hide lobby code until game starts or use invite-only
### **Applies To**
  - *.js
  - *.ts
  - *.cs
### **Test Cases**
  #### **Should Match**
    - displayLobbyCode(code)
    - show_room_code()
  #### **Should Not Match**
    - displayLobbyCode(code, hidden: true)
    - if (gameStarted) show_room_code()

## No Death Message Variety

### **Id**
no-death-message-variety
### **Pattern**
death.*message|you.*died|game.*over(?!.*random|.*array|.*list)
### **Severity**
info
### **Message**
Static death message - variety creates shareable moments
### **Fix**
Add randomized humorous death messages for clip potential
### **Applies To**
  - *.js
  - *.ts
  - *.cs
### **Test Cases**
  #### **Should Match**
    - showMessage("You died")
    - displayGameOver()
  #### **Should Not Match**
    - showMessage(randomDeathMessage())
    - deathMessages[Math.random()]

## Long Loading Screen

### **Id**
long-loading-screen
### **Pattern**
loading.*screen|load.*time(?!.*async|.*progress|.*quick)
### **Severity**
info
### **Message**
Loading screens create dead air in streams
### **Fix**
Minimize loading times or add engaging loading content
### **Applies To**
  - *.js
  - *.ts
  - *.cs
### **Test Cases**
  #### **Should Match**
    - showLoadingScreen()
    - displayLoadTime()
  #### **Should Not Match**
    - showLoadingScreen({ tips: true })
    - asyncLoad()

## No Quick Restart

### **Id**
no-quick-restart
### **Pattern**
restart|retry|respawn(?!.*quick|.*instant|.*fast)
### **Severity**
warning
### **Message**
Restart without quick option - streamers need minimal downtime
### **Fix**
Add instant restart keybind that skips menus/cutscenes
### **Applies To**
  - *.js
  - *.ts
  - *.cs
  - *.gd
### **Test Cases**
  #### **Should Match**
    - handleRestart()
    - onPlayerRetry()
  #### **Should Not Match**
    - quickRestart()
    - instantRespawn()

## Fixed Audio No Ducking

### **Id**
fixed-audio-no-ducking
### **Pattern**
audio.*volume|master.*volume(?!.*duck|.*dynamic|.*adjust)
### **Severity**
info
### **Message**
Fixed audio volume - consider dynamic ducking for commentary
### **Fix**
Implement voice-activated audio ducking or commentary mode
### **Applies To**
  - *.js
  - *.ts
  - *.cs
### **Test Cases**
  #### **Should Match**
    - setMasterVolume(0.8)
    - audioVolume = 1.0
  #### **Should Not Match**
    - setDuckingVolume(0.3)
    - enableAudioDucking()