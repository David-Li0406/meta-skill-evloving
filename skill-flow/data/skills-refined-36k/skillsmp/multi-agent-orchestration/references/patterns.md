# Multi-Agent Orchestration

## Patterns


---
  #### **Name**
Sequential Chain Pattern
  #### **Description**
Agents execute in order, each building on previous output
  #### **When**
Tasks have clear stages that must complete in order
  #### **Example**
    import { StateGraph, END } from '@langchain/langgraph';
    
    // Define shared state
    interface WorkflowState {
        input: string;
        researchResults?: string;
        draftContent?: string;
        reviewFeedback?: string;
        finalOutput?: string;
    }
    
    // Create specialized agents
    class SequentialAgentChain {
        private graph: StateGraph<WorkflowState>;
    
        constructor() {
            this.graph = new StateGraph<WorkflowState>({
                channels: {
                    input: null,
                    researchResults: null,
                    draftContent: null,
                    reviewFeedback: null,
                    finalOutput: null
                }
            });
    
            // Add nodes (agents)
            this.graph.addNode('researcher', this.researchAgent.bind(this));
            this.graph.addNode('writer', this.writerAgent.bind(this));
            this.graph.addNode('reviewer', this.reviewerAgent.bind(this));
            this.graph.addNode('finalizer', this.finalizerAgent.bind(this));
    
            // Define sequential edges
            this.graph.addEdge('__start__', 'researcher');
            this.graph.addEdge('researcher', 'writer');
            this.graph.addEdge('writer', 'reviewer');
            this.graph.addEdge('reviewer', 'finalizer');
            this.graph.addEdge('finalizer', END);
        }
    
        private async researchAgent(state: WorkflowState): Promise<Partial<WorkflowState>> {
            const research = await this.llm.invoke({
                messages: [{
                    role: 'system',
                    content: 'You are a research specialist. Gather key facts and sources.'
                }, {
                    role: 'user',
                    content: `Research this topic: ${state.input}`
                }]
            });
    
            return { researchResults: research.content };
        }
    
        private async writerAgent(state: WorkflowState): Promise<Partial<WorkflowState>> {
            const draft = await this.llm.invoke({
                messages: [{
                    role: 'system',
                    content: 'You are a content writer. Create compelling content based on research.'
                }, {
                    role: 'user',
                    content: `Write content based on this research:\n${state.researchResults}`
                }]
            });
    
            return { draftContent: draft.content };
        }
    
        private async reviewerAgent(state: WorkflowState): Promise<Partial<WorkflowState>> {
            const review = await this.llm.invoke({
                messages: [{
                    role: 'system',
                    content: 'You are an editor. Review for accuracy, clarity, and style.'
                }, {
                    role: 'user',
                    content: `Review this draft:\n${state.draftContent}`
                }]
            });
    
            return { reviewFeedback: review.content };
        }
    
        private async finalizerAgent(state: WorkflowState): Promise<Partial<WorkflowState>> {
            const final = await this.llm.invoke({
                messages: [{
                    role: 'system',
                    content: 'You are a finalizer. Incorporate feedback and produce final output.'
                }, {
                    role: 'user',
                    content: `Original draft:\n${state.draftContent}\n\nFeedback:\n${state.reviewFeedback}\n\nProduce final version.`
                }]
            });
    
            return { finalOutput: final.content };
        }
    
        async run(input: string): Promise<string> {
            const app = this.graph.compile();
            const result = await app.invoke({ input });
            return result.finalOutput;
        }
    }
    

---
  #### **Name**
Parallel Execution Pattern
  #### **Description**
Multiple agents work simultaneously, results aggregated
  #### **When**
