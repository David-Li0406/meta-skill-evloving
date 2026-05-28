# shadcn/ui Component Catalog

Quick reference for all shadcn/ui components with use cases and installation.

## Installation Pattern

All components follow this pattern:
```bash
npx shadcn@latest add <component-name>
```

## Core Components

### Button
**Use for**: Primary actions, form submissions, navigation triggers
**Install**: `npx shadcn@latest add button`
**Variants**: default, destructive, outline, secondary, ghost, link
**Sizes**: default, sm, lg, icon

```tsx
<Button variant="default">Click me</Button>
<Button variant="outline" size="sm">Small</Button>
```

### Input
**Use for**: Text fields, search boxes, form inputs
**Install**: `npx shadcn@latest add input`
**Props**: type, placeholder, disabled, className

```tsx
<Input type="email" placeholder="Email" />
```

### Label
**Use for**: Form field labels (accessibility)
**Install**: `npx shadcn@latest add label`

```tsx
<Label htmlFor="email">Email</Label>
<Input id="email" />
```

### Textarea
**Use for**: Multi-line text input, comments, descriptions
**Install**: `npx shadcn@latest add textarea`

```tsx
<Textarea placeholder="Enter description..." />
```

### Checkbox
**Use for**: Boolean selections, multi-select lists
**Install**: `npx shadcn@latest add checkbox`

```tsx
<Checkbox id="terms" />
<Label htmlFor="terms">Accept terms</Label>
```

### Radio Group
**Use for**: Single selection from multiple options
**Install**: `npx shadcn@latest add radio-group`

```tsx
<RadioGroup defaultValue="option1">
  <RadioGroupItem value="option1" id="opt1" />
  <Label htmlFor="opt1">Option 1</Label>
</RadioGroup>
```

### Select
**Use for**: Dropdown selections
**Install**: `npx shadcn@latest add select`

```tsx
<Select>
  <SelectTrigger><SelectValue placeholder="Select..." /></SelectTrigger>
  <SelectContent>
    <SelectItem value="1">Option 1</SelectItem>
  </SelectContent>
</Select>
```

### Switch
**Use for**: Toggle settings, enable/disable features
**Install**: `npx shadcn@latest add switch`

```tsx
<Switch />
```

## Layout Components

### Card
**Use for**: Content containers, sections, panels
**Install**: `npx shadcn@latest add card`

```tsx
<Card>
  <CardHeader><CardTitle>Title</CardTitle></CardHeader>
  <CardContent>Content here</CardContent>
  <CardFooter>Footer actions</CardFooter>
</Card>
```

### Separator
**Use for**: Visual dividers between sections
**Install**: `npx shadcn@latest add separator`

```tsx
<Separator />
<Separator orientation="vertical" />
```

### Tabs
**Use for**: Organizing content into switchable views
**Install**: `npx shadcn@latest add tabs`

```tsx
<Tabs defaultValue="tab1">
  <TabsList>
    <TabsTrigger value="tab1">Tab 1</TabsTrigger>
  </TabsList>
  <TabsContent value="tab1">Content</TabsContent>
</Tabs>
```

### Accordion
**Use for**: Collapsible content sections, FAQs
**Install**: `npx shadcn@latest add accordion`

```tsx
<Accordion type="single" collapsible>
  <AccordionItem value="item-1">
    <AccordionTrigger>Title</AccordionTrigger>
    <AccordionContent>Content</AccordionContent>
  </AccordionItem>
</Accordion>
```

## Navigation Components

### Navigation Menu
**Use for**: Site navigation, menu bars
**Install**: `npx shadcn@latest add navigation-menu`

### Breadcrumb
**Use for**: Page hierarchy navigation
**Install**: `npx shadcn@latest add breadcrumb`

### Pagination
**Use for**: Multi-page data navigation
**Install**: `npx shadcn@latest add pagination`

## Overlay Components

### Dialog
**Use for**: Modals, confirmations, forms in overlay
**Install**: `npx shadcn@latest add dialog`

