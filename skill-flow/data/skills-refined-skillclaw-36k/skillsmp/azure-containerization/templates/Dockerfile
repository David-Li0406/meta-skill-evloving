# =============================================================================
# Multi-Stage Dockerfile for .NET 10 Applications
# =============================================================================
# This Dockerfile uses multi-stage builds for smaller production images.
# Customize the project name and paths as needed.
# =============================================================================

# -----------------------------------------------------------------------------
# Stage 1: Base Runtime Image
# -----------------------------------------------------------------------------
FROM mcr.microsoft.com/dotnet/aspnet:10.0-alpine AS base
WORKDIR /app

# Expose ports
EXPOSE 8080
EXPOSE 8081

# Create non-root user for security
RUN adduser --disabled-password --gecos '' --home /app appuser
USER appuser

# Set environment variables
ENV ASPNETCORE_URLS=http://+:8080
ENV ASPNETCORE_ENVIRONMENT=Production
ENV DOTNET_RUNNING_IN_CONTAINER=true
ENV DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=false

# -----------------------------------------------------------------------------
# Stage 2: Build Stage
# -----------------------------------------------------------------------------
FROM mcr.microsoft.com/dotnet/sdk:10.0-alpine AS build
WORKDIR /src

# Copy project file and restore dependencies (layer caching)
COPY ["src/ProjectName.Web/ProjectName.Web.csproj", "src/ProjectName.Web/"]
RUN dotnet restore "src/ProjectName.Web/ProjectName.Web.csproj"

# Copy remaining source code
COPY . .

# Build the application
WORKDIR "/src/src/ProjectName.Web"
RUN dotnet build "ProjectName.Web.csproj" -c Release -o /app/build --no-restore

# -----------------------------------------------------------------------------
# Stage 3: Publish Stage
# -----------------------------------------------------------------------------
FROM build AS publish
RUN dotnet publish "ProjectName.Web.csproj" -c Release -o /app/publish --no-restore \
    /p:UseAppHost=false \
    /p:PublishTrimmed=false

# -----------------------------------------------------------------------------
# Stage 4: Final Production Image
# -----------------------------------------------------------------------------
FROM base AS final
WORKDIR /app

# Copy published output from publish stage
COPY --from=publish --chown=appuser:appuser /app/publish .

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

# Entry point
ENTRYPOINT ["dotnet", "ProjectName.Web.dll"]

# =============================================================================
# Build Commands:
# =============================================================================
# Build:
#   docker build -t myapp:latest .
#
# Run:
#   docker run -d -p 8080:8080 --name myapp myapp:latest
#
# Run with environment variables:
#   docker run -d -p 8080:8080 \
#     -e ConnectionStrings__DefaultConnection="..." \
#     -e ASPNETCORE_ENVIRONMENT=Development \
#     --name myapp myapp:latest
#
# Push to Azure Container Registry:
#   az acr login --name myregistry
#   docker tag myapp:latest myregistry.azurecr.io/myapp:latest
#   docker push myregistry.azurecr.io/myapp:latest
# =============================================================================
