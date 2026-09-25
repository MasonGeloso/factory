---
name: factory-initiative-start
description: Bootstrap a new "initiative listener" — a persistent, per-channel conversational agent that will run in its own terminal, take ad-hoc feedback and requests on one Slack/Discord channel, and drive them through a light version of the factory pipeline. Interviews the user for the channel (existing or new), scouts what the bot can actually do in it (post, upload, read-since-timestamp), asks the initiative's scope and its deploy behavior, assigns a slug, writes `factory/initiatives/<slug>.md` and a row in `factory/initiatives.md`, then hands off into `factory-initiative-listen`. Use when the user says "start an initiative", "set up a channel listener", "factory initiative start", or wants a dedicated agent watching one channel for one area of work.
---

# Factory — Initiative Start

*Give one channel a dedicated agent. Run this once per initiative, in a fresh terminal — the terminal
it finishes in is the one you'll leave running `factory-initiative-listen` all day.*

This is the bootstrap half of the initiative-listener pattern. The other half,
[`factory-initiative-listen`](../factory-initiative-listen/SKILL.md), is what actually stays open and
answers messages — read that skill too so you understand what you're setting up. There is also one
singleton, cross-initiative agent, [`factory-listener`](../factory-listener/SKILL.md), which is not
started here (it bootstraps itself the first time it runs).

---

## Step 0 — Config check

1. Locate `factory/` at the repo root. If it doesn't exist, tell the user to run `/factory-intake`
   first — this pattern is a later capability, not the entry point.
2. Check for `factory/communication.md`. If missing, this repo has never talked to a chat medium
   before — delegate to [`factory-communication-setup`](../factory-communication-setup/SKILL.md) for
   just the **medium / auth / credential** part (you still ask this initiative's own channel and
   scouting questions below; don't let that skill also try to own the per-initiative pieces). If it
   exists, **reuse its medium and credential** — don't stand up a second bot/token for the same org
   unless the user says this initiative genuinely needs a different one.
3. Check for `factory/initiatives.md`. If missing, create it from
   [templates/initiatives.md](templates/initiatives.md) — this registers the module (see the
   `factory-onboard` module registry).
4. Check `factory/deployment.md` — you'll need it in Step 4.

## Step 1 — Channel: existing or new

Ask the user:
- **Existing channel** this initiative should live in, or a **new one to create**?
- If new: can the bot create channels on this medium? If yes, create it (name it after the
  initiative, e.g. `#translations`); if not, ask the user to create it and hand you the ID.

Get the channel's ID/handle either way — don't proceed on a name alone.

## Step 2 — Scout the channel

Before trusting this channel for real work, actually try the things a listener will need to do,
using the medium's real API/CLI (never guess):
- **Post a plain message** — confirm it lands.
- **Upload a file or image** — confirm the exact call that works (this is usually a *different* API
  call from posting text — don't assume the same one covers both).
- **Read since a timestamp** — confirm the fetch-since-timestamp / pagination shape works, matching
  `communication.md`'s read-protocol pattern if that file exists, or documenting it fresh here if not.
- Note anything that **doesn't** work (e.g. no file upload permission) — the listener needs to know
  its own limits rather than discover them mid-task.

Record all of this — it goes straight into the identity doc in Step 5.

## Step 3 — Scope

Ask what this initiative owns: one feature area (e.g. "translations on the retail site"), a whole
small app/service, or — rare, and normally reserved for `factory-listener` — "everything." Get a
one-line scope statement concrete enough that a fresh session could read it and know what's in vs.
out.

## Step 4 — Deploy behavior

This decides how `factory-implement-light` closes the loop on every task for this initiative. Ask,
unless `factory/deployment.md` already answers it unambiguously for this exact scope:

- **Deploy straight to a dev environment** the user can audit any time (describe the environment and
  how to reach it) — no ask needed per change, or
- **Show proof and ask first** — post a screenshot/artifact/log to the channel and wait for a
  go-ahead before deploying.

Record the answer on **this initiative**, not globally — a sibling initiative in the same repo may
answer differently (e.g. one service has a real dev environment, another doesn't yet).

## Step 5 — Assign a slug, write the files

1. Pick a short slug (kebab-case, e.g. `translations`, `user-onboarding`). Check it isn't already a
   row in `factory/initiatives.md`.
2. Write `factory/initiatives/<slug>.md` from [templates/initiative.md](templates/initiative.md),
   filled concretely with everything from Steps 1–4. Leave the Queue and Running log sections
   started but empty — the listener fills those as it runs.
3. Add a row for it to `factory/initiatives.md`.
4. Make sure `factory/.gitignore` ignores `.state/` (same as the AI PM's watermark — the listener
   will create `factory/.state/initiative-<slug>.json` on its first run).

## Step 6 — Hand off

Show the user the written identity doc and registry row, confirm it's right, then tell them to run
`/factory-initiative-listen <slug>` — in this terminal, right now, or in a fresh one later. This skill's
job ends at the handoff; it does not itself loop or listen.

**Started by `factory-listener` on the user's request?** Then the listener does the handoff too: it
launches `factory-initiative-listen <slug>` as a separate session in a new multiplexer tab and
verifies it came up. That pattern, and its answers to Steps 1–4 when the user wants it unattended,
are in [`factory-listener/references/spin-up-initiative.md`](../factory-listener/references/spin-up-initiative.md).
