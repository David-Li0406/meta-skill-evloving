# Layout Components

Card, Dialog, Sheet, Drawer, Sidebar, and other container components.

## Table of Contents
- [Card](#card)
- [Dialog](#dialog)
- [Sheet](#sheet)
- [Drawer](#drawer)
- [Sidebar](#sidebar)
- [Collapsible](#collapsible)
- [Accordion](#accordion)
- [Tabs](#tabs)
- [Resizable](#resizable)
- [Scroll Area](#scroll-area)
- [Separator](#separator)
- [Aspect Ratio](#aspect-ratio)

---

## Card

```bash
pnpm dlx shadcn-vue@latest add card
```

### Basic Usage

```vue
<script setup lang="ts">
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
</script>

<template>
  <Card class="w-[350px]">
    <CardHeader>
      <CardTitle>Create project</CardTitle>
      <CardDescription>Deploy your new project in one-click.</CardDescription>
    </CardHeader>
    <CardContent>
      <div class="grid gap-4">
        <div class="grid gap-2">
          <Label for="name">Name</Label>
          <Input id="name" placeholder="Name of your project" />
        </div>
      </div>
    </CardContent>
    <CardFooter class="flex justify-between">
      <Button variant="outline">Cancel</Button>
      <Button>Deploy</Button>
    </CardFooter>
  </Card>
</template>
```

---

## Dialog

```bash
pnpm dlx shadcn-vue@latest add dialog
```

### Basic Usage

```vue
<script setup lang="ts">
import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogClose,
} from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
</script>

<template>
  <Dialog>
    <DialogTrigger as-child>
      <Button variant="outline">Edit Profile</Button>
    </DialogTrigger>
    <DialogContent class="sm:max-w-[425px]">
      <DialogHeader>
        <DialogTitle>Edit profile</DialogTitle>
        <DialogDescription>
          Make changes to your profile here. Click save when you're done.
        </DialogDescription>
      </DialogHeader>
      <div class="grid gap-4 py-4">
        <div class="grid grid-cols-4 items-center gap-4">
          <Label for="name" class="text-right">Name</Label>
          <Input id="name" value="John Doe" class="col-span-3" />
        </div>
      </div>
      <DialogFooter>
        <DialogClose as-child>
          <Button variant="outline">Cancel</Button>
        </DialogClose>
        <Button type="submit">Save changes</Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
```

### Controlled Dialog

```vue
<script setup lang="ts">
import { ref } from 'vue'

const open = ref(false)
</script>

<template>
  <Dialog v-model:open="open">
    <DialogTrigger as-child>
      <Button>Open</Button>
    </DialogTrigger>
    <DialogContent>
      <DialogHeader>
        <DialogTitle>Title</DialogTitle>
      </DialogHeader>
      <p>Content here</p>
      <DialogFooter>
        <Button @click="open = false">Close</Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
```

### Dialog with Form

```vue
<template>
  <Dialog>
    <DialogTrigger as-child>
      <Button>Open Form</Button>
    </DialogTrigger>
    <DialogContent>
      <form @submit.prevent="handleSubmit">
        <DialogHeader>
          <DialogTitle>Create Account</DialogTitle>
        </DialogHeader>
        <div class="py-4">
          <Input v-model="email" placeholder="Email" />
        </div>
        <DialogFooter>
          <Button type="submit">Submit</Button>
        </DialogFooter>
      </form>
    </DialogContent>
  </Dialog>
</template>
```

---

## Sheet

Side panel overlay.

```bash
pnpm dlx shadcn-vue@latest add sheet
```

```vue
<script setup lang="ts">
import { Button } from '@/components/ui/button'
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
  SheetFooter,
  SheetClose,
} from '@/components/ui/sheet'
</script>

<template>
  <Sheet>
    <SheetTrigger as-child>
      <Button variant="outline">Open</Button>
    </SheetTrigger>
    <SheetContent>
      <SheetHeader>
        <SheetTitle>Edit profile</SheetTitle>
        <SheetDescription>
          Make changes to your profile here.
        </SheetDescription>
      </SheetHeader>
      <div class="py-4">
        <!-- Content -->
      </div>
      <SheetFooter>
        <SheetClose as-child>
          <Button type="submit">Save</Button>
        </SheetClose>
      </SheetFooter>
    </SheetContent>
  </Sheet>
</template>
```

### Sheet Positions

```vue
<SheetContent side="top">...</SheetContent>
<SheetContent side="bottom">...</SheetContent>
<SheetContent side="left">...</SheetContent>
<SheetContent side="right">...</SheetContent>
```

---

## Drawer

Mobile-friendly bottom sheet.

```bash
pnpm dlx shadcn-vue@latest add drawer
```

```vue
<script setup lang="ts">
import { Button } from '@/components/ui/button'
import {
  Drawer,
  DrawerContent,
  DrawerDescription,
  DrawerFooter,
  DrawerHeader,
  DrawerTitle,
  DrawerTrigger,
  DrawerClose,
} from '@/components/ui/drawer'
</script>

<template>
  <Drawer>
    <DrawerTrigger as-child>
      <Button variant="outline">Open Drawer</Button>
    </DrawerTrigger>
    <DrawerContent>
      <DrawerHeader>
        <DrawerTitle>Are you sure?</DrawerTitle>
        <DrawerDescription>This action cannot be undone.</DrawerDescription>
      </DrawerHeader>
      <div class="p-4">
        <!-- Content -->
      </div>
      <DrawerFooter>
        <Button>Submit</Button>
        <DrawerClose as-child>
          <Button variant="outline">Cancel</Button>
        </DrawerClose>
      </DrawerFooter>
    </DrawerContent>
  </Drawer>
</template>
```

---

## Sidebar

Application sidebar navigation.

```bash
pnpm dlx shadcn-vue@latest add sidebar
```

### Basic Setup

```vue
<script setup lang="ts">
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarProvider,
  SidebarTrigger,
} from '@/components/ui/sidebar'
import { Home, Inbox, Settings } from 'lucide-vue-next'

const items = [
  { title: 'Home', icon: Home, url: '/' },
  { title: 'Inbox', icon: Inbox, url: '/inbox' },
  { title: 'Settings', icon: Settings, url: '/settings' },
]
</script>

<template>
  <SidebarProvider>
    <Sidebar>
      <SidebarHeader>
        <h2 class="text-lg font-semibold">My App</h2>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Navigation</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem v-for="item in items" :key="item.title">
                <SidebarMenuButton as-child>
                  <a :href="item.url">
                    <component :is="item.icon" />
                    <span>{{ item.title }}</span>
                  </a>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter>
        <p class="text-sm text-muted-foreground">© 2024</p>
      </SidebarFooter>
    </Sidebar>
    <main class="flex-1 p-4">
      <SidebarTrigger />
      <!-- Page content -->
    </main>
  </SidebarProvider>
</template>
```

---

## Collapsible

```bash
pnpm dlx shadcn-vue@latest add collapsible
```

```vue
<script setup lang="ts">
import { ref } from 'vue'
import { ChevronsUpDown } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from '@/components/ui/collapsible'

const isOpen = ref(false)
</script>

<template>
  <Collapsible v-model:open="isOpen" class="w-[350px] space-y-2">
    <div class="flex items-center justify-between space-x-4 px-4">
      <h4 class="text-sm font-semibold">@peduarte starred 3 repositories</h4>
      <CollapsibleTrigger as-child>
        <Button variant="ghost" size="sm">
          <ChevronsUpDown class="h-4 w-4" />
          <span class="sr-only">Toggle</span>
        </Button>
      </CollapsibleTrigger>
    </div>
    <div class="rounded-md border px-4 py-2 font-mono text-sm">
      @radix-ui/primitives
    </div>
    <CollapsibleContent class="space-y-2">
      <div class="rounded-md border px-4 py-2 font-mono text-sm">
        @radix-ui/colors
      </div>
      <div class="rounded-md border px-4 py-2 font-mono text-sm">
        @stitches/react
      </div>
    </CollapsibleContent>
  </Collapsible>
</template>
```

---

## Accordion

```bash
pnpm dlx shadcn-vue@latest add accordion
```

```vue
<script setup lang="ts">
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion'
</script>

<template>
  <Accordion type="single" collapsible class="w-full">
    <AccordionItem value="item-1">
      <AccordionTrigger>Is it accessible?</AccordionTrigger>
      <AccordionContent>
        Yes. It adheres to the WAI-ARIA design pattern.
      </AccordionContent>
    </AccordionItem>
    <AccordionItem value="item-2">
      <AccordionTrigger>Is it styled?</AccordionTrigger>
      <AccordionContent>
        Yes. It comes with default styles that match the other components.
      </AccordionContent>
    </AccordionItem>
  </Accordion>
</template>
```

### Multiple Open Items

```vue
<Accordion type="multiple">
  <!-- items -->
</Accordion>
```

---

## Tabs

```bash
pnpm dlx shadcn-vue@latest add tabs
```

```vue
<script setup lang="ts">
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
</script>

<template>
  <Tabs default-value="account" class="w-[400px]">
    <TabsList>
      <TabsTrigger value="account">Account</TabsTrigger>
      <TabsTrigger value="password">Password</TabsTrigger>
    </TabsList>
    <TabsContent value="account">
      <p>Account settings here.</p>
    </TabsContent>
    <TabsContent value="password">
      <p>Password settings here.</p>
    </TabsContent>
  </Tabs>
</template>
```

---

## Resizable

```bash
pnpm dlx shadcn-vue@latest add resizable
```

```vue
<script setup lang="ts">
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from '@/components/ui/resizable'
</script>

<template>
  <ResizablePanelGroup direction="horizontal" class="min-h-[200px] max-w-md rounded-lg border">
    <ResizablePanel :default-size="50">
      <div class="flex h-full items-center justify-center p-6">
        <span class="font-semibold">One</span>
      </div>
    </ResizablePanel>
    <ResizableHandle />
    <ResizablePanel :default-size="50">
      <div class="flex h-full items-center justify-center p-6">
        <span class="font-semibold">Two</span>
      </div>
    </ResizablePanel>
  </ResizablePanelGroup>
</template>
```

### Vertical

```vue
<ResizablePanelGroup direction="vertical">
  <!-- panels -->
</ResizablePanelGroup>
```

---

## Scroll Area

```bash
pnpm dlx shadcn-vue@latest add scroll-area
```

```vue
<script setup lang="ts">
import { ScrollArea } from '@/components/ui/scroll-area'
import { Separator } from '@/components/ui/separator'

const tags = Array.from({ length: 50 }).map((_, i) => `Tag ${i + 1}`)
</script>

<template>
  <ScrollArea class="h-72 w-48 rounded-md border">
    <div class="p-4">
      <h4 class="mb-4 text-sm font-medium leading-none">Tags</h4>
      <div v-for="tag in tags" :key="tag">
        <div class="text-sm">{{ tag }}</div>
        <Separator class="my-2" />
      </div>
    </div>
  </ScrollArea>
</template>
```

### Horizontal Scroll

```vue
<ScrollArea class="w-96 whitespace-nowrap rounded-md border">
  <div class="flex w-max space-x-4 p-4">
    <!-- horizontal content -->
  </div>
</ScrollArea>
```

---

## Separator

```bash
pnpm dlx shadcn-vue@latest add separator
```

```vue
<script setup lang="ts">
import { Separator } from '@/components/ui/separator'
</script>

<template>
  <div>
    <div class="space-y-1">
      <h4 class="text-sm font-medium leading-none">Radix Primitives</h4>
      <p class="text-sm text-muted-foreground">An open-source UI component library.</p>
    </div>
    <Separator class="my-4" />
    <div class="flex h-5 items-center space-x-4 text-sm">
      <div>Blog</div>
      <Separator orientation="vertical" />
      <div>Docs</div>
      <Separator orientation="vertical" />
      <div>Source</div>
    </div>
  </div>
</template>
```

---

## Aspect Ratio

```bash
pnpm dlx shadcn-vue@latest add aspect-ratio
```

```vue
<script setup lang="ts">
import { AspectRatio } from '@/components/ui/aspect-ratio'
</script>

<template>
  <div class="w-[450px]">
    <AspectRatio :ratio="16 / 9">
      <img
        src="https://images.unsplash.com/photo-1588345921523-c2dcdb7f1dcd?w=800"
        alt="Photo"
        class="rounded-md object-cover"
      />
    </AspectRatio>
  </div>
</template>
```
