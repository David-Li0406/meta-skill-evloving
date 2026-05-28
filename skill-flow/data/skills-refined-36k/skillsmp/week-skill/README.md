# WEEEK API Toolkit

A powerful toolkit for working with the [WEEEK](https://weeek.net) project management platform. Includes a convenient CLI utility and a Node.js library for integration.

## 🚀 Installation

### Option 1: Install directly from GitHub (for CLI usage)
To make the `weeek` command available globally on your system:

```bash
npm install -g github:slonikmak/week-skill
```

### Option 2: For Development
1. Clone the repository:
   ```bash
   git clone https://github.com/slonikmak/week-skill.git
   cd week-skill
   ```
2. Install dependencies and link:
   ```bash
   npm install
   npm link
   ```
Now the `weeek` command is available in your terminal.

## ⚙️ Configuration

The tool requires an API Key to function.
1. Generate a token in your WEEEK account settings.
2. Create a `.env` file in the project root (or wherever you run the script) or export an environment variable:

```env
WEEEK_API_KEY=your_token_here
```

## 🖥️ CLI Usage

After installation, use the `weeek` command.

### 🧠 Smart Actions (High-Level)

#### 📋 View Board
Finds a board by name (fuzzy match) and displays columns with tasks.
```bash
weeek board "Release 2.0"
```

#### 🆕 Create Task
Creates a task by automatically resolving Board ID, Column ID, and Assignee ID.
```bash
weeek create "Fix login bug" --board "Release" --col "Backlog" --prio 2 --assignee "Ivan"
```

#### 👁️ Show Task Details
Shows task details: description (HTML stripped), priority, status, and subtasks.
```bash
weeek show 893
```

#### 🚚 Move Task
Moves a task to another column (by column name).
```bash
weeek move 893 "Done"
```

#### 👥 Users & Assignment
Work with your team using names instead of UUIDs.
```bash
# List all workspace users
weeek users

# Assign a user (search by name/email)
weeek assign 893 "Maxim"
```

#### ⏱️ Timer
Manage time tracking.
```bash
weeek timer start 893
weeek timer stop 893
```

---

### 🔧 Low-Level Commands (API Explorer)
Direct access to the API for debugging or specific queries.

```bash
# List all available API tags
weeek tags

# List endpoints for a tag
weeek endpoints Task

# Raw request (GET)
weeek run GET tm/projects

# Raw request with parameters
weeek run GET tm/tasks -p "projectId=123"
```

---

## 📦 Using as a Library

You can use `WeeekClient` in your own Node.js scripts.

1. Install the package in your project:
   ```bash
   npm install github:slonikmak/week-skill
   ```

2. Import and use:

```javascript
import { WeeekClient } from 'week-skill';

const client = new WeeekClient('your_token_here');

async function main() {
    // Get all projects
    const projects = await client.getProjects();
    console.log(projects);

    // Find board by name
    const boards = await client.findBoard('Release');
    
    // Create a task
    const newTask = await client.createTask({
        title: 'New task from script',
        boardId: boards[0].id,
        priority: 1
    });
}

main();
```

## Requirements
- Node.js >= 16
- `weeek_spec.json` (OpenAPI specification) must be present in the package (included in the repo).
