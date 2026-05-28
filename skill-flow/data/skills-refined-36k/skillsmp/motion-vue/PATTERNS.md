# Motion Vue Common Patterns

Ready-to-use animation patterns for common UI interactions.

## Modal Dialog

```vue
<script setup>
import { motion, AnimatePresence } from 'motion-v'
import { ref } from 'vue'

const isOpen = ref(false)
</script>

<template>
  <button @click="isOpen = true">Open Modal</button>
  
  <AnimatePresence>
    <template v-if="isOpen">
      <!-- Backdrop -->
      <motion.div
        key="backdrop"
        class="fixed inset-0 bg-black/50"
        :initial="{ opacity: 0 }"
        :animate="{ opacity: 1 }"
        :exit="{ opacity: 0 }"
        @click="isOpen = false"
      />
      
      <!-- Modal -->
      <motion.div
        key="modal"
        class="fixed inset-0 flex items-center justify-center"
      >
        <motion.div
          class="bg-white rounded-lg p-6 shadow-xl"
          :initial="{ opacity: 0, scale: 0.9, y: 20 }"
          :animate="{ opacity: 1, scale: 1, y: 0 }"
          :exit="{ opacity: 0, scale: 0.9, y: 20 }"
          :transition="{ type: 'spring', damping: 25, stiffness: 300 }"
        >
          <h2>Modal Title</h2>
          <p>Modal content here</p>
          <button @click="isOpen = false">Close</button>
        </motion.div>
      </motion.div>
    </template>
  </AnimatePresence>
</template>
```

## Accordion / Collapsible

```vue
<script setup>
import { motion, AnimatePresence } from 'motion-v'
import { ref } from 'vue'

const isOpen = ref(false)
</script>

<template>
  <div class="border rounded-lg overflow-hidden">
    <motion.button
      class="w-full p-4 text-left flex justify-between items-center"
      @click="isOpen = !isOpen"
    >
      <span>Section Title</span>
      <motion.span
        :animate="{ rotate: isOpen ? 180 : 0 }"
        :transition="{ duration: 0.2 }"
      >
        ▼
      </motion.span>
    </motion.button>
    
    <AnimatePresence>
      <motion.div
        v-if="isOpen"
        key="content"
        :initial="{ height: 0, opacity: 0 }"
        :animate="{ height: 'auto', opacity: 1 }"
        :exit="{ height: 0, opacity: 0 }"
        :transition="{ duration: 0.3 }"
        class="overflow-hidden"
      >
        <div class="p-4 border-t">
          Content goes here
        </div>
      </motion.div>
    </AnimatePresence>
  </div>
</template>
```

## Tab Indicator (Shared Layout)

```vue
<script setup>
import { motion } from 'motion-v'
import { ref } from 'vue'

const tabs = ['Home', 'About', 'Contact']
const activeTab = ref('Home')
</script>

<template>
  <div class="flex gap-2 relative">
    <button
      v-for="tab in tabs"
      :key="tab"
      class="px-4 py-2 relative z-10"
      :class="activeTab === tab ? 'text-white' : 'text-gray-600'"
      @click="activeTab = tab"
    >
      {{ tab }}
      <motion.div
        v-if="activeTab === tab"
        layoutId="tab-indicator"
        class="absolute inset-0 bg-blue-500 rounded-lg -z-10"
        :transition="{ type: 'spring', stiffness: 500, damping: 30 }"
      />
    </button>
  </div>
</template>
```

## Staggered List Reveal

```vue
<script setup>
import { motion } from 'motion-v'

const items = ['Item 1', 'Item 2', 'Item 3', 'Item 4']

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2
    }
  }
}

const itemVariants = {
  hidden: { opacity: 0, x: -20 },
  visible: {
    opacity: 1,
    x: 0,
    transition: { type: 'spring', stiffness: 300, damping: 24 }
  }
}
</script>

<template>
  <motion.ul
    :variants="containerVariants"
    initial="hidden"
    animate="visible"
    class="space-y-2"
  >
    <motion.li
      v-for="item in items"
      :key="item"
      :variants="itemVariants"
      class="p-4 bg-white rounded shadow"
    >
      {{ item }}
    </motion.li>
  </motion.ul>
</template>
```

## Page Transitions

```vue
<script setup>
import { motion, AnimatePresence } from 'motion-v'
import { useRoute } from 'vue-router'
import { computed } from 'vue'

const route = useRoute()

const pageVariants = {
  initial: { opacity: 0, x: -20 },
  enter: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: 20 }
}
</script>

<template>
  <AnimatePresence mode="wait">
    <motion.div
      :key="route.path"
      :variants="pageVariants"
      initial="initial"
      animate="enter"
      exit="exit"
      :transition="{ duration: 0.3 }"
    >
      <RouterView />
    </motion.div>
  </AnimatePresence>
</template>
```

## Draggable Reorder List

