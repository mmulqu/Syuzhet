# Syuzhet: Information Architecture for Fiction

> *Named after the Russian Formalist concept distinguishing **fabula** (chronological events) from **syuzhet** (how the story is told)*

## The Problem This Solves

**LLMs are terrible at writing suspenseful fiction—but not for the reason you think.**

The issue isn't prose quality, characterization, or plot structure. It's **information economy**.

LLMs are trained to be helpful, clear, and complete. They want to:
- Resolve ambiguity
- Answer questions
- Explain motivations
- Close narrative loops

**Good fiction does the opposite.** It:
- Maintains strategic ambiguity
- Delays answers
- Shows behavior without explaining it
- Keeps loops open until the right moment

This repository provides a **scaffolding system** to enforce information discipline when using LLMs for fiction writing.

---

## Core Insight: The Two Layers LLMs Conflate

### Plot vs. Information Disclosure

| Layer | Description |
|-------|-------------|
| **Plot** | What happens (events, actions, consequences) |
| **Information Disclosure** | What the reader learns, when, and how |

**These are separate authorial decisions.**

- A murder can happen in Chapter 1, but the reader might not learn who did it until Chapter 20
- Or the reader might know from page 1 while watching characters fumble toward truth (dramatic irony)

**Most LLM prompts treat these as one thing. They're not.**

---

## The Four Information States

At any moment in a story, there are **four distinct information layers**:

```
┌─────────────────────────────────────────────────────────┐
│ OBJECTIVE REALITY                                       │
│ Everything that is "true" in the story world            │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ CHARACTER KNOWLEDGE                                      │
│ What each character knows/believes (often wrong)        │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ READER KNOWLEDGE                                         │
│ What's been disclosed to the reader so far              │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ READER SUSPICION                                         │
│ What the reader infers from patterns/hints              │
└─────────────────────────────────────────────────────────┘
```

**The gaps between these layers are the story's engine:**

- **Suspense** = gap between reader suspicion and reader knowledge
- **Dramatic irony** = gap between reader knowledge and character knowledge
- **Surprise** = gap between reader suspicion and objective reality

**LLMs collapse these layers because they're trained to be clear. Clarity is the enemy of suspense.**

---

## Architecture Overview

```
repo/
├── story_bible.yaml              # SOURCE OF TRUTH: Objective reality + disclosure schedule
├── tension_curve.yaml            # Target tension levels per chapter
├── chapter_plans/                # Beat sheets with information tags
│   ├── TEMPLATE_chapter_beats.yaml
│   ├── ch01_beats.yaml
│   └── ch07_beats.yaml (example)
├── drafts/                       # Chapter drafts (generated prose)
├── prompts/                      # LLM prompts for generation and criticism
│   ├── chapter_generator.md      # Generator with information discipline rules
│   ├── reader_simulation_critic.md
│   └── tension_auditor_critic.md
├── verification/                 # Automated checks
│   └── leakage_checker.py        # Detects premature disclosure
└── feedback/                     # Critic outputs (JSON)
```

---

## The Information Ledger: `story_bible.yaml`

This is the **master document** that tracks:

### 1. Objective Reality
Everything that is TRUE in the story world, regardless of when revealed:

```yaml
objective_reality:
  - id: killer_identity
    fact: "Marcus Webb killed Elena Reeves"
    when_happened: "Three months before story opens"
    method: "Pushed her from lighthouse observation deck"
    motive_true: "Elena discovered Marcus embezzled $2M"
```

### 2. Disclosure Schedule
**When** each fact should be revealed/suspected/confirmed to the reader:

```yaml
disclosure_schedule:
  - fact_id: killer_identity
    fact: "Marcus killed Elena"

    breadcrumbs:  # Subtle hints
      - chapter: 3
        hint: "Marcus knows detail about crime scene he shouldn't"
        delivery: "Casual dialogue, easy to miss"
      - chapter: 7
        hint: "Marcus burns photograph when alone"
        delivery: "Action without explanation"

    reader_should_suspect: 12
    reader_should_be_fairly_certain: 16
    confirmed_to_reader: 18
    confirmation_method: "Witness testimony"
```

