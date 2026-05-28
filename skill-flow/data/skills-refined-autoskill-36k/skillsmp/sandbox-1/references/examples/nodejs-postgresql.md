# Node.js + PostgreSQL REST API

Complete Node.js application with PostgreSQL database and web frontend on Buddy Sandbox.

## Result

| Service | Port | Public URL |
|---------|------|------------|
| Todo App (Frontend + API) | 3000 | `https://api-<sandbox>-<project>-<workspace>.us-1.buddy.app` |

## Step 1: Create Sandbox with Node.js and PostgreSQL

```bash
bdy sandbox create -i nodejs-api --resources 2x4 \
  --install-command "apt-get update && apt-get install -y nodejs npm postgresql postgresql-contrib"
```

Wait for setup to complete:
```bash
bdy sandbox status nodejs-api
# Wait until Setup: SUCCESS
```

**Note:** Using system Node.js (apt) instead of NodeSource for simplicity. For newer Node.js versions, add NodeSource setup script to install commands.

## Step 2: Start and Configure PostgreSQL

```bash
# Start PostgreSQL service
bdy sandbox exec command nodejs-api "service postgresql start" --wait

# Create database user
bdy sandbox exec command nodejs-api "su - postgres -c \"psql -c \\\"CREATE USER appuser WITH PASSWORD 'apppass123';\\\"\"" --wait

# Create database
bdy sandbox exec command nodejs-api "su - postgres -c \"psql -c \\\"CREATE DATABASE appdb OWNER appuser;\\\"\"" --wait
```

## Step 3: Deploy Application

### Option A: Copy Local Project

```bash
# Copy local project (use --silent to prevent stdout flood)
bdy sandbox cp --silent ./my-nodejs-app nodejs-api:/app

# Install dependencies
bdy sandbox exec command nodejs-api "cd /app && npm install" --wait

# Start application (runs in background by default)
bdy sandbox exec command nodejs-api "cd /app && npm start"
```

### Option B: Create Simple API In-Place

Create the application files locally first, then copy to sandbox:

**package.json:**
```bash
cat > /tmp/package.json << 'EOF'
{
  "name": "nodejs-api",
  "version": "1.0.0",
  "main": "server.js",
  "scripts": { "start": "node server.js" },
  "dependencies": { "express": "^4.18.2", "pg": "^8.11.3" }
}
EOF
```

