# Technology Identification RAG Database

This directory contains pattern definitions for detecting technologies in codebases using a tiered detection architecture optimized for both speed and accuracy.

## Overview

- **119 technologies** across 20+ categories
- **Markdown-based patterns** for easy reading and editing
- **Tiered detection** for quick SBOM scans vs deep file analysis
- **Evidence tracking** for all detections

## Detection Tiers

The detection system uses three tiers optimized for different use cases:

### Tier 1: Quick Detection (SBOM-based)
- **Speed**: Fast (~5-10 seconds)
- **Method**: Analyzes SBOM package lists from cdxgen
- **Data**: Package names from npm, pypi, go, maven, rubygems, etc.
- **Use case**: Quick scans, CI/CD pipelines, bulk organization analysis

### Tier 2: Deep Detection (File-based)
- **Speed**: Slower (~30-60 seconds depending on repo size)
- **Method**: Scans all files in repository
- **Data**: Import statements, code patterns, file extensions, config files
- **Use case**: Detailed analysis, security reviews, full technology inventory

### Tier 3: Configuration Extraction (Value Extraction)
- **Speed**: Runs alongside Tier 2
- **Method**: Parses DevOps configuration files to extract values
- **Data**: Container registries, cloud account IDs, service endpoints, cluster names
- **Use case**: Infrastructure inventory, security posture, dependency mapping

## Categories

| Category | Technologies | Description |
|----------|-------------|-------------|
| `languages` | Python, JavaScript, TypeScript, Go, Rust, Java, C#, Ruby, PHP, Kotlin, Swift, Scala, Elixir, Clojure, Haskell, Nim | Programming languages |
| `ai-ml/apis` | OpenAI, Anthropic, Cohere, Google AI, AI21, Mistral, Perplexity, Replicate, Together-AI | AI/ML API providers |
| `ai-ml/vectordb` | Pinecone, Weaviate, Qdrant, ChromaDB | Vector databases for embeddings |
| `ai-ml/mlops` | Hugging Face, Weights & Biases | ML operations platforms |
| `ai-ml/frameworks` | LangChain, TensorFlow, PyTorch | AI/ML frameworks |
| `authentication` | Auth0, Okta, AWS Cognito | Authentication providers |
| `cloud-providers` | AWS, GCP, Azure, Cloudflare | Cloud infrastructure |
| `databases` | PostgreSQL, MongoDB, Redis, MySQL, Elasticsearch, DynamoDB, Supabase, SQLite | Database systems |
| `messaging` | Kafka, RabbitMQ, SQS | Message queues |
| `monitoring` | Datadog, Sentry, New Relic | Observability platforms |
| `business-tools/payment` | Stripe, PayPal, Square, Braintree | Payment processors |
| `business-tools/email` | SendGrid, Mailgun, Resend, Postmark | Email services |
| `business-tools/analytics` | Segment, Mixpanel, Amplitude, PostHog | Analytics platforms |
| `business-tools/cms` | Contentful, Sanity, Strapi, Prismic | Content management |
| `developer-tools/testing` | Jest, Pytest, Cypress, Playwright, Vitest, Mocha | Testing frameworks |
| `developer-tools/cicd` | GitHub Actions, GitLab CI, CircleCI, Jenkins | CI/CD platforms |
| `developer-tools/feature-flags` | LaunchDarkly, Unleash, Flagsmith, GrowthBook | Feature flag services |
| `developer-tools/containers` | Docker, Kubernetes | Container platforms |
| `developer-tools/infrastructure` | Terraform, Pulumi, Ansible, CloudFormation | Infrastructure as Code |
| `developer-tools/linting` | ESLint, Prettier, RuboCop, Pylint, golangci-lint | Code linters/formatters |
| `developer-tools/bundlers` | Webpack, Vite, Rollup, esbuild, Parcel | JavaScript bundlers |
| `web-frameworks/frontend` | React, Vue, Angular, Svelte, Next.js, Nuxt, Astro, Remix | Frontend frameworks |
| `web-frameworks/backend` | Express, FastAPI, Django, Flask, Rails, Spring Boot, Laravel, NestJS, Fastify, Phoenix, ASP.NET Core | Backend frameworks |
| `cryptographic-libraries` | OpenSSL | Cryptography |

