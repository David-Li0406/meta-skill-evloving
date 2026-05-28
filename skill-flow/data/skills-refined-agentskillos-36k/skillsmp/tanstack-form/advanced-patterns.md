# Advanced Form Patterns

## Complex Forms with Sections

```tsx
<form className="space-y-8">
  <fieldset className="space-y-4">
    <legend className="text-lg font-semibold">Account</legend>
    <p className="text-muted-foreground">Configure your account.</p>
    <form.Field name="username" children={/*...*/} />
  </fieldset>

  <hr />

  <fieldset className="space-y-4">
    <legend className="text-lg font-semibold">Notifications</legend>
    <form.Field name="emailNotifications" children={/*...*/} />
  </fieldset>
</form>
```

## Accessibility Requirements

| Requirement   | Implementation                   |
| ------------- | -------------------------------- |
| Label         | React Aria handles automatically |
| Error         | `errorMessage` prop              |
| Invalid state | `isInvalid` prop                 |
| Help text     | `description` prop               |
| Grouping      | `<fieldset>` + `<legend>`        |

### Accessibility Pattern

```tsx
<TextField
  label="Email"
  description="We'll never share your email."
  value={field.state.value}
  onChange={(value) => field.handleChange(value)}
  isInvalid={isInvalid}
  errorMessage={isInvalid ? field.state.meta.errors.join(', ') : undefined}
/>
```

## Multi-Step Wizard Form

```tsx
type WizardStep = 'account' | 'profile' | 'preferences';

const wizardSchema = {
  account: z.object({
    email: z.email(),
    password: z.string().min(8),
  }),
  profile: z.object({
    name: z.string().min(1),
    avatar: z.string().optional(),
  }),
  preferences: z.object({
    notifications: z.boolean(),
    theme: z.enum(['light', 'dark', 'system']),
  }),
};

function WizardForm() {
  const [step, setStep] = useState<WizardStep>('account');

  const form = useForm({
    defaultValues: {
      email: '',
      password: '',
      name: '',
      avatar: '',
      notifications: true,
      theme: 'system',
    },
    onSubmit: async ({ value }) => {
      await createAccount({ data: value });
    },
  });

  const validateStep = async (): Promise<boolean> => {
    const schema = wizardSchema[step];
    const stepValues = getStepValues(form.state.values, step);
    const result = schema.safeParse(stepValues);

    if (!result.success) {
      // Set errors for current step fields
      for (const issue of result.error.issues) {
        form.setFieldMeta(issue.path.join('.'), (prev) => ({
          ...prev,
          errors: [...prev.errors, issue.message],
        }));
      }
      return false;
    }
    return true;
  };

  const nextStep = async () => {
    if (await validateStep()) {
      const steps: WizardStep[] = ['account', 'profile', 'preferences'];
      const nextIndex = steps.indexOf(step) + 1;
      if (nextIndex < steps.length) {
        setStep(steps[nextIndex]);
      } else {
        form.handleSubmit();
      }
    }
  };

  return (
    <form onSubmit={(e) => e.preventDefault()}>
      {/* Step indicator */}
      <WizardSteps current={step} />

      {/* Step content */}
      {step === 'account' && <AccountStep form={form} />}
      {step === 'profile' && <ProfileStep form={form} />}
      {step === 'preferences' && <PreferencesStep form={form} />}

      {/* Navigation */}
      <div className="flex justify-between">
        {step !== 'account' && (
          <Button variant="secondary" onPress={() => setStep(prev)}>
            Back
          </Button>
        )}
        <Button onPress={nextStep}>
          {step === 'preferences' ? 'Complete' : 'Next'}
        </Button>
      </div>
    </form>
  );
}
```

## File Upload

### Single File Upload

```tsx
const uploadFile = createServerFn({ method: 'POST' })
  .inputValidator(z.object({ file: z.instanceof(File) }))
  .handler(async ({ data }) => {
    const buffer = await data.file.arrayBuffer();
    const key = `uploads/${crypto.randomUUID()}-${data.file.name}`;

    // Upload to storage (S3, etc.)
    await storage.put(key, buffer, {
      contentType: data.file.type,
    });

    return { url: `${CDN_URL}/${key}` };
  });

function FileUploadField() {
  const field = useFieldContext<string>(); // Stores URL
  const [uploading, setUploading] = useState(false);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    try {
      const result = await uploadFile({ data: { file } });
      field.handleChange(result.url);
    } catch (error) {
      toast.error('Upload failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="space-y-2">
      <label htmlFor={field.name}>Image</label>
      {field.state.value && (
        <img
          src={field.state.value}
          alt="Preview"
          className="size-32 object-cover"
        />
      )}
      <input
        id={field.name}
        type="file"
        accept="image/*"
        onChange={handleUpload}
        disabled={uploading}
      />
      {uploading && (
        <p className="text-sm text-muted-foreground">Uploading...</p>
      )}
    </div>
  );
}
```

### Multiple Files with Progress

```tsx
function MultiFileUpload() {
  const field = useFieldContext<string[]>();
  const [uploads, setUploads] = useState<Map<string, number>>(new Map());

  const handleFiles = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files ?? []);

    for (const file of files) {
      const id = crypto.randomUUID();
      setUploads((prev) => new Map(prev).set(id, 0));

      try {
        const url = await uploadWithProgress(file, (progress) => {
          setUploads((prev) => new Map(prev).set(id, progress));
        });
        field.pushValue(url);
      } finally {
        setUploads((prev) => {
          const next = new Map(prev);
          next.delete(id);
          return next;
        });
      }
    }
  };

  return (
    <div className="space-y-2">
      <input type="file" multiple onChange={handleFiles} />
      {/* Progress indicators */}
      {Array.from(uploads).map(([id, progress]) => (
        <div key={id} className="h-2 bg-muted rounded">
          <div
            className="h-full bg-primary rounded"
            style={{ width: `${progress}%` }}
          />
        </div>
      ))}
      {/* Uploaded files */}
      <div className="flex gap-2 flex-wrap">
        {field.state.value.map((url, i) => (
          <div key={i} className="relative">
            <img src={url} className="size-20 object-cover rounded" alt="" />
            <Button
              size="sm"
              variant="destructive"
              className="absolute -top-2 -right-2"
              onPress={() => field.removeValue(i)}
            >
              ×
            </Button>
          </div>
        ))}
      </div>
    </div>
  );
}
```
