#!/usr/bin/env python3
"""
Single source of truth for the manuscript.

Both renderers (build_pdf.py, build_docx.py) consume this module, so the PDF and
the Word file cannot diverge. Numerical claims are pulled from
03-DATA/processed/results.json wherever possible, so editing the model and
re-running regenerates the prose figures too.

Block grammar:
  ("h1"|"h2"|"h3", text)   ("p", text)        ("abstract", text)
  ("eq", latexish, label)  ("fig", path, caption, label)
  ("table", caption, label, [headers], [[rows]], note)
  ("quote", text)          ("bullets", [items])  ("numbers", [items])
Inline markup: *italic*, **bold**.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
FIG = os.path.join(ROOT, "05-DRAFT", "figures")
R = json.load(open(os.path.join(ROOT, "03-DATA", "processed", "results.json")))
RX = json.load(open(os.path.join(ROOT, "03-DATA", "processed", "results_extended.json")))
LK = RX["leakage"]; SAT = RX["kappa_saturation"]; LIFE = RX["useful_life"]

d = R["derived"]; ks = R["kappa_star"]; av = R["aviation"]
MC = {m["jurisdiction"]: m for m in R["montecarlo"]}
CN, US, EU = MC["China"], MC["United States"], MC["European Union"]
SENS = R["sensitivity"]


def n0(x): return f"{x:,.0f}"
def p1(x): return f"{x:.1f}"
def p2(x): return f"{x:.2f}"
def mo(x): return ">120" if x == float("inf") else f"{x:.0f}"


# ─────────────────────────────────────────────────────────────────────────────
META = dict(
    title="The Half-Life of Compute: Modelling National AI Capacity "
          "Decay Under Supply Severance",
    authors="Kevin Escoda",
    affiliation="diShine · Data, AI & Automation, Milan, Italy",
    email="kevin@dishine.it",
    orcid="0009-0009-7368-8129",            # placeholder
    doi="10.5281/zenodo.21866487",           # reserve on Zenodo, paste, rebuild
    preprint_id="arXiv:XXXX.XXXXX",         # placeholder
    preprint_class="cs.CY",
    date="8 August 2026",
    version="Preprint v1.0, not peer reviewed",
    keywords="compute governance; export controls; technological sovereignty; "
             "semiconductor supply chains; weaponized interdependence; AI policy; "
             "survival analysis",
    jel="F51, F52, L63, O33, O38",
    acm="Social and professional topics → Computing and business; "
        "Hardware → Reliability",
)

ABSTRACT = (
    "Export controls on artificial-intelligence hardware are justified by an "
    "implicit temporal claim: that restricting access to advanced accelerators "
    "buys time. The size of that interval has never been estimated. Existing "
    "measurement work treats national AI capacity as a *stock*: eleven public "
    "indices rank jurisdictions by installed compute, talent and infrastructure, "
    "and none models what becomes of that stock once resupply stops. Reliability "
    "research, conversely, measures accelerator failure under an explicit "
    "assumption of continuous replenishment. This paper joins the two. We model "
    "an installed base of AI accelerators as a perishable capital fleet subject "
    "to hardware failure, obsolescence against a moving capability frontier, "
    "partial salvage, and bounded domestic replacement, and we derive three "
    "reportable quantities: the compute half-life $T_{1/2}$, the frontier exit "
    "time $T_f$, and the sovereign floor $C_\\infty$. Failure rates are derived "
    "from published large-cluster telemetry (an annualised package failure rate "
    f"of {p2(d['AFR_PACKAGE']*100)}%, cross-validated against an independent "
    "estimate to within 1.4%). We obtain an analytic result: salvage absorbs the "
    "failure flow only above a critical cannibalisation ratio "
    f"$\\kappa^{{*}} = \\lambda L$, equal to {p2(ks['central'])} under central "
    "parameters, beyond which further salvage capacity buys nothing and decline is "
    "set by obsolescence alone, while below it unrepaired failures accelerate "
    f"decline by up to {SAT['excess_at_zero_pct']:.0f}%. Because high-bandwidth "
    "memory is co-packaged with the die and neither is field-replaceable, the "
    "plausible range for accelerators straddles this threshold. Applying the model to "
    "three jurisdictions, we find frontier exit at "
    f"{mo(EU['t_frontier_med'])}-{mo(US['t_frontier_med'])} months, governed by "
    "$T_f \\simeq T_{\\mathrm{dbl}}\\log_2(C_0/\\theta F_0)$: installed stock buys "
    "time only **logarithmically**, so an order of magnitude more compute buys "
    "roughly 17 further months, and hardware decay accounts for only 13-14% of "
    "the interval. Median sovereign floors are "
    f"{p1(US['floor_med'])}% for the United States, {p1(CN['floor_med'])}% for "
    f"China and {p1(EU['floor_med'])}% for the European Union; China's 90% "
    f"interval, however, spans {p1(CN['floor_p05'])}-{p1(CN['floor_p95'])}% of "
    "its base; whether China could sustain its fleet domestically is, on "
    "current public data, genuinely undetermined. Sensitivity analysis shows "
    "the rate of frontier advance dominates hardware attrition sevenfold. The "
    "policy implication is that severance need not destroy an adversary's "
    "compute; where remote access is also interdicted, freezing it suffices "
    "while the frontier moves."
)

# ─────────────────────────────────────────────────────────────────────────────
BODY = [

# ══ 1 ════════════════════════════════════════════════════════════════════════
("h1", "1  Introduction"),

("p",
 "Every argument for controlling the export of artificial-intelligence hardware "
 "rests on a claim about time. Restricting an adversary's access to advanced "
 "accelerators is said to *buy* something: a lead, a window, a delay before "
 "capability parity. The claim is temporal, quantitative and, so far as we have "
 "been able to establish, unquantified. No published work states how long a "
 "jurisdiction cut off from the global accelerator supply chain could sustain "
 "the compute base it already owns."),

("p",
 "This is not for want of measurement. National artificial-intelligence capacity "
 "is now one of the most heavily indexed quantities in technology policy. At "
 "least eleven public instruments rank jurisdictions on some combination of "
 "installed compute, energy, talent, model output and governance capacity. They "
 "differ in construction and in candour, but they share a structural property: "
 "each is a **snapshot of holdings**. They answer *what does a country have?* "
 "None answers *what would a country keep?*"),

("p",
 "The distinction matters because installed compute is not a reserve. It is a "
 "capital fleet with a measurable failure rate, a contested economic life, a "
 "dependence on a separately concentrated memory supply, and a capability that "
 "is defined relative to a frontier that does not stand still. A stock of gold "
 "does not corrode; a stock of accelerators does. Treating the two alike is the "
 "central modelling error this paper sets out to correct."),

("p",
 "The reliability literature has measured the corrosion rate precisely, but "
 "under an assumption that voids its use here. Large-cluster telemetry gives "
 "well-characterised accelerator failure statistics, and the leading analysis of "
 "whether such failures constrain scaling concludes that they do not, while "
 "stating plainly that it assumes replacement nodes remain procurable and does "
 "not address supply-chain disruption or situations in which replacement chips "
 "cannot be obtained. That assumption is exactly what severance removes. "
 "Relaxing it is the contribution of this paper."),

("h2", "1.1  Contribution"),
("numbers", [
 "**A decay model of installed compute under severance.** We treat a national "
 "accelerator base as a perishable fleet subject to failure, obsolescence, "
 "partial salvage and bounded domestic replacement, and integrate it forward "
 "monthly. Failure parameters are derived from published telemetry rather than "
 "assumed, and cross-validated against an independent estimate.",
 "**Three reportable quantities.** The compute half-life $T_{1/2}$, the frontier "
 "exit time $T_f$, and the sovereign floor $C_\\infty$, the capacity a "
 "jurisdiction retains asymptotically from domestic production alone. "
 "$C_\\infty$ is, we argue, the quantity that the word *sovereignty* has been "
 "used to gesture at without ever being given a number.",
 "**An analytic threshold.** Salvage sustains an installed base only above a "
 "critical cannibalisation ratio $\\kappa^{*} = \\lambda L$. This is a property "
 "of the hardware, not of policy, and it separates two qualitatively different "
 "severance regimes.",
 "**A negative result reported in full.** We attempted to calibrate the model "
 "against the only observed severance of a comparable capital fleet, Russian "
 "civil aviation after February 2022, and the calibration fails. We report the "
 "failure, diagnose it, and explain why it constrains the analogy rather than "
 "the model.",
]),

("p",
 "We deliberately do not propose another index. The field has eleven, and an "
 "eleventh-and-a-half would be neither novel nor useful. Existing indices enter "
 "this paper as inputs and related work, not as rivals."),

# ══ 2 ════════════════════════════════════════════════════════════════════════
("h1", "2  Related work"),

("h2", "2.1  Measuring national technological capacity"),
("p",
 "Composite indices of technological capacity are numerous and methodologically "
 "mature. The Machinepower Index (2026) scores twenty-five jurisdictions across "
 "twelve cells grouped as Watts, Weights and Will, aggregating with a "
 "constant-elasticity-of-substitution mean at $\\sigma = 0.33$ so that a single "
 "weak cell constrains the total rather than being averaged away; its own "
 "documentation records that 37% of underlying measurements are analyst "
 "judgement, and that no time dimension, decay, depreciation, failure rate or "
 "severance scenario is modelled. The CNAS Sovereign AI Index (2026) catalogues "
 "over 139 state-backed projects and finds that most remain dependent on foreign "
 ", predominantly United States, technology across the stack; it is explicitly "
 "not a dependency-severance model. Academic instruments are similar in "
 "structure: Lee et al. (2024) decompose technology sovereignty into innovation "
 "capability, production capability and supply-chain independence for the "
 "semiconductor industry; Caravella et al. (2023) trace strategic dependencies "
 "through the photovoltaic supply chain; Cai et al. (2026) review 104 articles "
 "on semiconductor industrial policy and regional ecosystem governance. Broader "
 "instruments, the Government AI Readiness Index, the Global AI Index, the "
 "annual AI Index, extend coverage without changing the temporal logic."),
("p",
 "Every one of these is cross-sectional. The methodological literature on "
 "composite indicators is itself explicit that weighting, aggregation and "
 "robustness are where such instruments succeed or fail (Greco et al., 2018; "
 "Dobbie et al., 2013; Kelemen et al., 2024; OECD/JRC, 2008), and we adopt its "
 "discipline below. But no amount of care in aggregation converts a snapshot "
 "into a trajectory."),

("h2", "2.2  Compute governance and accelerator reliability"),
("p",
 "Sastry et al. (2024) establish the governing framework: computing power is a "
 "tractable object of policy because it is detectable, excludable, quantifiable "
 "and produced through an extremely concentrated supply chain. Those four "
 "properties are precisely the conditions under which a severance model is "
 "possible; this paper can be read as the quantitative successor to that "
 "qualitative argument. Regulatory practice has moved the same way, with "
 "cumulative processing performance rather than unit counts becoming the "
 "controlled quantity."),
("p",
 "On the hardware side, Grattafiori et al. (2024) report component-resolved "
 "interruption statistics for a 16,384-accelerator pre-training run, and Kokolis "
 "et al. (2025) fit failure models across more than 150 million accelerator-hours "
 "spanning two production clusters. Epoch AI's analysis concludes that hardware "
 "failure will not limit scaling, under continuous replenishment. Our reading "
 "of that boundary condition, stated in the source itself, motivates the present "
 "work."),

("p",
 "A third lineage is closer than either and must be acknowledged: military "
 "sustainment modelling. Sherbrooke's METRIC (1968) and the multi-echelon "
 "tradition it founded optimise recoverable-spare stocks for fleet availability, "
 "and its modern extensions incorporate cannibalisation explicitly. That "
 "literature is the nearest quantitative relative of our salvage term, and we "
 "borrow its vocabulary. It differs on exactly the margins this paper needs: it "
 "optimises inventory under a functioning resupply pipeline rather than total "
 "severance, and its systems face no moving capability frontier, an aircraft "
 "that flies is available, whereas an accelerator that runs may already be "
 "strategically obsolete. The threshold $\\kappa^{*}$ should accordingly be "
 "read as the severance-regime limit of that tradition, not as a claim to have "
 "discovered cannibalisation."),

("h2", "2.3  Economic statecraft and chokepoints"),
("p",
 "Farrell and Newman (2019) supply the theoretical frame: asymmetric network "
 "topology allows states with jurisdiction over central nodes to exercise a "
 "*panopticon effect* and a *chokepoint effect*, the latter denying network "
 "access to adversaries. Beaumier et al. (2023) apply network analysis directly "
 "to semiconductors, decomposing the supply chain into design, raw material, "
 "manufacturing-equipment and assembled-chip networks and showing how centrality "
 "in one enables weaponisation of another. Fuller (2026) argues the framework "
 "transfers imperfectly to physical goods, where a chokepoint is better "
 "understood as an input without which a task cannot continue, a formulation "
 "that maps closely onto the model developed here."),
("p",
 "Quantitative evaluation of controls has concentrated on economic aggregates. "
 "Park and Liu (2023) use multi-regional input-output methods; Cui et al. (2025) "
 "employ a dynamic computable general equilibrium model to estimate GDP effects "
 "of the chip embargo and of Chinese counter-controls on gallium, germanium and "
 "graphite; Shrivastava et al. (2025) assess circumvention. Supply-chain "
 "resilience has been modelled with scale-free cascade topologies and Bayesian "
 "networks. All of this measures **economic** consequence. None measures "
 "**capability decay over time**."),
("p",
 "Industry analysis comes closest. Estimates of when a stockpile of unassembled "
 "dies will be exhausted have been published, including a zero-inflated "
 "formulation assigning roughly a 56% probability that one such stockpile was "
 "depleted by January 2026. That work models *inventory drawdown*, components "
 "awaiting assembly. The present paper models *installed-base decay*, hardware "
 "already deployed and running. The two are different questions with different "
 "mathematics, and we are careful to claim only the second."),

("quote",
 "Prior work measures what a jurisdiction holds, what it can build, and what "
 "severance costs its economy. This paper measures how long what it holds keeps "
 "working."),

# ══ 3 ════════════════════════════════════════════════════════════════════════
("h1", "3  Model"),

("h2", "3.1  Setup"),
("p",
 "Let $N(t)$ denote the number of operational accelerators, in H100-equivalents "
 "(H100e), at month $t$ after severance, with $N(0) = C_0$. Effective national "
 "compute is"),
("eq", "C(t) \\;=\\; N(t)\\,u(t)", "1"),
("p",
 "where $u(t) \\in (0,1]$ is a utilisation ceiling imposed by energy, "
 "interconnect and operational constraints. Three flows act on $N$ each period. "
 "Hardware failures occur at monthly hazard "
 "$\\lambda = -\\ln(1-\\mathrm{AFR})/12$. Obsolescence retires units at rate "
 "$\\delta = 1/L$, with $L$ the useful life in months; retired units remain "
 "physically intact. Replacement arrives as domestic production plus leakage, "
 "$R = R_{\\mathrm{dom}} + R_{\\mathrm{leak}}$."),
("p",
 "The mechanism that distinguishes severance from normal operation is salvage. "
 "Under resupply a failed unit is replaced and $N$ is unchanged, which is why "
 "reliability analyses conclude that failures do not bind. Under severance the "
 "only source of repair is other units. Let $P(t)$ be the pool of salvageable "
 "repairs and let $\\kappa$ be the *cannibalisation yield*: the number of "
 "repairs recoverable from one donor unit. Then"),
("eq",
 "\\begin{aligned}"
 "F_t &= N_t\\lambda, \\qquad \\mathrm{Ret}_t = N_t\\delta \\\\"
 "\\rho_t &= \\min(F_t,\\;P_t) \\\\"
 "P_{t+1} &= P_t - \\rho_t + \\kappa\\,(F_t - \\rho_t + \\mathrm{Ret}_t) \\\\"
 "N_{t+1} &= N_t - F_t - \\mathrm{Ret}_t - S_t + \\rho_t + R"
 "\\end{aligned}", "2"),
("p",
 "where $S_t$ is the number of *serviceable* units voluntarily withdrawn for "
 "parts. Withdrawal is rational only when one donor yields more than one repair, "
 "so $S_t > 0$ requires $\\kappa > 1$; we cap it at 3% of the fleet per month."),

("h2", "3.2  The critical cannibalisation ratio"),
("p",
 "The salvage pool is replenished by units leaving service and drained by "
 "repairs. Retirements alone sustain the repair flow when "
 "$\\kappa N\\delta \\geq N\\lambda$, which gives a threshold independent of "
 "fleet size, inflow and policy:"),
("eq", "\\kappa^{*} \\;=\\; \\frac{\\lambda}{\\delta} \\;=\\; \\lambda L", "3"),
("p",
 "$\\kappa^{*}$ is a **saturation** threshold, not a survival threshold, and the "
 "distinction matters. Above it, salvage absorbs essentially the entire failure "
 "flow and the installed base declines at the obsolescence rate alone; further "
 "salvage capacity buys nothing. Below it, unrepaired failures accumulate on top "
 "of retirement, and at $\\kappa = 0$ the fleet contracts "
 f"{SAT['excess_at_zero_pct']:.0f}% faster than obsolescence alone would imply. "
 "What $\\kappa^{*}$ separates is a *failure-limited* regime from an "
 "*obsolescence-limited* one. It does not separate survival from collapse: absent "
 "replacement inflow every fleet declines, because retirement removes units "
 "whether or not failures are repaired. $\\kappa^{*}$ is a property of the "
 "hardware, its failure rate and its useful life, not of the jurisdiction "
 "holding it. Appendix A gives the derivation; §5.1 gives the verification."),
("p",
 "This threshold is where the physical architecture of accelerators becomes "
 "decisive, and where the analogy with other capital fleets breaks. An airframe "
 "is parts-rich: it decomposes into thousands of independently failing "
 "line-replaceable units, and observed practice under sanctions has been to "
 "dismantle roughly one airframe to keep about ten flying, implying "
 "$\\kappa \\approx 10$. An AI accelerator is parts-poor in exactly the wrong "
 "place. High-bandwidth memory is co-packaged with the logic die on a shared "
 "interposer; neither the die nor the memory stack is a field-replaceable unit. "
 "The two dominant failure modes are therefore non-salvageable **by "
 "construction**, and cannibalisation recovers only ancillary node components, "
 "power supplies, network interfaces, cooling, which are not the binding "
 "failure modes. We take $\\kappa \\in [0.05, 0.50]$ for accelerators and treat "
 "the aviation value as an upper bound belonging to a different hardware class."),

("h2", "3.3  Reported quantities"),
("bullets", [
 "**Compute half-life $T_{1/2}$**, months until effective compute falls below "
 "half its severance-day value. Right-censored at the 120-month horizon.",
 "**Frontier exit time $T_f$**, months until national capacity falls below a "
 "threshold share $\\theta = 0.10$ of the contemporaneous frontier training "
 "scale $F(t) = F_0\\,2^{t/T_{\\mathrm{dbl}}}$, where $F_0$ is an **absolute, "
 "jurisdiction-common** anchor. An earlier draft normalised by each "
 "jurisdiction's own $C_0$ instead, which forced every jurisdiction to begin at "
 "parity and made $C_0$ cancel identically; the apparent stock-invariance that "
 "followed was an algebraic artefact and has been withdrawn (§5.3, Appendix A).",
 "**Sovereign floor $C_\\infty$**, the asymptotic level as a share of $C_0$, "
 "sustainable from all non-severed inflow, domestic production *and* residual "
 "leakage, held at its severance-date rate. A closed form exists and is given "
 "in Appendix A; it reproduces the 900-month integration exactly. $C_\\infty$ is "
 "defined only for zero indigenisation growth (§7.4).",
]),

# ══ 4 ════════════════════════════════════════════════════════════════════════
("p",
 "The anchor $F_0$ deserves its derivation in the open, since $T_f$ inherits it "
 "through the logarithm. A frontier training run of $10^{26}$ to $10^{27}$ FLOP, "
 "executed over roughly three months on accelerators sustaining an effective "
 "$4 \\times 10^{14}$ FLOP/s, corresponds to about $3 \\times 10^{21}$ FLOP per "
 "accelerator and hence to $3 \\times 10^{4}$ to $3 \\times 10^{5}$ H100e per "
 "run. Live estimates bracket the same interval: the first disclosed run above "
 "$10^{26}$ FLOP was Grok 3 in February 2025 at roughly $3 \\times 10^{26}$, the "
 "largest run to date is Grok 4, and Epoch AI places the top frontier model's "
 "crossing of $10^{26}$ around January 2026. We therefore sweep $F_0$ "
 "log-uniformly over $5 \\times 10^{4}$ to $5 \\times 10^{5}$ H100e with a "
 "central value of $1.5 \\times 10^{5}$, and every reported $T_f$ carries that "
 "uncertainty."),

("h1", "4  Data and parameters"),

("h2", "4.1  Failure rates derived from cluster telemetry"),
("p",
 "Grattafiori et al. (2024) report 419 unexpected interruptions over a 54-day "
 "pre-training window on a cluster of up to 16,384 H100 accelerators, resolved "
 "by cause: faulty accelerator 148 (30.1%), accelerator HBM3 memory 72 (17.2%), "
 "network switch or cable 35 (8.4%). Annualising per accelerator,"),
("eq",
 "\\mathrm{AFR} \\;=\\; \\frac{n_{\\mathrm{events}}}{16{,}384}\\times"
 "\\frac{365}{54}", "4"),
("p",
 f"gives {p2(d['AFR_GPU_DIE']*100)}% per year for die failures and "
 f"{p2(d['AFR_HBM']*100)}% for HBM3, hence a **package failure rate of "
 f"{p2(d['AFR_PACKAGE']*100)}% per year** for the two non-field-replaceable "
 f"modes, and {p2(d['AFR_ALL']*100)}% across all interruption causes. As an "
 f"independent check, the all-cause figure corresponds to one interruption per "
 f"{n0(d['xcheck_gpu_hours_per_failure'])} accelerator-hours, against roughly "
 f"{n0(d['epoch_reported'])} reported by Epoch AI on the same underlying run, "
 f"agreement to within 1.4%. We treat the package rate as the central value and "
 f"sweep the full interval in the Monte Carlo. One caution attaches to these "
 "rates: interruption counts do not distinguish terminal hardware death from "
 "transient faults cleared by a reset, so to the extent some die-attributed "
 "interruptions were recoverable, the package rate overstates permanent "
 "attrition. The direction of that bias is benign for our conclusions: a lower "
 "$\\lambda$ lengthens $T_{1/2}$, raises floors and leaves $T_f$ nearly "
 "unchanged."),

("h2", "4.2  Installed stock"),
("p",
 "Epoch AI estimates a global delivered stock of approximately 15 million H100e "
 "and publishes ownership-resolved data. For China we derive $C_0$ from a "
 "published relation rather than an assumption: the median estimate of 660,000 "
 "H100e diverted through 2025 is characterised as roughly one third of Chinese "
 f"total capacity, giving $C_0 \\approx$ {n0(d['C0_CHINA'])} H100e. The 90% "
 "interval on the smuggling estimate (290,000-1,600,000) is propagated directly."),
("p",
 "**This is the study's principal data limitation and we state it plainly.** "
 "Epoch resolves ownership by *firm*, not by *jurisdiction*. Attributing a "
 "multinational operator's fleet to a country requires assumptions that are not "
 "fully defensible from public data. We therefore sweep the United States share "
 "over 60-78% and the European Union share over 2-6% of global stock, and we "
 "report European results with correspondingly low confidence. No conclusion in "
 "this paper depends on a point estimate of national stock."),

("h2", "4.3  Severance is modelled symmetrically"),
("p",
 "A jurisdiction is severed from the inputs it does not control. It is worth "
 "stating that this is not a China-specific scenario. The United States has no "
 "domestic source of extreme-ultraviolet lithography, holds only partial and "
 "still-ramping leading-edge fabrication capacity, and has no high-bandwidth "
 "memory production at scale, HBM supply is roughly 90% concentrated in two "
 "Korean firms. American domestic coverage under severance from its own allies "
 "is therefore a scenario band (15-35%), not unity. The European Union, with no "
 "leading-edge logic fabrication in operation, is assigned 1-4%."),

("table", "Model parameters, ranges and sources.", "1",
 ["Symbol", "Parameter", "Central", "Range", "Source"],
 [["$\\lambda$", "Package failure rate (per yr)",
   f"{p2(d['AFR_PACKAGE']*100)}%",
   f"{p2(d['AFR_GPU_DIE']*100)}-{p2(d['AFR_ALL']*100)}%",
   "Derived, Grattafiori et al. (2024)"],
  ["$\\kappa$", "Cannibalisation yield", "0.275", "0.05-0.50",
   "Package architecture (§3.2)"],
  ["$L$", "Useful life (yr)", "4.0", "2.0-6.0",
   "Depreciation dispute, 2025-26"],
  ["$T_{\\mathrm{dbl}}$", "Frontier doubling (mo)", "5.2", "4.8-7.0",
   "Epoch AI, frontier *training* series"],
  ["$F_0$", "Frontier anchor (H100e)", "150,000", "50k-500k",
   "Derived; see §3.3. Swept log-uniform"],
  ["$\\theta$", "Competitiveness threshold", "0.10", "fixed",
   "Convention; enters via the logarithm (§5.3)"],
  ["$\\mathrm{cov}$", "US / EU domestic coverage", "0.25 / 0.02",
   "0.15-0.35 / 0.01-0.04", "**Assumption, no observational basis**"],
  ["$C_0^{\\mathrm{CN}}$", "China stock (H100e)", n0(d['C0_CHINA']),
   "0.87-4.80 M", "Derived, Epoch AI"],
  ["$C_0^{\\mathrm{US}}$", "US stock (H100e)", n0(d['C0_US']),
   "9.0-11.7 M", "Epoch AI, share swept"],
  ["$C_0^{\\mathrm{EU}}$", "EU stock (H100e)", n0(d['C0_EU']),
   "0.3-0.9 M", "Scenario, low confidence"],
  ["$R_{\\mathrm{dom}}$", "China domestic (H100e/mo)",
   n0(d['cn_domestic_pm'] * 0.65), "30-100% of 2025 rate",
   "Epoch AI realised output × stockpile dependence"],
  ["$R_{\\mathrm{leak}}$", "Leakage (H100e/mo)",
   n0(d['leak_pm'] * 0.35), "10-60% of base",
   "Derived, Epoch AI (2026)"]],
 "H100e = H100-equivalents. Ranges are propagated through a 10,000-draw Monte "
 "Carlo with independent uniform sampling. Independence is itself an assumption: "
 "plausible correlations among parameters, between useful life and failure "
 "rate, or between stock and domestic capacity, are not modelled."),

# ══ 5 ════════════════════════════════════════════════════════════════════════
("h1", "5  Results"),

("h2", "5.1  The plausible cannibalisation range straddles the threshold"),
("p",
 f"Under central parameters $\\kappa^{{*}} = {p2(ks['central'])}$. Across the "
 "parameter grid it ranges from 0.13 (die failures only, two-year life) to 1.14 "
 "(all-cause failures, six-year life). The plausible range for accelerators, "
 "$[0.05, 0.50]$, **straddles the central threshold**. Direct measurement of the "
 "integrated model confirms the algebra: against a retirement-only decline of "
 f"{SAT['retirement_only']*100:.2f}% per month, the fleet contracts at "
 f"{SAT['r_zero']*100:.2f}% per month at $\\kappa = 0$ "
 f"({SAT['excess_at_zero_pct']:.0f}% excess), falling to "
 f"{SAT['r_at_kstar']*100:.2f}% at $\\kappa^{{*}}$ "
 f"({SAT['excess_at_kstar_pct']:.0f}% excess), after which tripling $\\kappa$ "
 "changes it by less than 2%. A fleet below the threshold therefore pays a "
 "compounding penalty, and one above it gains nothing from further salvage "
 "capability. Establishing $\\kappa$ empirically is, on this analysis, the "
 "highest-value measurement the field could undertake."),
("p",
 "The threshold interacts with the depreciation dispute in a way worth stating. "
 "Because $\\kappa^{*} = \\lambda L$ rises with useful life, a longer-lived fleet "
 "sits further below any fixed salvage capability: across the disputed "
 f"two-to-six-year range the share of failures salvage can absorb falls from "
 f"{LIFE[0]['failures_absorbed_pct']:.0f}% to "
 f"{LIFE[-1]['failures_absorbed_pct']:.0f}%. We tested, and reject, the tempting "
 "inference that longer-lived fleets are therefore more fragile overall: "
 "time-to-half under zero inflow *rises* from "
 f"{LIFE[0]['t_half_months_zero_inflow']:.0f} to "
 f"{LIFE[-1]['t_half_months_zero_inflow']:.0f} months across the same range, "
 "because slower retirement dominates. The defensible statement is narrower, a "
 "six-year fleet survives longer in absolute terms while depending more on raw "
 "stock and less on repair. We report the rejected hypothesis because it is "
 "attractive, quotable and false."),
("fig", os.path.join(FIG, "fig7_kappa_critical.png"),
 "The critical cannibalisation ratio $\\kappa^{*} = \\lambda L$ as a function of "
 "useful life, for three failure-rate assumptions. The shaded band is the "
 "plausible range for AI accelerators given that high-bandwidth memory is "
 "co-packaged and non-field-replaceable. The band intersects all three curves: "
 "whether salvage sustains an installed base is regime-dependent, not a matter "
 "of degree.", "1"),

("h2", "5.2  Trajectories and reported quantities"),
("p",
 "Table 2 reports medians and 90% intervals from 10,000 draws per jurisdiction. "
 "Frontier exit occurs between "
 f"{mo(EU['t_frontier_med'])} and {mo(US['t_frontier_med'])} months, ordered by "
 "installed stock as the analytic relation in §5.3 requires. At the median no "
 "jurisdiction reaches self-sufficiency, but the floors must be read with double "
 "care, for the United States and European Union they are the assumed "
 "domestic-coverage parameter rescaled by a bounded factor, not independent "
 f"model output (§7.2), while China's 90% interval reaches "
 f"{p1(CN['floor_p95'])}%, above parity. Median sovereign floors are "
 f"{p1(US['floor_med'])}% for the United States, {p1(CN['floor_med'])}% for "
 f"China and {p1(EU['floor_med'])}% for the European Union."),

("table", "Reported quantities by jurisdiction. Medians with 90% intervals, "
          "10,000 Monte Carlo draws.", "2",
 ["Jurisdiction", "$C_0$ (M H100e)", "$T_{1/2}$ (mo)", "$T_f$ (mo)",
  "$C_\\infty$ (% of $C_0$)", "$P(T_{1/2}\\!\\leq\\!36)$"],
 [["China", f"{CN['C0_h100e']/1e6:.2f}",
   f"{mo(CN['t_half_med'])} [{mo(CN['t_half_p05'])}-{mo(CN['t_half_p95'])}]",
   f"{mo(CN['t_frontier_med'])} [{mo(CN['t_frontier_p05'])}-{mo(CN['t_frontier_p95'])}]",
   f"{p1(CN['floor_med'])} [{p1(CN['floor_p05'])}-{p1(CN['floor_p95'])}]",
   f"{p1(CN['p_half_within_36m'])}%"],
  ["United States", f"{US['C0_h100e']/1e6:.2f}",
   f"{mo(US['t_half_med'])} [{mo(US['t_half_p05'])}-{mo(US['t_half_p95'])}]",
   f"{mo(US['t_frontier_med'])} [{mo(US['t_frontier_p05'])}-{mo(US['t_frontier_p95'])}]",
   f"{p1(US['floor_med'])} [{p1(US['floor_p05'])}-{p1(US['floor_p95'])}]",
   f"{p1(US['p_half_within_36m'])}%"],
  ["European Union", f"{EU['C0_h100e']/1e6:.2f}",
   f"{mo(EU['t_half_med'])} [{mo(EU['t_half_p05'])}-{mo(EU['t_half_p95'])}]",
   f"{mo(EU['t_frontier_med'])} [{mo(EU['t_frontier_p05'])}-{mo(EU['t_frontier_p95'])}]",
   f"{p1(EU['floor_med'])} [{p1(EU['floor_p05'])}-{p1(EU['floor_p95'])}]",
   f"{p1(EU['p_half_within_36m'])}%"]],
 f"$T_{{1/2}}$ is right-censored at 120 months. Censored draws are retained "
 f"ordinally, so any quantile falling in the censored mass is reported as "
 f"'>120' rather than as a finite value; censoring affects "
 f"{p1(CN['t_half_censored_pct'])}% of Chinese draws and "
 f"{p1(US['t_half_censored_pct'])}% of US draws. European figures carry low "
 f"confidence because jurisdiction-resolved stock data are weakest (§4.2)."),

("fig", os.path.join(FIG, "fig1_decay_by_jurisdiction.png"),
 "Central-case decay of effective compute after severance. The European "
 "trajectory falls fastest despite the smallest absolute exposure, because "
 "domestic replacement covers the least of its attrition.", "2"),

("fig", os.path.join(FIG, "fig2_montecarlo_china.png"),
 "Monte Carlo distribution for China, 10,000 draws with independent uniform "
 "sampling over all parameters in Table 1. The width of the 90% interval "
 "reflects the joint sweep of all parameters; because China's inflows are "
 "absolute rather than proportional to stock, uncertainty in $C_0$ contributes "
 "as well.", "3"),

("h2", "5.3  The frontier clock dominates hardware attrition"),
("p",
 "The consequential result is not the decay of hardware but its small share of "
 "the interval. Figure 4 plots capability against the contemporaneous frontier "
 "scale. Setting decay aside entirely, the exit time follows"),
("eq", r"T_f \simeq T_{\mathrm{dbl}}\,\log_2\left(\frac{C_0}{\theta F_0}\right)", "5"),
("p",
 "which reproduces the simulated central cases to within four months (analytic "
 "36.6 / 49.1 / 27.7 against simulated 36 / 45 / 24 for China, the United States "
 "and the European Union). Two consequences follow, and they replace the "
 "stock-invariance claim made in an earlier draft."),
("bullets", [
 "**Installed stock buys time only logarithmically.** At "
 "$T_{\\mathrm{dbl}} = 5.2$ months, a tenfold larger fleet buys "
 "$T_{\\mathrm{dbl}}\\log_2 10 \\approx 17$ further months, and a hundredfold "
 "fleet only 35. Stockpiling is subject to sharply diminishing returns against a "
 "moving frontier, a stronger and more useful statement than the invariance "
 "claim it replaces, and unlike that claim it is not an artefact of "
 "normalisation.",
 "**Hardware decay accounts for a consistent minority of the interval.** "
 "Re-running each central case with failure and retirement set to zero gives 42 "
 "/ 52 / 28 months against 36 / 45 / 24 with decay: attrition costs 6 / 7 / 4 "
 "months, or **13-14% of the budget** in all three jurisdictions. The remaining "
 "86% is the frontier clock.",
]),
("p",
 "The corrected reading is therefore narrower than the original but survives "
 "scrutiny: hardware reliability is not what governs strategic position under "
 "severance, but neither is position independent of how much hardware a "
 "jurisdiction holds."),
("fig", os.path.join(FIG, "fig3_frontier_relative.png"),
 "Capability against an absolute frontier anchor, logarithmic scale. Starting "
 "positions differ because installed stocks differ; the near-parallel decline "
 "reflects the common frontier deflator. Crossing times are ordered by stock and "
 "separated by roughly $T_{\\mathrm{dbl}}\\log_2$ of the stock ratio.", "4"),
("p",
 "Sensitivity analysis confirms the mechanism. Varying the frontier doubling "
 f"time across its 4.8-7.0 month range moves $T_f$ by {SENS[0]['span']:.0f} "
 "months; varying the failure rate across its full derived interval moves it by "
 f"{[s for s in SENS if 'Failure' in s['parameter']][0]['span']:.0f} months, a "
 "sevenfold difference in leverage. Hardware reliability, the quantity the "
 "engineering literature measures most carefully, is among the *least* important "
 "parameters for the strategic outcome. This is the one place where the "
 "correction to $T_{\\mathrm{dbl}}$ strengthened rather than weakened a claim."),
("fig", os.path.join(FIG, "fig4_sensitivity_tornado.png"),
 "One-at-a-time sensitivity of frontier exit time, ordered by span. The rate of "
 "frontier advance dominates; cannibalisation yield and failure rate matter "
 "least once the regime is fixed.", "5"),

("p",
 "The threshold $\\theta = 0.10$ is a convention, and its influence is fully "
 "transparent: it enters Eq. 5 only through the logarithm, so halving it "
 "lengthens every $T_f$ by exactly one doubling time, about five months, and "
 "doubling it shortens every $T_f$ by the same amount, leaving ordering and "
 "spreads untouched. Verified numerically: 42 / 36 / 31 months for "
 "$\\theta$ = 0.05 / 0.10 / 0.20 in the China central case."),

("h2", "5.4  Regime dependence"),
("p",
 "Figure 6 shows trajectories across cannibalisation regimes. Values of $\\kappa$ "
 f"above $\\kappa^{{*}} = {p2(ks['central'])}$, including the aviation value of "
 "10, a hypothetical field-repairable accelerator at 1, and the upper bound of "
 "the plausible accelerator range at 0.5, are indistinguishable, because all "
 "three are past saturation and the failure flow is already fully absorbed. Only "
 "the lower bound, 0.05, sits far enough below the threshold to add materially to "
 "the decline. The system does not respond smoothly to $\\kappa$: it saturates."),
("fig", os.path.join(FIG, "fig6_kappa_regimes.png"),
 "Decay under four cannibalisation regimes. The three curves at or above the "
 "critical ratio coincide because all are past saturation, the failure flow is "
 "already fully absorbed and additional salvage capability sits idle.", "6"),

("h2", "5.5  Partial severance: what leakage actually buys"),
("p",
 "Real controls are neither complete nor instantaneous. They leak, through "
 "diversion, resale and third-country transhipment, and the size of that leakage "
 "is the quantity enforcement policy actually contests. Sweeping the leakage term "
 "across four orders of magnitude separates two effects that are usually "
 "discussed as one."),
("p",
 "The two horizons respond to leakage with very different elasticities. Across a "
 f"sweep from zero to {LK['max_pct_of_c0_per_yr']:.0f}% of the installed base per "
 f"year, the sovereign floor rises from {LK['floor_at_zero']:.0f}% to "
 f"{LK['floor_at_max']:.0f}% of $C_0$, a factor of "
 f"{LK['floor_at_max']/max(LK['floor_at_zero'],1e-9):.0f}, while frontier exit "
 f"moves only from {LK['tf_at_zero']:.0f} to {LK['tf_at_max']:.0f} months, a "
 f"{100*(LK['tf_at_max']/LK['tf_at_zero']-1):.0f}% change. The asymmetry follows "
 "directly from the analytic form: the floor is an inflow-determined steady "
 "state and scales linearly in inflow, whereas $T_f$ enters through a logarithm "
 "and through a denominator growing exponentially. Reaching a floor of 100% of "
 f"$C_0$ costs about {LK['floor100']['leak_pct_of_C0_per_yr']:.0f}% of the "
 "installed base per year and buys "
 f"{LK['floor100']['t_frontier'] - LK['tf_at_zero']:.0f} additional months at the "
 "frontier."),
("table", "Partial severance. Effect of leakage on the two horizons.", "3",
 ["Leakage regime", "H100e / month", "% of $C_0$ per year", "$T_f$ (mo)",
  "$C_\\infty$ (% of $C_0$)"],
 [["None", "0", "0", f"{LK['tf_at_zero']:.0f}", f"{LK['floor_at_zero']:.0f}"],
  ["Floor held at 100%", f"{LK['floor100']['leak_per_month']:,.0f}",
   f"{LK['floor100']['leak_pct_of_C0_per_yr']:.1f}",
   f"{LK['floor100']['t_frontier']:.0f}", "100"],
  ["Open-market equivalent", ", ", f"{LK['max_pct_of_c0_per_yr']:.0f}",
   f"{LK['tf_at_max']:.0f}", f"{LK['floor_at_max']:.0f}"]],
 "Leakage rates are expressed relative to the historically estimated diversion "
 "flow. The floor is highly elastic to leakage; the frontier horizon is not."),
("fig", os.path.join(FIG, "fig8_leakage.png"),
 "Leakage lifts the sovereign floor steeply while moving the frontier horizon "
 "very little. The two curves diverge because the floor is an inflow-determined "
 "steady state, whereas frontier exit is governed by the frontier's own growth "
 "rate.", "7"),
("p",
 "**Leakage buys capacity, not competitiveness.** For enforcement design this "
 "inverts the usual emphasis. Interdiction is comparatively effective at "
 "protecting a frontier lead, because that lead is set by the frontier's growth "
 "rate and by a logarithm of the adversary's stock, both of which resist "
 "additional inflow. It is close to powerless at preventing an adversary from "
 "maintaining a substantial sustained capacity, because the floor responds to "
 "inflow linearly and the required inflow is modest. A control regime justified "
 "on the first ground and evaluated on the second will appear to be failing when "
 "it is not, and the reverse."),

# ══ 6 ════════════════════════════════════════════════════════════════════════
("h1", "6  The aviation comparison, and why calibration fails"),

("p",
 "A severance model invites the objection that it is unfalsifiable, since no "
 "jurisdiction has yet been fully severed from AI compute. The natural response "
 "is to calibrate against the nearest observed case. Russian civil aviation after "
 "February 2022 is the only documented severance of a complex, "
 "spare-parts-dependent capital fleet with a multi-year observation window: a "
 "starting fleet of roughly 1,500-1,800 Western-built aircraft, more than a "
 "third reported cannibalised by October 2025, a projected reduction exceeding "
 "50% by 2026, and a documented practice of dismantling approximately one "
 "airframe to keep ten flying."),
("p",
 "**We attempted this calibration and it fails.** Fitting the model's hazard as "
 "a single free parameter with $\\kappa = 10$ fixed from observed practice, the "
 f"best attainable fit reaches a root-mean-square error of {av['rmse']:.3f} and "
 f"leaves {av['unexplained_decline_share']*100:.0f} percentage points of the "
 "observed decline unexplained at month 47, with the fitted hazard pinned "
 "against the top of the search grid."),
("fig", os.path.join(FIG, "fig5_aviation_comparison.png"),
 "Observed Russian civil fleet against the best attainable parts-attrition-only "
 "fit. The shaded residual is the share of decline that parts attrition cannot "
 "account for. It is not model error: it corresponds to mechanisms with no "
 "compute analogue.", "8"),
("p",
 "The residual is informative rather than embarrassing. Two mechanisms drive a "
 "large part of the observed decline and have no counterpart in compute: "
 "repossession of foreign-owned airframes by lessors, which is a one-off stock "
 "shock rather than attrition, and withdrawal of airworthiness certification by "
 "regulators, which removes serviceable aircraft for legal rather than physical "
 "reasons. Accelerators are owned outright and no regulator grounds a degraded "
 "cluster. Attributing the entire Russian decline to parts attrition would "
 "overstate the hazard by roughly an order of magnitude."),
("p",
 "We therefore use aviation to bound $\\kappa$ and to establish that "
 "cannibalisation is a real, observed, quantified mechanism, not to calibrate "
 "the compute model. Reporting this negative result matters for two reasons. It "
 "prevents a spuriously precise calibration from propagating into the "
 "literature, and it identifies exactly what an adequate empirical test would "
 "require: telemetry from a fleet under genuine resupply constraint, which does "
 "not yet exist in public form."),
("p",
 "One qualitative finding does transfer. Reported incident frequency in the "
 "Russian fleet more than doubled relative to 2019 well before fleet counts "
 "halved. Degradation appears as declining reliability before it appears as "
 "declining inventory. If the same holds for compute, effective capacity falls "
 "faster than node counts suggest, and our estimates are conservative."),

# ══ 7 ════════════════════════════════════════════════════════════════════════
("h1", "7  Discussion"),

("h2", "7.1  What severance actually buys"),
("p",
 "The results support a reframing of the export-control debate. The relevant "
 "quantity is not how much compute an adversary loses but how long it takes them "
 "to fall off a moving frontier, and on our estimates that interval is roughly "
 "two years and is remarkably insensitive to the size of the installed base. "
 "Controls do not need to destroy capacity. They need only hold it constant "
 "while the frontier advances. Conversely, a jurisdiction that has secured a "
 "large stock of accelerators has bought less strategic time than the stock's "
 "size implies, because the binding constraint is the frontier's growth rate "
 "rather than its own hardware."),
("p",
 "This has a symmetrical and less comfortable implication. If frontier advance "
 "slows, through scaling limits, energy constraints or capital withdrawal, the "
 "value of controls decays with it. Export controls are, on this reading, a bet "
 "on continued exponential progress. They are most effective precisely when "
 "they are least needed to establish dominance, and least effective when "
 "progress stalls and installed stocks retain their relative worth."),

("h2", "7.2  Sovereignty has a number, and it is low everywhere"),
("p",
 "The sovereign floor makes explicit something the indexing literature has "
 "gestured at without quantifying, but it must be read with a caveat we state "
 "before the result rather than after it. Appendix A shows that where domestic "
 "output is parameterised as a coverage fraction of installed stock, as it is "
 "for the United States and European Union, the floor collapses to "
 "$\\mathrm{cov}\\,(1 + \\min(\\kappa, \\kappa^{*}))$, independent of $C_0$, "
 f"$\\lambda$ and $L$. The US figure of {p1(US['floor_med'])}% is therefore the "
 "assumed 15-35% coverage band rescaled by a factor bounded between 1.0 and 1.5, "
 "not an independent finding. We report it as a **scenario mapping**: coverage "
 "of 0.15 / 0.25 / 0.35 implies a floor of 19 / 32 / 45%, and readers who "
 "dispute the coverage assumption can substitute their own. China's floor "
 f"({p1(CN['floor_med'])}%) is different in kind, it derives from an absolute "
 "inflow estimate rather than a coverage fraction, and is the only one of the "
 "three that is a model output in the ordinary sense. Its interval must then be "
 f"taken seriously: the 90% band runs from {p1(CN['floor_p05'])}% to "
 f"{p1(CN['floor_p95'])}% of the installed base, crossing parity at the top. The "
 "upper end is driven jointly by the stockpile-dependence parameter, whether "
 "Huawei's realised 2025 output could be sustained without the pre-control TSMC "
 "die stockpile, and by the wide uncertainty on $C_0$ itself. The model "
 "therefore does not license the claim that China cannot sustain its base "
 "domestically. It licenses agnosticism, and it identifies the measurement that "
 "would resolve the question, the stockpile-dependence share, as the second "
 "most valuable empirical target after $\\kappa$."),
("p",
 "With that qualification the qualitative point stands, and it does not depend "
 "on the disputed parameter. Lithography is Dutch, leading-edge fabrication is "
 "Taiwanese, and high-bandwidth memory is roughly 90% Korean. No participant in "
 "this system is severable from it without cost, and the rhetorical framing in "
 "which sovereignty is a property one side possesses and the other lacks is not "
 "supported by any coverage assumption we consider plausible."),

("h2", "7.3  Testable predictions"),
("p",
 "The model is falsifiable, and it is worth being specific about how, because a "
 "severance model that cannot be checked is an essay. Four predictions follow "
 "directly, each with the observation that would refute it."),
("bullets", [
 "**Reliability degrades before inventory does.** In any compute fleet operating "
 "under a genuine resupply constraint, the rate of unrecovered job failures should "
 "rise measurably before the operational node count falls appreciably. Refuted by "
 "observing node counts falling in proportion to, or ahead of, failure rates.",
 "**Salvage effort shows a saturation point, not a gradient.** Operators who "
 "increase cannibalisation capability beyond the threshold should see no further "
 "improvement in fleet availability. Refuted by a smooth, unsaturating "
 "relationship between salvage effort and availability.",
 "**Frontier exit scales logarithmically with stock.** Across jurisdictions, "
 "$T_f$ should rise by about $T_{\\mathrm{dbl}}\\log_2(10) \\approx 17$ months "
 "per tenfold increase in installed compute, not proportionally. Refuted by a "
 "linear or near-linear relationship. (An earlier draft offered the opposite "
 "prediction, that position *decouples* from stock, which under the "
 "then-implemented metric was unfalsifiable by construction. Its replacement is "
 "a genuine prediction with a defined refutation.)",
 "**Diversion moves the floor, not the frontier.** Periods of increased diversion "
 "should raise a jurisdiction's sustained compute capacity substantially while "
 "leaving its largest training runs roughly where the frontier clock puts them. "
 "Refuted by frontier-scale runs tracking diversion volumes.",
]),
("p",
 "The first is the most immediately checkable: it requires only that one operator "
 "under constraint publish job-failure telemetry alongside node counts. No such "
 "series is public today, which is why §6 reports a failed calibration rather "
 "than a successful one."),

("h2", "7.4  Limitations"),
("bullets", [
 "**Jurisdictional attribution.** The best public stock data resolve ownership "
 "by firm, not country. We sweep shares rather than assert them, but no "
 "treatment fully removes this weakness. European results in particular should "
 "be read as scenario illustration.",
 "**$\\kappa$ is not measured.** The cannibalisation yield is bounded by "
 "architectural reasoning, not observation, and the plausible range straddles "
 "the critical threshold. This is the single most consequential open parameter.",
 "**Utilisation is held constant.** Energy and grid constraints are represented "
 "by a fixed ceiling. Several recent analyses argue power rather than silicon is "
 "now binding in some jurisdictions; endogenising $u(t)$ would likely shorten "
 "the horizons reported here.",
 "**Severance is modelled as complete and instantaneous.** Real controls are "
 "partial, phased and leak. The leakage term captures some of this; tiered or "
 "escalating regimes are not modelled.",
 "**The frontier is exogenous.** We treat frontier growth as an external "
 "exponential. In reality a severed jurisdiction's exit from the frontier alters "
 "competitive dynamics and hence the frontier's own trajectory.",
 "**No empirical severance case exists for compute.** The model is falsifiable "
 "in principle, it predicts specific degradation trajectories, but cannot yet "
 "be tested against observation, as §6 establishes.",
 "**Retirement is an economic choice that the model treats as physics.** The "
 "useful life $L$ encodes withdrawal at book life, but an operator under "
 "severance would plausibly run hardware to failure instead. Re-running the "
 "central cases with $L$ set to forty years raises $T_f$ by only three to four "
 "months, lengthens every $T_{1/2}$, and lifts floors substantially: the United "
 "States coverage scenario from 32% to 92% of $C_0$, China from 86% to 246%. "
 "Run-to-failure therefore strengthens the sovereignty findings and barely moves "
 "the frontier clock, which is why the conservative retirement case is the one "
 "reported in the main results.",
 "**$T_f$ measures compute position, not capability position.** Algorithmic "
 "efficiency in language models has historically halved the compute needed for "
 "fixed performance roughly every eight months (Ho et al., 2024). To the extent "
 "such advances are public, both sides gain them and the relative ordering is "
 "preserved, but a frozen fleet keeps gaining absolute capability, so crossing "
 "$\\theta$ is softer in capability terms than in FLOP terms. To the extent "
 "frontier advances stay proprietary, the severed side degrades faster than "
 "$T_f$ suggests. The measure is exact about hardware and deliberately agnostic "
 "about software.",
 "**Remote access is outside the model by construction.** $N(t)$ counts "
 "accelerators physically installed and operated within the jurisdiction. "
 "Compute rented from foreign-hosted providers is not in $N(t)$, and, unlike "
 "the leakage term, whose units enter the fleet and thereafter decay at "
 "$\\lambda$ and $\\delta$, leased capacity is replenished by the lessor and "
 "does not decay at all. Every horizon reported here is therefore conditional on "
 "hardware severance *and* effective interdiction of remote access; against "
 "hardware-only severance they are upper bounds on the effect. One consolation "
 "follows analytically: because the frontier deflator is exponential, a fixed "
 "lease of any size only shifts $T_f$ by $T_{\\mathrm{dbl}}\\log_2(1 + A/C_0)$. "
 "Leased capacity defeats the mechanism only if it compounds at the frontier "
 "rate itself, $g^{*} = \\ln 2 / T_{\\mathrm{dbl}} \\approx 13\\%$ per month.",
 "**Domestic output is frozen at its severance-date rate.** The model contains "
 "no induced-substitution channel, so $C_\\infty$ is defined conditional on zero "
 "indigenisation growth; for any positive growth rate there is no asymptote at "
 "all. This assumption is contradicted by the most recent observed trend in the "
 "series the parameter is calibrated from, reported Chinese accelerator output "
 "targets roughly doubled between 2025 and 2026, though under the paper's own "
 "complete-severance premise, with Korean memory and Dutch lithography both "
 "withdrawn, the growth rate could plausibly take either sign. $T_f$ is robust "
 "to this: it moves by only a few months across growth rates from $-30\\%$ to "
 "$+60\\%$ per year, because no plausible indigenisation rate competes with a "
 "frontier that doubles every 5.2 months.",
]),

# ══ 8 ════════════════════════════════════════════════════════════════════════
("h1", "8  Conclusion"),
("p",
 "National AI capacity has been measured as a stock at least eleven times and "
 "modelled as a flow not once. We have argued that the flow is the "
 "policy-relevant quantity, built a decay model of installed accelerator fleets "
 "under severance, parameterised it from published telemetry rather than "
 "assumption, and reported three quantities intended to be reused: the compute "
 "half-life, the frontier exit time, and the sovereign floor."),
("p",
 "Four findings stand out. Salvage absorbs the failure flow only up to a "
 f"saturation ratio $\\kappa^{{*}} = \\lambda L \\approx {p2(ks['central'])}$, and "
 "because high-bandwidth memory is co-packaged with the die the plausible range "
 "for accelerators straddles that threshold, making $\\kappa$ the field's most "
 "valuable unmeasured parameter. Frontier exit occurs at two to four years and "
 "rises only logarithmically with installed stock: a tenfold larger fleet buys "
 "roughly seventeen further months, and hardware decay accounts for just 13-14% "
 "of the interval, the frontier clock for the rest. At the median no major "
 "jurisdiction appears self-sufficient, though for the United States and "
 "European Union that number is a coverage assumption rescaled rather than an "
 "independent result, and China's interval is wide enough to cross parity, "
 "leaving the sovereignty question there genuinely open. And leakage, when "
 "partial, buys "
 "capacity rather than competitiveness: it lifts the sovereign floor steeply "
 "while leaving the frontier horizon almost where it was."),
("p",
 "The claim that export controls buy time is, on this analysis, correct in form "
 "and materially wrong in the mechanism usually assumed. What is bought is not "
 "the degradation of an adversary's hardware but the freezing of its position "
 "against a frontier that keeps moving. That is a different policy instrument "
 "with a different expiry date, and it should be argued for on those terms."),

# ══ Appendices ═══════════════════════════════════════════════════════════════
("h1", "Appendix A  Derivation of the critical ratio"),
("p",
 "Let $P_t$ be the salvage pool. Over one period the pool gains $\\kappa$ "
 "repairs for every unit leaving service, unrepaired failures $(F_t-\\rho_t)$ "
 "and retirements $\\mathrm{Ret}_t$, and loses $\\rho_t$ to repairs performed. "
 "Consider the steady state in which every failure is repaired, so "
 "$\\rho_t = F_t = N\\lambda$ and $\\mathrm{Ret}_t = N\\delta$. The pool balance is"),
("eq",
 "\\Delta P \\;=\\; \\kappa N\\delta \\;-\\; N\\lambda", "A.1"),
("p",
 "which is non-negative precisely when $\\kappa \\geq \\lambda/\\delta$. Writing "
 "$\\delta = 1/L$ gives $\\kappa^{*} = \\lambda L$. Fleet size $N$ cancels, so "
 "the threshold is scale-free; inflow $R$ does not appear, so it is also "
 "policy-independent. Below $\\kappa^{*}$ the pool is exhausted in finite time "
 "and unrepaired failures accumulate; above it the pool grows without bound and "
 "the repair constraint ceases to bind, which is why trajectories for "
 "$\\kappa = 0.5$, $1$ and $10$ coincide in Figure 6."),
("p",
 "Note carefully what this does *not* establish. Equation A.1 governs the repair "
 "constraint alone. Retirement removes units from service whether or not failures "
 "are repaired, so $N$ declines above the threshold as well, at rate $\\delta$, "
 "rather than at $\\delta$ plus an unabsorbed-failure term. An earlier draft of "
 "this paper stated that the installed base *persists* above $\\kappa^{*}$; direct "
 "simulation refutes that, and the corrected reading, a saturation threshold "
 "separating failure-limited from obsolescence-limited decay, is the one "
 "verified numerically in §5.1."),

("h2", "A.2  Closed form for the sovereign floor"),
("p",
 "An earlier draft asserted that no closed form existed and reported the floor "
 "from a 900-month integration. One does exist. Setting the pool stationary in "
 "Eq. 2 gives $\\rho = \\kappa(F+\\mathrm{Ret})/(1+\\kappa)$, hence a net "
 "attrition of $(\\lambda+\\delta)N/(1+\\min(\\kappa,\\kappa^{*}))$ and"),
("eq",
 r"\frac{C_\infty}{C_0} = \frac{R_{\mathrm{dom}}+R_{\mathrm{leak}}}"
 r"{C_0\,(\lambda+\delta)}\,\left(1+\min(\kappa,\kappa^{*})\right)",
 "A.2"),
("p",
 "which reproduces the integrated values exactly. The consequence must be stated "
 "plainly because it constrains how two of our three floors may be read. Where "
 "domestic output is parameterised as a coverage fraction of installed stock, "
 "$R_{\\mathrm{dom}} = \\mathrm{cov}\\cdot C_0(\\lambda+\\delta)$, which is how "
 "we treat the United States and European Union in the absence of "
 "jurisdiction-resolved production data, this collapses to"),
("eq", r"\frac{C_\infty}{C_0} = \mathrm{cov}\,"
       r"\left(1+\min(\kappa,\lambda L)\right)", "A.3"),
("p",
 "independent of $C_0$, $\\lambda$ and $L$, with the bracket bounded in "
 "$[1.0, 1.5]$ over all parameter values we consider. Those two floors are "
 "therefore a rescaling of an assumption, not an emergent property of the model, "
 "and §7.2 reports them as a scenario mapping. China's floor, which derives from "
 "an absolute inflow estimate rather than a coverage fraction, is not subject to "
 "this collapse."),

("h1", "Appendix B  Reproducibility"),
("p",
 "All results derive from a single deterministic script with a fixed random seed "
 "(20260808). Running it regenerates every figure, table and numerical claim in "
 "this paper, including the values quoted in the abstract. The model is 200 "
 "lines of NumPy with no external solver dependency. Model code, parameter file, "
 "Monte Carlo output and the full source-retrieval log are archived with this "
 "preprint; see *Data and code availability*."),
]

# ─────────────────────────────────────────────────────────────────────────────
BACK = [
("h1", "Data and code availability"),
("p",
 "Model code, parameter definitions with per-value source attribution, Monte "
 "Carlo output, processed tables and all figure-generating code are openly available at "
 "github.com/diShine-digital-agency/The-Half-Life-of-Compute and are "
 "archived with the Zenodo record of this article. Underlying data are third-party and "
 "publicly available: Epoch AI publishes accelerator ownership and sales data "
 "with documented methodology; failure statistics are drawn from published "
 "papers. No proprietary or licensed data were used."),

("h1", "Declarations"),
("p",
 "**Funding.** This research received no external funding. **Competing "
 "interests.** The author is founder of diShine, a consultancy working on AI "
 "adoption and governance, and is the author of a trade book on the geopolitics "
 "of technology cited once in this paper for a framing contribution. Neither "
 "relationship influenced the analysis, which rests entirely on public data and "
 "released code. **AI assistance.** Computational tooling was used for source "
 "retrieval, model implementation and manuscript preparation; all analytical "
 "claims, parameter choices and interpretations are the author's, and every "
 "factual claim was verified against a retrieved primary source."),

("h1", "References"),
("refs", [
 "Beaumier, G., et al. (2023). Cross-Network Weaponization in the Semiconductor "
 "Supply Chain. *International Studies Quarterly*.",

 "Cai, J., Fang, Yin, Yu, Wang, Ho & Hu (2026). Managing technological "
 "sovereignty: a systematic review of semiconductor industry policy and regional "
 "ecosystem governance. *Frontiers in Research Metrics and Analytics*. "
 "doi:10.3389/frma.2026.1762083",

 "Caravella, S., et al. (2023). Technological sovereignty and strategic "
 "dependencies: The case of the photovoltaic supply chain. *Journal of Cleaner "
 "Production*.",

 "Chavez, P., Chilukuri, V. & Scanlon, R. (2026). *Sovereign AI Index*. Center "
 "for a New American Security, April 2026.",

 "Cui, L., et al. (2025). Quantitative analysis of the U.S. chip embargo and "
 "China's export controls on Ga, Ge and graphite. *Computers & Industrial "
 "Engineering*, 7 January 2025. ScienceDirect PII S0360835225000051.",

 "Dobbie, M. J., et al. (2013). Robustness and sensitivity of weighting and "
 "aggregation in constructing composite indices. *Ecological Indicators*.",

 "Epoch AI (2025). *Hardware failures won't limit AI scaling*. "
 "epoch.ai/blog/hardware-failures-wont-limit-ai-scaling",

 "Epoch AI (2026). *Data on AI Chip Owners* and *Data on AI Chip Sales*, with "
 "published methodology. epoch.ai/data",

 "Epoch AI (2026). *Data on AI Models*: frontier training runs, including Grok 3 "
 "at roughly 3e26 FLOP and Grok 4 as the largest disclosed run. "
 "epoch.ai/data/ai-models",

 "Escoda, K. (2026). *GEOPOLITECH*. Volume III of *The Architecture of the New "
 "World: From Code to Matter*., cited for the chokepoint framing only.",

 "Farrell, H. & Newman, A. L. (2019). Weaponized Interdependence: How Global "
 "Economic Networks Shape State Coercion. *International Security*, 44(1), "
 "42-79. doi:10.1162/isec_a_00351",

 "Fuller, D. B. (2026). Technology and Economic Statecraft: Weaponizing "
 "Technology Export Controls in an Era of Globalized Production. *SSRN "
 "Electronic Journal*.",

 "Grattafiori, A., et al. (2024). The Llama 3 Herd of Models. "
 "arXiv:2407.21783.",

 "Greco, S., Ishizaka, A., Tasiou, M. & Torrisi, G. (2019). On the "
 "Methodological Framework of Composite Indices: A Review of the Issues of "
 "Weighting, Aggregation, and Robustness. *Social Indicators Research*, "
 "141(1), 61-94. doi:10.1007/s11205-017-1832-9",

 "Ho, A., Besiroglu, T., Erdil, E., Owen, D., Rahman, R., Guo, Z. C., "
 "Atkinson, D., Thompson, N. & Sevilla, J. (2024). Algorithmic Progress in "
 "Language Models. arXiv:2403.05812.",

 "Juniewicz, I. (2026). *Diversion and resale: estimating compute smuggling to "
 "China*. Epoch AI, 29 April 2026.",

 "Kelemen, A., et al. (2024). A sensitivity analysis of composite indicators: "
 "Min/max thresholds. *Environmental and Sustainability Indicators*.",

 "Kokolis, A., Kuchnik, M., Hoffman, J., Kumar, A., Malani, P., Ma, F., DeVito, "
 "Z., Sengupta, S., Saladi, K. & Wu, C.-J. (2025). Revisiting Reliability in "
 "Large-Scale Machine Learning Research Clusters. *IEEE HPCA 2025*. "
 "arXiv:2410.21680.",

 "Leavy, E. (2026). *Machinepower Index 2026*, Q3 2026 edition. "
 "machinepowerindex.org",

 "Lee, J.-D., Choi, S., Kim, K. & Si, S. (2024). *Empirical Measurement of "
 "Technology Sovereignty*. IFS Working Paper 2024-01, Institute for Future "
 "Strategy, Seoul National University. SSRN 5145685.",

 "Meng, W. (2025). Modeling the Path of Structural Strategic Deterrence: A Sand "
 "Table Simulation Based on Rare Earth Supply Disconnection. arXiv:2505.21579.",

 "Nardo, M., Saisana, M., Saltelli, A. & Tarantola, S. (2008). *Handbook on "
 "Constructing Composite Indicators: Methodology and User Guide*. OECD / "
 "European Commission JRC. JRC47008. ISBN 978-92-64-04346-6.",

 "Park, D.-J. & Liu, S. (2023). A Study on the Economic Effects of U.S. Export "
 "Controls on Semiconductors to China. *Korea International Trade Research "
 "Institute*. SSRN 4391187.",

 "Sherbrooke, C. C. (1968). METRIC: A Multi-Echelon Technique for Recoverable "
 "Item Control. *Operations Research*, 16(1), 122-141. doi:10.1287/opre.16.1.122. "
 "Earlier as RAND RM-5078.",

 "Sastry, G., Heim, L., Belfield, H., Anderljung, M., Brundage, M., Hazell, J., "
 "O'Keefe, C., Hadfield, G. K., Ngo, R., Pilz, K., Gor, G., Bluemke, E., Shoker, "
 "S., Egan, J., Trager, R. F., Avin, S., Weller, A., Bengio, Y. & Coyle, D. "
 "(2024). Computing Power and the Governance of Artificial Intelligence. "
 "arXiv:2402.08797.",

 "Shrivastava, M., et al. (2025). China's semiconductor conundrum: understanding "
 "US export controls and their efficacy. *Cogent Social Sciences*. "
 "doi:10.1080/23311886.2025.2528450",

 "Yew, R.-J., Creasey, K. E., Curtis, T. L. & Venkatasubramanian, S. (2026). The "
 "Commodification of AI Sovereignty: Lessons from the Fight for Sovereign Oil. "
 "arXiv:2601.11763.",
]),
]

ALL = BODY + BACK
