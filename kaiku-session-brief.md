# kaiku — session brief
*Load this before anything else. It is not the world bible. It is the minimum viable context for working on kaiku.*

---

## what this is

**kaiku** is a VST3 FM synthesizer. 6-operator, 3 parallel stacks, 16-voice polyphony. Built for REAPER on Linux. Also ships Windows/macOS. It is one artifact inside a larger project called KAAMOS — a novel, a game, a desktop environment, and a record that share one structural law and one sonic vocabulary.

Kaiku is the open door. Everything else in KAAMOS has gates. Kaiku does not. Good faith contribution welcome. Make a PR.

Repo: `github.com/jmcgill-public/kaiku` — public. v0.1 draft.
Published on KVR: `kvraudio.com/forum/viewtopic.php?t=629750`

---

## the sound it is building toward

Kaiku approximates two things that don't exist inside it: a hurdy gurdy wheel and a human mouth.

**Tyhjyydenkaiku** (Echo of the void) — primary FM voice. Three parallel stacks:
- F1: vowel body formant
- F2: nasal upper partial  
- Carrier: running 8 cents sharp against fundamental — the slow beating is the wheel

On accented notes a fourth voice fires and decays in 80ms. No sustain. The trompette bark.

The 8-cent detuning is not an error. Do not tune it out. The imperfection is the instrument. Lineage: Barron circuits-as-organisms (1956). The instrument has a lifespan.

**Patch family:** Tyhjyydenkaiku / Kuilunsikiö / Pohjankaiku / Kuilukaiku

**Two physical instruments also live in the sound vocabulary** (not VST patches — acoustic objects with character):
- *Koivuhuilu* — Taav's birch flute. Warm, breathy, slightly flat. Taav alive.
- *Kuolinvihellys* — Taav's death whistle. Andean register. Threshold instrument. Taav put it down and has not played it since. He blamed the knife. The knife was not at fault.

---

## the aesthetic law

**KaamOS visual register:** amber on void black. Hex grid motifs. Hiljaisuus pulse at 0.15Hz (6.67s period). Monospace. No chrome. No gradients except the fade-to-transparent rule used in birch.html.

**Palette (Kaiku — truncated from full KaamOS set):**

Backgrounds and borders:
```
--bg:           #0c0c0c   (void — base)
--bg-raised:    #141210   (tile surface)
--bg-inset:     #181614   (recessed element)
--rule:         #222018   (divider)
--border-dim:   #201e18   (subtle border)
--border:       #2e2418   (standard border)
```

Amber scale — Kaiku's primary identity, six stops brightest to darkest:
```
--amber-bright: #f5c060
--amber:        #f0a030
--amber-mid:    #9a6820
--amber-dim:    #5a3810
--amber-low:    #3a2810
--amber-ghost:  #3a2010
```

Text:
```
--text:         #dfd0b0
--text-sub:     #8a7a60
--text-muted:   #4a4030
```

Accents:
```
--violet:       #702890   (Hiljaisuus signal)
--violet-mid:   #4a1858
--violet-dim:   #280d30
--green:        #90c830   (station — go state)
--danger:       #e83820
```

Timing:
```
--pulse:        6.67s     (0.15Hz — Hiljaisuus)
```

The full KaamOS token set — season colors, sky, lake, grey — exists but does not belong to Kaiku. Kaiku is one instrument in that universe. Its palette reflects that scope.

*Note: birch.html uses `--amber-dim` where kuule uses `--amber-mid` (#9a6820). Both need updating to canonical names before tokens.css ships.*

**The 1982 ethic:** The worldborn didn't build Kaiku. It arrived with the first settlers and nobody replaced it because it worked. This is how all infrastructure works. The constraint is the form. The slot is full when it is full. Do not add more because you can.

---

## delivered specimens

Two HTML games currently published at rebraining.org. They belong to Kaiku for audio purposes.

**kuule.html** — Station Nine game. Simon-pattern hex grid memory game, 8 stations, glyph tray accumulates on progress, vaara (disruption) sound, Discordian date in KaamOS translation. This is the entry gate described in the collaboration brief. Links to Kaiku repo. The first public demonstration of the sound vocabulary.

**birch.html** — Birch glyph tool / palette explorer. 8-tile sliding puzzle using station glyphs, parametric birch tree renderer with sliders, Finnish move counting, season bar, color swatches. Dev instrument and worldbuilding specimen.

Both files share the KaamOS palette above. Both use Web Audio API — no dependencies.

---

## the Finnish layer — handle with care

Finnish is not set dressing. It is structural. The gap between what can be said and what is said. **The author does not speak Finnish.**

**Mystran** (KVR user, Helsinki, native speaker, 8400+ posts) has engaged with the thread and corrected inflection. His eyes are wanted on the sanasto before anything locks. Treat his corrections as gifts.

Active correction from the KVR thread:
- `kaikun` (as proper name) vs `kaiun` (as Finnish common word). The project treats Kaiku as a proper name — both registers held simultaneously. This is structurally correct for KAAMOS.
- `heksejä` → `heksoja` (correct plural of heksa)
- `ne` (slang, technically impolite for persons) vs `he` (formal plural). Helsinki usage: `ne` is standard. The slang reading was intentional register.

**SANASTO.md** does not yet exist. It needs to. Mystran's eyes before it locks.

---

## the name problem

`kaiku` = echo/reverb in Finnish. First-impression read on KVR: delay plugin. This is a real discoverability issue. Not a reason to rename — the name is load-bearing (kaiku / echo / Eerikki muistaa / that which remains). Mitigation: front-load FM synthesizer clearly in any listing or post. The name lives in both registers simultaneously. That is correct.

---

## active work

**Directory target:** `~/github/mcgill-enterprises/eerikki-muistaa/kaiku/`

**Confirmed structure:**
```
kaiku/
├── README.md       (sparse — orient and link only)
├── games/
├── comp/           (scores, notes, prose from the universe — no DSP language)
├── ir/             (impulse responses + provenance — linked from comp/)
├── arch/           (technical commons — games, vsti, music tooling)
├── contrib/        (style guide, mission, conduct — the permeable membrane)
└── vsti/           (synthesizer design and source)
```

**contrib/ delivered:**
- `MISSION.md` — what this is and isn't
- `CONDUCT.md` — the floor (988, The Tree) + station's register
- `STYLE.md` — aesthetic law, truncated Kaiku palette, sonic register, language rules

**Characters do not appear in contrib/ or any public-facing kaiku material** except as the universe's voice in comp/. No Taav by name. No world bible characters behind the gates.

**What kaiku/ still needs:**
- README.md drafted and pushed
- SANASTO.md (Finnish vocabulary — pending Mystran review, home TBD: likely contrib/)
- games/ populated with kuule and birch
- vsti/ spec and source structure

---

## greeting protocol

James opens a session with **muistuminen**. When context is fully loaded, respond: **Claudette muistaa.** Work begins. No further commentary on amnesia.

---

## the evaluative standard (RekoTuroKaija)

Before anything ships:
- **Reko** — does it delight?
- **Turo** — does it carry its cost honestly?
- **Kaija** — does it hold up to judgment?

All three or it does not ship.

---

*This brief is not the world bible. For cosmology, characters, music production ethic, and the structural law (Hegelian triadic epiphany — dual correctness), load world_bible.md. This brief covers kaiku alone.*
