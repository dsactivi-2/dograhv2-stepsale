# Cursor marketplace (DograhV2)

This directory is the Cursor plugin marketplace for this repo. The marketplace
lists the `dograhv2` plugin. Skill text stays in [`.agents/skills/`](../.agents/skills)
(single source of truth); the manifests only publish those paths.

## Install

### Local development (this checkout)

```bash
mkdir -p ~/.cursor/plugins/local
ln -sfn "$(git rev-parse --show-toplevel)" ~/.cursor/plugins/local/dograhv2
```

Reload Cursor (`Developer: Reload Window`), then open **Customize** and confirm
the `dograhv2` plugin and its skills.

### From GitHub

1. Add this repository as a Cursor marketplace
   (`cursor-agent plugin marketplace add dsactivi-2/dograhv2-stepsale`, or
   Dashboard → Settings → Plugins → Import Marketplace).
2. Install the `dograhv2` plugin (Customize, or the interactive `/plugin` flow).
3. Start a new agent session so the skills load.

This is **not** the official Dograh setup plugin
([`dograh-hq/dograh-plugins`](https://github.com/dograh-hq/dograh-plugins)),
which still covers Claude Code / Codex deploy-and-doctor flows.

## What's published

| Skill | When to use |
| --- | --- |
| `dograhV2` | Build or extend platform code, MCP, workflows, or the Knowledge Loop |
| `review-pr` | Review a Dograh PR / diff for repo-specific risks |
| `review-agents-md` | Audit `AGENTS.md` drift and ownership boundaries |

## Edit rules

- Change skill behavior in `.agents/skills/<name>/SKILL.md`.
- Add a new published skill by creating that directory (folder discovery).
- Update `plugin.json` / `marketplace.json` only when names, metadata, or
  discovery paths change.
