# Charts Reference

Complete reference for Recharts components available in Browser Canvas.

## LineChart

Line chart for showing trends over time.

```jsx
function App() {
  const data = [
    { month: "Jan", sales: 4000, profit: 2400 },
    { month: "Feb", sales: 3000, profit: 1398 },
    { month: "Mar", sales: 2000, profit: 9800 },
    { month: "Apr", sales: 2780, profit: 3908 },
    { month: "May", sales: 1890, profit: 4800 },
    { month: "Jun", sales: 2390, profit: 3800 },
  ];

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="sales" stroke="#8884d8" />
        <Line type="monotone" dataKey="profit" stroke="#82ca9d" />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

### Line Props

| Prop | Type | Description |
|------|------|-------------|
| `type` | string | Line interpolation: `"monotone"`, `"linear"`, `"step"` |
| `dataKey` | string | Key in data for Y values |
| `stroke` | string | Line color |
| `strokeWidth` | number | Line thickness |
| `dot` | boolean | Show data points |
| `activeDot` | object | Hover point style `{ r: 8 }` |

---

## BarChart

Bar chart for comparing categories.

```jsx
function App() {
  const data = [
    { name: "Page A", visits: 4000, unique: 2400 },
    { name: "Page B", visits: 3000, unique: 1398 },
    { name: "Page C", visits: 2000, unique: 9800 },
    { name: "Page D", visits: 2780, unique: 3908 },
  ];

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="visits" fill="#8884d8" />
        <Bar dataKey="unique" fill="#82ca9d" />
      </BarChart>
    </ResponsiveContainer>
  );
}
```

### Stacked Bar Chart

```jsx
<BarChart data={data}>
  <CartesianGrid strokeDasharray="3 3" />
  <XAxis dataKey="name" />
  <YAxis />
  <Tooltip />
  <Legend />
  <Bar dataKey="sales" stackId="a" fill="#8884d8" />
  <Bar dataKey="returns" stackId="a" fill="#82ca9d" />
