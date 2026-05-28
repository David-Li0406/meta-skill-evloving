# Modal Max

Modal Max (`variant="max"`) cung cấp trải nghiệm modal toàn màn hình trong Shopify embedded apps. Đây là sự thay thế cho Fullscreen API cũ, phù hợp cho các workflow phức tạp, editor chi tiết và quy trình nhiều bước.

> [!NOTE]
> Modal Max là một phần của **Shopify App Bridge v4** và sử dụng component `<Modal>` từ `@shopify/app-bridge-react` hoặc element `<ui-modal>` trong HTML.

## Khi Nào Sử Dụng Modal Max

| Use Case | Example |
|----------|---------|
| Multi-step wizards | Product creation flow, campaign setup |
| Complex editors | Rich text editor, email template editor |
| Draggable interfaces | List reordering, canvas editors |
| Third-party integrations | Libraries cần document access |
| Full-screen previews | Email preview, theme preview |

## Lựa Chọn Content Type

### HTML Children vs src Attribute

| Approach | Khi Nào Dùng |
|----------|--------------|
| **Children** (inline content) | Confirmations đơn giản, forms ít fields, Polaris components cơ bản |
| **src** (route-based) | Complex editors, draggable lists, third-party libraries, document-dependent functionality |

> [!IMPORTANT]
> "Complex use cases should use the `src` attribute to render a route while simple content can use HTML children."

## Core Implementation

### Dependencies

```bash
npm install @shopify/app-bridge-react@v4
```

Đảm bảo có script tag trong HTML:
```html
<script src="https://cdn.shopify.com/shopifycloud/app-bridge.js"></script>
```

### React Component - Inline Content

```jsx
import { Modal, TitleBar } from '@shopify/app-bridge-react';
import { Text, Button, BlockStack } from '@shopify/polaris';
import { useState } from 'react';

export default function MyPage() {
  const [modalOpen, setModalOpen] = useState(false);

  return (
    <>
      <Button onClick={() => setModalOpen(true)}>Open Editor</Button>

      <Modal id="editor-modal" variant="max" open={modalOpen}>
        <BlockStack gap="400">
          <Text as="p">Your modal content here.</Text>
        </BlockStack>

        <TitleBar title="Full Screen Editor">
          <button variant="primary" onClick={() => console.log('Save')}>
            Save
          </button>
          <button onClick={() => setModalOpen(false)}>Cancel</button>
        </TitleBar>
      </Modal>
    </>
  );
}
```

### React Component - Route-Based (src)

**Main Page:**
```jsx
// app/routes/app._index.jsx
import { Modal, TitleBar } from '@shopify/app-bridge-react';
import { Button } from '@shopify/polaris';
import { useState } from 'react';

export default function Index() {
  const [modalOpen, setModalOpen] = useState(false);

  return (
    <>
      <Button onClick={() => setModalOpen(true)}>Open Product Editor</Button>

      <Modal id="product-editor" variant="max" src="/app/modal/product-editor" open={modalOpen}>
        <TitleBar title="Edit Product">
          <button variant="primary">Save</button>
          <button onClick={() => setModalOpen(false)}>Cancel</button>
        </TitleBar>
      </Modal>
    </>
  );
}
```

**Modal Route:**
```jsx
// app/routes/app.modal.product-editor.jsx
import { Page, Layout, Card, FormLayout, TextField, BlockStack } from '@shopify/polaris';
import { useState } from 'react';

export default function ProductEditorModal() {
  const [title, setTitle] = useState('');

  return (
    <Page title="Product Details">
      <Layout>
        <Layout.Section>
          <Card>
            <BlockStack gap="400">
              <FormLayout>
                <TextField
                  label="Product Title"
                  value={title}
                  onChange={setTitle}
                  autoComplete="off"
                />
              </FormLayout>
            </BlockStack>
          </Card>
        </Layout.Section>
      </Layout>
    </Page>
  );
}
```

> [!WARNING]
> Modal routes cần có `app-bridge.js` script tag và các CSS/JS assets riêng. Chúng chạy trong iframe tách biệt.

### HTML Approach

```html
<!-- Main page -->
<ui-modal id="my-modal" src="/modal-route" variant="max">
  <ui-title-bar title="Full Screen Editor">
    <button variant="primary">Save</button>
    <button onclick="document.getElementById('my-modal').hide()">Cancel</button>
  </ui-title-bar>
</ui-modal>

<button onclick="document.getElementById('my-modal').show()">Open Modal</button>
```

## Opening & Closing Modals

### React State Approach (Recommended)

