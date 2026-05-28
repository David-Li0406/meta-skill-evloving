# Test IDs - Production Examples

Real-world examples of test ID patterns from the web codebase using data-testid attributes.

## Example 1: Basic Test ID with Context

**File**: `app/unified-spaces/plans-sections/single-question-flow/components/steps/rte-number-of-people-step/NumberOfPeopleStep.tsx:119`

```typescript
import { Box } from '@/libs/zest';

{numberOfPeopleOptions.map((numberOfPeopleOption, index) => (
  <Box
    key={index}
    as="button"
    role="checkbox"
    data-testid={`goalsPlanNumberOfPeople-${numberOfPeopleOption}`}
    onClick={() => setSelectedNumberOfPeople(numberOfPeopleOption)}
    aria-checked={selectedNumberOfPeople === numberOfPeopleOption}
  >
    {numberOfPeopleOption}
  </Box>
))}
```

**Test:**
```typescript
// app/unified-spaces/plans-sections/single-question-flow/components/steps/rte-number-of-people-step/NumberOfPeopleStep.spec.tsx:68
import { render, screen } from '@testing-library/react';

it('renders options with correct test ids', async () => {
  renderComponent();

  let options = await screen.findAllByRole('checkbox');
  expect(options.length).toBe(3);

  expect(options[0]).toHaveAttribute(
    'data-testid',
    'goalsPlanNumberOfPeople-justMe'
  );
  expect(options[1]).toHaveAttribute(
    'data-testid',
    'goalsPlanNumberOfPeople-twoOfUs'
  );
  expect(options[2]).toHaveAttribute(
    'data-testid',
    'goalsPlanNumberOfPeople-groupFamily'
  );
});
```

**Key patterns:**
- Contextual prefix: `goalsPlanNumberOfPeople`
- Dynamic suffix from variable: `${numberOfPeopleOption}`
- Kebab-case naming convention
- Combines role queries with test ID assertions

## Example 2: Container with Base Test ID

**File**: `app/unified-spaces/plans-sections/single-question-flow/components/steps/rte-number-of-people-step/NumberOfPeopleStep.tsx:102`

```typescript
<Box
  data-test-id="goalsPlanNumberOfPeople"
  role="group"
  as="section"
>
  {numberOfPeopleOptions.map((numberOfPeopleOption, index) => (
    <Box
      key={index}
      data-testid={`goalsPlanNumberOfPeople-${numberOfPeopleOption}`}
    >
      {/* Option content */}
    </Box>
  ))}
</Box>
```

**Key patterns:**
- Parent container has base ID: `goalsPlanNumberOfPeople`
- Children have suffixed IDs: `goalsPlanNumberOfPeople-justMe`
- Hierarchical naming for related elements
- Note: Uses `data-test-id` (with hyphen) on container

## Example 3: Hierarchical Test IDs with Dots

**File**: `app/spaces/checkout/modules/single-page/CheckoutFooter.tsx:48`

```typescript
import { Button } from '@/libs/zest';

<Button.Primary
  id="upm-playground.btn.submit"
  data-test-id="upm-playground.btn.submit"
  disabled={isDisabled}
  type="submit"
  form={ADDRESS_FORM_ID}
  onClick={onClickButton}
  loading={isPlacingOrder}
>
  {CTALabel}
</Button.Primary>
```

**Key patterns:**
- Module prefix: `upm-playground`
- Element type: `btn`
- Action/purpose: `submit`
- Dot notation for hierarchy: `module.element.action`
- Uses both `id` and `data-test-id`

## Example 4: Indexed Test IDs in Lists

**File**: `app/features/freebie-in-helloshare-challenge-card-feature/components/CircularProgressIndicator/index.tsx:54`

```typescript
import { Box } from '@/libs/zest';

{stepsArray.map((_, index) => (
  <StepCircleDivider
    key={index}
    data-test-id={`step-circle-divider-${index}`}
    angle={(360 / numberOfSteps) * index}
  />
))}
```

**Test:**
```typescript
it('renders correct number of dividers', () => {
  render(<CircularProgressIndicator steps={5} currentStep={2} />);

  expect(screen.getByTestId('step-circle-divider-0')).toBeInTheDocument();
  expect(screen.getByTestId('step-circle-divider-1')).toBeInTheDocument();
  expect(screen.getByTestId('step-circle-divider-2')).toBeInTheDocument();
  expect(screen.getByTestId('step-circle-divider-3')).toBeInTheDocument();
  expect(screen.getByTestId('step-circle-divider-4')).toBeInTheDocument();
});
```

