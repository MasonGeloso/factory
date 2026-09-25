---
name: factory-prototype
description: Before building a task for real, produce a disposable, no-corners-cut prototype of what "done" looks like — a fully designed, animated, production-shaped UI on a throwaway branch for frontend-facing work, or a concise before/after schema diagram + job DAG + per-job TLDR for backend-shaped work. Lets the user react to the actual thing (not a wireframe, not a description) and catch both design taste and functionality misunderstandings while they're still cheap to fix. The prototype is reference-only — real implementation is built fresh, using it and its correction notes as the spec for intent, not as code to inherit. Standalone skill, invoked by hand between planning and building. Use when the user says "factory prototype", "prototype this", "mock this up before we build it", or wants to see the UI/shape before committing to an implementation.
---

# Factory — Prototype

*Show what "done" looks like before building it for real, so design and functionality
misunderstandings get caught while they're still cheap.*

This exists because of two specific failure modes:

1. **No artifact to react to.** Without seeing an actual candidate UI, taste stays unstated until
   the real thing ships — and the real thing is usually a letdown, because "make it look nice" never
   got pinned down to anything concrete.
2. **A wireframe handed off as if it were the spec.** Passed a rough sketch, an implementation either
   over-indexes on it pixel-for-pixel (including things that were never meant to be literal) or
   under-builds it — generic cards, generic tables, whatever the nearest stock component is — treating
   the wireframe as a layout suggestion instead of an intentional design to actually build.

The fix for both is the same: stop describing the end state and **build it**, with full effort, before
committing to the real implementation. A front end is also the clearest evidence of whether the
intended *functionality* was understood — seeing the end state surfaces "that's not what I meant" far
earlier and far more cheaply than discovering it after the real build.

## When to use

Invoke this **by hand**, typically after [`factory-plan`](../factory-plan/SKILL.md) has produced a
plan (not required — it can run directly off an issue link or a raw description) and before
[`factory-execute`](../factory-execute/SKILL.md) / [`factory-implement`](../factory-implement/SKILL.md)
builds the real thing. It is not wired into the `factory-implement` driver — decide per task whether
you want to see it first.

Good candidates: any task with a real UI surface, or a backend task whose final data shape or job
graph isn't already obvious from the codebase. Skip it for changes with an already-unambiguous shape
(a bug fix, a parameter tweak, a one-line logic change) — there's nothing to usefully prototype.

## Two tracks — pick whichever the task actually has

- **Frontend track** — a real, finished-feeling, animated UI, wired to production-shaped data, on a
  disposable branch.
- **Backend track** — a concise before/after schema diagram, a DAG of the jobs/triggers involved, and
  a plain TLDR of each job's current vs. final behavior, published as an Artifact.

A task can need both (e.g. a feature with both a new UI and a new pipeline behind it). Read the
task/plan to decide which track(s) apply; ask the user if it's genuinely ambiguous.

## Step 0 — Load context

- `factory/deployment.md` and `factory/codebases.md` (if this repo has them) — reuse the existing
  worktree base dir and run/stack instructions rather than inventing new ones.
- `factory/prototype.md` — this module's own config: where real, production-shaped data can safely be
  read from, what's off-limits, and the diagram convention for the backend track. **If it's missing,
  self-onboard it now** using [onboarding.md](onboarding.md) before continuing — do not guess at data
  access.
- The task/issue, and the `factory-plan` doc if one exists, including every comment. Pull in any
  wireframes, sketches, or reference screenshots the user attached — treat them as **evidence of
  intent, not a literal layout to trace**. The point of this skill is to actually design the thing
  well using that intent, not to reproduce a sketch at higher fidelity.

## Frontend track

1. **Worktree + branch.** Create (or reuse) a worktree per `factory/deployment.md`'s convention.
   Branch off the base branch as `prototype/<task-id>-<slug>`. This is a **separate, disposable**
   worktree — not the eventual feature worktree.
