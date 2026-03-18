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

Copy the template ledgers:

```bash
cp ~/.openclaw/skills/self-evolving-agent/assets/LEARNINGS.md ~/.openclaw/workspace/.evolution/LEARNINGS.md
cp ~/.openclaw/skills/self-evolving-agent/assets/ERRORS.md ~/.openclaw/workspace/.evolution/ERRORS.md
cp ~/.openclaw/skills/self-evolving-agent/assets/FEATURE_REQUESTS.md ~/.openclaw/workspace/.evolution/FEATURE_REQUESTS.md
cp ~/.openclaw/skills/self-evolving-agent/assets/CAPABILITIES.md ~/.openclaw/workspace/.evolution/CAPABILITIES.md
cp ~/.openclaw/skills/self-evolving-agent/assets/TRAINING_UNITS.md ~/.openclaw/workspace/.evolution/TRAINING_UNITS.md
cp ~/.openclaw/skills/self-evolving-agent/assets/EVALUATIONS.md ~/.openclaw/workspace/.evolution/EVALUATIONS.md
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

## Promotion Targets

Only promote validated strategies into durable context:

- `AGENTS.md` for workflow rules
- `TOOLS.md` for tool-specific constraints
- `SOUL.md` for behavioral policies
- `MEMORY.md` for durable project or operator facts

## Minimum Operating Routine

Before major tasks:

1. Review relevant entries from `LEARNINGS`, `ERRORS`, and `CAPABILITIES`.
2. Identify the most likely failure mode.
3. Choose an execution strategy that reduces that risk.

After major tasks:

1. Log incidents and learnings.
2. Diagnose the weakest capability involved.
3. Create or update a training unit if recurrence appears.
4. Record evaluation status.
5. Promote only after validated transfer.

