# Dashboard Wireframes

> Interactive prototypes for data-heavy layouts.

## About This Recipe

Dashboards are complex, data-heavy interfaces. Use these wireframes to explore layouts, chart placements, and information hierarchy.

```css live
@import '../../assets/elementary/tokens/sketch.css';
@import '../../assets/elementary/components.css';
```

---

## Dashboard Layout

```jsx live
function NavItem({ item, isActive, onClick }) {
  return (
    <button
      onClick={onClick}
      className={`item ${isActive ? 'active' : ''}`}
    >
      <span>{item.icon}</span>
      <span>{item.label}</span>
    </button>
  );
}

function MetricCard({ label, value }) {
  return (
    <article className="wf-card">
      <div className="label">{label}</div>
      <div className="value">{value}</div>
    </article>
  );
}

export default function DashboardLayout() {
  const [activeNav, setActiveNav] = React.useState('overview');

  const navItems = [
    { id: 'overview', icon: '📊', label: 'Overview' },
    { id: 'analytics', icon: '📈', label: 'Analytics' },
    { id: 'reports', icon: '📋', label: 'Reports' },
    { id: 'settings', icon: '⚙️', label: 'Settings' },
  ];

  const metrics = [
    { label: 'Metric 1', value: Math.floor(Math.random() * 1000) },
    { label: 'Metric 2', value: Math.floor(Math.random() * 1000) },
    { label: 'Metric 3', value: Math.floor(Math.random() * 1000) },
  ];

  return (
    <div className="wf-dashboard">
      <aside className="sidebar">
        <h2 className="title">Dashboard</h2>
        <nav className="nav">
          {navItems.map((item) => (
            <NavItem
              key={item.id}
              item={item}
              isActive={activeNav === item.id}
              onClick={() => setActiveNav(item.id)}
            />
          ))}
        </nav>
      </aside>

      <main className="main">
        <h1 className="heading">{activeNav}</h1>
        <div className="wf-grid metrics">
          {metrics.map((metric, i) => (
            <MetricCard key={i} label={metric.label} value={metric.value} />
          ))}
        </div>
      </main>
    </div>
  );
}
```

## Stat Cards

```jsx live
function StatCard({ stat }) {
  return (
    <article className="wf-card">
      <div className="label">{stat.label}</div>
      <div className="value">{stat.value}</div>
      <div className={`change ${stat.up ? 'positive' : ''}`}>
        {stat.change} vs last month
      </div>
    </article>
  );
}

const stats = [
  { label: 'Total Revenue', value: '$45,231', change: '+12.5%', up: true },
  { label: 'Active Users', value: '2,350', change: '+4.2%', up: true },
  { label: 'Bounce Rate', value: '32%', change: '-2.1%', up: false },
  { label: 'Conversion', value: '3.2%', change: '+0.5%', up: true },
];

export default function StatCards() {
  return (
    <section className="wf-grid stats">
      {stats.map((stat) => (
        <StatCard key={stat.label} stat={stat} />
      ))}
    </section>
  );
}
```

---
*Created with [Reactive MD](https://marketplace.visualstudio.com/items?itemName=million-views.reactive-md)*
