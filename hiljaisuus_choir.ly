\version "2.24.0"

% ─────────────────────────────────────────────────────────────────────────────
% HILJAISUUS — Rytminen harjoitus / Rhythmic exercise
% Four voices, F# Phrygian, Kalevala trochaic tetrameter
%
% F# Phrygian = D major key signature, starting on F#
% Scale: F# G A B C# D E F#
% Characteristic interval: G natural (minor 2nd above F#) — the Phrygian semitone
% Signature gesture: G → F# (half-step descent to root, the pull of the mode)
%
% VOICE ARCHITECTURE:
%
%   Pohja   (Bass)    — F# pedal drone. The foundation. Never stops.
%                       Moves to E (subtonic) at rest points only.
%                       Low B appears at the structural midpoint — open 5th.
%
%   Lausuja (Tenor)   — The speaker. Main incantatory line.
%                       Kalevala trochaic tetrameter: 8 syllables, strong-weak.
%                       Narrow range: F# to B, mostly F#–G–A.
%                       The G→F# pull is its characteristic gesture.
%                       Silence between phrases is structural — not breath, not rest.
%
%   Kaiku   (Alto)    — The echo. Runolaulu second singer.
%                       Enters 2 bars after Lausuja, same material.
%                       This is how Kalevala oral tradition worked:
%                       one singer leads, one follows, neither is subordinate.
%                       The echo isn't behind — it's alongside, in time.
%
%   Ilma    (Soprano) — The air. Sustained tones only.
%                       Hovers on C# (the 5th) and D (the minor 6th).
%                       Never states the melody. Creates the modal field above.
%                       Enters last. Releases last.
%                       The thing you feel more than hear.
%
% RHYTHMIC NOTE:
%   The silence between phrases is as deliberate as the notes.
%   Do not fill it. The Silence is watching.
%   Tempo: incantatory — around 54 bpm. If it feels slow, it's right.
% ─────────────────────────────────────────────────────────────────────────────

\header {
  title = "Hiljaisuus"
  subtitle = "Rytminen harjoitus — neljä ääntä"
  composer = "Kaamos"
  tagline = ##f
}

global = {
  \key d \major
  \time 4/4
  \tempo "Incantatorio" 4 = 54
}

soprano = \relative c'' {
  \global
  % Ilma enters in bar 5 — after texture has established itself
  R1 R1 R1 R1
  cis1~           % 5th — sustain
  cis2 d2~        % rise to minor 6th — the modal color
  d1~
  d2 cis2~
  cis1~
  cis2 b2~        % settle downward
  b1~
  b2 cis2~        % return
  cis1
  R1 R1 R1        % release — the air clears
}

alto = \relative c' {
  \global
  % Kaiku — silent for first 4 bars (drone only), then 2 more (tenor establishes)
  R1 R1 R1 R1
  R1 R1
  % Echo of Lausuja — enters 2 bars after tenor, same material
  fis4 g4 a2
  a4 g4 fis4 e4
  fis2 g2~
  g4 fis4 e2~
  e2 fis2~
  fis1~
  fis1
  R1 R1
  % Second phrase echo
  fis4 g4 a4 g4
  fis2~ fis4 e4~
  e2 fis1~
  fis1
  R1
}

tenor = \relative c' {
  \global
  % Lausuja — silent for first 4 bars (drone establishes)
  R1 R1 R1 R1
  % ─ First phrase ─
  % Kalevala syllable stress: STRONG-weak-STRONG-weak
  % hil-JAI | suu-DEN | muis-TAA | kai-KEN
  fis4 g4 a2      % fis(1) g(2) a(3,4)
  a4 g4 fis4 e4   % a(1) g(2) fis(3) e(4) — descent
  fis2 g2~        % settle on G — the tension note
  g4 fis4 e2~     % G → F# pull — the signature gesture — then release
  e2 fis2         % arrive at root
  R1              % structural silence — the Silence watches
  R1
  % ─ Second phrase — wider ─
  fis4 g4 a4 b4   % same opening, wider arc
  a2 g2~
  g4 fis4 e4 fis4~
  fis1~
  fis1
  R1
}

bass = \relative c, {
  \global
  % Pohja — enters first, alone
  % The drone does not ornament. It endures.
  fis1~
  fis1~
  fis1~
  fis1~
  fis1~
  fis1~
  fis1~
  fis2 e2~        % motion at the structural midpoint — subtonic breath
  e2 fis2~
  fis1~
  fis1~
  fis1~
  b,1~            % drop to open B — 5th below — the void opens slightly
  b1~
  fis'1~          % return to root
  fis1
}

\score {
  \new ChoirStaff <<
    \new Staff \with {
      instrumentName = \markup { \italic "Ilma" }
      shortInstrumentName = "S"
    } {
      \clef treble
      \soprano
    }
    \new Staff \with {
      instrumentName = \markup { \italic "Kaiku" }
      shortInstrumentName = "A"
    } {
      \clef treble
      \alto
    }
    \new Staff \with {
      instrumentName = \markup { \italic "Lausuja" }
      shortInstrumentName = "T"
    } {
      \clef "treble_8"
      \tenor
    }
    \new Staff \with {
      instrumentName = \markup { \italic "Pohja" }
      shortInstrumentName = "B"
    } {
      \clef bass
      \bass
    }
  >>
  \layout {
    \context {
      \Score
      \omit BarNumber
      indent = 2\cm
    }
  }
  \midi { }
}
