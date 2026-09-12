# Factory Ads — Budget — <PROJECT NAME>

> The spend envelope. Read by `factory-ads-post` before launching anything and by
> `factory-ads-assess` when judging what an ad earned. Filled during onboarding.

- **Envelope:** <total, per period — e.g. "$250 per two weeks ($500/month)">
- **Period boundary:** <when a period starts/resets, and in which timezone>
- **Per-ad allocation:** <what one ad gets — e.g. "$125 for one week">
- **Run length:** <fixed window | runs until its allocation is spent, whichever comes first>
- **How the cap is enforced:** <the campaign's own budget cap, set in the platform at launch — the
  platform enforces, this suite records. Name the exact field in `platforms.md` terms.>
- **Concurrency:** <how many ads may run at once in this period>
- **What happens when the envelope is exhausted:** <stop launching and say so | ask the user>
- **Spend record:** `factory/ads/.state/` (gitignored) — written by the `ads-collect` agent.

> Spend is real money. Never launch a campaign whose cap isn't set per the rule above, and never
> raise the envelope without the user saying so explicitly.
