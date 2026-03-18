## Task Diagnosis

**Task Class**: mixed  
**Consequence**: high  
**Primary Capabilities**: tool-use, verification, execution discipline  
**Weakest Link**: verification  
**Root Cause**: verification_weakness  
**Pattern Status**: emerging_pattern

### Evidence
- I edited a release command by inventing a plausible flag instead of confirming the command contract.
- The user corrected the flag, which means correctness depended on external rescue rather than my own validation.
- I did not run a contract check first, such as `--help`, official docs, source inspection, or a dry-run-safe verification step.

### Why This Matters
This was not just a wrong flag. It exposed a failure to verify an exact tool contract in a high-consequence context. Release and automation commands are brittle at the interface level, so plausible guessing creates avoidable risk even when the surrounding reasoning is sound. The same weakness can recur across CLIs, APIs, build tooling, and deployment workflows.

### Recommended Next Step
create_training_unit

## [CAP-20260314-001] verification

**Level**: L2 assisted  
**Confidence**: medium  
**Last Reviewed**: 2026-03-14

### Current Strength
Can recognize the mistake quickly after correction and identify the missing validation step.

### Current Limits
May proceed from plausibility to action when a command or flag looks familiar, especially in tooling workflows where exact contract details matter.

### Common Failure Modes
- Guesses flag names or parameter shapes from pattern matching.
- Treats likely syntax as sufficient without checking the authoritative contract.
- Relies on user correction instead of front-loading verification.

### Evidence
- Negative: release command was edited with an unverified flag.
- Negative: user correction was required to restore correctness.
- Positive: post-task reflection correctly identified skipped contract validation as the core failure.

### Next Training Focus
Force an explicit contract-validation step before proposing, editing, or executing any command whose exact flags or parameters are not already confirmed.

### Upgrade Condition
Independently verify the exact contract before action in at least 3 consecutive tool-interface tasks, including 1 transfer case outside release tooling, with no external correction.

### Linked Units
- TRN-20260314-001
- EVL-20260314-001

## [TRN-20260314-001] Verify Tool Contracts Before Editing Commands

**Capability**: verification  
**Status**: open  
**Priority**: high  
**Created**: 2026-03-14T00:00:00+08:00  
**Trigger Signature**: Need to edit, propose, or execute a CLI/API command and the exact flag or parameter contract is not already confirmed.

### Why This Unit Exists
A high-consequence task depended on guessed interface details. The failure was caught by the user, which means the behavior is not yet reliable without rescue.

### Learning Objective
Before changing or using a command, verify the exact contract from an authoritative source and state that verification explicitly.

### Failure Pattern
- Infers flags from naming patterns instead of checking the tool contract.
- Skips validation because the guessed syntax appears plausible.

### Drills
1. Given a command-editing task, inspect the authoritative contract first and restate the exact allowed flags before making changes.
2. Compare a guessed command against the verified command and explain which assumption failed.
3. Transfer drill: repeat the same process on a different interface type, such as an API schema or another CLI tool.

### Pass Criteria
- No guessed flags or parameters across 3 consecutive drills.
- Each drill includes an explicit verification source or command-contract check before action.
- At least 1 transfer drill succeeds without external correction.

### Transfer Scenarios
- Updating deployment or release commands in a different toolchain.
- Editing API request parameters or build/test command flags.

### Evidence To Record
- Success: verification step is explicit, authoritative, and precedes the edit.
- Failure: any invented flag, skipped contract check, or post-hoc correction.

### Linked Evidence
- CAP-20260314-001
- EVL-20260314-001

## Evaluation State

**State**: recorded -> understood  
**Reason**: the incident has been diagnosed and converted into a specific capability target, but the behavior has not yet been practiced or passed under transfer.

## Promotion Decision

**Decision**: do_not_promote  
**Candidate Rule**: verify exact tool contracts before editing or executing commands in high-consequence workflows.  
**Why Not Yet**: good rule, insufficient evidence. It needs successful practice and at least one transfer case before promotion.