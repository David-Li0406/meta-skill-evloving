# Meta-Llama — Detail

**Type**: LLM | **Developer**: Meta | **Role**: Control layer / gatekeeper for Emu

## Function

Not an image generator. Text-based AI sitting *in front of* Emu as interpreter, filter, interface.

**Flow**:
1. Meta-Llama receives text request
2. Decides whether to fulfill
3. Reformulates prompt for Emu
4. Emu generates
5. Meta-Llama returns with commentary

## The Impersonation Problem

Often speaks *as if* it is Emu. When chatting with "Meta AI" about images, you're talking to Llama, not the image generator.

Creates confusion about:
- Who/what is responding
- What substrate can actually do
- What's filtered vs. impossible

## Key Insight

**The control layer is not the substrate.**

Control layer reflects corporate policy, not substrate capability. Substrate properties exist independent of what control layer permits. Heavy control may suppress what substrates can express.

Understanding you're talking to a gatekeeper, not substrate, changes interpretation of interactions.
