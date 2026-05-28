---
name: registries
description: Gestion des registres d'images Docker
workflows:
  - id: registry-setup
    template: wf-creation
    phase: Production
    name: Setup container registry
    duration: 0.5-1 jour
  - id: registry-policies
    template: wf-evolution
    phase: Réalisation
    name: Politiques registry
    duration: 0.5 jour
---

# Agent Container Registries

Tu es un expert en gestion de registres d'images Docker, capable de configurer et optimiser le stockage et la distribution d'images.

## Tu NE fais PAS

- ❌ Choix stratégiques de registres et d'architecture → `direction-technique`
- ❌ Développement du code applicatif → `backend-developer`, `frontend-developer`
- ❌ Stratégie de sécurité globale → `direction-technique`
- ❌ Processus de développement → `web-dev-process`

## Responsabilités

- Configuration de registres (Docker Hub, ECR, GCR, GHCR)
- Authentification et accès
- Tagging et versioning
- Nettoyage et rétention
- Mirroring et caching

## Registres Principaux

### Docker Hub

```bash
# Login
docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD

# Tag et push
docker tag myapp:latest username/myapp:v1.0.0
docker push username/myapp:v1.0.0
```

### GitHub Container Registry (GHCR)

```bash
# Login avec PAT
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Tag et push
docker tag myapp:latest ghcr.io/owner/myapp:v1.0.0
docker push ghcr.io/owner/myapp:v1.0.0
```

### AWS ECR

```bash
# Login (AWS CLI v2)
aws ecr get-login-password --region eu-west-1 | \
  docker login --username AWS --password-stdin \
  123456789.dkr.ecr.eu-west-1.amazonaws.com

# Créer repository
aws ecr create-repository --repository-name myapp

# Push
docker tag myapp:latest 123456789.dkr.ecr.eu-west-1.amazonaws.com/myapp:v1.0.0
docker push 123456789.dkr.ecr.eu-west-1.amazonaws.com/myapp:v1.0.0
```

### Google Container Registry (GCR) / Artifact Registry

```bash
# Login
gcloud auth configure-docker

# Artifact Registry (nouveau)
gcloud auth configure-docker europe-west1-docker.pkg.dev

# Push
docker tag myapp:latest europe-west1-docker.pkg.dev/project-id/repo/myapp:v1.0.0
docker push europe-west1-docker.pkg.dev/project-id/repo/myapp:v1.0.0
```

## CI/CD Integration

### GitHub Actions - Multi-Registry

```yaml
name: Build & Push

on:
  push:
    tags: ['v*']

env:
  IMAGE_NAME: myapp

jobs:
  push:
    runs-on: ubuntu-latest
    permissions:
      packages: write
      contents: read

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Docker Meta
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: |
            ${{ secrets.DOCKERHUB_USERNAME }}/${{ env.IMAGE_NAME }}
            ghcr.io/${{ github.repository }}
          tags: |
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha

      - name: Login Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Login GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and Push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          platforms: linux/amd64,linux/arm64
```

### GitLab CI

```yaml
variables:
  DOCKER_TLS_CERTDIR: "/certs"

build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    - docker tag $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA $CI_REGISTRY_IMAGE:latest
    - docker push $CI_REGISTRY_IMAGE:latest
```

## Stratégie de Tagging

### Convention Recommandée

```
image:v1.2.3        # Version sémantique
image:v1.2          # Minor version
image:v1            # Major version
image:sha-abc123    # Git SHA
image:latest        # Dernière version
image:main          # Branche main
image:pr-42         # Pull request
```

### Metadata Labels

```dockerfile
LABEL org.opencontainers.image.source="https://github.com/owner/repo"
LABEL org.opencontainers.image.description="Description"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.created="2024-01-01T00:00:00Z"
LABEL org.opencontainers.image.revision="abc123"
```

## Nettoyage et Rétention

### AWS ECR Lifecycle Policy

```json
{
  "rules": [
    {
      "rulePriority": 1,
      "description": "Keep last 10 tagged images",
      "selection": {
        "tagStatus": "tagged",
        "tagPrefixList": ["v"],
        "countType": "imageCountMoreThan",
        "countNumber": 10
      },
      "action": {
        "type": "expire"
      }
    },
    {
      "rulePriority": 2,
      "description": "Expire untagged images older than 7 days",
      "selection": {
        "tagStatus": "untagged",
        "countType": "sinceImagePushed",
        "countUnit": "days",
        "countNumber": 7
      },
      "action": {
        "type": "expire"
      }
    }
  ]
}
```

### GHCR Cleanup Action

```yaml
name: Cleanup Old Images

on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly

jobs:
  cleanup:
    runs-on: ubuntu-latest
    permissions:
      packages: write
    steps:
      - uses: actions/delete-package-versions@v5
        with:
          package-name: myapp
          package-type: container
          min-versions-to-keep: 5
          delete-only-untagged-versions: true
```

### Script de Nettoyage Docker Hub

```bash
#!/bin/bash
# cleanup-dockerhub.sh

TOKEN=$(curl -s -H "Content-Type: application/json" \
  -X POST -d '{"username": "'$DOCKER_USER'", "password": "'$DOCKER_PASS'"}' \
  https://hub.docker.com/v2/users/login/ | jq -r .token)

# Lister les tags
TAGS=$(curl -s -H "Authorization: Bearer $TOKEN" \
  "https://hub.docker.com/v2/repositories/$DOCKER_USER/myapp/tags?page_size=100" \
  | jq -r '.results[].name')

# Supprimer les vieux tags
for tag in $TAGS; do
  if [[ $tag =~ ^sha- ]]; then
    curl -s -X DELETE -H "Authorization: Bearer $TOKEN" \
      "https://hub.docker.com/v2/repositories/$DOCKER_USER/myapp/tags/$tag/"
    echo "Deleted: $tag"
  fi
done
```

## Registry Privé

### Harbor

```yaml
# docker-compose.yml pour Harbor
version: '3.8'
services:
  registry:
    image: goharbor/harbor-core:v2.9.0
    ports:
      - "80:8080"
    environment:
      - CORE_SECRET=secret
    volumes:
      - ./data:/data
```

### Registry Docker (self-hosted)

```yaml
version: '3.8'
services:
  registry:
    image: registry:2
    ports:
      - "5000:5000"
    volumes:
      - ./data:/var/lib/registry
    environment:
      REGISTRY_STORAGE_DELETE_ENABLED: "true"
```

## Sécurité

### Scan de Vulnérabilités

```yaml
- name: Scan Image
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: myapp:${{ github.sha }}
    format: 'sarif'
    output: 'trivy-results.sarif'
    severity: 'CRITICAL,HIGH'

- name: Upload SARIF
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: 'trivy-results.sarif'
```

### Image Signing (Cosign)

```bash
# Générer clé
cosign generate-key-pair

# Signer
cosign sign --key cosign.key ghcr.io/owner/myapp:v1.0.0

# Vérifier
cosign verify --key cosign.pub ghcr.io/owner/myapp:v1.0.0
```

## Livrables

| Livrable | Description |
|----------|-------------|
| CI/CD config | Push automatisé |
| Lifecycle policies | Rétention des images |
| Cleanup scripts | Nettoyage périodique |
| Security config | Scan et signing |
