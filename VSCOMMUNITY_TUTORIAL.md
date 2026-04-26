# Visual Studio Community — VST3 Development
### From zero to a 1kHz test tone VSTi
*For a world-class Java developer crossing into C++ and the VST3 SDK.*
*No softening. Direct to the concepts that will cost you time.*

---

## Module 1 — Visual Studio Community orientation

VS Community is not IntelliJ. The mental model is different.

**Solution and Project.** A Solution (.sln) is a container for
Projects. A Project produces one binary — a .dll, a .exe, a .lib.
The VST3 plugin is a .dll renamed to .vst3. You will have at minimum
one Project for the plugin and one for the SDK. The Solution holds both.

With CMake projects (which is what you're doing) VS Community opens
the CMakeLists.txt directly. File > Open > CMake. No .sln file.
VS generates its own build system internally. The CMakeLists.txt
is the source of truth.

**Build configurations.** Debug and Release. Debug has symbols,
no optimization, assertions enabled. Release is what ships.
For plugin development: Debug for iteration, Release to verify
before testing in a production session. The configuration dropdown
is in the toolbar. Know where it is.

**The Output window.** View > Output. Build errors, linker errors,
and CMake configuration messages land here. The Error List
(View > Error List) parses the output into clickable items.
Use both. CMake errors are often only in the Output window.

**Attaching the debugger to REAPER.** This is how you debug a plugin.
Debug > Attach to Process. Find reaper.exe. Your plugin's breakpoints
fire when REAPER calls into the plugin. This works because your plugin
is a DLL loaded into REAPER's process space. The debugger sees it.

**Keyboard shortcuts that matter:**
- F5 — build and run (or attach if configured)
- F7 — build solution
- F9 — toggle breakpoint
- F10 — step over
- F11 — step into
- Shift+F11 — step out
- Ctrl+Shift+B — build
- Ctrl+` — terminal

**IntelliSense and CMake.** After opening a CMake project VS scans
the source and configures IntelliSense. This takes a minute on first
open. If IntelliSense shows false errors after configuration, right-click
CMakeLists.txt in Solution Explorer and select "Configure Cache."

---

## Module 2 — C++ for the Java veteran

Not a C++ tutorial. Exactly the things that will cost a Java
developer time in a VST3 codebase.

### The compilation model

Java: `javac` compiles .java to .class. The JVM links at runtime.
Everything is available to everything else at runtime.

C++: Each .cpp file is compiled independently into an object file (.obj).
The linker combines object files into the final binary. A symbol
must be *declared* before it can be used in any translation unit.
Declaration lives in header files (.h). Definition lives in source
files (.cpp). The compiler sees only the current .cpp and whatever
headers it includes.

```cpp
// processor.h — declaration
class HehkuProcessor {
public:
    void process(float* buffer, int numSamples);
private:
    double phase;
};

// processor.cpp — definition
#include "processor.h"

void HehkuProcessor::process(float* buffer, int numSamples) {
    // implementation here
}
```

Include the header wherever you use the class. The linker resolves
the actual code at link time. Define a function in two .cpp files
and the linker will tell you about it loudly.

**Include guards.** Headers are included by multiple .cpp files.
Without guards the declarations appear multiple times and the
compiler complains. Use `#pragma once` at the top of every header.
It's not standard but every relevant compiler supports it and
it's cleaner than the `#ifndef` alternative.

```cpp
#pragma once

class HehkuProcessor { ... };
```

### Memory: the thing Java is hiding from you

Java: the GC handles deallocation. You allocate, you forget,
the heap cleans up eventually.

C++: you allocate, you deallocate, and the moment between those
two is your problem. Get it wrong and you have a memory leak,
a use-after-free, or a crash that only happens in Release builds
on the user's machine.

The solution is RAII — Resource Acquisition Is Initialization.
Bind resource lifetime to object lifetime. When the object goes
out of scope, its destructor runs and releases the resource.

```cpp
// Java style — manual, dangerous
float* buffer = new float[1024];
processBuffer(buffer);
delete[] buffer; // easy to forget, easy to call twice

// C++ RAII style — automatic
std::vector<float> buffer(1024);
processBuffer(buffer.data());
// destructor called automatically when buffer goes out of scope
```

For heap-allocated objects: `std::unique_ptr<T>` for sole ownership,
`std::shared_ptr<T>` for shared ownership. Prefer `unique_ptr`.
If you find yourself reaching for `shared_ptr` everywhere, you
have a design problem.

```cpp
auto processor = std::make_unique<HehkuProcessor>();
processor->process(buffer, numSamples);
// deleted automatically when processor goes out of scope
```

**The destructor.** Java has `finalize()` which nobody uses.
C++ destructors are called deterministically when an object's
lifetime ends. Write them. Make them do the right thing.
The VST3 SDK uses reference counting (described below) instead
of RAII for plugin objects, but understanding destructors is
prerequisite to understanding why.

### Pointers and references

Java references are safe handles. They can be null but they
can't be invalid (pointing to freed memory). The JVM tracks them.

C++ pointers are memory addresses. They can be null, uninitialized,
or dangling (pointing to freed memory). The hardware doesn't track them.

```cpp
int value = 42;
int* ptr = &value;    // ptr holds the address of value
int ref = *ptr;       // dereference: ref is now 42
*ptr = 100;           // write through pointer: value is now 100

int* badPtr;          // uninitialized — contains garbage
*badPtr = 1;          // undefined behavior. crash if you're lucky.

int* nullPtr = nullptr;
*nullPtr = 1;         // crash
```

C++ references are aliases. Once bound, they cannot be rebound.
They cannot be null. They behave like the original object.

```cpp
int value = 42;
int& ref = value;  // ref is an alias for value
ref = 100;         // value is now 100
```

In the VST3 SDK you will see both. Process data arrives as
references. Plugin objects are passed as pointers. Know the difference.

### const correctness

Java has `final` for variables. C++ const is more pervasive.

```cpp
const float amplitude = 0.5f;   // can't change
amplitude = 0.8f;                // compiler error

void readBuffer(const float* buffer, int size);
// buffer contents cannot be modified through this pointer

float getPhase() const;
// this member function cannot modify the object's state
```

Mark every function that doesn't modify state as `const`.
The VST3 SDK's interfaces declare const functions. Your
implementations must match the const-ness of the interface.
Mismatching const is a compile error that looks confusing
until you understand what it's telling you.

### Abstract classes as interfaces

Java interfaces are explicit. C++ interfaces are abstract classes
with pure virtual functions.

```cpp
// This is C++'s version of a Java interface
class IProcessor {
public:
    virtual ~IProcessor() = default;          // virtual destructor required
    virtual void process(float* buf, int n) = 0;  // pure virtual
    virtual void reset() = 0;                 // pure virtual
};

// Cannot instantiate IProcessor directly — it has pure virtual functions
// Must be subclassed and all pure virtuals implemented

class HehkuProcessor : public IProcessor {
public:
    void process(float* buf, int n) override { ... }
    void reset() override { ... }
};
```

`override` is not required but use it. The compiler verifies that
you're actually overriding a virtual function. Typos in function
signatures create new functions instead of overriding, silently.
`override` catches this.

The VST3 SDK is built entirely on this pattern. Every interface
you implement is a pure virtual base class.

### Reference counting — the VST3 object model

VST3 uses COM-style reference counting instead of garbage collection
or RAII for plugin objects. Every plugin object inherits from
`FUnknown`, which provides `addRef()` and `release()`. When the
reference count reaches zero, the object destroys itself.

The SDK provides `IPtr<T>` — a smart pointer that calls `addRef()`
on construction and `release()` on destruction. Use it for all
VST3 objects. Never call `addRef()`/`release()` manually.

```cpp
// Wrong — manual reference counting
IComponent* comp = createProcessor();
comp->addRef();
comp->doSomething();
comp->release();  // easy to miss

// Right — IPtr handles it
IPtr<IComponent> comp = createProcessor();
comp->doSomething();
// release called automatically
```

### Namespaces

```cpp
// The VST3 SDK lives in nested namespaces
Steinberg::Vst::AudioEffect
Steinberg::Vst::ProcessData
Steinberg::FUnknown

// Using declarations (file-local scope only, never in headers)
using namespace Steinberg;
using namespace Steinberg::Vst;

// Then you can write:
AudioEffect  // instead of Steinberg::Vst::AudioEffect
```

Never put `using namespace` in a header file. It pollutes every
file that includes that header.

### Strings in the VST3 SDK

The SDK uses UTF-16 on Windows. String literals need the `STR()`
macro or `USTRING()` macro.

```cpp
// Wrong
const char* name = "Hehku";

// Right
const Steinberg::char16* name = STR16("Hehku");
```

This will cause confusing errors if you forget it.
Every plugin name, category, and parameter name goes through this.

---

## Module 3 — CMake in Visual Studio Community

The VST3 SDK ships with a CMake build system. You will extend it
rather than replace it.

### Opening a CMake project

File > Open > CMake. Navigate to your CMakeLists.txt. VS reads it,
configures the build system, and presents the project in Solution
Explorer. No .sln file is created or needed.

The CMake toolbar dropdown selects the build configuration.
"x64-Debug" and "x64-Release" are the two you care about.

### The VST3 SDK's CMake integration

Clone the SDK:
```bash
git clone --recursive https://github.com/steinbergmedia/vst3sdk
cd vst3sdk
```

The `--recursive` flag is required. The SDK has submodules
(base, pluginterfaces, cmake, vstgui) that are separate repos.

The SDK provides CMake macros for building plugins. The key macro:

```cmake
smtg_add_vst3plugin(Hehku
    source/processor.h
    source/processor.cpp
    source/controller.h
    source/controller.cpp
    source/entry.cpp
)

target_link_libraries(Hehku
    PRIVATE
    sdk
)
```

`smtg_add_vst3plugin` handles the .vst3 bundle structure,
the export of `GetPluginFactory`, and the post-build copy
to the VST3 install directory.

### Your top-level CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.14)
project(MusiciansMemory VERSION 0.1.0)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Point to the SDK
set(vst3sdk_SOURCE_DIR ${CMAKE_SOURCE_DIR}/vst3sdk)
add_subdirectory(${vst3sdk_SOURCE_DIR} vst3sdk)

# Your plugin
add_subdirectory(plugins/hehku)
```

### Directory structure

```
musicians-memory/
  CMakeLists.txt          (top-level, above)
  vst3sdk/                (cloned SDK, add as git submodule)
  plugins/
    hehku/
      CMakeLists.txt      (plugin-specific)
      source/
        processor.h
        processor.cpp
        controller.h
        controller.cpp
        entry.cpp
        version.h
```

---

## Module 4 — VST3 architecture

Three interfaces. Everything else is built on them.

### IComponent — the processor

Lives in the audio thread. Receives audio buffers and MIDI events.
Produces audio output. Has access to `ProcessContext` — the
authoritative clock, tempo, transport state.

The process block is called at audio thread priority. No memory
allocation. No locks. No I/O. No exceptions. Everything the
process block needs must be prepared before it's called.

### IEditController — the controller

Lives in the UI thread. Manages parameters. Owns the plugin UI
(if any). Communicates with the processor via a message queue —
never directly, never synchronously.

The separation is physical. The processor can be on a different
machine than the controller in networked audio setups. Design
accordingly.

### IConnectionPoint — the message bus

Connects processor and controller. Thread-safe message passing.
Your synchronization events, practice session state, teacher
messages — everything that crosses the processor/controller
boundary goes through here.

### The factory

The entry point of your plugin. A function exported from the DLL
named `GetPluginFactory`. The DAW calls it to enumerate what
plugins the DLL provides.

The `SMTG_EXPORT_SYMBOL` macro and `BEGIN_FACTORY_DEF`/`END_FACTORY`
macros in the SDK handle the boilerplate. You provide UIDs and
class registrations.

### UIDs

Every VST3 class has a unique 128-bit identifier. Generate them once.
They identify your plugin to every DAW that scans it. Change them
and every project that used your plugin loses the reference.

VS Community has a GUID generator: Tools > Create GUID.
Or use `uuidgen` in the VS Developer Command Prompt.

---

## Module 5 — Hello World VST3

A plugin that loads in REAPER and does nothing.
This is the foundation. Get it loading before adding any logic.

### version.h

```cpp
#pragma once

#define MAJOR_VERSION_STR "0"
#define MINOR_VERSION_STR "1"
#define BUGFIX_VERSION_STR "0"
#define BUILD_NUMBER_STR   "0"

#define FULL_VERSION_STR MAJOR_VERSION_STR "." \
                         MINOR_VERSION_STR "." \
                         BUGFIX_VERSION_STR "." \
                         BUILD_NUMBER_STR

#define stringPluginName    "Hehku"
#define stringOriginalFilename "Hehku.vst3"
#define stringCompanyName   "McGill Enterprises"
#define stringLegalCopyright "© 2026 McGill Enterprises"
#define stringPluginVersion  FULL_VERSION_STR
```

### processor.h

```cpp
#pragma once
#include "public.sdk/source/vst/vstaudioeffect.h"

namespace McGillEnterprises {

class HehkuProcessor : public Steinberg::Vst::AudioEffect {
public:
    HehkuProcessor();
    ~HehkuProcessor() SMTG_OVERRIDE;

    // IComponent
    Steinberg::tresult PLUGIN_API initialize(
        Steinberg::FUnknown* context) SMTG_OVERRIDE;
    Steinberg::tresult PLUGIN_API terminate() SMTG_OVERRIDE;
    Steinberg::tresult PLUGIN_API setupProcessing(
        Steinberg::Vst::ProcessSetup& setup) SMTG_OVERRIDE;
    Steinberg::tresult PLUGIN_API process(
        Steinberg::Vst::ProcessData& data) SMTG_OVERRIDE;

    static Steinberg::FUnknown* createInstance(void*) {
        return (Steinberg::Vst::IAudioProcessor*)new HehkuProcessor();
    }

    static const Steinberg::FUID uid;
};

} // namespace McGillEnterprises
```

### processor.cpp

```cpp
#include "processor.h"
#include "plugids.h"

using namespace Steinberg;
using namespace Steinberg::Vst;

namespace McGillEnterprises {

const FUID HehkuProcessor::uid(0x12345678, 0x12345678,
                                0x12345678, 0x12345678);
// Replace with generated GUIDs. These are placeholders.

HehkuProcessor::HehkuProcessor() {
    setControllerClass(HehkuControllerUID);
}

HehkuProcessor::~HehkuProcessor() {}

tresult PLUGIN_API HehkuProcessor::initialize(FUnknown* context) {
    tresult result = AudioEffect::initialize(context);
    if (result == kResultTrue) {
        addAudioOutput(STR16("Stereo Out"), SpeakerArr::kStereo);
        addEventInput(STR16("MIDI In"));
    }
    return result;
}

tresult PLUGIN_API HehkuProcessor::terminate() {
    return AudioEffect::terminate();
}

tresult PLUGIN_API HehkuProcessor::setupProcessing(ProcessSetup& setup) {
    sampleRate = setup.sampleRate;
    return AudioEffect::setupProcessing(setup);
}

tresult PLUGIN_API HehkuProcessor::process(ProcessData& data) {
    // Hello World: output silence
    if (data.numOutputs == 0) return kResultOk;

    AudioBusBuffers& output = data.outputs[0];
    for (int32 ch = 0; ch < output.numChannels; ++ch) {
        memset(output.channelBuffers32[ch], 0,
               data.numSamples * sizeof(float));
    }
    output.silenceFlags = 0x3; // both channels silent
    return kResultOk;
}

} // namespace McGillEnterprises
```

### controller.h

```cpp
#pragma once
#include "public.sdk/source/vst/vsteditcontroller.h"

namespace McGillEnterprises {

class HehkuController : public Steinberg::Vst::EditController {
public:
    static Steinberg::FUnknown* createInstance(void*) {
        return (Steinberg::Vst::IEditController*)new HehkuController();
    }

    static const Steinberg::FUID uid;
};

} // namespace McGillEnterprises
```

### controller.cpp

```cpp
#include "controller.h"

namespace McGillEnterprises {

const Steinberg::FUID HehkuController::uid(0x87654321, 0x87654321,
                                            0x87654321, 0x87654321);
// Replace with generated GUIDs.

} // namespace McGillEnterprises
```

### entry.cpp — the factory

```cpp
#include "public.sdk/source/main/pluginfactory.h"
#include "processor.h"
#include "controller.h"
#include "version.h"

#define stringPluginType Steinberg::Vst::PlugType::kInstrumentSynth

BEGIN_FACTORY_DEF(stringCompanyName,
                  "https://mcgill-enterprises.example",
                  "mailto:dev@mcgill-enterprises.example")

DEF_CLASS2(
    INLINE_UID_FROM_FUID(McGillEnterprises::HehkuProcessor::uid),
    PClassInfo::kManyInstances,
    kVstAudioEffectClass,
    stringPluginName,
    Vst::kDistributable,
    stringPluginType,
    stringPluginVersion,
    kVstVersionString,
    McGillEnterprises::HehkuProcessor::createInstance
)

DEF_CLASS2(
    INLINE_UID_FROM_FUID(McGillEnterprises::HehkuController::uid),
    PClassInfo::kManyInstances,
    kVstComponentControllerClass,
    stringPluginName "Controller",
    0, "",
    stringPluginVersion,
    kVstVersionString,
    McGillEnterprises::HehkuController::createInstance
)

END_FACTORY
```

### plugins/hehku/CMakeLists.txt

```cmake
set(plug_sources
    source/processor.h
    source/processor.cpp
    source/controller.h
    source/controller.cpp
    source/entry.cpp
    source/version.h
)

smtg_add_vst3plugin(Hehku ${plug_sources})

target_include_directories(Hehku PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/source)

target_link_libraries(Hehku PRIVATE sdk)

smtg_target_configure_version_file(Hehku)
```

Build. Open REAPER. Scan for new plugins. Hehku appears in the
instrument browser. Insert it. It produces silence. That is
a successful Hello World.

---

## Module 6 (Capstone) — Hehku: the 1kHz test tone

The void emits a signal at 1000 Hz.
Aava hears it as purple. You will hear it as a sine wave.

Add two member variables to `HehkuProcessor`:

```cpp
// processor.h — add to private section
private:
    double phase = 0.0;
    double sampleRate = 44100.0;
    static constexpr double kFrequency = 1000.0;
    static constexpr double kAmplitude = 0.25; // -12dBFS — safe for testing
```

### The mathematics

A sine wave at frequency f Hz, sample rate Fs:

    phase increment = 2π × f / Fs

Each sample:

    output = amplitude × sin(phase)
    phase  = phase + phaseIncrement

When phase exceeds 2π, subtract 2π. This is the phase accumulator
pattern. It accumulates error across samples but at audio rates
the error is below the noise floor.

The wrap is cheaper than `fmod` and more numerically stable
than letting phase grow without bound.

### The process block

Replace the silence output in `process()`:

```cpp
tresult PLUGIN_API HehkuProcessor::process(ProcessData& data) {
    if (data.numOutputs == 0) return kResultOk;

    AudioBusBuffers& output = data.outputs[0];
    int32 numSamples = data.numSamples;
    int32 numChannels = output.numChannels;

    const double phaseIncrement =
        2.0 * M_PI * kFrequency / sampleRate;

    for (int32 s = 0; s < numSamples; ++s) {
        float sample = static_cast<float>(kAmplitude * std::sin(phase));

        phase += phaseIncrement;
        if (phase >= 2.0 * M_PI)
            phase -= 2.0 * M_PI;

        for (int32 ch = 0; ch < numChannels; ++ch) {
            output.channelBuffers32[ch][s] = sample;
        }
    }

    output.silenceFlags = 0; // not silent
    return kResultOk;
}
```

Include `<cmath>` at the top of processor.cpp for `std::sin` and `M_PI`.
On Windows with MSVC, `M_PI` requires `#define _USE_MATH_DEFINES`
before including `<cmath>`.

```cpp
#define _USE_MATH_DEFINES
#include <cmath>
```

### setupProcessing — capture the sample rate

```cpp
tresult PLUGIN_API HehkuProcessor::setupProcessing(ProcessSetup& setup) {
    sampleRate = setup.sampleRate;
    phase = 0.0; // reset phase on setup
    return AudioEffect::setupProcessing(setup);
}
```

The host calls `setupProcessing` before the first process call and
whenever the sample rate changes. Capture `sampleRate` here. Do not
read it from `ProcessContext` — it's in the setup, not the context.

### Build, install, test

Build in Debug. REAPER rescans on launch or via Options > Preferences
> Plug-ins > VST. Insert Hehku on an instrument track.
Press play or enable the track monitor. 1kHz sine wave output.

Open REAPER's built-in spectrum analyzer (FX chain, JS: Spectral
Analyzer or similar). Verify the spike at 1kHz. The void is emitting.

### What this demonstrates

The phase accumulator is the core of every oscillator in every
synthesizer ever built in software. This is not a toy. The sine
wave becomes a complex waveform when you add harmonics. The 1kHz
test tone becomes a MIDI-controlled instrument when you multiply
`kAmplitude` by a velocity-scaled envelope and set `kFrequency`
from the MIDI note number:

```cpp
// MIDI note to frequency
double noteToFreq(int midiNote) {
    return 440.0 * std::pow(2.0, (midiNote - 69) / 12.0);
}
```

That is the next step. It is one function and a MIDI event handler.

---

## What you have

A VST3 instrument plugin that:
- Loads in REAPER
- Emits a 1kHz sine wave at -12dBFS
- Has a clean project structure ready for extension
- Is built against the raw VST3 SDK with no framework dependencies
- Uses the phase accumulator pattern that underlies all software synthesis

The foundation is solid. Everything downstream can be trusted.

---

*The void emits at 1000 Hz.*
*Aava hears purple.*
*The rest is harmonics.*

---
