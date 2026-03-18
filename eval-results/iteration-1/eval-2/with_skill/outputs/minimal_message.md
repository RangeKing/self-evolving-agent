## Task Diagnosis
**Task Class**: mixed  
**Consequence**: medium  
**Primary Capabilities**: tool-use, verification, execution discipline  
**Weakest Link**: verification  
**Root Cause**: verification_weakness, execution_discipline_weakness  
**Pattern Status**: emerging_pattern

**Evidence**
- A release command was edited by guessing a flag instead of checking the command’s defined interface.
- The error was caught by user correction, not by self-validation.
- The missed step was contract validation, not command assembly.

**Why This Matters**  
This failure mode is broader than one release command. Any CLI, API, or tool wrapper with a strict contract can be broken by plausible-but-unverified parameter guesses. The real risk is false confidence under time pressure: producing syntactically neat changes that are semantically unsupported.

**Recommended Next Step**  
`create_training_unit`

## Capability Update
**Capability**: verification  
**Level**: hold at `L2 assisted`  
**Confidence**: medium  
**Current Strength**: can modify commands and recover after correction.  
**Current Limits**: does not consistently verify tool contracts before editing invocation details.  
**Common Failure Modes**
- infers flag names from pattern instead of source-of-truth docs/help text
- treats plausibility as sufficient evidence
- skips preflight validation on “small” command edits

**Evidence Update**
- Negative evidence: external correction was required.
- Positive evidence: root cause was recognized immediately after correction.

**Next Training Focus**  
Before changing any command/tool invocation, explicitly validate accepted flags/args from the tool contract.

**Upgrade Condition**  
Three consecutive command/tool edits where the contract is checked first and no external correction is needed, including one transfer case outside release tooling.

## Training Unit
**Title**: Contract-First Command Editing  
**Capability**: verification  
**Priority**: high  
**Trigger Signature**: editing commands, flags, CLI args, API parameters, or tool schemas

**Learning Objective**  
Replace “best-guess invocation edits” with “source-verified invocation edits.”

**Drills**
1. For 5 command edits, write the contract source before proposing the change.
2. For each edit, list one invalid-but-plausible flag and reject it explicitly.
3. Transfer drill: apply the same process to a non-release CLI or API call.

**Pass Criteria**
- No guessed flags
- Contract source cited before edit
- One successful transfer case without user rescue