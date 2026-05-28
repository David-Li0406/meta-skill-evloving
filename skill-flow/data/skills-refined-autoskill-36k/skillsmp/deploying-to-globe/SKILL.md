---
name: deploying-to-globe
description: Deploys Dart and Flutter applications to Globe.dev serverless platform. Use when deploying apps, configuring globe.yaml, Globe KV, Globe DB, Globe AI, cron jobs, custom domains, environment variables, or troubleshooting Globe errors.
---

# Globe Deployment Skill

Globe is a serverless deployment platform for Dart and Flutter applications. Apps compile to x86_64 native executables and deploy to 300+ edge locations with automatic scaling.

## Critical Requirements

All Globe server apps MUST:

1. **Listen on `PORT` environment variable** (not hardcoded):

```dart
final port = int.parse(Platform.environment['PORT'] ?? '8080');
```

2. **Be stateless** — no local file persistence between requests

3. **Compile FFI to x86_64** if using native code

## CLI Quick Reference

```bash
# Install
dart pub global activate globe_cli

# Auth
globe login
globe logout

# Project Management
globe link              # Link existing project
globe unlink            # Unlink project
globe create -t <tpl>   # New project from template

# Deploy
globe deploy            # Preview deployment
globe deploy --prod     # Production deployment
globe build-logs        # Stream build logs

# Tokens (for CI/CD)
globe token create
globe token list
globe token delete
```

**Global flags:** `--help`, `--verbose`, `--token <t>`, `--project <id>`, `--org <id>`

## globe.yaml (Optional)

Globe auto-detects most project types. A `globe.yaml` is **required** for:

- **Cron jobs** — must be defined in config file
- **Static assets** — must be defined in config file

Other settings (preferred regions, build settings, etc.) can be configured via the dashboard instead.

**Example** (when needed):

```yaml
# yaml-language-server: $schema=https://globe.dev/globe.schema.json

entrypoint: bin/server.dart

build:
  preset:
    type: dart_frog # or: shelf, flutter, jaspr, serverpod

# These require globe.yaml:
assets:
  - public/

crons:
  - id: daily_cleanup
    schedule: "0 0 * * *"
    path: "/cron/cleanup"
```

**Validate** (if globe.yaml exists):

```bash
bash scripts/validate-globe-yaml.sh globe.yaml
```

## Build Presets

| Preset           | Use Case                              |
| ---------------- | ------------------------------------- |
| `dart_frog`      | File-based routing APIs               |
| `shelf`          | Flexible Dart servers (manual config) |
| `flutter`        | Flutter Web SPAs                      |
| `flutter_server` | Flutter with server-side rendering    |
| `jaspr`          | Jaspr SSR sites                       |
| `jaspr_static`   | Jaspr static site generation          |
| `serverpod`      | Full-stack Dart framework             |

## Common Code Patterns

### Shelf Hello World

```dart
import 'dart:io';
import 'package:shelf/shelf.dart';
import 'package:shelf/shelf_io.dart' as io;

void main() async {
  final port = int.parse(Platform.environment['PORT'] ?? '8080');
  final handler = const Pipeline()
      .addMiddleware(logRequests())
      .addHandler((req) => Response.ok('Hello from Globe!'));
  await io.serve(handler, InternetAddress.anyIPv4, port);
}
```

### Environment Variables

```dart
// User-defined secrets (set in Globe dashboard)
final apiKey = Platform.environment['API_KEY'];
final dbUrl = Platform.environment['DATABASE_URL'];

// Globe system variables (auto-set)
final isGlobe = Platform.environment['GLOBE'] == '1';
final buildEnv = Platform.environment['GLOBE_BUILD_ENV']; // 'preview' or 'production'
```

### Cron Job Handler

```dart
// Cron jobs POST to your path at scheduled times
app.post('/cron/daily', (Request req) async {
  final cronId = req.headers['x-globe-cron-id'];
  // Do work...
  return Response.ok('done'); // 2xx = success
});
```

### Globe KV (Key-Value Store)

