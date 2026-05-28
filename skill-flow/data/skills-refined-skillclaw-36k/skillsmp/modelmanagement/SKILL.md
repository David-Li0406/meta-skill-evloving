---
name: ModelManagement
description: Instructions for managing AI models and providers, including icon usage and implementation status.
---

# Model Management Skill

This skill provides guidelines for managing AI models and their respective providers in the application.

## Supported Providers & Icons

When implementing or updating model-related features, use the following icons located in `src/assets/icons/`. It is preferred to import these as React components or use them via `img` tags/CSS to maintain consistency.

| Provider | Icon File | Implementation Status |
| :--- | :--- | :--- |
| **OpenAI** | `openai.svg` | Fully Configured |
| **Anthropic** | `anthropic.svg` | Pending Implementation |
| **Gemini** | `gemini.svg` | Pending Implementation |
| **Grok** | `grok.svg` | Pending Implementation |
| **Mistral** | `mistral.svg` | Pending Implementation |

## Usage Guidelines

1.  **Icon Source**: Always use the SVGs from `src/assets/icons/`. Do not use hardcoded SVG paths in components if an equivalent file exists in the icons directory.
2.  **Centralization**: Model-related logic and UI (like icons) should ideally be centralized to avoid duplication across `ChatInterface.tsx`, `ModelManagementModal.tsx`, etc.
3.  **Future Implementations**: When implementing new providers (Anthropic, Gemini, Grok, Mistral), ensure they follow the established pattern for IPC handlers and state management.
4.  **UI Placeholders**: For providers not yet fully implemented, ensure they still display their correct icon as a placeholder in the UI.

## Current Configuration
Currently, only **OpenAI** is fully functional in the backend IPC handlers. The other providers (Anthropic, Gemini, Grok, Mistral) are represented in the UI but require further backend work for actual API interaction.
