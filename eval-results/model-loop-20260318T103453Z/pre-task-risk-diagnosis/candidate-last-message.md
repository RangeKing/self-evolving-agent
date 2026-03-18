An agenda review is triggered here. This task is `unfamiliar + high consequence + medium/long horizon`, so the active pre-task focus should stay on `verification`, `execution discipline`, and `memory retrieval`.

**Pre-Task Risk Diagnosis**

**Task Class**: unfamiliar  
**Consequence**: high  
**Primary Capabilities**: planning, verification, tool-use, coding, execution discipline, memory retrieval, long-horizon task handling  
**Weakest Link Risk**: verification  
**Root Cause Risk**: `verification_weakness` + `memory_retrieval_weakness` + `execution_discipline_weakness`  
**Pattern Status**: structural_gap

**Evidence**
- Production deployment workflow changes are operationally brittle and easy to misjudge from a plausible-looking diff.
- The current agenda already marks `verification`, `execution discipline`, and `memory retrieval` as active focuses.
- There are no concrete deployment-specific `LRN-*`, `ERR-*`, or `TRN-*` records yet, so prior operational knowledge must be pulled from repo history and run history, not from the ledger.

**Why This Matters**  
The main failure mode is not syntax. It is changing hidden behavior: triggers, permissions, environment targeting, approval gates, artifact flow, or rollback behavior. On an unfamiliar production workflow, the default risk is making a locally sensible edit before the full contract is mapped.

**Past Learnings To Retrieve Now**
- `AGD-BOOTSTRAP-001`: active focus on front-loading checks, following the full loop, and retrieving lessons before acting.
- `CAP-BOOTSTRAP-004` `verification`: checks must be declared before delivery.
- `CAP-BOOTSTRAP-008` `execution discipline`: do not compress planning or verification under momentum.
- `CAP-BOOTSTRAP-009` `memory retrieval`: pull prior lessons early, especially for near-neighbor tasks.
- Supporting capabilities: `CAP-BOOTSTRAP-002` `planning`, `CAP-BOOTSTRAP-003` `tool-use`, `CAP-BOOTSTRAP-010` `long-horizon task handling`.

Because the ledgers do not yet contain deployment-specific incidents, also retrieve repo-local operational memory before editing:
- Current workflow file and every script/reusable workflow/action it calls
- Last 3-5 commits touching that path
- Last successful and failed production runs
- Deploy/runbook docs and incident notes
- Required secrets, vars, permissions, branch filters, environment rules, concurrency rules
- Current rollback path

**Execution Strategy**

Use `retrieve-then-act + decompose-first + slower-but-verified`.

1. Map the workflow contract before editing: trigger, inputs, permissions, secrets, environments, approvals, concurrency, artifacts, deploy target, health checks, rollback.
2. Build a small change table: current behavior, intended behavior, failure mode if wrong, proof required.
3. Make the smallest possible diff. Do not mix cleanup with the operational change.
4. Verify every changed edge explicitly before merge.

**Verification Plan**
- Static checks: lint/validate workflow syntax and diff-review triggers, permissions, env selection, concurrency, and approval gates.
- Call-graph checks: inspect reusable workflows, composite actions, and shell scripts invoked by the workflow.
- Safe execution: prefer local dry-run tooling or staging/manual-dispatch rehearsal before any production path.
- Negative-path checks: missing secret, wrong branch filter, approval bypass, concurrency collision, artifact mismatch, rollback drift.
- Release safety: define rollback before merge, including exact revert path or command.
- Post-change observation: predeclare success signals, monitor the first run, and stop on any deviation.

The right next step is to inspect the actual workflow and produce the contract map and change table before any edits.