# =============================================================================
# SOCIOPULSE / MEDICOPULSE - Multi-Brand Next.js Frontend
# Production-Ready Dockerfile with Multi-Stage Build
# =============================================================================
#
# Usage:
#   docker build --build-arg NEXT_PUBLIC_APP_MODE=SOCIAL -t sociopulse-web .
#   docker build --build-arg NEXT_PUBLIC_APP_MODE=MEDICAL -t medicopulse-web .
#
# =============================================================================

# =============================================================================
# STAGE 1: BASE
# =============================================================================
FROM node:20-alpine AS base
WORKDIR /app
RUN apk add --no-cache libc6-compat openssl

# =============================================================================
# STAGE 2: DEPS
# =============================================================================
FROM base AS deps
WORKDIR /app

COPY package.json package-lock.json* yarn.lock* pnpm-lock.yaml* ./
COPY packages ./packages

RUN \
  if [ -f yarn.lock ]; then corepack enable && yarn --frozen-lockfile; \
  elif [ -f package-lock.json ]; then npm ci --legacy-peer-deps; \
  elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm i --frozen-lockfile; \
  else echo "Lockfile not found." && exit 1; \
  fi

# =============================================================================
# STAGE 3: BUILDER
# =============================================================================
FROM base AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY --from=deps /app/packages ./packages
COPY . .
RUN rm -rf apps/api

# Ensure public directory exists
RUN mkdir -p public

# Generate Prisma client
RUN npx prisma generate

# -----------------------------------------------------------------------------
# BUILD ARGUMENTS - Declared before ENV assignment
# -----------------------------------------------------------------------------
ARG NEXT_PUBLIC_APP_MODE=SOCIAL
ARG NEXT_PUBLIC_API_URL=https://api.sociopulse.fr

# -----------------------------------------------------------------------------
# CRITICAL: Set ENV vars BEFORE npm run build
# Next.js inlines NEXT_PUBLIC_* variables at build time
# -----------------------------------------------------------------------------
ENV NEXT_PUBLIC_APP_MODE=$NEXT_PUBLIC_APP_MODE
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV NEXT_TELEMETRY_DISABLED=1
# Increase Node.js memory limit for build
ENV NODE_OPTIONS="--max-old-space-size=4096"

# Log build configuration
RUN echo "==========================================" && \
  echo "Building Next.js Application" && \
  echo "Brand Mode:  $NEXT_PUBLIC_APP_MODE" && \
  echo "API URL:     $NEXT_PUBLIC_API_URL" && \
  echo "==========================================" 

# Build the application
RUN npm run build

# Verify standalone output exists
RUN ls -la .next/ && ls -la .next/standalone/ || echo "WARNING: standalone not found"

# =============================================================================
# STAGE 4: RUNNER (Production)
# =============================================================================
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Install curl for healthcheck
RUN apk add --no-cache curl

# Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
  adduser --system --uid 1001 nextjs

# Create required directories
RUN mkdir -p .next/static public && chown -R nextjs:nodejs .

# Copy standalone build output
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# Copy public folder (if exists)
COPY --from=builder --chown=nextjs:nodejs /app/public ./public

USER nextjs

EXPOSE 3000
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
  CMD curl -f http://localhost:3000/ || exit 1

CMD ["node", "server.js"]
