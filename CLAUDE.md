# Loom

A multi-agent system for writing fiction with controlled information disclosure.

## Core Insight

**LLMs are eager explicators**—they want to resolve ambiguity and close loops.

**Good fiction does the opposite:** it opens loops strategically and keeps them open until the right moment.

This system enforces **information discipline** through architecture.

---

## The Problem

When using LLMs to write suspenseful fiction, they naturally:
- Resolve ambiguity prematurely
- Explain character motivations directly
- Confirm suspicions too early
- Close narrative loops before the right moment

This kills suspense. Not because the prose is bad, but because **information economy** is broken.

**The solution:** Separate **plot** (what happens) from **disclosure** (when reader learns about it).

**The method:** Use **constraints** instead of creative direction.

---

## The Four Agents

| Agent | Role | Key Responsibility |
|-------|------|--------------------|
| **Architect** | Designs constraints | Disclosure schedule, withheld lists, tension targets |
| **Scribe** | Writes within constraints | Creative freedom + respect for constraints |
| **Critic** | Evaluates blindly | Reader experience (sees prose only, not plans) |
| **Keeper** | Verifies against constraints | Pass/fail gate for leakage and tension |

---

## The Four Information Layers

At any moment in a story, there are four distinct states:

```
┌─────────────────────────────────────────┐
│  OBJECTIVE REALITY                      │
│  Everything that's "true"               │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  CHARACTER KNOWLEDGE                     │
│  What each character knows/believes     │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  READER KNOWLEDGE                        │
│  What's been disclosed to reader        │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  READER SUSPICION                        │
│  What reader infers from patterns       │
└─────────────────────────────────────────┘
```

**The gaps between these layers create:**
- **Suspense** = gap between reader suspicion and reader knowledge
- **Dramatic irony** = gap between reader knowledge and character knowledge
- **Surprise** = gap between reader suspicion and objective reality

---

## The Loop

```
Architect
    ↓
  Creates story bible + constraints (once per chapter)
    ↓
Scribe
    ↓
  Writes draft within constraints
    ↓
Critic
    ↓
  Evaluates blindly (prose only)
    ↓
Scribe
    ↓
  Revises based on feedback
    ↓
Keeper
    ↓
  Verifies against constraints (leakage? tension? preserved spans?)
    ↓
  [if failed] → back to Scribe
  [if passed] → next chapter
```

---

## Sacred Rules

### 1. Story Bible is FROZEN Once Approved

**Once Architect hands off to Scribe, objective reality is locked.**

Changes to disclosure schedule or character knowledge require re-evaluating all prior chapters.

### 2. Critic Never Sees Story Architecture

When Critic evaluates, they **only see prose**.

No story bible, no disclosure schedule, no constraints files, no withheld lists.

This prevents the bias of "I know what's coming."

### 3. Keeper is the Only Verification Agent with Full Access

Keeper sees everything: story bible, disclosure schedule, withheld lists, tension targets.

Keeper compares draft against disclosure schedule to catch leakage.

Keeper compares Critic's tension assessment to the target.

This is the enforcement layer.

### 4. Preserved Spans are Inviolable

When Critic marks prose as `preserve`, Scribe **never modifies** it.

If feedback conflicts with a preserved span → preserve wins.

### 5. No Agent Reveals Anything Before Its Scheduled Disclosure

Every agent is constrained by the disclosure schedule.

