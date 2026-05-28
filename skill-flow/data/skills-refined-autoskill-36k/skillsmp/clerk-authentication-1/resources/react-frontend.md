# React Frontend Implementation

Complete guide for implementing Clerk authentication in React applications.

## Installation

```bash
# Using npm
npm install @clerk/clerk-react

# Using yarn
yarn add @clerk/clerk-react

# Using pnpm
pnpm add @clerk/clerk-react
```

## Environment Setup

Create a `.env` file in your React project root:

```bash
# For Vite projects
VITE_CLERK_PUBLISHABLE_KEY=pk_test_your_publishable_key_here

# For Create React App
REACT_APP_CLERK_PUBLISHABLE_KEY=pk_test_your_publishable_key_here
```

## Basic Setup (main.jsx / index.jsx)

```javascript
import React from 'react'
import ReactDOM from 'react-dom/client'
import { ClerkProvider } from '@clerk/clerk-react'
import App from './App'
import './index.css'

// Get the publishable key from environment variables
const PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY

if (!PUBLISHABLE_KEY) {
  throw new Error('Missing Publishable Key. Please check your .env file.')
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ClerkProvider publishableKey={PUBLISHABLE_KEY}>
      <App />
    </ClerkProvider>
  </React.StrictMode>,
)
```

## Authentication Components

### Sign In and Sign Up Pages

```javascript
// src/pages/SignInPage.jsx
import { SignIn } from '@clerk/clerk-react'

export default function SignInPage() {
  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      minHeight: '100vh',
      backgroundColor: '#f5f5f5'
    }}>
      <SignIn 
        routing="path" 
        path="/sign-in"
        signUpUrl="/sign-up"
        afterSignInUrl="/dashboard"
      />
    </div>
  )
}
```

```javascript
// src/pages/SignUpPage.jsx
import { SignUp } from '@clerk/clerk-react'

export default function SignUpPage() {
  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      minHeight: '100vh',
      backgroundColor: '#f5f5f5'
    }}>
      <SignUp 
        routing="path" 
        path="/sign-up"
        signInUrl="/sign-in"
        afterSignUpUrl="/dashboard"
      />
    </div>
  )
}
```

### User Profile Page

```javascript
// src/pages/ProfilePage.jsx
import { UserProfile } from '@clerk/clerk-react'

export default function ProfilePage() {
  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      padding: '2rem'
    }}>
      <UserProfile 
        routing="path" 
        path="/profile"
      />
    </div>
  )
}
```

## Protected Routes

### Method 1: Using RedirectToSignIn

```javascript
// src/components/ProtectedRoute.jsx
import { useUser, RedirectToSignIn } from '@clerk/clerk-react'

export default function ProtectedRoute({ children }) {
  const { isSignedIn, isLoaded } = useUser()

  // Show loading state while checking authentication
  if (!isLoaded) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        minHeight: '100vh' 
      }}>
        <p>Loading...</p>
      </div>
    )
  }

  // Redirect to sign-in if not authenticated
  if (!isSignedIn) {
    return <RedirectToSignIn />
  }

  // Render protected content
  return children
}
```

### Method 2: Using React Router with Clerk

```javascript
// src/App.jsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useUser } from '@clerk/clerk-react'
import SignInPage from './pages/SignInPage'
import SignUpPage from './pages/SignUpPage'
import Dashboard from './pages/Dashboard'
import ProfilePage from './pages/ProfilePage'
import LandingPage from './pages/LandingPage'

function PrivateRoute({ children }) {
  const { isSignedIn, isLoaded } = useUser()

  if (!isLoaded) {
    return <div>Loading...</div>
  }

  return isSignedIn ? children : <Navigate to="/sign-in" replace />
}

function PublicRoute({ children }) {
  const { isSignedIn, isLoaded } = useUser()

  if (!isLoaded) {
    return <div>Loading...</div>
  }

  return !isSignedIn ? children : <Navigate to="/dashboard" replace />
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<LandingPage />} />
        
        {/* Auth routes - redirect to dashboard if already signed in */}
        <Route 
          path="/sign-in/*" 
          element={
            <PublicRoute>
              <SignInPage />
            </PublicRoute>
          } 
        />
        <Route 
          path="/sign-up/*" 
          element={
            <PublicRoute>
              <SignUpPage />
            </PublicRoute>
          } 
        />

        {/* Protected routes */}
        <Route 
          path="/dashboard" 
          element={
            <PrivateRoute>
              <Dashboard />
            </PrivateRoute>
          } 
        />
        <Route 
          path="/profile/*" 
          element={
            <PrivateRoute>
              <ProfilePage />
            </PrivateRoute>
          } 
        />
      </Routes>
    </BrowserRouter>
  )
}
```

