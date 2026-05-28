# Component Reference

Complete API reference for all pre-bundled shadcn/ui components.

## Button

Interactive button with multiple variants and sizes.

```jsx
<Button
  variant="default"       // "default" | "destructive" | "outline" | "secondary" | "ghost" | "link"
  size="default"          // "default" | "sm" | "lg" | "icon"
  disabled={false}
  onClick={() => {}}
>
  Click me
</Button>
```

### Variants

```jsx
<Button variant="default">Default</Button>      // Primary action
<Button variant="destructive">Delete</Button>   // Dangerous action
<Button variant="outline">Outline</Button>      // Secondary action
<Button variant="secondary">Secondary</Button>  // Less prominent
<Button variant="ghost">Ghost</Button>          // Minimal style
<Button variant="link">Link</Button>            // Looks like a link
```

### Sizes

```jsx
<Button size="default">Default</Button>
<Button size="sm">Small</Button>
<Button size="lg">Large</Button>
<Button size="icon"><Plus /></Button>  // Square icon button
```

### With Icon

```jsx
<Button>
  <Mail className="mr-2 h-4 w-4" />
  Send Email
</Button>
```

---

## Card

Container for grouped content.

```jsx
<Card className="w-96">
  <CardHeader>
    <CardTitle>Card Title</CardTitle>
    <CardDescription>Card description text</CardDescription>
  </CardHeader>
  <CardContent>
    <p>Main content goes here</p>
  </CardContent>
  <CardFooter className="flex justify-between">
    <Button variant="outline">Cancel</Button>
    <Button>Save</Button>
  </CardFooter>
</Card>
```

### Sub-components

| Component | Purpose |
|-----------|---------|
| `Card` | Outer container |
| `CardHeader` | Top section for title/description |
| `CardTitle` | Main heading |
| `CardDescription` | Subtitle or description |
| `CardContent` | Main content area |
| `CardFooter` | Bottom section for actions |

---

## Input

Text input field.

```jsx
<Input
  type="text"              // "text" | "email" | "password" | "number" | "tel" | "url"
  placeholder="Enter text"
  value={value}
  onChange={e => setValue(e.target.value)}
  disabled={false}
  className="w-full"
/>
```

### With Label

```jsx
<div className="space-y-2">
  <Label htmlFor="email">Email</Label>
  <Input id="email" type="email" placeholder="you@example.com" />
</div>
```

### With Error State

```jsx
<div className="space-y-2">
  <Label htmlFor="email">Email</Label>
  <Input id="email" className="border-red-500" />
  <p className="text-sm text-red-500">Please enter a valid email</p>
</div>
```

---

## Label

Label for form inputs.

```jsx
<Label htmlFor="name" className="text-sm font-medium">
  Name
</Label>
```

---

## Textarea

Multi-line text input.

```jsx
<Textarea
  placeholder="Enter your message..."
  value={value}
  onChange={e => setValue(e.target.value)}
  rows={4}
  className="resize-none"
/>
```

---

## Table

Data table with header, body, and rows.

```jsx
<Table>
  <TableHeader>
    <TableRow>
      <TableHead className="w-[100px]">ID</TableHead>
      <TableHead>Name</TableHead>
      <TableHead>Email</TableHead>
      <TableHead className="text-right">Amount</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    <TableRow>
      <TableCell className="font-medium">001</TableCell>
      <TableCell>Alice Johnson</TableCell>
      <TableCell>alice@example.com</TableCell>
      <TableCell className="text-right">$250.00</TableCell>
    </TableRow>
    <TableRow>
      <TableCell className="font-medium">002</TableCell>
      <TableCell>Bob Smith</TableCell>
      <TableCell>bob@example.com</TableCell>
      <TableCell className="text-right">$150.00</TableCell>
    </TableRow>
  </TableBody>
</Table>
```

### Sub-components

| Component | Purpose |
|-----------|---------|
| `Table` | Outer container |
| `TableHeader` | Header section |
| `TableBody` | Body section |
| `TableRow` | Table row |
| `TableHead` | Header cell |
| `TableCell` | Body cell |

---

## Badge

Small label for status or categories.

```jsx
<Badge variant="default">Default</Badge>
<Badge variant="secondary">Secondary</Badge>
<Badge variant="destructive">Error</Badge>
<Badge variant="outline">Outline</Badge>
```

