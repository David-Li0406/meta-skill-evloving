# shadcn/ui Composition Patterns

Common UI patterns built with shadcn/ui components.

## Form Patterns

### Basic Form
```tsx
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

<form onSubmit={handleSubmit}>
  <div className="grid gap-4">
    <div className="grid gap-2">
      <Label htmlFor="email">Email</Label>
      <Input id="email" type="email" placeholder="m@example.com" />
    </div>
    <div className="grid gap-2">
      <Label htmlFor="password">Password</Label>
      <Input id="password" type="password" />
    </div>
    <Button type="submit">Submit</Button>
  </div>
</form>
```

### Validated Form
```tsx
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

const formSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string().min(8, "Password must be at least 8 characters"),
})

const form = useForm<z.infer<typeof formSchema>>({
  resolver: zodResolver(formSchema),
  defaultValues: { email: "", password: "" },
})

<Form {...form}>
  <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
    <FormField
      control={form.control}
      name="email"
      render={({ field }) => (
        <FormItem>
          <FormLabel>Email</FormLabel>
          <FormControl><Input {...field} type="email" /></FormControl>
          <FormMessage />
        </FormItem>
      )}
    />
    <FormField
      control={form.control}
      name="password"
      render={({ field }) => (
        <FormItem>
          <FormLabel>Password</FormLabel>
          <FormControl><Input {...field} type="password" /></FormControl>
          <FormMessage />
        </FormItem>
      )}
    />
    <Button type="submit">Submit</Button>
  </form>
</Form>
```

### Multi-Step Form
```tsx
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"

const [step, setStep] = useState(1)

<Card>
  <CardHeader>
    <CardTitle>Step {step} of 3</CardTitle>
  </CardHeader>
  <CardContent>
    {step === 1 && <Step1Fields />}
    {step === 2 && <Step2Fields />}
    {step === 3 && <Step3Fields />}
  </CardContent>
  <CardFooter className="flex justify-between">
    <Button variant="outline" onClick={() => setStep(step - 1)} disabled={step === 1}>
      Previous
    </Button>
    <Button onClick={() => setStep(step + 1)} disabled={step === 3}>
      {step === 3 ? "Submit" : "Next"}
    </Button>
  </CardFooter>
</Card>
```

### Form in Dialog
```tsx
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

<Dialog>
  <DialogTrigger asChild>
    <Button>Add Item</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Create New Item</DialogTitle>
    </DialogHeader>
    <form className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="name">Name</Label>
        <Input id="name" placeholder="Enter name" />
      </div>
      <div className="flex justify-end gap-2">
        <Button variant="outline" type="button">Cancel</Button>
        <Button type="submit">Create</Button>
      </div>
    </form>
  </DialogContent>
</Dialog>
```

## Data Display Patterns

### Data Table with Actions
```tsx
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Button } from "@/components/ui/button"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { MoreHorizontal } from "lucide-react"

<Table>
  <TableHeader>
    <TableRow>
      <TableHead>Name</TableHead>
      <TableHead>Status</TableHead>
      <TableHead className="text-right">Actions</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    {data.map((item) => (
      <TableRow key={item.id}>
        <TableCell>{item.name}</TableCell>
        <TableCell>
          <Badge variant={item.status === "active" ? "default" : "secondary"}>
            {item.status}
          </Badge>
        </TableCell>
        <TableCell className="text-right">
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="icon">
                <MoreHorizontal className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem>Edit</DropdownMenuItem>
              <DropdownMenuItem>Delete</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </TableCell>
      </TableRow>
    ))}
  </TableBody>
</Table>
```

### Card Grid
```tsx
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

<div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
  {items.map((item) => (
    <Card key={item.id}>
      <CardHeader>
        <CardTitle>{item.title}</CardTitle>
        <CardDescription>{item.description}</CardDescription>
      </CardHeader>
      <CardContent>
        <p>{item.content}</p>
      </CardContent>
      <CardFooter>
        <Button>View Details</Button>
      </CardFooter>
    </Card>
  ))}
</div>
```

