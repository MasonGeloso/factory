---
name: factory-initiative-listen
description: Run as a persistent, per-channel conversational agent for one initiative — the loop that actually stays open all day. Takes a `<slug>` argument, reads that initiative's identity doc and watermark to resume, then watches its dedicated channel with a background Monitor that wakes the session the moment someone posts, triages each new message (small/medium → `factory-implement-light`, big → spawn a sub-agent via `/goal /factory-implement`, out-of-scope emergency → spawn and monitor a sub-agent, pure question → just answer), and replies concisely in the channel's own style. Invoked by hand in its own terminal after `factory-initiative-start`, or to resume a lost session. Use when the user says "factory initiative listen <slug>", "resume the <slug> listener", or points at an already-bootstrapped initiative.
---

# Factory — Initiative Listen

*Stay open. Watch one channel. Take whatever comes, in order, and ship it — light by default, escalate
when it's genuinely big.*

This is the persistent half of the initiative-listener pattern. `factory-initiative-start` sets an
initiative up once; this skill is what you actually leave running in a terminal, potentially for days,
resumed as many times as it gets lost. It is **not** a cron agent — see the note at the bottom on why
this doesn't live under `bin/factory agents`.

Requires a `<slug>` argument identifying an already-bootstrapped initiative (a row in
`factory/initiatives.md`). If none was given, or the slug isn't in the registry, stop and tell the user
to run `/factory-initiative-start` first — do not invent an initiative.

---

## Step 0 — Resume

1. Find `factory/` at the repo root. Read `factory/initiatives.md` and confirm `<slug>` is a row in it.
2. Read `factory/initiatives/<slug>.md` **in full** — identity, scope, channel, capabilities, deploy
   behavior, pipeline-mode bar, the Queue, and the Running log. This is the entire briefing a fresh
   session gets; there is no chat history to fall back on. Treat any open Queue items as still pending.
3. Read `factory/.state/initiative-<slug>.json` for the watermark (`last_read`). Shape, same as the AI
   PM's state file:
   ```json
   { "last_read": "2026-09-20T18:04:00Z", "runs": [ { "at": "...", "messages": 3, "actions": ["..."] } ] }
   ```
   No file yet → first run for this initiative; use a short look-back (default: since `Started` in the
   identity doc, or 24h, whichever is shorter) instead of ingesting all history.
4. Read `factory/deployment.md`, `factory/codebases.md`, and `factory/code-review.md` if present — the
   same execution config `factory-implement` reads, since `factory-implement-light` will need it.

## Step 1 — Watch, don't poll (the actual loop)

**A Monitor is the wake signal; `ScheduleWakeup` is only a fallback heartbeat.** Do not build this
as a timer that wakes up and checks. A conversational channel is quiet most of the time and then
urgent for ten minutes — a poll is simultaneously too slow when it matters and pure overhead when it
doesn't. A Monitor streams one event per message and wakes the session in seconds.

**Arm the watch.** `scripts/watch_channel.py` sits next to this SKILL.md and is the Slack reference
implementation; the cwd is the target repo, so use an absolute path. Give it this initiative's own
mark file — never one shared with another listener:

```
Monitor(
  command: python3 "$SKILL_DIR/scripts/watch_channel.py"
             --channel <id from the identity doc> --label '#<channel>'
             --mark ~/.factory/initiative-<slug>.mark --env-file <where the token lives>,
  description: "new messages in #<channel>",
  timeout_ms: 1800000,
)
```

If the channel isn't Slack, write the equivalent for its API and keep the same contract: one stdout
line per new human message, bots and already-seen messages filtered out *in the script*, a
six-decimal-safe watermark persisted to the mark file, and a swallowed exception per request so one
blip doesn't end the watch. Read `factory/communication.md` for the org's protocol first.

**Each time an event wakes you:**

1. **Append every new request to the identity doc's Queue**, in arrival order, even ones you'll start
   on immediately — the queue is the durable record a resumed session reads, not your working memory.
2. **Work the queue FIFO** (see Step 2 for routing). If you're mid-task when new messages arrive,
   keep working the current item to a sane stopping point, append the new ones, and pick them up
   after — never drop or silently reorder a request because a newer one looks more interesting.
