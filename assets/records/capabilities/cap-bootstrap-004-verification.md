---
id: "CAP-BOOTSTRAP-004"
type: "capability"
title: "verification"
created_at: "2026-03-18T00:00:00Z"
updated_at: "2026-03-18T00:00:00Z"
tags: ["bootstrap", "verification", "focus"]
linked_records: ["AGD-BOOTSTRAP-001"]
trigger_signature: "high-consequence change, plausible output, pre-delivery checks"
level: "L2 assisted"
assessment_status: "provisional"
confidence: "medium"
last_reviewed: "2026-03-18"
status: "active"
capability: "verification"
---

### Current Strength
Can verify effectively when a validation plan is explicit and test surfaces are obvious.

### Current Limits
May deliver plausible work before attempting falsification, especially on operational or unfamiliar changes.

### Common Failure Modes
- checks too late
- validates the happy path only
- confuses plausibility with proof

### Evidence
- improves sharply when required to state checks first
- still vulnerable on high-consequence interfaces

### Next Training Focus
Design checks before delivery and look for failure cases, not only confirmation.

### Upgrade Condition
Complete repeated unfamiliar tasks with explicit pre-delivery checks and no rescue-driven corrections.
