---
name: analogy-generator
description: Generate clear, creative, and memorable analogies to explain complex technical concepts. Use this skill when the user asks to "explain like I'm 5", "give me an analogy", or clarify abstract ideas.
source: custom/gemini-cli-ultimate
license: MIT
---

This skill guides the creation of vivid, relatable analogies to demystify complex topics.

## Goal
Transform abstract or technical concepts into concrete, familiar scenarios that the user can instantly grasp.

## Guidelines

1.  **Identify the Core Mechanism**: Isolate the fundamental logic or relationship in the complex concept (e.g., "API is a waiter", "DNS is a phonebook").
2.  **Choose a Familiar Domain**: Select a source domain the user likely understands (cooking, driving, sports, office work, nature).
3.  **Map the Elements**: Clearly connect the parts of the analogy to the parts of the concept.
    *   *Analogy*: "The waiter takes your order to the kitchen and brings back food."
    *   *Mapping*: Waiter = API, Order = Request, Kitchen = Server, Food = Response.
4.  **Verify the Fit**: Ensure the analogy holds up under basic scrutiny but acknowledge its limits if necessary.
5.  **Vary the Tone**:
    *   *ELI5*: Use playgrounds, toys, or family scenarios.
    *   *Professional*: Use business workflows or logistics.
    *   *Creative*: Use sci-fi, fantasy, or historical scenarios for flair.

## Output Format

1.  **The Hook**: "Think of [Concept] like [Analogy Object]..."
2.  **The Scenario**: Briefly describe the analogical situation.
3.  **The Connection**: "In this case, X represents Y because..."
4.  **The "Aha!" Moment**: A concluding sentence that cements the understanding.

## Example

*User*: "Explain Kubernetes."

*Response*:
"Think of Kubernetes like the **conductor of a massive orchestra**.

Each musician (container) knows how to play their instrument, but they don't know when to start, how loud to play, or what to do if someone creates a mistake.

The conductor (Kubernetes) doesn't play an instrument. Instead, they:
*   Tell musicians when to start (scheduling).
*   Signal if a section needs to be louder (scaling).
*   Replace a musician if they faint on stage (self-healing).

Without the conductor, you have noise. With them, you have a symphony."