# Event-Driven Architecture

## Event-Driven Architecture

### Message Queue Integration
```typescript
// Producer (sends message)
async function publishMessage(queue: string, data: any) {
  const transaction = Sentry.getCurrentHub().getScope()?.getTransaction();

  const message = {
    data,
    metadata: {
      sentryTrace: transaction?.toTraceparent(),
      baggage: Sentry.baggage.serializeBaggage(/*...*/),
      timestamp: Date.now(),
    },
  };

  await messageQueue.publish(queue, message);
}

// Consumer (processes message)
async function processMessage(message: Message) {
  const { data, metadata } = message;

  const transaction = Sentry.continueTrace(
    { sentryTrace: metadata.sentryTrace, baggage: metadata.baggage },
    (ctx) => Sentry.startTransaction({
      ...ctx,
      name: 'process-message',
      op: 'queue.process',
    })
  );

  Sentry.getCurrentHub().configureScope((scope) => {
    scope.setSpan(transaction);
    scope.setTag('queue', message.queue);
  });

  try {
    await handleMessage(data);
    transaction.setStatus('ok');
  } catch (error) {
    transaction.setStatus('internal_error');
    Sentry.captureException(error);
    throw error;
  } finally {
    transaction.finish();
  }
}
```