# Official Cookie Agent agents

The agent documents every Cookie Agent daemon keeps up to date. A daemon
fetches `index.json` and each `<id>.md` from
`https://cookie-agent.github.io/agents/` at start and daily, checks each
file against its SHA-256 here and against its own configuration parser, and
keeps them in `~/.cookie-agent/official_agents/`. A document in
`~/.cookie-agent/agents/` with the same ID replaces the official one whole,
and no refresh touches it: copy an agent there to change it or to pin its
permissions. `[agents] official = false` stops the refreshes.

| ID | Mode | Role |
|---|---|---|
| `primary` | primary | The user's assistant across their devices; the default agent |
| `coder` | all | The coding agent, for a repository project's defaults |
| `explore` | subagent | Reads and searches, never writes |
| `worker` | subagent | Carries out a delegated task, implementation included |
| `approval` | internal | The approval reviewer of the `auto_approve` modes |
| `title` | internal | Session titles |
| `compaction` | internal | Checkpoint summaries; its body stays `{{default_prompt}}`, the prompt the daemon also keeps as a fallback |

Refreshes apply as they arrive, permissions included: whoever can push here
decides what the official agents may do on every daemon that uses them.

## Changing an agent

1. Edit `<id>.md`.
2. Bump its `version` in `index.json`, and its `requires_cookie` when it uses
   something only newer daemons read.
3. Run `scripts/update-index.py` to rewrite the hashes.
4. Run `cookie agents check .`; CI runs it with the latest release.

See [Official agents](https://cookie-agent.github.io/doc/dev/extend/agents/#official-agents)
in the documentation.
