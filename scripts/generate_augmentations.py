#!/usr/bin/env python3
"""
Illustrative augmentation demo: take one GMD clip and show the three augmentation
families used in the study (Gaussian noise, room simulation, time stretch) as
log-mel spectrograms + playable audio. Approximations for visualisation; the study
itself used the `audiomentations` library.

Outputs:
  public/figures/augmentation-spectrograms.webp  (2x2 mel spectrograms)
  public/audio/aug-{original,noise,room,stretch}.wav
  src/data/augmentation-demo.json
"""
import json
import numpy as np
from scipy.io import wavfile
from scipy import signal
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "public" / "audio" / "drummer8_session1_2_001.wav"   # funk, 95 bpm
AUD = ROOT / "public" / "audio"
FIG = ROOT / "public" / "figures"
SR_DEFAULT = 16000

def hz_to_mel(f): return 2595.0 * np.log10(1.0 + f / 700.0)
def mel_to_hz(m): return 700.0 * (10.0 ** (m / 2595.0) - 1.0)

def mel_fb(sr, n_fft, n_mels=64):
    fmax = sr / 2
    pts = mel_to_hz(np.linspace(hz_to_mel(0), hz_to_mel(fmax), n_mels + 2))
    bins = np.floor((n_fft + 1) * pts / sr).astype(int)
    fb = np.zeros((n_mels, n_fft // 2 + 1))
    for m in range(1, n_mels + 1):
        l, c, r = bins[m - 1], bins[m], bins[m + 1]
        for k in range(l, c): fb[m - 1, k] = (k - l) / max(1, c - l)
        for k in range(c, r): fb[m - 1, k] = (r - k) / max(1, r - c)
    return fb

def logmel(x, sr, n_fft=1024, hop=256, n_mels=64):
    f, t, Z = signal.stft(x, sr, nperseg=n_fft, noverlap=n_fft - hop)
    power = np.abs(Z) ** 2
    fb = mel_fb(sr, n_fft, n_mels)
    return np.log(fb @ power + 1e-6)

def norm(x):
    m = np.max(np.abs(x))
    return x / m if m > 0 else x

def main():
    sr, x = wavfile.read(SRC)
    x = x.astype(np.float32)
    if x.ndim > 1: x = x.mean(axis=1)
    x = norm(x)
    rng = np.random.RandomState(42)

    # Gaussian noise
    noise = x + rng.normal(0, 0.02, len(x))
    noise = norm(noise)
    # Room simulation: convolve with a short exponentially-decaying impulse response
    ir_len = int(0.28 * sr)
    ir = rng.randn(ir_len) * np.exp(-np.linspace(0, 6, ir_len))
    room = np.convolve(x, ir)[: len(x)]
    room = norm(room)
    # Time stretch (illustrative, ~1.25x longer via resampling)
    stretch = signal.resample(x, int(len(x) * 1.25))
    stretch = norm(stretch)

    variants = {"original": (x, sr), "noise": (noise, sr), "room": (room, sr), "stretch": (stretch, sr)}
    for name, (y, s) in variants.items():
        wavfile.write(AUD / f"aug-{name}.wav", s, (y * 32767).astype(np.int16))

    titles = {"original": "Original", "noise": "+ Gaussian noise", "room": "+ Room simulation", "stretch": "+ Time stretch"}
    fig, axes = plt.subplots(2, 2, figsize=(11, 6))
    for ax, name in zip(axes.flat, ["original", "noise", "room", "stretch"]):
        y, s = variants[name]
        M = logmel(y, s)
        ax.imshow(M, aspect="auto", origin="lower", cmap="magma",
                  extent=[0, len(y) / s, 0, s / 2000])
        ax.set_title(titles[name], fontsize=12)
        ax.set_xlabel("time (s)", fontsize=9)
        ax.set_ylabel("kHz", fontsize=9)
        ax.tick_params(labelsize=8)
    fig.suptitle("Augmentation effects on a two-bar funk groove (log-mel spectrogram)", fontsize=13)
    fig.tight_layout()
    png = FIG / "augmentation-spectrograms.png"
    fig.savefig(png, dpi=130, bbox_inches="tight")
    plt.close(fig)
    subprocess.run(["cwebp", "-quiet", "-q", "86", str(png), "-o", str(FIG / "augmentation-spectrograms.webp")], check=True)
    png.unlink()

    meta = {
        "sourceClip": "drummer8_session1_2_001.wav",
        "style": "funk", "bpm": 95,
        "note": "Illustrative augmentations applied to one GMD clip for visualisation. The study used the audiomentations library; the time-stretch here is resampling-based.",
        "variants": [
            {"key": "original", "label": "Original", "file": "/audio/aug-original.wav"},
            {"key": "noise", "label": "+ Gaussian noise", "file": "/audio/aug-noise.wav"},
            {"key": "room", "label": "+ Room simulation", "file": "/audio/aug-room.wav"},
            {"key": "stretch", "label": "+ Time stretch", "file": "/audio/aug-stretch.wav"},
        ],
        "spectrogram": "/figures/augmentation-spectrograms.webp",
    }
    (ROOT / "src" / "data" / "augmentation-demo.json").write_text(json.dumps(meta, indent=2))
    print("✓ augmentation spectrograms + 4 audio variants + augmentation-demo.json")
    for n in ["original", "noise", "room", "stretch"]:
        print(f"  aug-{n}.wav {(AUD / f'aug-{n}.wav').stat().st_size // 1024} KB")
    print(f"  spectrogram {(FIG / 'augmentation-spectrograms.webp').stat().st_size // 1024} KB")

if __name__ == "__main__":
    main()