```dart
import 'package:globe_kv/globe_kv.dart';

final kv = GlobeKV('namespace-id'); // Create namespace in dashboard first

await kv.set('key', 'value', ttl: 3600);  // TTL in seconds
final value = await kv.getString('key');
await kv.delete('key');
final keys = await kv.list(prefix: 'user:', limit: 100);
```

### Globe DB (SQLite)

```dart
import 'package:drift/drift.dart';
import 'package:drift/native.dart';
import 'package:sqlite3/sqlite3.dart';

// Connect to Globe DB (name from dashboard)
final db = NativeDatabase.opened(sqlite3.open('your-db-name.db'));
```

### Globe AI

```dart
import 'package:globe_ai/globe_ai.dart';

final result = await generateText(
  model: openai.chat('gpt-4o'),
  prompt: 'What is the capital of France?',
);
```

## globe.yaml Full Example

```yaml
# yaml-language-server: $schema=https://globe.dev/globe.schema.json

entrypoint: bin/server.dart

build:
  preset:
    type: dart_frog
    version: "2.0.0" # Optional: pin framework version
    buildCommand: "custom" # Optional: override build command
  build_runner:
    automatic_detection: true
    command: "dart run build_runner build" # Optional override
  melos:
    automatic_detection: true # For monorepos
    command: "melos bootstrap"
    version: "3.0.0"

assets:
  - public/
  - assets/images/

crons:
  - id: daily_cleanup # 1-50 chars, alphanumeric + underscores
    schedule: "0 0 * * *" # Cron expression (midnight UTC)
    path: "/cron/cleanup"

preferred_regions: # See full list below
  - us-east1
  - europe-west1
```

## Preferred Regions

Valid values for `preferred_regions`:

```
africa-south1, asia-east1, asia-east2, asia-northeast1, asia-northeast2,
asia-northeast3, asia-south1, asia-south2, asia-southeast1, asia-southeast2,
australia-southeast1, australia-southeast2, europe-central2, europe-north1,
europe-southwest1, europe-west1, europe-west2, europe-west3, europe-west4,
europe-west6, europe-west8, europe-west9, europe-west10, europe-west12,
me-central1, me-central2, me-west1, northamerica-northeast1, northamerica-northeast2,
northamerica-south1, southamerica-east1, southamerica-west1, us-central1,
us-east1, us-east4, us-east5, us-south1, us-west1, us-west2, us-west4
```

## System Environment Variables

| Variable          | Description                     |
| ----------------- | ------------------------------- |
| `PORT`            | Port your server must listen on |
| `GLOBE`           | `"1"` when running on Globe     |
| `GLOBE_BUILD_ENV` | `"1"` during build phase        |
| `HOSTNAME`        | Container hostname              |
| `CRON_ID`         | Cron job ID (if cron-triggered) |
| `CRON_SCHEDULE`   | Cron schedule expression        |

## Globe Request Headers

Globe adds these headers to incoming requests:

- `x-globe-country` — ISO country code
- `x-globe-city` — City name
- `x-globe-region` — Region/state
- `x-globe-latitude` / `x-globe-longitude` — Coordinates
- `x-globe-timezone` — IANA timezone
- `x-globe-temperature` — `cold`, `warm`, or `hot` (container state)

## Resource Limits

| Resource          | Limit                         |
| ----------------- | ----------------------------- |
| Requests          | 50K/month                     |
| Compute Bandwidth | 1GB/month                     |
| Asset Bandwidth   | 1GB/month                     |
| Memory            | 256MB/container               |
| Execution Time    | 30 seconds/request            |
| Databases         | 2 active                      |
| Cron Jobs         | 1 job (unlimited invocations) |

## Error Quick Fixes

| Error              | Cause                     | Fix                                              |
| ------------------ | ------------------------- | ------------------------------------------------ |
| 413                | Archive >100MB            | Add large files to `.gitignore`                  |
| 503 on deploy      | Build failed              | Check `globe build-logs`                         |
| Cold start slow    | First request initializes | Use `preferred_regions` in globe.yaml            |
| CORS errors        | Missing headers           | Add CORS middleware                              |
| Domain not working | DNS not propagated        | Wait 24h, verify CNAME to `domains.globeapp.dev` |

## Reference Documentation

