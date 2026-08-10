# Adversarial Review — findings and revision record

**Date:** 2026-08-08
**Method:** 8 hostile referees across distinct attack surfaces; every critique independently
re-checked by a separate agent instructed to *refute* it; 4 live evidence sweeps run in parallel.
The run hit an account usage limit after 15 of 55 agents; **7 confirmed defects** were returned
before it stopped, and all 7 are addressed below. The unfinished surfaces are listed in §5.

> Two referees working from different assignments (`parameters-data`, `geopolitics`) independently
> converged on the same defect in the paper's headline finding. That convergence is why it was
> acted on rather than argued with.

---

## 1 · The headline finding was an artefact. It has been withdrawn.

**The claim:** frontier exit occurs at 23–25 months and is *"nearly invariant to the size of the
installed base"* — reported in the abstract, §5.2, §5.3, the Figure 3 caption, a falsifiable
prediction and the conclusion.

**The defect.** The code computed `frontier_relative = (eff / c0) / 2^(t/T_dbl)`. The denominator
was **each jurisdiction's own severance-day stock**, so every jurisdiction began at exactly 1.0 by
construction and `C₀` cancelled identically. §3.3 meanwhile described an *absolute*,
jurisdiction-common frontier scale. **Code and text described different objects.**

Verification (independent, both referees): under the US functional form, T_f = 28 months and the
floor = 31.875% at C₀ = 10³, 10⁶, 10⁹ and 10¹⁰ — identical to eight significant figures. Monte
Carlo corr(C₀, T_f) = 0.015. For China, where inflows are absolute rather than proportional, stock
*did* enter — with the **opposite sign** to the paper's story (larger stock → earlier exit).

**Worst consequence:** §7.3 offered as a *falsifiable prediction* that "frontier position decouples
from stock… refuted by a strong stock correlation." Under the implemented metric that correlation
was zero **by algebra**. The paper advertised an identity as a testable prediction.

**Fix.** `frontier_relative = eff / (F₀·2^(t/T_dbl))` with F₀ an absolute anchor, swept
log-uniformly over 5×10⁴–5×10⁵ H100e with its derivation shown in §3.3 and Table 1.

---

## 2 · The frontier growth rate was the wrong Epoch AI series

The model used **10 months**, sourced to Epoch's *NVIDIA installed-stock* doubling time. §3.3 used
the same number as the growth rate of the *frontier training scale*. Those are different series.

Verified live this session: frontier training compute grows **4–5× per year, doubling every ~5.2
months since 2020**; notable models ~6 months. The paper's stated 6–12 month band did not even
bracket the correct quantity — its lower endpoint was roughly the correct central value, biasing
every reported horizon long.

**Fix.** `FRONTIER_DOUBLING_C = 5.2`, band 4.8–7.0, Table 1 source cell now names the specific
series rather than "Epoch AI" undifferentiated.

---

## 3 · What replaced the withdrawn claim is stronger

Re-running under the corrected metric produced an **emergent analytic relation** that the broken
metric had concealed:

```
T_f  ≈  T_dbl · log₂( C₀ / (θ·F₀) )
```

Analytic vs simulated central cases: **36.6/36 (China), 49.1/45 (US), 27.7/24 (EU)** — agreement
within four months, the residual being exactly the decay the formula omits.

| New finding | Value |
|---|---|
| Frontier exit, MC medians | **EU 25 · China 41 · US 49 months** (was a false 23–25 band) |
| Stock buys time **logarithmically** | 10× the compute buys **+17 months**; 100× buys +35 |
| Hardware decay's share of the interval | **13–14%**, consistently across all three jurisdictions |
| Frontier clock vs hardware attrition | **7×** (was 5× under the mis-sourced doubling time) |

"Stockpiling is subject to sharply diminishing returns against a moving frontier" is a sharper,
more useful and more defensible statement than the invariance claim it replaces — and unlike that
claim it is not an artefact of normalisation. The ordering now also runs the intuitive way: the
largest holder survives longest.

---

## 4 · Other confirmed defects, and what was done

### 4.1 The US and EU sovereign floors are an assumption rescaled — **major**
A closed form exists (the paper had claimed none did):

```
C∞/C₀ = (R_dom + R_leak)(1 + min(κ, κ*)) / (C₀(λ + δ))
```

Where R_dom is parameterised as `cov·C₀(λ+δ)` — the US and EU cases — this collapses to
**`cov·(1 + min(κ, λL))`**, independent of C₀, λ and L, with the bracket bounded in [1.0, 1.5].
Verified numerically at 1.275000 to six decimals across C₀ spanning 0.6M–10.5M H100e.

So "US 31.5%" was the assumed 0.25 coverage × 1.275. The coverage parameter appeared **only in a
code comment** and was absent from Table 1 entirely.

