#!/usr/bin/env python3
"""
hiljaisuus_ir.py — KAAMOS synthetic impulse response generator

Portability fallback. Primary tool is Voxengo Impulse Modeler.
See ir_settings.md for canonical parameter values and workflow.

Requires: Python 3.8+, numpy. No other dependencies.

Usage:
  python3 hiljaisuus_ir.py                    # station corridor (default)
  python3 hiljaisuus_ir.py --preset forest    # voidborn forest
  python3 hiljaisuus_ir.py --all              # both
  python3 hiljaisuus_ir.py --help
"""

import argparse
import struct
import sys
import time
import numpy as np

C = 343.0  # speed of sound m/s at ~20°C


# ---------------------------------------------------------------------------
# WAV I/O — float32 IEEE, no scipy required
# ---------------------------------------------------------------------------

def write_float32_wav(filename, data, sample_rate):
    data = np.clip(data, -1.0, 1.0).astype(np.float32)
    raw = data.tobytes()
    with open(filename, 'wb') as f:
        f.write(b'RIFF')
        f.write(struct.pack('<I', 36 + len(raw)))
        f.write(b'WAVE')
        f.write(b'fmt ')
        f.write(struct.pack('<I', 16))
        f.write(struct.pack('<H', 3))            # WAVE_FORMAT_IEEE_FLOAT
        f.write(struct.pack('<H', 1))            # mono
        f.write(struct.pack('<I', sample_rate))
        f.write(struct.pack('<I', sample_rate * 4))  # byte rate
        f.write(struct.pack('<H', 4))            # block align
        f.write(struct.pack('<H', 32))           # bits per sample
        f.write(b'data')
        f.write(struct.pack('<I', len(raw)))
        f.write(raw)


# ---------------------------------------------------------------------------
# FIR low-pass — windowed sinc, FFT convolution, pure numpy
# ---------------------------------------------------------------------------

def lowpass(data, cutoff_hz, sr, taps=513):
    """Windowed-sinc FIR low-pass. Returns same length as input."""
    if cutoff_hz >= sr / 2.0:
        return data.copy()
    fc = cutoff_hz / (sr / 2.0)
    n = np.arange(taps) - (taps - 1) / 2.0
    h = np.sinc(fc * n) * np.blackman(taps)
    h /= h.sum()
    N = len(data) + taps - 1
    fft_len = 1 << int(np.ceil(np.log2(N)))
    y = np.fft.irfft(np.fft.rfft(h, fft_len) * np.fft.rfft(data, fft_len), fft_len)
    d = (taps - 1) // 2
    return y[d:d + len(data)].astype(np.float32)


# ---------------------------------------------------------------------------
# Image source method — Allen & Berkley (1979)
# ---------------------------------------------------------------------------

def image_sources(room, src, mic, sr, ir_len, refl, order):
    """
    Rectangular room image source method.
    room = (Lx, Ly, Lz), src/mic = (x, y, z), refl = amplitude coefficient.

    Image positions:  xi = 2*px*Lx + (-1)^qx * sx
    Reflection count: 2*|px| (qx=0) or |2*px-1| (qx=1), summed over axes.
    """
    Lx, Ly, Lz = room
    sx, sy, sz = src
    mx, my, mz = mic
    ir = np.zeros(ir_len, dtype=np.float64)
    max_dist = ir_len / sr * C
    count = 0

    for px in range(-order, order + 1):
        for qx in range(2):
            ix = 2*px*Lx + ((-1)**qx)*sx
            rx = 2*abs(px) if qx == 0 else abs(2*px - 1)

            for py in range(-order, order + 1):
                for qy in range(2):
                    iy = 2*py*Ly + ((-1)**qy)*sy
                    ry = 2*abs(py) if qy == 0 else abs(2*py - 1)

                    for pz in range(-order, order + 1):
                        for qz in range(2):
                            iz = 2*pz*Lz + ((-1)**qz)*sz
                            rz = 2*abs(pz) if qz == 0 else abs(2*pz - 1)

                            dist = np.sqrt((ix-mx)**2 + (iy-my)**2 + (iz-mz)**2)
                            if dist < 1e-6 or dist > max_dist:
                                continue

                            n_refl = rx + ry + rz
                            ds = int(dist / C * sr)
                            if ds >= ir_len:
                                continue

                            ir[ds] += (refl ** n_refl) / dist
                            count += 1

    print(f"    {count} image sources", file=sys.stderr)
    return ir


# ---------------------------------------------------------------------------
# Full IR: early (image sources) + late (stochastic tail)
# ---------------------------------------------------------------------------

