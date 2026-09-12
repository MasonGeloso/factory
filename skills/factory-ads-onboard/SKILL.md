---
name: factory-ads-onboard
description: Interactive, hands-on onboarding for the ads pillar — sets up `factory/ads/platforms.md`, `budget.md`, `attribution.md`, `offers.md`, and the `strategies/`, `visuals/`, `ads/` directories. Like the marketing onboarding and unlike the rest of Factory's, this is not a batch of upfront questions — after a short setup interview (which ad platforms, what budget, what the business can afford to discount), it learns each platform live by walking a real campaign to the final review step WITHOUT submitting it, pulls the account's existing ad history for a baseline, then builds the user's FIRST real ad with them and files what it learns into the right doc as it goes. Entirely optional — a repo can say "no ads here" and nothing about this pillar gets touched. Use when `/factory-onboard` reports the ads module missing, when the user runs `/factory-ads-onboard` directly, or says "set up ads for this repo", "onboard the ads factory", "I want to run ads".
---

# Factory — Ads Onboarding (do-it-together, not a form)

*Set up the ads pillar by actually opening the ad platform and building a real ad with the user, not
by interviewing them about a system that doesn't exist yet.*

This is the onboarding source for every `ads/*` module in `factory-onboard`'s registry. If
`factory-onboard` routes here because one of those is missing, or the user invokes this directly, run
the whole flow below — it's one contiguous session, not five separate interviews.

> **This is optional, and skippable with zero side effects.** If the user says this repo has no ads
> need, tell `factory-onboard` to mark the module skipped and stop here. Nothing gets installed, no
> cron agent gets scheduled, no `factory/ads/` directory gets created.

**What the ads pillar does, in three jobs:** (1) turn an idea or a data source into a finished ad,
(2) post it to a platform on a set budget, (3) learn from how it did. This skill sets up the ground
truth all three read from. The ads themselves are built by `factory-ads-create` /
`factory-ads-clone`, posted by `factory-ads-post`, measured by the `ads-collect` agent, and reviewed
by `factory-ads-assess`.

---

## The shape of what you're building

```
factory/ads/
  platforms.md      # one section per ad platform: account switch, campaign mechanics, analytics
  budget.md         # the spend envelope, the period, what a single ad gets
  attribution.md    # how a campaign is traced to a click, a signup, and a paying user
  offers.md         # discounts/deals: the mechanism, the floor, how aggressive is acceptable
  strategies/       # the ANGLE — what value prop an ad argues. Reusable across ads.
  visuals/          # the METHOD — how the creative gets made. Reusable across ads.
  targeting/        # the AUDIENCE — who sees it. Reusable, but platform-specific.
  ads/<ad-id>/      # one directory per real ad: its .md plus its committed creative files
  .state/           # gitignored — spend, results, the collector's ledger
```

**The bucket model matters, so get it right rather than fast.** There are three reusable dimensions:

- **Strategy — the argument.** "This is cheap enough to be an impulse buy." "The people you respect
  already use this."
- **Visual — the production technique.** "An HTML/CSS template rendered to PNG." "AI video
  generation" — with everything learned about doing it well.
- **Targeting — the audience.** The platform configuration that decides who sees it: lookalike seeds,
  keywords, interests, geography, bid strategy. **Unlike the other two, targeting is inherently
  platform-specific** — the knobs on one ad platform have no counterpart on another, so a preset
  names its platform and is never reused across platforms.

An ad picks from these, or — very often — stands completely alone.

**A self-contained ad is a first-class outcome, not a failure.** Many good ads don't decompose into a
reusable angle plus a reusable technique. When that happens, write everything into
`ads/<ad-id>/<ad-id>.md` and create nothing in `strategies/`, `visuals/`, or `targeting/`. Only promote something to
its own file when it's genuinely reusable — a technique with real accumulated know-how, or an angle
that more than one ad will argue. **Never create a strategy, visual, or targeting file just to make an ad
look decomposed.** A `visuals/` file earns its existence by holding knowledge that is true regardless of
which ad uses it (which API, which env var, where output goes, what prompt style works, what wastes
money); an `ads/` file holds the specifics and the variations of one ad.

