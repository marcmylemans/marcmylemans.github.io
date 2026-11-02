#!/usr/bin/env python3
"""Collect one giscus comment, its thread and the post it belongs to into ctx/.

Writes ctx/comment.md and ctx/post.md for Claude, ctx/meta.json for the issue
step, and sets the step output skip=true when there is nothing to triage.
"""
import glob
import json
import os
import subprocess
from pathlib import Path

QUERY = """
query($id: ID!) {
  node(id: $id) {
    ... on DiscussionComment {
      id url body createdAt authorAssociation isMinimized
      author { login }
      replyTo { id url body author { login } }
      discussion {
        id number title url category { name }
        comments(first: 30) {
          nodes {
            id body createdAt author { login }
            replies(first: 20) { nodes { id body createdAt author { login } } }
          }
        }
      }
    }
  }
}
"""

out = Path("ctx")
out.mkdir(exist_ok=True)


def set_output(key, value):
    with open(os.environ["GITHUB_OUTPUT"], "a") as fh:
        fh.write(f"{key}={value}\n")


def login(node):
    return ((node or {}).get("author") or {}).get("login") or "ghost"


raw = subprocess.run(
    ["gh", "api", "graphql", "-f", f"query={QUERY}", "-F", f"id={os.environ['COMMENT_ID']}"],
    check=True, capture_output=True, text=True).stdout
c = json.loads(raw)["data"]["node"]
if not c or c.get("isMinimized") or c.get("authorAssociation") == "OWNER":
    print("Nothing to triage (missing, hidden, or my own comment).")
    set_output("skip", "true")
    raise SystemExit(0)

d = c["discussion"]
title = d["title"].strip().strip("/")              # e.g. "posts/proxmox-backup-server"
slug = title.split("/")[-1]
post_url = f"https://mylemans.online/{title}/" if title.startswith("posts/") else f"https://mylemans.online/{title}"
matches = [p for p in glob.glob("site/_posts/*.md") if Path(p).stem.split("-", 3)[-1] == slug] if title.startswith("posts/") else []
post_path = matches[0] if matches else None
if post_path:
    (out / "post.md").write_text(Path(post_path).read_text(encoding="utf-8"), encoding="utf-8")

# The thread, oldest first, with the new comment marked.
lines = [f"# Comment thread for {post_url}", ""]
for top in d["comments"]["nodes"]:
    for n, indent in [(top, "")] + [(r, "    ") for r in top["replies"]["nodes"]]:
        marker = "  <-- NEW COMMENT TO TRIAGE" if n["id"] == c["id"] else ""
        who = login(n) + (" (Marc, the author)" if login(n) == "marcmylemans" else "")
        lines.append(f"{indent}- {who}, {n['createdAt']}{marker}:")
        for bl in (n["body"] or "").splitlines():
            lines.append(f"{indent}    | {bl}")
lines += ["", "## The new comment on its own", f"Author: {login(c)}", "", c["body"] or ""]
if c.get("replyTo"):
    lines += ["", f"It is a reply to {login(c['replyTo'])}:", c["replyTo"]["body"] or ""]
(out / "comment.md").write_text("\n".join(lines), encoding="utf-8")

meta = {
    "comment_node": c["id"],
    "comment_url": c["url"],
    "comment_body": c["body"] or "",
    "author": login(c),
    "discussion_id": d["id"],
    "discussion_url": d["url"],
    # giscus threads are one level deep: a reply to a reply goes under the top-level comment
    "reply_to": (c.get("replyTo") or {}).get("id") or c["id"],
    "slug": slug,
    "post_url": post_url,
    "post_path": post_path.replace("site/", "", 1) if post_path else None,
}
(out / "meta.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
set_output("skip", "false")
print(f"Comment by {meta['author']} on {post_url} (post file: {meta['post_path']})")
