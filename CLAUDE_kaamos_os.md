# CLAUDE.md — KaamOS
## Agent context for the KaamOS desktop environment and Kaiku VST project

*Read this before touching anything. This is the ground truth.*

---

## What this is

**KaamOS** is simultaneously:

1. The **Hollywood OS** of the Kaamos cinematic universe — the diegetic computer environment stationhands use on the Expanse. When a character opens a terminal in this world, this is what they see.

2. A **real desktop environment** the author actually uses. Not a mockup. Not a screenshot. Something that boots and works.

3. A **VST synthesizer** — Kaiku, a JUCE-based 6-operator FM synth with a gel electropherogram display, designed to produce the sounds of the Kaamos soundtrack and deployable as a real audio plugin.

4. A **portfolio piece.** The author is a developer. This shows taste, range, and follow-through.

These goals are not in conflict. The Hollywood prop constraint is the design brief. Real usability is the test of whether the brief was worth following.

---

## Design language — non-negotiable

### Palette (hardcoded, exact values)

| Token | Hex | Meaning |
|-------|-----|---------|
| `--void` | `#070711` | Background. The deep. |
| `--kaiku` / amber | `#c8a050` | Primary UI. The echo. |
| `--hiljaisuus` / violet | `#8030c0` | Station 9. The Silence. Warning/threshold. |
| `--hehku` / ember | `#c85020` | The heat from within. Error/active-danger. |
| `--pohja` / blue | `#3030a0` | The bottom/ground. Inactive/depth. |
| `--asema` / green | `#40c080` | Station active. Clear/go. |
| `--muted` | `#2a2a5a` | Dimmed elements. |

These token names are load-bearing. `--kaiku` means the echo. `--hiljaisuus` means the Silence. `--pohja` means the ground beneath. Do not rename them to generic values. Do not change the hex values.

### Typography
- **Terminal font:** Iosevka or Fira Code. Good Unicode coverage and Finnish character support.
- **UI font:** system-ui fallback is acceptable; something that reads as designed-for-a-purpose.
- No rounded corners. The grid has edges.

### Shape language
- Hexagonal motifs where decorative elements appear (dock separators, wallpaper, loading screens)
- The hex grid from `mvp.html` is the visual vocabulary
- Icons: angular, rune-adjacent, readable at small sizes
- No gradients. Flat color, sharp edges, intentional.
- 60° angles throughout. This is the hex grid constraint and it applies everywhere.

### Motion
None, or nearly none. The terminal doesn't animate. If something moves, it is because it is communicating information.

**The one exception:** The Hiljaisuus pulse. A slow pulse on the status indicator, in void-violet, at **exactly 0.15Hz (period 6.67 seconds)**. This is a cosmological constant from the Kaamos world. Do not change it. It is in `kaamos.css` as `--pulse-duration: 6.67s` and in the `.hiljaisuus-pulse` animation. The Silence is always there.

---

## The design system

### kaamos.css
The full design system. Token names in ur-myth vocabulary.

**Key components:**
- `.kaamos-nav` — sticky navigation bar
- `.kaamos-hero` — full-width hero with `.hex-bg` option
- `.kaamos-section` / `.kaamos-section-full` — content sections
- `.kh` — section heading label (amber mono, uppercase)
- `.prose` — body text (serif, 1.1rem, line-height 1.9)
- `.dual-callout` — the Dual Correctness box (amber border left; `.violet` variant for Hiljaisuus content)
- `.char-grid` / `.char-card` — character cards with variants:
  - `.voidbound` — standard amber card
  - `.void-called` — violet heading (threshold content)
  - `.mimir` — muted (Emo, the recorder)
  - `.dead` — dashed border (Ara, speaks from structural gaps)
  - `.full-width` — spans full grid (the poles, structural relationships)
- `.scene-text` — scene prose with `.scene-click`, `.scene-beat`, `.scene-void`
- `.gel-container` — electropherogram display container
- `.kaamos-table` — mono-register data table
- `.hiljaisuus-pulse` — the pulse animation (6.67s)
- `.status-dot` — colored status indicators (`.green`, `.amber`, `.hehku`, `.violet`)
- `.mono-label` — inline mono labels
- `.kaamos-quote` — blockquote (amber left border; `.violet` variant)
- `.kaamos-footer` — footer with pulse

**Game-suggestive geometry (CSS classes that imply topology without gameplay):**
- `.hex-bg` — hex tessellation background (faint, amber on void)
- `.bfs-bg` — BFS traversal hint background
- `.nine-border` — notched ninth corner (the missing vertex, violet)
- `.bfs-border` — amber left + violet bottom (directional trace)
- `.station-card` — node with amber dot, pulses when `.nine`
- `.route-line` — amber path with endpoint dots
- `.glyph-frame` — cipher box with `data-edges` attribute
- `.void-corridor` — amber left wall, violet right wall

