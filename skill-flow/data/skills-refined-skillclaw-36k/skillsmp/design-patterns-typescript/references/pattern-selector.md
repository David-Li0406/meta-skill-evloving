# Design Pattern Catalog (TypeScript)

Use this as the detailed router reference. Each entry includes definition, strong/weak signals, TS notes, and the next skill name.

Quick routing (common symptoms):
| Symptom | Pattern | Next skill |
| --- | --- | --- |
| Third-party or legacy interface mismatch (shape, naming, sync/async, error model) | Adapter | adapter-pattern-typescript |
| Many variants of the same operation; big switch/if to pick an algorithm; want to swap behavior at runtime; add new variant without touching context | Strategy | strategy-pattern-typescript |
| Complex object creation with variants | Factory Method | factory-method-pattern-typescript |
| Need families of related objects | Abstract Factory | abstract-factory-pattern-typescript |
| Need a consistent family of related objects (variant must match across collaborators) | Abstract Factory | abstract-factory-pattern-typescript |
| Telescoping constructors / too many optional params / step-by-step configuration | Builder | builder-pattern-typescript |
| Need fast copies / expensive setup / configuration presets | Prototype | prototype-pattern-typescript |
| RAM pressure from huge numbers of similar objects; lots of duplicated immutable state | Flyweight | flyweight-pattern-typescript |
| Need exactly one shared instance (process-wide) for a resource/config/cache | Singleton | singleton-pattern-typescript |
| Class hierarchy exploding from 2+ independent dimensions (e.g., type × platform, feature × renderer) | Bridge | bridge-pattern-typescript |
| You have a tree of objects (folders/nodes/boxes) and want to apply the same operation uniformly to leaves and groups | Composite | composite-pattern-typescript |
| Need a small, stable API to a complex subsystem/framework (hide setup/order/deps) | Facade | facade-pattern-typescript |
| Need to add optional behaviors/features to an object at runtime without changing its interface (stackable wrappers) | Decorator | decorator-pattern-typescript |
| Need a sequence of handlers/checks where each can handle, transform, or short-circuit (auth, validation, rate limit, cache) | Chain of Responsibility | chain-of-responsibility-pattern-typescript |
| Need to represent actions as objects for queueing/scheduling/retry/logging, or to support undo/redo | Command | command-pattern-typescript |
| Need to traverse a collection (tree/graph/remote pages) without exposing internals; want multiple traversal orders (DFS/BFS) or pause/resume | Iterator | iterator-pattern-typescript |
| Object behavior changes based on internal state; lots of switch/if by state; states/transitions grow over time; want to add states without touching every method | State | state-pattern-typescript |
| Several classes share the same workflow/algorithm skeleton with minor step variations; lots of duplicate code; want to standardize sequence while allowing overrides | Template Method | template-method-pattern-typescript |
| Need undo/rollback: save and restore object state safely without exposing private internals; want snapshots/history | Memento | memento-pattern-typescript |
| Need a drop-in stand-in that controls access to a real service (lazy init, caching, auth, logging) without changing clients | Proxy | proxy-pattern-typescript |
| Need many listeners to react to events/state changes; subscribers come/go at runtime; avoid coupling producer to consumers | Observer | observer-pattern-typescript |
| Many components talk to each other directly (UI widgets/services), changes ripple everywhere; want central coordination to reduce coupling | Mediator | mediator-pattern-typescript |
| You need to add multiple operations across a stable class hierarchy/object structure (AST/Shapes/Graph nodes) without modifying those classes; want to group operation variants per element type | Visitor | visitor-pattern-typescript |

