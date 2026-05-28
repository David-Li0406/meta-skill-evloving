# ==================================================
# NEXT.JS - DOCKERFILE TEMPLATE
# ==================================================
# Multi-stage build for size reduction
# Security: non-root user
# ==================================================

# Stage 1: Dependencies
FROM node:18-alpine AS deps

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm ci --only=production

# Stage 2: Builder
FROM node:18-alpine AS builder

WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Build application
RUN npm run build

# Stage 3: Runtime
FROM node:18-alpine

WORKDIR /app

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Copy necessary files from builder
COPY --from=builder --chown=nextjs:nodejs /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# Switch to non-root user
USER nextjs

# Expose port
EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

# Run application
CMD ["node", "server.js"]
