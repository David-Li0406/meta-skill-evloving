# Agent Communication

## Patterns


---
  #### **Name**
Typed Message Passing
  #### **Description**
Strongly typed messages with schema validation
  #### **When**
Agents need to exchange structured data
  #### **Example**
    import { z } from 'zod';
    
    // Define message types
    const TaskRequestSchema = z.object({
        type: z.literal('task_request'),
        requestId: z.string().uuid(),
        fromAgent: z.string(),
        toAgent: z.string(),
        task: z.object({
            description: z.string(),
            priority: z.enum(['low', 'medium', 'high', 'critical']),
            deadline: z.number().optional(),
            context: z.record(z.unknown())
        }),
        timestamp: z.number()
    });
    
    const TaskResponseSchema = z.object({
        type: z.literal('task_response'),
        requestId: z.string().uuid(),
        fromAgent: z.string(),
        status: z.enum(['accepted', 'rejected', 'completed', 'failed']),
        result: z.unknown().optional(),
        error: z.string().optional(),
        timestamp: z.number()
    });
    
    const MessageSchema = z.discriminatedUnion('type', [
        TaskRequestSchema,
        TaskResponseSchema,
        // Add more message types...
    ]);
    
    type Message = z.infer<typeof MessageSchema>;
    
    class TypedMessageBus {
        private handlers: Map<string, Set<MessageHandler>> = new Map();
        private messageLog: Message[] = [];
    
        async send(message: Message): Promise<void> {
            // Validate message
            const validated = MessageSchema.parse(message);
    
            // Log for debugging
            this.messageLog.push({
                ...validated,
                _logged: Date.now()
            });
    
            // Deliver to subscribers
            const handlers = this.handlers.get(validated.toAgent);
            if (!handlers || handlers.size === 0) {
                throw new Error(`No handlers for agent: ${validated.toAgent}`);
            }
    
            await Promise.all(
                Array.from(handlers).map(h => h(validated))
            );
        }
    
        subscribe(agentId: string, handler: MessageHandler): () => void {
            if (!this.handlers.has(agentId)) {
                this.handlers.set(agentId, new Set());
            }
            this.handlers.get(agentId)!.add(handler);
    
            return () => this.handlers.get(agentId)!.delete(handler);
        }
    
        // Replay for debugging
        getMessages(filter?: MessageFilter): Message[] {
            return this.messageLog.filter(m => {
                if (filter?.fromAgent && m.fromAgent !== filter.fromAgent) return false;
                if (filter?.toAgent && m.toAgent !== filter.toAgent) return false;
                if (filter?.type && m.type !== filter.type) return false;
                return true;
            });
        }
    }
    
    // Agent with typed messaging
    class TypedAgent {
        constructor(
            private id: string,
            private bus: TypedMessageBus
        ) {
            this.bus.subscribe(this.id, this.handleMessage.bind(this));
        }
    
        async requestTask(toAgent: string, task: TaskRequest['task']): Promise<TaskResponse> {
            const requestId = crypto.randomUUID();
    
            const request: TaskRequest = {
                type: 'task_request',
                requestId,
                fromAgent: this.id,
                toAgent,
                task,
                timestamp: Date.now()
            };
    
            await this.bus.send(request);
    
            // Wait for response
            return this.waitForResponse(requestId);
        }
    
        private async handleMessage(message: Message): Promise<void> {
            switch (message.type) {
                case 'task_request':
                    await this.handleTaskRequest(message);
                    break;
                case 'task_response':
                    this.resolveResponse(message);
                    break;
            }
        }
    }
    

---
  #### **Name**
Blackboard Pattern
  #### **Description**
Shared knowledge space that agents read/write to
  #### **When**
