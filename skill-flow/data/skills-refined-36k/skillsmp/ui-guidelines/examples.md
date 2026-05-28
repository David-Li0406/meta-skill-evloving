# Code Examples

Complete examples for creating UI components in ludiscan-webapp.

## Creating a New Atom Component

```tsx
// src/component/atoms/Badge.tsx
import styled from '@emotion/styled';
import type { FC } from 'react';

export type BadgeProps = {
  className?: string;
  label: string;
  variant: 'success' | 'warning' | 'error' | 'info';
};

const Component: FC<BadgeProps> = ({ className, label }) => {
  return <span className={className}>{label}</span>;
};

export const Badge = styled(Component)`
  display: inline-flex;
  align-items: center;
  padding: ${({ theme }) => `${theme.spacing.xs} ${theme.spacing.sm}`};
  font-size: ${({ theme }) => theme.typography.fontSize.xs};
  font-weight: ${({ theme }) => theme.typography.fontWeight.semibold};
  border-radius: ${({ theme }) => theme.borders.radius.full};

  background-color: ${({ theme, variant }) => theme.colors.semantic[variant].main};
  color: ${({ theme, variant }) => theme.colors.semantic[variant].contrast};
`;
```

## Creating a New Molecule Component

```tsx
// src/component/molecules/LabeledInput.tsx
import styled from '@emotion/styled';
import type { FC } from 'react';

import { FlexColumn } from '@src/component/atoms/Flex';
import { Text } from '@src/component/atoms/Text';
import { TextField } from '@src/component/molecules/TextField';
import { useSharedTheme } from '@src/hooks/useSharedTheme';

export type LabeledInputProps = {
  className?: string;
  label: string;
  value: string;
  onChange: (value: string) => void;
  required?: boolean;
};

const Component: FC<LabeledInputProps> = ({
  className,
  label,
  value,
  onChange,
  required
}) => {
  const { theme } = useSharedTheme();

  return (
    <FlexColumn className={className} gap={4}>
      <Text
        text={`${label}${required ? ' *' : ''}`}
        fontSize={theme.typography.fontSize.sm}
        fontWeight={theme.typography.fontWeight.medium}
        color={theme.colors.text.secondary}
      />
      <TextField
        value={value}
        onChange={onChange}
      />
    </FlexColumn>
  );
};

export const LabeledInput = styled(Component)`
  width: 100%;
`;
```

## Creating a Storybook Story

```tsx
// src/component/atoms/Badge.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Badge } from './Badge';

const meta: Meta<typeof Badge> = {
  title: 'Atoms/Badge',
  component: Badge,
  argTypes: {
    variant: {
      control: 'select',
      options: ['success', 'warning', 'error', 'info'],
    },
  },
};

export default meta;
type Story = StoryObj<typeof Badge>;

export const Success: Story = {
  args: {
    variant: 'success',
    label: 'Active',
  },
};

export const Warning: Story = {
  args: {
    variant: 'warning',
    label: 'Pending',
  },
};

export const Error: Story = {
  args: {
    variant: 'error',
    label: 'Failed',
  },
};
```

## Custom Hook Example

```tsx
// src/hooks/useUserProfile.ts
import { useGetApi } from '@src/hooks/useGetApi';
import type { components } from '@generated/api.d.ts';

type User = components['schemas']['User'];

export const useUserProfile = (userId: string) => {
  const { data, isLoading, error, refetch } = useGetApi<User>(
    `/api/users/${userId}`,
    { enabled: !!userId }
  );

  return {
    user: data,
    isLoading,
    error,
    refetch,
  };
};
```

## Event Handler Pattern

```tsx
// src/component/molecules/ActionButton.tsx
import styled from '@emotion/styled';
import { useCallback, type FC } from 'react';

import { Button } from '@src/component/atoms/Button';

export type ActionButtonProps = {
  className?: string;
  id: string;
  label: string;
  onAction: (id: string) => void;
};

const Component: FC<ActionButtonProps> = ({
  className,
  id,
  label,
  onAction,
}) => {
  const handleClick = useCallback(
    (e: React.MouseEvent) => {
      e.stopPropagation();
      onAction(id);
    },
    [id, onAction]
  );

  return (
    <Button className={className} scheme="primary" onClick={handleClick}>
      {label}
    </Button>
  );
};

export const ActionButton = styled(Component)``;
```

## Responsive Component Example

```tsx
// src/component/organisms/ResponsiveCard.tsx
import styled from '@emotion/styled';
import type { FC, ReactNode } from 'react';

import { FlexColumn, FlexRow } from '@src/component/atoms/Flex';
import { useIsDesktop } from '@src/hooks/useIsDesktop';

export type ResponsiveCardProps = {
  className?: string;
  header: ReactNode;
  content: ReactNode;
  actions: ReactNode;
};

const Component: FC<ResponsiveCardProps> = ({
  className,
  header,
  content,
  actions,
}) => {
  const isDesktop = useIsDesktop();

  if (isDesktop) {
    return (
      <FlexRow className={className} gap={16} align="center">
        <div>{header}</div>
        <FlexColumn style={{ flex: 1 }}>{content}</FlexColumn>
        <div>{actions}</div>
      </FlexRow>
    );
  }

  return (
    <FlexColumn className={className} gap={8}>
      {header}
      {content}
      {actions}
    </FlexColumn>
  );
};

export const ResponsiveCard = styled(Component)`
  padding: ${({ theme }) => theme.spacing.md};
  background: ${({ theme }) => theme.colors.surface.base};
  border-radius: ${({ theme }) => theme.borders.radius.md};
