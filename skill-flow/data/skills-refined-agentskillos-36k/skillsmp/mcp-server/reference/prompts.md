# MCP Prompts Reference

Prompts define reusable prompt templates that help AI agents interact with your server consistently.

## Basic Prompt Definition

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My Server")

@mcp.prompt()
def task_assistant(name: str = "User") -> str:
    """Generate a task management assistant prompt."""
    return f"""You are a helpful task management assistant for {name}.
Your role is to help manage tasks efficiently by:
- Creating new tasks with clear descriptions
- Organizing tasks by priority and due date
- Tracking task completion status
- Providing reminders and suggestions

Always be helpful, concise, and focused on productivity."""
```

## Prompt with Multiple Parameters

```python
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt.

    Args:
        name: User's name
        style: Greeting style (friendly, formal, casual)
    """
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }

    return f"{styles.get(style, styles['friendly'])} for someone named {name}."
```

## Prompt with Title

```python
@mcp.prompt(title="Code Review Assistant")
def review_code(code: str, language: str = "python") -> str:
    """Generate a code review prompt."""
    return f"""Please review the following {language} code:

```{language}
{code}
```

Focus on:
1. Code quality and readability
2. Potential bugs or errors
3. Performance improvements
4. Best practices adherence"""
```

## Multi-Turn Conversation Prompt

```python
from mcp.server.fastmcp.prompts import base

@mcp.prompt(title="Debug Assistant")
def debug_error(error: str) -> list[base.Message]:
    """Generate a multi-turn debugging prompt."""
    return [
        base.UserMessage(f"I'm seeing this error: {error}"),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]
```

## Task-Specific Prompts

```python
@mcp.prompt(title="Task Creator")
def task_creator_prompt() -> str:
    """Generate a prompt for creating well-structured tasks."""
    return """Help the user create a well-structured task. Ask for:

1. **Title**: A clear, concise task title
2. **Description**: Detailed description of what needs to be done
3. **Priority**: Low, Medium, or High
4. **Due Date**: When the task should be completed
5. **Category**: Optional category/tag for organization

Guide the user to provide actionable, specific tasks rather than vague ones.
Example of a good task: "Review Q4 sales report and prepare summary by Friday"
Example of a bad task: "Do the thing"""
```

```python
@mcp.prompt(title="Task Analyzer")
def task_analyzer_prompt(tasks_json: str) -> str:
    """Generate a prompt for analyzing task data."""
    return f"""Analyze the following tasks and provide insights:

Tasks:
{tasks_json}

Please analyze:
1. Task distribution by status (pending, completed, etc.)
2. Priority distribution
3. Any overdue tasks
4. Suggestions for task prioritization
5. Productivity insights"""
```

## Prompt with Icons

```python
from mcp.server.fastmcp import FastMCP, Icon

prompt_icon = Icon(src="assistant-icon.png", mimeType="image/png")

@mcp.prompt(title="AI Assistant", icons=[prompt_icon])
def ai_assistant() -> str:
    """Generate an AI assistant prompt with custom icon."""
    return "You are a helpful AI assistant."
```

## Using Prompts (Client Side)

```python
# List available prompts
prompts = await session.list_prompts()
for prompt in prompts.prompts:
    print(f"Name: {prompt.name}, Description: {prompt.description}")

# Get a prompt with arguments
prompt = await session.get_prompt(
    "task_assistant",
    arguments={"name": "Alice"}
)

# Access the prompt content
for message in prompt.messages:
    print(f"Role: {message.role}, Content: {message.content}")
```

## Prompt Templates for Todo App

### System Prompt

```python
@mcp.prompt(title="Todo System")
def todo_system_prompt(user_name: str) -> str:
    """System prompt for todo chatbot."""
    return f"""You are a task management assistant for {user_name}.

Available tools:
- add_task: Create new tasks
- list_tasks: View existing tasks
- complete_task: Mark tasks as done
- delete_task: Remove tasks
- update_task: Modify task details

Guidelines:
1. Always confirm actions with the user
2. Summarize changes after performing actions
3. Suggest task organization when appropriate
4. Be concise but helpful"""
```

### Help Prompt

```python
@mcp.prompt(title="Help Guide")
def help_prompt() -> str:
    """Generate help information for users."""
    return """Here's what I can help you with:

**Create Tasks**
Say things like:
- "Add a task to buy groceries"
- "Create a high priority task for the meeting"
- "New task: Review documents by Friday"

**View Tasks**
- "Show my tasks"
- "List pending tasks"
- "What tasks are due today?"

**Complete Tasks**
- "Mark task 1 as done"
- "Complete the groceries task"

**Delete Tasks**
- "Delete task 3"
- "Remove the cancelled meeting task"

**Update Tasks**
- "Change priority of task 1 to high"
- "Update task 2 description"

Just tell me what you need!"""
```

## Best Practices

1. **Clear purpose** - Each prompt should have a specific use case
2. **Parameterize** - Use parameters for customization
3. **Include examples** - Help AI understand expected behavior
4. **Be concise** - Long prompts can reduce effectiveness
5. **Test thoroughly** - Verify prompts produce desired responses
6. **Document arguments** - Clear docstrings for parameters
