# Factory Ads — Offers & Discounts — <PROJECT NAME>

> Whether this business can run temporary deals, how they're created, and how far they can go. Read
> by `factory-ads-create` whenever an ad's angle is a price offer.

- **Offers enabled:** <yes | no — if no, say why and nothing else in this file matters>
- **Mechanism:** <exactly how a discount is created and redeemed — e.g. the API call that mints a
  coupon, the env var holding the key (name only), and the checkout path that accepts it. **Verify
  the redemption half exists**: being able to create a discount is useless if checkout can't apply
  one. If it can't, say so and name the product-side task needed.>
- **Cost structure / why aggressive pricing is or isn't safe:** <the reasoning, not just a number —
  what an extra user actually costs to serve. This is what lets a future run make a judgment call
  instead of asking again.>
- **Floor:** <the lowest acceptable price/discount>
- **Typical shape:** <e.g. "$1/month for 3 months, then standard pricing">
- **Duration limits:** <how long an offer may run, and whether it must have an end date>
- **Never:** <anything explicitly out of bounds — dark patterns, auto-renew traps, misrepresenting
  the standard price, or any claim the product can't honor>
