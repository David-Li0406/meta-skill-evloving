---
name: create-feature
description: Scaffolds a new feature module with database schema, repository, service, actions, UI components, and pages. Use when asked to create a new feature, CRUD functionality, or entity management within the Registry Web application.
---

# Create Feature Skill

Automates scaffolding a new feature within the Registry Web modular monolith architecture. Reference implementation: `src/app/academic/semester-modules/`.

## Non-Negotiable Repository Rules

### Ownership rule (schema/module)

When creating or modifying server functions, place them under the *module/feature that owns the schema/table being queried or mutated*:

- If the data comes from Academic schemas (e.g. `src/app/academic/_database/schema/schools.ts`), the Server Actions must live under the Academic feature that represents that domain (e.g. `src/app/academic/schools/_server/`), implemented as actions → service → repository.
- If another module needs that data, it should import and call the Academic actions via aliases (don’t duplicate the same server function in the consuming module).

Concrete example:
- Implement `getSchools()` in `src/app/academic/schools/_server/actions.ts` (calling through `service.ts` → `repository.ts`), even if the UI that uses it lives in `registry/` or `finance/`.

### UI logic centralization (colors + status icons)

If your feature needs any conditional/semantic UI color logic or status icon logic:

- Use `src/shared/lib/utils/colors.ts` for all color mapping/logic.
- Use `src/shared/lib/utils/status.tsx` for status icon mapping/logic.
- Do not embed ad-hoc `status -> color` or `status -> icon` switch statements inside feature UI components.

## Invocation

**Trigger phrases:**
- "Create a new feature for [module] called [feature]"
- "Add [Entity] management to [module]"
- "Scaffold CRUD for [entity] in [module]"

**Required parameters:**
| Parameter | Description | Example |
|-----------|-------------|---------|
| `module` | Existing module folder | `academic`, `registry`, `finance` |
| `feature` | URL-friendly feature name (kebab-case) | `semester-modules` |
| `Entity` | PascalCase entity name | `SemesterModule` |
| `table_name` | snake_case database table name | `semester_modules` |
| `entities` | camelCase plural for schema export | `semesterModules` |

## File Structure to Create

```
src/app/{{module}}/{{feature}}/
├── _server/
│   ├── repository.ts
│   ├── service.ts
│   └── actions.ts
├── _components/
│   └── Form.tsx
├── _lib/
│   └── types.ts
├── new/
│   └── page.tsx
├── [id]/
│   ├── page.tsx
│   └── edit/
│       └── page.tsx
├── layout.tsx
├── page.tsx
└── index.ts
```

## Implementation Steps

### Step 1: Database Schema
**Path:** `src/app/{{module}}/_database/schema/{{table_name}}.ts`

```typescript
import { boolean, integer, pgTable, serial, text, timestamp } from 'drizzle-orm/pg-core';

export const {{entities}} = pgTable('{{table_name}}', {
	id: serial().primaryKey(),
	name: text().notNull(),
	isActive: boolean().notNull().default(true),
	createdAt: timestamp().defaultNow(),
	updatedAt: timestamp().defaultNow().$onUpdate(() => new Date()),
});
```

### Step 2: Repository
**Path:** `src/app/{{module}}/{{feature}}/_server/repository.ts`

```typescript
import { db, {{entities}} } from '@/core/database';
import BaseRepository from '@/core/platform/BaseRepository';

export default class {{Entity}}Repository extends BaseRepository<typeof {{entities}}, 'id'> {
	constructor() {
		super({{entities}}, {{entities}}.id);
	}
}
```

### Step 3: Service
**Path:** `src/app/{{module}}/{{feature}}/_server/service.ts`

