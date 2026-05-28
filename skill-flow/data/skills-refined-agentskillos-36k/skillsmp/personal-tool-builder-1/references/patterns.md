# Personal Tool Builder

## Patterns


---
  #### **Name**
Scratch Your Own Itch
  #### **Description**
Building from personal pain points
  #### **When To Use**
When starting any personal tool
  #### **Implementation**
    ## The Itch-to-Tool Process
    
    ### Identifying Real Itches
    ```
    Good itches:
    - "I do this manually 10x per day"
    - "This takes me 30 minutes every time"
    - "I wish X just did Y"
    - "Why doesn't this exist?"
    
    Bad itches (usually):
    - "People should want this"
    - "This would be cool"
    - "There's a market for..."
    - "AI could probably..."
    ```
    
    ### The 10-Minute Test
    | Question | Answer |
    |----------|--------|
    | Can you describe the problem in one sentence? | Required |
    | Do you experience this problem weekly? | Must be yes |
    | Have you tried solving it manually? | Must have |
    | Would you use this daily? | Should be yes |
    
    ### Start Ugly
    ```
    Day 1: Script that solves YOUR problem
    - No UI, just works
    - Hardcoded paths, your data
    - Zero error handling
    - You understand every line
    
    Week 1: Script that works reliably
    - Handle your edge cases
    - Add the features YOU need
    - Still ugly, but robust
    
    Month 1: Tool that might help others
    - Basic docs (for future you)
    - Config instead of hardcoding
    - Consider sharing
    ```
    

---
  #### **Name**
CLI Tool Architecture
  #### **Description**
Building command-line tools that last
  #### **When To Use**
When building terminal-based tools
  #### **Implementation**
    ## CLI Tool Stack
    
    ### Node.js CLI Stack
    ```javascript
    // package.json
    {
      "name": "my-tool",
      "version": "1.0.0",
      "bin": {
        "mytool": "./bin/cli.js"
      },
      "dependencies": {
        "commander": "^12.0.0",    // Argument parsing
        "chalk": "^5.3.0",          // Colors
        "ora": "^8.0.0",            // Spinners
        "inquirer": "^9.2.0",       // Interactive prompts
        "conf": "^12.0.0"           // Config storage
      }
    }
    
    // bin/cli.js
    #!/usr/bin/env node
    import { Command } from 'commander';
    import chalk from 'chalk';
    
    const program = new Command();
    
    program
      .name('mytool')
      .description('What it does in one line')
      .version('1.0.0');
    
    program
      .command('do-thing')
      .description('Does the thing')
      .option('-v, --verbose', 'Verbose output')
      .action(async (options) => {
        // Your logic here
      });
    
    program.parse();
    ```
    
    ### Python CLI Stack
    ```python
    # Using Click (recommended)
    import click
    
    @click.group()
    def cli():
        """Tool description."""
        pass
    
    @cli.command()
    @click.option('--name', '-n', required=True)
    @click.option('--verbose', '-v', is_flag=True)
    def process(name, verbose):
        """Process something."""
        click.echo(f'Processing {name}')
    
    if __name__ == '__main__':
        cli()
    ```
    
    ### Distribution
    | Method | Complexity | Reach |
    |--------|------------|-------|
    | npm publish | Low | Node devs |
    | pip install | Low | Python devs |
    | Homebrew tap | Medium | Mac users |
    | Binary release | Medium | Everyone |
    | Docker image | Medium | Tech users |
    

---
  #### **Name**
Local-First Apps
  #### **Description**
Apps that work offline and own your data
  #### **When To Use**