### 3. Character Knowledge States
What each character knows/believes at different points:

```yaml
character_knowledge:
  marcus_webb:
    role: "Killer"
    knows_from_start:
      - "He killed Elena"
      - "He forged the suicide note"
    believes_falsely_at_start:
      - "No one saw him"

    arc:  # How his knowledge/beliefs change
      - chapter: 15
        learns: "Investigation is focusing on him"
        impact: "Increasing desperation"
```

### 4. Withheld Information Rules
Explicit constraints on what MUST NOT be revealed:

```yaml
withheld_until_scheduled:
  - fact: "Marcus killed Elena"
    no_explicit_confirmation_before: 18
    allowed_before: "Hints, suspicious behavior, dramatic irony via his POV"
    forbidden: "Character stating it, narrator confirming it, undeniable proof"
```

---

## Tension Curve: `tension_curve.yaml`

Tracks **target tension levels** (1-10 scale) for each chapter:

```yaml
chapters:
  - number: 7
    title: "The Burning"
    target_tension: 6
    tension_type: "Ominous behavior, psychological unease"
    pacing: "Slow burn, atmospheric"

    micro_tensions:
      - "Why is Marcus burning the photograph?"
      - "What will happen if Sarah discovers it?"

    end_on: "Ominous image - photo disappears into ash"
```

**Tension scale:**
- 1-3: Low (setup, breathing room)
- 4-6: Medium (investigation, complications)
- 7-8: High (revelations, confrontations)
- 9-10: Peak (climax, life-or-death stakes)

---

## Beat Sheets with Information Tags

Each chapter gets a detailed beat sheet specifying:

### Plot + Information Architecture

```yaml
chapter_number: 7
target_tension: 6/10

information_state:
  reader_learns:
    - "Marcus has childhood photograph with Elena"
    - "He destroys it in secret"

  reader_suspects:
    - "Marcus is hiding something about their relationship"

  withheld:  # CRITICAL - what MUST NOT be revealed
    - "That they're siblings (ch 17)"
    - "That Marcus killed Elena (ch 18)"
    - "Explicit guilty thoughts"

beats:
  - beat_number: 1
    description: "Marcus retrieves hidden box from closet"

    information_function:
      reveals: "Marcus has kept something secret"
      withholds: "What else is in the box"
      hints_at: "He's been protecting this secret for a while"

    pacing: "Slow, building tension"
    end_beat_on:
      type: "Revelation"
      description: "Pulls out old photograph"
```

---

## The Workflow

### 1. Planning Phase

```bash
# Define objective reality and disclosure schedule
edit story_bible.yaml

# Set tension targets for each chapter
edit tension_curve.yaml

# Create beat sheet for current chapter
cp chapter_plans/TEMPLATE_chapter_beats.yaml chapter_plans/ch07_beats.yaml
edit chapter_plans/ch07_beats.yaml
```

### 2. Generation Phase

```bash
# Use generator prompt with LLM
# Inputs: story_bible.yaml + ch07_beats.yaml + generator prompt
# Output: drafts/ch07_draft.md
```

The **Chapter Generator** prompt (`prompts/chapter_generator.md`) includes:
- Information discipline rules
- Show-don't-tell techniques
- Forbidden phrases (that indicate over-explanation)
- POV constraints
- Pacing techniques for different tension levels

### 3. Criticism Phase

Run multiple specialized critics:

#### A. Information Leakage Checker (Automated)

```bash
python verification/leakage_checker.py 7 drafts/ch07_draft.md
```

This script:
- Cross-references `disclosure_schedule` with chapter number
- Searches for patterns that would confirm withheld facts
- Flags premature disclosure with severity ratings:
  - `MINOR`: Small detail
  - `MAJOR`: Key reveal, damages tension
  - `CRITICAL`: Central mystery spoiled

**Example output:**

