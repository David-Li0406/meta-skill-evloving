---
name: browser-use
description: Web automation using LLMs and Playwright. Enables agents to autonomously navigate web pages, interact with elements, and complete complex tasks.
---

# Browser-Use Skill

Browser-Use is a powerful library that allows AI agents to control web browsers (Chromium, Chrome, Edge) using LLMs. It handles DOM processing, element interaction, and vision-based decision making.

## Core Capabilities

- **Autonomous Navigation**: Agents can navigate to any URL and follow links.
- **Element Interaction**: Clicking, typing, scrolling, and form filling.
- **Vision Integration**: Uses screenshots to help the agent understand the page layout.
- **DOM Extraction**: Intelligent extraction of text and structured data from pages.
- **Authentication**: Can use existing browser profiles to stay logged into websites.

## Installation

The skill requires Python 3.11+ and the `browser-use` package.

```powershell
pip install browser-use playwright
playwright install chromium
```

## Basic Usage

To run an agent, you need an LLM provider (OpenAI, Anthropic, Google, etc.) and a task.

```python
from browser_use import Agent, ChatOpenAI
import asyncio

async def main():
    agent = Agent(
        task="Find the latest news about SpaceX on Google",
        llm=ChatOpenAI(model="gpt-4o"),
    )
    result = await agent.run()
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

## Best Practices

- **Be Specific**: Give the agent clear, step-by-step instructions in the task string.
- **Use Vision**: Set `use_vision=True` when the page layout is complex or requires visual confirmation.
- **Wait for Actions**: The agent automatically waits for pages to load, but you can add explicit waits in the task if needed.
- **Browser Profiles**: Use `user_data_dir` to preserve login sessions and cookies.
- **Sandboxes**: For production, consider using the `@sandbox` wrapper provided by Browser-Use Cloud.

## Troubleshooting

- **Cloudflare/Captchas**: If blocked, try using `headless=False` or connecting to a real browser instance.
- **Element Not Found**: Ensure the agent has enough steps (`max_steps`) and that the page has fully loaded.
- **Timeout**: Adjust `step_timeout` or `llm_timeout` for slow pages or complex reasoning.

## Related Resources

- [Browser-Use Documentation](https://docs.browser-use.com/)
- [GitHub Repository](https://github.com/browser-use/browser-use)