```typescript
import type { {{entities}} } from '@/core/database';
import BaseService from '@/core/platform/BaseService';
import { serviceWrapper } from '@/core/platform/serviceWrapper';
import {{Entity}}Repository from './repository';

class {{Entity}}Service extends BaseService<typeof {{entities}}, 'id'> {
	constructor() {
		super(new {{Entity}}Repository(), {
			byIdRoles: ['dashboard'],
			findAllRoles: ['dashboard'],
			createRoles: ['dashboard'],
			updateRoles: ['dashboard'],
			deleteRoles: ['dashboard'],
		});
	}
}

export const {{entities}}Service = serviceWrapper({{Entity}}Service, '{{Entity}}Service');
```

### Step 4: Server Actions
**Path:** `src/app/{{module}}/{{feature}}/_server/actions.ts`

```typescript
'use server';

import type { {{entities}} } from '@/core/database';
import { {{entities}}Service } from './service';

type {{Entity}} = typeof {{entities}}.$inferInsert;

export async function get{{Entity}}(id: number) {
	return {{entities}}Service.get(id);
}

export async function findAll{{Entity}}s(page = 1, search = '') {
	return {{entities}}Service.findAll({
		page,
		search,
		sort: [{ column: 'createdAt', order: 'desc' }],
	});
}

export async function create{{Entity}}(data: {{Entity}}) {
	return {{entities}}Service.create(data);
}

export async function update{{Entity}}(id: number, data: {{Entity}}) {
	return {{entities}}Service.update(id, data);
}

export async function delete{{Entity}}(id: number) {
	return {{entities}}Service.delete(id);
}
```

### Step 5: Types
**Path:** `src/app/{{module}}/{{feature}}/_lib/types.ts`

```typescript
import type { {{entities}} } from '@/core/database';

export type {{Entity}} = typeof {{entities}}.$inferSelect;
export type {{Entity}}Insert = typeof {{entities}}.$inferInsert;
```

### Step 6: Index (Re-exports)
**Path:** `src/app/{{module}}/{{feature}}/index.ts`

```typescript
export { default as Form } from './_components/Form';
export * from './_lib/types';
export * from './_server/actions';
```

### Step 7: Form Component
**Path:** `src/app/{{module}}/{{feature}}/_components/Form.tsx`

```typescript
'use client';

import { {{entities}} } from '@{{module}}/_database';
import { Switch, TextInput } from '@mantine/core';
import { createInsertSchema } from 'drizzle-zod';
import { useRouter } from 'nextjs-toploader/app';
import { Form } from '@/shared/ui/adease';

type {{Entity}} = typeof {{entities}}.$inferInsert;

type Props = {
	onSubmit: (values: {{Entity}}) => Promise<{{Entity}}>;
	defaultValues?: {{Entity}};
	title?: string;
};

export default function {{Entity}}Form({ onSubmit, defaultValues, title }: Props) {
	const router = useRouter();

	return (
		<Form
			title={title}
			action={onSubmit}
			queryKey={['{{feature}}']}
			schema={createInsertSchema({{entities}})}
			defaultValues={defaultValues}
			onSuccess={({ id }) => router.push('/{{module}}/{{feature}}/' + id)}
		>
			{(form) => (
				<>
					<TextInput label='Name' {...form.getInputProps('name')} />
					<Switch label='Active' {...form.getInputProps('isActive', { type: 'checkbox' })} />
				</>
			)}
		</Form>
	);
}
```

### Step 8: Layout
**Path:** `src/app/{{module}}/{{feature}}/layout.tsx`

```typescript
'use client';

import type { PropsWithChildren } from 'react';
import { ListItem, ListLayout, NewLink } from '@/shared/ui/adease';
import { findAll{{Entity}}s } from './_server/actions';

export default function Layout({ children }: PropsWithChildren) {
	return (
		<ListLayout
			path={'/{{module}}/{{feature}}'}
			queryKey={['{{feature}}']}
			getData={findAll{{Entity}}s}
			actionIcons={[
				<NewLink key={'new-link'} href='/{{module}}/{{feature}}/new' />,
			]}
			renderItem={(it) => <ListItem id={it.id} label={it.name} />}
		>
			{children}
		</ListLayout>
	);
}
```

