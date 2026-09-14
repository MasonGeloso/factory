# Factory — Prototype Onboarding

Run when `factory/prototype.md` is missing and `/factory-onboard` or `factory-prototype` needs it.
This module is **optional** — a repo can run Factory forever without it. It only matters the first
time someone wants to prototype a task before building it for real.

Ask in small batches (AskUserQuestion where it fits).

## 1. Real data access

The whole point of a prototype is that it reads true — rooted in data that actually looks like
production, not hand-invented fixtures.

- **Is there a safe, read-only way to pull production-shaped data** for a throwaway prototype? Options,
  roughly in order of preference:
  - A read-only replica or reporting DB.
  - A staging environment seeded from a recent (possibly anonymized) production snapshot.
  - An existing anonymized/sample dataset already used for demos or local dev.
  - None of the above — prototypes fall back to realistic hand-authored seed data, and must say so
    explicitly whenever they do.
- Get the **exact command/connection** to use (a query, a script, an env var pointing at a read
  replica, an existing fixture-loading command). This is what `factory-prototype` runs — don't leave
  it to be reinvented per task.
- **What's strictly off-limits:** PII columns/tables that must never appear even in a disposable
  branch, any write path, any production credential that isn't read-only. Be explicit — this file is
  read before every prototype run.

## 2. Worktree / branch convention

- Confirm the worktree base dir matches `factory/deployment.md` (reuse it; don't ask again if that
  file already exists). If there's no `deployment.md`, ask for one now (a temp dir is fine for
  prototypes even if the real implementation later needs something sturdier).
- Confirm the branch prefix: default is `prototype/<task-id>-<slug>`. Ask if this project wants a
  different convention (e.g. to keep it out of a branch-protection pattern that would otherwise
  trigger CI on push).
- Confirm: prototype branches are **pushed but never opened as a PR**. Note anywhere else this needs
  to be true (e.g. a CI rule that would otherwise run full test/deploy pipelines on every push).

## 3. Backend diagram convention

- Default is Mermaid (ER diagram for schema before/after, flowchart for the job/trigger DAG),
  published as an Artifact — Artifacts render Mermaid natively, no extra tooling. Confirm this is fine,
  or note an existing house convention (a different diagramming tool, an existing docs style) to match
  instead. Whatever is chosen, it should stay the **same every time** — the user explicitly wants one
  consistent visual language across prototypes, not a novel diagram style per task.

## 4. How the user reviews a frontend prototype

- Will the user click through a **live dev server** themselves (needs `factory/deployment.md`'s run
  instructions to actually work for a prototype branch), or should `factory-prototype` drive it via
  browser automation and hand back screenshots/a short clip?
- If live: any quirks specific to running a *second*, throwaway instance alongside a real one (ports,
  shared DB, etc.) — usually already covered by `factory/deployment.md`'s "concurrent instances" /
  "piggyback rules" sections; point at those instead of re-asking.

## 5. Write, confirm

Write `factory/prototype.md` from the template, filled concretely. Show the user and confirm before
the first `factory-prototype` run relies on it.
