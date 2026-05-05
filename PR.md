# vsti: source lands / lähdekoodi saapuu

---

## what this is

Main held the contract. This branch is the instrument.

The vsti/ source — FM engine, voice management, GUI, look and feel — is present and structured. It does not yet compile cleanly (see below). It is not provisional. It is the implementation of `vsti/SPEC.md` as written.

---

## what changed

**vsti/Source/** — 14 files, previously absent from main:

```
FM/FMEngine.cpp + .h          — 6-operator engine, 3-stack algorithm, 4 patches
FM/FMOperator.cpp + .h        — per-operator synthesis, ADSR, index envelope, feedback
Synth/KaikuVoice.cpp + .h     — primary voice + trompette layer, velocity threshold
Synth/VoiceManager.cpp + .h   — 16-voice polyphony, steal policy
PluginProcessor.cpp + .h      — APVTS parameters, MIDI, patch management
PluginEditor.cpp + .h         — GUI: header, 6 operator panels, trompette strip, status bar
GUI/KaamOSLookAndFeel.cpp + .h — amber on void black, hex grid, Hiljaisuus pulse
```

**contrib/MISSION.md** — "before you build" section added. Clocks essay and `arch/time.md` named as prerequisites for anything temporal.

**contrib/STYLE.md** — Timing token annotated. Contributors touching motion or progression are directed to the clocks essay and `arch/time.md` before deciding how something counts.

---

## known issue before merge

`CMakeLists.txt` lists two source files that do not exist:

- `Source/GUI/OperatorPanel.cpp` — `OperatorPanel` is defined in `PluginEditor.cpp`. Remove or split before building.
- `Source/Presets/PresetManager.cpp` — patch factories live in `FMEngine.cpp`. No manager class exists or is needed. Remove.

The build does not close until these are resolved.

---

## what this branch is not

Not passing Kaija. Not ready to ship. The CMakeLists issue is blocking; the instrument has not been heard in a host. The spec is implemented. The instrument is not yet proven.

Proof of concept remains in `games/` — that is what Kaiku sounds like right now.

---

---

## mikä tämä on

Päähaara piti sopimuksen. Tässä haarassa on soitin.

`vsti/`-lähdekoodi — FM-moottori, äänienhallinta, käyttöliittymä — on paikallaan ja rakennettu. Se ei vielä käänny puhtaasti (katso alla). Se ei ole väliaikainen. Se on `vsti/SPEC.md`:n toteutus sellaisena kuin se on kirjoitettu.

---

## mitä muuttui

**vsti/Source/** — 14 tiedostoa, joita ei aiemmin ollut päähaarassa. Katso englanninkielinen luettelo yllä.

**contrib/MISSION.md** — lisätty "before you build" -osio. Kelloesseet-essee ja `arch/time.md` nimetään esitietovaatimuksiksi kaikelle ajalliselle työlle.

**contrib/STYLE.md** — ajoitustokeni kommentoitu. Liikettä tai etenemistä käsittelevät osallistujat ohjataan kelloesseen ja `arch/time.md`:n pariin ennen kuin he päättävät, miten jokin laskee.

---

## tunnettu ongelma ennen yhdistämistä

`CMakeLists.txt` viittaa kahteen lähdetiedostoon, joita ei ole olemassa. Katso englanninkielinen kuvaus yllä. Rakenne ei sulkeudu ennen kuin nämä on korjattu.

---

## mitä tämä haara ei ole

Se ei läpäise Kaijaa. Se ei ole valmis toimitettavaksi. Soitinta ei ole vielä kuultu isäntäohjelmassa. Spesifikaatio on toteutettu. Soitin ei ole vielä todistettu.

Proof of concept on edelleen `games/`-hakemistossa — se on Kaiku tällä hetkellä.

---

*Finnish pending Mystran review before anything in this message locks into interface or documentation copy.*
