---
name: debugging-practice-generator
description: Generate React and Express debugging practice projects with intentional bugs for student learning. Use when the user requests to create debugging exercises, practice projects with bugs, student coding challenges, or educational debugging scenarios. Supports custom bug specifications, difficulty levels, and project types (React, Express, or full-stack). Always creates proper project structure with .gitignore files (especially for Express projects to ignore node_modules).
---

# Debugging Practice Generator

Generate educational React and Express projects with intentional bugs for debugging practice. This skill helps create realistic coding scenarios that teach students to use console.log effectively and develop systematic debugging skills.

## Core Workflow

### 1. Understand the Requirements

Ask the user or review their plan for:
- **Project type**: React, Express, or full-stack
- **Difficulty level**: Beginner (1-2 obvious bugs), Intermediate (3-5 bugs), Advanced (5+ complex bugs)
- **Bug types**: State management, async issues, routing, middleware, etc.
- **Learning objectives**: What debugging concepts should students practice?

### 2. Select Bug Patterns

Based on requirements, choose appropriate bugs from reference files:
- See [references/react_bug_patterns.md](references/react_bug_patterns.md) for React bugs
- See [references/express_bug_patterns.md](references/express_bug_patterns.md) for Express bugs

**Bug selection principles:**
- Mix difficulty levels appropriately (more easy bugs for beginners)
- Include bugs that benefit from console.log debugging
- Avoid syntax errors that prevent code from running (unless that's the lesson)
- Ensure bugs are realistic and educational
- Consider bug interactions for advanced projects

### 3. Generate Project Structure

Follow patterns from [references/project_setup.md](references/project_setup.md).

**React Project:**
```bash
npm create vite@latest [project-name] -- --template react
cd [project-name]
npm install
```

**Express Project:**
```bash
mkdir [project-name]
cd [project-name]
npm init -y
npm install express
npm install --save-dev nodemon
```

**CRITICAL for Express: Create .gitignore**
Always create a `.gitignore` file that includes:
```
node_modules/
.env
.env.local
*.log
.DS_Store
```

### 4. Implement Bugs Intentionally

Insert bugs into the generated project files:

**For React (`src/App.jsx` or component files):**
- Implement missing useState hooks
- Add stale closure bugs in effects
- Include missing dependency arrays
- Create event handler invocation issues
- Add conditional rendering problems

**For Express (`server.js` or route files):**
- Implement missing middleware (body-parser, CORS)
- Add route ordering issues
- Include missing error handling
- Create async/await bugs
- Add response handling problems

**Best practices:**
- Make bugs discoverable but not obvious
- Add comments like `// TODO: Debug this function` as hints
- Ensure the app runs (even if buggy) so students can test it
- Include console.log opportunities throughout

### 5. Create Student Documentation

Generate a `README.md` with:

```markdown
# Debugging Practice: [Project Name]

## Setup
1. Install dependencies: `npm install`
2. Start dev server: `npm run dev` (or `npm start`)

## Your Mission
Find and fix [X] bugs in this project using systematic debugging:
- Use console.log() to inspect values
- Check browser/terminal console for errors
- Test each feature thoroughly
- Trace the flow of data

## Features to Test
- [Feature 1 description]
- [Feature 2 description]
- [Feature 3 description]

## Hints
- [ ] Bug 1 is related to [vague hint]
- [ ] Bug 2 occurs when [vague hint]
- [ ] Bug 3 affects [vague hint]

## Difficulty: [Level]

Good luck debugging! 🐛
```

**Documentation guidelines:**
- Don't reveal bug solutions
- Provide vague hints about locations
- List features students should test
- Include difficulty level
- Keep instructions encouraging

### 6. Verify Setup

Before delivering to students:

**React checklist:**
- [ ] `npm install` completes successfully
- [ ] `npm run dev` starts without immediate crashes
- [ ] Bugs are present and discoverable
- [ ] Console provides useful error hints

**Express checklist:**
- [ ] `.gitignore` includes `node_modules/`
- [ ] `npm install` completes successfully
- [ ] Server starts (even if buggy)
- [ ] Endpoints can be tested
- [ ] Bugs manifest when testing features

**Full-stack checklist:**
- [ ] Both projects have separate `package.json`
- [ ] CORS is configured (or intentionally broken as a bug)
- [ ] Both `.gitignore` files exist
- [ ] Projects can run independently

## Project Type Patterns

### Beginner React Project Example
**Features:**
- Simple counter with increment/decrement
- Todo list with add/delete
- Basic form with input handling

**Common bugs:**
- Missing `useState` hook
- Incorrect event handler invocation
- Missing key props in lists

### Intermediate Express Project Example
**Features:**
- REST API with CRUD operations
- Basic user authentication
- Data validation

**Common bugs:**
- Missing body parser middleware
- Route ordering issues
- Missing error handling
- Unhandled promise rejections

### Advanced Full-Stack Project Example
**Features:**
- React frontend with API calls
- Express backend with database
- Real-time updates or complex state

**Common bugs:**
- Race conditions in async operations
- CORS configuration issues
- Stale closures in React effects
- Multiple response sends in Express
- Missing dependency cleanup

## Quick Reference: Common Bug Types

### React
- **State bugs**: Missing useState, stale closures, incorrect updates
- **Effect bugs**: Missing dependencies, no cleanup, infinite loops
- **Event bugs**: Incorrect invocation, missing preventDefault
- **Rendering bugs**: Missing keys, incorrect conditional rendering
- **Async bugs**: Race conditions, missing error handling

### Express
- **Routing bugs**: Order matters, missing responses, wrong HTTP methods
- **Middleware bugs**: Missing next(), wrong order, incorrect signatures
- **Async bugs**: Missing await, unhandled rejections, callback errors
- **Response bugs**: Multiple sends, wrong status codes, missing error handling
- **Security bugs**: SQL injection, missing validation, CORS issues

## Tips for Effective Debugging Practice

### Encourage Console Logging
Students should learn to log:
- Function entry points: `console.log('fetchUser called with:', userId)`
- Variable values: `console.log('count before:', count, 'after:', count + 1)`
- Conditional branches: `console.log('Taking true branch')`
- Async results: `console.log('API response:', data)`
- Error catches: `console.error('Error occurred:', error)`

### Progressive Difficulty
- **Beginner**: 1-2 bugs, obvious symptoms, single component/route
- **Intermediate**: 3-5 bugs, some hidden, multiple files
- **Advanced**: 5+ bugs, complex interactions, requires systematic debugging

### Realistic Scenarios
Base projects on real-world features:
- E-commerce cart
- Social media feed
- Todo/task manager
- Blog with comments
- User dashboard
- API integrations

## Resources

This skill includes comprehensive reference documentation:

### references/react_bug_patterns.md
Complete catalog of React bug patterns organized by category (state management, effects, props, rendering, async). Each pattern includes:
- Bug code example
- Difficulty level
- Fix explanation
- Console.log debugging tips

### references/express_bug_patterns.md
Complete catalog of Express bug patterns organized by category (routing, middleware, async, responses, errors, database). Each pattern includes:
- Bug code example
- Difficulty level
- Fix explanation
- Testing approaches

### references/project_setup.md
Detailed setup instructions for:
- React project initialization (Vite)
- Express project initialization
- Full-stack monorepo structure
- Essential dependencies
- .gitignore file templates
- package.json configuration
- Testing checklists

Read these references when:
- Selecting specific bugs to implement
- Setting up project structure
- Choosing appropriate difficulty levels
- Creating comprehensive debugging exercises
