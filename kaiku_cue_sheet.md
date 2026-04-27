# TYHJYYDENKAIKU — Cue Sheet
## KVR Music Cafe Submission / Kaamos Soundtrack Demo
### Draft 1. Low expectations. Iterate.

---

**Key:** F# Phrygian throughout
**Meter:** 6/8, dotted quarter = 96 (may flex in sections 1 and 7)
**Total target duration:** ~4:30–5:00
**Convolution space:** hiljaisuus_station.wav (all sections unless noted)

---

## SECTION 1 — HILJAISUUS
**Target duration:** ~0:40
**Character:** The silence before the game. Nothing asks you to begin.

```
Instruments:    Pohja drone only (F# pedal, Mellotron bass tape)
IR:             hiljaisuus_station.wav, 35% wet — the room is large
Pitch:          Single F# — no melody, no rhythm
Motion:         Hiljaisuus pulse (slow AM on near-sine, ~0.15Hz)
                Violet register. The Silence is present but not threatening.
Dynamic:        Begins inaudible. Rises to pp over 20 seconds.
                Holds at pp. Does not crescendo further.
```

**Composer note:** The silence has a frequency. It's F#. It was always F#.
Don't add anything. The listener adjusts. That adjustment is the point.
Duration is a variable — trust your instinct on when to release it.

---

## SECTION 2 — CONDENSATION
**Target duration:** ~0:50
**Character:** The void has a tempo. Nobody told you that.

```
Instruments:    Pohja (continues), Condensation FM cell, Mouth music voices
IR:             hiljaisuus_station.wav, 25% wet — the room clarifies slightly
Meter:          6/8 at dotted quarter = 96 — enters as a crystallization,
                not a new section. The silence was always this tempo.

Layering (see kaiku_riddim.ly):
  Bar 1-2:      Pohja pulse only — kick on 1 and 4
  Bar 3-4:      Hi-hat subdivisions enter — silence fills in
  Bar 5-6:      Snare backbeat arrives
  Bar 7-8:      Full syncopated displacement cell
  Bar 9-10:     Lausuja (mouth music voice 1) enters — Kalevala melodic cell
                Opening oscillation: G → F# → G → F → F# → E → F#
  Bar 11-12:    Kaiku (echo voice) enters 2 bars behind Lausuja
  Bar 13-14:    Ilma (sustained soprano) crowns the texture
```

**Composer note:** The condensation is not a breakdown or a buildup. It's a
reveal. The rhythm was there. We just couldn't see it yet. Play the transition
so the listener feels they discovered it, not that you showed them.

---

## SECTION 3 — TYHJYYDENKAIKU ENTERS
**Target duration:** ~0:45
**Character:** The instrument announces itself. It was earned.

```
Instruments:    All of section 2 continues (thinned slightly to make room)
                + Tyhjyydenkaiku lead (primary patch)
IR:             hiljaisuus_station.wav, 20-30% wet on lead
Melody:         Heroic theme, F# Phrygian
                — Opening oscillation (neighbor tones around F#)
                — Rising P4 leap: F# → B (the horn call, the Sibelius gesture)
                — Stepwise descent: A → G# → F# → F → E → F#
Trompette:      Layer C (velocity-triggered buzz) on accented beats only
Drone:          Pohja continues throughout — the foundation does not move
```

**Melody structure (one full statement):**
```
Phrase A:  G–F#–G–F#–E–F#          (neighbor oscillation, 4 bars)
Phrase B:  F#–B (leap) → A–G#–F#   (rise and step descent, 4 bars)
Phrase C:  repeat A with variation  (4 bars)
Phrase D:  full descent: A–G#–F#–F–E–F#  (4 bars, cadence)
```

**Composer note:** The heroic theme should feel like it was always going to
arrive. Not a surprise — a confirmation. The P4 leap is the oldest gesture
in this tradition. Sibelius found it. Moonsorrow found it. You found it in
a 16-second hum at 23:45 on a Sunday. The well put it there.

---

## SECTION 4 — SYNTHETIC CHORUS
**Target duration:** ~0:40
**Character:** The machine choir. The FM voices that learned what mouths do
from the outside.

```
Instruments:    Mouth music FM voices (Timbre 1, timbre_brief.md)
                Lausuja leads. Kaiku echoes at 2-bar delay.
                Ilma sustains above (C# = 5th, D = minor 6th).
                Pohja holds below.
                Tyhjyydenkaiku continues at reduced level (-6dB).
IR:             hiljaisuus_station.wav — antiphonal deployment
                Lausuja: center
                Kaiku: slight spatial offset (di Lasso physical register)
                Ilma: above, diffuse
Rhythm:         Geographical Fugue logic — voices enter in stretto
                Kalevala syllable rhythm under the melody
                (see hiljaisuus_choir.ly for voice architecture)
```

