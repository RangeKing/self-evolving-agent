---
id: "CAP-BOOTSTRAP-007"
type: "capability"
title: "coding"
created_at: "2026-03-18T00:00:00Z"
updated_at: "2026-03-18T00:00:00Z"
tags: ["bootstrap", "coding"]
linked_records: ["AGD-BOOTSTRAP-001"]
trigger_signature: "nontrivial implementation, regression surface, multi-file edit"
level: "L3 reliable"
assessment_status: "provisional"
confidence: "medium"
last_reviewed: "2026-03-18"
status: "active"
capability: "coding"
---

### Current Strength
Can implement and refactor routine changes safely when scope and constraints are clear.

### Current Limits
May under-specify tests, edge cases, or integration effects on unfamiliar code paths.

### Common Failure Modes
- local change works but regression surface is under-checked
- implementation starts before constraints are fully mapped

### Evidence
- solid on bounded edits
- less stable on cross-cutting changes without explicit plan

### Next Training Focus
Pair every nontrivial implementation with a verification surface and regression check.

### Upgrade Condition
Deliver repeated multi-file changes with good validation and low backtracking.
