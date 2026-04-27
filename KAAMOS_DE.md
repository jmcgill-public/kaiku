# KaamOS Desktop Environment
## Agent Context and Project Brief

*For any agent working on this project: read this first.*

---

## What this is

KaamOS is simultaneously:

1. **The Hollywood OS** of the Kaamos cinematic universe — the diegetic
   computer environment that stationhands use on the Expanse. When a
   character opens a terminal in this world, this is what they see.

2. **A real desktop environment** the author actually wants to use. Not a
   mockup. Not a screenshot for a repo. Something that boots and works.

3. **A portfolio piece.** The author is a developer. This is the kind of
   project that shows taste, range, and follow-through.

4. **A personal itch.** The author has nostalgia for the 6809/OS-9 era and
   a strong opinion about what a terminal-first Linux desktop should feel like
   in 2026. This is that opinion made real.

These four goals are not in conflict. The Hollywood prop constraint is the
design brief. The real usability requirement is the test of whether the brief
was worth following.

---

## Scope — where to start

**Minimum viable KaamOS:** A WindowMaker theme.

WindowMaker is the right starting point:
- Still maintained and installable in 2026
- Based on NeXTSTEP — clean, dock-based, minimal chrome
- Highly themeable: colors, fonts, textures, icons, dock appearance
- The aesthetic is already closer to KaamOS than any other WM
- The author can actually use it day-to-day

A WindowMaker theme that looks like KaamOS is a complete, shippable artifact.
Everything beyond that is additive.

**Extended scope (additive, not required):**
- GTK 3/4 theme for applications that run inside the environment
- Custom icon set (runic/hex-grid aesthetic, see Design Language below)
- Custom panel or dock configuration
- Terminal color scheme and font stack (the most important thing)
- A dotfiles repo that bootstraps the whole environment

---

## Design Language

### Palette
The KaamOS palette derives from phosphor terminal aesthetics and the
novel's Finnish/Nordic color register.