Common confusions (quick disambiguation):
- Factory Method vs Abstract Factory: Factory Method selects one product; Abstract Factory selects a family of related products.
- Factory Method vs Builder: Factory Method picks which product to create; Builder assembles one product step-by-step.
- Decorator vs Proxy: Decorator adds behavior while keeping the same interface; Proxy controls access or lifecycle to the underlying object.
- Adapter vs Facade: Adapter translates one interface to another; Facade simplifies a subsystem behind a new, usually smaller API.
- Abstract Factory vs DI container module binding: Use Abstract Factory when you must guarantee compatible families; DI modules wire variants but do not enforce family completeness by themselves.
- Builder vs plain object config + validation: Use Builder when construction order/steps matter; stop at config objects if validation alone solves it.
- Prototype vs Memento: Prototype copies an object (often for new instances); Memento captures/restores prior state of the same instance.
- Flyweight vs cache: Flyweight shares intrinsic state across many objects; caches may store whole objects/results and don’t require state-splitting.
- Singleton vs DI singleton-scope: both create one instance, but DI keeps dependencies explicit and testable.
- Bridge vs Strategy: Bridge separates two axes that both vary; Strategy swaps one algorithm/behavior behind a stable abstraction.
- Composite vs Decorator: Composite represents part-whole trees (many children); Decorator wraps a single object to add behavior.
- Decorator vs Adapter: Decorator keeps the same interface and adds behavior; Adapter changes the interface to fit a target.
- Facade vs Adapter: Facade simplifies a subsystem behind a new API; Adapter translates one interface into another.
- Proxy vs Decorator: Proxy controls access/lifecycle of the same service interface; Decorator composes extra behavior but clients typically assemble the stack.
- CoR vs middleware: both form a pipeline, but CoR commonly lets a handler stop propagation entirely or “handle-or-pass” without requiring a fixed framework.
- Command vs Event: a Command requests an action (often one handler), while an Event reports something happened (often many listeners).
- Iterator vs Generator: a generator is one way to implement an iterator; Iterator is the abstraction that hides traversal and representation.
- State vs Strategy: Strategy swaps algorithms chosen by the client; State swaps behavior based on the context's internal state and can trigger transitions.
- Strategy vs State: Strategy is selected externally to choose an algorithm; State changes internally as the object moves through lifecycle states.
- Template Method vs Strategy: Template Method varies steps via inheritance (static per subclass); Strategy swaps algorithms via composition (runtime).
- Visitor vs pattern-matching/switch: Visitor centralizes operations per algorithm and uses `accept` for double dispatch; switches centralize per element type and grow with each new operation.
- Mediator vs Observer: Mediator centralizes coordination logic; Observer broadcasts events to subscribers without owning the collaboration rules.
- Observer vs Pub/Sub: Observer typically links subscribers to a specific publisher instance; Pub/Sub routes via a broker/topic decoupling publishers and subscribers further.
- Memento vs Event Sourcing: Memento stores state snapshots for rollback; event sourcing stores domain events and replays to rebuild state.

## Creational patterns

Category definition:
- Solve object creation complexity and decouple construction from use.
- Manage variants or families while keeping callers stable.
- Improve testability by swapping implementations or factories.
- Common in Node services, frontend factories, and DI container wiring.
- Avoid when constructors are simple and stable.

### Factory Method

Definition: Let subclasses or modules decide which concrete product to instantiate via a common creator.
Strong signals:
- Many `new` scattered with slight variations.
- Need to add new concrete types without changing callers.
- Base workflow creates objects but defers the concrete choice.
- Adding a new variant currently requires changing many call sites or switch statements.
- You want downstream users to extend your library/framework by overriding creation.
Weak/avoid signals:
- Single constructor or small switch is stable.
- No expected variation in product types.
TypeScript notes:
- Model creators with interfaces and generics.
- Module-level factory functions are often enough.
- Keep product interfaces narrow.
- In TypeScript, prefer DI bindings / registry maps / function factories over subclassing unless you already have an inheritance hierarchy.
Next skill: factory-method-pattern-typescript

### Abstract Factory

Definition: Provide an interface for creating families of related objects without specifying concrete classes.
Strong signals:
- Need consistent variants (e.g., AWS vs GCP clients) across a module.
- UI or service layers swap sets of collaborators together.
- Enforce compatibility among created objects.
- You must guarantee that created collaborators are compatible (same variant).
- Switching a variant should be a single configuration change, not many conditionals.
Weak/avoid signals:
- Only one family exists or unlikely to change.
- Objects can be chosen independently.
- Only one product type exists (you don’t have a “family”).
TypeScript notes:
- Define product family interfaces and factory interface.
- Use DI to bind a family per environment.
- Discriminated unions can model variants.
- In TypeScript, Abstract Factory is often implemented as an object with creation functions (or DI provider group), not necessarily a class hierarchy.
Next skill: abstract-factory-pattern-typescript

### Builder

Definition: Separate complex construction from representation using a stepwise builder.
Strong signals:
- Many optional fields or conditional parts.
- Validation or staged defaults are required.
- Fluent API helps assemble complex configs.
- The product has many optional/conditional parts and construction order matters.
- You need multiple representations from the same construction steps (e.g., product + manual).
Weak/avoid signals:
- Object literal or constructor is simple.
- Construction is trivial and fixed.
- A simple object literal (or single config type) is enough and stays stable.
TypeScript notes:
- Builder holds mutable draft; product is immutable.
- Use readonly types for final object.
- Generic builders preserve type safety.
- Prefer fluent builders over telescoping constructors; keep the final product immutable and the builder mutable.
Next skill: builder-pattern-typescript

### Prototype

