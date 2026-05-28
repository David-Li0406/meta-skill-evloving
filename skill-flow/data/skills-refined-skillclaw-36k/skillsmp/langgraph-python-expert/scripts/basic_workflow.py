#!/usr/bin/env python3
"""
Basic LangGraph Workflow Example
A simple chatbot with state persistence
"""

from typing import TypedDict, List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
import os

# State definition
class ChatState(TypedDict):
    messages: List[BaseMessage]
    user_name: str
    conversation_count: int

def main():
    """Main function to run the basic workflow"""

    # Initialize LLM
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.7
    )

    # Define node functions
    def chat_node(state: ChatState) -> ChatState:
        """Process chat messages with the LLM"""
        messages = state["messages"]

        # Add system message if this is the start
        if len(messages) == 1 and messages[0].type == "human":
            system_msg = AIMessage(
                content=f"Hello {state['user_name']}! I'm your AI assistant. "
                       f"This is conversation #{state['conversation_count']}. "
                       "How can I help you today?"
            )
            messages = [system_msg] + messages

        # Get LLM response
        response = llm.invoke(messages)

        return {
            "messages": messages + [response],
            "conversation_count": state["conversation_count"] + 1
        }

    def should_continue(state: ChatState) -> str:
        """Determine if conversation should continue"""
        last_message = state["messages"][-1]

        # Check for goodbye messages
        goodbye_keywords = ["goodbye", "bye", "exit", "quit", "see you"]
        if any(keyword in last_message.content.lower() for keyword in goodbye_keywords):
            return END

        return "continue"

    def end_conversation(state: ChatState) -> ChatState:
        """Add a goodbye message when ending"""
        goodbye_msg = AIMessage(
            content=f"Goodbye {state['user_name']}! "
                   f"We had {state['conversation_count']} exchanges. "
                   "Feel free to come back anytime!"
        )

        return {
            "messages": state["messages"] + [goodbye_msg]
        }

    # Build the workflow
    print("Building LangGraph workflow...")
    workflow = StateGraph(ChatState)

    # Add nodes
    workflow.add_node("chat", chat_node)
    workflow.add_node("end", end_conversation)

    # Add edges
    workflow.set_entry_point("chat")
    workflow.add_conditional_edges(
        "chat",
        should_continue,
        {
            "continue": "chat",
            "__end__": "end"
        }
    )
    workflow.add_edge("end", END)

    # Add memory for persistence
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)

    print("Workflow compiled successfully!")
    print("\n" + "="*50)
    print("LANGGRAPH CHATBOT DEMO")
    print("="*50)
    print("Type 'quit', 'exit', or 'bye' to end the conversation")
    print("-"*50)

    # Interactive chat loop
    user_name = input("What's your name? ").strip()
    if not user_name:
        user_name = "User"

    # Create thread configuration for persistence
    thread_id = f"chat-{user_name.lower()}-{hash(user_name)}"
    config = {"configurable": {"thread_id": thread_id}}

    # Initial state
    initial_state = {
        "messages": [],
        "user_name": user_name,
        "conversation_count": 1
    }

    print(f"\nHello {user_name}! I'm ready to chat.")
    print("Your conversation will be saved and can be resumed.")
    print("-"*50)

    try:
        while True:
            # Get user input
            user_input = input("\nYou: ").strip()

            if not user_input:
                continue

            # Add user message to state
            current_state = {
                "messages": [HumanMessage(content=user_input)],
                "user_name": user_name,
                "conversation_count": initial_state["conversation_count"]
            }

            # Run the workflow
            print("\nAssistant: ", end="", flush=True)

            # Stream the response for better UX
            for chunk in app.stream(current_state, config):
                for node_name, node_output in chunk.items():
                    if "messages" in node_output:
                        # Get the last message (AI response)
                        messages = node_output["messages"]
                        if messages and messages[-1].type == "ai":
                            print(messages[-1].content, end="", flush=True)

            print()  # New line after response

            # Check if conversation ended
            state = app.get_state(config)
            if state and state.values.get("messages"):
                last_message = state.values["messages"][-1]
                if "goodbye" in last_message.content.lower():
                    break

    except KeyboardInterrupt:
        print("\n\nGoodbye! Thanks for chatting!")
    except Exception as e:
        print(f"\nError occurred: {e}")

    print("\n" + "="*50)
    print("Conversation ended. Your chat history has been saved.")
    print(f"Thread ID: {thread_id}")
    print("You can resume this conversation later using the same thread ID.")
    print("="*50)

if __name__ == "__main__":
    # Check for required environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is required")
        print("Please set it using: export OPENAI_API_KEY='your-api-key'")
        exit(1)

    main()