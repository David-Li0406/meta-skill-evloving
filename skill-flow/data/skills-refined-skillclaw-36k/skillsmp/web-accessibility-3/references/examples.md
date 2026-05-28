# Production Examples

Real-world accessibility patterns from the YourCompany web monorepo.

## Number Stepper Component

**Location**: `app/spaces/one-time-purchase/modules/main/components/cart/components/Stepper.tsx`

### Complete Example with Context-Aware Labels

```typescript
import React, { useState, useEffect, useRef } from 'react';
import { Box, NumberStepper, Tooltip } from '@/libs/zest';
import { useT9n } from '@/libs/translation';

export const Stepper = ({
  onIncrease,
  onDecrease,
  quantity,
  canIncrease = true,
  canDecrease = true,
  tooltipMessage,
  shouldShowTooltip,
  itemName,
}: Props) => {
  const { translateRaw } = useT9n('one-time-purchase');
  const decreaseRef = useRef<HTMLButtonElement | null>(null);
  const increaseRef = useRef<HTMLButtonElement | null>(null);

  return (
    <NumberStepper size="sm" aria-label={`${itemName} quantity stepper`}>
      {canDecrease ? (
        <NumberStepper.DecrementButton
          onClick={onDecrease}
          data-test-id="cart-quantity-btn-decrease"
          ref={decreaseRef}
          aria-label={`Decrease ${itemName} quantity`}
        />
      ) : (
        <Box
          aria-label={`Decrease ${itemName} quantity (disabled)`}
          onMouseEnter={() => handleButtonTooltip()}
        >
          <Tooltip
            variant="dark"
            position="top"
            isVisible={visibleTooltip && shouldShowTooltip}
            content={tooltipMessage as string}
            trigger={
              <NumberStepper.DecrementButton
                onClick={onDecrease}
                disabled={!canDecrease}
                ref={decreaseRef}
                aria-label={`Decrease ${itemName} quantity (disabled)`}
              />
            }
          />
        </Box>
      )}

      <NumberStepper.Value
        data-test-id="cart-quantity-btn-value"
        aria-label={`${itemName} quantity`}
      >
        {quantity}
      </NumberStepper.Value>

      {canIncrease ? (
        <NumberStepper.IncrementButton
          onClick={onIncrease}
          data-test-id="cart-quantity-btn-increase"
          ref={increaseRef}
          aria-label={`Increase ${itemName} quantity`}
        />
      ) : (
        <Box
          aria-label={`Increase ${itemName} quantity (disabled)`}
          onMouseEnter={() => handleButtonTooltip()}
        >
          <Tooltip
            variant="dark"
            position="top"
            isVisible={visibleTooltip && shouldShowTooltip}
            content={translateRaw(
              'one-time-purchase.cart.stepper.tooltip-text'
            )}
            trigger={
              <NumberStepper.IncrementButton
                onClick={onIncrease}
                disabled={!canIncrease}
                ref={increaseRef}
                aria-label={`Increase ${itemName} quantity (disabled)`}
              />
            }
          />
        </Box>
      )}
    </NumberStepper>
  );
};
```

**Key Patterns**:

- ✅ Container has descriptive `aria-label` with item context
- ✅ Each button has specific `aria-label` describing its action
- ✅ Disabled state communicated in `aria-label`
- ✅ Dynamic labels include item name for context
- ✅ Tooltips provide additional information for disabled states
- ✅ Value display has its own `aria-label`
- ✅ Translated strings used for user-facing content

## Form Input with Label

**Pattern**: Always associate labels with inputs using `htmlFor`

```typescript
import { useT9n } from '@/libs/translation';

const EmailInput = () => {
  const { translateRaw } = useT9n('checkout');

  return (
    <div>
      <label htmlFor="email-input">
        {translateRaw('checkout.form.email.label')}
      </label>
      <input
        id="email-input"
        type="email"
        name="email"
        aria-describedby="email-helper"
        aria-invalid={hasError}
        aria-required="true"
      />
      {hasError && (
        <span id="email-error" role="alert">
          {translateRaw('checkout.form.email.error')}
        </span>
      )}
      <span id="email-helper">
        {translateRaw('checkout.form.email.helper')}
      </span>
    </div>
  );
};
```

**Key Patterns**:

- ✅ `htmlFor` links label to input
- ✅ `aria-describedby` references helper text
- ✅ `aria-invalid` indicates error state
- ✅ `aria-required` indicates required field
- ✅ Error messages use `role="alert"` for immediate announcement
- ✅ All text content is translated

## Modal Dialog

**Pattern**: Proper dialog role with focus management

```typescript
import { Dialog } from '@/libs/zest';

const ConfirmationDialog = ({ isOpen, onClose, onConfirm }) => {
  return (
    <Dialog
      open={isOpen}
      onOpenChange={onClose}
      aria-labelledby="dialog-title"
      aria-describedby="dialog-description"
    >
      <Dialog.Content>
        <Dialog.Title id="dialog-title">Confirm Action</Dialog.Title>
        <Dialog.Description id="dialog-description">
          Are you sure you want to proceed with this action?
        </Dialog.Description>
        <div role="group" aria-label="Dialog actions">
          <button onClick={onClose} aria-label="Cancel action">
            Cancel
          </button>
          <button onClick={onConfirm} aria-label="Confirm action">
            Confirm
          </button>
        </div>
      </Dialog.Content>
    </Dialog>
  );
};
```

**Key Patterns**:

- ✅ `role="dialog"` on container (handled by Zest Dialog)
- ✅ `aria-labelledby` references dialog title
- ✅ `aria-describedby` references dialog description
- ✅ Actions grouped with `role="group"`
- ✅ Buttons have descriptive `aria-label`
- ✅ Focus automatically managed by Zest Dialog component

