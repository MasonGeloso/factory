# Factory Initiatives — <REPO/SERVICE NAME>

> Registry of active initiative-listener agents — persistent, per-channel conversational agents
> started by `/factory-initiative-start` and kept alive by `/factory-initiative-listen <slug>`,
> run by hand in their own terminal (not a cron agent — see `factory-initiative-listen/SKILL.md`).
> One row per initiative. The singleton triage agent, `factory-listener`, reads this whole file
> to know what already has a dedicated owner before it decides to handle something itself.

| Slug | Channel | Medium | Scope | Deploy behavior | Status |
|------|---------|--------|-------|------------------|--------|
| `<slug>` | #<channel-name> | <Slack \| Discord \| …> | <one line: what this initiative owns> | <deploy-to-dev \| ask-before-deploy> | <active \| paused \| retired> |

- **Identity docs:** `factory/initiatives/<slug>.md` — one per row above, written by `factory-initiative-start`, kept current by that initiative's own listener session.
- **Watermarks:** `factory/.state/initiative-<slug>.json` — gitignored, last-read timestamp + run log, same shape as the AI PM's `.state/ai-pm.json`.
- **Resuming a listener:** in a fresh terminal, run `/factory-initiative-listen <slug>` — it reads this row plus the identity doc and picks back up without full history.
- **Adding a row:** only `factory-initiative-start` adds rows (it also creates the identity doc and scouts the channel). Don't hand-edit a new row into existence — the listener that would own it wouldn't exist.