Tasks can be parallelized for speed or diversity
  #### **Example**
    class ParallelAgentExecution {
        // Parallel agents for code review
        async parallelCodeReview(code: string): Promise<AggregatedReview> {
            // Define specialized reviewers
            const reviewers = [
                {
                    name: 'security',
                    prompt: 'Review for security vulnerabilities. Focus on injection, auth, data exposure.'
                },
                {
                    name: 'performance',
                    prompt: 'Review for performance issues. Focus on complexity, memory, async patterns.'
                },
                {
                    name: 'maintainability',
                    prompt: 'Review for maintainability. Focus on naming, structure, documentation.'
                },
                {
                    name: 'correctness',
                    prompt: 'Review for logical correctness. Focus on edge cases, error handling.'
                }
            ];
    
            // Execute all reviewers in parallel
            const reviews = await Promise.all(
                reviewers.map(async (reviewer) => {
                    const result = await this.llm.invoke({
                        messages: [{
                            role: 'system',
                            content: `You are a ${reviewer.name} code reviewer. ${reviewer.prompt}`
                        }, {
                            role: 'user',
                            content: `Review this code:\n\`\`\`\n${code}\n\`\`\``
                        }]
                    });
    
                    return {
                        category: reviewer.name,
                        findings: this.parseFindings(result.content)
                    };
                })
            );
    
            // Aggregate with synthesizer agent
            const synthesis = await this.synthesizeReviews(reviews);
    
            return {
                individualReviews: reviews,
                synthesis,
                overallScore: this.calculateScore(reviews)
            };
        }
    
        private async synthesizeReviews(reviews: Review[]): Promise<string> {
            const synthesizer = await this.llm.invoke({
                messages: [{
                    role: 'system',
                    content: 'You are a senior engineer. Synthesize multiple code reviews into a coherent summary with prioritized action items.'
                }, {
                    role: 'user',
                    content: `Synthesize these reviews:\n${JSON.stringify(reviews, null, 2)}`
                }]
            });
    
            return synthesizer.content;
        }
    }
    

---
  #### **Name**
Router/Dispatcher Pattern
  #### **Description**
Intelligent routing to specialized agents based on task classification
  #### **When**
Different task types require different expertise
  #### **Example**
    import { z } from 'zod';
    
    // Define routing schema
    const RouteSchema = z.object({
        category: z.enum(['technical', 'billing', 'general', 'escalate']),
        confidence: z.number().min(0).max(1),
        reasoning: z.string()
    });
    
    class RouterAgent {
        private readonly agents: Map<string, Agent> = new Map();
    
        constructor() {
            // Register specialized agents
            this.agents.set('technical', new TechnicalSupportAgent());
            this.agents.set('billing', new BillingSupportAgent());
            this.agents.set('general', new GeneralSupportAgent());
            this.agents.set('escalate', new EscalationAgent());
        }
    
        async route(userMessage: string, context: ConversationContext): Promise<AgentResponse> {
            // Step 1: Classify the request
            const classification = await this.classify(userMessage, context);
    
            // Step 2: Confidence threshold check
            if (classification.confidence < 0.7) {
                // Low confidence: ask clarifying question
                return {
                    type: 'clarification',
                    message: 'I want to make sure I help you with the right thing. Could you tell me more about your issue?',
                    suggestedCategories: this.getSuggestedCategories(classification)
                };
            }
    
            // Step 3: Route to specialized agent
            const agent = this.agents.get(classification.category);
            if (!agent) {
                throw new Error(`Unknown category: ${classification.category}`);
            }
    
            // Step 4: Execute with context handoff
            return agent.handle(userMessage, {
                ...context,
                routingDecision: classification,
                previousAgents: [...(context.previousAgents || []), 'router']
            });
        }
    
        private async classify(message: string, context: ConversationContext): Promise<z.infer<typeof RouteSchema>> {
            const result = await this.llm.invoke({
                messages: [{
                    role: 'system',
                    content: `You are a request classifier. Categorize user requests.
    
                        Categories:
                        - technical: Code issues, API problems, integration help, bugs
                        - billing: Payments, subscriptions, invoices, refunds
                        - general: Account questions, feature info, how-to questions
                        - escalate: Complaints, urgent issues, requests for human agent
    
                        Respond with JSON: { "category": "...", "confidence": 0.0-1.0, "reasoning": "..." }`
                }, {
                    role: 'user',
                    content: message
                }],
                response_format: { type: 'json_object' }
            });
    
            return RouteSchema.parse(JSON.parse(result.content));
        }
    }
    

---
  #### **Name**
Hierarchical Supervisor Pattern
  #### **Description**
Manager agent delegates to and coordinates worker agents
  #### **When**
