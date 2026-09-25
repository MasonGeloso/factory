---
name: factory-demo-light
description: Minimum-sufficient proof that a small/medium change works — one screenshot, a short clip only if something animates, a log excerpt for backend/pipeline work, or a Claude Artifact link for something visual/interactive. Not the full demo package (`factory-demo-video`/`factory-demo-terminal` produce a .webm plus numbered stills plus an artifacts.md manifest); this produces just enough evidence for someone to trust it in a chat message. Used by `factory-implement-light` to close the loop instead of a full demo + QA gate. Use when the user asks for quick proof of a small change, or when `factory-implement-light` reaches its demo step.
---

# Factory — Demo Light

*One piece of evidence, picked to fit the change, posted where the request came from. Not a review
package — a "trust me, look" attachment.*

The full demo skills ([`factory-demo-video`](../factory-demo-video/SKILL.md),
[`factory-demo-terminal`](../factory-demo-terminal/SKILL.md)) exist to hand a reviewer everything they'd
need to judge a feature without running it themselves — a whole multi-scene package. This skill is for
the opposite situation: a person who's already in the conversation, already knows what was asked for,
and just needs to see that it's actually done.

---

## Step 0 — Pick the right artifact for the change

Don't default to any one format — match it to what was actually built:

| Change shape | Artifact |
|---|---|
| UI change, one or two states | **One screenshot** (desktop; add a mobile-width shot only if the change is mobile-specific or the initiative's scope is mobile) |
| Something that animates/transitions | **A short clip** — a few seconds, not a full walkthrough |
| Backend / pipeline / data change | **A log excerpt or command output** showing the real behavior on a real input — not a synthetic example |
| Something visual/interactive worth exploring, not just looking at | A **Claude Artifact** link, if the stack/tooling makes one straightforward to build; otherwise fall back to a screenshot |
| A CLI/script change | **Terminal output**, pasted or as a short clip if the interaction itself is the point |

If genuinely nothing fits (e.g. a config-only change with no observable output), say so explicitly
instead of forcing an artifact — "no visible output, changed `<file>`, verified via `<command>`" is a
valid demo-light result.

## Step 1 — Capture it against the real running change

Same standard as the full demo skills on this one point: it has to be **the actual thing that was just
built**, stood up and exercised, not a mockup or a description of expected behavior. Use whatever's
already running from `factory-execute`'s stand-up (or bring it up per `factory/deployment.md` if it
isn't).

## Step 2 — Post it

One message: the artifact plus a one-line caption of what it shows. No numbered scene list, no
`artifacts.md` manifest, no separate desktop/mobile pair unless the change genuinely needs both to be
trusted. This goes straight into the channel per `factory-implement-light` Step 7 — it **is** the
handoff, not a precursor to one.
