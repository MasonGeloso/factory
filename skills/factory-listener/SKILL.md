---
name: factory-listener
description: The one general-purpose, cross-initiative triage agent — a persistent conversational listener on its own channel that knows about every initiative in `factory/initiatives.md` and either routes a request into the right initiative's channel (for that initiative's own `factory-initiative-listen` to pick up) or, if it's small and general with no dedicated owner, handles it itself via `factory-implement-light`. A singleton per repo: bootstraps its own channel the first time it runs instead of going through `factory-initiative-start`. Use when the user says "factory listener", "start the general listener", "run the triage agent", or wants one catch-all entry point for bugs, ideas, and paper-cuts that don't belong to a specific initiative.
---

# Factory — Listener (the general triage agent)

*One inbox for everything that doesn't already have an owner. Route what belongs somewhere else; handle
what doesn't.*

This is the special case of the initiative-listener pattern — read
[`factory-initiative-listen`](../factory-initiative-listen/SKILL.md) first, since this skill reuses
almost everything from it (the poll/reschedule loop, the FIFO queue, the concise reply style, the
big-lift/emergency sub-agent escalation). What's different here is **scope: everything**, and the
**routing step** before triage.

There is exactly one of these per repo. It is not started via `factory-initiative-start` — bootstrap it
inline, below, the first time it runs.

---

## Step 0 — Bootstrap or resume

- **First run** (no `factory/initiatives/general.md` yet, or the user is explicitly setting this up):
  ask the same channel questions `factory-initiative-start` would (existing channel or new, scout it —
  post/upload/read-since-timestamp), then write `factory/initiatives/general.md` from
  [`factory-initiative-start`'s template](../factory-initiative-start/templates/initiative.md) with
  **Scope: everything not owned by a dedicated initiative**, and add its own row to
  `factory/initiatives.md` (slug: `general`, or whatever the user prefers). There's no per-initiative
  deploy-behavior decision to make in the same way — if this agent ends up handling something itself,
  it uses that thing's own `factory/deployment.md` config the same way any `factory-implement-light`
  run would.
- **Resume**: read `factory/initiatives/general.md` and its watermark
  (`factory/.state/initiative-general.json`) exactly as `factory-initiative-listen` Step 0 describes.

**Also read `factory/initiatives.md` in full, plus every `factory/initiatives/<slug>.md` it lists** —
unlike a scoped initiative listener, this one needs to know what every other initiative already owns
before it can decide whether to route or handle. Re-read the registry each poll pass in case a new
initiative was added since the last one.

## Step 1 — Poll and reschedule

Identical mechanism to `factory-initiative-listen` Step 1: fetch since the watermark, append to this
initiative's own Queue, reschedule via `ScheduleWakeup` (`prompt: "/factory-listener"`,
falling back to a `Bash` sleep loop or `/loop` if unavailable), never miss a message, never advance the
watermark past what was actually processed.

## Step 2 — Route, or handle

For each item, in order:

1. **Does it clearly belong to an existing initiative** (matches one row's Scope in
   `factory/initiatives.md`)? **Route it**: post the request into that initiative's channel, in your
   own concise style, crediting who asked — then stop. That initiative's own `factory-initiative-listen`
   session picks it up from its channel; do **not** also do the work here. If you're not sure it's
   actually running right now, still post it — the queue mechanism means it'll be there whenever that
   session resumes.
2. **Is it general** — a small paper-cut, a bug, a UI tweak, a question, nothing that maps to a
   specific initiative's scope? **Handle it yourself**, same triage `factory-initiative-listen` Step 2
   uses: pure question → answer; small/medium → `factory-implement-light`; big or an out-of-scope
   emergency → spawn and monitor a sub-agent via `/goal /factory-implement`.
3. **Is it a new initiative-shaped thing** — sizable, ongoing, would benefit from its own dedicated
   channel and agent? **Don't create it on your own initiative.** Say in-channel that it looks like it
   deserves its own initiative and offer to set it up. This agent triages; it doesn't spin up standing
   agents because work *looks* big.
   - **When the user asks** ("make an initiative for X", "spin up an agent for X") or accepts the
     offer, **do the whole thing yourself**: run `factory-initiative-start` for them, creating and
     scouting the channel, writing the identity doc with their request as the first Queue item, and
     adding the registry row. Then **hand off to a separate, long-lived session** that runs
     `factory-initiative-listen <slug>` in a new terminal-multiplexer tab (Herdr or tmux). Verify it
     started, and tell the user which channel to talk in. Full, tested pattern:
     [references/spin-up-initiative.md](references/spin-up-initiative.md).

## Step 3 — Reply style and record-keeping

Same hard rules as `factory-initiative-listen`: short, native-formatted replies, no report-shaped
write-ups. Keep `factory/initiatives/general.md`'s Queue and Running log current the same way, including
routing decisions ("routed to #translations, asked by X") so a resumed session doesn't re-triage
something it already sent elsewhere.
