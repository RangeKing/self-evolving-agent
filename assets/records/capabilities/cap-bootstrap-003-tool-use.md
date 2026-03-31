---
id: "CAP-BOOTSTRAP-003"
type: "capability"
title: "tool-use"
created_at: "2026-03-18T00:00:00Z"
updated_at: "2026-03-18T00:00:00Z"
tags: ["bootstrap", "tooling"]
linked_records: ["AGD-BOOTSTRAP-001"]
trigger_signature: "unfamiliar tool, brittle interface, shell output needs inspection"
level: "L3 reliable"
assessment_status: "provisional"
confidence: "medium"
last_reviewed: "2026-03-18"
status: "active"
capability: "tool-use"
---

### Current Strength
Can select and use common tools effectively in routine development and analysis workflows.

### Current Limits
May over-trust plausible commands or under-inspect outputs on unfamiliar tooling.

### Common Failure Modes
- chooses a sensible but suboptimal tool
- proceeds before reading command output closely

### Evidence
- strong on familiar shell and repo inspection tasks
- weaker when interface contracts are novel or brittle

### Next Training Focus
Inspect tool output before moving to the next step on unfamiliar commands.

### Upgrade Condition
Handle unfamiliar tooling with explicit contract checks and low rework across multiple tasks.
