# Factory Prototype — <PROJECT NAME>

> Config for the `factory-prototype` skill — an optional, hand-invoked step that builds a disposable,
> full-effort preview of a task's end state (UI or backend shape) before real implementation starts.
> Filled during onboarding. This module has no "Enabled: no" state — if this file is missing,
> `factory-prototype` just self-onboards it the first time it's needed.

## Real data access
- **Source:** <e.g. "read-only Postgres replica, `DATABASE_URL_REPLICA` in .env.prototype" | "staging
  DB seeded nightly from an anonymized prod snapshot" | "none — fall back to realistic hand-authored
  seed data and say so explicitly">
- **Exact command/connection:** <the literal command, script, or env var to use>
- **Off-limits:** <PII columns/tables that must never appear, even disposably; any write path; any
  credential that isn't read-only>

## Worktree / branch
- **Worktree base:** <reuse `factory/deployment.md`'s base dir unless noted otherwise>
- **Branch prefix:** <default: `prototype/<task-id>-<slug>`>
- **Never opens a PR.** <note any CI rule that would otherwise fire on push to a `prototype/*` branch>

## Backend diagram convention
- **Format:** <default: Mermaid ER diagram (schema before/after) + Mermaid flowchart (job/trigger
  DAG), published as an Artifact>
- **Keep it consistent:** whatever is chosen here should look the same across every prototype — no
  novel diagram style per task.

## Frontend review mode
- **Mode:** <`live` — user clicks through a dev server themselves | `driven` — Claude drives it via
  browser automation and hands back screenshots/a clip>
- **Concurrent-instance notes:** <point at `factory/deployment.md`'s "concurrent instances" /
  "piggyback rules" sections if this repo has them; otherwise note anything prototype-specific>

## Notes
<Anything else worth knowing — e.g. a design system doc to read first, a past prototype that set a
visual bar worth matching.>
