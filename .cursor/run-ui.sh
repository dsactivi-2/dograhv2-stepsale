#!/usr/bin/env bash
# UI terminal: runs the Next.js dev server (Turbopack) on 0.0.0.0:3000 under
# node 24. The runtime injects an older node ahead of nvm on PATH, so the
# node-24 bin directory is prepended explicitly.
set -euo pipefail

cd /workspace/ui
export NVM_DIR="$HOME/.nvm"
set +u
# shellcheck disable=SC1091
. "$NVM_DIR/nvm.sh"
set -u
export PATH="$NVM_DIR/versions/node/$(nvm version 24)/bin:$PATH"
node --version

exec npm run dev -- --hostname 0.0.0.0
