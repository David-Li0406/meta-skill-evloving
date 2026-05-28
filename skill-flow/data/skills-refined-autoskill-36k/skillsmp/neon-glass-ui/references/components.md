# Component Reference — Neon Glass UI for FastApps

Complete Vue 3 implementations following FastApps project conventions.

---

## 1. Pomodoro Timer App

`src/apps/pomodoro/PomodoroApp.vue`

```vue
<template>
  <ion-page class="pomodoro-app">
    <div class="ambient-glow">
      <div class="ambient-glow__orb ambient-glow__orb--1"></div>
      <div class="ambient-glow__orb ambient-glow__orb--2"></div>
      <div class="ambient-glow__orb ambient-glow__orb--3"></div>
    </div>
    
    <AppHeader 
      title="Pomodoro" 
      :show-settings="true" 
      @settings="showSettings = true" 
    />
    
    <ion-content :fullscreen="true" class="ion-no-border">
      <div class="pomodoro">
        <p class="pomodoro__label">{{ isBreak ? 'BREAK TIME' : 'FOCUS TIME' }}</p>
        
        <!-- Liquid Timer Blob -->
        <div class="timer-blob">
          <div class="timer-blob__fill" :style="{ '--progress': progress + '%' }"></div>
          <div class="timer-blob__inner">
            <span class="timer-blob__time">{{ displayTime }}</span>
          </div>
        </div>
        
        <div class="pomodoro__controls glass-card">
          <button 
            class="btn-gradient btn-gradient--full" 
            @click="toggle"
          >
            {{ isRunning ? 'Pause' : 'Start' }}
          </button>
          <button class="btn-outline btn-outline--full" @click="reset">
            Reset
          </button>
        </div>
        
        <div class="pomodoro__stats glass-card">
          <div class="stat">
            <span class="stat__value">{{ completedSessions }}</span>
            <span class="stat__label">SESSIONS</span>
          </div>
          <div class="stat">
            <span class="stat__value">{{ totalMinutes }}</span>
            <span class="stat__label">MINUTES</span>
          </div>
        </div>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup>
import { ref, computed, onUnmounted, watch } from 'vue'
import { IonPage, IonContent } from '@ionic/vue'
import AppHeader from '@/components/app/AppHeader.vue'
import { useAppTheme } from '@/composables/useAppTheme'

const WORK_DURATION = 25 * 60
const BREAK_DURATION = 5 * 60

const timeLeft = ref(WORK_DURATION)
const isRunning = ref(false)
const isBreak = ref(false)
const completedSessions = ref(0)
const showSettings = ref(false)
let interval = null

// Dynamic theme based on mode
watch(isBreak, (breaking) => {
  if (breaking) {
    useAppTheme('#4361EE', '#00D9FF') // Cool blue for break
  } else {
    useAppTheme('#FF0080', '#7209B7') // Warm pink for focus
  }
}, { immediate: true })

const progress = computed(() => {
  const total = isBreak.value ? BREAK_DURATION : WORK_DURATION
  return ((total - timeLeft.value) / total) * 100
})

const displayTime = computed(() => {
  const mins = Math.floor(timeLeft.value / 60)
  const secs = timeLeft.value % 60
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
})

const totalMinutes = computed(() => completedSessions.value * 25)

function toggle() {
  isRunning.value ? pause() : start()
}

function start() {
  isRunning.value = true
  interval = setInterval(() => {
    if (timeLeft.value > 0) {
      timeLeft.value--
    } else {
      if (!isBreak.value) completedSessions.value++
      isBreak.value = !isBreak.value
      timeLeft.value = isBreak.value ? BREAK_DURATION : WORK_DURATION
    }
  }, 1000)
}

function pause() {
  isRunning.value = false
  if (interval) clearInterval(interval)
}

function reset() {
  pause()
  isBreak.value = false
  timeLeft.value = WORK_DURATION
}

onUnmounted(() => {
  if (interval) clearInterval(interval)
})
</script>

<style scoped>
.pomodoro-app {
  --background: #0A0A12;
}

ion-content {
  --background: transparent;
}

/* Ambient Glow */
.ambient-glow {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
}

.ambient-glow__orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.5;
  animation: float 8s ease-in-out infinite;
}

.ambient-glow__orb--1 {
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, #FF0080 0%, transparent 70%);
  top: -80px;
  right: -60px;
}

.ambient-glow__orb--2 {
  width: 350px;
  height: 350px;
  background: radial-gradient(circle, #4361EE 0%, transparent 70%);
  bottom: 20%;
  left: -100px;
  animation-delay: -3s;
}

.ambient-glow__orb--3 {
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, #7209B7 0%, transparent 70%);
  bottom: -50px;
  right: 20%;
  animation-delay: -5s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(20px, -20px) scale(1.05); }
  66% { transform: translate(-15px, 15px) scale(0.95); }
}

/* Main Layout */
.pomodoro {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100%;
  padding: 20px;
  padding-top: calc(env(safe-area-inset-top) + 80px);
  padding-bottom: calc(env(safe-area-inset-bottom) + 40px);
  position: relative;
  z-index: 1;
}

.pomodoro__label {
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 3px;
  color: #A0A0B8;
  margin-bottom: 40px;
}

/* Timer Blob */
.timer-blob {
  position: relative;
  width: 280px;
  height: 280px;
  margin-bottom: 40px;
}

.timer-blob__fill {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: conic-gradient(
    from 0deg,
    #FF0080 0%,
    #FF6B35 25%,
    #FFBE0B 50%,
    rgba(255, 255, 255, 0.1) 50%,
    rgba(255, 255, 255, 0.1) 100%
  );
  mask: conic-gradient(
    from 0deg,
    black 0%,
    black var(--progress, 0%),
    transparent var(--progress, 0%),
    transparent 100%
  );
  -webkit-mask: conic-gradient(
    from 0deg,
    black 0%,
    black var(--progress, 0%),
    transparent var(--progress, 0%),
    transparent 100%
  );
  filter: blur(2px);
  animation: blob-morph 8s ease-in-out infinite;
}

.timer-blob__fill::before {
  content: '';
  position: absolute;
  inset: 4px;
  background: #0A0A12;
  border-radius: 50%;
}

.timer-blob__inner {
  position: absolute;
  inset: 8px;
  border-radius: 50%;
  background: rgba(20, 20, 35, 0.8);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 
    inset 0 2px 20px rgba(0, 0, 0, 0.5),
    0 0 60px rgba(255, 0, 128, 0.2);
}

.timer-blob__time {
  font-size: 56px;
  font-weight: 700;
  color: white;
  font-variant-numeric: tabular-nums;
  letter-spacing: -2px;
}

@keyframes blob-morph {
  0%, 100% { border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; }
  50% { border-radius: 30% 60% 70% 40% / 50% 60% 30% 60%; }
}

/* Controls */
.pomodoro__controls {
  width: 100%;
  max-width: 320px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
}

.pomodoro__stats {
  width: 100%;
  max-width: 320px;
  display: flex;
  justify-content: space-around;
}

.stat {
  text-align: center;
}

.stat__value {
  display: block;
  font-size: 32px;
  font-weight: 700;
  color: white;
}

.stat__label {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 2px;
  color: #6B6B80;
}

/* Glass Card */
.glass-card {
  background: rgba(30, 30, 50, 0.6);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  padding: 20px;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
}

/* Buttons */
.btn-gradient {
  background: linear-gradient(135deg, #00D9FF 0%, #4361EE 50%, #7209B7 100%);
  border: none;
  border-radius: 100px;
  padding: 16px 32px;
  color: white;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  position: relative;
  transition: transform 0.2s ease;
}

.btn-gradient::after {
  content: '';
  position: absolute;
  inset: -2px;
  background: inherit;
  border-radius: inherit;
  z-index: -1;
  filter: blur(15px);
  opacity: 0.5;
}

.btn-gradient:active {
  transform: scale(0.97);
}

.btn-gradient--full {
  width: 100%;
}

.btn-outline {
  background: transparent;
  border: 1.5px solid rgba(255, 255, 255, 0.3);
  border-radius: 100px;
  padding: 16px 32px;
  color: white;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-outline:active {
  background: rgba(255, 255, 255, 0.05);
  transform: scale(0.97);
}

.btn-outline--full {
  width: 100%;
}
</style>
```

