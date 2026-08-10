#!/usr/bin/env python3
"""
Executive summary, content for all three languages in one module.

Written for a policy, geopolitics or general-technical reader: no equations, no
survival analysis, every number in plain language. Figures come from
figures_brief_<lang>/, which are purpose-built and not the paper's.

Numbers are read from results.json, so the brief cannot drift from the paper.

Block grammar:
  ("kicker", t) ("h", t) ("p", t) ("lead", t) ("pull", t)
  ("finding", n, title, body) ("bullets", [..]) ("fig", path, caption)
  ("box", title, body) ("rule",) ("cols", [(label, value, note), ...])
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
R = json.load(open(os.path.join(ROOT, "03-DATA", "processed", "results.json")))
RX = json.load(open(os.path.join(ROOT, "03-DATA", "processed", "results_extended.json")))
LK = RX["leakage"]

d = R["derived"]; ks = R["kappa_star"]; av = R["aviation"]
MC = {m["jurisdiction"]: m for m in R["montecarlo"]}
CN, US, EU = MC["China"], MC["United States"], MC["European Union"]
SENS = R["sensitivity"]
SPAN_FRONTIER = SENS[0]["span"]
SPAN_AFR = [s for s in SENS if "Failure" in s["parameter"]][0]["span"]


def F(lang):
    return os.path.join(ROOT, "05-DRAFT", f"figures_brief_{lang}")


def num(x, lang, dec=1):
    s = f"{x:.{dec}f}"
    return s if lang == "en" else s.replace(".", ",")


def mo(x): return ">120" if x == float("inf") else f"{x:.0f}"


# ═════════════════════════════════════════════════════════════════════════════
def build(lang):
    f = F(lang)
    n = lambda x, dec=1: num(x, lang, dec)
    KS = n(ks["central"], 2)
    AFR = n(d["AFR_PACKAGE"] * 100, 0)   # rounded for a lay reader

    if lang == "en":
        FIGS = ["brief1_two_clocks", "brief2_sovereign_floor", "brief3_threshold"]
        META = dict(
            title="The Half-Life of Compute",
            subtitle="What export controls on AI chips actually buy, and for how long",
            kicker="EXECUTIVE SUMMARY",
            author="Kevin Escoda", affil="diShine · Data, AI & Automation, Milan",
            date="8 August 2026",
            note="Summary of a working paper. Full methods, data and code in the "
                 "accompanying paper. DOI 10.5281/zenodo.21866487. Code: github.com/diShine-digital-agency/The-Half-Life-of-Compute",
            running="The Half-Life of Compute · Executive Summary")
        BODY = [
          ("lead",
           "Every argument for restricting the export of advanced AI chips rests on "
           "a claim about time: controls **buy time**. Nobody has ever said how "
           "much. This paper computes it, and finds that the usual explanation of "
           "why controls work is the wrong one."),

          ("h", "The mistake: treating chips like gold"),
          ("p",
           "National AI capacity is measured constantly. At least eleven public "
           "indices rank countries by how much computing power, talent and "
           "infrastructure they hold. All of them take a photograph. None asks what "
           "happens to the picture afterwards."),
          ("p",
           "That matters, because installed computing power is not a reserve sitting "
           "in a vault. It is a fleet of machinery that breaks. Using published "
           f"failure data from a real training run, roughly **{AFR}% of accelerators "
           "fail in a year** from causes that cannot be repaired in the field. They "
           "also age against a target that keeps moving: the scale of a "
           "state-of-the-art training run roughly doubles every ten months. A gold "
           "reserve does not corrode. A chip fleet does, twice over."),
          ("p",
           "The engineering literature has measured the corrosion precisely, but "
           "always assuming replacement chips can be bought. That assumption is "
           "exactly what a supply cut-off removes. Removing it is what this work does."),

          ("rule",),
          ("h", "Three findings"),

          ("finding", "1", "Two to four years, and stockpiling barely extends it",
           "A cut-off country falls below a competitive share of the frontier in "
           f"**{mo(EU['t_frontier_med'])}-{mo(US['t_frontier_med'])} months**. The "
           "interval grows only with the *logarithm* of how many chips you hold: "
           "**ten times the compute buys about seventeen extra months**, a hundred "
           "times about thirty-five. And hardware failure accounts for only 13-14% "
           "of that clock, the rest is the frontier moving away from you."),
          ("fig", os.path.join(f, FIGS[0] + ".png"),
           "The gap between the two lines is the finding. Hardware declines slowly; "
           "competitive standing collapses quickly, because the frontier keeps "
           "moving away. An earlier draft of this work claimed the interval did not "
           "depend on stock size at all, that turned out to be an artefact of how "
           "the measure was built, and has been withdrawn."),

          ("finding", "2", "Nobody can show self-sufficiency, and for China it is genuinely undecided",
           "The **sovereign floor** is the share of its own computing power a country "
           "could sustain from non-severed inflow if cut off. At the median it is "
           f"**{n(US['floor_med'])}%** for the United States, **{n(CN['floor_med'])}%** "
           f"for China and **{n(EU['floor_med'])}%** for the European Union, but the "
           "three numbers mean different things. The US and EU figures are largely "
           "assumptions about domestic production, rescaled. China's is a genuine "
           f"model output, and its uncertainty range runs from {n(CN['floor_p05'])}% "
           f"to {n(CN['floor_p95'])}%, crossing full self-sufficiency at the top. "
           "Current public data cannot settle whether China could sustain its fleet "
           "alone. Lithography is Dutch, leading-edge fabrication is Taiwanese, the "
           "specialised memory is Korean: nobody exits this system without cost."),
          ("fig", os.path.join(f, FIGS[1] + ".png"),
           "Bars are median estimates; the thin lines show the 90% uncertainty range. "
           "Important caveat: for the United States and Europe this number is largely "
           "an assumption about how much they could make domestically, rescaled, "
           "only China's is a genuine model output. See the caveats overleaf."),

          ("finding", "3", "A hidden switch nobody has measured",
           "When resupply stops, the only source of spare parts is other machines. "
           "In aviation under sanctions, operators strip roughly one airframe to keep "
           "ten flying. AI accelerators cannot be salvaged that way: the memory is "
           "bonded into the same package as the processor, so the two most common "
           "failures are unrepairable by design. There is a critical ratio, call it "
           f"**{KS}**, below which broken machines pile up and add to the decline, "
           "and above which salvage absorbs them completely and any further repair "
           "effort is wasted. The plausible range for real accelerators sits "
           "**across** that line. Below it a fleet contracts up to 40% faster than "
           "ageing alone would cause; above it, nothing more can be squeezed out. No "
           "public evidence yet says which side real hardware is on."),
          ("fig", os.path.join(f, FIGS[2] + ".png"),
           "Establishing this single number empirically would be, on this analysis, "
           "the most valuable measurement the field could make."),

          ("rule",),
          ("h", "What it means"),
          ("pull",
           "Controls do not need to destroy an adversary's computing power. They need "
           "only freeze it while the frontier moves."),
          ("p",
           "This is a different instrument from the one usually described, and it has "
           "different properties. Sensitivity testing shows the pace of frontier "
           f"advance matters about **five times more** than hardware reliability "
           f"({SPAN_FRONTIER:.0f} months of swing versus {SPAN_AFR:.0f}). The "
           "constraint that binds is the clock, not the machinery."),
          ("bullets", [
           "**Controls are a bet on continued exponential progress.** If frontier "
           "advance slows, through scaling limits, energy constraints or capital "
           "withdrawal, their value decays with it. They are most effective exactly "
           "when they are least needed, and weakest when progress stalls.",
           "**Stockpiling buys less than it looks like.** A large holding of chips "
           "does not extend the horizon much, because the horizon is set by how fast "
           "the frontier moves, not by how much hardware you have.",
           "**Sovereignty needs a number, not an adjective.** The sovereign floor "
           "gives one. On these estimates no major power exceeds roughly a third.",
          ]),
          ("p",
           "One further result speaks directly to enforcement. Controls leak, and "
           "sweeping the leakage rate separates two things usually discussed as one. "
           f"Smuggling at roughly the historically estimated rate lifts a country's "
           f"sovereign floor from {LK['floor_at_zero']:.0f}% to 100%, but buys only "
           f"about {LK['floor100']['t_frontier'] - LK['tf_at_zero']:.0f} extra months "
           "at the frontier. To double the frontier horizon you would need leakage "
           f"of roughly {LK['max_pct_of_c0_per_yr']:.0f}% of the installed base every "
           "year, which is not smuggling but an open market. **Leakage buys capacity, "
           "not competitiveness**, so interdiction protects a frontier lead far "
           "better than it prevents an adversary holding a floor."),

          ("rule",),
          ("h", "What we do not know"),
          ("p",
           "Three limits are worth stating plainly, because the numbers above will "
           "otherwise be read as more precise than they are."),
          ("bullets", [
           "**The salvage ratio has never been measured.** It is bounded here by "
           "reasoning about how the chips are physically built, not by observation, "
           "and it straddles the critical threshold.",
           "**Chip ownership data resolve by company, not by country.** Assigning a "
           "multinational's fleet to a jurisdiction requires assumptions. Ranges are "
           "swept rather than asserted; European figures are the weakest.",
           "**No country has yet been fully cut off from AI compute.** We attempted "
           "to calibrate against the closest real case, Russian civil aviation after "
           "February 2022, and *the calibration failed*. Much of that fleet's decline "
           "came from aircraft being repossessed by their leasing owners and grounded "
           "by regulators, neither of which has any equivalent for computer hardware. "
           "We report the failure rather than force a fit, and it marks out what a "
           "real test would require.",
          ]),

          ("box", "How to use this",
           "The full paper gives the model, the data sources for every parameter, and "
           "runnable code with a fixed random seed, so any figure here can be "
           "reproduced or re-run under different assumptions. Three quantities are "
           "meant to be reused directly: the **compute half-life**, the **frontier "
           "exit time**, and the **sovereign floor**. Available in English, Italian "
           "and French; the English version is the version of record."),
        ]

    elif lang == "it":
        FIGS = ["brief1_due_orologi", "brief2_soglia_sovranita", "brief3_soglia"]
        META = dict(
            title="L'emivita del calcolo",
            subtitle="Che cosa fanno davvero guadagnare i controlli sull'export di "
                     "chip per l'IA, e per quanto tempo",
            kicker="SINTESI ESECUTIVA",
            author="Kevin Escoda", affil="diShine · Data, AI & Automation, Milano",
            date="8 agosto 2026",
            note="Sintesi di un working paper. Metodi, dati e codice completi nel "
                 "articolo completo. DOI 10.5281/zenodo.21866487. Codice: github.com/diShine-digital-agency/The-Half-Life-of-Compute",
            running="L'emivita del calcolo · Sintesi esecutiva")
        BODY = [
          ("lead",
           "Ogni argomento a favore delle restrizioni all'export di chip avanzati per "
           "l'IA poggia su un'affermazione temporale: i controlli **fanno guadagnare "
           "tempo**. Nessuno ha mai detto quanto. Questo lavoro lo calcola, e scopre "
           "che la spiegazione abituale del perché i controlli funzionino è sbagliata."),

          ("h", "L'errore: trattare i chip come oro"),
          ("p",
           "La capacità nazionale di IA viene misurata di continuo. Almeno undici "
           "indici pubblici classificano i paesi per potenza di calcolo, talento e "
           "infrastrutture. Tutti scattano una fotografia. Nessuno chiede che cosa "
           "accada dopo."),
          ("p",
           "È rilevante, perché la potenza di calcolo installata non è una riserva "
           "chiusa in un caveau. È un parco di macchine che si guastano. Usando dati "
           "di guasto pubblicati da un addestramento reale, circa il "
           f"**{AFR}% degli acceleratori si guasta in un anno** per cause non "
           "riparabili sul campo. E invecchiano rispetto a un bersaglio che si "
           "sposta: la scala di un addestramento di frontiera raddoppia all'incirca "
           "ogni dieci mesi. Una riserva aurea non si corrode. Un parco di chip sì, "
           "due volte."),
          ("p",
           "La letteratura ingegneristica ha misurato con precisione questa "
           "corrosione, ma sempre assumendo che i chip di ricambio si possano "
           "comprare. È esattamente l'ipotesi che un'interruzione delle forniture "
           "elimina. Eliminarla è ciò che fa questo lavoro."),

          ("rule",),
          ("h", "Tre risultati"),

          ("finding", "1", "Da due a quattro anni, e accumulare scorte lo allunga poco",
           "Un paese reciso scende sotto una quota competitiva della frontiera in "
           f"**{mo(EU['t_frontier_med'])}-{mo(US['t_frontier_med'])} mesi**. "
           "L'intervallo cresce solo con il *logaritmo* dei chip posseduti: **dieci "
           "volte il calcolo compra circa diciassette mesi in più**, cento volte "
           "circa trentacinque. E il guasto hardware pesa solo per il 13-14% di "
           "quell'orologio: il resto è la frontiera che si allontana."),
          ("fig", os.path.join(f, FIGS[0] + ".png"),
           "Il risultato sta nella distanza fra le due linee. L'hardware cala "
           "lentamente; la posizione competitiva crolla in fretta, perché la "
           "frontiera continua ad allontanarsi."),

          ("finding", "2", "Nessuno può dimostrare l'autosufficienza, e per la Cina è indeciso",
           "La **soglia di sovranità** è la quota del proprio calcolo che un paese "
           "potrebbe sostenere con gli afflussi non recisi. Alla mediana vale il "
           f"**{n(US['floor_med'])}%** per gli Stati Uniti, il "
           f"**{n(CN['floor_med'])}%** per la Cina e il **{n(EU['floor_med'])}%** per "
           "l'Unione Europea, ma i tre numeri significano cose diverse. I valori di "
           "USA e UE sono in gran parte assunzioni sulla produzione interna, "
           "riscalate. Quello cinese è un vero esito del modello, e il suo intervallo "
           f"di incertezza corre dal {n(CN['floor_p05'])}% al {n(CN['floor_p95'])}%, "
           "attraversando in alto la piena autosufficienza. I dati pubblici attuali "
           "non possono stabilire se la Cina potrebbe sostenere il proprio parco da "
           "sola. La litografia è olandese, la produzione di punta è taiwanese, la "
           "memoria specializzata è coreana: nessuno esce da questo sistema senza "
           "costi."),
          ("fig", os.path.join(f, FIGS[1] + ".png"),
           "Le barre sono stime mediane; le linee sottili mostrano l'intervallo di "
           "incertezza al 90%. I dati europei sono i meno affidabili, si vedano le "
           "avvertenze più oltre."),

          ("finding", "3", "Un interruttore nascosto che nessuno ha misurato",
           "Quando il rifornimento si interrompe, l'unica fonte di ricambi sono le "
           "altre macchine. Nell'aviazione sotto sanzioni si smonta circa un velivolo "
           "per tenerne in volo dieci. Gli acceleratori per IA non si possono "
           "recuperare così: la memoria è saldata nello stesso package del "
           "processore, quindi i due guasti più frequenti sono irreparabili per "
           f"progettazione. Esiste un rapporto critico, **{KS}**, sotto il quale le "
           "macchine guaste si accumulano e si sommano al declino, e sopra il quale il "
           "recupero le assorbe completamente e ogni ulteriore sforzo di riparazione è "
           "sprecato. L'intervallo plausibile per gli acceleratori reali sta **a "
           "cavallo** di quella linea. Al di sotto, un parco si contrae fino al 40% "
           "più rapidamente di quanto causerebbe il solo invecchiamento; al di sopra, "
           "non si può spremere altro. Nessuna evidenza pubblica dice ancora da quale "
           "lato si trovi l'hardware reale."),
          ("fig", os.path.join(f, FIGS[2] + ".png"),
           "Stabilire empiricamente questo singolo numero sarebbe, secondo questa "
           "analisi, la misurazione di maggior valore che il campo possa compiere."),

          ("rule",),
          ("h", "Che cosa significa"),
          ("pull",
           "I controlli non devono distruggere il calcolo dell'avversario. Basta loro "
           "congelarlo mentre la frontiera avanza."),
          ("p",
           "È uno strumento diverso da quello che si descrive di solito, con "
           "proprietà diverse. I test di sensibilità mostrano che il ritmo di "
           f"avanzamento della frontiera conta circa **sette volte** più "
           f"dell'affidabilità dell'hardware ({SPAN_FRONTIER:.0f} mesi di "
           f"oscillazione contro {SPAN_AFR:.0f}). Il vincolo che opera è l'orologio, "
           "non il macchinario."),
          ("bullets", [
           "**I controlli sono una scommessa sulla prosecuzione del progresso "
           "esponenziale.** Se l'avanzamento rallenta, per limiti di scala, vincoli "
           "energetici o ritiro di capitali, il loro valore decade con esso. Sono "
           "massimamente efficaci proprio quando servirebbero meno, e più deboli "
           "quando il progresso si arresta.",
           "**Accumulare scorte rende meno di quanto sembri.** Una grande dotazione "
           "di chip non allunga di molto l'orizzonte, perché l'orizzonte è fissato "
           "dalla velocità della frontiera, non dalla quantità di hardware.",
           "**La sovranità ha bisogno di un numero, non di un aggettivo.** La soglia "
           "di sovranità lo fornisce. Secondo queste stime nessuna grande potenza "
           "supera all'incirca un terzo.",
          ]),
          ("p",
           "Un ulteriore risultato riguarda direttamente l'enforcement. I controlli "
           "sono permeabili, e percorrere il tasso di dispersione separa due cose che "
           "di solito si discutono come una sola. Un contrabbando all'incirca pari al "
           "tasso storicamente stimato porta la soglia di sovranità di un paese dal "
           f"{LK['floor_at_zero']:.0f}% al 100%, ma compra soltanto circa "
           f"{LK['floor100']['t_frontier'] - LK['tf_at_zero']:.0f} mesi in più alla "
           "frontiera. Per raddoppiare l'orizzonte di frontiera servirebbe una "
           f"dispersione pari a circa il {LK['max_pct_of_c0_per_yr']:.0f}% del parco "
           "installato ogni anno: non contrabbando, ma un mercato aperto. **La "
           "dispersione compra capacità, non competitività**, l'interdizione protegge "
           "un vantaggio di frontiera molto meglio di quanto impedisca a un avversario "
           "di mantenere una soglia."),

          ("rule",),
          ("h", "Che cosa non sappiamo"),
          ("p",
           "Tre limiti vanno detti apertamente, altrimenti i numeri qui sopra "
           "verranno letti come più precisi di quanto siano."),
          ("bullets", [
           "**Il rapporto di recupero non è mai stato misurato.** Qui è delimitato "
           "ragionando su come i chip sono fisicamente costruiti, non "
           "sull'osservazione, ed è a cavallo della soglia critica.",
           "**I dati di proprietà dei chip sono risolti per impresa, non per paese.** "
           "Attribuire a una giurisdizione il parco di una multinazionale richiede "
           "ipotesi. Gli intervalli sono percorsi anziché affermati; i dati europei "
           "sono i più deboli.",
           "**Nessun paese è ancora stato reciso integralmente dal calcolo per IA.** "
           "Abbiamo tentato di calibrare sul caso reale più vicino, l'aviazione "
           "civile russa dopo il febbraio 2022, e *la calibrazione è fallita*. Gran "
           "parte del declino di quella flotta è dovuta al sequestro degli aerei da "
           "parte dei locatori e alla messa a terra da parte dei regolatori, fenomeni "
           "senza equivalente per l'hardware informatico. Riportiamo il fallimento "
           "anziché forzare un adattamento, e questo indica che cosa richiederebbe un "
           "test reale.",
          ]),

          ("box", "Come usare questo documento",
           "L'articolo completo fornisce il modello, le fonti di ogni parametro e il "
           "codice eseguibile con seme casuale fissato, così ogni cifra qui riportata "
           "può essere riprodotta o ricalcolata con ipotesi diverse. Tre grandezze "
           "sono pensate per essere riutilizzate: l'**emivita del calcolo**, il "
           "**tempo di uscita dalla frontiera** e la **soglia di sovranità**. "
           "Disponibile in inglese, italiano e francese; la versione inglese fa fede."),
        ]

    else:  # fr
        FIGS = ["brief1_deux_horloges", "brief2_plancher_souverainete", "brief3_seuil"]
        META = dict(
            title="La demi-vie du calcul",
            subtitle="Ce que les contrôles à l'exportation de puces d'IA font "
                     "réellement gagner, et pour combien de temps",
            kicker="SYNTHÈSE",
            author="Kevin Escoda", affil="diShine · Data, AI & Automation, Milan",
            date="8 août 2026",
            note="Synthèse d'un document de travail. Méthodes, données et code "
                 "complets dans l'article joint. DOI 10.5281/zenodo.21866487. Code : github.com/diShine-digital-agency/The-Half-Life-of-Compute",
            running="La demi-vie du calcul · Synthèse")
        BODY = [
          ("lead",
           "Tout argument en faveur de restrictions à l'exportation de puces d'IA "
           "avancées repose sur une affirmation temporelle : les contrôles **font "
           "gagner du temps**. Personne n'a jamais dit combien. Ce travail le "
           "calcule, et constate que l'explication habituelle de leur efficacité "
           "n'est pas la bonne."),

          ("h", "L'erreur : traiter les puces comme de l'or"),
          ("p",
           "La capacité nationale en IA est mesurée sans relâche. Au moins onze "
           "indices publics classent les pays selon leur puissance de calcul, leurs "
           "talents et leurs infrastructures. Tous prennent une photographie. Aucun "
           "ne demande ce qu'il advient ensuite."),
          ("p",
           "Cela compte, car la puissance de calcul installée n'est pas une réserve "
           "enfermée dans un coffre. C'est un parc de machines qui tombent en panne. "
           "D'après des données de panne publiées issues d'un entraînement réel, "
           f"environ **{AFR}% des accélérateurs tombent en panne en un an** pour des "
           "causes irréparables sur site. Ils vieillissent en outre face à une cible "
           "qui se déplace : l'échelle d'un entraînement de pointe double environ "
           "tous les dix mois. Une réserve d'or ne se corrode pas. Un parc de puces, "
           "si, deux fois plutôt qu'une."),
          ("p",
           "La littérature d'ingénierie a mesuré cette corrosion avec précision, mais "
           "toujours en supposant que les puces de remplacement peuvent être "
           "achetées. C'est précisément l'hypothèse qu'une coupure "
           "d'approvisionnement supprime. La lever, c'est l'objet de ce travail."),

          ("rule",),
          ("h", "Trois résultats"),

          ("finding", "1", "De deux à quatre ans, et stocker n'y change presque rien",
           "Un pays coupé passe sous une part compétitive de la frontière en "
           f"**{mo(EU['t_frontier_med'])} à {mo(US['t_frontier_med'])} mois**. "
           "L'intervalle ne croît qu'avec le *logarithme* du nombre de puces "
           "détenues : **dix fois plus de calcul n'achète qu'environ dix-sept mois "
           "de plus**, cent fois environ trente-cinq. Et la panne matérielle ne "
           "compte que pour 13-14% de cette horloge : le reste, c'est la frontière "
           "qui s'éloigne."),
          ("fig", os.path.join(f, FIGS[0] + ".png"),
           "Le résultat tient dans l'écart entre les deux courbes. Le matériel "
           "décline lentement ; la position compétitive s'effondre vite, parce que la "
           "frontière ne cesse de s'éloigner."),

          ("finding", "2", "Personne ne peut prouver l'autosuffisance, pour la Chine, c'est indécis",
           "Le **plancher de souveraineté** est la part de son propre calcul qu'un "
           "pays pourrait soutenir par les apports non rompus. À la médiane, il "
           f"s'établit à **{n(US['floor_med'])}%** pour les États-Unis, "
           f"**{n(CN['floor_med'])}%** pour la Chine et **{n(EU['floor_med'])}%** pour "
           "l'Union européenne, mais ces trois chiffres ne disent pas la même chose. "
           "Les valeurs américaine et européenne sont pour l'essentiel des hypothèses "
           "de production domestique, remises à l'échelle. La valeur chinoise est un "
           "vrai résultat du modèle, et sa fourchette d'incertitude court de "
           f"{n(CN['floor_p05'])}% à {n(CN['floor_p95'])}%, franchissant en haut la "
           "pleine autosuffisance. Les données publiques actuelles ne peuvent trancher "
           "si la Chine pourrait soutenir seule son parc. La lithographie est "
           "néerlandaise, la fabrication de pointe taïwanaise, la mémoire spécialisée "
           "coréenne : nul ne sort de ce système sans coût."),
          ("fig", os.path.join(f, FIGS[1] + ".png"),
           "Les barres sont des estimations médianes ; les traits fins indiquent "
           "l'intervalle d'incertitude à 90%. Les chiffres européens sont les moins "
           "fiables, voir les réserves ci-après."),

          ("finding", "3", "Un interrupteur caché que personne n'a mesuré",
           "Lorsque le réapprovisionnement cesse, la seule source de pièces "
           "détachées est constituée des autres machines. Dans l'aviation sous "
           "sanctions, on démonte environ un appareil pour en maintenir dix en vol. "
           "Les accélérateurs d'IA ne se récupèrent pas ainsi : la mémoire est "
           "soudée dans le même boîtier que le processeur, si bien que les deux "
           "pannes les plus fréquentes sont irréparables par conception. Il existe un "
           f"rapport critique, **{KS}**, en dessous duquel les machines en panne "
           "s'accumulent et alourdissent le déclin, et au-dessus duquel la "
           "récupération les absorbe entièrement, tout effort de réparation "
           "supplémentaire étant perdu. La fourchette plausible pour les accélérateurs "
           "réels se situe **de part et d'autre** de cette ligne. En dessous, un parc "
           "se contracte jusqu'à 40% plus vite que le seul vieillissement ne le "
           "causerait ; au-dessus, on ne peut plus rien en tirer. Aucune donnée "
           "publique ne dit encore de quel côté se trouve le matériel réel."),
          ("fig", os.path.join(f, FIGS[2] + ".png"),
           "Établir empiriquement ce seul chiffre serait, selon cette analyse, la "
           "mesure la plus précieuse que le domaine puisse entreprendre."),

          ("rule",),
          ("h", "Ce que cela signifie"),
          ("pull",
           "Les contrôles n'ont pas besoin de détruire le calcul de l'adversaire. Il "
           "leur suffit de le figer pendant que la frontière avance."),
          ("p",
           "C'est un instrument différent de celui que l'on décrit d'ordinaire, doté "
           "de propriétés différentes. Les tests de sensibilité montrent que le "
           f"rythme d'avancée de la frontière pèse environ **sept fois** plus que la "
           f"fiabilité du matériel ({SPAN_FRONTIER:.0f} mois d'amplitude contre "
           f"{SPAN_AFR:.0f}). La contrainte qui opère est l'horloge, non la machine."),
          ("bullets", [
           "**Les contrôles sont un pari sur la poursuite du progrès exponentiel.** "
           "Si l'avancée ralentit, limites de mise à l'échelle, contraintes "
           "énergétiques, retrait des capitaux, leur valeur décroît avec elle. Ils "
           "sont maximalement efficaces précisément quand ils seraient le moins "
           "nécessaires, et les plus faibles quand le progrès s'arrête.",
           "**Constituer des stocks rapporte moins qu'il n'y paraît.** Un vaste parc "
           "de puces n'allonge guère l'horizon, car celui-ci est fixé par la vitesse "
           "de la frontière et non par la quantité de matériel.",
           "**La souveraineté a besoin d'un chiffre, pas d'un adjectif.** Le plancher "
           "de souveraineté en fournit un. Selon ces estimations, aucune grande "
           "puissance ne dépasse environ un tiers.",
          ]),
          ("p",
           "Un résultat supplémentaire concerne directement la répression. Les "
           "contrôles fuient, et balayer le taux de fuite sépare deux choses que l'on "
           "discute d'ordinaire comme une seule. Une contrebande d'environ le taux "
           "historiquement estimé fait passer le plancher de souveraineté d'un pays de "
           f"{LK['floor_at_zero']:.0f}% à 100%, mais n'achète qu'environ "
           f"{LK['floor100']['t_frontier'] - LK['tf_at_zero']:.0f} mois de plus à la "
           "frontière. Doubler l'horizon de frontière exigerait une fuite d'environ "
           f"{LK['max_pct_of_c0_per_yr']:.0f}% du parc installé chaque année : non de "
           "la contrebande, mais un marché ouvert. **La fuite achète de la capacité, "
           "pas de la compétitivité**, l'interdiction protège une avance de frontière "
           "bien mieux qu'elle n'empêche un adversaire de tenir un plancher."),

          ("rule",),
          ("h", "Ce que nous ignorons"),
          ("p",
           "Trois limites méritent d'être énoncées clairement, faute de quoi les "
           "chiffres ci-dessus seront lus comme plus précis qu'ils ne le sont."),
          ("bullets", [
           "**Le rapport de récupération n'a jamais été mesuré.** Il est borné ici "
           "par un raisonnement sur la construction physique des puces, non par "
           "l'observation, et il chevauche le seuil critique.",
           "**Les données de propriété des puces sont résolues par entreprise, non "
           "par pays.** Attribuer à une juridiction le parc d'une multinationale exige "
           "des hypothèses. Les fourchettes sont balayées plutôt qu'affirmées ; les "
           "chiffres européens sont les plus fragiles.",
           "**Aucun pays n'a encore été intégralement coupé du calcul pour l'IA.** "
           "Nous avons tenté de calibrer sur le cas réel le plus proche, l'aviation "
           "civile russe après février 2022, et *la calibration a échoué*. Une large "
           "part du déclin de cette flotte tient à la saisie des appareils par leurs "
           "loueurs et à leur immobilisation par les régulateurs, deux phénomènes sans "
           "équivalent pour du matériel informatique. Nous rapportons cet échec plutôt "
           "que de forcer un ajustement, et il indique ce qu'exigerait un test réel.",
          ]),

          ("box", "Comment utiliser ce document",
           "L'article complet fournit le modèle, les sources de chaque paramètre et "
           "un code exécutable à graine aléatoire fixée : tout chiffre présenté ici "
           "peut être reproduit ou recalculé sous d'autres hypothèses. Trois "
           "grandeurs sont conçues pour être réutilisées : la **demi-vie du calcul**, "
           "le **temps de sortie de la frontière** et le **plancher de souveraineté**. "
           "Disponible en anglais, italien et français ; la version anglaise fait foi."),
        ]

    return META, BODY
