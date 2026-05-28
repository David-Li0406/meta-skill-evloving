---
name: mongoose
description: Use this skill when you need to implement Mongoose with MongoDB, focusing on TypeScript integration and performance best practices for Mongoose 8.x/9.x.
---

# Mongoose Skill (2025-2026 Edition)

This skill provides modern guidelines for using Mongoose with MongoDB, focusing on Mongoose 8.x/9.x, strict TypeScript integration, and performance optimizations relevant to the 2025 ecosystem.

## 🚀 Key Trends & Features (2025/2026)

*   **TypeScript-First:** Mongoose 8+ has superior built-in type inference. `@types/mongoose` is obsolete.
*   **Performance:** Mongoose 9 introduces architectural changes for lower overhead. Native vector search support is now standard for AI features.
*   **Modern JavaScript:** Full support for `async/await` iterators and native Promises.

## 📐 TypeScript Integration (The Strict Way)

Do **NOT** extend `LengthyDocument` or standard `Document`. Use a plain interface and let Mongoose infer the rest.

### 1. Define the Interface (Raw Data)
Define what your data looks like in plain JavaScript objects.

```typescript
import { Types } from 'mongoose';

export interface IUser {
  name: string;
  email: string;
  role: 'admin' | 'user';
  tags: string[];
  organization?: Types.ObjectId; // Use specific type for ObjectIds
  createdAt?: Date;
}
```

### 2. Define the Schema & Model
Create the model with generic typing.

```typescript
import mongoose, { Schema, model } from 'mongoose';
import { IUser } from './interfaces';

const userSchema = new Schema<IUser>({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  role: { type: String, enum: ['admin', 'user'], default: 'user' },
  tags: [String],
  organization: { type: Schema.Types.ObjectId, ref: 'Organization' }
}, {
  timestamps: true /* Automatically manages createdAt/updatedAt */
});

// ⚡ 2025 Best Practice: Avoid "extends Document" on the interface.
// Let 'model<IUser>' handle the HydratedDocument type automatically.
export const User = mongoose.models.User || model<IUser>('User', userSchema);
```

### 3. Usage (Type-Safe)

```typescript
// 'user' is typed as HydratedDocument<IUser> automatically
const user = await User.findOne({ email: 'test@example.com' });

if (user) {
  console.log(user.name); // Typed string
  await user.save(); // Typed method
}
```

## ⚡ Performance Optimization

### 1. `.lean()` for Reads
Always use `.lean()` for read-only operations (e.g., GET requests). It skips Mongoose hydration, speeding up queries.