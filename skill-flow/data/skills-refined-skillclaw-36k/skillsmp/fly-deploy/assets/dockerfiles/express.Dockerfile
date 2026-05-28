# Express.js Dockerfile for fly.io

FROM node:20-alpine AS base

# Install dependencies
FROM base AS deps
WORKDIR /app

# Copy package files
COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* ./

# Install dependencies based on lockfile
RUN \
  if [ -f yarn.lock ]; then yarn --frozen-lockfile --production; \
  elif [ -f package-lock.json ]; then npm ci --only=production; \
  elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm i --frozen-lockfile --prod; \
  else echo "Lockfile not found." && exit 1; \
  fi

# Build stage (if you have a build step)
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# If using TypeScript, uncomment:
# RUN npm run build

# Production runner
FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production

# Create non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 expressuser

# Copy dependencies
COPY --from=deps --chown=expressuser:nodejs /app/node_modules ./node_modules

# Copy application code
# For TypeScript apps, copy dist/ instead of src/
COPY --chown=expressuser:nodejs . .
# OR for TypeScript:
# COPY --from=builder --chown=expressuser:nodejs /app/dist ./dist
# COPY --chown=expressuser:nodejs package.json ./

USER expressuser

EXPOSE 8080

ENV PORT=8080

# Adjust the command based on your entry point
CMD ["node", "index.js"]
# OR for TypeScript:
# CMD ["node", "dist/index.js"]
