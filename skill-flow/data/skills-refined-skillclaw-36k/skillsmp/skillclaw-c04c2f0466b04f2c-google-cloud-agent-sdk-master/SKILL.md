---
name: google-cloud-agent-sdk-master
description: Use this skill when you need to build and deploy production-grade containerized agents using Google's Agent Development Kit (ADK) and Agent Starter Pack.
---

# Skill body

## Overview
This skill provides comprehensive mastery of Google's Agent Development Kit (ADK) and Agent Starter Pack for building and deploying production-grade containerized agents.

## Trigger Phrases
- "adk", "agent development kit", "agent starter pack", "multi-agent", "build agent"
- "cloud run agent", "gke deployment", "agent engine", "containerized agent"
- "rag agent", "react agent", "agent orchestration", "agent templates"

## Auto-Invokes For
- Agent creation and scaffolding
- Multi-agent system design
- Containerized agent deployment
- RAG (Retrieval-Augmented Generation) implementation
- CI/CD pipeline setup for agents
- Agent evaluation and monitoring

## Core Capabilities

### 🤖 Agent Development Kit (ADK)
- **Open-source Python framework** from Google
- Build production agents in less than 100 lines of code
- Model-agnostic and deployment-agnostic (local, Cloud Run, GKE, Agent Engine)

#### Supported Agent Types
1. **LLM Agents**: Dynamic routing with intelligence
2. **Workflow Agents**:
   - Sequential: Linear execution
   - Loop: Iterative processing
   - Parallel: Concurrent execution
3. **Custom Agents**: User-defined implementations
4. **Multi-agent Systems**: Hierarchical coordination

#### Key Features
- Flexible orchestration (workflow & LLM-driven)
- Tool ecosystem (search, code execution, custom functions)
- Third-party integrations (LangChain, CrewAI)
- Agents-as-tools capability
- Built-in evaluation framework
- Cloud Trace integration

### 📦 Agent Starter Pack
#### Production Templates
1. **adk_base** - ReAct agent using ADK
2. **agentic_rag** - Document retrieval + Q&A with search
3. **langgraph_base_react** - LangGraph ReAct implementation
4. **crewai_coding_crew** - Multi-agent coding system
5. **adk_live** - Multimodal RAG (audio/video/text)

#### Infrastructure Automation
- CI/CD setup with a single command
- GitHub Actions or Cloud Build pipelines
- Multi-environment support (dev, staging, prod)
- Automated testing and evaluation
- Deployment rollback mechanisms