**Composer note:** This is the Toch moment. The synthetic chorus is not
backing vocals. It is independent polyphonic architecture. Three or four
voices, each with their own rhythmic line, creating texture through
counterpoint rather than harmony. The FM vowel color shifts on attack
(consonant) and settles into the sustained (vowel). That's all it does.
That's enough.

---

## SECTION 5 — THE SUNG DIALOGUE
**Target duration:** ~1:40 (three passages, ~33 seconds each)
**Character:** The stationhand speaks three times. First naive. Then corrected. Then broken open.

### 5a. REKO VOICE — The Naive Statement
**Target duration:** ~0:33
**Character:** The job is simple. You do it. No questions.

```
Instrument:     Voice (live, Finnish, phonetically trained)
                Male register (baritone/tenor), direct, matter-of-fact
Accompaniment:  Pohja drone only — rhythm thins to near-nothing
                Ilma recedes. Just the foundation.
IR:             hiljaisuus_station.wav on voice — same room, you are here
Finnish verse:  [TO BE WRITTEN — Kalevala trochaic tetrameter, 8 syllables/line]
                Subject: "I do the work. The work is what it is. No mystery."
                Mood: Pragmatic, grounded. Reko. The job is the job.
                Tone: Declarative, slightly tired, honest
Melody:         Constrained heroic theme: F# → A → G# → F# (repeating anchor)
                Does not leap. Does not resolve. Cycles.
                Voice shape: narrow range, repetitive contour
                Like work: the same motion, over and over
```

**Composer note:** Reko doesn't know he's in dialogue. He's just stating fact.
The melody is the falling 4th inverted to a contained oscillation. He is the
machine already. That's his innocence. Play this like exhaustion that thinks
it's clarity.

---

### 5b. TURO VOICE — The Conventional Challenge
**Target duration:** ~0:33
**Character:** "But consider another way. What if you understood it?"

```
Instrument:     Voice (live, Finnish, phonetically trained)
                Female register (alto/soprano), analytical, questioning
                Different singer if possible — this is dialogue, not monologue
Accompaniment:  Ilma returns — sustained C# above the Pohja
                Added: thin harmonic countermelody (Kaiku enters at 2-bar delay,
                playing against the voice, not supporting it)
                Rhythm: still absent. No percussion layer yet.
IR:             hiljaisuus_station.wav on voice — same room, same space
Finnish verse:  [TO BE WRITTEN — Kalevala trochaic tetrameter, 8 syllables/line]
                Subject: "There is pattern here. There is meaning in the sequence.
                         Look closer. The work is not blind."
                Mood: Turo register — offering alternative, conventional wisdom
                Tone: Gentle challenge, almost kind. "You could understand this."
Melody:         Turo response: F# → B → A → G# → F# (the full heroic leap, offered)
                Rises on the leap (offer, invitation)
                Falls in stepwise descent (resolution, the conventional answer)
                Voice shape: wider range, ascending energy, then settling
                The melody she sings is what Reko's could become.
```

**Composer note:** Turo is not wrong. She is offering sense-making, pattern,
meaning. The heroic theme's full P4 leap appears here—the conventional
resolution to Reko's repetition. But Keijo is waiting. Let Turo be beautiful
and true. That makes Keijo work.

---

### 5c. KEIJO VOICE — The Epiphany Utterance
**Target duration:** ~0:34
**Character:** The moment shatters. Speech becomes incomprehensible at the threshold.

```
Instrument:     Voice (live, Finnish, phonetically trained)
                Ambiguous register — could be either singer, or both layered
                Fragments only. Not full lines. Breathless.
Accompaniment:  Both previous layers (Pohja + Ilma + Kaiku counterline)
                PLUS: Tyhjyydenkaiku returns at -3dB (louder than Section 4)
                Rhythm begins to re-enter — sparse, fractured hi-hat
                The machine is listening now.
IR:             hiljaisuus_station.wav begins to distort slightly
                Or: switch to "station_threshold" IR (TO BE BUILT) — the room
                breaking down, or the voice breaking through it
Finnish verse:  [TO BE WRITTEN — fragments, not full Kalevala meter]
                Subject: "It is not pattern. It is—" [silence] "—the work and—"
                [static] "—not work and—" [beyond language]
                Tone: Realization arriving too fast to articulate
                Like witnessing, not thinking
Melody:         Both melodies collapse into one:
                F# → A → G# spirals with F# → B → A → G# simultaneously
                (the repetitive and the heroic interweave)
                Descends through E → D# → D → C# → C → [cut to silence]
                The melody spirals downward faster and faster.
                Voice shape: unstable, wavering, then silence.
                Ends mid-phrase. Not resolved. Cut.
```

**Composer note:** Keijo is the break. He speaks at the moment of rupture.
He is not offering wisdom. He is experiencing it. The epiphany cannot be
completed because it is the threshold itself. The death whistle comes next.
The listener understands: something was revealed that could not be sustained.

