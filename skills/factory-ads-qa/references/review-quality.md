# What image review actually gets wrong

Accumulated from real rounds. Read this before trusting or dismissing a finding.

## Reviewers hallucinate missing brand marks and clipped headlines

**Three separate rounds, two different models, reported a missing logo or a clipped non-English
headline on creatives where both were plainly present.** Twice on one ad, once on another. It is the
most common false positive in this gate, and independent reviewers produce it independently — so two
reviewers agreeing is not evidence.

**The artifact adjudicates, not the vote count.** Open the file and look.

## But check you are looking at the same bytes

Before disputing anything, confirm the export has not changed since the review ran. On one round a
rejection was *correct* but reached by looking at a stale render — right answer, wrong method, and it
would have been wrong the next time. Re-render, then look.

## A reviewer without network cannot verify a live claim

That is `BLOCKED` on that row, not `FAIL`. The author supplies the evidence — a captured response
with a timestamp — and the reviewer records it rather than guessing.

## Rules get mis-scoped

A checklist rule written for one palette or one surface gets applied to all of them. When a finding
is a scoping error rather than a defect, **fix the scope in the checklist** so the next round does
not re-raise it. Two live examples: a gold-usage rule scoped to the light palette applied to a dark
creative, and an ad-copy type floor applied to microcopy inside a depicted product screen.

## What reviewers reliably catch that authors do not

Worth the gate's existence on its own:

- **Claims the author flagged and then walked past.** On one ad the author twice noted that real
  company names were paired with invented events, and shipped it anyway both times. The gate stopped it.
- **Negation claims.** "No X. Just Y." — where X was a real product feature. Nobody fact-checks a denial, including the person who wrote it.
- **Internal inconsistency.** A screen reading "3 of 3 items" while showing two.
- **Claim creep.** "Every disclosure", "every answer", "delivered every morning" — each a small
  widening past what the evidence supports.
- **Regulatory framing.** Whether the advertiser's category triggers a platform's financial-services
  authorization requirements is not something a creative review can settle, but naming it is what
  gets it in front of the owner before the money moves.

## What the gate has still missed, and a human caught

Be honest about this, and keep adding to it:

- **Crowding.** A bullet touching a footer pill passed a round, because the reviewer checked for
  overlap, found none, and moved on. Overlap is the extreme case, not the defect.
- **Stiff, clinical phrasing.** "A 07:00 recap" is not an AI tell in any lexical sense and breaks no
  written rule. It is simply not how a person speaks. No scanner and no checklist has caught this
  class; it needs an ear.