Definition: Create new objects by cloning an existing instance instead of constructing from scratch.
Strong signals:
- Expensive setup repeated many times.
- Need many variants derived from a base template.
- Runtime templates drive instantiation.
- You repeatedly create similar objects from a baseline template/preset.
- Construction is expensive or involves many fields that you don’t want to re-initialize manually.
Weak/avoid signals:
- Deep clone is complex or risky.
- Construction cost is trivial.
- Cloning is ambiguous (deep vs shallow) or objects hold external resources/circular refs you can’t safely copy.
TypeScript notes:
- Prefer explicit `clone()` methods.
- Be clear about shallow vs deep copies.
- Avoid JSON cloning for class instances.
- Prefer explicit `clone()` methods (or copy constructors) over ad-hoc spreading; be clear about shallow vs deep copy.
- Avoid JSON-based cloning for class instances; it drops prototypes, Dates, Maps/Sets, and methods.
Next skill: prototype-pattern-typescript

### Singleton

Definition: Ensure a class has a single instance with a global access point.
Strong signals:
- Process-wide shared resource is required.
- Central coordination of state is necessary.
- You truly need exactly one process-wide instance (e.g., cache, metrics registry, config snapshot).
- You must prevent multiple initializations of an expensive shared resource.
Weak/avoid signals:
- Hides dependencies and hurts tests.
- DI scope can handle it cleanly.
- The “singleton” would hide dependencies or create global mutable state that makes testing/debugging harder.
TypeScript notes:
- Module-level singletons are simplest in Node.
- Prefer DI container scopes when available.
- Keep shared state minimal and observable.
- In Node/TS, a module-level exported instance is the simplest singleton; prefer DI container single-instance scope where available.
- Avoid singletons for domain logic; keep them for infrastructure (config, telemetry, caches) and make state observable.
Next skill: singleton-pattern-typescript

## Structural patterns

Category definition:
- Solve composition and wrapper concerns, keeping interfaces stable.
- Simplify boundaries between subsystems and modules.
- Improve memory/performance through shared structure or indirection.
- Common in SDK wrappers, HTTP clients, caching/logging layers, and UI trees.
- Avoid when extra layers obscure ownership or debugging.

### Adapter

Definition: Convert one interface into another expected by clients.
Strong signals:
- You can’t change the upstream/downstream API (3rd-party SDK, legacy module, generated client).
- Callers need a stable internal interface while the external API evolves.
- You must translate data shape, naming, sync/async style, or error semantics at a boundary.
Weak/avoid signals:
- You own both sides and can refactor the interface directly (no boundary needed).
- The “adapter” would become a grab-bag of business rules instead of thin translation.
TypeScript notes:
- Prefer composition: implement your internal interface and wrap the external client.
- Keep mapping functions pure and unit-test them separately from I/O.
- Model error translation explicitly (e.g., Result/Either, typed errors), don’t leak SDK exceptions.
Next skill: adapter-pattern-typescript

### Bridge

Definition: Separate abstraction from implementation so both can vary independently.
Strong signals:
- You have two orthogonal dimensions that both need independent extension (e.g., shape × color, UI × platform, domain × storage).
- Adding variants currently forces a cross-product of subclasses or big conditional matrices.
- You want to swap implementations at runtime without changing high-level logic.
Weak/avoid signals:
- Only one dimension varies; Strategy or simple composition is enough.
- The abstraction and implementation are tightly coupled and cannot be meaningfully separated.
TypeScript notes:
- Model the “implementation” as an interface (port) and inject it into the “abstraction”.
- Keep the abstraction’s API stable; add new implementations without touching abstraction code.
- Don’t over-engineer: if there’s no cross-product pressure, keep it simpler.
Next skill: bridge-pattern-typescript

### Composite

Definition: Compose objects into tree structures and treat them uniformly.
Strong signals:
- Your domain model is naturally tree-shaped (e.g., folders, UI component tree, BOM, org chart) with arbitrary nesting.
- Client code should treat single items and groups uniformly via one interface.
- Operations should traverse recursively without type checks or “if leaf vs container” branching.
Weak/avoid signals:
- The structure is not a tree (graph/mesh/shared nodes) or cycles are common; Composite alone won’t fit.
- Leaves and containers share too little behavior, forcing a vague interface that hurts clarity.
TypeScript notes:
- Model a small Component interface (e.g., total(), render(), walk()) implemented by leaves and composites.
- Keep child management out of the Component interface if it pollutes leaves; consider narrowing it to Composite only.
- For traversal-heavy use, add iterator/walk methods to avoid exposing internal arrays everywhere.
Composite vs Visitor: Composite structures the tree; Visitor adds new operations over the tree without changing node classes.
Next skill: composite-pattern-typescript

### Decorator

