#!/usr/bin/env python3
"""
The Half-Life of Compute — severance decay model.
Escoda (2026). Reproduction script.

Every parameter carries its source. Nothing is invented: values are either
(a) taken from a cited source, or (b) derived arithmetically from cited
sources, with the derivation shown in code.

Run:  python3 compute_decay_model.py
Out:  ../figures/*.pdf|png ; ../../03-DATA/processed/*.csv ; results.json
"""
from __future__ import annotations

import json, os
from dataclasses import dataclass, asdict, replace

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

RNG = np.random.default_rng(20260808)
HERE = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.normpath(os.path.join(HERE, "..", "figures"))
DATADIR = os.path.normpath(os.path.join(HERE, "..", "..", "03-DATA", "processed"))
os.makedirs(FIGDIR, exist_ok=True); os.makedirs(DATADIR, exist_ok=True)

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "mathtext.fontset": "stix", "font.size": 9, "axes.labelsize": 9,
    "axes.titlesize": 9.5, "legend.fontsize": 7.6, "xtick.labelsize": 8,
    "ytick.labelsize": 8, "axes.spines.top": False, "axes.spines.right": False,
    "axes.linewidth": .7, "xtick.major.width": .7, "ytick.major.width": .7,
    "lines.linewidth": 1.5, "figure.dpi": 200, "savefig.bbox": "tight",
    "savefig.pad_inches": .02,
})
INK, ACCENT, BLUE, GREY, LGREY, GREEN = "#1a1a1a", "#8c2d04", "#08519c", "#737373", "#d9d9d9", "#00441b"

# ═════════════════════════════════════════════════════════════════════════════
# 1 · PARAMETERS
# ═════════════════════════════════════════════════════════════════════════════
# 1.1 Failure rates — derived from Grattafiori et al. (2024) arXiv:2407.21783.
#     16,384 H100 GPUs, 54-day pre-training window, 419 interruptions:
#     faulty GPU 148 (30.1%) · GPU HBM3 72 (17.2%) · network 35 (8.4%)
LLAMA3_GPUS, LLAMA3_DAYS = 16_384, 54
FAIL_GPU_DIE, FAIL_HBM, FAIL_ALL = 148, 72, 419

def _afr(n):                                    # events per GPU per year
    return (n / LLAMA3_GPUS) * (365.0 / LLAMA3_DAYS)

AFR_GPU_DIE  = _afr(FAIL_GPU_DIE)               # ≈ 0.0611
AFR_HBM      = _afr(FAIL_HBM)                   # ≈ 0.0297
AFR_PACKAGE  = AFR_GPU_DIE + AFR_HBM            # ≈ 0.0908  ← headline
AFR_ALL      = _afr(FAIL_ALL)                   # ≈ 0.1729
# Cross-check vs Epoch AI (~1 failure / 50,000 GPU-hours, all causes):
XCHECK_GPUH = LLAMA3_GPUS * LLAMA3_DAYS * 24 / FAIL_ALL   # ≈ 50,677 ✓
EPOCH_GPUH = 50_000

# 1.2 Cannibalisation yield κ — repairs recoverable per unit withdrawn.
KAPPA_AVIATION = 10.0            # Russian civil fleet: ~1 airframe per ~10 kept flying
KAPPA_COMPUTE  = (0.05, 0.50)    # HBM is co-packaged (CoWoS); neither die nor stack
                                 # is field-replaceable ⇒ dominant failure modes are
                                 # non-salvageable by construction.

# 1.3 Obsolescence — the FRONTIER TRAINING-COMPUTE series.
#   CORRECTION (2026-08-08). An earlier draft used Epoch AI's NVIDIA *installed
#   stock* doubling time (~10 months) as the growth rate of the frontier
#   TRAINING scale. Those are different series. Epoch reports frontier training
#   compute growing 4–5x/year, doubling every ~5.2 months since 2020
#   (epoch.ai/blog/training-compute-of-frontier-ai-models-grows-by-4-5x-per-year);
#   notable models doubling ~6 months (epoch.ai/data-insights/compute-trend-post-2010).
#   The band below brackets the 4.4x/yr long-run and 5x/yr post-2020 estimates.
FRONTIER_DOUBLING = (4.8, 7.0); FRONTIER_DOUBLING_C = 5.2

# 1.3b Absolute frontier anchor F0 — compute of the largest contemporaneous
#   training run, in H100-equivalents. Derivation (shown so it can be contested):
#   a frontier run of 1e26-1e27 FLOP; an H100 sustains ~4e14 FLOP/s effective
#   BF16, so ~3e21 FLOP per accelerator over a 3-month run; hence
#   1e26/3e21 ~ 3.3e4 to 1e27/3e21 ~ 3.3e5 H100e. Swept, never a point value.
FRONTIER_SCALE = (5.0e4, 5.0e5); FRONTIER_SCALE_C = 1.5e5
FRONTIER_THRESHOLD = 0.10          # "competitive" share of a frontier run
# 1.4 Economic useful life — the 2025–26 depreciation dispute (2–3 yr vs 5–6 yr).
USEFUL_LIFE = (2.0, 6.0); USEFUL_LIFE_C = 4.0

