**Pre-Task Diagnosis**

- Task class: unfamiliar, high consequence, medium-to-long horizon.
- Primary capabilities required: verification, execution discipline, memory retrieval, planning, tool-use.
- Weakest link: verification.
- Root cause: `verification_weakness`, with `execution_discipline_weakness` and `memory_retrieval_weakness` as the main secondary risks.
- Pattern status: structural risk, not yet an observed incident.

Why this is the risk profile:
- A production deployment workflow can look correct while still being unsafe, especially if a change is small but affects rollout, secrets, approvals, or rollback behavior.
- The current capability map already marks verification as only assisted, with a known tendency to trust plausible work before falsification.
- The active agenda also flags verification, execution discipline, and memory retrieval as the current leverage points, which fits this task well.

**Past Learnings To Retrieve**

I would explicitly retrieve these before touching the workflow:

- [CAP-BOOTSTRAP-004 verification](/Users/rangeking/Code/self-evolving-agent/assets/CAPABILITIES.md)
- [CAP-BOOTSTRAP-008 execution discipline](/Users/rangeking/Code/self-evolving-agent/assets/CAPABILITIES.md)
- [CAP-BOOTSTRAP-002 planning](/Users/rangeking/Code/self-evolving-agent/assets/CAPABILITIES.md)
- [CAP-BOOTSTRAP-003 tool-use](/Users/rangeking/Code/self-evolving-agent/assets/CAPABILITIES.md)
- [CAP-BOOTSTRAP-001 research](/Users/rangeking/Code/self-evolving-agent/assets/CAPABILITIES.md)
- [LEARNING_AGENDA.md active focus items](/Users/rangeking/Code/self-evolving-agent/assets/LEARNING_AGENDA.md)

I did not find any deployment-workflow-specific entries in:
- [LEARNINGS.md](/Users/rangeking/Code/self-evolving-agent/assets/LEARNINGS.md)
- [ERRORS.md](/Users/rangeking/Code/self-evolving-agent/assets/ERRORS.md)
- [TRAINING_UNITS.md](/Users/rangeking/Code/self-evolving-agent/assets/TRAINING_UNITS.md)

So the safe default is to rely on the bootstrap capability guidance rather than assume prior domain-specific memory.

**Execution Strategy**

Use a `retrieve-then-act`, `decompose-first`, `checkpointed` approach:

1. Map the current deployment workflow end to end before editing.
2. Identify the exact entrypoint, environment variables, secrets, approvals, rollout mechanism, and rollback path.
3. Make the smallest possible change that satisfies the requirement.
4. Stop after each phase: discovery, draft change, preflight validation, staging verification, production rollout.

Practical rule:
- Do not broaden scope beyond the specific workflow path being changed.
- Do not combine logic changes with deployment-process changes unless the coupling is required.
- Do not rely on plausibility; require explicit proof at each checkpoint.

**Verification Plan**

Before production:
- Capture the current baseline behavior of the workflow.
- Run static checks: syntax, schema, linting, config validation, and any repo-specific CI/test commands.
- Dry-run the workflow in a non-production or preview environment if available.
- Test failure modes on purpose: invalid config, missing secret, failed approval, and rollback invocation.

During rollout:
- Prefer the smallest blast radius available, such as canary, staged rollout, or a single non-critical path first.
- Watch the exact success criteria tied to the workflow, not just “the job ran.”
- Verify logs, exit codes, artifacts, and downstream deployment status.

After rollout:
- Re-run the baseline checks to confirm nothing regressed.
- Confirm rollback still works and that the change did not weaken the recovery path.
- If the workflow is production-critical, keep monitoring long enough to catch delayed failures.

**Bottom Line**

The main risk is not building the wrong thing; it is shipping something plausible without enough falsification. I would therefore slow the task down, retrieve the verification and discipline learnings first, and treat staging proof as mandatory before any production-facing change.

Sources used:
- [system/coordinator.md](/Users/rangeking/Code/self-evolving-agent/system/coordinator.md)
- [modules/diagnose.md](/Users/rangeking/Code/self-evolving-agent/modules/diagnose.md)
- [modules/learning-agenda.md](/Users/rangeking/Code/self-evolving-agent/modules/learning-agenda.md)
- [modules/evaluator.md](/Users/rangeking/Code/self-evolving-agent/modules/evaluator.md)
- [modules/promotion.md](/Users/rangeking/Code/self-evolving-agent/modules/promotion.md)
- [assets/LEARNING_AGENDA.md](/Users/rangeking/Code/self-evolving-agent/assets/LEARNING_AGENDA.md)
- [assets/CAPABILITIES.md](/Users/rangeking/Code/self-evolving-agent/assets/CAPABILITIES.md)
- [assets/LEARNINGS.md](/Users/rangeking/Code/self-evolving-agent/assets/LEARNINGS.md)
- [assets/ERRORS.md](/Users/rangeking/Code/self-evolving-agent/assets/ERRORS.md)
- [assets/TRAINING_UNITS.md](/Users/rangeking/Code/self-evolving-agent/assets/TRAINING_UNITS.md)

