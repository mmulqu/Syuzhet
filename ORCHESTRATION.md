# Loom Orchestration Guide

How to coordinate the four agents to write a story.

---

## Overview

The workflow is:

```
Architect → Scribe → Critic → Scribe → Keeper → [repeat]
```

Each agent has a specific role and communicates through artifact files.

---

## Prerequisites

1. Have access to Claude (via API, Claude.ai, or Claude Code)
2. Create a project directory based on Loom structure
3. Copy agent `CLAUDE.md` files to have agent identities available

---

## Phase 1: Story Design (Architect)

### Step 1: Load Architect Identity

**System prompt:**
```
[Paste full contents of agents/architect/CLAUDE.md]
```

**User prompt:**
```
I want to write a psychological thriller about [your premise].

Please create:
1. Story bible (story_bible.yaml)
2. Tension curve (artifacts/tension_curve.yaml)
3. Beat sheet for Chapter 1 (chapters/ch01/beats.yaml)
```

### Step 2: Review and Iterate

The Architect will propose:
- Objective reality (all the true facts)
- Disclosure schedule (when each fact is revealed)
- Character knowledge maps
- Tension targets

**Review carefully.** Once you approve and hand off to Scribe, the story bible is **frozen**.

### Step 3: Save Artifacts

Architect produces:
- `story_bible.yaml`
- `artifacts/tension_curve.yaml`
- `chapters/ch01/beats.yaml`

Save these files to your project directory.

### Step 4: Update Architect State

Architect should update `agents/architect/state.yaml`:

```yaml
story_status: active
current_chapter: 1
story_bible_locked: true
chapters_planned: [1]
chapters_handed_to_scribe: [1]
```

---

## Phase 2: Draft Writing (Scribe)

### Step 1: Load Scribe Identity

**New conversation** (or clear context)

**System prompt:**
```
[Paste full contents of agents/scribe/CLAUDE.md]
```

**User prompt:**
```
You are writing Chapter 1.

STORY BIBLE:
[Paste contents of story_bible.yaml]

BEAT SHEET:
[Paste contents of chapters/ch01/beats.yaml]

TENSION TARGET: 3/10 (from tension_curve.yaml)

Please write the chapter draft.
```

### Step 2: Receive Draft

Scribe produces prose for `chapters/ch01/draft.md`.

Save this file.

### Step 3: Update Scribe State

Scribe should update `agents/scribe/state.yaml`:

```yaml
current_chapter: 1
draft_version: 1
```

---

## Phase 3: Evaluation (Critic)

### Step 1: Load Critic Identity

**New conversation** (or clear context)

**System prompt:**
```
[Paste full contents of agents/critic/CLAUDE.md]
```

**User prompt:**
```
You are evaluating Chapter 1 draft.

BEAT SHEET (what was intended):
[Paste contents of chapters/ch01/beats.yaml]

DRAFT (what was written):
[Paste contents of chapters/ch01/draft.md]

IMPORTANT: For reader simulation lens, do NOT look at the story bible.
You are a first-time reader who only knows what the text has shown.

Please evaluate through all three lenses:
1. Reader simulation
2. Tension assessment
3. Craft critique

Produce feedback.json output.
```

### Step 2: Receive Feedback

Critic produces JSON for `chapters/ch01/feedback.json`.

Save this file.

### Step 3: Update Critic State

Critic should update `agents/critic/state.yaml`:

```yaml
chapters_reviewed: [1]
reader_state:
  confirmed_beliefs: [... from feedback]
  active_suspicions: [... from feedback]
  burning_questions: [... from feedback]
```

---

## Phase 4: Revision (Scribe Again)

### Step 1: Load Scribe Identity (Resume Session)

**Resume Scribe conversation or new conversation**

**System prompt:**
```
[Paste full contents of agents/scribe/CLAUDE.md]
```

**User prompt:**
```
You are revising Chapter 1 based on Critic feedback.

CURRENT DRAFT:
[Paste contents of chapters/ch01/draft.md]

FEEDBACK:
[Paste contents of chapters/ch01/feedback.json]

Please apply the feedback in priority order (high → medium → low).

CRITICAL: Preserve these spans verbatim:
[List preserved spans from feedback.json]

If any feedback conflicts with a preserved span, flag the conflict.

Produce revised draft.
```

### Step 2: Receive Revised Draft

Scribe produces revised prose for `chapters/ch01/draft.md` (overwrite or version as v2).

Save this file.

### Step 3: Update Scribe State

```yaml
draft_version: 2
applied_feedback:
  - issue_id: "C-1-01"
    action: "Removed explicit emotion statement"
  - issue_id: "C-1-02"
    action: "Replaced cliché with specific detail"
preserved_spans:
  - "The exact preserved quote"
```

---

## Phase 5: Verification (Keeper)

### Step 1: Load Keeper Identity

**New conversation** (or clear context)

**System prompt:**
```
[Paste full contents of agents/keeper/CLAUDE.md]
```

