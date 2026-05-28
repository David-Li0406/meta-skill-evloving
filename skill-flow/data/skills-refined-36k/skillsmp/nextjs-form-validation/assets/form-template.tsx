"use client"

import { useState, useTransition } from "react"
import { AlertCircle } from "lucide-react"
import { LoadingButton } from "@/components/ui/loading-button"
import { submitFormAction } from "@/actions/form"
import { cn } from "@/lib/utils"

// Validation constants
const MIN_NAME_LENGTH = 2
const MAX_NAME_LENGTH = 50

interface FormData {
    // Define your form fields here
    name: string
    email: string
}

interface ValidationErrors {
    name?: string
    email?: string
}

export function ValidatedForm() {
    const [formData, setFormData] = useState<FormData>({
        name: "",
        email: "",
    })
    const [errors, setErrors] = useState<ValidationErrors>({})
    const [isPending, startTransition] = useTransition()

    // Validation functions
    const validateName = (value: string): string | undefined => {
        if (!value || value.trim() === "") {
            return "Name is required"
        }
        if (value.length < MIN_NAME_LENGTH) {
            return `Name must be at least ${MIN_NAME_LENGTH} characters`
        }
        if (value.length > MAX_NAME_LENGTH) {
            return `Name cannot exceed ${MAX_NAME_LENGTH} characters`
        }
        return undefined
    }

    const validateEmail = (value: string): string | undefined => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
        if (!emailRegex.test(value)) {
            return "Invalid email address"
        }
        return undefined
    }

    // Validate entire form
    const validateForm = (): boolean => {
        const newErrors: ValidationErrors = {}

        const nameError = validateName(formData.name)
        if (nameError) newErrors.name = nameError

        const emailError = validateEmail(formData.email)
        if (emailError) newErrors.email = emailError

        setErrors(newErrors)
        return Object.keys(newErrors).length === 0
    }

    // Handle form submission
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()

        // Validate before submission
        if (!validateForm()) return

        // Clear errors
        setErrors({})

        // Submit with transition
        startTransition(async () => {
            const formDataObj = new FormData()
            formDataObj.append("name", formData.name)
            formDataObj.append("email", formData.email)

            await submitFormAction(formDataObj)
        })
    }

    return (
        <form onSubmit={handleSubmit} className="space-y-6">
            {/* Name Field */}
            <div className="space-y-2">
                <label className="text-sm font-medium text-zinc-300">
                    Name
                </label>
                <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => {
                        setFormData(prev => ({ ...prev, name: e.target.value }))
                        // Clear error on change
                        setErrors(prev => ({ ...prev, name: undefined }))
                    }}
                    onBlur={(e) => {
                        // Validate on blur
                        const error = validateName(e.target.value)
                        setErrors(prev => ({ ...prev, name: error }))
                    }}
                    disabled={isPending}
                    className={cn(
                        "w-full bg-zinc-950 border rounded-xl px-4 py-3 text-white outline-none focus:border-emerald-500 transition-colors disabled:opacity-50",
                        errors.name ? "border-red-500" : "border-zinc-800"
                    )}
                />
                {errors.name && (
                    <div className="flex items-center gap-2 text-red-400 text-sm">
                        <AlertCircle className="h-4 w-4 flex-shrink-0" />
                        {errors.name}
                    </div>
                )}
            </div>

            {/* Email Field */}
            <div className="space-y-2">
                <label className="text-sm font-medium text-zinc-300">
                    Email
                </label>
                <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => {
                        setFormData(prev => ({ ...prev, email: e.target.value }))
                        setErrors(prev => ({ ...prev, email: undefined }))
                    }}
                    onBlur={(e) => {
                        const error = validateEmail(e.target.value)
                        setErrors(prev => ({ ...prev, email: error }))
                    }}
                    disabled={isPending}
                    className={cn(
                        "w-full bg-zinc-950 border rounded-xl px-4 py-3 text-white outline-none focus:border-emerald-500 transition-colors disabled:opacity-50",
                        errors.email ? "border-red-500" : "border-zinc-800"
                    )}
                />
                {errors.email && (
                    <div className="flex items-center gap-2 text-red-400 text-sm">
                        <AlertCircle className="h-4 w-4 flex-shrink-0" />
                        {errors.email}
                    </div>
                )}
            </div>

            {/* Submit Button */}
            <LoadingButton
                type="submit"
                loading={isPending}
                className="w-full bg-emerald-500 hover:bg-emerald-400 text-black font-bold px-6 py-3 rounded-xl transition-colors"
            >
                Submit
            </LoadingButton>
        </form>
    )
}
