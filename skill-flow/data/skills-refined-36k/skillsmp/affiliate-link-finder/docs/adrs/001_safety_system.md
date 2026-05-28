# ADR 001: Safety System Architecture

## Context
The application requires a robust safety system to protect users from dangerous supplement interactions (e.g., stimulants + MAOIs) and manage timing conflicts. This system must be trusted, fail-safe, and capable of functioning even when offline (using cached data).

## Decision
We implemented a **domain-centric safety architecture** following the Hexagonal (Ports & Adapters) pattern.

### 1. Domain Entities
- **`SupplementInteraction`**: Represents a known conflict between two supplements. Includes `severity` (Critical, Caution), `description`, `recommendation`, and `scientificReferences`.
- **`SafetyOverride`**: Represents a user's explicit decision to ignore a warning. Logs the `userId`, `interactionId`, `timestamp`, and `userReason`.

### 2. Repositories (Ports)
- **`SafetyRepository`**: Defines the contract for:
  - `getInteraction(id A, id B)`: Checks for conflicts between two items.
  - `logOverride(override)`: Persists user acknowledgement of risks.

### 3. Implementation (Adapters)
- **`FirebaseSafetyRepository`**: Connects to Firestore `interactions` and `safety_overrides` collections.
  - *Future Optimization*: Will implement local SQLite caching for offline safety checks.

### 4. Logic (ViewModels)
- **`SafetyViewModel`**: Orchestrates the safety check process.
  - Subscribes to the user's current stack and `StackBuilder` inputs.
  - Debounces checks to avoid excessive reads.
  - Exposes a unified `interactions` list for UI banners.

## Consequences
### Positive
- **Decoupling**: The UI knows nothing about *how* interactions are checked, just that they exist.
- **Audit Trail**: Every override is strictly logged for liability and safety auditing.
- **Flexibility**: We can swap the backend (e.g., to a local JSON database) without breaking the app.

### Negative
- **Latency**: Real-time checks against Firestore can be slow on poor connections.
  - *Mitigation*: We are loading a "critical subset" of interactions into memory on app start.
- **Data Maintenance**: The interaction database needs regular updates from clinical sources.

## Status
Accepted and Implemented (Phase 2)
