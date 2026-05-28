# Crewai - Sharp Edges

## Context Window Overflow

### **Id**
context-window-overflow
### **Summary**
Agent conversation exceeds context window
### **Severity**
high
### **Situation**
Agent stops mid-task or gives truncated responses
### **Why**
  Long tasks accumulate messages.
  No automatic trimming by default.
  LLM hits context limit.
  
### **Solution**
  from crewai import Agent
  
  # Enable automatic context management
  agent = Agent(
      role="Researcher",
      goal="Find information",
      backstory="...",
      respect_context_window=True,  # Enable trimming
      max_rpm=10,  # Rate limiting
      max_iter=15,  # Max iterations per task
  )
  
  # For verbose tasks, summarize periodically
  # Use memory to store key facts, not full conversation
  
  # Task-level control
  task = Task(
      description="...",
      agent=agent,
      max_iterations=10  # Limit per task
  )
  
  # Monitor context usage
  # CrewAI will summarize when needed with respect_context_window=True
  
### **Symptoms**
  - Truncated responses
  - I apologize, I seem to have lost context
  - Repeated information
### **Detection Pattern**
respect_context_window|max_iter

## Delegation Loops

### **Id**
delegation-loops
### **Summary**
Agents delegate back and forth infinitely
### **Severity**
high
### **Situation**
Execution never completes, burns tokens
### **Why**
  Agent A delegates to Agent B.
  Agent B can't complete, delegates back.
  No loop detection.
  
### **Solution**
  # Control delegation
  agent = Agent(
      role="Specialist",
      goal="...",
      backstory="...",
      allow_delegation=False  # Prevent delegation
  )
  
  # Or limit delegation depth
  crew = Crew(
      agents=[...],
      tasks=[...],
      max_delegation_depth=2  # Max 2 levels of delegation
  )
  
  # Clear task ownership
  task = Task(
      description="...",
      agent=specific_agent,  # Explicit assignment
      allow_delegation=False  # Task-level control
  )
  
  # In hierarchical process, manager controls delegation
  crew = Crew(
      process=Process.hierarchical,
      manager_llm=ChatOpenAI(model="gpt-4o"),
      # Manager decides delegation, not agents
  )
  
### **Symptoms**
  - Execution never ends
  - Same task passed between agents
  - Token usage spikes
### **Detection Pattern**
allow_delegation|delegation

## Missing Task Context

### **Id**
missing-task-context
### **Summary**
Tasks don't receive previous task outputs
### **Severity**
high
### **Situation**
Agent doesn't have needed information
### **Why**
  Tasks run independently by default.
  Output not passed to next task.
  Must explicitly set context.
  
### **Solution**
  # WRONG - no context
  research_task = Task(
      description="Research AI trends",
      agent=researcher,
      expected_output="Research report"
  )
  
  writing_task = Task(
      description="Write article",  # Doesn't know about research!
      agent=writer,
      expected_output="Article"
  )
  
  # CORRECT - with context
  writing_task = Task(
      description="Write article based on the research",
      agent=writer,
      expected_output="Article",
      context=[research_task]  # Receives research output
  )
  
  # YAML config equivalent
  # tasks.yaml
  writing_task:
    description: "Write article based on research"
    agent: writer
    context:
      - research_task
    expected_output: "Article"
  
  # Multiple contexts
  final_task = Task(
      description="Combine all work",
      agent=editor,
      context=[research_task, writing_task, review_task]
  )
  
### **Symptoms**
  - Agent says "I don't have that information"
  - Repeating work already done
  - Missing details from previous steps
### **Detection Pattern**
context.*=.*\[\]|Task\([^)]*\)(?!.*context)

## Yaml Config Not Loading

### **Id**
yaml-config-not-loading
### **Summary**
YAML configuration ignored
### **Severity**
medium
### **Situation**
Agent uses defaults instead of config
### **Why**
  Wrong file path.
  YAML syntax errors.
  Config keys don't match.
  
