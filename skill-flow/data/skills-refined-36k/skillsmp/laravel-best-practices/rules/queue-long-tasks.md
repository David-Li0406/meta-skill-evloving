---
title: Queue Long-Running Tasks
impact: MEDIUM
impactDescription: Prevents request timeouts and improves UX
tags: queues, jobs, background, async
---

## Queue Long-Running Tasks

Long operations in HTTP requests cause timeouts and poor UX. Queue them for background processing.

**Incorrect (blocking request):**

```php
<?php

class ReportController extends Controller
{
    public function generate(Request $request)
    {
        // ❌ User waits 30+ seconds
        $data = $this->analyzeMillionsOfRecords();
        $pdf = $this->generatePdfReport($data);
        $this->sendEmailWithAttachment($user, $pdf);

        return response()->download($pdf);
    }
}
```

**Correct (queue background job):**

```php
<?php

// Controller - dispatch and respond immediately
class ReportController extends Controller
{
    public function generate(Request $request)
    {
        GenerateReportJob::dispatch(
            $request->user(),
            $request->validated()
        );

        return response()->json([
            'message' => 'Report generation started. You will receive an email when ready.',
        ], 202);
    }
}

// Job - runs in background
class GenerateReportJob implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public function __construct(
        public User $user,
        public array $params
    ) {}

    public function handle(ReportService $reports): void
    {
        $data = $reports->analyze($this->params);
        $pdf = $reports->generatePdf($data);

        // Store for download
        Storage::put("reports/{$this->user->id}/report.pdf", $pdf);

        // Notify user
        $this->user->notify(new ReportReadyNotification($pdf));
    }

    public function failed(\Throwable $exception): void
    {
        $this->user->notify(new ReportFailedNotification($exception->getMessage()));
    }
}
```

**Job configuration:**

```php
<?php

class ProcessLargeImport implements ShouldQueue
{
    // Retry configuration
    public int $tries = 3;
    public int $maxExceptions = 2;
    public array $backoff = [60, 300, 600]; // Seconds between retries

    // Timeout (seconds)
    public int $timeout = 600;

    // Queue and connection
    public string $queue = 'imports';
    public string $connection = 'redis';

    // Unique job (prevent duplicates)
    public function uniqueId(): string
    {
        return $this->import->id;
    }

    public function uniqueFor(): int
    {
        return 3600; // 1 hour uniqueness window
    }
}
```

**Batch processing:**

```php
<?php

// Dispatch multiple jobs as a batch
$batch = Bus::batch([
    new ProcessChunk($data[0]),
    new ProcessChunk($data[1]),
    new ProcessChunk($data[2]),
])
->then(fn () => /* all completed */)
->catch(fn () => /* one failed */)
->finally(fn () => /* cleanup */)
->dispatch();
```

Reference: [Queues](https://laravel.com/docs/queues)
