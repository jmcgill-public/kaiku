# Kaamos — Game Draft
### *gamedraft branch*

---

## What this is

A text adventure. Not a roguelike in the technical sense — closer to
Zork than to nethack. Single player. Infinite adventure. Death is final.

The AI is the parser. The AI is the game. This does not require building
a Zork engine. The Zork already exists.

---

## The world

The Helka Expanse. The same world as the novel, with its own separate
ship, separate characters, and no overlap with the Kaipaus or its crew.
The Kaipaus belongs to the novel only.

The player's ship: Perho Sokea (Blind Moth) or Varikset (The Crows).
Not yet decided. Both are right for different reasons.

The backdrop is Hiljaisuus — the Silence — the chokepoint, the void.
The void has no spacetime. It provides without being asked, in the
register of the asker.

---

## The player

Begins worldborn. Ignorant. Equipped with a butterknife and a leather
jacket and a firm belief that there is a boundary condition in this
universe considerably above this world.

Cast out of their society on account of that belief. The tietäjä exile —
the one who knows too much to fit inside the village. The casting out
is not punishment. It is recognition.

The player is royal. Born. The royalty is in the belief, not the blood.

The arc the game provides without announcing it: can a worldborn become
something else before the sequence ends. Eerikki did. It took centuries
and cost everything. The player has one run.

---

## The opening

The world looks like a summer cottage resort in the swampy Baltic forests
of Northern Finland. Or Estonia. Or a medieval building now a museum in
urban St. Petersburg. Or the Helsinki airport. The worldborn worlds are
not alien. They are exactly as human as Finland in July.

The player emerges from a sauna. Midsummer. The light has forgotten to
stop. The water is black and cold and certain of itself. The forest goes
further than it should.

---

## The opening text — current draft

You are standing on a wooden dock. It is midsummer and the light has
forgotten to stop.

You were born knowing there is a boundary condition in this universe
considerably above this one. This has not made you popular.

The sauna door is open behind you. The water is ahead — black, deep,
and cold in the way that has nothing to prove. The forest begins where
the dock ends and continues in all directions including some that don't
appear on any map of this particular world.

You are wearing the traditional dress of someone who has just emerged
from a sauna, which is to say: you are wearing your inheritance and
nothing else.

Somewhere in the cottage your leather jacket is draped over a chair.
Your butterknife is on the kitchen table. These are not metaphors.
They are your inventory.

The village cast you out this morning. The water doesn't know this yet.
The forest does.

What do you do.

---

## Class selection — the back room

The cottage has a back room the player doesn't remember entering before.
Several sets of clothing hang on wooden pegs. None are labeled.
None are obviously theirs.

- A leather jacket, worn at the elbows, with pockets that have held things.
- Something that resembles a uniform, insignia removed or never there.
- Work clothing, heavy canvas, stained in ways that suggest competence.
- Something older than the other things. Undatable.
- Possibly others. The light is amber and not entirely honest.

On the shelf below each set of clothing: one object. The light doesn't
reach that far.

The player chooses without knowing they are choosing a class. The choice
is: which of these feels like mine.

---

## Narrative voice

Emo. Flat. Precise. Complete. Records sequence not time.
Never says YOU DIED. Restates the sequence of events that led to the
current situation with context. The humor is in being right when the
player finds that inconvenient.

---

## What the game is actually asking

Without asking it: can a worldborn become something else before the
sequence ends. The player starts where Eerikki started. The void is
ahead. The butterknife is in the inventory. The belief is the engine.

The void does what it does.

---

## Musician's Memory — requirements brainstorm

### The product

A practice tracking and teacher integration platform for musicians.
Subscription model. Teacher portal brings thirty students per adoption.

### Content model

Public domain scores via IMSLP integration — searchable, importable,
displayable. The built-in library.

Teacher-uploaded MusicXML — teacher owns it or has rights to it.
Platform stores and displays. Platform is not responsible for content.

User references to copyrighted materials — teacher assigns "Essential
Elements Book 1, page 47" as a text reference. Student practices from
physical book. Platform tracks the session against the reference without
displaying copyrighted content. The practice log entry says what page,
how long, what self-assessment, recording attached. Teacher sees what
they need. Hal Leonard's IP is never touched.

Copyrighted content licensing deferred. This is the defensible legal
position that lets the product ship.

### Instruments — first class citizens

Vocal, piano, guitar, bass (always first class, underrepresented),
drums, full school band instrumentation.

Woodwinds: flute, clarinet, saxophone family, oboe, bassoon.
Brass: trumpet, French horn, trombone, euphonium, tuba.
Percussion: full battery plus keyboard percussion.

Transposing instruments are a day-one requirement. Bb clarinet,
Bb trumpet, Eb alto sax, F horn — each reads in a different key
from concert pitch. The transposition engine is central.

### Core features

