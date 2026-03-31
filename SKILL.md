---
name: self-evolving-agent
description: Build a phase-aware capability-evolution runtime for OpenClaw and coding agents. Use when the agent should classify work into task_light, task_full, agenda_review, or promotion_review mode; retrieve only the most relevant prior records; write canonical evidence into `.evolution/records`; maintain a capability map and learning agenda; and promote only validated, transferable strategies.
metadata:
  short-description: Phase-aware capability evolution runtime
---

# Self-Evolving Agent

`self-evolving-agent` is a control plane for capability evolution.

It keeps the original memory discipline from self-improving agents, but it stops treating "log the lesson" as the whole product. The runtime now does three things explicitly:

1. Classify the task into the right operating mode.
2. Retrieve only the records that mode requires.
3. Write new evidence into canonical records, then regenerate summaries and the manifest.

## When To Use This Skill

Use this skill when any of the following is true:

- A task is unfamiliar, high-consequence, recurring, or likely to expose a reusable weakness.
- A user correction, failed command, or near-miss suggests more than a one-off incident.
- You need an agenda review, transfer check, or promotion decision.
- You want the agent to retrieve prior learning selectively instead of dragging the whole history into every task.

## Core Principle

Do not run `task_full` by habit.

Use the smallest mode that is still safe:

- `task_light`
- `task_full`
- `agenda_review`
- `promotion_review`

The mode is the policy. The records are the memory. The generated ledgers are views, not the source of truth.

## Canonical Source Of Truth

The workspace stores mutable records under `.evolution/records/`:

- `records/learnings/`
- `records/errors/`
- `records/feature_requests/`
- `records/capabilities/`
- `records/training_units/`
- `records/evaluations/`
- `records/agenda/`

The runtime regenerates:

- `index/manifest.json`
- `LEARNINGS.md`
- `ERRORS.md`
- `FEATURE_REQUESTS.md`
- `CAPABILITIES.md`
- `TRAINING_UNITS.md`
- `EVALUATIONS.md`
- `LEARNING_AGENDA.md`

Treat the Markdown ledgers as generated dashboards for humans and compatibility. New evidence should be written through the runtime, not by hand-editing the ledgers.

## Modes

### `task_light`

Use when the task is familiar, low-consequence, and short-horizon.

- Retrieve only the top 1-3 relevant records.
- Name one likely risk and one verification check.
- Escalate only if execution reveals a real defect, user rescue, recurrence, or hidden consequence.
- Output artifact: a small retrieval pass plus a verification-first execution plan.

### `task_full`

Use when the task is unfamiliar, medium/high-consequence, medium/long-horizon, or recurrence is likely.

- Retrieve learnings, errors, capabilities, open training units, evaluations, and the active agenda.
- Identify the weakest likely capability.
- Choose an execution strategy and verification plan before acting.
- Output artifact: a pre-task diagnosis, then post-task evidence updates if anything reusable happened.

### `agenda_review`

Use only when agenda triggers fire:

- after five meaningful cycles
- when a structural gap appears
- when transfer fails
- before a new unfamiliar project

- Retrieve the active agenda, related capabilities, open training units, evaluations, and recent structural errors.
- Return the next 1-3 active focus capabilities with rationale and exit criteria.
- Output artifact: an agenda decision, not a generic reflection.

### `promotion_review`

Use only for transfer and promotion decisions.

- Retrieve evaluations, linked learnings, linked training units, and the relevant capability records.
- Decide the correct ladder state: `recorded -> understood -> practiced -> passed -> generalized -> promoted`.
- Promote only the smallest durable rule that has transfer evidence.
- Output artifact: evaluation state and promotion readiness.

## Runtime Commands

The control plane lives in `scripts/evolution_runtime.py`.

Primary commands:

- `classify-task --prompt "<task>"`
- `retrieve-context --prompt "<task>" --mode <mode>`
- `record-incident --source error|reflection ...`
- `review-agenda`
- `evaluate --subject <record-id>`
- `rebuild-index`

## Recommended Workflow

1. Read `system/coordinator.md`.
2. Run `classify-task`.
3. Run `retrieve-context` for the chosen mode.
4. Do the work with a mode-appropriate verification plan.
5. If meaningful evidence appears, write it with `record-incident`.
6. Regenerate summaries with `rebuild-index`.
7. Run `review-agenda` or `evaluate` only when their triggers apply.

## Migration Rules

- Treat `.evolution/legacy-self-improving/` as a read-only memory layer.
- Search legacy logs during retrieval if they are relevant.
- Do not bulk-convert old logs into new records on day one.
- Normalize legacy evidence only when it becomes active input for retrieval, agenda review, evaluation, or promotion.