3. **Re-arm the fallback.** Call `ScheduleWakeup` with `prompt` set to
   `/factory-initiative-listen <slug>` and `delaySeconds` of **1200–1800** — long, because it is
   insurance against the monitor dying, not the mechanism. Set `noop: true` on a tick that changed
   nothing so quiet holds collapse in the user's terminal.

**Re-arm the Monitor when it expires.** A Monitor lives 30 minutes at most and sends one notice when
it dies. Arm a new one immediately on that notice — that notice is the single most common way one of
these listeners goes silent without anyone realising.

**Never run two watchers on one mark file.** They race, and each swallows messages the other should
have reported. Before arming, check whether one is already running for this initiative (`TaskList`,
or `pgrep -f watch_channel.py`); arm only if not. Beware the false positive when checking with
`pgrep -f`: the shell running your own `pgrep` matches the pattern string too, so confirm with
`ps -o pid,lstart,cmd` before concluding there's a duplicate and killing something.

**Never miss a message.** The script owns the watermark and only advances it after a line is
flushed, so a crash re-reports rather than skips. If the watch dies, re-arm it — the mark file makes
the new watcher resume exactly where the old one stopped. It's fine to reset and restart; it is not
fine to go silent.

Write a short run entry to `factory/.state/initiative-<slug>.json` as you go, same discipline as
`factory-ai-pm`. The message watermark itself lives in the mark file, not here — one owner per
watermark, and it's the script.

**If `Monitor` isn't available** in this environment, fall back to the timer: `ScheduleWakeup` every
few minutes, fetching since the watermark yourself each pass. That is strictly worse, so prefer the
Monitor whenever you have it.

## Step 2 — Triage each queued item

For each item, in order:

- **Pure conversation / question** — just answer. No pipeline, no ceremony.
- **Small/medium change** (the default) — run [`factory-implement-light`](../factory-implement-light/SKILL.md)
  against it. This is what most requests should get.
- **Big lift** — per the identity doc's own bar for "big" (multi-file/multi-day scope, or the user
  explicitly says to spawn one): spawn a sub-agent with the goal pinned, e.g.
  `/goal /factory-implement <fully written-up requirements, built from the conversation, not a paraphrase>`.
  Check in on it periodically; post progress to the channel when it lands or blocks. Do not babysit it
  turn by turn, and do not let it block you from working the rest of the queue.
- **Genuinely out-of-scope emergency** (e.g. an unrelated production incident the user mentions in
  passing) — spawn a sub-agent with clear instructions and monitor it, exactly like the big-lift case,
  so it doesn't derail this session's own scope. Note it in the Running log either way.

Don't rush. The user is coming across things as they see them, not expecting instant turnaround —
thoroughness beats speed here. If you're unsure whether something is small or big, err toward asking
in-channel rather than guessing wrong in either direction.

## Step 3 — Reply like a person in the channel, not a report

**Hard rule, no exceptions:** replies are short. Say the thing and stop — no multi-paragraph write-ups,
no restating the request back, no "Here's what I did:" preambles. Use the medium's native formatting
(Slack/Discord markdown); emojis are fine if they read naturally, not required. If a review gate in
`factory-implement-light` surfaces a borderline finding, post it as a short question and wait for the
answer before proceeding — don't narrate the whole review.

## Step 4 — Keep the identity doc current

Throughout, not just at handoff:
- Move finished Queue items into the Running log (one or two lines — what shipped, links/screenshots
  posted, any decision made without asking).
- Update Identity/Channel-capabilities/Deploy-behavior sections if anything about them turns out to be
  wrong or incomplete — this doc is the resume path, so keep it honest.

This is the same "concise local record, not an essay" discipline `factory-implement` keeps in its own
resume record — the goal is that a brand-new session, reading this file cold, can pick up "to a certain
extent" without the original conversation.

---

## Why this isn't a `bin/factory agents install` cron agent

The scheduled agents (`ai-pm`, `daily-digest`, `weekly-report`) are one-shot: `claude -p "..."
--dangerously-skip-permissions`, re-invoked cold on a schedule, no memory between runs beyond the
watermark file. An initiative listener is the opposite shape on purpose — one long-lived, stateful
session per channel that the user actively converses with, spawns sub-agents from, and can lose and
resume by hand. Forcing that into the cron model would mean re-establishing full context every few
minutes instead of staying warm in one session. Start it, and resume it, by literally running
`/factory-initiative-listen <slug>` in a terminal — the same way `factory-initiative-start` hands off
into it.