**Architect** designs it.
**Scribe** follows withheld lists (doesn't see full disclosure schedule).
**Critic** evaluates against it (unknowingly, through reader simulation).
**Keeper** enforces it.

### 6. Constraints Over Creative Direction

**Architect provides:**
- WHAT to hide (withheld lists)
- WHEN to reveal (disclosure schedule)
- WHAT tension level to hit (tension targets)

**Architect does NOT provide:**
- HOW to write scenes (Scribe's job)
- WHAT events to include (Scribe's creative freedom)
- Beat-by-beat plot outlines (removed - too prescriptive)

**Scribe has creative freedom within constraints.**

---

## Agent Details

### Architect

**Identity:** Designer of information economy and constraints

**Creates:**
- Story bible (`story_bible.yaml`)
- Disclosure schedule (`disclosure_schedule.yaml`) - when facts: hinted → suspected → confirmed (for Keeper verification)
- Tension targets (`artifacts/tension_targets.yaml`) - target intensity per chapter (constraint for Scribe)
- Withheld lists (per chapter in `chapters/chXX/constraints.yaml`) - facts that MUST NOT be revealed
- Character knowledge maps

**Does NOT create:**
- ~~Beat sheets~~ (removed - were creative direction, not constraints)
- ~~Scene outlines~~ (Scribe's creative freedom)

**State:** `agents/architect/state.yaml`

**See:** `agents/architect/CLAUDE.md` for full instructions

---

### Scribe

**Identity:** Writer with creative freedom within constraints

**Reads:**
- Chapter constraints (`chapters/chXX/constraints.yaml`) - withheld lists + tension target
- Story bible (for consistency reference only)
- Previous chapter prose (for continuity)
- Feedback from Critic

**Does NOT read:**
- ~~Beat sheets~~ (don't exist)
- ~~Disclosure schedule~~ (that's for Keeper verification)

**Writes:**
- Draft prose (`chapters/chXX/draft.md`)

**Creative freedom:**
- What events happen
- What scenes to include
- POV character (unless specified)
- How to structure chapter
- Voice and style

**Must respect:**
- Withheld list (never reveal these facts)
- Tension target (hit this emotional level)
- Allowed breadcrumbs (can plant these subtly)
- Continuity with previous chapters

**Rules:**
- NEVER reveal anything in withheld list
- NEVER have characters explain motivations
- End scenes on questions, not answers
- Show, don't tell
- Character knowledge ≠ reader knowledge

**State:** `agents/scribe/state.yaml`

**See:** `agents/scribe/CLAUDE.md` for full instructions

---

### Critic

**Identity:** Evaluator through three lenses (completely blind to architecture)

**Three Lenses:**

1. **Reader Simulation**
   - What does reader know/suspect/wonder?
   - Where is dramatic irony active?
   - Where was curiosity killed?
   - **Critically:** Does this WITHOUT seeing story architecture

2. **Tension Assessment**
   - What tension level does this create?
   - Where are stakes deflated?
   - Where does pacing go flat?
   - **Note:** Assesses FELT tension, doesn't compare to target (Keeper does that)

3. **Craft Critique**
   - Clichés, weak verbs, telling not showing
   - POV violations, overwriting
   - Also: notes STRENGTHS (preserve candidates)

**Reads:**
- Prose only (`chapters/chXX/draft.md`)
- Chapter summaries (optional, for continuity)

**Does NOT read:**
- ~~Story bible~~ (stay blind)
- ~~Disclosure schedule~~ (stay blind)
- ~~Withheld lists~~ (stay blind)
- ~~Constraints files~~ (stay blind)
- ~~Tension targets~~ (assess actual, don't compare)

**Output:** `chapters/chXX/feedback.json`

**State:** `agents/critic/state.yaml`

**See:** `agents/critic/CLAUDE.md` for full instructions

---

### Keeper

**Identity:** Gatekeeper who verifies against constraints

**Checks:**

1. **Information Discipline**
   - Compare draft against disclosure schedule
   - Compare draft against withheld lists
   - Flag leakage (critical/major/near-miss)
   - Verify POV character only knows what they should

2. **Tension Verification**
   - Compare Critic's tension assessment to target
   - Variance ≤1: PASS
   - Variance 2: WARN
   - Variance ≥3: REJECT

3. **Revision Integrity**
   - Preserved spans intact?
   - No new leakage introduced in editing?
   - Constraints satisfied (word count, POV, banned phrases)?
   - No continuity errors?

**Verdict:** PASS or REJECT

**Output:** `chapters/chXX/verification.json`

**State:** `agents/keeper/state.yaml`

**See:** `agents/keeper/CLAUDE.md` for full instructions

---

## Directory Structure

```
loom/
├── CLAUDE.md                     # This file - project overview
├── README.md                     # Detailed documentation
├── story_bible.yaml              # Frozen source of truth
├── disclosure_schedule.yaml      # When facts are revealed (for Keeper)
│
├── agents/
│   ├── architect/
│   │   ├── CLAUDE.md             # Architect identity & instructions
│   │   └── state.yaml            # Planning status
│   │
│   ├── scribe/
│   │   ├── CLAUDE.md             # Scribe identity & instructions
│   │   └── state.yaml            # Writing status
│   │
│   ├── critic/
│   │   ├── CLAUDE.md             # Critic identity & instructions
│   │   └── state.yaml            # Evaluation history
│   │
│   └── keeper/
│       ├── CLAUDE.md             # Keeper identity & instructions
│       └── state.yaml            # Verification audit trail
│
├── chapters/
│   └── ch01/
│       ├── constraints.yaml      # Withheld lists + tension target
│       ├── draft.md              # Scribe's prose
│       ├── feedback.json         # Critic's evaluation
│       └── verification.json     # Keeper's pass/fail verdict
│
├── artifacts/
│   └── tension_targets.yaml     # Tension targets per chapter
│
├── prompts/                      # Legacy single-agent prompts
├── verification/                 # Legacy leakage checker script
└── examples/                     # Templates and examples
```

---

## Workflow Example: Writing Chapter 7

### Step 1: Architect Creates Constraints

**Architect creates:** `chapters/ch07/constraints.yaml`

```yaml
chapter: 7
tension_target: 6

withheld:  # Scribe MUST NOT reveal these
  - fact_id: central_mystery
    fact: "That Marcus killed Elena"
    specific_prohibitions:
      - "No internal thoughts like 'I killed her'"
      - "No explicit guilt about the murder"
      - "No memories of pushing her"

  - fact_id: sibling_relationship
    fact: "That Marcus and Elena are siblings"
    specific_prohibitions:
      - "Don't state the relationship"
      - "Photo can show them as children but not labeled"

allowed_breadcrumbs:  # What CAN be shown this chapter
  - "Marcus burns childhood photograph (suspicious behavior)"
  - "Marcus avoids looking at lighthouse (guilt reaction)"

previous_chapter_prose: "chapters/ch06/draft.md"
```

**Updates:** `agents/architect/state.yaml`

```yaml
chapters_with_constraints: [1, 2, 3, 7]
bible_locked: true
```

---

### Step 2: Scribe Writes

**Scribe reads:**
- `chapters/ch07/constraints.yaml` (the constraints)
- `story_bible.yaml` (for consistency)
- `chapters/ch06/draft.md` (previous chapter for continuity)

**Scribe decides:**
- What events happen in this chapter (creative freedom)
- How to hit tension target of 6
- How to plant allowed breadcrumbs subtly

**Scribe writes:** `chapters/ch07/draft.md`

**Updates:** `agents/scribe/state.yaml`

```yaml
current_chapter: 7
draft_version: 1
```

---

### Step 3: Critic Evaluates (Blind)

**Critic reads:**
- `chapters/ch07/draft.md` (prose only)

**Critic does NOT see:**
- `story_bible.yaml`
- `disclosure_schedule.yaml`
- `chapters/ch07/constraints.yaml`

**Critic produces:** `chapters/ch07/feedback.json`

```json
{
  "reader_state": {
    "confirmed_beliefs": [...],
    "active_suspicions": [...],
    "burning_questions": [...]
  },
  "tension": {
    "actual": 5,
    "diagnosis": "Stakes deflated in scene 2"
  },
  "issues": [
    {
      "id": "C-7-01",
      "severity": "high",
      "quote": "She realized he must be lying",
      "instruction": "Show her noticing inconsistency without conclusion"
    }
  ],
  "preserve": [
    "The coffee had gone cold in the way of neglected things"
  ]
}
```

**Updates:** `agents/critic/state.yaml`

```yaml
chapters_reviewed: [1, 2, 3, 7]
reader_state:
  confirmed_beliefs: [... updated]
  active_suspicions: [... updated]
```

---

### Step 4: Scribe Revises

**Scribe reads:** `chapters/ch07/feedback.json`

**Prioritizes issues:**
1. High severity first (C-7-01)
2. Medium severity
3. Low severity

**Revises:** `chapters/ch07/draft.md` (v2)

**Protects preserve spans:** Must appear verbatim

**Updates:** `agents/scribe/state.yaml`

```yaml
draft_version: 2
applied_feedback:
  - issue_id: "C-7-01"
    action: "Removed explicit realization"
preserved_spans:
  - "The coffee had gone cold..."
```

---

### Step 5: Keeper Verifies

**Keeper reads:**
- `story_bible.yaml` (objective reality)
- `disclosure_schedule.yaml` (when facts should be revealed)
- `chapters/ch07/constraints.yaml` (withheld lists, tension target)
- `chapters/ch07/draft.md` (v2)
- `chapters/ch07/feedback.json` (preserved spans, Critic's tension assessment)

**Checks:**

1. **Information discipline**
   - Scans for facts withheld until ch 17+
   - Confirms no explicit revelations

2. **Tension verification**
   - Target: 6, Actual: 5 (from Critic)
   - Variance: 1 → PASS (within acceptable range)

3. **Revision integrity**
   - Verifies preserved spans intact
   - Checks no new leakage introduced
   - Confirms constraints met

**Keeper produces:** `chapters/ch07/verification.json`

```json
{
  "passed": true,
  "information_discipline": {"status": "pass"},
  "tension_verification": {
    "target": 6,
    "actual": 5,
    "variance": 1,
    "status": "pass"
  },
  "revision_integrity": {"status": "pass"},
  "constraints": {"status": "pass"},
  "cleared": true,
  "action": "Approved - proceed to next chapter"
}
```

**Updates:** `agents/keeper/state.yaml`

```yaml
chapters_cleared: [1, 2, 3, 7]
verification_history:
  7:
    - v1: "failed - leakage"
    - v2: "passed"
```

---

### Step 6: Next Chapter

**Architect** creates `chapters/ch08/constraints.yaml` and cycle repeats.

---

## Agent Communication

Agents communicate through **state files** and **artifact files**, not direct messages.

### Architect → Scribe

**Via:** `chapters/chXX/constraints.yaml`

Architect provides constraints:
- Withheld list (hard constraint: don't reveal these)
- Tension target (constraint: hit this level)
- Allowed breadcrumbs (what CAN be shown)

### Scribe → Critic

**Via:** `chapters/chXX/draft.md`

Scribe provides draft for evaluation.

### Critic → Scribe

**Via:** `chapters/chXX/feedback.json`

Critic provides:
- Reader state (what reader knows/suspects/wonders)
- Tension assessment (actual felt tension)
- Prioritized issues
- Preserved spans

### Scribe → Keeper

**Via:** `chapters/chXX/draft.md` (revised)

Scribe provides revised draft for verification.

### Keeper → Scribe

**Via:** `chapters/chXX/verification.json`

Keeper provides:
- PASS or REJECT
- Specific flags if failed
- Clearance if passed

---

## Key Innovations

### 1. Constraints Over Creative Direction

**Old approach (removed):**
```yaml
# Beat sheet told Scribe HOW to write
beats:
  - description: "Marcus retrieves hidden box"
    pacing: "slow, building tension"
    end_on: "Pulls out photograph - revelation"
```

**New approach:**
```yaml
# Constraints tell Scribe WHAT to hide and WHAT tension to hit
withheld:
  - "That Marcus killed Elena"
  - "That photo shows sibling relationship"
allowed_breadcrumbs:
  - "Marcus has childhood photo with Elena"
tension_target: 6
```

Scribe decides HOW to create a compelling chapter within these constraints.

### 2. Enforced Separation of Knowledge States

**Architect** knows everything (designs constraints).

**Scribe** knows what's withheld (follows constraints).

**Critic** only knows what text has shown (evaluates blindly).

**Keeper** knows everything (verifies against constraints).

This prevents knowledge contamination.

### 3. Automated Constraint Verification

**Keeper** programmatically checks:
- Disclosure schedule against draft (leakage?)
- Withheld lists against draft (violations?)
- Tension target vs. Critic's assessment (missed target?)

This catches violations that humans might miss.

### 4. Preserved Spans as Inviolable Artifacts

When Critic identifies exceptional prose, it's locked in.

Revision can happen around it, but the preserved span itself is sacred.

This protects voice and strong writing from death-by-revision.

### 5. Blind Evaluation

Critic never sees story architecture - only prose.

This ensures feedback models actual reader experience, not biased by "I know what's coming."

---

## Design Principles

### 1. Each Agent Has One Job

**Architect:** Design constraints
**Scribe:** Write within constraints
**Critic:** Evaluate blindly
**Keeper:** Verify against constraints

No overlap. No confusion.

### 2. State is Explicit and Tracked

Every agent maintains `state.yaml` showing:
- Where they are in the process
- What they've done
- What they need to do next

This makes the system auditable and resumable.

### 3. Communication Through Artifacts, Not Chat

Agents don't "talk" to each other.

They produce artifacts (constraints, drafts, feedback, verification) that the next agent reads.

This makes the workflow clear and debuggable.

### 4. The Story Bible is the Constitution

Once locked, it's the source of truth.

All agents are bound by it.

Changes require project-wide re-evaluation.

### 5. Creative Freedom Within Constraints

Scribe has full creative control WITHIN constraints.

Architect tells WHAT to hide and WHAT tension to hit.

Scribe decides HOW to write a compelling chapter.

This balance prevents both over-prescription and under-constraint.

---

## When to Use This System

**Use Loom when:**
- Writing mystery, thriller, suspense
- Information control is critical to the story
- You need to maintain ambiguity strategically
- Reader's knowledge state must be carefully managed

**Don't use Loom when:**
- Writing non-fiction or documentation
- Linear storytelling where everything is revealed as it happens
- Character study where mystery isn't the point
- Short pieces where the overhead isn't worth it

---

## Getting Started

### Quick Start

1. **Architect** creates `story_bible.yaml`:
   - Define objective reality
   - Map character knowledge

2. **Architect** creates `disclosure_schedule.yaml`:
   - Schedule when facts are disclosed (for Keeper verification)

3. **Architect** creates `artifacts/tension_targets.yaml`:
   - Set tension targets per chapter

4. **Architect** creates first constraints:
   - `chapters/ch01/constraints.yaml` (withheld lists, tension target)

5. **Scribe** writes first draft:
   - `chapters/ch01/draft.md`

6. **Critic** evaluates:
   - `chapters/ch01/feedback.json`

7. **Scribe** revises

8. **Keeper** verifies:
   - `chapters/ch01/verification.json`

9. If passed → Architect creates constraints for Chapter 2

### Detailed Workflow

See `WORKFLOW.md` for comprehensive guide.

---

## Philosophy

**Good fiction is information warfare.**

The author controls:
1. **What** the reader knows
2. **When** they learn it
3. **How** they learn it (directly/indirectly, reliably/unreliably)

**Suspense = uncertainty about important outcome**

This system gives you the tools to control that uncertainty with precision.

Not by prescribing every beat (removed).

By **defining constraints** and letting creativity fill the space within them.

---

## The Name

**Loom** captures the weaving metaphor:
- Weaving threads of plot and information
- Adjusting **tension** (literal loom terminology)
- "To loom" = to emerge threateningly (what good suspense does)

Also: Russian Formalists distinguished **fabula** (raw events) from **syuzhet** (how story is told).

This system is syuzhet made operational through constraints.

---

## Further Reading

- `README.md` - Comprehensive documentation
- `WORKFLOW.md` - Detailed workflow guide
- `QUICKSTART.md` - 5-step getting started
- `agents/*/CLAUDE.md` - Individual agent instructions
- `story_bible.yaml` - Example story with disclosure schedule
- `tension_targets.yaml` - Example tension targets

---

**Welcome to Loom. Let's weave some suspense with constraints, not prescriptions.**
