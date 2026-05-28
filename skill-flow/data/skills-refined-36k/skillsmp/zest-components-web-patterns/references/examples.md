# Real Component Examples from Production

This document contains real examples from the YourCompany web repository, extracted from actual PRs.

## Simple Component: Badge

**Location**: `packages/zest/src/Badge/`

### Badge.tsx
```typescript
import React, { Ref, forwardRef } from 'react';
import { BoxWithNewTokens as Box } from '../Box';
import Text from '../Text';
import variants from './variants';
import defaultStyles from './styles';
import { BadgeProps } from './types';

/**
 * ### Badge
 * A small visual indicator for status, count, or label.
 *
 * See the [docs](https://www-staging.yourcompany.com/zest-docs/Badge) for more information.
 *
 * #### Usage
 *
    ```js
    import { Badge } from '@/libs/zest';

    return (
      <Badge variant="error">5</Badge>
    )
    ```
  */

const Badge = forwardRef((props: BadgeProps, ref?: Ref<HTMLDivElement>) => {
  const { children, variant = 'neutral', ...rest } = props;

  return (
    <Box
      ref={ref}
      variants={variants}
      variant={variant}
      {...rest}
      {...defaultStyles}
    >
      {children}
    </Box>
  );
});

Badge.displayName = 'Badge';

export default Badge;
```

### index.ts
```typescript
import Badge from './Badge';
export default Badge;
```

### types.ts
```typescript
import type { StyledSystemComponent } from '@/libs/zest-support';
import type { CSSProperties } from 'react';

export type BadgeProps = {
  variant?: 'neutral' | 'error' | 'success' | 'warning';
  children: React.ReactNode;
} & Omit<React.HTMLAttributes<HTMLDivElement>, keyof CSSProperties | 'style'>;
```

### styles.ts
```typescript
import type { BoxProps } from '../Box/BoxWithNewTokens';

export default {
  display: 'inline-flex',
  justifyContent: 'center',
  alignItems: 'center',
  borderRadius: 'components.badge.border-radius.default',
  minWidth: '1.25rem',
  height: '1.25rem',
  paddingX: 'components.badge.spacing.padding-x',
  paddingY: 'components.badge.spacing.padding-y',
} as BoxProps;
```

### variants.ts
```typescript
import type { Variant, UseNewTokens } from '@/libs/zest-support';

const variants: Variant<UseNewTokens>[] = [
  {
    prop: 'variant',
    variants: {
      neutral: {
        bg: 'components.badge.color.neutral.background',
        color: 'components.badge.color.foreground',
      },
      error: {
        bg: 'components.badge.color.negative.background',
        color: 'components.badge.color.foreground',
      },
      success: {
        bg: 'components.badge.color.positive.background',
        color: 'components.badge.color.foreground',
      },
      warning: {
        bg: 'components.badge.color.warning.background',
        color: 'components.badge.color.foreground',
      },
    },
  },
];

export default variants;
```

---

## Complex Component: Accordion

**Location**: `packages/zest/src/Accordion/`

### index.tsx
```typescript
import React, { createContext, useContext, useState } from 'react';
import { BoxWithNewTokens as Box } from '../Box';
import Title from './Title';
import Description from './Description';
import ButtonWrapper from './ButtonWrapper';
import type { AccordionProps, AccordionContextType } from './types';

const AccordionContext = createContext<AccordionContextType | undefined>(undefined);

export const useAccordionContext = () => {
  const context = useContext(AccordionContext);
  if (!context) {
    throw new Error('Accordion compound components must be used within Accordion');
  }
  return context;
};

/**
 * ### Accordion
 * Collapsible content sections with title and description.
 *
 * #### Usage
 *
    ```js
    import { Accordion } from '@/libs/zest';

    return (
      <Accordion defaultOpen={false}>
        <Accordion.Title>Title</Accordion.Title>
        <Accordion.Description>Content</Accordion.Description>
      </Accordion>
    )
    ```
  */

const Accordion: React.FC<AccordionProps> = ({ children, defaultOpen = false, onToggle }) => {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  const handleToggle = () => {
    setIsOpen(!isOpen);
    onToggle?.(!isOpen);
  };

  return (
    <AccordionContext.Provider value={{ isOpen, onToggle: handleToggle }}>
      <Box
        borderWidth="1px"
        borderColor="global.border.default"
        borderRadius="global.md"
        padding="global.md"
      >
        {children}
      </Box>
    </AccordionContext.Provider>
  );
};

export default Object.assign(Accordion, {
  Title,
  Description,
  ButtonWrapper,
});
```

