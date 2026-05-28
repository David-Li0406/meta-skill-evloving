import asyncio
import os
from browser_use import Agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables (OPENAI_API_KEY)
load_dotenv()

async def run_search_task():
    """
    Example task: Search for the latest version of Python on the official website.
    """
    # Initialize the LLM
    llm = ChatOpenAI(model="gpt-4o")

    # Define the task
    task = "Go to python.org and find the latest stable release version number."

    # Create the agent
    agent = Agent(
        task=task,
        llm=llm,
        use_vision=True
    )

    # Run the agent
    history = await agent.run(max_steps=10)
    
    # Print the final result
    print("\nFinal Result:")
    print(history.final_result())

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("Please set the OPENAI_API_KEY environment variable.")
    else:
        asyncio.run(run_search_task())
