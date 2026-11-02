#!/usr/bin/env python3
"""Rewrites index.json's hashes from the agent documents on disk.

Each `<id>.md` beside index.json (README.md aside) is listed under `agents`,
and each template `_<name>.md` under `templates` as `<name>`. An entry
already in the index keeps its version and requires_cookie; a new one starts
at version 1.0.0 and must have its requires_cookie set by hand. Bump an
entry's version whenever its document changes. The presets (`acp_presets`,
`mcp_presets`) are edited by hand and kept as they are.
"""
import hashlib
import json
import os
import sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(root, "index.json")
index = json.load(open(path)) if os.path.exists(path) else {"version": 1, "agents": []}


def entries(kind, names):
    known = {entry["id"]: entry for entry in index.get(kind, [])}
    listed = []
    for entry_id, name in names:
        digest = hashlib.sha256(open(os.path.join(root, name), "rb").read()).hexdigest()
        entry = known.get(entry_id, {"id": entry_id, "version": "1.0.0", "requires_cookie": ""})
        if not entry["requires_cookie"]:
            print(f"{name}: set requires_cookie in index.json", file=sys.stderr)
        listed.append(
            {
                "id": entry_id,
                "version": entry["version"],
                "requires_cookie": entry["requires_cookie"],
                "sha256": digest,
            }
        )
    return listed


documents = sorted(
    name for name in os.listdir(root) if name.endswith(".md") and name != "README.md"
)
agents = [(name[: -len(".md")], name) for name in documents if not name.startswith("_")]
templates = [(name[1 : -len(".md")], name) for name in documents if name.startswith("_")]
updated = {"version": 1, "agents": entries("agents", agents)}
if templates:
    updated["templates"] = entries("templates", templates)
for kind in ("acp_presets", "mcp_presets"):
    if kind in index:
        updated[kind] = index[kind]
with open(path, "w") as out:
    json.dump(updated, out, indent=2)
    out.write("\n")
