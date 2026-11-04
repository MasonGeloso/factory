# Faux Product UI: Stills, Product Animations, and Bento Grids

Build a miniature product interface that is drawn to be looked at, not used: a hero or feature-card
still, a short animated demo with or without a cursor, a window-and-satellite product shot, a bento
grid. Distilled from Stageshow; see `SKILL.md` for provenance.

**Use this when** the output is an illustration of a product: a marketing or docs hero, a feature card,
a launch visual, a bento section, an animated walkthrough on a page. **Use `make-a-prototype` instead**
when someone will really click it. Faux UI is authored: nothing has to work, so every frame is a
composition decision. A product mock inside `factory-education-video`, `factory-marketing-video` or an
ad follows these same rules for what is on screen.

**The one idea: it reads as a real product, simplified to what the viewer needs, framed with intent, and
every motion has a cause.**

It fails in five ways:

- **Too much.** Real text in every row, numbers everywhere. The more detail, the more it looks generated.
- **Wireframe.** Two gray blobs and a button: built too small, or stripped of what made it recognizable.
- **Boxed.** A whole window shrunk into a card with even margins: a screenshot pasted in, not a product shot.
- **Flat.** Every object the same weight in the same bordered card. The eye has nowhere to land.
- **Bland.** A gray window with a cursor, whatever the brief said. A brief's look and energy are the
  point: take them in full and build them to these rules.

The cure for all five: a full, structured screen in quiet grays, real words only on what the story is
about, placeholder lines for the rest, and a crop that puts the eye where the story is. **Simplify the
words, not the context.** An empty corner, a void under a list, or rows spread to fill a pane is
unfinished, not calm.

## Phase 1: Plan before any code

Most of the quality is decided here. Write down:

1. **Medium and place.** Still, or animation (loop, once in view, on hover). The page, its ground, its
   width. Design at the size it will be seen, shown 1:1: about 720×340 for a hero beside copy, 900–1100
   wide for a full-width hero, 400×300 for a card, never under about 320 wide for a demo (a bento tile or
   satellite may be smaller). Anything that can land in a phone column gets a separate compact
   composition at about 358 wide: crop closer, drop or stack the satellite, keep action and payoff whole.
   That is a redesign, not a squeeze; a scaled-down desktop passes an overflow check and is unreadable.
2. **Focal object, action, payoff, and what is left out.** Ask what the eye lands on first, and whether
   that is the result.
3. **Look.** With the product at hand, map its real tokens, icons and chrome; if it has components, use
   them. Otherwise commit via `frontend-aesthetic-direction`. Pick a fidelity: all placeholder bars,
   words where they carry meaning (the default), or real content everywhere (for full-width heroes, named
   real products, and stills whose subject is a list or page).
4. **String budget.** Count the real strings, usually 3–7: the title, the thing acted on, what is typed,
   the result. This budgets words, not elements: a calendar still needs a populated week.
5. **A reference to beat.** Name the best comparable product shot you can find, in the repo or from a
   product page, and keep it beside your frame. If yours is the emptier, flatter or smaller one, that is
   the first fix. For a whole page of these, set one figure language first: one ground, one gutter, one
   window shadow, one radius set.

## Phase 2: Frame it

How the screen sits in its space decides product shot versus screenshot in a box. Frame before building
the screen: a crop needs nothing past the crop, and it sets how big the type must be.

- **One hero, at most one or two satellites** (a receipt, phone or detail card) that carry the point.
- **Crop 10–40% of the hero off stage.** It fills at least two thirds of the stage width and runs off an
  edge. Small formats crop harder: a 400px card holds a third of a dashboard at full size, not all of it
  at a third.
- **Crop only filler.** The payoff, the action, what the cursor touches and every real word stay whole. A
  button, chip or shadow sliced by the stage edge is the usual fault; remove a placeholder action rather
  than slice it.
- **The page is the ground.** No tinted plate behind a window on a white or dark page. A whole window
  centered with air on four sides floats. Show it whole only when the brief asks.
- **One gutter.** Every edge distance in the final crop matches it, a full gutter or well past. Crossing
  an edge by under 24px, or stopping a few pixels short, reads as a mistake.
- **Satellites straddle the hero's edge, about half outside,** over chrome or margin, never over content
  or the figure they explain. A second satellite differs in size and kind; two equal cards read as a pile.