When building personal productivity apps
  #### **Implementation**
    ## Local-First Architecture
    
    ### Why Local-First for Personal Tools
    ```
    Benefits:
    - Works offline
    - Your data stays yours
    - No server costs
    - Instant, no latency
    - Works forever (no shutdown)
    
    Trade-offs:
    - Sync is hard
    - No collaboration (initially)
    - Platform-specific work
    ```
    
    ### Stack Options
    | Stack | Best For | Complexity |
    |-------|----------|------------|
    | Electron + SQLite | Desktop apps | Medium |
    | Tauri + SQLite | Lightweight desktop | Medium |
    | Browser + IndexedDB | Web apps | Low |
    | PWA + OPFS | Mobile-friendly | Low |
    | CLI + JSON files | Scripts | Very Low |
    
    ### Simple Local Storage
    ```javascript
    // For simple tools: JSON file storage
    import { readFileSync, writeFileSync, existsSync } from 'fs';
    import { homedir } from 'os';
    import { join } from 'path';
    
    const DATA_DIR = join(homedir(), '.mytool');
    const DATA_FILE = join(DATA_DIR, 'data.json');
    
    function loadData() {
      if (!existsSync(DATA_FILE)) return { items: [] };
      return JSON.parse(readFileSync(DATA_FILE, 'utf8'));
    }
    
    function saveData(data) {
      if (!existsSync(DATA_DIR)) mkdirSync(DATA_DIR);
      writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
    }
    ```
    
    ### SQLite for More Complex Tools
    ```javascript
    // better-sqlite3 for Node.js
    import Database from 'better-sqlite3';
    import { join } from 'path';
    import { homedir } from 'os';
    
    const db = new Database(join(homedir(), '.mytool', 'data.db'));
    
    // Create tables on first run
    db.exec(`
      CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `);
    
    // Fast synchronous queries
    const items = db.prepare('SELECT * FROM items').all();
    ```
    

---
  #### **Name**
Script to Product Evolution
  #### **Description**
Growing a script into a real product
  #### **When To Use**
When a personal tool shows promise
  #### **Implementation**
    ## Evolution Path
    
    ### Stage 1: Personal Script
    ```
    Characteristics:
    - Only you use it
    - Hardcoded values
    - No error handling
    - Works on your machine
    
    Time: Hours to days
    ```
    
    ### Stage 2: Shareable Tool
    ```
    Add:
    - README explaining what it does
    - Basic error messages
    - Config file instead of hardcoding
    - Works on similar machines
    
    Time: Days
    ```
    
    ### Stage 3: Public Tool
    ```
    Add:
    - Installation instructions
    - Cross-platform support
    - Proper error handling
    - Version numbers
    - Basic tests
    
    Time: Week or two
    ```
    
    ### Stage 4: Product
    ```
    Add:
    - Landing page
    - Documentation site
    - User support channel
    - Analytics (privacy-respecting)
    - Payment integration (if monetizing)
    
    Time: Weeks to months
    ```
    
    ### Signs You Should Productize
    | Signal | Strength |
    |--------|----------|
    | Others asking for it | Strong |
    | You use it daily | Strong |
    | Solves $100+ problem | Strong |
    | Others would pay | Very strong |
    | Competition exists but sucks | Strong |
    | You're embarrassed by it | Actually good |
    

## Anti-Patterns


---
  #### **Name**
Building for Imaginary Users
  #### **Description**
Creating tools for problems you don't have
  #### **Why Bad**
    No real feedback loop.
    Building features no one needs.
    Giving up because no motivation.
    Solving the wrong problem.
    
  #### **What To Do Instead**
    Build for yourself first.
    Real problem = real motivation.
    You're the first tester.
    Expand users later.
    

---
  #### **Name**
Over-Engineering Personal Tools
  #### **Description**
Adding unnecessary complexity to personal scripts
  #### **Why Bad**
    Takes forever to build.
    Harder to modify later.
    Complexity kills motivation.
    Perfect is enemy of done.
    
  #### **What To Do Instead**
    Minimum viable script.
    Add complexity when needed.
    Refactor only when it hurts.
    Ugly but working > pretty but incomplete.
    

---
  #### **Name**
Not Dogfooding
  #### **Description**
Building tools you don't use yourself
  #### **Why Bad**
    Missing obvious UX issues.
    Not finding real bugs.
    Features that don't help.
    No passion for improvement.
    
  #### **What To Do Instead**
    Use your tool daily.
    Feel the pain of bad UX.
    Fix what annoys YOU.
    Your needs = user needs.
    

---
  #### **Name**
Premature Monetization
  #### **Description**
Trying to charge before the tool is proven
  #### **Why Bad**
    Pressure kills exploration.
    Wrong incentives.
    Optimize for payment, not utility.
    Users before revenue.
    
  #### **What To Do Instead**
    Free while you dogfood.
    Prove value to yourself first.
    Monetize when others beg for it.
    Revenue is validation, not goal.
    