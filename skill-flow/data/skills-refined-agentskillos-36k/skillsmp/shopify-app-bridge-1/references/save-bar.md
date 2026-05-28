# Save Bar

Save Bar (Contextual Save Bar) hiển thị khi form có thay đổi chưa lưu, cung cấp actions Save và Discard cho user. Đây là pattern chuẩn trong Shopify Admin.

> [!NOTE]
> Save Bar là một phần của **Shopify App Bridge v4** và có thể dùng qua `<SaveBar>` React component, `<ui-save-bar>` HTML element, hoặc `data-save-bar` attribute.

## Khi Nào Sử Dụng Save Bar

| Use Case | Approach |
|----------|----------|
| Simple forms | `data-save-bar` attribute (automatic) |
| Complex state management | `<SaveBar>` React component |
| Non-React apps | `<ui-save-bar>` HTML element |
| Programmatic control | JavaScript API |

## Implementation Methods

### Method 1: Automatic Form Tracking (Recommended)

Cách đơn giản nhất - chỉ cần thêm `data-save-bar` attribute vào form:

```html
<form data-save-bar>
  <label>
    Name:
    <input name="username" />
  </label>
  <button type="submit">Save</button>
</form>
```

**Automatic behaviors:**
- Save bar xuất hiện khi form có changes
- `submit` event fires khi nhấn Save hoặc submit form
- `reset` event fires khi nhấn Discard

```javascript
const form = document.querySelector('form[data-save-bar]');

form.addEventListener('submit', (e) => {
  e.preventDefault();
  console.log('Saving...');
  // Save logic here
});

form.addEventListener('reset', (e) => {
  console.log('Discarding changes...');
});
```

**Thêm Discard Confirmation:**
```html
<form data-save-bar data-discard-confirmation>
  <!-- form fields -->
</form>
```

### Method 2: React SaveBar Component

```jsx
import { SaveBar } from '@shopify/app-bridge-react';
import { useAppBridge } from '@shopify/app-bridge-react';
import { useState } from 'react';

export default function SettingsPage() {
  const shopify = useAppBridge();
  const [isDirty, setIsDirty] = useState(false);
  const [saving, setSaving] = useState(false);
  const [formData, setFormData] = useState({ name: '' });

  const handleChange = (value) => {
    setFormData({ ...formData, name: value });
    setIsDirty(true);
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      // Save logic here
      await saveData(formData);
      setIsDirty(false);
      shopify.toast.show('Settings saved');
    } catch (error) {
      shopify.toast.show('Error saving settings', { isError: true });
    } finally {
      setSaving(false);
    }
  };

  const handleDiscard = () => {
    setFormData({ name: '' }); // Reset to original
    setIsDirty(false);
  };

  return (
    <>
      <TextField
        label="Name"
        value={formData.name}
        onChange={handleChange}
      />

      <SaveBar id="settings-save-bar" open={isDirty}>
        <button variant="primary" onClick={handleSave} loading={saving}>
          Save
        </button>
        <button onClick={handleDiscard}>Discard</button>
      </SaveBar>
    </>
  );
}
```

### Method 3: HTML ui-save-bar Element

```html
<ui-save-bar id="my-save-bar">
  <button variant="primary" id="save-btn">Save</button>
  <button id="discard-btn">Discard</button>
</ui-save-bar>

<script>
  const saveBar = document.getElementById('my-save-bar');
  const saveBtn = document.getElementById('save-btn');
  const discardBtn = document.getElementById('discard-btn');

  // Show save bar when form changes
  document.querySelector('input').addEventListener('input', () => {
    saveBar.show();
  });

  saveBtn.addEventListener('click', async () => {
    // Save logic
    await saveData();
    saveBar.hide();
  });

  discardBtn.addEventListener('click', () => {
    // Discard logic
    resetForm();
    saveBar.hide();
  });
</script>
```

## SaveBar Props & Attributes

### React Component Props