**Key patterns:**
- Descriptive name: `step-circle-divider`
- Zero-indexed: `${index}`
- Enables testing of list length
- Individual element targeting

## Example 5: State-Based Test IDs

**File**: `app/features/freebie-in-helloshare-challenge-card-feature/components/FIHCardTasks.tsx:46`

```typescript
<Box
  data-test-id={`step-container-step-${stepIndex}${
    isCompleted ? '-completed' : ''
  }`}
>
  {/* Step content */}
</Box>
```

**Generated IDs:**
```
step-container-step-0
step-container-step-1-completed
step-container-step-2
```

**Test:**
```typescript
it('marks completed steps with completed suffix', () => {
  render(<CardTasks steps={steps} completedSteps={[1]} />);

  expect(screen.getByTestId('step-container-step-0')).toBeInTheDocument();
  expect(screen.getByTestId('step-container-step-1-completed')).toBeInTheDocument();
  expect(screen.getByTestId('step-container-step-2')).toBeInTheDocument();
});
```

**Key patterns:**
- Base ID: `step-container-step-${stepIndex}`
- Conditional suffix: `-completed`
- Encodes state in test ID
- Enables state-specific testing

## Example 6: SVG and Icon Test IDs

**File**: `app/features/freebie-in-helloshare-challenge-card-feature/components/CircularProgressIndicator/index.tsx:38`

```typescript
<Svg viewBox={`0 0 ${externalRadius * 2} ${externalRadius * 2}`}>
  <Background
    data-test-id="radial-bg-circle"
    cx={externalRadius}
    cy={externalRadius}
    r={externalRadius}
    fill={theme.colors.neutral['200']}
  />
  <Progress
    data-test-id="radial-progress-circle"
    cx={externalRadius}
    cy={externalRadius}
    r={internalRadius}
    stroke={theme.colors.primary['600']}
    strokeDasharray={circumference}
    strokeDashoffset={offset}
  />
</Svg>
```

**Icon test IDs:**
```typescript
import { CheckmarkOutline16 } from '@/libs/zest-support/icons/generated/16';
import { BoxClosedOutline24 } from '@/libs/zest-support/icons/generated/24';

<CheckmarkOutline16 data-test-id="progress-checkmark" />
<BoxClosedOutline24 data-test-id="progress-box" />
```

**Test:**
```typescript
it('renders SVG elements', () => {
  render(<CircularProgressIndicator />);

  expect(screen.getByTestId('radial-bg-circle')).toBeInTheDocument();
  expect(screen.getByTestId('radial-progress-circle')).toBeInTheDocument();
});

it('shows checkmark when complete', () => {
  render(<CircularProgressIndicator currentStep={3} totalSteps={3} />);

  expect(screen.getByTestId('progress-checkmark')).toBeInTheDocument();
  expect(screen.queryByTestId('progress-box')).not.toBeInTheDocument();
});
```

**Key patterns:**
- Semantic names: `radial-bg-circle`, `radial-progress-circle`
- Icon identifiers: `progress-checkmark`, `progress-box`
- SVG elements can have test IDs
- Enables visual element testing

## Example 7: Form Element Test IDs

**File**: Production pattern for forms

```typescript
<form data-testid="login-form" onSubmit={handleSubmit}>
  <Box>
    <label htmlFor="email">Email</label>
    <input
      id="email"
      type="email"
      data-testid="email-input"
      value={email}
      onChange={(e) => setEmail(e.target.value)}
    />
  </Box>

  <Box>
    <label htmlFor="password">Password</label>
    <input
      id="password"
      type="password"
      data-testid="password-input"
      value={password}
      onChange={(e) => setPassword(e.target.value)}
    />
  </Box>

  <Button.Primary data-test-id="submit-button" type="submit">
    Submit
  </Button.Primary>
</form>
```

**Test:**
```typescript
import userEvent from '@testing-library/user-event';

it('submits login form', async () => {
  const handleSubmit = jest.fn();
  render(<LoginForm onSubmit={handleSubmit} />);

  const emailInput = screen.getByTestId('email-input');
  const passwordInput = screen.getByTestId('password-input');
  const submitButton = screen.getByTestId('submit-button');

  await userEvent.type(emailInput, 'user@example.com');
  await userEvent.type(passwordInput, 'password123');
  await userEvent.click(submitButton);

  expect(handleSubmit).toHaveBeenCalledWith({
    email: 'user@example.com',
    password: 'password123',
  });
});
```