Load the appropriate reference file based on user intent. For topics not listed, explore the `references/` folder.

### Getting Started

| Topic                       | File                                                                                                                     |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Installation & first deploy | [references/getting-started/index.mdx](references/getting-started/index.mdx)                                             |
| Quickstart guide            | [references/getting-started/quickstart.mdx](references/getting-started/quickstart.mdx)                                   |
| GitHub auto-deploy          | [references/getting-started/environment-setup/github.mdx](references/getting-started/environment-setup/github.mdx)       |
| CLI installation            | [references/getting-started/environment-setup/globe-cli.mdx](references/getting-started/environment-setup/globe-cli.mdx) |

### Core Concepts

| Topic                    | File                                                                                                     |
| ------------------------ | -------------------------------------------------------------------------------------------------------- |
| globe.yaml configuration | [references/core-concepts/globe-yaml.mdx](references/core-concepts/globe-yaml.mdx)                       |
| Build settings           | [references/core-concepts/build-settings.mdx](references/core-concepts/build-settings.mdx)               |
| Environment variables    | [references/core-concepts/environment-variables.mdx](references/core-concepts/environment-variables.mdx) |
| Custom domains           | [references/core-concepts/domains.mdx](references/core-concepts/domains.mdx)                             |
| Cron jobs                | [references/core-concepts/cron-jobs.mdx](references/core-concepts/cron-jobs.mdx)                         |
| Static assets            | [references/core-concepts/static-assets.mdx](references/core-concepts/static-assets.mdx)                 |
| Deployments              | [references/core-concepts/deployments.mdx](references/core-concepts/deployments.mdx)                     |
| GitHub integration       | [references/core-concepts/github-integration.mdx](references/core-concepts/github-integration.mdx)       |
| Logs                     | [references/core-concepts/logs.mdx](references/core-concepts/logs.mdx)                                   |
| Usage & billing          | [references/core-concepts/usage.mdx](references/core-concepts/usage.mdx)                                 |

### CLI Commands

| Command        | File                                                                                                               |
| -------------- | ------------------------------------------------------------------------------------------------------------------ |
| CLI overview   | [references/core-concepts/cli/index.mdx](references/core-concepts/cli/index.mdx)                                   |
| Create project | [references/core-concepts/cli/creating-a-new-project.mdx](references/core-concepts/cli/creating-a-new-project.mdx) |
| Deploy         | [references/core-concepts/cli/deploying-a-project.mdx](references/core-concepts/cli/deploying-a-project.mdx)       |
| Login/logout   | [references/core-concepts/cli/login-and-logout.mdx](references/core-concepts/cli/login-and-logout.mdx)             |
| Link/unlink    | [references/core-concepts/cli/link-and-unlink.mdx](references/core-concepts/cli/link-and-unlink.mdx)               |
| Tokens         | [references/core-concepts/cli/managing-tokens.mdx](references/core-concepts/cli/managing-tokens.mdx)               |
| Build logs     | [references/core-concepts/cli/viewing-build-logs.mdx](references/core-concepts/cli/viewing-build-logs.mdx)         |
| Update CLI     | [references/core-concepts/cli/updating-the-cli.mdx](references/core-concepts/cli/updating-the-cli.mdx)             |

### Frameworks

| Framework   | File                                                                             |
| ----------- | -------------------------------------------------------------------------------- |
| Overview    | [references/frameworks/index.mdx](references/frameworks/index.mdx)               |
| Dart Frog   | [references/frameworks/dart-frog.mdx](references/frameworks/dart-frog.mdx)       |
| Shelf       | [references/frameworks/shelf-server.mdx](references/frameworks/shelf-server.mdx) |
| Flutter Web | [references/frameworks/flutter-web.mdx](references/frameworks/flutter-web.mdx)   |
| Jaspr       | [references/frameworks/jaspr.mdx](references/frameworks/jaspr.mdx)               |
| Serverpod   | [references/frameworks/serverpod.mdx](references/frameworks/serverpod.mdx)       |
| Monorepos   | [references/frameworks/monorepos.mdx](references/frameworks/monorepos.mdx)       |

### Products

