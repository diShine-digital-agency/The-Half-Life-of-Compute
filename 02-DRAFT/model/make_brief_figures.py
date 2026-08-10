#!/usr/bin/env python3
"""
Purpose-built graphics for the executive summary.

The paper's figures are correct but assume a reader comfortable with log axes and
survival curves. These three are built for a policy or general-technical reader:
one idea each, labelled in plain language, readable at a glance.

    BRIEF_LANG=en|it|fr python3 make_brief_figures.py  → ../figures_brief_<lang>/
"""
import os, json

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

import compute_decay_model as M

LANG = os.environ.get("BRIEF_LANG", "en").lower()
OUTDIR = os.path.normpath(os.path.join(M.HERE, "..", f"figures_brief_{LANG}"))
os.makedirs(OUTDIR, exist_ok=True)

R = json.load(open(os.path.join(M.DATADIR, "results.json")))
MC = {m["jurisdiction"]: m for m in R["montecarlo"]}
KSTAR = R["kappa_star"]["central"]

INK, ACCENT, BLUE, GREY, LGREY, GREEN = "#1a1a1a", "#8c2d04", "#08519c", "#737373", "#dcdcdc", "#00441b"

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": 10, "axes.labelsize": 10, "legend.fontsize": 9,
    "xtick.labelsize": 9, "ytick.labelsize": 9,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.linewidth": .8, "lines.linewidth": 2.2,
    "figure.dpi": 220, "savefig.bbox": "tight", "savefig.pad_inches": .04,
})

T = {
 "en": dict(
   c1_title="Your hardware survives. Your position does not.",
   c1_x="Months after supply is cut",
   c1_hw="Chips still working",
   c1_fr="Standing versus the moving frontier",
   c1_note="When the frontier-exit line is crossed, the country\nstill holds most of its chips. Position is lost\nlong before hardware is.",
   c1_mark="frontier exit",
   f2_x="Share of its own compute a country could sustain if cut off",
   f2_note="100% would mean genuine self-sufficiency.\nNo one is close.",
   f2_names=["United States", "China", "European Union"],
   f2_self="self-sufficient",
   f3_x="Cannibalisation yield $\\kappa$: repairs recovered per dead unit",
   f3_decay="Failures add\nto the decline", f3_persist="Salvage absorbs them\nextra effort is idle",
   f3_band="What accelerators\nplausibly are",
   f3_star="critical threshold $\\kappa^{*}$ = 0.38",
   f3_note="",
   files=["brief1_two_clocks", "brief2_sovereign_floor", "brief3_threshold"]),

 "it": dict(
   c1_title="L'hardware sopravvive. La posizione no.",
   c1_x="Mesi dall'interruzione delle forniture",
   c1_hw="Chip ancora funzionanti",
   c1_fr="Posizione rispetto alla frontiera mobile",
   c1_note="Quando si attraversa la linea di uscita, il paese\npossiede ancora quasi tutti i suoi chip. La posizione\nsi perde molto prima dell'hardware.",
   c1_mark="uscita dalla frontiera",
   f2_x="Quota del proprio calcolo sostenibile se reciso dalle forniture",
   f2_note="Il 100% significherebbe vera autosufficienza.\nNessuno vi si avvicina.",
   f2_names=["Stati Uniti", "Cina", "Unione Europea"],
   f2_self="autosufficienza",
   f3_x="Resa di cannibalizzazione $\\kappa$: riparazioni per unità guasta",
   f3_decay="I guasti si sommano\nal declino", f3_persist="Il recupero li assorbe\nsforzo extra inutile",
   f3_band="Ciò che gli acceleratori\nplausibilmente sono",
   f3_star="soglia critica $\\kappa^{*}$ = 0,38",
   f3_note="",
   files=["brief1_due_orologi", "brief2_soglia_sovranita", "brief3_soglia"]),

 "fr": dict(
   c1_title="Le matériel survit. La position, non.",
   c1_x="Mois après la coupure d'approvisionnement",
   c1_hw="Puces encore en fonctionnement",
   c1_fr="Position face à la frontière mobile",
   c1_note="Au franchissement de la ligne de sortie, le pays\ndétient encore l'essentiel de ses puces. La position\nse perd bien avant le matériel.",
   c1_mark="sortie de la frontière",
   f2_x="Part de son calcul soutenable en cas de rupture",
   f2_note="100% signifierait une véritable autosuffisance.\nPersonne n'en approche.",
   f2_names=["États-Unis", "Chine", "Union européenne"],
   f2_self="autosuffisance",
   f3_x="Rendement de cannibalisation $\\kappa$ : réparations par unité morte",
   f3_decay="Les pannes s'ajoutent\nau déclin", f3_persist="La récupération les absorbe\neffort supplémentaire inutile",
   f3_band="Ce que sont plausiblement\nles accélérateurs",
   f3_star="seuil critique $\\kappa^{*}$ = 0,38",
   f3_note="",
   files=["brief1_deux_horloges", "brief2_plancher_souverainete", "brief3_seuil"]),
}[LANG]

pct = FuncFormatter(lambda y, _: f"{y*100:.0f}%")


def save(fig, name):
    for e in ("pdf", "png"):
        fig.savefig(os.path.join(OUTDIR, f"{name}.{e}"))
    plt.close(fig)