Definition: Add responsibilities dynamically by wrapping an object.
Strong signals:
- You need to add responsibilities dynamically (logging, metrics, caching, validation, retries) without subclass explosions.
- Multiple behaviors should be combinable (stacked) in different orders/configurations.
- Client code must keep calling the same interface regardless of added behaviors.
Weak/avoid signals:
- You only need one fixed variant; a simple wrapper or composition in the client may be enough.
- Behavior depends heavily on wrapper order and becomes hard to reason about/debug.
TypeScript notes:
- Model a small interface and implement wrappers that delegate then add behavior (before/after).
- Keep wrappers side-effect transparent where possible; document order dependence when it’s not.
- For Node services, decorators are great for cross-cutting concerns around a port (e.g., HttpClient, Repository).
Decorator vs Proxy: both wrap, but Proxy controls access/lifecycle (lazy load, auth, remote), while Decorator adds features.
Decorator vs Chain of Responsibility: CoR handlers may stop the chain; Decorators should preserve the call flow and interface.
Next skill: decorator-pattern-typescript

### Facade

Definition: Provide a simplified interface to a complex subsystem.
Strong signals:
- Client code is getting coupled to many classes and call-order rules in a subsystem/framework.
- You repeatedly write the same initialization/wiring/ordering boilerplate in multiple places.
- You want one “entrypoint” per subsystem boundary with a small, stable surface area.
Weak/avoid signals:
- You only need to change a single incompatible interface (use Adapter instead).
- The facade would become a dumping ground (“god object”) spanning unrelated concerns.
TypeScript notes:
- Keep facades narrow: one facade per bounded subsystem; split into multiple facades if scope grows.
- Hide sequencing and resource lifecycle behind the facade; expose typed methods with clear inputs/outputs.
- Prefer injecting subsystem dependencies into the facade (DI) so it stays testable.
Facade vs Mediator: Facade is a one-way simplified entrypoint; Mediator coordinates interactions between peer components.
Facade vs Adapter: Facade changes the API to be simpler; Adapter changes the API to be compatible.
Facade vs Proxy: Facade offers a different, simplified API; Proxy keeps the same API and controls access/lifecycle.
Next skill: facade-pattern-typescript

### Flyweight

Definition: Share common state across many fine-grained objects to save memory.
Strong signals:
- You have a very large number of objects and memory usage is a proven bottleneck (heap/metrics).
- Many objects repeat the same immutable data (intrinsic state) that can be shared safely.
- You can pass per-instance context (extrinsic state) into methods instead of storing it in the shared object.
Weak/avoid signals:
- You haven’t measured memory pressure; this would be premature optimization.
- The “shared” state is mutable or frequently changes, risking spooky action-at-a-distance.
- CPU cost of pooling/lookups would outweigh the memory savings for your scale.
TypeScript notes:
- Model flyweights as immutable objects; freeze or avoid setters/public mutation.
- Use a Map keyed by intrinsic state (string/tuple key) as the flyweight factory/pool.
- Keep the context (extrinsic state) in lightweight structs or arrays; pass it into flyweight methods.
- Watch for memory leaks: pools need bounds/eviction if the intrinsic key space can grow unbounded.
Flyweight vs Singleton: Singleton enforces one instance; Flyweight allows many instances but shares intrinsic state across them.
Flyweight vs cache: caches often store computed results or full objects; Flyweight specifically splits state into shared intrinsic + external extrinsic.
Flyweight vs interning: interning is a special case of flyweight for identical immutable values (e.g., strings).
Next skill: flyweight-pattern-typescript

### Proxy

Definition: Provide a stand-in that controls access to another object.
Strong signals:
- Clients must depend on a stable service interface, but you need to add access control/caching/logging without touching them.
- The real service is expensive or remote, so you want lazy initialization or connection management.
- You need to manage the service lifecycle (create/close/retry) independently of client code.
- You want a transparent substitute that can be swapped for the real service at wiring time.
Weak/avoid signals:
- You need a different interface/shape; use Adapter instead.
- You’re building a simplified API for a whole subsystem; use Facade instead.
- You only want to add optional behaviors that the client composes explicitly; Decorator may fit better.
TypeScript notes:
- Define a Service interface and implement both RealService and Proxy to keep them interchangeable.
- Use constructor injection for collaborators; avoid reaching into global singletons inside the proxy.
- For async setup, cache the initialization Promise to prevent double-connect under concurrent calls.
- Make failure modes explicit (timeouts, retries, cache invalidation) to avoid “silent” behavioral changes.
Proxy vs Adapter: Proxy preserves the same interface; Adapter converts between incompatible interfaces.
Proxy vs Decorator: Proxy is about access/lifecycle/indirection; Decorator is about layering responsibilities and is composed by the client.
Proxy vs Facade: Proxy stands in for one service; Facade simplifies a whole subsystem behind a new interface.
Proxy vs cache: a cache can be one feature inside a proxy; proxy also covers access control, lazy init, remoting, and lifecycle.
Next skill: proxy-pattern-typescript

