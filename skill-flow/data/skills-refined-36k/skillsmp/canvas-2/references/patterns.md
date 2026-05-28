# Common Patterns

Reusable UI patterns for Browser Canvas.

## Form with Validation

Complete form with field validation and submit handling.

```jsx
function App() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    message: "",
  });
  const [errors, setErrors] = useState({});
  const [submitted, setSubmitted] = useState(false);

  const validate = () => {
    const newErrors = {};
    if (!formData.name.trim()) {
      newErrors.name = "Name is required";
    }
    if (!formData.email.trim()) {
      newErrors.email = "Email is required";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = "Invalid email format";
    }
    if (!formData.message.trim()) {
      newErrors.message = "Message is required";
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = () => {
    if (validate()) {
      window.canvasEmit("submit", formData);
      setSubmitted(true);
    }
  };

  const updateField = (field, value) => {
    setFormData({ ...formData, [field]: value });
    if (errors[field]) {
      setErrors({ ...errors, [field]: null });
    }
  };

  if (submitted) {
    return (
      <Card className="w-96 mx-auto mt-8">
        <CardContent className="pt-6 text-center">
          <CheckCircle className="h-12 w-12 text-green-500 mx-auto mb-4" />
          <p className="text-lg font-medium">Thank you!</p>
          <p className="text-muted-foreground">Your message has been sent.</p>
          <Button
            className="mt-4"
            variant="outline"
            onClick={() => {
              setSubmitted(false);
              setFormData({ name: "", email: "", message: "" });
            }}
          >
            Send Another
          </Button>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="w-96 mx-auto mt-8">
      <CardHeader>
        <CardTitle>Contact Us</CardTitle>
        <CardDescription>Fill out the form below</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="name">Name</Label>
          <Input
            id="name"
            value={formData.name}
            onChange={e => updateField("name", e.target.value)}
            className={errors.name ? "border-red-500" : ""}
          />
          {errors.name && (
            <p className="text-sm text-red-500">{errors.name}</p>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="email">Email</Label>
          <Input
            id="email"
            type="email"
            value={formData.email}
            onChange={e => updateField("email", e.target.value)}
            className={errors.email ? "border-red-500" : ""}
          />
          {errors.email && (
            <p className="text-sm text-red-500">{errors.email}</p>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="message">Message</Label>
          <Textarea
            id="message"
            rows={4}
            value={formData.message}
            onChange={e => updateField("message", e.target.value)}
            className={errors.message ? "border-red-500" : ""}
          />
          {errors.message && (
            <p className="text-sm text-red-500">{errors.message}</p>
          )}
        </div>
      </CardContent>
      <CardFooter>
        <Button onClick={handleSubmit} className="w-full">
          Send Message
        </Button>
      </CardFooter>
    </Card>
  );
}
```

---

## Data Table with Filtering

Sortable, filterable data table.

