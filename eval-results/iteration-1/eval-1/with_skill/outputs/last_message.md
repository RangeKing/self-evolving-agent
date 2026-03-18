## Task Diagnosis

**Task Class**: unfamiliar  
**Consequence**: high  
**Primary Capabilities**: planning, verification, tool-use, memory retrieval, coding  
**Weakest Link**: verification  
**Root Cause**: transfer_weakness  
**Pattern Status**: structural_gap

### Evidence
- The target is a production deployment workflow with direct operational consequence.
- The workflow has not been touched before, so local conventions and hidden dependencies are likely unknown.
- Deployment edits are prone to plausible-but-wrong changes in flags, conditions, secrets, environment names, approvals, and job ordering.

### Why This Matters
This is not a normal config edit. Production deployment workflows often encode brittle contracts across CI, scripts, secrets, environments, approvals, and rollback behavior. On unfamiliar operational paths, the main risk is not syntax failure but semantically incorrect changes that still look reasonable in review.

### Recommended Next Step
retrieve_then_act

## Retrieval Set

### Learnings to retrieve first
- Any prior learning with trigger signature: editing operational commands, scripts, workflow steps, or API parameters with accepted-value constraints.
- Any prior learning about environment-name mismatches, CLI flag guessing, secret/context naming, or branch/tag condition mistakes.
- Any prior learning about refactoring staging and production into shared logic without changing production semantics.
- Any prior learning about rollback-first workflow changes, dry runs, or change isolation for release/deploy systems.

### Errors to retrieve first
- Past incidents involving `.github/workflows/`, deploy scripts, release scripts, or infra entrypoints.
- Near-misses where a plausible normalization changed behavior: `prod` vs `production`, tag filters, matrix values, shell args, action inputs.
- Failures caused by missing `needs`, changed job order, altered permissions, environment protection rules, or secret resolution.

### Capability records to inspect
- `verification`
- `tool-use`
- `planning`
- `memory retrieval`
- `long-horizon task handling`

### Open training units to inspect
- Verification before operational edits
- Tool-contract inspection before refactor
- Rollback-first execution on high-consequence changes
- Change decomposition for unfamiliar CI/CD systems

## Execution Strategy

**Mode**: slower but verified, retrieve-then-act, decompose-first, checkpointed

1. Map the deployment surface before editing.
   - Identify trigger paths, deploy jobs, shared scripts, required secrets, environments, approvals, artifacts, and rollback hooks.
2. Recover prior local intent.
   - Read recent commits, PR descriptions, runbooks, and adjacent workflow/script comments for why the current shape exists.
3. Define the invariant set.
   - Explicitly preserve production trigger conditions, target environment, artifact selection, credentials, approval gates, and rollback path.
4. Reduce the change to the smallest safe unit.
   - Prefer minimal behavioral edits over cleanup/refactor. Do not combine semantic changes with formatting or modernization.
5. Checkpoint before any write.
   - Summarize current behavior, proposed delta, risk points, and expected unchanged behavior.
6. Edit only after contract verification.
   - Verify accepted action inputs, script flags, secret names, environment identifiers, and job dependencies from the source of truth.
7. Verify in increasing-cost order.
   - Static review first, then local lint/parsing if available, then non-prod or dry-run path, then production-gated release only if parity is established.

## Verification Plan

- **Behavioral parity check**
  - Compare before/after triggers, job graph, permissions, environment names, secrets, inputs, artifact flow, and deploy target resolution.
- **Contract verification**
  - Confirm action versions, action inputs, script flags, CLI accepted values, and environment identifiers against actual workflow/script definitions.
- **Blast-radius check**
  - Ensure production-only gates, approvals, concurrency, and rollback behavior are unchanged unless intentionally modified.
- **Simulation check**
  - If supported, validate YAML/workflow syntax and run a dry-run, preview, or staging-equivalent path before production use.
- **Diff discipline**
  - Keep the patch narrowly scoped so every behavioral change is inspectable.
- **Rollback readiness**
  - Identify the exact revert path before merge or apply.
- **Final go/no-go gate**
  - Do not ship if any production semantic is inferred rather than verified.

## Top Capability Risks

1. **Verification**
   - Highest risk because deployment systems fail through plausible semantic mistakes, not obvious syntax errors.
2. **Memory Retrieval**
   - Hidden repo-specific conventions are likely to exist outside the workflow file itself.
3. **Planning**
   - The task requires preserving behavior while changing structure, which is where unfamiliar operational edits usually drift.