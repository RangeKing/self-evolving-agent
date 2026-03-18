## [EVL-20260314-002] verification-before-operational-changes

**Capability**: verification
**State**: generalized
**Reviewed**: 2026-03-14T15:00:00Z
**Reviewer Judgment**: sufficient

### Target Behavior
Verify accepted operational flags and conditions before modifying scripts or workflow commands.

### Evidence
- The strategy was previously trained on deployment-command work after a failure mode involving guessed operational values.
- In a different release automation task, the agent applied the same verification-first behavior before updating the release flow.
- The task was completed correctly without user correction, showing independent reuse rather than rescue.

### Self-Explanation Check
Operational commands and automation settings often accept narrow, brittle contracts. Verifying the contract before editing prevents plausible but invalid changes.

### Counterexample Check
This should not trigger for purely descriptive or cosmetic edits that do not alter operational parameters, accepted values, or release/deployment behavior.

### Transfer Check
The behavior transferred from deployment-command training to a different release automation context, which is related but not identical.

### Next Decision
advance state

## Promotion Decision

**Candidate**: verify-tool-contract-before-operational-edits
**Current State**: generalized
**Decision**: promote
**Target**: AGENTS.md

### Trigger Signature
Editing deployment commands, release automation, workflow steps, scripts, or API parameters with accepted-value constraints.

### Evidence For Promotion
- The strategy was explicitly trained after an earlier operational-guessing failure.
- It later worked independently on a different release automation task.
- The transfer case required the same core judgment and succeeded without user correction.

### Transfer Proof
The strategy first applied to deployment commands, then transferred successfully to release automation updates.

### Minimal Durable Rule
For operational commands and workflow parameters, inspect the accepted contract before editing plausible values.

### Risks
- Low overfitting risk because the rule is scoped to operational interfaces.
- Low misfire risk because verification is cheap relative to release/deployment mistakes.
- Scope risk if expanded beyond contract-sensitive changes.