# 1.5 Installed stock C0 (H100-equivalents)
GLOBAL_H100E = 15_000_000                        # Epoch AI
CH_SMUG_MED, CH_SMUG_LO, CH_SMUG_HI = 660_000, 290_000, 1_600_000
C0_CHINA = CH_SMUG_MED * 3.0                     # Epoch: median ≈ 1/3 of China's total
C0_US = GLOBAL_H100E * 0.70                      # swept 0.60–0.78 (firm→jurisdiction)
C0_EU = GLOBAL_H100E * 0.04                      # swept 0.02–0.06 (weak evidence)
US_SHARE, EU_SHARE = (0.60, 0.78), (0.02, 0.06)

# 1.6 Domestic replacement
#   CORRECTION (2026-08-08). Epoch AI's 530k H100e for Huawei in 2025 is
#   REALISED chip output — the source states "Our data tracks chip sales, not
#   deployments" — so it already embodies whatever yield Huawei achieved. An
#   earlier draft multiplied it by (0.30/0.90), applying yield a second time.
#   That haircut is removed. A downward adjustment may still be warranted on a
#   different and separately sourced ground — 2025 output was partly fed by the
#   ~2.9M pre-control TSMC die stockpile — so we sweep a STOCKPILE-DEPENDENCE
#   factor instead, and label it as such rather than as yield.
HUAWEI_H100E_2025 = 530_000
CN_DOMESTIC_PM = HUAWEI_H100E_2025 / 12.0
CN_STOCKPILE_DEPENDENCE = (0.30, 1.00)   # share of 2025 output replicable w/o the stockpile
CN_STOCKPILE_DEPENDENCE_C = 0.65
CN_YIELD = (0.20, 0.40); TSMC_YIELD = 0.90       # retained for reference only
# Severance is modelled symmetrically: each jurisdiction is cut off from the
# inputs it does not control. The United States is NOT self-sufficient — it has
# no domestic EUV source (ASML, NL), limited leading-edge capacity (TSMC Arizona,
# Intel, Samsung Taylor all partial/ramping), and no domestic HBM at scale
# (SK Hynix + Samsung ≈ 90% of supply, both Korean). Its coverage is therefore a
# scenario band, not unity.
US_COVERAGE_RANGE, EU_COVERAGE_RANGE = (0.15, 0.35), (0.01, 0.04)
US_COVERAGE, EU_COVERAGE = 0.25, 0.02

# 1.7 Leakage — Epoch AI (Juniewicz 2026), spread over 2024–25, enforcement haircut
LEAK_PM = CH_SMUG_MED / 24.0
LEAK_SUPPRESS = (0.10, 0.60)

HORIZON = 120
LONG_HORIZON = 900        # for the sovereign-floor asymptote
SACRIFICE_CAP = 0.03      # max fraction of fleet withdrawn per month for parts


@dataclass
class Params:
    c0: float; afr: float; kappa: float
    useful_life_years: float; frontier_doubling_months: float
    domestic_per_month: float; leakage_per_month: float
    utilisation_ceiling: float = 1.0
    frontier_scale: float = FRONTIER_SCALE_C   # absolute anchor F0, H100e
    dom_growth_yr: float = 0.0                 # indigenisation growth g, per year