## Behavioral patterns

Category definition:
- Solve algorithm variation, collaboration, and event-driven coordination.
- Structure workflows, state machines, and handler pipelines.
- Support undo/history and command execution flows.
- Common in NestJS middleware, React state flows, event emitters, and queues.
- Avoid when flow is small and unlikely to change.

### Chain of Responsibility

Definition: Pass requests through a chain of handlers until one handles it.
Strong signals:
- Requests must pass through a configurable sequence of checks/steps (auth → validate → rate-limit → cache).
- You need early-exit/short-circuit when a handler rejects or fully handles the request.
- Different contexts require different subsets/order of handlers without duplicating logic.
- You want to add/remove handlers without changing client code that triggers the chain.
Weak/avoid signals:
- The steps are always fixed and centralized; a simple function pipeline may be enough.
- You need to swap one algorithm behind a stable API; Strategy fits better.
- You’re trying to extend behavior while always continuing; Decorator/middleware may be clearer.
TypeScript notes:
- Model handlers as `(ctx) => Result` or `{ handle(ctx): Result }` and compose them in arrays.
- Use discriminated unions for `Result` to make “continue/stop/handled/error” explicit.
- Keep handlers small, side-effect-light, and independently testable.
- For async handlers, standardize on `Promise<Result>` and avoid hidden shared mutable state.
CoR vs Middleware: middleware usually assumes a framework contract (next()), while CoR is a pattern you can wire anywhere with explicit stop/continue semantics.
CoR vs Decorator: CoR can stop the chain and handlers are peers; Decorator composes wrappers and typically always delegates.
CoR vs Strategy: Strategy swaps one behavior implementation; CoR sequences multiple behaviors that may each handle or pass.
CoR vs Pipeline: pipelines often always run all stages; CoR emphasizes conditional handling and early-exit.
Next skill: chain-of-responsibility-pattern-typescript

### Command

Definition: Encapsulate an action as an object to enable queuing, logging, or undo.
Strong signals:
- You want to treat an operation as data: queue it, schedule it, retry it, or persist it for audit.
- Multiple invokers (UI, API, cron, message consumer) should trigger the same action without duplicating logic.
- You need undo/redo, compensations, or reversible workflows (explicit inverse operations).
- You want a uniform execution API (e.g., `execute()`), independent of the receiver’s concrete method signatures.
- You need to add cross-cutting concerns (logging, metrics, auth) around actions without coupling invokers to receivers.
Weak/avoid signals:
- You just need to swap one algorithm behind a stable interface (use Strategy).
- You need a pipeline of checks/handlers where each may pass/stop (use Chain of Responsibility).
- The action is trivial and never queued/logged/replayed; a function call is enough.
- You’re modeling domain facts rather than requested work (use Events).
TypeScript notes:
- Prefer immutable command objects with typed payloads; avoid runtime mutation of inputs.
- Model execution results as typed `Result` (success/failure) for retries and observability.
- For async, standardize on `Promise<Result>` and keep commands side-effect boundaries explicit.
- Use a small `CommandBus` mapping `command.type` → handler to keep wiring centralized.
Command vs Strategy: Strategy swaps how to do one thing; Command packages a request so it can be queued, logged, retried, or undone.
Command vs Chain of Responsibility: CoR routes a request through multiple handlers; Command typically targets a single action/handler.
Command vs Event: Command asks for work to be done; Event announces work (or a fact) already happened.
Command vs Job: a Job is often a scheduled/executed unit; Command is the representation of the requested action (which may become a job).
Next skill: command-pattern-typescript

### Iterator

Definition: Provide a way to traverse a collection without exposing internal structure.
Strong signals:
- The collection’s representation is complex or sensitive (tree/graph, cursor/pagination, remote API), but clients need simple traversal.
- You need multiple traversal strategies over the same data (DFS vs BFS, filtered vs unfiltered, forward vs reverse).
- You want to pause/resume traversal and keep iteration state outside the collection.
- You need parallel traversals over the same collection without shared mutable cursor state.
- Traversal logic is duplicating across the codebase and is blurring collection responsibilities.
Weak/avoid signals:
- A simple array/list is all you have; built-in iteration is sufficient.
- Only one trivial traversal exists and won’t change; keep it as a loop/helper.
- You only need a one-off transformation (use `map/filter/reduce` directly).
- You’re applying it just for “patterns sake” without complexity, state, or strategy needs.
TypeScript notes:
- Prefer `Iterable<T>`/`Iterator<T>` and `for...of` for sync traversal.
- Use generator functions (`function*`) to implement iterators cleanly when state is simple.
- For I/O-bound traversal, use `AsyncIterable<T>`/`AsyncIterator<T>` with `for await...of`.
- Keep iterators small and stateful; keep collections focused on storage/access.
- Expose multiple iterators via named methods (e.g., `dfs()`, `bfs()`) rather than flags.
Iterator vs Generator: Generator is an implementation technique; Iterator is the interface/contract clients depend on.
Iterator vs Visitor: Iterator controls traversal; Visitor controls what operation runs on each element during traversal.
Iterator vs Composite: Composite models tree structure; Iterator is how you traverse that tree without exposing internals.
Iterator vs Stream: streams are push/pull pipelines with backpressure concerns; iterators are pull-based traversal state.
Next skill: iterator-pattern-typescript

