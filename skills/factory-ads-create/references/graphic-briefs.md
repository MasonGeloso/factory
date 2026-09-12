# Briefing a graphic to a design-capable model

Graphics for these ads are generated as **self-contained SVG** by a design-capable model, then
composited into the brand shell. The brief is the artifact worth keeping — the picture is
reproducible from it, and a good brief is a few hundred words.

## Invocation

Any CLI agent with a design-capable model works. What matters is a sandbox that can write a file,
and a model that is actually good at vector layout. Verify the model id before a batch — a wrong id
fails fast and loudly, which is preferable to a silent fallback.

Run briefs **in parallel, one working directory each**, with `BRIEF.md` and any `PRIOR.svg` in the
directory and a one-line prompt telling the agent to read them and write `graphic.svg`. Four
concepts in parallel cost about as much wall-clock as one.

## The brief skeleton

```
## Canvas
Exact viewBox. Which vertical band the graphic may occupy. Which bands must stay EMPTY
(the headline and any footer are composited over it later). Side margins.

## Palette — EXACT hex only
Every colour, named, from the project's real design tokens. Say which is the hero accent.
Say explicitly: do NOT draw a full-canvas background rect (it covers the composited logo).

## Type
The two faces. A hard minimum size. A cap on the number of labels.

## The idea
What the viewer must UNDERSTAND, in plain prose. Not what to draw — what it must mean.

## Draw
The elements, and what each one represents. Enough to be unambiguous, loose enough to invent within.

## The bar
The register, named concretely. The failure mode to avoid, named concretely.

## Hard rules
Self-contained SVG, no external refs, no raster. No logo/headline/price/URL/CTA.
No real identifiers on invented events. Nothing clipped. No overlapping text.
Output ONE file. No commentary.
```

## What actually moves quality

- **Brief the idea, not the geometry.** Specified coordinates produce compliance and no invention.
  A described idea plus a quality bar produces the erosion particles, the target bracket, the
  vanishing point, the readout panel — none of which were asked for.
- **Name the failure.** "The previous attempt was rejected as boring: flat, light, sparse, a
  typography slide" changed the output more than any positive instruction.
- **Permission is not enough — instruct.** "Filters are allowed" gets flat output; "use SVG filters
  aggressively for depth and glow" gets depth and glow.
- **State the stop-scrolling bar.** Say the viewer must stop because it looks extraordinary, before
  reading anything.
- **Every mark must mean something**, and say so in the brief. Include the test: cover every label —
  if it stops communicating, it has failed.

## Revisions

Hand back `PRIOR.svg` plus a brief that says *keep everything, change only this list*. Revision
briefs work well and are cheap. For a localisation, say it is a localisation pass and that only text
changes — then warn that the target language sets to a different width and every label must be
re-fitted.

**Never hand-edit generated filter geometry.** Erosion, glow and mask effects are anchored per
element; moving a text node's `y` pulls the glyph out of its own mask and it disappears, leaving
only the particles. Give the defect back to the model.

## Traps

- Text inside a generated SVG never passes through the copy pipeline, so **no de-slop scanner ever
  sees it.** Graphic labels are copy. Check them by hand.
- `clamp(..., Nvw, ...)` resolves against the export viewport, not the canvas. Check the PNG.
- A graphic with content near the top will reveal any stacking-order bug in the shell. Give the
  brand bar an explicit z-index above the graphic layer.
- Generate one graphic per language, always.
