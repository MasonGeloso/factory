---
name: factory-ads-post
description: Launch one finished ad on an ad platform, with the user's explicit go-ahead — set the campaign, the budget caps, the schedule and the targeting, upload the creative, walk to the review screen, and publish. Spends real money, so it never runs on its own initiative and never guesses a value that isn't written in `factory/ads/`. Reads platforms.md, budget.md, targeting/ and the ad's own file; records the campaign id and the exact published settings back into the ad file afterwards. Use when the user says "post this ad", "launch it", "factory ads post", or approves a specific ad for a specific budget.
---

# Factory — Ads Post

*The only skill in this suite that spends money. Everything it does is written down somewhere else
first; its job is to transfer that faithfully into the platform and prove it did.*

---

## Step 0 — Authorization, and what counts as it

**Never launch on your own initiative.** Launch only when the user has, in this conversation,
approved **this specific ad** for **a specific budget**. "Make an ad" is not authorization. "Looks
good" is not authorization. If the ad or the number is ambiguous, ask.

Then check the gates the project declares. Do not launch past an unresolved blocking gate; say which
one and stop. A gate the user explicitly overrules is fine — **record the override and its
reasoning** in the ad file, as a decision rather than as a fix.

## Step 1 — Read, don't recall

`factory/ads/platforms.md`, `budget.md`, `targeting/<preset>.md`, and the ad's own
`ads/<ad-id>/<ad-id>.md`. Every value you type into the platform comes from one of those files. If a
value isn't written down, stop and ask — **never invent a budget, a cap, an end date or a targeting
value at the keyboard.**

## Step 2 — The account switch is an action, every single time

Perform the platform's documented switch procedure before opening the ads surface, then confirm it
landed. **Do not skip it because you switched earlier in the session.**

> Observed on one real day: the browser was on the correct account, then on the personal account,
> then correct again, across three checks in a single session. A remembered state is worth nothing.
> The ads dashboard inherits whatever account the browser has, and an ad account carries a payment
> method.

## Step 3 — Build the campaign

Platform mechanics live in `platforms.md`; it should name every deterministic URL so you navigate
rather than hunt. Whatever the platform, these are the things that go wrong:

- **The default objective is usually the wrong one.** Set it deliberately and say why in the log.
- **Clear a pre-filled field before typing.** Typing into a populated name field appends; you get
  `Campaign — Sep 11 — 11:25 PMad-read-what-it-said`. Select-all, delete, then type, then read it back.
- **Set BOTH money limits**: the per-day budget and the **total spend cap**. The cap is usually
  optional and empty by default, and it is the one that actually stops spending.
- **Set an explicit end date.** "Run indefinitely" is a common default and it is never what
  `budget.md` says.
- **Fix the location.** A platform whose default audience is the wrong country will spend the whole
  budget there without a single warning. This is the most expensive default in the flow.
- **Re-enter targeting from the preset by hand** — a new ad group starts empty.
- **Read the live audience estimate before moving on.** It is the fastest check that targeting is
  doing anything at all, and it is how you discover that a preset does not actually narrow.

## Step 4 — The creative

- Upload the **language variant that will run**, not the review copy.
- To attach media, find the **file input element** and upload to it directly. Do not click the
  upload button — that opens a native file picker you cannot see or operate.
- Confirm the platform accepted the file: no crop warning, no size warning, and the preview renders.
  **This is also the moment to verify aspect-ratio acceptance** if it has never been confirmed.
- Set any AI-disclosure control per the project's recorded decision; do not decide it here.
- **Put the campaign tag in the landing URL before you launch.** If `attribution.md` says the
  project can read campaign parameters, the URL ships tagged — checked at the review screen, not
  remembered afterwards. An ad launched untagged buys clicks that can never be attributed, and under
  a first-touch model it also poisons those visitors for the length of the attribution window: they
  arrive credited to nothing and stay that way even if they return through a tagged link.
  Retro-fitting a tag onto a live ad recovers none of the clicks already bought — **and on some
  platforms it is not possible at all.** On X, a published ad's destination URL, post text, headline
  and media are locked; only campaign and ad-group settings stay editable. The only route to a
  tagged link mid-flight is a new ad in the same ad group, which restarts that ad's delivery
  learning. Treat the landing URL as a one-shot setting.
- Only if `attribution.md` says parameters cannot yet be read: **leave it empty and say so** — a
  parameter nothing consumes is noise that looks like measurement.

## Step 5 — Review, verify against the source, publish

Walk to the review screen. Then read every value back **against the files from Step 1**, not against
what you remember typing. Confirm the funding source is the one the user expects.

If the platform reports issues, fix them and re-review. **Publish only when the review screen is
clean and every value matches.**

## Step 6 — Prove it landed, then write it down

- Confirm the campaign is live: capture its **id**, its status, and the platform's own count of
  campaigns before and after.
- Write into the ad file: the campaign id, a table of **every published setting**, the creative that
  ran, and the date.
- Update `budget.md` with the committed spend for the period and what remains.
- Seed/refresh the collector's state directory so the first collection run has somewhere to write.
- **State the measurement caveat plainly** if attribution is incomplete: name exactly which metrics
  this spend can and cannot be judged on. A launch report that implies conversions will be
  measurable, when they will not be, is worse than no report.

## Hard rules

- **One ad at a time** while a baseline is being built, unless `budget.md` says otherwise.
- **Never exceed the period envelope.** Check what is already committed before adding more.
- **Never launch a creative that has not been through the project's gates**, or whose blocking gate
  is unresolved and un-overruled.
- **Never change a targeting preset silently while launching.** A deviation from the preset is a
  decision, and it goes in the ad file with its reasoning.
- Stop and ask on anything unexpected — a missing funding source, a policy warning, an issue count
  that will not clear. The cost of asking is a message; the cost of guessing is money and an account.
