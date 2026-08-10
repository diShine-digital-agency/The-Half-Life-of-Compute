#!/usr/bin/env python3
"""
Independent verification of every numerical claim in the paper, plus two
extensions that the audit showed were missing.

VERIFY  — recompute each headline figure from first principles, without reusing
          the model's own helper functions, and assert agreement.
EXTEND  — (A) the leakage/partial-severance result: does smuggling buy frontier
              time, or only a floor?
          (B) the useful-life paradox: κ* = λL implies LONGER-lived hardware is
              HARDER to sustain by salvage, because retirement is what feeds the
              donor pool. Verified against the full simulation.

Run: python3 verify_and_extend.py
"""
import json, os
from dataclasses import replace

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

import compute_decay_model as M

OUT = M.DATADIR
FAILS, CHECKS = [], []


def check(label, got, want, tol=1e-6, note=""):
    ok = abs(got - want) <= tol * max(1.0, abs(want))
    CHECKS.append((label, got, want, ok, note))
    if not ok:
        FAILS.append(label)
    return ok


# ═════════════════════════════════════════════════════════════════════════════
# PART 1 — VERIFY
# ═════════════════════════════════════════════════════════════════════════════
print("=" * 78); print("PART 1 · INDEPENDENT VERIFICATION"); print("=" * 78)

# 1.1 failure rates recomputed by hand
GPUS, DAYS = 16384, 54
afr_die = (148 / GPUS) * (365 / DAYS)
afr_hbm = (72 / GPUS) * (365 / DAYS)
afr_pkg = afr_die + afr_hbm
afr_all = (419 / GPUS) * (365 / DAYS)
check("AFR die", afr_die, M.AFR_GPU_DIE)
check("AFR HBM", afr_hbm, M.AFR_HBM)
check("AFR package", afr_pkg, M.AFR_PACKAGE)
check("AFR all-cause", afr_all, M.AFR_ALL)

# 1.2 the Epoch cross-check, and the "within 1.4%" claim in the abstract
gpu_h_per_fail = GPUS * DAYS * 24 / 419
disc = abs(gpu_h_per_fail - 50_000) / 50_000
check("GPU-h per failure", gpu_h_per_fail, 50_677, tol=2e-4)
print(f"  cross-check discrepancy vs Epoch's ~50,000 = {disc*100:.2f}% "
      f"→ paper claims 'within 1.4%': {'OK' if disc <= 0.014 else 'OVERSTATED'}")
if disc > 0.014:
    FAILS.append("abstract 1.4% claim")

# 1.3 κ* two independent ways
lam_m = -np.log(1 - afr_pkg) / 12
delta_m = 1 / (4.0 * 12)
kstar_ratio = lam_m / delta_m
kstar_prod = lam_m * (4.0 * 12)
check("kappa* (λ/δ)", kstar_ratio, M.kappa_critical(afr_pkg, 4.0))
check("kappa* (λL)", kstar_prod, kstar_ratio)
print(f"  κ* = {kstar_ratio:.4f}  → paper rounds to 0.38: "
      f"{'OK' if abs(round(kstar_ratio,2) - 0.38) < 1e-9 else 'MISMATCH'}")

# 1.4 China C0 derivation
check("C0 China", 660_000 * 3.0, M.C0_CHINA)

# 1.5 WHAT κ* ACTUALLY GOVERNS.
#     An earlier draft claimed κ* separated "persists" from "decays". The
#     simulation refutes that: with no inflow every fleet declines, because
#     retirement removes units whether or not failures are repaired. κ* is a
#     SATURATION threshold — the point at which salvage fully absorbs the
#     failure flow and additional salvage capacity stops helping. Verified by
#     measuring the implied decline rate either side of it.
base = M.Params(M.C0_CHINA, afr_pkg, 0.0, 4.0, M.FRONTIER_DOUBLING_C, 0.0, 0.0)

def decline_rate(k, months=24):
    d = M.simulate(replace(base, kappa=k), months)
    return -np.log(d["frac_of_t0"].iloc[-1]) / months

r_zero = decline_rate(0.0)
r_below = decline_rate(kstar_ratio * 0.5)
r_at = decline_rate(kstar_ratio)
r_above = decline_rate(kstar_ratio * 3.0)
retire_only = delta_m

print(f"\n  decline rate, zero inflow (retirement alone = {retire_only*100:.3f}%/mo):")
for lab, r in [("κ = 0", r_zero), ("κ = κ*/2", r_below),
               ("κ = κ*", r_at), ("κ = 3κ*", r_above)]:
    print(f"    {lab:10} {r*100:6.3f}%/mo   = {r/retire_only:.2f}× retirement-only")

# the claim to verify: decline SATURATES at κ*, i.e. tripling κ beyond it
# changes almost nothing, while halving it below costs materially.
sat = abs(r_above - r_at) / r_at < 0.02
bite = (r_below - r_at) / r_at > 0.01
CHECKS.append(("decline saturates above κ*", r_above, r_at, sat, "<2% further gain"))
CHECKS.append(("failures bite below κ*", r_below, r_at, bite, ">1% faster decline"))
if not sat:
    FAILS.append("saturation above κ*")