```vue
<script setup>
import { motion, Reorder } from 'motion-v'
import { ref } from 'vue'

const items = ref([
  { id: 1, text: 'Item 1' },
  { id: 2, text: 'Item 2' },
  { id: 3, text: 'Item 3' }
])
</script>

<template>
  <Reorder.Group
    v-model="items"
    axis="y"
    class="space-y-2"
  >
    <Reorder.Item
      v-for="item in items"
      :key="item.id"
      :value="item"
      class="p-4 bg-white rounded shadow cursor-grab active:cursor-grabbing"
    >
      {{ item.text }}
    </Reorder.Item>
  </Reorder.Group>
</template>
```

## Scroll Progress Indicator

```vue
<script setup>
import { motion, useScroll, useSpring } from 'motion-v'

const { scrollYProgress } = useScroll()
const scaleX = useSpring(scrollYProgress, {
  stiffness: 100,
  damping: 30,
  restDelta: 0.001
})
</script>

<template>
  <motion.div
    class="fixed top-0 left-0 right-0 h-1 bg-blue-500 origin-left z-50"
    :style="{ scaleX }"
  />
</template>
```

## Parallax Scroll Effect

```vue
<script setup>
import { ref } from 'vue'
import { motion, useScroll, useTransform } from 'motion-v'

const containerRef = ref(null)
const { scrollYProgress } = useScroll({
  target: containerRef,
  offset: ['start start', 'end start']
})

const y1 = useTransform(scrollYProgress, [0, 1], [0, -100])
const y2 = useTransform(scrollYProgress, [0, 1], [0, -200])
const opacity = useTransform(scrollYProgress, [0, 0.5, 1], [1, 1, 0])
</script>

<template>
  <div ref="containerRef" class="relative h-[150vh]">
    <motion.div
      class="sticky top-0 h-screen flex items-center justify-center"
      :style="{ opacity }"
    >
      <motion.h1 :style="{ y: y1 }" class="text-6xl font-bold">
        Parallax
      </motion.h1>
      <motion.p :style="{ y: y2 }" class="text-xl">
        Scroll down
      </motion.p>
    </motion.div>
  </div>
</template>
```

## Card Flip

```vue
<script setup>
import { motion } from 'motion-v'
import { ref } from 'vue'

const isFlipped = ref(false)
</script>

<template>
  <div
    class="relative w-64 h-40 perspective-1000 cursor-pointer"
    @click="isFlipped = !isFlipped"
  >
    <!-- Front -->
    <motion.div
      class="absolute inset-0 bg-blue-500 rounded-xl flex items-center justify-center text-white backface-hidden"
      :animate="{ rotateY: isFlipped ? 180 : 0 }"
      :transition="{ duration: 0.6 }"
    >
      Front
    </motion.div>
    
    <!-- Back -->
    <motion.div
      class="absolute inset-0 bg-red-500 rounded-xl flex items-center justify-center text-white backface-hidden"
      :initial="{ rotateY: 180 }"
      :animate="{ rotateY: isFlipped ? 0 : 180 }"
      :transition="{ duration: 0.6 }"
    >
      Back
    </motion.div>
  </div>
</template>

<style scoped>
.perspective-1000 {
  perspective: 1000px;
}
.backface-hidden {
  backface-visibility: hidden;
}
</style>
```

## Notification Toast

```vue
<script setup>
import { motion, AnimatePresence } from 'motion-v'
import { ref } from 'vue'

const notifications = ref([])

function addNotification(message) {
  const id = Date.now()
  notifications.value.push({ id, message })
  setTimeout(() => {
    notifications.value = notifications.value.filter(n => n.id !== id)
  }, 3000)
}
</script>

<template>
  <div class="fixed bottom-4 right-4 space-y-2 z-50">
    <AnimatePresence>
      <motion.div
        v-for="notification in notifications"
        :key="notification.id"
        layout
        :initial="{ opacity: 0, y: 50, scale: 0.8 }"
        :animate="{ opacity: 1, y: 0, scale: 1 }"
        :exit="{ opacity: 0, x: 100 }"
        class="bg-white rounded-lg shadow-lg p-4 min-w-[200px]"
      >
        {{ notification.message }}
      </motion.div>
    </AnimatePresence>
  </div>
</template>
```

## Hover Card with 3D Effect

```vue
<script setup>
import { motion, useMotionValue, useSpring, useTransform } from 'motion-v'

const x = useMotionValue(0.5)
const y = useMotionValue(0.5)

const rotateX = useSpring(useTransform(y, [0, 1], [10, -10]))
const rotateY = useSpring(useTransform(x, [0, 1], [-10, 10]))

function handleMouseMove(e) {
  const rect = e.currentTarget.getBoundingClientRect()
  x.set((e.clientX - rect.left) / rect.width)
  y.set((e.clientY - rect.top) / rect.height)
}

function handleMouseLeave() {
  x.set(0.5)
  y.set(0.5)
}
</script>

<template>
  <motion.div
    class="w-64 h-40 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl p-6 text-white cursor-pointer"
    :style="{ 
      rotateX, 
      rotateY,
      transformPerspective: '1000px'
    }"
    :whileHover="{ scale: 1.05 }"
    @mousemove="handleMouseMove"
    @mouseleave="handleMouseLeave"
  >
    <h3 class="text-xl font-bold">3D Card</h3>
    <p>Move your mouse around</p>
  </motion.div>
</template>
```