## Using Clerk Hooks

### Display User Information

```javascript
// src/components/UserInfo.jsx
import { useUser } from '@clerk/clerk-react'

export default function UserInfo() {
  const { user, isLoaded } = useUser()

  if (!isLoaded) {
    return <div>Loading user data...</div>
  }

  if (!user) {
    return <div>Not signed in</div>
  }

  return (
    <div>
      <h2>Welcome, {user.firstName}!</h2>
      <p>Email: {user.primaryEmailAddress?.emailAddress}</p>
      <p>User ID: {user.id}</p>
      <p>Member since: {new Date(user.createdAt).toLocaleDateString()}</p>
    </div>
  )
}
```

### Sign Out Button

```javascript
// src/components/SignOutButton.jsx
import { useClerk } from '@clerk/clerk-react'

export default function SignOutButton() {
  const { signOut } = useClerk()

  return (
    <button 
      onClick={() => signOut()}
      style={{
        padding: '0.5rem 1rem',
        backgroundColor: '#dc2626',
        color: 'white',
        border: 'none',
        borderRadius: '0.375rem',
        cursor: 'pointer'
      }}
    >
      Sign Out
    </button>
  )
}
```

### User Button Component

```javascript
// src/components/UserButton.jsx
import { UserButton as ClerkUserButton } from '@clerk/clerk-react'

export default function UserButton() {
  return (
    <ClerkUserButton 
      afterSignOutUrl="/"
      appearance={{
        elements: {
          avatarBox: 'w-10 h-10'
        }
      }}
    />
  )
}
```

## Making Authenticated API Requests

### Using Fetch with Token

```javascript
// src/utils/api.js
import { useAuth } from '@clerk/clerk-react'

export function useAuthenticatedFetch() {
  const { getToken } = useAuth()

  const authenticatedFetch = async (url, options = {}) => {
    try {
      // Get the Clerk session token
      const token = await getToken()

      if (!token) {
        throw new Error('No authentication token available')
      }

      // Add Authorization header
      const headers = {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        ...options.headers,
      }

      const response = await fetch(url, {
        ...options,
        headers,
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      return await response.json()
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  }

  return authenticatedFetch
}
```

### Example Usage in a Component

```javascript
// src/pages/Dashboard.jsx
import { useState, useEffect } from 'react'
import { useAuthenticatedFetch } from '../utils/api'
import { useUser } from '@clerk/clerk-react'

export default function Dashboard() {
  const { user } = useUser()
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const authenticatedFetch = useAuthenticatedFetch()

  useEffect(() => {
    async function fetchProtectedData() {
      try {
        const result = await authenticatedFetch('http://localhost:8000/protected')
        setData(result)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchProtectedData()
  }, [])

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error}</div>

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Dashboard</h1>
      <p>Welcome, {user?.firstName}!</p>
      {data && (
        <pre>{JSON.stringify(data, null, 2)}</pre>
      )}
    </div>
  )
}
```

### Using Axios with Interceptors

```javascript
// src/utils/axios.js
import axios from 'axios'

export function createAuthenticatedAxios(getToken) {
  const instance = axios.create({
    baseURL: 'http://localhost:8000',
    headers: {
      'Content-Type': 'application/json',
    },
  })

  // Request interceptor to add auth token
  instance.interceptors.request.use(
    async (config) => {
      const token = await getToken()
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    },
    (error) => {
      return Promise.reject(error)
    }
  )

  // Response interceptor for error handling
  instance.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response?.status === 401) {
        // Handle unauthorized access
        console.error('Authentication failed')
      }
      return Promise.reject(error)
    }
  )

  return instance
}

// Usage in a component
// const { getToken } = useAuth()
// const api = createAuthenticatedAxios(getToken)
// const response = await api.get('/protected')
```

## Navigation Bar with Auth