---

## Phase 1 — Short setup interview

Ask in one or two small batches (AskUserQuestion where it fits). Recon the repo first and pre-fill.

1. **Which ad platforms?** For each: the account/handle and the dashboard URL. Check whether a
   built-in starter exists in `factory-ads-onboard/starters/` (currently: `x-ads.md`). If so, seed
   that platform's section from it; if not, note "mechanics TBD — learned live in Phase 2".
2. **Account confusion.** Is more than one account for this platform logged in on this machine? If
   `factory/marketing/platforms.md` already exists, **read it first** — its account-switch procedure
   for the same platform is very likely already correct and hard-won, and should be referenced rather
   than rewritten from scratch. Ad platforms are usually a *separate surface on the same login*, so
   the same switch trap applies before you ever reach the ads dashboard.
3. **Budget.** What's the total envelope and over what period (e.g. "$250 per two weeks")? What does
   a single ad get, and for how long? Does an ad run for a fixed window, or until its money is spent?
4. **Offers/deals.** Can this business run temporary discounts? If yes: what's the mechanism (a
   Stripe coupon, a promo code, a manual price change), how aggressive can it get, and **why** — the
   reasoning is the part that makes future judgment calls possible, so capture the margin/cost
   structure behind the answer, not just a number. If no, write `offers.md` saying so and move on.
5. **Attribution.** How does a click become a traceable signup? Ask, then **verify in the code** —
   see the recon rules below. Do not write down an attribution path you have not confirmed exists.
6. **Credentials:** env var names only, never values.

Write first-draft `platforms.md`, `budget.md`, `offers.md` from this. Leave `attribution.md` until
Phase 2's verification is done.

## Phase 2 — Learn the platform live (and get a baseline)

For each platform, with the user watching, using **Chrome** (never a headless browser against a real
ad account — same ban/mute risk as any other logged-in platform):

1. **Perform the account switch first**, per that platform's section. Every time, as an action, not a
   check.
2. **Walk campaign creation end to end WITHOUT submitting.** Go all the way to the final review step
   — objective, audience/targeting, budget and schedule fields, creative upload, placements, the
   review screen — then **stop and abandon it**. Do not launch. The point is to learn and record
   every field, every trap, and exactly which button is the point of no return. Write what you learn
   into that platform's `platforms.md` section **as you go**, not from memory afterwards.
3. **Decide and record the campaign granularity** — one campaign for everything, one per ad, or one
   per ad type. Any of these is fine; what is NOT fine is leaving it unwritten, because the collector
   and the assessment both need to know how to find an ad's numbers later. Write the chosen rule and
   the naming convention that makes a campaign traceable back to an `ads/<ad-id>/`.
4. **Pull the existing history for a baseline.** Read whatever has already run: spend, impressions,
   CTR, conversions, date ranges. Record how to reach that view again (it is usually several clicks
   deep, and the path is worth writing down). Write a short, honest analysis of what the history
   suggests — and note where the numbers are not comparable, rather than ranking incomparable things.
   - **Ask which historical ad types to exclude from any analysis.** Some formats are structurally
     not comparable to a real ad (on X, for instance, boosted posts should be ignored entirely).
     Write the exclusion and its reason into `platforms.md` so every future assessment applies it
     without being told again.
5. **Capture the existing targeting configuration as the first preset.** If ad groups already exist
   on this account, open one and write down **every** audience knob and its exact value — lookalike
   / "similar to" seeds, follower look-alike handles, keywords, interests, geography, language,
   demographics, devices, placements, bid strategy and optimization goal — into
   `targeting/<preset-id>.md`. Record what was deliberately left at default too; "untouched" is a
   decision worth remembering. This is real configuration the user already thought about, and
   re-deriving it later from a changed UI is far harder than copying it down now.
   - Then ask **which ad types each preset suits** and note obvious experiments to try. A price-led
     ad and an authority-led ad frequently want different audiences at identical spend.