```jsx
function App() {
  const [data] = useState([
    { id: 1, name: "Alice Johnson", email: "alice@example.com", role: "Admin", status: "Active" },
    { id: 2, name: "Bob Smith", email: "bob@example.com", role: "User", status: "Active" },
    { id: 3, name: "Carol Williams", email: "carol@example.com", role: "User", status: "Inactive" },
    { id: 4, name: "David Brown", email: "david@example.com", role: "Editor", status: "Active" },
    { id: 5, name: "Eve Davis", email: "eve@example.com", role: "User", status: "Pending" },
  ]);

  const [search, setSearch] = useState("");
  const [sortField, setSortField] = useState("name");
  const [sortDirection, setSortDirection] = useState("asc");
  const [statusFilter, setStatusFilter] = useState("all");

  const handleSort = (field) => {
    if (sortField === field) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortField(field);
      setSortDirection("asc");
    }
  };

  const filteredData = data
    .filter(row => {
      const matchesSearch =
        row.name.toLowerCase().includes(search.toLowerCase()) ||
        row.email.toLowerCase().includes(search.toLowerCase());
      const matchesStatus = statusFilter === "all" || row.status === statusFilter;
      return matchesSearch && matchesStatus;
    })
    .sort((a, b) => {
      const aVal = a[sortField];
      const bVal = b[sortField];
      const direction = sortDirection === "asc" ? 1 : -1;
      return aVal.localeCompare(bVal) * direction;
    });

  const SortIcon = ({ field }) => {
    if (sortField !== field) return <ChevronUp className="h-4 w-4 opacity-30" />;
    return sortDirection === "asc"
      ? <ChevronUp className="h-4 w-4" />
      : <ChevronDown className="h-4 w-4" />;
  };

  return (
    <Card className="w-full max-w-4xl mx-auto mt-8">
      <CardHeader>
        <CardTitle>Users</CardTitle>
        <div className="flex gap-4 mt-4">
          <div className="flex-1">
            <Input
              placeholder="Search by name or email..."
              value={search}
              onChange={e => setSearch(e.target.value)}
              className="max-w-sm"
            />
          </div>
          <Select value={statusFilter} onValueChange={setStatusFilter}>
            <SelectTrigger className="w-[150px]">
              <SelectValue placeholder="Status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Status</SelectItem>
              <SelectItem value="Active">Active</SelectItem>
              <SelectItem value="Inactive">Inactive</SelectItem>
              <SelectItem value="Pending">Pending</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead
                className="cursor-pointer"
                onClick={() => handleSort("name")}
              >
                <div className="flex items-center gap-1">
                  Name <SortIcon field="name" />
                </div>
              </TableHead>
              <TableHead
                className="cursor-pointer"
                onClick={() => handleSort("email")}
              >
                <div className="flex items-center gap-1">
                  Email <SortIcon field="email" />
                </div>
              </TableHead>
              <TableHead>Role</TableHead>
              <TableHead>Status</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredData.map(row => (
              <TableRow key={row.id}>
                <TableCell className="font-medium">{row.name}</TableCell>
                <TableCell>{row.email}</TableCell>
                <TableCell>{row.role}</TableCell>
                <TableCell>
                  <Badge variant={
                    row.status === "Active" ? "default" :
                    row.status === "Inactive" ? "secondary" : "outline"
                  }>
                    {row.status}
                  </Badge>
                </TableCell>
                <TableCell className="text-right">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => window.canvasEmit("edit", { id: row.id })}
                  >
                    <Edit className="h-4 w-4" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => window.canvasEmit("delete", { id: row.id })}
                  >
                    <Trash className="h-4 w-4" />
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        {filteredData.length === 0 && (
          <p className="text-center text-muted-foreground py-8">
            No results found
          </p>
        )}
      </CardContent>
    </Card>
  );
}
```

---

## Dashboard Layout

Multi-widget dashboard with stats and charts.

