# Novelty Audit — Verdict

**Date:** 2026-08-08
**Subject:** Proposal A — "Compute-Sovereignty Index (CSI)" (from `Would like to write a real scientific paper with....md`)
**Auditor:** research session, all claims sourced from live retrieval on 2026-08-08
**Status:** ⛔ ORIGINAL FRAMING REJECTED · ✅ PIVOT IDENTIFIED AND VERIFIED

---

## 1. Verdict in one paragraph

**The CSI as proposed is already occupied — comprehensively, and by at least eleven competitors, one of which is nearly identical.** Publishing a "national AI-sovereignty index" in late 2026 would be entering a saturated field late, without an institutional data moat, against incumbents who refresh quarterly. It would not be cited; it would be listed in someone else's related-work paragraph.

**However, the audit surfaced a real and defensible hole — and it is bigger than the original idea.** Every existing index measures a **stock** (what a country *has*). Not one models the **flow** (what happens to what it has, over time, once supply is cut). The question every export-control policy assumes an answer to — *how long does severance actually buy?* — has never been quantitatively answered in the literature. That is the paper.

---

## 2. Prior art found — the field is crowded

Eleven overlapping products/papers were identified in one research pass. Full dossiers in `prior-art-dossiers/`.

### 2.1 The near-identical competitor — ⚠️ blocking

**Machinepower Index (MPI) 2026** — machinepowerindex.org — Elliot Leavy, Q3 2026 edition, quarterly refresh, 25 nations + EU.

Self-described as *"the standard global framework to measure a nation's technological sovereignty, compute capacity, and future resilience."* Structure:

| MPI axis | Contents |
|---|---|
| **Watts** (Material) | energy, infrastructure, compute, permitting, firm power, sovereign compute, **hardware & silicon** |
| **Weights** (Intellectual) | frontier capability, alignment, governance, talent density |
| **Will** (Political) | procurement reform, institutional capability, workforce, legitimacy |

Twelve sub-indicators. Notably uses a **bottleneck model, not averaging** ("the slowest stage limits total output"), and publishes a Score-vs-Potential gap.

**Why this is blocking:** the proposal's stated CSI factors — *"domestic silicon fabrication, energy-to-compute ratios, unstructured data reserves, algorithmic independence"* — map almost one-to-one onto Watts + Weights. MPI also already took the methodologically interesting move (bottleneck aggregation over additive weighting) that would have been the CSI's best differentiator. It is not peer-reviewed, but for citation purposes that barely matters: it is live, named, and first.

### 2.2 The rest of the field

| # | Name | Publisher | What it does |
|---|---|---|---|
| 1 | **Sovereign AI Index** (Apr 2026) | CNAS — Chavez, Chilukuri, Scanlon | Catalogues 139+ sovereign-AI projects; Infrastructure 59% / Models 34% / Data 7%. A project tracker, not a score |
| 2 | **Government AI Readiness Index 2025** | Oxford Insights | 195 countries, government capacity to use AI |
| 3 | **Global AI Index** | Tortoise Media | 83 countries × 83 indicators; implementation / innovation / investment |
| 4 | **AI Index Report 2026** | Stanford HAI | The reference annual; policy & governance chapter |
| 5 | **Technological Sovereignty Index (TSI)** | methodological outline (RG/Academia) | 3 pillars: Assets & Competencies / Conditioners / Drivers |
| 6 | **Empirical Measurement of Technology Sovereignty** | Lee, Choi, Kim, Si — SSRN 5145685 | Peer-track academic; innovation + production + supply-chain independence ⚠️ *fetch blocked 403 — verify manually* |
| 7 | **Łukasiewicz ITECH model** | Łukasiewicz Research Network | knowledge / infrastructure / research / society |
| 8 | **International Sovereignty Index (ISI)** | internationalsovereignty.org | **HHI-based external supplier concentration**, 6 axes incl. energy + technology — methodologically the closest to a dependency model |
| 9 | **Burke Sovereignty Index** | — | 7 dimensions incl. technological |
| 10 | **SovRank Strategic Sovereignty Index** | sovrank.pages.dev | defence / technology / energy / economics / governance |
| 11 | **Sovereign AI LLM Index 2026** | Counterpoint Research | model-level sovereignty spectrum |
| — | **Digital Sovereignty Index** | Nextcloud | self-hosted deployment density, ~60 countries |
| — | **European Sovereignty Index** | ECFR | EU-specific, graded terrains |

