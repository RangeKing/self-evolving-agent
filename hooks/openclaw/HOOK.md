---
name: self-evolving-agent
description: "Injects a capability-evolution reminder during agent bootstrap"
metadata: {"openclaw":{"emoji":"🧭","events":["agent:bootstrap"]}}
---

# Self-Evolving Agent Hook

This hook reminds the agent to use the phase-aware evolution runtime rather than treating `task_full` as always-on.

## What It Injects

- classify the task first
- choose exactly one mode: `task_light`, `task_full`, `agenda_review`, or `promotion_review`
- retrieve only the records required for that mode
- inspect the legacy migration layer as read-only evidence when it exists
- write new evidence through `scripts/evolution_runtime.py record-incident`
- regenerate ledgers and the manifest through the runtime, not by manual ledger edits
- run agenda review and evaluation only when their triggers fire
- promote only validated, transferable strategies

## Enable

```bash
openclaw hooks enable self-evolving-agent
```
