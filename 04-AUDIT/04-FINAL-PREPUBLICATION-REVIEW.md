# Final Pre-Publication Review (Fable pass)

**Date:** 2026-08-09 · **Scope:** everything outstanding from the adversarial review, executed
solo and incrementally after the multi-agent run hit the usage limit. All twelve deliverables
rebuilt and re-verified.

---

## 1 · Statistics defect found and fixed (the unverified referee was right)

The statistics referee's censoring critique, never verified in the workflow run, was checked
directly and **confirmed**:

- **China's T½ was reported as a median of 50 months while 57.7% of draws were censored** at the
  120-month horizon. With more than half the mass censored, the median is not identifiable — the
  old `qsum` silently dropped censored draws and took percentiles of the remainder, biasing every
  quantile downward and fabricating a number for an unidentifiable one.
- **Fix:** censored draws are retained ordinally (sentinel far above any physical value, so a
  quantile touching it is unambiguous); any quantile in the censored mass reports as **">120"**.
  China now reads T½ = [29, >120, >120]. The Table 2 note explains the treatment in all three
  languages. `verify_and_extend.py`: ALL CHECKS PASSED after the change.

## 2 · The abstract contradicted Table 2 — fixed

China's floor interval is [22.1, 53.4, **155.7**]% — the upper bound crosses parity. The abstract's
"sovereign floors lie far below self-sufficiency everywhere" was contradicted by the paper's own
table. Rewritten in all three languages: medians reported as medians, and China's interval stated
with the honest conclusion — **whether China could sustain its fleet domestically is, on current
public data, genuinely undetermined**. §5.2, §7.2, the conclusion and the executive summaries now
carry the same statement; the brief's second finding was retitled accordingly, and its bar chart's
axis was extended so China's parity-crossing whisker is visible rather than clipped.

## 3 · Prior art closed (the sweep that never ran)

Verified live: **Sherbrooke (1968), METRIC, *Operations Research* 16(1), 122-141,
doi:10.1287/opre.16.1.122** (originally RAND RM-5078) — the founding model of the military
sustainment tradition, whose modern extensions model cannibalisation explicitly. Added to §2.2 in
all three languages with honest positioning: κ\* is the severance-regime limit of that tradition,
not a claim to have discovered cannibalisation. Citation added to all three reference lists.

## 4 · Back-propagation debt cleared (IT/FR)

The adversarial-round corrections had reached English only in five places. Italian and French now
carry: the corrected Table 1 (frontier-training doubling 5.2 months; F₀; θ; the coverage row marked
"Assumption — no observational basis"; the relabelled China inflow), the §7.2 scenario-mapping
rewrite, the two new §7.4 limitations (remote access with the g\* ≈ 13%/month result; frozen
domestic output), Appendix A.2/A.3 closed forms, and the restructured §5.5 with the degenerate
table row removed.

## 5 · Independence disclosure added

Table 1 note, all three languages: parameters are sampled independently, and independence is itself
an assumption — plausible correlations are not modelled. The MC figure caption no longer claims
stock uncertainty doesn't matter (for China it does, since inflows are absolute).

## 6 · Typography: dashes eliminated

Per author instruction, all em-dashes and en-dashes were removed from every deliverable:
~330 em-dashes and ~100 en-dashes across four content modules, three figure scripts and three
builders. High-visibility instances converted to colons/semicolons/middots by hand; the remainder
to commas; numeric ranges to plain hyphens (25-49, 122-141). Figure labels, running heads, bullet
glyphs and META fields included. **Automated scan: 0 em-dashes, 0 en-dashes across all six PDFs and
six DOCX.**

## 7 · Rendering bug caught by visual inspection

The corrected abstract formula rendered as garbled text ("T_dbllog_2(C_/theta F_0)") because the
inline-math converter lacked `\simeq`, `\theta`, `\log`, `\ln`, `\min`, `\cdot`. Extended at
renderer level; all three languages healed in one fix. Verified by re-extraction:
"Tf ≈ T_dbl log2(C0/θ F0)".

## 8 · Final state

| Check | Result |
|---|---|
| Numerical verification (`verify_and_extend.py`) | ALL CHECKS PASSED |
| Withdrawn-claim scan (6 PDFs) | clean |
| Dash scan (6 PDFs + 6 DOCX) | 0 em, 0 en |
| Punctuation-artifact scan | clean |
| Sherbrooke / censoring / China-interval strings present | yes, all languages |
| Page counts | EN 16 · IT 17 · FR 18 · briefs 4 each |

## 9 · Still open (stated, not hidden)

- Referee surfaces `model-internals` and `presentation` raised critiques that were never
  independently verified; nothing from them was acted on. A future pass could verify them.
- κ and the stockpile-dependence share remain the two unmeasured parameters the paper itself
  identifies as the highest-value empirical targets.
- The four placeholders (DOI, arXiv ID, ORCID, repository URL) remain to be filled at submission.
