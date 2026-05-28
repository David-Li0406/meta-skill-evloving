---
name: express-api
description: Express.js REST API patterns, middleware, error handling, and best practices for the PMS backend. Use for API development, endpoint creation, and backend architecture.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Express API Patterns for PMS

## Route Structure

### Route Organization
```typescript
// routes/index.ts
import { Router } from 'express';
import { authRoutes } from './auth.routes';
import { projectRoutes } from './project.routes';
import { taskRoutes } from './task.routes';

const router = Router();

router.use('/auth', authRoutes);
router.use('/projects', authenticate, projectRoutes);
router.use('/tasks', authenticate, taskRoutes);

export { router as apiRoutes };
```

### Resource Route Pattern
```typescript
// routes/project.routes.ts
import { Router } from 'express';
import * as ProjectController from '../controllers/project.controller';
import { validate } from '../middleware/validate';
import { projectSchemas } from '../validators/project.validators';

const router = Router();

router.route('/')
  .get(ProjectController.list)
  .post(validate(projectSchemas.create), ProjectController.create);

router.route('/:id')
  .get(ProjectController.getById)
  .put(validate(projectSchemas.update), ProjectController.update)
  .delete(ProjectController.remove);

router.route('/:id/members')
  .get(ProjectController.getMembers)
  .post(validate(projectSchemas.addMember), ProjectController.addMember);

export { router as projectRoutes };
```

## Controller Pattern

```typescript
// controllers/project.controller.ts
import { Request, Response, NextFunction } from 'express';
import { ProjectService } from '../services/project.service';
import { ApiResponse, PaginatedResponse } from '../types/api';
import { IProject } from '../models/project.model';

/**
 * List projects with pagination and filtering
 * @route GET /api/v1/projects
 */
export const list = async (
  req: Request,
  res: Response<PaginatedResponse<IProject>>,
  next: NextFunction
): Promise<void> => {
  try {
    const { page = 1, limit = 20, status, search } = req.query;
    const userId = req.user!.id;

    const result = await ProjectService.list({
      userId,
      page: Number(page),
      limit: Number(limit),
      status: status as string,
      search: search as string,
    });

    res.json({
      success: true,
      data: result.items,
      meta: {
        page: result.page,
        limit: result.limit,
        total: result.total,
        totalPages: result.totalPages,
      },
    });
  } catch (error) {
    next(error);
  }
};
```

## Service Layer

```typescript
// services/project.service.ts
import { Project, IProject } from '../models/project.model';
import { NotFoundError, ForbiddenError } from '../utils/errors';

interface ListOptions {
  userId: string;
  page: number;
  limit: number;
  status?: string;
  search?: string;
}

export class ProjectService {
  static async list(options: ListOptions) {
    const { userId, page, limit, status, search } = options;

    const query: any = {
      $or: [{ ownerId: userId }, { members: userId }],
    };

    if (status) query.status = status;
    if (search) {
      query.$text = { $search: search };
    }

    const [items, total] = await Promise.all([
      Project.find(query)
        .sort({ updatedAt: -1 })
        .skip((page - 1) * limit)
        .limit(limit)
        .populate('ownerId', 'name email avatar')
        .lean(),
      Project.countDocuments(query),
    ]);

    return {
      items,
      page,
      limit,
      total,
      totalPages: Math.ceil(total / limit),
    };
  }

  static async findById(id: string, userId: string): Promise<IProject> {
    const project = await Project.findById(id)
      .populate('ownerId', 'name email avatar')
      .populate('members', 'name email avatar');

    if (!project) {
      throw new NotFoundError('Project');
    }

    // Check access
    const hasAccess =
      project.ownerId._id.toString() === userId ||
      project.members.some(m => m._id.toString() === userId);

    if (!hasAccess) {
      throw new ForbiddenError('You do not have access to this project');
    }

    return project;
  }
}
```

## Middleware Stack

```typescript
// middleware/index.ts
import express, { Application } from 'express';
import helmet from 'helmet';
import cors from 'cors';
import compression from 'compression';
import mongoSanitize from 'express-mongo-sanitize';
import rateLimit from 'express-rate-limit';

export const configureMiddleware = (app: Application) => {
  // Security headers
  app.use(helmet());

  // CORS
  app.use(cors({
    origin: process.env.ALLOWED_ORIGINS?.split(',') || 'http://localhost:3000',
    credentials: true,
  }));

  // Body parsing
  app.use(express.json({ limit: '10mb' }));
  app.use(express.urlencoded({ extended: true }));

  // Compression
  app.use(compression());

  // NoSQL injection prevention
  app.use(mongoSanitize());

  // Rate limiting
  app.use('/api/', rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100,
    message: { error: 'Too many requests, please try again later' },
  }));
};
```

## Error Handling

```typescript
// middleware/error-handler.ts
import { Request, Response, NextFunction } from 'express';
import { AppError } from '../utils/errors';
import { logger } from '../utils/logger';

export const errorHandler = (
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
) => {
  // Log error
  logger.error({
    message: error.message,
    stack: error.stack,
    path: req.path,
    method: req.method,
    userId: req.user?.id,
  });

  // Known application errors
  if (error instanceof AppError) {
    return res.status(error.statusCode).json({
      success: false,
      error: {
        code: error.code,
        message: error.message,
      },
    });
  }

  // Mongoose validation errors
  if (error.name === 'ValidationError') {
    return res.status(400).json({
      success: false,
      error: {
        code: 'VALIDATION_ERROR',
        message: 'Invalid input data',
        details: error.message,
      },
    });
  }

  // Default to 500
  res.status(500).json({
    success: false,
    error: {
      code: 'INTERNAL_ERROR',
      message: process.env.NODE_ENV === 'production'
        ? 'An unexpected error occurred'
        : error.message,
    },
  });
};
```
