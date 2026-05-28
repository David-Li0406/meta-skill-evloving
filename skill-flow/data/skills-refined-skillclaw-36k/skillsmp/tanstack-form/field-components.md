# Field Components Reference

## React Aria Component Integration

| Component     | React Aria    | Purpose         |
| ------------- | ------------- | --------------- |
| `TextField`   | `TextField`   | Text input      |
| `NumberField` | `NumberField` | Numeric input   |
| `Select`      | `Select`      | Dropdown select |
| `ComboBox`    | `ComboBox`    | Autocomplete    |
| `Checkbox`    | `Checkbox`    | Boolean toggle  |
| `Switch`      | `Switch`      | Toggle switch   |
| `RadioGroup`  | `RadioGroup`  | Single select   |
| `DatePicker`  | `DatePicker`  | Date selection  |

## Input Types

### Text Input

```tsx
<form.Field
  name="username"
  children={(field) => {
    const isInvalid = field.state.meta.isTouched && !field.state.meta.isValid;
    return (
      <TextField
        label="Username"
        value={field.state.value}
        onBlur={field.handleBlur}
        onChange={(value) => field.handleChange(value)}
        isInvalid={isInvalid}
        errorMessage={
          isInvalid ? field.state.meta.errors.join(', ') : undefined
        }
      />
    );
  }}
/>
```

### Select

```tsx
<form.Field
  name="language"
  children={(field) => (
    <Select
      label="Language"
      selectedKey={field.state.value}
      onSelectionChange={(key) => field.handleChange(key as string)}
    >
      <SelectItem id="en">English</SelectItem>
      <SelectItem id="es">Spanish</SelectItem>
      <SelectItem id="fr">French</SelectItem>
    </Select>
  )}
/>
```

### Switch

```tsx
<form.Field
  name="notifications"
  children={(field) => (
    <Switch isSelected={field.state.value} onChange={field.handleChange}>
      Enable notifications
    </Switch>
  )}
/>
```

### Checkbox

```tsx
<form.Field
  name="terms"
  children={(field) => (
    <Checkbox isSelected={field.state.value} onChange={field.handleChange}>
      Accept terms and conditions
    </Checkbox>
  )}
/>
```

### Radio Group

```tsx
const plans = [
  { id: 'basic', title: 'Basic', description: 'For individuals' },
  { id: 'pro', title: 'Pro', description: 'For teams' },
];

<form.Field
  name="plan"
  children={(field) => (
    <RadioGroup
      label="Plan"
      value={field.state.value}
      onChange={field.handleChange}
    >
      {plans.map((plan) => (
        <Radio key={plan.id} value={plan.id}>
          {plan.title}
        </Radio>
      ))}
    </RadioGroup>
  )}
/>;
```

## Array Fields

Use `mode="array"` for dynamic lists:

```tsx
<form.Field name="emails" mode="array">
  {(field) => (
    <div className="space-y-2">
      <Label>Emails</Label>
      {field.state.value.map((_, index) => (
        <form.Field
          key={index}
          name={`emails[${index}].address`}
          children={(subField) => (
            <div className="flex gap-2">
              <TextField
                value={subField.state.value}
                onChange={(value) => subField.handleChange(value)}
                className="flex-1"
              />
              <Button
                variant="secondary"
                onPress={() => field.removeValue(index)}
              >
                Remove
              </Button>
            </div>
          )}
        />
      ))}
      <Button
        variant="outline"
        onPress={() => field.pushValue({ address: '' })}
      >
        Add Email
      </Button>
    </div>
  )}
</form.Field>
```

### Array Methods

| Method                 | Description      |
| ---------------------- | ---------------- |
| `pushValue(value)`     | Add to end       |
| `removeValue(index)`   | Remove at index  |
| `insertValue(i, val)`  | Insert at index  |
| `replaceValue(i, val)` | Replace at index |
| `swapValues(i1, i2)`   | Swap two items   |
| `moveValue(from, to)`  | Move item        |
| `clearValues()`        | Remove all       |

## Field Listeners

Use `listeners` to trigger side effects when field values change:

```tsx
<form.Field
  name="country"
  listeners={{
    onChange: ({ value }) => {
      // Reset dependent field when country changes
      form.setFieldValue('province', '');
    },
  }}
  children={(field) => (
    <Select
      label="Country"
      selectedKey={field.state.value}
      onSelectionChange={(key) => field.handleChange(key as string)}
    >
      {countries.map((c) => (
        <SelectItem key={c.code} id={c.code}>{c.name}</SelectItem>
      ))}
    </Select>
  )}
/>

<form.Field
  name="province"
  children={(field) => (
    <Select
      label="Province"
      selectedKey={field.state.value}
      onSelectionChange={(key) => field.handleChange(key as string)}
    >
      {getProvinces(form.getFieldValue('country')).map((p) => (
        <SelectItem key={p.code} id={p.code}>{p.name}</SelectItem>
      ))}
    </Select>
  )}
/>
```

**Note:** For validation that depends on other fields, use `onChangeListenTo` in validators instead. See [Validation > Linked Fields](validation.md#linked-fields).

## Checkbox Group

```tsx
<form.Field
  name="features"
  mode="array"
  children={(field) => (
    <CheckboxGroup
      label="Features"
      value={field.state.value}
      onChange={field.handleChange}
    >
      {features.map((feature) => (
        <Checkbox key={feature.id} value={feature.id}>
          {feature.label}
        </Checkbox>
      ))}
    </CheckboxGroup>
  )}
/>
```

## Composable Field Components

### FormTextField

```tsx
export function FormTextField({
  label,
  placeholder,
  type = 'text',
}: {
  label: string;
  placeholder?: string;
  type?: 'text' | 'email' | 'password';
}) {
  const field = useFieldContext<string>();
  const errors = useStore(field.store, (s) => s.meta.errors);
  const isInvalid = field.state.meta.isTouched && errors.length > 0;

  return (
    <TextField
      label={label}
      type={type}
      value={field.state.value}
      placeholder={placeholder}
      onBlur={field.handleBlur}
      onChange={(value) => field.handleChange(value)}
      isInvalid={isInvalid}
      errorMessage={isInvalid ? errors.join(', ') : undefined}
    />
  );
}
```

### FormSelectField

```tsx
export function FormSelectField({
  label,
  options,
  placeholder,
}: {
  label: string;
  options: { label: string; value: string }[];
  placeholder?: string;
}) {
  const field = useFieldContext<string>();

  return (
    <Select
      label={label}
      placeholder={placeholder}
      selectedKey={field.state.value}
      onSelectionChange={(key) => field.handleChange(key as string)}
    >
      {options.map((opt) => (
        <SelectItem key={opt.value} id={opt.value}>
          {opt.label}
        </SelectItem>
      ))}
    </Select>
  );
}
```

### FormSwitchField

```tsx
export function FormSwitchField({ label }: { label: string }) {
  const field = useFieldContext<boolean>();

  return (
    <Switch isSelected={field.state.value} onChange={field.handleChange}>
      {label}
    </Switch>
  );
}
```

### SubmitButton

```tsx
export function SubmitButton({ label }: { label: string }) {
  const form = useFormContext();

  return (
    <form.Subscribe selector={(s) => s.isSubmitting}>
      {(isSubmitting) => (
        <Button type="submit" isDisabled={isSubmitting}>
          {label}
        </Button>
      )}
    </form.Subscribe>
  );
}
```
