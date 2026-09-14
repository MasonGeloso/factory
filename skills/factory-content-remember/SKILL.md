---
name: factory-content-remember
description: Given one finished piece of marketing content and feedback about what's wrong with it, track down the session that produced it, pull the actual published/drafted text, diagnose which step of the pipeline let the defect through, and propose (never auto-write) a checkable rule for `factory/content-review.md` or the content type's own doc. The content-side counterpart to `factory-remember`, but scoped to the marketing pillar's own gates — never writes into the software-factory gates (`factory/plan-review.md`, `factory/code-review.md`, `factory/qa.md`). Use when the user says "factory content remember", "diagnose this post", "why did this post do X", "content postmortem", or gives feedback on a specific published or drafted piece of content and wants the root cause turned into a standing rule.
user-invocable: true
---

# Factory — Content Remember

*A post shipped with something wrong in it. Before fixing that one post, find the session that made
the choice, name the exact step that made it, and turn it into a rule the next run of that content
type can't miss — without touching the software-factory gates, which are a different system reviewing
a different kind of artifact.*

The incident is the **trigger**. The rule is the **deliverable**. Write the rule as if the reader has
never heard of this post, because on the next run they haven't.

---

## Inputs required before starting

- **Which post.** Enough to find it uniquely: content type + date, or ticker, or a URL (X/note.com),
  or a path under `marketing-archive/`. If ambiguous, ask — don't guess which of several posts on the
  same day the feedback is about.
- **The feedback itself, verbatim.** Not your paraphrase of it. What's wrong, as the user said it.

If either is missing, ask. Do not start archaeology on a guess.

## Step 1 — Find the producing session

Some content types log a session id directly; most don't. Try in order, stop at the first hit:

1. **Logged session id.** Check the content type's `marketing-archive/<type>/LEDGER.md` row and any
   per-run evidence folder (e.g. `marketing-archive/mcp-use-case-articles/<run>/evidence/`) for a
   `session_...` id.
2. **Transcript search by time + content.** Claude Code session transcripts for this repo live at
   `~/.claude/projects/-home-hone-code-senki/*.jsonl` (or `-home-hone-code-senki-<worktree>` for a
   worktree run), one file per session, named by session id, `mtime` ≈ when the session ended. Narrow
   by the post's date, then `grep -l` the candidate files for a distinctive phrase from the post
   (headline, ticker, a sentence fragment) or the content type's own trigger phrase (e.g.
   `factory-marketing-post`, `reply-radar`, `thread-stories`) — the first line of a cron-fired session
   is often a `queue-operation`/`ai-title` entry naming exactly which skill ran.
3. **Confirm the match.** Read enough of the transcript to see it produced *this* post, not just a
   session that ran the same content type on a different day — check the final drafted text in the
   transcript against the actually-published text.

If no session can be found, say so plainly and stop — do not diagnose from the finished text alone;
half the point is seeing what the pipeline actually did, not guessing backward from the output.

## Step 2 — Pull the real artifact

Read the finished piece **verbatim, as published** (the X post, the note.com article, the ledger row's
actual text) — not a summary of it, not the draft two revisions before final if a later revision
shipped. Read the source-material packet the session gathered too, if the content type builds one
(filing figures, screenshots, evidence files) — you need it to tell whether the defect was a bad
source, a bad read of a good source, or a bad call with the right source in hand.

## Step 3 — Diagnose against the transcript

Walk the transcript to the specific decision that produced the flaw. State it at the level of "at
step X, given evidence Y, the session chose Z" — not "the model made a mistake." Concretely locate it
against:

- The content type's own build steps in `factory/marketing/content-types/<type>.md` — did a step that
  should have caught this exist and get skipped, or does the step simply not check for this class of
  thing?
- `factory/content-review.md`, if `factory-content-review` ran on this piece — did the review run at
  all, and if it did, why didn't its checklist catch this?
- A one-off judgment call with no doc governing it either way — the honest diagnosis is then "no rule
  exists yet," not "a rule was ignored."

## Step 4 — Propose the rule (dry run — nothing is written yet)

Output a tl;dr, in this shape:

```
WHAT WENT WRONG: <one or two sentences, plain language>
WHERE: <session <id>, step <name> in <file>>
WOULD NOT HAVE HAPPENED IF: <the exact bullet, in the format below>
```

The proposed bullet follows the same discipline as `factory-remember`'s rule format:

- **Bolded imperative title**, then 1–4 lines: what to look for (or what to do while drafting), plus
  the legitimate exception inline if there is one.
- **Never reference the originating post.** No dates, no ticker, no "like the 4967 piece" — a rule
  that needs its incident re-read to be usable will not get used.
- **Name real symbols and verify them first** — file paths, config keys, ledger columns — `grep` them
  before writing them down.
- **One check per bullet.**
- **Write the check, not the fix.** "Every quantified claim in the body has a matching line in the
  evidence packet" is a check. "Be more careful with numbers" is not.

**Pick the right home**, and say which one and why:

| Rule is about... | Goes in |
|---|---|
| something checkable only by reading the **finished piece** (accuracy, tone, a claim vs its source) | `factory/content-review.md` |
| a **generation-time** step this content type's own build should always do (a source to always pull, an order of operations, a check before drafting) | `factory/marketing/content-types/<type>.md` |
| scheduling, platform routing, autonomy mode | `factory/marketing/schedule.md` or `platforms.md` (rare — most defects are one of the two rows above) |

**Never propose a bullet for `factory/plan-review.md`, `factory/code-review.md`, or `factory/qa.md`.**
Those are the software-factory's gates, reviewing diffs and running apps, not marketing content — a
content defect has no business there even if the wording would technically fit.

## Step 5 — Dedupe, then stop for confirmation

`grep` the target file before proposing final wording — if a close bullet already exists, propose
*sharpening it in place* instead of adding a near-twin. Budget the same way `factory-remember` does:
past roughly 25 bullets a checklist stops being read item-by-item, so pushing past that means merging
two existing bullets first, not just appending.

**Do not edit the file yet.** Show the proposed diff and wait for explicit confirmation. Only after
the user confirms, apply it and show the actual diff that landed.

---

## What not to do

- **Don't diagnose without the transcript.** A rule guessed backward from the finished text alone is
  a guess about the pipeline, not a fact about it.
- **Don't write before confirmation.** This is the one hard difference from `factory-remember`, which
  writes directly — content rules get proposed first because the diagnosis step here is doing more
  inference (session-finding, transcript-reading) than remember's, and is more likely to be wrong.
- **Don't touch the software-factory gate files.** If the honest diagnosis lands on "the code that
  runs this pipeline has a bug," that's a `factory-implement`/bug-report task, not a content rule —
  say so and stop, don't force it into a checklist bullet.
- **Don't restate the whole content-type doc or content-review.md as the "rule."** Name the specific
  thing that was missing.