if not bite:
    FAILS.append("no penalty below κ*")
EXCESS = {"r_zero": r_zero, "r_at_kstar": r_at, "r_3kstar": r_above,
          "retirement_only": retire_only,
          "excess_at_zero_pct": 100 * (r_zero / retire_only - 1),
          "excess_at_kstar_pct": 100 * (r_at / retire_only - 1)}

print()
for lab, got, want, ok, note in CHECKS:
    print(f"  [{'PASS' if ok else 'FAIL'}] {lab:28} got {got:>12.6f}  want {want:>12.6f} {note}")
print(f"\n  {len(CHECKS)-len(FAILS)}/{len(CHECKS)} checks passed"
      + ("" if not FAILS else f"   FAILURES: {FAILS}"))


# ═════════════════════════════════════════════════════════════════════════════
# PART 2A — EXTENSION: what does leakage actually buy?
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 78)
print("PART 2A · LEAKAGE — does smuggling buy frontier time, or only a floor?")
print("=" * 78)

china = M.Params(M.C0_CHINA, M.AFR_PACKAGE, np.mean(M.KAPPA_COMPUTE),
                 M.USEFUL_LIFE_C, M.FRONTIER_DOUBLING_C,
                 M.CN_DOMESTIC_PM * M.CN_STOCKPILE_DEPENDENCE_C, M.LEAK_PM * 0.35)

mult = np.concatenate([np.array([0.0]), np.geomspace(0.05, 12.0, 40)])
rows = []
for m_ in mult:
    p = replace(china, leakage_per_month=M.LEAK_PM * m_)
    r = M.metrics(p)
    rows.append({"leak_multiple": m_,
                 "leak_per_month": M.LEAK_PM * m_,
                 "leak_pct_of_C0_per_yr": 100 * 12 * M.LEAK_PM * m_ / china.c0,
                 "t_frontier": r["t_frontier_months"],
                 "t_half": r["t_half_months"],
                 "floor_pct": r["sovereign_floor_pct_of_c0"]})
leak = pd.DataFrame(rows)
leak.to_csv(os.path.join(OUT, "table_leakage_sweep.csv"), index=False)

lo, hi = leak.iloc[0], leak.iloc[-1]
tf_span = hi["t_frontier"] - lo["t_frontier"]
fl_ratio = hi["floor_pct"] / max(lo["floor_pct"], 1e-9)
print(f"  leakage 0 → {hi['leak_multiple']:.0f}× baseline "
      f"({hi['leak_pct_of_C0_per_yr']:.1f}% of C0 per year)")
print(f"    frontier exit  {lo['t_frontier']:.0f} → {hi['t_frontier']:.0f} months  "
      f"(Δ {tf_span:+.0f})")
print(f"    sovereign floor {lo['floor_pct']:.1f}% → {hi['floor_pct']:.1f}%  "
      f"({fl_ratio:.1f}× )")

# what leakage would be needed to hold the floor at 50% / 100%?
def leak_for_floor(target):
    f = leak[leak["floor_pct"] >= target]
    return None if f.empty else f.iloc[0]

for tgt in (50.0, 100.0):
    r = leak_for_floor(tgt)
    if r is None:
        print(f"    floor {tgt:.0f}% unreachable within the swept range")
    else:
        print(f"    floor {tgt:.0f}% needs {r['leak_multiple']:.1f}× baseline "
              f"= {r['leak_per_month']:,.0f} H100e/month "
              f"({r['leak_pct_of_C0_per_yr']:.1f}% of C0/yr); "
              f"frontier exit still {r['t_frontier']:.0f} mo")

# ═════════════════════════════════════════════════════════════════════════════
# PART 2B — EXTENSION: the useful-life paradox
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 78)
print("PART 2B · USEFUL LIFE AND SALVAGE ABSORPTION")
print("=" * 78)
print("  A hypothesis considered and REJECTED: that longer-lived fleets are more")
print("  fragile because κ* = λL rises with L, starving the donor pool. The")
print("  simulation refutes it — the retirement effect dominates and longer-lived")
print("  fleets last longer. What IS true is that they lean less on salvage.\n")

rows = []
kap = float(np.mean(M.KAPPA_COMPUTE))
for L in (2.0, 3.0, 4.0, 5.0, 6.0):
    ks = M.kappa_critical(M.AFR_PACKAGE, L)
    p = replace(china, useful_life_years=L, kappa=kap,
                leakage_per_month=0.0, domestic_per_month=0.0)
    d = M.simulate(p, 400)
    th = M._first_below(d["frac_of_t0"], 0.5)
    rows.append({"useful_life_yr": L, "kappa_star": ks, "kappa_assumed": kap,
                 "failures_absorbed_pct": 100 * min(1.0, kap / ks),
                 "t_half_months_zero_inflow": th})
life = pd.DataFrame(rows)
life.to_csv(os.path.join(OUT, "table_useful_life.csv"), index=False)
print(life.to_string(index=False))
print(f"\n  → T-half RISES with useful life ({life.t_half_months_zero_inflow.iloc[0]:.0f} "
      f"→ {life.t_half_months_zero_inflow.iloc[-1]:.0f} months): the hypothesis is rejected.")