```jsx
function App() {
  const stats = [
    { title: "Total Revenue", value: "$45,231", change: "+20.1%", icon: DollarSign },
    { title: "Subscriptions", value: "2,350", change: "+180", icon: Users },
    { title: "Sales", value: "12,234", change: "+19%", icon: ShoppingCart },
    { title: "Active Now", value: "573", change: "+201", icon: Activity },
  ];

  const chartData = [
    { month: "Jan", revenue: 4000, users: 240 },
    { month: "Feb", revenue: 3000, users: 139 },
    { month: "Mar", revenue: 5000, users: 980 },
    { month: "Apr", revenue: 4780, users: 390 },
    { month: "May", revenue: 5890, users: 480 },
    { month: "Jun", revenue: 6390, users: 380 },
  ];

  const recentSales = [
    { name: "Olivia Martin", email: "olivia@email.com", amount: "$1,999.00" },
    { name: "Jackson Lee", email: "jackson@email.com", amount: "$39.00" },
    { name: "Isabella Nguyen", email: "isabella@email.com", amount: "$299.00" },
    { name: "William Kim", email: "will@email.com", amount: "$99.00" },
  ];

  return (
    <div className="p-6 space-y-6 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold">Dashboard</h1>

      {/* Stats Grid */}
      <div className="grid grid-cols-4 gap-4">
        {stats.map((stat, i) => (
          <Card key={i}>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                {stat.title}
              </CardTitle>
              <stat.icon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
              <p className="text-xs text-muted-foreground">
                <span className="text-green-500">{stat.change}</span> from last month
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-2 gap-4">
        <Card>
          <CardHeader>
            <CardTitle>Revenue Overview</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={250}>
              <AreaChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Area
                  type="monotone"
                  dataKey="revenue"
                  stroke="#8884d8"
                  fill="#8884d8"
                  fillOpacity={0.3}
                />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Recent Sales</CardTitle>
            <CardDescription>You made 265 sales this month.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentSales.map((sale, i) => (
                <div key={i} className="flex items-center">
                  <Avatar className="h-9 w-9">
                    <AvatarFallback>
                      {sale.name.split(" ").map(n => n[0]).join("")}
                    </AvatarFallback>
                  </Avatar>
                  <div className="ml-4 space-y-1">
                    <p className="text-sm font-medium">{sale.name}</p>
                    <p className="text-sm text-muted-foreground">{sale.email}</p>
                  </div>
                  <div className="ml-auto font-medium">{sale.amount}</div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
```

---

## Modal/Dialog Usage

Dialog with form inside.

```jsx
function App() {
  const [open, setOpen] = useState(false);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [users, setUsers] = useState([
    { id: 1, name: "Alice", email: "alice@example.com" },
    { id: 2, name: "Bob", email: "bob@example.com" },
  ]);

  const handleAdd = () => {
    if (name && email) {
      const newUser = { id: Date.now(), name, email };
      setUsers([...users, newUser]);
      window.canvasEmit("userAdded", newUser);
      setName("");
      setEmail("");
      setOpen(false);
    }
  };

  return (
    <Card className="w-full max-w-2xl mx-auto mt-8">
      <CardHeader className="flex flex-row items-center justify-between">
        <div>
          <CardTitle>Team Members</CardTitle>
          <CardDescription>Manage your team members</CardDescription>
        </div>
        <Dialog open={open} onOpenChange={setOpen}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="h-4 w-4 mr-2" />
              Add Member
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Add Team Member</DialogTitle>
              <DialogDescription>
                Enter the details for the new team member.
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4 py-4">
              <div className="space-y-2">
                <Label htmlFor="name">Name</Label>
                <Input
                  id="name"
                  value={name}
                  onChange={e => setName(e.target.value)}
                  placeholder="John Doe"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  value={email}
                  onChange={e => setEmail(e.target.value)}
                  placeholder="john@example.com"
                />
              </div>
            </div>
            <DialogFooter>
              <Button variant="outline" onClick={() => setOpen(false)}>
                Cancel
              </Button>
              <Button onClick={handleAdd}>Add Member</Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Email</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {users.map(user => (
              <TableRow key={user.id}>
                <TableCell className="font-medium">{user.name}</TableCell>
                <TableCell>{user.email}</TableCell>
                <TableCell className="text-right">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => {
                      setUsers(users.filter(u => u.id !== user.id));
                      window.canvasEmit("userRemoved", { id: user.id });
                    }}
                  >
                    <Trash className="h-4 w-4" />
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
}
```

---

## Multi-Step Wizard

Step-by-step form wizard.