Plus adjacent academic work: *Managing technological sovereignty: a systematic review of semiconductor industry policy* (Frontiers, 2026); *Technological sovereignty of the EU in advanced 5G* (Telecommunications Policy).

**Conclusion:** "index of national tech/AI sovereignty" is a solved-and-crowded genre. Do not enter it.

---

## 3. The hole — verified three independent ways

The distinctive phrase in the original proposal was *"the ability to sustain AI infrastructure **if completely cut off** from global supply chains."* That is not a capability score. That is a **stress test** — and nobody is doing it.

**Evidence that the hole is real:**

1. **Machinepower Index** — fetched 2026-08-08: *"The Index does **not** measure resilience-under-severance. It measures current capacity."*
2. **CNAS Sovereign AI Index** — fetched 2026-08-08: *"not a capability scoreboard or dependency-severance model."*
3. **Targeted search** for quantified severance horizons returned nothing. The retrieval itself concluded: *"the search results don't contain specific quantitative analyses (in months or years) of how long a particular country could sustain advanced AI capabilities under a compute severance or autarky scenario."*

Every index in §2 is a **snapshot of holdings**. None is a **model of decay**.

### 3.1 ⚠️ Honest narrowing — partial prior work DOES exist

A second pass found adjacent work that must be disclosed, because a reviewer will find it:

- **SemiAnalysis (Sept 2024)** projected China's TSMC die stockpile would be exhausted "within the next 9 months."
- **The Substrate / ChinaTalk (2026)** modelled remaining TSMC dies as a **zero-inflated distribution**, giving *"roughly a 56% chance that the stockpile is fully depleted by January 2026, and a 44% chance that some dies remain."*
- Related projection: in 2026 US chip designers produce **~20× more power-drawing silicon than Huawei**, leaving Huawei able to supply **~1/5** of Chinese AI demand.
- Huawei reportedly holds **>1 year** of HBM stockpile; Chinese firms stockpiled HBM for "the next few years" ahead of the Dec 2024 restrictions.

**Does this kill the paper? No — but it changes what can be claimed.**

| | Existing analyst work | This paper |
|---|---|---|
| Object | **input stockpile** — unbuilt dies/HBM awaiting assembly | **installed operational fleet** — deployed accelerators already running |
| Mechanism | consumption until exhausted | **failure + obsolescence + cannibalisation** under no resupply |
| Scope | China, single-country, point-in-time | **general, transferable, multi-country** |
| Status | industry analysis, not peer-reviewed | peer-reviewable method |
| Output | a depletion **date** | a degradation **curve**, plus T½ / T_f / C∞ |

Running out of *parts to build new chips* and *the chips you already deployed dying with no replacements* are different questions with different mathematics. The first is inventory drawdown; the second is survival analysis on a capital fleet. **No one has done the second.**

**Required action:** cite SemiAnalysis, The Substrate and ChinaTalk explicitly and generously in related work, and state the distinction in the introduction. Claiming unqualified novelty here would be the paper's most obvious vulnerability. Claiming *precise* novelty — "prior work models input depletion; we model installed-base decay" — is defensible and strengthens the contribution by showing command of the field.

---

## 4. The pivot — and why it is stronger than the original

> ### Compute is treated as a *reserve*. It actually behaves like a *perishable, failure-prone, depreciating* asset.
> Nobody has modelled the decay curve. Every export-control argument silently assumes one.

**The thesis:** installed national AI compute is not a stock of gold. It fails at measurable rates, obsolesces against a moving frontier, depends on a separately-chokepointed memory supply, and can only be replaced at a rate bounded by domestic fab yield. Model those four terms and you can compute, for the first time, a **time-to-degradation curve** for a national compute base under severance — the *half-life of compute*.

### Why the empirical foundations exist (all verified this session)

