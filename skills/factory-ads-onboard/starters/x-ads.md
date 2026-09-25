# Starter — X Ads (ads.x.com)

> Seed for an `## X Ads` section in `factory/ads/platforms.md`. This is a **starting skeleton, not a
> verified transcript** — X changes its ads UI often, and a stale click path is worse than none.
> During onboarding, walk the real flow to the review step and replace every `<confirm live>` below
> with what you actually saw. Delete this warning once the section is filled in.

- **Dashboard URL:** `ads.x.com`
- **Account switch (MANDATORY, every run — an action, not a check):** the ads dashboard inherits
  whichever X account is active in the browser session, so **the wrong account is a live risk here
  exactly as it is for posting.** If this project already has an X section in
  `factory/marketing/platforms.md`, that file's switch procedure is the authority — perform it on
  `x.com` FIRST, confirm it landed, and only then navigate to `ads.x.com`. Never switch accounts from
  inside the ads dashboard and assume it took.
  - Also confirm **which ad account** is selected once inside — an X user can have access to more
    than one, and the selector is separate from the account switch above.
- **Click by element `ref`, not by screenshot coordinates.** The claude-in-chrome screenshot is
  scaled relative to the real viewport, so a coordinate read off the image can land somewhere else
  and the click silently does nothing. Use `find`/`read_page` to get a ref. This has bitten X's UI
  repeatedly.
- **Structure:** X organizes spend as **campaign → ad group → ad**. The budget lives on the campaign
  (and optionally the ad group); targeting lives on the ad group; the creative lives on the ad. Which
  level this project treats as "one ad" is the campaign-granularity decision — write it down.
- **Targeting lives on the ad group.** X exposes, among others: **follower look-alikes** (target
  people who resemble the followers of handles you name), custom/similar audiences, keywords,
  interests, geography, language, gender/age, device and placements — plus the bid strategy and
  optimization goal, which behave like targeting in practice because they decide who the auction
  actually serves. **If ad groups already exist on this account, copy their full configuration into a
  `targeting/` preset before changing anything** — this is usually configuration a human thought hard
  about, and it is much cheaper to record now than to reconstruct from a redesigned UI later.
- **Creating a campaign:** `<confirm live>` — objective selection, funding source, campaign budget +
  schedule, ad group targeting, creative selection/upload, placements, then a review screen. Record
  the exact point of no return, and note that a **funding source must already exist on the account**
  or the flow dead-ends near the end.
- **Setting the budget cap:** `<confirm live>` — X offers daily and (for some objectives) total
  campaign budgets. Record which field this project uses, since the platform's own cap is what
  enforces spend.
- **Reading analytics:** `<confirm live>` — the campaign list shows spend, impressions, engagements
  and CTR per campaign; per-campaign detail is a further click. Record the exact path, the date-range
  control, and which columns must be enabled to see the metrics this project cares about.
- **Excluded from analysis — boosted posts.** Boosted/promoted posts created outside the campaign
  builder are not comparable to a real campaign: different objective, different targeting, different
  optimization. **Ignore them entirely in every baseline and every assessment.** Confirm with the
  user whether any other historical format should be excluded for the same reason.
- **Never point playwright-cli or any headless browser at this account.** Chrome only — the account
  suspension risk is the same as for posting, and an ad account carries a payment method.
