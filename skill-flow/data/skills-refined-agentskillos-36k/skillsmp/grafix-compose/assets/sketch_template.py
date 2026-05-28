from __future__ import annotations

import math

from grafix import E, G

W, H = 800, 800


def _ease_in_out(x: float) -> float:
    x = float(x)
    x = 0.0 if x < 0.0 else 1.0 if x > 1.0 else x
    return x * x * (3.0 - 2.0 * x)


def draw(t: float):
    """作品の 1 フレームを生成する。

    Parameters
    ----------
    t : float
        フレーム時刻。慣例として 0..1 を想定（ループ）。
    """
    tt = _ease_in_out((math.sin(float(t) * math.tau) + 1.0) * 0.5)

    base = G.polygon(n_sides=6, center=(W * 0.5, H * 0.5, 0), scale=300)
    fx = E.rotate(rotation=(0, 0, 360.0 * tt)).displace(amplitude=(4, 4, 0))
    return fx(base)

