# Autonomous Agents

## Patterns


---
  #### **Name**
ReAct Agent Loop
  #### **Description**
Alternating reasoning and action steps
  #### **When**
Interactive problem-solving, tool use, exploration
  #### **Example**
    # REACT PATTERN:
    
    """
    The ReAct loop:
    1. Thought: Reason about what to do next
    2. Action: Choose and execute a tool
    3. Observation: Receive result
    4. Repeat until goal achieved
    
    Key: Explicit reasoning traces make debugging possible
    """
    
    ## Basic ReAct Implementation
    """
    from langchain.agents import create_react_agent
    from langchain_openai import ChatOpenAI
    
    # Define the ReAct prompt template
    react_prompt = '''
    Answer the question using the following format:
    
    Question: the input question
    Thought: reason about what to do
    Action: tool_name
    Action Input: input to the tool
    Observation: result of the action
    ... (repeat Thought/Action/Observation as needed)
    Thought: I now know the final answer
    Final Answer: the answer
    '''
    
    # Create the agent
    agent = create_react_agent(
        llm=ChatOpenAI(model="gpt-4o"),
        tools=tools,
        prompt=react_prompt,
    )
    
    # Execute with step limit
    result = agent.invoke(
        {"input": query},
        config={"max_iterations": 10}  # Prevent runaway loops
    )
    """
    
    ## LangGraph ReAct (Production)
    """
    from langgraph.prebuilt import create_react_agent
    from langgraph.checkpoint.postgres import PostgresSaver
    
    # Production checkpointer
    checkpointer = PostgresSaver.from_conn_string(
        os.environ["POSTGRES_URL"]
    )
    
    agent = create_react_agent(
        model=llm,
        tools=tools,
        checkpointer=checkpointer,  # Durable state
    )
    
    # Invoke with thread for state persistence
    config = {"configurable": {"thread_id": "user-123"}}
    result = agent.invoke({"messages": [query]}, config)
    """
    

---
  #### **Name**
Plan-Execute Pattern
  #### **Description**
Separate planning phase from execution
  #### **When**
Complex multi-step tasks, when full plan visibility matters
  #### **Example**
    # PLAN-EXECUTE PATTERN:
    
    """
    Two-phase approach:
    1. Planning: Decompose goal into subtasks
    2. Execution: Execute subtasks, potentially re-plan
    
    Advantages:
    - Full visibility into plan before execution
    - Can validate/modify plan with human
    - Cleaner separation of concerns
    
    Disadvantages:
    - Less adaptive to mid-task discoveries
    - Plan may become stale
    """
    
    ## LangGraph Plan-Execute
    """
    from langgraph.prebuilt import create_plan_and_execute_agent
    
    # Planner creates the task list
    planner_prompt = '''
    For the given objective, create a step-by-step plan.
    Each step should be atomic and actionable.
    Format: numbered list of steps.
    '''
    
    # Executor handles individual steps
    executor_prompt = '''
    You are executing step {step_number} of the plan.
    Previous results: {previous_results}
    Current step: {current_step}
    Execute this step using available tools.
    '''
    
    agent = create_plan_and_execute_agent(
        planner=planner_llm,
        executor=executor_llm,
        tools=tools,
        replan_on_error=True,  # Re-plan if step fails
    )
    
    # Human approval of plan
    config = {
        "configurable": {
            "thread_id": "task-456",
        },
        "interrupt_before": ["execute"],  # Pause before execution
    }
    
    # First call creates plan
    plan = agent.invoke({"objective": goal}, config)
    
    # Review plan, then continue
    if human_approves(plan):
        result = agent.invoke(None, config)  # Continue from checkpoint
    """
    
    ## Decomposition Strategies
    """
    # Decomposition-First: Plan everything, then execute
    # Best for: Stable tasks, need full plan approval
    
    # Interleaved: Plan one step, execute, repeat
    # Best for: Dynamic tasks, learning as you go
    
    def interleaved_execute(goal, max_steps=10):
        state = {"goal": goal, "completed": [], "remaining": [goal]}
    
        for step in range(max_steps):
            # Plan next action based on current state
            next_action = planner.plan_next(state)
    
            if next_action == "DONE":
                break
    
            # Execute and update state
            result = executor.execute(next_action)
            state["completed"].append((next_action, result))
    
            # Re-evaluate remaining work
            state["remaining"] = planner.reassess(state)
    
        return state
    """
    

---
  #### **Name**
Reflection Pattern
  #### **Description**
Self-evaluation and iterative improvement
  #### **When**
