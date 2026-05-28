---
name: backend-core
description: Generate backend routes, handle requests and responses, and connect applications to databases. Use for API and server-side development.
---

# Backend Core Skill

## Instructions

1. **Routing**
   - Create RESTful routes (GET, POST, PUT, DELETE)
   - Organize routes by feature/module
   - Use clear and meaningful endpoint names

2. **Request & Response Handling**
   - Validate incoming request data
   - Handle headers, params, body, and query
   - Send proper HTTP status codes and JSON responses

3. **Database Connection**
   - Connect to databases (MongoDB, PostgreSQL, MySQL)
   - Use ORM/ODM when needed
   - Handle connection errors safely

4. **Business Logic**
   - Separate logic from routes (controllers/services)
   - Keep code clean and reusable
   - Handle async operations properly

## Best Practices
- Follow MVC or service-based architecture
- Always validate and sanitize user input
- Use environment variables for secrets
- Handle errors with try/catch or middleware
- Keep APIs consistent and predictable

## Example Structure
```js
// routes/user.routes.js
import express from "express";
import { createUser, getUsers } from "../controllers/user.controller.js";

const router = express.Router();

router.post("/users", createUser);
router.get("/users", getUsers);

export default router;
