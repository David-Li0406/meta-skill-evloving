# Taskflow Application Deployment Reference

## Application Architecture
The Taskflow application consists of three main components:
- Frontend: Next.js web application
- Backend: Python FastAPI API server
- MCP Server: Model Context Protocol server for AI operations

## Service Dependencies
- Frontend connects to Backend via HTTP requests
- Backend connects to MCP Server for AI operations
- All services may connect to a database for persistent storage

## Kubernetes Deployment Components

### Frontend Deployment
- Container image: taskflow-frontend
- Port: 3000 (Next.js default)
- Environment variables:
  - BACKEND_URL: URL of the backend service
  - NODE_ENV: production/development

### Backend Deployment
- Container image: taskflow-backend
- Port: 8000 (FastAPI default)
- Environment variables:
  - MCP_SERVER_URL: URL of the MCP server service (e.g., http://mcp-server:8080)
  - DATABASE_URL: Connection string for the database
  - API_KEY: Authentication key if needed

### MCP Server Deployment
- Container image: taskflow-mcp-server
- Port: 8080 (MCP server default)
- Environment variables:
  - GEMINI_API_KEY: API key for the Gemini service (or other LLM provider)
  - LOG_LEVEL: Logging verbosity

## Service Communication
- Backend connects to MCP Server using: `http://mcp-server:8080`
- Frontend connects to Backend using: `http://backend:8000`
- All service names should match the Kubernetes service names exactly

## Configuration Requirements
- Use ConfigMaps for non-sensitive configuration
- Use Secrets for API keys and sensitive data
- Implement proper CORS settings for frontend-backend communication

## Resource Requirements
- Frontend: 128Mi memory request, 256Mi limit
- Backend: 256Mi memory request, 512Mi limit
- MCP Server: 512Mi memory request, 1Gi limit (due to AI processing)

## Health Checks
- Frontend: Simple HTTP GET to root path
- Backend: HTTP GET to `/health` endpoint
- MCP Server: HTTP GET to health check endpoint

## Persistent Storage
- Database storage for task items and user data
- Consider using PersistentVolumeClaims with appropriate storage class
- Implement backup strategies for critical data

## Ingress Configuration
- Route frontend to the root path
- Configure TLS for secure connections
- Set up appropriate timeouts for AI operations

## Scaling Considerations
- MCP Server may require more resources during AI processing
- Backend may need scaling based on API request volume
- Frontend typically requires less scaling unless serving static assets

## Security Considerations
- Protect MCP Server from direct external access
- Implement proper authentication between services
- Secure API keys using Kubernetes Secrets
