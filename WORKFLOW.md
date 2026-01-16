# Workflow Guide: Using the Information Architecture System

## Overview

This guide walks through the complete workflow for writing a chapter using the information architecture system.

---

## Phase 1: Story Setup (Once per project)

### Step 1: Define Objective Reality

Edit `story_bible.yaml`:

```yaml
objective_reality:
  - id: your_fact_id
    fact: "What is objectively true"
    when_happened: "Timeline"
    relevant_details: "Additional context"
```

**Questions to answer:**
- What are ALL the facts that are true in your story world?
- What are the central mysteries/secrets?
- What do characters know that readers shouldn't (yet)?

### Step 2: Create Disclosure Schedule

Still in `story_bible.yaml`:

```yaml
disclosure_schedule:
  - fact_id: your_fact_id
    fact: "Description"

    breadcrumbs:
      - chapter: 3
        hint: "Subtle hint to plant"
        delivery: "How to deliver it"

    reader_should_suspect: 12
    confirmed_to_reader: 18
```

**Questions to answer:**
- When should reader first suspect each fact?
- When should they be fairly certain?
- When should it be confirmed?
- What breadcrumbs lead there?

### Step 3: Map Character Knowledge

Still in `story_bible.yaml`:

```yaml
character_knowledge:
  protagonist:
    knows_from_start: [...]
    believes_falsely: [...]
    learning_arc:
      - chapter: X
        learns: "New fact"
        impact: "How it changes them"
```

### Step 4: Set Tension Curve

Edit `tension_curve.yaml`:

```yaml
chapters:
  - number: 1
    target_tension: 3
    tension_type: "Curiosity"
    pacing: "Slow, methodical"
```

Map out all chapters' tension targets.

---

## Phase 2: Chapter Planning

### Step 1: Create Beat Sheet

```bash
cp chapter_plans/TEMPLATE_chapter_beats.yaml chapter_plans/ch07_beats.yaml
```

### Step 2: Fill in Information Architecture

```yaml
information_state:
  reader_learns:
    - "Concrete fact reader learns"

  reader_suspects:
    - "What reader should suspect"

  withheld:
    - "What MUST NOT be revealed"
```

**This is crucial.** The withheld list is your constraint.

### Step 3: Define Beats

For each beat:

```yaml
beats:
  - beat_number: 1
    description: "What happens"

    plot_function: "Events, actions"

    information_function:
      reveals: "What this shows reader"
      withholds: "What this specifically doesn't show"
      hints_at: "Breadcrumbs planted"
```

### Step 4: Set Chapter Opening/Closing

```yaml
opening:
  hook: "What grabs attention"
  example_first_line: "Draft opening"

closing:
  type: "Question / Revelation / Cliffhanger"
  example_last_line: "Draft closing"
```

---

## Phase 3: Generation

### Step 1: Prepare LLM Prompt

**System prompt:** Content from `prompts/chapter_generator.md`

**User prompt structure:**

```
You are writing Chapter 7: "The Burning"

STORY BIBLE (excerpt relevant to this chapter):
[Include: objective_reality items, disclosure_schedule for this chapter,
character_knowledge for POV character]

BEAT SHEET:
[Full contents of ch07_beats.yaml]

TENSION TARGET: 6/10 - Ominous behavior, psychological unease

CRITICAL CONSTRAINTS:
- DO NOT reveal: [List from withheld]
- DO plant breadcrumbs: [List from breadcrumbs]
- POV: Marcus (close third)
- Word count: ~2000 words

Please write the chapter following all information discipline rules.
```

### Step 2: Generate Draft

Run the LLM with the combined prompt.

Save output to `drafts/ch07_draft.md`.

---

## Phase 4: Verification & Criticism

### Step 1: Automated Leakage Check

```bash
python verification/leakage_checker.py 7 drafts/ch07_draft.md
```

**If leakage detected:**
- Review flagged passages
- Identify what was revealed too early
- Revise to ambiguate or withhold

**Repeat until clean.**

### Step 2: Reader Simulation Critique

**LLM prompt:**

```
System: [Contents of prompts/reader_simulation_critic.md]

User:
You are analyzing Chapter 7 of "The Silent Witness."

STORY BIBLE:
[Full story_bible.yaml]

BEAT SHEET:
[ch07_beats.yaml]

PREVIOUS CHAPTERS SUMMARY:
[Summary of chapters 1-6, or full text if available]

CURRENT CHAPTER DRAFT:
[Full text of ch07_draft.md]

Please provide a complete reader simulation analysis.
```

**Save output to:** `feedback/ch07_reader_simulation.md`

**Review for:**
- Information leakage (cross-check with automated checker)
- Over-explanation flags
- Reader questions active/closed
- Comparison to beat sheet targets

### Step 3: Tension Audit

**LLM prompt:**

```
System: [Contents of prompts/tension_auditor_critic.md]

User:
You are auditing Chapter 7.

TARGET TENSION: 6/10

CHAPTER DRAFT:
[Full text of ch07_draft.md]

BEAT SHEET:
[ch07_beats.yaml]

Please provide a complete tension audit.
```

