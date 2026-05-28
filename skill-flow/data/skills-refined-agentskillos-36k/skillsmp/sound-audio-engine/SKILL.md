---
name: Sound & Audio Engine
description: Game sounds, notifications, ambient audio, and music
---

# Sound & Audio Engine Skill

## Overview
Implement immersive audio for poker gameplay including card sounds, chips, notifications, and ambient music.

## Sound Categories
| Category | Examples |
|----------|----------|
| Cards | Deal, flip, shuffle |
| Chips | Bet, collect, stack |
| Actions | Check, fold, all-in |
| UI | Button click, notification |
| Ambient | Casino background |
| Music | Lobby music, game music |
| Voice | "Your turn", announcements |

## Audio Manager
```javascript
class AudioManager {
  constructor() {
    this.sounds = {};
    this.music = null;
    this.volume = {
      master: 1.0,
      sfx: 0.8,
      music: 0.5,
      voice: 1.0
    };
    this.muted = false;
  }
  
  async preload(soundMap) {
    for (const [name, path] of Object.entries(soundMap)) {
      const audio = new Audio(path);
      audio.preload = 'auto';
      this.sounds[name] = audio;
    }
  }
  
  play(name, options = {}) {
    if (this.muted) return;
    
    const sound = this.sounds[name];
    if (!sound) return;
    
    const clone = sound.cloneNode();
    clone.volume = (options.volume || 1) * this.volume.sfx * this.volume.master;
    clone.playbackRate = options.rate || 1;
    clone.play();
    
    return clone;
  }
  
  playMusic(name, loop = true) {
    if (this.music) this.music.pause();
    
    this.music = this.sounds[name];
    this.music.loop = loop;
    this.music.volume = this.volume.music * this.volume.master;
    this.music.play();
  }
  
  setVolume(category, value) {
    this.volume[category] = value;
    if (category === 'music' && this.music) {
      this.music.volume = value * this.volume.master;
    }
  }
}

export const audio = new AudioManager();
```

## Sound Preloading
```javascript
// sounds.js
export const SOUNDS = {
  // Cards
  cardDeal: '/sounds/card-deal.mp3',
  cardFlip: '/sounds/card-flip.mp3',
  cardShuffle: '/sounds/card-shuffle.mp3',
  
  // Chips
  chipBet: '/sounds/chip-bet.mp3',
  chipStack: '/sounds/chip-stack.mp3',
  chipCollect: '/sounds/chip-collect.mp3',
  
  // Actions
  check: '/sounds/check.mp3',
  fold: '/sounds/fold.mp3',
  allIn: '/sounds/all-in.mp3',
  
  // UI
  buttonClick: '/sounds/button-click.mp3',
  notification: '/sounds/notification.mp3',
  levelUp: '/sounds/level-up.mp3',
  
  // Ambient
  casinoAmbient: '/sounds/casino-ambient.mp3',
  
  // Music
  lobbyMusic: '/sounds/lobby-music.mp3',
  gameMusic: '/sounds/game-music.mp3'
};

// Preload on app start
audio.preload(SOUNDS);
```

## React Hook
```javascript
function useSound(soundName, options = {}) {
  const play = useCallback(() => {
    audio.play(soundName, options);
  }, [soundName, options]);
  
  return play;
}

// Usage
function DealButton() {
  const playDealSound = useSound('cardDeal');
  
  return (
    <button onClick={() => {
      playDealSound();
      dealCards();
    }}>
      Deal
    </button>
  );
}
```

## Poker Game Sounds Integration
```javascript
function usePokerSounds() {
  const playCardDeal = useSound('cardDeal');
  const playChipBet = useSound('chipBet');
  const playCheck = useSound('check');
  const playFold = useSound('fold');
  const playAllIn = useSound('allIn');
  
  const playActionSound = (action) => {
    switch(action) {
      case 'bet':
      case 'raise':
        playChipBet();
        break;
      case 'check':
        playCheck();
        break;
      case 'fold':
        playFold();
        break;
      case 'allin':
        playAllIn();
        break;
    }
  };
  
  return { playCardDeal, playActionSound };
}
```

## Settings Component
```jsx
function SoundSettings() {
  const [settings, setSettings] = useState({
    master: 1.0,
    sfx: 0.8,
    music: 0.5
  });
  
  const handleChange = (category, value) => {
    audio.setVolume(category, value);
    setSettings(prev => ({ ...prev, [category]: value }));
    saveToLocalStorage('soundSettings', settings);
  };
  
  return (
    <div className="sound-settings">
      <VolumeSlider label="Master" value={settings.master} onChange={(v) => handleChange('master', v)} />
      <VolumeSlider label="Sound Effects" value={settings.sfx} onChange={(v) => handleChange('sfx', v)} />
      <VolumeSlider label="Music" value={settings.music} onChange={(v) => handleChange('music', v)} />
    </div>
  );
}
```

## Haptic Feedback (Mobile)
```javascript
function haptic(type = 'light') {
  if ('vibrate' in navigator) {
    const patterns = {
      light: [10],
      medium: [20],
      heavy: [30],
      success: [10, 50, 10],
      error: [50, 30, 50]
    };
    navigator.vibrate(patterns[type]);
  }
}
```