### Examples

```jsx
<Badge>New</Badge>
<Badge variant="secondary">Draft</Badge>
<Badge variant="destructive">Failed</Badge>
<Badge variant="outline">Beta</Badge>
```

---

## Avatar

User avatar with image and fallback.

```jsx
<Avatar>
  <AvatarImage src="https://example.com/avatar.jpg" alt="User" />
  <AvatarFallback>JD</AvatarFallback>
</Avatar>
```

### Sizes (via className)

```jsx
<Avatar className="h-8 w-8">...</Avatar>   // Small
<Avatar className="h-10 w-10">...</Avatar> // Default
<Avatar className="h-16 w-16">...</Avatar> // Large
```

---

## Progress

Progress bar indicator.

```jsx
<Progress value={33} className="w-full" />
<Progress value={66} className="w-full" />
<Progress value={100} className="w-full" />
```

Props:
- `value` - Progress percentage (0-100)

---

## Alert

Alert message box.

```jsx
<Alert>
  <AlertCircle className="h-4 w-4" />
  <AlertTitle>Heads up!</AlertTitle>
  <AlertDescription>
    You can add components to your app using the CLI.
  </AlertDescription>
</Alert>
```

### Variants

```jsx
// Default
<Alert>
  <Info className="h-4 w-4" />
  <AlertTitle>Note</AlertTitle>
  <AlertDescription>This is an informational message.</AlertDescription>
</Alert>

// Destructive
<Alert variant="destructive">
  <AlertCircle className="h-4 w-4" />
  <AlertTitle>Error</AlertTitle>
  <AlertDescription>Something went wrong.</AlertDescription>
</Alert>
```

---

## Dialog

Modal dialog overlay.