**Metadata:** `public/apps/pomodoro/app.yaml`
```yaml
name: Pomodoro
description: Focus timer with liquid gradient visualization
emoji: 🍅
color: "linear-gradient(135deg, #FF0080 0%, #7209B7 100%)"
```

---

## 2. Breathing Exercise App

`src/apps/breathing/BreathingApp.vue`

```vue
<template>
  <ion-page class="breathing-app">
    <div class="ambient-glow">
      <div class="ambient-glow__orb ambient-glow__orb--1"></div>
      <div class="ambient-glow__orb ambient-glow__orb--2"></div>
    </div>
    
    <AppHeader title="Breathing" />
    
    <ion-content :fullscreen="true" class="ion-no-border">
      <div class="breathing">
        <p class="breathing__label">{{ phaseText }}</p>
        
        <!-- Breathing Orb -->
        <div 
          class="breath-orb" 
          :class="[`breath-orb--${phase}`]"
          @click="toggle"
        >
          <div class="breath-orb__glow"></div>
          <div class="breath-orb__ring breath-orb__ring--1"></div>
          <div class="breath-orb__ring breath-orb__ring--2"></div>
          <div class="breath-orb__core">
            <span class="breath-orb__instruction">{{ instruction }}</span>
          </div>
        </div>
        
        <div class="breathing__controls">
          <button 
            class="btn-gradient btn-gradient--full" 
            @click="toggle"
          >
            {{ isRunning ? 'Stop' : 'Begin Session' }}
          </button>
        </div>
        
        <div class="breathing__cycles glass-card">
          <span class="cycles__value">{{ cycleCount }}</span>
          <span class="cycles__label">CYCLES COMPLETED</span>
        </div>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue'
import { IonPage, IonContent } from '@ionic/vue'
import AppHeader from '@/components/app/AppHeader.vue'
import { useAppTheme } from '@/composables/useAppTheme'

useAppTheme('#00D9FF', '#4361EE')

const INHALE = 4000
const HOLD = 4000
const EXHALE = 4000

const phase = ref('idle')
const isRunning = ref(false)
const cycleCount = ref(0)
let timeout = null

const phaseText = computed(() => {
  const texts = {
    idle: 'TAP TO BEGIN',
    inhale: 'BREATHE IN',
    hold: 'HOLD',
    exhale: 'BREATHE OUT'
  }
  return texts[phase.value]
})

const instruction = computed(() => {
  const instructions = {
    idle: 'Ready',
    inhale: '4s',
    hold: '4s',
    exhale: '4s'
  }
  return instructions[phase.value]
})

function runCycle() {
  phase.value = 'inhale'
  timeout = setTimeout(() => {
    phase.value = 'hold'
    timeout = setTimeout(() => {
      phase.value = 'exhale'
      timeout = setTimeout(() => {
        cycleCount.value++
        if (isRunning.value) runCycle()
      }, EXHALE)
    }, HOLD)
  }, INHALE)
}

function toggle() {
  if (isRunning.value) {
    stop()
  } else {
    start()
  }
}

function start() {
  isRunning.value = true
  runCycle()
}

function stop() {
  isRunning.value = false
  phase.value = 'idle'
  if (timeout) clearTimeout(timeout)
}

onUnmounted(() => {
  if (timeout) clearTimeout(timeout)
})
</script>

<style scoped>
.breathing-app {
  --background: #0A0A12;
}

ion-content {
  --background: transparent;
}

.ambient-glow {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
}

.ambient-glow__orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
  animation: float 10s ease-in-out infinite;
}

.ambient-glow__orb--1 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, #00D9FF 0%, transparent 70%);
  top: -100px;
  left: -100px;
}

.ambient-glow__orb--2 {
  width: 350px;
  height: 350px;
  background: radial-gradient(circle, #4361EE 0%, transparent 70%);
  bottom: -80px;
  right: -80px;
  animation-delay: -4s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  50% { transform: translate(30px, -30px) scale(1.1); }
}

.breathing {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100%;
  padding: 20px;
  padding-top: calc(env(safe-area-inset-top) + 80px);
  padding-bottom: calc(env(safe-area-inset-bottom) + 40px);
  position: relative;
  z-index: 1;
}

.breathing__label {
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 3px;
  color: #A0A0B8;
  margin-bottom: 60px;
}

/* Breathing Orb */
.breath-orb {
  position: relative;
  width: 200px;
  height: 200px;
  cursor: pointer;
  margin-bottom: 60px;
}

.breath-orb__glow {
  position: absolute;
  inset: -40px;
  border-radius: 50%;
  background: radial-gradient(
    circle,
    rgba(0, 217, 255, 0.4) 0%,
    rgba(67, 97, 238, 0.2) 50%,
    transparent 70%
  );
  filter: blur(30px);
  transition: all 4s ease-in-out;
}

.breath-orb__ring {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: 2px solid rgba(0, 217, 255, 0.3);
  transition: all 4s ease-in-out;
}

.breath-orb__ring--1 {
  inset: -20px;
  border-color: rgba(0, 217, 255, 0.15);
}

.breath-orb__ring--2 {
  inset: -40px;
  border-color: rgba(0, 217, 255, 0.08);
}

.breath-orb__core {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: linear-gradient(135deg, 
    rgba(0, 217, 255, 0.3) 0%, 
    rgba(67, 97, 238, 0.3) 50%,
    rgba(114, 9, 183, 0.3) 100%
  );
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 4s ease-in-out;
  box-shadow: 
    inset 0 0 40px rgba(0, 217, 255, 0.2),
    0 0 60px rgba(0, 217, 255, 0.3);
}

.breath-orb__instruction {
  font-size: 24px;
  font-weight: 600;
  color: white;
}

/* Phase animations */
.breath-orb--inhale {
  .breath-orb__core { transform: scale(1.4); }
  .breath-orb__glow { transform: scale(1.5); opacity: 1; }
  .breath-orb__ring--1 { transform: scale(1.3); }
  .breath-orb__ring--2 { transform: scale(1.2); }
}

.breath-orb--hold {
  .breath-orb__core {
    transform: scale(1.4);
    box-shadow: 
      inset 0 0 60px rgba(0, 217, 255, 0.4),
      0 0 80px rgba(0, 217, 255, 0.5);
  }
  .breath-orb__glow { transform: scale(1.5); opacity: 1; }
}

.breath-orb--exhale {
  .breath-orb__core { transform: scale(1); }
  .breath-orb__glow { transform: scale(1); opacity: 0.6; }
  .breath-orb__ring--1 { transform: scale(1); }
  .breath-orb__ring--2 { transform: scale(1); }
}

.breathing__controls {
  width: 100%;
  max-width: 280px;
  margin-bottom: 40px;
}

.breathing__cycles {
  text-align: center;
}

.cycles__value {
  display: block;
  font-size: 48px;
  font-weight: 700;
  color: white;
}

.cycles__label {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 2px;
  color: #6B6B80;
}

/* Shared styles */
.glass-card {
  background: rgba(30, 30, 50, 0.6);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  padding: 24px 40px;
}

.btn-gradient {
  background: linear-gradient(135deg, #00D9FF 0%, #4361EE 100%);
  border: none;
  border-radius: 100px;
  padding: 16px 32px;
  color: white;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  position: relative;
}

.btn-gradient::after {
  content: '';
  position: absolute;
  inset: -2px;
  background: inherit;
  border-radius: inherit;
  z-index: -1;
  filter: blur(15px);
  opacity: 0.5;
}

.btn-gradient:active {
  transform: scale(0.97);
}

.btn-gradient--full {
  width: 100%;
}
</style>
```

