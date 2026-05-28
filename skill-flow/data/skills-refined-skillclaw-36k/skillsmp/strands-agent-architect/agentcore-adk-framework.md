Using Google Agent Development Kit (ADK) with Amazon Bedrock AgentCore

Amazon Bedrock AgentCore provides a flexible, framework-agnostic platform for deploying and operating AI agents. This design enables the integration of various open-source agentic frameworks, including the Google Agent Development Kit (ADK), and supports a wide range of foundation models, such as Google's Gemini. The core service facilitating this integration is the AgentCore Runtime, a secure, serverless environment purpose-built for deploying and scaling AI agents.

Core Principles of Integration

The ability to use Google ADK and Gemini models within AgentCore stems from two fundamental characteristics of the platform: framework agnosticism and model flexibility.

Framework Agnosticism

AgentCore Runtime is engineered to support any open-source or custom agent framework. It allows developers to transform local agent code into cloud-native deployments with minimal code changes. The documentation explicitly lists Google ADK as a compatible framework, alongside others like CrewAI, LangGraph, and LlamaIndex. This ensures that developers are not locked into a specific toolkit and can leverage the flexibility of open-source solutions while benefiting from AgentCore's enterprise-grade security and reliability.

Model Flexibility

AgentCore Runtime is compatible with any Large Language Model (LLM), including those available within or outside of Amazon Bedrock. The platform supports models from providers such as Google, OpenAI, Anthropic, and Meta. This flexibility allows agents built with frameworks like Google ADK to be powered by state-of-the-art models like Gemini.

Integration Example: Google Agent Development Kit (ADK)

AgentCore enables the deployment of agents constructed with the Google ADK. The integration is achieved by wrapping the ADK agent logic within the BedrockAgentCoreApp, which serves as the entry point for the AgentCore Runtime.

A full code example for this integration is available at the following GitHub repository: https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/03-integrations/agentic-frameworks/adk.

Code Implementation

The following code snippet demonstrates the core pattern for integrating a Google ADK agent with the AgentCore Runtime.

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types
import asyncio
import os

# adapted form https://google.github.io/adk-docs/tools/built-in-tools/#google-search
async def main(query: str):
    # [Implementation of the main agent logic using ADK components]
    ...

# Integration with Bedrock AgentCore
from bedrock_agentcore.runtime import BedrockAgentCoreApp
app = BedrockAgentCoreApp()

@app.entrypoint
async def agent_invocation(payload, context):
    logger.debug(f"Received payload: {payload}")
    query = payload.get("prompt", "How can I help you today?")
    
    try:
        result = await main(query)
        logger.debug("Agent execution completed successfully")
        return {"result": result.final_output}
    except Exception as e:
        logger.error(f"Error during agent execution: {e}", exc_info=True)
        return {"result": f"Error: {str(e)}"}

# Run the app when imported
if __name__== "__main__":
    app.run()


Key Components of the Integration:

* Google ADK Imports: The agent utilizes standard ADK components like Agent, Runner, and InMemorySessionService to define its core behavior and tools (google_search).
* BedrockAgentCoreApp: The BedrockAgentCoreApp from the bedrock_agentcore.runtime library acts as the interface between the custom agent code and the managed AgentCore Runtime environment.
* @app.entrypoint Decorator: This decorator designates the agent_invocation function as the primary handler for incoming requests to the deployed agent. The function receives a payload (containing the user prompt) and a context object from the runtime.
* Execution Logic: Inside the entry point, the function extracts the user's query from the payload and passes it to the main ADK agent logic for processing. The final output from the ADK agent is then returned as the response.

Using the Gemini Model

Agents deployed on AgentCore Runtime, including those built with Google ADK, can be configured to use any supported foundation model. The following example illustrates how to initialize and use a Google Gemini model within an agent.

Code Implementation

This snippet demonstrates initializing a Gemini model using the langchain.chat_models library, a common pattern for integrating various LLMs.

import os
from langchain.chat_models import init_chat_model

# Use your Google API key to initialize the chat model
os.environ["GOOGLE_API_KEY"] = "..."

llm = init_chat_model("google_genai:gemini-2.0-flash")


Implementation Details:

* API Key: Access to the Gemini model requires a GOOGLE_API_KEY, which should be set as an environment variable for secure access.
* Model Initialization: The init_chat_model function is used to instantiate the language model.
* Model Identifier: The string "google_genai:gemini-2.0-flash" specifies the exact provider and model to be used, in this case, the gemini-2.0-flash model from Google's generative AI services.