# Spinning up a new initiative from the general listener

A known, tested pattern (first run end to end in the Komori repo, 2026-09-25). The user talks to the
`factory-listener` in its channel, names a new stream of work, and wants to be talking to a *separate*
agent about it a few minutes later without touching a terminal. The general listener does the whole
setup, then hands off to a fresh session running `factory-initiative-listen <slug>`.

**Only on the user's word.** The listener never creates standing agents because work *looks*
initiative-shaped. It does this when the user asks ("make an initiative for X", "spin up an agent
for X"), or says yes when the listener suggests it.

---

## 1. Set it up: `factory-initiative-start`, run by the listener

Invoke `factory-initiative-start` with the user's own words as the brief, and a proposed slug. The
user has asked for this to happen unattended, so answer the skill's questions from the repo instead
of stopping to ask:

- **Channel: create a new one.** Most chat APIs let the bot do it. For Discord:
  `POST /guilds/{guild}/channels` with `parent_id` set to the category the other initiative channels
  live in, and `permission_overwrites` copied from a sibling initiative channel
  (`GET /channels/{sibling}`), so privacy matches exactly. Send a real `User-Agent`: Discord 403s
  library defaults, and the error reads like a permissions problem. Check first that no channel with
  that name exists.
- **Credential:** reuse the one in `factory/communication.md`. Add the new channel's id to the repo's
  secret store under the same naming scheme as its siblings (e.g. `DISCORD_CHANNEL_<SLUG>`), and add
  it to the list in `communication.md`.
- **Scout it for real:** post a message, upload a file and read back since an id, using the same
  scripts the listeners use. Write down anything that fails.
- **Scope:** write it from the user's request plus a short look at the code: what exists today, which
  routes or components the work will touch, and what is explicitly out. Quote the user's own sentence
  as the "why".
- **Deploy behavior: copy the closest sibling initiative's answer** (usually deploy-to-dev, with
  production as its own explicit step). Ask only if no sibling applies.
- Write `factory/initiatives/<slug>.md` with the user's request as the **first Queue item**, and add
  the registry row to `factory/initiatives.md`. Confirm `.state/` is gitignored.

## 2. Hand off: a new session in a terminal-multiplexer tab

The new listener must be its own long-lived session, not a sub-agent of this one: it has to outlive
this session's turns and be something the user can see and attach to. Start it in a new tab of
whatever multiplexer the current session runs in, with the repo's Claude launch command:

```
<claude> "/factory-initiative-listen <slug>"
```

`<claude>` is however the user launches Claude Code (often a shell alias). Check it resolves in a new
shell (`type <alias>`) rather than assuming.

**Herdr** (`HERDR_ENV=1` means this session is in a Herdr-managed pane):
```
herdr tab create --cwd <repo root> --label <slug> --no-focus   # JSON → result.root_pane.pane_id
herdr pane run <pane_id> '<claude> "/factory-initiative-listen <slug>"'
herdr pane read <pane_id> --source recent --lines 200          # verify it started
```
- `herdr <group>` prints each group's syntax; the installed binary is the authority. Never run bare
  `herdr`: it attaches the TUI.
- Read with `--source recent`. `visible` can come back empty just after `run`.
- A new tab gets a fresh interactive shell, so the user's aliases work there.
- Treat every id as opaque, and re-read ids from the JSON the create call returns.

**tmux** (when `$TMUX` is set):
```
tmux new-window -d -c <repo root> -n <slug> '<claude> "/factory-initiative-listen <slug>"'
tmux capture-pane -p -t <slug> | tail -40
```
A command passed straight to `new-window` gets no interactive shell, so use the full path to
`claude` (plus its flags), not an alias.

**Neither:** don't background a detached process nobody can attach to. Post the exact command in the
channel for the user to paste into a terminal, and say so.

## 3. Verify, then say so

- Poll the new tab's output with a bounded until-loop, never a bare sleep, until the new session has
  loaded the identity doc and started its channel watcher. A session that died on launch looks
  exactly like one that is quietly listening.
- Post one short intro in the **new** channel: what it's for, and that an agent is listening. Post a
  one-line "done" in the general channel with the channel name and the tab label.
- Log it in `factory/initiatives/general.md` (channel id, tab id, the command run), so a resumed
  general listener doesn't set it up twice.

## Gotchas seen doing this

- **One watcher per mark file.** The new listener arms its own watcher. The general listener must
  not also watch the new channel.
- **Check that the watcher's process pattern actually matches.** `pgrep -f` matches its own shell,
  so confirm with `ps` before concluding a watcher is already running.
- **Bot posts don't wake the new listener.** Watchers filter out bots. The first request must come
  from the identity doc's Queue (seeded in step 1), not from a bot message in the channel.
- **Don't navigate or type into the user's own tabs.** Create a new tab, and use `--no-focus` so their
  screen doesn't jump.