### kaamos_template.html
Full component showcase. Start here when building new Kaamos-themed pages. Links to `kaamos.css`.

### Logos
- `kaamos_logo.svg` — Kaamos brand mark: 8 amber station hexes in ring surrounding violet Station 9 (Hiljaisuus). "KAAMOS" mono wordmark below.
- `kaamos_os_logo.svg` — KaamOS brand mark: flat-top hex badge with notched ninth vertex in violet, K-rune (Younger Futhark ᚲ Kaun register) inscribed in amber at 60° hex-grid angles. "KaamOS" mono wordmark below.

Both are standalone SVGs with hardcoded KaamOS palette, suitable for print and web.

---

## Kaiku VST — architecture

### What it is
A JUCE-based 6-operator FM synthesizer producing the sounds of the Kaamos soundtrack. Primary target: REAPER on Linux x86_64 (VST3). The instrument that plays the Tyhjyydenkaiku heroic theme.

### Source location
`kaiku/` — CMake project, JUCE framework.

```
kaiku/
  CMakeLists.txt     — build configuration
  BUILD.md           — build instructions per platform
  README.md          — instrument overview
  Source/            — C++ source files
  Resources/         — assets
```

### Build (Linux primary)
```bash
sudo apt install cmake git build-essential \
    libx11-dev libxrandr-dev libxinerama-dev \
    libxcursor-dev libfreetype-dev \
    libasound2-dev libwebkit2gtk-4.0-dev

cd kaiku
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --parallel
# Output: build/Kaiku_artefacts/Release/VST3/Kaiku.vst3
```

### FM architecture — the Tyhjyydenkaiku patch
Three parallel 2-operator stacks. Each stack: modulator feeding carrier.

| Stack | Role | Character |
|-------|------|-----------|
| Stack A | Primary harmonic | Core timbral body |
| Stack B | Spectral edge | Adds upper partials |
| Stack C | Trompette buzz | Velocity-triggered, on accented beats only |

**Detuning:** 1.008× wheel detuning on Stack A to produce the hurdy-gurdy drone effect. This is the signature of Tyhjyydenkaiku — the slight beating of near-unison FM operators.

