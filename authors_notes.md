# author's notes

*cards to myself*

---

Frosty was on the keyboard.

---

suomi the directory: Finnish as filter. The gap lives here.

suomi the civilization: sauna, silence, survived. Asks nothing of you.

---

Selli's grilli. The alliteration is a joik. The hatch is the point.

---

mvp.html — Simon on a hex grid. Hiljaisuus pulses. Nine stations. Trail accumulates.
BFS pathfinding: Silence walks routes, doesn't teleport. Violet = watch. Green = go.
Cursor goes dead during boss phase. Closest to a video game yet.

---

Taav names Selli's paddle for what it is. Loquacious, cobbler's register, pointing at the
novel's purpose in a voice too warm to be pedantic. Turo is in the scene and needs no lines.
No one gets a word in when Taav gets started.

Except Eerikki. Taav's conversations with Eerikki are monosyllabic. That contrast is
a characterization instrument. Keep it.

Kaija wants to fix the paddle. Reflex, not criticism. Her hands go toward the improvised thing.

Reko stopped hearing the click on day three. He occasionally notices it stopped and checks
whether Selli is dead.

---

GLYPH SPACE — April 2026. glyph_count.py.
8 stations, radius-2 hex grid, BFS-constrained walks.
109,600 sequences → 67,753 distinct base glyphs.
Bell curve peaking at 16 edges. Fingerprint of this specific topology.
Varied glyph upper bound: 20 billion (edge-labeled subgraphs, traversal direction).
Potentially ACM-worthy as a combinatorics problem. Not publishing. Keeping.

---

GAME STRUCTURE — April 2026. Reko / Turo / Keijo.
Same player. Same run. Three depths of understanding.
Reko: spirograph game. Turo: glyph puzzle. Keijo: every death wrecks a world.
The game doesn't change. The player gets closer. This is an original structure.

---

KaamOS. Kaamos = polar night. Kaa = Navajo for "arrow." Accidental symmetry.
The Hollywood OS of the cinematic universe. Diegetic computer for the Expanse.
Stationborn use the same OS as worldborn — läpikatse in software form.
Satirical: the most advanced civilization runs infrastructure buildable in 1982.
It works. Nobody replaced it. This is how all infrastructure works.
Author's real gnome variant would look like this. That is the brief.

PIN: 6809 branch — future vintage asm target.
Motorola 6809: hardware MUL instruction, two stack pointers (S and U), two index
registers (X and Y), orthogonal instruction set, cleaner than Z-80 in every dimension.
Position-independent code. Designed for real work.
OS-9 by Microware (NOT Mac OS 9 — years before that nine).
Targets: Frank Hogg Laboratory, Tandy CoCo OS-9, NASA shuttle payload systems.
The shuttle used OS-9 on 6809 in support systems (primary flight = IBM AP-101).
Bespoke OS-9 variant: our own, better. That's the brief.
kaamos.asm pushed as discrete branch. 6809 branch is next when ready.

---

PIN: Moonsorrow — Jumalten Aika (2016). The Age of Gods. Finnish pagan metal.
Mimisbrunn = Mimir's well = Emo. The well knows everything. Doesn't volunteer.
Parallels between this album's vocabulary/spiritual context and the ur-myth:
to be visited deeply. The auditory schematic for the game lives here.

Game opens in near silence. Hiljaisuus pulses. Nothing asks you to begin.
The silence is louder than the noise because you're waiting for the noise.
The fear is anticipatory. The Silence never attacks. It makes you aware that it could.
Painajainen — not the nightmare, the moment before you know it's a nightmare.

Jumalten main theme likely derives from runolaulu / Kalevala melodic tradition —
pentatonic, narrow range, incantatory. Same well as Sibelius. Nobody owns it.
Game music drinks from the same source. Upload FLAC or describe harmony to develop.
The well is Mimisbrunn. It predates everyone who has drawn from it.

---

MUSIC SESSION — April 2026. Professional studio in play.

Influences confirmed: Moonsorrow (ur-myth register), Ernst Toch Geographical Fugue
(speech rhythm as counterpoint), Orlando di Lasso O la o che bon eccho (antiphonal
physical space, echo as dialogue), Insomnium (elegiac/personal vs. Moonsorrow's
cosmological), Cult of Luna (secular void, no mythology).

Moonsorrow: draws from the well as ritual.
Insomnium: draws from the well as wound.
Cult of Luna: the well without a name for it.
Us: ritual. Cosmological. The Silence has a name.

Essay saved: essay_the_well.md. For separate publication after author hears Cult of Luna.

