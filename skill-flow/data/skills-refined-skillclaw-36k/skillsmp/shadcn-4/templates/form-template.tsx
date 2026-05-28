/**
 * Form Template with react-hook-form and Zod Validation
 *
 * Complete form template demonstrating:
 * - Schema validation with Zod
 * - Form state management with react-hook-form
 * - shadcn/ui form components
 * - Error handling and loading states
 * - Accessibility best practices
 *
 * Dependencies:
 * - npm install react-hook-form @hookform/resolvers zod
 * - npx shadcn@latest add form input button label
 */

"use client";

import * as React from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Loader2 } from "lucide-react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Checkbox } from "@/components/ui/checkbox";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { AlertCircle } from "lucide-react";

// ==========================================
// SCHEMA DEFINITION
// ==========================================

/**
 * Define your form schema using Zod
 * This provides runtime validation and TypeScript types
 */
const formSchema = z.object({
  // Text field with length validation
  name: z
    .string()
    .min(2, "Name must be at least 2 characters")
    .max(50, "Name must be less than 50 characters"),

  // Email with format validation
  email: z.string().email("Please enter a valid email address"),

  // Password with multiple requirements
  password: z
    .string()
    .min(8, "Password must be at least 8 characters")
    .regex(/[A-Z]/, "Password must contain at least one uppercase letter")
    .regex(/[a-z]/, "Password must contain at least one lowercase letter")
    .regex(/[0-9]/, "Password must contain at least one number"),

  // Optional field
  bio: z.string().max(500, "Bio must be less than 500 characters").optional(),

  // Enum/Select field
  role: z.enum(["user", "admin", "moderator"], {
    required_error: "Please select a role",
  }),

  // Boolean field
  acceptTerms: z.literal(true, {
    errorMap: () => ({ message: "You must accept the terms and conditions" }),
  }),

  // Number field
  age: z.coerce
    .number()
    .min(18, "You must be at least 18 years old")
    .max(120, "Please enter a valid age"),
});

// Infer TypeScript type from schema
type FormData = z.infer<typeof formSchema>;

// ==========================================
// FORM COMPONENT
// ==========================================

export function FormTemplate() {
  const [isLoading, setIsLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  // Initialize form with react-hook-form
  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: "",
      email: "",
      password: "",
      bio: "",
      role: undefined,
      acceptTerms: false as unknown as true, // TypeScript workaround for literal type
      age: undefined as unknown as number,
    },
  });

  // Form submission handler
  async function onSubmit(data: FormData) {
    setIsLoading(true);
    setError(null);

    try {
      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 2000));

      // Handle success
      console.log("Form submitted:", data);
      toast.success("Form submitted successfully!");

      // Optionally reset form
      form.reset();
    } catch (err) {
      // Handle error
      const message =
        err instanceof Error ? err.message : "Something went wrong";
      setError(message);
      toast.error(message);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        {/* Global error message */}
        {error && (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* Name field */}
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Name</FormLabel>
              <FormControl>
                <Input placeholder="John Doe" {...field} />
              </FormControl>
              <FormDescription>Your full name as it appears.</FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Email field */}
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input
                  type="email"
                  placeholder="john@example.com"
                  autoComplete="email"
                  {...field}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Password field */}
        <FormField
          control={form.control}
          name="password"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Password</FormLabel>
              <FormControl>
                <Input
                  type="password"
                  placeholder="********"
                  autoComplete="new-password"
                  {...field}
                />
              </FormControl>
              <FormDescription>
                Must be at least 8 characters with uppercase, lowercase, and
                number.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Age field (number) */}
        <FormField
          control={form.control}
          name="age"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Age</FormLabel>
              <FormControl>
                <Input
                  type="number"
                  placeholder="25"
                  min={18}
                  max={120}
                  {...field}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Role select field */}
        <FormField
          control={form.control}
          name="role"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Role</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Select a role" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  <SelectItem value="user">User</SelectItem>
                  <SelectItem value="admin">Admin</SelectItem>
                  <SelectItem value="moderator">Moderator</SelectItem>
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Bio textarea (optional) */}
        <FormField
          control={form.control}
          name="bio"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Bio (optional)</FormLabel>
              <FormControl>
                <Textarea
                  placeholder="Tell us about yourself..."
                  className="resize-none"
                  rows={4}
                  {...field}
                />
              </FormControl>
              <FormDescription>
                {field.value?.length || 0}/500 characters
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Terms checkbox */}
        <FormField
          control={form.control}
          name="acceptTerms"
          render={({ field }) => (
            <FormItem className="flex flex-row items-start space-x-3 space-y-0">
              <FormControl>
                <Checkbox
                  checked={field.value}
                  onCheckedChange={field.onChange}
                />
              </FormControl>
              <div className="space-y-1 leading-none">
                <FormLabel>
                  I accept the{" "}
                  <a
                    href="/terms"
                    className="text-primary underline hover:text-primary/80"
                  >
                    terms and conditions
                  </a>
                </FormLabel>
                <FormMessage />
              </div>
            </FormItem>
          )}
        />

        {/* Submit button with loading state */}
        <Button type="submit" disabled={isLoading} className="w-full">
          {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
          {isLoading ? "Submitting..." : "Submit"}
        </Button>
      </form>
    </Form>
  );
}

