#!/usr/bin/env python3
"""Rewrites index.json's hashes from the agent documents on disk.

Each `<id>.md` beside index.json (README.md aside) is listed. An agent
already in the index keeps its version and requires_cookie; a new one starts
at version 1.0.0 and must have its requires_cookie set by hand. Bump an
agent's version whenever its document changes.
"""
import hashlib
import json
import os
import sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(root, "index.json")
index = json.load(open(path)) if os.path.exists(path) else {"version": 1, "agents": []}
known = {agent["id"]: agent for agent in index.get("agents", [])}
agents = []
for name in sorted(os.listdir(root)):
    if not name.endswith(".md") or name == "README.md":
        continue
    agent_id = name[: -len(".md")]
    digest = hashlib.sha256(open(os.path.join(root, name), "rb").read()).hexdigest()
    entry = known.get(agent_id, {"id": agent_id, "version": "1.0.0", "requires_cookie": ""})
    if not entry["requires_cookie"]:
        print(f"{agent_id}: set requires_cookie in index.json", file=sys.stderr)
    agents.append(
        {
            "id": agent_id,
            "version": entry["version"],
            "requires_cookie": entry["requires_cookie"],
            "sha256": digest,
        }
    )
with open(path, "w") as out:
    json.dump({"version": 1, "agents": agents}, out, indent=2)
    out.write("\n")
