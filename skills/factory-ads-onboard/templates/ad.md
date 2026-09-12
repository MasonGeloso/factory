# Factory Ads — Ad — <ad name>

> One directory per ad at `factory/ads/ads/<ad-id>/`, holding this file plus its committed creative
> files. Read by `factory-ads-post` to launch it and by `factory-ads-assess` to judge it.
>
> **This file may be fully self-contained.** If the ad doesn't decompose into a reusable angle, a
> reusable technique, and a reusable audience, say `none` below and write everything here. That is a
> normal, good outcome.

- **Ad id:** <ad-id>
- **What it is:** <one or two sentences — what a viewer sees and what it asks them to do>
- **Strategy:** <`strategies/<id>.md` | none — self-contained, described below>
- **Visual method:** <`visuals/<id>.md` | none — self-contained, described below>
- **Targeting preset:** <`targeting/<id>.md` | none — described below. Must match the ad's platform.>
- **Build steps:** <how to produce this specific ad. If strategy/visual/targeting are `none`, this is
  the complete recipe. If they're set, this is only what's specific to this ad on top of them —
  including any deliberate deviation from the preset's values, and why.>
- **Copy:** <the actual text, and any per-variant text>
- **Creative files:** <filenames in this directory, and what each is for>
- **Variants:** <the tweakable axes and the options on each — e.g. a brand-themed treatment vs. a
  high-density treatment. Say which is the default.>
- **Platforms:** <which platform(s) in `platforms.md`, plus anything specific to this ad there>
- **Landing URL:** <including the campaign parameter, per `attribution.md`>
- **Offer:** <the discount this ad promises, per `offers.md`, or none>
- **Campaign naming:** <the campaign name/id this maps to, per the platform's granularity rule>
- **Results:** <appended after each run: dates, spend, impressions, CTR, signups, paid conversions —
  and a plain-language note on what seemed to work or not>
