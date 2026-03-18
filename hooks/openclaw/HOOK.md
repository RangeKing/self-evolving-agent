---
name: self-evolving-agent
description: "Injects a capability-evolution reminder during agent bootstrap"
metadata: {"openclaw":{"emoji":"🧭","events":["agent:bootstrap"]}}
---

# Self-Evolving Agent Hook

This hook reminds the agent to think in capability-evolution terms, not only in incident-logging terms.

## What It Injects

- retrieve relevant prior learnings
- inspect capability risks for the upcoming task
- after the task, diagnose weaknesses and decide whether training or evaluation is needed

## Enable

```bash
openclaw hooks enable self-evolving-agent
```