**Mouth music FM (Sections 3-4):**
- Lausuja — mouth music voice 1, center
- Kaiku — echo voice, 2-bar delay, slight spatial offset
- Ilma — sustained soprano, above, diffuse (C# = 5th, D = minor 6th)
- Pohja — bass drone, F# pedal, continuous

FM vowel color shifts on attack (consonant) and settles into sustained (vowel). The FM formant logic matches Finnish vowel phonetics — when the live voice sings in Section 5 and the choir responds, the FM is matching the mouth.

### The gel display — the VST spectrogram
The player display in the game and the VST spectrogram are the same visual system.

The gel electropherogram maps to frequency domain:
- Stations = gel lanes
- Glyph edge count = molecular weight (migration distance)
- Bell curve peak at edge 16 = the band that runs farthest
- Ghost bands = FM sidebands
- Station 8 (Keijo) = degraded / smearing — violet tinge
- Station 9 (Hiljaisuus) = voltage-loss smear, violet pulse overlay, animated

Prototype: `lane_run.html`. This is the reference implementation for the JUCE `PluginEditor` spectrogram component.

### Pending VST work
- First clean JUCE compile pass (minor include fixes needed)
- JUCE spectrogram component (gel display replacing placeholder hex grid in PluginEditor)
- Koivuhuilu registration — warm, breathy, slightly flat; carved birch wood, not factory tolerance
- Kuolinvihellys registration — high FM index, near-noise, tonal center C# or F#; this does not live in the station IR; it comes from outside the room
- Kaipuus forest IR — longing register; the space Taav is from, not the space he works in
- Waldorf Blofeld SL waveset — 64 single-cycle waveforms, 16-bit 44.1kHz
- Mooer GE-200 body resonance IR — 512 samples, 44.1kHz, 16-bit
- Drum VST calibration — Prompt A ready in `prompts_all.ly`

---

## KaamOS desktop environment

### Starting point: WindowMaker
WindowMaker is the correct starting point.
- Still maintained and installable in 2026
- NeXTSTEP-derived: clean, dock-based, minimal chrome
- Highly themeable
- The aesthetic is already closer to KaamOS than any other WM
- The author can actually use it day-to-day

**Minimum viable KaamOS:** A WindowMaker theme. Everything beyond that is additive.

### Extended scope (additive)
- GTK 3/4 theme for in-environment applications
- Custom icon set (runic/hex-grid aesthetic, angular, readable at small sizes)
- Terminal color scheme (most important single artifact — ship this first)
- Dotfiles repo that bootstraps the entire environment

### WindowMaker theme files
```
~/.WindowMaker/WindowMaker          — main config (colors, fonts, decoration)
~/.WindowMaker/WMWindowAttributes   — per-application window behavior
~/.WindowMaker/WMRootMenu           — right-click menu
```

### Terminal — the most important application
Recommendation: Alacritty (GPU-accelerated, TOML config, no cruft) or kitty.

Config must specify:
- KaamOS palette
- Chosen monospace font (Iosevka or Fira Code)
- No title bar (WindowMaker handles decoration)
- Amber cursor

**The terminal color scheme ships before anything else.** It is the smallest artifact and the most important one.

### Wallpaper
Generated from the hex grid geometry in `mvp.html`. Export at 3840×2160. The Hiljaisuus hex at center. Station nodes named but dim. A solved spirograph trail is a valid alternative wallpaper.

### The Hollywood OS design constraint as brief
KaamOS should look like something that was designed once, correctly, and has been running ever since. Not dated. Not retro for retro's sake. **Settled.** The way a tool looks after it has been used for a long time by people who knew what they were doing. The opposite of a UI trying to impress you.

The stationborn use it because it arrived with the first settlers and nobody replaced it because it worked. The worldborn use it because it is the only computer they have. Same OS. Different relationship to it.

---

## The 6809 / OS-9 layer

`kaamos.asm` — 6809 assembly branch. The spiritual ancestor of KaamOS.

`os9_notes.md` — full worldbuilding and historical context. Key facts:

- **Microware OS-9 (1979):** Real-time, multitasking, Unix-influenced. Written almost entirely in 6809 assembly. Modular kernel, relocatable modules, position-independent code, two stack pointers (S = hardware, U = user), hardware multiply (MUL: A×B→D).
- **The shuttle:** OS-9 on 6809 was used in payload data handling and ground support. Not the primary flight computers (those were IBM AP-101/System-360). The payload bay ran Microware code. This is confirmed historical register. The author's nostalgia is the 6809's actual role — real work, serious machines.
- **The time traveler's brief:** Not OS-9. Informed by OS-9. The OS a 6809-era machine could have had if anyone had pushed it as hard as it deserved. Position-independent code, modular kernel, pipes and I/O redirection, preemptive multitasking — all of these were possible in 1979 and OS-9 proved it. KaamOS is that machine with hindsight applied.

`z80asm.py` — assembler utility (related toolchain).

---

## Web presence

`index.html` — current public-facing web page.

The site at `eerikki.jamesmcgill.us` (S3 static hosting) uses the same KaamOS palette. The `world_bible.html` in the Kaamos repo is styled to match this aesthetic and can be deployed alongside or as its own page.

When building new web pages for this project: start from `kaamos_template.html`. Apply `kaamos.css`. The design system handles everything.

---

## File inventory (this repo)

### Design system
- `kaamos.css` — full design system
- `kaamos_template.html` — component showcase
- `kaamos_logo.svg` — Kaamos project brand mark
- `kaamos_os_logo.svg` — KaamOS product brand mark

### VST synthesizer
- `kaiku/` — JUCE project (full FM synth)
- `timbre_brief.md` — FM voice and timbre specifications

### Desktop environment
- `os9_notes.md` — 6809/OS-9 worldbuilding and historical context
- `KAAMOS_DE.md` — combined KaamOS/game design document (shared with Kaamos repo)
- `kaamos.asm` — 6809 assembly (spiritual ancestor)
- `kaamos.com` — compiled binary artifact
- `z80asm.py` — assembler utility

### Prototypes
- `mvp.html` — hex grid prototype with full BFS visualization, complete palette
- `lane_run.html` — gel electropherogram prototype (VST display reference implementation)

### Web
- `index.html` — public-facing web page

---

## Agent operating instructions

**On the palette:** Never substitute these colors. `#c8a050` is amber. `#8030c0` is the Silence. These are not design choices — they are the identity of the project. If you are tempted to use `#c8902a` or `#7828b0` because they are "close enough," you are wrong.

**On the pulse:** 6.67 seconds. 0.15Hz. Always. If you change this, you have changed the cosmological constant of the project. Don't.

**On the gel display:** The electropherogram IS the spectrogram. They are not two different visualizations — they are the same visual system in two contexts: game UI and VST UI. Design decisions in one propagate to the other.

**On the terminal:** Ship the terminal color scheme before anything else. It takes one afternoon and it proves you understand the environment.

**On WindowMaker:** Read `KAAMOS_DE.md` before starting the WM theme. The design brief is there. The README for the KaamOS theme repo should be fiction and documentation simultaneously — describes KaamOS as real infrastructure with the fiction layered lightly over the technical documentation.

**On "done":** A repository containing: a WindowMaker theme installable with a script, a terminal color scheme (Alacritty or kitty TOML), a wallpaper (SVG + PNG from hex grid), and a README that is also a piece of worldbuilding. Screenshots that would not look out of place in the novel's world and also look like something a developer would actually use. Optional: a GTK theme that matches.

**On the Kaiku VST:** The gel display is the next major milestone after the first clean compile. Build the spectrogram component against `lane_run.html` as reference. The visual must match — not "similar to" — because they are the same thing.
