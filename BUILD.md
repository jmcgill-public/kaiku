# Kaiku — Build Notes

## Target Platforms

| Platform | Status | Notes |
|---|---|---|
| REAPER Linux x86_64 | **Primary** | VST3 |
| REAPER macOS x86_64 | Stretch | VST3 + AU |
| REAPER macOS ARM64 | Stretch | VST3 + AU, universal binary |
| REAPER Windows | Incidental | VST3 |
| KVR standalone | Stretch | Standalone target via JUCE |

REAPER on Linux is the development target. Test there first.
Everything else is a bonus.

---

## Linux (primary)

### Prerequisites
```bash
# Ubuntu / Debian
sudo apt install cmake git build-essential \
    libx11-dev libxrandr-dev libxinerama-dev \
    libxcursor-dev libfreetype-dev \
    libasound2-dev libwebkit2gtk-4.0-dev
```

### Build
```bash
git clone <repo>
cd kaiku
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --parallel
```

VST3 output: `build/Kaiku_artefacts/Release/VST3/Kaiku.vst3`

Install to REAPER:
```bash
mkdir -p ~/.vst3
cp -r build/Kaiku_artefacts/Release/VST3/Kaiku.vst3 ~/.vst3/
# Then: REAPER → Options → Preferences → VST → Re-scan
```

---

## macOS (stretch goal)

### Universal binary (x86_64 + ARM64)
```bash
cmake -B build -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_OSX_ARCHITECTURES="x86_64;arm64"
cmake --build build --parallel
```

AU component: `build/Kaiku_artefacts/Release/AU/Kaiku.component`
VST3:         `build/Kaiku_artefacts/Release/VST3/Kaiku.vst3`

---

## CLAP (future stretch goal)

JUCE 8 supports CLAP via the `juce_clap_hosting` module.
Add `CLAP` to the `FORMATS` list in CMakeLists.txt when ready.
CLAP is REAPER's preferred modern format on all platforms.
Worth doing once the VST3 is stable.

---

## JS Plugin (REAPER-native, separate stretch goal)

REAPER's JS (jesusonic) plugin format runs inside REAPER without
a build step. A JS port of the FM engine would be:
- Zero installation friction on Linux
- Available to KVR users without downloading a binary
- Compilable directly in REAPER's built-in editor

Relevant: REAPER JS runs at audio sample rate in its own VM.
The FMEngine algorithm (3-stack, 6-operator) is implementable in JS.
See: https://www.reaper.fm/sdk/js/js.php

Candidate path: after VST3 ships and the patch is validated,
port the core algorithm to JS as a companion release.
Both formats on KVR. Different audiences, same instrument.

---

## Notes on JUCE version

Using JUCE 7.0.9 via FetchContent.
JUCE 8 available — upgrade when stable.
The JUCE AudioProcessorValueTreeState API is stable across 7→8.
The LookAndFeel API has minor changes — check before upgrading.
