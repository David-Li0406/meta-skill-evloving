# Loading States with useTransition

## Basic Loading Button

```typescript
"use client"

import { Loader2 } from "lucide-react"
import { cn } from "@/lib/utils"

interface LoadingButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    loading?: boolean
    children: React.ReactNode
}

export function LoadingButton({
    loading = false,
    disabled,
    children,
    className,
    ...props
}: LoadingButtonProps) {
    return (
        <button
            disabled={disabled || loading}
            className={cn(
                "flex items-center gap-2 justify-center transition-colors disabled:opacity-50 disabled:cursor-not-allowed",
                className
            )}
            {...props}
        >
            {loading && <Loader2 className="h-4 w-4 animate-spin" />}
            {children}
        </button>
    )
}
```

## Form with useTransition

```typescript
"use client"

import { useState, useTransition } from "react"
import { LoadingButton } from "@/components/ui/loading-button"
import { submitForm } from "@/actions/form"

export function MyForm() {
    const [isPending, startTransition] = useTransition()
    const [errors, setErrors] = useState<Record<string, string>>({})

    const handleSubmit = async (formData: FormData) => {
        // Validate first
        if (!validateForm()) return

        // Clear errors
        setErrors({})

        // Submit with transition
        startTransition(async () => {
            await submitForm(formData)
        })
    }

    return (
        <form action={handleSubmit}>
            {/* Form fields */}
            
            <LoadingButton
                type="submit"
                loading={isPending}
                className="bg-emerald-500 hover:bg-emerald-400 text-black font-bold px-6 py-3 rounded-xl"
            >
                Submit
            </LoadingButton>
        </form>
    )
}
```

## Disable Form During Submission

```typescript
<input
    disabled={isPending}
    className={cn(
        "w-full bg-zinc-950 border border-zinc-800 rounded-xl px-4 py-3",
        isPending && "opacity-50 cursor-not-allowed"
    )}
/>
```

## Loading Overlay

For complex forms, show an overlay:

```typescript
{isPending && (
    <div className="absolute inset-0 bg-black/50 flex items-center justify-center rounded-xl">
        <div className="bg-zinc-900 border border-zinc-800 rounded-lg px-6 py-4 flex items-center gap-3">
            <Loader2 className="h-5 w-5 animate-spin text-emerald-500" />
            <span className="text-white font-medium">Submitting...</span>
        </div>
    </div>
)}
```

## Progress Indicator

Show progress for multi-step operations:

```typescript
const [progress, setProgress] = useState(0)

startTransition(async () => {
    setProgress(25)
    await step1()
    setProgress(50)
    await step2()
    setProgress(75)
    await step3()
    setProgress(100)
})

// Display
<div className="w-full bg-zinc-800 rounded-full h-2">
    <div 
        className="bg-emerald-500 h-2 rounded-full transition-all duration-300"
        style={{ width: `${progress}%` }}
    />
</div>
```
