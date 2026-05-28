# Forms & Validation

## Patterns

### **React Hook Form Zod**
  #### **Description**
React Hook Form with Zod validation
  #### **Example**
    import { useForm } from "react-hook-form";
    import { zodResolver } from "@hookform/resolvers/zod";
    import { z } from "zod";
    
    const schema = z.object({
      email: z.string().email("Invalid email address"),
      password: z
        .string()
        .min(8, "Password must be at least 8 characters")
        .regex(/[A-Z]/, "Must contain uppercase letter"),
    });
    
    type FormData = z.infer<typeof schema>;
    
    export function SignupForm() {
      const {
        register,
        handleSubmit,
        formState: { errors, isSubmitting },
      } = useForm<FormData>({
        resolver: zodResolver(schema),
        mode: "onBlur",
      });
    
      const onSubmit = async (data: FormData) => {
        await createUser(data);
      };
    
      return (
        <form onSubmit={handleSubmit(onSubmit)} noValidate>
          <div>
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              aria-invalid={errors.email ? "true" : "false"}
              aria-describedby={errors.email ? "email-error" : undefined}
              {...register("email")}
            />
            {errors.email && (
              <span id="email-error" role="alert">
                {errors.email.message}
              </span>
            )}
          </div>
    
          <button type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Creating..." : "Sign up"}
          </button>
        </form>
      );
    }
    
### **Server Actions**
  #### **Description**
Next.js Server Actions with forms
  #### **Example**
    // actions/contact.ts
    "use server";
    
    import { contactSchema } from "@/lib/schemas";
    
    export type ContactState = {
      errors?: Record<string, string[]>;
      success?: boolean;
    };
    
    export async function submitContact(
      prevState: ContactState,
      formData: FormData
    ): Promise<ContactState> {
      const parsed = contactSchema.safeParse({
        name: formData.get("name"),
        email: formData.get("email"),
        message: formData.get("message"),
      });
    
      if (!parsed.success) {
        return { errors: parsed.error.flatten().fieldErrors };
      }
    
      await sendEmail(parsed.data);
      return { success: true };
    }
    
    
    // components/ContactForm.tsx
    "use client";
    
    import { useActionState } from "react";
    import { submitContact } from "@/actions/contact";
    
    export function ContactForm() {
      const [state, formAction, isPending] = useActionState(
        submitContact,
        {}
      );
    
      return (
        <form action={formAction}>
          <input name="name" required />
          {state.errors?.name && <span>{state.errors.name[0]}</span>}
    
          <input name="email" type="email" required />
          {state.errors?.email && <span>{state.errors.email[0]}</span>}
    
          <textarea name="message" required />
          {state.errors?.message && <span>{state.errors.message[0]}</span>}
    
          <button type="submit" disabled={isPending}>
            {isPending ? "Sending..." : "Send"}
          </button>
        </form>
      );
    }
    
### **Field Arrays**
  #### **Description**
Dynamic field arrays
  #### **Example**
    import { useForm, useFieldArray } from "react-hook-form";
    
    export function OrderForm() {
      const { control, register, handleSubmit } = useForm({
        defaultValues: {
          items: [{ name: "", quantity: 1 }],
        },
      });
    
      const { fields, append, remove } = useFieldArray({
        control,
        name: "items",
      });
    
      return (
        <form onSubmit={handleSubmit(onSubmit)}>
          {fields.map((field, index) => (
            <div key={field.id}>
              <input {...register("items.${index}.name")} />
              <input
                type="number"
                {...register("items.${index}.quantity", { valueAsNumber: true })}
              />
              <button type="button" onClick={() => remove(index)}>
                Remove
              </button>
            </div>
          ))}
    
          <button type="button" onClick={() => append({ name: "", quantity: 1 })}>
            Add Item
          </button>
          <button type="submit">Submit</button>
        </form>
      );
    }
    

## Anti-Patterns

### **Validation Client Only**
  #### **Description**
Only validating on client side
  #### **Wrong**
Trust client validation, skip server check
  #### **Right**
Always validate server-side
### **Clearing Form On Error**
  #### **Description**
Resetting form when submission fails
  #### **Wrong**
form.reset() in error handler
  #### **Right**
Preserve input, show inline errors
### **Alert For Errors**
  #### **Description**
Using alert() for form errors
  #### **Wrong**
alert('Please fill all fields')
  #### **Right**
Inline errors next to each field