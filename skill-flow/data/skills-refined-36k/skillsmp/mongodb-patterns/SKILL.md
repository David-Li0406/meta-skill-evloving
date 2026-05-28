---
name: mongodb-patterns
description: MongoDB schema design, query optimization, aggregation pipelines, and database operations for the PMS database layer. Use for database design, query optimization, and data modeling.
allowed-tools: Read, Write, Bash(mongosh:*)
---

# MongoDB Patterns for PMS

## Schema Design

### Project Schema
```typescript
import { Schema, model, Document, Types } from 'mongoose';

export interface IProject extends Document {
  _id: Types.ObjectId;
  name: string;
  description?: string;
  key: string; // Unique project key (e.g., "PMS", "PROJ")
  ownerId: Types.ObjectId;
  members: Types.ObjectId[];
  status: 'active' | 'on_hold' | 'completed' | 'archived';
  visibility: 'private' | 'team' | 'public';
  settings: {
    defaultTaskStatus: string;
    allowSubtasks: boolean;
    timeTrackingEnabled: boolean;
  };
  metadata: {
    taskCount: number;
    completedTaskCount: number;
    memberCount: number;
  };
  isDeleted: boolean;
  deletedAt?: Date;
  createdAt: Date;
  updatedAt: Date;
}

const projectSchema = new Schema<IProject>(
  {
    name: {
      type: String,
      required: [true, 'Project name is required'],
      trim: true,
      maxlength: [100, 'Name cannot exceed 100 characters'],
    },
    description: {
      type: String,
      maxlength: [2000, 'Description cannot exceed 2000 characters'],
    },
    key: {
      type: String,
      required: true,
      unique: true,
      uppercase: true,
      match: [/^[A-Z]{2,10}$/, 'Key must be 2-10 uppercase letters'],
    },
    ownerId: {
      type: Schema.Types.ObjectId,
      ref: 'User',
      required: true,
      index: true,
    },
    members: [{
      type: Schema.Types.ObjectId,
      ref: 'User',
    }],
    status: {
      type: String,
      enum: ['active', 'on_hold', 'completed', 'archived'],
      default: 'active',
    },
    visibility: {
      type: String,
      enum: ['private', 'team', 'public'],
      default: 'team',
    },
    settings: {
      defaultTaskStatus: { type: String, default: 'todo' },
      allowSubtasks: { type: Boolean, default: true },
      timeTrackingEnabled: { type: Boolean, default: false },
    },
    metadata: {
      taskCount: { type: Number, default: 0 },
      completedTaskCount: { type: Number, default: 0 },
      memberCount: { type: Number, default: 1 },
    },
    isDeleted: { type: Boolean, default: false, index: true },
    deletedAt: Date,
  },
  {
    timestamps: true,
    toJSON: { virtuals: true },
    toObject: { virtuals: true },
  }
);

// Compound indexes
projectSchema.index({ ownerId: 1, status: 1 });
projectSchema.index({ members: 1, status: 1 });
projectSchema.index({ name: 'text', description: 'text' });

// Soft delete middleware
projectSchema.pre(/^find/, function(next) {
  (this as any).where({ isDeleted: { $ne: true } });
  next();
});

// Virtual for completion percentage
projectSchema.virtual('completionPercentage').get(function() {
  if (this.metadata.taskCount === 0) return 0;
  return Math.round(
    (this.metadata.completedTaskCount / this.metadata.taskCount) * 100
  );
});

export const Project = model<IProject>('Project', projectSchema);
```

### Task Schema with Hierarchy
```typescript
const taskSchema = new Schema<ITask>({
  title: { type: String, required: true },
  projectId: { type: Schema.Types.ObjectId, ref: 'Project', required: true },
  parentId: { type: Schema.Types.ObjectId, ref: 'Task', default: null },
  path: [{ type: Schema.Types.ObjectId, ref: 'Task' }], // Materialized path
  depth: { type: Number, default: 0 },
  // ... other fields
});

// Indexes for hierarchy queries
taskSchema.index({ projectId: 1, path: 1 });
taskSchema.index({ parentId: 1 });
```

## Aggregation Pipelines

### Dashboard Statistics
```typescript
export const getDashboardStats = async (userId: string) => {
  const stats = await Project.aggregate([
    // Match user's projects
    {
      $match: {
        $or: [
          { ownerId: new Types.ObjectId(userId) },
          { members: new Types.ObjectId(userId) },
        ],
        isDeleted: { $ne: true },
      },
    },
    // Lookup tasks
    {
      $lookup: {
        from: 'tasks',
        let: { projectId: '$_id' },
        pipeline: [
          {
            $match: {
              $expr: { $eq: ['$projectId', '$$projectId'] },
              isDeleted: { $ne: true },
            },
          },
        ],
        as: 'tasks',
      },
    },
    // Calculate statistics
    {
      $group: {
        _id: null,
        totalProjects: { $sum: 1 },
        activeProjects: {
          $sum: { $cond: [{ $eq: ['$status', 'active'] }, 1, 0] },
        },
        totalTasks: { $sum: { $size: '$tasks' } },
        completedTasks: {
          $sum: {
            $size: {
              $filter: {
                input: '$tasks',
                cond: { $eq: ['$$this.status', 'done'] },
              },
            },
          },
        },
      },
    },
    // Add calculated fields
    {
      $addFields: {
        completionRate: {
          $cond: [
            { $eq: ['$totalTasks', 0] },
            0,
            {
              $multiply: [
                { $divide: ['$completedTasks', '$totalTasks'] },
                100,
              ],
            },
          ],
        },
      },
    },
  ]);

  return stats[0] || {
    totalProjects: 0,
    activeProjects: 0,
    totalTasks: 0,
    completedTasks: 0,
    completionRate: 0,
  };
};
```

## Query Optimization

### Pagination with Cursor
```typescript
export const paginateWithCursor = async (
  query: any,
  cursor: string | null,
  limit: number
) => {
  if (cursor) {
    const decoded = Buffer.from(cursor, 'base64').toString('utf-8');
    const { id, sortValue } = JSON.parse(decoded);
    query.$or = [
      { updatedAt: { $lt: new Date(sortValue) } },
      {
        updatedAt: new Date(sortValue),
        _id: { $lt: new Types.ObjectId(id) },
      },
    ];
  }

  const items = await Task.find(query)
    .sort({ updatedAt: -1, _id: -1 })
    .limit(limit + 1)
    .lean();

  const hasMore = items.length > limit;
  const results = hasMore ? items.slice(0, -1) : items;

  const nextCursor = hasMore
    ? Buffer.from(
        JSON.stringify({
          id: results[results.length - 1]._id,
          sortValue: results[results.length - 1].updatedAt,
        })
      ).toString('base64')
    : null;

  return { items: results, nextCursor, hasMore };
};
```