def main():
    china = M.Params(M.C0_CHINA, M.AFR_PACKAGE, np.mean(M.KAPPA_COMPUTE),
                     M.USEFUL_LIFE_C, M.FRONTIER_DOUBLING_C,
                     M.CN_DOMESTIC_PM * M.CN_STOCKPILE_DEPENDENCE_C, M.LEAK_PM * 0.35)
    d = M.simulate(china, 60)

    # ── 1 · the two clocks — the central insight, one picture ────────────────
    f, ax = plt.subplots(figsize=(6.4, 3.5))
    ax.plot(d.month, d.frac_of_t0, color=BLUE, label=T["c1_hw"])
    fr = np.clip(d.frontier_relative, 0, 1)
    ax.plot(d.month, fr, color=ACCENT, label=T["c1_fr"])
    ax.fill_between(d.month, fr, d.frac_of_t0, color=LGREY, alpha=.55, lw=0)

    tf = MC["China"]["t_frontier_med"]
    ax.axvline(tf, color=GREY, lw=.8, ls=":")
    ax.annotate(T["c1_mark"], xy=(tf, 1.02), fontsize=8, color=GREY,
                ha="center", va="bottom")
    ax.annotate(T["c1_note"], xy=(28.5, .40), fontsize=8.4, color=INK, ha="left",
                va="center")
    ax.annotate("", xy=(25.5, .77), xytext=(30.5, .50),
                arrowprops=dict(arrowstyle="-", color=GREY, lw=.7))
    ax.annotate("", xy=(25.5, .14), xytext=(30.5, .33),
                arrowprops=dict(arrowstyle="-", color=GREY, lw=.7))

    ax.set_xlabel(T["c1_x"]); ax.set_ylabel("")
    ax.set_xlim(0, 60); ax.set_ylim(0, 1.12)
    ax.yaxis.set_major_formatter(pct)
    ax.legend(frameon=False, loc="lower left", bbox_to_anchor=(0.0, -0.03))
    ax.set_title(T["c1_title"], fontsize=10.5, loc="left", pad=14, color=INK)
    save(f, T["files"][0])

    # ── 2 · sovereign floors — the most quotable number ──────────────────────
    f, ax = plt.subplots(figsize=(6.4, 2.7))
    order = ["United States", "China", "European Union"]
    vals = [MC[k]["floor_med"] / 100 for k in order]
    los = [MC[k]["floor_p05"] / 100 for k in order]
    his = [MC[k]["floor_p95"] / 100 for k in order]
    y = np.arange(len(order))[::-1]
    cols = [BLUE, ACCENT, GREEN]
    for i, (v, lo, hi, c) in enumerate(zip(vals, los, his, cols)):
        ax.barh(y[i], v, height=.5, color=c, alpha=.85, lw=0)
        ax.plot([lo, hi], [y[i], y[i]], color=INK, lw=1.1, alpha=.55)
        for e in (lo, hi):
            ax.plot([e, e], [y[i] - .09, y[i] + .09], color=INK, lw=1.1, alpha=.55)
        # label clear of the whisker, never on top of it
        ax.text(hi + .028, y[i], f"{v*100:.0f}%",
                va="center", fontsize=11.5, color=INK, fontweight="bold")
    ax.axvline(1.0, color=GREY, lw=1.0, ls="--")
    ax.text(1.0, len(order) - 0.52, f"100% = {T['f2_self']}", fontsize=8.2,
            color=GREY, ha="center", va="bottom")
    ax.set_yticks(y); ax.set_yticklabels(T["f2_names"], fontsize=10.5)
    # xmax must clear the widest whisker (China's interval crosses parity)
    ax.set_xlim(0, max(1.22, max(his) + 0.22)); ax.set_ylim(-0.55, len(order) - 0.25)
    ax.xaxis.set_major_formatter(pct)
    ax.set_xlabel(T["f2_x"], fontsize=9.4)
    ax.spines["left"].set_visible(False); ax.tick_params(axis="y", length=0)
    save(f, T["files"][1])

    # ── 3 · the threshold — why the answer is not yet knowable ───────────────
    # Two stacked registers: regime bands on top, the plausible range as a
    # discrete bar beneath, so neither can obscure the other's label.
    f, ax = plt.subplots(figsize=(6.4, 2.35))
    lo, hi = M.KAPPA_COMPUTE

    # regime bands (upper register only)
    ax.add_patch(plt.Rectangle((0, .45), KSTAR, .55, color=ACCENT, alpha=.13, lw=0))
    ax.add_patch(plt.Rectangle((KSTAR, .45), 1 - KSTAR, .55, color=GREEN, alpha=.12, lw=0))
    ax.plot([KSTAR, KSTAR], [0, 1.0], color=INK, lw=1.5, zorder=5)

    ax.text(KSTAR / 2, .72, T["f3_decay"], ha="center", va="center",
            fontsize=9.2, color=ACCENT, linespacing=1.35)
    ax.text((KSTAR + 1.0) / 2, .72, T["f3_persist"], ha="center", va="center",
            fontsize=9.2, color=GREEN, linespacing=1.35)
    ax.text(KSTAR, 1.05, T["f3_star"], ha="center", va="bottom",
            fontsize=8.8, color=INK)

    # plausible range (lower register)
    ax.add_patch(plt.Rectangle((lo, .12), hi - lo, .20, facecolor=INK, alpha=.16,
                               edgecolor=INK, lw=1.1, zorder=4))
    ax.annotate("", xy=(lo, .22), xytext=(hi, .22),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=1.0), zorder=6)
    ax.text((lo + hi) / 2, .015, T["f3_band"], ha="center", va="bottom",
            fontsize=8.6, color=INK)

    ax.set_xlim(0, 1.0); ax.set_ylim(0, 1.0)
    ax.set_yticks([]); ax.spines["left"].set_visible(False)
    ax.set_xlabel(T["f3_x"], fontsize=9.4)
    save(f, T["files"][2])

    print(f"brief figures [{LANG}] → {OUTDIR}")
    for fn in sorted(os.listdir(OUTDIR)):
        if fn.endswith(".png"):
            print("  ", fn)


if __name__ == "__main__":
    main()
