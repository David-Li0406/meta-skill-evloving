# Feature Flags - Implementation Patterns

Implementation patterns for feature flags.

## Pattern: Use Feature Gates

Control feature visibility.

✅ **Good:**
\`\`\`typescript
const { value: isEnabled } = useGate('new_checkout');

return isEnabled ? <NewCheckout /> : <OldCheckout />;
\`\`\`

❌ **Bad:**
\`\`\`typescript
const isEnabled = process.env.NEW_CHECKOUT === 'true';
\`\`\`

**Why:** Feature gates:
- Dynamic control
- No deployments
- Gradual rollout
- Easy rollback

## Pattern: Use Dynamic Configs

Configure features remotely.

✅ **Good:**
\`\`\`typescript
const config = useDynamicConfig('ui_config');
const maxItems = config.get('max_items', 10);
\`\`\`

**Why:** Dynamic configs:
- Remote configuration
- No deployments
- Easy adjustments
- A/B testing

## Pattern: Test Both States

Test feature enabled and disabled.

✅ **Good:**
\`\`\`typescript
it('renders new feature when enabled', () => {
  mockGate.mockReturnValue({ value: true });
  render(<Component />);
  expect(screen.getByText('New Feature')).toBeInTheDocument();
});

it('renders old feature when disabled', () => {
  mockGate.mockReturnValue({ value: false });
  render(<Component />);
  expect(screen.getByText('Old Feature')).toBeInTheDocument();
});
\`\`\`

**Why:** Test both:
- Ensure both paths work
- Prevent regressions
- Confidence in rollout

## Pattern: Provide Fallback Values

Always provide defaults.

✅ **Good:**
\`\`\`typescript
const maxItems = config.get('max_items', 10); // Fallback: 10
\`\`\`

❌ **Bad:**
\`\`\`typescript
const maxItems = config.get('max_items'); // No fallback
\`\`\`

**Why:** Fallbacks:
- Prevents crashes
- Predictable behavior
- Safe defaults

## Summary

**Key Patterns:**
- Use feature gates
- Dynamic configs
- Test both states
- Provide fallbacks
- Clean up old flags

**Anti-Patterns:**
- Hardcoded flags
- No testing
- Missing fallbacks
- Never removing flags
