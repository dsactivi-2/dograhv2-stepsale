#!/usr/bin/env bash
# Idempotent repository bootstrap for the Cloud Agent environment.
#
# System packages (python3.13, postgresql-16 + pgvector, redis-server, the
# minio/mc binaries and uv) live in the base snapshot. This script only
# refreshes repo-derived state: the pipecat submodule, the Python venv, node
# dependencies, the local .env files, and the Postgres data directory. It must
# stay safe to re-run and must terminate (no long-running processes here).
set -euo pipefail

ROOT="/workspace"
SVC="$HOME/dograh-services"
MINIO_RELEASE="minio.RELEASE.2025-09-07T16-13-09Z"
MC_RELEASE="mc.RELEASE.2025-08-13T08-35-41Z"
cd "$ROOT"

echo "==> [1/7] Installing system dependencies"
# Idempotent: skip the (slow) apt work once the key toolchains are present, so
# re-runs against a warm base or snapshot are fast. Postgres 16 + pgvector,
# Redis, ffmpeg and the Python 3.13 toolchain come from apt; uv and the
# MinIO server/client are fetched as static binaries.
if ! command -v python3.13 >/dev/null 2>&1 \
   || ! command -v psql >/dev/null 2>&1 \
   || ! command -v redis-server >/dev/null 2>&1 \
   || ! command -v uv >/dev/null 2>&1 \
   || [ ! -x /usr/local/bin/minio ]; then
  export DEBIAN_FRONTEND=noninteractive
  sudo apt-get update
  sudo apt-get install -y --no-install-recommends software-properties-common curl ca-certificates
  sudo add-apt-repository -y ppa:deadsnakes/ppa
  sudo apt-get update
  sudo apt-get install -y --no-install-recommends \
    build-essential git jq rsync procps pkg-config \
    ffmpeg libpq-dev postgresql-client redis-tools redis-server \
    python3.13 python3.13-venv python3.13-dev \
    postgresql-16 postgresql-16-pgvector
  if ! command -v uv >/dev/null 2>&1; then
    curl -LsSf https://astral.sh/uv/install.sh | sudo env UV_INSTALL_DIR=/usr/local/bin sh
  fi
  if [ ! -x /usr/local/bin/minio ]; then
    sudo curl -fsSL -o /usr/local/bin/minio "https://dl.min.io/server/minio/release/linux-amd64/${MINIO_RELEASE}"
    sudo chmod +x /usr/local/bin/minio
  fi
  if [ ! -x /usr/local/bin/mc ]; then
    sudo curl -fsSL -o /usr/local/bin/mc "https://dl.min.io/client/mc/release/linux-amd64/${MC_RELEASE}"
    sudo chmod +x /usr/local/bin/mc
  fi
fi
export PATH="/usr/lib/postgresql/16/bin:/usr/local/bin:$PATH"

echo "==> [2/7] Initializing pipecat submodule"
git submodule update --init --recursive

echo "==> [3/7] Creating/refreshing Python venv (python3.13)"
if [ ! -x venv/bin/python ]; then
  python3.13 -m venv venv
fi
# shellcheck disable=SC1091
source venv/bin/activate
uv pip install -r api/requirements.txt -r api/requirements.dev.txt

echo "==> [4/7] Installing pipecat with provider extras (editable)"
# Mirror the devcontainer image: install pipecat from the local submodule with
# every provider extra the app can use, swap opencv for the headless build
# (the X11/Qt-linked wheel fails to import without those libs), pre-fetch the
# NLTK tokenizer, then re-register pipecat editable so source edits take effect.
uv pip install "$ROOT/pipecat[cartesia,deepgram,openai,elevenlabs,groq,google,azure,sarvam,soundfile,silero,webrtc,speechmatics,openrouter,camb,mcp,inworld,smallest]"
uv pip install --group "$ROOT/pipecat/pyproject.toml:dev"
uv pip uninstall opencv-python >/dev/null 2>&1 || true
# Match pipecat's own opencv-python pin (>=4.11.0.86,<5). Leaving this
# unconstrained pulls the opencv 5.x prerelease, which drops constants the
# pipecat smallwebrtc transport imports (e.g. cv2.COLOR_YUV2RGB_I420).
# --reinstall is required for idempotence: opencv-python and
# opencv-python-headless ship the same `cv2` module, so uninstalling the
# former deletes cv2's files; without --reinstall a re-run treats the headless
# metadata as already satisfied and leaves `import cv2` broken.
uv pip install --reinstall "opencv-python-headless>=4.11.0.86,<5"
python -c "import nltk; nltk.download('punkt_tab', download_dir='$ROOT/venv/nltk_data', quiet=True)"
uv pip install -e "$ROOT/pipecat" --no-deps

echo "==> [5/7] Installing node dependencies (ui + ts_validator, node 24)"
export NVM_DIR="$HOME/.nvm"
if [ ! -s "$NVM_DIR/nvm.sh" ]; then
  curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
fi
set +u
# shellcheck disable=SC1091
. "$NVM_DIR/nvm.sh"
nvm install 24 >/dev/null 2>&1 || true
set -u
export PATH="$NVM_DIR/versions/node/$(nvm version 24)/bin:$PATH"
node --version
npm ci --prefix ui
npm ci --prefix api/mcp_server/ts_validator

echo "==> [6/7] Creating local .env files (localhost hostnames)"
# Everything runs on localhost in the Cloud Agent VM, so the *.example files
# are used verbatim (unlike the devcontainer, which rewrites hostnames to the
# docker-compose service names).
[ -f api/.env ]      || cp api/.env.example api/.env
[ -f api/.env.test ] || cp api/.env.test.example api/.env.test
[ -f ui/.env ]       || cp ui/.env.example ui/.env

echo "==> [7/7] Initializing Postgres data directory"
mkdir -p "$SVC/pgdata" "$SVC/redis" "$SVC/minio" "$SVC/logs" "$SVC/run"
if [ ! -f "$SVC/pgdata/PG_VERSION" ]; then
  echo postgres > /tmp/pgpw
  initdb -D "$SVC/pgdata" -U postgres \
    --auth-local=trust --auth-host=scram-sha-256 --pwfile=/tmp/pgpw
  rm -f /tmp/pgpw
  {
    echo "listen_addresses = 'localhost'"
    echo "port = 5432"
    echo "unix_socket_directories = '$SVC/run'"
  } >> "$SVC/pgdata/postgresql.conf"
fi

echo "Install complete."
