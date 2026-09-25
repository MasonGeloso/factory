# Initiative — <slug>

> Identity + running state for one `factory-initiative-listen` session. Read in full on every
> resume; kept current by the session itself throughout the day — this is how a brand-new session,
> started after the previous one was lost or shut down, picks back up without full chat history.

## Identity
- **Slug:** `<slug>`
- **Scope:** <what this initiative owns — a feature area (e.g. "translations on the retail site"),
  a whole small app, or "everything" for the general `factory-listener`>
- **Channel:** #<channel-name> (<medium>, ID `<...>`)
- **Started:** <date>

## Channel capabilities (from scouting during start)
- **Can post plain messages:** <yes/no>
- **Can upload files/images:** <yes/no — exact call used, e.g. Slack `files.upload_v2` / Discord multipart>
- **Can read since a timestamp:** <yes/no — exact call, same shape as `communication.md`'s read protocol>
- **Auth:** <env var name only — reuses `factory/communication.md`'s credential if this repo already has one, otherwise the one set up during start>

## Deploy behavior
> Decided once, during `factory-initiative-start`, specific to this initiative — a sibling initiative
> in the same repo may answer differently.
- <**deploy-to-dev** — describe the environment and how the user can reach/audit it any time, no ask needed>
- <**ask-before-deploy** — show proof (screenshot/artifact/log) in-channel and wait for a go-ahead before deploying>

## Pipeline mode
- **Default:** `factory-implement-light` for anything small/medium.
- **Escalate to a sub-agent** (`/goal /factory-implement <fully written-up requirements>`) when: <this
  initiative's own bar for "big" — default: multi-file/multi-day scope, or the user explicitly says
  "spawn a sub-agent for this">. Check in on it periodically; don't babysit it turn by turn.
- **Spin off a sub-agent for genuinely out-of-scope emergencies** (e.g. an unrelated production
  incident) instead of derailing this session's own scope.

## Queue
> FIFO. The user comes and goes and fires off requests ad hoc — append every new one here as it
> arrives, even mid-task, and work them in the order received. Move a line into the log once done.
- [ ] <request — one line, who asked, when>

## Running log
> Short entries, newest last. What shipped, what this session learned about the initiative or the
> codebase, decisions made without asking (and why), anything a fresh resume needs to know.
- <date> — <one or two lines>
