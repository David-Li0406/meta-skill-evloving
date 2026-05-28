// TypeScript Code Review: Before/After Examples
// This file demonstrates common refactoring patterns for TypeScript/React code review.

import { useState, useEffect, useMemo, useCallback, memo } from 'react';

// =============================================================================
// Example 1: Type Safety
// =============================================================================

// BEFORE: Using 'any' type
interface UserBefore {
  data: any; // Loses type information
}

function processDataBefore(input: any): any {
  return input.value; // No type checking
}

// AFTER: Proper typing
interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user' | 'guest';
}

interface ApiResponse<T> {
  data: T;
  status: number;
  message?: string;
}

function processData<T>(input: ApiResponse<T>): T {
  return input.data;
}

// =============================================================================
// Example 2: Component Structure
// =============================================================================

// BEFORE: Monolithic component
function UserListBefore({ users }: { users: any[] }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [sortOrder, setSortOrder] = useState('asc');
  const [filter, setFilter] = useState('all');

  const filteredUsers = users
    .filter((u) => u.name.includes(searchTerm))
    .filter((u) => filter === 'all' || u.role === filter)
    .sort((a, b) => (sortOrder === 'asc' ? a.name.localeCompare(b.name) : b.name.localeCompare(a.name)));

  return (
    <div>
      <input value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} />
      <select value={sortOrder} onChange={(e) => setSortOrder(e.target.value)}>
        <option value="asc">Ascending</option>
        <option value="desc">Descending</option>
      </select>
      <select value={filter} onChange={(e) => setFilter(e.target.value)}>
        <option value="all">All</option>
        <option value="admin">Admin</option>
        <option value="user">User</option>
      </select>
      {filteredUsers.map((user) => (
        <div key={user.id}>
          {user.name} - {user.email}
        </div>
      ))}
    </div>
  );
}

// AFTER: Decomposed with proper types
interface UserListProps {
  users: User[];
}

interface FilterState {
  searchTerm: string;
  sortOrder: 'asc' | 'desc';
  roleFilter: User['role'] | 'all';
}

function useUserFilters(users: User[], filters: FilterState): User[] {
  return useMemo(() => {
    return users
      .filter((u) => u.name.toLowerCase().includes(filters.searchTerm.toLowerCase()))
      .filter((u) => filters.roleFilter === 'all' || u.role === filters.roleFilter)
      .sort((a, b) =>
        filters.sortOrder === 'asc' ? a.name.localeCompare(b.name) : b.name.localeCompare(a.name)
      );
  }, [users, filters]);
}

function SearchInput({ value, onChange }: { value: string; onChange: (value: string) => void }) {
  return (
    <input
      type="search"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder="Search users..."
      aria-label="Search users"
    />
  );
}

function UserListItem({ user }: { user: User }) {
  return (
    <div className="user-item">
      <span className="user-name">{user.name}</span>
      <span className="user-email">{user.email}</span>
      <span className="user-role">{user.role}</span>
    </div>
  );
}

function UserList({ users }: UserListProps) {
  const [filters, setFilters] = useState<FilterState>({
    searchTerm: '',
    sortOrder: 'asc',
    roleFilter: 'all',
  });

  const filteredUsers = useUserFilters(users, filters);

  const updateFilter = useCallback(<K extends keyof FilterState>(key: K, value: FilterState[K]) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  }, []);

  return (
    <div className="user-list">
      <div className="filters">
        <SearchInput value={filters.searchTerm} onChange={(v) => updateFilter('searchTerm', v)} />
        {/* Other filter controls */}
      </div>
      <div className="users">
        {filteredUsers.map((user) => (
          <UserListItem key={user.id} user={user} />
        ))}
      </div>
    </div>
  );
}

// =============================================================================
// Example 3: Effect Dependencies
// =============================================================================

// BEFORE: Missing or incorrect dependencies
function UserProfileBefore({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    fetch(`/api/users/${userId}`)
      .then((res) => res.json())
      .then(setUser);
  }, []); // Missing userId dependency!

  return <div>{user?.name}</div>;
}

// AFTER: Correct dependencies with cleanup
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function loadUser() {
      setLoading(true);
      setError(null);

      try {
        const response = await fetch(`/api/users/${userId}`);
        if (!response.ok) throw new Error('Failed to fetch user');

        const data = await response.json();
        if (!cancelled) {
          setUser(data);
        }
      } catch (e) {
        if (!cancelled) {
          setError(e instanceof Error ? e : new Error('Unknown error'));
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadUser();

    return () => {
      cancelled = true;
    };
  }, [userId]); // Correct dependency

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!user) return <div>User not found</div>;

  return <div>{user.name}</div>;
}

// =============================================================================
// Example 4: Memoization
// =============================================================================

// BEFORE: Unnecessary re-renders
function ExpensiveListBefore({ items, onSelect }: { items: string[]; onSelect: (item: string) => void }) {
  // New function created every render
  const handleClick = (item: string) => {
    console.log('Selected:', item);
    onSelect(item);
  };

  // Computed every render
  const sortedItems = items.slice().sort();

  return (
    <ul>
      {sortedItems.map((item) => (
        <li key={item} onClick={() => handleClick(item)}>
          {item}
        </li>
      ))}
    </ul>
  );
}

// AFTER: Proper memoization
interface ExpensiveListProps {
  items: string[];
  onSelect: (item: string) => void;
}

const ListItem = memo(function ListItem({
  item,
  onClick,
}: {
  item: string;
  onClick: (item: string) => void;
}) {
  return <li onClick={() => onClick(item)}>{item}</li>;
});

function ExpensiveList({ items, onSelect }: ExpensiveListProps) {
  const handleClick = useCallback(
    (item: string) => {
      console.log('Selected:', item);
      onSelect(item);
    },
    [onSelect]
  );

  const sortedItems = useMemo(() => items.slice().sort(), [items]);

  return (
    <ul>
      {sortedItems.map((item) => (
        <ListItem key={item} item={item} onClick={handleClick} />
      ))}
    </ul>
  );
}

// =============================================================================
// Example 5: Error Boundaries
// =============================================================================

// BEFORE: No error handling
function AppBefore() {
  return (
    <div>
      <UserProfile userId="1" />
    </div>
  );
}

// AFTER: With error boundary
import { Component, ReactNode } from 'react';

interface ErrorBoundaryProps {
  children: ReactNode;
  fallback?: ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback ?? <div>Something went wrong</div>;
    }
    return this.props.children;
  }
}

function App() {
  return (
    <ErrorBoundary fallback={<div>Failed to load user profile</div>}>
      <UserProfile userId="1" />
    </ErrorBoundary>
  );
}

export { UserList, UserProfile, ExpensiveList, ErrorBoundary, App };