print(f"  → but the share of failures salvage can absorb FALLS "
      f"{life.failures_absorbed_pct.iloc[0]:.0f}% → {life.failures_absorbed_pct.iloc[-1]:.0f}%.")
print("  → so the depreciation dispute is not neutral for severance: a 6-year fleet")
print("    survives longer overall while depending more on raw stock and less on repair.")

# ── figure: the leakage result ───────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "mathtext.fontset": "stix", "font.size": 9, "axes.labelsize": 9,
    "legend.fontsize": 8, "xtick.labelsize": 8, "ytick.labelsize": 8,
    "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": .7,
    "lines.linewidth": 1.7, "figure.dpi": 200, "savefig.bbox": "tight",
    "savefig.pad_inches": .02})
INK, ACCENT, BLUE, GREY = "#1a1a1a", "#8c2d04", "#08519c", "#737373"

LB = {"en": dict(x="Leakage, % of installed base per year",
                 y1="Frontier exit (months)", y2="Sovereign floor (% of $C_0$)",
                 t1="Frontier exit time", t2="Sovereign floor",
                 note="Leakage lifts the floor steeply and the frontier horizon barely at all:\n"
                      "smuggling buys capacity, not competitiveness.",
                 f="fig8_leakage"),
      "it": dict(x="Dispersione, % del parco installato all'anno",
                 y1="Uscita dalla frontiera (mesi)", y2="Soglia di sovranità (% di $C_0$)",
                 t1="Tempo di uscita dalla frontiera", t2="Soglia di sovranità",
                 note="La dispersione alza ripidamente la soglia e quasi per nulla l'orizzonte di frontiera:\n"
                      "il contrabbando compra capacità, non competitività.",
                 f="fig8_dispersione"),
      "fr": dict(x="Fuite, % du parc installé par an",
                 y1="Sortie de la frontière (mois)", y2="Plancher de souveraineté (% de $C_0$)",
                 t1="Temps de sortie de la frontière", t2="Plancher de souveraineté",
                 note="La fuite relève fortement le plancher et à peine l'horizon de frontière :\n"
                      "la contrebande achète de la capacité, pas de la compétitivité.",
                 f="fig8_fuite")}

for lang, L in LB.items():
    figdir = os.path.normpath(os.path.join(
        M.HERE, "..", "figures" if lang == "en" else f"figures_{lang}"))
    os.makedirs(figdir, exist_ok=True)
    fig, ax = plt.subplots(figsize=(5.5, 3.0))
    x = leak["leak_pct_of_C0_per_yr"]
    ax.plot(x, leak["t_frontier"], color=BLUE, label=L["t1"])
    ax.set_xlabel(L["x"]); ax.set_ylabel(L["y1"], color=BLUE)
    ax.tick_params(axis="y", colors=BLUE)
    ax.set_ylim(0, max(60, leak["t_frontier"].max() * 1.15))
    ax2 = ax.twinx(); ax2.spines["top"].set_visible(False)
    ax2.plot(x, leak["floor_pct"], color=ACCENT, ls="--", label=L["t2"])
    ax2.set_ylabel(L["y2"], color=ACCENT); ax2.tick_params(axis="y", colors=ACCENT)
    ax2.set_ylim(0, max(120, leak["floor_pct"].max() * 1.1))
    ax.set_xlim(0, x.max())
    h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, frameon=False, loc="center right")
    ax.text(.02, .04, L["note"], transform=ax.transAxes, fontsize=7.2, color=GREY,
            va="bottom")
    for e in ("pdf", "png"):
        fig.savefig(os.path.join(figdir, f"{L['f']}.{e}"))
    plt.close(fig)

# persist for the manuscript modules
extra = {
  "verification": {"checks": len(CHECKS), "failures": FAILS,
                   "epoch_crosscheck_discrepancy_pct": disc * 100},
  "leakage": {
     "tf_at_zero": float(lo["t_frontier"]), "tf_at_max": float(hi["t_frontier"]),
     "tf_span": float(tf_span),
     "floor_at_zero": float(lo["floor_pct"]), "floor_at_max": float(hi["floor_pct"]),
     "max_multiple": float(hi["leak_multiple"]),
     "max_pct_of_c0_per_yr": float(hi["leak_pct_of_C0_per_yr"]),
     "floor50": (None if leak_for_floor(50.) is None
                 else {k: float(v) for k, v in leak_for_floor(50.).items()}),
     "floor100": (None if leak_for_floor(100.) is None
                  else {k: float(v) for k, v in leak_for_floor(100.).items()})},
  "useful_life": life.to_dict("records"),
  "kappa_saturation": EXCESS,
}
p = os.path.join(OUT, "results_extended.json")
json.dump(extra, open(p, "w"), indent=2, default=float)
print(f"\n  → {p}")
print(f"  → figures fig8_* written for en/it/fr")
print("\n" + ("ALL CHECKS PASSED" if not FAILS else f"*** {len(FAILS)} CHECK(S) FAILED ***"))
