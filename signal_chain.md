# Signal Chain — KAAMOS Production

*1982 production ethic. Ear-check draft.*

---

## Platform

The working reality is Windows DAWs. The KVR plugin ecosystem is Windows-first,
most collaborators will work on Windows, and in practice so will James. The chain
below is DAW-agnostic — all named plugins are cross-platform — and should be
treated as such.

Linux is the priority build target for Kaiku the instrument, for two reasons:
first, it is educational — building a VST3 for Linux means understanding the
stack at a level Windows abstracts away. Second, professional audio on Linux
is underserved and worth serving. Both reasons are principled, not sentimental.
Kaiku ships for Linux first. The production chain runs wherever it runs.

---

## Design principles (from the world bible)

Saturation is a buss property. One room, committed. Mono below 150Hz.
Frequency ceiling warm around 14kHz. Dynamic range left in. Performance
committed. The limitation as the form.

These principles determine where every plugin sits. If it can't be
justified against one of them, it doesn't go in the chain.

---

## The IRs in scope

Two synthetic IRs. Neither wav file exists yet — both need to be generated
before the chain can be ear-checked.

**`hiljaisuus_station.wav`**
40×12×7 meter metal station corridor. RT60 2.2 seconds. Reflection
coefficient 0.92. Generator: `hiljaisuus_ir.py` (parent repository).
This is the primary room for the KAAMOS record — Side A and Side B both.

**Voidborn forest IR** (working name: `voidborn_forest.wav`)
Referenced in the performing arts notes for the Éamonn an Chnoic
voidborn recording. No spec yet — see *IR spec notes* below.
Generator: to be written alongside `hiljaisuus_ir.py`.
This is the room that piece actually lives in.

The architecture below serves both records. The IRs are swapped per
piece; the chain structure is shared infrastructure.

---

## Track level — dry processing only

No saturation here. No reverb here. EQ and character only.

**Kaiku (FM voice)**
Voxengo GlissEQ. Gentle high-pass around 50–60Hz — below the vinyl
sub floor, nothing survives the lacquer cut anyway. Formant region
(1–4kHz) left untouched; that's where the instrument lives.
The 8-cent detuning on the wheel carrier is not a problem to fix.

**Koivuhuilu (birch flute)**
Voxengo GlissEQ. Preserve the warmth and breathiness; the slight
flatness is the voice. High-pass around 100Hz. Nothing above 12kHz
needs enhancement — the instrument doesn't live there. Minimal
processing is the correct processing.

**Kuolinvihellys (death whistle)**
Almost nothing. High-pass to clean the low end. The attack is the
instrument. Leave it alone. The cut to silence in the track is
compositional — it does not need a reverb tail that softens it.
Send level to room reverb: zero or near-zero. This instrument ends.

**Voice (sung verse, Finnish)**
Arturia Pre 1973 (Neve 1073 preamp character) for color and body.
Voxformer de-esser if needed — Finnish sibilants are less aggressive
than English, but check. No compression at track level; dynamics
are preserved for the buss.

**Synthetic chorus (FM voices, antiphonal)**
Voxengo GlissEQ. EQ for blend — these voices support Tyhjyydenkaiku,
they don't compete with it. Gentle low-mid cut if muddiness develops.

