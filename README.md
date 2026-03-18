# self-evolving-agent

Most self-improving agents only log mistakes.

`self-evolving-agent` learns more like a serious student: it diagnoses capability gaps, generates training units, evaluates progress, verifies transfer, and only then internalizes durable strategies.

This project is a full OpenClaw skill redesign built on top of the useful parts of classic self-improvement systems:

- incident logging
- correction capture
- recurring-pattern detection
- long-term promotion of high-value guidance

Those strengths remain, but only as the memory layer.

The new layer is capability evolution.

This upgraded version also adds a control layer: a proactive learning agenda that selects the next capabilities to train, instead of waiting for every lesson to emerge only after incidents.

This repository is intentionally structured as an OpenClaw-first skill project. It does not require `agents/openai.yaml` to be operational.

## Why This Is A New Paradigm

Traditional self-improving agents often stop at:

- "something failed"
- "log the fix"
- "write a rule"

That helps prevent repeated mistakes, but it does not answer the harder questions:

- What can the agent reliably do today?
- Which capability is actually weak?
- What should it practice next?
- Has it truly learned, or only recorded?
- Can the strategy transfer to a different task?

`self-evolving-agent` answers those questions with a structured loop:

1. Diagnose the task.
2. Map the required capabilities.
3. Detect the weakest link.
4. Prioritize active learning goals.
5. Generate targeted training.
6. Evaluate progress.
7. Test transfer.
8. Promote only validated strategies.

## What It Keeps From `self-improving-agent`

- Error logging
- Learning capture
- Feature request logging
- Recurring issue detection
- Review of past learnings before major work
- Promotion into durable workspace context
- Hook-friendly operation

## What It Adds

- Capability map with levels, evidence, failure modes, and upgrade criteria
- Learning diagnoser that distinguishes incidents from systemic weaknesses
- Learning agenda that keeps only 1-3 high-leverage capability goals active at a time
- Curriculum builder that creates concrete training units
- Evaluator that tracks `recorded -> understood -> practiced -> passed -> generalized -> promoted`
- Promotion gate that requires training success and transfer evidence
- Reflection routines that force self-explanation, counterexamples, and trigger signatures

## What Classic Self-Improvement Misses

Classic mistake-log systems are useful, but they usually remain limited in four ways:

1. They are reactive correction systems, not proactive learning systems.
2. They behave like error notebooks, not capability growth systems.
3. They accumulate rules, but often lack a real training loop.
4. They confuse persistence with mastery, even though recording is not the same as learning.

`self-evolving-agent` is designed around those gaps. It treats every meaningful incident as potential evidence about capability level, training need, evaluation state, transfer readiness, and agenda priority.

## Core Philosophy

Do not optimize only for "fewer repeated mistakes."

Optimize for agents that become:

- more independent
- more stable
- more transferable
- better on unfamiliar tasks

## Directory Structure

```text
self-evolving-agent/
├── SKILL.md
├── README.md
├── install.md
├── agents/
│   └── openai.yaml
├── system/
│   └── coordinator.md
├── modules/
│   ├── capability-map.md
│   ├── curriculum.md
│   ├── diagnose.md
│   ├── evaluator.md
│   ├── learning-agenda.md
│   ├── promotion.md
│   └── reflection.md
├── assets/
│   ├── CAPABILITIES.md
│   ├── ERRORS.md
│   ├── EVALUATIONS.md
│   ├── FEATURE_REQUESTS.md
│   ├── LEARNING_AGENDA.md
│   ├── LEARNINGS.md
│   └── TRAINING_UNITS.md
├── demos/
│   ├── demo-1-diagnosis.md
│   ├── demo-2-training-loop.md
│   ├── demo-3-promotion-and-transfer.md
│   └── demo-4-agenda-review.md
├── evals/
│   └── evals.json
├── hooks/
│   └── openclaw/
│       ├── HOOK.md
│       └── handler.ts
└── scripts/
    ├── activator.sh
    ├── bootstrap-workspace.sh
    ├── error-detector.sh
    └── run-evals.py
```

## Mental Model

Think of the system as four stacked layers:

1. Memory layer
   - Errors, learnings, and feature requests
2. Diagnosis layer
   - Which capability failed, and why
3. Training layer
   - What deliberate practice should happen next
4. Policy layer
   - What has earned promotion into durable behavior

Above those layers sits a control loop:

- Learning agenda
  - Which capabilities are the top priorities right now
  - What evidence would retire or advance them

## Best Fit

Use this skill when you want an agent that can:

- improve across sessions
- convert repeated failures into curriculum
- measure whether learning actually happened
- grow from incident handling into capability development

## Quick Start

1. Install the skill in your OpenClaw skills directory.
2. Run `scripts/bootstrap-workspace.sh` to seed a directly usable `.evolution` workspace.
3. Enable the optional hook if you want bootstrap reminders.
4. Before difficult tasks, review the active learning agenda and capability risks.
5. After meaningful tasks, update memory, diagnosis, training, evaluation, and agenda artifacts.
6. Run `scripts/run-evals.py` for a repeatable local compliance check.

Setup details are in [install.md](./install.md).