# ═════════════════════════════════════════════════════════════════════════════
# 2 · THE MODEL
# ═════════════════════════════════════════════════════════════════════════════
def simulate(p: Params, months: int = HORIZON) -> pd.DataFrame:
    """
    Monthly integration.  State: N operational units, P salvageable-repair pool.

      1. F   = N·λ      hardware failures (units go offline)
      2. Ret = N·δ      obsolescence retirement (intact but frontier-obsolete)
      3. repairs drawn from P
      4. failed-unrepaired and retired units become donors, each yielding κ repairs
      5. if κ > 1, withdrawing a SERVICEABLE unit is net-positive (κ repairs for
         one unit): the operator does so against the outstanding backlog. This is
         the aviation dynamic and it actively shrinks the fleet.
         If κ < 1 it is never rational, so no serviceable unit is withdrawn.
      6. inflow = domestic production + leakage
    """
    lam = -np.log(max(1e-12, 1.0 - p.afr)) / 12.0
    delta = 1.0 / (p.useful_life_years * 12.0)
    n, pool = float(p.c0), 0.0
    rows = []
    for t in range(months + 1):
        eff = n * p.utilisation_ceiling
        # Frontier position is measured against an ABSOLUTE, jurisdiction-common
        # anchor. An earlier draft divided by the jurisdiction's OWN c0, which
        # forced every jurisdiction to start at 1.0 and made c0 cancel
        # identically — so "invariance to installed stock" was an algebraic
        # identity, not a finding. See Appendix A.
        f_t = p.frontier_scale * (2.0 ** (t / p.frontier_doubling_months))
        rows.append({"month": t, "operational": n, "effective": eff,
                     "frac_of_t0": eff / p.c0 if p.c0 else 0.0,
                     "frontier_relative": eff / f_t if f_t else 0.0,
                     "pool": pool})
        if t == months:
            break

        F, Ret = n * lam, n * delta
        rep = min(F, pool); pool -= rep
        backlog = F - rep
        pool += p.kappa * (backlog + Ret)          # dead + retired units donate

        sacrificed = 0.0
        if p.kappa > 1.0 and backlog > 0:          # withdrawing serviceable units pays
            want = backlog / p.kappa
            sacrificed = min(want, n * SACRIFICE_CAP)
            pool += p.kappa * sacrificed
            rep2 = min(backlog, pool); pool -= rep2
            rep += rep2

        # domestic output may grow (induced substitution) or shrink (tool
        # attrition under severance); g = 0 recovers the frozen-output case.
        dom_t = p.domestic_per_month * (1.0 + p.dom_growth_yr) ** (t / 12.0)
        n = max(0.0, n - F - Ret - sacrificed + rep + dom_t + p.leakage_per_month)
    return pd.DataFrame(rows)


CENSORED = float("inf")

def _first_below(a, thr):
    i = np.nonzero(np.asarray(a) < thr)[0]
    return float(i[0]) if i.size else CENSORED


def kappa_critical(afr: float, useful_life_years: float) -> float:
    """
    Critical cannibalisation ratio κ*.

    Salvage supply per period is κ·(retirements + unrepaired failures); repair
    demand is the failure flow. Retirements alone sustain repair when

        κ · N·δ  ≥  N·λ      ⇒      κ* = λ / δ = λ · L

    with λ the monthly hazard, δ = 1/L the monthly retirement rate and L the
    useful life in months. Above κ* the salvage pool is self-replenishing and the
    installed base persists; below it the base decays monotonically. κ* is a
    property of the hardware, not of policy.
    """
    lam = -np.log(max(1e-12, 1.0 - afr)) / 12.0
    return lam * (useful_life_years * 12.0)


def floor_closed_form(p: Params) -> float:
    """
    Exact asymptote of Eq. 2 at g = 0, as a share of C0.

        C_inf/C0 = (R_dom + R_leak) (1 + min(kappa, kappa*)) / (C0 (lambda + delta))

    Reported because an earlier draft claimed no closed form existed. Note the
    consequence: where R_dom is parameterised as cov*C0*(lambda+delta) — the US
    and EU cases — this collapses to cov*(1 + min(kappa, kappa*)), independent
    of C0, lambda and L. Those two "floors" are the coverage assumption rescaled,
    not model outputs.
    """
    lam = -np.log(max(1e-12, 1.0 - p.afr)) / 12.0
    delta = 1.0 / (p.useful_life_years * 12.0)
    kstar = lam / delta
    R = p.domestic_per_month + p.leakage_per_month
    return R * (1.0 + min(p.kappa, kstar)) / (p.c0 * (lam + delta))


def metrics(p: Params) -> dict:
    d = simulate(p, HORIZON)
    long = simulate(p, LONG_HORIZON)
    floor = float(long["frac_of_t0"].iloc[-1])
    fr = d["frac_of_t0"].to_numpy()
    return {"t_half_months": _first_below(d["frac_of_t0"], 0.50),
            "t_frontier_months": _first_below(d["frontier_relative"], FRONTIER_THRESHOLD),
            "sovereign_floor_pct_of_c0": 100.0 * floor,
            "sovereign_floor_closed_form_pct": 100.0 * floor_closed_form(p),
            "sovereign_floor_h100e": floor * p.c0,
            # horizon-anchored capacity: well defined for ALL g, unlike the floor
            "cap_60mo_pct": 100.0 * float(fr[60]) if len(fr) > 60 else float("nan"),
            "cap_120mo_pct": 100.0 * float(fr[120]) if len(fr) > 120 else float("nan"),
            "frontier_share_t0": p.c0 / p.frontier_scale}