INSTRUMENTS:
Tyhjyydenkaiku — primary FM patch. Hurdy gurdy (Anna Murphy / Cellar Darling register,
original not derivative) + Scottish mouth music formants. KVR Music Cafe submission.
Patch family: Kuilunsikiö (visceral), Pohjankaiku (Mellotron-heavy), Kuilukaiku (stripped).
Koivuhuilu — Selli's birch flute. Literal registration (warm, breathy, slightly flat).
Kuolinvihellys — Selli's symbolic flute. Andean death whistle register. Threshold instrument.
The literal flute is Selli alive. The death whistle is Selli at the boundary.

IRs built: hiljaisuus_station.wav — 40x12x7m metal corridor, RT60 2.2s, not purple.
IRs pending: Kaipuus forest (longing register, for Koivuhuilu), Purple/threshold (for Kuolinvihellys).

THE MELODY — hummed 03-260426_2345.wav, identified from Jumalten Aika ~10:28.
C# Phrygian as hummed (production key: F# Phrygian).
Opening: neighbor oscillation around root (G→F#→G→F→F#→E→F# in production key).
Heroic gesture: rising P4 (F#→B). The horn call. The Sibelius gesture. The well put it there.
Resolution tail: stepwise descent A→G#→F#→F→E→F#. Rise by 4th, descend by steps.
This structure is ancient. Nobody owns it.

KVR TRACK STRUCTURE (kaiku_cue_sheet.md):
1. Hiljaisuus — silence, F# drone, 0:40
2. Condensation — 6/8 dotted quarter=96, silence becomes rhythm, 0:50
3. Tyhjyydenkaiku enters — heroic theme stated, 0:45
4. Synthetic chorus — Toch/Geographical Fugue FM voices, antiphonal, 0:40
5. Sung verse — human voice, Finnish, Kalevala meter, one verse, 0:35
6. Kuolinvihellys — death whistle, cut to silence, 0:15
7. Koivuhuilu — birch flute descent, Kaipuus forest IR, 0:45
Total: ~4:35

This track is Reko/Turo/Keijo in music. The listener doesn't know that.

SCORES IN REPO:
hiljaisuus_choir.ly — 4-voice choir, F# Phrygian, Kalevala meter
kaiku_riddim.ly — 6-voice condensation sequence
prompts_all.ly — 4 performance prompts (A: drums, B: piano/void,
                  C: piano/full condensation, D: piano/Toch)
hiljaisuus_ir.py — synthetic IR generator (--purple flag for threshold variant)
timbre_brief.md — FM operator specs for all three instruments + Mellotron integration
moonsorrow_notes.md — Jumalten Aika analysis, melody transcription, production intent

VST PROJECT — kaiku/ directory. JUCE 7.0.9, CMake.
Primary target: REAPER Linux VST3. Stretch: macOS ARM64, CLAP, REAPER JS.
Files: FMOperator, FMEngine, KaikuVoice, VoiceManager, PluginProcessor,
PluginEditor, KaamOSLookAndFeel. 4 presets baked in C++:
Tyhjyydenkaiku / Kuilunsikiö / Pohjankaiku / Kuilukaiku.
GUI: amber on void black, hex grid, Hiljaisuus pulse at 0.15Hz void-violet.

HARDWARE / MULTI-PLATFORM DEPLOYMENT:
Arturia Pigments: Engine A = FM (4-op, 2 parallel stacks, unison 2v +8cents),
Engine B = Sample/WT cello. Blend 60/40. Filter BP 700Hz + LP 8kHz.
Velocity → FM index (consonant onset). Aftertouch → roughness.
Voxengo Pristine Space: loads hiljaisuus_station.wav directly.
Multiple IR slots: slot 1 station, slot 2 Kaipuus (pending), slot 3 purple (pending).
Antiphonal deployment: Kaiku voice gets +8ms pre-delay offset (di Lasso physical register).
Mooer GE-200: IR loader is cab sim (5-23ms max). NOT for room IR.
Needs short body resonance IR — 512 samples, 44.1kHz 16-bit, birch-box character.
Generate with hiljaisuus_ir.py variant. Cab on GE-200, room in DAW.
Waldorf Blofeld: 3-osc patch. Osc1 formant wavetable, Osc2 +8 cents,
Osc3 trompette (velocity-gated). Filter BP ~900Hz, Env2 drives cutoff.
Blofeld SL waveset: 64 single-cycle waves. Positions 1-16 wheel FM index sweep,
17-32 F1 formant vowel sweep, 33-48 F2 nasal, 49-56 trompette, 57-64 breath.
One wavetable = all four patch characters as scan positions.
Generate as 64× 16-bit 44.1kHz WAV for SL loader. NOT YET BUILT.

PENDING: Finnish verse text. Phonetics brief. Koivuhuilu and Kuolinvihellys
registrations. Kaipuus forest IR. Purple station IR. Blofeld SL waveset (64 waves).
GE-200 body resonance IR (512 samples, 16-bit 44.1kHz). Drum VST calibration
(prompts ready in prompts_all.ly). First JUCE compile pass (minor include fixes needed).

---