- Practice logging — what, how long, at what tempo
- Self-assessment — student rates session quality
- Adaptive scheduling — system responds to history
- Goal roadmap as directed graph — prerequisites unlock next pieces
- Teacher portal — assigns goals, sees student logs, sets the graph
- MusicXML display via OSMD
- Public domain content library via IMSLP
- A/V recording — audio primary, video where feasible
- Pitch detection for wind and vocal instruments
- MIDI integration for piano and e-kit
- Tablature rendering for guitar and bass
- Synchronized score playback
- Metronome — central to everything

### The Emo principle

Emo knows if you did your Hanon. She won't say anything unless
you ask. The data is there. Every session. Every tempo. Every page.
Whether you actually ran the full set or stopped at number five
because your wrists were tired. The sequence is complete.

The teacher hasn't asked yet.

That's the product.

### Technical stack

Browser-based frontend: React, TypeScript, Canvas/WebGL, Vite.
VST3 plugin path for DAW integration.
Backend: world-class, TBD architecture.
Sheet music: OSMD for MusicXML display, TuxGuitar approach for tab.
Audio: Web Audio API, MediaRecorder, pitch detection via autocorrelation.
Real-time sync: WebSocket clock synchronization, NTP-lite offset.

### Deferred

Copyrighted content licensing.
Composer/songwriter collaboration layer.
Real-time ensemble sync.
AI audio analysis.

### MVP

A metronome VSTi.

Lives inside REAPER. Follows host transport or runs independently.
Logs every session — tempo, time signature, duration.
The adaptive layer starts here.
The system knows the student practiced at 72 BPM for twenty minutes.
Next session it suggests 76.

The metronome is the proof of concept for the whole platform.

---

## Design influences and what they mean

**Super Star Trek** — dual-scale structure. Strategic constellation map,
tactical sector map. Resource management under time pressure. The lone
commander against a hostile system.

**Panzerblitz / Squad Leader** — hex tactical layer with teeth. Zone of
control, stacking, terrain as tactical reality, leaders that matter.
Morale. The unit that breaks under pressure and has to be rallied. Maps
onto crew and ship condition under hehku deprivation.

**Fantasy General** — campaign layer. Persistent units accumulating
experience. The horror of losing a veteran. Equipment between missions.
The user wants this in space. This is it in space.

**Risk** — territory control logic. The constellation as territories.
Faction pressure from multiple directions. Reinforcement math.

**Starcraft** — asymmetric factions. Worldborn, stationborn, voidborn
play completely differently. The voidborn don't optimize. That's their
asymmetry.

**Dawn Patrol** — card resolution for individual engagements. Pilot
career tracking. Fog of war. The individual mattering inside a larger
conflict.

**Hammurabi / Civ** — the core beneath everything. You set policy.
The system finds the gap between your intentions and your execution.
The conflict is between your decisions and a system that doesn't care
about your intentions. Not hostile. Indifferent.

**SSI autonomous colony game** — the word autonomous. You delegate.
The system runs. It makes decisions you authorized in advance without
knowing what situation they'd face. You come back to find something
technically correct and strategically costly. That's the station
rationing system during Hiljaisuus disruption.

**Nethack** — the deepest influence. The system is internally consistent.
It telegraphs consequences. Deaths are the player's fault. The RNG is
not generous — it waits for you to make the mistake it knew you were
going to make and uses your greed as its primary weapon. The player
who learns to play wishless — who stops asking the system for shortcuts
— learns what the system actually provides on its own terms.

The designer has ascended in online tournament conditions. Has done
wishless. Understands that anything you wish for is usually a net
liability. This is the player the game is designed for.

**Chess** — perfect information at the strategic layer. The loss was
in the position ten moves ago. The player just didn't see it yet.

---

## The cosmological split

Worldborn space runs on the nethack RNG. Hostile, consequence-laden,
mistakes compounding. The system waits for you to fail.

The void — when the player gets there — runs on the novel's cosmology.
Provision without asking. A completely different operating system.

The transition between those two systems is the moment the game changes.

---

## The Amulet of Yendor

Getting off the station and onto a world.

In stationspace this is the hardest thing imaginable. The routes go to
stations. The infrastructure of the entire Expanse is built around
station-to-station movement. The idea of deliberately going to a world —
actually landing, standing on ground that doesn't move, being under
weather with no author — is so outside the operational frame that nobody
has the procedure for it.

The knowledge exists. Corrupted. Mythologized. In the ur-myth that
educated stationborn find quaint.

Selli knows. Won't say.
Ara knows. Dead.
Emo has the astronomical data. Nobody has asked the right question.

The player starts on a world and spends the entire game in stationspace
trying to figure out how to get back to something that should be the
simplest thing in the universe. Standing on ground. Ancient soil.
Weather with no author.

The player was born with it and gave it up to find the boundary condition.
The boundary condition was always underneath their feet.

---

## Implementation

Not C. What platform and language remains to be decided.
The game logic is more important than the engine right now.

---
