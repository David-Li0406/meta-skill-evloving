# CrewAI

## Patterns


---
  #### **Name**
Basic Crew with YAML Config
  #### **Description**
Define agents and tasks in YAML (recommended)
  #### **When To Use**
Any CrewAI project
  #### **Implementation**
    # config/agents.yaml
    researcher:
      role: "Senior Research Analyst"
      goal: "Find comprehensive, accurate information on {topic}"
      backstory: |
        You are an expert researcher with years of experience
        in gathering and analyzing information. You're known
        for your thorough and accurate research.
      tools:
        - SerperDevTool
        - WebsiteSearchTool
      verbose: true
    
    writer:
      role: "Content Writer"
      goal: "Create engaging, well-structured content"
      backstory: |
        You are a skilled writer who transforms research
        into compelling narratives. You focus on clarity
        and engagement.
      verbose: true
    
    # config/tasks.yaml
    research_task:
      description: |
        Research the topic: {topic}
    
        Focus on:
        1. Key facts and statistics
        2. Recent developments
        3. Expert opinions
        4. Contrarian viewpoints
    
        Be thorough and cite sources.
      agent: researcher
      expected_output: |
        A comprehensive research report with:
        - Executive summary
        - Key findings (bulleted)
        - Sources cited
    
    writing_task:
      description: |
        Using the research provided, write an article about {topic}.
    
        Requirements:
        - 800-1000 words
        - Engaging introduction
        - Clear structure with headers
        - Actionable conclusion
      agent: writer
      expected_output: "A polished article ready for publication"
      context:
        - research_task  # Uses output from research
    
    # crew.py
    from crewai import Agent, Task, Crew, Process
    from crewai.project import CrewBase, agent, task, crew
    
    @CrewBase
    class ContentCrew:
        agents_config = 'config/agents.yaml'
        tasks_config = 'config/tasks.yaml'
    
        @agent
        def researcher(self) -> Agent:
            return Agent(config=self.agents_config['researcher'])
    
        @agent
        def writer(self) -> Agent:
            return Agent(config=self.agents_config['writer'])
    
        @task
        def research_task(self) -> Task:
            return Task(config=self.tasks_config['research_task'])
    
        @task
        def writing_task(self) -> Task:
            return Task(config=self.tasks_config['writing_task'])
    
        @crew
        def crew(self) -> Crew:
            return Crew(
                agents=self.agents,
                tasks=self.tasks,
                process=Process.sequential,
                verbose=True
            )
    
    # main.py
    crew = ContentCrew()
    result = crew.crew().kickoff(inputs={"topic": "AI Agents in 2025"})
    

---
  #### **Name**
Hierarchical Process
  #### **Description**
Manager agent delegates to workers
  #### **When To Use**
Complex tasks needing coordination
  #### **Implementation**
    from crewai import Crew, Process
    
    # Define specialized agents
    researcher = Agent(
        role="Research Specialist",
        goal="Find accurate information",
        backstory="Expert researcher..."
    )
    
    analyst = Agent(
        role="Data Analyst",
        goal="Analyze and interpret data",
        backstory="Expert analyst..."
    )
    
    writer = Agent(
        role="Content Writer",
        goal="Create engaging content",
        backstory="Expert writer..."
    )
    
    # Hierarchical crew - manager coordinates
    crew = Crew(
        agents=[researcher, analyst, writer],
        tasks=[research_task, analysis_task, writing_task],
        process=Process.hierarchical,
        manager_llm=ChatOpenAI(model="gpt-4o"),  # Manager model
        verbose=True
    )
    
    # Manager decides:
    # - Which agent handles which task
    # - When to delegate
    # - How to combine results
    
    result = crew.kickoff()
    

---
  #### **Name**
Planning Feature
  #### **Description**
Generate execution plan before running
  #### **When To Use**
Complex workflows needing structure
  #### **Implementation**
    from crewai import Crew, Process
    
    # Enable planning
    crew = Crew(
        agents=[researcher, writer, reviewer],
        tasks=[research, write, review],
        process=Process.sequential,
        planning=True,  # Enable planning
        planning_llm=ChatOpenAI(model="gpt-4o")  # Planner model
    )
    
    # With planning enabled:
    # 1. CrewAI generates step-by-step plan
    # 2. Plan is injected into each task
    # 3. Agents see overall structure
    # 4. More consistent results
    
    result = crew.kickoff()
    
    # Access the plan
    print(crew.plan)
    

---
  #### **Name**
Memory Configuration
  #### **Description**
Enable agent memory for context
  #### **When To Use**
