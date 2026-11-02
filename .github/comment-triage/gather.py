#!/usr/bin/env python3
"""Collect one giscus comment (REST API), its thread and the post it belongs to into ctx/.

Writes ctx/comment.md and ctx/post.md for Claude, ctx/meta.json for the issue
step, and sets the step output skip=true when there is nothing to triage.
"""
import glob
import json
import os
import subprocess
from pathlib import Path

REPO = os.environ["GITHUB_REPOSITORY"]
NUMBER = os.environ["DISCUSSION"]

out = Path("ctx")
out.mkdir(exist_ok=True)


def set_output(key, value):
    with open(os.environ["GITHUB_OUTPUT"], "a") as fh:
        fh.write(f"{key}={value}\n")


def api(path):
    """GitHub REST call through gh; prints GitHub's own error message on failure."""
    r = subprocess.run(["gh", "api", path], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"gh api {path} failed: {(r.stderr or r.stdout).strip()}")
    return json.loads(r.stdout)


def login(node):
    return ((node or {}).get("user") or {}).get("login") or "ghost"


d = api(f"repos/{REPO}/discussions/{NUMBER}")
# The REST list holds top-level comments and their replies; a reply has parent_id set.
comments = []
page = 1
while True:
    batch = api(f"repos/{REPO}/discussions/{NUMBER}/comments?per_page=100&page={page}")
    comments += batch
    if len(batch) < 100:
        break
    page += 1
by_id = {x["id"]: x for x in comments}
c = next((x for x in comments if x["node_id"] == os.environ["COMMENT_ID"]), None)
if not c or c.get("author_association") == "OWNER":
    print("Nothing to triage (comment not found in this discussion, or it's my own).")
    set_output("skip", "true")
    raise SystemExit(0)
parent = by_id.get(c.get("parent_id"))

title = d["title"].strip().strip("/")              # e.g. "posts/proxmox-backup-server"
slug = title.split("/")[-1]
post_url = f"https://mylemans.online/{title}/" if title.startswith("posts/") else f"https://mylemans.online/{title}"
matches = [p for p in glob.glob("site/_posts/*.md") if Path(p).stem.split("-", 3)[-1] == slug] if title.startswith("posts/") else []
post_path = matches[0] if matches else None
if post_path:
    (out / "post.md").write_text(Path(post_path).read_text(encoding="utf-8"), encoding="utf-8")

# The thread, oldest first, replies under their comment, with the new comment marked.
lines = [f"# Comment thread for {post_url}", ""]
for top in [x for x in comments if not x.get("parent_id")]:
    replies = [x for x in comments if x.get("parent_id") == top["id"]]
    for n, indent in [(top, "")] + [(r, "    ") for r in replies]:
        marker = "  <-- NEW COMMENT TO TRIAGE" if n["id"] == c["id"] else ""
        who = login(n) + (" (Marc, the author)" if n.get("author_association") == "OWNER" else "")
        lines.append(f"{indent}- {who}, {n['created_at']}{marker}:")
        for bl in (n.get("body") or "").splitlines():
            lines.append(f"{indent}    | {bl}")
lines += ["", "## The new comment on its own", f"Author: {login(c)}", "", c.get("body") or ""]
if parent:
    lines += ["", f"It is a reply to {login(parent)}:", parent.get("body") or ""]
(out / "comment.md").write_text("\n".join(lines), encoding="utf-8")

meta = {
    "comment_node": c["node_id"],
    "comment_url": c["html_url"],
    "comment_body": c.get("body") or "",
    "author": login(c),
    "discussion_id": d["node_id"],
    "discussion_url": d["html_url"],
    # giscus threads are one level deep: a reply to a reply goes under the top-level comment
    "reply_to": parent["node_id"] if parent else c["node_id"],
    "slug": slug,
    "post_url": post_url,
    "post_path": post_path.replace("site/", "", 1) if post_path else None,
}
(out / "meta.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
set_output("skip", "false")
print(f"Comment by {meta['author']} on {post_url} (post file: {meta['post_path']})")