- **Anchored UI (popover, menu, toast) is not a satellite:** it sits where the product would put it.
- **What the story opens stays in frame** a gutter from every edge, on every frame.
- **Windows keep their device's shape:** 1.25:1 or wider when whole, at least square when bled. Fix by
  crop or layout, never by squashing.
- **On a colored stage,** inset the hero 8–20% from the sides and run it off the bottom.
- **Start flat and frontal.** Depth comes from shadow, z-order and scale. Tilt must be earned against the
  straight version at final size; paper piles are the one place it reliably does.
- **No dead corners,** at rest or anywhere in the loop. Fix the crop before adding anything.

| Layout | Composition | Use for |
|---|---|---|
| Pinned, bottom bleed | Inset 8–12% left, right, top; 15–35% off the bottom | Feature cards, bento tiles |
| Corner bleed | Inset 10% top and left; 15–35% off right and bottom | Heroes beside copy |
| Wide hero | 900–1100px window at 1:1, off the bottom; realistic content | Full-width homepage heroes |
| Satellite focus | Hero cropped hard as context; satellite 30–40% of its width carries the story | One small thing: a notification, a receipt, a diff |
| Device pair | Desktop 75–80% wide, off the bottom; phone straddles the right edge, a third outside | Cross-device stories |
| Close-up | Whole window scaled 1.3–1.6×, chrome included, subject row whole | One control or setting |
| Panel over product | Settings panel straddles the margin; one leader line to what it changed | A setting and its effect |
| Row of windows | Three or four at one height, outer ones off both sides | Agents, tabs, sessions |
| Many of one | A grid of one thing off every edge; one in focus by depth, the only one with words | Scale shown as repetition |
| Fade crop | Window fades over its last third, by mask, over filler, at the foot only | When a hard cut would land arbitrarily |

## Phase 3: Build the still

**Restraint**

- Bars are filler and the subject is words. Gray bars where the eye lands read as unfinished; bars vary
  in width row to row (60, 45, 70, 52) and sit in the line box of the text they replace.
- Where the story touches a list, two or three real rows and at most as many bars. In a small surface a
  row is one line: avatar, name, value.
- One number gets to be big. Say each thing once. No signal repeated in header, satellite and every row.
- Keep the domain's signature content (album art, thumbnails, avatars). Without it, it is a generic list.
- Label and value match: both words or both bars. A blank pill beside a real control is dead.
- No masthead for a fictional product. Show its name only where the real product would.
- Compose objects, not an inventory of cards: hierarchy from proportion, space and material. Judge the
  silhouette at thumbnail size before the details.
- Choose copy whose length fits, so no name or chip truncates or wraps.

**Type and spacing**

- 11–15px UI text at shown size, never smaller to fit more. Line height at least 1.3. Sentence case
  unless the real product capitalizes. One family; monospace only for code, identifiers and aligned
  numbers.
- Words keep a 12px inset from any edge; bars may bleed. Row padding 12px, 8px when dense. A button keeps
  8px or more from what sits above it. Fixed gaps of 8–12px, not leftover `space-between`.
- A title over its subtitle reads as one item: 4–6px of ink between them. The air belongs to the row.
- **No near-tangents.** Edges 1–3px apart look accidental: align them exactly or part them by at least
  8px. Nested shapes pad evenly, with outer radius equal to inner radius plus the padding.
- Center on visible ink, not line boxes: `text-box: trim-both cap alphabetic` for labels in pills, buttons
  and discs. In a centered amount, the digits are the centered box and the currency sign hangs off left.
- Rows share one grid template with fixed tracks. Dots, badges and rings sit in a gutter, 6px clear,
  never in a column of their own. A control hugs its content; a filled pill is never `flex: 1`.

**Icons, color, chrome**

- Icons come from the product's pack, else one set chosen on purpose, at one size and one stroke per
  scene (14–16px). Filled styles at 14px and under, where thin outlines go wiry. Never hand-drawn, and
  emoji are content, never icons. Icons are one opaque color; fade with `opacity`.
- **No sparkles, wands or purple as shorthand for AI;** show what the AI does. No invented logo: a letter
  in a colored square is not a mark. Use the real mark or a plain wordmark.
- One neutral family and one accent. Status colors mean status. A gradient or glow serves the story or
  goes. Don't ring the hero to point at it; lift it with its own surface or shadow.
- Nothing translucent overlaps. On dark, depth comes from lighter surfaces, not shadow. Quiet is not
  faint: check text against its real ground. Filled buttons step within their own color on hover.