**User prompt:**
```
You are verifying Chapter 1, version 2.

STORY BIBLE (disclosure schedule):
[Paste relevant parts of story_bible.yaml - especially disclosure_schedule]

CURRENT CHAPTER NUMBER: 1

REVISED DRAFT:
[Paste contents of chapters/ch01/draft.md v2]

FEEDBACK (preserved spans):
[Paste preserved spans from chapters/ch01/feedback.json]

Please verify:
1. Information discipline (no leakage of facts scheduled for later chapters)
2. Revision integrity (preserved spans intact, no regressions)
3. Constraints (word count, POV, etc.)
4. Continuity

Produce verification.json output.
```

### Step 2: Receive Verification

Keeper produces JSON for `chapters/ch01/verification.json`.

### Step 3: Check Result

**If `"passed": true`:**
- Chapter 1 is complete!
- Save verification.json
- Update Keeper state:
  ```yaml
  chapters_cleared: [1]
  verification_history:
    1:
      - v1: "not verified"
      - v2: "passed"
  ```
- Proceed to Chapter 2

**If `"passed": false`:**
- Review Keeper's flags
- Return to **Phase 4 (Revision)**
- Scribe fixes flagged issues
- Re-run Keeper verification
- Repeat until passed

---

## Phase 6: Next Chapter

### Step 1: Architect Plans Chapter 2

**Resume Architect conversation**

**User prompt:**
```
Chapter 1 is complete.

Based on the reader state after Chapter 1:
[Paste reader_state from critic/state.yaml]

Please create beat sheet for Chapter 2.
```

### Step 2: Repeat the Loop

```
Architect (ch02/beats.yaml) →
Scribe (ch02/draft.md) →
Critic (ch02/feedback.json) →
Scribe (revision) →
Keeper (ch02/verification.json) →
[if passed] → Architect (ch03/beats.yaml) →
...
```

---

## Practical Tips

### Managing Conversations

**Option 1: Four Separate Conversation Threads**

- Architect thread (persistent, used for planning each chapter)
- Scribe thread (persistent, used for writing and revision)
- Critic thread (persistent, accumulates reader state)
- Keeper thread (persistent, tracks verification history)

**Option 2: Fresh Conversations Per Agent Task**

- Start new conversation for each agent action
- Load agent identity + current state
- Prevents context contamination

**Recommended:** Option 1 for continuity, Option 2 for debugging

### State Management

**Keep state files updated manually if agents don't:**

After each phase, update relevant `agents/*/state.yaml` file yourself.

This creates audit trail and makes resuming easier.

### Artifact Naming

```
chapters/
└── ch01/
    ├── beats.yaml
    ├── draft_v1.md
    ├── draft_v2.md
    ├── draft_v3.md (if needed)
    ├── draft_FINAL.md (after Keeper clearance)
    ├── feedback_v1.json (from first Critic pass)
    ├── feedback_v2.json (if re-evaluated after revision)
    └── verification_v2.json (Keeper on draft_v2)
```

Versioning helps track iteration history.

### When to Iterate

**Scribe → Critic → Scribe loop:**

Run **once** per chapter by default.

Only iterate if Keeper rejects or if Critic feedback reveals major issues.

**Avoid:**
Endless revision loops. Set a limit (e.g., 3 revisions max per chapter).

---

## Troubleshooting

### Problem: Keeper Keeps Rejecting for Leakage

**Diagnosis:** Scribe not respecting withheld list.

**Fix:**
1. Make withheld list more explicit in beat sheet
2. Add examples to Scribe prompt: "NEVER write [specific example]"
3. Consider tightening disclosure schedule (maybe hinting too early)

### Problem: Critic Says Reader is Confused

**Diagnosis:** Disclosure too vague, reader doesn't have enough information.

**Fix:**
1. Architect may need to adjust disclosure schedule for future chapters
2. Scribe may need to be clearer about what IS being revealed
3. Check if withholding the right things vs. withholding too much

### Problem: Preserved Spans Keep Getting Modified

**Diagnosis:** Scribe not tracking preserved spans properly.

**Fix:**
1. Explicitly list preserved spans in revision prompt
2. Instruct Scribe to copy them verbatim first, then revise around them
3. Keeper should reject immediately if span modified

### Problem: Tension Consistently Off Target

**Diagnosis:** Scribe not matching pacing to tension level.

**Fix:**
1. Include pacing guide in Scribe prompt (from Scribe CLAUDE.md)
2. Architect may need to give more specific pacing notes in beat sheet
3. Critic should provide concrete suggestions (add time pressure, cut description, etc.)

---

## Automation Ideas

### Shell Script

```bash
#!/bin/bash
# orchestrate.sh

CHAPTER=$1

echo "=== ARCHITECT: Planning Chapter $CHAPTER ==="
# Call Claude with Architect identity + prompt

echo "=== SCRIBE: Writing Chapter $CHAPTER ==="
# Call Claude with Scribe identity + beat sheet

echo "=== CRITIC: Evaluating Chapter $CHAPTER ==="
# Call Claude with Critic identity + draft

echo "=== SCRIBE: Revising Chapter $CHAPTER ==="
# Call Claude with Scribe identity + feedback

echo "=== KEEPER: Verifying Chapter $CHAPTER ==="
# Call Claude with Keeper identity + revised draft

# Check verification result
if [ "$PASSED" = "true" ]; then
  echo "✓ Chapter $CHAPTER cleared!"
else
  echo "✗ Chapter $CHAPTER rejected - see verification.json"
fi
```

