# games

Two browser compositions. Web Audio API. No dependencies. Each runs in a single HTML file.

These are finished musical works. They are also the public demonstration of the Kaiku sound vocabulary — the entry point before the synthesizer itself exists as a distributable.

---

## kuule

Station Nine — a Simon-pattern memory game on a hex grid. Eight stations. A glyph tray that accumulates on progress.

The audio engine: sawtooth oscillators through a lowpass filter. Two voices per tone, the second running 8 cents sharp against the fundamental. The beating between them is the wheel. A 0.15Hz tremolo runs continuously — the Hiljaisuus pulse. The drone underneath the game never stops.

Live: [rebraining.org/kuule.html](https://rebraining.org/kuule.html)

---

## birch

A birch glyph tool and palette explorer. An 8-tile sliding puzzle using station glyphs, a parametric birch tree renderer, Finnish move counting, a season bar.

The audio engine: sine oscillators through a lowpass filter. Two voices per tone, interval-separated. Voice 2 is slightly darker — lower filter cutoff, lower tremolo depth. Both voices tuned 8 cents flat. The instrument is warm, imprecise, and correct. The forest breathes at 0.15Hz underneath the duo.

Live: [rebraining.org/birch.html](https://rebraining.org/birch.html)

---

## shared architecture

Both compositions:

- run exactly 13 minutes
- use F# Phrygian throughout (G natural is always present — the characteristic semitone, the pull toward the root)
- breathe at 0.15Hz
- fade to silence in the final 30 seconds
- were composed in a while loop — duration variation is in the architecture, not added afterward
- use no samples, no wavetables, no external dependencies

The 8-cent detuning is not an error. Do not tune it out.

For synthesis architecture detail: `arch/webapi.md`.
