"""A pure-NumPy source-filter reference synthesizer.

This backend is deterministic and dependency-free: it turns a plan into audible
speech by exciting a formant filter with a glottal source for voiced phones and
shaping noise for obstruents. It is a *reference* — it will not be mistaken for a
neural vocoder — but it makes the whole pipeline runnable and testable offline,
and it honours every prosodic control (pitch, rate, energy) faithfully.
"""

from __future__ import annotations

import numpy as np

from prosodia.synthesis.backends.base import AcousticBackend
from prosodia.synthesis.backends.formants import (
    MURMUR_FORMANTS,
    consonant_class,
    formants_for,
)
from prosodia.synthesis.plan import Segment

_FORMANT_BW = (90.0, 110.0, 170.0)
_FORMANT_AMP = (1.0, 0.7, 0.4)


def _stable_seed(symbol: str, n: int) -> int:
    """A process-independent seed so rendered noise is reproducible."""
    return (sum(ord(c) for c in symbol) * 131 + n) % (2**32)


class FormantSynthBackend(AcousticBackend):
    name = "reference"

    def __init__(self, gain: float = 0.5, murmur_f0: float = 160.0) -> None:
        self.gain = gain
        self.murmur_f0 = murmur_f0

    # -- public ----------------------------------------------------------
    def render_segment(self, segment: Segment, sample_rate: int) -> np.ndarray:
        n = max(1, round(segment.duration * sample_rate))
        if segment.is_silence:
            return np.zeros(n, dtype=np.float32)
        if segment.is_vowel and segment.f0 is not None:
            f0 = self._upsample(segment.f0, n)
            formants = formants_for(segment.symbol)
            return self._voiced(f0, formants, sample_rate, n, segment.energy)
        return self._consonant(segment, sample_rate, n)

    # -- voiced / murmur -------------------------------------------------
    def _voiced(
        self,
        f0: np.ndarray,
        formants: tuple[float, float, float],
        sample_rate: int,
        n: int,
        energy: float,
    ) -> np.ndarray:
        phase = 2.0 * np.pi * np.cumsum(f0) / sample_rate
        # Sawtooth glottal source, rich in harmonics for the filter to shape.
        source = 2.0 * ((phase / (2.0 * np.pi)) % 1.0) - 1.0
        shaped = self._formant_filter(source, sample_rate, formants)
        env = self._amp_env(n)
        return (shaped * env * self.gain * energy).astype(np.float32)

    def _formant_filter(
        self, source: np.ndarray, sample_rate: int, formants: tuple[float, float, float]
    ) -> np.ndarray:
        spectrum = np.fft.rfft(source)
        freqs = np.fft.rfftfreq(len(source), d=1.0 / sample_rate)
        response = np.full_like(freqs, 0.05)
        for center, bw, amp in zip(formants, _FORMANT_BW, _FORMANT_AMP):
            response += amp / (1.0 + ((freqs - center) / bw) ** 2)
        filtered = np.fft.irfft(spectrum * response, n=len(source))
        filtered -= float(np.mean(filtered))  # drop DC so segment joins stay click-free
        peak = float(np.max(np.abs(filtered))) or 1.0
        return filtered / peak

    # -- obstruents ------------------------------------------------------
    def _consonant(self, segment: Segment, sample_rate: int, n: int) -> np.ndarray:
        cls = consonant_class(segment.symbol)
        energy = segment.energy or 1.0
        if cls in ("nasal", "approximant"):
            f0: np.ndarray = np.full(n, self.murmur_f0, dtype=np.float64)
            return 0.6 * self._voiced(f0, MURMUR_FORMANTS, sample_rate, n, energy)
        if cls == "plosive":
            return self._plosive(segment.symbol, sample_rate, n, energy)
        # fricative / affricate / other -> shaped noise
        return self._fricative(segment.symbol, sample_rate, n, energy)

    def _plosive(self, symbol: str, sample_rate: int, n: int, energy: float) -> np.ndarray:
        out: np.ndarray = np.zeros(n, dtype=np.float32)
        burst_len = min(n, max(1, round(0.02 * sample_rate)))
        start = n - burst_len
        rng = np.random.default_rng(_stable_seed(symbol, n))
        burst = rng.standard_normal(burst_len).astype(np.float32)
        out[start:] = burst * np.linspace(1.0, 0.0, burst_len) ** 2
        return out * (0.4 * self.gain * energy)

    def _fricative(self, symbol: str, sample_rate: int, n: int, energy: float) -> np.ndarray:
        rng = np.random.default_rng(_stable_seed(symbol, n))
        noise = rng.standard_normal(n)
        # Sibilants (s/sh/x) get a high-pass tilt; others stay broadband.
        spectrum = np.fft.rfft(noise)
        freqs = np.fft.rfftfreq(n, d=1.0 / sample_rate)
        if symbol in ("s", "sh", "x", "c", "ch"):
            tilt = np.clip(freqs / 4000.0, 0.05, 1.0)
        else:
            tilt = np.clip(1.2 - freqs / 6000.0, 0.1, 1.0)
        shaped = np.fft.irfft(spectrum * tilt, n=n)
        shaped -= float(np.mean(shaped))  # drop DC so segment joins stay click-free
        peak = float(np.max(np.abs(shaped))) or 1.0
        env = self._amp_env(n)
        return (shaped / peak * env * 0.35 * self.gain * energy).astype(np.float32)

    # -- helpers ---------------------------------------------------------
    @staticmethod
    def _upsample(frames: np.ndarray, n: int) -> np.ndarray:
        if len(frames) == n:
            return frames.astype(np.float64)
        xs = np.linspace(0.0, len(frames) - 1, n)
        return np.interp(xs, np.arange(len(frames)), frames)

    @staticmethod
    def _amp_env(n: int, fade: int = 64) -> np.ndarray:
        env: np.ndarray = np.ones(n, dtype=np.float64)
        f = min(fade, n // 2)
        if f > 0:
            ramp = 0.5 * (1.0 - np.cos(np.linspace(0.0, np.pi, f)))
            env[:f] = ramp
            env[-f:] = ramp[::-1]
        return env
