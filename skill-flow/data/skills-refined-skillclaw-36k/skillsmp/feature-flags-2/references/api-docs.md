# Feature Flags - API Reference

API reference for feature flag patterns with Statsig.

## Official Documentation

- **Statsig**: https://docs.statsig.com/client/jsClientSDK

## Statsig SDK

### Check Feature Gate

\`\`\`typescript
import { useGate } from '@statsig/react-bindings';

const MyComponent = () => {
  const { value: isEnabled } = useGate('new_feature');

  if (isEnabled) {
    return <NewFeature />;
  }

  return <OldFeature />;
};
\`\`\`

### Get Dynamic Config

\`\`\`typescript
import { useDynamicConfig } from '@statsig/react-bindings';

const MyComponent = () => {
  const config = useDynamicConfig('button_config');
  const buttonColor = config.get('color', 'blue');

  return <Button color={buttonColor}>Click</Button>;
};
\`\`\`

### Get Experiment

\`\`\`typescript
import { useExperiment } from '@statsig/react-bindings';

const MyComponent = () => {
  const experiment = useExperiment('button_test');
  const variant = experiment.get('variant', 'control');

  return variant === 'treatment' ? <NewButton /> : <OldButton />;
};
\`\`\`

## Best Practices

1. Use feature gates for on/off features
2. Use dynamic configs for configurable features
3. Use experiments for A/B tests
4. Clean up old feature flags
5. Test both enabled/disabled states
