---
name: nextjs-project-initialization-and-best-practices
description: This skill provides guidance for initializing and structuring Next.js projects with modern best practices. It covers project setup, component organization, API integration, and development patterns following the specified architecture.
---

# Next.js Project Initialization and Best Practices

## Overview
This skill provides guidance for initializing and structuring Next.js projects with modern best practices. It covers project setup, component organization, API integration, and development patterns following the specified architecture.

## Project Initialization

### Create Next.js Project
Initialize a new Next.js project with the recommended configuration:

```bash
npx create-next-app@latest project-name --yes --typescript --tailwind --app --src-dir --turbopack --eslint
```

**Parameters Explanation:**
- `--yes`: Skip prompts and use default options
- `--typescript`: Include TypeScript support
- `--tailwind`: Add Tailwind CSS for styling
- `--app`: Use the App Router (app directory)
- `--src-dir`: Create a `src` directory
- `--turbopack`: Use Turbopack for faster builds (optional)
- `--eslint`: Include ESLint for linting

### Important Note on Tailwind CSS v4
With Tailwind CSS v4, there's no need to create a `tailwind.config.ts` file. The configuration is handled automatically.

## ShadCN UI Setup

### Initialize ShadCN
After creating the project, initialize ShadCN UI components:

```bash
npx shadcn@latest init .
```

### Add ShadCN Components
Add specific components as needed:

```bash
npx shadcn@latest add button card formand wha input label textarea select checkbox radio-group
```

## Component Naming and Organization

### File Naming Convention
- All component file names MUST be in kebab-case (e.g., `user-profile.tsx`, not `UserProfile.tsx`)
- Use descriptive names that reflect the component's purpose

### Folder Structure
- All components MUST be organized in folders
- Maintain consistent hierarchy for easy navigation
- Group related components together

### Export Convention
- All components MUST use named exports using arrow functions (not default exports)
- Example:
```tsx
// ✅ Correct
export const UserProfile = () => {
  return <div>Profile Component</div>;
}

// ❌ Incorrect
export default function UserProfile() {
  return <div>Profile Component</div>;
}
```

## Icon Usage

### Lucide React Icons
- All icons MUST be used from `lucide-react` library
- Import icons with "Icon" postfix
- Example:
```tsx
// ✅ Correct
import { ChatIcon, UserIcon, HomeIcon } from "lucide-react";

// ❌ Incorrect
import { Chat, User, Home } from "lucide-react";
```

## State Management and Mutations

### React TanStack Query
- All mutations MUST be done using React TanStack Query (React Query)
- Use `useMutation` for data modification operations
- Use `useQuery` for data fetching operations

### Hook Creation
- All hooks MUST be created independently without providers
- Hooks should encapsulate specific functionality
- Follow the naming convention: `use[FeatureName]`

## Form Handling

### Form Location
- Every form MUST be placed in `src/components/forms` folder
- Organize forms by feature or purpose
- Keep form components separate from UI components

### Form Creation
- Forms MUST be created through ShadCN form components
- Use Zod schema validation for all forms
- Combine ShadCN form components with Zod for robust validation

## Project Structure

### Library Folder (`src/lib`)
- All external libraries clients (supabase, stripe, better-auth, etc.) MUST be placed here
- Create individual files for each service
- Example structure:
```
src/lib/
├── supabase/
│   ├── client.ts
│   └── server.ts
├── stripe/
│   ├── client.ts
│   └── server.ts
└── better-auth/
    ├── client.ts
    └── server.ts
```

### Utilities Folder (`src/utils`)
- All utility functions (date, time, price, formatting) MUST be placed here
- Create specific files for different utility categories
- Example structure:
```
src/utils/
├── shadcn.ts
├── date.ts
├── price.ts
├── format.ts
└── validation.ts
```

### Features Folder (`src/features`)
- All business logic (including API calls) MUST be placed here
- Organize by feature with consistent structure

#### Feature Structure
```
src/features/
├── auth/
│   ├── hooks.tsx
│   ├── queries.ts
│   ├── types.ts
│   └── schema.ts
└── feature-name/
    ├── hooks.tsx     # Mutation hooks
    ├── queries.ts    # GET queries
    ├── types.ts      # TypeScript interfaces/types
    └── schema.ts     # Zod schemas
```

## Implementation Patterns

### Minimize Prop Drilling
- Components should use hooks directly to access data rather than receiving functions through props
- Dialogs and forms should use `use[Feature]` hooks directly instead of receiving callback functions
- This reduces prop chains and makes components more self-contained

### Centralized Configurations
- Define shared configuration objects (options, display configs) in a central file like `src/features/[feature-name]/config.ts`
- Import configurations in components instead of defining them locally to avoid duplication
- This ensures consistency and easier maintenance across the application

### Hooks Pattern (`hooks.tsx`)
```tsx
import { useMutation, useQuery } from "@tanstack/react-query";

export const useFeature = () => {
  const addFeature = useMutation({
    mutationFn: (data: any) => {
      // API call implementation
    },
    onSuccess: () => {},
    onError: () => {},
  });

  const updateFeature = useMutation({
    mutationFn: (data: any) => {},
    onSuccess: () => {},
    onError: (error) => {},
  });

  const deleteFeature = useMutation({
    mutationFn: (data: any) => {},
    onSuccess: () => {},
    onError: (error) => {},
  });

  const getFeatures = useQuery({
    queryKey: ['features'],
    queryFn: () => {
      // API call implementation
    }
  });

  return {
    addFeature,
    updateFeature,
    deleteFeature,
    getFeatures
  };
};
```

### Schema Pattern (`schema.ts`)
```tsx
import { z } from "zod";

export const featureFormSchema = z.object({
  id: z.string().optional(),
  name: z.string().min(1, "Name is required"),
  description: z.string().optional(),
  // Add more fields as needed
});

export type FeatureFormData = z.infer<typeof featureFormSchema>;
```

### Types Pattern (`types.ts`)
```tsx
export interface Feature {
  id: string;
  name: string;
  description?: string;
  createdAt: string;
  updatedAt: string;
}
```

### Queries Pattern (`queries.ts`)
```tsx
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Feature } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:3000/api";

export const fetchFeatures = async (): Promise<Feature[]> => {
  const response = await fetch(`${API_BASE_URL}/features`);
  if (!response.ok) throw new Error("Failed to fetch features");
  return response.json();
};

export const createFeature = async (data: Partial<Feature>) => {
  const response = await fetch(`${API_BASE_URL}/features`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!response.ok) throw new Error("Failed to create feature");
  return response.json();
};
```

## Development Workflow

### File Creation Guidelines
- No need to create every file, just create what is needed
- Follow the folder structure when adding new features
- Maintain consistency across the codebase

### Component Development
1. Create components in appropriate folders
2. Use kebab-case for file names
3. Use named exports for all components
4. Import icons with "Icon" postfix from lucide-react
5. Use ShadCN components for UI elements

### Form Development
1. Place forms in `src/components/forms` folder
2. Use ShadCN form components
3. Apply Zod schema validation
4. Follow the established patterns for form handling

## Common Commands

### Project Setup
```bash
# Initialize Next.js project
npx create-next-app@latest project-name --yes --typescript --tailwind --app --src-dir --turbopack --eslint

# Initialize ShadCN
npx shadcn@latest init .

# Add specific components
npx shadcn@latest add button card form input label textarea
```

### Development
```bash
# Start development server
npm run dev

# Build for production
npm run build

# Run linting
npm run lint
```

This skill provides a complete guide for setting up and maintaining Next.js projects following the specified architecture and best practices.
