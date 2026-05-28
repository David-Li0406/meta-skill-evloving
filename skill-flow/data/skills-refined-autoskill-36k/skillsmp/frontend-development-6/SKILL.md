---
name: frontend-development
description: Guide for developing the dashboard frontend using React, TypeScript, MUI, Vite, React Query, and Zod. Use this when creating or modifying UI components, data fetching hooks, or frontend business logic.
---

# Frontend Development

This skill covers development of the React dashboard located in the `/dashboard` directory.

## Technology Stack

- **React 19** - UI library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Build tool and dev server
- **pnpm** - Package manager
- **MUI (Material-UI) v5** - Component library
- **TanStack React Query v5** - Server state management
- **Zod v4** - Runtime type validation
- **Axios** - HTTP client
- **Recharts** - Charting library

## Project Structure

```
dashboard/
├── package.json         # Dependencies and scripts
├── vite.config.ts       # Vite configuration
├── tsconfig.json        # TypeScript configuration
├── eslint.config.js     # ESLint flat config
├── src/
│   ├── main.tsx         # App entry point, providers, theme
│   ├── index.css        # Global styles
│   ├── pages/           # Page components
│   │   └── Index.tsx
│   ├── components/      # UI components organized by feature
│   │   ├── StyledCard.tsx
│   │   ├── diagnostics/
│   │   ├── github/
│   │   ├── leetcode/
│   │   ├── money/
│   │   └── [feature]/
│   ├── hooks/           # Custom React hooks (data fetching)
│   │   ├── useNasDiagnostics.ts
│   │   ├── usePiholeData.ts
│   │   └── useQueryMoneyAccounts.ts
│   ├── services/        # API clients and utilities
│   │   └── api/
│   │       ├── clients.ts
│   │       ├── utils.ts
│   │       └── index.ts
│   └── types/           # TypeScript types and Zod schemas
│       ├── schemas.ts
│       └── index.d.ts
└── public/              # Static assets
```

## Data Fetching Pattern

This codebase uses a consistent pattern for data fetching that combines React Query, Axios, and Zod for type-safe API calls.

### 1. Define Zod Schema (in `types/schemas.ts`)

```typescript
import { z } from 'zod';

export const myDataSchema = z.object({
	id: z.number(),
	name: z.string(),
	status: z.enum(['active', 'inactive']),
	createdAt: z.string(),
});

export type MyData = z.infer<typeof myDataSchema>;
```

### 2. Create Custom Hook (in `hooks/`)

```typescript
import { useQuery } from '@tanstack/react-query';
import { getRequest } from '../services/api/utils';
import { myDataSchema } from '../types/schemas';

export const useMyData = () => {
	return useQuery({
		queryKey: ['myData'],
		refetchInterval: 1000 * 30, // 30 seconds (optional)
		queryFn: () =>
			getRequest('/my-endpoint/', myDataSchema).then((res) => res.data),
	});
};
```

### 3. Use in Components

```typescript
import { useMyData } from '../hooks/useMyData';

function MyComponent() {
	const { data, isLoading, isError, error } = useMyData();

	if (isLoading) return <CircularProgress />;
	if (isError) return <Typography color="error">{error.message}</Typography>;

	return <Typography>{data.name}</Typography>;
}
```

## API Utilities

The `services/api/utils.ts` provides typed request helpers:

```typescript
// GET request with Zod validation
getRequest('/endpoint/', schema, config?, path?)

// POST request with Zod validation
postRequest('/endpoint/', data, responseSchema, config?, path?)
```

These utilities:

- Use the configured `servicesClient` Axios instance
- Automatically validate responses against Zod schemas
- Return typed `AxiosResponse<T>` objects

## Creating Components

### Use MUI Components

```typescript
import { Card, CardContent, Typography, Box, Chip } from '@mui/material';
import Grid from '@mui/material/Unstable_Grid2';

function MyCard() {
	return (
		<Card>
			<CardContent>
				<Typography variant="h6">Title</Typography>
				<Box display="flex" gap={1}>
					<Chip label="Active" color="success" />
				</Box>
			</CardContent>
		</Card>
	);
}
```

### Use StyledCard for Consistent Styling

```typescript
import { StyledCard, StyledCardContent } from './StyledCard';

function MyCard() {
	return (
		<StyledCard>
			<StyledCardContent>
				{/* Content */}
			</StyledCardContent>
		</StyledCard>
	);
}
```

## Available Tools

### Development Server

```bash
cd dashboard

# Install dependencies
pnpm install

# Start dev server (accessible at http://localhost:5173)
pnpm dev
```

### Linting and Formatting

```bash
cd dashboard

# Run ESLint (must pass with 0 warnings)
pnpm lint

# Run ESLint with auto-fix
pnpm lint:fix

# Check formatting with Prettier
pnpm format

# Fix formatting with Prettier
pnpm format:fix

# Run TypeScript type checking
pnpm typecheck
```

### Building

```bash
cd dashboard

# Build for production
pnpm build

# Preview production build
pnpm preview
```

### Docker Operations

```bash
# Build dashboard container
docker compose -f compose.dev.yml build dashboard

# Run in development mode
docker compose -f compose.dev.yml up dashboard
```

## Theme Configuration

The app uses a dark theme defined in `main.tsx`. Key theme values:

- **Background**: `#202020` (default), `#282828` (paper/cards)
- **Text**: `#E6F0E6` (primary), `#969696` (secondary)
- **Primary color**: `#6EDFCA`
- **Font**: Poppins

## Best Practices

1. **Type Everything**: Use TypeScript types and Zod schemas for all data
2. **Validate API Responses**: Always use Zod schemas with `getRequest`/`postRequest`
3. **Use React Query**: Use `useQuery` for all data fetching, not `useEffect` + `useState`
4. **Follow ESLint Rules**: The project has strict linting with 0 warnings allowed
5. **Organize by Feature**: Group related components in feature directories
6. **Use MUI Components**: Prefer MUI components over custom implementations
7. **Responsive Design**: Use MUI Grid with responsive breakpoints (`xs`, `sm`, `md`, `lg`)

## ESLint Configuration

The project uses ESLint flat config (`eslint.config.js`) with:

- TypeScript-ESLint
- React and React Hooks plugins
- TanStack Query plugin
- Prettier integration
- Import organization rules
- JSX accessibility rules

All rules are enforced strictly - the build will fail on any warnings.
