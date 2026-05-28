---
name: spark-docker
description: Manage Docker Spark infrastructure for local development or production (S3). Use this skill to start, stop, or check status of Spark clusters. Invoke with /spark-docker.
---

# Spark Docker Management

This skill manages the Docker-based Spark infrastructure for the wc_simd project.

> **Use `spark_docker_s3/` for all Spark work.** The HDFS-based `spark_docker/` is deprecated.

## Primary Stack: `spark_docker_s3/`

- Spark 3.5.5 + S3 warehouse + RDS MySQL metastore
- Uses EC2 instance profile for S3 access
- Configure `.env` from `.env.example` with S3 bucket and RDS credentials

## Commands

### Start Spark
```bash
cd spark_docker_s3 && docker compose up -d --build
```

First time setup requires `INIT_HIVE_SCHEMA=true` in `.env` to create metastore tables.

### Stop Spark
```bash
cd spark_docker_s3 && docker compose down
```

### Check Status
```bash
cd spark_docker_s3 && docker compose ps
```

### View Logs
```bash
cd spark_docker_s3 && docker compose logs -f spark
```

### Access Spark Shell
```bash
docker exec -it spark /opt/spark/bin/spark-sql
```

## Troubleshooting

### OOM Errors
Add to Spark config:
- `spark.sql.orc.enableVectorizedReader=false`
- `spark.sql.parquet.columnarReaderBatchSize=256`

### Derby Lock Issues
Use MySQL-backed metastore (already configured in Docker stacks).

### Host Service Access from Spark
Use Docker gateway IP `172.19.0.1` instead of `localhost`.

## Deprecated: `spark_docker/` (HDFS-based)

> **DEPRECATED**: This stack is no longer maintained. Use `spark_docker_s3/` instead.

The old HDFS-based local stack in `spark_docker/` required:
- `127.0.0.1 hadoop-namenode` in `/etc/hosts`
- Local HDFS storage (not portable across machines)