# ═════════════════════════════════════════════════════════════════════════════
# 3 · MONTE CARLO
# ═════════════════════════════════════════════════════════════════════════════
def draw(base: Params, mode: str) -> Params:
    afr = RNG.uniform(AFR_GPU_DIE, AFR_ALL)
    kap = RNG.uniform(*KAPPA_COMPUTE)
    life = RNG.uniform(*USEFUL_LIFE)
    dbl = RNG.uniform(*FRONTIER_DOUBLING)
    fsc = np.exp(RNG.uniform(np.log(FRONTIER_SCALE[0]), np.log(FRONTIER_SCALE[1])))
    if mode == "CN":
        c0 = RNG.uniform(CH_SMUG_LO, CH_SMUG_HI) * 3.0
        dom = CN_DOMESTIC_PM * RNG.uniform(*CN_STOCKPILE_DEPENDENCE)
        leak = LEAK_PM * RNG.uniform(*LEAK_SUPPRESS)
    else:
        share = RNG.uniform(*(US_SHARE if mode == "US" else EU_SHARE))
        c0 = GLOBAL_H100E * share
        cov = RNG.uniform(*(US_COVERAGE_RANGE if mode == "US" else EU_COVERAGE_RANGE))
        lam = -np.log(1 - afr) / 12.0
        dom = c0 * (lam + 1.0 / (life * 12.0)) * cov
        leak = 0.0
    return Params(c0=c0, afr=afr, kappa=kap, useful_life_years=life,
                  frontier_doubling_months=dbl, domestic_per_month=dom,
                  leakage_per_month=leak, frontier_scale=fsc)


def monte_carlo(base: Params, mode: str, n_draws=10_000) -> pd.DataFrame:
    out = []
    for _ in range(n_draws):
        p = draw(base, mode)
        out.append(metrics(p) | asdict(p))
    return pd.DataFrame(out)


def qsum(s):
    """
    Quantiles under right-censoring, done correctly.

    An earlier version dropped censored (inf) draws and took percentiles of the
    remainder — which biases every quantile downward and, when censoring
    exceeds (1-q), reports a number for a quantile that is not identifiable at
    all. Censored draws are ordinally known (> horizon), so they are kept in
    the sort; any quantile falling in the censored mass returns CENSORED and is
    reported as ">120" rather than as a fabricated finite value.
    """
    s = pd.Series(s, dtype=float).dropna()
    if s.empty:
        return (np.nan, np.nan, np.nan, 0.0)
    cens = float(np.isinf(s).mean())
    # sentinel avoids inf-inf=nan in numpy's quantile interpolation; it is far
    # above any physical value (months <= 120, floors < 1e4 %), so a quantile
    # touching it is unambiguously in the censored mass
    SENT = 1e15
    a = s.replace(np.inf, SENT).to_numpy()
    out = []
    for q in (5, 50, 95):
        v = float(np.percentile(a, q))
        out.append(CENSORED if v > SENT / 100 else v)
    return (*out, cens)


# ═════════════════════════════════════════════════════════════════════════════
# 4 · AVIATION COMPARISON  —  parameter bounding, NOT calibration
# ═════════════════════════════════════════════════════════════════════════════
# The Russian civil fleet after February 2022 is the only observed severance of a
# complex, spare-parts-dependent capital fleet. We initially attempted to fit the
# model's hazard to the observed trajectory. THAT FIT FAILS, and it fails for a
# substantive reason worth reporting: the observed fleet decline is confounded by
# two mechanisms with NO compute analogue —
#   (i)  lessor repossession of foreign-owned airframes (a one-off stock shock,
#        not attrition), and
#   (ii) regulatory withdrawal of airworthiness certification.
# Attributing the whole decline to parts attrition would overstate the hazard by
# roughly an order of magnitude. We therefore use aviation ONLY to bound κ and to
# establish that cannibalisation is an observed, quantified mechanism — not as a
# quantitative calibration of the compute model. Reported for transparency.
AVIATION_OBS = [(0, 1.00, "Fleet at severance, Feb 2022"),
                (44, 0.67, "≥1/3 cannibalised, Oct 2025"),
                (47, 0.50, "≥50% reduction projected, 2026")]
AV_C0, AV_LIFE = 1650.0, 25.0


def aviation_comparison():
    """Best attainable single-parameter fit, reported WITH its failure."""
    obs = pd.DataFrame(AVIATION_OBS, columns=["month", "observed", "note"])
    best, best_sse = None, np.inf
    for lam_a in np.linspace(0.02, 4.0, 800):
        p = Params(c0=AV_C0, afr=1 - np.exp(-lam_a), kappa=KAPPA_AVIATION,
                   useful_life_years=AV_LIFE, frontier_doubling_months=1e9,
                   domestic_per_month=AV_C0 * 0.0015, leakage_per_month=AV_C0 * 0.0010)
        d = simulate(p, 60)
        pred = d.set_index("month")["frac_of_t0"].reindex(obs["month"]).to_numpy()
        sse = float(np.sum((pred - obs["observed"].to_numpy()) ** 2))
        if sse < best_sse:
            best_sse, best = sse, (lam_a, p, d, pred)
    lam_a, p, d, pred = best
    obs["model_attrition_only"] = pred
    obs["residual"] = obs["observed"] - obs["model_attrition_only"]
    # the residual is the share of decline NOT explained by parts attrition
    unexplained = float(-obs["residual"].iloc[-1])
    return lam_a, p, d, obs, best_sse, unexplained


