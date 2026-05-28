# Empty States Wireframes

> Zero-data, error, and loading state patterns.

## About This Recipe

Empty states are often overlooked but critical for user experience. These wireframes explore patterns for when there's no data, errors occur, or content is loading.

```css live
@import '../../assets/elementary/tokens/sketch.css';
@import '../../assets/elementary/components.css';
```
---

## Empty State Gallery

```jsx live
function StateTab({ state, isActive, onClick }) {
  return (
    <button
      onClick={onClick}
      className={`tab ${isActive ? 'active' : ''}`}
    >
      {state.title}
    </button>
  );
}

function StateDisplay({ state }) {
  return (
    <article className="display">
      <div className="icon">{state.icon}</div>
      <h3 className="title">{state.title}</h3>
      <p className="message">{state.message}</p>
      <button className="wf-btn action">
        {state.action}
      </button>
    </article>
  );
}

const emptyStates = [
  {
    id: 'no-data',
    title: 'No Data Yet',
    icon: '📭',
    message: 'You haven\'t added any items yet.',
    action: 'Add Your First Item',
  },
  {
    id: 'error',
    title: 'Something Went Wrong',
    icon: '😵',
    message: 'We couldn\'t load your data. Please try again.',
    action: 'Retry',
  },
  {
    id: 'search',
    title: 'No Results Found',
    icon: '🔍',
    message: 'We couldn\'t find anything matching your search.',
    action: 'Clear Search',
  },
  {
    id: 'success',
    title: 'All Done!',
    icon: '🎉',
    message: 'You\'ve completed all your tasks.',
    action: 'View History',
  },
];

export default function EmptyStateGallery() {
  const [active, setActive] = React.useState('no-data');

  const state = emptyStates.find(s => s.id === active);

  return (
    <section className="wf-empty-state">
      <nav className="selector">
        {emptyStates.map((s) => (
          <StateTab
            key={s.id}
            state={s}
            isActive={active === s.id}
            onClick={() => setActive(s.id)}
          />
        ))}
      </nav>

      <StateDisplay state={state} />
    </section>
  );
}
```

## Loading States

```jsx live
function SkeletonCard() {
  return (
    <article className="wf-card">
      <div className="wf-skeleton line title" />
      <div className="wf-skeleton line label" />
    </article>
  );
}

function PersonCard({ name }) {
  return (
    <article className="wf-card">
      <h4 className="title">{name}</h4>
      <p className="label">Team Member</p>
    </article>
  );
}

export default function LoadingStates() {
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    const timer = setInterval(() => setLoading(l => !l), 3000);
    return () => clearInterval(timer);
  }, []);

  const people = ['Alice', 'Bob', 'Carol'];

  return (
    <section>
      <p className="description">Auto-toggles every 3 seconds</p>

      <ul className="wf-list">
        {loading
          ? people.map((_, i) => <li key={i}><SkeletonCard /></li>)
          : people.map((name) => <li key={name}><PersonCard name={name} /></li>)
        }
      </ul>
    </section>
  );
}
```

---
*Created with [Reactive MD](https://marketplace.visualstudio.com/items?itemName=million-views.reactive-md)*
