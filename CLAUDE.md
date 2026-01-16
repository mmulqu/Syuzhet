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

---

## The Four Agents

| Agent | Role | Key Responsibility |
|-------|------|--------------------|
| **Architect** | Designs information economy | Story bible, disclosure schedule, beat sheets |
| **Scribe** | Writes and revises prose | Draft quality, applying feedback |
| **Critic** | Evaluates reader experience | Feedback through 3 lenses (reader/tension/craft) |
| **Keeper** | Guards constraints, verifies integrity | Pass/fail gate |

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
  Creates story bible + chapter beats (once per chapter)
    ↓
Scribe
    ↓
  Writes draft
    ↓
Critic
    ↓
  Produces feedback (reader state, tension, craft issues)
    ↓
Scribe
    ↓
  Revises based on prioritized feedback
    ↓
Keeper
    ↓
  Verifies (leakage? preserved spans intact? constraints?)
    ↓
  [if failed] → back to Scribe
  [if passed] → next chapter
```

---

## Sacred Rules

### 1. Story Bible is FROZEN Once Approved

**Once Architect hands off to Scribe, objective reality is locked.**

Changes to disclosure schedule or character knowledge require re-evaluating all prior chapters.

### 2. Critic Never Sees Story Bible

When Critic wears the "reader simulation" hat, they **only know what the text has shown**.

This prevents the bias of "I know what's coming."

### 3. Keeper is the Only Verification Agent with Full Bible Access

Keeper compares draft against disclosure schedule to catch leakage.

This is the enforcement layer.

### 4. Preserved Spans are Inviolable

When Critic marks prose as `preserve`, Scribe **never modifies** it.

If feedback conflicts with a preserved span → preserve wins.

### 5. No Agent Reveals Anything Before Its Scheduled Disclosure

Every agent is constrained by the disclosure schedule.

**Architect** designs it.
**Scribe** follows it.
**Critic** evaluates against it (unknowingly, through reader simulation).
**Keeper** enforces it.

---

## Agent Details

### Architect

**Identity:** Designer of information economy

**Creates:**
- Story bible (`story_bible.yaml`)
- Disclosure schedule (when facts: hinted → suspected → confirmed)
- Tension curve (`artifacts/tension_curve.yaml`)
- Character knowledge maps
- Chapter beat sheets (`chapters/chXX/beats.yaml`)

**State:** `agents/architect/state.yaml`

**See:** `agents/architect/CLAUDE.md` for full instructions

---

### Scribe

**Identity:** Writer and reviser of prose

**Reads:**
- Chapter beat sheet (what happens, what's withheld)
- Story bible (for consistency reference only)
- Feedback from Critic

**Writes:**
- Draft prose (`chapters/chXX/draft.md`)

**Rules:**
- NEVER reveal anything marked WITHHELD
- NEVER have characters explain motivations
- End scenes on questions, not answers
- Show, don't tell
- When character knows something reader doesn't, write behavior AS IF they know it

**State:** `agents/scribe/state.yaml`

**See:** `agents/scribe/CLAUDE.md` for full instructions

---

### Critic

**Identity:** Evaluator through three lenses

**Three Lenses:**

1. **Reader Simulation**
   - What does reader know/suspect/wonder?
   - Where is dramatic irony active?
   - Where was curiosity killed?
   - **Critically:** Does this WITHOUT seeing story bible

2. **Tension Assessment**
   - Does chapter hit target tension?
   - Where are stakes deflated?
   - Where does pacing go flat?

3. **Craft Critique**
   - Clichés, weak verbs, telling not showing
   - POV violations, overwriting
   - Also: notes STRENGTHS (preserve candidates)

**Output:** `chapters/chXX/feedback.json`

**State:** `agents/critic/state.yaml`

**See:** `agents/critic/CLAUDE.md` for full instructions

---

### Keeper

**Identity:** Gatekeeper who verifies nothing broke

**Checks:**

1. **Information Discipline**
   - Compare draft against disclosure schedule
   - Flag leakage (critical/major/near-miss)
   - Verify POV character only knows what they should

2. **Revision Integrity**
   - Preserved spans intact?
   - No new leakage introduced in editing?
   - Constraints satisfied (word count, POV, etc.)?
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
│       ├── beats.yaml            # Architect's plan for this chapter
│       ├── draft.md              # Scribe's prose
│       ├── feedback.json         # Critic's evaluation
│       └── verification.json     # Keeper's pass/fail verdict
│
├── artifacts/
│   └── tension_curve.yaml        # Tension targets per chapter
│
├── prompts/                      # Legacy single-agent prompts
├── verification/                 # Legacy leakage checker script
└── examples/                     # Templates and examples
```

---

## Workflow Example: Writing Chapter 7

### Step 1: Architect Plans

**Architect creates:** `chapters/ch07/beats.yaml`

```yaml
chapter_number: 7
target_tension: 6

information_state:
  reader_learns:
    - "Marcus has childhood photograph with Elena"
  reader_suspects:
    - "Marcus is hiding something about their relationship"
  withheld:
    - "That they're siblings (ch 17)"
    - "That Marcus killed Elena (ch 18)"

beats:
  - beat_number: 1
    description: "Marcus retrieves hidden box"
    # ...
```

**Updates:** `agents/architect/state.yaml`