def generate_ir(p, sr=48000):
    room    = p['room']
    src     = p['src']
    mic     = p['mic']
    rt60    = p['rt60']
    refl    = p['refl']
    hf_hz   = p['hf_hz']
    order   = p['order']
    length  = p['length_s']
    t_trans = p.get('transition_s', 0.08)

    ir_len   = int(length * sr)
    decay    = 3.0 * np.log(10.0) / rt60          # amplitude decay rate
    t        = np.arange(ir_len) / sr

    # Early reflections
    print(f"  early reflections ...", file=sys.stderr)
    t0 = time.time()
    early = image_sources(room, src, mic, sr, ir_len, refl, order)
    early *= np.exp(-decay * t)
    print(f"  done in {time.time()-t0:.1f}s", file=sys.stderr)

    # Late stochastic tail
    tr   = int(t_trans * sr)
    win  = max(1, int(0.015 * sr))
    rms  = np.sqrt(np.mean(early[max(0,tr-win):tr]**2) + 1e-20)
    rng  = np.random.default_rng(seed=42)
    noise = rng.standard_normal(ir_len) * np.exp(-decay * t)
    if hf_hz < sr / 2:
        noise = lowpass(noise, hf_hz, sr)
    noise_rms = np.sqrt(np.mean(noise[max(0,tr-win):tr]**2) + 1e-20)
    noise *= (rms * 0.4) / noise_rms
    noise[:tr] = 0.0

    ir = early + noise

    # HF rolloff on full IR (forest: significant; station: bypass)
    if hf_hz < sr * 0.45:
        ir = lowpass(ir, hf_hz, sr)

    peak = np.max(np.abs(ir))
    if peak > 0:
        ir *= 0.9 / peak

    return ir.astype(np.float32)


# ---------------------------------------------------------------------------
# Presets — Sabine-verified parameters
# See ir_settings.md for derivation and Impulse Modeler mappings
# ---------------------------------------------------------------------------

PRESETS = {
    'station': {
        'label':        'Hiljaisuus Station Corridor',
        'file':         'hiljaisuus_station.wav',
        # 40×12×7m metal corridor. Source/mic at one end.
        # Far-wall reflection at ~221ms creates corridor character.
        # Sabine RT60 = 2.20s at refl=0.924 (energy absorption 14.6%)
        'room':         (40.0, 12.0, 7.0),
        'src':          (2.0,  6.0,  1.8),
        'mic':          (2.05, 6.0,  1.8),
        'rt60':         2.2,
        'refl':         0.924,
        'hf_hz':        22000,      # metal: near-flat HF
        'order':        10,
        'length_s':     4.0,
        'transition_s': 0.10,
    },
    'forest': {
        'label':        'Voidborn Forest',
        'file':         'voidborn_forest.wav',
        # 18×14×11m boreal forest (Karelian pine/spruce/birch).
        # Rectangular approximation of irregular trunk spacing.
        # Sabine RT60 = 0.62s at refl=0.636 (energy absorption 59.6%)
        # HF rolloff above 4kHz: canopy + pine needle absorption.
        # See forest_ir_spec.md for the scene derivation.
        'room':         (18.0, 14.0, 11.0),
        'src':          (9.0,  7.0,  1.8),
        'mic':          (9.05, 7.0,  1.8),
        'rt60':         0.62,
        'refl':         0.636,
        'hf_hz':        4000,       # canopy absorption: significant rolloff
        'order':        6,
        'length_s':     2.0,
        'transition_s': 0.06,
    },
}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    pa = argparse.ArgumentParser(
        description='KAAMOS IR generator — numpy fallback for Voxengo Impulse Modeler',
        epilog='See ir_settings.md for canonical parameters and production workflow.'
    )
    pa.add_argument('--preset', choices=list(PRESETS), default='station')
    pa.add_argument('--all', action='store_true', help='Generate all presets')
    pa.add_argument('--sample-rate', '-r', type=int, default=48000)
    pa.add_argument('--output', '-o', type=str, default=None)
    pa.add_argument('--rt60', type=float, default=None)
    pa.add_argument('--refl', type=float, default=None,
                    help='Reflection coefficient override (amplitude, 0–1)')
    args = pa.parse_args()

    targets = list(PRESETS) if args.all else [args.preset]

    for name in targets:
        p = dict(PRESETS[name])
        if args.rt60:  p['rt60'] = args.rt60
        if args.refl:  p['refl'] = args.refl
        if args.output and len(targets) == 1:
            p['file'] = args.output

        print(f"\n[ {p['label']} ]", file=sys.stderr)
        print(f"  {p['room']}  RT60={p['rt60']}s  refl={p['refl']}  "
              f"HF={p['hf_hz']}Hz  {p['length_s']}s @ {args.sample_rate}Hz",
              file=sys.stderr)

        ir = generate_ir(p, sr=args.sample_rate)
        write_float32_wav(p['file'], ir, args.sample_rate)
        print(f"  → {p['file']}  ({len(ir)/args.sample_rate:.2f}s, "
              f"float32, {args.sample_rate}Hz)", file=sys.stderr)


if __name__ == '__main__':
    main()