### Title.tsx
```typescript
import React from 'react';
import { BoxWithNewTokens as Box } from '../Box';
import Text from '../Text';
import { useAccordionContext } from './index';
import ButtonWrapper from './ButtonWrapper';
import type { TitleProps } from './types';

const Title: React.FC<TitleProps> = ({ children }) => {
  const { onToggle } = useAccordionContext();

  return (
    <Box
      display="flex"
      justifyContent="space-between"
      alignItems="center"
      onClick={onToggle}
      cursor="pointer"
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          onToggle();
        }
      }}
    >
      <Text type="body-lg-bold">{children}</Text>
      <ButtonWrapper />
    </Box>
  );
};

export default Title;
```

### Description.tsx
```typescript
import React from 'react';
import { BoxWithNewTokens as Box } from '../Box';
import Text from '../Text';
import { useAccordionContext } from './index';
import type { DescriptionProps } from './types';

const Description: React.FC<DescriptionProps> = ({ children }) => {
  const { isOpen } = useAccordionContext();

  if (!isOpen) return null;

  return (
    <Box marginTop="global.sm">
      <Text type="body-md-regular">{children}</Text>
    </Box>
  );
};

export default Description;
```

### ButtonWrapper/index.tsx
```typescript
import React from 'react';
import { BoxWithNewTokens as Box } from '../../Box';
import { useAccordionContext } from '../index';
import ChevronIcon from './ChevronIcon';

const ButtonWrapper: React.FC = () => {
  const { isOpen } = useAccordionContext();

  return (
    <Box
      transition="transform 0.2s ease"
      transform={isOpen ? 'rotate(180deg)' : 'rotate(0deg)'}
    >
      <ChevronIcon />
    </Box>
  );
};

export default ButtonWrapper;
```

### types.ts
```typescript
import type { CSSProperties } from 'react';

export type AccordionProps = {
  children: React.ReactNode;
  defaultOpen?: boolean;
  onToggle?: (isOpen: boolean) => void;
} & Omit<React.HTMLAttributes<HTMLDivElement>, keyof CSSProperties | 'style'>;

export type TitleProps = {
  children: React.ReactNode;
};

export type DescriptionProps = {
  children: React.ReactNode;
};

export type AccordionContextType = {
  isOpen: boolean;
  onToggle: () => void;
};
```

---

## Component with Variants: Button

**Location**: `packages/zest/src/Button/`

### BaseButton.tsx
```typescript
import React, { Ref, forwardRef } from 'react';
import { BoxWithNewTokens as Box } from '../Box';
import Text from '../Text';
import Icon from '../Icon';
import variants from './variants';
import defaultStyles from './defaultStyles';
import type { BaseButtonProps } from './types';

const BaseButton = forwardRef((props: BaseButtonProps, ref?: Ref<HTMLButtonElement>) => {
  const {
    children,
    variant = 'primary',
    size = 'md',
    icon,
    iconPosition = 'left',
    disabled = false,
    loading = false,
    ...rest
  } = props;

  return (
    <Box
      as="button"
      ref={ref}
      variants={variants}
      variant={variant}
      size={size}
      disabled={disabled || loading}
      {...rest}
      {...defaultStyles}
    >
      {icon && iconPosition === 'left' && (
        <Icon name={icon} size={size === 'sm' ? 16 : 24} />
      )}
      <Text type={size === 'sm' ? 'body-sm-bold' : 'body-md-bold'}>{children}</Text>
      {icon && iconPosition === 'right' && (
        <Icon name={icon} size={size === 'sm' ? 16 : 24} />
      )}
      {loading && <span>Loading...</span>}
    </Box>
  );
});

BaseButton.displayName = 'BaseButton';

export default BaseButton;
```

