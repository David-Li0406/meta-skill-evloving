# FastApps Integration Guide — Neon Glass UI

Quick setup for adding Neon Glass UI to your FastApps project.

## 1. Add Global Styles

Copy `assets/styles/neon-glass.css` to `src/styles/neon-glass.css`

Then import in `src/main.js`:

```javascript
import { createApp } from 'vue'
import { IonicVue } from '@ionic/vue'
import App from './App.vue'
import router from './router'

// Ionic CSS
import '@ionic/vue/css/ionic.bundle.css'

// Add Neon Glass styles
import './styles/neon-glass.css'

const app = createApp(App)
  .use(IonicVue, { mode: 'ios' })
  .use(router)

router.isReady().then(() => {
  app.mount('#app')
})
```

## 2. Create a New App

### Step 1: Copy Template

```bash
cp -r src/apps/_template src/apps/my-new-app
mv src/apps/my-new-app/TemplateApp.vue src/apps/my-new-app/MyNewApp.vue
```

### Step 2: App Structure

Your app component should follow this structure:

```vue
<template>
  <ion-page class="neon-app">
    <!-- Required: Ambient glow background -->
    <div class="ambient-glow">
      <div class="ambient-glow__orb ambient-glow__orb--1"></div>
      <div class="ambient-glow__orb ambient-glow__orb--2"></div>
    </div>
    
    <!-- FastApps header component -->
    <AppHeader title="My App" />
    
    <ion-content :fullscreen="true" class="ion-no-border">
      <div class="app-content safe-all">
        <!-- Your content using glass-card, btn-gradient, etc. -->
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup>
import { IonPage, IonContent } from '@ionic/vue'
import AppHeader from '@/components/app/AppHeader.vue'
import { useAppTheme } from '@/composables/useAppTheme'

// Apply neon colors
useAppTheme('#FF0080', '#7209B7')
</script>

<style scoped>
/* Ambient glow - customize colors for your app */
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
  bottom: -100px;
  left: -80px;
  animation-delay: -3s;
}
</style>
```

### Step 3: Create Metadata

`public/apps/my-new-app/app.yaml`:

```yaml
name: My New App
description: A brief description of your app
emoji: 🎯
color: "linear-gradient(135deg, #FF0080 0%, #7209B7 100%)"
```

### Step 4: Register App

Add to `public/apps/apps-list.json`:

```json
{
  "apps": ["breathing", "tabata", "my-new-app"]
}
```

### Step 5: Add Route

In `src/router/index.js`:

```javascript
import MyNewApp from '../apps/my-new-app/MyNewApp.vue'

const routes = [
  // ... existing routes
  {
    path: '/apps/my-new-app',
    name: 'MyNewApp',
    component: MyNewApp
  }
]
```

## 3. useAppTheme Colors

Choose colors that match the Neon Glass aesthetic:

```javascript
// Focus/Work modes - warm
useAppTheme('#FF0080', '#FF6B35')  // Pink → Orange
useAppTheme('#FF3366', '#FF0080')  // Red → Pink
useAppTheme('#FF0080', '#7209B7')  // Pink → Purple

// Rest/Calm modes - cool
useAppTheme('#4361EE', '#00D9FF')  // Blue → Cyan
useAppTheme('#06D6A0', '#00D9FF')  // Teal → Cyan
useAppTheme('#00D9FF', '#4361EE')  // Cyan → Blue

// Neutral
useAppTheme('#7209B7', '#4361EE')  // Purple → Blue
useAppTheme('#4361EE', '#7209B7')  // Blue → Purple
```

## 4. Available CSS Classes

### Glass Effects
- `.glass-card` — Standard glass container
- `.glass-card--sm` — Smaller padding
- `.glass-card--interactive` — Adds active state
- `.glass-slip` — List item style

### Buttons
- `.btn-gradient` — Primary neon button with glow
- `.btn-gradient--warm` — Orange/pink gradient
- `.btn-gradient--cool` — Cyan/blue gradient
- `.btn-gradient--full` — Full width
- `.btn-outline` — Transparent with border
- `.btn-secondary` — Subtle glass button

### Typography
- `.heading-xl` — 32px bold
- `.heading-lg` — 24px semibold
- `.heading-md` — 18px semibold
- `.label-caps` — 14px uppercase tracking
- `.body-text` — 16px secondary color
- `.timer-display` — 96px tabular nums
- `.timer-display--lg` — 140px
- `.timer-display--sm` — 56px

### Inputs
- `.input-dark` — Rounded dark input

### Layout
- `.safe-all` — Full safe area padding
- `.safe-top` — Top safe area only
- `.safe-bottom` — Bottom safe area only
- `.flex`, `.flex-col`, `.items-center`, etc.

### Colors
- `.text-white`, `.text-secondary`, `.text-tertiary`
- `.text-success`, `.text-error`, `.text-cyan`, `.text-pink`
- `.bg-deep`, `.bg-elevated`

### Ambient Orb Colors
- `.ambient-glow__orb--pink`
- `.ambient-glow__orb--purple`
- `.ambient-glow__orb--blue`
- `.ambient-glow__orb--cyan`
- `.ambient-glow__orb--teal`
- `.ambient-glow__orb--orange`
- `.ambient-glow__orb--red`

## 5. Checklist

Before deploying your app:

- [ ] `useAppTheme()` called with neon colors
- [ ] Ambient glow orbs in template
- [ ] `.neon-app` class on `ion-page`
- [ ] No plain/solid backgrounds
- [ ] Glass cards using `.glass-card`
- [ ] Safe area padding applied (`.safe-all`)
- [ ] App registered in `apps-list.json`
- [ ] Route added to router
- [ ] YAML metadata created
- [ ] Gradient buttons have glow effect
