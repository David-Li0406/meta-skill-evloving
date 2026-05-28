# Frontend Development Templates

Quick copy-paste templates for common frontend patterns.

---

## Component Template

```tsx
"use client";

import { useState, useCallback } from "react";

/**
 * Props for the ComponentName component.
 */
interface ComponentNameProps {
  /** Description of this prop */
  title: string;
  /** Optional prop with default */
  variant?: "default" | "primary" | "secondary";
  /** Event handler */
  onAction?: () => void;
}

/**
 * Brief description of what this component does.
 *
 * @example
 * <ComponentName title="Hello" onAction={() => console.log("clicked")} />
 */
export function ComponentName({
  title,
  variant = "default",
  onAction,
}: ComponentNameProps): JSX.Element {
  const [isActive, setIsActive] = useState(false);

  const handleClick = useCallback(() => {
    setIsActive(true);
    onAction?.();
  }, [onAction]);

  return (
    <div className="card bg-base-100 shadow-xl">
      <div className="card-body">
        <h2 className="card-title">{title}</h2>
        <button
          className={`btn btn-${variant}`}
          onClick={handleClick}
        >
          {isActive ? "Active" : "Click me"}
        </button>
      </div>
    </div>
  );
}
```

---

## Server Component Template

```tsx
import { SomeClient } from "@/lib/api/someClient";

/**
 * Page metadata for SEO.
 */
export const metadata = {
  title: "Page Title | Claude Assistant",
  description: "Brief page description for search engines",
};

/**
 * Server component that fetches data on the server.
 */
export default async function ServerPage(): Promise<JSX.Element> {
  // Fetch data on the server
  const data = await SomeClient.fetchData();

  return (
    <main className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Page Title</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {data.map((item) => (
          <div key={item.id} className="card bg-base-100 shadow">
            <div className="card-body">
              <h2 className="card-title">{item.name}</h2>
              <p>{item.description}</p>
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}
```

---

## Zustand Store Template

```tsx
/**
 * State management for {feature}.
 */

import { create } from "zustand";
import { persist } from "zustand/middleware";

/**
 * Item interface.
 */
interface Item {
  id: string;
  name: string;
  status: "pending" | "active" | "completed";
}

/**
 * Store state interface.
 */
interface FeatureState {
  // State
  items: Item[];
  selectedId: string | null;
  isLoading: boolean;
  error: string | null;

  // Actions
  fetchItems: () => Promise<void>;
  addItem: (item: Omit<Item, "id">) => void;
  updateItem: (id: string, updates: Partial<Item>) => void;
  deleteItem: (id: string) => void;
  selectItem: (id: string | null) => void;
  clearError: () => void;
}

/**
 * Generate unique ID.
 */
const generateId = (): string => {
  return `${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
};

/**
 * API base URL.
 */
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Zustand store for {feature}.
 */
export const useFeatureStore = create<FeatureState>()(
  persist(
    (set, get) => ({
      items: [],
      selectedId: null,
      isLoading: false,
      error: null,

      fetchItems: async () => {
        set({ isLoading: true, error: null });
        try {
          const response = await fetch(`${API_URL}/api/items`);
          if (!response.ok) throw new Error("Failed to fetch items");
          const items = await response.json();
          set({ items, isLoading: false });
        } catch (error) {
          set({
            error: error instanceof Error ? error.message : "Unknown error",
            isLoading: false,
          });
        }
      },

      addItem: (item) => {
        const newItem: Item = { ...item, id: generateId() };
        set((state) => ({ items: [...state.items, newItem] }));
      },

      updateItem: (id, updates) => {
        set((state) => ({
          items: state.items.map((item) =>
            item.id === id ? { ...item, ...updates } : item
          ),
        }));
      },

      deleteItem: (id) => {
        set((state) => ({
          items: state.items.filter((item) => item.id !== id),
          selectedId: state.selectedId === id ? null : state.selectedId,
        }));
      },

      selectItem: (id) => set({ selectedId: id }),

      clearError: () => set({ error: null }),
    }),
    {
      name: "claude-assistant-feature",
      partialize: (state) => ({
        items: state.items,
      }),
    }
  )
);
```

---

## API Client Template

```tsx
/**
 * API client for {resource} operations.
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Resource response type.
 */
export interface Resource {
  id: string;
  name: string;
  description: string;
  createdAt: string;
  updatedAt: string;
}

/**
 * Request type for creating a resource.
 */
export interface CreateResourceRequest {
  name: string;
  description?: string;
}

/**
 * Request type for updating a resource.
 */
export interface UpdateResourceRequest {
  name?: string;
  description?: string;
}

/**
 * List response with pagination.
 */
export interface ResourceListResponse {
  items: Resource[];
  total: number;
  page: number;
  pageSize: number;
}

/**
 * API error class for structured error handling.
 */
export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public detail?: string
  ) {
    super(message);
    this.name = "ApiError";
  }
}

/**
 * Helper to handle API responses.
 */
async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new ApiError(
      error.detail || `Request failed: ${response.status}`,
      response.status,
      error.detail
    );
  }
  return response.json();
}