### PrimaryButton.tsx
```typescript
import React, { Ref, forwardRef } from 'react';
import BaseButton from './BaseButton';
import type { PrimaryButtonProps } from './types';

const PrimaryButton = forwardRef((props: PrimaryButtonProps, ref?: Ref<HTMLButtonElement>) => {
  return <BaseButton ref={ref} variant="primary" {...props} />;
});

PrimaryButton.displayName = 'PrimaryButton';

export default PrimaryButton;
```

### SecondaryButton.tsx
```typescript
import React, { Ref, forwardRef } from 'react';
import BaseButton from './BaseButton';
import type { SecondaryButtonProps } from './types';

const SecondaryButton = forwardRef((props: SecondaryButtonProps, ref?: Ref<HTMLButtonElement>) => {
  return <BaseButton ref={ref} variant="secondary" {...props} />;
});

SecondaryButton.displayName = 'SecondaryButton';

export default SecondaryButton;
```

### index.tsx
```typescript
import PrimaryButton from './PrimaryButton';
import SecondaryButton from './SecondaryButton';
import TertiaryButton from './TertiaryButton';

const Button = {
  Primary: PrimaryButton,
  Secondary: SecondaryButton,
  Tertiary: TertiaryButton,
};

export default Button;
```

### types.ts
```typescript
import type { Icons16, Icons24 } from '@/libs/zest-support/icons';
import type { CSSProperties } from 'react';

export type BaseButtonProps = {
  variant?: 'primary' | 'secondary' | 'tertiary';
  size?: 'sm' | 'md' | 'lg';
  icon?: Icons16 | Icons24;
  iconPosition?: 'left' | 'right';
  loading?: boolean;
  disabled?: boolean;
  children: React.ReactNode;
} & Omit<React.ButtonHTMLAttributes<HTMLButtonElement>, keyof CSSProperties | 'style'>;

export type PrimaryButtonProps = Omit<BaseButtonProps, 'variant'>;
export type SecondaryButtonProps = Omit<BaseButtonProps, 'variant'>;
export type TertiaryButtonProps = Omit<BaseButtonProps, 'variant'>;
```

### defaultStyles.ts
```typescript
import type { BoxProps } from '../Box/BoxWithNewTokens';

export default {
  display: 'inline-flex',
  alignItems: 'center',
  justifyContent: 'center',
  gap: 'global.sm',
  borderRadius: 'components.button.border-radius.default',
  cursor: 'pointer',
  transition: 'all 0.2s ease',
  border: 'none',
  outline: 'none',
  '&:disabled': {
    cursor: 'not-allowed',
    opacity: 0.5,
  },
  '&:focus-visible': {
    boxShadow: '0 0 0 3px rgba(0, 123, 255, 0.3)',
  },
} as BoxProps;
```

### variants/index.ts
```typescript
import type { Variant, UseNewTokens } from '@/libs/zest-support';
import brandVariants from './brandVariants';
import sizeVariants from './sizeVariants';

const variants: Variant<UseNewTokens>[] = [
  brandVariants,
  sizeVariants,
];

export default variants;
```

### variants/brandVariants.ts
```typescript
import type { Variant, UseNewTokens } from '@/libs/zest-support';

const brandVariants: Variant<UseNewTokens> = {
  prop: 'variant',
  variants: {
    primary: {
      bg: 'components.button.color.brand.background',
      color: 'components.button.color.foreground',
      '&:hover:not(:disabled)': {
        bg: 'components.button.color.brand.background-hover',
      },
      '&:active:not(:disabled)': {
        bg: 'components.button.color.brand.background-active',
      },
    },
    secondary: {
      bg: 'components.button.color.neutral.background',
      color: 'components.button.color.neutral.foreground',
      borderWidth: '1px',
      borderColor: 'components.button.color.neutral.border',
      '&:hover:not(:disabled)': {
        bg: 'components.button.color.neutral.background-hover',
      },
      '&:active:not(:disabled)': {
        bg: 'components.button.color.neutral.background-active',
      },
    },
    tertiary: {
      bg: 'transparent',
      color: 'components.button.color.brand.foreground',
      '&:hover:not(:disabled)': {
        textDecoration: 'underline',
      },
    },
  },
};

export default brandVariants;
```

