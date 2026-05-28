---
name: fab-actions
description: Floating Action Button (FAB) for form actions. Use when adding Save/Cancel buttons to forms that need to be accessible while scrolling through long content.
---

# FAB Actions

## Overview
This skill provides a Floating Action Button (FAB) pattern for form action buttons (Save, Cancel, etc.). The FAB stays fixed at the bottom-right corner and expands on click to reveal action buttons.

## Features
- Fixed position at bottom-right corner
- Click to expand/collapse
- Plus icon rotates 45° to become X when expanded
- Smooth animations with transitions
- Buttons are colinear (vertically aligned)
- Works with forms (submit button support)

## Required Imports

```typescript
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, Save, X } from 'lucide-react';
```

## State Setup

Add the FAB state to your component:

```typescript
const [fabOpen, setFabOpen] = useState(false);
```

## FAB Component Template

Place this at the end of your form, before the closing `</form>` tag:

```tsx
{/* Action Buttons - FAB */}
<div className="fixed bottom-8 right-8 z-50 flex flex-col items-center gap-3">
  {/* Expandable Buttons */}
  <div className={`flex flex-col items-center gap-3 transition-all duration-300 ${fabOpen ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4 pointer-events-none'}`}>
    {/* Cancel Button */}
    <button
      type="button"
      className="btn btn-lg btn-circle shadow-md bg-base-100 hover:bg-base-200"
      onClick={() => {
        navigate('/admin/your-route');
        setFabOpen(false);
      }}
      disabled={isLoading}
    >
      <X className="w-5 h-5" />
    </button>

    {/* Save/Update Button */}
    <button
      type="submit"
      className="btn btn-lg btn-circle btn-success shadow-md"
      disabled={isLoading}
    >
      {isSubmitting ? (
        <span className="loading loading-spinner loading-sm"></span>
      ) : (
        <Save className="w-5 h-5" />
      )}
    </button>
  </div>

  {/* Main FAB Trigger */}
  <button
    type="button"
    className={`btn btn-lg btn-circle btn-primary shadow-lg transition-transform duration-300 ${fabOpen ? 'rotate-45' : ''}`}
    onClick={() => setFabOpen(!fabOpen)}
  >
    <Plus className="w-5 h-5" />
  </button>
</div>
```

## Customization

### Button Order
Buttons appear from top to bottom in the expanded state:
1. Cancel (top) - furthest from trigger
2. Save (middle) - closer to trigger
3. FAB Trigger (bottom) - always visible

### Adding More Actions
Add buttons inside the expandable div, before the Cancel button:

```tsx
<div className={`flex flex-col items-center gap-3 transition-all duration-300 ${fabOpen ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4 pointer-events-none'}`}>
  {/* Delete Button (optional) */}
  <button
    type="button"
    className="btn btn-lg btn-circle btn-error shadow-md"
    onClick={handleDelete}
    disabled={isLoading}
  >
    <Trash className="w-5 h-5" />
  </button>

  {/* Cancel Button */}
  <button ...>
    <X className="w-5 h-5" />
  </button>

  {/* Save Button */}
  <button ...>
    <Save className="w-5 h-5" />
  </button>
</div>
```

### Button Variants

```tsx
// Primary action (main trigger)
className="btn btn-lg btn-circle btn-primary shadow-lg"

// Success action (save/confirm)
className="btn btn-lg btn-circle btn-success shadow-md"

// Neutral action (cancel)
className="btn btn-lg btn-circle shadow-md bg-base-100 hover:bg-base-200"

// Danger action (delete)
className="btn btn-lg btn-circle btn-error shadow-md"

// Secondary action
className="btn btn-lg btn-circle btn-secondary shadow-md"
```

### Icon Options

Common icons for FAB actions:
```typescript
import {
  Plus,      // Main trigger
  Save,      // Save/Update
  X,         // Cancel/Close
  Trash,     // Delete
  Check,     // Confirm
  Send,      // Submit/Send
  Download,  // Download
  Upload,    // Upload
  Edit,      // Edit mode
  Eye,       // Preview
} from 'lucide-react';
```

## Animation Details

### Transition Classes
- `transition-all duration-300` - Smooth 300ms transition
- `opacity-0` / `opacity-100` - Fade effect
- `translate-y-4` / `translate-y-0` - Slide up effect
- `pointer-events-none` - Disable clicks when collapsed
- `rotate-45` - Rotates Plus to X shape

### Customizing Animation Speed
```tsx
// Faster (200ms)
className="transition-all duration-200"

// Slower (500ms)
className="transition-all duration-500"
```

## Complete Example

```typescript
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { Plus, Save, X } from 'lucide-react';

export default function MyForm({ id }: { id?: string }) {
  const navigate = useNavigate();
  const [fabOpen, setFabOpen] = useState(false);

  const {
    handleSubmit,
    formState: { isSubmitting },
  } = useForm();

  const isLoading = isSubmitting;

  const onSubmit = async (data: FormData) => {
    // Submit logic
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* Form fields here */}

      {/* FAB Actions */}
      <div className="fixed bottom-8 right-8 z-50 flex flex-col items-center gap-3">
        <div className={`flex flex-col items-center gap-3 transition-all duration-300 ${fabOpen ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4 pointer-events-none'}`}>
          <button
            type="button"
            className="btn btn-lg btn-circle shadow-md bg-base-100 hover:bg-base-200"
            onClick={() => {
              navigate('/admin/list');
              setFabOpen(false);
            }}
            disabled={isLoading}
          >
            <X className="w-5 h-5" />
          </button>

          <button
            type="submit"
            className="btn btn-lg btn-circle btn-success shadow-md"
            disabled={isLoading}
          >
            {isSubmitting ? (
              <span className="loading loading-spinner loading-sm"></span>
            ) : (
              <Save className="w-5 h-5" />
            )}
          </button>
        </div>

        <button
          type="button"
          className={`btn btn-lg btn-circle btn-primary shadow-lg transition-transform duration-300 ${fabOpen ? 'rotate-45' : ''}`}
          onClick={() => setFabOpen(!fabOpen)}
        >
          <Plus className="w-5 h-5" />
        </button>
      </div>
    </form>
  );
}
```

## Accessibility

- FAB uses semantic `<button>` elements
- Proper `type="button"` for non-submit buttons
- `type="submit"` for form submission
- `disabled` state handled for loading
- Keyboard accessible (Tab, Enter, Space)

## Best Practices

1. Keep the FAB trigger always visible
2. Use consistent button sizes (`btn-lg btn-circle`)
3. Use distinct colors for different actions
4. Add shadows for depth (`shadow-md`, `shadow-lg`)
5. Include loading states for submit buttons
6. Close FAB after navigation actions
7. Use icons without text for circle buttons