/**
 * Fetch all resources with optional pagination.
 */
export async function getResources(
  page = 1,
  pageSize = 20
): Promise<ResourceListResponse> {
  const params = new URLSearchParams({
    page: page.toString(),
    page_size: pageSize.toString(),
  });

  const response = await fetch(`${API_URL}/api/resources?${params}`);
  return handleResponse<ResourceListResponse>(response);
}

/**
 * Fetch a single resource by ID.
 */
export async function getResource(id: string): Promise<Resource> {
  const response = await fetch(`${API_URL}/api/resources/${id}`);
  return handleResponse<Resource>(response);
}

/**
 * Create a new resource.
 */
export async function createResource(
  data: CreateResourceRequest
): Promise<Resource> {
  const response = await fetch(`${API_URL}/api/resources`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return handleResponse<Resource>(response);
}

/**
 * Update an existing resource.
 */
export async function updateResource(
  id: string,
  data: UpdateResourceRequest
): Promise<Resource> {
  const response = await fetch(`${API_URL}/api/resources/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return handleResponse<Resource>(response);
}

/**
 * Delete a resource.
 */
export async function deleteResource(id: string): Promise<void> {
  const response = await fetch(`${API_URL}/api/resources/${id}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new ApiError(
      error.detail || `Delete failed: ${response.status}`,
      response.status
    );
  }
}
```

---

## Form Component Template

```tsx
"use client";

import { useState, useCallback } from "react";

/**
 * Form data interface.
 */
interface FormData {
  name: string;
  description: string;
  priority: "low" | "medium" | "high";
}

/**
 * Props for the Form component.
 */
interface FormProps {
  /** Initial form values */
  initialData?: Partial<FormData>;
  /** Called when form is submitted */
  onSubmit: (data: FormData) => Promise<void>;
  /** Called when form is cancelled */
  onCancel?: () => void;
  /** Whether form is in loading state */
  isLoading?: boolean;
}

/**
 * Default form values.
 */
const defaultFormData: FormData = {
  name: "",
  description: "",
  priority: "medium",
};

/**
 * Reusable form component with validation.
 */
export function Form({
  initialData,
  onSubmit,
  onCancel,
  isLoading = false,
}: FormProps): JSX.Element {
  const [formData, setFormData] = useState<FormData>({
    ...defaultFormData,
    ...initialData,
  });
  const [errors, setErrors] = useState<Partial<Record<keyof FormData, string>>>({});

  /**
   * Handle input changes.
   */
  const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
      const { name, value } = e.target;
      setFormData((prev) => ({ ...prev, [name]: value }));
      // Clear error when user starts typing
      if (errors[name as keyof FormData]) {
        setErrors((prev) => ({ ...prev, [name]: undefined }));
      }
    },
    [errors]
  );

  /**
   * Validate form data.
   */
  const validate = useCallback((): boolean => {
    const newErrors: Partial<Record<keyof FormData, string>> = {};

    if (!formData.name.trim()) {
      newErrors.name = "Name is required";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  }, [formData]);

  /**
   * Handle form submission.
   */
  const handleSubmit = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault();

      if (!validate()) return;

      try {
        await onSubmit(formData);
      } catch (error) {
        console.error("Form submission error:", error);
      }
    },
    [formData, onSubmit, validate]
  );

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Name field */}
      <div className="form-control w-full">
        <label className="label">
          <span className="label-text">Name *</span>
        </label>
        <input
          type="text"
          name="name"
          value={formData.name}
          onChange={handleChange}
          className={`input input-bordered w-full ${errors.name ? "input-error" : ""}`}
          placeholder="Enter name"
          disabled={isLoading}
        />
        {errors.name && (
          <label className="label">
            <span className="label-text-alt text-error">{errors.name}</span>
          </label>
        )}
      </div>

      {/* Description field */}
      <div className="form-control w-full">
        <label className="label">
          <span className="label-text">Description</span>
        </label>
        <textarea
          name="description"
          value={formData.description}
          onChange={handleChange}
          className="textarea textarea-bordered w-full"
          placeholder="Enter description"
          rows={3}
          disabled={isLoading}
        />
      </div>

      {/* Priority field */}
      <div className="form-control w-full">
        <label className="label">
          <span className="label-text">Priority</span>
        </label>
        <select
          name="priority"
          value={formData.priority}
          onChange={handleChange}
          className="select select-bordered w-full"
          disabled={isLoading}
        >
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
      </div>

      {/* Actions */}
      <div className="flex justify-end gap-2 pt-4">
        {onCancel && (
          <button
            type="button"
            className="btn btn-ghost"
            onClick={onCancel}
            disabled={isLoading}
          >
            Cancel
          </button>
        )}
        <button
          type="submit"
          className="btn btn-primary"
          disabled={isLoading}
        >
          {isLoading ? (
            <>
              <span className="loading loading-spinner loading-sm" />
              Saving...
            </>
          ) : (
            "Save"
          )}
        </button>
      </div>
    </form>
  );
}
```

---

## Modal Component Template

```tsx
"use client";

