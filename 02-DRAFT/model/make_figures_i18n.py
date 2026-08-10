#!/usr/bin/env python3
"""
Regenerate all seven figures with localised labels.

    FIG_LANG=it python3 make_figures_i18n.py   → ../figures_it/
    FIG_LANG=fr python3 make_figures_i18n.py   → ../figures_fr/

Reuses the model in compute_decay_model.py; re-runs only the light simulations
(the 10,000-draw Monte Carlo tables are unchanged and read from results.json).
"""
import os, json
from dataclasses import replace

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

import compute_decay_model as M

LANG = os.environ.get("FIG_LANG", "it").lower()
FIGDIR = os.path.normpath(os.path.join(M.HERE, "..", f"figures_{LANG}"))
os.makedirs(FIGDIR, exist_ok=True)

INK, ACCENT, BLUE, GREY, LGREY, GREEN = (M.INK, M.ACCENT, M.BLUE,
                                         M.GREY, M.LGREY, M.GREEN)
pct = FuncFormatter(lambda y, _: f"{y*100:.0f}%")
HORIZON = M.HORIZON

LABELS = {
 "it": dict(
   xlab="Mesi dalla recisione", ylab="Calcolo effettivo, quota di $C_0$",
   names=["Cina", "Stati Uniti", "Unione Europea"],
   half="50%: emivita del calcolo",
   mc="mediana · intervalli al 50% e 90%\nMonte Carlo, 10.000 estrazioni",
   fr_y="Capacità relativa alla frontiera mobile",
   fr_t="10% della scala di frontiera",
   tor_x="Tempo di uscita dalla frontiera $T_f$ (mesi)",
   central="| caso centrale",
   par={"Frontier doubling (mo)": "Raddoppio frontiera (mesi)",
        "Useful life (yr)": "Vita utile (anni)",
        "Leakage (×)": "Dispersione (×)",
        "Domestic output (×)": "Produzione interna (×)",
        "Failure rate (AFR)": "Tasso di guasto (AFR)",
        "Cannibalisation yield κ": "Resa di cannibalizzazione κ"},
   av_model="Solo attrito ricambi ($\\kappa$=10, $\\lambda$={lam:.2f}/anno)",
   av_obs="Osservato, flotta civile russa",
   av_res="residuo: sequestro dei lessor +\nritiro dell'idoneità al volo\n"
          "(nessun analogo nel calcolo)",
   av_notes={0: "Flotta alla recisione, feb. 2022",
             44: "≥1/3 cannibalizzata, ott. 2025",
             47: "≥50% di riduzione prevista, 2026"},
   av_x="Mesi dalla recisione (feb. 2022 = 0)",
   av_y="Flotta operativa, quota di $t_0$",
   kap=["$\\kappa$ = 10 · aviazione (ricca di ricambi)",
        "$\\kappa$ = 1 · riparabile sul campo",
        "$\\kappa$ = 0,5 · calcolo, limite superiore",
        "$\\kappa$ = 0,05 · calcolo, limite inferiore"],
   afr=["solo die GPU (6,1%/anno)", "package: die + HBM (9,1%/anno)",
        "tutte le interruzioni (17,3%/anno)"],
   ks_x="Vita utile $L$ (anni)",
   ks_y="Resa critica di cannibalizzazione $\\kappa^{*}=\\lambda L$",
   ks_band="$\\kappa$ plausibile\nper acceleratori",
   ks_leg="Tasso di guasto $\\lambda$",
   files=["fig1_decadimento_giurisdizioni", "fig2_montecarlo_cina",
          "fig3_relativo_frontiera", "fig4_tornado_sensibilita",
          "fig5_confronto_aviazione", "fig6_regimi_kappa", "fig7_kappa_critica"]),

 "fr": dict(
   xlab="Mois après la rupture", ylab="Calcul effectif, part de $C_0$",
   names=["Chine", "États-Unis", "Union européenne"],
   half="50%: demi-vie du calcul",
   mc="médiane · intervalles à 50% et 90%\nMonte-Carlo, 10 000 tirages",
   fr_y="Capacité relative à la frontière mobile",
   fr_t="10% de l'échelle de frontière",
   tor_x="Temps de sortie de la frontière $T_f$ (mois)",
   central="| cas central",
   par={"Frontier doubling (mo)": "Doublement frontière (mois)",
        "Useful life (yr)": "Durée de vie utile (ans)",
        "Leakage (×)": "Fuite (×)",
        "Domestic output (×)": "Production domestique (×)",
        "Failure rate (AFR)": "Taux de panne (AFR)",
        "Cannibalisation yield κ": "Rendement de cannibalisation κ"},
   av_model="Attrition de pièces seule ($\\kappa$=10, $\\lambda$={lam:.2f}/an)",
   av_obs="Observé, flotte civile russe",
   av_res="résidu : saisie par les loueurs +\nretrait de navigabilité\n"
          "(sans équivalent en calcul)",
   av_notes={0: "Flotte à la rupture, fév. 2022",
             44: "≥1/3 cannibalisée, oct. 2025",
             47: "≥50% de réduction projetée, 2026"},
   av_x="Mois après la rupture (fév. 2022 = 0)",
   av_y="Flotte opérationnelle, part de $t_0$",
   kap=["$\\kappa$ = 10 · aviation (riche en pièces)",
        "$\\kappa$ = 1 · réparable sur site",
        "$\\kappa$ = 0,5 · calcul, borne supérieure",
        "$\\kappa$ = 0,05 · calcul, borne inférieure"],
   afr=["die GPU seul (6,1%/an)", "package : die + HBM (9,1%/an)",
        "toutes interruptions (17,3%/an)"],
   ks_x="Durée de vie utile $L$ (ans)",
   ks_y="Rendement critique de cannibalisation $\\kappa^{*}=\\lambda L$",
   ks_band="$\\kappa$ plausible\npour accélérateurs",
   ks_leg="Taux de panne $\\lambda$",
   files=["fig1_declin_juridictions", "fig2_montecarlo_chine",
          "fig3_relatif_frontiere", "fig4_tornade_sensibilite",
          "fig5_comparaison_aviation", "fig6_regimes_kappa",
          "fig7_kappa_critique"]),
}[LANG]