```javascript
// src/components/NavBar.jsx
import { useUser, UserButton } from '@clerk/clerk-react'
import { Link } from 'react-router-dom'

export default function NavBar() {
  const { isSignedIn, isLoaded } = useUser()

  return (
    <nav style={{
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      padding: '1rem 2rem',
      backgroundColor: '#1f2937',
      color: 'white'
    }}>
      <div>
        <Link to="/" style={{ color: 'white', textDecoration: 'none', fontSize: '1.5rem' }}>
          My App
        </Link>
      </div>

      <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
        {!isLoaded ? (
          <span>Loading...</span>
        ) : isSignedIn ? (
          <>
            <Link to="/dashboard" style={{ color: 'white', textDecoration: 'none' }}>
              Dashboard
            </Link>
            <Link to="/profile" style={{ color: 'white', textDecoration: 'none' }}>
              Profile
            </Link>
            <UserButton afterSignOutUrl="/" />
          </>
        ) : (
          <>
            <Link to="/sign-in" style={{ color: 'white', textDecoration: 'none' }}>
              Sign In
            </Link>
            <Link 
              to="/sign-up" 
              style={{
                color: 'white',
                textDecoration: 'none',
                padding: '0.5rem 1rem',
                backgroundColor: '#3b82f6',
                borderRadius: '0.375rem'
              }}
            >
              Sign Up
            </Link>
          </>
        )}
      </div>
    </nav>
  )
}
```

## Customizing Clerk Components

### Custom Styling

```javascript
// src/pages/SignInPage.jsx
import { SignIn } from '@clerk/clerk-react'

export default function SignInPage() {
  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      minHeight: '100vh'
    }}>
      <SignIn 
        appearance={{
          elements: {
            rootBox: 'mx-auto',
            card: 'shadow-xl',
            headerTitle: 'text-2xl font-bold',
            headerSubtitle: 'text-gray-600',
            socialButtonsBlockButton: 'border-2 hover:bg-gray-50',
            formButtonPrimary: 'bg-blue-600 hover:bg-blue-700',
          },
        }}
      />
    </div>
  )
}
```

### Using Variables for Theming

```javascript
const clerkAppearance = {
  variables: {
    colorPrimary: '#3b82f6',
    colorText: '#1f2937',
    colorBackground: '#ffffff',
    colorInputBackground: '#f9fafb',
    colorInputText: '#1f2937',
    borderRadius: '0.5rem',
  },
}

<ClerkProvider 
  publishableKey={PUBLISHABLE_KEY}
  appearance={clerkAppearance}
>
  <App />
</ClerkProvider>
```

## Error Handling

```javascript
// src/components/AuthErrorBoundary.jsx
import { Component } from 'react'

class AuthErrorBoundary extends Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  componentDidCatch(error, errorInfo) {
    console.error('Auth error:', error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          padding: '2rem',
          textAlign: 'center'
        }}>
          <h1>Authentication Error</h1>
          <p>Something went wrong with authentication.</p>
          <button onClick={() => window.location.reload()}>
            Reload Page
          </button>
        </div>
      )
    }

    return this.props.children
  }
}

export default AuthErrorBoundary
```

## Complete Example Application Structure

```
src/
├── main.jsx                 # App entry point with ClerkProvider
├── App.jsx                  # Main app with routing
├── components/
│   ├── NavBar.jsx          # Navigation with auth state
│   ├── ProtectedRoute.jsx  # Route protection wrapper
│   ├── UserInfo.jsx        # Display user information
│   ├── SignOutButton.jsx   # Sign out functionality
│   └── UserButton.jsx      # Clerk user button wrapper
├── pages/
│   ├── LandingPage.jsx     # Public landing page
│   ├── SignInPage.jsx      # Sign in page
│   ├── SignUpPage.jsx      # Sign up page
│   ├── Dashboard.jsx       # Protected dashboard
│   └── ProfilePage.jsx     # User profile management
├── utils/
│   ├── api.js              # Authenticated fetch utilities
│   └── axios.js            # Axios instance with auth
└── styles/
    └── index.css           # Global styles
```

## Testing

### Testing with React Testing Library

```javascript
// src/components/__tests__/ProtectedRoute.test.jsx
import { render, screen } from '@testing-library/react'
import { ClerkProvider } from '@clerk/clerk-react'
import ProtectedRoute from '../ProtectedRoute'

describe('ProtectedRoute', () => {
  it('shows loading state initially', () => {
    render(
      <ClerkProvider publishableKey="test_key">
        <ProtectedRoute>
          <div>Protected Content</div>
        </ProtectedRoute>
      </ClerkProvider>
    )
    
    expect(screen.getByText('Loading...')).toBeInTheDocument()
  })
})
```

## Next Steps

- See [fastapi-backend.md](fastapi-backend.md) for backend implementation
- See [user-management.md](user-management.md) for advanced user operations
- See [examples.md](examples.md) for complete working examples
