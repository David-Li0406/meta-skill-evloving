# NestJS Queue Reference (BullMQ)

## Setup

```bash
bun add @nestjs/bullmq bullmq
```

```typescript
// app.module.ts
@Module({
  imports: [
    BullModule.forRootAsync({
      imports: [ConfigModule],
      useFactory: (config: ConfigService) => ({
        connection: {
          host: config.get('REDIS_HOST', 'localhost'),
          port: config.get('REDIS_PORT', 6379),
          password: config.get('REDIS_PASSWORD'),
        },
        defaultJobOptions: {
          attempts: 3,
          backoff: {
            type: 'exponential',
            delay: 1000,
          },
          removeOnComplete: 100,
          removeOnFail: 500,
        },
      }),
      inject: [ConfigService],
    }),
  ],
})
export class AppModule {}
```

## Queue Definition

```typescript
// email.queue.ts
export const EMAIL_QUEUE = 'email';

export interface EmailJobData {
  to: string;
  subject: string;
  template: string;
  context: Record<string, unknown>;
}

export interface EmailJobResult {
  messageId: string;
  accepted: string[];
}

// Register queue in module
@Module({
  imports: [
    BullModule.registerQueue({
      name: EMAIL_QUEUE,
      defaultJobOptions: {
        attempts: 5,
        backoff: {
          type: 'exponential',
          delay: 2000,
        },
      },
    }),
  ],
  providers: [EmailProcessor, EmailService],
  exports: [EmailService],
})
export class EmailModule {}
```

## Processor (Consumer)

```typescript
// email.processor.ts
@Processor(EMAIL_QUEUE)
export class EmailProcessor extends WorkerHost {
  private readonly logger = new Logger(EmailProcessor.name);

  constructor(
    private readonly mailerService: MailerService,
    private readonly templateService: TemplateService,
  ) {
    super();
  }

  async process(job: Job<EmailJobData>): Promise<EmailJobResult> {
    this.logger.log(`Processing email job ${job.id} to ${job.data.to}`);

    const { to, subject, template, context } = job.data;

    // Render template
    const html = await this.templateService.render(template, context);

    // Update progress
    await job.updateProgress(50);

    // Send email
    const result = await this.mailerService.sendMail({
      to,
      subject,
      html,
    });

    await job.updateProgress(100);

    this.logger.log(`Email sent successfully: ${result.messageId}`);

    return {
      messageId: result.messageId,
      accepted: result.accepted as string[],
    };
  }

  @OnWorkerEvent('completed')
  onCompleted(job: Job<EmailJobData>) {
    this.logger.log(`Job ${job.id} completed`);
  }

  @OnWorkerEvent('failed')
  onFailed(job: Job<EmailJobData>, error: Error) {
    this.logger.error(`Job ${job.id} failed: ${error.message}`, error.stack);
  }

  @OnWorkerEvent('stalled')
  onStalled(jobId: string) {
    this.logger.warn(`Job ${jobId} stalled`);
  }
}
```

## Producer (Enqueuing Jobs)

```typescript
// email.service.ts
@Injectable()
export class EmailService {
  constructor(
    @InjectQueue(EMAIL_QUEUE)
    private readonly emailQueue: Queue<EmailJobData>,
  ) {}

  async sendWelcomeEmail(user: User): Promise<Job<EmailJobData>> {
    return this.emailQueue.add('welcome', {
      to: user.email,
      subject: 'Welcome to our platform!',
      template: 'welcome',
      context: { name: user.name },
    });
  }

  async sendPasswordReset(email: string, token: string): Promise<Job<EmailJobData>> {
    return this.emailQueue.add(
      'password-reset',
      {
        to: email,
        subject: 'Password Reset Request',
        template: 'password-reset',
        context: { token, expiresIn: '1 hour' },
      },
      {
        priority: 1, // Higher priority
        attempts: 3,
      },
    );
  }

  async sendBulkEmails(emails: EmailJobData[]): Promise<Job<EmailJobData>[]> {
    const jobs = emails.map((data) => ({
      name: 'bulk',
      data,
      opts: { priority: 10 }, // Lower priority for bulk
    }));

    return this.emailQueue.addBulk(jobs);
  }

  // Delayed job
  async scheduleReminder(user: User, delayMs: number): Promise<Job<EmailJobData>> {
    return this.emailQueue.add(
      'reminder',
      {
        to: user.email,
        subject: 'Reminder',
        template: 'reminder',
        context: { name: user.name },
      },
      {
        delay: delayMs,
      },
    );
  }

  // Recurring job (cron)
  async setupDailyDigest(): Promise<void> {
    await this.emailQueue.add(
      'daily-digest',
      { template: 'digest' } as EmailJobData,
      {
        repeat: {
          pattern: '0 9 * * *', // Every day at 9 AM
          tz: 'America/New_York',
        },
      },
    );
  }
}
```

## Advanced Patterns

### Job Batching