```tsx
<Dialog>
  <DialogTrigger asChild><Button>Open</Button></DialogTrigger>
  <DialogContent>
    <DialogHeader><DialogTitle>Title</DialogTitle></DialogHeader>
    <DialogDescription>Description</DialogDescription>
    <DialogFooter><Button>Save</Button></DialogFooter>
  </DialogContent>
</Dialog>
```

### Sheet
**Use for**: Side panels, drawers, sliding menus
**Install**: `npx shadcn@latest add sheet`
**Sides**: top, right, bottom, left

```tsx
<Sheet>
  <SheetTrigger>Open</SheetTrigger>
  <SheetContent side="right">
    <SheetHeader><SheetTitle>Title</SheetTitle></SheetHeader>
  </SheetContent>
</Sheet>
```

### Popover
**Use for**: Contextual information, tooltips with interaction
**Install**: `npx shadcn@latest add popover`

```tsx
<Popover>
  <PopoverTrigger>Trigger</PopoverTrigger>
  <PopoverContent>Content</PopoverContent>
</Popover>
```

### Tooltip
**Use for**: Hover information, icon explanations
**Install**: `npx shadcn@latest add tooltip`

```tsx
<TooltipProvider>
  <Tooltip>
    <TooltipTrigger>Hover me</TooltipTrigger>
    <TooltipContent>Info</TooltipContent>
  </Tooltip>
</TooltipProvider>
```

### Alert Dialog
**Use for**: Confirmations, destructive actions, important decisions
**Install**: `npx shadcn@latest add alert-dialog`

```tsx
<AlertDialog>
  <AlertDialogTrigger>Delete</AlertDialogTrigger>
  <AlertDialogContent>
    <AlertDialogHeader>
      <AlertDialogTitle>Are you sure?</AlertDialogTitle>
      <AlertDialogDescription>This action cannot be undone.</AlertDialogDescription>
    </AlertDialogHeader>
    <AlertDialogFooter>
      <AlertDialogCancel>Cancel</AlertDialogCancel>
      <AlertDialogAction>Continue</AlertDialogAction>
    </AlertDialogFooter>
  </AlertDialogContent>
</AlertDialog>
```

### Dropdown Menu
**Use for**: Action menus, context menus, user menus
**Install**: `npx shadcn@latest add dropdown-menu`

```tsx
<DropdownMenu>
  <DropdownMenuTrigger>Menu</DropdownMenuTrigger>
  <DropdownMenuContent>
    <DropdownMenuItem>Item 1</DropdownMenuItem>
    <DropdownMenuSeparator />
    <DropdownMenuItem>Item 2</DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>
```

### Context Menu
**Use for**: Right-click menus
**Install**: `npx shadcn@latest add context-menu`

## Feedback Components

### Alert
**Use for**: Static notifications, status messages
**Install**: `npx shadcn@latest add alert`
**Variants**: default, destructive

```tsx
<Alert>
  <AlertTitle>Heads up!</AlertTitle>
  <AlertDescription>Message here</AlertDescription>
</Alert>
```

### Toast
**Use for**: Temporary notifications, success/error messages
**Install**: `npx shadcn@latest add toast`

```tsx
import { useToast } from "@/components/ui/use-toast"

const { toast } = useToast()
toast({ title: "Success!", description: "Action completed" })
```

### Badge
**Use for**: Status indicators, tags, counts
**Install**: `npx shadcn@latest add badge`
**Variants**: default, secondary, destructive, outline

```tsx
<Badge>New</Badge>
<Badge variant="destructive">Error</Badge>
```

### Progress
**Use for**: Loading states, upload progress
**Install**: `npx shadcn@latest add progress`

```tsx
<Progress value={60} />
```

### Skeleton
**Use for**: Loading placeholders
**Install**: `npx shadcn@latest add skeleton`

```tsx
<Skeleton className="h-12 w-12 rounded-full" />
```

