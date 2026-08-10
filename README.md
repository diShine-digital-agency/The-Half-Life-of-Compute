# The Half-Life of Compute

**Modelling National AI Capacity Decay Under Supply Severance**

Kevin Escoda · diShine, Milan · August 2026
Paper DOI: `10.5281/zenodo.21866487` (Zenodo) · [Versione italiana](README.it.md) · [Version francaise](README.fr.md)

Export controls on AI chips are justified by a claim about time: they are said to buy it. This repository contains the model, data, verification suite and full manuscripts of the first quantitative estimate of how much, treating a national fleet of AI accelerators as perishable capital that fails, ages against a moving frontier, and can only partially be repaired by cannibalisation.

## Key results

| Quantity | Definition | Result (median, 10,000-draw Monte Carlo) |
|---|---|---|
| Frontier exit, T_f | months until capacity falls under 10% of the frontier training scale | EU 25 · China 41 · US 49 |
| Analytic law | T_f follows T_dbl x log2(C0 / (theta x F0)) | 10x the stock buys about 17 months |
| Compute half-life, T1/2 | months until 50% of severance-day capacity | US 51, EU 28; China censored (">120" in 58% of draws) |
| Sovereign floor, C_inf | capacity sustainable from non-severed inflow | US 31% (scenario), EU 3% (scenario), China 53% with an interval of 22-156%: Chinese self-sufficiency is genuinely undetermined |
| Saturation threshold | kappa* = lambda x L = 0.38 | above it, extra salvage effort buys nothing |

Hardware decay explains only 13-14% of the frontier-exit interval. The frontier clock explains the rest: severance does not need to destroy an adversary's compute, freezing it suffices while the frontier moves.

## Repository map

```
01-SUBMISSION/      final PDFs: paper and executive summary in EN, IT, FR
02-DRAFT/model/     the model (~200 lines of NumPy), verification suite, figure generators
02-DRAFT/figures*/  all figures, per language (papers and executive summaries)
03-DATA/processed/  results.json, results_extended.json, all CSV tables
04-AUDIT/           the full correction history, including withdrawn claims
```

## Reproduce everything

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r 05-DRAFT/model/requirements.txt
cd 05-DRAFT/model
python3 compute_decay_model.py     # model, Monte Carlo, figures, tables
python3 verify_and_extend.py       # independent re-derivation; must print ALL CHECKS PASSED
```

Fixed seed 20260808. Every number in every manuscript, including the abstracts, is read from `results.json` at build time; nothing is typed twice.

## A note on honesty

This paper was adversarially reviewed before release, and the record is public in `01-AUDIT/`. One headline claim of an earlier draft (stock-invariance of frontier exit) was found to be a normalisation artefact and withdrawn; the frontier doubling time was re-sourced; a calibration attempt against Russian civil aviation failed and is reported as a failure; a tempting hypothesis about long-lived fleets was tested, rejected, and documented. The two most consequential unmeasured parameters, the cannibalisation yield kappa and China's stockpile-dependence share, are named in the paper as the field's highest-value empirical targets.

## Citation

```bibtex
@misc{escoda2026halflife,
  author    = {Escoda, Kevin},
  title     = {The Half-Life of Compute: Modelling National AI Capacity
               Decay Under Supply Severance},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.21866487},
  url       = {https://github.com/diShine-digital-agency/The-Half-Life-of-Compute}
}
```

## Licence

Code: MIT. Manuscripts and figures: CC BY 4.0. Underlying third-party data (Epoch AI, published telemetry) remain under their original terms and are cited in the paper.
