# Install self-evolving-agent

## OpenClaw Installation

### Option 1: Copy into the skills directory

```bash
cp -r self-evolving-agent ~/.openclaw/skills/
```

### Option 2: Clone directly

```bash
git clone <your-repo-url> ~/.openclaw/skills/self-evolving-agent
```

## Workspace Setup

Create a persistent workspace memory area:

```bash
mkdir -p ~/.openclaw/workspace/.evolution
```

Seed the workspace ledgers with the bootstrap script:

```bash
~/.openclaw/skills/self-evolving-agent/scripts/bootstrap-workspace.sh ~/.openclaw/workspace/.evolution
```

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
cp -r ~/.openclaw/skills/self-evolving-agent/hooks/openclaw ~/.openclaw/hooks/self-evolving-agent
```

Enable it:

```bash
openclaw hooks enable self-evolving-agent
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

Before major tasks:

1. Review `LEARNING_AGENDA` to see what the agent is actively training.
2. Review relevant entries from `LEARNINGS`, `ERRORS`, and `CAPABILITIES`.
3. Identify the most likely failure mode.
4. Choose an execution strategy that reduces that risk.

After major tasks:

1. Log incidents and learnings.
2. Diagnose the weakest capability involved.
3. Refresh the learning agenda if priorities changed.
4. Create or update a training unit if recurrence appears.
5. Record evaluation status.
6. Promote only after validated transfer.

## Validation

Run the repeatable local compliance suite:

```bash
python3 ~/.openclaw/skills/self-evolving-agent/scripts/run-evals.py ~/.openclaw/skills/self-evolving-agent
```

Run the model-in-the-loop benchmark:

```bash
python3 ~/.openclaw/skills/self-evolving-agent/scripts/run-benchmark.py --skill-dir ~/.openclaw/skills/self-evolving-agent
```