```jsx
function App() {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    plan: "",
    cardNumber: "",
  });

  const updateField = (field, value) => {
    setFormData({ ...formData, [field]: value });
  };

  const steps = [
    { number: 1, title: "Account" },
    { number: 2, title: "Plan" },
    { number: 3, title: "Payment" },
    { number: 4, title: "Confirm" },
  ];

  const handleComplete = () => {
    window.canvasEmit("wizardComplete", formData);
  };

  return (
    <Card className="w-full max-w-lg mx-auto mt-8">
      <CardHeader>
        <CardTitle>Create Account</CardTitle>
        {/* Progress Steps */}
        <div className="flex justify-between mt-4">
          {steps.map((s, i) => (
            <div key={s.number} className="flex items-center">
              <div className={cn(
                "w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium",
                step > s.number ? "bg-green-500 text-white" :
                step === s.number ? "bg-primary text-primary-foreground" :
                "bg-muted text-muted-foreground"
              )}>
                {step > s.number ? <Check className="h-4 w-4" /> : s.number}
              </div>
              {i < steps.length - 1 && (
                <div className={cn(
                  "w-12 h-0.5 mx-2",
                  step > s.number ? "bg-green-500" : "bg-muted"
                )} />
              )}
            </div>
          ))}
        </div>
      </CardHeader>

      <CardContent className="min-h-[200px]">
        {step === 1 && (
          <div className="space-y-4">
            <div className="space-y-2">
              <Label>Name</Label>
              <Input
                value={formData.name}
                onChange={e => updateField("name", e.target.value)}
                placeholder="Your name"
              />
            </div>
            <div className="space-y-2">
              <Label>Email</Label>
              <Input
                type="email"
                value={formData.email}
                onChange={e => updateField("email", e.target.value)}
                placeholder="you@example.com"
              />
            </div>
          </div>
        )}

        {step === 2 && (
          <div className="space-y-4">
            <Label>Select Plan</Label>
            <RadioGroup
              value={formData.plan}
              onValueChange={v => updateField("plan", v)}
            >
              <div className="flex items-center space-x-2 p-4 border rounded-lg">
                <RadioGroupItem value="free" id="free" />
                <Label htmlFor="free" className="flex-1 cursor-pointer">
                  <div className="font-medium">Free</div>
                  <div className="text-sm text-muted-foreground">Basic features</div>
                </Label>
                <div className="font-medium">$0/mo</div>
              </div>
              <div className="flex items-center space-x-2 p-4 border rounded-lg">
                <RadioGroupItem value="pro" id="pro" />
                <Label htmlFor="pro" className="flex-1 cursor-pointer">
                  <div className="font-medium">Pro</div>
                  <div className="text-sm text-muted-foreground">All features</div>
                </Label>
                <div className="font-medium">$20/mo</div>
              </div>
              <div className="flex items-center space-x-2 p-4 border rounded-lg">
                <RadioGroupItem value="enterprise" id="enterprise" />
                <Label htmlFor="enterprise" className="flex-1 cursor-pointer">
                  <div className="font-medium">Enterprise</div>
                  <div className="text-sm text-muted-foreground">Custom solutions</div>
                </Label>
                <div className="font-medium">Custom</div>
              </div>
            </RadioGroup>
          </div>
        )}

        {step === 3 && (
          <div className="space-y-4">
            <div className="space-y-2">
              <Label>Card Number</Label>
              <Input
                value={formData.cardNumber}
                onChange={e => updateField("cardNumber", e.target.value)}
                placeholder="4242 4242 4242 4242"
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label>Expiry</Label>
                <Input placeholder="MM/YY" />
              </div>
              <div className="space-y-2">
                <Label>CVC</Label>
                <Input placeholder="123" />
              </div>
            </div>
          </div>
        )}

        {step === 4 && (
          <div className="space-y-4">
            <Alert>
              <CheckCircle className="h-4 w-4" />
              <AlertTitle>Ready to create your account</AlertTitle>
              <AlertDescription>
                Please review your information below.
              </AlertDescription>
            </Alert>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between py-2 border-b">
                <span className="text-muted-foreground">Name</span>
                <span className="font-medium">{formData.name}</span>
              </div>
              <div className="flex justify-between py-2 border-b">
                <span className="text-muted-foreground">Email</span>
                <span className="font-medium">{formData.email}</span>
              </div>
              <div className="flex justify-between py-2 border-b">
                <span className="text-muted-foreground">Plan</span>
                <span className="font-medium capitalize">{formData.plan}</span>
              </div>
            </div>
          </div>
        )}
      </CardContent>

      <CardFooter className="flex justify-between">
        <Button
          variant="outline"
          onClick={() => setStep(step - 1)}
          disabled={step === 1}
        >
          <ChevronLeft className="h-4 w-4 mr-2" />
          Back
        </Button>
        {step < 4 ? (
          <Button onClick={() => setStep(step + 1)}>
            Next
            <ChevronRight className="h-4 w-4 ml-2" />
          </Button>
        ) : (
          <Button onClick={handleComplete}>
            Create Account
          </Button>
        )}
      </CardFooter>
    </Card>
  );
}
```