## Pattern File Structure

Each technology has a `patterns.md` file organized by detection tier:

```
technology-name/
└── patterns.md    # All detection patterns in Markdown format
```

### Pattern File Format

```markdown
# Technology Name

**Category**: category/subcategory
**Description**: Brief description
**Homepage**: https://example.com

---

## TIER 1: Quick Detection (SBOM-based)

These patterns are used during quick scans that only analyze the SBOM.

### Package Detection

#### NPM
- `package-name`
- `@scope/package-name`

#### PYPI
- `python-package`

#### GO
- `github.com/org/package`

#### MAVEN
- `com.example:artifact-id`

#### RUBYGEMS
- `gem-name`

---

## TIER 2: Deep Detection (File-based)

These patterns require scanning repository files and take longer to run.

### File Extensions
*Presence of these extensions indicates the technology*

- `.ext` - Description
- `.ext2` - Description

### Configuration Files
*Known configuration files that indicate the technology*

- `config-file.json` - Description
- `*.config.js` - Glob pattern for config files
- `.technology-name/` - Configuration directory

### Import Patterns
*Code import statements that indicate usage*

#### JavaScript/TypeScript
Extensions: `.js`, `.jsx`, `.ts`, `.tsx`, `.mjs`

**Pattern**: `import\s+.*\s+from\s+['"]package-name['"]`
- ES6 import
- Example: `import foo from 'package-name';`

**Pattern**: `require\(['"]package-name['"]\)`
- CommonJS require
- Example: `const foo = require('package-name');`

#### Python
Extensions: `.py`

**Pattern**: `^import\s+package_name`
- Standard import
- Example: `import package_name`

**Pattern**: `^from\s+package_name\s+import`
- From import
- Example: `from package_name import module`

### Code Patterns
*Specific code patterns that indicate usage*

**Pattern**: `TechnologyClient\(`
- Client instantiation
- Example: `client = TechnologyClient(api_key='...')`

---

## Environment Variables

- `TECHNOLOGY_API_KEY`
- `TECHNOLOGY_SECRET`

## Detection Notes

- Important detection considerations
- Common usage patterns
- False positive mitigation

---

## TIER 3: Configuration Extraction

These patterns extract specific configuration values from DevOps files.

### Extraction Patterns

#### Container Registry
*Extract container registry URLs from Docker/Kubernetes configs*

**Files**: `Dockerfile`, `docker-compose.yml`, `*.yaml` (K8s)
**Pattern**: `^FROM\s+([a-z0-9.-]+(?::[0-9]+)?)/`
**Extracts**: `registry_url`
- Example: `FROM 123456789.dkr.ecr.us-east-1.amazonaws.com/myapp:latest`
- Result: `{"registry_url": "123456789.dkr.ecr.us-east-1.amazonaws.com", "type": "ecr"}`

**Pattern**: `image:\s*['"]?([a-z0-9.-]+(?::[0-9]+)?)/`
**Extracts**: `registry_url`
- Example: `image: gcr.io/my-project/app:v1`
- Result: `{"registry_url": "gcr.io/my-project", "type": "gcr"}`

#### AWS Account ID
*Extract AWS account IDs from various config files*

**Files**: `*.tf`, `*.yaml`, `*.yml`, `*.json`, `buildspec.yml`
**Pattern**: `(\d{12})\.dkr\.ecr\.`
**Extracts**: `aws_account_id`
- Example: `123456789012.dkr.ecr.us-west-2.amazonaws.com`
- Result: `{"aws_account_id": "123456789012"}`

**Pattern**: `arn:aws:[^:]+:[^:]*:(\d{12}):`
**Extracts**: `aws_account_id`
- Example: `arn:aws:iam::123456789012:role/MyRole`
- Result: `{"aws_account_id": "123456789012"}`

#### Kubernetes Cluster
*Extract cluster names and contexts*

**Files**: `kubeconfig`, `.kube/config`, `*.yaml`
**Pattern**: `cluster:\s*['"]?([a-z0-9-]+)`
**Extracts**: `cluster_name`

**Pattern**: `server:\s*['"]?(https?://[^'"\\s]+)`
**Extracts**: `cluster_endpoint`

### Extraction Output

```json
{
  "extractions": {
    "container_registries": [
      {
        "url": "123456789012.dkr.ecr.us-west-2.amazonaws.com",
        "type": "ecr",
        "source_file": "Dockerfile",
        "line": 1
      }
    ],
    "aws_accounts": [
      {
        "account_id": "123456789012",
        "source_file": "terraform/main.tf",
        "line": 15
      }
    ],
    "kubernetes_clusters": [
      {
        "name": "prod-cluster",
        "endpoint": "https://k8s.example.com",
        "source_file": ".kube/config"
      }
    ]
  }
}
```
```

## Evidence Tracking

All detections include evidence about where the technology was found:

```json
{
  "name": "React",
  "category": "web-frameworks/frontend",
  "confidence": 95,
  "detection_tier": 1,
  "detection_methods": ["package"],
  "evidence": [
    {
      "type": "package",
      "source": "package.json",
      "value": "react@18.2.0"
    }
  ]
}
```

For Tier 2 detections:

```json
{
  "name": "Terraform",
  "category": "developer-tools/infrastructure",
  "confidence": 95,
  "detection_tier": 2,
  "detection_methods": ["file-extension", "config-file"],
  "evidence": [
    {
      "type": "file-extension",
      "file": "main.tf",
      "line": null
    },
    {
      "type": "config-file",
      "file": ".terraform.lock.hcl",
      "line": null
    },
    {
      "type": "import",
      "file": "app/main.py",
      "line": 5,
      "content": "import terraform"
    }
  ]
}
```

## Confidence Scoring

Confidence scores are defined globally in `confidence-config.json` rather than per-pattern. This ensures consistent scoring across all technologies.

| Detection Method | Confidence | Tier |
|-----------------|------------|------|
| Package in SBOM | 95% (HIGH) | 1 |
| File Extension | 95% (HIGH) | 2 |
| Configuration File | 90% (HIGH) | 2 |
| Configuration Directory | 90% (HIGH) | 2 |
| Shebang Line | 90% (HIGH) | 2 |
| Import Statement | 85% (MEDIUM) | 2 |
| Code Pattern | 80% (MEDIUM) | 2 |
| Environment Variable | 70% (MEDIUM) | 2 |

See `confidence-config.json` for the full configuration.

## Usage

These patterns are used by the `technology-identification-analyser.sh` script:

```bash
# Quick scan (Tier 1 only - SBOM-based)
./utils/technology-identification/technology-identification-analyser.sh --quick --repo owner/repo

# Deep scan (Tier 1 + Tier 2 - includes file analysis)
./utils/technology-identification/technology-identification-analyser.sh --deep --repo owner/repo

# Default scan (Tier 1 + basic Tier 2)
./utils/technology-identification/technology-identification-analyser.sh --repo owner/repo

# Local directory
./utils/technology-identification/technology-identification-analyser.sh /path/to/repo
```

## Contributing

To add a new technology:

1. Create a directory under the appropriate category
2. Create a `patterns.md` file following the tiered format above
3. Separate SBOM patterns (Tier 1) from file patterns (Tier 2)
4. Include confidence scores based on pattern specificity
5. Add file extensions and config files where applicable
6. Test against real-world repositories

## License

GPL-3.0 - See [LICENSE](../../LICENSE) for details.