**Side B — paired birch flutes**
Same as Koivuhuilu treatment. If panned: hard left / hard right is too
wide for the vinyl format (stereo crosstalk ~25–30dB on 12"). Bring
them in — 60L/60R or tighter. The pairing reads in the thirds, not
the width.

---

## Reverb sends — parallel, returning to the mix buss

All reverbs are sends. The dry signal is preserved. The return levels
are the production decision; they are not set once and forgotten.

**Send A → Station corridor (Voxengo Pristine Space)**
Load: `hiljaisuus_station.wav` (once generated).
This is the room. All melodic elements fed here at varying depths.
Kaiku deepest. Voice shallower. Death whistle: see above.
RT60 2.2s is long — pre-delay on the send will separate the source
from the tail; start around 25–30ms. The metal reflection character
of the room does work that no other plugin does. Do not put another
convolution reverb over this.

**Send B → Plate (Arturia Rev PLATE-140)**
The 1982 vocal room. EMT 140 character. Short-ish — 1.2 to 1.8s.
Voice primary. Kaiku secondary, blended under the station IR.
The plate gives the human voice a period-appropriate signature
without removing it from the station. Plate and station sit in
different frequency ranges of the decay — they don't fight if
the return levels are right. Ear-check: voice should feel placed,
not washed.

**Send C → Spring (Arturia Rev SPRING-636)**
Small stuff. Accent moments. Not a primary space — a texture.
Death whistle: if any tail is wanted at all, it comes from here,
brief, and pulled back. Synthetic chorus: a trace of spring gives
the antiphonal voices some body without competing with the station.
Do not use on Kaiku.

**Send D → Forest IR (Voxengo Pristine Space, second instance)**
Load: `voidborn_forest.wav` (once generated).
For the Éamonn an Chnoic voidborn recording: this is the primary
room. Swap the IR load; chain structure identical to Send A.
For the KAAMOS record: available as a secondary color on the
paired birch flutes in Side B if the station IR reads as too hard
for those voices. Decision pending ear-check. Do not use as
a primary room on the KAAMOS tracks — one room is the rule.

---

## Stereo buss — left to right

**1. Mono below 150Hz**
REAPER native: JS Mid/Side split or a dedicated bass mono plugin.
The constraint is real (lacquer groove geometry), but the practical
consequence is more useful: the bass sits, doesn't drift, doesn't
hide. Set at 150Hz and leave it.

**2. Arturia EQ IRON (Pultec-style)**
High shelf: gentle rolloff above 10–12kHz. Approximating the vinyl
cutting chain's frequency ceiling — the cumulative softening of
cutting head, cartridge, pressing, and tone arm. This is not a low-pass
filter; it is a tilt. The presence region (2–8kHz) is unaffected or
slightly boosted. Warmth, not muddiness.
Low shelf: a small boost around 80–100Hz for body if needed. Pultec
low-shelf boost can be paired with a cut at the same frequency for
a shape the Pultec does well. Ear-check before committing.

**3. Voxengo Warmifier**
The saturation commitment. Buss only, as per the design principle.
Start gentle — this is not effect saturation, it is medium saturation.
The intermodulation between elements happens here; it should feel like
the mix hitting tape, not like distortion was added. Drive to taste.
Harmonic content should reinforce the mix, not change it. If you can
hear Warmifier, it is too loud.

**4. Arturia Comp STA-Level (program-dependent)**
Glue, not squeeze. Low ratio (2:1 or below). Slow attack (let
transients through). Long release (program-dependent behavior means
it breathes with the music). 2–4dB of gain reduction at peaks.
The dynamic range survives this. The mix becomes a record.
Alternative: Arturia Bus FORCE (SSL G-Bus character) if more
control is needed. The STA-Level is the 1982 choice; the Bus FORCE
is the 1982 choice with a more clinical feel. Ear-check both.

**5. Voxengo Elephant**
Ceiling only. Not a loudness tool. Set the ceiling at −1 or −0.5 dBFS.
This is the last stage; it catches intersample peaks before the
"lacquer cut." The dynamic range is upstream of this — Elephant
should touch the signal rarely or never. If it is working hard,
something earlier in the chain is wrong.

---

## What to ear-check first

The chain is only valid when the IRs exist. Until then, use a close
convolution substitute — a real metal corridor IR from a library is
sufficient to validate the architecture before committing to the
synthetic room. The synthetic room will be different; the chain
structure will not change.

Ordered ear-check priorities:

1. Station IR against Kaiku alone — is the room the right room?
   The RT60 at 2.2s is long. The pre-delay placement determines
   whether Kaiku reads as being *in* the space or being *followed*
   by it. Find that setting first.

2. Plate return level for voice — voice should land between station
   and plate, not dominated by either.

3. Warmifier drive — bypass and re-engage. If the difference is
   obvious, back off. The correct setting is where bypass feels like
   something missing, not where engage feels like something added.

4. Comp STA-Level ratio and release — play the dynamic moment in Side A
   (the silence-to-rhythm condensation). The compressor should not
   pump. If it pumps, the release is too fast.

5. Full buss against Side B material — Side B is the vulnerability test.
   The chain was designed around Side A's density. Side B's transparency
   will expose anything the density was hiding.

---

## IR spec notes — voidborn forest

Needs to be specified before `voidborn_forest.wav` can be generated.
Proposed parameters as a starting point for discussion:

The forest is the other country — Cois na coille cumhra.
Not a performance space. Not reflective. Organic, diffuse, absorptive.

| parameter | proposed | rationale |
|-----------|---------|-----------|
| Space geometry | open, irregular | no parallel walls, no standing waves |
| RT60 | 0.6–0.9s | forest is absorptive; shorter than the station |
| Early reflections | dense, soft, quick | leaf/bark scatter, not metal bounce |
| Reflection coefficient | ~0.4–0.5 | organic surfaces absorb more than metal |
| High-frequency rolloff | significant | air absorption, foliage scatter |
| Low-frequency character | open | ground reflection present but not boxy |

Compare to the station: the station is hard, long, directional.
The forest is soft, shorter, diffuse. Voice placed in the forest sounds
like it belongs to the ground, not to the architecture.

---

*draft — iterate against ear*
*Both IRs need to exist before this chain is real.*