import { useCallback, useEffect, useRef } from "react";

/**
 * Props for the Modal component.
 */
interface ModalProps {
  /** Whether the modal is open */
  isOpen: boolean;
  /** Called when modal should close */
  onClose: () => void;
  /** Modal title */
  title: string;
  /** Modal content */
  children: React.ReactNode;
  /** Optional footer actions */
  footer?: React.ReactNode;
  /** Modal size variant */
  size?: "sm" | "md" | "lg";
}

/**
 * Reusable modal dialog component.
 */
export function Modal({
  isOpen,
  onClose,
  title,
  children,
  footer,
  size = "md",
}: ModalProps): JSX.Element | null {
  const dialogRef = useRef<HTMLDialogElement>(null);

  /**
   * Sync dialog open state.
   */
  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;

    if (isOpen) {
      dialog.showModal();
    } else {
      dialog.close();
    }
  }, [isOpen]);

  /**
   * Handle backdrop click.
   */
  const handleBackdropClick = useCallback(
    (e: React.MouseEvent<HTMLDialogElement>) => {
      if (e.target === dialogRef.current) {
        onClose();
      }
    },
    [onClose]
  );

  /**
   * Handle escape key.
   */
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === "Escape" && isOpen) {
        onClose();
      }
    };

    document.addEventListener("keydown", handleEscape);
    return () => document.removeEventListener("keydown", handleEscape);
  }, [isOpen, onClose]);

  const sizeClasses = {
    sm: "max-w-sm",
    md: "max-w-md",
    lg: "max-w-2xl",
  };

  return (
    <dialog
      ref={dialogRef}
      className="modal"
      onClick={handleBackdropClick}
    >
      <div className={`modal-box ${sizeClasses[size]}`}>
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-bold text-lg">{title}</h3>
          <button
            className="btn btn-sm btn-circle btn-ghost"
            onClick={onClose}
            aria-label="Close"
          >
            ✕
          </button>
        </div>

        {/* Content */}
        <div className="py-2">{children}</div>

        {/* Footer */}
        {footer && (
          <div className="modal-action mt-4">
            {footer}
          </div>
        )}
      </div>
    </dialog>
  );
}
```

---

## List with Loading/Empty States Template

```tsx
"use client";

import { useEffect } from "react";
import { useFeatureStore } from "@/stores/featureStore";

/**
 * Item card component.
 */
function ItemCard({ item }: { item: Item }): JSX.Element {
  return (
    <div className="card bg-base-100 shadow hover:shadow-lg transition-shadow">
      <div className="card-body">
        <h3 className="card-title">{item.name}</h3>
        <p className="text-base-content/70">{item.description}</p>
        <div className="card-actions justify-end mt-2">
          <button className="btn btn-sm btn-ghost">Edit</button>
          <button className="btn btn-sm btn-error btn-outline">Delete</button>
        </div>
      </div>
    </div>
  );
}

/**
 * Empty state component.
 */
function EmptyState(): JSX.Element {
  return (
    <div className="text-center py-12">
      <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-base-200 flex items-center justify-center">
        <span className="text-2xl">📋</span>
      </div>
      <h3 className="text-lg font-medium mb-2">No items yet</h3>
      <p className="text-base-content/60 mb-4">
        Get started by creating your first item.
      </p>
      <button className="btn btn-primary">Create Item</button>
    </div>
  );
}

/**
 * Loading skeleton component.
 */
function LoadingSkeleton(): JSX.Element {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {[1, 2, 3, 4, 5, 6].map((i) => (
        <div key={i} className="card bg-base-100 shadow">
          <div className="card-body">
            <div className="skeleton h-6 w-3/4 mb-2" />
            <div className="skeleton h-4 w-full" />
            <div className="skeleton h-4 w-2/3" />
          </div>
        </div>
      ))}
    </div>
  );
}

/**
 * Error state component.
 */
function ErrorState({ message, onRetry }: { message: string; onRetry: () => void }): JSX.Element {
  return (
    <div className="alert alert-error">
      <span>{message}</span>
      <button className="btn btn-sm" onClick={onRetry}>
        Retry
      </button>
    </div>
  );
}

/**
 * Item list component with all states handled.
 */
export function ItemList(): JSX.Element {
  const items = useFeatureStore((state) => state.items);
  const isLoading = useFeatureStore((state) => state.isLoading);
  const error = useFeatureStore((state) => state.error);
  const fetchItems = useFeatureStore((state) => state.fetchItems);

  useEffect(() => {
    fetchItems();
  }, [fetchItems]);

  // Error state
  if (error) {
    return <ErrorState message={error} onRetry={fetchItems} />;
  }

  // Loading state
  if (isLoading) {
    return <LoadingSkeleton />;
  }

  // Empty state
  if (items.length === 0) {
    return <EmptyState />;
  }

  // Success state
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {items.map((item) => (
        <ItemCard key={item.id} item={item} />
      ))}
    </div>
  );
}
```