**server.js:**
```bash
cat > /tmp/server.js << 'EOF'
const express = require('express');
const { Pool } = require('pg');

const app = express();
app.use(express.json());

const pool = new Pool({
  host: process.env.DB_HOST || 'localhost',
  port: process.env.DB_PORT || 5432,
  database: process.env.DB_NAME || 'appdb',
  user: process.env.DB_USER || 'appuser',
  password: process.env.DB_PASSWORD || 'apppass123'
});

// Initialize table
async function initDB() {
  await pool.query(`
    CREATE TABLE IF NOT EXISTS todos (
      id SERIAL PRIMARY KEY,
      title VARCHAR(255) NOT NULL,
      completed BOOLEAN DEFAULT FALSE,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
  `);
}

app.get('/', (req, res) => res.json({ message: 'Node.js + PostgreSQL API' }));

app.get('/health', async (req, res) => {
  try {
    await pool.query('SELECT 1');
    res.json({ status: 'ok', database: 'connected' });
  } catch (err) {
    res.status(500).json({ status: 'error', error: err.message });
  }
});

app.get('/todos', async (req, res) => {
  const result = await pool.query('SELECT * FROM todos ORDER BY created_at DESC');
  res.json(result.rows);
});

app.post('/todos', async (req, res) => {
  const { title } = req.body;
  if (!title) return res.status(400).json({ error: 'Title required' });
  const result = await pool.query('INSERT INTO todos (title) VALUES ($1) RETURNING *', [title]);
  res.status(201).json(result.rows[0]);
});

// IMPORTANT: Bind to 0.0.0.0 for sandbox accessibility
const PORT = process.env.PORT || 3000;
initDB().then(() => {
  app.listen(PORT, '0.0.0.0', () => console.log(`Server on port ${PORT}`));
});
EOF
```

**Deploy files:**
```bash
# Create app directory
bdy sandbox exec command nodejs-api "mkdir -p /app" --wait

# Copy files to sandbox
bdy sandbox cp --silent /tmp/package.json nodejs-api:/app/package.json
bdy sandbox cp --silent /tmp/server.js nodejs-api:/app/server.js

# Install and start
bdy sandbox exec command nodejs-api "cd /app && npm install" --wait
bdy sandbox exec command nodejs-api "cd /app && npm start"
```

## Step 4: Add Web Frontend (Optional)

Create a simple HTML frontend for the Todo API:

**public/index.html:**
```bash
mkdir -p /tmp/public
cat > /tmp/public/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Todo App</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      min-height: 100vh; padding: 40px 20px;
    }
    .container {
      max-width: 500px; margin: 0 auto; background: white;
      border-radius: 16px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); overflow: hidden;
    }
    header { background: #667eea; color: white; padding: 30px; text-align: center; }
    header h1 { font-size: 28px; margin-bottom: 5px; }
    .status { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; margin-top: 10px; }
    .status.connected { background: #48bb78; }
    .status.disconnected { background: #f56565; }
    .add-form { display: flex; padding: 20px; gap: 10px; border-bottom: 1px solid #eee; }
    .add-form input { flex: 1; padding: 12px 16px; border: 2px solid #e2e8f0; border-radius: 8px; font-size: 16px; }
    .add-form button { padding: 12px 24px; background: #667eea; color: white; border: none; border-radius: 8px; cursor: pointer; }
    .todos { list-style: none; }
    .todo-item { display: flex; align-items: center; padding: 16px 20px; border-bottom: 1px solid #eee; }
    .todo-item.completed .todo-title { text-decoration: line-through; color: #a0aec0; }
    .todo-checkbox { width: 24px; height: 24px; border: 2px solid #cbd5e0; border-radius: 50%; margin-right: 16px; cursor: pointer; }
    .todo-item.completed .todo-checkbox { background: #48bb78; border-color: #48bb78; }
    .todo-title { flex: 1; }
    .todo-delete { width: 32px; height: 32px; border: none; background: none; color: #a0aec0; font-size: 20px; cursor: pointer; }
    .empty { text-align: center; padding: 60px 20px; color: #a0aec0; }
  </style>
</head>
<body>
  <div class="container">
    <header><h1>Todo App</h1><p>Node.js + PostgreSQL</p><span class="status" id="status">Connecting...</span></header>
    <form class="add-form" id="addForm"><input type="text" id="todoInput" placeholder="What needs to be done?" required><button type="submit">Add</button></form>
    <ul class="todos" id="todoList"></ul>
  </div>
  <script>
    const todoList = document.getElementById('todoList');
    const todoInput = document.getElementById('todoInput');
    const status = document.getElementById('status');

    async function checkHealth() {
      try {
        const res = await fetch('/health');
        const data = await res.json();
        status.textContent = data.database === 'connected' ? 'DB Connected' : 'DB Error';
        status.className = 'status ' + (data.database === 'connected' ? 'connected' : 'disconnected');
      } catch (e) { status.textContent = 'Offline'; status.className = 'status disconnected'; }
    }

    async function loadTodos() {
      const res = await fetch('/todos');
      const todos = await res.json();
      if (todos.length === 0) { todoList.innerHTML = '<div class="empty">No todos yet!</div>'; return; }
      todoList.innerHTML = todos.map(t => `
        <li class="todo-item ${t.completed ? 'completed' : ''}" data-id="${t.id}">
          <div class="todo-checkbox" onclick="toggleTodo(${t.id}, ${!t.completed})"></div>
          <span class="todo-title">${t.title}</span>
          <button class="todo-delete" onclick="deleteTodo(${t.id})">×</button>
        </li>`).join('');
    }

    document.getElementById('addForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      await fetch('/todos', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ title: todoInput.value }) });
      todoInput.value = ''; loadTodos();
    });

    async function toggleTodo(id, completed) {
      await fetch(`/todos/${id}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ completed }) });
      loadTodos();
    }

    async function deleteTodo(id) { await fetch(`/todos/${id}`, { method: 'DELETE' }); loadTodos(); }

    checkHealth(); loadTodos();
  </script>
