# Quick Start Guide

Get started with the Syuzhet information architecture system in 5 steps.

---

## Step 1: Understand the Core Concept (2 minutes)

**The problem:** LLMs naturally over-explain and resolve ambiguity, killing suspense.

**The solution:** Separate **plot** (what happens) from **information disclosure** (what reader learns when).

**Key insight:** Just because something happened doesn't mean the reader should know about it yet.

---

## Step 2: Define Your Story's Secrets (30 minutes)

Open `story_bible.yaml` and fill in:

### A. Objective Reality

What is actually TRUE in your story world?

```yaml
objective_reality:
  - id: central_secret
    fact: "The truth of your central mystery"
    details: "Supporting information"
```

Example:
```yaml
  - id: killer_identity
    fact: "Marcus Webb killed Elena Reeves"
    method: "Pushed her from lighthouse"
    motive: "She discovered his embezzlement"
```

### B. Disclosure Schedule

WHEN should reader learn each secret?

```yaml
disclosure_schedule:
  - fact_id: central_secret
    reader_should_suspect: 12      # Chapter where reader starts suspecting
    confirmed_to_reader: 18         # Chapter where it's confirmed
```

**This is your contract with the reader.** Don't break it.

---

## Step 3: Plan One Chapter (15 minutes)

Copy the template:
```bash
cp chapter_plans/TEMPLATE_chapter_beats.yaml chapter_plans/ch01_beats.yaml
```

Fill in three critical sections:

### A. Information State
```yaml
information_state:
  reader_learns:
    - "One concrete fact reader learns"

  reader_suspects:
    - "One thing reader should start suspecting"

  withheld:
    - "THE THING YOU MUST NOT REVEAL YET"
```

### B. Beats (3-5 scenes)
```yaml
beats:
  - beat_number: 1
    description: "What happens in this scene"

    information_function:
      reveals: "What reader learns"
      withholds: "What reader doesn't learn"
```

### C. Chapter Ending
```yaml
closing:
  type: "Question"  # or Revelation, Cliffhanger, Decision
  example_last_line: "End on a hook that pulls to next chapter"
```

---

## Step 4: Generate with Discipline (20 minutes)

### A. Use the Generator Prompt

System prompt for your LLM:
```
[Paste entire contents of prompts/chapter_generator.md]
```

User prompt:
```
Write Chapter 1 of my story.

STORY BIBLE (relevant excerpt):
[Copy the facts relevant to Chapter 1 from story_bible.yaml]

BEAT SHEET:
[Paste contents of chapter_plans/ch01_beats.yaml]

CRITICAL: Follow all information discipline rules. DO NOT reveal
anything in the "withheld" list.
```

### B. Save the output

Save to `drafts/ch01_draft.md`

---

## Step 5: Verify (10 minutes)

### A. Run the Leakage Checker

```bash
python verification/leakage_checker.py 1 drafts/ch01_draft.md
```

**If it says "NO LEAKAGE DETECTED":** ✓ You're good!

**If it flags issues:** Revise the draft to remove premature disclosures.

### B. Quick Manual Check

Ask yourself:
1. ✓ Did I show what happened without over-explaining WHY?
2. ✓ Does the chapter end on a question, not an answer?
3. ✓ Are the items in my "withheld" list still mysterious?

If yes to all three → You've successfully maintained information discipline!

---

## Next Steps

**To continue your story:**

1. Update reader state (what they know now)
2. Plan Chapter 2 based on Chapter 1's ending
3. Check disclosure schedule for what to reveal next
4. Repeat the process

**To go deeper:**

- Read `WORKFLOW.md` for the complete process
- Read `README.md` for the full theoretical framework
- Try the advanced critics (reader simulation, tension auditor)

---

## Common First-Time Mistakes

### Mistake 1: "I explained the character's motivation"

❌ "Sarah was investigating because she felt guilty about not protecting Elena."

✓ "Sarah pulled the case file closer. If she could just find one thing..."

**Fix: Show behavior, not motivation.**

---

### Mistake 2: "I confirmed the secret too early"

❌ "Marcus remembered killing Elena three months ago."

✓ "Marcus avoided looking at the lighthouse. His hands were shaking."

**Fix: Show effects of secret, not the secret itself.**

---

### Mistake 3: "I closed the loop at the end of the chapter"

❌ "Sarah realized the suicide note was forged. She felt satisfied with her progress."

✓ "Sarah stared at the note. The handwriting was too perfect. Almost like—
Her phone buzzed. Marcus's name on the screen."

**Fix: End on questions, not answers.**

---

## The Golden Rule

**When in doubt, withhold.**

You can always add clarity in revision.

You can never un-spoil a mystery.

---

## Success Metrics

You know it's working when:

1. ✓ Leakage checker passes
2. ✓ You're showing behavior instead of explaining it
3. ✓ Reader would want to turn the page
4. ✓ The central mystery is still mysterious
5. ✓ You're building suspicion without confirming it

---

## Get Help

**Stuck? Check:**
- `WORKFLOW.md` Section: "Getting Unstuck"
- `prompts/chapter_generator.md` Section: "Forbidden Phrases"
- `README.md` Section: "Show Don't Tell Techniques"

**Still stuck?** Open an issue describing:
1. What you're trying to withhold
2. What's being revealed instead
3. The passage that's causing trouble

---

## One-Minute Summary

1. **Define** what's true (story bible)
2. **Schedule** when reader learns it (disclosure schedule)
3. **Plan** chapter beats with withheld list
4. **Generate** with information discipline rules
5. **Verify** with leakage checker

**Remember:** Plot ≠ Disclosure. Control information, control suspense.

---

**Now go write something suspenseful!**
