# Frontend Engineering

## Patterns


---
  #### **Name**
Component Composition
  #### **Description**
Build complex UIs by composing simple, focused components rather than monolithic components with many props
  #### **When**
Component has more than 5-7 props, adding boolean props for variants, prop drilling
  #### **Example**
    // Composed from focused pieces
    <Card variant="horizontal">
      <Card.Image src="/img.jpg" />
      <Card.Body>
        <Card.Title>Product</Card.Title>
      </Card.Body>
      <Card.Footer>
        <Button>Buy</Button>
      </Card.Footer>
    </Card>
    

---
  #### **Name**
Container/Presenter
  #### **Description**
Separate data fetching and business logic (container) from pure presentation (presenter)
  #### **When**
Testing UI independent of data, reusing presentation with different sources
  #### **Example**
    // Presenter: Pure, easy to test
    function UserProfileView({ user, onFollow }) {
      return <div><Avatar src={user.avatar} /><Button onClick={onFollow}>Follow</Button></div>
    }
    
    // Container: Data logic
    function UserProfile({ userId }) {
      const { data: user } = useQuery(['user', userId], () => fetchUser(userId))
      return <UserProfileView user={user} onFollow={() => follow(userId)} />
    }
    

---
  #### **Name**
Optimistic Updates
  #### **Description**
Update UI immediately before server confirms, then reconcile if different
  #### **When**
Actions that usually succeed, low-latency feel is important
  #### **Example**
    useMutation({
      mutationFn: likePost,
      onMutate: async () => {
        await queryClient.cancelQueries(['post', id])
        const previous = queryClient.getQueryData(['post', id])
        queryClient.setQueryData(['post', id], old => ({...old, isLiked: true}))
        return { previous }
      },
      onError: (err, vars, context) => queryClient.setQueryData(['post', id], context.previous),
    })
    

---
  #### **Name**
Error Boundaries
  #### **Description**
Catch JavaScript errors in component trees and display fallback UI
  #### **When**
Always - around routes, third-party components, user-generated content
  #### **Example**
    <ErrorBoundary fallback={<FullPageError />}>
      <Header />
      <ErrorBoundary fallback={<SidebarError />}>
        <Sidebar />
      </ErrorBoundary>
      <MainContent />
    </ErrorBoundary>
    

---
  #### **Name**
Skeleton Loading
  #### **Description**
Show placeholder shapes that match content layout while data loads
  #### **When**
Predictable layout, content-heavy pages, preventing layout shift
  #### **Example**
    function PostCardSkeleton() {
      return (
        <div className="card">
          <Skeleton className="w-full aspect-video" />
          <Skeleton className="h-6 w-3/4 mb-2" />
          <Skeleton className="h-4 w-full" />
        </div>
      )
    }
    

---
  #### **Name**
Custom Hooks
  #### **Description**
Extract component logic into reusable functions that can use hooks
  #### **When**
Same logic in multiple components, complex logic cluttering component
  #### **Example**
    function useLocalStorage<T>(key: string, initial: T) {
      const [value, setValue] = useState<T>(() => {
        const stored = localStorage.getItem(key)
        return stored ? JSON.parse(stored) : initial
      })
      useEffect(() => localStorage.setItem(key, JSON.stringify(value)), [key, value])
      return [value, setValue] as const
    }
    

---
  #### **Name**
State Machine
  #### **Description**
Model component state as explicit states with defined transitions
  #### **When**
Complex UI with multiple states, states that are mutually exclusive
  #### **Example**
    type State =
      | { status: 'idle' }
      | { status: 'loading' }
      | { status: 'success'; data: Data }
      | { status: 'error'; error: Error }
    
    // Impossible states are impossible
    

---
  #### **Name**
Portal Pattern
  #### **Description**
Render children into different part of DOM, outside parent hierarchy
  #### **When**
Modals, tooltips, toasts, dropdowns that need to escape overflow:hidden
  #### **Example**
    function Modal({ children, isOpen }) {
      if (!isOpen) return null
      return createPortal(
        <div className="modal-overlay">{children}</div>,
        document.body
      )
    }
    

## Anti-Patterns


---
  #### **Name**
Prop Drilling
  #### **Description**
Passing props through 5+ components that don't use them
  #### **Why**
Every intermediate component depends on those props, refactoring becomes terrifying
  #### **Instead**
Use Context for cross-cutting concerns, or composition pattern

---
  #### **Name**
useEffect for Data Fetching
  #### **Description**
Fetching data in useEffect without proper handling
  #### **Why**
Creates waterfalls, race conditions, memory leaks
  #### **Instead**
Use data fetching library (React Query, SWR) or framework loaders

---
  #### **Name**
Boolean State Soup
  #### **Description**
Multiple boolean flags for mutually exclusive states (isLoading, isError, isSuccess)
  #### **Why**
Invalid combinations are possible (isLoading && isError both true)
  #### **Instead**
Use discriminated unions / state machines

---
  #### **Name**
Over-using memo
  #### **Description**
Adding memo() to everything without understanding why it helps
  #### **Why**
Memo has overhead, won't help if creating new objects/functions every render
  #### **Instead**
Fix the reference stability first, memo last resort

---
  #### **Name**
Import Entire Libraries
  #### **Description**
import _ from 'lodash' instead of import debounce from 'lodash/debounce'
  #### **Why**
Ships entire library to client, 10x bundle size increase
  #### **Instead**
Import only what you need, use smaller alternatives