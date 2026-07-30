# Lokaler Stepsales-Test (isoliert)

## Was das ist

- Pfad: `~/Code/Projects/dograhV2-stepsales-local`
- Branch: `local/main-plus-stepsales` = `origin/main` + lokal gemergter `feature/stepsales-sales-api-mvp`
- **Kein Push** nach GitHub — Origin unverändert
- Compose-Projekt: `dograhstepsaleslocal` (eigene Volumes)

## Start

```bash
cd ~/Code/Projects/dograhV2-stepsales-local
export COMPOSE_PROJECT_NAME=dograhstepsaleslocal
export ENABLE_TELEMETRY=false
docker compose -p dograhstepsaleslocal \
  -f docker-compose.yaml -f docker-compose.build-local.yaml \
  up -d --build
```

- UI: http://localhost:3010  
- API: http://localhost:8000/api/v1/health  
- Stepsales: http://localhost:8000/api/v1/stepsales/health  

## Stoppen / Löschen

```bash
# Container + Volumes weg, Repo behalten
docker compose -p dograhstepsaleslocal \
  -f docker-compose.yaml -f docker-compose.build-local.yaml down -v

# Komplett weg (Repo + Images optional)
cd ~/Code/Projects
rm -rf dograhV2-stepsales-local
docker rmi dograh-stepsales-local-api:test dograh-stepsales-local-ui:test 2>/dev/null || true
```

## GitHub

Unberührt. Merge/PR entscheidest du später separat.

## Live-Status (nach lokalem Build)

- API healthy: `GET /api/v1/health` → 200
- Stepsales: `GET /api/v1/stepsales/health` → 200 (`module=stepsales`)
- UI: http://localhost:3010 (oft 307 → Login) — Account lokal anlegen (signup enabled)
- Compose-Projekt: `dograhstepsaleslocal`
- Cloudflared-Warnungen in API-Logs sind OK (Tunnel-Profil nicht gestartet)

### Lokale Patches nur für Build/Preview (nicht für GitHub-Merge gedacht)

- `scripts/start_services_docker.sh` → `alembic upgrade heads`
- `ui/next.config.ts` → `typescript.ignoreBuildErrors` + eslint ignore (Branch hat TS-Drift in AppSidebar)
- kleine TS-Fixes in `LocalUser` / `SidebarTeamSwitcher`-Call

### Was im Browser prüfen

Nach Signup/Login Sidebar: Analytics, Campaign Ops, Costs, QA Center, Training, Scripts, Evals.