| Prop | Type | Description |
|------|------|-------------|
| `id` | string | Unique identifier (required) |
| `open` | boolean | Control visibility via React state |
| `discardConfirmation` | boolean | Show confirmation modal on discard |
| `children` | ReactNode | Button elements |

### Button Properties

| Property | Type | Description |
|----------|------|-------------|
| `variant` | `"primary"` | Designates Save button |
| `disabled` | boolean | Disable the button |
| `loading` | boolean | Show loading state |
| `onClick` | function | Click handler |

```jsx
<SaveBar id="my-save-bar" open={isDirty} discardConfirmation>
  <button
    variant="primary"
    onClick={handleSave}
    loading={saving}
    disabled={!isValid}
  >
    Save
  </button>
  <button onClick={handleDiscard}>
    Discard
  </button>
</SaveBar>
```

## JavaScript API

### Methods

```javascript
// Show save bar
shopify.saveBar.show('my-save-bar');

// Hide save bar
shopify.saveBar.hide('my-save-bar');

// Toggle visibility
shopify.saveBar.toggle('my-save-bar');

// Show leave confirmation if save bar is visible
shopify.saveBar.leaveConfirmation();
```

### Instance Methods (ui-save-bar element)

```javascript
const saveBar = document.getElementById('my-save-bar');

// Control visibility
await saveBar.show();
await saveBar.hide();
await saveBar.toggle();

// Check state
console.log(saveBar.showing); // boolean

// Event listeners
saveBar.addEventListener('show', () => {
  console.log('Save bar shown');
});

saveBar.addEventListener('hide', () => {
  console.log('Save bar hidden');
});
```

## Discard Confirmation

Hiển thị modal xác nhận trước khi discard:

### React

```jsx
<SaveBar id="my-save-bar" open={isDirty} discardConfirmation>
  <button variant="primary" onClick={handleSave}>Save</button>
  <button onClick={handleDiscard}>Discard</button>
</SaveBar>
```

### HTML

```html
<ui-save-bar id="my-save-bar" discardConfirmation>
  <button variant="primary">Save</button>
  <button>Discard</button>
</ui-save-bar>
```

### Form Attribute

```html
<form data-save-bar data-discard-confirmation>
  <!-- form fields -->
</form>
```

## Integration with Remix Forms

```jsx
import { SaveBar } from '@shopify/app-bridge-react';
import { useAppBridge } from '@shopify/app-bridge-react';
import { Form, useNavigation, useActionData } from '@remix-run/react';
import { useEffect, useState } from 'react';

export default function SettingsRoute() {
  const shopify = useAppBridge();
  const navigation = useNavigation();
  const actionData = useActionData();
  const [isDirty, setIsDirty] = useState(false);

  const isSubmitting = navigation.state === 'submitting';

  // Hide save bar on successful save
  useEffect(() => {
    if (actionData?.success) {
      setIsDirty(false);
      shopify.toast.show('Saved successfully');
    }
  }, [actionData]);

  return (
    <Form method="post" onChange={() => setIsDirty(true)}>
      <TextField name="title" label="Title" />

      <SaveBar id="settings-bar" open={isDirty} discardConfirmation>
        <button variant="primary" type="submit" loading={isSubmitting}>
          Save
        </button>
        <button type="reset" onClick={() => setIsDirty(false)}>
          Discard
        </button>
      </SaveBar>
    </Form>
  );
}
```

## Integration with Modal

Save Bar có thể dùng trong Modal với `<ui-save-bar>` element:

```jsx
import { Modal, TitleBar } from '@shopify/app-bridge-react';

function ModalWithSaveBar() {
  return (
    <Modal id="edit-modal" variant="large">
      <form data-save-bar data-discard-confirmation>
        <input name="title" />
      </form>
      <TitleBar title="Edit Item" />
    </Modal>
  );
}
```

## Handling Navigation

Ngăn user rời trang khi có unsaved changes:

```jsx
import { useEffect } from 'react';
import { useAppBridge } from '@shopify/app-bridge-react';

export default function PageWithUnsavedChanges() {
  const shopify = useAppBridge();
  const [isDirty, setIsDirty] = useState(false);

  useEffect(() => {
    if (isDirty) {
      // This will show confirmation when navigating away
      const handleBeforeUnload = (e) => {
        e.preventDefault();
        e.returnValue = '';
      };
      window.addEventListener('beforeunload', handleBeforeUnload);
      return () => window.removeEventListener('beforeunload', handleBeforeUnload);
    }
  }, [isDirty]);

  // Use shopify.saveBar.leaveConfirmation() for in-app navigation
  const handleNavigate = () => {
    if (isDirty) {
      shopify.saveBar.leaveConfirmation();
    } else {
      // Navigate
    }
  };

  return (
    // ...
  );
}
```

## Best Practices

> [!IMPORTANT]
> **Form Tracking**: Dùng `data-save-bar` cho simple forms, `<SaveBar>` component cho complex state management.

> [!TIP]
> **Loading States**: Luôn show loading state trên Save button khi đang submit.

> [!TIP]
> **Discard Confirmation**: Enable `discardConfirmation` để ngăn mất data vô tình.

### Do's

- Show loading state khi saving
- Disable Save button nếu form invalid
- Reset dirty state sau khi save thành công
- Show toast notification sau khi save
- Dùng `discardConfirmation` cho forms quan trọng

### Don'ts

- **KHÔNG** show Save Bar khi không có changes
- **KHÔNG** hide Save Bar mà không save hoặc confirm discard
- **KHÔNG** dùng custom save buttons thay vì Save Bar trong Shopify Admin
- **KHÔNG** quên handle error states

## Error Handling

```jsx
const handleSave = async () => {
  setSaving(true);
  try {
    await saveData(formData);
    setIsDirty(false);
    shopify.toast.show('Settings saved');
  } catch (error) {
    // Keep save bar open on error
    shopify.toast.show('Failed to save. Please try again.', {
      isError: true
    });
  } finally {
    setSaving(false);
  }
};
```

## Complete Example

```jsx
import { Page, Layout, Card, FormLayout, TextField, BlockStack } from '@shopify/polaris';
import { SaveBar } from '@shopify/app-bridge-react';
import { useAppBridge } from '@shopify/app-bridge-react';
import { useState, useCallback } from 'react';

export default function SettingsPage() {
  const shopify = useAppBridge();

  // Original data (from server)
  const [originalData] = useState({ name: 'My Store', email: 'store@example.com' });

  // Form state
  const [formData, setFormData] = useState(originalData);
  const [saving, setSaving] = useState(false);

  // Check if form has changes
  const isDirty = JSON.stringify(formData) !== JSON.stringify(originalData);

  const handleChange = useCallback((field) => (value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  }, []);

  const handleSave = async () => {
    setSaving(true);
    try {
      const response = await fetch('/api/settings', {
        method: 'POST',
        body: JSON.stringify(formData),
      });

      if (!response.ok) throw new Error('Save failed');

      shopify.toast.show('Settings saved');
    } catch (error) {
      shopify.toast.show('Error saving settings', { isError: true });
    } finally {
      setSaving(false);
    }
  };

  const handleDiscard = () => {
    setFormData(originalData);
  };

  return (
    <Page title="Settings">
      <Layout>
        <Layout.Section>
          <Card>
            <BlockStack gap="400">
              <FormLayout>
                <TextField
                  label="Store Name"
                  value={formData.name}
                  onChange={handleChange('name')}
                />
                <TextField
                  label="Email"
                  type="email"
                  value={formData.email}
                  onChange={handleChange('email')}
                />
              </FormLayout>
            </BlockStack>
          </Card>
        </Layout.Section>
      </Layout>

      <SaveBar id="settings-save-bar" open={isDirty} discardConfirmation>
        <button variant="primary" onClick={handleSave} loading={saving}>
          Save
        </button>
        <button onClick={handleDiscard}>Discard</button>
      </SaveBar>
    </Page>
  );
}
```
