"""
Python replication of the simulator in index.html.

Three-region Krugman (1991) core-periphery model with a congestion cost
(real wage = w * G^-mu * N^-delta), following the normalisation in
Fujita, Krugman & Venables (1999, ch. 5). Regions: London & South East,
North West (Manchester), Yorkshire & the Humber (Leeds).

Trade costs are tied to rail journey times: tau = 1 + theta * hours.

Run:  python3 model.py              central calibration + sensitivity table
      python3 model.py 0.06 0.45    a chosen (delta, theta)
Requires numpy.
"""
import sys
import numpy as np

MU, SIGMA = 0.3, 5.0
# Immobile shares: ONS mid-2025 population (ICAEW, 2026): London 9.1m + South East 9.7m, North West 7.7m, Yorkshire & Humber 5.7m
PHI = np.array([18.8, 7.7, 5.7]) / 32.2
# Starting footloose shares: financial & related professional services jobs, 2023 (TheCityUK, 2025): 1,182k / 298k / 149k
START = np.array([1182, 298, 149]) / 1629
FLOOR = 1e-6

# Journey times in minutes: (London-Manchester, London-Leeds, Manchester-Leeds)
# Today: HS2 Ltd (2014), ITV News (2021), DfT (2021). HS2: DfT (2021), ITV News (2021). NPR: DfT (2021).
PRESETS = {
    "today": (128, 133, 55),
    "hs2":   (71, 81, 55),
    "npr":   (128, 133, 33),
    "both":  (71, 81, 33),
}

def tmat(mins, theta):
    t = [1 + theta * m / 60 for m in mins]
    return np.array([[1, t[0], t[1]], [t[0], 1, t[2]], [t[1], t[2], 1]], float)

def short_run(lam, T, delta, w0=None):
    """Solve wages and price indices for a given distribution of mobile workers."""
    w = np.ones(3) if w0 is None else w0.copy()
    for _ in range(4000):
        Y = MU * lam * w + (1 - MU) * PHI
        G = (lam[:, None] * (w[:, None] * T) ** (1 - SIGMA)).sum(0) ** (1 / (1 - SIGMA))
        w_new = ((Y[None, :] * T ** (1 - SIGMA) * G[None, :] ** (SIGMA - 1)).sum(1)) ** (1 / SIGMA)
        done = np.max(abs(w_new - w)) < 1e-10
        w = 0.5 * w + 0.5 * w_new
        if done:
            break
    N = MU * lam + (1 - MU) * PHI          # total workers in each region
    crowd = N ** (-delta)
    omega = w * G ** (-MU) * crowd         # real wage of mobile workers
    immobile_real = G ** (-MU) * crowd     # real income of immobile residents (wage = 1)
    return w, G, N, omega, immobile_real

def long_run(lam, T, delta, rate=0.2, max_steps=8000):
    """Mobile workers move towards above-average real wages until no one gains by moving."""
    lam = np.array(lam, float); w = None
    for i in range(max_steps):
        w, _, _, om, _ = short_run(lam, T, delta, w)
        new = np.maximum(FLOOR, lam + rate * lam * (om - (lam * om).sum()))
        new /= new.sum()
        if np.max(abs(new - lam)) < 1e-9 and i > 50:
            return new
        lam = new
    return lam

def scenarios(delta, theta):
    today = long_run(START, tmat(PRESETS["today"], theta), delta)
    out = {"today": today}
    for k in ("hs2", "npr", "both"):
        out[k] = long_run(today, tmat(PRESETS[k], theta), delta)
    return out

def report(delta, theta):
    out = scenarios(delta, theta)
    _, _, _, om0, f0 = short_run(out["today"], tmat(PRESETS["today"], theta), delta)
    mob0 = (out["today"] * om0).sum()
    print(f"\ndelta = {delta}, theta = {theta}")
    print("Scenario  footloose (L/NW/Y)       all jobs (L/NW/Y)        mobile wage  immobile real income (L/NW/Y)")
    for k, lam in out.items():
        _, _, N, om, f = short_run(lam, tmat(PRESETS[k], theta), delta)
        print(f"{k:8s}  " + "/".join(f"{100*x:5.1f}" for x in lam) + "   " + "/".join(f"{100*x:5.1f}" for x in N)
              + f"   {100*((lam*om).sum()/mob0-1):+5.1f}%      " + "/".join(f"{100*(f[i]/f0[i]-1):+.1f}%" for i in range(3)))

if __name__ == "__main__":
    if len(sys.argv) == 3:
        report(float(sys.argv[1]), float(sys.argv[2]))
    else:
        report(0.08, 0.45)
        print("\nSensitivity: London & SE share of footloose industry (today / HS2 / NPR / both)")
        for d in (0.06, 0.08):
            for th in (0.35, 0.45, 0.60):
                o = scenarios(d, th)
                print(f"  delta={d:.2f} theta={th:.2f}: " + "  ".join(f"{100*o[k][0]:.0f}%" for k in ("today", "hs2", "npr", "both")))