## Button with Icon

**Pattern**: Descriptive labels for icon-only buttons

```typescript
import { IconButton } from '@/libs/zest';
import { useT9n } from '@/libs/translation';

const CloseButton = ({ onClose }) => {
  const { translateRaw } = useT9n('common');

  return (
    <IconButton
      onClick={onClose}
      aria-label={translateRaw('common.button.close')}
      data-test-id="close-button"
    >
      <CloseIcon />
    </IconButton>
  );
};

// For buttons with text + icon
const AddToCartButton = ({ onClick, productName }) => {
  return (
    <button onClick={onClick} aria-label={`Add ${productName} to cart`}>
      <PlusIcon aria-hidden="true" />
      <span>Add to Cart</span>
    </button>
  );
};
```

**Key Patterns**:

- ✅ Icon-only buttons have descriptive `aria-label`
- ✅ Decorative icons in text buttons use `aria-hidden="true"`
- ✅ Labels are translated
- ✅ Labels include context (product name, action)

## List with Accessible Items

**Pattern**: Proper list markup with accessible list items

```typescript
const RecipeList = ({ recipes }) => {
  return (
    <ul role="list" aria-label="Recipe collection">
      {recipes.map((recipe) => (
        <li key={recipe.id} role="listitem">
          <a
            href={`/recipes/${recipe.id}`}
            aria-label={`View ${recipe.name} recipe details`}
          >
            <img
              src={recipe.image}
              alt={`${recipe.name} recipe photo`}
              role="img"
            />
            <h3>{recipe.name}</h3>
            <p>{recipe.description}</p>
          </a>
        </li>
      ))}
    </ul>
  );
};
```

**Key Patterns**:

- ✅ `role="list"` and `role="listitem"` for proper list structure
- ✅ Container has descriptive `aria-label`
- ✅ Links have descriptive `aria-label` including item name
- ✅ Images have descriptive alt text
- ✅ Semantic HTML structure (`<a>`, `<h3>`, `<p>`)

## Loading States

**Pattern**: Announce loading states to screen readers

```typescript
import { Spinner } from '@/libs/zest';

const LoadingButton = ({ isLoading, onClick, children }) => {
  return (
    <button
      onClick={onClick}
      disabled={isLoading}
      aria-busy={isLoading}
      aria-live="polite"
    >
      {isLoading ? (
        <>
          <Spinner size="sm" aria-label="Loading" />
          <span className="sr-only">Loading...</span>
        </>
      ) : (
        children
      )}
    </button>
  );
};

// For page-level loading
const PageLoader = () => {
  return (
    <div role="status" aria-live="polite" aria-busy="true">
      <Spinner aria-label="Loading page content" />
      <span className="sr-only">Loading page content, please wait...</span>
    </div>
  );
};
```

**Key Patterns**:

- ✅ `aria-busy` indicates loading state
- ✅ `aria-live="polite"` announces changes
- ✅ Screen reader only text with `.sr-only` class
- ✅ `role="status"` for status updates
- ✅ Descriptive loading messages

## Navigation Menu

**Pattern**: Accessible navigation with proper ARIA roles

```typescript
const Navigation = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav aria-label="Main navigation">
      <button
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
        aria-controls="nav-menu"
        aria-label="Toggle navigation menu"
      >
        ☰ Menu
      </button>

      <ul
        id="nav-menu"
        role="menu"
        aria-label="Main menu items"
        hidden={!isOpen}
      >
        <li role="none">
          <a href="/recipes" role="menuitem">
            Recipes
          </a>
        </li>
        <li role="none">
          <a href="/plans" role="menuitem">
            Plans
          </a>
        </li>
        <li role="none">
          <a href="/about" role="menuitem">
            About
          </a>
        </li>
      </ul>
    </nav>
  );
};
```

**Key Patterns**:

- ✅ `<nav>` element with descriptive `aria-label`
- ✅ Toggle button has `aria-expanded` state
- ✅ `aria-controls` links button to menu
- ✅ Menu has `role="menu"` and descriptive label
- ✅ Menu items have `role="menuitem"`
- ✅ List items have `role="none"` when using ARIA menu roles

## Error Handling

**Pattern**: Accessible error messages with announcements

```typescript
const FormWithErrors = () => {
  const [errors, setErrors] = useState<string[]>([]);

  return (
    <form onSubmit={handleSubmit} noValidate>
      {errors.length > 0 && (
        <div
          role="alert"
          aria-live="assertive"
          aria-atomic="true"
          className="error-summary"
        >
          <h2 id="error-summary-title">
            There are {errors.length} errors in the form
          </h2>
          <ul aria-labelledby="error-summary-title">
            {errors.map((error, index) => (
              <li key={index}>
                <a href={`#${error.fieldId}`}>{error.message}</a>
              </li>
            ))}
          </ul>
        </div>
      )}

      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          aria-invalid={hasEmailError}
          aria-describedby={hasEmailError ? 'email-error' : undefined}
        />
        {hasEmailError && (
          <span id="email-error" role="alert">
            Please enter a valid email address
          </span>
        )}
      </div>
    </form>
  );
};
```

**Key Patterns**:

- ✅ Error summary with `role="alert"`
- ✅ `aria-live="assertive"` for immediate announcement
- ✅ `aria-atomic="true"` reads entire message
- ✅ Links to specific error fields
- ✅ Individual field errors also use `role="alert"`
- ✅ `aria-invalid` on fields with errors
- ✅ `aria-describedby` links to error messages