### Python Orchestrator

```python
# orchestrator.py

import anthropic
import yaml
import json

class LoomOrchestrator:
    def __init__(self, project_dir):
        self.client = anthropic.Anthropic()
        self.project_dir = project_dir

    def architect_plan(self, chapter_num):
        """Architect plans chapter"""
        identity = self.load_agent_identity("architect")
        prompt = f"Plan chapter {chapter_num}"
        # Call Claude with identity + prompt
        # Save beats.yaml

    def scribe_write(self, chapter_num):
        """Scribe writes draft"""
        identity = self.load_agent_identity("scribe")
        beats = self.load_beats(chapter_num)
        # Call Claude
        # Save draft.md

    def critic_evaluate(self, chapter_num):
        """Critic evaluates draft"""
        identity = self.load_agent_identity("critic")
        draft = self.load_draft(chapter_num)
        # Call Claude
        # Save feedback.json

    def scribe_revise(self, chapter_num):
        """Scribe revises based on feedback"""
        # ...

    def keeper_verify(self, chapter_num):
        """Keeper verifies revision"""
        # ...
        return passed  # True/False

    def run_chapter(self, chapter_num):
        """Orchestrate full loop for one chapter"""
        self.architect_plan(chapter_num)
        self.scribe_write(chapter_num)
        self.critic_evaluate(chapter_num)
        self.scribe_revise(chapter_num)

        passed = False
        attempts = 0
        while not passed and attempts < 3:
            passed = self.keeper_verify(chapter_num)
            if not passed:
                self.scribe_revise(chapter_num)  # Fix flagged issues
            attempts += 1

        return passed
```

---

## Advanced: Parallel Evaluation

For efficiency, run **Critic** and **Keeper** in parallel on the first draft:

```
Scribe (draft v1)
    ↓
    ├─→ Critic (evaluate) ──→ feedback.json
    └─→ Keeper (verify) ────→ verification.json
    ↓
If both pass → Done
If Critic has issues → Scribe revises → Keeper re-verifies
If Keeper fails → Scribe fixes leakage → Keeper re-verifies
```

This saves time when both would pass or when only one has issues.

---

## Example Session Transcript

### Chapter 1: Full Loop

```
[Architect Session]
User: Create story bible and chapter 1 beat sheet for a thriller about...
Architect: [Creates story_bible.yaml, tension_curve.yaml, ch01/beats.yaml]

[Scribe Session]
User: Write Chapter 1 using this beat sheet: [paste beats.yaml]
Scribe: [Produces draft.md]

[Critic Session]
User: Evaluate this draft: [paste draft.md]
Critic: [Produces feedback.json]

[Scribe Session - Resume]
User: Revise based on this feedback: [paste feedback.json]
Scribe: [Produces revised draft.md v2]

[Keeper Session]
User: Verify this revision: [paste draft v2 + story bible]
Keeper: [Produces verification.json]

Result: {"passed": true}

✓ Chapter 1 complete!
```

---

## Summary Workflow Diagram

```
┌──────────────┐
│  ARCHITECT   │  Designs info economy
└──────┬───────┘
       │ beats.yaml
       ↓
┌──────────────┐
│   SCRIBE     │  Writes prose
└──────┬───────┘
       │ draft.md
       ↓
┌──────────────┐
│   CRITIC     │  Evaluates (3 lenses)
└──────┬───────┘
       │ feedback.json
       ↓
┌──────────────┐
│   SCRIBE     │  Revises
└──────┬───────┘
       │ draft.md v2
       ↓
┌──────────────┐
│   KEEPER     │  Verifies
└──────┬───────┘
       │ verification.json
       ↓
   ┌───┴───┐
   │PASS?  │
   └───┬───┘
       │
   ┌───┴────────┐
   │            │
  YES          NO
   │            │
   │            └──→ Back to SCRIBE (fix issues)
   │
   ↓
Next chapter
```

---

## Final Checklist

Before moving to next chapter:

- [ ] Architect beat sheet approved
- [ ] Scribe draft complete
- [ ] Critic feedback received
- [ ] Scribe revision applied
- [ ] Keeper verification passed
- [ ] All artifacts saved:
  - [ ] `chapters/chXX/beats.yaml`
  - [ ] `chapters/chXX/draft_FINAL.md`
  - [ ] `chapters/chXX/feedback.json`
  - [ ] `chapters/chXX/verification.json`
- [ ] Agent states updated:
  - [ ] `agents/architect/state.yaml`
  - [ ] `agents/scribe/state.yaml`
  - [ ] `agents/critic/state.yaml`
  - [ ] `agents/keeper/state.yaml`

---

**Now you're ready to orchestrate Loom. Happy weaving!**
