# NestJS Scheduling Patterns

## Cron Jobs

```typescript
import { Injectable } from '@nestjs/common';
import { Cron, CronExpression, SchedulerRegistry } from '@nestjs/schedule';

@Injectable()
export class TasksService {
  constructor(private schedulerRegistry: SchedulerRegistry) {}

  // Every day at midnight
  @Cron('0 0 * * *')
  handleDailyCleanup() {
    console.log('Running daily cleanup');
  }

  // Every 5 minutes
  @Cron(CronExpression.EVERY_5_MINUTES)
  handleFrequentTask() {
    console.log('Running every 5 minutes');
  }

  // Dynamic cron job
  addCronJob(name: string, cronTime: string, callback: () => void) {
    const job = new CronJob(cronTime, callback);
    this.schedulerRegistry.addCronJob(name, job);
    job.start();
  }

  deleteCronJob(name: string) {
    this.schedulerRegistry.deleteCronJob(name);
  }
}
```

## Intervals and Timeouts

```typescript
import { Interval, Timeout } from '@nestjs/schedule';

@Injectable()
export class PollingService {
  @Interval(10000) // Every 10 seconds
  checkHealth() {
    console.log('Health check');
  }

  @Timeout(5000) // Run once after 5 seconds
  onApplicationReady() {
    console.log('Application warm-up complete');
  }
}
```

## Bull Queues

```typescript
// queue.module.ts
import { BullModule } from '@nestjs/bull';

@Module({
  imports: [
    BullModule.forRoot({
      redis: { host: 'localhost', port: 6379 },
    }),
    BullModule.registerQueue({ name: 'email' }),
  ],
})
export class QueueModule {}

// email.processor.ts
import { Processor, Process, OnQueueFailed } from '@nestjs/bull';
import { Job } from 'bull';

@Processor('email')
export class EmailProcessor {
  @Process()
  async sendEmail(job: Job<{ to: string; subject: string }>) {
    const { to, subject } = job.data;
    await this.mailer.send(to, subject);
  }

  @Process('welcome')
  async sendWelcome(job: Job) {
    // Named job processor
  }

  @OnQueueFailed()
  onFailed(job: Job, error: Error) {
    console.error(`Job ${job.id} failed:`, error.message);
  }
}

// Usage in service
@Injectable()
export class EmailService {
  constructor(@InjectQueue('email') private emailQueue: Queue) {}

  async queueEmail(to: string, subject: string) {
    await this.emailQueue.add({ to, subject }, {
      attempts: 3,
      backoff: { type: 'exponential', delay: 1000 },
    });
  }
}
```

## Distributed Locking

```typescript
import Redlock from 'redlock';

@Injectable()
export class DistributedTaskService {
  private redlock: Redlock;

  constructor(private redis: Redis) {
    this.redlock = new Redlock([redis]);
  }

  @Cron('0 * * * *')
  async runExclusiveTask() {
    try {
      const lock = await this.redlock.acquire(['task:hourly'], 30000);
      try {
        await this.doWork();
      } finally {
        await lock.release();
      }
    } catch (err) {
      // Another instance is running the task
    }
  }
}
```
