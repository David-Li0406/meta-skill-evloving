# MCP Server Deployment Checklist

When adding a new MCP server, update these files:

## 1. docker-compose.yml

Add new service:

```yaml
services:
  {name}-mcp:
    build:
      context: ./MCPS/{name}
      dockerfile: Dockerfile
    container_name: claude-assistant-{name}-mcp
    environment:
      - {NAME}_API_KEY=${{{NAME}_API_KEY}}
      - {NAME}_MCP_HOST=0.0.0.0
      - {NAME}_MCP_PORT=808X
    networks:
      - internal
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:808X/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped
```

## 2. Jenkinsfile

### Add Environment Variables

```groovy
environment {
    // ... existing ...
    {NAME}_API_KEY = credentials('{name}-api-key')
    {NAME}_MCP_IMAGE_NAME = 'claude-assistant-{name}-mcp'
    {NAME}_MCP_CONTAINER = 'claude-assistant-{name}-mcp'
    {NAME}_MCP_PORT = '808X'
}
```

### Add Prepare Stage

```groovy
env.{NAME}_MCP_IMAGE = "${DOCKER_REGISTRY}/${{{NAME}_MCP_IMAGE_NAME}}:${env.IMAGE_VERSION}"
echo "{Name} MCP Image: ${env.{NAME}_MCP_IMAGE}"
```

### Add Build Stage

```groovy
stage('Build {Name} MCP') {
    steps {
        script {
            sh """
            export DOCKER_HOST=${DOCKER_HOST}
            docker build --platform linux/arm64/v8 \
                -t ${env.{NAME}_MCP_IMAGE} \
                -f ./MCPS/{name}/Dockerfile \
                ./MCPS/{name}
            """
        }
    }
}
```

### Add Push Stage

```groovy
stage('Push {Name} MCP') {
    steps {
        script {
            sh "docker push ${env.{NAME}_MCP_IMAGE}"
        }
    }
}
```

### Add Stop Stage

```groovy
docker ps -f name=${{{NAME}_MCP_CONTAINER}} -q | xargs --no-run-if-empty docker container stop
docker container ls -a -f name=${{{NAME}_MCP_CONTAINER}} -q | xargs -r docker container rm
```

### Add Start Stage

```groovy
stage('Start {Name} MCP') {
    steps {
        script {
            sh """
            docker run -d \
                --name ${{{NAME}_MCP_CONTAINER}} \
                --network ${DOCKER_NETWORK} \
                --restart unless-stopped \
                -p ${{{NAME}_MCP_PORT}}:808X \
                -e {NAME}_API_KEY=\${{{NAME}_API_KEY}} \
                -e {NAME}_MCP_HOST=0.0.0.0 \
                -e {NAME}_MCP_PORT=808X \
                ${env.{NAME}_MCP_IMAGE}
            """

            sh """
            echo "Waiting for {Name} MCP to be healthy..."
            sleep 10
            curl -f http://localhost:${{{NAME}_MCP_PORT}}/health || echo "Health check pending..."
            """
        }
    }
}
```

### Update Backend Start Stage

Add environment variables:

```groovy
-e {NAME}_MCP_HOST=${{{NAME}_MCP_CONTAINER}} \
-e {NAME}_MCP_PORT=808X \
```

### Update Verify Stage

```groovy
echo "{Name} MCP:          http://192.168.50.35:${{{NAME}_MCP_PORT}}"
```

## 3. DOCUMENTATION/DEPLOYMENT.md

### Port Configuration Tables

Add to Production and Local Development tables:

```markdown
| {Name} MCP | 808X | 808X | HTTP | {Service} API tools |
```

### Port Allocation Strategy

```markdown
- 808X: {Name} MCP
```

### Container Reference

Add to Production and Development containers:

```markdown
| `claude-assistant-{name}-mcp` | `claude-assistant-{name}-mcp` | `192.168.50.35:5000/claude-assistant-{name}-mcp` |
```

### Internal Service Discovery

```markdown
| {Name} MCP | `claude-assistant-{name}-mcp` | 808X |
```

### Jenkins Credentials

```markdown
| `{name}-api-key` | Secret text | {Service} API key | [{Service} Console](https://...) |
```

### Environment Variables

Add new section:

```markdown
### {Name} Integration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `{NAME}_API_KEY` | Yes | — | {Service} API key |
| `{NAME}_MCP_HOST` | No | `{name}-mcp` | MCP server hostname |
| `{NAME}_MCP_PORT` | No | `808X` | MCP server port |
```

### Infrastructure Endpoints

```markdown
| {Name} MCP | `http://192.168.50.35:808X` | `/health` |
```

### Quick Reference - View Logs

```markdown
docker logs claude-assistant-{name}-mcp
```

### Quick Reference - Health Checks

```markdown
# {Name} MCP
curl http://localhost:808X/health
```

### Changelog

Add entry:

```markdown
| YYYY-MM-DD | Added {Name} MCP (port 808X) | Claude |
```

## 4. .env.example

Add:

```env
# {Name} Integration
{NAME}_API_KEY=your-{name}-api-key-here
{NAME}_MCP_HOST=claude-assistant-{name}-mcp
{NAME}_MCP_PORT=808X
```

## 5. Jenkins Credentials

Add to Jenkins:

1. Go to Jenkins → Manage Jenkins → Credentials
2. Add new Secret text credential:
   - ID: `{name}-api-key`
   - Secret: Your API key
   - Description: {Service} API Key

## Verification

After all updates, verify:

- [ ] `docker-compose.yml` builds successfully
- [ ] Jenkins pipeline passes
- [ ] Container starts and health check passes
- [ ] Backend can communicate with MCP server
- [ ] Documentation is complete and accurate
