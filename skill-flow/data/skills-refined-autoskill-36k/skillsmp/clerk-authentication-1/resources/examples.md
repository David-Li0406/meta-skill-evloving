# Complete Working Examples

Full-stack examples combining frontend React and backend FastAPI with Clerk authentication.

## Example 1: Simple Todo App with Authentication

### Backend (FastAPI)

```python
# backend/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import os
from dotenv import load_dotenv

from auth import verify_clerk_token

load_dotenv()

app = FastAPI(title="Todo API with Clerk Auth")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory database (use real database in production)
todos_db = {}

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class Todo(BaseModel):
    id: str
    title: str
    description: Optional[str]
    completed: bool
    user_id: str
    created_at: datetime
    updated_at: datetime

@app.get("/")
async def root():
    return {"message": "Todo API with Clerk Authentication"}

@app.get("/todos", response_model=List[Todo])
async def get_todos(auth_data = Depends(verify_clerk_token)):
    """Get all todos for the authenticated user."""
    user_id = auth_data["user_id"]
    user_todos = [todo for todo in todos_db.values() if todo["user_id"] == user_id]
    return user_todos

@app.post("/todos", response_model=Todo, status_code=201)
async def create_todo(
    todo: TodoCreate,
    auth_data = Depends(verify_clerk_token)
):
    """Create a new todo for the authenticated user."""
    user_id = auth_data["user_id"]
    
    todo_id = f"todo_{len(todos_db) + 1}"
    now = datetime.now()
    
    new_todo = {
        "id": todo_id,
        "title": todo.title,
        "description": todo.description,
        "completed": False,
        "user_id": user_id,
        "created_at": now,
        "updated_at": now
    }
    
    todos_db[todo_id] = new_todo
    return new_todo

@app.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(
    todo_id: str,
    auth_data = Depends(verify_clerk_token)
):
    """Get a specific todo."""
    user_id = auth_data["user_id"]
    
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo = todos_db[todo_id]
    
    if todo["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this todo")
    
    return todo

@app.patch("/todos/{todo_id}", response_model=Todo)
async def update_todo(
    todo_id: str,
    todo_update: TodoUpdate,
    auth_data = Depends(verify_clerk_token)
):
    """Update a todo."""
    user_id = auth_data["user_id"]
    
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo = todos_db[todo_id]
    
    if todo["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this todo")
    
    # Update fields
    if todo_update.title is not None:
        todo["title"] = todo_update.title
    if todo_update.description is not None:
        todo["description"] = todo_update.description
    if todo_update.completed is not None:
        todo["completed"] = todo_update.completed
    
    todo["updated_at"] = datetime.now()
    
    return todo

@app.delete("/todos/{todo_id}")
async def delete_todo(
    todo_id: str,
    auth_data = Depends(verify_clerk_token)
):
    """Delete a todo."""
    user_id = auth_data["user_id"]
    
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo = todos_db[todo_id]
    
    if todo["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this todo")
    
    del todos_db[todo_id]
    
    return {"message": "Todo deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Frontend (React)

```javascript
// src/pages/TodosPage.jsx
import { useState, useEffect } from 'react'
import { useAuth } from '@clerk/clerk-react'

