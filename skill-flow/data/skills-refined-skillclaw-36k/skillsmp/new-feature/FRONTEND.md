# Frontend Implementation Guide

Step-by-step instructions for implementing frontend components of a new feature.

## 1. TypeScript Types

**Add to resources/js/types/index.d.ts:**

```typescript
export interface FeatureItem {
    id: number;
    user_id: number;
    title: string;
    description: string | null;
    status: 'draft' | 'active' | 'archived';
    created_at: string;
    updated_at: string;
}

export interface FeatureItemFormData {
    title: string;
    description: string;
    status: 'draft' | 'active' | 'archived';
}
```

## 2. Page Components

### Index Page

```tsx
// resources/js/pages/feature-items/index.tsx
import { Head, Link } from '@inertiajs/react';
import { FeatureItem } from '@/types';

interface Props {
    items: {
        data: FeatureItem[];
        links: any;
    };
}

export default function FeatureItemsIndex({ items }: Props) {
    return (
        <>
            <Head title="Feature Items" />

            <div className="container mx-auto py-8">
                <div className="mb-6 flex items-center justify-between">
                    <h1 className="text-2xl font-bold">Feature Items</h1>
                    <Link href="/feature-items/create" className="btn btn-primary">
                        Create New
                    </Link>
                </div>

                <div className="space-y-4">
                    {items.data.map((item) => (
                        <div key={item.id} className="rounded-lg bg-white p-4 shadow">
                            <h2 className="font-semibold">{item.title}</h2>
                            <p className="text-gray-600">{item.description}</p>
                            <span className="text-sm text-gray-500">{item.status}</span>
                        </div>
                    ))}
                </div>
            </div>
        </>
    );
}
```

### Create/Edit Page with Form

```tsx
// resources/js/pages/feature-items/create.tsx
import { Head } from '@inertiajs/react';
import { useForm } from '@inertiajs/react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

interface FormData {
    title: string;
    description: string;
    status: 'draft' | 'active' | 'archived';
}

export default function FeatureItemCreate() {
    const { data, setData, post, processing, errors } = useForm<FormData>({
        title: '',
        description: '',
        status: 'draft',
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        post('/feature-items');
    };

    return (
        <>
            <Head title="Create Feature Item" />

            <div className="container mx-auto max-w-2xl py-8">
                <h1 className="mb-6 text-2xl font-bold">Create Feature Item</h1>

                <form onSubmit={handleSubmit} className="space-y-6">
                    <div className="space-y-2">
                        <Label htmlFor="title">
                            Title <span className="text-error">*</span>
                        </Label>
                        <Input
                            id="title"
                            value={data.title}
                            onChange={(e) => setData('title', e.target.value)}
                            aria-invalid={!!errors.title}
                            className={errors.title ? 'border-error' : ''}
                        />
                        {errors.title && <p className="text-sm text-error">{errors.title}</p>}
                    </div>

                    <div className="space-y-2">
                        <Label htmlFor="description">Description</Label>
                        <Textarea id="description" value={data.description} onChange={(e) => setData('description', e.target.value)} rows={4} />
                        {errors.description && <p className="text-sm text-error">{errors.description}</p>}
                    </div>

                    <div className="space-y-2">
                        <Label htmlFor="status">
                            Status <span className="text-error">*</span>
                        </Label>
                        <Select value={data.status} onValueChange={(value) => setData('status', value as FormData['status'])}>
                            <SelectTrigger>
                                <SelectValue placeholder="Select status" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="draft">Draft</SelectItem>
                                <SelectItem value="active">Active</SelectItem>
                                <SelectItem value="archived">Archived</SelectItem>
                            </SelectContent>
                        </Select>
                        {errors.status && <p className="text-sm text-error">{errors.status}</p>}
                    </div>

                    <div className="flex gap-4">
                        <Button type="submit" disabled={processing}>
                            {processing ? 'Creating...' : 'Create Item'}
                        </Button>
                        <Button type="button" variant="outline" asChild>
                            <Link href="/feature-items">Cancel</Link>
                        </Button>
                    </div>
                </form>
            </div>
        </>
    );
}
```

## 3. Translations (i18n)

Add translations for the feature. RentPath uses route-based translation organization:

```php
// resources/lang/en/feature-items.php
return [
    'title' => 'Feature Items',
    'create' => 'Create Feature Item',
    'edit' => 'Edit Feature Item',

    'form' => [
        'title' => [
            'label' => 'Title',
            'placeholder' => 'Enter title...',
        ],
        'description' => [
            'label' => 'Description',
            'placeholder' => 'Enter description...',
        ],
        'status' => [
            'label' => 'Status',
            'options' => [
                'draft' => 'Draft',
                'active' => 'Active',
                'archived' => 'Archived',
            ],
        ],
    ],

    'actions' => [
        'create' => 'Create Item',
        'update' => 'Update Item',
        'delete' => 'Delete Item',
        'cancel' => 'Cancel',
    ],

    'messages' => [
        'created' => 'Item created successfully',
        'updated' => 'Item updated successfully',
        'deleted' => 'Item deleted successfully',
    ],
];
```

Remember to add translations for all 4 locales (en, de, fr, nl). See `docs/architecture/i18n.md`.

## 4. Component Patterns

### Loading States

```tsx
{
    isLoading ? (
        <div className="space-y-4">
            <Skeleton className="h-20 w-full" />
            <Skeleton className="h-20 w-full" />
            <Skeleton className="h-20 w-full" />
        </div>
    ) : (
        <ItemList items={items} />
    );
}
```

### Error States

```tsx
{
    error && (
        <div className="rounded-lg bg-error/10 p-4 text-error">
            <p>{error.message}</p>
        </div>
    );
}
```

### Empty States

```tsx
{
    items.length === 0 && (
        <div className="py-12 text-center">
            <p className="text-muted-foreground">No items found</p>
            <Link href="/feature-items/create" className="btn btn-primary mt-4">
                Create your first item
            </Link>
        </div>
    );
}
```

## 5. Tailwind Best Practices

### Use Semantic Colors

```tsx
// GOOD
<p className="text-error">Error message</p>
<p className="text-success">Success message</p>
<div className="bg-primary text-primary-foreground">Button</div>

// BAD
<p className="text-red-500">Error message</p>
<div className="bg-blue-600 text-white">Button</div>
```

### Use Gap for Spacing

```tsx
// GOOD
<div className="flex gap-4">
    <Button>One</Button>
    <Button>Two</Button>
</div>

// BAD
<div className="flex">
    <Button className="mr-4">One</Button>
    <Button>Two</Button>
</div>
```

## 6. Accessibility Checklist

```
[ ] Labels associated with inputs (htmlFor/id)
[ ] aria-invalid on invalid inputs
[ ] Required fields marked visually
[ ] Error messages linked to inputs (aria-describedby)
[ ] Focus management after actions
[ ] Semantic HTML (button, nav, main, etc.)
```
