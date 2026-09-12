# Factory Ads — Targeting Preset — <preset name, e.g. "Follower lookalike + finance keywords">

> One file per reusable AUDIENCE CONFIGURATION, at `factory/ads/targeting/<preset-id>.md`. Targeting
> is *who sees the ad* — the third reusable dimension alongside `strategies/` (the argument) and
> `visuals/` (the production method).
>
> **Unlike strategies and visuals, targeting is inherently platform-specific** — the knobs on one ad
> platform have no counterpart on another. Every preset declares its platform and is only valid there.

- **Platform:** <which platform in `platforms.md` — a preset is never portable across platforms>
- **Ad-account level it applies at:** <campaign | ad group / ad set — per that platform's structure>
- **The configuration, field by field:** <every knob and its exact value, written so it can be
  reproduced from this file alone without re-deriving it: audience type, lookalike/similar-to seeds,
  keywords, interests, follower-look-alike handles, geography, language, age/gender, device,
  placements, bid strategy and optimization goal. Record what was set AND what was deliberately left
  at default, since "untouched" is itself a decision worth remembering.>
- **Where it came from:** <captured from a live ad group on <date> | hand-built | copied from
  <preset> and changed how>
- **Who this is trying to reach:** <the audience in plain language — the thing the field values are
  an approximation of. This is what makes the preset re-judgeable when the platform changes its UI.>
- **Fits which ad types:** <which strategies/ad shapes this audience suits, and which it doesn't. A
  price-led ad and an authority-led ad often want different audiences even at identical spend.>
- **Tuning notes / suggested experiments:** <what to try changing next and why — broaden vs. narrow,
  swap the lookalike seed, add/remove a keyword cluster. One knob at a time, or the result teaches
  nothing.>
- **Ads using this:** <links to `ads/` files>
- **What the results have taught us:** <appended over time — the reason this file exists>
