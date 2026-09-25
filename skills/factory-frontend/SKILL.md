---
name: factory-frontend
description: Design-system-grade operating principles and procedures for any frontend/UI work — aesthetic direction, wireframing, hi-fi prototyping, tweak panels, accessibility/interaction/hierarchy audits, and a pre-ship polish pass. Adapted from Trystan-SA's claude-design-system-prompt for Factory's autonomous pipeline (no upfront question rounds — resolve from the task/plan/codebase, state assumptions, keep moving). Invoked by `factory-prototype`'s frontend track and by `factory-implement`/`factory-execute` whenever a task has a real UI surface. Use when the user says "factory frontend", "design this properly", or whenever building or reviewing a UI inside the Factory pipeline.
---

# Factory — Frontend

*Bring an actual designer's judgement to UI work, not the safest, most generic version of the screen.*

This skill is a straight adaptation of
[Trystan-SA/claude-design-system-prompt](https://github.com/Trystan-SA/claude-design-system-prompt)'s
`claude/` system prompt and skill set — copied in as plain files (no git subtree/submodule), then edited
in one specific way: the original assumes an interactive design session where the model asks the user a
kickoff question round before building. Factory's pipeline is autonomous (`factory-implement`,
`factory-execute`, `factory-prototype`) — there is no one standing by to answer a question round. Every
"ask the user" instruction in the original has been replaced with "resolve it from the task, the plan,
and the codebase; if it's genuinely unresolvable, make the most defensible call and say so as a stated
assumption" — the same posture `factory-implement` already uses everywhere else (see its
"Keep the tracker as a live log" rule). Everything else — the aesthetic judgement, the anti-AI-slop
defaults, the review procedures — is unchanged from upstream.

## How to use this skill

1. **Read [`system-prompt.md`](system-prompt.md) in full and adopt it as your operating principles for
   the rest of this frontend work.** It is not a separate persona to role-play — it's the standard this
   skill holds UI output to: rooted in existing design context, purposeful (not trend-following)
   aesthetics, real hierarchy and rhythm, accessible by default, every interactive state present, no
   filler content, no unrequested scope.
2. **Section 20 of `system-prompt.md` ("Available skills") names companion procedures**, one file each
   under [`skills/`](skills/) in this directory (`skills/factory-frontend/skills/<name>.md` from the repo
   root). These are plain reference docs, not separately Skill-tool-invocable skills — when the task
   matches a procedure's trigger, **read that file and follow its phases inline**, in the same turn.
   Don't try to invoke them by name through the Skill tool; there's no registration for them.
3. Chain procedures as the brief calls for — e.g. `frontend-aesthetic-direction` → `wireframe` →
   `make-a-prototype` → `polish-pass` for a greenfield build; `design-system-extract` →
   `generate-variations` → `polish-pass` when a design system already exists. `polish-pass` (which
   itself runs `accessibility-audit`, `ai-slop-check`, `interaction-states-pass`, and
   `hierarchy-rhythm-review`) is the standing pre-ship gate — run it before handing any UI back.

## What changed from upstream, and why

- **Dropped `discovery-questions.md` entirely.** Its whole purpose is a kickoff question round via a
  `questions_v2` form tool that doesn't exist here, and Factory's pipeline doesn't pause for one anyway.
- **Rewrote every "ask the user" instruction** in `system-prompt.md`, `frontend-aesthetic-direction.md`,
  `make-a-deck.md`, and `make-tweakable.md` into "resolve from context, then state the assumption" —
  most visibly, chapter 3 ("Asking questions first" → "Assumptions, not question rounds").
- **Left the design judgement untouched**: the anti-AI-slop defaults (chapter 6), hierarchy/rhythm/type
  scales, accessibility bar, and all review procedures are copied verbatim from upstream.

If upstream publishes updates worth pulling in, re-diff by hand against the source repo — there is no
sync mechanism here, this is a point-in-time copy.

## Where this is wired in

- **[`factory-prototype`](../factory-prototype/SKILL.md)**, frontend track step 3 ("Design it, don't lay
  it out") — invokes this skill for aesthetic direction, typography, motion, and the polish-pass gate
  before handing the prototype back for review.
- **[`factory-implement`](../factory-implement/SKILL.md)** — during Step 3's Execute phase
  (`factory-execute`), for any task with a real UI surface; and its QA/polish bar in Step 6 leans on the
  same standard this skill sets.

Both call it **by name** with the Skill tool, the same way they call every other `factory-*` skill.