### Mediator

Definition: Centralize complex communication between objects to reduce coupling.
Strong signals:
- You have a many-to-many dependency web (components/services) and a change in one forces changes in many others.
- Collaboration rules are non-trivial (enable/disable, validation, orchestration) and currently scattered across components.
- Components should be reusable in other contexts, but direct references prevent reuse.
- You need a single place to enforce workflow constraints and ordering of interactions.
- You want components to depend on one stable “coordination contract” instead of dozens of peers.
Weak/avoid signals:
- Interactions are simple and localized; direct calls are clearer.
- The “mediator” would just forward calls without real coordination (unnecessary indirection).
- You really need a simplified API over a subsystem (use Facade instead).
- You’re centralizing everything into one mega-class (God Object risk).
TypeScript notes:
- Define a narrow mediator interface (e.g., `notify(sender, event)` or typed events) so components only depend on that.
- Keep components dumb: they emit events/requests; mediator owns coordination and routing.
- Prefer feature-scoped mediators (per dialog/workflow) over a global singleton.
- If using an event hub, type events with discriminated unions for safety.
- Test mediator rules with fake components; test components without needing real peers.
Mediator vs Observer: Mediator owns the collaboration rules; Observer is a pub/sub mechanism that may be used to implement it.
Mediator vs Facade: Facade simplifies a subsystem API; Mediator coordinates peers that would otherwise talk directly.
Mediator vs Command: Command packages an action/request; Mediator decides which peers react and in what order.
Mediator vs Event Bus: an event bus is infrastructure; a mediator is domain/UI-specific coordination logic.
Next skill: mediator-pattern-typescript

### Memento

Definition: Capture and restore an object's internal state without exposing it.
Strong signals:
- You need undo/redo or transactional rollback for an object with private/encapsulated state.
- Snapshotting must not expose internal fields to external code (encapsulation matters).
- Multiple independent instances need independent histories (e.g., multiple editor sessions).
- You need lightweight history metadata (timestamp/label) without leaking state.
- You want to keep “when to snapshot” outside the originator, but “how to snapshot” inside it.
Weak/avoid signals:
- State is already immutable and you can just keep prior values (simple persistence/immutability).
- Full snapshots are too large/frequent; a differential log is more appropriate.
- You mainly need a simplified API over a subsystem (use Facade instead).
- Snapshots would require serializing external resources you can’t safely restore.
TypeScript notes:
- Model mementos as immutable value objects; avoid setters and mutable references.
- Hide memento internals via private fields and expose only metadata to caretakers.
- Use bounded history (max size) or checkpointing to avoid unbounded RAM growth.
- Prefer explicit snapshot triggers (before mutating operations) for deterministic undo.
- Test restoration by asserting state equality after round-trip snapshot -> mutate -> restore.
Memento vs Command: Command represents an action; Memento represents prior state used to undo or rollback actions.
Memento vs Prototype: Prototype clones objects for copying; Memento snapshots state for later restoration, often with restricted access.
Memento vs Event Sourcing: Memento stores snapshots; event sourcing stores events and rebuilds state by replay.
Memento vs Deep Copy: deep copy duplicates data; memento formalizes who can read/write the snapshot and when it’s used.
Next skill: memento-pattern-typescript

### Observer

