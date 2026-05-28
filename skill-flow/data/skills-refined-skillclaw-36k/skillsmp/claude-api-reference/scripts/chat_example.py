#!/usr/bin/env python3
"""
Interactive Claude Chat Example
Supports multi-turn conversations and streaming responses
"""

import anthropic
from typing import Optional


class ClaudeChat:
    """Claude conversation manager"""
    
    def __init__(
        self,
        model: str = "claude-sonnet-4-5-20250929",
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096
    ):
        self.client = anthropic.Anthropic()
        self.model = model
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self.messages = []
    
    def chat(self, user_message: str, stream: bool = True) -> str:
        """
        Send message and get response
        
        Args:
            user_message: User's message
            stream: Whether to use streaming response
            
        Returns:
            Claude's response
        """
        self.messages.append({"role": "user", "content": user_message})
        
        kwargs = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "messages": self.messages
        }
        
        if self.system_prompt:
            kwargs["system"] = self.system_prompt
        
        if stream:
            response_text = self._stream_response(**kwargs)
        else:
            message = self.client.messages.create(**kwargs)
            response_text = message.content[0].text
        
        self.messages.append({"role": "assistant", "content": response_text})
        return response_text
    
    def _stream_response(self, **kwargs) -> str:
        """Stream response with real-time output"""
        response_text = ""
        
        with self.client.messages.stream(**kwargs) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
                response_text += text
        
        print()  # New line
        return response_text
    
    def reset(self):
        """Clear conversation history"""
        self.messages = []
    
    def get_history(self) -> list:
        """Get conversation history"""
        return self.messages.copy()


def main():
    """Interactive chat main program"""
    print("Claude Interactive Chat (type 'quit' to exit, 'reset' to clear history)")
    print("-" * 50)
    
    chat = ClaudeChat(
        system_prompt="You are a friendly and professional AI assistant."
    )
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == "quit":
                print("Goodbye!")
                break
            
            if user_input.lower() == "reset":
                chat.reset()
                print("Conversation history cleared")
                continue
            
            print("\nClaude: ", end="")
            chat.chat(user_input, stream=True)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    main()