#!/usr/bin/env python3
"""
hiljaisuus_ir.py — Synthetic Impulse Response Generator

Station acoustic space: large, metal, inhabited but proximate to the void.
Not purple. The Silence is close but this is still a working station.

Approach: classical composition, not effects.
- Image source method for early reflections (the architecture of the space)
- Exponential decay of frequency-shaped noise for late field
- Metal/composite surface coefficients (low absorption, long tail)
- Frequency shaping by surface physics, not EQ preset

The antiphon approach: we are encoding the physical space, not a simulation of
the feeling of a physical space. The difference is audible.

Output: hiljaisuus_station.wav (48kHz, 32-bit float, mono)
Use as convolution reverb IR in any DAW that accepts IR files.

Usage:
    python3 hiljaisuus_ir.py
    python3 hiljaisuus_ir.py --rt60 2.5 --width 15 --output my_station.wav
"""

import numpy as np
from scipy import signal
import scipy.io.wavfile as wav
import argparse
import sys

SR = 48000
C = 343.0  # speed of sound m/s

def generate_ir(
    room_dims=(40.0, 12.0, 7.0),   # L x W x H in meters
    source_pos=(2.0, 6.0, 1.8),    # source: one end of corridor
    receiver_pos=(38.0, 5.5, 1.7), # receiver: far end, slight offset
    rt60=2.2,                       # reverberation time in seconds
    late_onset_ms=80.0,             # early reflection window in ms
    reflection_coeff=0.92,          # metal surface: ~0.92 amplitude per bounce
    late_level=0.15,                # late field gain relative to direct
    duration=4.0,                   # total IR length in seconds
    seed=42,
):
    """
    Generate a synthetic impulse response for a station corridor space.

    Design parameters:
    - RT60 ~2.2s: longer than a concert hall, shorter than a cathedral.
      The station is large. The void is outside.
    - Reflection coefficient 0.92: metal surfaces. Almost nothing is absorbed.
      The sound keeps going. This is what makes it feel like the Silence is listening.
    - High cut at 8kHz (not 4kHz): "not purple" — the station is still inhabited,
      still resonant. A purple space would cut harder and earlier.
    - Presence peak 2-4kHz: metal resonance. The station talks back.
    - Low cut at 60Hz: life support hum lives below this. We don't want it in the IR.
    """

    N = int(SR * duration)
    ir = np.zeros(N)

    Lx, Ly, Lz = room_dims
    sx, sy, sz = source_pos
    rx, ry, rz = receiver_pos

    # ── EARLY REFLECTIONS via Image Source Method ──────────────────────────────
    # Each wall generates a mirror image of the source.
    # Direct sound + first order (6 walls) + second order (8 corner pairs).
    # This gives the architecture of the space — the shape the sound bounces through.

    images = []

    # Direct path
    dist = np.sqrt((rx-sx)**2 + (ry-sy)**2 + (rz-sz)**2)
    images.append((dist, 1.0))

    # First order: 6 walls
    first_order_sources = [
        (-sx,         sy,         sz      ),  # x=0
        (2*Lx - sx,   sy,         sz      ),  # x=Lx
        (sx,          -sy,        sz      ),  # y=0
        (sx,          2*Ly - sy,  sz      ),  # y=Ly
        (sx,          sy,         -sz     ),  # z=0 floor
        (sx,          sy,         2*Lz-sz ),  # z=Lz ceiling
    ]

    for (ix, iy, iz) in first_order_sources:
        d = np.sqrt((rx-ix)**2 + (ry-iy)**2 + (rz-iz)**2)
        images.append((d, reflection_coeff))

    # Second order: corner reflections (most significant pairs)
    second_order_sources = [
        (-sx,        -sy,        sz,      reflection_coeff**2),
        (-sx,        2*Ly-sy,    sz,      reflection_coeff**2),
        (2*Lx-sx,    -sy,        sz,      reflection_coeff**2),
        (2*Lx-sx,    2*Ly-sy,    sz,      reflection_coeff**2),
        (-sx,        sy,         -sz,     reflection_coeff**2),
        (-sx,        sy,         2*Lz-sz, reflection_coeff**2),
        (2*Lx-sx,    sy,         -sz,     reflection_coeff**2),
        (2*Lx-sx,    sy,         2*Lz-sz, reflection_coeff**2),
    ]

    for (ix, iy, iz, coeff) in second_order_sources:
        d = np.sqrt((rx-ix)**2 + (ry-iy)**2 + (rz-iz)**2)
        images.append((d, coeff))

    # Place reflections into IR — 1/r amplitude falloff (inverse distance law)
    for dist, amp in images:
        delay_samples = int(dist / C * SR)
        if delay_samples < N:
            ir[delay_samples] += amp / max(dist, 1.0)

    # ── LATE REVERBERATION ─────────────────────────────────────────────────────
    # Exponential decay of filtered noise.
    # The late field is diffuse — all directions, all surfaces have contributed.
    # We model it as shaped noise because that's what it is physically.

    decay_rate = np.log(1000) / (rt60 * SR)  # -60dB in rt60 seconds
    t = np.arange(N)
    envelope = np.exp(-decay_rate * t)

    late_onset = int(late_onset_ms * 0.001 * SR)

    np.random.seed(seed)
    noise = np.random.randn(N)
    late_field = noise * envelope
    late_field[:late_onset] = 0

    # ── FREQUENCY SHAPING BY SURFACE PHYSICS ──────────────────────────────────
    # Metal/composite surfaces: low absorption across the spectrum.
    # Below 60Hz: life support hum — not part of this IR.
    # Above 8kHz: the void begins to absorb. Not hard. Not purple. Just honest.
    # 2-4kHz presence peak: metal resonance. The station is alive.

    # Low cut: 60Hz
    b, a = signal.butter(2, 60.0 / (SR/2), btype='high')
    late_field = signal.lfilter(b, a, late_field)

    # High cut: 8kHz — soft. "Not purple" means we don't cut at 4kHz.
    # Purple would be: high cut at 3-4kHz, RT60 1.8s, presence dip instead of peak.
    b, a = signal.butter(2, 8000.0 / (SR/2), btype='low')
    late_field = signal.lfilter(b, a, late_field)

    # Presence peak: 2-4kHz
    b, a = signal.butter(2, [2000.0/(SR/2), 4000.0/(SR/2)], btype='band')
    presence = signal.lfilter(b, a, late_field)
    late_field = late_field + 0.3 * presence

    # Late field gain
    late_field *= late_level

    # ── COMBINE AND NORMALIZE ──────────────────────────────────────────────────
    ir = ir + late_field

    peak = np.max(np.abs(ir))
    if peak > 0:
        ir = ir / peak * 0.95

    return ir.astype(np.float32)