Definition: Let observers subscribe to and react to changes in a subject.
Strong signals:
- One object’s state changes must notify many unknown/dynamic dependents.
- Subscribers must be able to subscribe/unsubscribe at runtime.
- Producer must not depend on concrete subscriber classes (interface/callback only).
- You need optional observers (logging, metrics, UI refresh, cache invalidation).
- Same event should fan out to multiple handlers without coordinating them.
- You need a simple in-process event mechanism without introducing a full message broker.
Weak/avoid signals:
- You primarily need to centralize complex two-way UI coordination (use Mediator).
- You need reliable cross-process delivery/durability (use a message broker / Pub-Sub).
- You need strict ordering/transactions across handlers (consider explicit orchestration).
- Notifications are rare and only one dependent exists (direct call is simpler).
- Event storms would require backpressure/throttling you can’t implement safely.
- You’re actually modeling “undo”/rollback snapshots (use Memento).
TypeScript notes:
- Prefer typed event maps: `{ eventName: PayloadType }` for safe callbacks.
- Return an `unsubscribe()` function from `subscribe()` to prevent leaks.
- Decide sync vs async dispatch; document re-entrancy expectations.
- Avoid mutating shared payload objects; treat payloads as readonly.
- Consider listener order guarantees (stable insertion order or explicit priority).
- Guard against exceptions in one listener breaking others (try/catch per listener).
- Use weak references only if you understand GC semantics; otherwise require explicit unsubs.
Observer vs Mediator: Observer broadcasts events from a publisher; Mediator coordinates interactions between peers via a central controller.
Observer vs Pub/Sub: Pub/Sub introduces a broker/topic so publishers don’t know subscribers at all; Observer usually binds to a publisher instance.
Observer vs Node EventEmitter: EventEmitter is a common Observer implementation; the pattern adds discipline around interfaces, payload typing, and lifecycle.
Observer vs CQRS/Event Sourcing: Observer reacts to events for side-effects; event sourcing persists events as the source of truth and rebuilds state by replay.
Observer vs Callback: a callback is one listener; Observer formalizes a dynamic list of listeners and subscription management.
Next skill: observer-pattern-typescript

### State

Definition: Encapsulate state-specific behavior and transitions.
Strong signals:
- Behavior changes drastically depending on a finite set of states.
- You're seeing switch/if ladders spread across many methods keyed by `state`.
- Adding a new state forces edits in multiple places (violates OCP).
- Transitions have rules (some moves are illegal) and must be explicit.
- State-specific behavior changes frequently compared to stable shared behavior.
- You want state-local code + transition logic to be testable in isolation.
Weak/avoid signals:
- Only 2-3 states and logic is stable (a simple conditional may be fine).
- You mainly need pluggable algorithms with no transitions (use Strategy).
- State is just data validation rules without behavior changes (use validation/schema).
- You need a persisted workflow engine / long-running saga (consider workflow/orchestrator).
- The "state" is really user permission roles (consider RBAC/Policy).
- You can model it as pure data + table-driven transitions with no polymorphism needed.
TypeScript notes:
- Prefer a `State` interface with methods that exist meaningfully for all states.
- Keep transition method(s) on the context (`changeState`) but allow states to request transitions.
- Use `never`/exhaustive checks for action unions when modeling events.
- Make illegal transitions throw typed errors (or return Result) to keep invariants.
- Consider separating "state storage" (enum/string) from "behavior object" (classes) if serialization matters.
- Keep shared context operations private; expose minimal context API to states to reduce coupling.
- Avoid per-transition `new` allocations in hot paths; reuse singleton states if they're stateless.
State vs Strategy: Strategy is chosen externally to vary an algorithm; State changes internally based on the context's lifecycle and may drive transitions.
State vs table-driven FSM: a table-driven FSM stores transitions as data; State encapsulates behavior per state as polymorphic objects.
State vs polymorphic config: config switches behavior via flags; State makes the lifecycle and legal transitions explicit and testable.
State vs workflow engine: State is in-process object behavior; workflow engines coordinate long-running, persisted steps across systems.
Next skill: state-pattern-typescript

### Strategy

Definition: Define interchangeable algorithms behind a common interface.
Strong signals:
- You have multiple interchangeable ways to do the same task (a “family of algorithms”).
- The context has a large conditional (`if/switch`) choosing an algorithm variant.
- New variants are added often and shouldn’t require editing the context (OCP).
- You want to switch behavior at runtime (config, user choice, feature flags).
- Each algorithm has distinct dependencies (e.g., external services) that you want isolated.
- You need to unit test each algorithm independently from the calling code.
Weak/avoid signals:
- Behavior changes because of lifecycle state transitions (use State).
- You need to represent “a request” as an object, queue/log/undo it (use Command).
- Only 1–2 stable variants; a simple conditional or function parameter is clearer.
- Algorithm variations require shared skeleton with small overridable steps (Template Method).
- The real need is orchestration across multiple steps/components (consider Facade/Mediator).
- The differences are data-only (parameters/tables) rather than behavior (use configuration).
TypeScript notes:
- Prefer a small `Strategy` interface with one primary method; keep it cohesive.
- Use dependency injection to wire strategies; the context should depend on the interface only.
- Consider a registry `Record<StrategyKey, Strategy>` for selection by config/user input.
- Prefer stateless strategies; treat them as singletons to avoid allocations in hot paths.
- If strategies share logic, extract helpers—not inheritance chains that recreate Template Method.
- For simple cases, a function type can be a strategy (no need for classes).
- Make selection explicit and validated (unknown key => typed error or default strategy).
Strategy vs State: Strategy is chosen externally to vary an algorithm; State changes internally based on the context's lifecycle and may drive transitions.
Strategy vs Command: Strategy is an algorithm; Command is a request object you can queue/log/undo and execute later.
Strategy vs Template Method: Template Method uses inheritance to vary steps in a fixed algorithm skeleton; Strategy uses composition to swap whole algorithms at runtime.
Strategy vs configuration: configuration tweaks one algorithm via parameters; Strategy swaps distinct implementations behind the same interface.
Next skill: strategy-pattern-typescript

