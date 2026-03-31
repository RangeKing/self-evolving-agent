const reminder = `
<self-evolving-agent-reminder>
Use the phase-aware runtime, not the whole loop by default.

Before substantial work:
- classify first with scripts/evolution_runtime.py classify-task
- choose exactly one mode: task_light, task_full, agenda_review, or promotion_review
- retrieve only that mode's context with scripts/evolution_runtime.py retrieve-context
- if legacy-self-improving exists, treat it as read-only evidence during retrieval

While executing:
- keep task_light small unless a real defect, user rescue, recurrence, or high-consequence unknown forces escalation
- reserve agenda_review for explicit review triggers
- reserve promotion_review for transfer or promotion decisions

After meaningful work:
- write evidence through scripts/evolution_runtime.py record-incident
- rebuild summaries through the runtime, not by editing ledgers directly
- run scripts/evolution_runtime.py review-agenda only when triggers fire
- run scripts/evolution_runtime.py evaluate only when state advancement or promotion readiness is in question
</self-evolving-agent-reminder>
`.trim();

console.log(reminder);
