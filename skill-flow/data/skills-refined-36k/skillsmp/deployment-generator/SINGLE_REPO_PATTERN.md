# Single DockerHub Repository Pattern

**For deployment-generator skill**

## Overview

Some users prefer a **single private DockerHub repository** with multiple tagged images instead of separate repositories per component. This pattern is useful for:

- Cost savings (one private repo vs multiple)
- Centralized image management
- Better organization for multi-component projects
- Existing private repo utilization

## Image Naming Pattern

**Format:** `{username}/{repo}:{component-name}-{version}`

**Examples:**
```
kazishiplu/store:chronostash-backend-deploy-abc1234
kazishiplu/store:chronostash-frontend-deploy-abc1234
kazishiplu/store:toolz-admin-dev
kazishiplu/store:myapp-api-v1.0.0
```

## When to Use This Pattern

Use single-repo pattern when user:
- Mentions "single repository" or "one repo"
- Already has private DockerHub repo
- Wants cost-effective private image storage
- Shows example like `username/repo:image-tag`
- Has multiple projects in one repo

## Discovery Questions

Add these questions when single-repo pattern detected:

```
**DockerHub Configuration:**
- DockerHub username?
- Repository name for all images?
- Image naming prefix/pattern?
```

## Implementation

### GitHub Secrets

```yaml
Required Secrets:
- DOCKERHUB_USERNAME: DockerHub username
- DOCKERHUB_REPO: Repository name (e.g., "store")
- DOCKERHUB_TOKEN: Access token with Read & Write permissions
- KUBE_CONFIG: Base64-encoded kubeconfig
```

### Workflow Configuration

```yaml
env:
  DOCKERHUB_USERNAME: ${{ secrets.DOCKERHUB_USERNAME }}
  DOCKERHUB_REPO: ${{ secrets.DOCKERHUB_REPO || 'images' }}  # Default repo name
  REGISTRY: docker.io

jobs:
  build:
    steps:
      - name: Set image tag
        id: tag
        run: |
          # Determine version
          if [[ $GITHUB_REF == refs/tags/* ]]; then
            VERSION="${GITHUB_REF#refs/tags/}"
          else
            BRANCH="${GITHUB_REF#refs/heads/}"
            VERSION="${BRANCH}-${GITHUB_SHA::7}"
          fi

          # Component-specific image name
          IMAGE_NAME="myapp-${{ matrix.component.name }}-${VERSION}"
          echo "full_image=${DOCKERHUB_USERNAME}/${DOCKERHUB_REPO}:${IMAGE_NAME}" >> $GITHUB_OUTPUT

      - name: Build and push
        run: |
          docker build -f ${{ matrix.component.dockerfile }} -t ${{ steps.tag.outputs.full_image }} .
          docker push ${{ steps.tag.outputs.full_image }}
```

### Image Tag Logic

**Version patterns:**
- Branch push: `{component}-{branch}-{short-sha}` → `backend-deploy-abc1234`
- Version tag: `{component}-{version}` → `backend-v1.0.0`
- Environment: `{component}-{env}` → `backend-production`

**Component naming:**
- Use project name as prefix: `chronostash-backend`, `toolz-admin`
- Separate with hyphen: `project-component-version`
- Keep under 128 characters (Docker limit)

### Kubernetes Manifests

Use placeholders that get replaced during deployment:

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: backend
          image: IMAGE_BACKEND  # Replaced by CI/CD
```

**Replacement in workflow:**
```bash
sed -i "s|IMAGE_BACKEND|${DOCKERHUB_USERNAME}/${DOCKERHUB_REPO}:${IMAGE_NAME}|g" backend.yaml
```

## Template Files

### Workflow Template

```yaml
name: Build and Deploy

env:
  DOCKERHUB_USERNAME: ${{ secrets.DOCKERHUB_USERNAME }}
  DOCKERHUB_REPO: ${{ secrets.DOCKERHUB_REPO || 'images' }}
  PROJECT_NAME: myapp