### Template Method

Definition: Define an algorithm skeleton and let subclasses override steps.
Strong signals:
- Multiple implementations share the same high-level workflow but differ in a few steps.
- You're fighting duplication across subclasses (same sequence, different details).
- The order of steps is important and should be standardized in one place.
- You need extension points (hooks) before/after certain steps.
- Subclasses should customize behavior without rewriting the entire algorithm.
- You want to keep client code polymorphic (no type-based conditionals).
Weak/avoid signals:
- You need runtime switching between algorithms (use Strategy).
- Behavior changes due to lifecycle/state transitions (use State).
- You need queue/log/undo/remote execution of requests (use Command).
- The differences are data-only parameters/configuration (prefer configuration).
- Only 1-2 variants with low duplication; a simple shared function is clearer.
- You're centralizing cross-component orchestration (consider Mediator/Facade).
TypeScript notes:
- TS has no `final`; emulate by making the template orchestration method non-overridable by convention, or by using `private` helpers that call `protected` steps.
- Prefer `protected` step methods and keep template orchestration `public` and small.
- Don't call overridable methods from constructors (init order hazards).
- Provide optional hooks with empty defaults (`beforeX/afterX`) to avoid forcing overrides.
- Keep step method names cohesive and domain-specific (avoid "step1/step2").
- If subclasses need shared partial behavior, pull it into the base as default step implementations.
- When inheritance becomes painful, consider Strategy + composition instead.
Template Method vs Strategy: Template Method fixes the algorithm skeleton in a base class and varies steps via subclasses; Strategy swaps whole algorithms via composition at runtime.
Template Method vs State: Template Method varies steps for the same workflow; State varies behavior based on internal lifecycle transitions.
Template Method vs Command: Template Method structures a workflow; Command represents a request you can queue/log/undo and execute later.
Template Method vs shared utility: utilities share code; Template Method enforces ordering and extension points across variants.
Next skill: template-method-pattern-typescript

### Visitor

Definition: Separate operations from object structures by visiting elements with a visitor.
Strong signals:
- You have a stable element hierarchy (types change rarely), but you need to add new operations frequently.
- The operation differs per concrete element type (type-specific logic is unavoidable).
- You want to keep element classes focused on their core responsibilities (avoid “export/print/validate” clutter).
- Client code shouldn’t do `instanceof`/`switch` on concrete types to pick behavior.
- You want to group all variants of one operation in one place (one visitor per operation).
- You need to traverse a composite/object graph and apply the same operation everywhere.
Weak/avoid signals:
- New element types are added frequently (you’ll have to update every visitor each time).
- You only need one operation; a method on the element or a standalone function is simpler.
- You mostly need runtime-switchable algorithms (use Strategy).
- You need event-driven notification (Observer) or central orchestration (Mediator).
- You can model elements as a discriminated union and use exhaustive `switch` cleanly (may be simpler).
- You can’t touch element types at all (even to add `accept`) and adapters are too costly.
TypeScript notes:
- TS doesn’t do runtime overloading; use distinct visit method names per element (`visitCircle`, `visitDot`, etc.).
- Keep the `Visitor` interface explicit and stable; use `never` checks in visitors for exhaustiveness where possible.
- `accept(visitor)` is the key: it performs the second dispatch by calling the correct visit method.
- Prefer visitors with explicit state fields (e.g., output buffer) over hidden globals; reset between runs.
- If you use discriminated unions instead of classes, you can mimic Visitor with a `visit(node)` dispatcher object.
- When elements are immutable, visitors can return values; when mutable, visitors can apply in-place changes carefully.
- If traversal is complex, pair Visitor with Composite/Iterator; keep traversal outside visitors unless it’s part of the operation.
Visitor vs Strategy: Strategy swaps algorithms at runtime for one abstraction; Visitor adds new operations across many concrete element types without changing those types.
Visitor vs Command: Command encapsulates a request you can queue/log/undo; Visitor encapsulates a cross-cutting operation over a structure of typed elements.
Visitor vs Interpreter/pattern-matching: pattern-matching focuses on branching by type; Visitor focuses on organizing operations by algorithm and using double dispatch to avoid client branching.
Visitor vs adding methods: adding methods grows element responsibilities; Visitor keeps elements lean and moves auxiliary behaviors out.
Next skill: visitor-pattern-typescript