```yaml
chapters_planned: [1, 2, 3, 7]
chapters_handed_to_scribe: [1, 2, 3, 7]
```

---

### Step 2: Scribe Writes

**Scribe reads:**
- `story_bible.yaml` (for consistency)
- `chapters/ch07/beats.yaml` (the instructions)
- `artifacts/tension_curve.yaml` (target: 6/10)

**Scribe writes:** `chapters/ch07/draft.md`

**Updates:** `agents/scribe/state.yaml`

```yaml
current_chapter: 7
draft_version: 1
```

---

### Step 3: Critic Evaluates

**Critic reads:**
- `chapters/ch07/draft.md` (the prose)
- `chapters/ch07/beats.yaml` (what was intended)
- **NOT** `story_bible.yaml` (reads as naive reader)

**Critic produces:** `chapters/ch07/feedback.json`

```json
{
  "reader_state": {
    "confirmed_beliefs": [...],
    "active_suspicions": [...],
    "burning_questions": [...]
  },
  "tension": {
    "target": 6,
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
- `story_bible.yaml` (disclosure schedule)
- `chapters/ch07/draft.md` (v2)
- `chapters/ch07/feedback.json` (preserved spans)

**Checks:**

1. **Information discipline**
   - Scans for facts withheld until ch 17+
   - Confirms no explicit revelations

2. **Revision integrity**
   - Verifies preserved spans intact
   - Checks no new leakage introduced
   - Confirms constraints met

**Keeper produces:** `chapters/ch07/verification.json`

```json
{
  "passed": true,
  "information_discipline": {"status": "pass"},
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

**Architect** creates `chapters/ch08/beats.yaml` and cycle repeats.

---

## Agent Communication

Agents communicate through **state files** and **artifact files**, not direct messages.

### Architect → Scribe

**Via:** `chapters/chXX/beats.yaml`

Architect provides beat sheet with:
- What happens (plot)
- What's withheld (constraints)
- Target tension

### Scribe → Critic

**Via:** `chapters/chXX/draft.md`

Scribe provides draft for evaluation.

### Critic → Scribe

**Via:** `chapters/chXX/feedback.json`

Critic provides:
- Reader state
- Tension assessment
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

### 1. Information as First-Class Architectural Concern

Traditional beat sheet:
```
Scene 3: Marcus visits grave, feels guilty
```

This system:
```yaml
beat_3:
  plot: "Marcus visits grave at 3 AM"
  reader_learns: "Marcus feels intense guilt"
  reader_suspects: "Marcus may be involved"
  withheld: "That he actually killed her"
```

**Information function is separate from plot function.**

### 2. Enforced Separation of Knowledge States

**Architect** knows everything (designs objective reality).

**Scribe** knows what characters know (writes their POV).

**Critic** (as reader) only knows what text has shown.

**Keeper** knows everything (verifies against objective reality).

This prevents knowledge contamination.

### 3. Automated Verification

**Keeper** programmatically checks disclosure schedule against draft.

This catches leakage that humans might miss (especially after multiple drafts).

### 4. Preserved Spans as Inviolable Artifacts

When Critic identifies exceptional prose, it's locked in.

Revision can happen around it, but the preserved span itself is sacred.

This protects voice and strong writing from death-by-revision.

---

## Design Principles

### 1. Each Agent Has One Job

**Architect:** Design
**Scribe:** Write
**Critic:** Evaluate
**Keeper:** Verify

No overlap. No confusion.

### 2. State is Explicit and Tracked

Every agent maintains `state.yaml` showing:
- Where they are in the process
- What they've done
- What they need to do next

This makes the system auditable and resumable.

### 3. Communication Through Artifacts, Not Chat

Agents don't "talk" to each other.

They produce artifacts (beat sheets, drafts, feedback, verification) that the next agent reads.

This makes the workflow clear and debuggable.

### 4. The Story Bible is the Constitution

Once locked, it's the source of truth.

All agents are bound by it.

Changes require project-wide re-evaluation.

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
   - Schedule when facts are disclosed
   - Map character knowledge

2. **Architect** creates `artifacts/tension_curve.yaml`:
   - Set tension targets per chapter

3. **Architect** creates first beat sheet:
   - `chapters/ch01/beats.yaml`

4. **Scribe** writes first draft:
   - `chapters/ch01/draft.md`

5. **Critic** evaluates:
   - `chapters/ch01/feedback.json`

6. **Scribe** revises

7. **Keeper** verifies:
   - `chapters/ch01/verification.json`

8. If passed → Architect plans Chapter 2

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

Not by writing better prose (though that helps).

By **architecting information disclosure** as a first-class concern.

---

## The Name

**Loom** captures the weaving metaphor:
- Weaving threads of plot and information
- Adjusting **tension** (literal loom terminology)
- "To loom" = to emerge threateningly (what good suspense does)

Also: Russian Formalists distinguished **fabula** (raw events) from **syuzhet** (how story is told).

This system is syuzhet made operational.

---

## Further Reading

- `README.md` - Comprehensive documentation
- `WORKFLOW.md` - Detailed workflow guide
- `QUICKSTART.md` - 5-step getting started
- `agents/*/CLAUDE.md` - Individual agent instructions
- `story_bible.yaml` - Example story with disclosure schedule
- `tension_curve.yaml` - Example tension curve

---

**Welcome to Loom. Let's weave some suspense.**
