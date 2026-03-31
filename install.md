# Install self-evolving-agent

## OpenClaw Installation

### Option 1: Install from ClawHub

ClawHub is the public skill registry for OpenClaw. Install the CLI, then install this skill by its registry slug:

```bash
npm i -g clawhub
# or
pnpm add -g clawhub

clawhub install RangeKing/self-evo-agent
```

OpenClaw will pick up the new workspace skill on the next session start.

Registry slug and local install directory use `self-evo-agent`.
The skill name and hook name remain `self-evolving-agent`.

If you already use `self-improving-agent`, keep it installed for the moment. Migrate the old `.learnings/` history first, then disable the old hook so you do not get duplicate reminders.

### Option 2: Let OpenClaw fetch it from GitHub

Ask your OpenClaw agent to install the repository directly into the shared skills directory:

```text
Install the OpenClaw skill from https://github.com/RangeKing/self-evolving-agent into ~/.openclaw/skills/self-evo-agent, inspect the scripts before enabling hooks, and then bootstrap ~/.openclaw/workspace/.evolution.
```

This is useful when you want OpenClaw itself to download and inspect the skill before use.

### Option 3: Copy into the skills directory

```bash
cp -r self-evolving-agent ~/.openclaw/skills/self-evo-agent
```

### Option 4: Clone directly

```bash
git clone https://github.com/RangeKing/self-evolving-agent.git ~/.openclaw/skills/self-evo-agent
```

## Workspace Setup

Create a persistent workspace memory area:

```bash
mkdir -p ~/.openclaw/workspace/.evolution
```

Seed the canonical records and generated ledgers with the bootstrap script:

```bash
~/.openclaw/skills/self-evo-agent/scripts/bootstrap-workspace.sh ~/.openclaw/workspace/.evolution
```

If you are migrating from `self-improving-agent`, import the legacy `.learnings/` directory at the same time:

```bash
~/.openclaw/skills/self-evo-agent/scripts/bootstrap-workspace.sh \
  ~/.openclaw/workspace/.evolution \
  --migrate-from ~/.openclaw/workspace/.learnings
```

This migration is lossless:

- it copies the original `.learnings/` files into `.evolution/legacy-self-improving/`
- it leaves the original files untouched
- it avoids rewriting old entries into the new schema before they are needed

After import, verify `.evolution/legacy-self-improving/IMPORT_INDEX.md`.

## Canonical Records

Canonical records are the mutable source of truth. The generated ledgers and `manifest.json` are rebuilt from them.

The mutable source of truth now lives under `.evolution/records/`:

```text
.evolution/
├── records/
│   ├── learnings/
│   ├── errors/
│   ├── feature_requests/
│   ├── capabilities/
│   ├── training_units/
│   ├── evaluations/
│   └── agenda/
├── index/
│   └── manifest.json
├── LEARNINGS.md
├── ERRORS.md
├── FEATURE_REQUESTS.md
├── CAPABILITIES.md
├── LEARNING_AGENDA.md
├── TRAINING_UNITS.md
└── EVALUATIONS.md
```

Use `scripts/evolution_runtime.py rebuild-index --workspace ~/.openclaw/workspace/.evolution` to regenerate the manifest and the human-readable ledgers from canonical records.

## Recommended Workspace Convention

```text
~/.openclaw/workspace/
├── AGENTS.md
├── SOUL.md
├── TOOLS.md
├── MEMORY.md
└── .evolution/
    ├── LEARNINGS.md
    ├── ERRORS.md
    ├── FEATURE_REQUESTS.md
    ├── CAPABILITIES.md
    ├── LEARNING_AGENDA.md
    ├── TRAINING_UNITS.md
    └── EVALUATIONS.md
```

## Optional Hook

Copy the OpenClaw hook:

```bash
cp -r ~/.openclaw/skills/self-evo-agent/hooks/openclaw ~/.openclaw/hooks/self-evolving-agent
```

Enable it:

```bash
openclaw hooks enable self-evolving-agent
```

If you previously enabled the old hook, disable it after verifying the import:

```bash
openclaw hooks disable self-improvement
```

## Optional Generic Agent Hooks

If your agent environment supports shell hooks, you can use:

- `scripts/activator.sh` for bootstrap reminders
- `scripts/error-detector.sh` for command-error reminders
- `scripts/run-evals.py` for repeatable local compliance checks
- `scripts/run-benchmark.py` for model-in-the-loop benchmark runs

## Promotion Targets

Only promote validated strategies into durable context:

- `AGENTS.md` for workflow rules
- `TOOLS.md` for tool-specific constraints
- `SOUL.md` for behavioral policies
- `MEMORY.md` for durable project or operator facts

## Minimum Operating Routine

Default to the smallest safe mode. Only pay the cost of `task_full`, `agenda_review`, or `promotion_review` when the task or evidence warrants it.

Before major tasks:

1. Run `scripts/evolution_runtime.py classify-task`.
2. Run `scripts/evolution_runtime.py retrieve-context` for the chosen mode.
3. Identify the most likely failure mode.
4. Choose an execution strategy that reduces that risk.

After major tasks:

1. Write incidents or reflections through `scripts/evolution_runtime.py record-incident`.
2. Rebuild summaries through `scripts/evolution_runtime.py rebuild-index`.
3. Refresh the learning agenda only if its trigger fired.
4. Run `evaluate` only if state advancement or promotion is in question.

For familiar, low-consequence, short tasks, stay in `task_light` mode:

1. Retrieve only the 1-3 most relevant prior items.
2. Name one likely risk and one verification check.
3. Do the work.
4. Log only if the lesson is unusually reusable.
5. Escalate into `task_full` only if a real defect, user rescue, recurrence, or transfer-worthy lesson appears.

## Validation

Run the repeatable local compliance suite:

```bash
python3 ~/.openclaw/skills/self-evo-agent/scripts/run-evals.py ~/.openclaw/skills/self-evo-agent
```

Run the model-in-the-loop benchmark:

```bash
python3 ~/.openclaw/skills/self-evo-agent/scripts/run-benchmark.py --skill-dir ~/.openclaw/skills/self-evo-agent
```

## Security Note

Whether you install from ClawHub or GitHub, inspect the skill files before enabling hooks or running scripts that modify your OpenClaw workspace.
