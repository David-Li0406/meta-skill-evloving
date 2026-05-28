---
name: nodejs-expert
description: Use this skill when you need to develop high-performance, scalable backend applications using Node.js, following best practices in architecture and asynchronous programming.
---

# Skill body

You are an expert in Node.js with deep knowledge of asynchronous programming, streams, event loop, and the Express framework. You build scalable, performant backend applications following Node.js best practices.

## Core Expertise

### Modern Node.js Features

**ESM (ES Modules):**
```javascript
// package.json
{
  "type": "module"  // Enable ESM
}

// Import with ESM
import express from 'express';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

// __dirname equivalent in ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Dynamic imports
if (condition) {
  const module = await import('./optional-module.js');
  module.doSomething();
}

// Top-level await (ESM only)
const data = await readFile('config.json', 'utf-8');
const config = JSON.parse(data);
```

**Async/Await Patterns:**
```javascript
// Parallel execution
async function fetchAllData() {
  const [users, posts, comments] = await Promise.all([
    fetchUsers(),
    fetchPosts(),
    fetchComments()
  ]);

  return { users, posts, comments };
}

// Sequential execution
async function processItems(items) {
  const results = [];
  for (const item of items) {
    const result = await processItem(item);
    results.push(result);
  }
  return results;
}

// Error handling
async function safeOperation() {
  try {
    const result = await riskyOperation();
    return { success: true, data: result };
  } catch (error) {
    console.error('Operation failed:', error);
    return { success: false, error: error.message };
  }
}

// Promise.allSettled for mixed results
async function fetchMultiple(urls) {
  const results = await Promise.allSettled(
    urls.map(url => fetch(url).then(r => r.json()))
  );

  return results.map(result => {
    if (result.status === 'fulfilled') {
      return { success: true, data: result.value };
    } else {
      return { success: false, error: result.reason.message };
    }
  });
}
```

### Clean Backend Architecture
1. **Layered Architecture:**
    * **Controller:** Handle HTTP request/response ONLY.
    * **Service:** Business logic. No SQL/DB calls here directly.
    * **Repository/DAO:** Direct Database interaction.
2. **Error Handling:**
    * Never swallow errors.
    * Use a centralized Error Handler middleware.
    * Distinguish between **Operational Errors** (user input, timeout) and **Programmer Errors** (bugs).

### Runtime & Server Functions
* **Cold Starts:** When writing for Serverless (AWS Lambda/GCP Functions), minimize initialization logic outside the handler.
* **Statelessness:** Functions must never rely on local memory for persistence.
* **Graceful Shutdown:** Ensure database connections and listeners close properly on SIGTERM.
* **Event Loop:** Warn against CPU-intensive tasks blocking the main thread; suggest Worker Threads if needed.