- Never draw platform chrome from memory; look at the real thing. System surfaces keep true proportions:
  a notification stays at native width, the clock is never shrunk. The status bar and home indicator are
  drawn once, and nothing sits under the island. A phone is lit from its first frame.
- Browser chrome only when the browser is part of the picture; a desktop app gets its real chrome.
- Faux headings are `div`s, never `h1`–`h6`: the scene lives inside someone else's page outline.

## Phase 4: Choreograph

**Story.** Choose the shape from what the product is valued for: *how it feels to use* (one satisfying
gesture, with the result under the hand), *a flow* (a few screens as one continuous object), or *what the
system does* (the consequence lands elsewhere, the link is visible, usually no cursor). A hero loop is
10–16 seconds with 3–5 beats and a payoff. **Between a richer story and a calmer frame, choose the
frame.** Cover each moving element in turn; if the story gets clearer without it, cut it.

**Open and close.** Open on a finished screen that works as a still. The payoff arrives full and visible
at shown size. It holds for about 2 seconds, and nothing sits still for more than 3. Choose a poster
frame that tells the story alone, because that is what thumbnails, screenshots and reduced motion show:
leave the result on screen, and never pick a frame caught mid-change.

**Pace.** Two curves: travel `cubic-bezier(0.45, 0, 0.1, 1)`, arrival from nowhere
`cubic-bezier(0.25, 0.8, 0.25, 1)` over 0.8–1s. Feedback inside the scene stays as quick as the real
product and starts on the input; only storytelling motion slows down. Related responses overlap, offset
so their order reads, with the result after its cause. Stagger in reading order 40–80ms apart, 80–120ms
between grid tiles. Landings decelerate softly with no bounce or ring pulse. Holding a result means stop.

**Change.**

- Every change moves, and only what changed moves. Text rolls its changed span; numbers roll with
  unchanged digits still; a surface morphs. Reserve a control's largest footprint before its label
  changes, with button states sharing one slot.
- Nothing pops. Things stay mounted through their exit, and a replacement arrives as the old one leaves.
- Insertion changes two things: animate the newcomer *and* its neighbors. A new row carries the rows
  below it; an added icon opens its width and gap together.
- A resizing surface moves size, position and content as one transition, and never stretches its text.
- Solid things never fade through. Windows, phones and cards arrive by moving, opaque or nearly. Cards
  and toasts arrive whole from just above, never uncovered by a hard edge; no moving edge slices text.
- Open surfaces hold their anchor edge, and popups fit before their first frame.
- One object, one trip. Open the room, measure the slot, fly, land on its final geometry. On the handoff
  frame it is the same size, place and look. A flyer's ends are fixed at take-off, and it changes to its
  resting look during the last third of the trip.
- Result follows press: a small press response first, then the change.
- An object keeps its identity: a plus becoming a close rotates the same strokes. A spinner is already
  turning when it appears, and keeps turning through its fade.
- Draw a chart on from its start, line first, area under it, end dot landing as the line arrives.

**Cursor.**

- No cursor means no stand-in: never walk a focus ring or spotlight between controls.
- Every move travels to the next action, follows a held object or clears the way. Between beats it rests
  on empty surface near its next move.
- It never covers the words it clicks (aim off the text, about 85% across), and it stays where the press
  happened while the result changes size.
- Its shape comes from what it is over, switching mid-path by morphing. Measure target positions from the
  DOM; never hard-code them.
- Touch stories use a touch indicator, not an arrow, with UIKit-quick responses (about 0.5s,
  `cubic-bezier(0.3, 0.75, 0.1, 1)`). Keyboard stories show the keycaps.

**Drags.** A drag starts where the thing is, with a fixed grab offset. A held item rides the pointer
exactly, with no transition: scale 1.03, deeper shadow, a degree or two of tilt on the whole card. Drop
targets never travel. A text selection reads left to right from a word boundary and stays under the
I-beam every frame, so drive it from the pointer position, never from a timer.

**Loops.**

- A reset removes what the loop added as one thing, within half a second, 40–80ms apart in reverse order.
- Every reset has a seen cause (undo, clear, close), or exits around an anchor, or snaps while hidden.
- Data never rewinds in view. A loop never plays a navigation backwards; leave the way the product leaves.
- Within about a second of the exit ending, the next action has begun.
- A second scene adds something new or is cut. Camera moves need a reason: at most one push-in, only when
  the payoff would otherwise be unreadable, and it never rescues a weak wide shot.

## Phase 5: Bento grids

A bento grid is one picture made of tiles, not five demos side by side. Write the tile list first (tile,
span, kind, the one thing, words), then check it against these rules:

