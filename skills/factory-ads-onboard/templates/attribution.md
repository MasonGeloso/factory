# Factory Ads — Attribution — <PROJECT NAME>

> How a campaign is traced to a click, a signup, and a paying user. Read by the `ads-collect` agent
> and by `factory-ads-assess` — this file is what makes "which ad actually worked" answerable.
> **Every path here must be verified in the code, not assumed.**

- **Landing URL pattern:** <the URL an ad points at, including the campaign parameter convention>
- **Does the campaign parameter survive to the backend?** <VERIFIED YES (where, which file/endpoint)
  | VERIFIED NO (what drops it, and where) — this is the single most common silent failure: a
  renderer or beacon that strips the query string makes every campaign parameter unmeasurable>
- **Click / pageview:** <the system that records it, how to query it, what identifies the campaign>
- **Signup:** <the field on the user record that stores acquisition source, or "none — unavailable">
- **Paid conversion:** <how a subscription/payment joins back to that field, or "unavailable">
- **What is measurable today:** <the honest list>
- **What is NOT measurable, and what would fix it:** <name each broken link and the product-side task
  it needs. Leave this section standing until the task actually lands — a missing join that is
  written down is workable; one that is glossed over corrupts every future assessment.>
- **Verified on:** <date, and by what check>
