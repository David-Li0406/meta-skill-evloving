# Express Bug Patterns Reference

This document contains common bug patterns to include in Express debugging practice projects.

## Table of Contents

1. [Routing Issues](#routing-issues)
2. [Middleware Problems](#middleware-problems)
3. [Async/Promise Handling](#asyncpromise-handling)
4. [Request/Response Bugs](#requestresponse-bugs)
5. [Error Handling](#error-handling)
6. [Database Query Issues](#database-query-issues)

---

## Routing Issues

### Route Order Matters
**Bug Type**: Routing
**Difficulty**: Intermediate

```javascript
// Bug: Specific route defined after catch-all route
app.get('/users/:id', (req, res) => {
  res.json({ id: req.params.id });
});

app.get('/users/me', (req, res) => { // Never reached!
  res.json({ current: 'user' });
});
```

**Fix**: Put specific routes before parameterized routes
```javascript
app.get('/users/me', (req, res) => {
  res.json({ current: 'user' });
});

app.get('/users/:id', (req, res) => {
  res.json({ id: req.params.id });
});
```

---

### Missing Route Handler Response
**Bug Type**: Logic Error
**Difficulty**: Beginner

```javascript
app.get('/api/data', (req, res) => {
  const data = fetchData();
  console.log(data);
  // Bug: Forgot to send response - request hangs
});
```

**Fix**: Send response
```javascript
app.get('/api/data', (req, res) => {
  const data = fetchData();
  console.log(data);
  res.json(data);
});
```

---

## Middleware Problems

### Middleware Not Calling next()
**Bug Type**: Middleware
**Difficulty**: Beginner

```javascript
app.use((req, res, next) => {
  console.log(`${req.method} ${req.path}`);
  // Bug: Forgot to call next() - all requests hang
});

app.get('/api/users', (req, res) => {
  res.json([]);
});
```

**Fix**: Call next()
```javascript
app.use((req, res, next) => {
  console.log(`${req.method} ${req.path}`);
  next();
});
```

---

### Body Parser Not Applied
**Bug Type**: Middleware
**Difficulty**: Beginner

```javascript
const express = require('express');
const app = express();

app.post('/api/users', (req, res) => {
  console.log(req.body); // Bug: undefined - no body parser
  res.json({ received: req.body });
});
```

**Fix**: Add body parser middleware
```javascript
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
```

---

### CORS Middleware Order
**Bug Type**: Middleware
**Difficulty**: Intermediate

```javascript
const cors = require('cors');

app.get('/api/data', (req, res) => {
  res.json({ data: 'value' });
});

app.use(cors()); // Bug: CORS applied after routes
```

**Fix**: Apply CORS before routes
```javascript
app.use(cors());

app.get('/api/data', (req, res) => {
  res.json({ data: 'value' });
});
```

---

## Async/Promise Handling

### Missing Await
**Bug Type**: Async Issue
**Difficulty**: Intermediate

```javascript
app.get('/api/users', async (req, res) => {
  const users = getUsersFromDB(); // Bug: Missing await
  res.json(users); // Sends Promise object instead of data
});
```

**Fix**: Add await
```javascript
app.get('/api/users', async (req, res) => {
  const users = await getUsersFromDB();
  res.json(users);
});
```

---

### Unhandled Promise Rejection
**Bug Type**: Async Issue
**Difficulty**: Advanced

```javascript
app.get('/api/users/:id', async (req, res) => {
  const user = await getUserById(req.params.id); // Bug: No error handling
  res.json(user);
});
```

**Fix**: Add try-catch
```javascript
app.get('/api/users/:id', async (req, res) => {
  try {
    const user = await getUserById(req.params.id);
    res.json(user);
  } catch (error) {
    console.error('Error fetching user:', error);
    res.status(500).json({ error: 'Failed to fetch user' });
  }
});
```

---

### Promise Chain Not Returned
**Bug Type**: Async Issue
**Difficulty**: Intermediate

```javascript
app.post('/api/users', (req, res) => {
  createUser(req.body)
    .then(user => {
      res.json(user);
    }); // Bug: Promise not caught - unhandled rejection on error

  // Or alternatively:
  // Bug: Sending response before async operation completes
  res.status(201).send();
});
```

**Fix**: Use async/await or proper promise chain
```javascript
app.post('/api/users', async (req, res) => {
  try {
    const user = await createUser(req.body);
    res.status(201).json(user);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

---

## Request/Response Bugs

### Multiple Responses Sent
**Bug Type**: Logic Error
**Difficulty**: Intermediate

```javascript
app.get('/api/users/:id', async (req, res) => {
  try {
    const user = await getUserById(req.params.id);
    res.json(user);
  } catch (error) {
    res.status(404).json({ error: 'User not found' });
  }

  res.status(200).send(); // Bug: Headers already sent
});
```

**Fix**: Return after sending response
```javascript
app.get('/api/users/:id', async (req, res) => {
  try {
    const user = await getUserById(req.params.id);
    return res.json(user);
  } catch (error) {
    return res.status(404).json({ error: 'User not found' });
  }
});
```

---

### Wrong Status Code
**Bug Type**: Logic Error
**Difficulty**: Beginner

```javascript
app.post('/api/users', (req, res) => {
  const user = createUser(req.body);
  res.json(user); // Bug: Should be 201 Created, not 200
});

app.delete('/api/users/:id', (req, res) => {
  deleteUser(req.params.id);
  res.json({ success: true }); // Bug: Should be 204 No Content
});
```

**Fix**: Use correct status codes
```javascript
app.post('/api/users', (req, res) => {
  const user = createUser(req.body);
  res.status(201).json(user);
});

app.delete('/api/users/:id', (req, res) => {
  deleteUser(req.params.id);
  res.status(204).send();
});
```

---

## Error Handling

### Missing Error Middleware
**Bug Type**: Error Handling
**Difficulty**: Intermediate

```javascript
app.get('/api/data', async (req, res) => {
  const data = await fetchData(); // May throw error
  res.json(data);
});

// Bug: No error handling middleware - errors crash server
app.listen(3000);
```

**Fix**: Add error handling middleware
```javascript
app.get('/api/data', async (req, res, next) => {
  try {
    const data = await fetchData();
    res.json(data);
  } catch (error) {
    next(error); // Pass to error handler
  }
});

// Error handling middleware (must be last)
app.use((err, req, res, next) => {
  console.error('Error:', err);
  res.status(500).json({ error: 'Internal server error' });
});

app.listen(3000);
```

---

### Wrong Error Middleware Signature
**Bug Type**: Error Handling
**Difficulty**: Intermediate

```javascript
// Bug: Missing 'err' parameter - not recognized as error handler
app.use((req, res, next) => {
  console.error('Error handler');
  res.status(500).json({ error: 'Something went wrong' });
});
```

**Fix**: Include all 4 parameters
```javascript
app.use((err, req, res, next) => {
  console.error('Error:', err);
  res.status(500).json({ error: 'Something went wrong' });
});
```

---

## Database Query Issues

### SQL Injection Vulnerability
**Bug Type**: Security
**Difficulty**: Advanced

```javascript
app.get('/api/users/:id', (req, res) => {
  const query = `SELECT * FROM users WHERE id = ${req.params.id}`;
  // Bug: SQL injection vulnerability
  db.query(query, (err, results) => {
    res.json(results);
  });
});
```

**Fix**: Use parameterized queries
```javascript
app.get('/api/users/:id', (req, res) => {
  const query = 'SELECT * FROM users WHERE id = ?';
  db.query(query, [req.params.id], (err, results) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(results);
  });
});
```

---

### Missing Input Validation
**Bug Type**: Validation
**Difficulty**: Intermediate

```javascript
app.post('/api/users', (req, res) => {
  const user = createUser(req.body); // Bug: No validation
  res.status(201).json(user);
});
```

**Fix**: Add validation
```javascript
app.post('/api/users', (req, res) => {
  const { name, email } = req.body;

  if (!name || !email) {
    return res.status(400).json({ error: 'Name and email required' });
  }

  if (!email.includes('@')) {
    return res.status(400).json({ error: 'Invalid email' });
  }

  const user = createUser({ name, email });
  res.status(201).json(user);
});
```

---

### Callback Not Handling Errors
**Bug Type**: Async Issue
**Difficulty**: Beginner

```javascript
app.get('/api/data', (req, res) => {
  fs.readFile('data.json', 'utf8', (err, data) => {
    // Bug: Not checking err
    res.json(JSON.parse(data));
  });
});
```

**Fix**: Check error first
```javascript
app.get('/api/data', (req, res) => {
  fs.readFile('data.json', 'utf8', (err, data) => {
    if (err) {
      console.error('File read error:', err);
      return res.status(500).json({ error: 'Failed to read data' });
    }
    res.json(JSON.parse(data));
  });
});
```