// ==========================================
// ALTERNATIVE: SIMPLER LOGIN FORM
// ==========================================

const loginSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string().min(1, "Password is required"),
  rememberMe: z.boolean().default(false),
});

type LoginFormData = z.infer<typeof loginSchema>;

export function LoginForm() {
  const [isLoading, setIsLoading] = React.useState(false);

  const form = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: "",
      password: "",
      rememberMe: false,
    },
  });

  async function onSubmit(data: LoginFormData) {
    setIsLoading(true);
    try {
      // API call here
      console.log(data);
      toast.success("Logged in successfully!");
    } catch {
      toast.error("Invalid credentials");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input
                  type="email"
                  placeholder="name@example.com"
                  autoComplete="email"
                  {...field}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="password"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Password</FormLabel>
              <FormControl>
                <Input
                  type="password"
                  placeholder="********"
                  autoComplete="current-password"
                  {...field}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="rememberMe"
          render={({ field }) => (
            <FormItem className="flex flex-row items-center space-x-2 space-y-0">
              <FormControl>
                <Checkbox
                  checked={field.value}
                  onCheckedChange={field.onChange}
                />
              </FormControl>
              <FormLabel className="font-normal">Remember me</FormLabel>
            </FormItem>
          )}
        />
        <Button type="submit" disabled={isLoading} className="w-full">
          {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
          Sign In
        </Button>
      </form>
    </Form>
  );
}

// ==========================================
// ALTERNATIVE: SERVER ACTION FORM (Next.js)
// ==========================================

/*
"use server";

import { z } from "zod";

const serverSchema = z.object({
  email: z.string().email(),
  message: z.string().min(10),
});

export async function submitContactForm(formData: FormData) {
  const validated = serverSchema.safeParse({
    email: formData.get("email"),
    message: formData.get("message"),
  });

  if (!validated.success) {
    return { error: validated.error.flatten().fieldErrors };
  }

  // Process the form
  // await db.insert(...)

  return { success: true };
}

// Client component using server action
"use client";

import { useActionState } from "react";
import { submitContactForm } from "./actions";

export function ContactForm() {
  const [state, action, pending] = useActionState(submitContactForm, null);

  return (
    <form action={action} className="space-y-4">
      <div>
        <Input name="email" type="email" placeholder="Email" />
        {state?.error?.email && (
          <p className="text-sm text-destructive">{state.error.email}</p>
        )}
      </div>
      <div>
        <Textarea name="message" placeholder="Message" />
        {state?.error?.message && (
          <p className="text-sm text-destructive">{state.error.message}</p>
        )}
      </div>
      <Button type="submit" disabled={pending}>
        {pending ? "Sending..." : "Send Message"}
      </Button>
    </form>
  );
}
*/