```jsx
const [open, setOpen] = useState(false);

<Modal id="my-modal" variant="max" open={open} onHide={() => setOpen(false)}>
  {/* content */}
</Modal>

<Button onClick={() => setOpen(true)}>Open</Button>
```

### Imperative Approach

```jsx
import { useAppBridge } from '@shopify/app-bridge-react';

export default function MyPage() {
  const shopify = useAppBridge();

  const openModal = () => {
    shopify.modal.show('my-modal');
  };

  const closeModal = () => {
    shopify.modal.hide('my-modal');
  };

  return (
    <>
      <Button onClick={openModal}>Open</Button>
      <Modal id="my-modal" variant="max">
        <TitleBar title="Editor">
          <button onClick={closeModal}>Close</button>
        </TitleBar>
      </Modal>
    </>
  );
}
```

### HTML Imperative

```javascript
// Open
document.getElementById('my-modal').show();

// Close
document.getElementById('my-modal').hide();
```

## Inter-Frame Communication (src Modals)

Khi sử dụng `src` attribute, modal chạy trong iframe riêng. Dùng `postMessage` API để giao tiếp.

### Main App → Modal

```jsx
// Main app
const sendToModal = (data) => {
  const modal = document.getElementById('my-modal');
  modal.contentWindow.postMessage(data, location.origin);
};

// Listen for responses
useEffect(() => {
  const handleMessage = (event) => {
    if (event.origin !== location.origin) return;
    console.log('Received from modal:', event.data);
  };
  window.addEventListener('message', handleMessage);
  return () => window.removeEventListener('message', handleMessage);
}, []);
```

### Modal → Main App

```jsx
// Inside modal route
const sendToApp = (data) => {
  window.opener.postMessage(data, location.origin);
};

// Listen for messages from main app
useEffect(() => {
  const handleMessage = (event) => {
    if (event.origin !== location.origin) return;
    console.log('Received from app:', event.data);
  };
  window.addEventListener('message', handleMessage);
  return () => window.removeEventListener('message', handleMessage);
}, []);
```

## Passing Data

### Method 1: URL Parameters (src modals)

```jsx
// Main app - pass data via URL
<Modal
  id="editor-modal"
  variant="max"
  src={`/app/modal/editor?productId=${productId}`}
>

// Modal route - read from URL
import { useSearchParams } from '@remix-run/react';

export default function EditorModal() {
  const [searchParams] = useSearchParams();
  const productId = searchParams.get('productId');
  // ...
}
```

### Method 2: postMessage (src modals)

```jsx
// Main app
const openWithData = (product) => {
  setModalOpen(true);
  // Send data after modal is ready
  setTimeout(() => {
    const modal = document.getElementById('editor-modal');
    modal.contentWindow.postMessage({ type: 'INIT_DATA', payload: product }, location.origin);
  }, 100);
};
```

### Method 3: Props/State (inline content)

```jsx
// Direct access to parent component state
<Modal id="my-modal" variant="max" open={open}>
  <MyEditorComponent data={productData} onSave={handleSave} />
  <TitleBar title="Editor" />
</Modal>
```

## Multi-Step Wizard Pattern

```jsx
import { Modal, TitleBar } from '@shopify/app-bridge-react';
import { BlockStack, InlineStack, ProgressBar, Text, Button } from '@shopify/polaris';
import { useState } from 'react';

const STEPS = ['Basic Info', 'Configuration', 'Review'];

export default function WizardPage() {
  const [open, setOpen] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [formData, setFormData] = useState({});

  const progress = ((currentStep + 1) / STEPS.length) * 100;

  const handleNext = () => {
    if (currentStep < STEPS.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      handleComplete();
    }
  };

  const handleBack = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleComplete = () => {
    console.log('Complete:', formData);
    setOpen(false);
    shopify.toast.show('Setup complete!');
  };

  return (
    <>
      <Button onClick={() => setOpen(true)}>Start Setup Wizard</Button>

      <Modal id="wizard-modal" variant="max" open={open} onHide={() => setOpen(false)}>
        <BlockStack gap="400">
          {/* Progress */}
          <BlockStack gap="200">
            <InlineStack align="space-between">
              <Text variant="bodySm" tone="subdued">
                Step {currentStep + 1} of {STEPS.length}: {STEPS[currentStep]}
              </Text>
              <Text variant="bodySm" tone="subdued">{Math.round(progress)}%</Text>
            </InlineStack>
            <ProgressBar progress={progress} size="small" />
          </BlockStack>

          {/* Step Content */}
          {currentStep === 0 && <StepBasicInfo data={formData} onChange={setFormData} />}
          {currentStep === 1 && <StepConfiguration data={formData} onChange={setFormData} />}
          {currentStep === 2 && <StepReview data={formData} />}

          {/* Navigation */}
          <InlineStack align="end" gap="300">
            {currentStep > 0 && <Button onClick={handleBack}>Back</Button>}
            <Button variant="primary" onClick={handleNext}>
              {currentStep === STEPS.length - 1 ? 'Complete' : 'Next'}
            </Button>
          </InlineStack>
        </BlockStack>

        <TitleBar title={STEPS[currentStep]}>
          <button onClick={() => setOpen(false)}>Cancel</button>
        </TitleBar>
      </Modal>
    </>
  );
}
```