Agents need to collaborate on evolving shared state
  #### **Example**
    // Blackboard: shared knowledge space for agent collaboration
    
    interface BlackboardEntry {
        key: string;
        value: unknown;
        author: string;
        timestamp: number;
        confidence: number;
        dependencies: string[];  // Keys this entry depends on
    }
    
    class Blackboard {
        private entries: Map<string, BlackboardEntry> = new Map();
        private watchers: Map<string, Set<WatchCallback>> = new Map();
        private history: BlackboardChange[] = [];
    
        // Write with provenance tracking
        async write(
            key: string,
            value: unknown,
            author: string,
            metadata?: { confidence?: number; dependencies?: string[] }
        ): Promise<void> {
            const entry: BlackboardEntry = {
                key,
                value,
                author,
                timestamp: Date.now(),
                confidence: metadata?.confidence ?? 1.0,
                dependencies: metadata?.dependencies ?? []
            };
    
            const previousValue = this.entries.get(key);
            this.entries.set(key, entry);
    
            // Log change
            this.history.push({
                type: 'write',
                key,
                previousValue,
                newValue: entry,
                author,
                timestamp: Date.now()
            });
    
            // Notify watchers
            await this.notifyWatchers(key, entry);
        }
    
        // Read with dependency tracking
        read(key: string, reader?: string): BlackboardEntry | undefined {
            const entry = this.entries.get(key);
    
            if (entry && reader) {
                this.history.push({
                    type: 'read',
                    key,
                    reader,
                    timestamp: Date.now()
                });
            }
    
            return entry;
        }
    
        // Watch for changes
        watch(key: string, callback: WatchCallback): () => void {
            if (!this.watchers.has(key)) {
                this.watchers.set(key, new Set());
            }
            this.watchers.get(key)!.add(callback);
    
            return () => this.watchers.get(key)!.delete(callback);
        }
    
        // Query by pattern
        query(pattern: string | RegExp): BlackboardEntry[] {
            const regex = typeof pattern === 'string'
                ? new RegExp(pattern)
                : pattern;
    
            return Array.from(this.entries.values())
                .filter(e => regex.test(e.key));
        }
    
        // Get entries by author
        getByAuthor(author: string): BlackboardEntry[] {
            return Array.from(this.entries.values())
                .filter(e => e.author === author);
        }
    
        // Conflict resolution for concurrent writes
        async mergeConflict(
            key: string,
            entries: BlackboardEntry[],
            resolver: ConflictResolver
        ): Promise<BlackboardEntry> {
            const resolved = await resolver.resolve(entries);
            await this.write(key, resolved.value, 'conflict_resolver', {
                confidence: resolved.confidence,
                dependencies: entries.map(e => `${key}@${e.timestamp}`)
            });
            return this.entries.get(key)!;
        }
    }
    
    // Agent using blackboard for collaboration
    class BlackboardAgent {
        constructor(
            private id: string,
            private blackboard: Blackboard,
            private llm: LLMClient
        ) {}
    
        async contribute(topic: string): Promise<void> {
            // Read what others have written
            const existingEntries = this.blackboard.query(`${topic}.*`);
            const context = existingEntries.map(e =>
                `[${e.author}]: ${JSON.stringify(e.value)}`
            ).join('\n');
    
            // Generate contribution
            const response = await this.llm.invoke({
                messages: [{
                    role: 'system',
                    content: `You are contributing to a collaborative analysis on: ${topic}
    
                    Existing contributions:
                    ${context}
    
                    Add new insights that complement, not duplicate, existing contributions.`
                }]
            });
    
            // Write to blackboard
            await this.blackboard.write(
                `${topic}.${this.id}`,
                response.content,
                this.id,
                { confidence: 0.8 }
            );
        }
    
        // React to changes
        async watchAndRespond(pattern: string): Promise<void> {
            const entries = this.blackboard.query(pattern);
    
            for (const entry of entries) {
                this.blackboard.watch(entry.key, async (newValue) => {
                    await this.respondToChange(entry.key, newValue);
                });
            }
        }
    }
    

---
  #### **Name**
Event-Driven Agent Communication
  #### **Description**
Agents publish events, others subscribe and react
  #### **When**