jobs:
  build:
    strategy:
      matrix:
        component:
          - name: backend
            dockerfile: Dockerfile.backend
          - name: frontend
            dockerfile: Dockerfile.frontend

    steps:
      - name: Set image names
        id: images
        run: |
          if [[ $GITHUB_REF == refs/tags/* ]]; then
            VERSION="${GITHUB_REF#refs/tags/}"
          else
            BRANCH="${GITHUB_REF#refs/heads/}"
            VERSION="${BRANCH}-${GITHUB_SHA::7}"
          fi

          IMAGE_NAME="${PROJECT_NAME}-${{ matrix.component.name }}-${VERSION}"
          FULL_IMAGE="${DOCKERHUB_USERNAME}/${DOCKERHUB_REPO}:${IMAGE_NAME}"

          echo "image_name=${IMAGE_NAME}" >> $GITHUB_OUTPUT
          echo "full_image=${FULL_IMAGE}" >> $GITHUB_OUTPUT

      - name: Build and push
        run: |
          docker build -f ${{ matrix.component.dockerfile }} -t ${{ steps.images.outputs.full_image }} .
          docker push ${{ steps.images.outputs.full_image }}

  deploy:
    needs: build
    steps:
      - name: Update manifests
        run: |
          cd k8s
          sed -i "s|IMAGE_BACKEND|${DOCKERHUB_USERNAME}/${DOCKERHUB_REPO}:${PROJECT_NAME}-backend-${VERSION}|g" backend.yaml
          sed -i "s|IMAGE_FRONTEND|${DOCKERHUB_USERNAME}/${DOCKERHUB_REPO}:${PROJECT_NAME}-frontend-${VERSION}|g" frontend.yaml
```

## Documentation Template

Create `DOCKERHUB_SINGLE_REPO.md` with:

1. **Image naming pattern** - Format and examples
2. **GitHub secrets** - Required secrets with descriptions
3. **Manual build commands** - How to build/push manually
4. **Troubleshooting** - Common issues and solutions
5. **Migration guide** - If moving from separate repos

## Verification Checklist

- [ ] `DOCKERHUB_REPO` secret documented
- [ ] Image names include project prefix
- [ ] Workflow uses single repository
- [ ] Manifests use image placeholders
- [ ] Documentation includes single-repo pattern
- [ ] Image pull secrets configured (if private)
- [ ] Cleanup/retention policy documented

## Common Mistakes

| Mistake | Correct Approach |
|---------|-----------------|
| Using separate repos | Use `${DOCKERHUB_REPO}:component-version` |
| Forgetting project prefix | Always prefix: `myapp-backend` not just `backend` |
| Hardcoding repo name | Use `DOCKERHUB_REPO` secret variable |
| Not documenting pattern | Create DOCKERHUB_SINGLE_REPO.md |
| Missing image pull secret | Add if repo is private |

## Examples

### Multi-Project Repository

User has multiple projects in `username/store`:
```
username/store:chronostash-backend-v1.0.0
username/store:chronostash-frontend-v1.0.0
username/store:toolz-admin-dev
username/store:toolz-web-dev
username/store:trackwise-api-prod
```

**Pattern:** `{project}-{component}-{env/version}`

### Environment-Specific Tags

```
username/store:myapp-backend-production
username/store:myapp-backend-staging
username/store:myapp-backend-dev
```

**Pattern:** `{project}-{component}-{environment}`

### Version + Environment

```
username/store:myapp-backend-v1.2.3-prod
username/store:myapp-frontend-v1.2.3-prod
username/store:myapp-backend-v1.2.2-staging
```

**Pattern:** `{project}-{component}-{version}-{env}`

## Integration with Skill Workflow

### Phase 1: Discovery

When user mentions single repository:
```
User: "I want to use kazishiplu/store for all images like kazishiplu/store:toolz-admin-dev"
**Assistant Response:**
```
I see you want to use a single DockerHub repository with multiple tagged images.

Questions:
1. DockerHub username? (I see: kazishiplu)
2. Repository name? (I see: store)
3. Project name prefix? (e.g., "chronostash" for chronostash-backend-v1.0.0)
```

### Phase 2: Generation

Generate workflow with single-repo pattern:

```yaml
env:
  DOCKERHUB_USERNAME: ${{ secrets.DOCKERHUB_USERNAME }}
  DOCKERHUB_REPO: ${{ secrets.DOCKERHUB_REPO || 'store' }}

jobs:
  build:
    steps:
      - name: Set image tag
        run: |
          IMAGE_NAME="project-component-${VERSION}"
          echo "full_image=${DOCKERHUB_USERNAME}/${DOCKERHUB_REPO}:${IMAGE_NAME}" >> $GITHUB_OUTPUT
      
      - name: Build and push
        run: |
          docker build -t ${{ steps.tag.outputs.full_image }} .
          docker push ${{ steps.tag.outputs.full_image }}
```

**Key differences from separate-repo pattern:**
1. Add `DOCKERHUB_REPO` environment variable
2. Use `${REPO}:${TAG}` instead of `${REPO}:latest`
3. Include project prefix in tag: `chronostash-backend` not `backend`
4. Document DOCKERHUB_REPO secret

### Phase 3: Verification

Additional checks for single-repo pattern:

- [ ] `DOCKERHUB_REPO` secret documented
- [ ] Image names include project prefix
- [ ] Tag format: `project-component-version`
- [ ] DOCKERHUB_SINGLE_REPO.md created

## Quick Reference

**Detect single-repo pattern:**
- User mentions "single repo" or "one repository"
- Shows example: `username/repo:image-tag`
- Already has private repo

**Implementation checklist:**
1. Add `DOCKERHUB_REPO` env variable
2. Update image naming: `${REPO}:${PROJECT}-${COMPONENT}-${VERSION}`
3. Document in DOCKERHUB_SINGLE_REPO.md
4. Add to GitHub secrets list
5. Verify tag format includes project prefix

**Common pitfalls:**
- Forgetting project prefix (causes name collision)
- Hardcoding repo name (use secret variable)
- Not documenting the pattern
- Missing image pull secret for private repos