Quality matters, complex outputs, creative tasks
  #### **Example**
    # REFLECTION PATTERN:
    
    """
    Self-correction loop:
    1. Generate initial output
    2. Evaluate against criteria
    3. Critique and identify issues
    4. Refine based on critique
    5. Repeat until satisfactory
    
    Also called: Evaluator-Optimizer, Self-Critique
    """
    
    ## Basic Reflection
    """
    def reflect_and_improve(task, max_iterations=3):
        # Initial generation
        output = generator.generate(task)
    
        for i in range(max_iterations):
            # Evaluate output
            critique = evaluator.critique(
                task=task,
                output=output,
                criteria=[
                    "Correctness",
                    "Completeness",
                    "Clarity",
                ]
            )
    
            if critique["passes_all"]:
                return output
    
            # Refine based on critique
            output = generator.refine(
                task=task,
                previous_output=output,
                critique=critique["feedback"],
            )
    
        return output  # Best effort after max iterations
    """
    
    ## LangGraph Reflection
    """
    from langgraph.graph import StateGraph
    
    def build_reflection_graph():
        graph = StateGraph(ReflectionState)
    
        # Nodes
        graph.add_node("generate", generate_node)
        graph.add_node("reflect", reflect_node)
        graph.add_node("output", output_node)
    
        # Edges
        graph.add_edge("generate", "reflect")
        graph.add_conditional_edges(
            "reflect",
            should_continue,
            {
                "continue": "generate",  # Loop back
                "end": "output",
            }
        )
    
        return graph.compile()
    
    def should_continue(state):
        if state["iteration"] >= 3:
            return "end"
        if state["score"] >= 0.9:
            return "end"
        return "continue"
    """
    
    ## Separate Evaluator (More Robust)
    """
    # Use different model for evaluation to avoid self-bias
    generator = ChatOpenAI(model="gpt-4o")
    evaluator = ChatOpenAI(model="gpt-4o-mini")  # Different perspective
    
    # Or use specialized evaluators
    from langchain.evaluation import load_evaluator
    evaluator = load_evaluator("criteria", criteria="correctness")
    """
    

---
  #### **Name**
Guardrailed Autonomy
  #### **Description**
Constrained agents with safety boundaries
  #### **When**
Production systems, critical operations
  #### **Example**
    # GUARDRAILED AUTONOMY:
    
    """
    Production agents need multiple safety layers:
    1. Input validation
    2. Action constraints
    3. Output validation
    4. Cost limits
    5. Human escalation
    6. Rollback capability
    """
    
    ## Multi-Layer Guardrails
    """
    class GuardedAgent:
        def __init__(self, agent, config):
            self.agent = agent
            self.max_cost = config.get("max_cost_usd", 1.0)
            self.max_steps = config.get("max_steps", 10)
            self.allowed_actions = config.get("allowed_actions", [])
            self.require_approval = config.get("require_approval", [])
    
        async def execute(self, goal):
            total_cost = 0
            steps = 0
    
            while steps < self.max_steps:
                # Get next action
                action = await self.agent.plan_next(goal)
    
                # Validate action is allowed
                if action.name not in self.allowed_actions:
                    raise ActionNotAllowedError(action.name)
    
                # Check if approval needed
                if action.name in self.require_approval:
                    approved = await self.request_human_approval(action)
                    if not approved:
                        return {"status": "rejected", "action": action}
    
                # Estimate cost
                estimated_cost = self.estimate_cost(action)
                if total_cost + estimated_cost > self.max_cost:
                    raise CostLimitExceededError(total_cost)
    
                # Execute with rollback capability
                checkpoint = await self.save_checkpoint()
                try:
                    result = await self.agent.execute(action)
                    total_cost += self.actual_cost(action)
                    steps += 1
                except Exception as e:
                    await self.rollback_to(checkpoint)
                    raise
    
                if result.is_complete:
                    break
    
            return {"status": "complete", "total_cost": total_cost}
    """
    
    ## Least Privilege Principle
    """
    # Define minimal permissions per task type
    TASK_PERMISSIONS = {
        "research": ["web_search", "read_file"],
        "coding": ["read_file", "write_file", "run_tests"],
        "admin": ["all"],  # Rarely grant this
    }
    
    def create_scoped_agent(task_type):
        allowed = TASK_PERMISSIONS.get(task_type, [])
        tools = [t for t in ALL_TOOLS if t.name in allowed]
        return Agent(tools=tools)
    """
    
    ## Cost Control
    """
    # Context length grows quadratically in cost
    # Double context = 4x cost
    
    def trim_context(messages, max_tokens=4000):
        # Keep system message and recent messages
        system = messages[0]
        recent = messages[-10:]
    
        # Summarize middle if needed
        if len(messages) > 11:
            middle = messages[1:-10]
            summary = summarize(middle)
            return [system, summary] + recent
    
        return messages
    """
    