## Morphing Button

```vue
<script setup>
import { motion } from 'motion-v'
import { ref } from 'vue'

const isLoading = ref(false)
const isComplete = ref(false)

async function handleClick() {
  isLoading.value = true
  await new Promise(r => setTimeout(r, 2000))
  isLoading.value = false
  isComplete.value = true
  await new Promise(r => setTimeout(r, 1500))
  isComplete.value = false
}
</script>

<template>
  <motion.button
    class="px-6 py-3 bg-blue-500 text-white rounded-full font-medium"
    :animate="{
      width: isLoading ? 56 : isComplete ? 56 : 'auto',
      backgroundColor: isComplete ? '#22c55e' : '#3b82f6'
    }"
    :whileHover="isLoading || isComplete ? {} : { scale: 1.05 }"
    :whilePress="isLoading || isComplete ? {} : { scale: 0.95 }"
    :disabled="isLoading || isComplete"
    @click="handleClick"
  >
    <motion.span
      :animate="{ opacity: isLoading || isComplete ? 0 : 1 }"
    >
      Submit
    </motion.span>
    
    <motion.div
      v-if="isLoading"
      class="absolute inset-0 flex items-center justify-center"
      :initial="{ opacity: 0 }"
      :animate="{ opacity: 1, rotate: 360 }"
      :transition="{ rotate: { duration: 1, repeat: Infinity, ease: 'linear' } }"
    >
      ⟳
    </motion.div>
    
    <motion.div
      v-if="isComplete"
      class="absolute inset-0 flex items-center justify-center"
      :initial="{ opacity: 0, scale: 0 }"
      :animate="{ opacity: 1, scale: 1 }"
    >
      ✓
    </motion.div>
  </motion.button>
</template>
```

## Animated Counter

```vue
<script setup>
import { motion, animate, RowValue, useMotionValue } from 'motion-v'
import { onMounted, onUnmounted, watch } from 'vue'

const props = defineProps({
  value: { type: Number, required: true }
})

const count = useMotionValue(0)
let controls

watch(() => props.value, (newValue) => {
  controls = animate(count, newValue, {
    duration: 1,
    ease: 'easeOut'
  })
}, { immediate: true })

onUnmounted(() => {
  controls?.stop()
})
</script>

<template>
  <motion.span class="tabular-nums">
    <RowValue :value="count" />
  </motion.span>
</template>
```

## Swipe to Delete

```vue
<script setup>
import { motion, useMotionValue, useTransform, AnimatePresence } from 'motion-v'
import { ref } from 'vue'

const items = ref(['Item 1', 'Item 2', 'Item 3'])

function handleDragEnd(item, event, info) {
  if (Math.abs(info.offset.x) > 100) {
    items.value = items.value.filter(i => i !== item)
  }
}
</script>

<template>
  <div class="space-y-2 overflow-hidden">
    <AnimatePresence>
      <motion.div
        v-for="item in items"
        :key="item"
        layout
        drag="x"
        :dragConstraints="{ left: 0, right: 0 }"
        :dragElastic="0.5"
        :initial="{ opacity: 1, x: 0 }"
        :exit="{ opacity: 0, x: -300 }"
        @dragEnd="(e, info) => handleDragEnd(item, e, info)"
        class="p-4 bg-white rounded shadow cursor-grab"
      >
        {{ item }}
      </motion.div>
    </AnimatePresence>
  </div>
</template>
```

## Scroll Reveal with Stagger

```vue
<script setup>
import { motion } from 'motion-v'

const items = ['Feature 1', 'Feature 2', 'Feature 3', 'Feature 4']

const containerVariants = {
  hidden: {},
  visible: {
    transition: {
      staggerChildren: 0.15
    }
  }
}

const itemVariants = {
  hidden: { opacity: 0, y: 40, scale: 0.95 },
  visible: { 
    opacity: 1, 
    y: 0, 
    scale: 1,
    transition: { 
      type: 'spring', 
      stiffness: 100,
      damping: 15
    } 
  }
}
</script>

<template>
  <motion.div
    :variants="containerVariants"
    initial="hidden"
    :whileInView="'visible'"
    :inViewOptions="{ once: true, margin: '-100px' }"
    class="grid grid-cols-2 gap-4"
  >
    <motion.div
      v-for="item in items"
      :key="item"
      :variants="itemVariants"
      class="p-6 bg-white rounded-xl shadow-lg"
    >
      {{ item }}
    </motion.div>
  </motion.div>
</template>
```
