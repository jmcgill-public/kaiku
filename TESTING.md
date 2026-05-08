# kaiku — eval brief

How to test the instrument before it ships.

---

## Setup

**Host:** REAPER. Any version that loads VST3.

**Tempo:** Set REAPER project tempo to **40 BPM** before loading any eval MIDI.
REAPER ignores the MIDI file's embedded tempo and uses the project tempo.
At 40 BPM: 6s sustain, 6s rest per note. At 120 BPM (REAPER default): 2s/2s — too short to evaluate decay or IR tails.

**Gain:** One instance of Kaiku per MIDI track for solo tests. For ensemble, pull each track fader to **−14 dB** before rendering — five voices at unity will clip (+14 dBTP).

---

## Files

**Score sheets** — `comp/exercises/`

| file | voice | sounding range |
|---|---|---|
| `fsharp_phrygian_contrabass.ly` | contrabass | F#1–F#2 |
| `fsharp_phrygian_low_tenor.ly` | low tenor | F#3–F#4 |
| `fsharp_phrygian_lyric_soprano.ly` | lyric soprano | F#4–F#5 |
| `fsharp_phrygian_piano.ly` | piano (2 hands) | B1–B5 |

**MIDI eval suite** — `sounds/eval/`

| file | type | content |
|---|---|---|
| `eval_contrabass.mid` | Type 0 | 8 notes, F#1–F#2 |
| `eval_low_tenor.mid` | Type 0 | 8 notes, F#3–F#4 |
| `eval_lyric_soprano.mid` | Type 0 | 8 notes, F#4–F#5 |
| `eval_piano.mid` | Type 1, 2 tracks | treble 11 pitches (F#4–B5), bass 18 pitches (B1–F#4) |
| `eval_ensemble.mid` | Type 1, 5 tracks | all voices, channels 0–4, synchronized |

All MIDI: 40 BPM, TPQN 480, whole note + whole rest, sounding pitch.

**Renders** — `sounds/eval/`

| file | status | notes |
|---|---|---|
| `Contrabass-001.wav` | ✓ clean | baseline solo reference |
| `Ensemble_Preset_2.wav` | ✓ clean | baseline ensemble reference |
| `Contrabass.wav` | legacy | 120 BPM (short notes) — discard |
| `Ensemble.wav` | clipped | +9.4 dBTP, gain staging failure — discard |

---

## What to listen for

### Pitch

The F# Phrygian scale ascending: F#, G, A, B, C#, D, E, F#.

Each note should land on the correct scale degree and hold without drift.

**Known property:** a consistent +1–4¢ sharp offset across all patches and voices. This is stable — the Cw wheel stack at 1.008× interacting with the tuning reference. It is not a defect. It is the instrument. Flag any pitch that drifts *within* a sustained note, or any note that misses its scale degree.

### Patch character

Run each solo MIDI through all four patches:

| patch | what you are listening for |
|---|---|
| **Tyhjyydenkaiku** | the wheel beating — slow amplitude modulation from Cw at 1.008×. Present on every note across the full range. This is the instrument. |
| **Kuilunsikiö** | visceral, before-it-becomes-sound quality. Rougher than Tyhjyydenkaiku. |
| **Pohjankaiku** | Mellotron weight. Slower attack character. The echo across the north. |
| **Kuilukaiku** | stripped. The wheel alone. No formant body. Should feel sparse. |

### Range consistency

Check that each patch holds its character from the bottom of the range to the top. Specific things to flag:

- F#1 (contrabass low) — present and defined, not thin or missing
- F#5 (soprano high) — in character, not hardened or distorted
- Level variation across the scale — up to ~3 dB natural variation is expected; more than that is worth noting

### Trompette

On accented notes (high velocity), a fourth transient voice fires and decays in 80ms. This is the trompette bark. The eval MIDIs use moderate velocity (80) and may not trigger it. Test separately with a high-velocity note to confirm the transient fires and decays cleanly.

### Ensemble

Load `eval_ensemble.mid`. Five parts on channels 0–4: lyric soprano, low tenor, contrabass, piano treble, piano bass.

After gain staging (−14 dB per track or master):

- Listen for beating artifacts between voices on shared pitch classes (contrabass and soprano share F# an octave apart — interaction is expected; the question is whether it is musical or phasey)
- Check that the wheel beating in Tyhjyydenkaiku adds rather than subtracts across the 4-octave stack
- Confirm the bass register (F#1) is audible and not masked

---

## IR evaluation

Not part of the pre-release eval. Scheduled for next phase.

When ready: use `Contrabass-001.wav` as the dry reference. Run through `ir/hiljaisuus_station.wav` in REAPER (ReaVerb). Compare dry and wet at matched levels. Listen for tail length, color, and whether the room complements or obscures the wheel beating.

Flag: any additional clipping in the wet signal. The +0.8 dBTP intersample peak present in the dry solo render may compound through convolution.

---

## Render settings

- Format: WAV, 48kHz, 16-bit
- Target peak: −5 to −6 dBFS sample peak
- Check true peak (dBTP) in render stats — flag anything above 0 dBTP
- Check integrated LUFS — solo reference is −6.1 LUFS; ensemble reference is −14.6 LUFS

---

*Cross-ref: `vsti/SPEC.md` — patch topology and Cw detuning*
*Cross-ref: `ir/` — impulse responses*
*Cross-ref: `zds/kaiku/release_eval.md` — ZDS operational procedure*