**Metadata:** `public/apps/breathing/app.yaml`
```yaml
name: Breathing
description: Guided breathing exercises for relaxation
emoji: 🌬️
color: "linear-gradient(135deg, #00D9FF 0%, #4361EE 100%)"
```

---

## 3. Tabata Timer App

`src/apps/tabata/TabataApp.vue`

```vue
<template>
  <ion-page class="tabata-app" :class="{ 'tabata-app--work': isWork }">
    <div class="ambient-glow" :class="{ 'ambient-glow--rest': !isWork }">
      <div class="ambient-glow__orb ambient-glow__orb--1"></div>
      <div class="ambient-glow__orb ambient-glow__orb--2"></div>
    </div>
    
    <AppHeader title="Tabata" />
    
    <ion-content :fullscreen="true" class="ion-no-border">
      <div class="tabata">
        <div class="tabata__header">
          <span class="tabata__phase">{{ isWork ? 'WORK' : 'REST' }}</span>
          <span class="tabata__rounds">{{ currentRound }}/{{ ROUNDS }}</span>
        </div>
        
        <!-- Large Timer -->
        <div class="timer-display">
          <span class="timer-display__time">{{ displayTime }}</span>
          <span class="timer-display__label">seconds</span>
        </div>
        
        <!-- Progress Dots -->
        <div class="round-dots">
          <div 
            v-for="i in ROUNDS" 
            :key="i"
            class="round-dots__dot"
            :class="{ 
              'round-dots__dot--complete': i < currentRound,
              'round-dots__dot--active': i === currentRound 
            }"
          ></div>
        </div>
        
        <div class="tabata__controls glass-card">
          <button 
            class="btn-gradient btn-gradient--full" 
            @click="toggle"
          >
            {{ isRunning ? 'Pause' : 'Start' }}
          </button>
          <button class="btn-outline btn-outline--full" @click="reset">
            Reset
          </button>
        </div>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup>
import { ref, computed, onUnmounted, watch } from 'vue'
import { IonPage, IonContent } from '@ionic/vue'
import AppHeader from '@/components/app/AppHeader.vue'
import { useAppTheme } from '@/composables/useAppTheme'

const WORK_TIME = 20
const REST_TIME = 10
const ROUNDS = 8

const currentRound = ref(1)
const timeLeft = ref(WORK_TIME)
const isWork = ref(true)
const isRunning = ref(false)
let interval = null

// Dynamic theme based on work/rest
watch(isWork, (working) => {
  if (working) {
    useAppTheme('#FF3366', '#FF0080')
  } else {
    useAppTheme('#4361EE', '#00D9FF')
  }
}, { immediate: true })

const displayTime = computed(() => timeLeft.value.toString().padStart(2, '0'))

function toggle() {
  isRunning.value ? pause() : start()
}

function start() {
  isRunning.value = true
  interval = setInterval(() => {
    if (timeLeft.value > 0) {
      timeLeft.value--
    } else {
      if (isWork.value) {
        isWork.value = false
        timeLeft.value = REST_TIME
      } else {
        if (currentRound.value < ROUNDS) {
          currentRound.value++
          isWork.value = true
          timeLeft.value = WORK_TIME
        } else {
          reset()
        }
      }
    }
  }, 1000)
}

function pause() {
  isRunning.value = false
  if (interval) clearInterval(interval)
}

function reset() {
  pause()
  currentRound.value = 1
  timeLeft.value = WORK_TIME
  isWork.value = true
}

onUnmounted(() => {
  if (interval) clearInterval(interval)
})
</script>

<style scoped>
.tabata-app {
  --background: #0A0A12;
}

ion-content {
  --background: transparent;
}

/* Ambient with color shift */
.ambient-glow {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  transition: opacity 0.5s ease;
}

.ambient-glow__orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.5;
  transition: background 0.5s ease;
}

.ambient-glow__orb--1 {
  width: 350px;
  height: 350px;
  background: radial-gradient(circle, #FF3366 0%, transparent 70%);
  top: -100px;
  right: -80px;
}

.ambient-glow__orb--2 {
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, #FF0080 0%, transparent 70%);
  bottom: 10%;
  left: -100px;
}

.ambient-glow--rest .ambient-glow__orb--1 {
  background: radial-gradient(circle, #4361EE 0%, transparent 70%);
}

.ambient-glow--rest .ambient-glow__orb--2 {
  background: radial-gradient(circle, #00D9FF 0%, transparent 70%);
}

.tabata {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100%;
  padding: 20px;
  padding-top: calc(env(safe-area-inset-top) + 80px);
  padding-bottom: calc(env(safe-area-inset-bottom) + 40px);
  position: relative;
  z-index: 1;
}

.tabata__header {
  display: flex;
  justify-content: space-between;
  width: 100%;
  max-width: 300px;
  margin-bottom: 40px;
}

.tabata__phase {
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 4px;
  color: white;
}

.tabata__rounds {
  font-size: 14px;
  font-weight: 600;
  color: #A0A0B8;
}

/* Timer Display */
.timer-display {
  text-align: center;
  margin-bottom: 40px;
}

.timer-display__time {
  display: block;
  font-size: 140px;
  font-weight: 700;
  color: white;
  line-height: 1;
  font-variant-numeric: tabular-nums;
  text-shadow: 0 0 60px rgba(255, 51, 102, 0.5);
  transition: text-shadow 0.5s ease;
}

.tabata-app:not(.tabata-app--work) .timer-display__time {
  text-shadow: 0 0 60px rgba(0, 217, 255, 0.5);
}

.timer-display__label {
  font-size: 16px;
  color: #6B6B80;
  text-transform: uppercase;
  letter-spacing: 4px;
}

/* Round Dots */
.round-dots {
  display: flex;
  gap: 12px;
  margin-bottom: 60px;
}

.round-dots__dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.15);
  transition: all 0.3s ease;
}

.round-dots__dot--complete {
  background: #06D6A0;
  box-shadow: 0 0 12px rgba(6, 214, 160, 0.5);
}

.round-dots__dot--active {
  background: linear-gradient(135deg, #FF0080, #FF6B35);
  box-shadow: 0 0 16px rgba(255, 0, 128, 0.6);
  transform: scale(1.2);
}

.tabata__controls {
  width: 100%;
  max-width: 320px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* Shared */
.glass-card {
  background: rgba(30, 30, 50, 0.6);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  padding: 20px;
}

.btn-gradient {
  background: linear-gradient(135deg, #00D9FF 0%, #4361EE 50%, #7209B7 100%);
  border: none;
  border-radius: 100px;
  padding: 16px 32px;
  color: white;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
}

.btn-gradient:active { transform: scale(0.97); }
.btn-gradient--full { width: 100%; }

.btn-outline {
  background: transparent;
  border: 1.5px solid rgba(255, 255, 255, 0.3);
  border-radius: 100px;
  padding: 16px 32px;
  color: white;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
}

.btn-outline:active { 
  background: rgba(255, 255, 255, 0.05);
  transform: scale(0.97);
}
.btn-outline--full { width: 100%; }
</style>
```

