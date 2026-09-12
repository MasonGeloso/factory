---
name: factory-ads-assess
description: The recurring ads review — usually weekly, with the owner. Pulls each campaign's spend and clicks from the ad platform and its signups from the project's own attribution, separates measured from hand-set and presumed conversions, flags confounds, compares against the baseline, and ends in ONE recommendation for next week's single variable. Report only — it changes nothing. Pausing, launching, budget changes and database writes are never done here. Supports a dry run that produces the full report without posting it anywhere. Use when the user says "assess the ads", "weekly ads review", "how did the ads do", "factory ads assess", or at the end of a campaign flight.
---

# Factory — Ads Assess

*Turn a week of numbers into one decision the owner can make. Never make it for them.*

The loop this sits inside: `factory-ads-create` builds an ad, `factory-ads-post` launches it, the
project's reporting agent keeps a running card, and **this skill closes the week** — what happened,
how much of it is actually known, and what to change next.

---

## Step 0 — Mode

- **Dry run** (default when the user asks to "try" or "test" it, and whenever intent is unclear):
  produce the entire report and write it to a local file. **Post nothing, change nothing.** Say
  plainly at the top of the output that this was a dry run.
- **Live run:** the same report, plus delivering it where `factory/communication.md` says reports go.

**Neither mode takes action.** This skill never pauses a campaign, launches one, edits a budget,
changes targeting, or writes to the database. Its product is a recommendation. If the owner accepts
it, `factory-ads-create` and `factory-ads-post` do the work, under their own gates.

## Step 1 — Read the project's rules

`factory/ads/platforms.md` (how to read the numbers, what to exclude, the baseline),
`budget.md` (the envelope and what is committed), `attribution.md` (**how conversions are queried,
which campaigns were tagged when, and any presumption windows**), `targeting/`, and every
`ads/<ad-id>/<ad-id>.md` for campaigns live or finished in the period.

If `attribution.md` does not say how to query signups, the report can still run — on clicks only —
but it must say so in its first line.

## Step 2 — Gather, per campaign

**From the ad platform:** spend, impressions, CPM, clicks, CTR, cost per click, for the exact period,
with an explicit date range. Note the platform's reporting timezone. Apply every exclusion in
`platforms.md` (boosted posts and the like) before any number is compared to anything.

**From the project's own attribution:** run the query `attribution.md` names. Report four numbers,
**never collapsed into one**:

| | Meaning | Counts toward cost per signup? |
|---|---|---|
| **Measured** | captured by the tracking from a tagged link | **yes — the only one** |
| **Manual** | a human attributed it by judgement | no |
| **Presumed** | inside a documented presumption window for an untagged campaign | no — upper bound only |
| **Paying** | of the measured, the ones on a paid, current subscription | the real outcome |

A failed-payment status is neither paying nor churned; report it separately.

**Tagging status, per campaign:** tagged for the whole flight / untagged for the whole flight / tagged
part-way. An untagged campaign's missing signups are **a gap in measurement, not a result of zero**.
Never let an untagged blank sit in a table next to a tagged number as though they were comparable.

## Step 3 — Judge, honestly

For each campaign answer, in plain language:

1. **What did it cost, and what did it produce?** Cost per click always. Cost per measured signup and
   per paying user only when measured signups exist.
2. **Against the baseline** in `platforms.md`, and against any other campaign in the period that ran
   under comparable conditions.
3. **How much of that is known?** Sample size in words — "36 clicks" is not a trend. Say when a number
   is too small to act on, and say it before the number, not in a footnote.
4. **What moved between this campaign and its comparison?** List every variable that changed:
   creative, copy, targeting, objective, placement, budget pacing, landing page, week of the month.
   **If more than one moved, the comparison cannot attribute the difference to any of them — say so,
   and do not pick a favourite explanation.**
5. **What seems to be working, or not** — as a hypothesis, labelled as one, grounded in something
   observable (a CTR drop between two identical-audience creatives is evidence about creative; a CTR
   drop after changing both creative and audience is not evidence about either).

## Step 4 — One recommendation

End with **exactly one** recommendation for the next flight, in this shape:

> **Keep** <what stays the same>. **Change** <the one variable>. **Because** <the observation that
> makes this the most informative next test>. **We will know it worked if** <the metric and roughly
> what size of change would be meaningful at next week's likely sample size>.

- **One variable.** If the last flight changed several at once, the recommendation is usually to hold
  all but one fixed next time, specifically so the flight after produces something readable.
- **Never recommend spending above the envelope** in `budget.md`. If the right test needs more money,
  say that as a question for the owner, not as the recommendation.
- **Never recommend launching untagged.** If the project can read campaign tags, the recommendation
  assumes the next ad ships tagged, and says so.
- It is fine — often correct — to recommend **not changing anything and running the same ad again**
  when the sample was too small to learn from. Say that plainly rather than inventing a change.

## Step 5 — Write it down

- Save the report as `factory/ads/assessments/<YYYY-MM-DD>.md` — dated, append-only history. **This
  is the only file a dry run writes**, and its first line says it was a dry run.
- **Live run only:** append a short results note to each assessed campaign's `ads/<ad-id>/<ad-id>.md`,
  and deliver the report per `factory/communication.md`. A dry run touches neither — it exists so the
  owner can read the verdict before anything is recorded against a campaign.

## Report shape

Plain language, for someone who has not looked at a dashboard all week. Lead with the verdict.

```
# Ads assessment — <period>  [DRY RUN]

**Verdict, one sentence.**

## Numbers
<per-campaign table; measured / manual / presumed / paying as separate columns; tagging status>

## What we actually know
<sample sizes in words; what is and isn't measurable this week, and why>

## What changed, and what that means
<every variable that moved; the confound, named, if there is one>

## Recommendation
Keep … Change … Because … We will know it worked if …

## Open questions for the owner
<anything that needs a human decision: money, policy, a presumption window, a tracking gap>
```

## Hard rules

- **Report only.** No pausing, launching, budget edits, targeting edits or database writes — in either
  mode.
- **Never divide spend by anything but measured signups** when stating a cost per signup.
- **Never present an untagged campaign's missing conversions as zero.**
- **Never present manual or presumed conversions as measured**, and never merge them into one column.
- **Never name a single cause for a difference when more than one variable changed.**
- **Exactly one recommendation.**
- If a number cannot be gathered (platform unreachable, query failing), say which, run the rest, and
  mark that section incomplete. A partial report that is loud about its gap beats a complete-looking
  one that isn't.