Loose coupling and async communication needed
  #### **Example**
    import { EventEmitter } from 'events';
    
    // Event types
    interface AgentEvent {
        eventId: string;
        eventType: string;
        source: string;
        timestamp: number;
        payload: unknown;
        correlationId?: string;
    }
    
    interface TaskStartedEvent extends AgentEvent {
        eventType: 'task.started';
        payload: {
            taskId: string;
            description: string;
            assignee: string;
        };
    }
    
    interface TaskCompletedEvent extends AgentEvent {
        eventType: 'task.completed';
        payload: {
            taskId: string;
            result: unknown;
            duration: number;
        };
    }
    
    interface ErrorOccurredEvent extends AgentEvent {
        eventType: 'error.occurred';
        payload: {
            error: string;
            context: unknown;
            recoverable: boolean;
        };
    }
    
    type AgentEvents = TaskStartedEvent | TaskCompletedEvent | ErrorOccurredEvent;
    
    class EventBus {
        private emitter = new EventEmitter();
        private eventLog: AgentEvent[] = [];
    
        publish<T extends AgentEvent>(event: T): void {
            // Add metadata
            const enrichedEvent = {
                ...event,
                eventId: event.eventId || crypto.randomUUID(),
                timestamp: event.timestamp || Date.now()
            };
    
            // Log for replay
            this.eventLog.push(enrichedEvent);
    
            // Emit
            this.emitter.emit(event.eventType, enrichedEvent);
            this.emitter.emit('*', enrichedEvent);  // Wildcard subscribers
        }
    
        subscribe<T extends AgentEvent>(
            eventType: T['eventType'] | '*',
            handler: (event: T) => void | Promise<void>
        ): () => void {
            this.emitter.on(eventType, handler);
            return () => this.emitter.off(eventType, handler);
        }
    
        // Replay events for recovery or debugging
        async replay(
            filter?: { since?: number; types?: string[] },
            handler?: (event: AgentEvent) => Promise<void>
        ): Promise<AgentEvent[]> {
            const filtered = this.eventLog.filter(e => {
                if (filter?.since && e.timestamp < filter.since) return false;
                if (filter?.types && !filter.types.includes(e.eventType)) return false;
                return true;
            });
    
            if (handler) {
                for (const event of filtered) {
                    await handler(event);
                }
            }
    
            return filtered;
        }
    }
    
    // Event-driven agent
    class EventDrivenAgent {
        constructor(
            private id: string,
            private eventBus: EventBus
        ) {
            // Subscribe to relevant events
            this.eventBus.subscribe('task.started', this.onTaskStarted.bind(this));
            this.eventBus.subscribe('error.occurred', this.onError.bind(this));
        }
    
        private async onTaskStarted(event: TaskStartedEvent): Promise<void> {
            if (event.payload.assignee !== this.id) return;
    
            try {
                const result = await this.executeTask(event.payload);
    
                this.eventBus.publish({
                    eventType: 'task.completed',
                    source: this.id,
                    correlationId: event.eventId,
                    payload: {
                        taskId: event.payload.taskId,
                        result,
                        duration: Date.now() - event.timestamp
                    }
                } as TaskCompletedEvent);
            } catch (error) {
                this.eventBus.publish({
                    eventType: 'error.occurred',
                    source: this.id,
                    correlationId: event.eventId,
                    payload: {
                        error: error.message,
                        context: { taskId: event.payload.taskId },
                        recoverable: true
                    }
                } as ErrorOccurredEvent);
            }
        }
    
        private onError(event: ErrorOccurredEvent): void {
            console.error(`[${this.id}] Error from ${event.source}: ${event.payload.error}`);
        }
    }
    

---
  #### **Name**
Request-Response with Timeout
  #### **Description**
Synchronous-style communication with timeout handling
  #### **When**
Agent needs response before continuing
  #### **Example**
    class RequestResponseChannel {
        private pendingRequests: Map<string, {
            resolve: (value: Response) => void;
            reject: (error: Error) => void;
            timeout: NodeJS.Timeout;
        }> = new Map();
    
        private bus: TypedMessageBus;
        private defaultTimeout = 30000;
    
        async request<T>(
            toAgent: string,
            payload: unknown,
            options?: { timeout?: number }
        ): Promise<T> {
            const requestId = crypto.randomUUID();
            const timeout = options?.timeout ?? this.defaultTimeout;
    
            return new Promise((resolve, reject) => {
                // Set timeout
                const timeoutHandle = setTimeout(() => {
                    this.pendingRequests.delete(requestId);
                    reject(new Error(`Request ${requestId} timed out after ${timeout}ms`));
                }, timeout);
    
                // Store pending request
                this.pendingRequests.set(requestId, {
                    resolve: resolve as (value: Response) => void,
                    reject,
                    timeout: timeoutHandle
                });
    
                // Send request
                this.bus.send({
                    type: 'request',
                    requestId,
                    fromAgent: this.agentId,
                    toAgent,
                    payload,
                    timestamp: Date.now()
                }).catch(reject);
            });
        }
    
        respond(requestId: string, response: unknown): void {
            this.bus.send({
                type: 'response',
                requestId,
                fromAgent: this.agentId,
                payload: response,
                timestamp: Date.now()
            });
        }
    
        handleResponse(message: ResponseMessage): void {
            const pending = this.pendingRequests.get(message.requestId);
            if (!pending) return;
    
            clearTimeout(pending.timeout);
            this.pendingRequests.delete(message.requestId);
            pending.resolve(message.payload);
        }
    }
    

## Anti-Patterns


---
  #### **Name**
Untyped Messages
  #### **Description**
Sending arbitrary JSON between agents without schemas
  #### **Why**
Leads to runtime errors, hard to debug, no IDE support
  #### **Instead**
Define message schemas with Zod or TypeScript interfaces.

---
  #### **Name**
Synchronous Everywhere
  #### **Description**
All agent communication is blocking request-response
  #### **Why**
Creates bottlenecks, doesn't scale, fails cascade
  #### **Instead**
Use async events where response not immediately needed.

---
  #### **Name**
No Message Logging
  #### **Description**
Messages not persisted for debugging or replay
  #### **Why**
Impossible to debug failures, can't recover from crashes
  #### **Instead**
Log all messages with timestamps and correlation IDs.

---
  #### **Name**
Circular Dependencies
  #### **Description**
Agent A waits for B which waits for A
  #### **Why**
Deadlocks, hangs, hard to detect
  #### **Instead**
Design acyclic communication flows or use async events.