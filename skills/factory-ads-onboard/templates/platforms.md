# Factory Ads — Platforms — <PROJECT NAME>

> Every ad platform this project runs campaigns on, and the mechanics of operating it. Read by
> `factory-ads-post` before it touches a campaign builder, and by the `ads-collect` agent before it
> reads analytics. Filled during onboarding via `factory-ads-onboard`; one section per platform.

<!-- Repeat this section per platform. -->

## <Platform name, e.g. "X Ads">

- **Dashboard URL:** <e.g. ads.x.com>
- **Account / handle:** <which account owns the ad account>
- **Credentials:** <env var names only — never a value. Usually "already-logged-in Chrome session">
- **Account switch (MANDATORY, every run — an action, not a check):** <exactly how to get onto the
  right account before opening anything. If `factory/marketing/platforms.md` already documents this
  for the same login, reference that procedure rather than restating it — but say plainly that it
  applies here too, and note anything the ads surface does differently.>
- **Campaign granularity:** <one campaign for all ads | one per ad | one per ad type — whichever was
  chosen, plus the naming convention that ties a campaign back to an `ads/<ad-id>/` directory. The
  collector needs this to find an ad's numbers without a human.>
- **Creating a campaign — the real flow:** <every step learned live: objective, audience/targeting,
  budget + schedule fields, creative upload, placements, review. Note which button is the point of no
  return, and anything that cost real time to discover — silent validation failures, fields that
  reset, upload constraints, aspect ratios, character limits.>
- **Targeting knobs available here:** <the audience configuration this platform exposes, and at which
  level (campaign vs ad group / ad set) — this is what a `targeting/` preset for this platform may
  set. Note which knobs are expensive to get wrong.>
- **Setting the budget cap:** <exactly where the campaign's own daily/lifetime cap is set, since the
  platform — not this suite — is what enforces spend>
- **Reading analytics for one campaign:** <the click path to per-campaign numbers, which metrics are
  available, and how far back. Written for an agent with no human present.>
- **Excluded from analysis:** <ad/campaign types that are structurally not comparable and must be
  ignored in every assessment, plus why>
- **Baseline (as of <date>):** <what had already run before onboarding: spend, CTR, impressions,
  conversions, and an honest note on what is and isn't comparable>
