---
name: factory-initiative-archive
description: Put an initiative on ice until you come back to it — stop its listening agent, move its channel out of the active list (a Discord archive category, or Slack's archive), and mark it archived in `factory/initiatives.md` and its identity doc, with everything that was in flight written down and the exact steps to bring it back. Also does the reverse (unarchive and restart the listener). Use when the user says "archive the <slug> initiative", "turn off <slug>", "shut that agent down and move the channel to archived", "factory initiative archive", or "bring <slug> back" / "unarchive <slug>".
user-invocable: true
---

# Factory — Initiative Archive

*Turning an initiative off should be as cheap as turning it on, and coming back should not mean
re-learning where it was.*

The inverse of [`factory-initiative-start`](../factory-initiative-start/SKILL.md). An archived
initiative keeps its identity doc, its history and its channel. It just has no agent listening, and its
channel is out of the way. Nothing is deleted.

Takes a `<slug>` (several are fine; do them one at a time). The slug must be a row in
`factory/initiatives.md`; if it isn't, say so and stop rather than guessing which initiative was meant.

---

## Step 0 — Read before touching anything

1. Find `factory/` at the repo root and read `factory/initiatives.md`, `factory/communication.md` (medium,
   credential, where the token lives) and `factory/initiatives/<slug>.md` in full.
2. Note the channel id, the medium, and the category or section the channel sits in now. You need these
   to bring it back.
3. **Write down what is in flight**, from the identity doc's Queue and Running log and from the machine:
   - Queue items not yet done;
   - sub-agents, dev stacks or devmgr slots, open branches, worktrees and PRs that belong to it;
   - anything the doc says is waiting on someone.

   Archiving never discards work. It records it. Don't merge, close or delete any of it; if something
   is actively costing resources (a running dev stack), stop the stack, but leave its branch and
   worktree in place and say so.

## Step 1 — Stop the agent

The listener is a long-lived session in a terminal-multiplexer tab, not a cron job. Find the right one
**precisely**; the machine has many similar sessions.

- **Herdr** (`HERDR_ENV=1`): `herdr pane list`, then `herdr pane process-info --pane <id>` on candidates.
  The listener is the `claude` process whose argv contains `factory-initiative-listen <slug>`, or a
  `--resume <session-id>` that you can match to the slug from the session transcript's first command.
  The tab is usually labelled with the slug, but a label is a hint, not proof.
- **tmux**: `tmux list-windows -a -F '#{session_name}:#{window_index} #{window_name} #{pane_pid}'`, then
  check the process tree under the pane pid.

Stop it gently first: send it a short message to wrap up and exit if it is idle, or send `/exit`. If it
does not exit, stop **that exact pid** (`kill <pid>`). Never use name-matching kills (`pkill -f`,
`killall`): they hit other agents and your own shell. Confirm the pid is gone. Then close the empty tab
or window, unless the user wants to keep it.

Leave the channel watcher's mark file in place. It records the last message seen, so on resume the agent
picks up everything posted while it was off.

If no listener is running, say so and carry on. Archiving a stopped initiative is normal.

## Step 2 — Say goodbye in the channel

Post one short message in the initiative's own channel *before* moving it. Say:

- that the initiative is archived and no agent is listening;
- what was left in flight (one line each);
- how to bring it back ("ask the general listener to unarchive `<slug>`", or the command).

## Step 3 — Move the channel

```bash
python3 "$SKILL_DIR/scripts/channel_archive.py" archive --medium discord|slack --channel <id> --env-file <path>
```

- **Discord:** moves the channel into an `Archived` category, creating it on first use with the current
  category's permission overwrites, so privacy doesn't change. History stays readable. The script prints
  `from_category`: **record it**, it's what restore needs.
- **Slack:** there's no API for sidebar sections, so the move is Slack's own archive
  (`conversations.archive`): the channel becomes read-only and leaves the sidebar. Some workspaces only
  let a user (not a bot) token unarchive. If the bot lacks the scope, say so and give the user the
  one-click instruction rather than working around it.
- `--category-name` changes the Discord category name, if the org uses a different one.

## Step 4 — Mark it archived

- **`factory/initiatives.md`:** set the row's Status to `archived <YYYY-MM-DD>` with a few words of why,
  in the user's words. Keep the row; the registry is also the list of things you can come back to.
- **`factory/initiatives/<slug>.md`:**
  - Add a **Status** line under Identity: archived, the date, why.
  - Update the Channel line to the new category or "archived (Slack)".
  - Add a **Paused work** section listing everything from Step 0.3 with where it lives.
  - Add a **To resume** section with the exact restore command, including `--to-category <from_category>`.
  - Add a Running log entry.
- If a general listener tracks initiatives in its own doc, log the archive there too.

## Step 5 — Report

One short message where the request came from: archived, agent stopped (or none was running), channel
moved to where, what's paused, and the one-line way back.

---

## Coming back (unarchive)

When the user wants an archived initiative back:

1. Read its identity doc, especially **Paused work** and **To resume**.
2. Restore the channel: `channel_archive.py restore --medium … --channel <id> --to-category <from_category>`
   (Discord), or `restore` for Slack, which unarchives.
3. Set the registry Status back to `active`, remove the Status line from the identity doc (or mark it
   resumed with the date), and log it.
4. Start the listener the same way `factory-listener`'s spin-up reference does: a new multiplexer tab
   running `<claude> "/factory-initiative-listen <slug>"`. Verify that it armed its channel watcher before
   saying it's back.
5. Post in the channel that it's back, and which paused items it will pick up first.
