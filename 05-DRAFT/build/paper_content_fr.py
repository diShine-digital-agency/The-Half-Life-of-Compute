#!/usr/bin/env python3
"""
Version française du manuscrit, même structure que paper_content.py.

Les chiffres proviennent de 03-DATA/processed/results.json : les trois versions
linguistiques ne peuvent donc pas diverger numériquement. Les figures pointent
vers ../figures_fr/.

Note terminologique. Choix retenus pour les termes techniques :
    severance          → rupture (d'approvisionnement)
    compute            → calcul / capacité de calcul
    half-life          → demi-vie (terme standard en physique)
    installed base     → parc installé
    cannibalisation    → cannibalisation
    sovereign floor    → plancher de souveraineté
    chokepoint         → point d'étranglement
    weaponized interd. → interdépendance instrumentalisée
    field-replaceable  → remplaçable sur site
Décimales à la française (virgule), milliers séparés par une espace fine.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
FIG = os.path.join(ROOT, "05-DRAFT", "figures_fr")
R = json.load(open(os.path.join(ROOT, "03-DATA", "processed", "results.json")))
RX = json.load(open(os.path.join(ROOT, "03-DATA", "processed", "results_extended.json")))
LK = RX["leakage"]; SAT = RX["kappa_saturation"]; LIFE = RX["useful_life"]

d = R["derived"]; ks = R["kappa_star"]; av = R["aviation"]
MC = {m["jurisdiction"]: m for m in R["montecarlo"]}
CN, US, EU = MC["China"], MC["United States"], MC["European Union"]
SENS = R["sensitivity"]

NBSP = " "          # espace fine insécable, séparateur de milliers


def n0(x): return f"{x:,.0f}".replace(",", NBSP)
def p1(x): return f"{x:.1f}".replace(".", ",")
def p2(x): return f"{x:.2f}".replace(".", ",")
def p3(x): return f"{x:.3f}".replace(".", ",")
def mo(x): return ">120" if x == float("inf") else f"{x:.0f}"


META = dict(
    title="La demi-vie du calcul : modéliser le déclin de la capacité nationale "
          "en IA en régime de rupture d'approvisionnement",
    authors="Kevin Escoda",
    affiliation="diShine · Data, AI & Automation, Milan, Italie",
    email="kevin@dishine.it",
    orcid="0009-0009-7368-8129",
    doi="10.5281/zenodo.21866487",
    preprint_id="arXiv:XXXX.XXXXX",
    preprint_class="cs.CY",
    date="8 août 2026",
    version="Prépublication v1.0, non évaluée par les pairs",
    keywords="gouvernance du calcul ; contrôles à l'exportation ; souveraineté "
             "technologique ; chaînes d'approvisionnement des semi-conducteurs ; "
             "interdépendance instrumentalisée ; politiques de l'IA ; analyse de survie",
    jel="F51, F52, L63, O33, O38",
    acm="Social and professional topics → Computing and business; "
        "Hardware → Reliability",
    abstract_head="RÉSUMÉ",
    kw_label="Mots-clés",
    fig_label="Figure",
    tab_label="Tableau",
    running="Escoda · La demi-vie du calcul",
)

ABSTRACT = (
    "Les contrôles à l'exportation du matériel destiné à l'intelligence "
    "artificielle reposent sur une affirmation temporelle implicite : restreindre "
    "l'accès aux accélérateurs avancés *ferait gagner du temps*. L'ampleur de cet "
    "intervalle n'a jamais été estimée. Les travaux de mesure existants traitent "
    "la capacité nationale en IA comme un *stock* : onze indices publics classent "
    "les juridictions selon le calcul installé, les talents et les "
    "infrastructures, et aucun ne modélise ce qu'il advient de ce stock une fois "
    "le réapprovisionnement interrompu. À l'inverse, la recherche sur la fiabilité "
    "mesure la panne des accélérateurs sous l'hypothèse explicite d'un "
    "réapprovisionnement continu. Cet article réunit les deux. Nous modélisons un "
    "parc installé d'accélérateurs comme une flotte de capital périssable soumise "
    "à la panne matérielle, à l'obsolescence face à une frontière de capacité "
    "mobile, à une récupération partielle de pièces et à un remplacement domestique "
    "borné, et nous en dérivons trois grandeurs rapportables : la demi-vie du "
    "calcul $T_{1/2}$, le temps de sortie de la frontière $T_f$ et le plancher de "
    "souveraineté $C_\\infty$. Les taux de panne sont dérivés de télémétrie "
    "publiée de grands clusters (taux annuel de panne de package de "
    f"{p2(d['AFR_PACKAGE']*100)}%, validé de façon croisée contre une estimation "
    "indépendante à 1,4% près). Nous obtenons un résultat analytique : la "
    "récupération de pièces n'absorbe le flux de pannes que jusqu'à un rendement "
    f"critique de cannibalisation $\\kappa^{{*}} = \\lambda L$, égal à "
    f"{p2(ks['central'])} avec les paramètres centraux, au-delà duquel toute "
    "capacité de récupération supplémentaire n'apporte rien et le déclin est régi "
    "par la seule obsolescence, tandis qu'en deçà les pannes non réparées "
    f"accélèrent le déclin jusqu'à {SAT['excess_at_zero_pct']:.0f}%. Parce que la "
    "mémoire à haute bande passante est intégrée dans le même boîtier que la puce "
    "et qu'aucune des deux n'est remplaçable sur site, l'intervalle plausible pour "
    "les accélérateurs chevauche ce seuil. Appliqué à trois juridictions, le "
    "modèle situe la sortie de la frontière entre "
    f"{mo(EU['t_frontier_med'])} et {mo(US['t_frontier_med'])} mois, régie par "
    "$T_f \\simeq T_{\\mathrm{dbl}}\\log_2(C_0/\\theta F_0)$ : le parc installé "
    "n'achète du temps que de façon **logarithmique**, si bien qu'un ordre de "
    "grandeur de calcul supplémentaire n'achète qu'environ 17 mois de plus, et le "
    "déclin matériel ne compte que pour 13-14% de l'intervalle. Les planchers de "
    f"souveraineté médians sont de {p1(US['floor_med'])}% pour les États-Unis, "
    f"{p1(CN['floor_med'])}% pour la Chine, dont l'intervalle à 90% court "
    f"toutefois de {p1(CN['floor_p05'])}% à {p1(CN['floor_p95'])}%, si bien que "
    "l'autosuffisance chinoise demeure, sur les données publiques actuelles, "
    f"véritablement indéterminée, et {p1(EU['floor_med'])}% pour l'Union "
    "européenne. L'analyse de "
    "sensibilité montre que le rythme d'avancée de la frontière domine l'attrition "
    "matérielle d'un facteur sept. L'implication politique est qu'une rupture n'a "
    "pas besoin de détruire le calcul de l'adversaire : là où l'accès distant est "
    "également interdit, il suffit de le figer pendant que la frontière avance."
)

BODY = [

("h1", "1  Introduction"),

("p",
 "Tout argument en faveur du contrôle des exportations de matériel destiné à "
 "l'intelligence artificielle repose sur une affirmation relative au temps. "
 "Restreindre l'accès d'un adversaire aux accélérateurs avancés *ferait gagner* "
 "quelque chose : une avance, une fenêtre, un délai avant la parité des "
 "capacités. L'affirmation est temporelle, quantitative et, autant que nous "
 "avons pu l'établir, non quantifiée. Aucun travail publié n'indique combien de "
 "temps une juridiction coupée de la chaîne mondiale d'approvisionnement en "
 "accélérateurs pourrait soutenir le parc de calcul qu'elle possède déjà."),

("p",
 "Ce n'est pas faute de mesure. La capacité nationale en intelligence "
 "artificielle est aujourd'hui l'une des grandeurs les plus abondamment indexées "
 "des politiques technologiques. Au moins onze instruments publics classent les "
 "juridictions selon une combinaison de calcul installé, d'énergie, de talents, "
 "de production de modèles et de capacité de gouvernance. Ils diffèrent par leur "
 "construction et par leur transparence, mais partagent une propriété "
 "structurelle : chacun est un **instantané des dotations**. Ils répondent à la "
 "question *que possède un pays ?* Aucun ne répond à la question *que "
 "conserverait-il ?*"),

("p",
 "La distinction importe, car le calcul installé n'est pas une réserve. C'est "
 "une flotte de capital dotée d'un taux de panne mesurable, d'une durée de vie "
 "économique contestée, d'une dépendance à un approvisionnement en mémoire "
 "concentré par ailleurs, et d'une capacité qui se définit par rapport à une "
 "frontière qui ne reste pas immobile. Une réserve d'or ne se corrode pas ; un "
 "parc d'accélérateurs, si. Traiter les deux de la même manière est l'erreur de "
 "modélisation que cet article entend corriger."),

("p",
 "La littérature sur la fiabilité a mesuré ce taux de corrosion avec précision, "
 "mais sous une hypothèse qui en annule ici l'usage. La télémétrie des grands "
 "clusters fournit des statistiques de panne bien caractérisées, et l'analyse la "
 "plus autorisée sur la question de savoir si ces pannes limitent le passage à "
 "l'échelle conclut par la négative, tout en déclarant explicitement supposer "
 "que les nœuds de remplacement demeurent disponibles à l'achat, et ne pas "
 "traiter les ruptures d'approvisionnement ni les situations où les puces de "
 "remplacement ne peuvent être obtenues. C'est précisément cette hypothèse que la "
 "rupture supprime. La lever constitue l'apport du présent travail."),

("h2", "1.1  Contribution"),
("numbers", [
 "**Un modèle de déclin du calcul installé en régime de rupture.** Nous traitons "
 "un parc national d'accélérateurs comme une flotte périssable soumise à la "
 "panne, à l'obsolescence, à une récupération partielle de pièces et à un "
 "remplacement domestique borné, que nous intégrons mensuellement. Les paramètres "
 "de panne sont dérivés de télémétrie publiée plutôt que supposés, et validés de "
 "façon croisée contre une estimation indépendante.",
 "**Trois grandeurs rapportables.** La demi-vie du calcul $T_{1/2}$, le temps de "
 "sortie de la frontière $T_f$ et le plancher de souveraineté $C_\\infty$, la "
 "capacité qu'une juridiction conserve asymptotiquement par la seule production "
 "domestique. $C_\\infty$ est, soutenons-nous, la grandeur que le mot "
 "*souveraineté* désigne depuis longtemps sans jamais avoir reçu de chiffre.",
 "**Un seuil analytique.** La récupération de pièces ne soutient un parc "
 "installé qu'au-dessus d'un rendement critique de cannibalisation "
 "$\\kappa^{*} = \\lambda L$. Il s'agit d'une propriété du matériel, non des "
 "politiques, et elle sépare deux régimes de rupture qualitativement distincts.",
 "**Un résultat négatif rapporté intégralement.** Nous avons tenté de calibrer "
 "le modèle sur la seule rupture observée d'une flotte de capital comparable, "
 "l'aviation civile russe après février 2022, et la calibration échoue. Nous "
 "rapportons cet échec, en diagnostiquons la cause et expliquons pourquoi il "
 "contraint l'analogie et non le modèle.",
]),

("p",
 "Nous ne proposons délibérément pas un indice supplémentaire. Le champ en "
 "compte onze, et un onzième et demi ne serait ni original ni utile. Les indices "
 "existants entrent dans cet article comme intrants et comme littérature de "
 "référence, non comme concurrents."),

("h1", "2  Littérature de référence"),

("h2", "2.1  Mesurer la capacité technologique nationale"),
("p",
 "Les indices composites de capacité technologique sont nombreux et "
 "méthodologiquement mûrs. Le Machinepower Index (2026) évalue vingt-cinq "
 "juridictions sur douze cellules regroupées en Watts, Weights et Will, en "
 "agrégeant par une moyenne à élasticité de substitution constante avec "
 "$\\sigma = 0,33$, de sorte qu'une cellule faible contraigne le total plutôt que "
 "d'être neutralisée par la moyenne ; sa propre documentation indique que 37% des "
 "mesures sous-jacentes relèvent du jugement de l'analyste et qu'aucune dimension "
 "temporelle, aucun déclin, amortissement, taux de panne ou scénario de rupture "
 "n'est modélisé. Le Sovereign AI Index du CNAS (2026) recense plus de 139 "
 "projets soutenus par des États et constate que la plupart demeurent dépendants "
 "de technologies étrangères, majoritairement états-uniennes, sur l'ensemble de "
 "la pile ; il ne s'agit explicitement pas d'un modèle de dépendance et de "
 "rupture. Les instruments académiques présentent une structure analogue : Lee et "
 "al. (2024) décomposent la souveraineté technologique en capacité d'innovation, "
 "capacité de production et indépendance de la chaîne d'approvisionnement pour "
 "l'industrie des semi-conducteurs ; Caravella et al. (2023) retracent les "
 "dépendances stratégiques dans la filière photovoltaïque ; Cai et al. (2026) "
 "recensent 104 articles sur la politique industrielle des semi-conducteurs et la "
 "gouvernance des écosystèmes régionaux. Des instruments plus larges, le "
 "Government AI Readiness Index, le Global AI Index, l'AI Index annuel, élargissent "
 "la couverture sans modifier la logique temporelle."),
("p",
 "Chacun de ces travaux est transversal dans le temps. La littérature "
 "méthodologique sur les indicateurs composites reconnaît elle-même explicitement "
 "que la pondération, l'agrégation et la robustesse sont le point où de tels "
 "instruments réussissent ou échouent (Greco et al., 2018 ; Dobbie et al., 2013 ; "
 "Kelemen et al., 2024 ; OCDE/JRC, 2008), et nous en adoptons la discipline plus "
 "loin. Mais aucun soin apporté à l'agrégation ne convertit un instantané en "
 "trajectoire."),

("h2", "2.2  Gouvernance du calcul et fiabilité des accélérateurs"),
("p",
 "Sastry et al. (2024) établissent le cadre de référence : la puissance de "
 "calcul est un objet de politique publique traitable parce qu'elle est "
 "détectable, excluable, quantifiable et produite par une chaîne "
 "d'approvisionnement extrêmement concentrée. Ces quatre propriétés sont "
 "précisément les conditions qui rendent possible un modèle de rupture ; le "
 "présent article peut se lire comme le successeur quantitatif de cet argument "
 "qualitatif. La pratique réglementaire a suivi la même direction, retenant la "
 "performance de traitement cumulée, et non le décompte des unités, comme "
 "grandeur contrôlée."),
("p",
 "Du côté matériel, Grattafiori et al. (2024) rapportent des statistiques "
 "d'interruption résolues par composant pour un entraînement sur 16 384 "
 "accélérateurs, et Kokolis et al. (2025) ajustent des modèles de panne sur plus "
 "de 150 millions d'heures-accélérateur réparties sur deux clusters de "
 "production. L'analyse d'Epoch AI conclut que la panne matérielle ne limitera "
 "pas le passage à l'échelle, sous réapprovisionnement continu. C'est notre "
 "lecture de cette condition aux limites, énoncée dans la source elle-même, qui "
 "motive ce travail."),

("p",
 "Une troisième tradition est plus proche que les deux autres et doit être "
 "reconnue : la modélisation militaire du soutien logistique. Le METRIC de "
 "Sherbrooke (1968) et la tradition multi-échelon qu'il a fondée optimisent les "
 "stocks de rechanges récupérables pour la disponibilité des flottes, et ses "
 "extensions modernes intègrent explicitement la cannibalisation. C'est le "
 "parent quantitatif le plus proche de notre terme de récupération, et nous lui "
 "empruntons son vocabulaire. Elle diffère précisément sur les marges dont cet "
 "article a besoin : elle optimise l'inventaire sous une filière de "
 "réapprovisionnement en état de marche plutôt que sous rupture totale, et ses "
 "systèmes n'affrontent aucune frontière de capacité mobile, un avion qui vole "
 "est disponible, tandis qu'un accélérateur qui fonctionne peut être déjà "
 "stratégiquement obsolète. Le seuil $\\kappa^{*}$ doit donc se lire comme la "
 "limite en régime de rupture de cette tradition, non comme la prétention "
 "d'avoir découvert la cannibalisation."),

("h2", "2.3  Statecraft économique et points d'étranglement"),
("p",
 "Farrell et Newman (2019) fournissent le cadre théorique : une topologie de "
 "réseau asymétrique permet aux États disposant d'une juridiction sur les nœuds "
 "centraux d'exercer un *effet panoptique* et un *effet d'étranglement*, le "
 "second refusant l'accès au réseau aux adversaires. Beaumier et al. (2023) "
 "appliquent l'analyse de réseaux directement aux semi-conducteurs, décomposant "
 "la filière en réseaux de conception, de matières premières, d'équipements de "
 "production et de puces assemblées, et montrant comment la centralité dans l'un "
 "permet d'instrumentaliser un autre. Fuller (2026) soutient que le cadre se "
 "transpose imparfaitement aux biens physiques, où un point d'étranglement se "
 "comprend mieux comme un intrant sans lequel une tâche ne peut se poursuivre, "
 "formulation qui recoupe étroitement le modèle développé ici."),
("p",
 "L'évaluation quantitative des contrôles s'est concentrée sur les agrégats "
 "économiques. Park et Liu (2023) recourent à des méthodes entrées-sorties "
 "multirégionales ; Cui et al. (2025) emploient un modèle d'équilibre général "
 "calculable dynamique pour estimer les effets sur le PIB de l'embargo sur les "
 "puces et des contre-contrôles chinois sur le gallium, le germanium et le "
 "graphite ; Shrivastava et al. (2025) évaluent le contournement. La résilience "
 "des chaînes a été modélisée par des topologies de cascade sans échelle et des "
 "réseaux bayésiens. Tout cela mesure la **conséquence économique**. Rien ne "
 "mesure le **déclin de la capacité dans le temps**."),
("p",
 "L'analyse sectorielle s'en approche le plus. Des estimations du moment où un "
 "stock de puces non assemblées sera épuisé ont été publiées, dont une "
 "formulation zero-inflated attribuant environ 56% de probabilité à l'épuisement "
 "d'un tel stock avant janvier 2026. Ce travail modélise un *déstockage*, des "
 "composants en attente d'assemblage. Le présent article modélise le *déclin du "
 "parc installé*, du matériel déjà déployé et en fonctionnement. Ce sont deux "
 "questions distinctes relevant de mathématiques distinctes, et nous nous "
 "limitons scrupuleusement à revendiquer la seconde."),

("quote",
 "La littérature existante mesure ce qu'une juridiction possède, ce qu'elle peut "
 "construire et ce que la rupture coûte à son économie. Cet article mesure "
 "combien de temps ce qu'elle possède continue de fonctionner."),

("h1", "3  Le modèle"),

("h2", "3.1  Cadre"),
("p",
 "Soit $N(t)$ le nombre d'accélérateurs opérationnels, en équivalents-H100 "
 "(H100e), au mois $t$ suivant la rupture, avec $N(0) = C_0$. Le calcul national "
 "effectif est"),
("eq", "C(t) \\;=\\; N(t)\\,u(t)", "1"),
("p",
 "où $u(t) \\in (0,1]$ est un plafond d'utilisation imposé par des contraintes "
 "énergétiques, d'interconnexion et d'exploitation. Trois flux agissent sur $N$ à "
 "chaque période. Les pannes matérielles surviennent au risque mensuel "
 "$\\lambda = -\\ln(1-\\mathrm{AFR})/12$. L'obsolescence retire des unités au taux "
 "$\\delta = 1/L$, où $L$ est la durée de vie utile en mois ; les unités retirées "
 "demeurent physiquement intactes. Le remplacement arrive sous forme de "
 "production domestique et de fuite, $R = R_{\\mathrm{dom}} + R_{\\mathrm{fuite}}$."),
("p",
 "Le mécanisme qui distingue la rupture du fonctionnement ordinaire est la "
 "récupération de pièces. Sous réapprovisionnement, une unité en panne est "
 "remplacée et $N$ reste inchangé, c'est pourquoi les analyses de fiabilité "
 "concluent que les pannes ne contraignent pas. En régime de rupture, la seule "
 "source de réparation est constituée des autres unités. Soit $P(t)$ le vivier de "
 "réparations récupérables et $\\kappa$ le *rendement de cannibalisation* : le "
 "nombre de réparations tirées d'une unité donneuse. Alors"),
("eq",
 "\\begin{aligned}"
 "F_t &= N_t\\lambda, \\qquad \\mathrm{Ret}_t = N_t\\delta \\\\"
 "\\rho_t &= \\min(F_t,\\;P_t) \\\\"
 "P_{t+1} &= P_t - \\rho_t + \\kappa\\,(F_t - \\rho_t + \\mathrm{Ret}_t) \\\\"
 "N_{t+1} &= N_t - F_t - \\mathrm{Ret}_t - S_t + \\rho_t + R"
 "\\end{aligned}", "2"),
("p",
 "où $S_t$ désigne le nombre d'unités *encore en état de marche* retirées "
 "volontairement pour en prélever des pièces. Ce retrait n'est rationnel que "
 "lorsqu'une donneuse rend plus d'une réparation, de sorte que $S_t > 0$ exige "
 "$\\kappa > 1$ ; nous le plafonnons à 3% de la flotte par mois."),

("h2", "3.2  Le rendement critique de cannibalisation"),
("p",
 "Le vivier de récupération est alimenté par les unités quittant le service et "
 "vidé par les réparations. Les seuls retraits soutiennent le flux de réparation "
 "lorsque $\\kappa N\\delta \\geq N\\lambda$, ce qui donne un seuil indépendant de "
 "la taille de la flotte, des apports et des politiques :"),
("eq", "\\kappa^{*} \\;=\\; \\frac{\\lambda}{\\delta} \\;=\\; \\lambda L", "3"),
("p",
 "$\\kappa^{*}$ est un seuil de **saturation**, non de survie, et la distinction "
 "compte. Au-dessus, la récupération absorbe la quasi-totalité du flux de pannes "
 "et le parc installé décline au seul rythme de l'obsolescence ; toute capacité "
 "de récupération supplémentaire n'apporte rien. En dessous, les pannes non "
 "réparées s'ajoutent aux retraits et, à $\\kappa = 0$, le parc se contracte "
 f"{SAT['excess_at_zero_pct']:.0f}% plus vite que la seule obsolescence ne le "
 "laisserait attendre. Ce que $\\kappa^{*}$ sépare est donc un régime *limité "
 "par les pannes* d'un régime *limité par l'obsolescence*. Il ne sépare pas la "
 "survie de l'effondrement : sans apport de remplacement, tout parc décline, car "
 "le retrait ôte des unités que les pannes soient réparées ou non. "
 "$\\kappa^{*}$ est une propriété du matériel, de son taux de panne et de sa "
 "durée de vie utile, et non de la juridiction qui le détient. L'annexe A en "
 "donne la dérivation ; le §5.1 la vérification."),
("p",
 "C'est ici que l'architecture physique des accélérateurs devient déterminante, "
 "et ici que l'analogie avec d'autres flottes de capital se rompt. Une cellule "
 "d'avion est riche en pièces : elle se décompose en milliers d'unités "
 "remplaçables tombant en panne indépendamment, et la pratique observée sous "
 "sanctions a consisté à démonter environ un appareil pour en maintenir une "
 "dizaine en vol, ce qui implique $\\kappa \\approx 10$. Un accélérateur d'IA est "
 "pauvre en pièces exactement au mauvais endroit. La mémoire à haute bande "
 "passante est intégrée dans le même boîtier que la puce logique sur un "
 "interposeur partagé ; ni la puce ni la pile mémoire ne constituent une unité "
 "remplaçable sur site. Les deux modes de panne dominants sont donc non "
 "récupérables **par construction**, et la cannibalisation ne récupère que des "
 "composants annexes du nœud, alimentations, interfaces réseau, refroidissement "
 ", qui ne sont pas les modes de panne contraignants. Nous retenons "
 "$\\kappa \\in [0,05 ; 0,50]$ pour les accélérateurs et traitons la valeur "
 "aéronautique comme une borne supérieure relevant d'une autre classe de matériel."),

("h2", "3.3  Grandeurs rapportées"),
("bullets", [
 "**Demi-vie du calcul $T_{1/2}$**, mois nécessaires pour que le calcul "
 "effectif passe sous la moitié de sa valeur au jour de la rupture. Censurée à "
 "droite à l'horizon de 120 mois.",
 "**Temps de sortie de la frontière $T_f$**, mois nécessaires pour que la "
 "capacité nationale passe sous une part seuil $\\theta = 0,10$ de l'échelle "
 "d'entraînement de frontière contemporaine "
 "$F(t) = F_0\\,2^{t/T_{\\mathrm{dbl}}}$, où $F_0$ est un ancrage **absolu et "
 "commun à toutes les juridictions**. Une version antérieure normalisait par le "
 "$C_0$ propre à chaque juridiction, ce qui les faisait toutes partir à parité et "
 "annulait identiquement $C_0$ ; l'invariance au stock qui en résultait était un "
 "artefact algébrique et a été retirée (§5.3, annexe A).",
 "**Plancher de souveraineté $C_\\infty$**, le niveau asymptotique en part de "
 "$C_0$, soutenable par l'ensemble des apports non rompus, production "
 "domestique *et* fuite résiduelle, maintenus à leur rythme du jour de la "
 "rupture. Une forme close existe et figure en annexe A ; elle reproduit "
 "exactement l'intégration à 900 mois. $C_\\infty$ n'est défini que pour une "
 "croissance nulle de l'indigénisation (§7.4).",
]),

("p",
 "L'ancrage $F_0$ mérite une dérivation au grand jour, puisque $T_f$ en hérite "
 "par le logarithme. Un entraînement de frontière de $10^{26}$ à $10^{27}$ FLOP, "
 "exécuté en trois mois environ sur des accélérateurs soutenant "
 "$4 \\times 10^{14}$ FLOP/s effectifs, correspond à quelque "
 "$3 \\times 10^{21}$ FLOP par accélérateur, donc à $3 \\times 10^{4}$ à "
 "$3 \\times 10^{5}$ H100e par exécution. Les estimations vivantes encadrent "
 "le même intervalle : le premier entraînement déclaré au-dessus de $10^{26}$ "
 "FLOP fut Grok 3 en février 2025, à environ $3 \\times 10^{26}$ ; le plus "
 "grand à ce jour est Grok 4 ; et Epoch AI situe le franchissement de "
 "$10^{26}$ par le premier modèle de frontière vers janvier 2026. Nous balayons "
 "donc $F_0$ log-uniformément entre $5 \\times 10^{4}$ et "
 "$5 \\times 10^{5}$ H100e, avec $1{,}5 \\times 10^{5}$ en valeur centrale, "
 "et chaque $T_f$ rapporté porte cette incertitude."),

("h1", "4  Données et paramètres"),

("h2", "4.1  Taux de panne dérivés de la télémétrie des clusters"),
("p",
 "Grattafiori et al. (2024) rapportent 419 interruptions inattendues sur une "
 "fenêtre de pré-entraînement de 54 jours, sur un cluster comptant jusqu'à "
 "16 384 accélérateurs H100, résolues par cause : accélérateur défectueux 148 "
 "(30,1%), mémoire HBM3 de l'accélérateur 72 (17,2%), commutateur ou câble réseau "
 "35 (8,4%). En annualisant par accélérateur,"),
("eq",
 "\\mathrm{AFR} \\;=\\; \\frac{n_{\\mathrm{\\acute{e}v\\grave{e}nements}}}{16{,}384}"
 "\\times\\frac{365}{54}", "4"),
("p",
 f"on obtient {p2(d['AFR_GPU_DIE']*100)}% par an pour les pannes de puce et "
 f"{p2(d['AFR_HBM']*100)}% pour la HBM3, soit un **taux de panne de boîtier de "
 f"{p2(d['AFR_PACKAGE']*100)}% par an** pour les deux modes non remplaçables sur "
 f"site, et {p2(d['AFR_ALL']*100)}% toutes causes d'interruption confondues. À "
 f"titre de vérification indépendante, le chiffre toutes causes correspond à une "
 f"interruption toutes les {n0(d['xcheck_gpu_hours_per_failure'])} "
 f"heures-accélérateur, contre environ {n0(d['epoch_reported'])} rapportées par "
 f"Epoch AI sur la même exécution, un accord à 1,4% près. Nous retenons le taux "
 f"de boîtier comme valeur centrale et parcourons l'intervalle complet dans le "
 f"Monte-Carlo. Une précaution accompagne ces taux : les décomptes "
 "d'interruptions ne distinguent pas la mort définitive du matériel des pannes "
 "transitoires levées par un redémarrage ; dans la mesure où certaines "
 "interruptions attribuées à la puce étaient récupérables, le taux de boîtier "
 "surestime l'attrition permanente. La direction de ce biais est bénigne pour "
 "nos conclusions : un $\\lambda$ plus faible allonge $T_{1/2}$, relève les "
 "planchers et laisse $T_f$ quasi inchangé."),

("h2", "4.2  Parc installé"),
("p",
 "Epoch AI estime un stock mondial livré d'environ 15 millions de H100e et "
 "publie des données résolues par propriétaire. Pour la Chine, nous dérivons "
 "$C_0$ d'une relation publiée plutôt que d'une hypothèse : l'estimation médiane "
 "de 660 000 H100e détournés jusqu'en 2025 est décrite comme représentant environ "
 f"un tiers de la capacité totale chinoise, d'où $C_0 \\approx$ "
 f"{n0(d['C0_CHINA'])} H100e. L'intervalle à 90% de l'estimation de contrebande "
 "(290 000-1 600 000) est propagé directement."),
("p",
 "**C'est la principale limite de données de l'étude, et nous l'énonçons "
 "clairement.** Epoch résout la propriété par *entreprise*, non par "
 "*juridiction*. Attribuer à un pays le parc d'un opérateur multinational exige "
 "des hypothèses qui ne sont pas pleinement défendables à partir de données "
 "publiques. Nous parcourons donc la part états-unienne entre 60% et 78% et celle "
 "de l'Union européenne entre 2% et 6% du stock mondial, et nous rapportons les "
 "résultats européens avec une confiance d'autant plus faible. Aucune conclusion "
 "de cet article ne dépend d'une estimation ponctuelle du stock national."),

("h2", "4.3  La rupture est modélisée symétriquement"),
("p",
 "Une juridiction est coupée des intrants qu'elle ne contrôle pas. Il vaut la "
 "peine de souligner qu'il ne s'agit pas d'un scénario propre à la Chine. Les "
 "États-Unis ne disposent d'aucune source domestique de lithographie à "
 "ultraviolets extrêmes, ne détiennent qu'une capacité de production de pointe "
 "partielle et encore en montée en charge, et ne produisent pas de mémoire à "
 "haute bande passante à l'échelle, l'approvisionnement en HBM étant concentré à "
 "environ 90% chez deux entreprises coréennes. La couverture domestique "
 "états-unienne en régime de rupture avec ses propres alliés constitue donc une "
 "plage de scénario (15-35%) et non l'unité. À l'Union européenne, dépourvue de "
 "production de logique de pointe en exploitation, nous attribuons 1-4%."),

("table", "Paramètres du modèle, intervalles et sources.", "1",
 ["Symbole", "Paramètre", "Central", "Intervalle", "Source"],
 [["$\\lambda$", "Taux de panne boîtier (annuel)",
   f"{p2(d['AFR_PACKAGE']*100)}%",
   f"{p2(d['AFR_GPU_DIE']*100)}-{p2(d['AFR_ALL']*100)}%",
   "Dérivé, Grattafiori et al. (2024)"],
  ["$\\kappa$", "Rendement de cannibalisation", "0,275", "0,05-0,50",
   "Architecture du boîtier (§3.2)"],
  ["$L$", "Durée de vie utile (ans)", "4,0", "2,0-6,0",
   "Controverse sur l'amortissement, 2025-26"],
  ["$T_{\\mathrm{dbl}}$", "Doublement frontière (mois)", "5,2", "4,8-7,0",
   "Epoch AI, série de l'*entraînement* de frontière"],
  ["$F_0$", "Ancrage de frontière (H100e)", "150 000", "50k-500k",
   "Dérivé ; v. §3.3. Balayé log-uniforme"],
  ["$\\theta$", "Seuil de compétitivité", "0,10", "fixe",
   "Convention ; n'entre que par le logarithme (§5.3)"],
  ["$\\mathrm{cov}$", "Couverture domestique É.-U. / UE", "0,25 / 0,02",
   "0,15-0,35 / 0,01-0,04", "**Hypothèse, sans base observationnelle**"],
  ["$C_0^{\\mathrm{CN}}$", "Stock Chine (H100e)", n0(d['C0_CHINA']),
   "0,87-4,80 M", "Dérivé, Epoch AI"],
  ["$C_0^{\\mathrm{US}}$", "Stock É.-U. (H100e)", n0(d['C0_US']),
   "9,0-11,7 M", "Epoch AI, part balayée"],
  ["$C_0^{\\mathrm{EU}}$", "Stock UE (H100e)", n0(d['C0_EU']),
   "0,3-0,9 M", "Scénario, confiance faible"],
  ["$R_{\\mathrm{dom}}$", "Production Chine (H100e/mois)",
   n0(d['cn_domestic_pm'] * 0.65), "30-100% du rythme 2025",
   "Production réalisée (Epoch AI) × dépendance aux stocks"],
  ["$R_{\\mathrm{fuite}}$", "Fuite (H100e/mois)",
   n0(d['leak_pm'] * 0.35), "10-60% de la base",
   "Dérivé, Epoch AI (2026)"]],
 "H100e = équivalents-H100. Les intervalles sont propagés par un Monte-Carlo à "
 "10 000 tirages avec échantillonnage uniforme indépendant. L'indépendance est "
 "elle-même une hypothèse : les corrélations plausibles entre paramètres, "
 "entre durée de vie utile et taux de panne, ou entre stock et capacité "
 "domestique, ne sont pas modélisées."),

("h1", "5  Résultats"),

("h2", "5.1  L'intervalle plausible chevauche le seuil"),
("p",
 f"Avec les paramètres centraux, $\\kappa^{{*}} = {p2(ks['central'])}$. Sur "
 "l'ensemble de la grille de paramètres, il varie de 0,13 (pannes de puce "
 "seules, durée de vie de deux ans) à 1,14 (toutes causes, durée de vie de six "
 "ans). L'intervalle plausible pour les accélérateurs, $[0,05 ; 0,50]$, "
 "**chevauche le seuil central**. La mesure directe sur le modèle intégré "
 "confirme l'algèbre : face à un déclin par retrait seul de "
 f"{p2(SAT['retirement_only']*100)}% par mois, le parc se contracte de "
 f"{p2(SAT['r_zero']*100)}% par mois à $\\kappa = 0$ "
 f"(excès de {SAT['excess_at_zero_pct']:.0f}%), retombant à "
 f"{p2(SAT['r_at_kstar']*100)}% à $\\kappa^{{*}}$ "
 f"(excès de {SAT['excess_at_kstar_pct']:.0f}%), après quoi tripler $\\kappa$ ne "
 "le modifie que de moins de 2%. Un parc situé sous le seuil paie donc une "
 "pénalité cumulative, tandis qu'un parc au-dessus ne tire plus rien d'une "
 "capacité de récupération accrue. Établir empiriquement $\\kappa$ constitue, "
 "selon cette analyse, la mesure de plus grande valeur que le champ puisse "
 "entreprendre."),
("p",
 "Le seuil interagit avec la controverse sur l'amortissement d'une manière qui "
 "mérite d'être explicitée. Comme $\\kappa^{*} = \\lambda L$ croît avec la durée "
 "de vie utile, un parc plus durable se situe plus bas par rapport à toute "
 "capacité de récupération donnée : sur la fourchette contestée de deux à six "
 f"ans, la part des pannes que la récupération peut absorber chute de "
 f"{LIFE[0]['failures_absorbed_pct']:.0f}% à "
 f"{LIFE[-1]['failures_absorbed_pct']:.0f}%. Nous avons testé, et rejetons, "
 "l'inférence tentante selon laquelle les parcs plus durables seraient dès lors "
 "globalement plus fragiles : le temps de demi-vie sans apport *augmente* de "
 f"{LIFE[0]['t_half_months_zero_inflow']:.0f} à "
 f"{LIFE[-1]['t_half_months_zero_inflow']:.0f} mois sur la même plage, le retrait "
 "plus lent l'emportant. L'énoncé défendable est plus étroit : un parc à six ans "
 "survit plus longtemps en valeur absolue tout en dépendant davantage du stock "
 "brut et moins de la réparation. Nous rapportons l'hypothèse rejetée parce "
 "qu'elle est séduisante, citable et fausse."),
("fig", os.path.join(FIG, "fig7_kappa_critique.png"),
 "Le rendement critique de cannibalisation $\\kappa^{*} = \\lambda L$ en fonction "
 "de la durée de vie utile, pour trois hypothèses de taux de panne. La bande "
 "ombrée est l'intervalle plausible pour les accélérateurs d'IA, la mémoire à "
 "haute bande passante étant intégrée au même boîtier et non remplaçable sur "
 "site. La bande coupe les trois courbes : que la récupération soutienne un parc "
 "installé dépend du régime, et non d'une question de degré.", "1"),

("h2", "5.2  Trajectoires et grandeurs rapportées"),
("p",
 "Le tableau 2 rapporte les médianes et les intervalles à 90% sur 10 000 tirages "
 "par juridiction. La sortie de la frontière survient entre "
 f"{mo(EU['t_frontier_med'])} et {mo(US['t_frontier_med'])} mois, ordonnée selon "
 "le parc installé comme l'exige la relation analytique du §5.3. À la médiane, "
 "aucune juridiction n'atteint l'autosuffisance, mais les planchers doivent être "
 "lus avec une double précaution : pour les États-Unis et l'Union européenne, "
 "ils sont le paramètre de couverture domestique supposé, remis à l'échelle par "
 "un facteur borné, et non un résultat indépendant du modèle (§7.2), tandis que "
 f"l'intervalle à 90% de la Chine atteint {p1(CN['floor_p95'])}%, au-dessus de "
 "la parité. Les planchers médians s'établissent à "
 f"{p1(US['floor_med'])}% pour les États-Unis, {p1(CN['floor_med'])}% pour la "
 f"Chine et {p1(EU['floor_med'])}% pour l'Union européenne."),

("table", "Grandeurs rapportées par juridiction. Médianes avec intervalles à 90%, "
          "10 000 tirages Monte-Carlo.", "2",
 ["Juridiction", "$C_0$ (M H100e)", "$T_{1/2}$ (mois)", "$T_f$ (mois)",
  "$C_\\infty$ (% de $C_0$)", "$P(T_{1/2}\\!\\leq\\!36)$"],
 [["Chine", p2(CN['C0_h100e']/1e6),
   f"{mo(CN['t_half_med'])} [{mo(CN['t_half_p05'])}-{mo(CN['t_half_p95'])}]",
   f"{mo(CN['t_frontier_med'])} [{mo(CN['t_frontier_p05'])}-{mo(CN['t_frontier_p95'])}]",
   f"{p1(CN['floor_med'])} [{p1(CN['floor_p05'])}-{p1(CN['floor_p95'])}]",
   f"{p1(CN['p_half_within_36m'])}%"],
  ["États-Unis", p2(US['C0_h100e']/1e6),
   f"{mo(US['t_half_med'])} [{mo(US['t_half_p05'])}-{mo(US['t_half_p95'])}]",
   f"{mo(US['t_frontier_med'])} [{mo(US['t_frontier_p05'])}-{mo(US['t_frontier_p95'])}]",
   f"{p1(US['floor_med'])} [{p1(US['floor_p05'])}-{p1(US['floor_p95'])}]",
   f"{p1(US['p_half_within_36m'])}%"],
  ["Union européenne", p2(EU['C0_h100e']/1e6),
   f"{mo(EU['t_half_med'])} [{mo(EU['t_half_p05'])}-{mo(EU['t_half_p95'])}]",
   f"{mo(EU['t_frontier_med'])} [{mo(EU['t_frontier_p05'])}-{mo(EU['t_frontier_p95'])}]",
   f"{p1(EU['floor_med'])} [{p1(EU['floor_p05'])}-{p1(EU['floor_p95'])}]",
   f"{p1(EU['p_half_within_36m'])}%"]],
 f"$T_{{1/2}}$ est censurée à droite à 120 mois. Les tirages censurés sont "
 f"conservés ordinalement, de sorte que tout quantile tombant dans la masse "
 f"censurée est rapporté comme '>120' plutôt que comme une valeur finie ; la "
 f"censure concerne {p1(CN['t_half_censored_pct'])}% des tirages chinois et "
 f"{p1(US['t_half_censored_pct'])}% des tirages états-uniens. Les valeurs "
 f"européennes sont de faible confiance, les données de stock résolues par "
 f"juridiction y étant les plus fragiles (§4.2)."),

("fig", os.path.join(FIG, "fig1_declin_juridictions.png"),
 "Déclin du calcul effectif après la rupture, cas central. La trajectoire "
 "européenne est la plus rapide malgré l'exposition absolue la plus faible, car "
 "le remplacement domestique y couvre la moindre part de l'attrition.", "2"),

("fig", os.path.join(FIG, "fig2_montecarlo_chine.png"),
 "Distribution Monte-Carlo pour la Chine, 10 000 tirages avec échantillonnage "
 "uniforme indépendant sur tous les paramètres du tableau 1. La largeur de "
 "l'intervalle à 90% reflète le balayage conjoint de tous les paramètres ; les "
 "apports chinois étant absolus et non proportionnels au stock, l'incertitude "
 "sur $C_0$ y contribue également.", "3"),

("h2", "5.3  L'horloge de la frontière domine l'attrition matérielle"),
("p",
 "Le résultat déterminant n'est pas le déclin du matériel mais sa faible part de "
 "l'intervalle. La figure 4 représente la capacité rapportée à l'échelle de "
 "frontière contemporaine. En écartant entièrement le déclin, le temps de sortie "
 "suit"),
("eq", r"T_f \simeq T_{\mathrm{dbl}}\,\log_2\left(\frac{C_0}{\theta F_0}\right)", "5"),
("p",
 "qui reproduit les cas centraux simulés à quatre mois près (analytique 36,6 / "
 "49,1 / 27,7 contre simulé 36 / 45 / 24 pour la Chine, les États-Unis et l'Union "
 "européenne). Deux conséquences en découlent, et elles remplacent l'affirmation "
 "d'invariance au stock avancée dans une version antérieure."),
("bullets", [
 "**Le parc installé n'achète du temps que logarithmiquement.** À "
 "$T_{\\mathrm{dbl}} = 5,2$ mois, un parc dix fois plus grand achète "
 "$T_{\\mathrm{dbl}}\\log_2 10 \\approx 17$ mois de plus, et un parc cent fois "
 "plus grand seulement 35. Le stockage est soumis à des rendements fortement "
 "décroissants face à une frontière mobile, énoncé plus fort et plus utile que "
 "l'invariance qu'il remplace, et qui, contrairement à elle, n'est pas un "
 "artefact de normalisation.",
 "**Le déclin matériel compte pour une minorité constante de l'intervalle.** En "
 "rejouant chaque cas central avec panne et retrait annulés, on obtient 42 / 52 / "
 "28 mois contre 36 / 45 / 24 avec déclin : l'attrition coûte 6 / 7 / 4 mois, "
 "soit **13-14% du budget** dans les trois juridictions. Les 86% restants sont "
 "l'horloge de la frontière.",
]),
("p",
 "La lecture corrigée est donc plus étroite que l'originale mais résiste à "
 "l'examen : la fiabilité du matériel ne régit pas la position stratégique en "
 "régime de rupture, mais la position n'est pas non plus indépendante de la "
 "quantité de matériel détenue."),
("fig", os.path.join(FIG, "fig3_relatif_frontiere.png"),
 "Capacité relative à la frontière mobile, échelle logarithmique. Les trois "
 "juridictions partent de positions différentes car les parcs installés "
 "diffèrent ; le déclin quasi parallèle reflète le déflateur commun de "
 "frontière. Les temps de franchissement sont ordonnés selon le stock et séparés "
 "d'environ $T_{\\mathrm{dbl}}\\log_2$ du rapport des stocks.", "4"),
("p",
 "L'analyse de sensibilité confirme le mécanisme. En faisant varier le temps de "
 f"doublement de la frontière sur son intervalle de 4,8 à 7,0 mois, $T_f$ se "
 f"déplace de {SENS[0]['span']:.0f} mois ; en faisant varier le taux de panne sur "
 f"l'intégralité de l'intervalle dérivé, il se déplace de "
 f"{[s for s in SENS if 'Failure' in s['parameter']][0]['span']:.0f} mois, un "
 "écart de levier de sept fois. La fiabilité du matériel, la grandeur que "
 "la littérature d'ingénierie mesure avec le plus de soin, figure parmi les "
 "paramètres les *moins* importants pour l'issue stratégique."),
("fig", os.path.join(FIG, "fig4_tornade_sensibilite.png"),
 "Sensibilité univariée du temps de sortie de la frontière, ordonnée par "
 "amplitude. Le rythme d'avancée de la frontière domine ; le rendement de "
 "cannibalisation et le taux de panne comptent le moins une fois le régime fixé.", "5"),

("p",
 "Le seuil $\\theta = 0{,}10$ est une convention, et son influence est "
 "entièrement transparente : il n'entre dans l'éq. 5 que par le logarithme, de "
 "sorte que le diviser par deux allonge chaque $T_f$ d'exactement un temps de "
 "doublement, environ cinq mois, et le doubler le raccourcit d'autant, sans "
 "toucher ni l'ordre ni les écarts. Vérifié numériquement : 42 / 36 / 31 mois "
 "pour $\\theta$ = 0,05 / 0,10 / 0,20 dans le cas central chinois."),

("h2", "5.4  Dépendance au régime"),
("p",
 "La figure 6 montre les trajectoires selon les régimes de cannibalisation. Les "
 f"valeurs de $\\kappa$ supérieures à $\\kappa^{{*}} = {p2(ks['central'])}$, y "
 "compris la valeur aéronautique de 10, un accélérateur hypothétiquement "
 "réparable sur site à 1, et la borne supérieure de l'intervalle plausible à 0,5 "
 ", sont indiscernables, car toutes trois sont au-delà de la saturation et le "
 "flux de pannes est déjà intégralement absorbé. Seule la borne inférieure, 0,05, "
 "se situe assez bas pour peser sur le déclin. Le système ne répond pas "
 "continûment à $\\kappa$ : il sature."),
("fig", os.path.join(FIG, "fig6_regimes_kappa.png"),
 "Déclin sous quatre régimes de cannibalisation. Les trois courbes égales ou "
 "supérieures au rendement critique coïncident car toutes sont au-delà de la "
 "saturation : le flux de pannes est déjà absorbé et la capacité supplémentaire "
 "reste inutilisée.", "6"),

("h2", "5.5  Rupture partielle : ce que la fuite achète réellement"),
("p",
 "Les contrôles réels ne sont ni complets ni instantanés. Ils fuient, par "
 "détournement, revente et transbordement via pays tiers, et l'ampleur de cette "
 "fuite est précisément la grandeur que dispute la politique répressive. Balayer "
 "le terme de fuite sur quatre ordres de grandeur permet de séparer deux effets "
 "que l'on discute d'ordinaire comme un seul."),
("p",
 "Les deux horizons répondent à la fuite avec des élasticités très différentes. "
 f"Sur un balayage de zéro à {LK['max_pct_of_c0_per_yr']:.0f}% du parc installé "
 f"par an, le plancher de souveraineté monte de {LK['floor_at_zero']:.0f}% à "
 f"{LK['floor_at_max']:.0f}% de $C_0$, un facteur "
 f"{LK['floor_at_max']/max(LK['floor_at_zero'],1e-9):.0f}, tandis que la sortie "
 f"de la frontière ne passe que de {LK['tf_at_zero']:.0f} à "
 f"{LK['tf_at_max']:.0f} mois, une variation de "
 f"{100*(LK['tf_at_max']/LK['tf_at_zero']-1):.0f}%. L'asymétrie découle "
 "directement de la forme analytique : le plancher est un état stationnaire "
 "déterminé par les apports et y répond linéairement, tandis que $T_f$ n'y entre "
 "que par un logarithme et par un dénominateur à croissance exponentielle. "
 f"Atteindre un plancher de 100% de $C_0$ coûte environ "
 f"{LK['floor100']['leak_pct_of_C0_per_yr']:.0f}% du parc installé par an et "
 f"n'achète que {LK['floor100']['t_frontier'] - LK['tf_at_zero']:.0f} mois "
 "supplémentaires à la frontière."),
("table", "Rupture partielle. Effet de la fuite sur les deux horizons.", "3",
 ["Régime de fuite", "H100e / mois", "% de $C_0$ par an", "$T_f$ (mois)",
  "$C_\\infty$ (% de $C_0$)"],
 [["Aucune", "0", "0", f"{LK['tf_at_zero']:.0f}", f"{LK['floor_at_zero']:.0f}"],
  ["Plancher tenu à 100%", n0(LK['floor100']['leak_per_month']),
   p1(LK['floor100']['leak_pct_of_C0_per_yr']),
   f"{LK['floor100']['t_frontier']:.0f}", "100"],
  ["Équivalent marché ouvert", ", ", f"{LK['max_pct_of_c0_per_yr']:.0f}",
   f"{LK['tf_at_max']:.0f}", f"{LK['floor_at_max']:.0f}"]],
 "Les taux de fuite sont exprimés par rapport au flux de détournement "
 "historiquement estimé. Le plancher est très élastique à la fuite ; l'horizon de "
 "frontière ne l'est pas."),
("fig", os.path.join(FIG, "fig8_fuite.png"),
 "La fuite relève fortement le plancher de souveraineté tout en déplaçant très "
 "peu l'horizon de frontière. Les deux courbes divergent parce que le plancher "
 "est un état stationnaire déterminé par les apports, tandis que la sortie de la "
 "frontière est régie par le taux de croissance de la frontière elle-même.", "7"),
("p",
 "**La fuite achète de la capacité, pas de la compétitivité.** Pour la conception "
 "des dispositifs répressifs, cela inverse l'accent habituel. L'interdiction est "
 "relativement efficace pour protéger une avance de frontière, robuste à la fuite "
 "parce qu'elle est fixée par le rythme de croissance de la frontière et non par "
 "le stock de l'adversaire. Elle est presque impuissante à empêcher un adversaire "
 "de maintenir un plancher substantiel, car le plancher répond directement aux "
 "apports et l'apport requis est modeste. Un régime de contrôle justifié sur le "
 "premier terrain et évalué sur le second paraîtra échouer alors qu'il n'échoue "
 "pas, et réciproquement."),

("h1", "6  La comparaison aéronautique, et pourquoi la calibration échoue"),

("p",
 "Un modèle de rupture prête le flanc à l'objection d'être infalsifiable, "
 "puisqu'aucune juridiction n'a jusqu'ici été intégralement coupée du calcul "
 "pour l'IA. La réponse naturelle consiste à calibrer sur le cas observé le plus "
 "proche. L'aviation civile russe après février 2022 est la seule rupture "
 "documentée d'une flotte de capital complexe et dépendante des pièces "
 "détachées, avec une fenêtre d'observation pluriannuelle : une flotte initiale "
 "d'environ 1 500 à 1 800 appareils de construction occidentale, dont plus d'un "
 "tiers cannibalisé en octobre 2025, une réduction projetée supérieure à 50% "
 "d'ici 2026, et une pratique documentée consistant à démonter environ un "
 "appareil pour en maintenir dix en vol."),
("p",
 "**Nous avons tenté cette calibration et elle échoue.** En ajustant le risque "
 "du modèle comme unique paramètre libre avec $\\kappa = 10$ fixé d'après la "
 "pratique observée, le meilleur ajustement atteignable donne une erreur "
 f"quadratique moyenne de {p3(av['rmse'])} et laisse "
 f"{av['unexplained_decline_share']*100:.0f} points de pourcentage du déclin "
 "observé inexpliqués au mois 47, le risque estimé venant buter contre la borne "
 "supérieure de la grille de recherche."),
("fig", os.path.join(FIG, "fig5_comparaison_aviation.png"),
 "Flotte civile russe observée face au meilleur ajustement atteignable par la "
 "seule attrition de pièces. Le résidu ombré est la part du déclin que "
 "l'attrition de pièces ne peut expliquer. Il ne s'agit pas d'une erreur de "
 "modèle : il correspond à des mécanismes sans équivalent en matière de calcul.", "8"),
("p",
 "Le résidu est instructif, non embarrassant. Deux mécanismes expliquent une "
 "large part du déclin observé et n'ont pas d'équivalent en matière de calcul : "
 "la saisie par les loueurs des appareils de propriété étrangère, qui constitue "
 "un choc ponctuel sur le stock et non de l'attrition, et le retrait de "
 "navigabilité par les régulateurs, qui écarte des appareils en état de marche "
 "pour des motifs juridiques et non physiques. Les accélérateurs sont détenus en "
 "pleine propriété et aucun régulateur n'immobilise un cluster dégradé. Imputer "
 "à l'attrition de pièces l'intégralité du déclin russe surestimerait le risque "
 "d'environ un ordre de grandeur."),
("p",
 "Nous utilisons donc l'aéronautique pour borner $\\kappa$ et pour établir que la "
 "cannibalisation est un mécanisme réel, observé et quantifié, non pour calibrer "
 "le modèle du calcul. Rapporter ce résultat négatif importe pour deux raisons. "
 "Cela empêche qu'une calibration faussement précise se propage dans la "
 "littérature, et cela identifie exactement ce qu'exigerait un test empirique "
 "adéquat : la télémétrie d'un parc soumis à une contrainte réelle de "
 "réapprovisionnement, qui n'existe pas à ce jour sous forme publique."),
("p",
 "Un résultat qualitatif se transpose néanmoins. La fréquence des incidents "
 "rapportée pour la flotte russe a plus que doublé par rapport à 2019 bien avant "
 "que le nombre d'appareils ne diminue de moitié. La dégradation se manifeste "
 "comme une baisse de fiabilité avant de se manifester comme une baisse "
 "d'inventaire. Si cela vaut pour le calcul, la capacité effective décroît plus "
 "vite que le décompte des nœuds ne le suggère, et nos estimations sont "
 "conservatrices."),

("h1", "7  Discussion"),

("h2", "7.1  Ce que la rupture fait réellement gagner"),
("p",
 "Les résultats appuient une reformulation du débat sur les contrôles à "
 "l'exportation. La grandeur pertinente n'est pas la quantité de calcul qu'un "
 "adversaire perd, mais le temps qu'il met à décrocher d'une frontière en "
 "mouvement, et selon nos estimations cet intervalle est d'environ deux ans et "
 "se révèle remarquablement insensible à la taille du parc installé. Les "
 "contrôles n'ont pas besoin de détruire de la capacité : il leur suffit de la "
 "maintenir constante pendant que la frontière avance. À l'inverse, une "
 "juridiction qui s'est assuré un vaste parc d'accélérateurs a acheté moins de "
 "temps stratégique que sa taille ne le laisse croire, car la contrainte "
 "opérante est le taux de croissance de la frontière et non son propre matériel."),
("p",
 "Il en découle une implication symétrique et moins confortable. Si l'avancée de "
 "la frontière ralentit, du fait de limites de mise à l'échelle, de contraintes "
 "énergétiques ou d'un retrait des capitaux, la valeur des contrôles décroît "
 "avec elle. Dans cette lecture, les contrôles à l'exportation sont un pari sur "
 "la poursuite du progrès exponentiel. Ils sont maximalement efficaces "
 "précisément lorsqu'ils seraient le moins nécessaires pour établir une "
 "prééminence, et minimalement efficaces lorsque le progrès s'arrête et que les "
 "stocks installés conservent leur valeur relative."),

("h2", "7.2  La souveraineté a un chiffre, et il est partout faible"),
("p",
 "Le plancher de souveraineté explicite ce que la littérature des indices "
 "désignait sans le quantifier, mais il doit se lire avec une réserve que nous "
 "énonçons avant le résultat, non après. L'annexe A montre que, lorsque la "
 "production domestique est paramétrée comme fraction de couverture du stock "
 "installé, le cas des États-Unis et de l'Union européenne, le plancher "
 "s'effondre en $\\mathrm{cov}\\,(1 + \\min(\\kappa, \\kappa^{*}))$, "
 f"indépendant de $C_0$, $\\lambda$ et $L$. Le chiffre états-unien de "
 f"{p1(US['floor_med'])}% est donc la bande de couverture supposée (15-35%) "
 "remise à l'échelle par un facteur compris entre 1,0 et 1,5, et non un résultat "
 "indépendant. Nous le rapportons comme **cartographie de scénario** : une "
 "couverture de 0,15 / 0,25 / 0,35 implique un plancher de 19 / 32 / 45%, et "
 "quiconque conteste l'hypothèse de couverture peut y substituer la sienne. Le "
 f"plancher chinois ({p1(CN['floor_med'])}%) est d'une autre nature, il dérive "
 "d'une estimation d'apport absolu et non d'une fraction de couverture, et il "
 "est le seul des trois à constituer un résultat du modèle au sens propre. Son "
 f"intervalle doit alors être pris au sérieux : la bande à 90% court de "
 f"{p1(CN['floor_p05'])}% à {p1(CN['floor_p95'])}% du parc installé, franchissant "
 "la parité en haut. L'extrémité supérieure est mue conjointement par le "
 "paramètre de dépendance aux stocks, la production réalisée de Huawei en 2025 "
 "serait-elle tenable sans le stock de puces TSMC constitué avant les contrôles "
 ", et par la large incertitude sur $C_0$ lui-même. Le modèle n'autorise donc "
 "pas l'affirmation que la Chine ne peut soutenir son parc intérieurement : il "
 "autorise l'agnosticisme, et il désigne la mesure qui trancherait la question, "
 "la part de dépendance aux stocks, comme la deuxième cible empirique la plus "
 "précieuse après $\\kappa$."),
("p",
 "Cette réserve posée, le point qualitatif tient, et il ne dépend pas du "
 "paramètre contesté. La lithographie est néerlandaise, la production de pointe "
 "est taïwanaise et la mémoire à haute bande passante est coréenne à environ "
 "90%. Aucun participant à ce système ne peut en être coupé sans coût, et le "
 "cadrage rhétorique faisant de la souveraineté une propriété qu'un camp "
 "posséderait et l'autre non n'est soutenu par aucune hypothèse de couverture "
 "que nous jugions plausible."),

("h2", "7.3  Prédictions testables"),
("p",
 "Le modèle est falsifiable, et il vaut la peine de préciser comment, car un "
 "modèle de rupture invérifiable n'est qu'un essai. Quatre prédictions en "
 "découlent directement, chacune assortie de l'observation qui la réfuterait."),
("bullets", [
 "**La fiabilité se dégrade avant l'inventaire.** Dans tout parc de calcul opérant "
 "sous une contrainte réelle de réapprovisionnement, le taux de tâches échouées "
 "non récupérées devrait croître de façon mesurable avant que le nombre de nœuds "
 "opérationnels ne baisse sensiblement. Réfutée si les effectifs de nœuds baissent "
 "proportionnellement aux taux de panne, ou avant eux.",
 "**L'effort de récupération présente un point de saturation, non un gradient.** "
 "Les opérateurs qui accroissent leur capacité de cannibalisation au-delà du seuil "
 "ne devraient constater aucun gain supplémentaire de disponibilité. Réfutée par "
 "une relation régulière et non saturante entre effort de récupération et "
 "disponibilité.",
 "**La sortie de la frontière varie logarithmiquement avec le stock.** D'une "
 "juridiction à l'autre, $T_f$ devrait croître d'environ "
 "$T_{\\mathrm{dbl}}\\log_2(10) \\approx 17$ mois par décuplement du calcul "
 "installé, et non proportionnellement. Réfutée par une relation linéaire ou "
 "quasi linéaire. (Une version antérieure proposait la prédiction inverse, le "
 "découplage d'avec le stock, qui, sous la métrique alors implémentée, était "
 "infalsifiable par construction.)",
 "**Le détournement déplace le plancher, pas la frontière.** Les périodes de "
 "détournement accru devraient relever nettement la capacité de calcul soutenue "
 "d'une juridiction tout en laissant ses plus grands entraînements là où "
 "l'horloge de la frontière les situe. Réfutée si les entraînements à l'échelle de "
 "la frontière suivent les volumes détournés.",
]),
("p",
 "La première est la plus immédiatement vérifiable : il suffirait qu'un opérateur "
 "sous contrainte publie la télémétrie des tâches échouées à côté des effectifs de "
 "nœuds. Aucune série de ce type n'est publique aujourd'hui, et c'est pourquoi le "
 "§6 rapporte une calibration échouée plutôt que réussie."),

("h2", "7.4  Limites"),
("bullets", [
 "**Attribution juridictionnelle.** Les meilleures données publiques sur les "
 "stocks résolvent la propriété par entreprise et non par pays. Nous balayons les "
 "parts plutôt que de les affirmer, mais aucun traitement ne supprime totalement "
 "cette faiblesse. Les résultats européens en particulier doivent se lire comme "
 "une illustration de scénario.",
 "**$\\kappa$ n'est pas mesuré.** Le rendement de cannibalisation est borné par "
 "un raisonnement architectural et non par l'observation, et l'intervalle "
 "plausible chevauche le seuil critique. C'est le paramètre ouvert le plus "
 "déterminant.",
 "**L'utilisation est maintenue constante.** Les contraintes énergétiques et de "
 "réseau sont représentées par un plafond fixe. Plusieurs analyses récentes "
 "soutiennent que, dans certaines juridictions, c'est désormais l'énergie et non "
 "le silicium qui contraint ; endogénéiser $u(t)$ raccourcirait vraisemblablement "
 "les horizons rapportés ici.",
 "**La rupture est modélisée comme complète et instantanée.** Les contrôles "
 "réels sont partiels, progressifs et perméables. Le terme de fuite en capte une "
 "partie ; les régimes par paliers ou par escalade ne sont pas modélisés.",
 "**La frontière est exogène.** Nous traitons la croissance de la frontière comme "
 "une exponentielle externe. En réalité, la sortie de la frontière d'une "
 "juridiction coupée modifie les dynamiques concurrentielles et donc la "
 "trajectoire de la frontière elle-même.",
 "**Il n'existe aucun cas empirique de rupture pour le calcul.** Le modèle est "
 "falsifiable en principe, il prédit des trajectoires de dégradation précises, "
 "mais ne peut encore être confronté à l'observation, comme l'établit le §6.",
 "**Le retrait est un choix économique que le modèle traite comme de la "
 "physique.** La durée de vie utile $L$ encode un retrait à la fin de vie "
 "comptable, mais un opérateur en régime de rupture ferait plausiblement tourner "
 "le matériel jusqu'à la panne. En rejouant les cas centraux avec $L$ porté à "
 "quarante ans, $T_f$ ne croît que de trois à quatre mois, chaque $T_{1/2}$ "
 "s'allonge et les planchers montent nettement : le scénario de couverture "
 "états-unien passe de 32% à 92% de $C_0$, la Chine de 86% à 246%. La marche "
 "jusqu'à la panne renforce donc les résultats de souveraineté et déplace à "
 "peine l'horloge de la frontière, raison pour laquelle les résultats "
 "principaux rapportent le cas conservateur avec retrait.",
 "**$T_f$ mesure la position en calcul, non la position en capacité.** "
 "L'efficacité algorithmique des modèles de langage a historiquement divisé par "
 "deux le calcul requis à performance fixe environ tous les huit mois (Ho et "
 "al., 2024). Dans la mesure où ces avancées sont publiques, les deux camps en "
 "profitent et l'ordre relatif se conserve, mais un parc gelé continue de "
 "gagner en capacité absolue : franchir $\\theta$ est donc plus doux en termes "
 "de capacité qu'en termes de FLOP. Dans la mesure où les avancées de frontière "
 "restent propriétaires, le camp coupé se dégrade plus vite que $T_f$ ne le "
 "suggère. La mesure est exacte sur le matériel et délibérément agnostique sur "
 "le logiciel.",
 "**L'accès distant est hors du modèle par construction.** $N(t)$ compte les "
 "accélérateurs physiquement installés et exploités dans la juridiction. Le "
 "calcul loué auprès de fournisseurs étrangers n'est pas dans $N(t)$ et, à la "
 "différence du terme de fuite, dont les unités entrent dans le parc puis "
 "déclinent à $\\lambda$ et $\\delta$, la capacité louée est reconstituée par "
 "le bailleur et ne décline pas du tout. Tout horizon rapporté ici est donc "
 "conditionnel à la rupture matérielle *et* à l'interdiction effective de "
 "l'accès distant ; face à une rupture matérielle seule, il constitue une borne "
 "supérieure de l'effet. Une consolation suit analytiquement : le déflateur de "
 "frontière étant exponentiel, une location fixe de n'importe quelle taille ne "
 "déplace $T_f$ que de $T_{\\mathrm{dbl}}\\log_2(1 + A/C_0)$ ; la capacité "
 "louée ne défait le mécanisme que si elle croît elle-même au rythme de la "
 "frontière, $g^{*} = \\ln 2 / T_{\\mathrm{dbl}} \\approx 13\\%$ par mois.",
 "**La production domestique est gelée à son rythme du jour de la rupture.** Le "
 "modèle ne contient aucun canal de substitution induite, de sorte que "
 "$C_\\infty$ n'est défini que pour une croissance nulle de l'indigénisation ; "
 "pour tout taux positif, il n'existe aucune asymptote. Cette hypothèse est "
 "contredite par la tendance la plus récente de la série même qui calibre le "
 "paramètre, les objectifs chinois de production d'accélérateurs auraient à "
 "peu près doublé entre 2025 et 2026, quoique, sous la prémisse de rupture "
 "complète du présent article, mémoire coréenne et lithographie néerlandaise "
 "toutes deux retirées, le taux pourrait plausiblement prendre l'un ou l'autre "
 "signe. $T_f$ y est robuste : il ne bouge que de quelques mois pour des taux de "
 "croissance de $-30\\%$ à $+60\\%$ par an, aucun rythme plausible "
 "d'indigénisation ne rivalisant avec une frontière qui double tous les 5,2 "
 "mois.",
]),

("h1", "8  Conclusion"),
("p",
 "La capacité nationale en IA a été mesurée comme un stock au moins onze fois et "
 "modélisée comme un flux pas une seule. Nous avons soutenu que le flux est la "
 "grandeur pertinente pour l'action publique, construit un modèle de déclin des "
 "parcs installés d'accélérateurs en régime de rupture, paramétré à partir de "
 "télémétrie publiée plutôt que d'hypothèses, et rapporté trois grandeurs "
 "conçues pour être réutilisées : la demi-vie du calcul, le temps de sortie de la "
 "frontière et le plancher de souveraineté."),
("p",
 "Quatre résultats se détachent. La récupération de pièces n'absorbe le flux de "
 f"pannes que jusqu'à un rendement de saturation "
 f"$\\kappa^{{*}} = \\lambda L \\approx {p2(ks['central'])}$ et, la mémoire à "
 "haute bande passante étant intégrée au même boîtier que la puce, l'intervalle "
 "plausible pour les accélérateurs chevauche ce seuil, ce qui fait de $\\kappa$ "
 "le paramètre non mesuré le plus précieux du champ. La sortie de la frontière "
 "survient entre deux et quatre ans et ne croît que logarithmiquement avec le "
 "parc installé : un parc dix fois plus grand achète environ dix-sept mois de "
 "plus, tandis que le déclin matériel ne compte que pour 13-14% de l'intervalle "
 "et l'horloge de la frontière pour le reste. À la médiane, aucune grande "
 "juridiction n'apparaît autosuffisante, bien que pour les États-Unis et "
 "l'Union européenne ce chiffre soit une hypothèse de couverture remise à "
 "l'échelle plutôt qu'un résultat indépendant, et que l'intervalle chinois soit "
 "assez large pour franchir la parité, laissant là-bas la question de la "
 "souveraineté véritablement ouverte. Et la fuite, lorsqu'elle est partielle, achète de la "
 "capacité et non de la compétitivité : elle relève fortement le plancher de "
 "souveraineté en laissant l'horizon de frontière presque inchangé."),
("p",
 "L'affirmation selon laquelle les contrôles à l'exportation font gagner du "
 "temps est, selon cette analyse, correcte dans sa forme et substantiellement "
 "erronée quant au mécanisme qu'on lui prête habituellement. Ce que l'on gagne "
 "n'est pas la dégradation du matériel adverse, mais le gel de sa position face à "
 "une frontière qui continue d'avancer. C'est un instrument différent, doté d'une "
 "date de péremption différente, et c'est à ce titre qu'il devrait être défendu."),

("h1", "Annexe A  Dérivation du rendement critique"),
("p",
 "Soit $P_t$ le vivier de récupération. Sur une période, le vivier gagne "
 "$\\kappa$ réparations pour chaque unité quittant le service, pannes non "
 "réparées $(F_t-\\rho_t)$ et retraits $\\mathrm{Ret}_t$, et perd $\\rho_t$ du "
 "fait des réparations effectuées. Considérons l'état stationnaire où toute panne "
 "est réparée, de sorte que $\\rho_t = F_t = N\\lambda$ et "
 "$\\mathrm{Ret}_t = N\\delta$. Le bilan du vivier s'écrit"),
("eq", "\\Delta P \\;=\\; \\kappa N\\delta \\;-\\; N\\lambda", "A.1"),
("p",
 "quantité positive ou nulle précisément lorsque $\\kappa \\geq \\lambda/\\delta$. "
 "En posant $\\delta = 1/L$, on obtient $\\kappa^{*} = \\lambda L$. La taille de "
 "la flotte $N$ se simplifie : le seuil est donc invariant d'échelle ; l'apport "
 "$R$ n'y figure pas : il est donc aussi indépendant des politiques. En dessous "
 "de $\\kappa^{*}$, le vivier s'épuise en temps fini et les pannes non réparées "
 "s'accumulent ; au-dessus, le vivier croît sans borne et la contrainte de "
 "réparation cesse d'opérer, d'où la coïncidence des trajectoires pour "
 "$\\kappa = 0,5$, $1$ et $10$ à la figure 6."),
("p",
 "Notons soigneusement ce que cela n'établit *pas*. L'équation A.1 ne régit que la "
 "contrainte de réparation. Le retrait ôte des unités du service que les pannes "
 "soient réparées ou non : $N$ décline donc aussi au-dessus du seuil, au rythme "
 "$\\delta$, et non à $\\delta$ augmenté d'un terme de pannes non absorbées. Une "
 "version antérieure de cet article affirmait que le parc installé *persiste* "
 "au-dessus de $\\kappa^{*}$ ; la simulation directe la réfute, et la lecture "
 "corrigée, un seuil de saturation séparant un déclin limité par les pannes d'un "
 "déclin limité par l'obsolescence, est celle vérifiée numériquement au §5.1."),

("h2", "A.2  Forme close du plancher de souveraineté"),
("p",
 "Une version antérieure affirmait qu'aucune forme close n'existait et "
 "rapportait le plancher d'une intégration à 900 mois. Une forme close existe. "
 "En rendant le vivier stationnaire dans l'éq. 2, on obtient "
 "$\\rho = \\kappa(F+\\mathrm{Ret})/(1+\\kappa)$, d'où une attrition nette de "
 "$(\\lambda+\\delta)N/(1+\\min(\\kappa,\\kappa^{*}))$ et"),
("eq",
 r"\frac{C_\infty}{C_0} = \frac{R_{\mathrm{dom}}+R_{\mathrm{fuite}}}"
 r"{C_0\,(\lambda+\delta)}\,\left(1+\min(\kappa,\kappa^{*})\right)",
 "A.2"),
("p",
 "qui reproduit exactement les valeurs intégrées. La conséquence doit être dite "
 "clairement car elle contraint la lecture de deux de nos trois planchers. "
 "Lorsque la production domestique est paramétrée comme fraction de couverture "
 "du stock, $R_{\\mathrm{dom}} = \\mathrm{cov}\\cdot C_0(\\lambda+\\delta)$, "
 "notre traitement des États-Unis et de l'Union européenne faute de données de "
 "production résolues par juridiction, celle-ci s'effondre en"),
("eq", r"\frac{C_\infty}{C_0} = \mathrm{cov}\,"
       r"\left(1+\min(\kappa,\lambda L)\right)", "A.3"),
("p",
 "indépendante de $C_0$, $\\lambda$ et $L$, la parenthèse étant bornée dans "
 "$[1,0 ;\\,1,5]$ sur toutes les valeurs considérées. Ces deux planchers sont "
 "donc la remise à l'échelle d'une hypothèse, non une propriété émergente du "
 "modèle, et le §7.2 les rapporte comme cartographie de scénario. Le plancher "
 "chinois, dérivé d'une estimation d'apport absolu, n'est pas sujet à cet "
 "effondrement."),

("h1", "Annexe B  Reproductibilité"),
("p",
 "Tous les résultats proviennent d'un unique script déterministe à graine "
 "aléatoire fixée (20260808). Son exécution régénère chaque figure, chaque "
 "tableau et chaque valeur numérique de cet article, y compris celles citées dans "
 "le résumé. Le modèle tient en 200 lignes de NumPy sans dépendance à un solveur "
 "externe. Code du modèle, fichier de paramètres, sorties Monte-Carlo et journal "
 "complet de recherche des sources sont archivés avec cette prépublication ; voir "
 "*Disponibilité des données et du code*."),
]

BACK = [
("h1", "Disponibilité des données et du code"),
("p",
 "Le code du modèle, les définitions de paramètres avec attribution de source "
 "pour chaque valeur, les sorties Monte-Carlo, les tableaux traités et "
 "l'intégralité du code de génération des figures sont librement disponibles sur "
 "github.com/diShine-digital-agency/The-Half-Life-of-Compute et sont "
 "archivés avec le dépôt Zenodo de cet article. Les données sous-jacentes sont de tierces parties et "
 "publiquement accessibles : Epoch AI publie des données de propriété et de "
 "ventes d'accélérateurs avec une méthodologie documentée ; les statistiques de "
 "panne proviennent d'articles publiés. Aucune donnée propriétaire ou sous "
 "licence n'a été utilisée."),

("h1", "Déclarations"),
("p",
 "**Financement.** Cette recherche n'a bénéficié d'aucun financement externe. "
 "**Conflits d'intérêts.** L'auteur est fondateur de diShine, société de conseil "
 "en adoption et gouvernance de l'IA, et auteur d'un ouvrage de vulgarisation sur "
 "la géopolitique des technologies, cité une seule fois dans cet article pour un "
 "apport de cadrage. Aucune de ces deux relations n'a influencé l'analyse, qui "
 "repose entièrement sur des données publiques et du code publié. **Assistance "
 "par IA.** Des outils computationnels ont été employés pour la recherche des "
 "sources, l'implémentation du modèle et la préparation du manuscrit ; toutes les "
 "affirmations analytiques, les choix de paramétrage et les interprétations sont "
 "de l'auteur, et chaque affirmation factuelle a été vérifiée sur une source "
 "primaire consultée."),

("h1", "Note sur la version"),
("p",
 "Cet article est la version française de *The Half-Life of Compute: Modelling "
 "National AI Capacity Decay Under Supply Severance*. Les versions sont générées "
 "par le même modèle et partagent des résultats numériques identiques. En cas de "
 "divergence, la version anglaise fait foi : c'est elle qui est déposée sur "
 "Zenodo."),

("h1", "Bibliographie"),
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
 "for a New American Security, avril 2026.",
 "Cui, L., et al. (2025). Quantitative analysis of the U.S. chip embargo and "
 "China's export controls on Ga, Ge and graphite. *Computers & Industrial "
 "Engineering*, 7 janvier 2025. ScienceDirect PII S0360835225000051.",
 "Dobbie, M. J., et al. (2013). Robustness and sensitivity of weighting and "
 "aggregation in constructing composite indices. *Ecological Indicators*.",
 "Epoch AI (2025). *Hardware failures won't limit AI scaling*. "
 "epoch.ai/blog/hardware-failures-wont-limit-ai-scaling",
 "Epoch AI (2026). *Data on AI Chip Owners* et *Data on AI Chip Sales*, avec "
 "méthodologie publiée. epoch.ai/data",

 "Epoch AI (2026). *Data on AI Models* : entraînements de frontière, dont "
 "Grok 3 à environ 3e26 FLOP et Grok 4 comme le plus grand déclaré. "
 "epoch.ai/data/ai-models",
 "Escoda, K. (2026). *GEOPOLITECH*. Volume III de *The Architecture of the New "
 "World: From Code to Matter*., cité uniquement pour le cadrage sur les points "
 "d'étranglement.",
 "Farrell, H. & Newman, A. L. (2019). Weaponized Interdependence: How Global "
 "Economic Networks Shape State Coercion. *International Security*, 44(1), "
 "42-79. doi:10.1162/isec_a_00351",
 "Fuller, D. B. (2026). Technology and Economic Statecraft: Weaponizing "
 "Technology Export Controls in an Era of Globalized Production. *SSRN "
 "Electronic Journal*.",
 "Grattafiori, A., et al. (2024). The Llama 3 Herd of Models. arXiv:2407.21783.",
 "Greco, S., Ishizaka, A., Tasiou, M. & Torrisi, G. (2019). On the "
 "Methodological Framework of Composite Indices: A Review of the Issues of "
 "Weighting, Aggregation, and Robustness. *Social Indicators Research*, "
 "141(1), 61-94. doi:10.1007/s11205-017-1832-9",
 "Ho, A., Besiroglu, T., Erdil, E., Owen, D., Rahman, R., Guo, Z. C., "
 "Atkinson, D., Thompson, N. & Sevilla, J. (2024). Algorithmic Progress in "
 "Language Models. arXiv:2403.05812.",

 "Juniewicz, I. (2026). *Diversion and resale: estimating compute smuggling to "
 "China*. Epoch AI, 29 avril 2026.",
 "Kelemen, A., et al. (2024). A sensitivity analysis of composite indicators: "
 "Min/max thresholds. *Environmental and Sustainability Indicators*.",
 "Kokolis, A., Kuchnik, M., Hoffman, J., Kumar, A., Malani, P., Ma, F., DeVito, "
 "Z., Sengupta, S., Saladi, K. & Wu, C.-J. (2025). Revisiting Reliability in "
 "Large-Scale Machine Learning Research Clusters. *IEEE HPCA 2025*. "
 "arXiv:2410.21680.",
 "Leavy, E. (2026). *Machinepower Index 2026*, édition T3 2026. "
 "machinepowerindex.org",
 "Lee, J.-D., Choi, S., Kim, K. & Si, S. (2024). *Empirical Measurement of "
 "Technology Sovereignty*. IFS Working Paper 2024-01, Institute for Future "
 "Strategy, Seoul National University. SSRN 5145685.",
 "Meng, W. (2025). Modeling the Path of Structural Strategic Deterrence: A Sand "
 "Table Simulation Based on Rare Earth Supply Disconnection. arXiv:2505.21579.",
 "Nardo, M., Saisana, M., Saltelli, A. & Tarantola, S. (2008). *Handbook on "
 "Constructing Composite Indicators: Methodology and User Guide*. OCDE / "
 "Commission européenne JRC. JRC47008. ISBN 978-92-64-04346-6.",
 "Park, D.-J. & Liu, S. (2023). A Study on the Economic Effects of U.S. Export "
 "Controls on Semiconductors to China. *Korea International Trade Research "
 "Institute*. SSRN 4391187.",
 "Sherbrooke, C. C. (1968). METRIC: A Multi-Echelon Technique for Recoverable "
 "Item Control. *Operations Research*, 16(1), 122-141. doi:10.1287/opre.16.1.122. "
 "Antérieurement RAND RM-5078.",

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