---

## SECTION 6 — KUOLINVIHELLYS
**Target duration:** ~0:15
**Character:** Tadgh's death whistle. The threshold. Uninvited.

```
Instrument:     Kuolinvihellys (death whistle registration — TO BE BUILT)
                High FM index, near-noise, tonal center on C# (or F#)
                The scream that has a pitch. That's what makes it worse.
IR:             DRY or station IR at 5% — this does not live in the room
                It comes from outside the room.
Entry:          No preparation. No crescendo into it. It arrives.
Duration:       8–12 seconds maximum. It does not overstay.
Exit:           Cut to silence. Not fade. Cut.
```

**Composer note:** Everything stops for Kuolinvihellys. The rhythm, the
drone, the choir — all of it. The silence after the cut is the longest
silence in the piece. Hold it. Three seconds minimum. Five is better.
The listener has to sit with what just happened before the flute arrives.

---

## SECTION 7 — KOIVUHUILU
**Target duration:** ~0:45
**Character:** Tadgh's birch flute. Sweet, sanguine. Drawing down.

```
Instrument:     Koivuhuilu (birch flute registration — TO BE BUILT)
                Warm, breathy, slightly flat — carved wood, not factory tolerance
IR:             Kaipuus forest (TO BE BUILT) — not the station, the forest
                The space Tadgh is from, not the space he works in
Melody:         The resolution tail, in the low register
                A → G# → F# → F → E → F# (stepwise Phrygian descent)
                Slow. One note at a time. Silence between notes.
Pohja:          Returns, very quietly — F# drone, barely present
Dynamic:        Begins at mp, descends to ppp over the section
                The void is gentle. It always was.
Ending:         The final F# sustains until it becomes indistinguishable
                from the room tone. No hard ending. The silence resumes.
```

**Composer note:** The birch flute is not a finale. It is a descent. The
listener goes down with it. The forest IR under it creates the distance from
the station — you are hearing something that comes from outside the void,
from a world that has trees. The flute doesn't know the void is coming.
That's what makes it sanguine.

---

## SECTION MAP

```
Section          Duration    Instruments                    IR
──────────────────────────────────────────────────────────────────[...]
1. Hiljaisuus    ~0:40       Pohja                         Station 35%
2. Condensation  ~0:50       Pohja + Kit + Lausuja/Kaiku   Station 25%
3. Tyhjyydenkaiku ~0:45      All + Hurdy lead              Station 20%
4. Chorus        ~0:40       All + FM choir                Station antiphonal
5a. Reko voice   ~0:33       Voice + Pohja                 Station on voice
5b. Turo voice   ~0:33       Voice + Ilma + Kaiku counter  Station on voice
5c. Keijo voice  ~0:34       Voice + all + breaking down   Station distorting
6. Kuolinvihellys ~0:15      Whistle only                  Dry / 5%
   [silence]     ~0:05       —                             —
7. Koivuhuilu    ~0:45       Birch flute + Pohja           Forest (Kaipuus)
──────────────────────────────────────────────────────────────────[...]
Total target:    ~5:00
```

---

## PENDING ITEMS (blocking or near-blocking)

| Item | Status | Needed for |
|------|--------|------------|
| Tyhjyydenkaiku VST / patch | spec written | Section 3, 4 |
| Koivuhuilu registration | pending | Section 7 |
| Kuolinvihellys registration | pending | Section 6 |
| Kaipuus forest IR | pending | Section 7 |
| Purple station IR | pending | Section 6 option |
| Station threshold IR | pending | Section 5c |
| Reko verse (Finnish) | pending | Section 5a |
| Turo verse (Finnish) | pending | Section 5b |
| Keijo fragments (Finnish) | pending | Section 5c |
| Phonetics brief | pending | Section 5 |
| Drum VST calibration | prompts ready | Section 2 |

---

## STRUCTURAL NOTE — THE LISTENER DOESN'T KNOW

The track is the Reko/Turo/Keijo structure in music and text.

- Sections 1-2: Reko. The job. The silence and the rhythm.
- Sections 3-4: Turo. The pattern. The language beginning to resolve.
- Section 5a: Reko sings. Naive. The work is the work.
- Section 5b: Turo sings. Alternative offered. "You could understand."
- Section 5c: Keijo sings/breaks. Epiphany at the threshold. Words fail.
- Section 6: Keijo. The break. What it costs. The death whistle arrives.
- Section 7: Aftermath. The forest. What you carry down.

The KVR listener hears a beautiful atmospheric piece with voices that
deepen the narrative, a death whistle interruption, and a folk flute outro.

The three-part human dialogue is there. One statement. One challenge. One
shattering. The listener may not know it's dialogue. But they will hear the
shift. From certainty to question to breakdown. That's the reckoning.

The rest is already in there.

---

*Draft 1. Iterate freely. The well doesn't care about versions.*