### List with Empty State
```tsx
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

{items.length === 0 ? (
  <Card>
    <CardContent className="flex flex-col items-center justify-center py-16">
      <p className="text-muted-foreground mb-4">No items found</p>
      <Button>Add Your First Item</Button>
    </CardContent>
  </Card>
) : (
  <div className="space-y-2">
    {items.map((item) => (
      <Card key={item.id}>
        <CardContent className="flex items-center justify-between p-4">
          <span>{item.name}</span>
          <Button variant="ghost" size="sm">View</Button>
        </CardContent>
      </Card>
    ))}
  </div>
)}
```

## Navigation Patterns

### Sidebar Layout
```tsx
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"
import { Button } from "@/components/ui/button"
import { Menu } from "lucide-react"

<div className="flex h-screen">
  {/* Desktop Sidebar */}
  <aside className="hidden md:flex w-64 flex-col border-r bg-background">
    <nav className="flex-1 space-y-2 p-4">
      <Button variant="ghost" className="w-full justify-start">Dashboard</Button>
      <Button variant="ghost" className="w-full justify-start">Items</Button>
      <Button variant="ghost" className="w-full justify-start">Settings</Button>
    </nav>
  </aside>

  {/* Mobile Sidebar */}
  <Sheet>
    <SheetTrigger asChild className="md:hidden">
      <Button variant="outline" size="icon"><Menu /></Button>
    </SheetTrigger>
    <SheetContent side="left">
      <nav className="flex flex-col gap-2">
        <Button variant="ghost" className="justify-start">Dashboard</Button>
        <Button variant="ghost" className="justify-start">Items</Button>
        <Button variant="ghost" className="justify-start">Settings</Button>
      </nav>
    </SheetContent>
  </Sheet>

  {/* Main Content */}
  <main className="flex-1 overflow-y-auto p-6">
    {children}
  </main>
</div>
```

### Tabs Navigation
```tsx
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

<Tabs defaultValue="overview">
  <TabsList>
    <TabsTrigger value="overview">Overview</TabsTrigger>
    <TabsTrigger value="analytics">Analytics</TabsTrigger>
    <TabsTrigger value="settings">Settings</TabsTrigger>
  </TabsList>
  <TabsContent value="overview">
    <OverviewContent />
  </TabsContent>
  <TabsContent value="analytics">
    <AnalyticsContent />
  </TabsContent>
  <TabsContent value="settings">
    <SettingsContent />
  </TabsContent>
</Tabs>
```

## Dashboard Patterns

### Stats Grid
```tsx
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

<div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
  <Card>
    <CardHeader className="flex flex-row items-center justify-between pb-2">
      <CardTitle className="text-sm font-medium">Total Users</CardTitle>
    </CardHeader>
    <CardContent>
      <div className="text-2xl font-bold">1,234</div>
      <p className="text-xs text-muted-foreground">+20% from last month</p>
    </CardContent>
  </Card>
  {/* Repeat for other stats */}
</div>
```

### Dashboard with Sidebar and Stats
```tsx
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

<div className="flex h-screen">
  <aside className="w-64 border-r">
    <nav className="p-4 space-y-2">
      <Button variant="ghost" className="w-full justify-start">Dashboard</Button>
      <Button variant="ghost" className="w-full justify-start">Reports</Button>
    </nav>
  </aside>
  <main className="flex-1 overflow-y-auto">
    <div className="p-6 space-y-6">
      <h1 className="text-3xl font-bold">Dashboard</h1>
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader><CardTitle>Metric 1</CardTitle></CardHeader>
          <CardContent><div className="text-2xl font-bold">100</div></CardContent>
        </Card>
        {/* More stats cards */}
      </div>
    </div>
  </main>
</div>
```

## Feedback Patterns

### Toast Notifications
```tsx
import { useToast } from "@/components/ui/use-toast"
import { Button } from "@/components/ui/button"

const { toast } = useToast()

// Success
<Button onClick={() => toast({
  title: "Success!",
  description: "Your changes have been saved.",
})}>
  Save
</Button>

// Error
<Button onClick={() => toast({
  variant: "destructive",
  title: "Error",
  description: "Something went wrong. Please try again.",
})}>
  Delete
</Button>
```

