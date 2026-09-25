---
name: factory-implement-light
description: The reduced factory pipeline for small/medium requests inside an initiative-listener loop — plan → one critical-only review gate over the plan (borderline findings get asked as a short question instead of silently noted, and the run waits for the answer) → execute → a quick recheck → factory-demo-light → deploy per the initiative's recorded deploy behavior. Skips re-research, the post-execute code-review gate, and the QA gate entirely — this is the fast, conversational path, not the full `factory-implement` driver. Use when `factory-initiative-listen` or `factory-listener` picks up a small/medium request, or when the user explicitly asks for the light pipeline outside a listener.
---

# Factory — Implement Light

*The pipeline `factory-initiative-listen` reaches for by default. Plan it, get one fast critical-only
check on the plan, build it, prove it works with the minimum evidence, ship it.*

This is a deliberately thinner sibling of [`factory-implement`](../factory-implement/SKILL.md) — same
underlying skills, fewer gates, built for a conversational loop where the person on the other end of the
channel is available to answer a quick question rather than wait for a full second-opinion review cycle.
**Not** a replacement for `factory-implement` on anything genuinely large — that's what the listener's
sub-agent escalation is for (see `factory-initiative-listen` Step 2).

Normally invoked by `factory-initiative-listen` / `factory-listener` against one queued request, with a
channel to post to. If invoked standalone (no listener context), ask the user directly wherever this
conversation is happening instead of posting to a channel — everything else is identical.

---

## Step 0 — Config check

Same as `factory-implement` Step 0, minus the parts that don't apply here: locate `factory/`, read
`factory/intake.md` / `ownership.md` / `codebases.md` / `deployment.md`. **Do not** run full
`/factory-onboard` mid-conversation for a missing optional module (`code-review.md`, `plan-review.md`)
— if those are missing, just skip the review gate below and say so in the running log; don't stop the
loop to onboard something optional. If the core execution config (`codebases.md`/`deployment.md`) is
genuinely missing, that's the one case worth pausing for — ask in-channel before proceeding blind.

## Step 1 — Plan

Call the Skill tool: `factory-plan`. Write the plan to `./tasks` as usual. **Skip
`factory-reresearch`** — the light pipeline trades re-research depth for a human who's actively
available to answer questions, which the next step uses.

## Step 2 — One review gate, critical-only, ask on borderline

This is the one genuinely new behavior in the light pipeline — every other step below reuses an
existing skill unmodified.

1. Run the review exactly as [`factory-plan-review`](../factory-plan-review/SKILL.md) Steps 1–3
   describe (read the plan, the request, relevant existing code; score the same categories:
   completeness, doc/convention adherence, reuse/simplification, risk/unknowns, plus
   `factory/plan-review.md`'s project checklist if present) — reuse its external-tool config
   (`factory/code-review.md`) the same way `factory-implement` Step 3.3 does, or run it in-context if
   none is configured.
2. **Change the gate policy from PASS/FAIL to critical/ask:**
   - Any **❌** finding blocks — fix it (back to Step 1 if needed) and re-run this gate.
   - Any **⚠️** finding does **not** block automatically. Post it back to the channel as a short,
     single question — "found X, seems minor, skip it or should I fix it?" — and **wait for the
     answer** before proceeding. Don't batch multiple ⚠️ findings into one long message; if there are
     several, ask about the most consequential one first and only raise the rest if it's still unclear
     whether to proceed.
   - No open ❌ and no unanswered ⚠️ question → continue to Execute.
3. If `factory/plan-review.md` doesn't exist and no external tool is configured, run this review
   yourself in-context anyway — unlike `factory-implement`'s optional gate, this one isn't skippable
   just because the project file is missing, since it's the *only* review this pipeline runs.

## Step 3 — Execute

Call the Skill tool: `factory-execute`. If the task touches a real UI surface, also call
[`factory-frontend`](../factory-frontend/SKILL.md) during this phase, same as the full driver.

## Step 4 — Quick recheck

Call the Skill tool: `factory-recheck`. It's already fast — run it as-is, no reduction needed. FAIL →
fix and re-run; don't loop indefinitely without posting a status update if it's taking a while.

**No post-execute code-review gate. No QA gate.** The plan-stage review in Step 2 plus this recheck are
the only review this pipeline does — `factory-demo-light` next is what actually shows the user it works,
and their own read of it in-channel is the final check.

## Step 5 — Demo-light

Call the Skill tool: [`factory-demo-light`](../factory-demo-light/SKILL.md) against the change. Produces
one piece of minimum-sufficient evidence (a screenshot, a short clip, a log excerpt, or an Artifact
link) — not the full video-plus-stills package the standard pipeline produces.

## Step 6 — Deploy

Per this initiative's recorded deploy behavior (`factory/initiatives/<slug>.md`'s Deploy behavior
section):
- **Deploy-to-dev** — deploy now, per `factory/deployment.md`'s real commands. No ask needed.
- **Ask-before-deploy** — the demo-light evidence from Step 5 **is** the proof; post it in-channel and
  wait for a go-ahead before deploying. Don't deploy on silence.

## Step 7 — Post the result

Concisely, per `factory-initiative-listen`'s reply-style rule: link, screenshot, or whatever the demo
produced, plus a one-line description of what shipped. No report-shaped write-up. Then record it in the
initiative's Running log (move the Queue line there).

---

## What this skips, on purpose, and why it's safe here

| Skipped vs. `factory-implement` | Why it's OK in this context |
|---|---|
| Re-research rounds | The human is actively available to answer the Step 2 question instead |
| Post-execute code-review gate | The Step 2 plan-stage review already caught the critical stuff before any code was written |
| QA gate (real-user-scenario walkthrough) | Demo-light's evidence + the user's own eyes-on in the channel replace it for small/medium changes — this is exactly the tradeoff that made the pattern work in practice, not a corner cut silently |
| Full demo (video + stills + artifacts.md) | Minimum sufficient evidence, per `factory-demo-light` |

If a request turns out to be bigger than it looked once planning starts, **stop here and escalate** —
go back to the listener and spawn a sub-agent with `/goal /factory-implement` instead of pushing a big
change through the light gates. This pipeline is deliberately not built to catch everything a full
`factory-implement` run would.
