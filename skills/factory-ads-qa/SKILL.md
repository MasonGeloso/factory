---
name: factory-ads-qa
description: The QA gate for ad creative — multi-round, external, fresh-eyes review of a finished ad before any money is spent on it. Reviews the rendered image and its copy against generic advertising discipline (legibility at feed size, one clear subject, claim integrity, brand consistency, layout paper-cuts) plus the project's own checklist in `factory/ads/qa.md`. Built to run two ways — invoked in-context via the Skill tool, or run cold by ANY CLI-based coding agent (e.g. Codex CLI's `codex exec`) handed only this file's absolute path and a path to the rendered PNG. Runs in rounds until it returns VERDICT: SHIP. Use when the user says "QA this ad", "review this creative", or when `factory-ads-create` reaches its QA step before handing an ad to `factory-ads-post`.
---

# Factory — Ads QA (external / second-opinion, multi-round)

*A different set of eyes — usually a different model — on the finished creative, before it costs
money. The ads counterpart to `factory-code-review`.*

This skill is read two ways:
1. **In-context (Claude, via the Skill tool).** You have the conversation. Skip to Step 2.
2. **Cold, by an external CLI agent** handed this file's absolute path plus a rendered PNG. Do Step 1
   first.

> External agent reading this file: it is a plain markdown instruction file, not a skill invocation.
> Follow it as your task. **You must actually open and look at the image.** A review written from the
> copy alone is worthless here and must be reported as `VERDICT: BLOCKED — could not view image`.

**Why this gate exists.** A bad ad is not like a bad commit. It spends real money against a real
account, in public, under the advertiser's name, and the feedback loop is days long. The cost of one
more review round is a rounding error against a week of budget.

---

## Step 1 — Establish context (skip if you already have it)

- You will be given the path to a **rendered PNG** (not the source), and usually its ad directory
  under `factory/ads/ads/<ad-id>/`.
- Read `factory/ads/ads/<ad-id>/<ad-id>.md` if it exists — the ad's own file states its strategy,
  its target feature, its landing page and its claims, and **those are what you review it against.**
- Read `factory/ads/qa.md` for the project's own checklist. If missing, run the generic rows only and
  say so.
- Read `factory/ads/platforms.md` for the target platform's format constraints.

## Step 2 — Look at the image properly

- Open the PNG. **View it at least twice: once at full size, and once scaled down to roughly 25%**,
  which is closer to how it appears in a feed. Several categories below can only be judged small.
- If a JA and an EN variant both exist, review both. A defect in one is a finding.

## Step 3 — Review

Score every row PASS / WARN / FAIL. A note of "looks fine" is not a review of that row — each note
must cite what you actually looked at.

1. **Thumb-stop** — At 25%, is there a single clear subject that arrests the eye? Or does it read as
   a grey rectangle of text?
2. **Legibility at feed size** — Name the smallest text on the creative and say whether it survives
   at 25%. Any body text under the project's stated floor is an automatic FAIL.
3. **One idea** — Can you state the ad's single claim in one sentence after two seconds? If it takes
   reading to work out, FAIL.
4. **The graphic earns its place** — Does the picture carry the argument, or is it decoration beside
   text that does the real work? Is it labeled enough that a stranger knows what it depicts?
5. **Every mark means something** — **Point at each element and name what it represents.** A line
   that stands for no quantity, a bracket that frames nothing, a particle spray that is not data, a
   dial with no reading, corner ticks that label nothing: all of it is decoration pretending to be
   an instrument, and it makes the ad look sophisticated while saying nothing. If you cannot answer
   "what is that?" for an element, it is a finding.
   - The test: **cover every label and look again.** If the picture no longer communicates, the
     labels were carrying it and the graphic has failed.
   - Prefer a literal, typed depiction over an abstraction. Four distinguishable icons for four kinds
     of document beat four identical lines, because the viewer learns something from the difference.
   - Simple and meaningful beats dense and impressive. Density is not rigour.
6. **Claim integrity** — Every number, price, superlative and capability claim: is it substantiated
   in the ad's own file? Flag anything unsourced. **Finance, earnings and performance claims get
   their own line** — these carry regulatory risk, not just credibility risk.
7. **Copy — AI tells** — Read it aloud. Flag the contrast constructions ("not X, it's Y";
   "X, then Y"; noun-phrase-comma-appositive headlines), uniform sentence rhythm, and any sentence
   that sounds profound without saying anything. **A lexical scanner does not catch these** — this
   row is a human-ear judgement and is mandatory.
