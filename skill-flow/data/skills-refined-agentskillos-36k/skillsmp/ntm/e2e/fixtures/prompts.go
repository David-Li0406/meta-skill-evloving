// Package fixtures contains test data for E2E tests.
package fixtures

// PromptCodeGeneration is a prompt that triggers code generation output.
const PromptCodeGeneration = `Write a Go function that calculates the Fibonacci sequence recursively.
Include detailed comments explaining each step. Also add a memoization optimization version.`

// PromptSubstantialWork is a prompt that triggers substantial agent work.
const PromptSubstantialWork = `Create a complete REST API server in Go with CRUD operations for a blog system.
Include:
- Models (Blog, Post, Comment)
- Handlers with proper error handling
- Middleware for logging and authentication
- Routes with proper HTTP methods
- Detailed comments throughout the code`

// PromptSimple is a simple prompt for quick responses.
const PromptSimple = "What is 2+2?"

// PromptExploreCodebase is a prompt that causes agents to explore files.
const PromptExploreCodebase = "Explore the current directory and list all Go files with a brief description of each."

// PromptLongRunning is a prompt designed to keep agents busy longer.
const PromptLongRunning = `Implement a complete web scraper in Go that:
1. Takes a URL as input
2. Fetches the page content
3. Extracts all links from the page
4. Follows links up to 2 levels deep
5. Stores results in a SQLite database
6. Includes rate limiting and politeness features
7. Has comprehensive error handling
8. Includes unit tests
Please implement this step by step with detailed explanations.`

// PromptRefactor is a prompt that triggers refactoring work.
const PromptRefactor = `Review the code in the current directory and suggest refactoring improvements.
Focus on:
- Code duplication
- Function complexity
- Naming conventions
- Error handling patterns
Provide specific examples with before/after code.`