### Spinner (custom)
**Use for**: Inline loading indicators
**Note**: Create using Lucide icons (Loader2) with animation

```tsx
import { Loader2 } from "lucide-react"
<Loader2 className="h-4 w-4 animate-spin" />
```

## Data Display Components

### Table
**Use for**: Tabular data, data grids
**Install**: `npx shadcn@latest add table`

```tsx
<Table>
  <TableHeader>
    <TableRow>
      <TableHead>Column</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    <TableRow>
      <TableCell>Data</TableCell>
    </TableRow>
  </TableBody>
</Table>
```

### Avatar
**Use for**: User profile images, image placeholders
**Install**: `npx shadcn@latest add avatar`

```tsx
<Avatar>
  <AvatarImage src="/avatar.jpg" />
  <AvatarFallback>AB</AvatarFallback>
</Avatar>
```

### Calendar
**Use for**: Date pickers, scheduling
**Install**: `npx shadcn@latest add calendar`

### Data Table (complex)
**Use for**: Advanced tables with sorting, filtering, pagination
**Install**: Follow shadcn docs for tanstack/react-table integration

## Form Components

### Form
**Use for**: Complete form handling with validation
**Install**: `npx shadcn@latest add form`
**Note**: Integrates with react-hook-form and zod

```tsx
<Form {...form}>
  <form onSubmit={form.handleSubmit(onSubmit)}>
    <FormField
      control={form.control}
      name="username"
      render={({ field }) => (
        <FormItem>
          <FormLabel>Username</FormLabel>
          <FormControl><Input {...field} /></FormControl>
          <FormDescription>Your public username</FormDescription>
          <FormMessage />
        </FormItem>
      )}
    />
  </form>
</Form>
```

### Combobox
**Use for**: Searchable select, autocomplete
**Install**: Follow shadcn docs (combines Popover + Command)

### Command
**Use for**: Command palettes, search interfaces
**Install**: `npx shadcn@latest add command`

### Slider
**Use for**: Numeric ranges, volume controls
**Install**: `npx shadcn@latest add slider`

```tsx
<Slider defaultValue={[50]} max={100} step={1} />
```

## Utility Components

### Aspect Ratio
**Use for**: Responsive image/video containers
**Install**: `npx shadcn@latest add aspect-ratio`

```tsx
<AspectRatio ratio={16 / 9}>
  <img src="/image.jpg" alt="Image" />
</AspectRatio>
```

### Collapsible
**Use for**: Expandable content sections
**Install**: `npx shadcn@latest add collapsible`

### Hover Card
**Use for**: Rich hover previews
**Install**: `npx shadcn@latest add hover-card`

### Menubar
**Use for**: Application menu bars
**Install**: `npx shadcn@latest add menubar`

### Resizable
**Use for**: Split panes, resizable panels
**Install**: `npx shadcn@latest add resizable`

### Scroll Area
**Use for**: Custom scrollbars, contained scrolling
**Install**: `npx shadcn@latest add scroll-area`

### Sonner
**Use for**: Modern toast notifications (alternative to toast)
**Install**: `npx shadcn@latest add sonner`

## Component Selection Guide

### Forms & Input
- Simple form → Input + Label + Button
- Complex form → Form + FormField (with validation)
- Dropdown → Select
- Searchable dropdown → Combobox
- Toggle setting → Switch
- Multiple choices → Checkbox
- Single choice → Radio Group

### Overlays & Modals
- General modal → Dialog
- Confirmation → Alert Dialog
- Side panel → Sheet
- Hover info → Tooltip
- Click info → Popover
- Action menu → Dropdown Menu

### Feedback & Status
- Persistent message → Alert
- Temporary message → Toast/Sonner
- Loading → Progress, Skeleton, or Spinner
- Status tag → Badge

### Layout & Organization
- Content block → Card
- Tabs → Tabs
- Collapsible sections → Accordion
- Divider → Separator

### Data Display
- Simple table → Table
- Advanced table → Data Table
- User image → Avatar
- Date selection → Calendar
