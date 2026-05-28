# Data Display Components

Table, Data Table, Avatar, Badge, and other data display components.

## Table of Contents
- [Table](#table)
- [Data Table](#data-table)
- [Avatar](#avatar)
- [Badge](#badge)
- [Carousel](#carousel)
- [Empty](#empty)
- [Breadcrumb](#breadcrumb)
- [Pagination](#pagination)
- [Stepper](#stepper)
- [Typography](#typography)

---

## Table

```bash
pnpm dlx shadcn-vue@latest add table
```

### Basic Usage

```vue
<script setup lang="ts">
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'

const invoices = [
  { id: 'INV001', status: 'Paid', method: 'Credit Card', amount: '$250.00' },
  { id: 'INV002', status: 'Pending', method: 'PayPal', amount: '$150.00' },
  { id: 'INV003', status: 'Unpaid', method: 'Bank Transfer', amount: '$350.00' },
]
</script>

<template>
  <Table>
    <TableCaption>A list of your recent invoices.</TableCaption>
    <TableHeader>
      <TableRow>
        <TableHead class="w-[100px]">Invoice</TableHead>
        <TableHead>Status</TableHead>
        <TableHead>Method</TableHead>
        <TableHead class="text-right">Amount</TableHead>
      </TableRow>
    </TableHeader>
    <TableBody>
      <TableRow v-for="invoice in invoices" :key="invoice.id">
        <TableCell class="font-medium">{{ invoice.id }}</TableCell>
        <TableCell>{{ invoice.status }}</TableCell>
        <TableCell>{{ invoice.method }}</TableCell>
        <TableCell class="text-right">{{ invoice.amount }}</TableCell>
      </TableRow>
    </TableBody>
  </Table>
</template>
```

---

## Data Table

Full-featured data table with sorting, filtering, and pagination.

```bash
pnpm dlx shadcn-vue@latest add table
pnpm add @tanstack/vue-table
```

### Basic Setup

```vue
<script setup lang="ts">
import { ref } from 'vue'
import {
  FlexRender,
  getCoreRowModel,
  useVueTable,
  getPaginationRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  type ColumnDef,
  type SortingState,
} from '@tanstack/vue-table'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

interface Payment {
  id: string
  amount: number
  status: 'pending' | 'processing' | 'success' | 'failed'
  email: string
}

const data = ref<Payment[]>([
  { id: '1', amount: 100, status: 'pending', email: 'john@example.com' },
  { id: '2', amount: 200, status: 'success', email: 'jane@example.com' },
])

const sorting = ref<SortingState>([])
const globalFilter = ref('')

const columns: ColumnDef<Payment>[] = [
  {
    accessorKey: 'status',
    header: 'Status',
  },
  {
    accessorKey: 'email',
    header: 'Email',
  },
  {
    accessorKey: 'amount',
    header: () => h('div', { class: 'text-right' }, 'Amount'),
    cell: ({ row }) => {
      const amount = Number.parseFloat(row.getValue('amount'))
      const formatted = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
      }).format(amount)
      return h('div', { class: 'text-right font-medium' }, formatted)
    },
  },
]

const table = useVueTable({
  get data() { return data.value },
  columns,
  getCoreRowModel: getCoreRowModel(),
  getPaginationRowModel: getPaginationRowModel(),
  getSortedRowModel: getSortedRowModel(),
  getFilteredRowModel: getFilteredRowModel(),
  state: {
    get sorting() { return sorting.value },
    get globalFilter() { return globalFilter.value },
  },
  onSortingChange: updater => {
    sorting.value = typeof updater === 'function' ? updater(sorting.value) : updater
  },
})
</script>

<template>
  <div>
    <div class="flex items-center py-4">
      <Input
        v-model="globalFilter"
        placeholder="Filter..."
        class="max-w-sm"
      />
    </div>
    <div class="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow v-for="headerGroup in table.getHeaderGroups()" :key="headerGroup.id">
            <TableHead v-for="header in headerGroup.headers" :key="header.id">
              <FlexRender
                v-if="!header.isPlaceholder"
                :render="header.column.columnDef.header"
                :props="header.getContext()"
              />
            </TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <template v-if="table.getRowModel().rows?.length">
            <TableRow
              v-for="row in table.getRowModel().rows"
              :key="row.id"
              :data-state="row.getIsSelected() && 'selected'"
            >
              <TableCell v-for="cell in row.getVisibleCells()" :key="cell.id">
                <FlexRender
                  :render="cell.column.columnDef.cell"
                  :props="cell.getContext()"
                />
              </TableCell>
            </TableRow>
          </template>
          <TableRow v-else>
            <TableCell :colspan="columns.length" class="h-24 text-center">
              No results.
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </div>
    <div class="flex items-center justify-end space-x-2 py-4">
      <Button
        variant="outline"
        size="sm"
        :disabled="!table.getCanPreviousPage()"
        @click="table.previousPage()"
      >
        Previous
      </Button>
      <Button
        variant="outline"
        size="sm"
        :disabled="!table.getCanNextPage()"
        @click="table.nextPage()"
      >
        Next
      </Button>
    </div>
  </div>
</template>
```

### Column with Sorting

```typescript
const columns: ColumnDef<Payment>[] = [
  {
    accessorKey: 'email',
    header: ({ column }) => {
      return h(Button, {
        variant: 'ghost',
        onClick: () => column.toggleSorting(column.getIsSorted() === 'asc'),
      }, () => ['Email', h(ArrowUpDown, { class: 'ml-2 h-4 w-4' })])
    },
  },
]
```

### Row Selection

```typescript
import { Checkbox } from '@/components/ui/checkbox'

const columns: ColumnDef<Payment>[] = [
  {
    id: 'select',
    header: ({ table }) => h(Checkbox, {
      checked: table.getIsAllPageRowsSelected(),
      'onUpdate:checked': (value: boolean) => table.toggleAllPageRowsSelected(!!value),
      ariaLabel: 'Select all',
    }),
    cell: ({ row }) => h(Checkbox, {
      checked: row.getIsSelected(),
      'onUpdate:checked': (value: boolean) => row.toggleSelected(!!value),
      ariaLabel: 'Select row',
    }),
  },
  // ... other columns
]
```

---

## Avatar

```bash
pnpm dlx shadcn-vue@latest add avatar
```

### Basic Usage

```vue
<script setup lang="ts">
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
</script>

<template>
  <Avatar>
    <AvatarImage src="https://github.com/vuejs.png" alt="@vuejs" />
    <AvatarFallback>VU</AvatarFallback>
  </Avatar>
</template>
```

### Sizes

```vue
<Avatar class="h-6 w-6">...</Avatar>
<Avatar class="h-8 w-8">...</Avatar>
<Avatar class="h-10 w-10">...</Avatar>
<Avatar class="h-12 w-12">...</Avatar>
```

### Avatar Group

```vue
<div class="flex -space-x-4">
  <Avatar class="border-2 border-background">
    <AvatarImage src="..." />
    <AvatarFallback>A</AvatarFallback>
  </Avatar>
  <Avatar class="border-2 border-background">
    <AvatarImage src="..." />
    <AvatarFallback>B</AvatarFallback>
  </Avatar>
  <Avatar class="border-2 border-background">
    <AvatarFallback>+3</AvatarFallback>
  </Avatar>
</div>
```

---

## Badge

```bash
pnpm dlx shadcn-vue@latest add badge
```

### Basic Usage

```vue
<script setup lang="ts">
import { Badge } from '@/components/ui/badge'
</script>

<template>
  <Badge>Badge</Badge>
</template>
```

### Variants

```vue
<Badge variant="default">Default</Badge>
<Badge variant="secondary">Secondary</Badge>
<Badge variant="destructive">Destructive</Badge>
<Badge variant="outline">Outline</Badge>
```

### With Icon

```vue
<Badge>
  <Check class="mr-1 h-3 w-3" />
  Verified
</Badge>
```

---

## Carousel

```bash
pnpm dlx shadcn-vue@latest add carousel
```

```vue
<script setup lang="ts">
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from '@/components/ui/carousel'
import { Card, CardContent } from '@/components/ui/card'
</script>

<template>
  <Carousel class="w-full max-w-xs">
    <CarouselContent>
      <CarouselItem v-for="index in 5" :key="index">
        <div class="p-1">
          <Card>
            <CardContent class="flex aspect-square items-center justify-center p-6">
              <span class="text-4xl font-semibold">{{ index }}</span>
            </CardContent>
          </Card>
        </div>
      </CarouselItem>
    </CarouselContent>
    <CarouselPrevious />
    <CarouselNext />
  </Carousel>
</template>
```

### Multiple Items

```vue
<Carousel :opts="{ align: 'start' }" class="w-full max-w-sm">
  <CarouselContent>
    <CarouselItem v-for="index in 5" :key="index" class="md:basis-1/2 lg:basis-1/3">
      <!-- content -->
    </CarouselItem>
  </CarouselContent>
</Carousel>
```

### Vertical

```vue
<Carousel orientation="vertical" class="w-full max-w-xs">
  <!-- content -->
</Carousel>
```

---

## Empty

Empty state placeholder.

```bash
pnpm dlx shadcn-vue@latest add empty
```

```vue
<script setup lang="ts">
import { Empty, EmptyDescription, EmptyIcon, EmptyTitle } from '@/components/ui/empty'
import { Inbox } from 'lucide-vue-next'
</script>

<template>
  <Empty>
    <EmptyIcon :icon="Inbox" />
    <EmptyTitle>No messages</EmptyTitle>
    <EmptyDescription>
      You don't have any messages yet.
    </EmptyDescription>
  </Empty>
</template>
```

---

## Breadcrumb

```bash
pnpm dlx shadcn-vue@latest add breadcrumb
```

```vue
<script setup lang="ts">
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from '@/components/ui/breadcrumb'
</script>

<template>
  <Breadcrumb>
    <BreadcrumbList>
      <BreadcrumbItem>
        <BreadcrumbLink href="/">Home</BreadcrumbLink>
      </BreadcrumbItem>
      <BreadcrumbSeparator />
      <BreadcrumbItem>
        <BreadcrumbLink href="/products">Products</BreadcrumbLink>
      </BreadcrumbItem>
      <BreadcrumbSeparator />
      <BreadcrumbItem>
        <BreadcrumbPage>Current Page</BreadcrumbPage>
      </BreadcrumbItem>
    </BreadcrumbList>
  </Breadcrumb>
</template>
```

### With Dropdown

```vue
<BreadcrumbItem>
  <DropdownMenu>
    <DropdownMenuTrigger class="flex items-center gap-1">
      Components
      <ChevronDown class="h-4 w-4" />
    </DropdownMenuTrigger>
    <DropdownMenuContent>
      <DropdownMenuItem>Documentation</DropdownMenuItem>
      <DropdownMenuItem>Themes</DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>
</BreadcrumbItem>
```

---

## Pagination

```bash
pnpm dlx shadcn-vue@latest add pagination
```

```vue
<script setup lang="ts">
import {
  Pagination,
  PaginationEllipsis,
  PaginationFirst,
  PaginationLast,
  PaginationList,
  PaginationListItem,
  PaginationNext,
  PaginationPrev,
} from '@/components/ui/pagination'
import { Button } from '@/components/ui/button'
</script>

<template>
  <Pagination :total="100" :sibling-count="1" show-edges :default-page="1">
    <PaginationList v-slot="{ items }" class="flex items-center gap-1">
      <PaginationFirst />
      <PaginationPrev />
      <template v-for="(item, index) in items">
        <PaginationListItem v-if="item.type === 'page'" :key="index" :value="item.value" as-child>
          <Button variant="outline" class="w-10 h-10 p-0">
            {{ item.value }}
          </Button>
        </PaginationListItem>
        <PaginationEllipsis v-else :key="item.type" :index="index" />
      </template>
      <PaginationNext />
      <PaginationLast />
    </PaginationList>
  </Pagination>
</template>
```

---

## Stepper

```bash
pnpm dlx shadcn-vue@latest add stepper
```

```vue
<script setup lang="ts">
import { ref } from 'vue'
import {
  Stepper,
  StepperDescription,
  StepperItem,
  StepperSeparator,
  StepperTitle,
  StepperTrigger,
} from '@/components/ui/stepper'

const currentStep = ref(1)
const steps = [
  { title: 'Step 1', description: 'Description 1' },
  { title: 'Step 2', description: 'Description 2' },
  { title: 'Step 3', description: 'Description 3' },
]
</script>

<template>
  <Stepper v-model="currentStep">
    <StepperItem
      v-for="(step, index) in steps"
      :key="index"
      :step="index + 1"
    >
      <StepperTrigger>
        <StepperTitle>{{ step.title }}</StepperTitle>
        <StepperDescription>{{ step.description }}</StepperDescription>
      </StepperTrigger>
      <StepperSeparator v-if="index < steps.length - 1" />
    </StepperItem>
  </Stepper>
</template>
```

---

## Typography

```bash
pnpm dlx shadcn-vue@latest add typography
```

Pre-styled prose for content.

```vue
<script setup lang="ts">
import { Typography } from '@/components/ui/typography'
</script>

<template>
  <Typography>
    <h1>The Joke Tax Chronicles</h1>
    <p>
      Once upon a time, in a far-off land, there was a very lazy king who
      spent all day lounging on his throne.
    </p>
    <h2>The King's Plan</h2>
    <p>
      The king thought long and hard, and finally came up with
      <a href="#">a brilliant plan</a>: he would tax the jokes.
    </p>
    <blockquote>
      "After all," he said, "everyone enjoys a good joke."
    </blockquote>
    <ul>
      <li>First item</li>
      <li>Second item</li>
      <li>Third item</li>
    </ul>
  </Typography>
</template>
```
