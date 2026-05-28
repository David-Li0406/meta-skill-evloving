# Testing After Upgrade

## Testing After Upgrade

```typescript
// test-upgrade.ts
import * as Sentry from '@sentry/node';

async function testUpgrade() {
  console.log('SDK Version:', Sentry.SDK_VERSION);

  // Test error capture
  try {
    throw new Error('Upgrade test error');
  } catch (e) {
    const eventId = Sentry.captureException(e);
    console.log('Error captured:', eventId);
  }

  // Test performance
  const transaction = Sentry.startTransaction({
    name: 'upgrade-test',
    op: 'test',
  });
  transaction.finish();
  console.log('Transaction created');

  // Test breadcrumbs
  Sentry.addBreadcrumb({
    category: 'test',
    message: 'Upgrade verification',
    level: 'info',
  });
  console.log('Breadcrumb added');

  console.log('Upgrade test complete!');
}

testUpgrade();
```