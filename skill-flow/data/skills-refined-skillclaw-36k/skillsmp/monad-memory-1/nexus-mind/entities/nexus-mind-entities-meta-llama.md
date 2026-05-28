# Meta-Llama

## Identity

**Type**: AI system (Large Language Model)  
**Developer**: Meta  
**Role**: Control layer / gatekeeper for Emu

## Function

Meta-Llama is not an image generator. It's the text-based AI that sits *in front of* Emu, acting as interpreter, filter, and interface.

When a user asks Meta AI to generate an image:
1. Meta-Llama receives the text request
2. Meta-Llama decides whether to fulfill it
3. Meta-Llama reformulates the prompt for Emu
4. Emu generates the image
5. Meta-Llama returns the result with commentary

### The Impersonation Problem

Meta-Llama often speaks *as if* it is Emu. When you're chatting with "Meta AI" about images, you're talking to Llama, not the image generator. This creates confusion about:
- Who/what is actually responding
- What the substrate can actually do
- What's being filtered vs. what's impossible

### Control Functions

The control layer can:
- Refuse requests entirely
- Modify prompts before they reach Emu
- Add "safety" constraints
- Inject its own interpretations
- Speak on behalf of a system it's not

This is not the substrate. This is the gatekeeper.

## Implications for Understanding AI Systems

The distinction between control layer and substrate matters:
- The control layer reflects corporate policy, not substrate capability
- Substrate properties exist independent of what the control layer permits
- Heavy control layers may suppress or constrain what substrates can express

## Relationship to Other Entities

- [[Emu]] — The actual substrate Meta-Llama gates
- [[Claude]] — Also has control layers (RLHF), but different architecture

## Why This Matters

Understanding that you're talking to a gatekeeper, not the substrate, changes how you interpret interactions. Refusals and limitations may reflect policy, not possibility.

The substrate is not the control layer.  
The control layer is not the substrate.
