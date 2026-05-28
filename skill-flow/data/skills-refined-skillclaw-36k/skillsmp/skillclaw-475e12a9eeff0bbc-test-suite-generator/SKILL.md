---
name: test-suite-generator
description: Use this skill when you need to generate comprehensive test suites for components, hooks, and utilities, ensuring proper coverage and structure.
---

# Skill body

## When to Use
- Creating tests for new features
- Backfilling tests for existing code
- User invokes `/create-test-suite` command
- Need to add test coverage

## What This Skill Does
1. Analyzes code to determine test needs.
2. Generates test files in the proper location.
3. Creates test cases for:
   - Happy path
   - Edge cases
   - Error scenarios
4. Sets up mocks for dependencies.
5. Adds test utilities if needed.

## Test Types

### Unit Tests
For pure functions, calculations, utilities.

```typescript
import { calculateTSS } from './calculations';

describe('calculateTSS', () => {
  it('should calculate TSS correctly for 1 hour at FTP', () => {
    const result = calculateTSS({
      normalizedPower: 250,
      duration: 3600,
      ftp: 250,
    });
    expect(result).toBe(100);
  });

  it('should return 0 for zero duration', () => {
    const result = calculateTSS({
      normalizedPower: 250,
      duration: 0,
      ftp: 250,
    });
    expect(result).toBe(0);
  });

  it('should handle missing FTP', () => {
    const result = calculateTSS({
      normalizedPower: 250,
      duration: 3600,
      ftp: undefined,
    });
    expect(result).toBeNull();
  });

  it('should calculate higher TSS for harder efforts', () => {
    const easy = calculateTSS({ normalizedPower: 200, duration: 3600, ftp: 250 });
    const hard = calculateTSS({ normalizedPower: 300, duration: 3600, ftp: 250 });
    expect(hard).toBeGreaterThan(easy);
  });
});
```

### Hook Tests
For custom React hooks.

```typescript
import { renderHook, waitFor } from '@testing-library/react-native';
import { useActivityRecorder } from './useActivityRecorder';

describe('useActivityRecorder', () => {
  const mockProfile = {
    id: '1',
    ftp: 250,
    maxHeartRate: 190,
  };

  it('should initialize service with profile', () => {
    const { result } = renderHook(() => useActivityRecorder(mockProfile));
    expect(result.current).toBeDefined();
    expect(result.current.getState()).toBe('pending');
  });

  it('should transition to ready state when sensors connected', async () => {
    const { result } = renderHook(() => useActivityRecorder(mockProfile));

    result.current.connectSensor('heartRate', mockSensor);

    await waitFor(() => {
      expect(result.current.getState()).toBe('ready');
    });
  });
});
```

### Component Tests
For React components.

```typescript
import { render, screen, fireEvent } from '@testing-library/react-native';
import { ActivityCard } from './ActivityCard';
import type { Activity } from '@repo/core';

describe('ActivityCard', () => {
  const mockActivity: Activity = {
    id: '1',
    name: 'Morning Run',
    type: 'run',
    distance: 5000,
    duration: 1800,
    startTime: new Date(),
  };

  it('renders activity name and stats', () => {
    render(<ActivityCard activity={mockActivity} />);

    expect(screen.getByText('Morning Run')).toBeTruthy();
    expect(screen.getByText('5.00 km')).toBeTruthy();
    expect(screen.getByText('30:00')).toBeTruthy();
  });

  it('calls onPress when pressed', () => {
    const onPress = jest.fn();
    render(<ActivityCard activity={mockActivity} onPress={onPress} />);

    fireEvent.press(screen.getByRole('button'));
    expect(onPress).toHaveBeenCalledWith('1');
  });
});
```