```jsx
<Dialog>
  <DialogTrigger asChild>
    <Button>Open Dialog</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Dialog Title</DialogTitle>
      <DialogDescription>
        This is the dialog description.
      </DialogDescription>
    </DialogHeader>
    <div className="py-4">
      <p>Dialog content goes here.</p>
    </div>
    <DialogFooter>
      <Button variant="outline">Cancel</Button>
      <Button>Confirm</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

### Controlled Dialog

```jsx
function App() {
  const [open, setOpen] = useState(false);

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>Open</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Confirm Action</DialogTitle>
        </DialogHeader>
        <DialogFooter>
          <Button onClick={() => setOpen(false)}>Close</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
```

---

## Tabs

Tabbed content navigation.

```jsx
<Tabs defaultValue="account" className="w-full">
  <TabsList>
    <TabsTrigger value="account">Account</TabsTrigger>
    <TabsTrigger value="password">Password</TabsTrigger>
    <TabsTrigger value="settings">Settings</TabsTrigger>
  </TabsList>
  <TabsContent value="account">
    <p>Account settings content</p>
  </TabsContent>
  <TabsContent value="password">
    <p>Password settings content</p>
  </TabsContent>
  <TabsContent value="settings">
    <p>Other settings content</p>
  </TabsContent>
</Tabs>
```

### Controlled Tabs

```jsx
function App() {
  const [tab, setTab] = useState("account");

  return (
    <Tabs value={tab} onValueChange={setTab}>
      <TabsList>
        <TabsTrigger value="account">Account</TabsTrigger>
        <TabsTrigger value="password">Password</TabsTrigger>
      </TabsList>
      <TabsContent value="account">...</TabsContent>
      <TabsContent value="password">...</TabsContent>
    </Tabs>
  );
}
```

---

## Select

Dropdown select menu.

```jsx
<Select value={value} onValueChange={setValue}>
  <SelectTrigger className="w-[180px]">
    <SelectValue placeholder="Select option" />
  </SelectTrigger>
  <SelectContent>
    <SelectItem value="option1">Option 1</SelectItem>
    <SelectItem value="option2">Option 2</SelectItem>
    <SelectItem value="option3">Option 3</SelectItem>
  </SelectContent>
</Select>
```

### With Label

```jsx
<div className="space-y-2">
  <Label>Category</Label>
  <Select>
    <SelectTrigger>
      <SelectValue placeholder="Select category" />
    </SelectTrigger>
    <SelectContent>
      <SelectItem value="tech">Technology</SelectItem>
      <SelectItem value="design">Design</SelectItem>
      <SelectItem value="business">Business</SelectItem>
    </SelectContent>
  </Select>
</div>
```

---

## Checkbox

Checkbox input.

```jsx
<div className="flex items-center space-x-2">
  <Checkbox
    id="terms"
    checked={checked}
    onCheckedChange={setChecked}
  />
  <Label htmlFor="terms">Accept terms and conditions</Label>
</div>
```

---

## Switch

Toggle switch.

```jsx
<div className="flex items-center space-x-2">
  <Switch
    id="notifications"
    checked={enabled}
    onCheckedChange={setEnabled}
  />
  <Label htmlFor="notifications">Enable notifications</Label>
</div>
```

---

## Slider

Range slider input.

```jsx
<Slider
  value={[value]}
  onValueChange={([v]) => setValue(v)}
  max={100}
  step={1}
  className="w-full"
/>
```

### Range Slider

```jsx
<Slider
  value={[min, max]}
  onValueChange={setRange}
  max={100}
  step={1}
/>
```

---

## Tooltip

Hover tooltip.

```jsx
<TooltipProvider>
  <Tooltip>
    <TooltipTrigger asChild>
      <Button variant="outline">Hover me</Button>
    </TooltipTrigger>
    <TooltipContent>
      <p>Tooltip content</p>
    </TooltipContent>
  </Tooltip>
</TooltipProvider>
```

---

## Accordion

Collapsible content sections.

```jsx
<Accordion type="single" collapsible>
  <AccordionItem value="item-1">
    <AccordionTrigger>Section 1</AccordionTrigger>
    <AccordionContent>
      Content for section 1
    </AccordionContent>
  </AccordionItem>
  <AccordionItem value="item-2">
    <AccordionTrigger>Section 2</AccordionTrigger>
    <AccordionContent>
      Content for section 2
    </AccordionContent>
  </AccordionItem>
</Accordion>
```

### Multiple Open

```jsx
<Accordion type="multiple">
  ...
</Accordion>
```

---

## Skeleton

Loading placeholder.

```jsx
<div className="space-y-2">
  <Skeleton className="h-4 w-[250px]" />
  <Skeleton className="h-4 w-[200px]" />
  <Skeleton className="h-4 w-[150px]" />
</div>
```

### Card Skeleton

```jsx
<Card>
  <CardHeader>
    <Skeleton className="h-6 w-[150px]" />
    <Skeleton className="h-4 w-[250px]" />
  </CardHeader>
  <CardContent>
    <Skeleton className="h-32 w-full" />
  </CardContent>
</Card>
```

---

## RadioGroup

Radio button group.

```jsx
<RadioGroup value={value} onValueChange={setValue}>
  <div className="flex items-center space-x-2">
    <RadioGroupItem value="option1" id="option1" />
    <Label htmlFor="option1">Option 1</Label>
  </div>
  <div className="flex items-center space-x-2">
    <RadioGroupItem value="option2" id="option2" />
    <Label htmlFor="option2">Option 2</Label>
  </div>
  <div className="flex items-center space-x-2">
    <RadioGroupItem value="option3" id="option3" />
    <Label htmlFor="option3">Option 3</Label>
  </div>
</RadioGroup>
```

---

## Sheet

Slide-out panel.

```jsx
<Sheet>
  <SheetTrigger asChild>
    <Button variant="outline">Open Sheet</Button>
  </SheetTrigger>
  <SheetContent>
    <SheetHeader>
      <SheetTitle>Sheet Title</SheetTitle>
      <SheetDescription>
        Sheet description text.
      </SheetDescription>
    </SheetHeader>
    <div className="py-4">
      <p>Sheet content goes here.</p>
    </div>
  </SheetContent>
</Sheet>
```

### Side Options

```jsx
<SheetContent side="right">...</SheetContent>  // Default
<SheetContent side="left">...</SheetContent>
<SheetContent side="top">...</SheetContent>
<SheetContent side="bottom">...</SheetContent>
```

---

## Utility: cn()

Merge class names with Tailwind conflict resolution.

```jsx
// Combines classes, resolving Tailwind conflicts
cn("px-4 py-2", "px-6")  // Returns "py-2 px-6"

// Conditional classes
cn("base-class", isActive && "active-class")

// Object syntax
cn("base", {
  "text-red-500": hasError,
  "text-green-500": isValid
})
```