export default function TodosPage() {
  const { getToken } = useAuth()
  const [todos, setTodos] = useState([])
  const [loading, setLoading] = useState(true)
  const [newTodoTitle, setNewTodoTitle] = useState('')
  const [newTodoDescription, setNewTodoDescription] = useState('')

  const API_BASE = 'http://localhost:8000'

  useEffect(() => {
    fetchTodos()
  }, [])

  const fetchTodos = async () => {
    try {
      const token = await getToken()
      const response = await fetch(`${API_BASE}/todos`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })
      
      if (!response.ok) throw new Error('Failed to fetch todos')
      
      const data = await response.json()
      setTodos(data)
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setLoading(false)
    }
  }

  const createTodo = async (e) => {
    e.preventDefault()
    
    try {
      const token = await getToken()
      const response = await fetch(`${API_BASE}/todos`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: newTodoTitle,
          description: newTodoDescription,
        }),
      })
      
      if (!response.ok) throw new Error('Failed to create todo')
      
      const newTodo = await response.json()
      setTodos([...todos, newTodo])
      setNewTodoTitle('')
      setNewTodoDescription('')
    } catch (error) {
      console.error('Error:', error)
    }
  }

  const toggleTodo = async (todoId, completed) => {
    try {
      const token = await getToken()
      const response = await fetch(`${API_BASE}/todos/${todoId}`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ completed: !completed }),
      })
      
      if (!response.ok) throw new Error('Failed to update todo')
      
      const updatedTodo = await response.json()
      setTodos(todos.map(todo => 
        todo.id === todoId ? updatedTodo : todo
      ))
    } catch (error) {
      console.error('Error:', error)
    }
  }

  const deleteTodo = async (todoId) => {
    try {
      const token = await getToken()
      const response = await fetch(`${API_BASE}/todos/${todoId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })
      
      if (!response.ok) throw new Error('Failed to delete todo')
      
      setTodos(todos.filter(todo => todo.id !== todoId))
    } catch (error) {
      console.error('Error:', error)
    }
  }

  if (loading) {
    return <div className="flex justify-center p-8">Loading...</div>
  }

  return (
    <div className="max-w-4xl mx-auto p-8">
      <h1 className="text-3xl font-bold mb-6">My Todos</h1>
      
      {/* Create Todo Form */}
      <form onSubmit={createTodo} className="mb-8 p-6 bg-gray-50 rounded-lg">
        <h2 className="text-xl font-semibold mb-4">Add New Todo</h2>
        <div className="space-y-4">
          <input
            type="text"
            placeholder="Title"
            value={newTodoTitle}
            onChange={(e) => setNewTodoTitle(e.target.value)}
            required
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <textarea
            placeholder="Description (optional)"
            value={newTodoDescription}
            onChange={(e) => setNewTodoDescription(e.target.value)}
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows="3"
          />
          <button
            type="submit"
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Add Todo
          </button>
        </div>
      </form>

      {/* Todos List */}
      <div className="space-y-4">
        {todos.length === 0 ? (
          <p className="text-gray-500 text-center">No todos yet. Create one above!</p>
        ) : (
          todos.map(todo => (
            <div
              key={todo.id}
              className="p-4 bg-white border rounded-lg shadow-sm hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-3 flex-1">
                  <input
                    type="checkbox"
                    checked={todo.completed}
                    onChange={() => toggleTodo(todo.id, todo.completed)}
                    className="mt-1"
                  />
                  <div className="flex-1">
                    <h3 className={`font-semibold ${todo.completed ? 'line-through text-gray-400' : ''}`}>
                      {todo.title}
                    </h3>
                    {todo.description && (
                      <p className={`text-sm mt-1 ${todo.completed ? 'text-gray-400' : 'text-gray-600'}`}>
                        {todo.description}
                      </p>
                    )}
                    <p className="text-xs text-gray-400 mt-2">
                      Created: {new Date(todo.created_at).toLocaleString()}
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => deleteTodo(todo.id)}
                  className="text-red-500 hover:text-red-700 ml-4"
                >
                  Delete
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
```

## Example 2: Multi-Tenant Dashboard with Organizations

### Backend

```python
# backend/org_api.py
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from auth import verify_clerk_token
from clerk_backend_api import Clerk
import os

clerk = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))

class ProjectCreate(BaseModel):
    name: str
    description: str

# In-memory project storage
projects_db = {}

@app.get("/organizations/{org_id}/projects")
async def get_organization_projects(
    org_id: str,
    auth_data = Depends(verify_clerk_token)
):
    """Get all projects for an organization."""
    # Verify user is member of organization
    user_orgs = clerk.users.get_organization_memberships(
        user_id=auth_data["user_id"]
    )
    
    is_member = any(m.organization.id == org_id for m in user_orgs.data)
    if not is_member:
        raise HTTPException(status_code=403, detail="Not a member of this organization")
    
    # Get projects for this organization
    org_projects = [p for p in projects_db.values() if p["organization_id"] == org_id]
    return {"projects": org_projects}

@app.post("/organizations/{org_id}/projects")
async def create_organization_project(
    org_id: str,
    project: ProjectCreate,
    auth_data = Depends(verify_clerk_token)
):
    """Create a new project in an organization."""
    # Verify user is admin of organization
    user_orgs = clerk.users.get_organization_memberships(
        user_id=auth_data["user_id"]
    )
    
    user_org = next((m for m in user_orgs.data if m.organization.id == org_id), None)
    if not user_org:
        raise HTTPException(status_code=403, detail="Not a member of this organization")
    
    if user_org.role != "admin":
        raise HTTPException(status_code=403, detail="Admin role required")
    
    project_id = f"proj_{len(projects_db) + 1}"
    new_project = {
        "id": project_id,
        "name": project.name,
        "description": project.description,
        "organization_id": org_id,
        "created_by": auth_data["user_id"]
    }
    
    projects_db[project_id] = new_project
    return new_project
```

### Frontend

```javascript
// src/pages/OrganizationDashboard.jsx
import { useState, useEffect } from 'react'
import { useOrganization, useAuth } from '@clerk/clerk-react'

export default function OrganizationDashboard() {
  const { organization, membership } = useOrganization()
  const { getToken } = useAuth()
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (organization) {
      fetchProjects()
    }
  }, [organization])

  const fetchProjects = async () => {
    try {
      const token = await getToken()
      const response = await fetch(
        `http://localhost:8000/organizations/${organization.id}/projects`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        }
      )
      
      const data = await response.json()
      setProjects(data.projects)
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setLoading(false)
    }
  }

  if (!organization) {
    return <div className="p-8">Please select an organization</div>
  }

  if (loading) {
    return <div className="p-8">Loading...</div>
  }

  const isAdmin = membership?.role === 'admin'

  return (
    <div className="max-w-6xl mx-auto p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">{organization.name}</h1>
        <p className="text-gray-600">Your role: {membership?.role}</p>
        <p className="text-gray-600">Members: {organization.membersCount}</p>
      </div>

      <div className="mb-8">
        <h2 className="text-2xl font-semibold mb-4">Projects</h2>
        {projects.length === 0 ? (
          <p className="text-gray-500">No projects yet</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {projects.map(project => (
              <div key={project.id} className="p-4 border rounded-lg">
                <h3 className="font-semibold">{project.name}</h3>
                <p className="text-sm text-gray-600">{project.description}</p>
              </div>
            ))}
          </div>
        )}
      </div>

      {isAdmin && (
        <div className="mt-8 p-4 bg-blue-50 rounded-lg">
          <p className="text-blue-800">✨ As an admin, you can create new projects</p>
        </div>
      )}
    </div>
  )
}
```

## Example 3: Complete Authentication Flow

```javascript
// src/App.jsx - Complete app with all routes
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { ClerkProvider, SignIn, SignUp, useUser } from '@clerk/clerk-react'
import NavBar from './components/NavBar'
import LandingPage from './pages/LandingPage'
import Dashboard from './pages/Dashboard'
import TodosPage from './pages/TodosPage'
import ProfilePage from './pages/ProfilePage'
import OrganizationDashboard from './pages/OrganizationDashboard'

const PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY

function PrivateRoute({ children }) {
  const { isSignedIn, isLoaded } = useUser()

  if (!isLoaded) return <div>Loading...</div>

  return isSignedIn ? children : <Navigate to="/sign-in" replace />
}

function App() {
  return (
    <ClerkProvider publishableKey={PUBLISHABLE_KEY}>
      <BrowserRouter>
        <NavBar />
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/sign-in/*" element={<SignIn routing="path" path="/sign-in" />} />
          <Route path="/sign-up/*" element={<SignUp routing="path" path="/sign-up" />} />
          
          <Route
            path="/dashboard"
            element={
              <PrivateRoute>
                <Dashboard />
              </PrivateRoute>
            }
          />
          <Route
            path="/todos"
            element={
              <PrivateRoute>
                <TodosPage />
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
          <Route
            path="/organization"
            element={
              <PrivateRoute>
                <OrganizationDashboard />
              </PrivateRoute>
            }
          />
        </Routes>
      </BrowserRouter>
    </ClerkProvider>
  )
}

export default App
```

## Running the Examples

### 1. Setup Environment Variables

Backend `.env`:
```bash
CLERK_SECRET_KEY=sk_test_your_secret_key
CLERK_ISSUER=https://your-instance.clerk.accounts.dev
CLERK_JWKS_URL=https://your-instance.clerk.accounts.dev/.well-known/jwks.json
```

Frontend `.env`:
```bash
VITE_CLERK_PUBLISHABLE_KEY=pk_test_your_publishable_key
```

### 2. Install Dependencies

Backend:
```bash
cd backend
pip install fastapi uvicorn python-jose requests clerk-backend-api python-dotenv
```

Frontend:
```bash
cd frontend
npm install @clerk/clerk-react react-router-dom
```

### 3. Run the Applications

Backend:
```bash
cd backend
uvicorn main:app --reload
```

Frontend:
```bash
cd frontend
npm run dev
```

### 4. Test the Flow

1. Visit `http://localhost:5173`
2. Click "Sign Up" to create an account
3. Sign in with your credentials
4. Navigate to `/todos` to test the Todo app
5. Create, update, and delete todos
6. Check that todos are user-specific

## Next Steps

- Add database integration (PostgreSQL, MongoDB)
- Implement real-time updates with WebSockets
- Add file upload functionality
- Implement search and filtering
- Add pagination for large datasets
- Implement role-based access control
- Add email notifications
- Implement audit logging