**Metadata:** `public/apps/tabata/app.yaml`
```yaml
name: Tabata
description: High-intensity interval training timer
emoji: ⚡
color: "linear-gradient(135deg, #FF3366 0%, #FF0080 100%)"
```

---

## 4. Todo List App

`src/apps/todo/TodoApp.vue`

```vue
<template>
  <ion-page class="todo-app">
    <div class="ambient-glow">
      <div class="ambient-glow__orb ambient-glow__orb--1"></div>
      <div class="ambient-glow__orb ambient-glow__orb--2"></div>
    </div>
    
    <AppHeader title="Tasks" />
    
    <ion-content :fullscreen="true" class="ion-no-border">
      <div class="todo">
        <h1 class="todo__title">Today's Tasks</h1>
        <p class="todo__subtitle">{{ remaining }} remaining</p>
        
        <!-- Input -->
        <div class="todo-input">
          <input 
            v-model="newTodo"
            type="text" 
            placeholder="Add a new task..."
            class="todo-input__field"
            @keyup.enter="addTodo"
          />
          <button class="todo-input__btn" @click="addTodo">+</button>
        </div>
        
        <!-- Todo List -->
        <div class="todo-list">
          <TransitionGroup name="todo-item">
            <div 
              v-for="todo in todos" 
              :key="todo.id"
              class="todo-slip"
              :class="{ 'todo-slip--completed': todo.completed }"
              @click="toggleTodo(todo.id)"
            >
              <div class="todo-slip__check">
                <div class="todo-slip__checkbox" :class="{ 'todo-slip__checkbox--checked': todo.completed }">
                  <span v-if="todo.completed">✓</span>
                </div>
              </div>
              <span class="todo-slip__text">{{ todo.text }}</span>
              <button class="todo-slip__delete" @click.stop="deleteTodo(todo.id)">×</button>
            </div>
          </TransitionGroup>
        </div>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup>
import { ref, computed } from 'vue'
import { IonPage, IonContent } from '@ionic/vue'
import AppHeader from '@/components/app/AppHeader.vue'
import { useAppTheme } from '@/composables/useAppTheme'

useAppTheme('#7209B7', '#4361EE')

const todos = ref([
  { id: 1, text: 'Complete breathing exercise', completed: true },
  { id: 2, text: 'Focus session - 25 min', completed: false },
  { id: 3, text: 'Review project notes', completed: false },
])

const newTodo = ref('')

const remaining = computed(() => todos.value.filter(t => !t.completed).length)

function addTodo() {
  if (!newTodo.value.trim()) return
  todos.value.unshift({
    id: Date.now(),
    text: newTodo.value.trim(),
    completed: false
  })
  newTodo.value = ''
}

function toggleTodo(id) {
  const todo = todos.value.find(t => t.id === id)
  if (todo) todo.completed = !todo.completed
}

function deleteTodo(id) {
  todos.value = todos.value.filter(t => t.id !== id)
}
</script>

<style scoped>
.todo-app {
  --background: #0A0A12;
}

ion-content {
  --background: transparent;
}

.ambient-glow {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
}

.ambient-glow__orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
}

.ambient-glow__orb--1 {
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, #7209B7 0%, transparent 70%);
  top: -80px;
  right: -60px;
}

.ambient-glow__orb--2 {
  width: 350px;
  height: 350px;
  background: radial-gradient(circle, #4361EE 0%, transparent 70%);
  bottom: -100px;
  left: -80px;
}

.todo {
  padding: 20px;
  padding-top: calc(env(safe-area-inset-top) + 80px);
  padding-bottom: calc(env(safe-area-inset-bottom) + 40px);
  position: relative;
  z-index: 1;
}

.todo__title {
  font-size: 32px;
  font-weight: 700;
  color: white;
  margin: 0 0 8px;
}

.todo__subtitle {
  font-size: 16px;
  color: #6B6B80;
  margin: 0 0 32px;
}

/* Input */
.todo-input {
  display: flex;
  gap: 12px;
  margin-bottom: 32px;
}

.todo-input__field {
  flex: 1;
  background: rgba(0, 0, 0, 0.3);
  border: none;
  border-radius: 100px;
  padding: 16px 24px;
  font-size: 16px;
  color: white;
  outline: none;
}

.todo-input__field::placeholder {
  color: #6B6B80;
}

.todo-input__field:focus {
  box-shadow: 0 0 0 2px rgba(114, 9, 183, 0.4);
}

.todo-input__btn {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: linear-gradient(135deg, #7209B7 0%, #4361EE 100%);
  border: none;
  color: white;
  font-size: 24px;
  font-weight: 300;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.todo-input__btn:active {
  transform: scale(0.95);
}

/* Todo List */
.todo-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.todo-slip {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 18px 20px;
  background: rgba(30, 30, 50, 0.5);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.todo-slip:active {
  transform: scale(0.98);
  background: rgba(40, 40, 60, 0.6);
}

.todo-slip__checkbox {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  font-size: 14px;
  color: white;
}

.todo-slip__checkbox--checked {
  background: linear-gradient(135deg, #06D6A0, #00D9FF);
  border-color: transparent;
}

.todo-slip__text {
  flex: 1;
  font-size: 16px;
  color: white;
  transition: all 0.3s ease;
}

.todo-slip__delete {
  background: none;
  border: none;
  padding: 8px;
  font-size: 20px;
  color: #6B6B80;
  opacity: 0;
  transition: opacity 0.2s ease;
  cursor: pointer;
}

.todo-slip:hover .todo-slip__delete,
.todo-slip:active .todo-slip__delete {
  opacity: 1;
}

.todo-slip__delete:active {
  color: #FF3366;
}

.todo-slip--completed {
  opacity: 0.6;
}

.todo-slip--completed .todo-slip__text {
  text-decoration: line-through;
  color: #6B6B80;
}

/* Animations */
.todo-item-enter-active,
.todo-item-leave-active {
  transition: all 0.3s ease;
}

.todo-item-enter-from {
  opacity: 0;
  transform: translateX(-20px);
}

.todo-item-leave-to {
  opacity: 0;
  transform: translateX(20px);
}
</style>
```

