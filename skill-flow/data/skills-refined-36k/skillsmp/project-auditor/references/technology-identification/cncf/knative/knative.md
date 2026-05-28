# Knative

**Category**: cncf
**Description**: Kubernetes-based platform for serverless workloads
**Homepage**: https://knative.dev

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*Knative Go packages*

- `knative.dev/serving` - Knative Serving
- `knative.dev/eventing` - Knative Eventing
- `knative.dev/pkg` - Shared packages
- `knative.dev/client` - Knative CLI
- `knative.dev/func` - Knative Functions

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Knative usage*

- `service.yaml` - Knative Service
- `func.yaml` - Knative Function config
- `serving.yaml` - Serving configuration
- `eventing.yaml` - Eventing configuration

### Code Patterns

**Pattern**: `knative\.dev/|serving\.knative\.dev/|eventing\.knative\.dev/`
- Knative API groups
- Example: `serving.knative.dev/v1`

**Pattern**: `kind:\s*(Service|Route|Configuration|Revision)`
- Knative Serving resources
- Example: `kind: Service`

**Pattern**: `kind:\s*(Broker|Trigger|Channel|Subscription|Source)`
- Knative Eventing resources
- Example: `kind: Broker`

**Pattern**: `apiVersion:\s*serving\.knative\.dev/v[0-9]+`
- Knative Serving API
- Example: `apiVersion: serving.knative.dev/v1`

**Pattern**: `kn\s+(service|revision|route|trigger|source)`
- Knative CLI commands
- Example: `kn service create hello`

**Pattern**: `autoscaling\.knative\.dev/|concurrency|scale-to-zero`
- Knative autoscaling annotations
- Example: `autoscaling.knative.dev/target: "100"`

**Pattern**: `containerConcurrency:|minScale:|maxScale:`
- Knative scaling configuration
- Example: `containerConcurrency: 100`

**Pattern**: `knative-serving|knative-eventing`
- Knative namespaces
- Example: `namespace: knative-serving`

**Pattern**: `kourier|net-istio|net-contour`
- Knative networking layers
- Example: `kourier-system`

---

## Environment Variables

- `K_SERVICE` - Knative service name
- `K_REVISION` - Knative revision name
- `K_CONFIGURATION` - Knative configuration name
- `PORT` - Container port (often 8080)
- `K_SINK` - Event sink URL

## Detection Notes

- Serving manages stateless workloads
- Eventing handles event-driven architecture
- Scale-to-zero capability
- Supports multiple networking layers
- func CLI for function development

---

## Secrets Detection

### Credentials

#### Image Pull Secret
**Pattern**: `imagePullSecrets:\s*\n\s*-\s*name:\s*['"]?([^\s'"]+)['"]?`
**Severity**: high
**Description**: Image pull secret for private registries
**Multiline**: true

---

## TIER 3: Configuration Extraction

### Min Scale Extraction

**Pattern**: `minScale:\s*['"]?([0-9]+)['"]?`
- Minimum replicas
- Extracts: `min_scale`
- Example: `minScale: "1"`

### Max Scale Extraction

**Pattern**: `maxScale:\s*['"]?([0-9]+)['"]?`
- Maximum replicas
- Extracts: `max_scale`
- Example: `maxScale: "10"`

### Concurrency Target Extraction

**Pattern**: `autoscaling\.knative\.dev/target:\s*['"]?([0-9]+)['"]?`
- Target concurrency per replica
- Extracts: `concurrency_target`
- Example: `autoscaling.knative.dev/target: "100"`

### Container Image Extraction

**Pattern**: `image:\s*['"]?([a-zA-Z0-9._\-/:]+)['"]?`
- Container image
- Extracts: `container_image`
- Example: `image: gcr.io/my-project/my-app:v1`