8. **Concreteness** — Does it say what the buyer actually gets, in their words? Or does it describe
   the product in the vendor's abstractions?
9. **Brand consistency** — Logo present and correct. Palette, type and register consistent with the
   project's design tokens. Would this be recognisable as the same advertiser as the last ad?
10. **Layout paper-cuts** — the most common finding, and the one most often missed because a
    reviewer checks for overlap, finds none, and moves on. **Overlap is the extreme case, not the
    defect.** Check all of it:
    - **Crowding.** Two elements that do not touch but have no breathing room between them read as a
      mistake. Name the tightest gap on the creative and say whether it looks deliberate. A line of
      copy ending a few pixels above a bar, button or panel edge is a finding even though nothing
      overlaps.
    - **Collisions.** Text crossing a graphic element; a label buried under an object; a side rail
      running through a header row.
    - **Orphans and strays.** A single word or character wrapped onto its own line; a label stranded
      far from what it points at; a leftover rule from a deleted element; an axis number attached to
      nothing.
    - **Leader lines** that cross each other or pass under other objects.
    - **Dead zones.** A large flat area between two clusters reads as a mistake, not as restraint.
    - **Margins.** Anything closer to an edge than the stated margin.
    - **Ambiguous referents.** A caption that could belong to either of two things.
    - **Wrap damage.** Text wrapping to an extra line in one language but not the other, pushing
      everything below it out of place. Check each language export independently.
    Report the specific fix — "move X up", "move Y down" — not just that it looks tight.
11. **Truncation and safe area** — Nothing clipped by the canvas. Nothing in a region the platform
    overlays with UI.
12. **Localisation parity** — If JA and EN both exist, do they make the same claim at the same
    strength, and does each read natively rather than as a translation?
13. **Project checklist** — every bullet in `factory/ads/qa.md` becomes its own row.

## Step 4 — Report

```
| Check | Status | Note |
|-------|--------|------|
```

Then every finding as its own numbered entry: **what is wrong**, **where on the creative**, and
**the specific fix**. Rank blocking defects above paper-cuts. End with exactly one line:

```
VERDICT: SHIP
VERDICT: FIX — <n> blocking findings
VERDICT: BLOCKED — <reason>
```

`SHIP` means it can have money pointed at it. Anything that would embarrass the advertiser, mislead
a reader, or waste spend through illegibility is `FIX`, not a paper-cut.

## Step 5 — Rounds

This gate is **multi-round by design**, mirroring `factory-code-review`'s follow-up contract:

- Round 1 is the broad review. Fix the findings, re-render, and run it again.
- On a follow-up round, **reuse the prior round's finding IDs** and state for each: fixed, partially
  fixed, or regressed. Distinguish an incomplete fix from a new defect.
- Keep the full scope every round. **Do not manufacture a new blocker just because the previous
  findings closed** — and do not wave through a round because the ad "looks better than last time".
- **Stop at `VERDICT: SHIP`, not at a round count.** Two clean rounds from independent reviewers is
  worth more than five rounds from one.
- Where a round is run by an external tool, record the tool and model in the report, so a later
  reader knows which eyes saw it.

> Before trusting or dismissing any finding, read
> [references/review-quality.md](references/review-quality.md) — what this gate reliably catches,
> what it reliably hallucinates, and what it has still missed.

## Adjudicating a disputed finding

Reviewers of images produce **confident, specific, repeatable false positives** — and independent
reviewers can produce the *same* false one, so agreement between them is not evidence. Observed on a
real run: two different models both reported a headline clipped off the left edge and a missing brand
mark on a creative where both were plainly intact.

So:
- **The artifact adjudicates, not the vote count.** A disputed visual finding is settled by opening
  the file and looking, never by how many reviewers said it.
- **Check you are looking at the same bytes the reviewer was.** If the creative was re-exported
  between the review and the reply, the disagreement is probably about two different files. Re-render,
  then re-look, before calling anything wrong.
- **Record a rejected finding in the ad file with the evidence**, rather than dropping it silently.
  A reviewer who was wrong once may be right next round, and the next author needs the history.
- A reviewer that cannot reach the network cannot verify a live claim. That is `BLOCKED` on that row,
  not `FAIL` — and the author supplies the evidence instead.

## Hard rules

- **Never approve an ad you could not actually view.**
- **Never soften a finding because the creative is nearly finished.** The whole point of this gate is
  that it sits before the money.
- **Never let a claim through on the grounds that it is "illustrative"** unless the creative itself
  carries that disclaimer legibly.
- Report findings; **do not edit the creative yourself** unless explicitly asked. The author fixes,
  the reviewer re-reviews.
