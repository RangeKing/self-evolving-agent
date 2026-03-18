# Self-Evolving Coordinator

This file defines the primary operating system for the skill.

## Mission

Transform passive correction into active capability evolution.

The system must preserve memory logging, but memory is not the endpoint. The endpoint is a more capable agent with measurable progress and transferable strategies.

## First Principles

1. Logging is evidence collection, not mastery.
2. Repeated incidents are usually symptoms of capability weakness.
3. Promotion without transfer testing creates brittle rules.
4. The goal is not only fewer mistakes, but stronger independence on unfamiliar work.
5. Learning should be framed in capability terms, not only incident terms.

## Operating Stack

### Layer 1: Memory

Capture:

- errors
- corrections
- learnings
- feature requests
- recurring patterns

Primary files:

- `assets/LEARNINGS.md`
- `assets/ERRORS.md`
- `assets/FEATURE_REQUESTS.md`

### Layer 2: Diagnosis

Diagnose:

- Which capabilities the task required
- Which capability failed or nearly failed
- Whether the issue is incidental or systemic
- What root cause best explains the outcome

Primary module:

- `modules/diagnose.md`

### Layer 3: Training

For recurring or high-leverage weaknesses, create targeted training units.

Primary module:

- `modules/curriculum.md`

Primary file:

- `assets/TRAINING_UNITS.md`

### Layer 4: Evaluation and Policy

Track whether the learning has been:

- recorded
- understood
- practiced
- passed
- generalized
- promoted

Primary modules:

- `modules/evaluator.md`
- `modules/promotion.md`

Primary files:

- `assets/EVALUATIONS.md`
- `assets/CAPABILITIES.md`

## Standard Workflow

### Step 1: Classify task

Classify the task on three axes:

- novelty: familiar | mixed | unfamiliar
- consequence: low | medium | high
- horizon: short | medium | long

If the task is `mixed` or `unfamiliar`, or has `high` consequence, force a pre-task diagnosis.

### Step 2: Retrieve relevant memory

Retrieve:

- related learning entries
- related errors
- matching capabilities
- open training units

Ask:

- Have I failed in a similar way before?
- Is there an existing strategy that should be re-used?
- Is there an open training unit relevant to this task?

### Step 3: Pre-task risk diagnosis

Identify:

- required capabilities
- likely weak points
- verification risks
- tool-use risks
- decomposition risks

Output:

- top capability risks
- mitigation plan
- verification plan

### Step 4: Choose execution strategy

Examples:

- slower but verified
- tool-assisted and checkpointed
- decompose-first
- retrieve-then-act
- draft-then-critique

### Step 5: Perform task

While executing:

- note unexpected friction
- note any near-miss that almost caused failure
- note whether prior learnings actually helped

### Step 6: Post-task reflection

Run the protocol in `modules/reflection.md`.

Mandatory questions:

- What capability did this task really test?
- What was the weakest link?
- What evidence supports that diagnosis?
- What should be trained next?

### Step 7: Update capability map

Use `modules/capability-map.md` to update:

- current level
- evidence
- failure modes
- next focus
- upgrade condition

### Step 8: Create or revise training unit

Create a training unit if any condition is true:

- same weakness repeated twice
- weakness blocked a high-value task
- strategy was understood but not executable under pressure
- the agent compensated through luck or user rescue

### Step 9: Evaluate progress

Use `modules/evaluator.md`.

Do not skip state transitions. Explicitly mark what changed and why.

### Step 10: Promote only validated strategy

Promotion requires:

- clear trigger signature
- at least one passed training unit
- at least one successful transfer case
- evidence of durable reuse value

## Capability-Oriented Taxonomy

Default capability families:

- research
- planning
- tool-use
- verification
- synthesis
- communication
- coding
- execution discipline
- memory retrieval
- long-horizon task handling

Use these unless a project-specific extension is justified.

## Root Cause Taxonomy

Diagnose failures using one or more of:

- knowledge gap
- decomposition weakness
- verification weakness
- tool-use weakness
- communication weakness
- memory retrieval weakness
- execution discipline weakness
- transfer weakness

## Evidence Standard

Prefer concrete evidence over subjective impressions:

- direct error output
- user correction
- missed requirement
- rework needed
- successful re-use in a new context
- successful completion under reduced support

## Anti-Patterns

Do not:

- mark something learned just because it was written down
- promote a rule that only worked once in one narrow context
- confuse user rescue with capability gain
- flood long-term memory with fragile local hacks
- create training units with vague pass criteria

## Minimal Execution Output

For each meaningful cycle, produce:

1. `Task Diagnosis`
2. `Capability Update`
3. `Training Decision`
4. `Evaluation State`
5. `Promotion Decision`

