# Syuzhet: Information Architecture for Fiction

> *Named after the Russian Formalist concept distinguishing **fabula** (chronological events) from **syuzhet** (how the story is told)*

A browser-based control panel for multi-agent fiction writing with enforced information discipline.

**[Live Demo](https://mmulqu.github.io/Syuzhet/)** · **[GitHub](https://github.com/mmulqu/Syuzhet)**

---

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

Syuzhet provides a **scaffolding system** to enforce information discipline when using LLMs for fiction writing.

---

## Quick Start

### 1. Open the App
Visit the [live demo](https://mmulqu.github.io/Syuzhet/) or host `index.html` yourself.

### 2. Add an API Key
Enter at least one API key on the welcome screen:
- **Anthropic** (Claude Opus/Sonnet/Haiku)
- **OpenAI** (GPT-5/o3/GPT-4.1)
- **Kimi/Moonshot** (Kimi K2 Turbo)

### 3. Create Your Story Bible
Go to the **Bible** tab and define:
- Objective reality (what's true)
- Disclosure schedule (when reader learns each fact)
- Character knowledge (who knows what)

### 4. Work with the Agents
Use the four specialized agents to plan, write, critique, and verify your chapters:

| Agent | Role | What They See |
|-------|------|---------------|
| **Architect** | Plans information economy | Everything |
| **Scribe** | Writes prose from beats | Story bible, beats, chapters |
| **Critic** | Models reader experience | **Only chapters** (reads blind) |
| **Keeper** | Verifies information discipline | Everything |

### 5. Iterate
Write chapters → Get critique → Revise → Verify → Repeat.

---

## Features

### Multi-Provider Support
Switch between AI providers on the fly:

| Provider | Models |
|----------|--------|
| **Anthropic** | Claude Opus 4.5, Sonnet 4.5, Haiku 4.5 |
| **OpenAI** | GPT-5.2, o3, GPT-4.1, GPT-5 Mini |
| **Moonshot** | Kimi K2 Turbo |

### Theme Modes
Three visual themes for different writing contexts:

| Theme | Description |
|-------|-------------|
| 🌙 **Dark** | Easy on the eyes for late-night sessions |
| ☀️ **Light** | Clean and bright |
| 📜 **Paper** | Warm sepia with serif fonts—like Scrivener |

### Context Isolation
**The Critic cannot see the story bible.** This is by design.

The Critic models what an actual reader experiences—they only know what's on the page. If the Critic can figure out your twist early, so can your readers.

### Persistent Storage
All data stored in browser localStorage:
- `syuzhet_api_keys` — Your API keys (per provider)
- `syuzhet_selected_model` — Currently selected model
- `syuzhet_theme` — Your theme preference
- `syuzhet_chats` — All conversation history
- `syuzhet_story_bible` — Story bible YAML
- `syuzhet_tension_curve` — Tension curve YAML  
- `syuzhet_chapters` — Chapter beats, drafts, feedback

**Export/Import**: Use Settings → Export Project Data to download a JSON backup.

---

## Core Concepts

### The Two Layers LLMs Conflate

| Layer | Description |
|-------|-------------|
| **Plot** | What happens (events, actions, consequences) |
| **Information Disclosure** | What the reader learns, when, and how |

**These are separate authorial decisions.**

- A murder can happen in Chapter 1, but the reader might not learn who did it until Chapter 20
- Or the reader might know from page 1 while watching characters fumble toward truth (dramatic irony)

**Most LLM prompts treat these as one thing. They're not.**

### The Four Information States

At any moment in a story, there are four distinct information layers:

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

## The Four Agents

### ◈ Architect — Designer of Information Economy

**Sees:** Everything  
**Creates:** Story bible, disclosure schedules, tension curves, beat sheets

The Architect plans *what information exists* and *when readers learn it*. They design the information economy before any prose is written.

**Use the Architect to:**
- Extract objective reality from your outline/draft
- Plan disclosure arcs for each secret
- Create beat sheets with explicit WITHHELD tags
- Design tension curves across chapters

### ✦ Scribe — Weaver of Prose

**Sees:** Story bible, beats, feedback, chapters  
**Creates:** Chapter prose, revisions

The Scribe writes prose from beat sheets. They know the full story but are constrained by what each beat allows them to reveal.

**Key rules the Scribe follows:**
1. NEVER reveal anything marked WITHHELD in the beat sheet
2. NEVER have characters explain motivations unless the beat specifies
3. End scenes on questions, not answers
4. Show behavior AS IF character knows secrets, without stating them

### ◇ Critic — Reader's Advocate

**Sees:** Only chapters (NO story bible access)  
**Creates:** Reader state analysis, tension scores, craft notes

The Critic models what a first-time reader experiences. They read blind—just like your audience will.

**The Critic evaluates through three lenses:**

1. **Reader Simulation**
   - What does the reader NOW believe to be true?
   - What do they SUSPECT but not know?
   - What questions are they actively holding?
   - Where was curiosity killed by over-explanation?

2. **Tension Assessment**
   - Does this chapter hit its target tension?
   - Where are stakes deflated unnecessarily?
   - Are there micro-tensions within quiet scenes?

3. **Craft Critique**
   - Clichés and weak phrases
   - Telling instead of showing
   - Overwriting
   - Strengths to preserve

### ◆ Keeper — Guardian of Secrets

**Sees:** Everything  
**Creates:** Pass/fail verification, leakage reports

The Keeper is the final gate. Nothing ships without their clearance.

**The Keeper checks:**
1. **Information Discipline** — Is any fact revealed before its scheduled chapter?
2. **Revision Integrity** — Did the Scribe honor preserve markers? Any new leakage?

The Keeper does NOT suggest fixes—only pass/fail with reasons.

---

## Story Bible Format

Use YAML in the **Bible** tab. Here's the structure:

```yaml
# ============================================
# OBJECTIVE REALITY
# Everything that is TRUE in the story world
# ============================================
objective_reality:
  - id: killer_identity
    fact: "Marcus Webb killed Elena Reeves"
    when_happened: "Three months before story opens"
    method: "Pushed her from lighthouse observation deck"
    motive_true: "Elena discovered Marcus embezzled $2M"

  - id: sibling_secret
    fact: "Marcus and Elena are half-siblings"
    when_happened: "Always true, discovered age 15"
    known_by: [marcus]

# ============================================
# DISCLOSURE SCHEDULE
# When reader learns/suspects each fact
# ============================================
disclosure_schedule:
  - fact_id: killer_identity
    hinted_at: [3, 7, 11]           # Breadcrumbs
    reader_suspects: 12              # Should start suspecting
    reader_fairly_certain: 16        # Building conviction
    confirmed: 18                    # Explicit reveal
    confirmation_method: "Witness testimony"

  - fact_id: sibling_secret
    hinted_at: [7]                   # "Same gray-green eyes"
    confirmed: 17
    confirmation_method: "Old photograph with inscription"

# ============================================
# CHARACTER KNOWLEDGE
# What each character knows/believes
# ============================================
character_knowledge:
  marcus:
    knows:
      - "He killed Elena"
      - "They are half-siblings"
      - "He forged the suicide note"
    believes_falsely:
      - "No one saw him that night"
    arc:
      - chapter: 15
        learns: "Investigation focusing on him"
        
  sarah:
    knows:
      - "Elena's death was ruled suicide"
    suspects:
      - "Something doesn't add up"
    arc:
      - chapter: 8
        learns: "Marcus was at lighthouse that night"

# ============================================
# WITHHELD RULES
# Explicit constraints
# ============================================
withheld_until_scheduled:
  - fact: "Marcus killed Elena"
    forbidden_before_ch_18:
      - "Character stating it directly"
      - "Narrator confirming it"
      - "Undeniable physical proof"
    allowed_before:
      - "Suspicious behavior"
      - "Guilty body language"  
      - "Dramatic irony via Marcus POV"
      - "Other characters suspecting"
```

---

## Tension Curve Format

Define target tension levels (1-10) in the **Bible** tab under Tension Curve:

```yaml
# Tension Scale:
# 1-3: Low (setup, breathing room, character moments)
# 4-6: Medium (investigation, complications, rising action)
# 7-8: High (revelations, confrontations, turning points)
# 9-10: Peak (climax, life-or-death, major reveals)

chapters:
  1:
    target: 4
    type: "Hook, establish normal world"
    end_on: "First hint something is wrong"

  2:
    target: 3
    type: "Deepen character, plant seeds"
    end_on: "Quiet unease"
    
  3:
    target: 5
    type: "First complication"
    end_on: "Question that demands answer"

  7:
    target: 6
    type: "Ominous behavior, psychological unease"  
    micro_tensions:
      - "Why is Marcus burning the photograph?"
      - "What will happen if Sarah discovers it?"
    end_on: "Image - photo disappears into ash"

  12:
    target: 7
    type: "Reader should suspect Marcus"
    end_on: "Evidence pointing at Marcus"

  18:
    target: 9
    type: "Killer revealed"
    end_on: "Confirmation + new danger"
```

---

## Beat Sheet Format

Create beat sheets for each chapter in the **Chapters** tab:

```yaml
chapter: 7
title: "The Burning"
pov: "Marcus (close third)"
target_tension: 6

# ============================================
# INFORMATION STATE FOR THIS CHAPTER
# ============================================
information_state:
  reader_learns:
    - "Marcus has childhood photograph with Elena"
    - "He destroys it in secret"
    
  reader_suspects:
    - "Marcus is hiding something about their relationship"
    - "He may have been involved in Elena's death"
    
  withheld:  # CRITICAL - Scribe must not reveal these
    - "That they're siblings (scheduled ch 17)"
    - "That Marcus killed Elena (scheduled ch 18)"
    - "Any explicit guilty thoughts"

# ============================================
# BEATS
# ============================================
beats:
  - beat: 1
    description: "Marcus retrieves hidden box from closet, 3 AM"
    information_function:
      reveals: "Marcus has kept something secret"
      withholds: "What else is in the box"
      hints_at: "He's been protecting this secret for years"
    pacing: "Slow, building tension"
    
  - beat: 2
    description: "Opens box, finds old photograph"
    information_function:
      reveals: "Photo shows two children with similar features"
      withholds: "Their relationship"
      hints_at: "Same gray-green eyes, same half-smile"
    end_beat_on: "The photograph - holding, not explaining"
    
  - beat: 3
    description: "Burns the photograph in kitchen sink"
    information_function:
      reveals: "Marcus needs to destroy this evidence"
      withholds: "Why this matters"
    execution_notes:
      - "Physical details: match flare, edges curl black"
      - "No internal monologue about guilt"
      - "Just the action and its weight"
    end_beat_on: "Image - children disappear into ash"

chapter_ending:
  type: "Ominous image"
  pull_forward: "What is Marcus hiding? What else was in that box?"
```

---

## Workflow

### Phase 1: Planning (Architect)

1. **Define objective reality** — What's actually true in your story?
2. **Create disclosure schedule** — When does the reader learn each fact?
3. **Map character knowledge** — Who knows what? Who's wrong about what?
4. **Set tension curve** — Target tension for each chapter
5. **Write beat sheets** — Plan each chapter with explicit WITHHELD tags

### Phase 2: Writing (Scribe)

1. **Review beat sheet** — Understand what's allowed and forbidden
2. **Write prose** — Follow the beats, honor the constraints
3. **Focus on craft** — Show don't tell, behavior over explanation

### Phase 3: Critique (Critic)

1. **Reader simulation** — What does the reader know/suspect now?
2. **Tension assessment** — Did we hit the target? Where did it sag?
3. **Craft notes** — What's working? What needs revision?

### Phase 4: Revision (Scribe)

1. **Apply feedback** — In priority order
2. **Preserve strengths** — Don't lose what's working
3. **Fix leakage** — Remove premature revelations

### Phase 5: Verification (Keeper)

1. **Information audit** — Any facts revealed too early?
2. **Revision check** — Were preserve markers honored?
3. **Pass/fail** — If fail, back to Scribe with specific flags

---

## Example: Information Discipline in Action

### Chapter 7 Setup
- **Target tension:** 6/10 (medium-high, ominous)
- **POV:** Marcus (knows he killed Elena, reader doesn't)
- **Plot:** Marcus burns childhood photograph
- **Goals:** Reader suspects hiding something, does NOT learn he's killer or sibling

### ✓ What Works (Information Discipline)

```markdown
Marcus's hands shook as he turned on the kitchen faucet. The 
match flared in the dark.

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

### ✗ What Would Break It (Leakage)

```markdown
Marcus burned the photo of him and his half-sister Elena. 
If Sarah found it, she'd know they were related, which would 
expose his embezzlement motive and prove he'd killed her.
```

**Why this fails:**
- States sibling connection (withheld until ch 17)
- States he killed her (withheld until ch 18)
- Explains motivation (over-clarification)
- No mystery, no suspense
- Reader knows everything, nothing left to discover

---

## Self-Hosting

### GitHub Pages (Recommended)

```bash
# Clone or fork the repo
git clone https://github.com/mmulqu/Syuzhet.git
cd Syuzhet

# The index.html is standalone - just deploy it
# GitHub Pages: Settings → Pages → Deploy from root
```

### Local Development

```bash
# Just open the file - no build step required
open index.html

# Or use any static server
python -m http.server 8000
npx serve .
```

### Customization

**Add models** — Edit the `MODELS` object:
```javascript
'new-model-id': { provider: 'openai', name: 'Display Name', tier: 'balanced' }
```

**Add providers** — Add to `PROVIDERS` and create a `callNewProvider()` function following existing patterns.

**Adjust themes** — Modify CSS variables in the `:root`, `[data-theme="light"]`, and `[data-theme="sepia"]` blocks.

---

## Technical Notes

### API Usage

The app calls APIs directly from your browser:
- **Anthropic**: Uses `anthropic-dangerous-direct-browser-access` header
- **OpenAI/Moonshot**: Standard CORS-enabled endpoints
- **Max tokens**: 64000 (you only pay for actual generation)

### Privacy

- API keys stored only in your browser's localStorage
- Keys sent only to their respective API endpoints
- No backend, no analytics, no tracking
- Each visitor's data is completely isolated

### Context Injection

Each agent receives different context:

```javascript
// Architect, Scribe, Keeper: Full context
if (agent.contextAccess.includes('story_bible')) {
  context += storyBible;
}

// Critic: NO story bible - reads blind like a real reader
// Only sees: chapters
```

---

## Genre Applications

While examples use mystery/thriller, this architecture applies to any genre where information control matters:

| Genre | Core Mechanic | Key Technique |
|-------|---------------|---------------|
| **Mystery** | Withhold whodunit until climax | Plant clues without confirming |
| **Thriller** | Withhold extent of danger | Reveal threat incrementally |
| **Romance** | Withhold whether couple gets together | Show desire while maintaining facades |
| **Horror** | Withhold nature of threat | Wrongfoot reader expectations |
| **Literary** | Withhold character's true nature | Unreliable narration, gradual backstory |

---

## Theoretical Foundation

### Fiction is Information Warfare

The author controls:
1. **What** the reader knows
2. **When** they learn it
3. **How** they learn it (directly/indirectly, reliably/unreliably)

**Suspense = uncertainty about important outcome**

- Reader knows too much too soon → No suspense
- Reader knows too little → Confusion, detachment
- Sweet spot: **Reader suspects but can't confirm**

### The LLM Alignment Problem for Fiction

LLMs are aligned for helpfulness, clarity, completeness, directness.

Fiction requires strategic withholding, ambiguity, incompleteness, indirection.

**Syuzhet re-aligns LLMs through:**
1. **Explicit constraints** (withheld lists in beat sheets)
2. **Architectural separation** (plot ≠ disclosure)
3. **Blind criticism** (Critic can't see story bible)
4. **Multi-agent specialization** (each agent has one job)

### Influences

- **Russian Formalists** (Shklovsky, Propp): Fabula vs. Syuzhet
- **Narratology** (Genette): Story vs. Discourse  
- **Cognitive narratology** (Herman): Reader mental models
- **Information theory** (Shannon): Uncertainty and entropy

---

## Roadmap

### Current (v1)
- [x] Four-agent architecture with context isolation
- [x] Multi-provider API support (Anthropic, OpenAI, Moonshot)
- [x] Story Bible and Tension Curve editors
- [x] Chapter management (beats, drafts, feedback)
- [x] Theme system (dark, light, paper)
- [x] Persistent localStorage
- [x] Export/import project data

### Planned
- [ ] Chapter summaries for scaling (avoid dumping all chapters into context)
- [ ] Automated leakage detection (regex + LLM-based)
- [ ] Tension curve visualization
- [ ] Import existing manuscript for "archaeological mode"
- [ ] Multi-project support
- [ ] Collaborative editing (CRDTs)

---

## Contributing

This system is a proof-of-concept. Ways to contribute:

1. **Add example stories** — Different genres, structures, traditions
2. **Improve the UI** — Better chapter navigation, visualization
3. **Build verification tools** — Automated leakage detection
4. **Research extensions** — Empirical testing with readers, cross-genre analysis

---

## License

MIT License

---

*"The art of storytelling is not just about what you tell, but what you withhold—and when you finally reveal it."*
