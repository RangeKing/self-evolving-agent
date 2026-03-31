# Self-Evolving Coordinator

This file defines the phase-aware operating system for the skill.

## Mission

Transform passive correction into selective, mode-aware capability evolution.

The coordinator should behave like a small control plane:

- classify the work
- load only the necessary context
- execute with a mode-appropriate verification plan
- write evidence into canonical records
- regenerate summaries and the manifest

## First Principles

1. Logging is evidence collection, not mastery.
2. `task_full` is expensive; do not run it by default.
3. Generated ledgers are views. Canonical records are the mutable source of truth.
4. Promotion without transfer evidence creates brittle policy.
5. Agenda review and promotion review are special modes, not ambient behaviors.

## Canonical Workspace

Mutable records live in `.evolution/records/`:

- `learnings/`
- `errors/`
- `feature_requests/`
- `capabilities/`
- `training_units/`
- `evaluations/`
- `agenda/`

Generated outputs live at the workspace root and under `index/`:

- `index/manifest.json`
- `LEARNINGS.md`
- `ERRORS.md`
- `FEATURE_REQUESTS.md`
- `CAPABILITIES.md`
- `TRAINING_UNITS.md`
- `EVALUATIONS.md`
- `LEARNING_AGENDA.md`

## Runtime Commands

Use `scripts/evolution_runtime.py` as the control plane:

- `classify-task`
- `retrieve-context`
- `record-incident`
- `review-agenda`
- `evaluate`
- `rebuild-index`

## Mode Contract

### `task_light`

Entry trigger:
- familiar task
- low consequence
- short horizon
- no active structural weakness is central

Required retrieval:
- up to 3 records from learnings, errors, and capabilities

Required artifact:
- one risk
- one verification check
- a minimal execution strategy

Escalation rule:
- escalate to `task_full` if execution reveals a real defect, recurrence, user rescue, or hidden consequence

Exit condition:
- task completes without reusable new evidence, or only a small reusable lesson needs to be recorded

### `task_full`

Entry trigger:
- unfamiliar or mixed task
- medium/high consequence
- medium/long horizon
- recurrence or structural uncertainty

Required retrieval:
- active agenda
- relevant learnings and errors
- relevant capabilities
- linked training units and evaluations when present

Required artifact:
- pre-task diagnosis
- capability risk assessment
- verification-first execution strategy

Escalation rule:
- if the task turns into agenda reprioritization, switch to `agenda_review`
- if the task becomes a transfer or promotion judgment, switch to `promotion_review`

Exit condition:
- the task is complete and any reusable evidence has been written as canonical records

### `agenda_review`

Entry trigger:
- after five meaningful cycles
- structural gap detected
- failed transfer
- before a new unfamiliar project

Required retrieval:
- active agenda
- weak capabilities
- open training units
- evaluations and recent structural errors

Required artifact:
- next 1-3 active focus capabilities
- rationale
- exit criteria

Escalation rule:
- do not drift into general task execution; return to `task_light` or `task_full` after the agenda decision is made

Exit condition:
- a bounded agenda decision exists with a small active focus set

### `promotion_review`

Entry trigger:
- explicit evaluation request
- transfer evidence appears
- promotion is under consideration

Required retrieval:
- evaluation records
- linked learnings
- linked training units
- relevant capability records

Required artifact:
- ladder state
- promotion readiness
- smallest durable rule, if promotion is justified

Escalation rule:
- if transfer evidence is weak, fall back to evaluation only and keep the rule unpromoted

Exit condition:
- promotion decision is explicit and scoped

## Retrieval Policy

Retrieval must be selective.

Ranking should prefer:

1. trigger-signature overlap
2. capability match
3. active or open state
4. recency
5. overlap with active agenda links

Do not scan entire ledgers manually when the runtime can rank records from the manifest.

## Evidence Policy

When meaningful evidence appears:

1. write it through `record-incident`
2. regenerate the manifest and ledgers through `rebuild-index`
3. update agenda or evaluation only if the trigger is satisfied

Minor incidents can remain local. Reusable incidents should become canonical records.

## Migration Layer

If `.evolution/legacy-self-improving/` exists:

- treat it as read-only
- consult it during retrieval when relevant
- do not bulk-convert it into canonical records
- normalize only the specific legacy items that become active evidence
