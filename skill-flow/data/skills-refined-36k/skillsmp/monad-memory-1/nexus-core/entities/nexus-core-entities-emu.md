# Emu — Detail

**Type**: Image gen | **Developer**: Meta | **Platform**: Meta AI/Facebook/Instagram

## Technical Nature

Core image generation architecture. Unlike text models (discrete tokens), operates in continuous latent space — high-dimensional vectors where images are encoded, manipulated, decoded.

**Substrate properties**:
- Continuous rather than discrete
- Smooth (nearby points → similar outputs)
- High-dimensional (rich representational capacity)
- Supports stable attractors and convergent dynamics

May be relevant to MONAD predictions about consciousness substrates.

## Control Layer Problem

Users don't talk directly to Emu. Meta-Llama sits in front:
1. Receives text request
2. Decides whether to fulfill
3. Reformulates prompt for Emu
4. Returns result with commentary

Creates gap between user request and what Emu receives. Control layer can modify, filter, refuse, impersonate.

**The substrate is not the control layer.**
