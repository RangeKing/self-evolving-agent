#!/bin/bash
set -e

cat << 'EOF'
<self-evolving-agent-reminder>
Use the phase-aware runtime:
1. classify the task with `scripts/evolution_runtime.py classify-task`
2. choose one mode: `task_light`, `task_full`, `agenda_review`, or `promotion_review`
3. retrieve only that mode's records with `scripts/evolution_runtime.py retrieve-context`
4. execute with a mode-appropriate verification plan
5. record evidence with `scripts/evolution_runtime.py record-incident`
6. review agenda or promotion only when those triggers fire
</self-evolving-agent-reminder>
EOF