Complex tasks require breakdown and coordination
  #### **Example**
    class HierarchicalAgentSystem {
        private supervisor: SupervisorAgent;
        private workers: Map<string, WorkerAgent>;
    
        async execute(task: ComplexTask): Promise<TaskResult> {
            // Supervisor breaks down task
            const plan = await this.supervisor.planTask(task);
    
            // Track execution state
            const executionState: ExecutionState = {
                plan,
                completedSteps: [],
                pendingSteps: [...plan.steps],
                workerOutputs: new Map()
            };
    
            // Execute with supervisor oversight
            while (executionState.pendingSteps.length > 0) {
                const step = executionState.pendingSteps.shift()!;
    
                // Supervisor assigns to appropriate worker
                const assignment = await this.supervisor.assignStep(step, executionState);
    
                // Worker executes
                const worker = this.workers.get(assignment.workerId);
                if (!worker) throw new Error(`Worker not found: ${assignment.workerId}`);
    
                const result = await worker.execute(step, assignment.context);
    
                // Supervisor reviews result
                const review = await this.supervisor.reviewResult(step, result, executionState);
    
                if (review.approved) {
                    executionState.completedSteps.push({ step, result });
                    executionState.workerOutputs.set(step.id, result);
                } else if (review.retry) {
                    // Put back in queue with feedback
                    executionState.pendingSteps.unshift({
                        ...step,
                        feedback: review.feedback,
                        attempt: (step.attempt || 0) + 1
                    });
                } else {
                    // Escalate or fail
                    throw new Error(`Step failed after review: ${step.id}`);
                }
    
                // Check if plan needs adjustment
                if (review.planAdjustment) {
                    const newSteps = await this.supervisor.adjustPlan(
                        executionState,
                        review.planAdjustment
                    );
                    executionState.pendingSteps.push(...newSteps);
                }
            }
    
            // Supervisor synthesizes final result
            return this.supervisor.synthesize(executionState);
        }
    }
    
    class SupervisorAgent {
        async planTask(task: ComplexTask): Promise<ExecutionPlan> {
            const plan = await this.llm.invoke({
                messages: [{
                    role: 'system',
                    content: `You are a project manager. Break down complex tasks into discrete steps.
                    Each step should be:
                    - Specific and actionable
                    - Assignable to one worker
                    - Have clear success criteria
                    - List dependencies on other steps
    
                    Available workers: ${this.describeWorkers()}`
                }, {
                    role: 'user',
                    content: `Plan this task: ${task.description}`
                }]
            });
    
            return this.parsePlan(plan.content);
        }
    
        async reviewResult(step: Step, result: StepResult, state: ExecutionState): Promise<ReviewDecision> {
            const review = await this.llm.invoke({
                messages: [{
                    role: 'system',
                    content: `You are a quality reviewer. Evaluate if the step was completed successfully.
                    Consider: correctness, completeness, alignment with overall task.`
                }, {
                    role: 'user',
                    content: `Step: ${JSON.stringify(step)}
                    Result: ${JSON.stringify(result)}
                    Overall task: ${state.plan.task.description}
    
                    Respond with: { "approved": bool, "retry": bool, "feedback": string, "planAdjustment": string | null }`
                }]
            });
    
            return JSON.parse(review.content);
        }
    }
    

## Anti-Patterns


---
  #### **Name**
Premature Multi-Agent Architecture
  #### **Description**
Using multiple agents when one would suffice
  #### **Why**
Coordination overhead, increased latency, debugging complexity
  #### **Instead**
Start with single agent, split only when clearly beneficial.

---
  #### **Name**
Global Shared State
  #### **Description**
All agents read/write to single global state
  #### **Why**
Race conditions, debugging nightmares, tight coupling
  #### **Instead**
Use scoped state channels with clear ownership.

---
  #### **Name**
Unbounded Agent Loops
  #### **Description**
Agents that can call each other indefinitely
  #### **Why**
Infinite loops, runaway costs, system hangs
  #### **Instead**
Enforce maximum iterations and circuit breakers.

---
  #### **Name**
Implicit Handoffs
  #### **Description**
Agent transitions without explicit state transfer
  #### **Why**
Lost context, inconsistent behavior, debugging difficulty
  #### **Instead**
Explicit handoff protocol with state snapshot.

---
  #### **Name**
No Observability
  #### **Description**
Multi-agent system without tracing and logging
  #### **Why**
Impossible to debug failures or optimize performance
  #### **Instead**
Trace every agent invocation, state change, and decision.