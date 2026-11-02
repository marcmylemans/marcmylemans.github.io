#!/usr/bin/env python3
"""Turn Claude's triage JSON into an issue in marcmylemans/mylemans-online.

Plain code on purpose: Claude never gets write access. Comments that need
nothing ("other") don't create an issue.
"""
import json
import os
import subprocess
from pathlib import Path

SITE_REPO = "marcmylemans/mylemans-online"
LABELS = {
    "correction": ("reader-correction", "d93f0b", "A reader says a post is wrong or outdated"),
    "question": ("reader-question", "1d76db", "A reader asked a question on a post"),
    "spam": ("reader-spam", "6a737d", "Comment that looks like spam"),
}

raw = os.environ.get("RESULT") or ""
if not raw:
    raise SystemExit("No structured output from Claude; see the triage step log.")
r = json.loads(raw)
meta = json.loads(Path("ctx/meta.json").read_text(encoding="utf-8"))
kind = r["kind"]
print(f"kind={kind} confidence={r['confidence']}: {r['summary']}")
if kind not in LABELS:
    print("Nothing for Marc to do; no issue.")
    raise SystemExit(0)


def gh(*args, check=True):
    return subprocess.run(["gh", *args], check=check, capture_output=True, text=True).stdout


def safe(text):
    """Reader and model text goes into the issue as plain text: no @mentions
    (they would notify people) and no HTML comments (they would break the
    markers the reply workflow reads)."""
    return (text or "").replace("@", "@​").replace("<!--", "&lt;!--").replace("-->", "--&gt;")


# Don't open a second issue if this comment was already triaged.
existing = gh("issue", "list", "-R", SITE_REPO, "--state", "all", "--search",
              f"{meta['comment_node']} in:body", "--json", "number", "-q", ".[].number").strip()
if existing:
    print(f"Already triaged in issue #{existing.splitlines()[0]}.")
    raise SystemExit(0)

label, color, desc = LABELS[kind]
gh("label", "create", label, "-R", SITE_REPO, "--color", color, "--description", desc, "--force", check=False)

quoted = "\n".join("> " + l for l in safe(meta["comment_body"]).splitlines()) or "> (empty)"
post = f"[{meta['slug']}]({meta['post_url']})"
if meta.get("post_path"):
    post += f" (`{meta['post_path']}`)"
parts = [
    f"**Reader comment** by `{meta['author']}` on {post} · [view the comment]({meta['comment_url']})",
    "",
    quoted,
    "",
    f"### Assessment (confidence: {r['confidence']})",
    safe(r["summary"]),
    "",
    safe(r["assessment"]),
]
if kind == "correction" and r.get("proposed_change"):
    parts += ["", "### Proposed change to the post", safe(r["proposed_change"])]
if kind == "spam":
    parts += ["", f"Looks like spam. Hide or delete it in [the discussion]({meta['discussion_url']}), then close this issue."]
else:
    parts += [
        "",
        "### Draft reply",
        "Edit the text between the markers if you like, then comment `/post-reply` on this issue "
        "to post it under the reader's comment, as you. Close the issue to skip replying.",
        "",
        "<!-- reply:start -->",
        safe(r["draft_reply"]),
        "<!-- reply:end -->",
    ]
if kind == "correction":
    parts += ["", "To have Claude fix the post: add the `claude` label. It opens a PR for you to review; nothing is merged without you."]
parts += ["", "<!-- giscus-meta " + json.dumps({k: meta[k] for k in ("discussion_id", "reply_to", "comment_node", "comment_url")}) + " -->"]

title = f"[{label}] {meta['slug']}: {r['summary']}"[:120]
url = gh("issue", "create", "-R", SITE_REPO, "--title", title, "--label", label, "--body", "\n".join(parts)).strip()
print(f"Opened {url}")