| Product             | File                                                                                                         |
| ------------------- | ------------------------------------------------------------------------------------------------------------ |
| Globe KV            | [references/products/index.mdx](references/products/index.mdx)                                               |
| Globe DB overview   | [references/products/database/index.mdx](references/products/database/index.mdx)                             |
| Globe DB quickstart | [references/products/database/quickstart.mdx](references/products/database/quickstart.mdx)                   |
| Globe DB management | [references/products/database/database-management.mdx](references/products/database/database-management.mdx) |
| Globe AI            | [references/products/ai.mdx](references/products/ai.mdx)                                                     |

### Infrastructure

| Topic             | File                                                                                                                                     |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Overview          | [references/infrastructure/overview/index.mdx](references/infrastructure/overview/index.mdx)                                             |
| Cold starts       | [references/infrastructure/overview/cold-starts.mdx](references/infrastructure/overview/cold-starts.mdx)                                 |
| Resource limits   | [references/infrastructure/overview/resources-and-limits.mdx](references/infrastructure/overview/resources-and-limits.mdx)               |
| Compute regions   | [references/infrastructure/overview/compute-regions.mdx](references/infrastructure/overview/compute-regions.mdx)                         |
| Global CDN        | [references/infrastructure/overview/global-cdn.mdx](references/infrastructure/overview/global-cdn.mdx)                                   |
| Automatic caching | [references/infrastructure/overview/automatic-caching.mdx](references/infrastructure/overview/automatic-caching.mdx)                     |
| HTTP headers      | [references/infrastructure/overview/http-headers.mdx](references/infrastructure/overview/http-headers.mdx)                               |
| Using FFI         | [references/infrastructure/overview/using-ffi.mdx](references/infrastructure/overview/using-ffi.mdx)                                     |
| Performance       | [references/infrastructure/performance-and-security/performance.mdx](references/infrastructure/performance-and-security/performance.mdx) |
| Security          | [references/infrastructure/performance-and-security/security.mdx](references/infrastructure/performance-and-security/security.mdx)       |

### Guides

| Guide                  | File                                                                                             |
| ---------------------- | ------------------------------------------------------------------------------------------------ |
| Guides index           | [references/guides/index.mdx](references/guides/index.mdx)                                       |
| Add custom domain      | [references/guides/add-custom-domain.mdx](references/guides/add-custom-domain.mdx)               |
| Connect Flutter app    | [references/guides/connect-flutter-app.mdx](references/guides/connect-flutter-app.mdx)           |
| Dart Frog deployment   | [references/guides/dart-frog-deployment.mdx](references/guides/dart-frog-deployment.mdx)         |
| Shelf backend          | [references/guides/shelf-backend-globe.mdx](references/guides/shelf-backend-globe.mdx)           |
| Jaspr deployment       | [references/guides/jaspr-globe-deployment.mdx](references/guides/jaspr-globe-deployment.mdx)     |
| GitHub integration     | [references/guides/github-integration.mdx](references/guides/github-integration.mdx)             |
| Globe cron jobs        | [references/guides/globe-cron-jobs.mdx](references/guides/globe-cron-jobs.mdx)                   |
| Build notes app        | [references/guides/build-notes-app.mdx](references/guides/build-notes-app.mdx)                   |
| Cache with KV          | [references/guides/cache-github-api-with-kv.mdx](references/guides/cache-github-api-with-kv.mdx) |
| Handle file uploads    | [references/guides/handle-file-uploads.mdx](references/guides/handle-file-uploads.mdx)           |
| Secure Dart APIs       | [references/guides/secure-dart-apis.mdx](references/guides/secure-dart-apis.mdx)                 |
| Validate API requests  | [references/guides/validate-api-requests.mdx](references/guides/validate-api-requests.mdx)       |
| Sign in with Google    | [references/guides/sign-in-with-google.mdx](references/guides/sign-in-with-google.mdx)           |
| Sign in with GitHub    | [references/guides/sign-in-with-github.mdx](references/guides/sign-in-with-github.mdx)           |
| Sign in with Apple     | [references/guides/sign-in-with-apple.mdx](references/guides/sign-in-with-apple.mdx)             |
| Email verification     | [references/guides/auth-email-verification.mdx](references/guides/auth-email-verification.mdx)   |
| Use external service   | [references/guides/use-external-service.mdx](references/guides/use-external-service.mdx)         |
| Test Dart Frog backend | [references/guides/test-dart-frog-backend.mdx](references/guides/test-dart-frog-backend.mdx)     |

