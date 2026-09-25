# Marketing Post Dispatcher — English pillar (`marketing-post-en`)

A cron-style Factory agent, sibling to `marketing-post`. Every hour it wakes up, checks the target
project's **English** marketing pillar timetable (`factory/marketing-en/schedule.md`), and fires
whatever content type(s) are due against that pillar's account (`@komori_en` for Komori).

## Why a separate agent instead of a flag on `marketing-post`

`marketing-post` (and the `factory-marketing-post` skill it runs) hardcodes `factory/marketing/`
throughout its own steps and has no parameter for a different root directory. Rather than edit a skill
other repos may also depend on, this is a small, separately named sibling — its own skill
(`factory-marketing-post-en`), its own agent definition, pointed at `factory/marketing-en/` — so a
project can run a second, differently-configured marketing pillar (different account, different
audience, different language) alongside its first without touching the original at all.

## What it does each run

Same shape as `marketing-post`, with one addition: before touching the account switcher, it acquires
a **shared cross-pillar lock** (`factory/.state/x-browser-session.lock`, documented in both pillars'
`platforms.md` files) for the whole tick. Both pillars drive the same physical Chrome profile through
Claude-in-Chrome, so switching the active X account is a global mutation neither pillar's own
per-content-type lock can see across the other — this lock is what prevents a `marketing-post` (JP)
tick and a `marketing-post-en` tick from silently pulling the composer out from under each other.

1. Reads `factory/marketing-en/schedule.md`, `content-types/`, and `platforms.md` for that pillar.
2. Evaluates every scheduled row's gate against the current time in the pillar's own configured
   timezone (deliberately independent of the JP pillar's timezone — see that schedule's own notes).
3. Acquires the cross-pillar lock (wait + reclaim, not a bare skip) before any account-switch attempt,
   holds it through every content type the tick fires, releases it when the tick is done.
4. For each content type that fires: verifies the account, builds the content, runs a de-slop pass,
   and either publishes (`autonomous-publish`) or saves a draft and stops (`draft-only`).
5. Records the outcome to that pillar's own ledger under `factory/marketing-en/.state/`.

Same trivial, identical-everywhere scheduled command as every other Factory agent — it just tells
Claude Code to run the `factory-marketing-post-en` skill (`prompt.md`), with Chrome access
(`needs_chrome: true`).

## Install

```bash
factory agents install marketing-post-en /path/to/repo
```

Requires `factory/marketing-en/platforms.md`, `content-types/README.md`, and `schedule.md` to already
exist (this pillar's own onboarding, done by hand or via `factory-marketing-onboard` pointed at
`factory/marketing-en/`) — the installer's normal auto-onboard fallback assumes `factory/marketing/`
and won't build the right tree for this agent.

## Requirements

- `factory/marketing-en/` already set up in the target repo (a second marketing pillar, distinct
  account/audience from the primary one).
- Claude Code on `PATH`, with Claude-in-Chrome connected and logged into the account this pillar's
  `platforms.md` names.
- The primary pillar's `marketing-post` agent, if also installed, must be running the version of
  `factory-marketing-post`/`platforms.md` that knows about the shared cross-pillar lock — check
  `factory/marketing/platforms.md`'s X section names `factory/.state/x-browser-session.lock` before
  installing this agent alongside it.
- Genuinely optional — a repo with only one marketing pillar never installs this agent.