### Confirmation Dialog
```tsx
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger } from "@/components/ui/alert-dialog"
import { Button } from "@/components/ui/button"

<AlertDialog>
  <AlertDialogTrigger asChild>
    <Button variant="destructive">Delete Item</Button>
  </AlertDialogTrigger>
  <AlertDialogContent>
    <AlertDialogHeader>
      <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
      <AlertDialogDescription>
        This action cannot be undone. This will permanently delete the item.
      </AlertDialogDescription>
    </AlertDialogHeader>
    <AlertDialogFooter>
      <AlertDialogCancel>Cancel</AlertDialogCancel>
      <AlertDialogAction onClick={handleDelete}>Delete</AlertDialogAction>
    </AlertDialogFooter>
  </AlertDialogContent>
</AlertDialog>
```

### Loading States
```tsx
import { Button } from "@/components/ui/button"
import { Skeleton } from "@/components/ui/skeleton"
import { Loader2 } from "lucide-react"

// Button loading
<Button disabled={isLoading}>
  {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
  Submit
</Button>

// Content loading
{isLoading ? (
  <div className="space-y-2">
    <Skeleton className="h-12 w-full" />
    <Skeleton className="h-12 w-full" />
    <Skeleton className="h-12 w-full" />
  </div>
) : (
  <div>{content}</div>
)}
```

## Search and Filter Patterns

### Search with Filters
```tsx
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Button } from "@/components/ui/button"
import { Search } from "lucide-react"

<div className="flex gap-2">
  <div className="relative flex-1">
    <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
    <Input placeholder="Search..." className="pl-9" />
  </div>
  <Select>
    <SelectTrigger className="w-40">
      <SelectValue placeholder="Status" />
    </SelectTrigger>
    <SelectContent>
      <SelectItem value="all">All</SelectItem>
      <SelectItem value="active">Active</SelectItem>
      <SelectItem value="inactive">Inactive</SelectItem>
    </SelectContent>
  </Select>
  <Button>Apply</Button>
</div>
```

### Command Palette
```tsx
import { Command, CommandDialog, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "@/components/ui/command"
import { useState } from "react"

const [open, setOpen] = useState(false)

<CommandDialog open={open} onOpenChange={setOpen}>
  <CommandInput placeholder="Type a command or search..." />
  <CommandList>
    <CommandEmpty>No results found.</CommandEmpty>
    <CommandGroup heading="Suggestions">
      <CommandItem onSelect={() => {}}>Dashboard</CommandItem>
      <CommandItem onSelect={() => {}}>Settings</CommandItem>
    </CommandGroup>
  </CommandList>
</CommandDialog>
```

## User Profile Patterns

### User Menu Dropdown
```tsx
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { Button } from "@/components/ui/button"

<DropdownMenu>
  <DropdownMenuTrigger asChild>
    <Button variant="ghost" className="relative h-10 w-10 rounded-full">
      <Avatar>
        <AvatarImage src="/avatar.jpg" alt="User" />
        <AvatarFallback>JD</AvatarFallback>
      </Avatar>
    </Button>
  </DropdownMenuTrigger>
  <DropdownMenuContent align="end">
    <DropdownMenuLabel>My Account</DropdownMenuLabel>
    <DropdownMenuSeparator />
    <DropdownMenuItem>Profile</DropdownMenuItem>
    <DropdownMenuItem>Settings</DropdownMenuItem>
    <DropdownMenuSeparator />
    <DropdownMenuItem>Log out</DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>
```

## Responsive Patterns

### Responsive Grid
```tsx
<div className="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
  {items.map((item) => (
    <Card key={item.id}>{/* card content */}</Card>
  ))}
</div>
```

### Mobile-First Navigation
```tsx
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"
import { Button } from "@/components/ui/button"
import { Menu } from "lucide-react"

{/* Mobile */}
<Sheet>
  <SheetTrigger asChild className="lg:hidden">
    <Button variant="outline" size="icon"><Menu /></Button>
  </SheetTrigger>
  <SheetContent side="left">
    <nav>{/* nav items */}</nav>
  </SheetContent>
</Sheet>

{/* Desktop */}
<nav className="hidden lg:flex gap-4">
  {/* nav items */}
</nav>
```