`;
```

## Mock Data Factory Example

```tsx
// src/utils/mockData.ts
import type { components } from '@generated/api.d.ts';

type Project = components['schemas']['Project'];
type Session = components['schemas']['Session'];

export const createMockProject = (overrides?: Partial<Project>): Project => {
  return {
    id: 'mock-project-1',
    name: 'Mock Project',
    description: 'A mock project for testing',
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    owner_id: 'mock-user-1',
    ...overrides,
  };
};

export const createMockSession = (overrides?: Partial<Session>): Session => {
  return {
    id: 'mock-session-1',
    project_id: 'mock-project-1',
    name: 'Mock Session',
    created_at: new Date().toISOString(),
    map_data_url: '/mock/map.obj',
    ...overrides,
  };
};

// Usage
const mockProject = createMockProject();
const customProject = createMockProject({ name: 'Custom' });
const projects = [
  createMockProject({ id: '1', name: 'Project 1' }),
  createMockProject({ id: '2', name: 'Project 2' }),
];
```

## Three.js Component Example

```tsx
// src/features/heatmap/HeatmapPoint.tsx
import { useMemo, useRef, useEffect } from 'react';
import * as THREE from 'three';

type HeatmapPointProps = {
  position: [number, number, number];
  intensity: number;
  color: string;
};

export const HeatmapPoint = ({ position, intensity, color }: HeatmapPointProps) => {
  const meshRef = useRef<THREE.Mesh>(null);

  // Memoize geometry to avoid recreation
  const geometry = useMemo(
    () => new THREE.SphereGeometry(0.5 * intensity, 16, 16),
    [intensity]
  );

  // Memoize material
  const material = useMemo(
    () => new THREE.MeshStandardMaterial({ color }),
    [color]
  );

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      geometry.dispose();
      material.dispose();
    };
  }, [geometry, material]);

  return (
    <mesh ref={meshRef} position={position}>
      <primitive object={geometry} attach="geometry" />
      <primitive object={material} attach="material" />
    </mesh>
  );
};
```

## Form with Validation Example

```tsx
// src/component/organisms/LoginForm.tsx
import styled from '@emotion/styled';
import { useState, useCallback, type FC, type FormEvent } from 'react';

import { FlexColumn } from '@src/component/atoms/Flex';
import { Button } from '@src/component/atoms/Button';
import { TextField } from '@src/component/molecules/TextField';
import { Text } from '@src/component/atoms/Text';
import { useSharedTheme } from '@src/hooks/useSharedTheme';

export type LoginFormProps = {
  className?: string;
  onSubmit: (email: string, password: string) => Promise<void>;
};

const validateEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

const Component: FC<LoginFormProps> = ({ className, onSubmit }) => {
  const { theme } = useSharedTheme();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = useCallback(
    async (e: FormEvent) => {
      e.preventDefault();
      setError(null);

      if (!validateEmail(email)) {
        setError('Please enter a valid email address');
        return;
      }

      if (password.length < 8) {
        setError('Password must be at least 8 characters');
        return;
      }

      setIsLoading(true);
      try {
        await onSubmit(email, password);
      } catch (err) {
        setError('Login failed. Please try again.');
      } finally {
        setIsLoading(false);
      }
    },
    [email, password, onSubmit]
  );

  return (
    <form className={className} onSubmit={handleSubmit}>
      <FlexColumn gap={16}>
        <TextField
          label="Email"
          type="email"
          value={email}
          onChange={setEmail}
          placeholder="user@example.com"
        />
        <TextField
          label="Password"
          type="password"
          value={password}
          onChange={setPassword}
          placeholder="Enter password"
        />
        {error && (
          <Text
            text={error}
            color={theme.colors.semantic.error.main}
            fontSize={theme.typography.fontSize.sm}
          />
        )}
        <Button
          type="submit"
          scheme="primary"
          width="full"
          disabled={isLoading}
        >
          {isLoading ? 'Logging in...' : 'Login'}
        </Button>
      </FlexColumn>
    </form>
  );
};

export const LoginForm = styled(Component)`
  max-width: 400px;
  padding: ${({ theme }) => theme.spacing.xl};
  background: ${({ theme }) => theme.colors.surface.base};
  border-radius: ${({ theme }) => theme.borders.radius.lg};
`;
```

## QA Checklist

Before submitting a PR with UI changes, verify:

### Styling
- [ ] All styling uses Emotion styled components
- [ ] Theme tokens used (no hardcoded values)
- [ ] `useSharedTheme()` hook used
- [ ] Z-index uses predefined values

### Component Structure
- [ ] Component follows atomic design
- [ ] Props include `className?: string`
- [ ] TypeScript types properly defined
- [ ] Storybook story created (if new component)

### React Patterns
- [ ] No overuse of useEffect
- [ ] No redundant state
- [ ] useMemo/useCallback used appropriately
- [ ] Lists have stable unique keys

### TypeScript
- [ ] No `any` types
- [ ] Generated API types used
- [ ] Return types explicitly defined

### Security
- [ ] No `dangerouslySetInnerHTML`
- [ ] User input validated
- [ ] API errors checked