## Nested Modals

Modal max có thể mở một modal base/large trong parent window:

```jsx
// Inside max modal
const openConfirmation = () => {
  window.opener.shopify.modal.show('confirm-modal');
};
```

## Polaris Components trong Modal

Một số Polaris components (Popover, Tooltip, Combobox) sử dụng React Portals cần AppProvider wrapper:

```jsx
import { Modal, TitleBar } from '@shopify/app-bridge-react';
import { AppProvider, Popover, Button } from '@shopify/polaris';

function ModalWithPopover() {
  const [active, setActive] = useState(false);

  return (
    <Modal id="my-modal" variant="max">
      <AppProvider i18n={{}}>
        <Popover
          active={active}
          activator={<Button onClick={() => setActive(true)}>Show options</Button>}
          onClose={() => setActive(false)}
        >
          {/* Popover content */}
        </Popover>
      </AppProvider>
      <TitleBar title="Editor" />
    </Modal>
  );
}
```

> [!NOTE]
> Yêu cầu Polaris 13.19.x hoặc cao hơn.

## Event Callbacks

```jsx
<Modal
  id="my-modal"
  variant="max"
  open={open}
  onShow={() => console.log('Modal opened')}
  onHide={() => {
    console.log('Modal closed');
    setOpen(false);
  }}
>
  {/* content */}
</Modal>
```

## Loading States

```jsx
import { SkeletonPage, Layout, Card, BlockStack, SkeletonBodyText } from '@shopify/polaris';
import { useNavigation } from '@remix-run/react';

export default function ModalWithLoading() {
  const navigation = useNavigation();
  const isLoading = navigation.state === 'loading';

  if (isLoading) {
    return (
      <SkeletonPage title="Loading...">
        <Layout>
          <Layout.Section>
            <Card>
              <BlockStack gap="400">
                <SkeletonBodyText lines={3} />
                <SkeletonBodyText lines={2} />
              </BlockStack>
            </Card>
          </Layout.Section>
        </Layout>
      </SkeletonPage>
    );
  }

  return (
    // Actual content
  );
}
```

## Best Practices

> [!IMPORTANT]
> **Route Organization**: Đặt modal routes trong folder riêng (e.g., `app/routes/app.modal.*.jsx`).

> [!TIP]
> **Unique IDs**: Luôn dùng ID mô tả, unique để tránh conflicts.

> [!WARNING]
> **Variant Restriction**: Sau khi modal đã show, chỉ có thể thay đổi giữa `small`, `base`, `large`. Không thể đổi sang/từ `max`.

### Do's

- Dùng React state (`open` prop) để control modal thay vì imperative API khi có thể
- Implement loading states với Polaris skeleton components
- Validate form data trước khi cho phép "Next" trong wizards
- Dùng `TitleBar` component cho modal header
- Wrap Polaris portal components trong `AppProvider`

### Don'ts

- **KHÔNG** dùng inline styles - sử dụng Polaris layout components
- **KHÔNG** quên handle "Cancel" và close events
- **KHÔNG** store sensitive data trong URL parameters
- **KHÔNG** expect modal route access parent app state trực tiếp (dùng postMessage)
- **KHÔNG** quên include `app-bridge.js` script trong modal routes

## Limitations

**HTML Content Modals không thể:**
- Execute custom JavaScript ngoài HTML/CSS
- Access document trực tiếp (separate iframe)
- Sử dụng third-party libraries cần document access

**src Modals không thể:**
- Access App Bridge toast, navigation trực tiếp từ modal
- Share context không qua postMessage
- Access main app stylesheets (phải include lại)

## Size Options Reference

| Variant | Description | Use Case |
|---------|-------------|----------|
| `small` | ~450px width | Simple confirmations |
| `base` | Default size | Standard forms (default) |
| `large` | ~720px width | Complex forms, selections |
| `max` | Full viewport | Editors, wizards, previews |
