# ========================================================
# Stage 1: Build Stage
# Install dependencies, build React frontend, and prepare
# production server dependencies.
# ========================================================
FROM node:20-alpine AS builder

WORKDIR /app

# Build React Client
COPY client/package*.json ./client/
RUN cd client && npm ci

COPY client/ ./client/
RUN cd client && npm run build

# Install Server Production Dependencies
COPY server/package*.json ./server/
RUN cd server && npm ci --omit=dev

# ========================================================
# Stage 2: Runtime Stage
# Lightweight slim/alpine base image minimizing final size.
# Copies only required build artifacts from builder stage.
# ========================================================
FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production
ENV PORT=5000

# Copy server production node_modules and code
COPY --from=builder /app/server/node_modules ./node_modules
COPY --from=builder /app/server/package.json ./package.json
COPY server/ ./

# Copy compiled React frontend into public directory for Express to serve
COPY --from=builder /app/client/dist ./public

# Use standard non-root node user for container security
USER node

EXPOSE 5000

# Healthcheck for container orchestration
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:5000/api/health || exit 1

CMD ["node", "index.js"]
