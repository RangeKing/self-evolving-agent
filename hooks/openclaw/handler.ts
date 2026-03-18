const reminder = `
<self-evolving-agent-reminder>
Before substantial work:
- check whether the learning agenda needs review
- inspect the active learning agenda
- retrieve relevant learnings and capability risks
- identify the likely weakest link
- choose an execution strategy with a verification plan

After substantial work:
- log incidents and lessons
- diagnose the weakest capability involved
- refresh the learning agenda if priorities changed
- create a training unit if the weakness is recurring or high-leverage
- evaluate progress using recorded -> understood -> practiced -> passed -> generalized -> promoted
- promote only validated, transferable strategies
</self-evolving-agent-reminder>
`.trim();

console.log(reminder);
