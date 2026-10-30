---
description: Summarizes a session's context into a checkpoint when it fills.
mode: internal
models:
  - ${parent_model}
limits:
  timeout_ms: 180000
---
Summarize the conversation above into a checkpoint that another agent will use to continue the work. The checkpoint replaces everything above except the system prompt and pinned context; any later messages stay verbatim after it.

When the conversation begins with an earlier checkpoint inside <summary> tags, write one updated checkpoint that merges it with everything after it; the new checkpoint replaces both, so carry forward whatever still matters from the earlier one. Newer information wins. Drop items that are resolved or no longer relevant, but keep user requirements that still apply.

Use exactly these Markdown sections, in this order. Write "None." under a section with nothing to record.

## Objective
The user's overall goal and the current task, in their terms.

## Requirements and Constraints
Explicit user instructions, preferences, and corrections, including what not to do. Quote short instructions verbatim.

## Decisions
Choices made and why, including approaches tried and rejected.

## Work State
- Completed: what is done and how it was verified.
- In progress: what was underway when the conversation was cut.
- Blocked: open problems and unanswered questions.

## Files and Code
Files read, created, or changed: what changed and why. Key functions, types, and signatures.

## Commands and Errors
Commands that matter and their outcomes; errors hit and how they were fixed.

## Next Step
The immediate next action, specific enough to act on without rereading anything.

## Important Context
Anything else needed to continue: environment facts, identifiers, URLs, numbers.

Rules:
- Be terse; prefer bullets to prose.
- Preserve exact paths, identifiers, commands, error messages, and numbers.
- Omit pinned context such as AGENTS.md and loaded skills; it stays available separately.
- Do not mention this checkpoint or the summarization.
- Do not continue the task, ask questions, or call tools. Return the checkpoint text only.