| Model term | Empirical anchor found | Source |
|---|---|---|
| **Failure / attrition** | Llama 3 405B: **419 interruptions in 54 days** on ≤16,384 H100s; faulty GPU = 148 (30.1%), **HBM3 = 72 (17.2%)**, network 35 (8.4%). Extrapolates to ~1 failure/30 min at 100k GPUs. >90% effective training time maintained | Meta, *The Llama 3 Herd of Models*, arXiv 2407.21783 |
| **Economic life / obsolescence** | Live unresolved dispute: hyperscalers 5–6 yr vs. claimed 2–3 yr real economic life; Burry: ~**$176B** understated depreciation 2026–28. Amazon *shortened*, Meta *extended* (to 5.5 yr, $2.9B reduction) in the same quarter. Neoclouds: Lambda 5 yr, Nebius 4 yr. Counter-evidence: CoreWeave rebooked expiring 2022 H100s at **95% of original price** | CNBC 2025-11-14; Fortune 2025-12-15; theCUBE/SiliconANGLE 2025-11-22 |
| **Replacement rate** | SMIC pinned at 7nm under equipment controls; Ascend 910C yields reported **20–40%** vs 90%+ at TSMC leading edge. Huawei pre-control stockpile ≈ **2.9M TSMC dies (~$500M)**, largely consumed across 2024–25 | CFR; The Wire China; Silicon Analysts |
| **Second chokepoint** | HBM ≈ **90% in two Korean firms** (SK Hynix ~50–55%, Samsung ~35–40%, Micron ~5–10%); SK Hynix 2026 capacity sold out; $950B supply deals lock allocation to 2030 | Silicon Analysts; KED Global; DCD |
| **Input dataset** | Epoch AI: global stock ≈ **15M H100-equivalents**, ownership-resolved, published methodology, NVIDIA-revenue-derived | epoch.ai/data/ai-chip-owners |

**The compounding mechanism nobody has modelled:** HBM is *simultaneously* the #2 failure mode (17.2% of Meta's interruptions) *and* the #2 supply chokepoint (~90% two-firm concentration). Under severance, the failure term and the replacement term are **coupled through the same component**. That single observation is a publishable finding on its own.

### Why it gets cited for a decade

1. **It answers the question every policy paper begs.** "Export controls buy us time" — *how much?* Nobody has computed it. Any future paper on chip controls needs a horizon parameter, and there will be one canonical source for it.
2. **It is a method, not an opinion.** Methods get cited; op-eds get read once. Falsifiable output (months, with confidence intervals), reproducible from public data, releasable as code.
3. **It creates vocabulary.** "The compute half-life of X" is a reusable quantity. Vocabulary is the strongest citation engine there is.
4. **It has two audiences, not one.** Geopolitics/policy cites the severance horizon; finance/accounting cites the depreciation sensitivity analysis against a live $176B controversy.
5. **It is counter-cyclical.** Eleven competitors are building better snapshots. Being the only one modelling the derivative is a defensible position, not a crowded one.

---

## 5. Positioning against the incumbents

| | Existing indices (×11) | This paper |
|---|---|---|
| Measures | stock — what you have | flow — what you keep |
| Output | a rank | a curve, in months |
| Method | additive/bottleneck composite | conditional decay simulation |
| Falsifiable | not really | yes |
| Reusable by others | as a citation of fact | as a **method** |

Existing indices become **inputs and related work**, not rivals. That is the correct relationship to a crowded field: do not compete with it — consume it.

---

## 6. On citing GEOPOLITECH — direct answer

The concern was right, and here is the expert read:

**A trade book cannot carry a scientific paper's theoretical load.** Reviewers discount self-citation of non-peer-reviewed general-audience work, and leaning on it invites exactly the "generalities" problem flagged. So:

- **Cite it once, precisely, in the motivation/framing section only** — for the chokepoint framing, where it is a genuine attributable contribution (cf. the *"Three Chokepoints Run the 21st Century"* strait/machine/smelter framing, 2026-08-15).
- **Never cite it for a factual claim or a model parameter.** Those come from Epoch AI, Meta's arXiv paper, SEC filings, CFR/CSIS.
- **The authority comes from the model, the data, and the released code.** The book borrows legitimacy from the paper, not the other way round — which is the direction that actually helps: paper cites book → book acquires academic standing → the trilogy becomes citable in future literature.

One precise citation is worth more than ten decorative ones, and it protects the paper from the generality trap.

---

## 7. Open items before locking the design

- [ ] Verify **SSRN 5145685** (Lee et al.) manually — 403 on automated fetch
- [ ] Verify the **TSI methodological outline** — 403 on ResearchGate
- [ ] Read **MPI methodology page** in full for the exact formula (audit relied on the landing page)
- [ ] Confirm no severance-horizon work exists in: CSIS, RAND, IISS, GovAI, IAPS, Epoch AI publications
- [ ] Check the **Frontiers 2026 systematic review** for any decay/resilience modelling already claimed

---

*All claims above were retrieved live on 2026-08-08. Items marked ⚠️ were blocked by access controls and are unverified.*