### Tutorials

| Tutorial                   | File                                                                                                       |
| -------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Tutorials index            | [references/tutorials/index.mdx](references/tutorials/index.mdx)                                           |
| What is CORS               | [references/tutorials/what-is-cors.mdx](references/tutorials/what-is-cors.mdx)                             |
| What is JWT                | [references/tutorials/what-is-jwt.mdx](references/tutorials/what-is-jwt.mdx)                               |
| What is OAuth              | [references/tutorials/what-is-oauth.mdx](references/tutorials/what-is-oauth.mdx)                           |
| What is middleware         | [references/tutorials/what-is-middleware.mdx](references/tutorials/what-is-middleware.mdx)                 |
| What is backend validation | [references/tutorials/what-is-backend-validation.mdx](references/tutorials/what-is-backend-validation.mdx) |
| What to store in Globe KV  | [references/tutorials/what-to-store-in-globe-kv.mdx](references/tutorials/what-to-store-in-globe-kv.mdx)   |
| Serverless file handling   | [references/tutorials/serverless-file-handling.mdx](references/tutorials/serverless-file-handling.mdx)     |

### Troubleshooting

| Issue                         | File                                                                                 |
| ----------------------------- | ------------------------------------------------------------------------------------ |
| Troubleshooting index         | [references/troubleshooting/index.mdx](references/troubleshooting/index.mdx)         |
| Error 413 (archive too large) | [references/troubleshooting/error-413.mdx](references/troubleshooting/error-413.mdx) |
| Domain issues                 | [references/troubleshooting/domains.mdx](references/troubleshooting/domains.mdx)     |

## Deployment Workflow

Copy this checklist and track progress:

```
Deployment Progress:
- [ ] Step 1: Verify PORT usage in code
- [ ] Step 2: Create globe.yaml (only if needed for crons/assets/regions)
- [ ] Step 3: Set environment variables in dashboard (if needed)
- [ ] Step 4: Run `globe deploy` for preview
- [ ] Step 5: Test preview URL
- [ ] Step 6: Run `globe deploy --prod` for production
- [ ] Step 7: Configure custom domain (if needed)
```

**Step 1**: Ensure server listens on `Platform.environment['PORT']`

**Step 2**: Create `globe.yaml` only if you need cron jobs or static assets. Globe auto-detects presets for most projects.

**Step 3**: Add secrets via Dashboard → Settings → Environment Variables

**Step 4**: Deploy preview: `globe deploy`

**Step 5**: Test the preview URL thoroughly

**Step 6**: Deploy production: `globe deploy --prod`

**Step 7**: Add custom domain via Dashboard → Domains → CNAME to `domains.globeapp.dev`

## Decision Tree

```
Deploying Dart/Flutter to Globe?
├── New project?
│   ├── Yes → globe create -t <template>
│   └── No → globe link
│
├── Framework?
│   ├── Dart Frog → preset: dart_frog (auto-detected)
│   ├── Shelf → preset: shelf
│   ├── Flutter Web → preset: flutter
│   └── Jaspr → preset: jaspr
│
├── Deployment type?
│   ├── Preview → globe deploy
│   └── Production → globe deploy --prod
│
├── Needs caching?
│   └── Globe KV → Create namespace in dashboard, use globe_kv package
│
├── Needs database?
│   └── Globe DB → Create in dashboard, use Drift with sqlite3
│
├── Needs AI?
│   └── Globe AI → Install globe_ai, configure model provider
│
├── Background jobs?
│   └── Add crons to globe.yaml, handler returns 2xx
│
├── Custom domain?
│   └── Dashboard → Domains → Add → CNAME to domains.globeapp.dev
│
└── CI/CD?
    ├── GitHub → Enable GitHub integration
    └── Other → globe token create
```
