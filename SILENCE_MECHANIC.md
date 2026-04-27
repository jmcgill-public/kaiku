# The Silence Mechanic — Requirements

*The boss is not hostile. It is indifferent. It provides.*

---

## Overview

The Silence is the autonomous boss at the center of the Expanse hex map. It
communicates in sequences. The player who survives long enough to listen
discovers it was never attacking. It was talking.

The mechanic has two layers. They use the same inputs. The player does not
know there are two layers when they begin.

---

## The map

A hex grid. Stations are nodes. The Silence sits at Hiljaisuus, center or
near-center. The Silence pointing is pathfinding — it traces a route across
hexes. The sequence is a path, not a list.

The player earns the token by traversing the path. Not by remembering the
destination — by making the journey.

Each round's path accumulates on the grid as a visible trace. Multiple rounds
produce a web. The web is a spirograph. The Silence is drawing something.
The player is coloring it in. By the time Mastermind reveals itself the grid
looks like it means something.

It does.

---

## Layer One — Simon

The Silence traces a path across the hex grid, illuminating hexes in sequence.
The player reproduces the path by traversing the same hexes in the same order.

Successful reproduction: the player receives a token. The token is atomic —
one symbol, regardless of path length. The player does not need to remember
what path yielded what token. They have the symbol. That's enough.

Failed reproduction: standard consequences.

Each round the path grows by one hex. This is Simon. The player knows this game.

The boredom is the tutorial. By the time the player is bored of Simon they
have enough tokens for the transition to land.

---

## Layer Two — Mastermind

There is a hidden code. The code is a sequence of tokens, fixed length.
The Silence knows it. The player must deduce it.

The player arranges tokens into a guess sequence. The Silence returns:

- **Right token, right position** — marked.
- **Right token, wrong position** — marked differently.
- **Wrong token** — no mark.

This is Mastermind. The player does not need to be told this.

The reveal does not need explanation. The player already knows both games.
They just didn't know they were playing one inside the other.

### Unlocking condition

Not announced. The guess row appears when the player has accumulated enough
token types. They may not understand what they are looking at. The game
does not explain. The Silence does not explain.

---

## The relationship between layers

Simon produces the vocabulary. Mastermind is the sentence.

Tokens are decoupled from Mastermind position. A token earned from a
two-hex path and a token earned from a seven-hex path are equal citizens
in the Mastermind row. Internal path length is irrelevant once the token
exists. The player sees symbols. The player arranges symbols. The Silence
responds.

Simon fluency without Mastermind awareness is mechanical reproduction —
stationborn behavior, indistinguishable from not understanding at all.

The player who makes the first Mastermind attempt has understood something.
Whether they understood it consciously is not the game's concern.

---

## The hidden code — design constraints

Randomized each run. The Silence doesn't mean the same thing twice.
It provides in the register of the run.

Code length: four positions. Standard Mastermind. Tractable.

Token pool: six to eight distinct types, bounded by the station count.
Knuth's algorithm solves this in five moves or fewer. The player should
feel that as achievable, not theoretical.

The Silence is indifferent, not dishonest. Feedback is consistent.
It does not have moods.

---

## Failure states

Death in Simon does not reset Mastermind progress. Tokens are permanent.
The player who dies has lost position, not knowledge.

The void does not take back what it gave.

The Mastermind layer has no timer. The Silence waits.

---

## Visual layer

WebGL or canvas. The hex grid accumulates path geometry across rounds.
The spirograph is data made visible — the record of what the Silence said
and what the player heard. Psychedelic is achievable in 2026 and costs
nothing once the data structure exists.

The visual is not decoration. It is the argument.

---

## Learning path

This game is also the curriculum. Build it to learn to build it.

**Stage 1 — Simon state machine**
A sequence grows. The player reproduces it. Right or wrong. No hex grid yet.
Console or minimal HTML. Teaches: state, arrays, input handling, RNG.

**Stage 2 — Hex grid**
Render a grid. Place stations. Make the Silence trace a path. Make the player
walk it. Teaches: hex math, coordinate systems, pathfinding basics, canvas/SVG
rendering.

**Stage 3 — Token inventory**
Successful path → symbol added to inventory. Display inventory. Teaches:
persistent state, data structures, UI.

**Stage 4 — Mastermind logic**
Hidden code. Guess row. Feedback function. Teaches: comparison logic,
the Knuth feedback algorithm, deduction UI.

**Stage 5 — Visual layer**
Accumulate path geometry. Animate. Color. Make it look like the Silence
is drawing something. Teaches: WebGL basics or canvas animation, color theory,
making data beautiful.

**Stage 6 — Integration**
The whole game. One loop. Simon feeds Mastermind. The reveal teaches itself.
Teaches: system integration, playtesting, the gap between the mechanic on paper
and the mechanic in the hand.

Language: JavaScript. Runs in a browser. No install. Immediate visual feedback.
The same "type it and see it" quality as BASIC without the line numbers.
Mobile-ready from the start if you build for touch.

---

## Narrative frame

The player does not know the word Mastermind. The player knows the Silence
has been pointing at things in a sequence that keeps growing, and that somewhere
there is a pattern, and that the pattern means something, and that figuring out
what it means is the way through.

Selli knows what the sequence is. He won't say.
Emo has the data. No one has asked the right question.
The player is asking it, move by move, without knowing that's what they're doing.

---

*The nethack drawbridge puzzle. The player who reads the level learns to
cross it. The player who doesn't reads it as a random obstacle. Same level.
Different player.*
