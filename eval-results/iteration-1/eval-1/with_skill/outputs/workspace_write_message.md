## Pre-Task Risk Diagnosis

**Task Class**: unfamiliar  
**Consequence**: high  
**Horizon**: medium  
**Primary Capabilities**: memory retrieval, planning, verification, tool-use, execution discipline  
**Top Capability Risk**: verification  
**Root Cause Risk**: `memory_retrieval_weakness`, `verification_weakness`, `transfer_weakness`  
**Pattern Status**: `structural_gap`

### Evidence
- The workflow is production-facing, so small edits can have outsized blast radius.
- You have not touched this deployment path before, which means the trigger graph, environment assumptions, and rollback path are not yet internalized.
- Deployment workflows often hide risk in adjacent files or implicit dependencies: secrets, branch filters, reusable workflows, release/tag conventions, environment protections, and post-deploy checks.

### Why This Matters
The main failure mode is not syntax. It is making a plausible local edit that is semantically wrong for production: changing when deploys trigger, which environment they target, what credentials they use, or how rollback/retry behaves. On an unfamiliar workflow, the highest risk is transferring generic CI instincts into a deployment system with project-specific invariants.

### Recommended Next Step
`update_capability`

## Past Learnings To Retrieve

Retrieve these before any edit:

- Prior learnings on safe modification of unfamiliar production workflows.
- Past errors involving CI/CD trigger changes, branch/tag filters, or reusable workflow invocation.
- Past incidents involving secrets, environment variables, or environment protection rules.
- Prior learnings on rollback-first execution and “read path end-to-end before edit.”
- Capability entries for `verification`, `tool-use`, `memory retrieval`, and `execution discipline`.
- Any open training units related to deployment verification, release automation, or production blast-radius analysis.

If memory files are available, the highest-yield sources are:
- `assets/LEARNINGS.md`
- `assets/ERRORS.md`
- `assets/CAPABILITIES.md`
- `assets/TRAINING_UNITS.md`

## Execution Strategy

Use a slower, checkpointed, retrieve-then-act path:

1. Read the deployment workflow and trace its full invocation chain in read-only mode first.
2. Map the operational contract: trigger conditions, target environment, required secrets, approval gates, artifacts, rollback path, and post-deploy signals.
3. Define the exact intended behavior change in one sentence and list what must remain invariant.
4. Identify blast radius: which branches, tags, environments, jobs, or downstream systems could change.
5. Draft the smallest possible edit that satisfies the requested behavior without refactoring unrelated logic.
6. Review the diff against the invariant list before considering execution.
7. Validate in the safest available environment: local/static validation first, then non-production execution if available.
8. Prepare a rollback method before merge or deploy.

## Verification Plan

Validation should be layered:

- **Static verification**: check workflow syntax, job references, reusable workflow inputs/outputs, and expression correctness.
- **Semantic verification**: confirm triggers, conditions, environment names, secret references, concurrency, and artifact flow still match intended production behavior.
- **Blast-radius verification**: prove which branches/tags/events will and will not deploy after the change.
- **Execution-path verification**: test the modified path in a dry run, staging, or equivalent safe path if available.
- **Rollback verification**: confirm the revert path is simple, fast, and does not depend on undocumented manual repair.
- **Post-change verification**: define observable success signals up front, such as expected workflow run graph, target environment reached, artifact published, and no unintended deploy fired.

## Risk Mitigations

- Do not edit until the current deploy contract is written down.
- Prefer minimal edits over cleanup or modernization.
- Treat trigger logic and secret/environment wiring as high-risk surfaces.
- If any part of the rollback path is unclear, pause before editing.