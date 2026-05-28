---
name: defining-mobile-architecture
description: Defines the standard architecture, folder structure, and development principles for React Native Expo mobile applications. Use when setting up a new project or validating adherence to architectural standards.
---

# Mobile App Architecture Guidelines

## When to use this skill
- When initializing a new React Native Expo project.
- When creating new features or modules to ensure they fit the established structure.
- When refactoring existing code to align with architectural standards.
- When you need to check where a specific file type (service, model, etc.) belongs.

## Framework
- **Framework**: React Native with Expo
- **Target Platforms**: iOS, Android, Web

## Architecture Pattern
- **Pattern**: Clean Architecture / MVVM (Model-View-ViewModel)
- **Core Rule**: Separate business logic from UI components.
- **Modularity**: Components must be modular and reusable.

## Folder Structure
Strictly adhere to this directory layout in `/src`:

```
/src
  /components    # Reusable UI components (Buttons, Cards, Inputs)
  /screens       # Screen/page components (Home, Profile, Settings)
  /services      # API calls, external services, data fetching
  /utils         # Pure helper functions, formatters, validators
  /models        # TypeScript interfaces, types, data models
  /navigation    # Navigation configuration and navigators
  /state         # State management (Redux, Context, Zustand)
  /assets        # Images, fonts, static files
  /config        # Environment configurations, constants
  /hooks         # Custom React hooks
```

## Key Principles
1.  **Type Safety**: All code must be written in TypeScript. Strict typing is required.
2.  **Single Responsibility**: Each component, function, or service should have exactly one responsibility.
3.  **Environment Variables**: Never hardcode API keys or endpoints. Use the `/config` directory and environment variables.
4.  **Reusable Components**: If a UI element is used more than once, extract it to `/components`.
5.  **State Management**: Keep local state local. Use global state (`/state`) only for data shared across multiple screens.

## Instructions for implementation
1.  **Check Structure**: When evaluating code, verify it lives in the correct folder based on the structure above.
2.  **Verify Types**: Ensure `interface` or `type` definitions exist in `/models` for all data structures.
3.  **Review Logic**: Ensure business logic (calculations, API calls) is NOT inside UI components (screens), but in `hooks` or `services`.