6. Record **how to read analytics for a single campaign**, since `ads-collect` will do exactly this
   on a schedule with no human present.

## Phase 3 — Verify attribution for real

The self-improvement job is worthless if a campaign can't be tied to a signup, so **confirm the path
in the code, don't take a yes for an answer.** Trace it concretely:

- Where does the ad's landing URL go, and **do campaign parameters survive to the backend?** Check
  the actual beacon/analytics call — a very common failure is a renderer that drops the query string
  before reporting, which silently makes every campaign parameter unmeasurable.
- Is there a field on the user/signup record that stores where they came from?
- Can the paying/subscription event be joined back to that field?

Write `attribution.md` describing the **real, verified** path. Where a link is missing, say so
plainly in the file, mark that metric as unavailable, and **tell the user it needs a separate task in
the product's own tracker** — do not paper over it, and do not let the ads pillar quietly depend on a
join that doesn't exist. A partially-attributed setup is fine and normal at the start; an imaginary
one is not.

## Phase 4 — Build the first real ad together

Ask: **"What's one ad you want to make right now?"** Then actually make it, narrating as you go.

While doing it, **stop and ask where each new thing you learn belongs**:

- True of *this platform, regardless of ad* → `platforms.md`.
- True of *this production technique, regardless of ad* → a file in `visuals/`.
- True of *this argument, regardless of how it's produced* → a file in `strategies/`.
- True of *this audience on this platform, regardless of the ad* → a file in `targeting/`.
- True only of *this ad* — including its variations and what's tweakable → `ads/<ad-id>/<ad-id>.md`.
- **Unsure, or it only exists once so far → put it in the ad file.** Promote it later when a second
  ad actually wants it. Premature abstraction here produces empty scaffolding that future runs have
  to read and ignore.

Check what the repo already has before inventing a technique — a project with an existing design or
video capability should use it rather than grow a parallel one.

Build the creative, save it under `ads/<ad-id>/`, and **stop before posting.** Publishing spends real
money on a real account and is `factory-ads-post`'s job with the user's explicit go-ahead — never a
side effect of onboarding.

## Phase 5 — Hand off

Show the resulting `factory/ads/` tree and confirm it matches reality. Then:

- Point at `factory-ads-create` / `factory-ads-clone` for making more ads, `factory-ads-post` for
  launching one, and `factory-ads-assess` for the recurring review.
- Offer to install the collector agent:
  ```
  factory agents install ads-collect /path/to/repo
  ```
  Only with explicit confirmation — a cron agent is a standing autonomous action against a live ad
  account.
- If this run was triggered by `factory-onboard`, hand control back to it.

## Recon before writing, always

Verify with the project's real tools instead of guessing: confirm the ad account is reachable, read
`factory/marketing/platforms.md` if it exists (the account-switch procedure and platform traps are
usually already solved there — reference, don't duplicate), grep the codebase for the analytics and
billing paths named in Phases 1 and 3, and read any existing brand/marketing docs. Audience and brand
research stays project-local; `factory/ads/` holds mechanics, money, and process.

## Hard rules

- **Never submit, launch, or publish a campaign during onboarding.** Walk to the review step and
  abandon. The whole point is to learn the flow without spending money.
- **Never write a secret into any file** — env var names only.
- **Never use playwright-cli or any headless browser against a real ad account.** Chrome only.
- **Never record an attribution path you haven't verified in code.** Write "unavailable, needs a
  product task" instead — that is a useful, honest answer and the assessment skill can work around it.
- **Never invent a budget, a discount floor, or a campaign-granularity rule the user didn't give you.**
  Ask. These are money decisions.
- **Never silently change a targeting preset that's already running.** Record the proposed change as
  an experiment in the preset file and let a human approve it — audience configuration is where spend
  quietly goes to die, and an unlogged change makes every earlier result uncomparable.
