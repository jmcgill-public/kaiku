# kaiku

An FM synthesizer. 6 operators. 3 parallel stacks. 16 voices.

Built to approximate two things that don't exist inside it: a hurdy gurdy wheel and a human mouth.

Primary target: REAPER on Linux. Also ships Windows and macOS.

KVR: [kvraudio.com/forum/viewtopic.php?t=629750](https://kvraudio.com/forum/viewtopic.php?t=629750)

---

## on the grilli

*The grilli menu is the version. What's smoking is what's shipping or nearly shipping.*

**v0.1**

You will regret playing either of these. If you want to hear Kaiku in her first iteration, she's there. You were warned.

- kuule — [rebraining.org/kuule](https://rebraining.org/kuule)
- birch — [rebraining.org/birch](https://rebraining.org/birch)

Both render in fosfori. Void black. No chrome. Bring headphones.

---

## the repo

```
games/    browser compositions — the open door
comp/     scores, notes, prose from the universe
ir/       impulse responses and provenance
arch/     technical commons
vsti/     synthesizer design and source
contrib/  how to read this, style guide, conduct, mission
```

---

## why vsti/ has no code

The instrument's scope is still changing to meet the composer's needs. The proof of concept lives in the web audio implementations in `games/` — that is what Kaiku sounds like right now, at this minute, and it is enough to work from. The third reason is left as an exercise.

AI assistance is being used in the development of this instrument. This is not vibe coding.

*(It is, though.)*

The spec is in `vsti/SPEC.md`. Source is in the feature branch, as-is, uncompiled. Main holds the contract.

---

## contributing

Start with [contrib/READING.md](contrib/READING.md) — it will tell you what's load-bearing and what's depth. Make a PR.

---

## a note on ai usage

[contrib/AI.md](contrib/AI.md)