Multi-turn or complex workflows
  #### **Implementation**
    from crewai import Crew
    
    # Memory types:
    # - Short-term: Within task execution
    # - Long-term: Across executions
    # - Entity: About specific entities
    
    crew = Crew(
        agents=[...],
        tasks=[...],
        memory=True,  # Enable all memory types
        verbose=True
    )
    
    # Custom memory config
    from crewai.memory import LongTermMemory, ShortTermMemory
    
    crew = Crew(
        agents=[...],
        tasks=[...],
        memory=True,
        long_term_memory=LongTermMemory(
            storage=CustomStorage()  # Custom backend
        ),
        short_term_memory=ShortTermMemory(
            storage=CustomStorage()
        ),
        embedder={
            "provider": "openai",
            "config": {"model": "text-embedding-3-small"}
        }
    )
    
    # Memory helps agents:
    # - Remember previous interactions
    # - Build on past work
    # - Maintain consistency
    

---
  #### **Name**
Flows for Complex Workflows
  #### **Description**
Event-driven orchestration with state
  #### **When To Use**
Complex, multi-stage workflows
  #### **Implementation**
    from crewai.flow.flow import Flow, listen, start, and_, or_, router
    
    class ContentFlow(Flow):
        # State persists across steps
        model_config = {"extra": "allow"}
    
        @start()
        def gather_requirements(self):
            """First step - gather inputs."""
            self.topic = self.inputs.get("topic", "AI")
            self.style = self.inputs.get("style", "professional")
            return {"topic": self.topic}
    
        @listen(gather_requirements)
        def research(self, requirements):
            """Research after requirements gathered."""
            research_crew = ResearchCrew()
            result = research_crew.crew().kickoff(
                inputs={"topic": requirements["topic"]}
            )
            self.research = result.raw
            return result
    
        @listen(research)
        def write_content(self, research_result):
            """Write after research complete."""
            writing_crew = WritingCrew()
            result = writing_crew.crew().kickoff(
                inputs={
                    "research": self.research,
                    "style": self.style
                }
            )
            return result
    
        @router(write_content)
        def quality_check(self, content):
            """Route based on quality."""
            if self.needs_revision(content):
                return "revise"
            return "publish"
    
        @listen("revise")
        def revise_content(self):
            """Revision flow."""
            # Re-run writing with feedback
            pass
    
        @listen("publish")
        def publish_content(self):
            """Final publishing."""
            return {"status": "published", "content": self.content}
    
    # Run flow
    flow = ContentFlow()
    result = flow.kickoff(inputs={"topic": "AI Agents"})
    

---
  #### **Name**
Custom Tools
  #### **Description**
Create tools for agents
  #### **When To Use**
Agents need external capabilities
  #### **Implementation**
    from crewai.tools import BaseTool
    from pydantic import BaseModel, Field
    
    # Method 1: Class-based tool
    class SearchInput(BaseModel):
        query: str = Field(..., description="Search query")
    
    class WebSearchTool(BaseTool):
        name: str = "web_search"
        description: str = "Search the web for information"
        args_schema: type[BaseModel] = SearchInput
    
        def _run(self, query: str) -> str:
            # Implementation
            results = search_api.search(query)
            return format_results(results)
    
    # Method 2: Function decorator
    from crewai import tool
    
    @tool("Database Query")
    def query_database(sql: str) -> str:
        """Execute SQL query and return results."""
        return db.execute(sql)
    
    # Assign tools to agents
    researcher = Agent(
        role="Researcher",
        goal="Find information",
        backstory="...",
        tools=[WebSearchTool(), query_database]
    )
    

## Anti-Patterns


---
  #### **Name**
Vague Agent Roles
  #### **Description**
Generic roles without clear expertise
  #### **Why Bad**
    Agent doesn't know its specialty.
    Overlapping responsibilities.
    Poor task delegation.
    
  #### **What To Do Instead**
    Be specific:
    - "Senior React Developer" not "Developer"
    - "Financial Analyst specializing in crypto" not "Analyst"
    Include specific skills in backstory.
    

---
  #### **Name**
Missing Expected Outputs
  #### **Description**
Tasks without clear expected_output
  #### **Why Bad**
    Agent doesn't know done criteria.
    Inconsistent outputs.
    Hard to chain tasks.
    
  #### **What To Do Instead**
    Always specify expected_output:
    expected_output: |
      A JSON object with:
      - summary: string (100 words max)
      - key_points: list of strings
      - confidence: float 0-1
    

---
  #### **Name**
Too Many Agents
  #### **Description**
Creating agent for every small task
  #### **Why Bad**
    Coordination overhead.
    Inconsistent communication.
    Slower execution.
    
  #### **What To Do Instead**
    3-5 agents with clear roles.
    One agent can handle multiple related tasks.
    Use tools instead of agents for simple actions.
    

---
  #### **Name**
No Task Context
  #### **Description**
Tasks don't reference previous outputs
  #### **Why Bad**
    Agents work in isolation.
    Lost information between tasks.
    Redundant work.
    
  #### **What To Do Instead**
    Use context in task config:
    writing_task:
      context:
        - research_task
        - analysis_task
    