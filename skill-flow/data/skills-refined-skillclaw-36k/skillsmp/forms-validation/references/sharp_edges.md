# Forms Validation - Sharp Edges

## Client Only Validation

### **Id**
client-only-validation
### **Summary**
Trusting client-side validation for security
### **Severity**
critical
### **Situation**
  Form validates email format in JavaScript. User disables JS or
  uses curl to submit. Invalid data reaches your database.
  
### **Why**
  Client-side validation is for UX only. It can always be bypassed.
  Server must be the source of truth.
  
### **Solution**
  # VALIDATE ON BOTH SIDES
  
  // Shared schema
  export const userSchema = z.object({
    email: z.string().email(),
    age: z.number().min(18),
  });
  
  // Client: for immediate feedback
  const { register } = useForm({
    resolver: zodResolver(userSchema),
  });
  
  // Server: always validate again
  export async function createUser(formData: FormData) {
    const parsed = userSchema.safeParse({
      email: formData.get("email"),
      age: Number(formData.get("age")),
    });
    if (!parsed.success) {
      return { errors: parsed.error.flatten().fieldErrors };
    }
    await db.insert(users).values(parsed.data);
  }
  
### **Symptoms**
  - Invalid data in database
  - curl bypasses all checks
### **Detection Pattern**


## Losing Form Data

### **Id**
losing-form-data
### **Summary**
Form clears on validation error
### **Severity**
high
### **Situation**
  User fills out long form. Clicks submit. Server returns error.
  Form resets to empty. User has to re-enter everything.
  
### **Why**
  Not preserving form state across submissions. Not passing back
  the submitted data on error.
  
### **Solution**
  # PRESERVE FORM DATA
  
  export async function submitForm(prevState, formData) {
    const data = Object.fromEntries(formData);
    const parsed = schema.safeParse(data);
  
    if (!parsed.success) {
      return {
        errors: parsed.error.flatten().fieldErrors,
        data, // Return submitted data!
      };
    }
    return { success: true };
  }
  
  // Form uses returned data as defaults
  <input name="email" defaultValue={state.data?.email ?? ""} />
  
### **Symptoms**
  - Form empties after error
  - High form abandonment
### **Detection Pattern**


## No Loading State

### **Id**
no-loading-state
### **Summary**
No feedback during form submission
### **Severity**
medium
### **Situation**
  User clicks Submit. Nothing happens visually. They click again.
  Now you have duplicate submissions.
  
### **Why**
  Not disabling the submit button or showing a loading state.
  
### **Solution**
  # ALWAYS SHOW LOADING STATE
  
  const [state, action, isPending] = useActionState(submitForm, {});
  
  <button type="submit" disabled={isPending}>
    {isPending ? "Submitting..." : "Submit"}
  </button>
  
### **Symptoms**
  - Duplicate submissions
  - No visual feedback on submit
### **Detection Pattern**


## Zod Coercion Missing

### **Id**
zod-coercion-missing
### **Summary**
Form data types wrong without coercion
### **Severity**
medium
### **Situation**
  Number input submitted. Zod schema expects number. Validation
  fails because formData.get() returns string, not number.
  
### **Why**
  Form data is always strings. Need to coerce to correct types.
  
### **Solution**
  # USE ZOD COERCION
  
  // WRONG
  const schema = z.object({
    age: z.number().min(18),
  });
  
  // RIGHT
  const schema = z.object({
    age: z.coerce.number().min(18),
  });
  
### **Symptoms**
  - Number validation failing on valid input
  - Expected number received string errors
### **Detection Pattern**