</body>
</html>
EOF
```

**Update server.js to serve static files:**

Add this line after `app.use(express.json());`:
```javascript
app.use(express.static(path.join(__dirname, 'public')));
```

And add at the top:
```javascript
const path = require('path');
```

**Deploy frontend:**
```bash
bdy sandbox cp --silent /tmp/public nodejs-api:/app/public
```

**Restart application:**
```bash
bdy sandbox exec command nodejs-api "pkill -f 'node server.js'" --wait
bdy sandbox exec command nodejs-api "cd /app && npm start"
```

## Step 5: Expose Endpoint

```bash
bdy sandbox endpoint add nodejs-api -n api -e 3000
```

## Step 5: Verify

```bash
# Check process is running
bdy sandbox exec command nodejs-api "ps aux | grep node" --wait

# Test API
curl https://api-nodejs-api-<project>-<workspace>.us-1.buddy.app/health
# Expected: {"status":"ok","database":"connected"}

# Test CRUD operations
curl -X POST -H "Content-Type: application/json" \
  -d '{"title":"My first todo"}' \
  https://api-nodejs-api-<project>-<workspace>.us-1.buddy.app/todos

curl https://api-nodejs-api-<project>-<workspace>.us-1.buddy.app/todos
```

## Database Credentials

| Service | Username | Password | Database |
|---------|----------|----------|----------|
| PostgreSQL | appuser | apppass123 | appdb |
| PostgreSQL | postgres | (no password, local only) | - |

## Critical Requirements

### 1. App must bind to `0.0.0.0`

```javascript
// CORRECT
app.listen(3000, '0.0.0.0', callback);

// WRONG - won't be accessible from outside
app.listen(3000, 'localhost', callback);
app.listen(3000, '127.0.0.1', callback);
```

### 2. PostgreSQL service must be started manually

PostgreSQL doesn't auto-start after sandbox creation:
```bash
bdy sandbox exec command nodejs-api "service postgresql start" --wait
```

### 3. Database commands require `su - postgres`

PostgreSQL uses peer authentication for local connections:
```bash
# CORRECT
bdy sandbox exec command nodejs-api "su - postgres -c \"psql -c \\\"CREATE USER ...\\\"\"" --wait

# WRONG - permission denied
bdy sandbox exec command nodejs-api "psql -c \"CREATE USER ...\"" --wait
```

### 4. Always use `--silent` with `bdy sandbox cp`

Prevents stdout flood that breaks AI agent execution.

## Troubleshooting

### Connection refused on endpoint

**Cause:** App not running or bound to wrong host

**Fix:**
```bash
# Check if process is running
bdy sandbox exec command nodejs-api "ps aux | grep node" --wait

# Check if listening on correct port
bdy sandbox exec command nodejs-api "ss -tlnp | grep 3000" --wait
```

### Database connection error

**Cause:** PostgreSQL not started or wrong credentials

**Fix:**
```bash
# Start PostgreSQL
bdy sandbox exec command nodejs-api "service postgresql start" --wait

# Verify user exists
bdy sandbox exec command nodejs-api "su - postgres -c \"psql -c \\\"\\\\du\\\"\"" --wait
```

### npm: command not found

**Cause:** npm not installed (may happen with minimal nodejs package)

**Fix:**
```bash
bdy sandbox exec command nodejs-api "apt-get install -y npm" --wait
```

### Services not running after sandbox restart

**Fix:** Manually restart services:
```bash
bdy sandbox exec command nodejs-api "service postgresql start" --wait
bdy sandbox exec command nodejs-api "cd /app && npm start"
```
