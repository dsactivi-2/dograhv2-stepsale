#!/usr/bin/env bash
# Backend terminal: launches the FastAPI stack (uvicorn + ari_manager +
# campaign_orchestrator + arq) via the repo's dev launcher, which runs Alembic
# migrations, waits for the /api/v1/health check, then returns. We then tail the
# service logs so this terminal stays live and the agent can watch backend output.
set -euo pipefail

cd /workspace
# shellcheck disable=SC1091
source venv/bin/activate
bash scripts/start_services_dev.sh

echo ""
echo "Backend is up on http://localhost:8000 — tailing logs (Ctrl-C to stop tail; services keep running)."
exec tail -F logs/latest/*.log