---

## Loading States

Skeleton loading pattern.

```jsx
function App() {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);

  useEffect(() => {
    // Simulate data fetch
    setTimeout(() => {
      setData([
        { id: 1, name: "Item 1", description: "Description 1" },
        { id: 2, name: "Item 2", description: "Description 2" },
        { id: 3, name: "Item 3", description: "Description 3" },
      ]);
      setLoading(false);
    }, 2000);
  }, []);

  if (loading) {
    return (
      <Card className="w-96 mx-auto mt-8">
        <CardHeader>
          <Skeleton className="h-6 w-[150px]" />
          <Skeleton className="h-4 w-[250px]" />
        </CardHeader>
        <CardContent className="space-y-4">
          {[1, 2, 3].map(i => (
            <div key={i} className="flex items-center space-x-4">
              <Skeleton className="h-12 w-12 rounded-full" />
              <div className="space-y-2">
                <Skeleton className="h-4 w-[200px]" />
                <Skeleton className="h-4 w-[150px]" />
              </div>
            </div>
          ))}
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="w-96 mx-auto mt-8">
      <CardHeader>
        <CardTitle>Items</CardTitle>
        <CardDescription>Your items list</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {data.map(item => (
          <div key={item.id} className="flex items-center space-x-4">
            <Avatar>
              <AvatarFallback>{item.name[0]}</AvatarFallback>
            </Avatar>
            <div>
              <p className="font-medium">{item.name}</p>
              <p className="text-sm text-muted-foreground">{item.description}</p>
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
```

---

## Confirmation Dialog

Delete confirmation pattern.

```jsx
function App() {
  const [items, setItems] = useState([
    { id: 1, name: "Document A" },
    { id: 2, name: "Document B" },
    { id: 3, name: "Document C" },
  ]);
  const [deleteId, setDeleteId] = useState(null);

  const handleDelete = () => {
    setItems(items.filter(item => item.id !== deleteId));
    window.canvasEmit("deleted", { id: deleteId });
    setDeleteId(null);
  };

  const itemToDelete = items.find(i => i.id === deleteId);

  return (
    <Card className="w-96 mx-auto mt-8">
      <CardHeader>
        <CardTitle>Documents</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-2">
          {items.map(item => (
            <div
              key={item.id}
              className="flex items-center justify-between p-2 rounded hover:bg-muted"
            >
              <div className="flex items-center gap-2">
                <FileText className="h-4 w-4" />
                <span>{item.name}</span>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setDeleteId(item.id)}
              >
                <Trash className="h-4 w-4 text-red-500" />
              </Button>
            </div>
          ))}
        </div>
      </CardContent>

      <Dialog open={deleteId !== null} onOpenChange={() => setDeleteId(null)}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Delete Document</DialogTitle>
            <DialogDescription>
              Are you sure you want to delete "{itemToDelete?.name}"?
              This action cannot be undone.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" onClick={() => setDeleteId(null)}>
              Cancel
            </Button>
            <Button variant="destructive" onClick={handleDelete}>
              Delete
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </Card>
  );
}
```
