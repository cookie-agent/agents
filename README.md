# Official Cookie Agent agents

The agent documents every Cookie Agent daemon keeps up to date. A daemon
fetches `index.json` and each `<id>.md` from
`https://cookie-agent.github.io/agents/` at start and daily, checks each
file against its SHA-256 here and against its own configuration parser, and
keeps them in `~/.cookie-agent/official_agents/`. A document in
`~/.cookie-agent/agents/` with the same ID replaces the official one whole,
and no refresh touches it: copy an agent there to change it or to pin its
permissions. In that copy, `{{default_prompt}}` stands for the official
agent's prompt, so `{{default_prompt}}` followed by your own lines extends it.
An official agent never uses `{{default_prompt}}` itself.
To change only some keys, such as the models, and keep the rest in step
with the official agent, write `inherit: ../official_agents/<id>.md` and
those keys alone. `[agents] official = false` stops the refreshes.

| ID | Mode | Role |
|---|---|---|
| `primary` | primary | The user's assistant across their devices; the default agent |
| `explore` | subagent | Reads and searches, never writes |
| `worker` | subagent | Carries out a delegated task, implementation included |
| `approval` | internal | The approval reviewer of the `auto_approve` modes |
| `title` | internal | Session titles |
| `compaction` | internal | Checkpoint summaries; the daemon keeps a prompt of its own for when this one is missing |

## Templates

A file named `_<name>.md` is a template: a document others inherit, never an
agent itself. `index.json` lists templates under `templates` by `<name>`.

| Template | Role |
|---|---|
| `_acp` | What every ACP agent (Claude Code, Codex, ...) without a document of its own follows: cookie's rules for its harness's requests, and a prompt that tells it how to work inside cookie |

To change it for every ACP agent, write `~/.cookie-agent/agents/_acp.md`
with `inherit: ../official_agents/_acp.md` and the keys you change; for one
agent, `~/.cookie-agent/agents/<id>.md` with the same `inherit`.

## Presets

`index.json` also carries what onboarding offers:

- `acp_presets`: the ACP agents it can link (Claude Code and Codex), each
  with the command that launches it, what the machine needs, and how long
  the agent keeps its prompt cache (`cache_ttl`: an hour for Claude Code,
  30 minutes assumed for Codex), which lets cookie compact an idle
  session before it expires;
- `mcp_presets`: MCP servers that work without signing in (web search,
  library and repository documentation, and a browser), each with its
  `[mcp.servers.<name>]` table and whether it runs where the daemon does
  (`global`) or on a machine the user picks (`machine`).

Onboarding writes a preset's values into the user's `config.toml`; a later
change here does not rewrite them.

Refreshes apply as they arrive, permissions included: whoever can push here
decides what the official agents may do on every daemon that uses them.

## Changing an agent

1. Edit `<id>.md` (or `_<name>.md`).
2. Bump its `version` in `index.json`, and its `requires_cookie` when it uses
   something only newer daemons read.
3. Run `scripts/update-index.py` to rewrite the hashes.
4. Run `cookie agents check .`; CI runs it with the latest release.

See [Official agents](https://cookie-agent.github.io/doc/dev/extend/agents/#official-agents)
in the documentation.
