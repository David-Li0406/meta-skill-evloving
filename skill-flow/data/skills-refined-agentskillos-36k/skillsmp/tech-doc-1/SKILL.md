---
name: tech-doc
description: Generate technical documentation for a specified technology domain with optional customization.
---

## Overview

This skill generates **technical documentation** for a specified technology domain (e.g., WebCodecs, WebRTC, Media Playback, WebAudio, Graphics) in the Firefox/Gecko codebase.

The generated document serves as **context input** for AI coding assistants in scenarios such as feature planning, spec implementation, debugging, or code tracing.

## Workflow

1. Ask the user for the target **technology domain** if not already specified
2. Show the pre-filled prompt and ask if the user wants to customize it
3. If user wants to customize: let them provide modifications
4. Ask the user where to save the generated documentation
5. Generate the technical documentation based on the finalized prompt and save to specified location

## Instructions

When this skill is invoked:

### Step 1: Check if domain is specified

If the user has not specified a domain, use **AskUserQuestion** to ask them to choose one. Common domains include:
- WebCodecs
- Media Playback (HTMLMediaElement)
- Media Source Extensions (MSE)
- MediaRecorder
- MediaSession
- WebRTC
- WebAudio
- Graphics (WebGL, WebGPU, Canvas)
- DOM Events
- Layout Engine
- Networking (Necko)
- IPC/IPDL
- Or any other Firefox subsystem

### Step 2: Show pre-filled prompt and offer customization

Once you have the domain, look up the primary directories and specs from the **Domain Reference** table below. Then show the user the pre-filled prompt (see **Prompt Template** section) and use **AskUserQuestion** to ask:

> "Here's the documentation request I'll use. Would you like to customize it?"
> - **Generate now** - Proceed with the default prompt
> - **Customize** - Let me modify the prompt first

### Step 3: Handle customization (if requested)

If the user chooses to customize, ask them what they'd like to change:
- Additional context or focus areas
- Specific sections to emphasize or skip
- Additional directories to analyze
- Any other modifications

### Step 4: Ask for storage destination

Before generating, use **AskUserQuestion** to ask where to save the documentation:

> "Where would you like to save the generated documentation?"
> - **Default location** - Save to `.claude/skills/tech-doc/{domain}.md`
> - **Custom path** - Let me specify a different location

If the user chooses a custom path, ask them to provide the full file path.

### Step 5: Generate the technical documentation

After the prompt is finalized and destination is determined, **generate the actual technical documentation** by:

1. Use `searchfox-cli` and file reads to explore the codebase for the specified domain
2. Analyze the architecture, key classes, data flows, and interactions
3. Write the comprehensive technical document following the structure in the prompt
4. Save the document to the specified location in Markdown format

**IMPORTANT**: Do NOT just output the prompt template. Actually generate the technical documentation by researching the codebase.

---

## Prompt Template

Use this template internally to guide documentation generation. Replace placeholders with actual values from the Domain Reference table.

```
# Technical Documentation: {{DOMAIN}}

**Generated Date**: {{CURRENT_DATE}}

**Scope**: Comprehensive technical documentation for {{DOMAIN}} in Firefox/Gecko, covering architecture, key modules, data flows, and cross-boundary interactions.

## Target Codebase

- **Repository**: Mozilla Firefox (Gecko engine)
- **Primary directories**: {{PRIMARY_DIRECTORIES}}
- **Related specifications**: {{RELEVANT_SPECS}}

## Document Sections to Generate

1. **High-Level Architecture**
   - Primary modules/components
   - Inter-module dependencies
   - Process hosting (parent, content, GPU, etc.)
   - Architecture diagram (ASCII/text)

2. **Core Modules Deep Dive**
   - Purpose and responsibilities
   - Key classes/structures
   - Lifetime/lifecycle management
   - Process/thread model
   - Task queue dynamics

3. **Architectural Control Points**
   - Orchestration components
   - State management
   - Data flow drivers
   - External API entry points

4. **Key Data Flows**
   - Input sources
   - Transformations/processing
   - Output destinations
   - Sequence descriptions

5. **Key Event Flows**
   - Event types and meanings
   - Dispatch mechanisms
   - State machine transitions
   - Error handling paths

6. **Action-to-Behavior Mappings**
   - User action triggers
   - System triggers
   - Internal method call chains
   - Cross-process communication

7. **Critical Cross-Boundary Interactions**
   - Process boundaries (IPC/IPDL)
   - Thread boundaries
   - Module boundaries
   - Tech stack boundaries (C++/Rust/JS, WebIDL)

## Additional Context

{{ADDITIONAL_CONTEXT}}
```

---

## Domain Reference

| Domain | Primary Directories | Related Specs |
|--------|---------------------|---------------|
| WebCodecs | `dom/media/webcodecs/`, `media/ffvpx/` | W3C WebCodecs API, Codec Registry |
| Media Playback | `dom/media/`, `dom/html/` | WHATWG HTML Media Element |
| MSE | `dom/media/mediasource/` | W3C Media Source Extensions |
| MediaRecorder | `dom/media/mediarecorder/` | W3C MediaStream Recording |
| WebRTC | `dom/media/webrtc/`, `media/webrtc/` | W3C WebRTC, IETF RFCs |
| WebAudio | `dom/media/webaudio/` | W3C Web Audio API |
| Graphics | `gfx/`, `dom/canvas/` | WHATWG Canvas, WebGL, WebGPU |
| IPC | `ipc/`, `dom/ipc/` | Mozilla IPDL |
| Networking | `netwerk/` | HTTP specs, Fetch API |
| Layout | `layout/` | CSS specs, WHATWG |

---

## Example Invocations

- `/tech-doc WebCodecs` - Generate WebCodecs documentation
- `/tech-doc for MSE` - Generate MSE documentation
- `/tech-doc` - Will prompt for domain selection