</BarChart>
```

### Bar Props

| Prop | Type | Description |
|------|------|-------------|
| `dataKey` | string | Key in data for values |
| `fill` | string | Bar color |
| `stackId` | string | Stack bars with same ID |
| `radius` | array | Corner radius `[topLeft, topRight, bottomRight, bottomLeft]` |
| `barSize` | number | Bar width in pixels |

---

## PieChart

Pie chart for showing proportions.

```jsx
function App() {
  const data = [
    { name: "Group A", value: 400 },
    { name: "Group B", value: 300 },
    { name: "Group C", value: 300 },
    { name: "Group D", value: 200 },
  ];

  const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042"];

  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          outerRadius={100}
          fill="#8884d8"
          dataKey="value"
          label
        >
          {data.map((entry, index) => (
            <Cell key={index} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
}
```

### Donut Chart

```jsx
<Pie
  data={data}
  cx="50%"
  cy="50%"
  innerRadius={60}
  outerRadius={100}
  dataKey="value"
>
  {data.map((entry, index) => (
    <Cell key={index} fill={COLORS[index % COLORS.length]} />
  ))}
</Pie>
```

### Pie Props

| Prop | Type | Description |
|------|------|-------------|
| `data` | array | Data array |
| `dataKey` | string | Key for values |
| `cx`, `cy` | string/number | Center position |
| `innerRadius` | number | For donut charts |
| `outerRadius` | number | Pie size |
| `label` | boolean/function | Show labels |
| `labelLine` | boolean | Show label lines |

---

## AreaChart

Area chart for showing volume over time.

```jsx
function App() {
  const data = [
    { month: "Jan", value: 4000 },
    { month: "Feb", value: 3000 },
    { month: "Mar", value: 2000 },
    { month: "Apr", value: 2780 },
    { month: "May", value: 1890 },
    { month: "Jun", value: 2390 },
  ];

  return (
    <ResponsiveContainer width="100%" height={300}>
      <AreaChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />
        <Area
          type="monotone"
          dataKey="value"
          stroke="#8884d8"
          fill="#8884d8"
          fillOpacity={0.3}
        />
      </AreaChart>
    </ResponsiveContainer>
  );
}
```

### Stacked Area Chart

```jsx
<AreaChart data={data}>
  <CartesianGrid strokeDasharray="3 3" />
  <XAxis dataKey="month" />
  <YAxis />
  <Tooltip />
  <Area
    type="monotone"
    dataKey="sales"
    stackId="1"
    stroke="#8884d8"
    fill="#8884d8"
  />
  <Area
    type="monotone"
    dataKey="profit"
    stackId="1"
    stroke="#82ca9d"
    fill="#82ca9d"
  />
</AreaChart>
```

### Area Props

| Prop | Type | Description |
|------|------|-------------|
| `type` | string | Interpolation type |
| `dataKey` | string | Key for values |
| `stroke` | string | Line color |
| `fill` | string | Fill color |
| `fillOpacity` | number | Fill transparency (0-1) |
| `stackId` | string | Stack areas with same ID |

---

## Common Components

### ResponsiveContainer

Wrapper for responsive charts. Always use this as the outermost component.

```jsx
<ResponsiveContainer width="100%" height={300}>
  <LineChart data={data}>
    ...
  </LineChart>
</ResponsiveContainer>
```

| Prop | Type | Description |
|------|------|-------------|
| `width` | string/number | Container width (`"100%"` recommended) |
| `height` | number | Container height in pixels |
| `aspect` | number | Width/height ratio (alternative to fixed height) |

### XAxis

Horizontal axis.

```jsx
<XAxis
  dataKey="name"
  tick={{ fontSize: 12 }}
  tickLine={false}
  axisLine={false}
  interval={0}
/>
```

| Prop | Type | Description |
|------|------|-------------|
| `dataKey` | string | Key for labels |
| `tick` | object/boolean | Tick style or false to hide |
| `tickLine` | boolean | Show tick lines |
| `axisLine` | boolean | Show axis line |
| `interval` | number | Label interval (0 = show all) |
| `angle` | number | Rotate labels |
| `tickFormatter` | function | Format tick labels |

### YAxis

Vertical axis.

```jsx
<YAxis
  tickFormatter={(value) => `$${value}`}
  width={80}
/>
```

| Prop | Type | Description |
|------|------|-------------|
| `tickFormatter` | function | Format tick values |
| `width` | number | Axis width |
| `domain` | array | Value range `[min, max]` or `['auto', 'auto']` |
| `tickCount` | number | Number of ticks |

### CartesianGrid

Background grid lines.

```jsx
<CartesianGrid
  strokeDasharray="3 3"
  vertical={false}
/>
```

| Prop | Type | Description |
|------|------|-------------|
| `strokeDasharray` | string | Dash pattern |
| `horizontal` | boolean | Show horizontal lines |
| `vertical` | boolean | Show vertical lines |

### Tooltip

Hover tooltip.

```jsx
<Tooltip
  formatter={(value) => [`$${value}`, "Revenue"]}
  labelFormatter={(label) => `Month: ${label}`}
/>
```

| Prop | Type | Description |
|------|------|-------------|
| `formatter` | function | Format values `(value, name) => [formattedValue, formattedName]` |
| `labelFormatter` | function | Format label |
| `cursor` | object/boolean | Cursor style |
| `contentStyle` | object | Tooltip container style |

### Legend

Chart legend.

```jsx
<Legend
  verticalAlign="bottom"
  height={36}
/>
```

| Prop | Type | Description |
|------|------|-------------|
| `verticalAlign` | string | `"top"`, `"middle"`, `"bottom"` |
| `align` | string | `"left"`, `"center"`, `"right"` |
| `layout` | string | `"horizontal"`, `"vertical"` |
| `iconType` | string | Icon shape |

### Cell

Individual styling for pie/bar segments.

```jsx
const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042"];

<Pie data={data} dataKey="value">
  {data.map((entry, index) => (
    <Cell key={index} fill={COLORS[index % COLORS.length]} />
  ))}
</Pie>
```

---

## Complete Dashboard Example

```jsx
function App() {
  const lineData = [
    { month: "Jan", revenue: 4000, expenses: 2400 },
    { month: "Feb", revenue: 3000, expenses: 1398 },
    { month: "Mar", revenue: 5000, expenses: 3800 },
    { month: "Apr", revenue: 4780, expenses: 3908 },
    { month: "May", revenue: 5890, expenses: 4800 },
    { month: "Jun", revenue: 6390, expenses: 3800 },
  ];

  const pieData = [
    { name: "Product A", value: 400 },
    { name: "Product B", value: 300 },
    { name: "Product C", value: 200 },
    { name: "Product D", value: 100 },
  ];

  const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042"];

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">Sales Dashboard</h1>

      <div className="grid grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Revenue vs Expenses</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={lineData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="revenue" stroke="#8884d8" />
                <Line type="monotone" dataKey="expenses" stroke="#82ca9d" />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Product Distribution</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  dataKey="value"
                  label
                >
                  {pieData.map((entry, index) => (
                    <Cell key={index} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
```

---

## Color Palettes

### Default Palette

```javascript
const COLORS = [
  "#8884d8",  // Purple
  "#82ca9d",  // Green
  "#ffc658",  // Yellow
  "#ff7300",  // Orange
  "#00C49F",  // Teal
  "#FFBB28",  // Gold
  "#FF8042",  // Coral
  "#0088FE",  // Blue
];
```

### Accessible Palette

```javascript
const ACCESSIBLE_COLORS = [
  "#2563eb",  // Blue
  "#dc2626",  // Red
  "#16a34a",  // Green
  "#ca8a04",  // Yellow
  "#9333ea",  // Purple
  "#ea580c",  // Orange
];
```
