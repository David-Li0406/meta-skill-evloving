# 4. Client-Side Hooks & Server Actions

**Impact: HIGH**

React 19+ introduces specialized hooks to handle asynchronous state and form lifecycles natively.

## 4.1 The `use()` API

**Impact: HIGH (simplifies data fetching logic)**

The `use()` hook can unwrap promises or context values within the render body, allowing for conditional data loading.

**Incorrect: The old `useEffect` boilerplate**

```tsx
function Profile({ id }) {
  const [data, setData] = useState(null);
  useEffect(() => {
    fetchData(id).then(setData);
  }, [id]);

  if (!data) return <Loading />;
  return <div>{data.name}</div>;
}
```

**Correct: Using `use()` with Suspense**

```tsx
import { use } from 'react';

function Profile({ dataPromise }) {
  // Automatically suspends the component until dataPromise resolves
  const data = use(dataPromise);
  return <div>{data.name}</div>;
}
```

## 4.2 native Form Management with `useActionState`

**Impact: HIGH (built-in pending and error states)**

Formerly `useFormState`, this hook is the standard for handling form submissions with Server Actions.

```tsx
import { useActionState } from 'react';
import { updateProfile } from './actions';

function ProfileForm() {
  const [state, action, isPending] = useActionState(updateProfile, {
    message: null,
  });

  return (
    <form action={action}>
      <input name="username" disabled={isPending} />
      <button type="submit" disabled={isPending}>
        {isPending ? 'Saving...' : 'Save'}
      </button>
      {state.message && <p>{state.message}</p>}
    </form>
  );
}
```

## 4.3 `useOptimistic` for Instant UI

**Impact: MEDIUM (better UX)**

Provides a way to show a temporary state while an async action is in flight.

```tsx
import { useOptimistic } from 'react';

function ChatList({ messages }) {
  const [optimisticMessages, addOptimisticMessage] = useOptimistic(
    messages,
    (state, newMessage) => [...state, { text: newMessage, sending: true }]
  );

  async function formAction(formData) {
    const text = formData.get("message");
    addOptimisticMessage(text);
    await sendMessage(text);
  }

  return (
    <div>
      {optimisticMessages.map(m => <div key={m.id}>{m.text}</div>)}
      <form action={formAction}>
        <input name="message" />
      </form>
    </div>
  );
}
```

## 4.4 Deduplicate Global Event Listeners

Use `useEffectEvent` (React 19.2+) for logic that depends on reactive values but shouldn't trigger the effect itself.

```tsx
function Chat({ roomId, theme }) {
  const onConnected = useEffectEvent(() => {
    logAnalytics("Connected", { theme }); // theme is captured but doesn't re-run effect
  });

  useEffect(() => {
    const socket = connect(roomId);
    socket.on('connect', onConnected);
    return () => socket.disconnect();
  }, [roomId]); // theme is NOT a dependency
}
```