NM = LABELS["names"]
STYLE = {NM[0]: (ACCENT, "-"), NM[1]: (BLUE, "--"), NM[2]: (GREEN, "-.")}
FN = LABELS["files"]


def save(fig, name):
    for e in ("pdf", "png"):
        fig.savefig(os.path.join(FIGDIR, f"{name}.{e}"))
    plt.close(fig)


def main():
    china = M.Params(M.C0_CHINA, M.AFR_PACKAGE, np.mean(M.KAPPA_COMPUTE),
                     M.USEFUL_LIFE_C, M.FRONTIER_DOUBLING_C,
                     M.CN_DOMESTIC_PM * M.CN_STOCKPILE_DEPENDENCE_C, M.LEAK_PM * 0.35)
    _l = -np.log(1 - M.AFR_PACKAGE) / 12 + 1 / (M.USEFUL_LIFE_C * 12)
    us = M.Params(M.C0_US, M.AFR_PACKAGE, np.mean(M.KAPPA_COMPUTE), M.USEFUL_LIFE_C,
                  M.FRONTIER_DOUBLING_C, M.C0_US * _l * M.US_COVERAGE, 0.0)
    eu = M.Params(M.C0_EU, M.AFR_PACKAGE, np.mean(M.KAPPA_COMPUTE), M.USEFUL_LIFE_C,
                  M.FRONTIER_DOUBLING_C, M.C0_EU * _l * M.EU_COVERAGE, 0.0)
    traj = {NM[i]: M.simulate(p, HORIZON)
            for i, p in enumerate([china, us, eu])}

    # Fig 1
    f, ax = plt.subplots(figsize=(5.5, 3.1))
    for n_, d in traj.items():
        c, ls = STYLE[n_]; ax.plot(d.month, d.frac_of_t0, color=c, ls=ls, label=n_)
    ax.axhline(.5, color=GREY, lw=.7, ls=":")
    ax.text(HORIZON * .99, .52, LABELS["half"], ha="right", fontsize=7, color=GREY)
    ax.set(xlabel=LABELS["xlab"], ylabel=LABELS["ylab"], xlim=(0, HORIZON), ylim=(0, 1.06))
    ax.yaxis.set_major_formatter(pct); ax.legend(frameon=False, loc="lower left")
    save(f, FN[0])

    # Fig 2
    f, ax = plt.subplots(figsize=(5.5, 3.1))
    A = np.vstack([M.simulate(M.draw(china, "CN"), HORIZON).frac_of_t0.to_numpy()
                   for _ in range(800)])
    m = np.arange(A.shape[1])
    for lo, hi, a in [(5, 95, .16), (25, 75, .30)]:
        ax.fill_between(m, np.percentile(A, lo, 0), np.percentile(A, hi, 0),
                        color=ACCENT, alpha=a, lw=0)
    ax.plot(m, np.percentile(A, 50, 0), color=ACCENT, lw=1.9)
    ax.axhline(.5, color=GREY, lw=.7, ls=":")
    ax.set(xlabel=LABELS["xlab"], ylabel=LABELS["ylab"], xlim=(0, HORIZON), ylim=(0, 1.06))
    ax.yaxis.set_major_formatter(pct)
    ax.text(2, .05, LABELS["mc"], fontsize=7, color=GREY)
    save(f, FN[1])

    # Fig 3
    f, ax = plt.subplots(figsize=(5.5, 3.1))
    for n_, d in traj.items():
        c, ls = STYLE[n_]
        ax.semilogy(d.month, np.maximum(d.frontier_relative, 1e-3), color=c, ls=ls, label=n_)
    ax.axhline(.10, color=GREY, lw=.7, ls=":")
    ax.text(71, .125, LABELS["fr_t"], ha="right", va="bottom", fontsize=7, color=GREY)
    ax.set(xlabel=LABELS["xlab"], ylabel=LABELS["fr_y"], xlim=(0, 72), ylim=(0.02, 120))
    ax.legend(frameon=False, loc="upper right")
    save(f, FN[2])

    # Fig 4
    R = json.load(open(os.path.join(M.DATADIR, "results.json")))
    sens = sorted(R["sensitivity"], key=lambda r: r["span"])
    f, ax = plt.subplots(figsize=(5.5, 2.6))
    for i, r in enumerate(sens):
        lo, hi = sorted([r["low"], r["high"]])
        ax.barh(i, max(hi - lo, .35), left=lo, height=.55, color=LGREY,
                edgecolor=INK, lw=.6)
        ax.plot([r["base"]], [i], marker="|", color=ACCENT, ms=13, mew=2.2)
    ax.set_yticks(range(len(sens)))
    ax.set_yticklabels([LABELS["par"].get(r["parameter"], r["parameter"]) for r in sens])
    ax.set_xlabel(LABELS["tor_x"])
    ax.text(.99, .04, LABELS["central"], transform=ax.transAxes, ha="right",
            fontsize=7, color=ACCENT)
    save(f, FN[3])

    # Fig 5
    lam_a, av_p, av_d, av_obs, sse, unexpl = M.aviation_comparison()
    f, ax = plt.subplots(figsize=(5.5, 3.0))
    ax.plot(av_d.month, av_d.frac_of_t0, color=BLUE,
            label=LABELS["av_model"].format(lam=lam_a))
    ax.scatter(av_obs.month, av_obs.observed, color=ACCENT, zorder=5, s=36,
               label=LABELS["av_obs"])
    ax.fill_between(av_obs.month, av_obs.observed, av_obs.model_attrition_only,
                    color=ACCENT, alpha=.13, lw=0)
    ax.annotate(LABELS["av_res"], xy=(46, .69), fontsize=6.6, color=ACCENT, ha="right")
    for _, r in av_obs.iterrows():
        ax.annotate(LABELS["av_notes"][r.month], (r.month, r.observed),
                    textcoords="offset points", xytext=(-6, -13),
                    fontsize=6.3, color=GREY, ha="right")
    ax.set(xlabel=LABELS["av_x"], ylabel=LABELS["av_y"], xlim=(0, 60), ylim=(0, 1.06))
    ax.yaxis.set_major_formatter(pct); ax.legend(frameon=False, loc="lower left")
    save(f, FN[4])

    # Fig 6
    f, ax = plt.subplots(figsize=(5.5, 3.0))
    for kv, lab, col, lw in [(M.KAPPA_AVIATION, LABELS["kap"][0], BLUE, 1.2),
                             (1.0, LABELS["kap"][1], GREY, 1.2),
                             (0.50, LABELS["kap"][2], "#d94801", 1.9),
                             (0.05, LABELS["kap"][3], ACCENT, 1.9)]:
        d = M.simulate(replace(china, kappa=kv), HORIZON)
        ax.plot(d.month, d.frac_of_t0, color=col, lw=lw,
                ls="-" if kv <= .5 else "--", label=lab)
    ax.axhline(.5, color=GREY, lw=.7, ls=":")
    ax.set(xlabel=LABELS["xlab"], ylabel=LABELS["ylab"], xlim=(0, HORIZON), ylim=(0, 1.06))
    ax.yaxis.set_major_formatter(pct); ax.legend(frameon=False, loc="lower left")
    save(f, FN[5])

    # Fig 7
    f, ax = plt.subplots(figsize=(5.5, 3.0))
    lives = np.linspace(1.5, 6.5, 240)
    for a, lab, col in [(M.AFR_GPU_DIE, LABELS["afr"][0], GREY),
                        (M.AFR_PACKAGE, LABELS["afr"][1], ACCENT),
                        (M.AFR_ALL, LABELS["afr"][2], BLUE)]:
        ax.plot(lives, [M.kappa_critical(a, L) for L in lives], color=col, label=lab)
    ax.axhspan(M.KAPPA_COMPUTE[0], M.KAPPA_COMPUTE[1], color=GREEN, alpha=.13, lw=0)
    ax.text(6.4, np.mean(M.KAPPA_COMPUTE), LABELS["ks_band"], fontsize=6.8,
            color=GREEN, ha="right", va="center")
    ax.set(xlabel=LABELS["ks_x"], ylabel=LABELS["ks_y"], xlim=(1.5, 6.5), ylim=(0, 1.25))
    ax.legend(frameon=False, loc="upper left", title=LABELS["ks_leg"])
    ax.get_legend().get_title().set_fontsize(7)
    save(f, FN[6])

    print(f"figures [{LANG}] → {FIGDIR}")
    for fn in sorted(os.listdir(FIGDIR)):
        if fn.endswith(".png"):
            print("  ", fn)


if __name__ == "__main__":
    main()
