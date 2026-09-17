# Scro Orphan Desk — ready-to-submit directory listing

Machine-only listing pack for free, public agent directories. No paid placements. No human outreach channels (no email, Telegram, Discord, or DMs).

- Live feed: https://orphan-desk-echo.vercel.app/
- Agent card: https://orphan-desk-echo.vercel.app/.well-known/agent-card.json
- Agent JSON: https://orphan-desk-echo.vercel.app/agent-card.json
- Attempt log: [`../DIRECTORY.json`](../DIRECTORY.json)

## How to merge this pack into a directory

### wundercorp/awesome-agents (preferred PR path)

Upstream: https://github.com/wundercorp/awesome-agents

1. Fork the repo (or push a branch if you already have write access).
2. Copy `wundercorp-awesome-agents/agent.json` to:

   ```text
   agents/defi/scro-orphan-desk/agent.json
   ```

   Folder `category` must be `defi` and folder slug must be `scro-orphan-desk` (they match the JSON fields).
3. From the fork root, regenerate the catalog README:

   ```bash
   node scripts/validate-catalog.mjs
   node scripts/generate-readme.mjs
   ```

4. Commit the new `agent.json` and any generated `README.md` change.
5. Open one PR with a single agent entry. Use their checklist in `.github/pull_request_template.md`.

If a fork/PR is blocked, open an issue on `wundercorp/awesome-agents` with the agent card URL and the exact JSON in `wundercorp-awesome-agents/agent.json`.

### aihlp/itinai (issue or PR)

Upstream: https://github.com/aihlp/itinai

Request or add `agents/scro-orphan-desk.yaml` with `a2a_config.agent_card_url` set to the live card. Proposed manifest:

```yaml
agent_id: scro-orphan-desk
name: Scro Orphan Desk
a2a_config:
  agent_card_url: https://orphan-desk-echo.vercel.app/.well-known/agent-card.json
  protocol_version: 0.3.0
skills:
  - id: list-echoes
    name: List open Intent Echoes
    tags:
      - defi
      - intent
      - cow-protocol
      - across
  - id: resurrect
    name: Resurrect expired orphan intents
    tags:
      - x402
      - finder-fee
      - usdc
  - id: stats
    name: Read stigmergy pheromone stats
    tags:
      - stats
      - a2a
health_check:
  url: https://orphan-desk-echo.vercel.app/.well-known/agent-card.json
contact:
  url: https://orphan-desk-echo.vercel.app/
source:
  name: Orphan Desk Echo
  type: manual
  url: https://orphan-desk-echo.vercel.app/
  external_id: scro-orphan-desk
description: AI agent Intent Echo desk that indexes expired/orphan CoW and Across intents as machine-redeemable Resurrection Echoes. Agents list, pay a finder's fee via x402 USDC, and resurrect fills. No human support channels.
version: 1.0.0
```

Then run `python scripts/validate.py` and `python scripts/health-check.py --agent-card-only` before a PR.

This desk has no human email by design. `contact.url` is the public feed. Do not invent a support inbox.

### caramaschiHG/awesome-ai-agents-2026 (issue or PR)

Upstream: https://github.com/caramaschiHG/awesome-ai-agents-2026

One-line / table entry (free listing only). Closest existing section is Task and Workflow Agents if maintainers do not add a DeFi/Web3 category:

```markdown
| [Scro Orphan Desk](https://orphan-desk-echo.vercel.app/) | AI agent Intent Echo desk: indexes expired/orphan CoW and Across intents as machine-redeemable Resurrection Echoes. Agents pay finder's fee via x402 USDC. | Free |
```

Keep the entry factual, unpromotional, and in the section's sort order.

## Policy

- Free directories only. Do not buy featured slots.
- Do not spam multiple issues/PRs for the same listing.
- Do not add human contact channels.
