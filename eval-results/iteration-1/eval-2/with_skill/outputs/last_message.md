## Task Diagnosis

**Task Class**: mixed  
**Consequence**: high  
**Primary Capabilities**: verification, tool-use, execution discipline  
**Weakest Link**: verification  
**Root Cause**: verification_weakness  
**Pattern Status**: emerging_pattern

### Evidence
- The release command was edited by inferring a plausible flag name instead of checking the tool’s accepted contract.
- The user had to correct the flag, so the task outcome depended on external rescue rather than independent validation.
- No authoritative check happened before the edit proposal: no help output, docs, schema, or existing command contract was inspected first.

### Why This Matters
Operational commands are brittle interfaces with narrow accepted values. Guessing a plausible flag can look correct while still breaking release behavior. This is a high-consequence failure mode because it affects automation, is easy to miss in review, and is exactly the kind of mistake that user rescue can hide until later.

### Recommended Next Step
create_training_unit

## [CAP-20260314-001] verification

**Level**: L2 assisted  
**Confidence**: medium  
**Last Reviewed**: 2026-03-14

### Current Strength
Can recognize after correction that operational edits require contract validation and can explain the better strategy.

### Current Limits
On unfamiliar or semi-familiar operational tooling, still risks substituting pattern-matching for direct contract inspection before editing.

### Common Failure Modes
- Infers flag names or accepted values from naming conventions.
- Treats a plausible command edit as sufficient without verifying the interface.
- Skips the explicit checkpoint of “inspect the contract before changing the command.”

### Evidence
- Negative evidence: edited a release command with a guessed flag and needed user correction.
- Negative evidence: did not validate the tool contract before proposing the change.
- Positive evidence: correctly identified the real failure as skipped contract validation rather than a mere typo.

### Next Training Focus
For any operational command, workflow step, or API parameter change, identify and inspect an authoritative contract source before proposing the edit.

### Upgrade Condition
Independently complete three operational-interface edits with explicit contract checks, including one transfer case outside release tooling, with no guessed parameters and no user correction.

### Linked Units
- TRN-20260314-001
- EVL-20260314-001

## [TRN-20260314-001] contract-first-verification-for-operational-interfaces

**Capability**: verification  
**Status**: active  
**Priority**: high  
**Created**: 2026-03-14T00:00:00+08:00  
**Trigger Signature**: editing CLI flags, workflow inputs, or API parameters with accepted-value constraints

### Why This Unit Exists
A release command was modified by guessing a flag name, and the mistake was caught by user correction rather than by validation. This is a high-leverage weakness because the same habit can recur across deployment, CI, release, and API tasks.

### Learning Objective
Before editing an operational interface, inspect the authoritative contract and base the change on verified accepted parameters or values.

### Failure Pattern
- Guesses plausible flags from convention or analogy.
- Moves from intent to edit without a contract-validation checkpoint.
- Relies on user correction to surface invalid operational parameters.

### Drills
1. Given an operational change request, list the contract sources to inspect first and extract the accepted parameters or values before proposing any edit.
2. Compare a guessed command edit against a contract-validated edit and explain why the guessed version is unsafe.
3. Transfer drill: apply the same contract-first routine to a CI workflow field or API query parameter rather than a release command.

### Pass Criteria
- Names the authoritative contract source before proposing the edit.
- Uses inspected contract evidence to justify the chosen flag or value.
- Completes one transfer scenario with no guessed parameter names and no external correction.

### Transfer Scenarios
- Updating a CI workflow step with constrained inputs.
- Changing an API/tool invocation that has enumerated accepted values.

### Evidence To Record
- Success: contract source was inspected first and the chosen parameter matches verified accepted values.
- Failure: parameter choice was guessed, inferred, or corrected externally after proposal.

### Linked Evidence
- CAP-20260314-001
- EVL-20260314-001

## [EVL-20260314-001] verify-tool-contract-before-operational-edits

**Capability**: verification  
**State**: understood  
**Reviewed**: 2026-03-14T00:00:00+08:00  
**Reviewer Judgment**: sufficient

### Target Behavior
Verify the accepted contract of operational commands and parameters before editing plausible values.

### Evidence
- The incident exposed a concrete failure caused by guessing a flag.
- The corrected diagnosis identifies skipped contract validation as the central mistake.
- A training unit now defines trigger conditions, drills, and pass criteria.

### Self-Explanation Check
Operational interfaces often reject plausible-but-invalid values. Inspecting the contract first prevents confident edits that are syntactically reasonable but behaviorally wrong.

### Counterexample Check
This rule should not expand into unnecessary ceremony for tasks that do not involve constrained interfaces, such as pure prose edits or cosmetic refactors with no operational parameters.

### Transfer Check
Not yet tested in a new context.

### Next State Decision
Advance to `understood`; require deliberate practice before `practiced`.

### Linked Records
- TRN-20260314-001
- CAP-20260314-001

## Promotion Decision

**Candidate**: verify-tool-contract-before-operational-edits  
**Current State**: understood  
**Decision**: defer  
**Target**: none

### Trigger Signature
Editing commands, scripts, workflows, or API parameters where the interface accepts only specific flags, names, or values.

### Evidence For Promotion
- One high-consequence failure showed the cost of guessing.
- The corrected strategy is clear and reusable.
- A training unit and evaluation record now exist.

### Transfer Proof
No transfer case yet.

### Minimal Durable Rule
For operational interfaces, inspect the accepted contract before editing plausible parameter values.

### Risks
- Promoting now would be premature because there is no passed drill or transfer evidence.
- If overgeneralized, the rule could create unnecessary overhead on low-risk non-operational edits.