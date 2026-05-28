---
name: Non-Blocking Execution
description: Guidelines for running long-lived processes (servers, watchers) without blocking agent execution.
---

# Non-Blocking Execution Skill

Agents often need to run servers (`npm start`), watchers (`npm run watch`), or long builds. Standard execution blocks the agent until the command finishes—which for a server is **never**.

## 1. The Async Pattern (Preventing the Hang)

**The Problem**: By default, `run_command` waits for the command to finish. For `npm run dev`, this means the agent **hangs forever** and never gets to Step 3.

**The Solution**: You **MUST** use the `WaitMsBeforeAsync` parameter.
- This parameter tells the tool: "Run for X milliseconds, then **detach** and give me back control."
- This is the ONLY way to run a server without killing it or hanging the agent.

### Mandatory Parameters
- **`WaitMsBeforeAsync`**: Set to `2000` (2 seconds).
    - **Effect**: The tool runs the command, waits 2 seconds to catch startup errors, and then **IMMEDIATELY returns** a `CommandId` while the process keeps running in the background.
    - **Result**: You regain control to perform Step 2 & 3.

### Example
```javascript
// ❌ WRONG - The agent will HANG FOREVER here.
// It will never reach the next line of code.
run_command({ CommandLine: "npm run dev" })

// ✅ CORRECT - The agent waits 2 seconds, then wakes up.
// The server stays running in the background.
run_command({ 
    CommandLine: "npm run dev",
    WaitMsBeforeAsync: 2000 
})
```

## 2. The Verification Loop

Async commands return a `CommandId`. You **MUST** verify they are actually running.

1.  **Launch**: Run with `WaitMsBeforeAsync: 2000`.
2.  **Wait**: Sleep/Tokens (implicit in tool usage).
3.  **Check Status**: Use `command_status` with the `CommandId` and `WaitDurationSeconds: 5` (to peek at new output).
    - **Status**: Is it `running`?
    - **Output**: Does it say "Server started on localhost:3000"?
4.  **Confirm**: Only proceed once output confirms success.

## 3. Clean Termination (Ctrl+C)

**Trigger**: You are done testing the server or need to stop a blocking process.
**Tool**: `send_command_input`

- **Action**: `Terminate: true`
- **Why?**: Leaving zombie servers eats resources and blocks ports for future agents.
- **Equivalent**: This is exactly the same as pressing `Ctrl+C` in a terminal.

**Example**:
```javascript
// Stop the server
send_command_input({
    CommandId: "previously-returned-uuid",
    Terminate: true
})
```

## 4. Troubleshooting Blocking Commands

If you accidentally run a blocking command (forgot `WaitMsBeforeAsync`):
1.  You will likely timeout or be stuck.
2.  In the next turn, **IMMEDIATELY** use `send_command_input` with `Terminate: true` on the blocking command if you can identify it, or ask the user to kill it.
3.  **Self-Correction**: Restart the command with `WaitMsBeforeAsync: 2000`.

## 5. Common Blocking Commands (The Block List)

**MANDATORY**: If you see a command in this list OR a compound command containing one of these (e.g., `npm install && npm run dev`), you MUST use `WaitMsBeforeAsync: 2000`.

### Compound Commands (Chains)
- **Rule**: If a command uses `&&`, `;`, or `|` and *any part* of it is a blocking command, the **entire command** is blocking.
- **Example**: `npm install && npm start` -> **BLOCKING**. Use async pattern.
- **Example**: `cd app && python manage.py runserver` -> **BLOCKING**. Use async pattern.

### Web & Node.js
- `npm start`, `npm run start`, `npm run dev`, `npm run watch`, `npm run serve`, `npm run build:watch`
- `yarn start`, `yarn dev`, `yarn watch`
- `pnpm start`, `pnpm dev`
- `npx next dev`, `npx vite`, `npx webpack serve`, `npx nodemon`
- `node --watch`

### Mobile (iOS/Android/Cross-Platform)
- `npx react-native start`, `npx expo start`
- `flutter run`, `flutter drive`
- `./gradlew installDebug`, `./gradlew bootRun`
- `xcodebuild -scheme <Schema> run`
- `adb logcat` (unless piped/limited)

### Backend & Systems
- **Python**: `python manage.py runserver`, `uvicorn`, `flask run`, `celery worker`
- **.NET**: `dotnet watch`, `dotnet run`
- **Java/JVM**: `./gradlew bootRun`, `mvn spring-boot:run`
- **Go**: `go run .`, `air` (live reload)
- **Rust**: `cargo run`, `cargo watch`
- **Ruby**: `rails server`, `bundle exec sidekiq`
- **PHP**: `php artisan serve`, `symfony server:start`

### Infrastructure & Tools
- **Docker**: `docker-compose up` (without `-d`), `docker run` (without `-d` if interactive service)
- **Database Consoles**: `psql`, `mysql`, `mongo` (interactive shells block)
- **Terraform/Cloud**: `terraform apply` (can be long/interactive), `kubectl port-forward`, `kubectl logs -f`
