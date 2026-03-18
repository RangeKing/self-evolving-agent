## Task Diagnosis

**Task Class**: unfamiliar  
**Consequence**: high  
**Horizon**: medium  
**Primary Capabilities**: memory retrieval, planning, verification, tool-use, execution discipline  
**Top Capability Risks**: memory retrieval, verification, decomposition  
**Weakest Likely Link**: verification  
**Likely Root Causes**: `memory_retrieval_weakness`, `verification_weakness`, `decomposition_weakness`  
**Pattern Status**: emerging_pattern

### Evidence
- The workflow is production-facing, so hidden side effects matter.
- You have not touched this deployment path before, so transfer from familiar repos is unreliable.
- Deployment workflows often encode non-obvious contracts: triggers, approvals, secrets, environment bindings, rollback assumptions.

### Why This Matters
This is the kind of task where a plausible edit can still be dangerous. The main failure mode is not syntax breakage; it is changing runtime behavior without noticing, such as altered triggers, permission scope, artifact flow, environment selection, concurrency, or rollback posture. Because the workflow is unfamiliar, the safest path is retrieval-first and verification-heavy.

### Recommended Next Step
`update_capability` and use a `retrieve_then_act` strategy before any edit.

## Past Learnings To Retrieve

Retrieve any prior entries or repo knowledge related to:

- Production deployment incidents, postmortems, or near-misses.
- Previous CI/CD workflow changes that affected triggers, approvals, secrets, permissions, or rollback.
- Known verification checklists for deploy pipelines: dry-run, staging parity, smoke tests, rollback criteria.
- Environment-specific constraints: protected branches, tag/release conventions, required reviewers, manual approvals.
- Artifact promotion rules: build once/promote many, image tags, immutable artifacts, migration ordering.
- Open training units or past mistakes involving automation changes, especially skipped verification or misunderstood workflow dependencies.

## Execution Strategy

Use: `retrieve_then_act` + `decompose_first` + `slower_but_verified`

1. Build a workflow map before editing.
   - Identify triggers, jobs, dependencies, environments, secrets, permissions, concurrency rules, approval gates, artifact inputs/outputs, and rollback touchpoints.

2. Define the exact requested behavior change.
   - Separate the desired behavioral delta from incidental refactoring. Keep the patch minimal.

3. Trace blast radius.
   - For each changed line, ask what job behavior, trigger condition, environment binding, or release invariant it can affect.

4. Compare against retrieved learnings.
   - Reuse any known-safe patterns already validated in this repo or adjacent workflows.

5. Prepare a minimal patch plus explicit rollback.
   - Know how to revert quickly if verification fails.

## Verification Plan

1. Static verification
   - Validate workflow syntax and schema.
   - Review the diff specifically for triggers, `permissions`, `secrets`, `environment`, `concurrency`, conditional expressions, and artifact references.

2. Behavioral verification
   - Confirm the modified workflow still matches the intended deploy path, approval flow, and environment targeting.
   - Check that unchanged jobs remain unchanged in behavior.

3. Safe execution check
   - Prefer branch-scoped, non-prod, or manual-dispatch validation first.
   - If staging exists, run there before production.
   - If no safe environment exists, require an especially small patch and explicit rollback readiness.

4. Post-run verification
   - Confirm expected jobs ran, only expected jobs ran, and the target environment/artifact/version is correct.
   - Run smoke checks appropriate to the service.
   - Verify logs for skipped guards, permission failures, or unexpected retries.

5. Rollback readiness
   - Define the exact revert action before merge/apply.
   - Define what signal triggers rollback and who/what confirms recovery.

## Practical Guardrail

Do not start by editing YAML. Start by reconstructing the workflow’s operational contract. In unfamiliar production automation, understanding the current guarantees is the real first task.