**Fix.** Closed form now stated as Eq. A.2/A.3 in Appendix A; `cov` added to Table 1 with its
source cell reading *"Assumption — no observational basis"*; §7.2 reports the US/EU floors as an
explicit **scenario mapping** (cov 0.15/0.25/0.35 → 19/32/45%) rather than as a finding; the
US-vs-China proximity argument is withdrawn, since it compared an assumption to a computed value.

### 4.2 The Huawei figure was double-discounted — **major**
Epoch AI's 530k H100e for Huawei in 2025 is **realised chip output** — the source states *"Our data
tracks chip sales, not deployments"* — so it already embodies achieved yield. The model then
multiplied by (0.30/0.90), applying yield a second time.

**Fix.** Haircut removed. A downward adjustment is still applied but on a *separately argued*
ground — dependence on the ~2.9M pre-control TSMC die stockpile — and is now labelled
`CN_STOCKPILE_DEPENDENCE` (0.30–1.00) rather than mislabelled as yield. China's floor rises
accordingly and is reported as found.

### 4.3 C∞ was mislabelled — **moderate**
Defined as *"sustainable from domestic production alone"*, but China's central case carries ~40% of
its inflow as leakage. **Fix:** relabelled "sustainable from all non-severed inflow — domestic
production *and* residual leakage".

### 4.4 Remote access is outside the model — **major**
`N(t)` counts physically installed accelerators. Leased offshore capacity is **not** covered by the
leakage term: leaked units enter the fleet and thereafter decay at λ and δ, whereas leased capacity
is replenished by the lessor and does not decay at all.

**Fix.** New limitation in §7.4 stating the scope explicitly, the abstract's closing sentence now
carries the condition ("where remote access is also interdicted"), and — converting the objection
into a result — the analytic consolation is reported: a fixed lease of any size shifts T_f by only
`T_dbl·log₂(1 + A/C₀)`; leased capacity defeats the mechanism only if it compounds at
**g\* = ln2/T_dbl ≈ 13% per month**.

### 4.5 Domestic output was frozen with no disclosure — **major**
`R_dom` is held at its severance-date level for the whole 900-month integration, so C∞ exists
**only** at zero indigenisation growth; for any g > 0 there is no asymptote (verified: g = +5%/yr
sends the 900-month value to 1,105% of C₀). The assumption is contradicted by the most recent trend
in the very series the parameter is calibrated from.

**Fix.** A `dom_growth_yr` parameter added; the assumption is now stated in §3.3 and §7.4; T_f is
shown to be robust to it (a few months across −30% to +60%/yr, because no plausible indigenisation
rate competes with a frontier doubling every 5.2 months) — which converts the objection into a
robustness result.

---

## 5 · Not completed — outstanding at the usage limit

These referee surfaces reported critiques but their verification agents did not run. **Nothing from
them has been acted on**, because acting on an unverified critique is exactly the error the
verification stage exists to prevent.

| Surface | Status |
|---|---|
| `model-internals` (6 critiques) | raised, **unverified** |
| `statistics` (6) | raised, **unverified** |
| `presentation` (6) | raised, **unverified** |
| `novelty-priorart` (6) | raised, **unverified** — the military sustainment / METRIC spares-optimisation literature sweep did not run, and remains the most likely source of a novelty challenge |
| `reproducibility` | referee itself did not run |
| All 4 evidence sweeps | did not run |

**Highest-value next step:** the prior-art sweep. Multi-echelon inventory and readiness modelling
(Sherbrooke's METRIC and successors) formalises cannibalisation and availability under spares
constraint, and if it already contains a threshold equivalent to κ\*, the paper must cite and
position against it rather than be found out.

---

## 6 · What was *not* changed, and why

Over-correction is its own failure mode. These survived scrutiny and were deliberately left alone:

- **κ\* = λL and the saturation result.** Untouched by every confirmed defect. Independently
  re-derived and numerically re-verified.
- **The failure rate λ = 9.08%/yr** and its 1.35% cross-check against Epoch.
- **The failed aviation calibration (§6).** Reported as a failure; the referees did not dispute it.
- **The "5×" → "7×" frontier dominance ratio.** One referee argued monthly quantisation opened this
  to a 4–8× band; re-integration at 0.05-month resolution gave 5.29 against the published 5.33 —
  **the critique was refuted and the claim was not weakened on its account.** It changed only
  because the doubling time was re-sourced.
- **The rejected useful-life hypothesis** from the earlier audit stays rejected.

---

## 7 · Net effect

One headline finding was withdrawn and replaced by a stronger one. Two parameters were re-sourced.
One double-count was removed. Two undisclosed assumptions are now disclosed and swept. One
unfalsifiable prediction was replaced by a falsifiable one.

The paper is shorter on claims and longer on caveats than it was this morning, and it is
considerably harder to attack.