# ═════════════════════════════════════════════════════════════════════════════
# 5 · RUN
# ═════════════════════════════════════════════════════════════════════════════
def fmt(v):
    return ">120" if (v == CENSORED or (isinstance(v, float) and np.isinf(v))) else f"{v:.0f}"


def main():
    R = {"derived": {"AFR_GPU_DIE": AFR_GPU_DIE, "AFR_HBM": AFR_HBM,
                     "AFR_PACKAGE": AFR_PACKAGE, "AFR_ALL": AFR_ALL,
                     "xcheck_gpu_hours_per_failure": XCHECK_GPUH,
                     "epoch_reported": EPOCH_GPUH, "C0_CHINA": C0_CHINA,
                     "C0_US": C0_US, "C0_EU": C0_EU,
                     "cn_domestic_pm": CN_DOMESTIC_PM, "leak_pm": LEAK_PM}}

    # 5.0 critical cannibalisation ratio κ*
    kstar_c = kappa_critical(AFR_PACKAGE, USEFUL_LIFE_C)
    kstar_grid = [{"afr": a, "useful_life_years": L, "kappa_star": kappa_critical(a, L)}
                  for a in (AFR_GPU_DIE, AFR_PACKAGE, AFR_ALL)
                  for L in (2.0, 4.0, 6.0)]
    pd.DataFrame(kstar_grid).to_csv(os.path.join(DATADIR, "table_kappa_star.csv"), index=False)
    R["kappa_star"] = {"central": kstar_c, "grid": kstar_grid,
                       "compute_range": list(KAPPA_COMPUTE)}

    # 5.1 aviation comparison (bounding, not calibration)
    lam_a, av_p, av_d, av_obs, sse, unexpl = aviation_comparison()
    av_obs.to_csv(os.path.join(DATADIR, "table_aviation_comparison.csv"), index=False)
    R["aviation"] = {"best_fit_lambda_annual": lam_a, "kappa": KAPPA_AVIATION,
                     "design_life_years": AV_LIFE, "sse": sse,
                     "rmse": float(np.sqrt(sse / len(av_obs))),
                     "unexplained_decline_share": unexpl,
                     "note": "fit fails; residual attributed to lessor repossession "
                             "and regulatory withdrawal, which have no compute analogue"}

    # 5.2 central cases
    CEN = {}
    china = Params(C0_CHINA, AFR_PACKAGE, np.mean(KAPPA_COMPUTE), USEFUL_LIFE_C,
                   FRONTIER_DOUBLING_C, CN_DOMESTIC_PM * CN_STOCKPILE_DEPENDENCE_C, LEAK_PM * 0.35)
    _lamc = -np.log(1 - AFR_PACKAGE) / 12 + 1 / (USEFUL_LIFE_C * 12)
    us = Params(C0_US, AFR_PACKAGE, np.mean(KAPPA_COMPUTE), USEFUL_LIFE_C,
                FRONTIER_DOUBLING_C, C0_US * _lamc * US_COVERAGE, 0.0)
    eu = Params(C0_EU, AFR_PACKAGE, np.mean(KAPPA_COMPUTE), USEFUL_LIFE_C,
                FRONTIER_DOUBLING_C, C0_EU * _lamc * EU_COVERAGE, 0.0)
    traj = {}
    for name, p in [("China", china), ("United States", us), ("European Union", eu)]:
        traj[name] = simulate(p, HORIZON)
        traj[name].to_csv(os.path.join(
            DATADIR, f"trajectory_{name.replace(' ','_').lower()}.csv"), index=False)
        CEN[name] = metrics(p) | {"c0": p.c0}
    R["central"] = CEN

    # 5.3 Monte Carlo
    mcs, rows = {}, []
    for name, base, mode in [("China", china, "CN"), ("United States", us, "US"),
                             ("European Union", eu, "EU")]:
        mc = monte_carlo(base, mode, 10_000); mcs[name] = mc
        th, tf, sf = qsum(mc["t_half_months"]), qsum(mc["t_frontier_months"]), qsum(mc["sovereign_floor_pct_of_c0"])
        rows.append({"jurisdiction": name, "C0_h100e": base.c0,
                     "t_half_p05": th[0], "t_half_med": th[1], "t_half_p95": th[2],
                     "t_half_censored_pct": 100 * th[3],
                     "t_frontier_p05": tf[0], "t_frontier_med": tf[1], "t_frontier_p95": tf[2],
                     "floor_p05": sf[0], "floor_med": sf[1], "floor_p95": sf[2],
                     "p_half_within_36m": 100 * (mc["t_half_months"] <= 36).mean()})
    mc_sum = pd.DataFrame(rows)
    mc_sum.to_csv(os.path.join(DATADIR, "table_results_montecarlo.csv"), index=False)
    mcs["China"].to_csv(os.path.join(DATADIR, "montecarlo_china.csv"), index=False)
    R["montecarlo"] = mc_sum.to_dict("records")

    # 5.4 sensitivity — one-at-a-time on China, T-frontier (uncensored metric)
    base_tf = metrics(china)["t_frontier_months"]
    sweeps = {"Failure rate (AFR)": ("afr", AFR_GPU_DIE, AFR_ALL),
              "Cannibalisation yield κ": ("kappa", *KAPPA_COMPUTE),
              "Useful life (yr)": ("useful_life_years", *USEFUL_LIFE),
              "Frontier doubling (mo)": ("frontier_doubling_months", *FRONTIER_DOUBLING),
              "Domestic output (×)": ("domestic_per_month", china.domestic_per_month * .5,
                                      china.domestic_per_month * 2),
              "Leakage (×)": ("leakage_per_month", china.leakage_per_month * .2,
                              china.leakage_per_month * 3)}
    sens = []
    for lab, (f, lo, hi) in sweeps.items():
        v = [metrics(replace(china, **{f: x}))["t_frontier_months"] for x in (lo, hi)]
        v = [HORIZON if np.isinf(x) else x for x in v]
        sens.append({"parameter": lab, "low": v[0], "high": v[1], "base": base_tf,
                     "span": abs(v[1] - v[0])})
    sens_df = pd.DataFrame(sens).sort_values("span", ascending=False)
    sens_df.to_csv(os.path.join(DATADIR, "table_sensitivity.csv"), index=False)
    R["sensitivity"] = sens_df.to_dict("records")

    # 5.5 κ regimes — the aviation/compute contrast
    kap_rows = []
    for kv, lab in [(KAPPA_AVIATION, "κ=10 · aviation (parts-rich)"),
                    (1.0, "κ=1 · hypothetical field-repairable"),
                    (0.50, "κ=0.5 · compute, upper bound"),
                    (0.05, "κ=0.05 · compute, lower bound")]:
        m = metrics(replace(china, kappa=kv))
        kap_rows.append({"kappa": kv, "regime": lab,
                         "t_half_months": m["t_half_months"],
                         "t_frontier_months": m["t_frontier_months"],
                         "floor_pct": m["sovereign_floor_pct_of_c0"]})
    kap_df = pd.DataFrame(kap_rows)
    kap_df.to_csv(os.path.join(DATADIR, "table_kappa_regimes.csv"), index=False)
    R["kappa_regimes"] = kap_rows

    with open(os.path.join(DATADIR, "results.json"), "w") as f:
        json.dump(R, f, indent=2, default=float)

    # ── FIGURES ──────────────────────────────────────────────────────────────
    pct = FuncFormatter(lambda y, _: f"{y*100:.0f}%")
    st = {"China": (ACCENT, "-"), "United States": (BLUE, "--"), "European Union": (GREEN, "-.")}

    f1, ax = plt.subplots(figsize=(5.5, 3.1))
    for n_, d in traj.items():
        c, ls = st[n_]; ax.plot(d.month, d.frac_of_t0, color=c, ls=ls, label=n_)
    ax.axhline(.5, color=GREY, lw=.7, ls=":")
    ax.text(HORIZON*.99, .52, "50%: compute half-life", ha="right", fontsize=7, color=GREY)
    ax.set(xlabel="Months after severance", ylabel="Effective compute, share of $C_0$",
           xlim=(0, HORIZON), ylim=(0, 1.06)); ax.yaxis.set_major_formatter(pct)
    ax.legend(frameon=False, loc="lower left")
    for e in ("pdf", "png"): f1.savefig(os.path.join(FIGDIR, f"fig1_decay_by_jurisdiction.{e}"))
    plt.close(f1)

    f2, ax = plt.subplots(figsize=(5.5, 3.1))
    A = np.vstack([simulate(draw(china, "CN"), HORIZON).frac_of_t0.to_numpy() for _ in range(800)])
    m = np.arange(A.shape[1])
    for lo, hi, a in [(5, 95, .16), (25, 75, .30)]:
        ax.fill_between(m, np.percentile(A, lo, 0), np.percentile(A, hi, 0), color=ACCENT, alpha=a, lw=0)
    ax.plot(m, np.percentile(A, 50, 0), color=ACCENT, lw=1.9)
    ax.axhline(.5, color=GREY, lw=.7, ls=":")
    ax.set(xlabel="Months after severance", ylabel="Effective compute, share of $C_0$",
           xlim=(0, HORIZON), ylim=(0, 1.06)); ax.yaxis.set_major_formatter(pct)
    ax.text(2, .05, "median · 50% and 90% intervals\n10,000-draw Monte Carlo",
            fontsize=7, color=GREY)
    for e in ("pdf", "png"): f2.savefig(os.path.join(FIGDIR, f"fig2_montecarlo_china.{e}"))
    plt.close(f2)

    f3, ax = plt.subplots(figsize=(5.5, 3.1))
    for n_, d in traj.items():
        c, ls = st[n_]
        ax.semilogy(d.month, np.maximum(d.frontier_relative, 1e-3), color=c, ls=ls, label=n_)
    ax.axhline(.10, color=GREY, lw=.7, ls=":")
    ax.text(71, .125, "10% of frontier scale", ha="right", va="bottom",
            fontsize=7, color=GREY)
    ax.set(xlabel="Months after severance", ylabel="Capability relative to moving frontier",
           xlim=(0, 72), ylim=(0.02, 120))
    ax.legend(frameon=False, loc="upper right")
    for e in ("pdf", "png"): f3.savefig(os.path.join(FIGDIR, f"fig3_frontier_relative.{e}"))
    plt.close(f3)

    f4, ax = plt.subplots(figsize=(5.5, 2.6))
    sd = sens_df.iloc[::-1]
    for i, (_, r) in enumerate(sd.iterrows()):
        lo, hi = sorted([r.low, r.high])
        ax.barh(i, max(hi-lo, .35), left=lo, height=.55, color=LGREY, edgecolor=INK, lw=.6)
        ax.plot([r.base], [i], marker="|", color=ACCENT, ms=13, mew=2.2)
    ax.set_yticks(range(len(sd))); ax.set_yticklabels(sd.parameter)
    ax.set_xlabel("Frontier exit time $T_f$ (months)")
    ax.text(.99, .04, "| central case", transform=ax.transAxes, ha="right", fontsize=7, color=ACCENT)
    for e in ("pdf", "png"): f4.savefig(os.path.join(FIGDIR, f"fig4_sensitivity_tornado.{e}"))
    plt.close(f4)

    f5, ax = plt.subplots(figsize=(5.5, 3.0))
    ax.plot(av_d.month, av_d.frac_of_t0, color=BLUE,
            label=f"Parts-attrition model only ($\\kappa$=10, best-fit $\\lambda$={lam_a:.2f}/yr)")
    ax.scatter(av_obs.month, av_obs.observed, color=ACCENT, zorder=5, s=36,
               label="Observed, Russian civil fleet")
    ax.fill_between(av_obs.month, av_obs.observed, av_obs.model_attrition_only,
                    color=ACCENT, alpha=.13, lw=0)
    ax.annotate("residual: repossession +\nregulatory withdrawal\n(no compute analogue)",
                xy=(46, .69), fontsize=6.6, color=ACCENT, ha="right")
    for _, r in av_obs.iterrows():
        ax.annotate(r.note, (r.month, r.observed), textcoords="offset points",
                    xytext=(-6, -13), fontsize=6.3, color=GREY, ha="right")
    ax.set(xlabel="Months after severance (Feb 2022 = 0)",
           ylabel="Operational fleet, share of $t_0$", xlim=(0, 60), ylim=(0, 1.06))
    ax.yaxis.set_major_formatter(pct); ax.legend(frameon=False, loc="lower left")
    for e in ("pdf", "png"): f5.savefig(os.path.join(FIGDIR, f"fig5_aviation_comparison.{e}"))
    plt.close(f5)

    # Fig 7 — the critical cannibalisation threshold κ*
    f7, ax = plt.subplots(figsize=(5.5, 3.0))
    lives = np.linspace(1.5, 6.5, 240)
    for a, lab, col in [(AFR_GPU_DIE, "GPU die only (6.1%/yr)", GREY),
                        (AFR_PACKAGE, "Package: die + HBM (9.1%/yr)", ACCENT),
                        (AFR_ALL, "All interruptions (17.3%/yr)", BLUE)]:
        ax.plot(lives, [kappa_critical(a, L) for L in lives], color=col, label=lab)
    ax.axhspan(KAPPA_COMPUTE[0], KAPPA_COMPUTE[1], color=GREEN, alpha=.13, lw=0)
    ax.text(6.4, np.mean(KAPPA_COMPUTE), "plausible $\\kappa$\nfor accelerators",
            fontsize=6.8, color=GREEN, ha="right", va="center")
    ax.set(xlabel="Useful life $L$ (years)",
           ylabel="Critical cannibalisation ratio $\\kappa^{*}=\\lambda L$",
           xlim=(1.5, 6.5), ylim=(0, 1.25))
    ax.legend(frameon=False, loc="upper left", title="Failure rate $\\lambda$")
    ax.get_legend().get_title().set_fontsize(7)
    for e in ("pdf", "png"): f7.savefig(os.path.join(FIGDIR, f"fig7_kappa_critical.{e}"))
    plt.close(f7)

    f6, ax = plt.subplots(figsize=(5.5, 3.0))
    for kv, lab, col, lw in [(KAPPA_AVIATION, "$\\kappa$ = 10 · aviation (parts-rich)", BLUE, 1.2),
                             (1.0, "$\\kappa$ = 1 · field-repairable", GREY, 1.2),
                             (0.50, "$\\kappa$ = 0.5 · compute, upper bound", "#d94801", 1.9),
                             (0.05, "$\\kappa$ = 0.05 · compute, lower bound", ACCENT, 1.9)]:
        d = simulate(replace(china, kappa=kv), HORIZON)
        ax.plot(d.month, d.frac_of_t0, color=col, lw=lw, ls="-" if kv <= .5 else "--", label=lab)
    ax.axhline(.5, color=GREY, lw=.7, ls=":")
    ax.set(xlabel="Months after severance", ylabel="Effective compute, share of $C_0$",
           xlim=(0, HORIZON), ylim=(0, 1.06)); ax.yaxis.set_major_formatter(pct)
    ax.legend(frameon=False, loc="lower left")
    for e in ("pdf", "png"): f6.savefig(os.path.join(FIGDIR, f"fig6_kappa_regimes.{e}"))
    plt.close(f6)

    # ── REPORT ───────────────────────────────────────────────────────────────
    L = "=" * 76
    print(f"\n{L}\nDERIVED FAILURE RATES  (Llama 3, arXiv:2407.21783)\n{L}")
    print(f"  GPU die .............. {AFR_GPU_DIE*100:6.2f} %/yr")
    print(f"  HBM3 ................. {AFR_HBM*100:6.2f} %/yr")
    print(f"  Package (die+HBM) .... {AFR_PACKAGE*100:6.2f} %/yr   ← headline")
    print(f"  All interrupts ....... {AFR_ALL*100:6.2f} %/yr")
    print(f"  Cross-check .......... {XCHECK_GPUH:,.0f} GPU-h/failure (Epoch ~{EPOCH_GPUH:,}) ✓")
    print(f"  C0 China (derived) ... {C0_CHINA:,.0f} H100e")

    print(f"\n{L}\nCRITICAL CANNIBALISATION RATIO  κ* = λ·L\n{L}")
    print(f"  κ* (central: AFR={AFR_PACKAGE*100:.2f}%/yr, L={USEFUL_LIFE_C}yr) = {kstar_c:.3f}")
    print(f"  assumed compute κ range .................. {KAPPA_COMPUTE}")
    print(f"  ⇒ the plausible κ range STRADDLES κ*: outcome is regime-dependent")
    print(pd.DataFrame(kstar_grid).to_string(index=False))

    print(f"\n{L}\nAVIATION COMPARISON  (bounding, NOT calibration — fit fails)\n{L}")
    print(f"  best-fit λ = {lam_a:.3f}/yr   RMSE = {R['aviation']['rmse']:.4f}")
    print(f"  decline unexplained by parts attrition at t=47mo: {unexpl*100:.1f} pp")
    print("  → attributed to lessor repossession + regulatory withdrawal (no compute analogue)")
    print(av_obs[["month", "observed", "model_attrition_only", "residual"]].to_string(index=False))

    print(f"\n{L}\nMONTE CARLO  (10,000 draws each)\n{L}")
    for r in rows:
        print(f"\n  {r['jurisdiction']}   C0 = {r['C0_h100e']:,.0f} H100e")
        print(f"    T½ (mo)         {fmt(r['t_half_med']):>6}   "
              f"[{fmt(r['t_half_p05'])} – {fmt(r['t_half_p95'])}]   "
              f"censored {r['t_half_censored_pct']:.0f}%")
        print(f"    T_f (mo)        {fmt(r['t_frontier_med']):>6}   "
              f"[{fmt(r['t_frontier_p05'])} – {fmt(r['t_frontier_p95'])}]")
        print(f"    Floor (% C0)    {r['floor_med']:6.1f}   [{r['floor_p05']:.1f} – {r['floor_p95']:.1f}]")
        print(f"    P(T½ ≤ 36 mo)   {r['p_half_within_36m']:.1f}%")

    print(f"\n{L}\nSENSITIVITY — China, T_f (months)\n{L}")
    print(sens_df.to_string(index=False))
    print(f"\n{L}\nCANNIBALISATION REGIMES\n{L}")
    print(kap_df.to_string(index=False))
    print(f"\n figures → {FIGDIR}\n data    → {DATADIR}\n")


if __name__ == "__main__":
    main()