**Metadata:** `public/apps/todo/app.yaml`
```yaml
name: Tasks
description: Beautiful task management with glass design
emoji: ✅
color: "linear-gradient(135deg, #7209B7 0%, #4361EE 100%)"
```

---

## 5. Route Registration

Add all apps to `src/router/index.js`:

```javascript
import { createRouter, createWebHistory } from '@ionic/vue-router'
import Home from '../views/Home.vue'
import Settings from '../views/Settings.vue'

// Apps
import PomodoroApp from '../apps/pomodoro/PomodoroApp.vue'
import BreathingApp from '../apps/breathing/BreathingApp.vue'
import TabataApp from '../apps/tabata/TabataApp.vue'
import TodoApp from '../apps/todo/TodoApp.vue'

const routes = [
  { path: '/', redirect: '/home' },
  { path: '/home', name: 'Home', component: Home },
  { path: '/settings', name: 'Settings', component: Settings },
  
  // Apps
  { path: '/apps/pomodoro', name: 'PomodoroApp', component: PomodoroApp },
  { path: '/apps/breathing', name: 'BreathingApp', component: BreathingApp },
  { path: '/apps/tabata', name: 'TabataApp', component: TabataApp },
  { path: '/apps/todo', name: 'TodoApp', component: TodoApp },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
```

## 6. Update apps-list.json

`public/apps/apps-list.json`:

```json
{
  "apps": ["pomodoro", "breathing", "tabata", "todo"]
}
```