2. **Data.** Pull real, production-shaped data through whatever safe read-only path
   `factory/prototype.md` names. Minimize hand-authored seed data — only fill gaps the real source
   genuinely can't cover, and say explicitly which fields were fabricated versus real.
3. **Design it, don't lay it out.** Read the repo's existing design system/components first. Where the
   task needs something the system doesn't already have, design it properly — call the Skill tool for
   [`factory-frontend`](../factory-frontend/SKILL.md) for aesthetic direction, typography, motion, and
   its pre-ship polish pass. Default to the effort level Factory expects from any new UI work: highly
   visual, deliberately animated, built from design first principles — not the safest, most generic
   version of the screen. No half-built states, no placeholder components standing in for the real
   design decision.
4. **Build against the real app shell** — real routing, real layout, real state — not an isolated
   component sandbox. It needs to read as "this is what's shipping," not a mood board.
5. **Show it live.** Stand it up per `factory/deployment.md`'s run instructions and hand the user a
   URL to click through themselves. If there's genuinely no way to do that, drive it yourself via
   browser automation and capture screenshots (and a short clip if useful) instead — reuse
   [`factory-demo-video`](../factory-demo-video/SKILL.md)'s screenshot/`artifacts.md` conventions so
   it's reviewable without a live session.
6. **Push the branch. Do not open a PR.** Nothing on this branch is meant to merge.
7. **Review together and capture two kinds of feedback**, explicitly labeled as such:
   - **Design/UX corrections** — layout, hierarchy, motion, taste.
   - **Functionality/behavior corrections** — places where the prototype reveals a misunderstanding
     of what the feature is actually supposed to do. These are corrections to the *requirements*, not
     cosmetic notes — flag them clearly, since they change what the real implementation must build.
8. Iterate (revise → re-show) until the user approves.

## Backend track

1. Read the plan/task and scope exactly which tables and jobs are actually touched — no wider.
2. Produce, as a single Artifact, using the **same diagram convention every time** (per
   `factory/prototype.md`, default: Mermaid ER diagram + Mermaid flowchart — Artifacts render Mermaid
   natively):
   - A **before/after schema diagram** — only the tables/columns that change.
   - A **DAG of the jobs/triggers** involved in this change.
   - A **one-paragraph TLDR per job**: what it does today, what it will do after.
   - If the task also has an API/CLI surface, add real vs. proposed call/response examples using
     production-shaped payloads (same data-access rule as the frontend track).
3. Review with the user the same way as the frontend track — capture design-of-the-shape corrections
   and functionality corrections separately.

## Output contract

Every prototype run ends with:

- **Frontend:** a pushed `prototype/<task-id>-*` branch (the worktree itself can be discarded once
  pushed), plus screenshots/clip if no live walkthrough was possible.
- **Backend:** a published Artifact holding the diagrams and TLDRs.
- **Either way:** a short **Prototype notes** section appended to the plan doc (or a new
  `tasks/<task-id>-prototype-notes.md` if no plan exists), recording: what was validated, every
  functionality correction that came out of the review (now a requirement, not a nice-to-have), and
  an explicit line that the branch/Artifact is a **disposable reference**, not a base to build on.

## Reference-only — not a seed for the real build

State this plainly to whoever picks up the real implementation: **do not build on top of the
prototype branch's commits.** It exists to settle a decision, not to ship. Wire the real logic against
the real backend and data layer from scratch, using the prototype and its correction notes as the
spec for intent — not as code the real feature inherits. This keeps prototype shortcuts (fabricated
data, skipped auth, hardcoded states) from leaking into what actually ships.

## Relationship to the rest of the pipeline

Suggested sequence: `factory-plan` → `factory-prototype` (this skill, optional) → `factory-execute` /
`factory-implement`. This skill is **not** invoked automatically by the `factory-implement` driver —
run it yourself, by hand, when you want to see the end state before telling the driver to build it.
