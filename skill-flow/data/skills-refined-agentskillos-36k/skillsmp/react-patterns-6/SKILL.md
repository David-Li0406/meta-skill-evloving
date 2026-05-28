---
name: react-patterns
description: React component patterns, hooks, state management, and performance optimization for the PMS frontend. Use for React development questions, component creation, and frontend architecture.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# React Patterns for PMS

## Component Architecture

### Atomic Design Structure
```
components/
├── atoms/          # Basic elements (Button, Input, Text)
├── molecules/      # Simple combinations (SearchBar, Card)
├── organisms/      # Complex sections (Header, TaskList)
├── templates/      # Page layouts
└── pages/          # Full pages
```

### Component Patterns

#### Container/Presenter Pattern
```tsx
// TaskListContainer.tsx (Container - logic)
export const TaskListContainer: FC = () => {
  const { data: tasks, isLoading } = useQuery(['tasks'], fetchTasks);
  const updateTask = useMutation(updateTaskApi);

  const handleStatusChange = (taskId: string, status: TaskStatus) => {
    updateTask.mutate({ taskId, status });
  };

  return (
    <TaskList
      tasks={tasks}
      isLoading={isLoading}
      onStatusChange={handleStatusChange}
    />
  );
};

// TaskList.tsx (Presenter - UI)
export const TaskList: FC<TaskListProps> = memo(({
  tasks,
  isLoading,
  onStatusChange
}) => {
  if (isLoading) return <TaskListSkeleton />;

  return (
    <ul className="task-list">
      {tasks.map(task => (
        <TaskItem
          key={task.id}
          task={task}
          onStatusChange={onStatusChange}
        />
      ))}
    </ul>
  );
});
```

#### Compound Component Pattern
```tsx
// For complex components with related parts
const Card = ({ children }) => (
  <div className="card">{children}</div>
);

Card.Header = ({ children }) => (
  <div className="card-header">{children}</div>
);

Card.Body = ({ children }) => (
  <div className="card-body">{children}</div>
);

Card.Footer = ({ children }) => (
  <div className="card-footer">{children}</div>
);

// Usage
<Card>
  <Card.Header>Title</Card.Header>
  <Card.Body>Content</Card.Body>
  <Card.Footer>Actions</Card.Footer>
</Card>
```

## Custom Hooks

### Data Fetching Hook
```tsx
export const useProject = (projectId: string) => {
  return useQuery(
    ['project', projectId],
    () => projectService.getById(projectId),
    {
      enabled: !!projectId,
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 30 * 60 * 1000, // 30 minutes
    }
  );
};
```

### Form Hook
```tsx
export const useForm = <T extends Record<string, any>>(
  initialValues: T,
  validate: (values: T) => Partial<Record<keyof T, string>>
) => {
  const [values, setValues] = useState(initialValues);
  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({});
  const [touched, setTouched] = useState<Partial<Record<keyof T, boolean>>>({});

  const handleChange = (name: keyof T) => (
    e: ChangeEvent<HTMLInputElement>
  ) => {
    setValues(prev => ({ ...prev, [name]: e.target.value }));
  };

  const handleBlur = (name: keyof T) => () => {
    setTouched(prev => ({ ...prev, [name]: true }));
    setErrors(validate(values));
  };

  const handleSubmit = (onSubmit: (values: T) => void) => (
    e: FormEvent
  ) => {
    e.preventDefault();
    const validationErrors = validate(values);
    setErrors(validationErrors);

    if (Object.keys(validationErrors).length === 0) {
      onSubmit(values);
    }
  };

  return { values, errors, touched, handleChange, handleBlur, handleSubmit };
};
```

## Performance Optimization

### Memoization
```tsx
// Memoize expensive calculations
const expensiveValue = useMemo(() => {
  return computeExpensiveValue(data);
}, [data]);

// Memoize callbacks
const handleClick = useCallback(() => {
  doSomething(id);
}, [id]);

// Memoize components
const MemoizedComponent = memo(Component, (prevProps, nextProps) => {
  return prevProps.id === nextProps.id;
});
```

### Code Splitting
```tsx
// Route-level splitting
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Projects = lazy(() => import('./pages/Projects'));

// Component-level splitting
const HeavyChart = lazy(() => import('./components/HeavyChart'));
```

### Virtual Lists
```tsx
import { FixedSizeList } from 'react-window';

const VirtualTaskList: FC<{ tasks: Task[] }> = ({ tasks }) => (
  <FixedSizeList
    height={600}
    width="100%"
    itemCount={tasks.length}
    itemSize={50}
  >
    {({ index, style }) => (
      <TaskRow task={tasks[index]} style={style} />
    )}
  </FixedSizeList>
);
```
