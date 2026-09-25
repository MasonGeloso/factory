---
name: factory-ads-create
description: Build one ad, end to end — pick an angle, verify the feature it sells by actually opening it, write copy as plain declarative sentences, brief a graphic to a design-capable model, render both languages, self-check, and hand it to the `factory-ads-qa` gate before any money is pointed at it. Reads per-project rules from `factory/ads/` (platforms, budget, offers, attribution, qa) and files what it learns into `strategies/`, `visuals/` and `ads/`. Use when the user says "make an ad", "new ad", "factory ads create", or when `factory-ads-onboard` reaches its build-the-first-ad phase.
---

# Factory — Ads Create

*One ad, built properly. The picture carries the argument; the copy says what the thing is.*

This skill exists because ad creative fails in a small number of repeatable ways, and every one of
them is cheaper to prevent than to discover after a week of spend. The rules below were each paid
for by a rejected ad.

---

## Step 0 — Config and context

Read `factory/ads/platforms.md`, `budget.md`, `offers.md`, `attribution.md` and `qa.md`. If any is
missing, invoke `factory-ads-onboard` rather than guessing. Read `factory/ads/strategies/`,
`visuals/` and `targeting/` so you reuse what exists instead of reinventing it.

## Step 1 — Verify the feature, in the product, with your own eyes

**Do not write a word until you have opened the thing you are selling.** Not the code, not a doc —
the running product, on the surface the ad's audience would land on.

- Deprecated surfaces do not count. Beta features that are currently free must not be sold as paid.
- Capabilities that "should exist" do not exist.
- **Name the landing page before writing the headline.** An ad that cannot say where it lands is not
  an ad, and the mismatch is the single most common cause of a wasted click.
- **Write the landing URL WITH its campaign tag, now, in the ad file.** If `factory/ads/attribution.md`
  says the project can read campaign parameters, the URL is never recorded bare:
  `https://<site>/?utm_source=<platform>&utm_medium=paid&utm_campaign=<ad-id>`. The tag has to be
  decided at creation, because **it cannot be added later** — on X a published ad's URL is locked,
  and under first-touch attribution an untagged arrival stays credited to nothing for the whole
  window even if they return through a tagged link. Launching one ad untagged cost this suite a
  full week of unmeasurable spend. `factory-ads-post` re-checks it at the review screen; this is
  where it gets written.
- Record what you saw, and the date, in the ad's own file. Product surfaces change.

> The costliest error in this suite's history was writing three ads for features nobody had opened.
> One sold a supply-chain taxonomy that had been deleted; one sold "screening", which was never a
> feature; one sold a beta that was free to everyone.

## Step 2 — Pick an angle, deliberately

Read [references/angles.md](references/angles.md) and choose. Then check the angle against every ad
already in `factory/ads/ads/`.

**Two ads that make the same argument in different words are one ad.** A set of four "here is a
useful thing we do" ads is not a test of anything. If everything in the directory is a benefit
angle, the next ad is not allowed to be one.

## Step 3 — Write the copy

Short. Plain. Say what the buyer gets, in their words.

- **Declarative sentences: subject, verb, object.** "The service checks every invoice against 12
  dimensions."
- **Banned outright, in every language:**
  - the contrast construction — "not X, it's Y", "X, then Y", any then/now reversal pair;
  - the noun-phrase-comma-appositive headline — "Every disclosure, scored across 12 dimensions";
  - lines that sound profound and state nothing — "Twelve companies overnight. One screen at 7am."
- Specifics beat adjectives. Lead with the buyer's outcome, not the brand name.
- No jargon the reader does not already use. Name a feature only if you say what it does in the
  same breath.
- **Run `factory-humanizer`** in each language. Then read it aloud anyway: **the scanner catches
  lexical tells and is blind to every structural one above.** It has cleared the banned construction
  every single time it has been tested against it.
- **Write both languages from the source, not by translating.** Each must read natively.

### If the brand is unknown to the audience

A claim from a brand nobody recognises is a claim about nothing. Either put the category in the
headline, or run a descriptor under the wordmark — **not both**, or it says the same thing twice.
See `strategies/category-lead.md` in a project that has one.

## Step 4 — Brief the graphic

Graphics go to a design-capable model — see [references/graphic-briefs.md](references/graphic-briefs.md)
for the full contract, the working brief skeleton, and how to invoke it.

The two rules that decide whether the result is any good:

1. **Brief the IDEA, not the geometry.** Say what must be *understood*, name the failure to avoid,
   and set a quality bar. Where briefs specified coordinates, the model complied and invented
   nothing. Where they described the idea and the feeling, it produced the erosion particles, the
   target bracket, the vanishing point and the readout panel unprompted.
2. **Every mark must represent a real thing.** A line that stands for no quantity, a bracket that
   frames nothing, a particle spray that is not data: that is decoration impersonating an
   instrument. It looks sophisticated and communicates nothing.
   - **The test: cover every label and look again.** If the picture stops communicating, the labels
     were carrying it, and the graphic has failed.
   - A literal, typed depiction beats an abstraction. Four distinguishable icons for four kinds of
     document beat four identical lines, because the difference teaches the viewer something.
   - Simple and meaningful beats dense and impressive. Density is not rigour.

**Generate one graphic per language. Always.** Language is a *generation* parameter, not a
compositing one — a shared graphic under a swapped headline ships one language's labels on another's
export. This has happened three times; assume it will happen again.

**Never hand-edit generated filter geometry.** Erosion, glow and mask effects are anchored per
element; moving a text node's `y` pulls the glyphs out of their own mask and they vanish, leaving
loose particles. Hand the defect back to the model that built it.

## Step 5 — Composite and render

Per-project rig (see the project's `visuals/`). Non-negotiable across all of them:

- **The logo is on every creative.** An ad without it is not an ad.
- **Type floor.** Read it from `factory/ads/qa.md`. Small print is where it is always violated.
- **Check the stacking order.** A graphic layer with a `z-index` above the brand bar hides the logo,
  and it will not be noticed until a graphic happens to have content near the top.
- Render at the platform's real export size, then **look at the exported file** — not the browser.

## Step 6 — Self-check, then hand to the gate

Look at the export at full size **and at 25%**. Then run **`factory-ads-qa`**, externally, in rounds,
until `VERDICT: SHIP`.

- **Re-render before disputing a finding.** A rejection argued from a stale export is worthless, and
  the reviewer is usually looking at bytes you have since replaced.
- **Reviewers produce confident, specific, repeatable false positives about visual detail, and two
  independent reviewers can produce the same false one.** Agreement is not evidence. Open the file.
- Record rejected findings with their evidence rather than dropping them.

## Step 7 — File it

Write `ads/<ad-id>/<ad-id>.md` from `factory-ads-onboard/templates/ad.md`: the verified feature and
the date it was opened, the landing page, a claim table with a source for every claim, the creative
files, the variants, and the QA history including anything rejected and why.

Promote to `strategies/`, `visuals/` or `targeting/` **only what a second ad will genuinely reuse.**
A self-contained ad is a good outcome; scaffolding created for one ad is a cost every future run pays.

## Hard rules

- **Never launch.** Publishing spends real money on a live account — that is `factory-ads-post`, with
  the user's explicit go-ahead.
- **Never state a claim you have not verified today**, prices most of all. Read them live.
- **Round derived figures against yourself** and state the basis on the creative.
- **Never sell a deprecated, unbuilt, or free-in-beta capability.**
- Never put a real company identifier on an invented event.
- Keep the regulatory disclaimer on the creative, or carry it in the platform copy — and say which.