### variants/sizeVariants.ts
```typescript
import type { Variant, UseNewTokens } from '@/libs/zest-support';

const sizeVariants: Variant<UseNewTokens> = {
  prop: 'size',
  variants: {
    sm: {
      height: '2rem',
      paddingX: 'global.md',
      paddingY: 'global.sm',
    },
    md: {
      height: '2.5rem',
      paddingX: 'global.lg',
      paddingY: 'global.md',
    },
    lg: {
      height: '3rem',
      paddingX: 'global.xl',
      paddingY: 'global.lg',
    },
  },
};

export default sizeVariants;
```

---

## Migration Example: Converting Legacy Component

**Before** (PriceItem.js - Old Pattern):
```javascript
import PropTypes from 'prop-types';

export const PriceItem = ({ amount, label, isTotal, isShipping, freeLabel }) => {
  return (
    <div css={styles.row({ isTotal, isShipping })}>
      <span>{label}</span>
      <span css={styles.priceAmount}>{amount ? `$${amount}` : freeLabel}</span>
    </div>
  );
};

PriceItem.propTypes = {
  amount: PropTypes.number,
  label: PropTypes.string,
  isTotal: PropTypes.bool,
  isShipping: PropTypes.bool,
  freeLabel: PropTypes.string,
};

const styles = {
  row: ({ isTotal }) => (theme) => ({
    display: 'flex',
    justifyContent: 'space-between',
    ...(isTotal && { fontWeight: 600 }),
  }),
  priceAmount: {
    fontWeight: 500,
  },
};
```

**After** (PriceItem.tsx - Zest Pattern):
```typescript
import React from 'react';
import { Box, Text } from '@/libs/zest';
import type { TextTypes, TextProps } from '@/libs/zest';

interface PriceItemProps {
  amount: number;
  label: string;
  testid: string;
  isLoading?: boolean;
  color?: TextProps['color'];
}

export const PriceItem: React.FC<PriceItemProps> = (props) => (
  <Box display="flex" justifyContent="space-between" marginBottom="xs">
    <Item {...props} textType="body-md-regular" />
  </Box>
);

export const TotalPriceItem: React.FC<PriceItemProps> = (props) => (
  <Box
    display="flex"
    justifyContent="space-between"
    marginBottom="xs"
    borderTopWidth="1px"
    borderTopColor="global.gray.300"
    borderTopStyle="solid"
    paddingTop="global.sm-1"
  >
    <Item {...props} textType="body-lg-bold" />
  </Box>
);

const Item: React.FC<PriceItemProps & { textType: TextTypes }> = ({
  amount,
  label,
  testid,
  textType,
  color,
}) => {
  const formatCurrency = useFormattedCurrency();
  const price = !!amount ? formatCurrency({ value: amount }) : freeLabel;

  return (
    <>
      <Text as="span" type={textType} data-testid={`${testid}-label`} color={color}>
        {label}
      </Text>
      <Text as="span" type={textType} data-testid={`${testid}-amount`} color={color}>
        {price}
      </Text>
    </>
  );
};
```

**Key Migration Changes**:
1. Convert `.js` → `.tsx`
2. Replace PropTypes with TypeScript interfaces
3. Replace CSS-in-JS with Zest Box component props
4. Use Zest Text component instead of styled spans
5. Replace boolean flags with component composition
6. Use design tokens instead of hardcoded values
7. Add proper TypeScript types
8. Improve component structure with composition

---

## Storybook Example: Badge Stories

**Location**: `apps/zest-docs/stories/Badge.stories.tsx`

