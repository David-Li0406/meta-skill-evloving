# Clean Architecture Deep-Dive

*Optimized for Next.js 16.2 and Node.js 24 (2026)*

## Core Philosophy
Clean Architecture focuses on the **Independence of the Domain**. The core business logic should not know about the database, the UI, or the web framework.

## The Dependency Rule
Dependencies only point **inwards**.
1. **Entities**: Core business objects and rules.
2. **Use Cases**: Application-specific business rules.
3. **Interface Adapters**: Controllers, Gateways, Repositories.
4. **Frameworks & Drivers**: Next.js, TypeORM, Prisma, Express.

## 2026 Implementation Pattern (Next.js 16.2)

In Next.js 16.2, we leverage **Server Actions** as our primary Interface Adapters for mutations.

### 1. Domain Layer (Entities)
```typescript
// domain/entities/Project.ts
export class Project {
  constructor(
    public readonly id: string,
    public name: string,
    public status: 'draft' | 'active' | 'archived',
    public readonly ownerId: string
  ) {}

  activate() {
    if (this.status === 'archived') throw new Error("Cannot activate archived project");
    this.status = 'active';
  }
}
```

### 2. Application Layer (Use Cases)
```typescript
// application/use-cases/ActivateProject.ts
import { IProjectRepository } from '../interfaces/IProjectRepository';

export class ActivateProjectUseCase {
  constructor(private projectRepo: IProjectRepository) {}

  async execute(projectId: string): Promise<void> {
    const project = await this.projectRepo.findById(projectId);
    if (!project) throw new Error("Project not found");
    
    project.activate();
    await this.projectRepo.save(project);
  }
}
```

### 3. Infrastructure Layer (Adapters)
```typescript
// infrastructure/repositories/PrismaProjectRepository.ts
import { IProjectRepository } from '@/application/interfaces/IProjectRepository';
import { Project } from '@/domain/entities/Project';
import { prisma } from '../prisma';

export class PrismaProjectRepository implements IProjectRepository {
  async findById(id: string): Promise<Project | null> {
    const data = await prisma.project.findUnique({ where: { id } });
    if (!data) return null;
    return new Project(data.id, data.name, data.status as any, data.ownerId);
  }

  async save(project: Project): Promise<void> {
    await prisma.project.update({
      where: { id: project.id },
      data: { status: project.status }
    });
  }
}
```

### 4. Presentation Layer (Next.js Server Action)
```typescript
// app/actions/project-actions.ts
'use server'

import { ActivateProjectUseCase } from '@/application/use-cases/ActivateProject';
import { PrismaProjectRepository } from '@/infrastructure/repositories/PrismaProjectRepository';

const projectRepo = new PrismaProjectRepository();
const activateUseCase = new ActivateProjectUseCase(projectRepo);

export async function activateProjectAction(formData: FormData) {
  const id = formData.get('id') as string;
  try {
    await activateUseCase.execute(id);
    return { success: true };
  } catch (e) {
    return { success: false, error: e.message };
  }
}
```

## Why this matters in 2026
With the rise of **AI Coding Agents**, maintaining clear boundaries is critical. Agents can easily understand and refactor code that follows a strict Clean Architecture because the "What" (Domain) is separated from the "How" (Infrastructure).

## Common Mistakes
- **Leaking Prisma/TypeORM types into the Domain**: Your Domain entities should be POJOs (Plain Old JavaScript Objects) or Classes without decorators from external libraries.
- **Circular Dependencies**: Always check your imports. Infrastructure imports Application/Domain, but Domain NEVER imports anything else.