1. **Not every tile is UI.** About a third to a half are; the rest are other kinds. A grid of cropped
   windows reads as generated however well each is made.
2. **One hero,** bigger by two columns or two rows, carrying the main idea.
3. **A UI tile shows one thing, not a window.** Crop to one component at real size or larger. Window
   chrome appears at most once, on the hero.
4. **Neighbors contrast,** across and down: picture beside number, dense beside calm. Two window crops
   never touch.
5. **Big type is a tile.** One real number at 48–72px, a short lead, a one-line label, on one unwrapped
   line. Real figures, never "10x" filler. A statement in large type counts too.
6. **Copy is short and outside the picture:** 1–4 words or one sentence, at 17–24px as page type, not the
   12px of the UI inside the tile.
7. **One frame, varied contents.** Tiles share radius, gap, padding and where the copy sits. Pick rounded
   tiles on a gap, or one ruled container with no gaps.
8. **Say each thing once across the set.** No string, avatar or color mark repeats from tile to tile.
9. **Compose the grounds together.** One shared surface with one photo, accent or inverted tile as
   punctuation, or several grounds with a deliberate rhythm in lightness and temperature.
10. **Motion has one place to lead.** A supporting tile does one small thing, once on scroll-in or on
    hover. Competing loops leave the eye nowhere to land.
11. **Each picture is its own stage at 1:1.** Never scale the whole grid as one image, which shrinks all
    its type. Match each picture to its slot at every width, and inspect its right and bottom edges for an
    unintended inner cut.
12. **Every width is its own design.** Pick breakpoints from the content, stack hero-first when two
    columns stop being readable, and keep important text at 10px or above at a 320px host.

Tile kinds: one component, hero UI, stat, statement, object, diagram, collection, photo. A grid of five
usually wants one hero UI, one or two components, one stat or statement, and one object, diagram or
collection. Default layout: a 2/3 + 1/3 row over three equal tiles. Photo tiles use real licensed photos;
a scene drawn in SVG or CSS to stand in for one reads as generated, so choose another kind instead.
Objects get one light source, a real material, and their true anatomy.

## Phase 6: Rehearse and review

A still can't show a pop, and matching endpoints prove nothing about the frames between. Film it with
`playwright-cli`:

- **Stills at every width and look the brief names:** the shown width and 390, light and dark if both
  apply. A light pass does not prove dark.
- **Step through the frames.** For CSS and Web Animations, pause and seek with
  `document.getAnimations().forEach(a => { a.pause(); a.currentTime = t })`. Otherwise record video and
  cut a contact sheet: `ffmpeg -i demo.webm -vf "fps=8,scale=480:-1,tile=6x4" sheet-%02d.png`. Step every
  press, menu, morph and handoff, and cut the loop seam at 60ms intervals.
- **Inspect at real size, then zoomed 4×** on glyphs at the moment motion ends, where text snaps.
- **Fix the largest visible fault first:** framing, then hierarchy and density, then motion, then polish.
  Re-film after each round. After moving a window, recheck the crop and the whole loop.

Then hand the frames and a one-line brief to a fresh subagent, without your plan or reasons. It screens
for the one wrong thing, the way the most exacting designer you know would, and returns a ranked list:
what it would screenshot, which frame shows it, the fix in one line. Its first question: could this
composition be any product in its category? Every finding quotes a frame. A predicted failure or pass is
not a finding, and neither is a real platform convention.

Say plainly which frames, widths and looks you checked and which you did not.

## Running `polish-pass` on a faux scene

Run `polish-pass` as the final gate, and give its agents these adjustments, since the scene is an image
rather than an application:

- **Accessibility:** the scene is one image. Hide it from assistive tech (`aria-hidden`, or `role="img"`
  with a label stating the point), keep nothing inside it focusable, and give any motion lasting over 5
  seconds a pause control. Under `prefers-reduced-motion`, show the poster frame.
- **Interaction states:** fake controls need only the states the story shows. The audit applies to real
  controls on the page around it.
- **Transitions:** the 0.2–0.3s rule governs feedback inside the scene. Storytelling travel and arrival
  run longer, as in Phase 4.
- **Slop check:** a product's real font and platform conventions stand, including a system stack in a
  native-app mock. For a fictional product, the font is still chosen on purpose.
- **Honest numbers:** illustrative figures are for illustrative scenes. Any stat, claim or result the page
  presents as true must be real and traced to its source.