Primary: **amber** (#C8A050) on deep void black (#070711)
Accent: **void blue** (#3030A0) and **hehku** (#C85020 — the heat from within)
Success/active: **station green** (#40C080)
Warning/boss: **hiljaisuus violet** (#8030C0)
Inactive/dim: (#2A2A5A)

These are already in mvp.html. The desktop should feel like the game's map.

### Typography
- **Terminal font:** A monospace with good Unicode coverage and Finnish
  character support. Iosevka or Fira Code are candidates. The font renders
  the actual Finnish characters in kaamos.asm and the suomi directory.
- **UI font:** Something that reads as designed-for-a-purpose, not chosen
  from a default list. System-ui fallback is acceptable.
- No rounded corners. The grid has edges.

### Shape language
- Hexagonal motifs where decorative elements appear (dock separators,
  wallpaper, loading screens)
- The hex grid from mvp.html is the visual vocabulary
- Icons: angular, rune-adjacent, readable at small sizes
- No gradients. Flat color, sharp edges, intentional.

### Motion
- None, or nearly none. The terminal doesn't animate.
  If something moves, it is because it is communicating information.
- The one exception: the Hiljaisuus pulse. A subtle slow pulse on the
  clock or status indicator, in void-violet, at the rate used in mvp.html.
  The Silence is always there.

---

## Technical stack

### WindowMaker theme files:
- `~/.WindowMaker/WindowMaker` — main config (colors, fonts, decoration style)
- `~/.WindowMaker/WMWindowAttributes` — per-application window behavior
- `~/.WindowMaker/WMRootMenu` — right-click menu
- Pixmap themes via GNUstep's theming system

### GTK theme (extended scope):
- GTK 3/4 CSS — `gtk.css` overrides palette and widget geometry
- The GTK theme should read as the same design language as the WM theme

### Terminal:
- The terminal emulator is the most important application in the environment
- Recommendation: Alacritty (GPU-accelerated, TOML config, no cruft) or
  kitty (more features, same philosophy)
- Config should specify: KaamOS palette, chosen monospace font, no title bar
  (WindowMaker handles decoration), subtle amber cursor

### Wallpaper:
- Generated from the hex grid geometry in mvp.html
- Export the canvas as SVG, convert to high-res PNG
- The spirograph trail from a solved Simon sequence is a valid wallpaper
- Alternatively: a static hex grid, dimly lit, with Hiljaisuus at center

---

## The Hollywood OS constraint as design brief

The stationborn in the novel use this OS because it arrived with the first
settlers and nobody replaced it because it worked. The worldborn use it
because it is the only computer they have and they built it from what they
knew. Same OS. Different relationship to it.

Design implication: KaamOS should look like something that was designed once,
correctly, and has been running ever since. Not dated. Not retro for retro's
sake. Just... settled. The way a tool looks after it has been used for a long
time by people who knew what they were doing.

The opposite of a UI that is trying to impress you.

---

## What "done" looks like

A repository containing:

1. A WindowMaker theme installable with a script
2. A terminal color scheme (Alacritty or kitty TOML)
3. A wallpaper (SVG + PNG, generated from the hex grid)
4. A README that is also a piece of worldbuilding — describes KaamOS
   as if it were real infrastructure, with the fiction layered lightly
   over the technical documentation
5. Screenshots that would not look out of place in the novel's world
   and also look like something a developer would actually use

Optional: a GTK theme that matches.

---

## Connection to the rest of the project

- mvp.html contains the hex grid geometry and the color palette
- kaamos.asm demonstrates the OS's spiritual ancestor (CP/M / OS-9 era)
- os9_notes.md contains the deeper worldbuilding context
- The suomi directory contains the linguistic register
- The novel's characters live in this environment — Selli at his terminal
  looks like this. Kaija's diagnostic tools run here. Emo's interface
  is a single blinking cursor and nothing else.

---

## The three-act structure of a single run

The player doesn't change character. They change understanding.
Reko, Turo, and Keijo are the same person at different depths of the same shift.

**Reko:** Dumb spirograph game. Does the job. Doesn't ask questions. The glyph
is a byproduct of routing. Mildly satisfying. Whatever. Logs back in after death
without grief because that's what stationborn do.

**Turo:** The spirograph has a glyph game. Notices the Mastermind layer.
Treats it as a puzzle worth solving. Gets good. Feels the system. Starts to see
that the Silence is consistent, that something is being communicated.
Engages on its own terms. A challenge at human proportions for a smarter player.

**Keijo:** Every time you fuck it up, a world dies.
The sequence the Silence was sending wasn't routing instructions. It was a warning.
The hehku misrouted three shifts ago didn't arrive. The station it was going to
is dark. The people on it were worldborn. They had a word for what happened to them.
The stationborn don't have that word. You were playing a spirograph game.

The game didn't get harder. The player got closer.

This is an invented game structure. Note the date: April 2026.

---

## What the player doesn't know

1. The game is a language lesson.

2. They've been reading the novel. The glyph vocabulary is the suomi directory.
   The Silence is hiljaisuus. The ATC job is the journey. When they pick up the
   novel they'll recognize the station. They worked their way in.

3. Their deaths are wrecking worlds. The stationhand who fails a routing sequence
   and resets — the hehku that didn't move, the station that went dark, the thing
   downstream that needed it — being stationborn, they wouldn't care. The job is
   the job. You log back in. You start the shift.

   The worldborn know what a station going dark means.
   The player finds out in the novel.

---

## Brane folds — the symbol set

Not glyphs. **Brane folds.** The hehku routing anomalies create fold patterns
in the network topology. The ATC reads folds. The Silence sends folds. The
player earns folds. The vault is a fold catalog.

The term derives from the novel's cosmology: the void has no spacetime, but
it has structure. The folds are where that structure becomes legible.

**Proportions (Miller's Law / Nethack drawbridge):**
- Mastermind code length N = 4
- Base fold vocabulary K = 7 or 8
- Ratio ~1.5-2x — enough deduction power, fits in working memory
- Nethack uses 8 notes for a 6-note sequence. Same human proportion.
- The vault feels full at 7-8 tiles. Not overflowing. Full. Ready.

**Two tiers:**
- Base vocabulary: 7-8 fold types from unidirectional traversal
- Varied vocabulary: 7-8 additional types from bidirectional hehku (probing)
- Turo's game and Keijo's game use the same board with a richer alphabet
- The second tier unlocks without announcement

---

## Playability — the last chance mechanic

On Simon failure: the partial glyph freezes on the board. Traversed edges remain lit,
dim. The player sees what they were building.

Last chance: complete the glyph by tracing the shape directly. Different cognitive
task from the sequence — spatial not temporal. Some players are better at one than
the other. The game accommodates both without announcing it.

Input: player clicks remaining stations to complete the shape. Evaluated against
the target glyph, not the sequence order. One shot. Wrong trace — dead. Correct
trace — token earned, shift continues.

The penalty is not death. The penalty is that the Silence saw you needed it.

Reko never needs it. Turo uses it strategically. Keijo understands the last chance
isn't mercy — it's the Silence showing you what it was saying, one more time,
more slowly.

---

## Glyph alphabet — design parameters

**Human proportion:** 7 ± 2 (Miller's Law). The ceiling before spirograph becomes
noise instead of symbol. Six to eight active stations per run. Nine total for full
hex symmetry — inactive stations are dead channels, grey on the board, part of lore.

**Sweet spot:** Glyphs with 8-12 edges. Too few = a line. Too many = a tangle.
8-12 gives internal structure, negative space, recognizable topology. That's where
the runes live. The bell curve peaks at 16 — pull from the left shoulder.

**Visual register:** Ogham meets Younger Futhark meets hex grid.
- Ogham: linear strokes off a central line — the path structure of a walk
- Futhark: angular, carved, meant to be cut into stone or bone
- Hex grid: sixty-degree angles exclusively — already the geometry of Celtic knotwork
The glyphs are angular, non-representational, internally consistent.
Feels ancient without being any specific historical script.
Carved by people who understood the void and needed to write in it.

**Mood:** The boundary between the living and the eternal. Finnish/Celtic/Nordic
mysticism. Not horror. Not fantasy. The quiet register of something that has always
been there and does not need to announce itself.

**Memory footprint:** 6-8 glyph types per run, each a frozenset of edges.
Fits in a lookup table a 6809 wouldn't blink at.

**Lore compatibility:** The glyphs the player earns ARE the writing system of
the station culture. The player learns to read without being taught to read.
By the time the novel arrives, they already know the alphabet.

---

## Agent instructions

If you are working on the WindowMaker theme:
- Start with the palette. Get the colors right before touching anything else.
- The terminal color scheme ships first. It's the smallest artifact and the
  most important one.
- Test on a real WindowMaker installation, not a screenshot.
- Read mvp.html before writing a single color value.

If you are working on the GTK theme:
- Match the WindowMaker palette exactly.
- Flat. No shadows unless they are load-bearing (indicating Z-order).
- Buttons have edges. Inputs have borders. Nothing is ambiguous.

If you are working on the wallpaper:
- Export the hex grid from mvp.html at 3840x2160.
- The Hiljaisuus hex is at center. The stations are named but dim.
- The spirograph trail, if used, should be from a real solved sequence.

If you are working on the README:
- It is fiction and documentation simultaneously.
- The tone is os9_notes.md. The structure is a real README.
- It should be possible to install KaamOS from it.
