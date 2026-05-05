# CLAUDE.md — kaiku

This is a standing brief for AI instances working in this repository.
The authoritative world bible and full session protocol live in the ur branch (private).
Load the world bible before beginning any session. This file is a local complement, not a substitute.

## What this repo is

The kaiku VST3 FM synthesizer and associated KAAMOS audio/game work.
Primary collaborator: Claudette (session persona established in world_bible.md).

## Closing ritual — session coda

**When James says `tallenna`, generate and file a session coda before any push.**

The coda goes in `agents/` as `coda_YYYY_MM_DD.md`.

It covers three things, in this order:

1. **What was built or decided** — brief inventory of the session's output: files created or changed, decisions made, questions resolved, questions opened.

2. **Patterns observed** — map the session's work against the rebraining.org practice vocabulary (foundation → patterns → direction). Name which patterns were active, where they worked, where they were absent. If the session surfaces a candidate new pattern, name it in draft form using Problem / Solution / Context.

3. **Muistaa update** — one paragraph: what the next session needs to know that isn't already in the world bible. Anything that should be pushed to the world bible before the session closes.

The coda is filed, not announced. James reads it before he pushes. If it surfaces something that needs a world bible edit, he makes it before the push.

## Repo structure

- `vsti/` — JUCE/C++ VST3 plugin source
- `arch/` — architecture and planning documents
- `comp/` — composition: scores, track briefs, percussion kits
- `games/` — HTML games (birch.html, kuule.html); canonical source for deploy
- `agents/` — session documents: Billy/Claudette correspondence, pattern analyses, codas
- `ir/` — impulse response specs and scripts
- `sounds/` — audio pipeline scripts

## Key planning documents

- `vsti/SPEC.md` — plugin specification
- `vsti/PLAN.md` — build plan
- `arch/sid_brief.md` — SID/chiptune branch planning brief
- `agents/claudette_to_billy.md` — open issues and work plan for the VST build

## Standing constraints

The world bible is canonical. When code and spec conflict, the spec wins.
The 6809/KaamOS software platform is out of scope for this repo.
KaamOS in the visual layer (palette, LookAndFeel) is in scope and correct.
