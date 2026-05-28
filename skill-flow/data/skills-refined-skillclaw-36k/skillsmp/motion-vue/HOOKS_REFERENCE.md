# Motion Vue Hooks Reference

Complete API reference for Motion Vue composables.

## useMotionValue

Creates a reactive value that can animate without triggering Vue re-renders.

```vue
<script setup>
import { useMotionValue } from 'motion-v'
import { onMounted, onUnmounted } from 'vue'

const x = useMotionValue(0)

// Set value (triggers animation if attached to spring)
x.set(100)

// Get current value
console.log(x.get())

// Get velocity
console.log(x.getVelocity())

// Jump to value without animation
x.jump(50)

// Check if animating
console.log(x.isAnimating())

// Subscribe to changes
const unsubscribe = x.on('change', (latest) => {
  console.log('Value changed:', latest)
})

// Events: 'change', 'animationStart', 'animationComplete', 'animationCancel'
</script>

<template>
  <motion.div :style="{ x }" />
</template>
```

## useSpring

Creates a spring-animated motion value.

```vue
<script setup>
import { useMotionValue, useSpring } from 'motion-v'

const x = useMotionValue(0)

// Spring follows the source value
const springX = useSpring(x, {
  stiffness: 300,  // Spring stiffness (default: 100)
  damping: 20,     // Resistance (default: 10)
  mass: 1,         // Mass of the object (default: 1)
  restDelta: 0.01, // When to consider "at rest" (default: 0.01)
  restSpeed: 0.01  // Velocity threshold for rest (default: 0.01)
})

// Or create standalone spring
const standalone = useSpring(0, { stiffness: 300 })
</script>

<template>
  <motion.div :style="{ x: springX }" @pointerMove="(e) => x.set(e.clientX)" />
</template>
```

## useTransform

Maps one or more motion values to a new motion value.

```vue
<script setup>
import { useMotionValue, useTransform } from 'motion-v'

const x = useMotionValue(0)

// Map input range to output range
const opacity = useTransform(x, [-200, 0, 200], [0, 1, 0])

// Transform with custom function
const rotate = useTransform(x, (latest) => latest * 0.1)

// Combine multiple values
const y = useMotionValue(0)
const distance = useTransform([x, y], ([latestX, latestY]) => {
  return Math.sqrt(latestX ** 2 + latestY ** 2)
})

// Color interpolation
const backgroundColor = useTransform(
  x,
  [-200, 0, 200],
  ['#ff0000', '#00ff00', '#0000ff']
)
</script>
```

## useVelocity

Tracks the velocity of a motion value.

```vue
<script setup>
import { useMotionValue, useVelocity, useTransform } from 'motion-v'

const x = useMotionValue(0)
const xVelocity = useVelocity(x)

// Use velocity to affect other properties
const skewX = useTransform(xVelocity, [-1000, 0, 1000], [-15, 0, 15])
</script>

<template>
  <motion.div
    drag="x"
    :style="{ x, skewX }"
  />
</template>
```

## useScroll

Tracks scroll progress of the page or a specific element.

```vue
<script setup>
import { ref } from 'vue'
import { useScroll } from 'motion-v'

// Track page scroll
const { scrollX, scrollY, scrollXProgress, scrollYProgress } = useScroll()

// Track element scroll
const containerRef = ref(null)
const { scrollYProgress: containerProgress } = useScroll({
  container: containerRef
})

// Track element within viewport
const targetRef = ref(null)
const { scrollYProgress: elementProgress } = useScroll({
  target: targetRef,
  offset: ['start end', 'end start']  // [targetStart containerEnd, targetEnd containerStart]
})
</script>
```

### Offset Syntax

```ts
// Format: [targetPoint containerPoint]
// Points: 'start' | 'center' | 'end' | number (0-1) | 'Npx'

offset: ['start end', 'end start']     // Element enters from bottom, leaves at top
offset: ['start start', 'end end']     // Element fills viewport
offset: ['center center', 'end start'] // Custom tracking
offset: ['0 1', '1 0']                 // Same as first example using numbers
offset: ['start end', 'center center'] // Track until center
```

## useAnimate

Provides imperative animation control with automatic cleanup.

```vue
<script setup>
import { useAnimate } from 'motion-v'
import { onMounted, watch } from 'vue'

const [scope, animate] = useAnimate()

onMounted(() => {
  // Animate the scoped element
  animate(scope.value, { opacity: 1, y: 0 }, { duration: 0.5 })
  
  // Animate children using selectors (scoped to parent)
  animate('li', { opacity: 1 }, { delay: stagger(0.1) })
})

// Timeline animations
async function playSequence() {
  await animate(scope.value, { x: 100 })
  await animate(scope.value, { rotate: 180 })
  await animate(scope.value, { scale: 1.2 })
}

// Control animations
const controls = animate(scope.value, { x: 100 })
controls.pause()
controls.play()
controls.stop()
controls.speed = 0.5  // Half speed
controls.time = 0.5   // Seek to 0.5s
</script>

<template>
  <ul ref="scope">
    <li v-for="item in items" :key="item.id">{{ item.name }}</li>
  </ul>
</template>
```