```
❌ 1 LEAKAGE ISSUE DETECTED

Issue #1: 🔴 CRITICAL
FACT ID: killer_identity
FACT: Marcus Webb killed Elena Reeves

SCHEDULED REVEAL: Chapter 18
CURRENT CHAPTER: Chapter 7
REVEALED: 11 chapters too early

LINE NUMBER: 45
EXPLANATION: Narrator explicitly confirms Marcus killed Elena

EVIDENCE:
"...Marcus remembered the night he'd killed Elena, pushing her from
the lighthouse railing. The guilt consumed him..."
```

#### B. Reader Simulation Critic (LLM-based)

Use `prompts/reader_simulation_critic.md` to:
- Model what an attentive first-time reader knows/suspects
- Identify over-explained moments
- Check if chapter achieves information targets
- Flag curiosity killers

#### C. Tension Auditor Critic (LLM-based)

Use `prompts/tension_auditor_critic.md` to:
- Score actual tension vs. target
- Identify tension generators and killers
- Evaluate pacing appropriateness
- Check chapter ending pull-forward

### 4. Revision Phase

Based on critic feedback:
- Remove information leakage
- Add withheld information where under-revealed
- Adjust pacing to hit tension target
- Sharpen chapter ending

### 5. Verification Phase

Re-run leakage checker until clean:

```bash
python verification/leakage_checker.py 7 drafts/ch07_draft_v2.md

✓ NO LEAKAGE DETECTED

All information is being withheld according to schedule.
The chapter maintains appropriate information discipline.
```

---

## Key Innovations

### 1. Information as First-Class Architectural Concern

Unlike traditional beat sheets or outlines, this system **explicitly tracks information flow** as separate from plot.

**Traditional beat sheet:**
```
Scene 3: Marcus visits Elena's grave, struggles with guilt
```

**Information-architecture beat sheet:**
```yaml
beat_3:
  plot: "Marcus visits Elena's grave at 3 AM"

  reader_learns: "Marcus feels intense guilt about Elena"
  reader_suspects: "Marcus may have been involved in her death"
  withheld: "That he actually killed her"

  execution_notes:
    - "Show physical manifestation of guilt (shaking, tears)"
    - "Have him speak to grave: 'I had no choice' (ambiguous)"
    - "DO NOT have him think 'I killed you' explicitly"
```

### 2. Separation of Character Knowledge and Reader Knowledge

The system enforces: **Character knowing ≠ Reader learning**

POV characters can know secrets, but those secrets are revealed through:
- Behavior affected by the knowledge
- Suppressed memories (fragments, not full flashbacks)
- Emotional/physical reactions
- Actions that make sense only if character knows the secret

**Never through explicit internal monologue until scheduled.**

### 3. Automated Enforcement via Leakage Checker

The Python script provides **literal verification** that information discipline is maintained.

While it can't catch every possible leak (natural language is complex), it catches the most common LLM mistakes:
- Character explicitly stating a secret
- Narrator confirming withheld information
- Obvious premature revelations

### 4. Reader Simulation as Critic Type

Most writing critique focuses on **prose quality**. This system focuses on **cognitive state modeling**:

*"What does the reader know right now? What do they suspect? What questions are they holding? Is this creating the intended experience?"*

This is the defense against **clarity creep**—the LLM's natural tendency to over-explain.

### 5. Tension as Measurable Target

By setting **numerical tension targets** and using the Tension Auditor to score drafts, the system operationalizes something normally considered "subjective feel."

The auditor checks:
- Are unanswered questions creating pull forward?
- Are stakes clear?
- Does pacing match tension level?
- Is protagonist active or passive?

---

## Example: Chapter 7 Analysis

