#!/usr/bin/env python3
"""Archive or restore an initiative's channel.

Discord: moves the channel into an archive category (created on first use, with the permission overwrites
of the channel's current category, so privacy does not change). Restore moves it back to the category it
came from. The channel and its history stay readable.

Slack: archives the conversation (`conversations.archive`). Restore calls `conversations.unarchive`.
Slack has no API for sidebar sections, so this is the only move there is; an archived Slack channel is
read-only, and a workspace may require a user (not bot) token to unarchive.

    python3 channel_archive.py archive --medium discord --channel 123 --env-file .env
    python3 channel_archive.py restore --medium discord --channel 123 --to-category 456 --env-file .env
    python3 channel_archive.py archive --medium slack --channel C0123 --env-file .env

Prints one JSON line describing what changed (keep it: `from_category` is what restore needs).
Fails loudly: any API error exits non-zero without guessing.
"""

import argparse
import json
import os
import sys
import urllib.request

DISCORD = "https://discord.com/api/v10"


def env(path: str | None) -> dict:
    values = dict(os.environ)
    if path:
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                values.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    return values


def call(method: str, url: str, headers: dict, body: dict | None = None) -> dict:
    req = urllib.request.Request(url, method=method, headers=headers,
                                 data=json.dumps(body).encode() if body is not None else None)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        sys.exit(f"{method} {url} -> {e.code} {e.read()[:300]!r}")


def discord(a, E) -> dict:
    token = E.get(a.token_env or "DISCORD_BOT_TOKEN") or sys.exit("no Discord bot token in the env")
    # Discord rejects default library user agents with an error that reads like a permissions problem.
    h = {"Authorization": f"Bot {token}", "User-Agent": "DiscordBot (https://github.com, 1.0)",
         "Content-Type": "application/json"}
    ch = call("GET", f"{DISCORD}/channels/{a.channel}", h)
    guild, current = ch["guild_id"], ch.get("parent_id")
    if a.action == "restore":
        if not a.to_category:
            sys.exit("restore needs --to-category (the from_category the archive step printed)")
        call("PATCH", f"{DISCORD}/channels/{a.channel}", h, {"parent_id": a.to_category})
        return {"medium": "discord", "action": "restore", "channel": a.channel, "from_category": current,
                "to_category": a.to_category}
    cats = [c for c in call("GET", f"{DISCORD}/guilds/{guild}/channels", h) if c["type"] == 4]
    target = next((c for c in cats if c["name"].lower() == a.category_name.lower()), None)
    created = False
    if not target:
        perms = call("GET", f"{DISCORD}/channels/{current}", h).get("permission_overwrites", []) if current else []
        target = call("POST", f"{DISCORD}/guilds/{guild}/channels", h,
                      {"name": a.category_name, "type": 4, "permission_overwrites": perms})
        created = True
    if current == target["id"]:
        return {"medium": "discord", "action": "archive", "channel": a.channel, "already_archived": True,
                "category": target["id"]}
    call("PATCH", f"{DISCORD}/channels/{a.channel}", h, {"parent_id": target["id"]})
    return {"medium": "discord", "action": "archive", "channel": a.channel, "from_category": current,
            "to_category": target["id"], "created_category": created}


def slack(a, E) -> dict:
    token = E.get(a.token_env or "SLACK_BOT_TOKEN") or sys.exit("no Slack token in the env")
    h = {"Authorization": f"Bearer {token}", "Content-Type": "application/json; charset=utf-8"}
    method = "conversations.archive" if a.action == "archive" else "conversations.unarchive"
    r = call("POST", f"https://slack.com/api/{method}", h, {"channel": a.channel})
    if not r.get("ok") and r.get("error") not in ("already_archived", "not_archived"):
        sys.exit(f"{method} failed: {r.get('error')}")
    return {"medium": "slack", "action": a.action, "channel": a.channel, "result": r.get("error") or "ok"}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["archive", "restore"])
    ap.add_argument("--medium", required=True, choices=["discord", "slack"])
    ap.add_argument("--channel", required=True)
    ap.add_argument("--category-name", default="Archived", help="Discord archive category (created if missing)")
    ap.add_argument("--to-category", help="Discord restore target: the from_category printed at archive time")
    ap.add_argument("--env-file")
    ap.add_argument("--token-env", help="env var holding the bot token (default DISCORD_BOT_TOKEN / SLACK_BOT_TOKEN)")
    a = ap.parse_args()
    E = env(a.env_file)
    print(json.dumps(discord(a, E) if a.medium == "discord" else slack(a, E)))


if __name__ == "__main__":
    main()
