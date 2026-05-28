---
name: modern-javascript-patterns
description: Use this skill when you want to master ES6+ features and functional programming patterns for writing clean, efficient JavaScript code, especially when refactoring legacy code or optimizing applications.
---

# Skill body

## Overview

Master ES6+ features including async/await, destructuring, spread operators, arrow functions, promises, modules, iterators, generators, and functional programming patterns for writing clean, efficient JavaScript code.

## When to Use This Skill

- Refactoring legacy JavaScript to modern syntax
- Implementing functional programming patterns
- Optimizing JavaScript performance
- Writing maintainable and readable code
- Working with asynchronous operations
- Building modern web applications
- Migrating from callbacks to Promises/async-await
- Implementing data transformation pipelines

## ES6+ Core Features

### 1. Arrow Functions

**Syntax and Use Cases:**

```javascript
// Traditional function
function add(a, b) {
  return a + b;
}

// Arrow function
const add = (a, b) => a + b;

// Single parameter (parentheses optional)
const double = x => x * 2;

// No parameters
const getRandom = () => Math.random();

// Multiple statements (need curly braces)
const processUser = user => {
  const normalized = user.name.toLowerCase();
  return { ...user, name: normalized };
};

// Returning objects (wrap in parentheses)
const createUser = (name, age) => ({ name, age });
```

**Lexical 'this' Binding:**

```javascript
class Counter {
  constructor() {
    this.count = 0;
  }

  // Arrow function preserves 'this' context
  increment = () => {
    this.count++;
  };

  // Traditional function loses 'this' in callbacks
  incrementTraditional() {
    setTimeout(function () {
      this.count++; // 'this' is undefined
    }, 1000);
  }

  // Arrow function maintains 'this'
  incrementArrow() {
    setTimeout(() => {
      this.count++; // 'this' refers to Counter instance
    }, 1000);
  }
}
```

### 2. Destructuring

**Object Destructuring:**

```javascript
const user = {
  id: 1,
  name: 'John Doe',
  email: 'john@example.com',
  address: {
    city: 'New York',
    country: 'USA',
  },
};

// Basic destructuring
const { name, email } = user;

// Rename variables
const { name: userName, email: userEmail } = user;

// Default values
const { age = 25 } = user;

// Nested destructuring
const {
  address: { city, country },
} = user;
```

**Array Destructuring:**

```javascript
const numbers = [1, 2, 3, 4, 5];

// Basic destructuring
const [first, second] = numbers;

// Skip elements
const [, , third] = numbers;

// Rest parameters
const [head, ...tail] = numbers; // head is 1, tail is [2, 3, 4, 5]
```

### 3. Spread & Rest

```javascript
// Spread arrays
const combined = [...arr1, ...arr2];
const copy = [...arr1];

// Spread objects
const settings = { ...defaults, ...userPrefs };
const newObj = { ...user, age: 31 };

// Rest parameters
function sum(...numbers) {
  return numbers.reduce((total, n) => total + n, 0);
}
```

### 4. Async/Await

```javascript
// Basic usage
async function fetchUser(id) {
  try {
    const response = await fetch(`/api/users/${id}`);
    return await response.json();
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}

// Parallel execution
const fetchUsers = async (ids) => {
  const users = await Promise.all(ids.map(id => fetchUser(id)));
  return users;
};
```