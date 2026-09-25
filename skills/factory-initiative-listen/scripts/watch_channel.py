"""One stdout line per new human message in a Slack channel, top-level or in a thread.

Written to be the `command` of a Monitor: the listener is woken the moment someone posts,
instead of waking on a timer and usually finding nothing. Every line printed becomes one
notification, so the filtering that matters (bots out, already-seen out) happens here rather
than in the agent's context.

Two things are load-bearing and easy to get wrong:

* The high-water mark is a Slack `ts`, never a clock reading, and `oldest` is formatted to
  EXACTLY six decimals. Given more, Slack returns `ok: true` with zero messages — a silent
  "nothing new" that looks identical to a quiet channel.
* The mark file is the resume point across restarts, so exactly one watcher may own it. Two
  watchers on one mark file race, and each swallows messages the other should have reported.

A failed request is swallowed rather than raised: one rate-limit or blip must not end a watch
that is supposed to stay up for hours.

Usage:
    python3 watch_channel.py --channel C08PB525VSN --mark ~/.factory/initiative-<slug>.mark \
        [--label '#channel-name'] [--env-file /path/to/.env] [--token-env SLACK_BOT_TOKEN] \
        [--poll 30]
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request


def resolve_token(token_env, env_file):
    token = os.environ.get(token_env)
    if token:
        return token.strip().strip('"')
    if env_file:
        # Grep the single key rather than sourcing the file: these .envs routinely hold live
        # database and payment credentials that must not enter the process or the transcript.
        match = re.search(r"^{}=(.+)$".format(re.escape(token_env)),
                          open(os.path.expanduser(env_file)).read(), re.M)
        if match:
            return match.group(1).strip().strip('"')
    sys.exit("watch_channel: no {} in the environment or --env-file".format(token_env))


class Watcher:
    def __init__(self, token, channel, label):
        self.token = token
        self.channel = channel
        self.label = label
        self.names = {}

    def api(self, method, **params):
        url = "https://slack.com/api/{}?{}".format(method, urllib.parse.urlencode(params))
        request = urllib.request.Request(url, headers={"Authorization": "Bearer " + self.token})
        try:
            with urllib.request.urlopen(request, timeout=25) as response:
                return json.loads(response.read())
        except Exception:
            return {}

    def who(self, user_id):
        if user_id not in self.names:
            user = self.api("users.info", user=user_id or "").get("user") or {}
            self.names[user_id] = (user.get("real_name") or user.get("name")
                                   or (user_id or "someone"))
        return self.names[user_id]

    def line(self, message):
        text = " ".join((message.get("text") or "").split())[:400] or "(no text)"
        files = [f.get("name") or f.get("filetype") or "file" for f in message.get("files") or []]
        if files:
            text += "  [attached: " + ", ".join(files) + "]"
        in_thread = (message.get("thread_ts") or message["ts"]) != message["ts"]
        return "{} {}{}: {}".format(self.label, self.who(message.get("user")),
                                    " (in thread)" if in_thread else "", text)


def human(message):
    return not (message.get("bot_id") or message.get("subtype") == "bot_message")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--channel", required=True)
    parser.add_argument("--mark", required=True)
    parser.add_argument("--label", default="")
    parser.add_argument("--env-file", default="")
    parser.add_argument("--token-env", default="SLACK_BOT_TOKEN")
    parser.add_argument("--poll", type=int, default=30)
    args = parser.parse_args()

    mark_file = os.path.expanduser(args.mark)
    os.makedirs(os.path.dirname(mark_file) or ".", exist_ok=True)
    watcher = Watcher(resolve_token(args.token_env, args.env_file),
                      args.channel, args.label or args.channel)

    if os.path.exists(mark_file):
        mark = float(open(mark_file).read().strip() or 0)
    else:
        # A first run starts at NOW, not at the beginning of history: the point is to react to
        # what happens next, and replaying a year of backlog as notifications is its own outage.
        latest = watcher.api("conversations.history", channel=args.channel, limit=1)
        mark = float((latest.get("messages") or [{}])[0].get("ts") or time.time())

    while True:
        history = watcher.api("conversations.history", channel=args.channel,
                              oldest="{:.6f}".format(mark), limit=100)
        highest = mark
        for parent in reversed(history.get("messages") or []):
            batch = [parent]
            # A reply can land under an old parent long after it scrolled past; without this the
            # thread is invisible to a watcher that only reads top-level messages.
            if float(parent.get("latest_reply") or 0) > mark:
                batch += (watcher.api("conversations.replies", channel=args.channel,
                                      ts=parent["ts"]).get("messages") or [])[1:]
            for message in batch:
                ts = float(message.get("ts") or 0)
                if ts <= mark or not human(message):
                    continue
                highest = max(highest, ts)
                print(watcher.line(message), flush=True)
        if highest > mark:
            mark = highest
            # Written only after the lines are flushed, so a crash re-reports rather than skips.
            with open(mark_file, "w") as out:
                out.write("{:.6f}".format(mark))
        time.sleep(args.poll)


if __name__ == "__main__":
    sys.exit(main())
