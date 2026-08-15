#!/usr/bin/env bash
# Per-boot infrastructure reconciliation. Brings up Postgres, Redis and MinIO
# (all as background daemons owned by the agent user) and ensures the test
# database, pgvector extension and MinIO bucket exist. Idempotent: it detects
# already-running services and returns once everything is reachable. The
# backend and UI processes are started by the `terminals` entries instead, so
# their logs stay visible to the agent.
set -euo pipefail

ROOT="/workspace"
SVC="$HOME/dograh-services"
export PATH="/usr/lib/postgresql/16/bin:/usr/local/bin:$PATH"
mkdir -p "$SVC/logs" "$SVC/run"

echo "==> Starting Postgres"
if ! pg_ctl -D "$SVC/pgdata" status >/dev/null 2>&1; then
  pg_ctl -D "$SVC/pgdata" -l "$SVC/logs/postgres.log" -w start
fi
for _ in $(seq 1 30); do
  PGPASSWORD=postgres psql -h 127.0.0.1 -U postgres -d postgres -c "SELECT 1" >/dev/null 2>&1 && break
  sleep 1
done
PGPASSWORD=postgres psql -h 127.0.0.1 -U postgres -d postgres -tc \
  "SELECT 1 FROM pg_database WHERE datname='test_db'" | grep -q 1 \
  || PGPASSWORD=postgres psql -h 127.0.0.1 -U postgres -d postgres -c "CREATE DATABASE test_db"
PGPASSWORD=postgres psql -h 127.0.0.1 -U postgres -d postgres -c \
  "CREATE EXTENSION IF NOT EXISTS vector" >/dev/null

echo "==> Starting Redis"
if ! redis-cli -a redissecret -p 6379 ping >/dev/null 2>&1; then
  redis-server --port 6379 --requirepass redissecret --daemonize yes \
    --dir "$SVC/redis" --logfile "$SVC/logs/redis.log"
fi

echo "==> Starting MinIO"
if ! curl -fsS http://127.0.0.1:9000/minio/health/live >/dev/null 2>&1; then
  MINIO_ROOT_USER=minioadmin MINIO_ROOT_PASSWORD=minioadmin \
    nohup minio server "$SVC/minio" --address ':9000' --console-address ':9001' \
    > "$SVC/logs/minio.log" 2>&1 &
  for _ in $(seq 1 30); do
    curl -fsS http://127.0.0.1:9000/minio/health/live >/dev/null 2>&1 && break
    sleep 1
  done
fi
mc alias set localminio http://127.0.0.1:9000 minioadmin minioadmin >/dev/null 2>&1 || true
mc mb --ignore-existing localminio/voice-audio >/dev/null 2>&1 || true

echo "Infrastructure ready: Postgres (5432), Redis (6379), MinIO (9000/9001)."
