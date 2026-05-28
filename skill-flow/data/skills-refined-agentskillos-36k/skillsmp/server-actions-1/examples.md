# Server Actions Examples

Complete, production-ready examples for common server action patterns.

## Table of Contents

1. [Basic CRUD Operations](#basic-crud-operations)
2. [Form Submission with Redirect](#form-submission-with-redirect)
3. [Multi-Step Form Flow](#multi-step-form-flow)
4. [Action with Toast Notifications](#action-with-toast-notifications)
5. [Action with Authentication](#action-with-authentication)
6. [Action with useActionState](#action-with-useactionstate)
7. [Batch Operations](#batch-operations)
8. [File Upload Action](#file-upload-action)

---

## Basic CRUD Operations

### Create

```typescript
// features/posts/server/actions/create-post.ts
"use server";

import { revalidatePath } from "next/cache";
import { auth } from "@clerk/nextjs/server";
import { createPostInDb } from "../db/posts";
import { postSchema, type CreatePostData } from "../../schemas/post";
import type { ActionResponse } from "~/lib/action-types";
import type { Post } from "../../types/post";
import { createLogger } from "~/lib/logger";

const logger = createLogger({ module: "posts-actions" });

export async function createPost(data: CreatePostData): ActionResponse<Post> {
  // 1. Authentication
  const { userId } = await auth();
  if (!userId) {
    return { success: false, error: "Authentication required" };
  }

  // 2. Validation
  const parsed = postSchema.safeParse(data);
  if (!parsed.success) {
    return {
      success: false,
      error: "Validation failed",
      fieldErrors: parsed.error.flatten().fieldErrors
    };
  }

  // 3. Database operation
  const [error, post] = await createPostInDb({
    ...parsed.data,
    authorId: userId
  });

  if (error) {
    logger.error({ userId, error }, "Failed to create post");
    return { success: false, error: "Failed to create post" };
  }

  // 4. Revalidate cache
  revalidatePath("/posts");

  // 5. Return success with data
  logger.info({ userId, postId: post.id }, "Post created");
  return {
    success: true,
    data: post,
    message: "Post created successfully"
  };
}
```

### Read (Single Item)

```typescript
// features/posts/server/actions/get-post.ts
"use server";

import { getPostById } from "../db/posts";
import type { ActionResponse } from "~/lib/action-types";
import type { Post } from "../../types/post";

export async function getPost(postId: string): ActionResponse<Post> {
  if (!postId) {
    return { success: false, error: "Post ID is required" };
  }

  const [error, post] = await getPostById(postId);

  if (error) {
    if (error.isNotFound) {
      return { success: false, error: "Post not found" };
    }
    return { success: false, error: "Failed to fetch post" };
  }

  return { success: true, data: post };
}
```

### Update

```typescript
// features/posts/server/actions/update-post.ts
"use server";

import { revalidatePath } from "next/cache";
import { auth } from "@clerk/nextjs/server";
import { getPostById, updatePostInDb } from "../db/posts";
import { updatePostSchema, type UpdatePostData } from "../../schemas/post";
import type { ActionResponse } from "~/lib/action-types";
import type { Post } from "../../types/post";
import { createLogger } from "~/lib/logger";

const logger = createLogger({ module: "posts-actions" });

export async function updatePost(
  postId: string,
  data: UpdatePostData
): ActionResponse<Post> {
  // 1. Authentication
  const { userId } = await auth();
  if (!userId) {
    return { success: false, error: "Authentication required" };
  }

  // 2. Check ownership
  const [fetchError, existingPost] = await getPostById(postId);
  if (fetchError) {
    return { success: false, error: "Post not found" };
  }

  if (existingPost.authorId !== userId) {
    return { success: false, error: "Not authorized to edit this post" };
  }

  // 3. Validation
  const parsed = updatePostSchema.safeParse(data);
  if (!parsed.success) {
    return {
      success: false,
      error: "Validation failed",
      fieldErrors: parsed.error.flatten().fieldErrors
    };
  }

  // 4. Update in database
  const [error, updatedPost] = await updatePostInDb(postId, parsed.data);

  if (error) {
    logger.error({ userId, postId, error }, "Failed to update post");
    return { success: false, error: "Failed to update post" };
  }

  // 5. Revalidate cache
  revalidatePath("/posts");
  revalidatePath(`/posts/${postId}`);

  logger.info({ userId, postId }, "Post updated");
  return {
    success: true,
    data: updatedPost,
    message: "Post updated successfully"
  };
}
```

### Delete

```typescript
// features/posts/server/actions/delete-post.ts
"use server";

import { revalidatePath } from "next/cache";
import { auth } from "@clerk/nextjs/server";
import { getPostById, deletePostFromDb } from "../db/posts";
import type { ActionResponse } from "~/lib/action-types";
import { createLogger } from "~/lib/logger";

const logger = createLogger({ module: "posts-actions" });

export async function deletePost(postId: string): ActionResponse<void> {
  // 1. Authentication
  const { userId } = await auth();
  if (!userId) {
    return { success: false, error: "Authentication required" };
  }

  // 2. Check ownership
  const [fetchError, existingPost] = await getPostById(postId);
  if (fetchError) {
    return { success: false, error: "Post not found" };
  }

  if (existingPost.authorId !== userId) {
    return { success: false, error: "Not authorized to delete this post" };
  }

  // 3. Delete from database
  const [error] = await deletePostFromDb(postId);

  if (error) {
    logger.error({ userId, postId, error }, "Failed to delete post");
    return { success: false, error: "Failed to delete post" };
  }

  // 4. Revalidate cache
  revalidatePath("/posts");

  logger.info({ userId, postId }, "Post deleted");
  return { success: true, data: undefined, message: "Post deleted" };
}
```

---

## Form Submission with Redirect

For forms that should navigate to a new page after successful submission.

```typescript
// features/onboarding/server/actions/submit-preferences.ts
"use server";

import { redirect } from "next/navigation";
import { auth } from "@clerk/nextjs/server";
import { updateOnboarding } from "../db/onboarding";
import { preferencesSchema, type PreferencesFormData } from "../../schemas/preferences";
import type { RedirectAction } from "~/lib/action-types";
import type { Onboarding, UpdateOnboardingDto } from "../../types/onboarding";
import { createLogger } from "~/lib/logger";

const logger = createLogger({ module: "onboarding-actions" });

export async function submitPreferences(
  formData: PreferencesFormData,
  onboarding: Onboarding
): RedirectAction {
  const { userId } = await auth();
  logger.info({ userId, onboardingId: onboarding.id }, "Submitting preferences");

  // 1. Validation (optional if already validated client-side)
  const parsed = preferencesSchema.safeParse(formData);
  if (!parsed.success) {
    return {
      success: false,
      error: "Invalid preferences data",
      fieldErrors: parsed.error.flatten().fieldErrors
    };
  }

  // 2. Prepare update data
  const updateData: UpdateOnboardingDto = {
    currentStep: "budget-setup",
    preferences: parsed.data
  };

  // 3. Update database
  const [error] = await updateOnboarding(onboarding.id, updateData);

  if (error) {
    logger.error({ onboardingId: onboarding.id, error }, "Failed to save preferences");
    return { success: false, error: error.message };
  }

  // 4. Redirect to next step (never returns on success)
  logger.info({ onboardingId: onboarding.id }, "Preferences saved, redirecting");
  redirect("/onboarding/budget-setup");
}
```

### Usage in Page Component

```typescript
// app/onboarding/preferences/page.tsx
import { auth } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import { getOnboardingById } from "~/features/onboarding/server/db/onboarding";
import { PreferencesForm } from "~/features/onboarding/components/preferences-form";
import { submitPreferences } from "~/features/onboarding/server/actions/submit-preferences";
import type { PreferencesFormData } from "~/features/onboarding/schemas/preferences";

export default async function PreferencesPage() {
  const { userId } = await auth();
  if (!userId) redirect("/sign-in");

  const [error, onboarding] = await getOnboardingById(userId);
  if (error?.isNotFound) redirect("/onboarding/welcome");
  if (error) throw error;

  // Bind onboarding to the action
  async function handleSubmit(data: PreferencesFormData) {
    "use server";
    return await submitPreferences(data, onboarding);
  }

  return (
    <PreferencesForm
      onSubmitAction={handleSubmit}
      defaultValues={onboarding.preferences}
    />
  );
}
```

---

## Multi-Step Form Flow

Pattern for wizard-like forms with skip functionality.

```typescript
// features/onboarding/server/actions/submit-investments.ts
"use server";

import { redirect } from "next/navigation";
import { updateOnboarding } from "../db/onboarding";
import type { RedirectAction } from "~/lib/action-types";
import type { Investment, Onboarding, UpdateOnboardingDto } from "../../types/onboarding";
import { setToastCookie } from "~/lib/toast/server/toast.cookie";
import { createLogger } from "~/lib/logger";

const logger = createLogger({ module: "onboarding-actions" });

// Main submission action
export async function submitInvestments(
  investments: Investment[],
  onboarding: Onboarding
): RedirectAction {
  logger.info({ onboardingId: onboarding.id, count: investments.length }, "Submitting investments");

  const updateData: UpdateOnboardingDto = {
    currentStep: "complete",
    investments
  };

  const [error] = await updateOnboarding(onboarding.id, updateData);

  if (error) {
    logger.error({ onboardingId: onboarding.id, error }, "Failed to save investments");
    return { success: false, error: error.message };
  }

  await setToastCookie("Investment accounts saved successfully!", "success");
  redirect("/onboarding/complete");
}

// Skip action for optional steps
export async function skipInvestments(onboarding: Onboarding): RedirectAction {
  logger.info({ onboardingId: onboarding.id }, "Skipping investments step");

  const updateData: UpdateOnboardingDto = {
    currentStep: "complete",
    investments: [] // Empty array to indicate skipped
  };

  const [error] = await updateOnboarding(onboarding.id, updateData);

  if (error) {
    return { success: false, error: error.message };
  }

  await setToastCookie("Investments step skipped. You can add accounts later.", "info");
  redirect("/onboarding/complete");
}
```

---

## Action with Toast Notifications

Using cookie-based toasts for server-to-client messaging.

```typescript
// features/settings/server/actions/update-profile.ts
"use server";

import { revalidatePath } from "next/cache";
import { auth } from "@clerk/nextjs/server";
import { updateUserProfile } from "../db/users";
import { profileSchema, type ProfileFormData } from "../../schemas/profile";
import type { ActionResponse } from "~/lib/action-types";
import type { UserProfile } from "../../types/user";
import { setToastCookie } from "~/lib/toast/server/toast.cookie";
import { createLogger } from "~/lib/logger";

const logger = createLogger({ module: "settings-actions" });

export async function updateProfile(data: ProfileFormData): ActionResponse<UserProfile> {
  const { userId } = await auth();
  if (!userId) {
    return { success: false, error: "Authentication required" };
  }

  // Validation
  const parsed = profileSchema.safeParse(data);
  if (!parsed.success) {
    await setToastCookie("Please fix the errors in the form", "error");
    return {
      success: false,
      error: "Validation failed",
      fieldErrors: parsed.error.flatten().fieldErrors
    };
  }

  // Update database
  const [error, profile] = await updateUserProfile(userId, parsed.data);

  if (error) {
    logger.error({ userId, error }, "Failed to update profile");
    await setToastCookie("Failed to update profile. Please try again.", "error");
    return { success: false, error: "Failed to update profile" };
  }

  // Success
  revalidatePath("/settings/profile");
  await setToastCookie("Profile updated successfully!", "success");

  return {
    success: true,
    data: profile
  };
}
```

### Toast Cookie Implementation

```typescript
// lib/toast/server/toast.cookie.ts
"use server";

import { cookies } from "next/headers";

export type ToastType = "success" | "error" | "warning" | "info";

type ToastData = {
  type: ToastType;
  message: string;
  duration?: number;
};

const COOKIE_NAME = "app-toast";
const DEFAULT_DURATION = 5000; // 5 seconds

export async function setToastCookie(
  message: string,
  type: ToastType = "success",
  duration: number = DEFAULT_DURATION
) {
  const cookieStore = await cookies();

  const toastData: ToastData = { type, message, duration };

  cookieStore.set(COOKIE_NAME, JSON.stringify(toastData), {
    maxAge: 5, // Cookie expires in 5 seconds
    path: "/",
    httpOnly: false, // Must be accessible to client JS
    sameSite: "lax",
    secure: process.env.NODE_ENV === "production"
  });
}
```

---

## Action with Authentication

Complete authentication and authorization pattern.

```typescript
// features/admin/server/actions/manage-users.ts
"use server";

import { auth } from "@clerk/nextjs/server";
import { getUserRole, banUserInDb, unbanUserInDb } from "../db/users";
import type { ActionResponse } from "~/lib/action-types";
import { createLogger } from "~/lib/logger";

const logger = createLogger({ module: "admin-actions" });

export async function banUser(targetUserId: string, reason: string): ActionResponse<void> {
  // 1. Get current user
  const { userId } = await auth();
  if (!userId) {
    return { success: false, error: "Authentication required" };
  }

  // 2. Check admin permission
  const [roleError, role] = await getUserRole(userId);
  if (roleError || role !== "admin") {
    logger.warn({ userId, targetUserId }, "Unauthorized ban attempt");
    return { success: false, error: "Admin access required" };
  }

  // 3. Prevent self-ban
  if (userId === targetUserId) {
    return { success: false, error: "Cannot ban yourself" };
  }

  // 4. Validate reason
  if (!reason || reason.length < 10) {
    return { success: false, error: "Ban reason must be at least 10 characters" };
  }

  // 5. Perform ban
  const [error] = await banUserInDb(targetUserId, {
    bannedBy: userId,
    reason,
    bannedAt: new Date()
  });

  if (error) {
    logger.error({ userId, targetUserId, error }, "Failed to ban user");
    return { success: false, error: "Failed to ban user" };
  }

  // 6. Audit log
  logger.info({ adminId: userId, targetUserId, reason }, "User banned");

  return { success: true, data: undefined, message: "User banned successfully" };
}
```

---

## Action with useActionState

Pattern for forms using React 19's useActionState hook.

```typescript
// features/contact/server/actions/send-message.ts
"use server";

import { z } from "zod";
import { sendEmail } from "~/lib/email";
import type { ActionResponse } from "~/lib/action-types";

const contactSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  email: z.string().email("Invalid email address"),
  message: z.string().min(10, "Message must be at least 10 characters")
});

type ContactState = Awaited<ActionResponse<{ sent: boolean }>>;

// Action signature for useActionState: (prevState, formData) => newState
export async function sendContactMessage(
  previousState: ContactState | null,
  formData: FormData
): ActionResponse<{ sent: boolean }> {
  // Extract form data
  const rawData = {
    name: formData.get("name"),
    email: formData.get("email"),
    message: formData.get("message")
  };

  // Validate
  const parsed = contactSchema.safeParse(rawData);
  if (!parsed.success) {
    return {
      success: false,
      error: "Please fix the errors below",
      fieldErrors: parsed.error.flatten().fieldErrors
    };
  }

  // Send email
  try {
    await sendEmail({
      to: "support@example.com",
      subject: `Contact from ${parsed.data.name}`,
      body: parsed.data.message,
      replyTo: parsed.data.email
    });
  } catch (error) {
    return { success: false, error: "Failed to send message. Please try again." };
  }

  return {
    success: true,
    data: { sent: true },
    message: "Message sent successfully!"
  };
}
```

### Client Component with useActionState

```typescript
// features/contact/components/contact-form.tsx
"use client";

import { useActionState } from "react";
import { sendContactMessage } from "../server/actions/send-message";

export function ContactForm() {
  const [state, formAction, pending] = useActionState(sendContactMessage, null);

  // Show success message
  if (state?.success) {
    return (
      <div className="text-center p-8">
        <h2 className="text-2xl font-bold text-green-600">Thank you!</h2>
        <p>{state.message}</p>
      </div>
    );
  }

  return (
    <form action={formAction} className="space-y-4">
      <div>
        <label htmlFor="name">Name</label>
        <input
          id="name"
          name="name"
          type="text"
          required
          aria-describedby={state?.fieldErrors?.name ? "name-error" : undefined}
        />
        {state?.fieldErrors?.name && (
          <p id="name-error" className="text-red-500 text-sm">
            {state.fieldErrors.name[0]}
          </p>
        )}
      </div>

      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          name="email"
          type="email"
          required
          aria-describedby={state?.fieldErrors?.email ? "email-error" : undefined}
        />
        {state?.fieldErrors?.email && (
          <p id="email-error" className="text-red-500 text-sm">
            {state.fieldErrors.email[0]}
          </p>
        )}
      </div>

      <div>
        <label htmlFor="message">Message</label>
        <textarea
          id="message"
          name="message"
          rows={4}
          required
          aria-describedby={state?.fieldErrors?.message ? "message-error" : undefined}
        />
        {state?.fieldErrors?.message && (
          <p id="message-error" className="text-red-500 text-sm">
            {state.fieldErrors.message[0]}
          </p>
        )}
      </div>

      {/* General error message */}
      {state && !state.success && !state.fieldErrors && (
        <p className="text-red-500" role="alert">
          {state.error}
        </p>
      )}

      <button type="submit" disabled={pending}>
        {pending ? "Sending..." : "Send Message"}
      </button>
    </form>
  );
}
```

---

## Batch Operations

Pattern for actions that operate on multiple items.

```typescript
// features/posts/server/actions/batch-delete.ts
"use server";

import { revalidatePath } from "next/cache";
import { auth } from "@clerk/nextjs/server";
import { getPostsByIds, deletePostsFromDb } from "../db/posts";
import type { ActionResponse } from "~/lib/action-types";
import { createLogger } from "~/lib/logger";

const logger = createLogger({ module: "posts-actions" });

type BatchDeleteResult = {
  deleted: number;
  failed: string[];
};

export async function batchDeletePosts(postIds: string[]): ActionResponse<BatchDeleteResult> {
  // 1. Validate input
  if (!postIds.length) {
    return { success: false, error: "No posts selected" };
  }

  if (postIds.length > 50) {
    return { success: false, error: "Maximum 50 posts can be deleted at once" };
  }

  // 2. Authentication
  const { userId } = await auth();
  if (!userId) {
    return { success: false, error: "Authentication required" };
  }

  // 3. Verify ownership of all posts
  const [fetchError, posts] = await getPostsByIds(postIds);
  if (fetchError) {
    return { success: false, error: "Failed to fetch posts" };
  }

  const unauthorized = posts.filter(post => post.authorId !== userId);
  if (unauthorized.length > 0) {
    return {
      success: false,
      error: `Not authorized to delete ${unauthorized.length} post(s)`
    };
  }

  // 4. Delete posts
  const [error, result] = await deletePostsFromDb(postIds);

  if (error) {
    logger.error({ userId, postIds, error }, "Failed to batch delete posts");
    return { success: false, error: "Failed to delete posts" };
  }

  // 5. Revalidate cache
  revalidatePath("/posts");

  logger.info({ userId, deletedCount: result.deleted }, "Posts batch deleted");

  return {
    success: true,
    data: result,
    message: `${result.deleted} post(s) deleted successfully`
  };
}
```

---

## File Upload Action

Pattern for handling file uploads with server actions.

```typescript
// features/uploads/server/actions/upload-file.ts
"use server";

import { auth } from "@clerk/nextjs/server";
import { uploadToStorage, createFileRecord } from "../db/files";
import type { ActionResponse } from "~/lib/action-types";
import type { UploadedFile } from "../../types/file";
import { createLogger } from "~/lib/logger";

const logger = createLogger({ module: "upload-actions" });

const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
const ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp", "application/pdf"];

export async function uploadFile(formData: FormData): ActionResponse<UploadedFile> {
  // 1. Authentication
  const { userId } = await auth();
  if (!userId) {
    return { success: false, error: "Authentication required" };
  }

  // 2. Get file from form data
  const file = formData.get("file") as File | null;
  if (!file) {
    return { success: false, error: "No file provided" };
  }

  // 3. Validate file type
  if (!ALLOWED_TYPES.includes(file.type)) {
    return {
      success: false,
      error: `Invalid file type. Allowed: ${ALLOWED_TYPES.join(", ")}`
    };
  }

  // 4. Validate file size
  if (file.size > MAX_FILE_SIZE) {
    return {
      success: false,
      error: `File too large. Maximum size: ${MAX_FILE_SIZE / 1024 / 1024}MB`
    };
  }

  // 5. Upload to storage
  const [uploadError, storageUrl] = await uploadToStorage(file, userId);
  if (uploadError) {
    logger.error({ userId, fileName: file.name, error: uploadError }, "Upload failed");
    return { success: false, error: "Failed to upload file" };
  }

  // 6. Create database record
  const [dbError, fileRecord] = await createFileRecord({
    userId,
    fileName: file.name,
    fileType: file.type,
    fileSize: file.size,
    url: storageUrl
  });

  if (dbError) {
    logger.error({ userId, storageUrl, error: dbError }, "Failed to create file record");
    return { success: false, error: "Failed to save file record" };
  }

  logger.info({ userId, fileId: fileRecord.id }, "File uploaded successfully");

  return {
    success: true,
    data: fileRecord,
    message: "File uploaded successfully"
  };
}
```

### Client Component for File Upload

```typescript
// features/uploads/components/file-upload-form.tsx
"use client";

import { useRef, useState, useTransition } from "react";
import { uploadFile } from "../server/actions/upload-file";
import type { UploadedFile } from "../types/file";

export function FileUploadForm({ onSuccess }: { onSuccess?: (file: UploadedFile) => void }) {
  const formRef = useRef<HTMLFormElement>(null);
  const [isPending, startTransition] = useTransition();
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(formData: FormData) {
    setError(null);

    startTransition(async () => {
      const result = await uploadFile(formData);

      if (result.success) {
        formRef.current?.reset();
        onSuccess?.(result.data);
      } else {
        setError(result.error);
      }
    });
  }

  return (
    <form ref={formRef} action={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="file">Choose file</label>
        <input
          id="file"
          name="file"
          type="file"
          accept=".jpg,.jpeg,.png,.webp,.pdf"
          required
          disabled={isPending}
        />
      </div>

      {error && (
        <p className="text-red-500" role="alert">{error}</p>
      )}

      <button type="submit" disabled={isPending}>
        {isPending ? "Uploading..." : "Upload"}
      </button>
    </form>
  );
}
```
