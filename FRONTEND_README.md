# Syuzhet — Fiction Control Panel

A browser-based control panel for the **Syuzhet** multi-agent fiction writing system. Manages four specialized agents (Architect, Scribe, Critic, Keeper) with proper context isolation and persistent chat history.

---

## Features

### Four Agent System with Proper Context Isolation

- **Architect** — Designs information economy (sees everything)
  - Story bible, tension curve, chapters, beats
  - Creates disclosure schedules
  - Plans information architecture

- **Scribe** — Writes prose from beats (sees bible + beats + feedback)
  - Follows beat sheets with withheld constraints
  - Applies Critic feedback
  - Protects preserved spans

- **Critic** — Evaluates drafts (reads blind — NO story bible access)
  - Reader simulation (models naive first-time reader)
  - Tension assessment
  - Craft critique
  - **Critical:** Does NOT see the story bible to prevent knowledge contamination

- **Keeper** — Verifies information discipline (sees everything)
  - Checks disclosure schedule compliance
  - Verifies revision integrity
  - Pass/fail verdict

### Additional Features

- **Persistent Storage**: All chats, story bible, chapters stored in localStorage
- **Multiple Conversations**: Create multiple chat sessions per agent
- **Story Bible Editor**: YAML editor for objective reality and disclosure schedules
- **Chapter Manager**: Organize beats, drafts, and feedback per chapter
- **Tension Visualization**: See tension scores across chapters

---

## Quick Start

### Option 1: Run Locally

1. Download `index.html` from this repository
2. Open in any modern browser (Chrome, Firefox, Safari, Edge)
3. Enter your Anthropic API key
4. Start writing

**No installation required.** Everything runs in the browser.

### Option 2: Deploy to GitHub Pages

1. Fork this repository or create a new repo
2. Add `index.html` to the root directory
3. Go to Settings → Pages
4. Set Source to "Deploy from a branch" → `main` / `root`
5. Access at `https://yourusername.github.io/repo-name`

### Option 3: Deploy to Any Static Host

Upload `index.html` to:
- **Netlify** (drag & drop)
- **Vercel**
- **Cloudflare Pages**
- **Any web server**

The file is completely self-contained with no dependencies.

---

## Usage Guide

### 1. Set Up Story Bible

Navigate to **Bible** tab and define your story's information architecture:

```yaml
# story_bible.yaml

objective_reality:
  - fact: "Marcus killed Elena"
    when: "3 months before story"
    method: "Pushed from lighthouse"
    motive: "Elena discovered his embezzlement"

disclosure_schedule:
  - fact_id: killer_identity
    hinted_at: [3, 7]
    suspected_by_reader: 12
    confirmed: 18

character_knowledge:
  marcus:
    knows: ["he killed Elena"]
    believes_falsely: ["no witnesses"]
```

**What this does:**
- Defines what's objectively true in your story world
- Schedules when reader learns each fact
- Maps what each character knows/believes

### 2. Create Tension Curve

Still in the **Bible** tab, switch to Tension Curve:

```yaml
# tension_curve.yaml

chapters:
  1:
    target: 4
    type: "hook, establish normal"
  2:
    target: 3
    type: "deepen character"
  3:
    target: 5
    type: "first complication"
```

**What this does:**
- Sets target tension levels (1-10) per chapter
- Critic will score drafts against these targets

### 3. Create Chapter Beat Sheets

In **Chapters** tab, add chapters and define beats:

```yaml
chapter: 7
target_tension: 6

beats:
  - number: 1
    description: "Marcus retrieves hidden box"
    withheld: ["box contents", "why he's hiding it"]
    reader_learns: ["Marcus has secrets"]

  - number: 2
    description: "Marcus looks at photograph"
    withheld: ["photo shows sibling connection"]
    reader_learns: ["Photo is important to him"]
```

**What this does:**
- Defines what happens in each scene (plot)
- Explicitly lists what must be WITHHELD (information discipline)
- Specifies what reader should learn

### 4. Work with Agents

**Typical workflow:**

1. **Architect** (once per project):
   - Bootstrap story bible from your outline/draft
   - "Here's my story outline. Please create a story bible."

2. **Architect** (per chapter):
   - Create beat sheet for next chapter
   - "Create beat sheet for Chapter 7 where Marcus burns the photo."

3. **Scribe** (draft):
   - Write chapter from beat sheet
   - "Write Chapter 7 from the beat sheet."
   - Scribe sees: story bible + beat sheet + tension target