### Setup
- **Target tension:** 6/10 (medium-high, ominous)
- **POV:** Marcus (knows he killed Elena, reader doesn't)
- **Plot:** Marcus burns childhood photograph
- **Information goals:**
  - Reader suspects Marcus is hiding something
  - Reader does NOT learn he's the killer
  - Reader does NOT learn sibling connection

### What Works (Information Discipline)

```markdown
Marcus's hands shook as he turned on the kitchen faucet.
The match flared in the dark.

The photograph caught quickly, edges curling black. The two
children—those same gray-green eyes, that same half-smile—
disappeared into ash.
```

**Why this works:**
- Shows Marcus destroying evidence (action)
- Doesn't explain why (withheld)
- Plants breadcrumb about similarity ("same eyes") without stating sibling connection
- Creates ominous atmosphere (tension target: 6)
- Ends on image, not explanation

### What Would Break It (Leakage)

```markdown
❌ Marcus burned the photo of him and his half-sister Elena.
If Sarah found it, she'd know they were related, which would
expose his embezzlement motive and prove he'd killed her.
```

**Why this fails:**
- States sibling connection (withheld until ch 17)
- States he killed her (withheld until ch 18)
- Explains motivation (over-clarification)
- No mystery, no suspense
- **Leakage checker would flag this immediately**

---

## Philosophical Foundation

### Fiction is Information Warfare

The author controls:
1. **What** the reader knows
2. **When** they learn it
3. **How** they learn it (directly/indirectly, reliably/unreliably)

**Suspense = uncertainty about important outcome**

If the reader knows too much too soon → No suspense
If the reader knows too little → Confusion, detachment

The sweet spot: **Reader suspects but doesn't confirm**

### The LLM Alignment Problem for Fiction

LLMs are aligned for:
- Helpfulness
- Clarity
- Completeness
- Directness

Fiction requires:
- Strategic withholding
- Ambiguity
- Incompleteness (until the right moment)
- Indirection (subtext, implication)

**This system re-aligns the LLM toward fiction-appropriate behavior through:**
1. **Explicit constraints** (withheld lists)
2. **Architectural separation** (plot ≠ disclosure)
3. **Automated verification** (leakage checking)
4. **Specialized criticism** (reader simulation, tension auditing)

---

## Genre Applications

While the example story is a **mystery/thriller**, this architecture applies to any genre where information control matters:

### Mystery/Thriller
- **Core mechanic:** Withhold whodunit until climax
- **Information layers:** Detective knowledge vs. reader knowledge vs. killer knowledge
- **Key technique:** Plant clues without confirming theories

### Romance
- **Core mechanic:** Withhold whether couple will get together
- **Information layers:** Each partner's feelings vs. what they reveal to each other
- **Key technique:** Show internal desire while characters maintain facades

### Horror
- **Core mechanic:** Withhold nature/extent of threat
- **Information layers:** What's actually happening vs. protagonist's understanding
- **Key technique:** Reveal danger incrementally, wrongfoot reader expectations

### Literary Fiction
- **Core mechanic:** Withhold character's true nature/motivation
- **Information layers:** Character's self-perception vs. reality vs. what they show others
- **Key technique:** Unreliable narration, gradual revelation of backstory

---

## Extending the System

### Adding New Critics

Create new specialized critics as needed:

```bash
prompts/
├── chapter_generator.md
├── reader_simulation_critic.md
├── tension_auditor_critic.md
├── dialogue_critic.md          # New: Check for subtext vs. on-the-nose
├── pacing_critic.md            # New: Sentence-level rhythm analysis
└── continuity_critic.md        # New: Track consistency across chapters
```

### Enhancing Leakage Checker

The current `leakage_checker.py` uses regex patterns. Enhance with:

1. **LLM-based semantic analysis**
   - Feed draft + story bible to LLM
   - Ask: "Does this passage reveal [FACT] too early?"
   - More nuanced than pattern matching

2. **Character knowledge tracking**
   - Model what each character knows at each point
   - Flag POV violations (character knowing things they shouldn't)

3. **Inference chain analysis**
   - Detect when reader can infer withheld fact from combination of clues
   - "If reader knows A and B, they can deduce C (which is withheld)"

### Integration with Writing Tools

```bash
# Makefile for workflow automation
make plan         # Create beat sheet from template
make generate     # Call LLM with generator prompt
make critique     # Run all critics
make verify       # Run leakage checker
make revise       # Track revision cycle
```

---

## Research Questions

This repository is also a **research artifact** exploring:

1. **Can information architecture be formalized?**
   - YAML schemas for disclosure schedules
   - Graph representations of information flow
   - Formal verification of consistency

2. **Can reader cognition be modeled programmatically?**
   - Reader simulation agents
   - Belief state tracking
   - Question/answer loop modeling

3. **What are the limits of LLM fiction generation?**
   - With scaffolding, how close to human-level suspense?
   - Which aspects still require human judgment?
   - Can LLMs learn to withhold information with enough constraint?

4. **How does information economy vary by genre?**
   - Different disclosure patterns for mystery vs. romance vs. literary
   - Cultural variations (Western vs. Eastern narrative traditions)
   - Reader expectation as constraint

---

## Contributing

This system is a proof-of-concept. Ways to contribute:

### 1. Add Example Stories
- Different genres
- Different structures (non-linear, multiple POV, etc.)
- Different cultural traditions

### 2. Improve Verification
- Better leakage detection patterns
- LLM-based semantic analysis
- Character knowledge state tracking

### 3. Build Tools
- Web interface for beat sheet creation
- Visualization of tension curves
- Automated critic orchestration

### 4. Research Extensions
- Empirical testing with readers
- Comparison to human-written fiction
- Cross-genre pattern analysis

---

## Usage Guide

### Quick Start

```bash
# 1. Define your story's objective reality
cp story_bible.yaml my_story_bible.yaml
# Edit: objective_reality, disclosure_schedule, character_knowledge

# 2. Set your tension curve
cp tension_curve.yaml my_tension_curve.yaml
# Edit: target tension for each chapter

# 3. Create a chapter beat sheet
cp chapter_plans/TEMPLATE_chapter_beats.yaml chapter_plans/ch01_beats.yaml
# Fill in: beats, information goals, withheld items

# 4. Generate chapter with LLM
# Use prompts/chapter_generator.md as system prompt
# Input: story bible + beat sheet + generator rules

# 5. Verify information discipline
python verification/leakage_checker.py 1 drafts/ch01_draft.md

# 6. Run critics (using LLM)
# Use prompts/reader_simulation_critic.md
# Use prompts/tension_auditor_critic.md

# 7. Revise based on feedback

# 8. Repeat for each chapter
```

### Best Practices

1. **Freeze story_bible.yaml early**
   - Objective reality shouldn't change mid-writing
   - Disclosure schedule is the contract with the reader
   - Major changes require re-evaluating all prior chapters

2. **Run leakage checker frequently**
   - After every draft
   - Before any revisions
   - Catch problems early

3. **Trust the reader simulation critic**
   - If reader knows too much too soon, tension is lost
   - If reader is confused, engagement is lost
   - Sweet spot: reader suspects correctly but can't confirm

4. **Vary tension levels**
   - All peaks = numbness
   - Valleys make peaks feel higher
   - Follow tension curve, don't ad-lib

5. **Show, don't tell**
   - Action over explanation
   - Physical sensation over stated emotion
   - Dialogue subtext over exposition
   - Behavior over internal monologue

---

## License

MIT License - See LICENSE file

---

## Acknowledgments

**Theoretical foundations:**
- Russian Formalists (Shklovsky, Propp): Fabula vs. Syuzhet
- Narratology (Genette): Story vs. Discourse
- Cognitive narratology (Herman): Reader mental models
- Information theory (Shannon): Uncertainty and entropy

**Inspiration:**
- Every mystery author who's mastered the art of strategic withholding
- Every reader who's experienced the perfect reveal at the perfect moment
- Every editor who's red-penned "show don't tell" a thousand times

---

## Contact

For questions, discussions, or collaboration:
- Open an issue
- Submit a PR
- Fork and experiment

**The goal: Better fiction through better information architecture.**

---

*"The art of storytelling is not just about what you tell, but what you withhold—and when you finally reveal it."*