### **Solution**
  # Correct file structure
  my_crew/
  ├── config/
  │   ├── agents.yaml
  │   └── tasks.yaml
  ├── crew.py
  └── main.py
  
  # crew.py
  from crewai.project import CrewBase, agent, task, crew
  
  @CrewBase
  class MyCrew:
      # Paths relative to this file
      agents_config = 'config/agents.yaml'
      tasks_config = 'config/tasks.yaml'
  
      @agent
      def researcher(self) -> Agent:
          # Key must match YAML key
          return Agent(config=self.agents_config['researcher'])
  
  # YAML key matching
  # agents.yaml
  researcher:  # This key
    role: "Researcher"
    ...
  
  # Must match in crew.py
  @agent
  def researcher(self) -> Agent:  # Same name
      return Agent(config=self.agents_config['researcher'])  # Same key
  
  # Debug: Print config to verify loading
  print(self.agents_config)
  
### **Symptoms**
  - Default agent behavior
  - Missing tools or settings
  - "KeyError" on config access
### **Detection Pattern**
agents_config|tasks_config

## Tool Not Called

### **Id**
tool-not-called
### **Summary**
Agent has tool but doesn't use it
### **Severity**
medium
### **Situation**
Agent tries to answer without using available tool
### **Why**
  Tool description unclear.
  Agent doesn't know when to use it.
  Tool not appropriate for task.
  
### **Solution**
  # Good tool description
  @tool("Search Web")
  def search_web(query: str) -> str:
      """
      Search the web for current information.
  
      Use this tool when you need to:
      - Find recent news or events
      - Look up facts you're unsure about
      - Research topics you don't have data on
  
      Args:
          query: The search query (be specific)
  
      Returns:
          Search results with titles and snippets
      """
      return search_api.search(query)
  
  # Explicit instruction in backstory
  researcher = Agent(
      role="Research Analyst",
      goal="Find accurate, current information",
      backstory="""
      You are a meticulous researcher who ALWAYS uses
      the search_web tool to verify information before
      including it in your reports. Never rely on memory
      alone for facts and statistics.
      """,
      tools=[search_web]
  )
  
  # Task-level instruction
  task = Task(
      description="""
      Research current AI trends.
  
      IMPORTANT: Use the search_web tool to find
      recent articles and data. Do not rely on
      training data alone.
      """,
      agent=researcher
  )
  
### **Symptoms**
  - Agent makes up facts
  - "Based on my knowledge" instead of search
  - Outdated information
### **Detection Pattern**
tools.*=.*\[\]|@tool

## Process Mismatch

### **Id**
process-mismatch
### **Summary**
Wrong process type for workflow
### **Severity**
medium
### **Situation**
Suboptimal execution or coordination issues
### **Why**
  Sequential when parallel would help.
  Hierarchical when tasks are independent.
  No consideration of dependencies.
  
### **Solution**
  from crewai import Process
  
  # SEQUENTIAL: Tasks depend on each other
  # Task A → Task B → Task C
  crew = Crew(
      process=Process.sequential,
      ...
  )
  # Use when: Linear pipeline, each step needs previous output
  
  # HIERARCHICAL: Manager coordinates workers
  crew = Crew(
      process=Process.hierarchical,
      manager_llm=ChatOpenAI(model="gpt-4o"),
      ...
  )
  # Use when: Complex coordination, dynamic task assignment
  
  # For independent tasks, use Flows
  from crewai.flow.flow import Flow, listen, start
  
  class ParallelFlow(Flow):
      @start()
      def begin(self):
          return self.inputs
  
      @listen(begin)
      async def task_a(self, inputs):
          # Runs in parallel with task_b
          pass
  
      @listen(begin)
      async def task_b(self, inputs):
          # Runs in parallel with task_a
          pass
  
      @listen(and_(task_a, task_b))
      def combine(self, results):
          # Runs after both complete
          pass
  
  # Decision guide:
  # - Pipeline? → Sequential
  # - Need coordinator? → Hierarchical
  # - Independent + combine? → Flows with and_()
  
### **Symptoms**
  - Unnecessary waiting
  - Coordination overhead
  - Wrong task order
### **Detection Pattern**
Process\.