4. **Critic** (evaluate):
   - Evaluate draft (doesn't see story bible!)
   - "Evaluate this Chapter 7 draft."
   - Critic sees: ONLY previous chapters + current draft
   - Produces JSON feedback with issues and preserved spans

5. **Scribe** (revise):
   - Revise based on feedback
   - "Revise Chapter 7 based on this feedback."
   - Must protect preserved spans verbatim

6. **Keeper** (verify):
   - Verify no information leakage
   - "Verify this Chapter 7 revision."
   - Keeper sees: story bible + disclosure schedule + draft
   - Produces pass/fail verdict

7. **Repeat** until Keeper passes, then move to next chapter

---

## Context Isolation: The Key Feature

### What Makes This System Work

**The Critic reads blind.**

When you chat with the Critic, it only sees:
- ✓ Previous chapter drafts
- ✓ Current chapter draft being evaluated
- ✗ Story bible
- ✗ Disclosure schedule
- ✗ What's supposed to be withheld

**Why this matters:**

The Critic models an actual reader's experience. It evaluates:
- "What does the reader know right now?"
- "What do they suspect?"
- "Is this too obvious or too vague?"

Without seeing the story bible, the Critic can't be biased by "knowing what's coming."

### Context by Agent

| Agent | Story Bible | Tension Curve | Chapters | Beat Sheets |
|-------|-------------|---------------|----------|-------------|
| **Architect** | ✓ Creates it | ✓ Creates it | ✓ | ✓ Creates them |
| **Scribe** | ✓ For consistency | ✓ For target | ✓ Previous ones | ✓ Current one |
| **Critic** | ✗ **Blind** | ✗ | ✓ Only drafts | ✗ |
| **Keeper** | ✓ For verification | ✓ | ✓ | ✓ |

---

## API Usage

### How It Works

The app calls the Anthropic API directly from your browser:

- **Model**: `claude-sonnet-4-20250514`
- **Max tokens**: 8192
- **Your API key**: Stored only in localStorage (never sent anywhere except Anthropic)

### CORS Note

The app uses `anthropic-dangerous-direct-browser-access` header. This is officially allowed by Anthropic for client-side applications.

### Cost

Typical costs per chapter:
- **Architect** (beat sheet): ~$0.05-0.10
- **Scribe** (draft): ~$0.20-0.40
- **Critic** (evaluation): ~$0.15-0.25
- **Keeper** (verification): ~$0.05-0.10

**Total per chapter:** ~$0.50-1.00 depending on chapter length and complexity.

---

## Data Storage

### What's Stored

All data stored in browser localStorage:
- `syuzhet_api_key` — Your API key
- `syuzhet_chats` — All conversation history
- `syuzhet_story_bible` — Story bible YAML
- `syuzhet_tension_curve` — Tension curve YAML
- `syuzhet_chapters` — Chapter beats, drafts, feedback

### Export Your Data

**To export:**
1. Open browser DevTools (F12)
2. Go to Application → Local Storage
3. Find `syuzhet_*` entries
4. Copy values

**To import:**
1. Paste values into localStorage in new browser
2. Refresh the page

### Reset

- **Clear all data**: Use "Disconnect API" button
- **Clear specific chats**: Delete individual conversations
- **Clear browser localStorage**: Use browser settings

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│              Syuzhet Control Panel               │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌───┐ │
│  │Architect│  │ Scribe  │  │ Critic  │  │...│ │
│  │  Chat   │  │  Chat   │  │  Chat   │  │   │ │
│  └────┬────┘  └────┬────┘  └────┬────┘  └───┘ │
│       │            │            │              │
│       ▼            ▼            ▼              │
│  ┌─────────────────────────────────────────┐  │
│  │      Context Injection Layer            │  │
│  │  • Architect: bible + curve + chapters  │  │
│  │  • Scribe: bible + beats + feedback     │  │
│  │  • Critic: chapters ONLY (blind)        │  │
│  │  • Keeper: everything                   │  │
│  └─────────────────────────────────────────┘  │
│                    │                           │
│                    ▼                           │
│          Anthropic API Call                    │
└─────────────────────────────────────────────────┘
```

---

## Customization

### Change Model

Find this line in the HTML and change the model:

```javascript
model: 'claude-sonnet-4-20250514',
```

Available models:
- `claude-sonnet-4-20250514` (recommended)
- `claude-opus-4-20250514` (more powerful, higher cost)
- `claude-haiku-3-5-20250219` (faster, lower cost)

### Modify Agent Prompts

Edit the `AGENTS` object at the top of the script:

```javascript
const AGENTS = {
  architect: {
    id: 'architect',
    name: 'Architect',
    systemPrompt: `Your custom prompt here...`,
    // ...
  },
  // ...
}
```

### Add New Agents

Add to the `AGENTS` object:

```javascript
newagent: {
  id: 'newagent',
  name: 'New Agent',
  subtitle: 'Description',
  color: 'blue',  // gold, emerald, rose, violet
  icon: '◎',
  contextAccess: ['story_bible', 'chapters'],  // what it can see
  systemPrompt: `Your prompt here...`
}
```

### Customize Colors/Fonts

Edit the Tailwind config at the top of the HTML:

```javascript
tailwind.config = {
  theme: {
    extend: {
      colors: {
        // Add or modify colors
        'custom': '#yourcolor',
      }
    }
  }
}
```

---

## Integration with Syuzhet Repository

This control panel is designed to work alongside the [Syuzhet](https://github.com/mmulqu/Syuzhet) repository:

### Workflow Integration

1. **Use the panel** for interactive agent work and experimentation
2. **Copy finalized artifacts** to the repository:
   - `story_bible.yaml` → Copy to repo root
   - `tension_curve.yaml` → Copy to `artifacts/`
   - Beat sheets → Copy to `chapters/chXX/beats.yaml`
   - Final drafts → Copy to `chapters/chXX/draft.md`
3. **Run automated checks** from the repository:
   - `python verification/leakage_checker.py 7 chapters/ch07/draft.md`
4. **Commit approved chapters** to git

### Benefits of This Workflow

- **Panel**: Interactive, fast iteration, visual feedback
- **Repository**: Version control, automated verification, documentation
- **Best of both**: Experiment in panel, formalize in repo

---

## Limitations

Current limitations (may be addressed in future versions):

- **No file upload**: Copy/paste content instead of uploading files
- **No automated orchestration**: Manual agent switching required
- **LocalStorage only**: No cloud sync between devices
- **Single project at a time**: Can't switch between multiple stories
- **No export/import**: Manual copy from DevTools localStorage

---

## Troubleshooting

### API Key Issues

**Problem**: "API error: 401"
- **Solution**: Check your API key is correct
- Get key from: https://console.anthropic.com/

**Problem**: "API error: 429"
- **Solution**: Rate limit reached, wait a minute and retry

### Context Not Loading

**Problem**: Agent doesn't seem to see story bible
- **Solution**: Check agent's context access (see table above)
- Critic deliberately does NOT see story bible (by design)

### Tension Visualization Not Showing

**Problem**: Bars are empty in tension viz
- **Solution**: Critic feedback must include tension score in JSON format:
  ```json
  {
    "tension": {
      "actual": 7
    }
  }
  ```

### Chat History Lost

**Problem**: Refreshing page clears conversations
- **Solution**: Check browser localStorage isn't being cleared automatically
- Ensure you're not in incognito/private mode

---

## Future Enhancements

Potential features for future versions:

- [ ] Export/import project as JSON file
- [ ] Multiple project support with project switcher
- [ ] GitHub integration (commit directly from panel)
- [ ] Automated orchestration (run full chapter loop)
- [ ] WebSocket for real-time collaboration
- [ ] Cloud sync with account system
- [ ] Diff view for revision comparison
- [ ] Timeline view of disclosure schedule
- [ ] Visual story bible editor (graph-based)

---

## Browser Compatibility

**Tested and working:**
- ✓ Chrome/Edge 90+
- ✓ Firefox 88+
- ✓ Safari 14+

**Requirements:**
- JavaScript enabled
- localStorage enabled
- Modern CSS support (grid, flexbox)

---

## Security & Privacy

### API Key Security

- API key stored in browser localStorage only
- Never sent to any server except Anthropic's API
- Not logged or tracked
- Use "Disconnect API" to remove from storage

### Data Privacy

- All data stays in your browser
- No analytics or tracking
- No external dependencies except:
  - React (CDN)
  - Tailwind CSS (CDN)
  - Google Fonts (CDN)
  - Anthropic API (for Claude)

### Recommendations

- Don't use on shared/public computers
- Clear localStorage when done if using public machine
- Keep backups of important story bibles

---

## License

MIT License — Use freely for your fiction projects.

---

## Support & Contribution

**Found a bug?** Open an issue on GitHub.

**Have a feature request?** Open an issue describing your use case.

**Want to contribute?** Fork the repo and submit a PR.

---

*"The art of storytelling is not just about what you tell, but what you withhold—and when you finally reveal it."*
