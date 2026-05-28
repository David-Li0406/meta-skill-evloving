# HTML to shadcn Component Mapping

Quick reference for mapping Stitch HTML patterns to shadcn/ui components.

## Table of Contents
- [Icon Mapping](#icon-mapping)
- [Buttons](#buttons)
- [Form Inputs](#form-inputs)
- [Data Display](#data-display)
- [Feedback](#feedback)
- [Navigation](#navigation)
- [Overlays](#overlays)
- [Layout](#layout)
- [Tailwind Patterns](#tailwind-patterns)

---

## Icon Mapping

Stitch uses Material Symbols (`material-symbols-outlined`). Convert to Lucide React icons.

| Material Symbol | Lucide Icon | Import |
|-----------------|-------------|--------|
| `close` | X | `import { X } from "lucide-react"` |
| `search` | Search | `import { Search } from "lucide-react"` |
| `settings` | Settings | `import { Settings } from "lucide-react"` |
| `add` / `add_circle` | Plus / PlusCircle | `import { Plus } from "lucide-react"` |
| `delete` | Trash2 | `import { Trash2 } from "lucide-react"` |
| `folder` | Folder / FolderOpen | `import { Folder } from "lucide-react"` |
| `folder_open` | FolderOpen | `import { FolderOpen } from "lucide-react"` |
| `terminal` | Terminal | `import { Terminal } from "lucide-react"` |
| `code` | Code | `import { Code } from "lucide-react"` |
| `info` | Info | `import { Info } from "lucide-react"` |
| `help` | HelpCircle | `import { HelpCircle } from "lucide-react"` |
| `arrow_upward` | ArrowUp | `import { ArrowUp } from "lucide-react"` |
| `arrow_downward` | ArrowDown | `import { ArrowDown } from "lucide-react"` |
| `keyboard_arrow_down` | ChevronDown | `import { ChevronDown } from "lucide-react"` |
| `keyboard_arrow_right` | ChevronRight | `import { ChevronRight } from "lucide-react"` |
| `keyboard_arrow_up` | ChevronUp | `import { ChevronUp } from "lucide-react"` |
| `more_horiz` | MoreHorizontal | `import { MoreHorizontal } from "lucide-react"` |
| `more_vert` | MoreVertical | `import { MoreVertical } from "lucide-react"` |
| `link` | Link | `import { Link } from "lucide-react"` |
| `image` | Image | `import { Image } from "lucide-react"` |
| `filter_list` | Filter | `import { Filter } from "lucide-react"` |
| `bolt` | Zap | `import { Zap } from "lucide-react"` |
| `token` | Coins | `import { Coins } from "lucide-react"` |
| `check_circle` | CheckCircle | `import { CheckCircle } from "lucide-react"` |
| `dock_to_right` | PanelRight | `import { PanelRight } from "lucide-react"` |
| `data_object` | Braces | `import { Braces } from "lucide-react"` |

### Filled Icons
Stitch uses `style="font-variation-settings: 'FILL' 1;"` for filled icons. In Lucide, use solid variants or add `fill="currentColor"`:

```tsx
// Filled folder in Stitch
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">folder</span>

// Lucide equivalent
<Folder className="fill-current" />
```

---

## Buttons

| HTML Pattern | shadcn Component | Variant/Props |
|--------------|------------------|---------------|
| `<button class="primary">` | Button | `variant="default"` |
| `<button class="secondary">` | Button | `variant="secondary"` |
| `<button class="outline">` | Button | `variant="outline"` |
| `<button class="ghost">` | Button | `variant="ghost"` |
| `<button class="destructive">` | Button | `variant="destructive"` |
| `<button class="link">` | Button | `variant="link"` |
| `<button class="icon">` | Button | `variant="ghost" size="icon"` |
| `<button class="sm">` | Button | `size="sm"` |
| `<button class="lg">` | Button | `size="lg"` |
| Button with loading spinner | Button + Loader2 icon | Add `disabled` + animate-spin icon |

### Button with Icon Example
```tsx
<Button variant="outline" size="sm">
  <PlusIcon className="mr-2 h-4 w-4" />
  Add Item
</Button>
```

---

## Form Inputs

| HTML Pattern | shadcn Component | Notes |
|--------------|------------------|-------|
| `<input type="text">` | Input | Basic text input |
| `<input type="password">` | Input | `type="password"` |
| `<input type="email">` | Input | `type="email"` |
| `<input type="search">` | Input | `type="search"` |
| `<textarea>` | Textarea | Multi-line input |
| `<select>` | Select | Use Select + SelectTrigger + SelectContent + SelectItem |
| `<input type="checkbox">` | Checkbox | Standalone checkbox |
| `<input type="radio">` | RadioGroup | RadioGroup + RadioGroupItem |
| `<input type="range">` | Slider | Range slider |
| `<input type="file">` | Input | `type="file"` or custom Dropzone |
| Toggle/switch | Switch | On/off toggle |
| Date picker | Calendar + Popover | Date selection |
| Combobox/autocomplete | Combobox | Searchable select |

### Form Field Wrapper Pattern
```tsx
<div className="space-y-2">
  <Label htmlFor="email">Email</Label>
  <Input id="email" type="email" placeholder="email@example.com" />
  <p className="text-sm text-muted-foreground">Helper text here</p>
</div>
```

---

## Data Display

| HTML Pattern | shadcn Component | Notes |
|--------------|------------------|-------|
| Card container | Card | Card + CardHeader + CardContent + CardFooter |
| Badge/tag/chip | Badge | `variant="default|secondary|destructive|outline"` |
| Avatar/profile image | Avatar | Avatar + AvatarImage + AvatarFallback |
| Data table | Table | Table + TableHeader + TableBody + TableRow + TableCell |
| Progress bar | Progress | `value={percent}` |
| Skeleton loader | Skeleton | Loading placeholder |
| Separator/divider | Separator | `orientation="horizontal|vertical"` |
| Code block | Code snippets | Use `<pre><code>` with syntax highlighting |
| Key-value list | Description list | Custom or dl/dt/dd pattern |

### Card Example
```tsx
<Card>
  <CardHeader>
    <CardTitle>Card Title</CardTitle>
    <CardDescription>Card description</CardDescription>
  </CardHeader>
  <CardContent>
    <p>Content here</p>
  </CardContent>
  <CardFooter>
    <Button>Action</Button>
  </CardFooter>
</Card>
```

### Badge Variants
```tsx
<Badge>Default</Badge>
<Badge variant="secondary">Secondary</Badge>
<Badge variant="destructive">Error</Badge>
<Badge variant="outline">Outline</Badge>
```

---

## Feedback

| HTML Pattern | shadcn Component | Notes |
|--------------|------------------|-------|
| Alert/notification | Alert | Alert + AlertTitle + AlertDescription |
| Toast/snackbar | Toast | Use Sonner or shadcn Toast |
| Tooltip | Tooltip | Tooltip + TooltipTrigger + TooltipContent |
| Loading spinner | Loader2 icon | `animate-spin` class |
| Empty state | Custom | Card with illustration + message |

### Alert Example
```tsx
<Alert variant="destructive">
  <AlertCircle className="h-4 w-4" />
  <AlertTitle>Error</AlertTitle>
  <AlertDescription>Something went wrong.</AlertDescription>
</Alert>
```

---

## Navigation

| HTML Pattern | shadcn Component | Notes |
|--------------|------------------|-------|
| Tabs | Tabs | Tabs + TabsList + TabsTrigger + TabsContent |
| Breadcrumbs | Breadcrumb | Breadcrumb + BreadcrumbList + BreadcrumbItem |
| Pagination | Pagination | Pagination components |
| Navigation menu | NavigationMenu | Complex nav with dropdowns |
| Sidebar nav | Custom | Compose from Button/Link |
| Accordion/collapsible | Accordion | Accordion + AccordionItem + AccordionTrigger + AccordionContent |
| Command menu | Command | Command palette (Cmd+K style) |
| Dropdown menu | DropdownMenu | DropdownMenu + DropdownMenuTrigger + DropdownMenuContent + DropdownMenuItem |

### Tabs Example
```tsx
<Tabs defaultValue="tab1">
  <TabsList>
    <TabsTrigger value="tab1">Tab 1</TabsTrigger>
    <TabsTrigger value="tab2">Tab 2</TabsTrigger>
  </TabsList>
  <TabsContent value="tab1">Content 1</TabsContent>
  <TabsContent value="tab2">Content 2</TabsContent>
</Tabs>
```

---

## Overlays

| HTML Pattern | shadcn Component | Notes |
|--------------|------------------|-------|
| Modal/dialog | Dialog | Dialog + DialogTrigger + DialogContent |
| Drawer/slide-over | Sheet | Sheet + SheetTrigger + SheetContent |
| Popover | Popover | Popover + PopoverTrigger + PopoverContent |
| Context menu | ContextMenu | Right-click menu |
| Alert dialog | AlertDialog | Confirmation dialogs |
| Hover card | HoverCard | Rich preview on hover |

### Dialog Example
```tsx
<Dialog>
  <DialogTrigger asChild>
    <Button>Open</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Title</DialogTitle>
      <DialogDescription>Description</DialogDescription>
    </DialogHeader>
    {/* Content */}
    <DialogFooter>
      <Button>Save</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

---

## Layout

| HTML Pattern | shadcn Component | Notes |
|--------------|------------------|-------|
| Aspect ratio container | AspectRatio | Maintain aspect ratio |
| Scroll area | ScrollArea | Custom scrollbars |
| Resizable panels | ResizablePanelGroup | Resizable + ResizablePanel + ResizableHandle |
| Collapsible section | Collapsible | Collapsible + CollapsibleTrigger + CollapsibleContent |

---

## Stitch-Specific Patterns

Google Stitch often generates these patterns:

### Inline Styles → Tailwind Classes
| Stitch CSS | Tailwind Equivalent |
|------------|---------------------|
| `display: flex` | `flex` |
| `justify-content: center` | `justify-center` |
| `align-items: center` | `items-center` |
| `gap: 8px` | `gap-2` |
| `padding: 16px` | `p-4` |
| `margin: 8px` | `m-2` |
| `border-radius: 8px` | `rounded-lg` |
| `font-weight: 600` | `font-semibold` |
| `font-size: 14px` | `text-sm` |
| `color: #6b7280` | `text-gray-500` |

### Common Stitch Class Mappings
| Stitch Class | Likely shadcn Component |
|--------------|------------------------|
| `.card`, `.panel` | Card |
| `.btn`, `.button` | Button |
| `.input`, `.text-field` | Input |
| `.badge`, `.tag`, `.chip` | Badge |
| `.modal`, `.dialog` | Dialog |
| `.dropdown` | DropdownMenu or Select |
| `.tabs` | Tabs |
| `.nav`, `.sidebar` | Custom navigation |
| `.avatar` | Avatar |
| `.table` | Table |

---

## When shadcn Doesn't Have It

If no direct mapping exists:

1. **Check extended components** - shadcn has 100+ components including charts, navbars, etc.
2. **Use Radix UI** - shadcn is built on Radix; use primitives directly
3. **Build custom** - Follow shadcn patterns (CVA, forwardRef, cn())
4. **Compose existing** - Often multiple shadcn components can be combined

---

## Tailwind Patterns

### Group Hover

Stitch uses Tailwind's named group hover patterns. Preserve these in React:

```tsx
// Stitch HTML
<div class="group/item">
  <p class="text-gray-400 group-hover/item:text-white">Label</p>
  <button class="opacity-60 group-hover/item:opacity-100">Action</button>
</div>

// React component - preserve group patterns
<div className="group/item">
  <p className="text-muted-foreground group-hover/item:text-foreground">{label}</p>
  <Button className="opacity-60 group-hover/item:opacity-100">{action}</Button>
</div>
```

### Recursive/Tree Components

For nested structures like file trees:

```tsx
interface TreeNode {
  name: string
  type: "file" | "folder"
  children?: TreeNode[]
}

const TreeItem = ({ node, depth = 0 }: { node: TreeNode; depth?: number }) => (
  <div className="relative">
    <div className="flex items-center gap-1.5" style={{ paddingLeft: depth * 16 }}>
      {node.type === "folder" ? <ChevronRight /> : null}
      {node.type === "folder" ? <Folder /> : <File />}
      <span>{node.name}</span>
    </div>
    {node.children?.map((child) => (
      <TreeItem key={child.name} node={child} depth={depth + 1} />
    ))}
  </div>
)
```

### Focus-Within States

Stitch uses `focus-within:` for input containers:

```tsx
// Stitch: input with icon that highlights on focus
<div class="group focus-within:border-blue-500">
  <span class="text-gray-400 group-focus-within:text-white">🔍</span>
  <input class="bg-transparent" />
</div>

// React equivalent
<div className="group focus-within:border-primary">
  <Search className="text-muted-foreground group-focus-within:text-foreground" />
  <Input className="bg-transparent border-none" />
</div>
```

### Custom Scrollbar

Stitch includes custom scrollbar CSS. Add to `globals.css`:

```css
/* Custom scrollbar for dark theme */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: hsl(var(--border));
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: hsl(var(--primary));
}
```