```typescript
@Injectable()
export class BatchProcessor {
  constructor(
    @InjectQueue('reports')
    private readonly reportQueue: Queue,
  ) {}

  async processLargeDataset(datasetId: string, totalItems: number): Promise<void> {
    const batchSize = 100;
    const batches = Math.ceil(totalItems / batchSize);

    // Create parent job
    const parentJob = await this.reportQueue.add('process-dataset', {
      datasetId,
      totalItems,
    });

    // Create child jobs
    for (let i = 0; i < batches; i++) {
      await this.reportQueue.add(
        'process-batch',
        {
          datasetId,
          offset: i * batchSize,
          limit: batchSize,
          parentJobId: parentJob.id,
        },
        {
          parent: {
            id: parentJob.id!,
            queue: 'reports',
          },
        },
      );
    }
  }
}
```

### Rate Limiting

```typescript
@Module({
  imports: [
    BullModule.registerQueue({
      name: 'api-calls',
      limiter: {
        max: 100,        // Max 100 jobs
        duration: 60000, // Per minute
      },
    }),
  ],
})
export class ApiModule {}
```

### Priority Queues

```typescript
// Define priority levels
export enum JobPriority {
  CRITICAL = 1,
  HIGH = 2,
  NORMAL = 5,
  LOW = 10,
}

// Use when adding jobs
await this.queue.add('urgent-task', data, {
  priority: JobPriority.CRITICAL,
});

await this.queue.add('background-task', data, {
  priority: JobPriority.LOW,
});
```

### Job Dependencies (Flows)

```typescript
import { FlowProducer } from 'bullmq';

@Injectable()
export class OrderFlowService {
  private flowProducer: FlowProducer;

  constructor() {
    this.flowProducer = new FlowProducer({
      connection: { host: 'localhost', port: 6379 },
    });
  }

  async createOrderFlow(orderId: string): Promise<void> {
    await this.flowProducer.add({
      name: 'complete-order',
      queueName: 'orders',
      data: { orderId },
      children: [
        {
          name: 'process-payment',
          queueName: 'payments',
          data: { orderId },
        },
        {
          name: 'reserve-inventory',
          queueName: 'inventory',
          data: { orderId },
        },
        {
          name: 'send-confirmation',
          queueName: 'notifications',
          data: { orderId },
          children: [
            {
              name: 'generate-invoice',
              queueName: 'invoices',
              data: { orderId },
            },
          ],
        },
      ],
    });
  }
}
```

## Monitoring & Health

```typescript
// Queue health check
@Injectable()
export class QueueHealthIndicator extends HealthIndicator {
  constructor(
    @InjectQueue(EMAIL_QUEUE)
    private readonly emailQueue: Queue,
  ) {
    super();
  }

  async isHealthy(key: string): Promise<HealthIndicatorResult> {
    try {
      const client = await this.emailQueue.client;
      await client.ping();

      const [waiting, active, failed] = await Promise.all([
        this.emailQueue.getWaitingCount(),
        this.emailQueue.getActiveCount(),
        this.emailQueue.getFailedCount(),
      ]);

      return this.getStatus(key, true, {
        waiting,
        active,
        failed,
      });
    } catch (error) {
      return this.getStatus(key, false, { error: error.message });
    }
  }
}

// Metrics endpoint
@Controller('admin/queues')
@UseGuards(AdminGuard)
export class QueueAdminController {
  constructor(
    @InjectQueue(EMAIL_QUEUE)
    private readonly emailQueue: Queue,
  ) {}

  @Get('stats')
  async getStats() {
    const [waiting, active, completed, failed, delayed] = await Promise.all([
      this.emailQueue.getWaitingCount(),
      this.emailQueue.getActiveCount(),
      this.emailQueue.getCompletedCount(),
      this.emailQueue.getFailedCount(),
      this.emailQueue.getDelayedCount(),
    ]);

    return { waiting, active, completed, failed, delayed };
  }

  @Post('retry-failed')
  async retryFailed() {
    const failed = await this.emailQueue.getFailed(0, 100);
    await Promise.all(failed.map((job) => job.retry()));
    return { retried: failed.length };
  }

  @Delete('clean')
  async clean() {
    await this.emailQueue.clean(24 * 60 * 60 * 1000, 100, 'completed');
    await this.emailQueue.clean(7 * 24 * 60 * 60 * 1000, 100, 'failed');
    return { cleaned: true };
  }
}
```

## Testing Queues

```typescript
describe('EmailProcessor', () => {
  let processor: EmailProcessor;
  let mailerService: MockType<MailerService>;

  beforeEach(async () => {
    const module = await Test.createTestingModule({
      providers: [
        EmailProcessor,
        {
          provide: MailerService,
          useFactory: () => ({
            sendMail: jest.fn().mockResolvedValue({ messageId: 'test-id' }),
          }),
        },
      ],
    }).compile();

    processor = module.get(EmailProcessor);
    mailerService = module.get(MailerService);
  });

  it('should process email job', async () => {
    const job = {
      id: '1',
      data: {
        to: 'test@example.com',
        subject: 'Test',
        template: 'welcome',
        context: {},
      },
      updateProgress: jest.fn(),
    } as unknown as Job<EmailJobData>;

    const result = await processor.process(job);

    expect(result.messageId).toBe('test-id');
    expect(mailerService.sendMail).toHaveBeenCalledWith(
      expect.objectContaining({ to: 'test@example.com' }),
    );
  });
});
```