---
  #### **Name**
Durable Execution Pattern
  #### **Description**
Agents that survive failures and resume
  #### **When**
Long-running tasks, production systems, multi-day processes
  #### **Example**
    # DURABLE EXECUTION:
    
    """
    Production agents must:
    - Survive server restarts
    - Resume from exact point of failure
    - Handle hours/days of runtime
    - Allow human intervention mid-process
    
    LangGraph 1.0 provides this natively.
    """
    
    ## LangGraph Checkpointing
    """
    from langgraph.checkpoint.postgres import PostgresSaver
    from langgraph.graph import StateGraph
    
    # Production checkpointer (not MemorySaver!)
    checkpointer = PostgresSaver.from_conn_string(
        os.environ["POSTGRES_URL"]
    )
    
    # Build graph with checkpointing
    graph = StateGraph(AgentState)
    # ... add nodes and edges ...
    
    agent = graph.compile(checkpointer=checkpointer)
    
    # Each invocation saves state
    config = {"configurable": {"thread_id": "long-task-789"}}
    
    # Start task
    agent.invoke({"goal": complex_goal}, config)
    
    # If server dies, resume later:
    state = agent.get_state(config)
    if not state.is_complete:
        agent.invoke(None, config)  # Continues from checkpoint
    """
    
    ## Human-in-the-Loop Interrupts
    """
    # Pause at specific nodes
    agent = graph.compile(
        checkpointer=checkpointer,
        interrupt_before=["critical_action"],  # Pause before
        interrupt_after=["validation"],        # Pause after
    )
    
    # First invocation pauses at interrupt
    result = agent.invoke({"goal": goal}, config)
    
    # Human reviews state
    state = agent.get_state(config)
    if human_approves(state):
        # Continue from pause point
        agent.invoke(None, config)
    else:
        # Modify state and continue
        agent.update_state(config, {"approved": False})
        agent.invoke(None, config)
    """
    
    ## Time-Travel Debugging
    """
    # LangGraph stores full history
    history = list(agent.get_state_history(config))
    
    # Go back to any previous state
    past_state = history[5]
    agent.update_state(config, past_state.values)
    
    # Replay from that point with modifications
    agent.invoke(None, config)
    """
    

## Anti-Patterns


---
  #### **Name**
Unbounded Autonomy
  #### **Description**
Letting agents run without step/cost limits
  #### **Why**
    Agents can enter infinite loops, burn thousands in API costs, or
    take destructive actions. One startup spent $47 per support ticket.
    Without limits, you're gambling with resources.
    
  #### **Instead**
    Set hard limits: max steps, max cost, max time. Fail-safe to human
    escalation. Better to stop early than run forever.
    

---
  #### **Name**
Trusting Agent Outputs
  #### **Description**
Treating agent outputs as ground truth
  #### **Why**
    Agents hallucinate, fabricate, and confidently produce nonsense.
    An expense agent invented fake restaurant names when stuck.
    Outputs are proposals, not facts.
    
  #### **Instead**
    Validate all outputs. Use structured outputs with schemas.
    Require evidence/sources for claims. Human review for critical data.
    

---
  #### **Name**
General-Purpose Autonomy
  #### **Description**
Building agents that can "do anything"
  #### **Why**
    General agents fail at everything. Benchmarks show 14% success on
    complex tasks vs 78% for humans. The more general, the less reliable.
    
  #### **Instead**
    Build constrained, domain-specific agents. Do one thing well.
    Add capabilities only after proving reliability.
    

---
  #### **Name**
Silent Failures
  #### **Description**
Agents that fail without clear signals
  #### **Why**
    Autonomous agents can fail in subtle ways that corrupt data or
    leave tasks half-done. Without explicit failure handling, problems
    compound invisibly.
    
  #### **Instead**
    Explicit error states. Checkpoint before risky operations.
    Alert humans on failures. Never leave inconsistent state.
    

---
  #### **Name**
Demo-Driven Development
  #### **Description**
Building for impressive demos over reliable operation
  #### **Why**
    The gap between demo and production is where projects die. A working
    demo proves nothing about reliability, cost, or scale.
    
  #### **Instead**
    Build for the boring case. Handle errors, retries, edge cases.
    Measure success rate over 1000 runs, not 3 demos.
    