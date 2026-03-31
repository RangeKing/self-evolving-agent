#!/bin/bash
set -e

OUTPUT="${CLAUDE_TOOL_OUTPUT:-}"

ERROR_PATTERNS=(
  "error:"
  "Error:"
  "ERROR:"
  "failed"
  "FAILED"
  "command not found"
  "No such file"
  "Permission denied"
  "fatal:"
  "Exception"
  "Traceback"
  "TypeError"
  "SyntaxError"
  "exit code"
  "non-zero"
)

contains_error=false
for pattern in "${ERROR_PATTERNS[@]}"; do
  if [[ "$OUTPUT" == *"$pattern"* ]]; then
    contains_error=true
    break
  fi
done

if [ "$contains_error" = true ]; then
  cat << 'EOF'
<self-evolving-agent-error>
An execution failure was detected.
Do not only patch the symptom.
Also ask:
- which capability failed or was weak?
- should the task escalate from task_light mode to task_full mode?
- should this be recorded through `scripts/evolution_runtime.py record-incident`?
- does this require a training unit, agenda review, or evaluation update?
</self-evolving-agent-error>
EOF
fi