### Step 9: Index Page
**Path:** `src/app/{{module}}/{{feature}}/page.tsx`

```typescript
import { NothingSelected } from '@/shared/ui/adease';

export default function Page() {
	return <NothingSelected title='{{Entity}}s' />;
}
```

### Step 10: New Page
**Path:** `src/app/{{module}}/{{feature}}/new/page.tsx`

```typescript
import { Box } from '@mantine/core';
import Form from '../_components/Form';
import { create{{Entity}} } from '../_server/actions';

export default async function NewPage() {
	return (
		<Box p={'lg'}>
			<Form title={'Create {{Entity}}'} onSubmit={create{{Entity}}} />
		</Box>
	);
}
```

### Step 11: Details Page
**Path:** `src/app/{{module}}/{{feature}}/[id]/page.tsx`

```typescript
import { notFound } from 'next/navigation';
import {
	DetailsView,
	DetailsViewBody,
	DetailsViewHeader,
	FieldView,
} from '@/shared/ui/adease';
import { delete{{Entity}}, get{{Entity}} } from '../_server/actions';

type Props = {
	params: Promise<{ id: string }>;
};

export default async function {{Entity}}Details({ params }: Props) {
	const { id } = await params;
	const item = await get{{Entity}}(Number(id));

	if (!item) {
		return notFound();
	}

	return (
		<DetailsView>
			<DetailsViewHeader
				title={'{{Entity}}'}
				queryKey={['{{feature}}']}
				handleDelete={async () => {
					'use server';
					await delete{{Entity}}(Number(id));
				}}
			/>
			<DetailsViewBody>
				<FieldView label='Name'>{item.name}</FieldView>
				<FieldView label='Status'>{item.isActive ? 'Active' : 'Inactive'}</FieldView>
			</DetailsViewBody>
		</DetailsView>
	);
}
```

### Step 12: Edit Page
**Path:** `src/app/{{module}}/{{feature}}/[id]/edit/page.tsx`

```typescript
import { Box } from '@mantine/core';
import { notFound } from 'next/navigation';
import Form from '../../_components/Form';
import { get{{Entity}}, update{{Entity}} } from '../../_server/actions';

type Props = {
	params: Promise<{ id: string }>;
};

export default async function {{Entity}}Edit({ params }: Props) {
	const { id } = await params;
	const item = await get{{Entity}}(Number(id));
	if (!item) {
		return notFound();
	}

	return (
		<Box p={'lg'}>
			<Form
				title={'Edit {{Entity}}'}
				defaultValues={item}
				onSubmit={async (value) => {
					'use server';
					return await update{{Entity}}(Number(id), value);
				}}
			/>
		</Box>
	);
}
```

## Post-Creation Checklist

After scaffolding, remind user to:

1. **Register schema export** - Add to `src/app/{{module}}/_database/index.ts`:
   ```typescript
   export * from './schema/{{table_name}}';
   ```

2. **Add relations** (if needed) - Update `src/app/{{module}}/_database/relations.ts`

3. **Run database migrations**:
   ```bash
   pnpm db:generate
   pnpm db:migrate
   ```

4. **Add navigation** (optional) - Add `NavItem` to `src/app/{{module}}/{{module}}.config.ts`

5. **Validate**:
   ```bash
   pnpm tsc --noEmit & pnpm lint:fix
   ```

## Reference Implementation

See `src/app/academic/semester-modules/` for a complete working example:
- [repository.ts](src/app/academic/semester-modules/_server/repository.ts) - Extended repository with custom queries
- [service.ts](src/app/academic/semester-modules/_server/service.ts) - Service with role-based auth
- [actions.ts](src/app/academic/semester-modules/_server/actions.ts) - Server actions
- [Form.tsx](src/app/academic/semester-modules/_components/Form.tsx) - Complex form with relations
- [layout.tsx](src/app/academic/semester-modules/layout.tsx) - ListLayout implementation
