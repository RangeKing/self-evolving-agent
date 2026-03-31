<img width="1424" height="425" alt="Image" src="https://github.com/user-attachments/assets/7b84ae6a-db3e-4abe-a551-02e04f97344f" />

# self-evolving-agent
[![English](https://img.shields.io/badge/Language-English-0A7CFF?style=flat-square)](./README.md)
[![简体中文](https://img.shields.io/badge/%E8%AF%AD%E8%A8%80-%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87-16A34A?style=flat-square)](./README.zh-CN.md)

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-111827?style=flat-square)](./SKILL.md)
[![CI](https://img.shields.io/github/actions/workflow/status/RangeKing/self-evolving-agent/ci.yml?branch=main&style=flat-square&label=CI)](https://github.com/RangeKing/self-evolving-agent/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/RangeKing/self-evolving-agent?style=flat-square)](./LICENSE)
[![Stars](https://img.shields.io/github/stars/RangeKing/self-evolving-agent?style=flat-square)](https://github.com/RangeKing/self-evolving-agent/stargazers)
[![Model-in-the-Loop Benchmark](https://img.shields.io/badge/Benchmark-Model--in--the--Loop-7C3AED?style=flat-square)](./benchmarks/suite.json)
[![Goal-Driven Learning](https://img.shields.io/badge/Agent-Goal--Driven%20Learning-0F766E?style=flat-square)](./system/coordinator.md)

🧠 self-improving-agent only log mistakes.

`self-evolving-agent` is an OpenClaw-first, phase-aware capability-evolution runtime. It classifies work into `task_light`, `task_full`, `agenda_review`, or `promotion_review` mode; retrieves only the most relevant prior records; writes evidence into canonical records; and regenerates human-facing ledgers plus `manifest.json`.

It preserves the best parts of [`self-improving-agent`](https://github.com/peterskoett/self-improving-agent), but upgrades the paradigm from:

- incident logging -> capability evolution
- passive memory -> active learning agenda
- correction archive -> curriculum + evaluation + promotion gate

## ✨ Why It Exists

Traditional self-improving agents often stop at:

- "something failed"
- "log the fix"
- "write a rule"

That helps reduce repeated mistakes, but it does not answer the harder questions:

- What can the agent reliably do today?
- Which capability is actually weak?
- What should it practice next?
- Has it truly learned, or only recorded?
- Can the strategy transfer to a different task?

`self-evolving-agent` is built to answer those questions explicitly.

## 📊 self-evolving-agent vs self-improving-agent

| Dimension | `self-improving-agent` | `self-evolving-agent` |
| --- | --- | --- |
| Primary mode | Reactive correction | Goal-driven capability evolution |
| Core unit | Incident, error, note | Capability, training unit, evaluation state |
| Memory model | Learnings and recurring issues | Learnings + capability map + learning agenda |
| Before-task behavior | Review past notes if relevant | Review notes, capability risks, and active training priorities |
| After-task behavior | Log errors and lessons | Diagnose weakest capability, update map, revise agenda, create training if needed |
| Recurrence handling | Detect recurring patterns | Convert recurrence into curriculum with pass criteria |
| Learning states | Mostly implicit | `recorded -> understood -> practiced -> passed -> generalized -> promoted` |
| Promotion rule | Promote useful rules | Promote only validated, transferable strategies |
| Transfer awareness | Limited | Explicit transfer check before promotion |
| What it optimizes for | Fewer repeated mistakes | More independence, stability, transfer, and unfamiliar-task competence |

## 🚀 What Makes This Different

- 🧭 **Learning agenda:** keeps only 1-3 high-leverage capabilities active at a time
- 🗺️ **Capability map:** tracks level, evidence, limits, failure modes, and upgrade conditions
- 🧠 **Phase-aware control plane:** routes tasks into the smallest safe mode instead of assuming `task_full` every time
- 🗂️ **Canonical records:** stores mutable state under `records/` and generates human-readable ledgers from those records
- 🔬 **Diagnosis layer:** turns incidents into capability-level root-cause analysis
- 🏋️ **Curriculum layer:** generates drills, pass criteria, and transfer scenarios
- ✅ **Evaluation ladder:** separates writing something down from actually learning it
- 🔒 **Promotion gate:** prevents brittle one-off rules from polluting long-term behavior
- 🤝 **Memory retention:** still preserves classic logging for errors, learnings, and feature requests

## 🧱 Architecture

```mermaid
flowchart TD
    A["Task Starts"] --> B["classify-task"]
    B --> C["Mode: task_light | task_full | agenda_review | promotion_review"]
    C --> D["retrieve-context"]
    D --> E["Execute with verification"]
    E --> F["record-incident"]
    F --> G["rebuild-index"]
    G --> H["Generated ledgers + manifest.json"]
    H --> I["review-agenda / evaluate when triggered"]
```

The runtime entrypoint is [`scripts/evolution_runtime.py`](./scripts/evolution_runtime.py). It treats `assets/records/` and workspace `records/` directories as the mutable source of truth and regenerates summaries plus `index/manifest.json`.

## 🔁 Phase-Aware Loop

For every meaningful cycle, the skill follows this control plane:

1. Classify the task with `scripts/evolution_runtime.py classify-task`
2. Choose the smallest safe mode
3. Retrieve only that mode's records with `retrieve-context`
4. Execute with a mode-appropriate verification plan
5. Write reusable evidence through `record-incident`
6. Regenerate `records/` views and `manifest.json` through `rebuild-index`

Outside the task loop, it runs `review-agenda` and `evaluate` only when their triggers fire.

## 🧩 What It Keeps From self-improving-agent

- Error logging
- Learning capture
- Feature request logging
- Recurring pattern detection
- Review of past learnings before major work
- Promotion into durable workspace context
- Hook-friendly operation

Those strengths remain, but only as the **memory layer**, not the whole system.

## 🔄 Migration From self-improving-agent

The most common conflict is not data loss. It is double activation.

If a user already has `self-improving-agent`, the safe migration path is:

1. Install `self-evolving-agent` without deleting the old skill.
2. Bootstrap `.evolution/` and import the old `.learnings/` directory.
3. Keep the imported logs in `.evolution/legacy-self-improving/` as read-only history.
4. Disable the old `self-improvement` hook after verifying the import.
5. Gradually normalize only the legacy items that become active evidence for diagnosis, agenda review, evaluation, or promotion.

This keeps prior experience intact without forcing a lossy one-shot conversion into the new schema.

Example:

```bash
~/.openclaw/skills/self-evo-agent/scripts/bootstrap-workspace.sh \
  ~/.openclaw/workspace/.evolution \
  --migrate-from ~/.openclaw/workspace/.learnings
openclaw hooks disable self-improvement
openclaw hooks enable self-evolving-agent
```

## 🎯 Best Fit

Use this skill when you want an agent that should:

- improve across sessions
- become safer on unfamiliar work
- convert repeated failures into deliberate practice
- distinguish recording from mastery
- prove transfer before promotion

## ⚖️ Modes

The `task_full` capability-evolution pipeline is intentionally not the default for every tiny mistake.

Use `task_light` when the task is familiar, low-consequence, and short-horizon. In that mode, retrieve only the top few relevant records, state one risk and one verification check, and avoid spawning agenda or promotion work.

Escalate into `task_full` when the task is mixed or unfamiliar, consequence matters, an active agenda item is involved, a failure pattern repeats, the user had to rescue the task, transfer failed, or the lesson may deserve training or evaluation.

Use `agenda_review` only for agenda triggers such as five meaningful cycles, structural gaps, failed transfer, or an upcoming unfamiliar project.

Use `promotion_review` only for transfer and promotion decisions.

## 📁 Repository Layout

```text
self-evolving-agent/
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── install.md
├── agents/
│   └── openai.yaml
├── benchmarks/
│   ├── suite.json
│   └── schemas/
│       └── judge-output.schema.json
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
│   ├── records/
│   │   ├── agenda/
│   │   └── capabilities/
│   ├── CAPABILITIES.md
│   ├── ERRORS.md
│   ├── EVALUATIONS.md
│   ├── FEATURE_REQUESTS.md
│   ├── LEARNING_AGENDA.md
│   ├── LEARNINGS.md
│   └── TRAINING_UNITS.md
├── evals/
│   └── evals.json
├── demos/
│   ├── demo-1-diagnosis.md
│   ├── demo-2-training-loop.md
│   ├── demo-3-promotion-and-transfer.md
│   ├── demo-4-agenda-review.md
│   └── demo-5-pre-task-risk-diagnosis.md
├── hooks/
│   └── openclaw/
│       ├── HOOK.md
│       └── handler.ts
└── scripts/
    ├── activator.sh
    ├── bootstrap-workspace.sh
    ├── evolution_runtime.py
    ├── error-detector.sh
    ├── run-benchmark.py
    └── run-evals.py
```

## ⚡ Quick Start

1. Install the skill into your OpenClaw skills directory.
2. Bootstrap a persistent `.evolution` workspace.
3. Classify work through the runtime and retrieve only the required records.
4. Let the runtime regenerate ledgers and `manifest.json` after canonical record updates.
5. Run the benchmark suite to see how the skill performs in model-in-the-loop conditions.

```bash
cp -r self-evolving-agent ~/.openclaw/skills/self-evo-agent
~/.openclaw/skills/self-evo-agent/scripts/bootstrap-workspace.sh ~/.openclaw/workspace/.evolution
python3 ~/.openclaw/skills/self-evo-agent/scripts/evolution_runtime.py classify-task \
  --workspace ~/.openclaw/workspace/.evolution \
  --prompt "I need to modify a production deployment workflow I have never touched before."
python3 ~/.openclaw/skills/self-evo-agent/scripts/run-evals.py ~/.openclaw/skills/self-evo-agent
python3 ~/.openclaw/skills/self-evo-agent/scripts/run-benchmark.py --skill-dir ~/.openclaw/skills/self-evo-agent
```

More setup details are in [install.md](./install.md).

## 📦 Installation Options

### Option A: Install from ClawHub

Use this when you want the simplest registry-based install into your current OpenClaw workspace.

```bash
npm i -g clawhub
# or
pnpm add -g clawhub

clawhub install RangeKing/self-evo-agent
```

Then start a new OpenClaw session so the skill is loaded from your workspace `skills/` folder.
The registry slug and local directory are `self-evo-agent`; the skill and hook name stay `self-evolving-agent`.
If you are migrating from `self-improving-agent`, import `.learnings/` before you disable the old hook.

### Option B: Let OpenClaw install it from GitHub

If you prefer to have your agent fetch the GitHub repository directly, you can tell OpenClaw something like:

```text
Install the OpenClaw skill from https://github.com/RangeKing/self-evolving-agent into ~/.openclaw/skills/self-evo-agent, inspect the scripts before enabling hooks, and then bootstrap ~/.openclaw/workspace/.evolution.
```

This works well when you want the skill installed as a shared managed skill under `~/.openclaw/skills`.

### Option C: Manual Git clone

```bash
git clone https://github.com/RangeKing/self-evolving-agent.git ~/.openclaw/skills/self-evo-agent
~/.openclaw/skills/self-evo-agent/scripts/bootstrap-workspace.sh ~/.openclaw/workspace/.evolution
```

If you already have `~/.openclaw/workspace/.learnings`, use:

```bash
~/.openclaw/skills/self-evo-agent/scripts/bootstrap-workspace.sh \
  ~/.openclaw/workspace/.evolution \
  --migrate-from ~/.openclaw/workspace/.learnings
```

### Safety Note

ClawHub is a public registry and skills are effectively trusted local code. Review the repository or installed files before enabling hooks or running benchmark scripts.

## 🤝 Project Health

- Contribution guide: [CONTRIBUTING.md](./CONTRIBUTING.md)
- Changelog: [CHANGELOG.md](./CHANGELOG.md)
- Security policy: [SECURITY.md](./SECURITY.md)
- License: [MIT](./LICENSE)

## 🧪 Benchmarking

This repository includes two evaluation modes:

- `scripts/run-evals.py`
  - Structural compliance checks for files, modules, and benchmark assets
- `scripts/run-benchmark.py`
  - Real model-in-the-loop execution using `codex exec`
  - Captures candidate prompt, raw events, final output, judge output, and report

Example smoke run:

```bash
python3 scripts/run-benchmark.py \
  --skill-dir . \
  --candidate-model gpt-5.4-mini \
  --judge-model gpt-5.4-mini \
  --max-scenarios 1 \
  --timeout-seconds 90
```

## 🧭 Use Cases

- Upgrading a self-correcting agent into a self-training agent
- Running postmortems that produce training, not just notes
- Building skill memory systems that do not confuse logging with mastery
- Evaluating whether an agent can transfer strategies across task families
- Designing agent curricula for research, coding, verification, or operations workflows

## 🛣️ Roadmap

- [x] Memory, diagnosis, curriculum, evaluator, reflection, promotion modules
- [x] Capability bootstrap map and proactive learning agenda
- [x] Model-in-the-loop benchmark harness
- [ ] More benchmark scenarios for coding, research, and long-horizon execution
- [ ] Optional benchmark trend summaries across repeated runs
- [ ] Example workspace packs for different agent domains
