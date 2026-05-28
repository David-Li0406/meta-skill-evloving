# Form Components

Button, Input, Select, Checkbox, Switch, and other form controls.

## Table of Contents
- [Button](#button)
- [Input](#input)
- [Textarea](#textarea)
- [Select](#select)
- [Checkbox](#checkbox)
- [Radio Group](#radio-group)
- [Switch](#switch)
- [Slider](#slider)
- [Toggle](#toggle)
- [Toggle Group](#toggle-group)
- [Label](#label)
- [Number Field](#number-field)
- [Pin Input](#pin-input)
- [Tags Input](#tags-input)
- [Combobox](#combobox)
- [Date Picker](#date-picker)
- [Calendar](#calendar)

---

## Button

```bash
pnpm dlx shadcn-vue@latest add button
```

### Basic Usage

```vue
<script setup lang="ts">
import { Button } from '@/components/ui/button'
</script>

<template>
  <Button>Click me</Button>
</template>
```

### Variants

```vue
<Button variant="default">Default</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="destructive">Destructive</Button>
<Button variant="outline">Outline</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="link">Link</Button>
```

### Sizes

```vue
<Button size="default">Default</Button>
<Button size="sm">Small</Button>
<Button size="lg">Large</Button>
<Button size="icon">
  <IconPlus class="h-4 w-4" />
</Button>
```

### With Icon

```vue
<script setup lang="ts">
import { Mail } from 'lucide-vue-next'
</script>

<template>
  <Button>
    <Mail class="mr-2 h-4 w-4" /> Login with Email
  </Button>
</template>
```

### Loading State

```vue
<script setup lang="ts">
import { Loader2 } from 'lucide-vue-next'
</script>

<template>
  <Button disabled>
    <Loader2 class="mr-2 h-4 w-4 animate-spin" />
    Please wait
  </Button>
</template>
```

### As Link

```vue
<Button as-child>
  <a href="/dashboard">Dashboard</a>
</Button>
```

---

## Input

```bash
pnpm dlx shadcn-vue@latest add input
```

### Basic Usage

```vue
<script setup lang="ts">
import { Input } from '@/components/ui/input'
</script>

<template>
  <Input type="email" placeholder="Email" />
</template>
```

### With Label

```vue
<script setup lang="ts">
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
</script>

<template>
  <div class="grid gap-1.5">
    <Label for="email">Email</Label>
    <Input id="email" type="email" placeholder="Email" />
  </div>
</template>
```

### Disabled

```vue
<Input disabled placeholder="Disabled" />
```

### With Button

```vue
<div class="flex gap-2">
  <Input type="email" placeholder="Email" />
  <Button type="submit">Subscribe</Button>
</div>
```

### File Input

```vue
<Input type="file" />
```

---

## Textarea

```bash
pnpm dlx shadcn-vue@latest add textarea
```

```vue
<script setup lang="ts">
import { Textarea } from '@/components/ui/textarea'
</script>

<template>
  <Textarea placeholder="Type your message here." />
</template>
```

### With Label

```vue
<div class="grid gap-1.5">
  <Label for="message">Your message</Label>
  <Textarea id="message" placeholder="Type here..." />
</div>
```

---

## Select

```bash
pnpm dlx shadcn-vue@latest add select
```

### Basic Usage

```vue
<script setup lang="ts">
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
</script>

<template>
  <Select>
    <SelectTrigger class="w-[180px]">
      <SelectValue placeholder="Select a fruit" />
    </SelectTrigger>
    <SelectContent>
      <SelectGroup>
        <SelectLabel>Fruits</SelectLabel>
        <SelectItem value="apple">Apple</SelectItem>
        <SelectItem value="banana">Banana</SelectItem>
        <SelectItem value="orange">Orange</SelectItem>
      </SelectGroup>
    </SelectContent>
  </Select>
</template>
```

### With v-model

```vue
<script setup lang="ts">
import { ref } from 'vue'

const selected = ref('')
</script>

<template>
  <Select v-model="selected">
    <SelectTrigger>
      <SelectValue placeholder="Select..." />
    </SelectTrigger>
    <SelectContent>
      <SelectItem value="1">Option 1</SelectItem>
      <SelectItem value="2">Option 2</SelectItem>
    </SelectContent>
  </Select>
</template>
```

---

## Checkbox

```bash
pnpm dlx shadcn-vue@latest add checkbox
```

### Basic Usage

```vue
<script setup lang="ts">
import { Checkbox } from '@/components/ui/checkbox'
</script>

<template>
  <div class="flex items-center space-x-2">
    <Checkbox id="terms" />
    <label for="terms">Accept terms and conditions</label>
  </div>
</template>
```

### With v-model

```vue
<script setup lang="ts">
import { ref } from 'vue'

const checked = ref(false)
</script>

<template>
  <Checkbox v-model:checked="checked" />
</template>
```

### Disabled

```vue
<Checkbox disabled />
<Checkbox disabled checked />
```

---

## Radio Group

```bash
pnpm dlx shadcn-vue@latest add radio-group
```

```vue
<script setup lang="ts">
import { ref } from 'vue'
import { Label } from '@/components/ui/label'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'

const selected = ref('comfortable')
</script>

<template>
  <RadioGroup v-model="selected">
    <div class="flex items-center space-x-2">
      <RadioGroupItem value="default" id="r1" />
      <Label for="r1">Default</Label>
    </div>
    <div class="flex items-center space-x-2">
      <RadioGroupItem value="comfortable" id="r2" />
      <Label for="r2">Comfortable</Label>
    </div>
    <div class="flex items-center space-x-2">
      <RadioGroupItem value="compact" id="r3" />
      <Label for="r3">Compact</Label>
    </div>
  </RadioGroup>
</template>
```

---

## Switch

```bash
pnpm dlx shadcn-vue@latest add switch
```

```vue
<script setup lang="ts">
import { ref } from 'vue'
import { Label } from '@/components/ui/label'
import { Switch } from '@/components/ui/switch'

const enabled = ref(false)
</script>

<template>
  <div class="flex items-center space-x-2">
    <Switch id="airplane-mode" v-model:checked="enabled" />
    <Label for="airplane-mode">Airplane Mode</Label>
  </div>
</template>
```

---

## Slider

```bash
pnpm dlx shadcn-vue@latest add slider
```

```vue
<script setup lang="ts">
import { ref } from 'vue'
import { Slider } from '@/components/ui/slider'

const value = ref([50])
</script>

<template>
  <Slider v-model="value" :max="100" :step="1" class="w-[60%]" />
</template>
```

### Range Slider

```vue
<script setup lang="ts">
const range = ref([25, 75])
</script>

<template>
  <Slider v-model="range" :max="100" :step="1" />
</template>
```

---

## Toggle

```bash
pnpm dlx shadcn-vue@latest add toggle
```

```vue
<script setup lang="ts">
import { Bold } from 'lucide-vue-next'
import { Toggle } from '@/components/ui/toggle'
</script>

<template>
  <Toggle aria-label="Toggle bold">
    <Bold class="h-4 w-4" />
  </Toggle>
</template>
```

### Variants

```vue
<Toggle variant="default">Default</Toggle>
<Toggle variant="outline">Outline</Toggle>
```

### Sizes

```vue
<Toggle size="sm">Small</Toggle>
<Toggle size="default">Default</Toggle>
<Toggle size="lg">Large</Toggle>
```

---

## Toggle Group

```bash
pnpm dlx shadcn-vue@latest add toggle-group
```

```vue
<script setup lang="ts">
import { AlignCenter, AlignLeft, AlignRight } from 'lucide-vue-next'
import { ToggleGroup, ToggleGroupItem } from '@/components/ui/toggle-group'
</script>

<template>
  <ToggleGroup type="single">
    <ToggleGroupItem value="left" aria-label="Align left">
      <AlignLeft class="h-4 w-4" />
    </ToggleGroupItem>
    <ToggleGroupItem value="center" aria-label="Align center">
      <AlignCenter class="h-4 w-4" />
    </ToggleGroupItem>
    <ToggleGroupItem value="right" aria-label="Align right">
      <AlignRight class="h-4 w-4" />
    </ToggleGroupItem>
  </ToggleGroup>
</template>
```

### Multiple Selection

```vue
<ToggleGroup type="multiple">
  <!-- items -->
</ToggleGroup>
```

---

## Number Field

```bash
pnpm dlx shadcn-vue@latest add number-field
```

```vue
<script setup lang="ts">
import { ref } from 'vue'
import {
  NumberField,
  NumberFieldContent,
  NumberFieldDecrement,
  NumberFieldIncrement,
  NumberFieldInput,
} from '@/components/ui/number-field'

const value = ref(0)
</script>

<template>
  <NumberField v-model="value" :min="0" :max="100">
    <NumberFieldContent>
      <NumberFieldDecrement />
      <NumberFieldInput />
      <NumberFieldIncrement />
    </NumberFieldContent>
  </NumberField>
</template>
```

---

## Pin Input

```bash
pnpm dlx shadcn-vue@latest add pin-input
```

```vue
<script setup lang="ts">
import { ref } from 'vue'
import { PinInput, PinInputGroup, PinInputInput } from '@/components/ui/pin-input'

const value = ref<string[]>([])
</script>

<template>
  <PinInput v-model="value" placeholder="○">
    <PinInputGroup>
      <PinInputInput v-for="(id, index) in 6" :key="id" :index="index" />
    </PinInputGroup>
  </PinInput>
</template>
```

---

## Tags Input

```bash
pnpm dlx shadcn-vue@latest add tags-input
```

```vue
<script setup lang="ts">
import { ref } from 'vue'
import {
  TagsInput,
  TagsInputInput,
  TagsInputItem,
  TagsInputItemDelete,
  TagsInputItemText,
} from '@/components/ui/tags-input'

const tags = ref(['Vue', 'TypeScript'])
</script>

<template>
  <TagsInput v-model="tags">
    <TagsInputItem v-for="tag in tags" :key="tag" :value="tag">
      <TagsInputItemText />
      <TagsInputItemDelete />
    </TagsInputItem>
    <TagsInputInput placeholder="Add tag..." />
  </TagsInput>
</template>
```

---

## Combobox

```bash
pnpm dlx shadcn-vue@latest add combobox
```

```vue
<script setup lang="ts">
import { ref } from 'vue'
import { Check, ChevronsUpDown } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from '@/components/ui/command'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'
import { cn } from '@/lib/utils'

const frameworks = [
  { value: 'vue', label: 'Vue' },
  { value: 'react', label: 'React' },
  { value: 'angular', label: 'Angular' },
  { value: 'svelte', label: 'Svelte' },
]

const open = ref(false)
const value = ref('')

const selectedLabel = computed(() => 
  frameworks.find(f => f.value === value.value)?.label ?? 'Select framework...'
)
</script>

<template>
  <Popover v-model:open="open">
    <PopoverTrigger as-child>
      <Button variant="outline" role="combobox" class="w-[200px] justify-between">
        {{ selectedLabel }}
        <ChevronsUpDown class="ml-2 h-4 w-4 shrink-0 opacity-50" />
      </Button>
    </PopoverTrigger>
    <PopoverContent class="w-[200px] p-0">
      <Command>
        <CommandInput placeholder="Search framework..." />
        <CommandEmpty>No framework found.</CommandEmpty>
        <CommandList>
          <CommandGroup>
            <CommandItem
              v-for="framework in frameworks"
              :key="framework.value"
              :value="framework.value"
              @select="value = framework.value; open = false"
            >
              <Check :class="cn('mr-2 h-4 w-4', value === framework.value ? 'opacity-100' : 'opacity-0')" />
              {{ framework.label }}
            </CommandItem>
          </CommandGroup>
        </CommandList>
      </Command>
    </PopoverContent>
  </Popover>
</template>
```

---

## Date Picker

```bash
pnpm dlx shadcn-vue@latest add date-picker calendar popover button
```

```vue
<script setup lang="ts">
import { ref } from 'vue'
import { CalendarDate, DateFormatter, getLocalTimeZone } from '@internationalized/date'
import { Calendar as CalendarIcon } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Calendar } from '@/components/ui/calendar'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'
import { cn } from '@/lib/utils'

const df = new DateFormatter('en-US', { dateStyle: 'long' })
const value = ref<CalendarDate>()
</script>

<template>
  <Popover>
    <PopoverTrigger as-child>
      <Button
        variant="outline"
        :class="cn('w-[280px] justify-start text-left font-normal', !value && 'text-muted-foreground')"
      >
        <CalendarIcon class="mr-2 h-4 w-4" />
        {{ value ? df.format(value.toDate(getLocalTimeZone())) : 'Pick a date' }}
      </Button>
    </PopoverTrigger>
    <PopoverContent class="w-auto p-0">
      <Calendar v-model="value" initial-focus />
    </PopoverContent>
  </Popover>
</template>
```

---

## Calendar

```bash
pnpm dlx shadcn-vue@latest add calendar
```

```vue
<script setup lang="ts">
import { ref } from 'vue'
import { Calendar } from '@/components/ui/calendar'

const date = ref()
</script>

<template>
  <Calendar v-model="date" class="rounded-md border" />
</template>
```

### Range Calendar

```bash
pnpm dlx shadcn-vue@latest add range-calendar
```

```vue
<script setup lang="ts">
import { ref } from 'vue'
import { RangeCalendar } from '@/components/ui/range-calendar'

const range = ref()
</script>

<template>
  <RangeCalendar v-model="range" class="rounded-md border" />
</template>
```