```typescript
import type { Meta, StoryObj } from '@storybook/nextjs';
import { Badge } from '@/packages/zest';

const meta: Meta<typeof Badge> = {
  title: 'Components/Feedback/Badge',
  component: Badge,
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['neutral', 'error', 'success', 'warning'],
      description: 'Visual variant style of the badge',
    },
    children: {
      control: 'text',
      description: 'Content to display inside the badge',
    },
  },
  parameters: {
    docs: {
      description: {
        component:
          'A small visual indicator used to display counts, status, or labels. Commonly used for notification counts, status indicators, or highlighting new content.',
      },
    },
  },
};

export default meta;
type Story = StoryObj<typeof Badge>;

export const Default: Story = {
  args: {
    variant: 'neutral',
    children: '5',
  },
};

export const Variants: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
      <Badge variant="neutral">Neutral</Badge>
      <Badge variant="error">3</Badge>
      <Badge variant="success">✓</Badge>
      <Badge variant="warning">!</Badge>
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story: 'Badge supports multiple variants for different use cases.',
      },
    },
  },
};

export const WithNumbers: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
      <Badge>1</Badge>
      <Badge>12</Badge>
      <Badge>99+</Badge>
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story: 'Badges automatically adjust width based on content.',
      },
    },
  },
};

export const WithText: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
      <Badge variant="error">New</Badge>
      <Badge variant="success">Active</Badge>
      <Badge variant="warning">Pending</Badge>
    </div>
  ),
  parameters: {
    docs: {
      description: {
        story: 'Badges can also display short text labels.',
      },
    },
  },
};
```

---

## Test Example: Comprehensive Button Tests

```typescript
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { ThemeProvider } from '@/libs/zest-support';
import Button from './index';

describe('Button', () => {
  it('should render primary button correctly', () => {
    render(
      <ThemeProvider>
        <Button.Primary>Click me</Button.Primary>
      </ThemeProvider>
    );
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('should render all variants', () => {
    const { rerender } = render(
      <ThemeProvider>
        <Button.Primary>Primary</Button.Primary>
      </ThemeProvider>
    );
    expect(screen.getByText('Primary')).toBeInTheDocument();

    rerender(
      <ThemeProvider>
        <Button.Secondary>Secondary</Button.Secondary>
      </ThemeProvider>
    );
    expect(screen.getByText('Secondary')).toBeInTheDocument();

    rerender(
      <ThemeProvider>
        <Button.Tertiary>Tertiary</Button.Tertiary>
      </ThemeProvider>
    );
    expect(screen.getByText('Tertiary')).toBeInTheDocument();
  });

  it('should handle click events', () => {
    const handleClick = jest.fn();
    render(
      <ThemeProvider>
        <Button.Primary onClick={handleClick}>Click me</Button.Primary>
      </ThemeProvider>
    );

    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('should not trigger click when disabled', () => {
    const handleClick = jest.fn();
    render(
      <ThemeProvider>
        <Button.Primary disabled onClick={handleClick}>
          Disabled
        </Button.Primary>
      </ThemeProvider>
    );

    fireEvent.click(screen.getByText('Disabled'));
    expect(handleClick).not.toHaveBeenCalled();
  });

  it('should render with icon', () => {
    render(
      <ThemeProvider>
        <Button.Primary icon="arrow-right">With Icon</Button.Primary>
      </ThemeProvider>
    );
    expect(screen.getByText('With Icon')).toBeInTheDocument();
    // Icon assertion would depend on Icon component implementation
  });

  it('should render loading state', () => {
    render(
      <ThemeProvider>
        <Button.Primary loading>Loading</Button.Primary>
      </ThemeProvider>
    );
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('should match snapshot', () => {
    const { container } = render(
      <ThemeProvider>
        <Button.Primary variant="primary" size="md">
          Snapshot Test
        </Button.Primary>
      </ThemeProvider>
    );
    expect(container).toMatchSnapshot();
  });

  it('should support keyboard navigation', () => {
    const handleClick = jest.fn();
    render(
      <ThemeProvider>
        <Button.Primary onClick={handleClick}>Keyboard Test</Button.Primary>
      </ThemeProvider>
    );

    const button = screen.getByText('Keyboard Test');
    button.focus();
    expect(button).toHaveFocus();

    fireEvent.keyDown(button, { key: 'Enter' });
    expect(handleClick).toHaveBeenCalled();
  });
});
```

---

These examples represent actual patterns used in production. Use them as templates when creating or updating Zest components.