**Save output to:** `feedback/ch07_tension_audit.md`

**Review for:**
- Actual tension score vs. target
- Tension generators (what's working)
- Tension killers (what's undermining)
- Pacing issues
- Chapter ending strength

### Step 4: Aggregate Feedback

Create `feedback/ch07_aggregated.md`:

```markdown
# Chapter 7 Feedback Summary

## Leakage Check
[Result: PASS/FAIL]
[Issues if any]

## Reader Simulation
[Key findings]
[Critical flags]

## Tension Audit
[Actual vs. target]
[Major recommendations]

## Revision Priority
1. [Most critical issue]
2. [Second priority]
3. [Third priority]
```

---

## Phase 5: Revision

### Step 1: Address Critical Issues First

**Priority order:**
1. Information leakage (breaks suspense)
2. Under-revelation (reader confusion)
3. Tension misses (reader disengagement)
4. Pacing issues
5. Prose polish

### Step 2: Revise Draft

Create `drafts/ch07_draft_v2.md` with changes.

**Revision strategies:**

**For leakage:**
- Cut explicit statements
- Replace "telling" with "showing"
- Ambiguate language
- Remove narrator omniscience

**For under-revelation:**
- Add concrete details
- Show character reactions more clearly
- Clarify stakes

**For tension:**
- Tighten pacing (shorter sentences, faster beats)
- Or slow pacing (longer description, interiority)
- Strengthen chapter ending
- Add micro-tensions within scenes

### Step 3: Re-verify

```bash
python verification/leakage_checker.py 7 drafts/ch07_draft_v2.md
```

If clean, proceed.

If issues remain, revise again.

---

## Phase 6: Finalization

### Step 1: Final Quality Pass

- Prose polish
- Consistency check
- Typos, grammar
- Voice consistency with previous chapters

### Step 2: Update Reader State

Create/update `reader_state_ch07.md`:

```markdown
# Reader Knowledge State: After Chapter 7

## What Reader KNOWS (confirmed facts):
- [List]

## What Reader SUSPECTS (theories):
- [List with confidence levels]

## Active Questions Reader Is Holding:
1. [Most pressing question]
2. [Second question]
3. [Third question]

## Dramatic Irony Currently Active:
- Reader knows X, character doesn't

## Loops Opened This Chapter:
- [New questions raised]

## Loops Closed This Chapter:
- [Questions answered, if any]
```

**This becomes input for next chapter's planning.**

### Step 3: Archive

```bash
# Move final draft to published
mv drafts/ch07_draft_v2.md drafts/ch07_FINAL.md

# Archive beat sheet (don't change it after publication)
# This locks in what you intended, for later analysis
```

---

## Phase 7: Repeat for Next Chapter

### Planning Next Chapter

When planning Chapter 8, you have:
- Updated reader state (from ch 7)
- Remaining disclosure schedule (from story bible)
- Next tension target (from tension curve)
- Character knowledge changes (from ch 7's events)

**Key question:** "Given what reader knows now, what should they learn next?"

Not: "What happens next in the plot?"

But: "What information is revealed next, and how does that change reader understanding?"

---

## Common Pitfalls

### Pitfall 1: Changing Objective Reality Mid-Story

**Problem:** You decide in Chapter 10 that actually, Marcus didn't kill Elena, someone else did.

**Impact:** Invalidates all previous breadcrumbs, disclosure schedule, reader expectations.

**Solution:** Lock objective reality early. If you must change it, it's a full story bible revision and may require re-writing previous chapters.

---

### Pitfall 2: Ignoring Withheld List

**Problem:** "The beat sheet says to withhold X, but it felt natural for the character to think about it..."

**Impact:** Premature disclosure kills suspense.

**Solution:** Trust the architecture. If it feels "natural" to reveal it, that's the LLM's helpfulness bias. Fight it.

---

### Pitfall 3: Over-Planning Prose

**Problem:** Beat sheet specifies exact dialogue or prose.

**Impact:** Stifles natural flow, makes prose feel rigid.

**Solution:** Beat sheet should specify:
- Information state changes
- Emotional arc
- Function of scene

NOT exact words. Leave room for generative flow.

---

### Pitfall 4: Skipping Critics

**Problem:** "The draft feels good, I'll skip the reader simulation."

**Impact:** You can't see your own information leakage. You know the secrets, so you can't model a reader who doesn't.

**Solution:** Always run critics. They see what you can't.

---

### Pitfall 5: Not Updating Reader State

**Problem:** After Chapter 7, you forget to document what reader now knows.

**Impact:** Chapter 8 might repeat information or assume reader knows more/less than they do.

**Solution:** Treat `reader_state` as essential artifact. Update it religiously.

---

## Advanced Techniques

### Multi-POV Stories

For stories with multiple POV characters:

**In story_bible.yaml:**

```yaml
character_knowledge:
  sarah:  # Detective POV
    # ...
  marcus:  # Killer POV
    # ...
```

**In beat sheet:**

```yaml
pov:
  character: "sarah"  # This chapter's POV

narrative_constraints:
  - "Sarah doesn't know Marcus is the killer"
  - "Reader may know more than Sarah (dramatic irony)"
```

**Dramatic irony management:**
- Marcus's POV chapters can hint at guilt without stating it
- Sarah's POV chapters show her investigation from position of ignorance
- Reader pieces together truth faster than Sarah

---

### Non-Linear Narratives

For stories with flashbacks or non-chronological structure:

**In story_bible.yaml:**

Track TWO timelines:
- **Chronological (fabula):** When events actually happened
- **Narrative (syuzhet):** When reader learns about them

```yaml
objective_reality:
  - id: murder
    chronological_position: "Day 0 (three months before Ch 1)"
    revealed_in_chapter: 18
    narrative_position: "Late in story"
```

---

### Unreliable Narrators

**In story_bible.yaml:**

```yaml
character_knowledge:
  narrator:
    believes: ["List of narrator's beliefs"]
    believes_falsely: ["What narrator thinks but is wrong about"]
    truth: ["What actually happened"]

unreliable_narrator_reveal: 20  # When reader learns narrator was wrong
```

**Special constraint:**
- Narrator's POV reflects their false beliefs
- But plant subtle inconsistencies reader can catch
- When reveal happens (ch 20), reader should re-evaluate entire story

---

## Workflow Automation Ideas

### Makefile

```makefile
CHAPTER ?= 1

plan:
	cp chapter_plans/TEMPLATE_chapter_beats.yaml chapter_plans/ch$(CHAPTER)_beats.yaml
	echo "Edit chapter_plans/ch$(CHAPTER)_beats.yaml"

verify:
	python verification/leakage_checker.py $(CHAPTER) drafts/ch$(CHAPTER)_draft.md

critique:
	@echo "Run reader simulation and tension auditor via LLM"
	@echo "Save to feedback/ch$(CHAPTER)_*.md"

status:
	@echo "Story progress:"
	@ls chapter_plans/ch*.yaml | wc -l
	@echo "chapters planned"
	@ls drafts/ch*_FINAL.md | wc -l
	@echo "chapters completed"
```

Usage:
```bash
make plan CHAPTER=7
make verify CHAPTER=7
make status
```

---

## Quality Checklist

Before marking a chapter as FINAL:

- [ ] Leakage checker passes with no issues
- [ ] Reader simulation confirms target information state achieved
- [ ] Tension audit scores within 1 point of target
- [ ] Chapter ending creates pull to next chapter
- [ ] No forbidden phrases (realized, understood, felt sad)
- [ ] Show/tell ratio heavily favors show
- [ ] POV constraints respected
- [ ] Character knowledge states accurate
- [ ] Reader state document updated
- [ ] Prose polished

---

## Getting Unstuck

### "I don't know how to hint without revealing"

**Strategy: Use ambiguous behavior**
- Show character acting as if they know X
- Don't have them think "I know X"

Example:
- Don't: "Marcus knew he had to avoid Sarah's questions about the lighthouse."
- Do: "When Sarah mentioned the lighthouse, Marcus's coffee cup rattled against the saucer. 'Sorry,' he said. 'Didn't sleep well.'"

---

### "The scene feels too vague"

**Check:**
1. Is reader learning SOMETHING concrete this scene?
2. Are you withholding meaning, not facts?
3. Is the ambiguity strategic or accidental?

**Fix:**
- Make actions concrete and specific
- Make emotions clear through physical manifestation
- Make dialogue sharp
- Withhold interpretation, not events

---

### "How do I know if I've revealed too much?"

**Test:**
1. Run leakage checker (catches explicit leaks)
2. Run reader simulation (catches inferential leaks)
3. Ask: "If I were reading this for the first time, would I now be certain about [WITHHELD FACT]?"

If yes → Too much revealed
If reader would suspect but not confirm → Just right
If reader wouldn't even suspect when they should → Too vague

---

### "The tension feels flat but I hit the word count"

**Common causes:**
1. Pacing too even (no variation in sentence/paragraph length)
2. No micro-tensions within scene (everything flows smoothly)
3. Stakes unclear (reader doesn't know why to care)
4. Protagonist too passive (things happen TO them, not BY them)

**Fixes:**
1. Vary rhythm: fast dialogue, slow description, medium action
2. Add complications: plans don't work, new obstacles arise
3. Clarify stakes: show what character stands to lose
4. Give character agency: force them to make difficult choice

---

## Summary

The workflow is:

1. **Plan** (story bible + beat sheets) → Define information architecture
2. **Generate** (with constraints) → Write chapter following discipline rules
3. **Verify** (automated check) → Ensure no leakage
4. **Critique** (reader simulation + tension audit) → Check effectiveness
5. **Revise** (based on feedback) → Fix issues
6. **Finalize** (update reader state) → Lock it in
7. **Repeat** → Next chapter

**The key differentiator:** Information is planned explicitly, tracked carefully, and verified programmatically.

**The goal:** Suspenseful fiction that maintains mystery without confusion, and revelation without premature disclosure.