### Timeline Syntax

```vue
<script setup>
const [scope, animate] = useAnimate()

onMounted(() => {
  animate([
    [scope.value, { opacity: 1 }],
    ['h1', { y: 0 }, { at: '-0.3' }],  // Start 0.3s before previous ends
    ['p', { opacity: 1 }, { at: '+0.2' }],  // Start 0.2s after previous ends
    ['button', { scale: 1 }, { at: 0.5 }]  // Start at absolute 0.5s
  ])
})
</script>
```

## useInView

Detects when an element enters/leaves the viewport.

```vue
<script setup>
import { ref, watch } from 'vue'
import { useInView } from 'motion-v'

const elementRef = ref(null)

const isInView = useInView(elementRef, {
  once: false,           // Trigger only once (default: false)
  margin: '-100px',      // Viewport margin (default: '0px')
  amount: 'some'         // 'some' | 'all' | number (0-1)
})

watch(isInView, (inView) => {
  if (inView) {
    console.log('Element entered viewport')
  }
})
</script>

<template>
  <div ref="elementRef">
    {{ isInView ? 'Visible!' : 'Hidden' }}
  </div>
</template>
```

## useReducedMotion

Returns whether the user prefers reduced motion.

```vue
<script setup>
import { useReducedMotion } from 'motion-v'
import { computed } from 'vue'

const prefersReducedMotion = useReducedMotion()

const animationDuration = computed(() => 
  prefersReducedMotion.value ? 0 : 0.5
)

const animationProps = computed(() => 
  prefersReducedMotion.value 
    ? {} 
    : { x: 100, rotate: 180 }
)
</script>
```

## useAnimationFrame

Runs a callback every animation frame.

```vue
<script setup>
import { useAnimationFrame, useMotionValue } from 'motion-v'

const rotation = useMotionValue(0)

useAnimationFrame((time, delta) => {
  // time: Total elapsed time in ms
  // delta: Time since last frame in ms
  rotation.set(rotation.get() + delta * 0.1)
})
</script>

<template>
  <motion.div :style="{ rotate: rotation }" />
</template>
```

## useTime

Returns a motion value that represents elapsed time.

```vue
<script setup>
import { useTime, useTransform } from 'motion-v'

const time = useTime()

// Create continuous animations
const rotate = useTransform(time, (t) => (t / 1000) * 360)  // 1 rotation per second
const pulse = useTransform(time, (t) => Math.sin(t / 500) * 0.1 + 1)  // Pulsing scale
</script>

<template>
  <motion.div :style="{ rotate, scale: pulse }" />
</template>
```

## useDragControls

Programmatic control over drag gestures.

```vue
<script setup>
import { motion, useDragControls } from 'motion-v'

const dragControls = useDragControls()

function startDrag(event) {
  // Start drag from external element
  dragControls.start(event, { snapToCursor: true })
}
</script>

<template>
  <div @pointerDown="startDrag">Drag Handle</div>
  <motion.div
    drag
    :dragControls="dragControls"
    :dragListener="false"
  >
    Draggable Content
  </motion.div>
</template>
```

## useMotionTemplate

Creates a motion value from a template string.

```vue
<script setup>
import { useMotionValue, useMotionTemplate } from 'motion-v'

const x = useMotionValue(0)
const y = useMotionValue(0)

// Compose motion values into a string
const transform = useMotionTemplate`translateX(${x}px) translateY(${y}px)`
const gradient = useMotionTemplate`linear-gradient(${x}deg, #ff0000, #0000ff)`
</script>

<template>
  <motion.div :style="{ transform }" />
</template>
```

## useMotionValueEvent

Subscribe to motion value events with automatic cleanup.

```vue
<script setup>
import { useMotionValue, useMotionValueEvent } from 'motion-v'

const x = useMotionValue(0)

// Automatically cleaned up on unmount
useMotionValueEvent(x, 'change', (latest) => {
  console.log('x changed to:', latest)
})

useMotionValueEvent(x, 'animationStart', () => {
  console.log('Animation started')
})

useMotionValueEvent(x, 'animationComplete', () => {
  console.log('Animation complete')
})
</script>
```

## useDomRef

Get a DOM reference compatible with Motion's constraint system.

```vue
<script setup>
import { motion, useDomRef } from 'motion-v'

const constraintsRef = useDomRef()
</script>

<template>
  <motion.div ref="constraintsRef" class="container">
    <motion.div
      drag
      :dragConstraints="constraintsRef"
    />
  </motion.div>
</template>
```
