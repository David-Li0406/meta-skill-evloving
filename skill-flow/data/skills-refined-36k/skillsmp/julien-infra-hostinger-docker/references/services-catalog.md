# Hostinger VPS Services Catalog

Complete list of Docker services running on srv759970 (automation@69.62.108.82).

## Optimized Applications

Multi-stage Docker builds deployed with security enhancements.

### support-dashboard
- **Path:** `/opt/support-dashboard`
- **Size:** 665 MB (optimized from 838 MB, -20.6%)
- **Port:** 8501
- **Stack:** Python, Streamlit
- **Status:** Healthy
- **Optimizations:** Multi-stage build, non-root user (streamlit)

### downto40-streamlit
- **Path:** `/opt/downto40`
- **Size:** 778 MB (optimized from 951 MB, -18.2%)
- **Port:** 8502
- **Stack:** Python, Streamlit
- **Status:** Healthy
- **Config:** Uses docker-compose.simple.yml
- **Optimizations:** Multi-stage build, non-root user (streamlit)

### discord-bot
- **Path:** `/opt/discord-bot`
- **Size:** 617 MB (optimized from 810 MB, -23.8%)
- **Stack:** Python, Discord.py
- **Status:** Running
- **Optimizations:** Multi-stage build, non-root user (discord)

### langchain-service
- **Path:** `/opt/langchain-service`
- **Size:** 333 MB
- **Port:** 5000
- **Stack:** Python, FastAPI, LangChain
- **Status:** Healthy
- **Healthcheck:** http://localhost:5000/health
- **Optimizations:** Multi-stage build, non-root user (langchain), curl for healthcheck

### mkdocs
- **Path:** `/opt/mkdocs`
- **Size:** 225 MB
- **Port:** 8005 (mapped to 8000 internal)
- **Stack:** Python, MkDocs
- **Status:** Running
- **Optimizations:** Multi-stage build, non-root user (mkdocs)

### photos-chantier
- **Path:** `/opt/photos-chantier`
- **Size:** 247 MB
- **Port:** 3001
- **Stack:** Next.js
- **Status:** Well-optimized (already multi-stage)

## ML Applications

Large applications with ML models - do NOT optimize these.

### whisperx
- **Path:** `/opt/whisperx`
- **Size:** 12.2 GB
- **Ports:**
  - API: 5001
  - Dashboard: 6379 (RQ Dashboard)
- **Stack:** Python, WhisperX, Redis, RQ
- **Model:** large-v3
- **Language:** French (fr)
- **Components:**
  - whisperx (main service)
  - whisperx-worker (background worker)
  - whisperx-dashboard (RQ dashboard)
  - rq-queue-redis (Redis for task queue)
- **Note:** Model size requires 12GB+ disk space

### paperflow
- **Path:** `/opt/paperflow`
- **Size:** 6.65 GB
- **Ports:**
  - API: 8000
  - Flower: 5555
- **Stack:** Python, FastAPI, Celery, ML dependencies
- **Components:**
  - paperflow-api (FastAPI backend)
  - paperflow-worker (Celery worker)
  - paperflow-flower (Celery monitoring)
- **Note:** Heavy ML dependencies for document processing

## Supporting Services

### telegram-bot
- **Path:** `/opt/telegram-bot`
- **Size:** 155 MB
- **Stack:** Python, Telegram Bot API
- **Status:** Running

### human-chain
- **Path:** `/opt/human-chain`
- **Components:**
  - human-chain_frontend (53.3 MB)
  - human-chain_backend (173 MB)
- **Stack:** React frontend, FastAPI backend

## Infrastructure Services

### Monitoring Stack

**prometheus**
- **Image:** prom/prometheus:latest (370 MB)
- **Port:** 9090
- **Purpose:** Metrics collection and storage

**grafana**
- **Image:** grafana/grafana:latest (733 MB)
- **Port:** 3000
- **Purpose:** Metrics visualization dashboards

**loki**
- **Image:** grafana/loki:latest (123 MB)
- **Port:** 3100
- **Purpose:** Log aggregation

**promtail**
- **Image:** grafana/promtail:latest (200 MB)
- **Purpose:** Log collection and forwarding to Loki

### Database Services

**postgres**
- **Image:** postgres:17-alpine (278 MB)
- **Port:** 5432
- **Purpose:** Primary PostgreSQL database

**mysql-clemence**
- **Image:** mysql:8.0 (780 MB)
- **Port:** 3307 (mapped to 3306 internal)
- **Purpose:** WordPress database

**mongo**
- **Image:** mongo:7 (834 MB)
- **Port:** 27017
- **Purpose:** MongoDB for document storage

**redis (rq-queue-redis)**
- **Image:** redis:7-alpine (41.4 MB)
- **Port:** 6379
- **Purpose:** Redis for RQ task queue (WhisperX)

### Management Tools

**portainer**
- **Image:** portainer/portainer-ce:latest (186 MB)
- **Port:** 9000
- **Purpose:** Docker container management UI

**postgres-exporter**
- **Image:** prometheuscommunity/postgres-exporter:latest (22.7 MB)
- **Port:** 9187
- **Purpose:** PostgreSQL metrics for Prometheus

**rq-exporter**
- **Image:** mdawar/rq-exporter:latest (133 MB)
- **Purpose:** RQ queue metrics for Prometheus

**glances**
- **Image:** nicolargo/glances:latest (86.2 MB)
- **Port:** 61208
- **Purpose:** System monitoring

**rustdesk-server**
- **Image:** rustdesk/rustdesk-server:latest (12.8 MB)
- **Ports:** 21115-21119
- **Purpose:** Remote desktop server

**rq-dashboard**
- **Image:** eoranged/rq-dashboard:latest (242 MB)
- **Port:** 9181
- **Purpose:** RQ queue monitoring dashboard

## WordPress Sites

### wordpress-clemence (Production)
- **Path:** `/opt/wordpress-clemence`
- **Image:** wordpress-clemence-custom:production (268 MB)
- **Port:** 8081
- **Database:** mysql-clemence
- **Proxy:** nginx-clemence (nginx:alpine, 52.8 MB)

### wordpress-clemence (Test/Phase3)
- **Image:** wordpress-clemence-custom:phase3 (268 MB)
- **Port:** 8084
- **Proxy:** nginx-clemence-test

### wordpress-test-themes
- **Image:** wordpress-sqlite-optimized:latest (373 MB)
- **Port:** 8082
- **Database:** SQLite (no external DB)
- **Proxy:** nginx-test-themes
- **Status:** Unhealthy (testing environment)

## Service Groups by Purpose

**Dashboards & Monitoring:**
- support-dashboard
- downto40-streamlit
- grafana
- portainer
- glances
- rq-dashboard

**AI/ML Services:**
- whisperx
- paperflow
- langchain-service

**Communication:**
- discord-bot
- telegram-bot

**Web Applications:**
- wordpress-clemence (prod + test)
- wordpress-test-themes
- photos-chantier
- human-chain

**Documentation:**
- mkdocs

**Infrastructure:**
- prometheus, loki, promtail
- postgres, mysql, mongo, redis
- nginx (multiple instances)

## Disk Usage Summary

- **Total Images:** 32 (27.41 GB)
- **Total Containers:** 37
- **Total Volumes:** 45 (3.71 GB, 14 active)
- **Optimizations Saved:** ~5.17 GB (optimizations + cleanup)
