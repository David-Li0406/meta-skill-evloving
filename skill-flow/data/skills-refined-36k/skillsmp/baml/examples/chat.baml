// Multi-turn Chat Example
// Demonstrates: message history, role tags, template strings, streaming

class Message {
    role "user" | "assistant"
    content string
}

class ChatResponse {
    response string
    suggested_followups string[] @description("2-3 suggested follow-up questions")
}

// Reusable system prompt
template_string SystemPrompt() #"
    {{ _.role("system") }}
    You are a helpful assistant. Be concise and accurate.
    If you don't know something, say so.
"#

// Reusable message formatter
template_string FormatMessages(messages: Message[]) #"
    {% for msg in messages %}
        {{ _.role(msg.role) }}
        {{ msg.content }}
    {% endfor %}
"#

function Chat(messages: Message[]) -> string {
    client "openai/gpt-4o"
    prompt #"
        {{ SystemPrompt() }}
        {{ FormatMessages(messages) }}
    "#
}

function ChatWithFollowups(messages: Message[]) -> ChatResponse {
    client "openai/gpt-4o"
    prompt #"
        {{ SystemPrompt() }}
        {{ FormatMessages(messages) }}

        {{ _.role("user") }}
        Respond to the conversation, then suggest follow-up questions.

        {{ ctx.output_format }}
    "#
}

// Agent-style chat with tool hints
enum ToolChoice {
    SEARCH @description("Search the web for current information")
    CALCULATE @description("Perform mathematical calculations")
    CODE @description("Write or analyze code")
    NONE @description("No tool needed, respond directly")
}

class AgentResponse {
    tool_needed ToolChoice
    tool_input string? @description("Input for the tool, if applicable")
    direct_response string? @description("Response if no tool needed")
}

function AgentChat(messages: Message[]) -> AgentResponse {
    client "openai/gpt-4o"
    prompt #"
        {{ _.role("system") }}
        You are an AI assistant with access to tools.
        Decide if you need a tool to answer, or can respond directly.

        {{ FormatMessages(messages) }}

        {{ ctx.output_format }}
    "#
}

// Tests
test SimpleChat {
    functions [Chat]
    args {
        messages [
            {
                role "user"
                content "What's the capital of France?"
            }
        ]
    }
}

test MultiTurnChat {
    functions [ChatWithFollowups]
    args {
        messages [
            {
                role "user"
                content "What's Python?"
            },
            {
                role "assistant"
                content "Python is a programming language."
            },
            {
                role "user"
                content "How do I install it?"
            }
        ]
    }
}