**Key patterns:**
- Form container: `login-form`
- Input fields: `email-input`, `password-input`
- Submit button: `submit-button`
- Descriptive action-based names

## Example 8: Integration Test with Providers

**File**: `app/data-access/CONTRIBUTING.md:274`

```typescript
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';

const TestComponent: React.FC = () => {
  const { data } = useCustomerInfo({});

  return <div data-test-id="email">{data?.email}</div>;
};

it('renders customer email', async () => {
  const queryClient = new QueryClient();

  render(
    <QueryClientProvider client={queryClient}>
      <TestComponent />
    </QueryClientProvider>
  );

  const email = await screen.findByTestId('email');
  expect(email).toHaveTextContent('user@example.com');
});
```

**Key patterns:**
- Simple test ID: `email`
- Wraps with QueryClientProvider for React Query hooks
- Uses `findByTestId` for async data loading

## Example 9: User Interaction Test

**File**: `app/unified-spaces/plans-sections/single-question-flow/components/steps/rte-number-of-people-step/NumberOfPeopleStep.spec.tsx:68`

```typescript
import { render, screen, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

it('handles option selection', async () => {
  const onSelectionChange = jest.fn();
  renderComponent({ onSelectionChange });

  let options = await screen.findAllByRole('checkbox');

  // Click third option
  await act(async () => {
    userEvent.click(options[2]);
  });

  // Re-query after state update
  options = await screen.findAllByRole('checkbox');

  // Verify selection
  expect(options[2]).toHaveAttribute('aria-checked', 'true');
  expect(options[2]).toHaveAttribute(
    'data-testid',
    'goalsPlanNumberOfPeople-groupFamily'
  );

  // Verify callback
  expect(onSelectionChange).toHaveBeenCalledWith('groupFamily');
});
```

**Key patterns:**
- Find elements by role first
- Verify test IDs with `toHaveAttribute`
- Use `act` for state updates
- Re-query after interactions
- Check both ARIA and test IDs

## Example 10: Multiple Providers Pattern

**File**: `app/unified-spaces/plans-sections/single-question-flow/components/steps/rte-number-of-people-step/NumberOfPeopleStep.spec.tsx:26`

```typescript
import { QueryClient, QueryClientProvider } from 'react-query';
import { SystemCountryProvider, SystemCountry } from '@/libs/system-country';
import { ServerEnvProvider } from '@/libs/server-env';
import { LocalStorageProvider } from '@/libs/local-storage';

const renderComponent = () =>
  render(
    <QueryClientProvider client={new QueryClient()}>
      <ServerEnvProvider>
        <SystemCountryProvider systemCountry={SystemCountry.FJ}>
          <LocalStorageProvider>
            <SingleQuestionPageProvider>
              <QuestionnaireConfigProvider>
                <NumberOfPeopleProvider>
                  <NumberOfPeopleStep
                    onGoalsPlanRecommendationSelectionChange={onSelectionChange}
                  />
                </NumberOfPeopleProvider>
              </QuestionnaireConfigProvider>
            </SingleQuestionPageProvider>
          </LocalStorageProvider>
        </SystemCountryProvider>
      </ServerEnvProvider>
    </QueryClientProvider>
  );

it('renders with all providers', async () => {
  renderComponent();

  const container = await screen.findByTestId('goalsPlanNumberOfPeople');
  expect(container).toBeInTheDocument();

  const options = await screen.findAllByRole('checkbox');
  expect(options.length).toBe(3);
});
```

**Key patterns:**
- Create `renderComponent` helper
- Nest all required providers
- Component has access to all context
- Enables realistic integration testing

## Summary

**Common test ID patterns:**
- Context + entity: `goalsPlanNumberOfPeople`
- Context + entity + variant: `goalsPlanNumberOfPeople-justMe`
- Module + element + action: `upm-playground.btn.submit`
- Feature + component: `challenge-card-title`
- Indexed lists: `step-circle-divider-${index}`
- State-based: `step-container-step-${index}${isCompleted ? '-completed' : ''}`
- Semantic descriptive: `radial-progress-circle`, `progress-checkmark`

**Testing patterns:**
- Query by role first: `screen.findAllByRole('checkbox')`
- Verify test ID: `expect(element).toHaveAttribute('data-testid', '...')`
- Direct query: `screen.getByTestId('...')`
- User interactions: `await userEvent.click(element)`
- Async queries: `await screen.findByTestId('...')`
- Wrap with providers for realistic tests