def main():
    parser = argparse.ArgumentParser(
        description='Generate Hiljaisuus Station impulse response'
    )
    parser.add_argument('--rt60', type=float, default=2.2,
                        help='Reverberation time in seconds (default: 2.2)')
    parser.add_argument('--length', type=float, default=40.0,
                        help='Room length in meters (default: 40.0)')
    parser.add_argument('--width', type=float, default=12.0,
                        help='Room width in meters (default: 12.0)')
    parser.add_argument('--height', type=float, default=7.0,
                        help='Room height in meters (default: 7.0)')
    parser.add_argument('--output', type=str, default='hiljaisuus_station.wav',
                        help='Output WAV filename')
    parser.add_argument('--purple', action='store_true',
                        help='Generate the purple variant (Hiljaisuus-adjacent, dangerous)')
    args = parser.parse_args()

    if args.purple:
        # The space the Silence occupies. Do not use carelessly.
        print("Generating PURPLE variant — Hiljaisuus-adjacent space")
        ir = generate_ir(
            room_dims=(args.length, args.width, args.height),
            rt60=min(args.rt60, 1.8),   # shorter tail — the Silence absorbs
            reflection_coeff=0.78,       # surfaces absorb more — something is wrong
            late_level=0.08,             # quieter late field — the void swallows it
        )
        # Override high cut to 3kHz — the brightness is gone
        # (done inside generate_ir with purple flag ideally — left as exercise)
        output = args.output.replace('.wav', '_purple.wav')
    else:
        print(f"Generating Station IR: {args.length}m x {args.width}m x {args.height}m")
        print(f"RT60: {args.rt60}s | Character: inhabited, proximate to void, not purple")
        ir = generate_ir(
            room_dims=(args.length, args.width, args.height),
            rt60=args.rt60,
        )
        output = args.output

    wav.write(output, SR, ir)

    duration = len(ir) / SR
    peak = np.max(np.abs(ir))
    print(f"Written: {output}")
    print(f"Duration: {duration:.2f}s | Sample rate: {SR}Hz | Peak: {peak:.4f}")
    print(f"Format: 32-bit float WAV — load directly as convolution IR")


if __name__ == '__main__':
    main()
