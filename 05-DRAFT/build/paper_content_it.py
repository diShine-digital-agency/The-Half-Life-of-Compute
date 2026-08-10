#!/usr/bin/env python3
"""
Versione italiana del manoscritto, stessa struttura di paper_content.py.

Le cifre sono lette da 03-DATA/processed/results.json, quindi le due lingue non
possono divergere numericamente. Le figure puntano a ../figures_it/.

Nota terminologica. Alcuni termini tecnici non hanno un equivalente italiano
consolidato; le scelte adottate sono:
    severance          → recisione (delle forniture)
    compute            → calcolo / capacità di calcolo
    half-life          → emivita (termine standard in fisica)
    installed base     → parco installato
    cannibalisation    → cannibalizzazione
    sovereign floor    → soglia di sovranità
    chokepoint         → punto di strozzatura
    weaponized interd. → interdipendenza armata
    field-replaceable  → sostituibile sul campo
Numeri decimali secondo l'uso italiano (virgola); migliaia con punto.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
FIG = os.path.join(ROOT, "05-DRAFT", "figures_it")
R = json.load(open(os.path.join(ROOT, "03-DATA", "processed", "results.json")))
RX = json.load(open(os.path.join(ROOT, "03-DATA", "processed", "results_extended.json")))
LK = RX["leakage"]; SAT = RX["kappa_saturation"]; LIFE = RX["useful_life"]

d = R["derived"]; ks = R["kappa_star"]; av = R["aviation"]
MC = {m["jurisdiction"]: m for m in R["montecarlo"]}
CN, US, EU = MC["China"], MC["United States"], MC["European Union"]
SENS = R["sensitivity"]


def it(s):
    """Punto decimale → virgola, separatore migliaia → punto."""
    return s.replace(",", "\x00").replace(".", ",").replace("\x00", ".")


def n0(x): return it(f"{x:,.0f}")
def p1(x): return it(f"{x:.1f}")
def p2(x): return it(f"{x:.2f}")
def mo(x): return ">120" if x == float("inf") else f"{x:.0f}"


META = dict(
    title="L'emivita del calcolo: un modello di decadimento della capacità "
          "nazionale di IA in regime di recisione delle forniture",
    authors="Kevin Escoda",
    affiliation="diShine · Data, AI & Automation, Milano, Italia",
    email="kevin@dishine.it",
    orcid="0009-0009-7368-8129",
    doi="10.5281/zenodo.21866487",
    preprint_id="arXiv:XXXX.XXXXX",
    preprint_class="cs.CY",
    date="8 agosto 2026",
    version="Preprint v1.0, non sottoposto a revisione paritaria",
    keywords="governance del calcolo; controlli sulle esportazioni; sovranità "
             "tecnologica; catene di fornitura dei semiconduttori; interdipendenza "
             "armata; politiche dell'IA; analisi di sopravvivenza",
    jel="F51, F52, L63, O33, O38",
    acm="Social and professional topics → Computing and business; "
        "Hardware → Reliability",
    abstract_head="ABSTRACT",
    kw_label="Parole chiave",
    fig_label="Figura",
    tab_label="Tabella",
    running="Escoda · L'emivita del calcolo",
)

ABSTRACT = (
    "I controlli sulle esportazioni di hardware per l'intelligenza artificiale "
    "sono giustificati da un'affermazione temporale implicita: limitare l'accesso "
    "agli acceleratori avanzati farebbe *guadagnare tempo*. L'ampiezza di questo "
    "intervallo non è mai stata stimata. La letteratura di misurazione tratta la "
    "capacità nazionale di IA come uno *stock*: undici indici pubblici classificano "
    "le giurisdizioni per calcolo installato, talento e infrastrutture, e nessuno "
    "modella che cosa accada a quello stock una volta interrotto il "
    "riapprovvigionamento. La ricerca sull'affidabilità, all'opposto, misura il "
    "guasto degli acceleratori sotto l'ipotesi esplicita di rifornimento continuo. "
    "Questo articolo congiunge i due filoni. Modelliamo un parco installato di "
    "acceleratori come una flotta di capitale deperibile, soggetta a guasto "
    "hardware, obsolescenza rispetto a una frontiera di capacità mobile, recupero "
    "parziale di componenti e sostituzione interna limitata, e ne deriviamo tre "
    "grandezze riportabili: l'emivita del calcolo $T_{1/2}$, il tempo di uscita "
    "dalla frontiera $T_f$ e la soglia di sovranità $C_\\infty$. I tassi di guasto "
    "sono derivati da telemetria pubblicata di grandi cluster (tasso annuo di "
    f"guasto di package pari al {p2(d['AFR_PACKAGE']*100)}%, validato per via "
    "incrociata contro una stima indipendente entro l'1,4%). Otteniamo un risultato "
    "analitico: il recupero di componenti assorbe il flusso di guasti solo fino a "
    "una resa critica di cannibalizzazione "
    f"$\\kappa^{{*}} = \\lambda L$, pari a {p2(ks['central'])} con i parametri "
    "centrali, oltre la quale ulteriore capacità di recupero non produce alcun "
    "beneficio e il decadimento è governato dalla sola obsolescenza, mentre al di "
    "sotto i guasti non riparati accelerano il declino fino al "
    f"{SAT['excess_at_zero_pct']:.0f}%. Poiché la memoria ad alta banda è integrata "
    "nello stesso package del die e nessuno dei due è sostituibile sul campo, "
    "l'intervallo plausibile per gli acceleratori è a cavallo di questa soglia. "
    "Applicando il modello a tre giurisdizioni, collochiamo l'uscita dalla "
    f"frontiera fra {mo(EU['t_frontier_med'])} e {mo(US['t_frontier_med'])} mesi, "
    "governata da $T_f \\simeq T_{\\mathrm{dbl}}\\log_2(C_0/\\theta F_0)$: il "
    "parco installato compra tempo solo in modo **logaritmico**, sicché un ordine "
    "di grandezza in più di calcolo compra circa 17 mesi ulteriori, e il "
    "decadimento hardware pesa solo per il 13-14% dell'intervallo. Le soglie di "
    "sovranità mediane sono il "
    f"{p1(US['floor_med'])}% per gli Stati Uniti, il {p1(CN['floor_med'])}% per "
    f"la Cina, il cui intervallo al 90% spazia però dal {p1(CN['floor_p05'])}% "
    f"al {p1(CN['floor_p95'])}%, sicché l'autosufficienza cinese è, sui dati "
    f"pubblici attuali, genuinamente indeterminata, e il {p1(EU['floor_med'])}% per "
    "l'Unione Europea. L'analisi di sensibilità mostra che il ritmo di avanzamento "
    "della frontiera domina l'attrito hardware di sette volte. L'implicazione di "
    "policy è che la recisione non deve distruggere il calcolo dell'avversario: "
    "dove anche l'accesso remoto è interdetto, basta congelarlo mentre la "
    "frontiera avanza."
)

BODY = [

# ══ 1 ════════════════════════════════════════════════════════════════════════
("h1", "1  Introduzione"),

("p",
 "Ogni argomento a favore del controllo delle esportazioni di hardware per "
 "l'intelligenza artificiale poggia su un'affermazione relativa al tempo. "
 "Limitare l'accesso di un avversario agli acceleratori avanzati *farebbe "
 "guadagnare* qualcosa: un vantaggio, una finestra, un ritardo prima della "
 "parità di capacità. L'affermazione è temporale, quantitativa e, per quanto "
 "abbiamo potuto accertare, non quantificata. Nessun lavoro pubblicato indica "
 "per quanto tempo una giurisdizione recisa dalla catena globale di fornitura "
 "degli acceleratori potrebbe sostenere il parco di calcolo che già possiede."),

("p",
 "Non è per carenza di misurazione. La capacità nazionale di intelligenza "
 "artificiale è oggi una delle grandezze più intensamente indicizzate delle "
 "politiche tecnologiche. Almeno undici strumenti pubblici classificano le "
 "giurisdizioni secondo qualche combinazione di calcolo installato, energia, "
 "talento, produzione di modelli e capacità di governance. Differiscono per "
 "costruzione e per trasparenza, ma condividono una proprietà strutturale: "
 "ciascuno è una **fotografia delle dotazioni**. Rispondono alla domanda *che "
 "cosa possiede un paese?* Nessuno risponde alla domanda *che cosa "
 "conserverebbe?*"),

("p",
 "La distinzione conta perché il calcolo installato non è una riserva. È una "
 "flotta di capitale con un tasso di guasto misurabile, una vita economica "
 "controversa, una dipendenza da una fornitura di memoria concentrata a parte, e "
 "una capacità che si definisce rispetto a una frontiera che non sta ferma. Una "
 "riserva aurea non si corrode; un parco di acceleratori sì. Trattare le due cose "
 "allo stesso modo è l'errore di modellazione che questo articolo intende "
 "correggere."),

("p",
 "La letteratura sull'affidabilità ha misurato con precisione il tasso di "
 "corrosione, ma sotto un'ipotesi che ne annulla l'uso in questo contesto. La "
 "telemetria dei grandi cluster fornisce statistiche di guasto ben "
 "caratterizzate, e l'analisi più autorevole sulla questione se tali guasti "
 "limitino la scalabilità conclude di no, dichiarando però esplicitamente di "
 "assumere che i nodi di ricambio restino acquistabili e di non trattare le "
 "interruzioni della catena di fornitura né le situazioni in cui i chip di "
 "sostituzione non possano essere procurati. È precisamente questa l'ipotesi che "
 "la recisione rimuove. Rimuoverla è il contributo del presente lavoro."),

("h2", "1.1  Contributo"),
("numbers", [
 "**Un modello di decadimento del calcolo installato in regime di recisione.** "
 "Trattiamo un parco nazionale di acceleratori come una flotta deperibile "
 "soggetta a guasto, obsolescenza, recupero parziale di componenti e "
 "sostituzione interna limitata, integrandola mensilmente. I parametri di guasto "
 "sono derivati da telemetria pubblicata anziché assunti, e validati per via "
 "incrociata contro una stima indipendente.",
 "**Tre grandezze riportabili.** L'emivita del calcolo $T_{1/2}$, il tempo di "
 "uscita dalla frontiera $T_f$ e la soglia di sovranità $C_\\infty$, la "
 "capacità che una giurisdizione conserva asintoticamente con la sola produzione "
 "interna. $C_\\infty$ è, sosteniamo, la grandezza che il termine *sovranità* ha "
 "indicato finora senza mai riceverne un numero.",
 "**Una soglia analitica.** Il recupero di componenti sostiene un parco "
 "installato solo al di sopra di una resa critica di cannibalizzazione "
 "$\\kappa^{*} = \\lambda L$. È una proprietà dell'hardware, non delle "
 "politiche, e separa due regimi di recisione qualitativamente diversi.",
 "**Un risultato negativo riportato per intero.** Abbiamo tentato di calibrare "
 "il modello sull'unica recisione osservata di una flotta di capitale "
 "comparabile, l'aviazione civile russa dopo il febbraio 2022, e la "
 "calibrazione fallisce. Riportiamo il fallimento, ne diagnostichiamo la causa e "
 "spieghiamo perché esso vincola l'analogia e non il modello.",
]),

("p",
 "Deliberatamente non proponiamo un ulteriore indice. Il campo ne conta undici, e "
 "un undicesimo e mezzo non sarebbe né originale né utile. Gli indici esistenti "
 "entrano in questo articolo come input e come letteratura di riferimento, non "
 "come concorrenti."),

# ══ 2 ════════════════════════════════════════════════════════════════════════
("h1", "2  Letteratura di riferimento"),

("h2", "2.1  Misurare la capacità tecnologica nazionale"),
("p",
 "Gli indici compositi di capacità tecnologica sono numerosi e metodologicamente "
 "maturi. Il Machinepower Index (2026) valuta venticinque giurisdizioni su dodici "
 "celle raggruppate in Watts, Weights e Will, aggregando con una media a "
 "elasticità di sostituzione costante con $\\sigma = 0,33$, così che una singola "
 "cella debole vincoli il totale anziché essere annullata dalla media; la sua "
 "stessa documentazione registra che il 37% delle misurazioni sottostanti è "
 "giudizio dell'analista e che non è modellata alcuna dimensione temporale, né "
 "decadimento, ammortamento, tasso di guasto o scenario di recisione. Il "
 "Sovereign AI Index del CNAS (2026) cataloga oltre 139 progetti sostenuti da "
 "Stati e rileva che la maggior parte resta dipendente da tecnologia estera, "
 "prevalentemente statunitense, lungo l'intero stack; non è, esplicitamente, un "
 "modello di dipendenza e recisione. Gli strumenti accademici hanno struttura "
 "analoga: Lee et al. (2024) scompongono la sovranità tecnologica in capacità di "
 "innovazione, capacità produttiva e indipendenza della catena di fornitura per "
 "l'industria dei semiconduttori; Caravella et al. (2023) tracciano le dipendenze "
 "strategiche lungo la filiera fotovoltaica; Cai et al. (2026) passano in "
 "rassegna 104 articoli su politica industriale dei semiconduttori e governance "
 "degli ecosistemi regionali. Strumenti più ampi, il Government AI Readiness "
 "Index, il Global AI Index, l'AI Index annuale, estendono la copertura senza "
 "modificare la logica temporale."),
("p",
 "Ognuno di questi è trasversale nel tempo. La letteratura metodologica sugli "
 "indicatori compositi è essa stessa esplicita nel riconoscere che ponderazione, "
 "aggregazione e robustezza sono il punto in cui simili strumenti riescono o "
 "falliscono (Greco et al., 2018; Dobbie et al., 2013; Kelemen et al., 2024; "
 "OCSE/JRC, 2008), e ne adottiamo la disciplina più avanti. Ma nessuna cura "
 "nell'aggregazione converte una fotografia in una traiettoria."),

("h2", "2.2  Governance del calcolo e affidabilità degli acceleratori"),
("p",
 "Sastry et al. (2024) stabiliscono il quadro di riferimento: la potenza di "
 "calcolo è un oggetto trattabile di policy perché è rilevabile, escludibile, "
 "quantificabile e prodotta attraverso una catena di fornitura estremamente "
 "concentrata. Queste quattro proprietà sono precisamente le condizioni che "
 "rendono possibile un modello di recisione; il presente articolo può essere "
 "letto come il successore quantitativo di quell'argomento qualitativo. La "
 "prassi regolatoria si è mossa nella stessa direzione, assumendo la potenza di "
 "elaborazione cumulata, e non il conteggio delle unità, come grandezza "
 "controllata."),
("p",
 "Sul versante hardware, Grattafiori et al. (2024) riportano statistiche di "
 "interruzione risolte per componente per un addestramento su 16.384 "
 "acceleratori, e Kokolis et al. (2025) stimano modelli di guasto su oltre 150 "
 "milioni di ore-acceleratore distribuite su due cluster di produzione. "
 "L'analisi di Epoch AI conclude che il guasto hardware non limiterà la "
 "scalabilità, in regime di rifornimento continuo. È la nostra lettura di "
 "quella condizione al contorno, dichiarata nella fonte stessa, a motivare "
 "questo lavoro."),

("p",
 "Una terza tradizione è più vicina di entrambe e va riconosciuta: la "
 "modellistica militare del sostegno logistico. Il METRIC di Sherbrooke (1968) e "
 "la tradizione multi-echelon che ha fondato ottimizzano le scorte di ricambi "
 "recuperabili per la disponibilità di flotta, e le sue estensioni moderne "
 "incorporano esplicitamente la cannibalizzazione. È il parente quantitativo più "
 "prossimo del nostro termine di recupero, e ne prendiamo in prestito il "
 "lessico. Differisce esattamente sui margini che servono a questo articolo: "
 "ottimizza l'inventario sotto una filiera di rifornimento funzionante anziché "
 "sotto recisione totale, e i suoi sistemi non affrontano alcuna frontiera di "
 "capacità in movimento, un velivolo che vola è disponibile, mentre un "
 "acceleratore che funziona può essere già strategicamente obsoleto. La soglia "
 "$\\kappa^{*}$ va dunque letta come il limite in regime di recisione di quella "
 "tradizione, non come la pretesa di aver scoperto la cannibalizzazione."),

("h2", "2.3  Statecraft economico e punti di strozzatura"),
("p",
 "Farrell e Newman (2019) forniscono il quadro teorico: una topologia di rete "
 "asimmetrica consente agli Stati che hanno giurisdizione sui nodi centrali di "
 "esercitare un *effetto panopticon* e un *effetto punto di strozzatura*, il "
 "secondo dei quali nega l'accesso alla rete agli avversari. Beaumier et al. "
 "(2023) applicano l'analisi di rete direttamente ai semiconduttori, "
 "scomponendo la filiera in reti di progettazione, materie prime, "
 "apparecchiature di produzione e chip assemblati, e mostrando come la "
 "centralità in una consenta di rendere arma un'altra. Fuller (2026) sostiene "
 "che il quadro si trasferisca imperfettamente ai beni fisici, dove un punto di "
 "strozzatura si intende meglio come un input senza il quale un compito non può "
 "proseguire, formulazione che si sovrappone strettamente al modello qui "
 "sviluppato."),
("p",
 "La valutazione quantitativa dei controlli si è concentrata sugli aggregati "
 "economici. Park e Liu (2023) impiegano metodi input-output multiregionali; Cui "
 "et al. (2025) adottano un modello di equilibrio economico generale dinamico per "
 "stimare gli effetti sul PIL dell'embargo sui chip e dei contro-controlli cinesi "
 "su gallio, germanio e grafite; Shrivastava et al. (2025) valutano l'elusione. "
 "La resilienza delle filiere è stata modellata con topologie a cascata scale-free "
 "e reti bayesiane. Tutto ciò misura la **conseguenza economica**. Nessuno misura "
 "il **decadimento della capacità nel tempo**."),
("p",
 "L'analisi di settore è quella che vi si avvicina di più. Sono state pubblicate "
 "stime del momento in cui una scorta di die non assemblati si esaurirà, "
 "compresa una formulazione zero-inflated che assegna circa il 56% di probabilità "
 "all'esaurimento di una di tali scorte entro il gennaio 2026. Quel lavoro "
 "modella lo *smaltimento di magazzino*, componenti in attesa di assemblaggio. "
 "Il presente articolo modella il *decadimento del parco installato*, hardware "
 "già dispiegato e in funzione. Sono due domande diverse con matematiche diverse, "
 "e ci limitiamo scrupolosamente a rivendicare la seconda."),

("quote",
 "La letteratura esistente misura ciò che una giurisdizione possiede, ciò che "
 "può costruire e quanto la recisione costi alla sua economia. Questo articolo "
 "misura per quanto tempo ciò che possiede continui a funzionare."),

# ══ 3 ════════════════════════════════════════════════════════════════════════
("h1", "3  Il modello"),

("h2", "3.1  Impostazione"),
("p",
 "Sia $N(t)$ il numero di acceleratori operativi, in equivalenti-H100 (H100e), al "
 "mese $t$ successivo alla recisione, con $N(0) = C_0$. Il calcolo nazionale "
 "effettivo è"),
("eq", "C(t) \\;=\\; N(t)\\,u(t)", "1"),
("p",
 "dove $u(t) \\in (0,1]$ è un tetto di utilizzo imposto da vincoli energetici, di "
 "interconnessione e operativi. Tre flussi agiscono su $N$ in ciascun periodo. I "
 "guasti hardware avvengono con rischio mensile "
 "$\\lambda = -\\ln(1-\\mathrm{AFR})/12$. L'obsolescenza ritira unità al tasso "
 "$\\delta = 1/L$, con $L$ la vita utile in mesi; le unità ritirate restano "
 "fisicamente integre. La sostituzione arriva come produzione interna più "
 "dispersione, $R = R_{\\mathrm{int}} + R_{\\mathrm{disp}}$."),
("p",
 "Il meccanismo che distingue la recisione dal funzionamento ordinario è il "
 "recupero di componenti. In regime di rifornimento un'unità guasta viene "
 "sostituita e $N$ resta invariato, ed è per questo che le analisi di "
 "affidabilità concludono che i guasti non vincolano. In regime di recisione "
 "l'unica fonte di riparazione sono le altre unità. Sia $P(t)$ il bacino di "
 "riparazioni recuperabili e sia $\\kappa$ la *resa di cannibalizzazione*: il "
 "numero di riparazioni ricavabili da una unità donatrice. Allora"),
("eq",
 "\\begin{aligned}"
 "F_t &= N_t\\lambda, \\qquad \\mathrm{Rit}_t = N_t\\delta \\\\"
 "\\rho_t &= \\min(F_t,\\;P_t) \\\\"
 "P_{t+1} &= P_t - \\rho_t + \\kappa\\,(F_t - \\rho_t + \\mathrm{Rit}_t) \\\\"
 "N_{t+1} &= N_t - F_t - \\mathrm{Rit}_t - S_t + \\rho_t + R"
 "\\end{aligned}", "2"),
("p",
 "dove $S_t$ è il numero di unità *ancora efficienti* ritirate volontariamente "
 "per ricavarne componenti. Il ritiro è razionale solo quando una donatrice rende "
 "più di una riparazione, cosicché $S_t > 0$ richiede $\\kappa > 1$; lo limitiamo "
 "al 3% della flotta al mese."),

("h2", "3.2  La resa critica di cannibalizzazione"),
("p",
 "Il bacino di recupero è alimentato dalle unità che escono dal servizio e "
 "prosciugato dalle riparazioni. I soli ritiri sostengono il flusso di "
 "riparazione quando $\\kappa N\\delta \\geq N\\lambda$, il che fornisce una "
 "soglia indipendente dalla dimensione della flotta, dagli afflussi e dalle "
 "politiche:"),
("eq", "\\kappa^{*} \\;=\\; \\frac{\\lambda}{\\delta} \\;=\\; \\lambda L", "3"),
("p",
 "$\\kappa^{*}$ è una soglia di **saturazione**, non di sopravvivenza, e la "
 "distinzione conta. Al di sopra, il recupero assorbe di fatto l'intero flusso di "
 "guasti e il parco installato declina al solo tasso di obsolescenza; ulteriore "
 "capacità di recupero non produce alcun beneficio. Al di sotto, i guasti non "
 "riparati si sommano ai ritiri e, con $\\kappa = 0$, il parco si contrae del "
 f"{SAT['excess_at_zero_pct']:.0f}% più rapidamente di quanto la sola obsolescenza "
 "implicherebbe. Ciò che $\\kappa^{*}$ separa è dunque un regime *limitato dai "
 "guasti* da uno *limitato dall'obsolescenza*. Non separa la sopravvivenza dal "
 "collasso: in assenza di afflussi di sostituzione ogni parco declina, perché il "
 "ritiro rimuove unità indipendentemente dalla riparazione dei guasti. "
 "$\\kappa^{*}$ è una proprietà dell'hardware, del suo tasso di guasto e della "
 "sua vita utile, non della giurisdizione che lo detiene. L'Appendice A ne "
 "riporta la derivazione; il §5.1 la verifica."),
("p",
 "È qui che l'architettura fisica degli acceleratori diventa decisiva, ed è qui "
 "che l'analogia con altre flotte di capitale si rompe. Una cellula aeronautica è "
 "ricca di ricambi: si scompone in migliaia di unità sostituibili che si "
 "guastano indipendentemente, e la prassi osservata sotto sanzioni è stata "
 "smontare circa un velivolo per tenerne in volo una decina, il che implica "
 "$\\kappa \\approx 10$. Un acceleratore per IA è povero di ricambi esattamente "
 "nel punto sbagliato. La memoria ad alta banda è integrata nello stesso package "
 "del die logico su un interposer condiviso; né il die né lo stack di memoria "
 "sono unità sostituibili sul campo. I due modi di guasto dominanti sono dunque "
 "non recuperabili **per costruzione**, e la cannibalizzazione recupera soltanto "
 "componenti accessorie del nodo, alimentatori, interfacce di rete, "
 "raffreddamento, che non sono i modi di guasto vincolanti. Assumiamo "
 "$\\kappa \\in [0,05; 0,50]$ per gli acceleratori e trattiamo il valore "
 "aeronautico come limite superiore appartenente a una diversa classe di "
 "hardware."),

("h2", "3.3  Grandezze riportate"),
("bullets", [
 "**Emivita del calcolo $T_{1/2}$**, mesi necessari perché il calcolo effettivo "
 "scenda sotto la metà del valore al giorno della recisione. Censurata a destra "
 "all'orizzonte di 120 mesi.",
 "**Tempo di uscita dalla frontiera $T_f$**, mesi necessari perché la capacità "
 "nazionale scenda sotto una quota soglia $\\theta = 0,10$ della scala di "
 "addestramento di frontiera contemporanea $F(t) = F_0\\,2^{t/T_{\\mathrm{ddp}}}$, "
 "dove $F_0$ è un ancoraggio **assoluto e comune a tutte le giurisdizioni**. Una "
 "versione precedente normalizzava invece rispetto al $C_0$ di ciascuna "
 "giurisdizione, il che imponeva a tutte di partire alla pari e faceva cancellare "
 "identicamente $C_0$; l'apparente invarianza rispetto allo stock che ne "
 "derivava era un artefatto algebrico ed è stata ritirata (§5.3, Appendice A).",
 "**Soglia di sovranità $C_\\infty$**, il livello asintotico come quota di "
 "$C_0$, sostenibile con tutti gli afflussi non recisi, produzione interna *e* "
 "dispersione residua, mantenuti al tasso del giorno della recisione. Una forma "
 "chiusa esiste ed è riportata nell'Appendice A; riproduce esattamente "
 "l'integrazione a 900 mesi. $C_\\infty$ è definita solo per crescita "
 "dell'indigenizzazione nulla (§7.4).",
]),

# ══ 4 ════════════════════════════════════════════════════════════════════════
("p",
 "L'ancoraggio $F_0$ merita una derivazione alla luce del sole, poiché $T_f$ lo "
 "eredita attraverso il logaritmo. Un addestramento di frontiera da $10^{26}$ a "
 "$10^{27}$ FLOP, eseguito in circa tre mesi su acceleratori che sostengono "
 "$4 \\times 10^{14}$ FLOP/s effettivi, corrisponde a circa "
 "$3 \\times 10^{21}$ FLOP per acceleratore e dunque a $3 \\times 10^{4}$ "
 "fino a $3 \\times 10^{5}$ H100e per esecuzione. Le stime correnti delimitano "
 "lo stesso intervallo: la prima esecuzione dichiarata sopra $10^{26}$ FLOP è "
 "stata Grok 3 nel febbraio 2025, a circa $3 \\times 10^{26}$; la più grande a "
 "oggi è Grok 4; ed Epoch AI colloca il superamento di $10^{26}$ da parte del "
 "primo modello di frontiera attorno al gennaio 2026. Percorriamo quindi $F_0$ "
 "in modo log-uniforme fra $5 \\times 10^{4}$ e $5 \\times 10^{5}$ H100e con "
 "valore centrale $1{,}5 \\times 10^{5}$, e ogni $T_f$ riportato incorpora tale "
 "incertezza."),

("h1", "4  Dati e parametri"),

("h2", "4.1  Tassi di guasto derivati dalla telemetria dei cluster"),
("p",
 "Grattafiori et al. (2024) riportano 419 interruzioni inattese in una finestra "
 "di pre-addestramento di 54 giorni su un cluster di un massimo di 16.384 "
 "acceleratori H100, risolte per causa: acceleratore difettoso 148 (30,1%), "
 "memoria HBM3 dell'acceleratore 72 (17,2%), switch o cavo di rete 35 (8,4%). "
 "Annualizzando per acceleratore,"),
("eq",
 "\\mathrm{AFR} \\;=\\; \\frac{n_{\\mathrm{eventi}}}{16{,}384}\\times"
 "\\frac{365}{54}", "4"),
("p",
 f"si ottiene il {p2(d['AFR_GPU_DIE']*100)}% annuo per i guasti del die e il "
 f"{p2(d['AFR_HBM']*100)}% per la HBM3, dunque un **tasso di guasto di package "
 f"del {p2(d['AFR_PACKAGE']*100)}% annuo** per i due modi non sostituibili sul "
 f"campo, e il {p2(d['AFR_ALL']*100)}% considerando tutte le cause di "
 f"interruzione. Come verifica indipendente, il dato onnicomprensivo corrisponde "
 f"a un'interruzione ogni {n0(d['xcheck_gpu_hours_per_failure'])} "
 f"ore-acceleratore, contro circa {n0(d['epoch_reported'])} riportate da Epoch AI "
 f"sulla medesima esecuzione, un accordo entro l'1,4%. Assumiamo il tasso di "
 f"package come valore centrale e percorriamo l'intero intervallo nel Monte "
 "Carlo. Una cautela accompagna questi tassi: i conteggi delle interruzioni non "
 "distinguono la morte definitiva dell'hardware dai guasti transitori risolti "
 "con un riavvio, sicché, nella misura in cui alcune interruzioni attribuite al "
 "die erano recuperabili, il tasso di package sovrastima l'attrito permanente. "
 "La direzione di questa distorsione è benigna per le nostre conclusioni: un "
 "$\\lambda$ più basso allunga $T_{1/2}$, alza le soglie e lascia $T_f$ quasi "
 "invariato."),

("h2", "4.2  Parco installato"),
("p",
 "Epoch AI stima uno stock globale consegnato di circa 15 milioni di H100e e "
 "pubblica dati risolti per proprietario. Per la Cina deriviamo $C_0$ da una "
 "relazione pubblicata anziché da un'ipotesi: la stima mediana di 660.000 H100e "
 "dirottati entro il 2025 è descritta come pari a circa un terzo della capacità "
 f"totale cinese, da cui $C_0 \\approx$ {n0(d['C0_CHINA'])} H100e. L'intervallo "
 "al 90% sulla stima di contrabbando (290.000-1.600.000) è propagato "
 "direttamente."),
("p",
 "**Questo è il limite principale dei dati dello studio e lo dichiariamo "
 "apertamente.** Epoch risolve la proprietà per *impresa*, non per "
 "*giurisdizione*. Attribuire a un paese il parco di un operatore multinazionale "
 "richiede ipotesi non pienamente difendibili sulla base di dati pubblici. "
 "Percorriamo quindi la quota statunitense fra il 60% e il 78% e quella "
 "dell'Unione Europea fra il 2% e il 6% dello stock globale, e riportiamo i "
 "risultati europei con confidenza corrispondentemente bassa. Nessuna "
 "conclusione di questo articolo dipende da una stima puntuale dello stock "
 "nazionale."),

("h2", "4.3  La recisione è modellata in modo simmetrico"),
("p",
 "Una giurisdizione è recisa dagli input che non controlla. Vale la pena "
 "sottolineare che non si tratta di uno scenario specificamente cinese. Gli Stati "
 "Uniti non dispongono di una fonte interna di litografia a ultravioletto "
 "estremo, detengono capacità di produzione all'avanguardia solo parziale e "
 "ancora in fase di avviamento, e non producono memoria ad alta banda su scala, "
 "la fornitura di HBM è concentrata per circa il 90% in due imprese coreane. La "
 "copertura interna statunitense in regime di recisione dai propri alleati è "
 "dunque una banda di scenario (15-35%), non l'unità. All'Unione Europea, priva "
 "di produzione di logica all'avanguardia in esercizio, è assegnato l'1-4%."),

("table", "Parametri del modello, intervalli e fonti.", "1",
 ["Simbolo", "Parametro", "Centrale", "Intervallo", "Fonte"],
 [["$\\lambda$", "Tasso di guasto package (annuo)",
   f"{p2(d['AFR_PACKAGE']*100)}%",
   f"{p2(d['AFR_GPU_DIE']*100)}-{p2(d['AFR_ALL']*100)}%",
   "Derivato, Grattafiori et al. (2024)"],
  ["$\\kappa$", "Resa di cannibalizzazione", "0,275", "0,05-0,50",
   "Architettura del package (§3.2)"],
  ["$L$", "Vita utile (anni)", "4,0", "2,0-6,0",
   "Controversia sull'ammortamento, 2025-26"],
  ["$T_{\\mathrm{ddp}}$", "Raddoppio frontiera (mesi)", "5,2", "4,8-7,0",
   "Epoch AI, serie dell'*addestramento* di frontiera"],
  ["$F_0$", "Ancoraggio di frontiera (H100e)", "150.000", "50k-500k",
   "Derivato; v. §3.3. Percorso log-uniforme"],
  ["$\\theta$", "Soglia di competitività", "0,10", "fissa",
   "Convenzione; entra via logaritmo (§5.3)"],
  ["$\\mathrm{cov}$", "Copertura interna USA / UE", "0,25 / 0,02",
   "0,15-0,35 / 0,01-0,04", "**Assunzione, senza base osservativa**"],
  ["$C_0^{\\mathrm{CN}}$", "Stock Cina (H100e)", n0(d['C0_CHINA']),
   "0,87-4,80 mln", "Derivato, Epoch AI"],
  ["$C_0^{\\mathrm{US}}$", "Stock USA (H100e)", n0(d['C0_US']),
   "9,0-11,7 mln", "Epoch AI, quota variata"],
  ["$C_0^{\\mathrm{EU}}$", "Stock UE (H100e)", n0(d['C0_EU']),
   "0,3-0,9 mln", "Scenario, confidenza bassa"],
  ["$R_{\\mathrm{int}}$", "Produzione interna Cina (H100e/mese)",
   n0(d['cn_domestic_pm'] * 0.65), "30-100% del tasso 2025",
   "Output realizzato (Epoch AI) × dipendenza dalle scorte"],
  ["$R_{\\mathrm{disp}}$", "Dispersione (H100e/mese)",
   n0(d['leak_pm'] * 0.35), "10-60% della base",
   "Derivato, Epoch AI (2026)"]],
 "H100e = equivalenti-H100. Gli intervalli sono propagati con un Monte Carlo a "
 "10.000 estrazioni con campionamento uniforme indipendente. L'indipendenza è "
 "essa stessa un'assunzione: correlazioni plausibili fra i parametri, fra vita "
 "utile e tasso di guasto, o fra stock e capacità interna, non sono modellate."),

# ══ 5 ════════════════════════════════════════════════════════════════════════
("h1", "5  Risultati"),

("h2", "5.1  L'intervallo plausibile è a cavallo della soglia"),
("p",
 f"Con i parametri centrali $\\kappa^{{*}} = {p2(ks['central'])}$. Sull'intera "
 "griglia dei parametri varia da 0,13 (soli guasti del die, vita utile biennale) "
 "a 1,14 (tutte le cause, vita utile sessennale). L'intervallo plausibile per gli "
 "acceleratori, $[0,05; 0,50]$, **è a cavallo della soglia centrale**. La misura "
 "diretta sul modello integrato conferma l'algebra: contro un declino da soli "
 f"ritiri pari al {p2(SAT['retirement_only']*100)}% mensile, il parco si contrae "
 f"del {p2(SAT['r_zero']*100)}% al mese con $\\kappa = 0$ "
 f"(eccesso del {SAT['excess_at_zero_pct']:.0f}%), scendendo al "
 f"{p2(SAT['r_at_kstar']*100)}% in corrispondenza di $\\kappa^{{*}}$ "
 f"(eccesso del {SAT['excess_at_kstar_pct']:.0f}%), dopo di che triplicare "
 "$\\kappa$ lo modifica di meno del 2%. Un parco al di sotto della soglia paga "
 "quindi una penalità cumulativa, mentre uno al di sopra non trae alcun vantaggio "
 "da ulteriore capacità di recupero. Stabilire empiricamente $\\kappa$ è, su "
 "questa analisi, la misurazione di maggior valore che il campo potrebbe "
 "intraprendere."),
("p",
 "La soglia interagisce con la controversia sull'ammortamento in un modo che vale "
 "la pena esplicitare. Poiché $\\kappa^{*} = \\lambda L$ cresce con la vita "
 "utile, un parco più longevo si colloca più in basso rispetto a qualunque "
 "capacità di recupero fissata: sull'intervallo conteso di due-sei anni la quota "
 f"di guasti che il recupero può assorbire scende dal "
 f"{LIFE[0]['failures_absorbed_pct']:.0f}% al "
 f"{LIFE[-1]['failures_absorbed_pct']:.0f}%. Abbiamo verificato, e respinto, "
 "l'inferenza allettante che i parchi più longevi siano perciò complessivamente "
 "più fragili: il tempo di dimezzamento senza afflussi *cresce* da "
 f"{LIFE[0]['t_half_months_zero_inflow']:.0f} a "
 f"{LIFE[-1]['t_half_months_zero_inflow']:.0f} mesi sullo stesso intervallo, "
 "perché il ritiro più lento prevale. L'affermazione difendibile è più stretta: "
 "un parco a sei anni sopravvive più a lungo in termini assoluti, ma dipende di "
 "più dallo stock grezzo e di meno dalla riparazione. Riportiamo l'ipotesi "
 "respinta perché è allettante, citabile e falsa."),
("fig", os.path.join(FIG, "fig7_kappa_critica.png"),
 "La resa critica di cannibalizzazione $\\kappa^{*} = \\lambda L$ in funzione "
 "della vita utile, per tre ipotesi sul tasso di guasto. La banda ombreggiata è "
 "l'intervallo plausibile per gli acceleratori di IA, dato che la memoria ad alta "
 "banda è integrata nello stesso package e non è sostituibile sul campo. La banda "
 "interseca tutte e tre le curve: che il recupero sostenga un parco installato "
 "dipende dal regime, non è una questione di grado.", "1"),

("h2", "5.2  Traiettorie e grandezze riportate"),
("p",
 "La Tabella 2 riporta mediane e intervalli al 90% su 10.000 estrazioni per "
 "giurisdizione. L'uscita dalla frontiera avviene fra "
 f"{mo(EU['t_frontier_med'])} e {mo(US['t_frontier_med'])} mesi, ordinata "
 "secondo il parco installato come la relazione analitica del §5.3 richiede. "
 "Alla mediana nessuna giurisdizione raggiunge l'autosufficienza, ma le soglie "
 "vanno lette con doppia cautela: per Stati Uniti e Unione Europea sono il "
 "parametro di copertura interna assunto, riscalato di un fattore limitato, non "
 f"un esito indipendente del modello (§7.2), mentre l'intervallo al 90% della "
 f"Cina raggiunge il {p1(CN['floor_p95'])}%, sopra la parità. Le soglie di "
 "sovranità mediane sono il "
 f"{p1(US['floor_med'])}% per gli Stati Uniti, il {p1(CN['floor_med'])}% per la "
 f"Cina e il {p1(EU['floor_med'])}% per l'Unione Europea."),

("table", "Grandezze riportate per giurisdizione. Mediane con intervalli al 90%, "
          "10.000 estrazioni Monte Carlo.", "2",
 ["Giurisdizione", "$C_0$ (mln H100e)", "$T_{1/2}$ (mesi)", "$T_f$ (mesi)",
  "$C_\\infty$ (% di $C_0$)", "$P(T_{1/2}\\!\\leq\\!36)$"],
 [["Cina", it(f"{CN['C0_h100e']/1e6:.2f}"),
   f"{mo(CN['t_half_med'])} [{mo(CN['t_half_p05'])}-{mo(CN['t_half_p95'])}]",
   f"{mo(CN['t_frontier_med'])} [{mo(CN['t_frontier_p05'])}-{mo(CN['t_frontier_p95'])}]",
   f"{p1(CN['floor_med'])} [{p1(CN['floor_p05'])}-{p1(CN['floor_p95'])}]",
   f"{p1(CN['p_half_within_36m'])}%"],
  ["Stati Uniti", it(f"{US['C0_h100e']/1e6:.2f}"),
   f"{mo(US['t_half_med'])} [{mo(US['t_half_p05'])}-{mo(US['t_half_p95'])}]",
   f"{mo(US['t_frontier_med'])} [{mo(US['t_frontier_p05'])}-{mo(US['t_frontier_p95'])}]",
   f"{p1(US['floor_med'])} [{p1(US['floor_p05'])}-{p1(US['floor_p95'])}]",
   f"{p1(US['p_half_within_36m'])}%"],
  ["Unione Europea", it(f"{EU['C0_h100e']/1e6:.2f}"),
   f"{mo(EU['t_half_med'])} [{mo(EU['t_half_p05'])}-{mo(EU['t_half_p95'])}]",
   f"{mo(EU['t_frontier_med'])} [{mo(EU['t_frontier_p05'])}-{mo(EU['t_frontier_p95'])}]",
   f"{p1(EU['floor_med'])} [{p1(EU['floor_p05'])}-{p1(EU['floor_p95'])}]",
   f"{p1(EU['p_half_within_36m'])}%"]],
 f"$T_{{1/2}}$ è censurata a destra a 120 mesi. Le estrazioni censurate sono "
 f"conservate ordinalmente, sicché ogni quantile che cada nella massa censurata "
 f"è riportato come '>120' anziché come valore finito; la censura riguarda il "
 f"{p1(CN['t_half_censored_pct'])}% delle estrazioni cinesi e il "
 f"{p1(US['t_half_censored_pct'])}% di quelle statunitensi. I valori europei "
 f"hanno confidenza bassa perché i dati di stock risolti per giurisdizione sono "
 f"i più deboli (§4.2)."),

("fig", os.path.join(FIG, "fig1_decadimento_giurisdizioni.png"),
 "Decadimento del calcolo effettivo dopo la recisione, caso centrale. La "
 "traiettoria europea è la più rapida nonostante la minore esposizione assoluta, "
 "perché la sostituzione interna copre la quota più bassa del proprio attrito.", "2"),

("fig", os.path.join(FIG, "fig2_montecarlo_cina.png"),
 "Distribuzione Monte Carlo per la Cina, 10.000 estrazioni con campionamento "
 "uniforme indipendente su tutti i parametri della Tabella 1. L'ampiezza "
 "dell'intervallo al 90% riflette il campionamento congiunto di tutti i "
 "parametri; poiché gli afflussi cinesi sono assoluti e non proporzionali allo "
 "stock, contribuisce anche l'incertezza su $C_0$.", "3"),

("h2", "5.3  L'orologio della frontiera domina l'attrito hardware"),
("p",
 "Il risultato rilevante non è il decadimento dell'hardware, ma la sua modesta "
 "quota dell'intervallo. La Figura 4 rappresenta la capacità rispetto alla scala "
 "di frontiera contemporanea. Trascurando del tutto il decadimento, il tempo di "
 "uscita segue"),
("eq", r"T_f \simeq T_{\mathrm{ddp}}\,\log_2\left(\frac{C_0}{\theta F_0}\right)", "5"),
("p",
 "che riproduce i casi centrali simulati entro quattro mesi (analitico 36,6 / "
 "49,1 / 27,7 contro simulato 36 / 45 / 24 per Cina, Stati Uniti e Unione "
 "Europea). Ne discendono due conseguenze, che sostituiscono l'affermazione di "
 "invarianza rispetto allo stock avanzata in una versione precedente."),
("bullets", [
 "**Il parco installato compra tempo solo in modo logaritmico.** Con "
 "$T_{\\mathrm{ddp}} = 5,2$ mesi, un parco dieci volte più grande compra "
 "$T_{\\mathrm{ddp}}\\log_2 10 \\approx 17$ mesi ulteriori, e uno cento volte "
 "più grande soltanto 35. L'accumulo di scorte è soggetto a rendimenti "
 "fortemente decrescenti contro una frontiera in movimento, un'affermazione più "
 "forte e più utile di quella di invarianza che sostituisce, e a differenza di "
 "quella non è un artefatto di normalizzazione.",
 "**Il decadimento hardware pesa per una minoranza costante dell'intervallo.** "
 "Rieseguendo ciascun caso centrale con guasto e ritiro azzerati si ottengono 42 "
 "/ 52 / 28 mesi contro 36 / 45 / 24 con il decadimento: l'attrito costa 6 / 7 / "
 "4 mesi, cioè il **13-14% del bilancio** in tutte e tre le giurisdizioni. Il "
 "restante 86% è l'orologio della frontiera.",
]),
("p",
 "La lettura corretta è dunque più stretta dell'originale ma regge alla verifica: "
 "l'affidabilità dell'hardware non governa la posizione strategica in regime di "
 "recisione, ma neppure la posizione è indipendente da quanto hardware una "
 "giurisdizione detenga."),
("fig", os.path.join(FIG, "fig3_relativo_frontiera.png"),
 "Capacità relativa alla frontiera mobile, scala logaritmica. Tutte e tre le "
 "giurisdizioni partono da posizioni diverse perché i parchi installati "
 "differiscono; il declino quasi parallelo riflette il deflatore comune di "
 "frontiera. I tempi di attraversamento sono ordinati secondo lo stock e "
 "separati da circa $T_{\\mathrm{ddp}}\\log_2$ del rapporto fra gli stock.", "4"),
("p",
 "L'analisi di sensibilità conferma il meccanismo. Facendo variare il tempo di "
 f"raddoppio della frontiera nel suo intervallo di 4,8-7,0 mesi, $T_f$ si sposta "
 f"di {SENS[0]['span']:.0f} mesi; facendo variare il tasso di guasto sull'intero "
 f"intervallo derivato, si sposta di "
 f"{[s for s in SENS if 'Failure' in s['parameter']][0]['span']:.0f} mesi, una "
 "differenza di leva di sette volte. L'affidabilità dell'hardware, la "
 "grandezza che la letteratura ingegneristica misura con maggiore cura, è fra i "
 "parametri *meno* importanti per l'esito strategico."),
("fig", os.path.join(FIG, "fig4_tornado_sensibilita.png"),
 "Sensibilità univariata del tempo di uscita dalla frontiera, ordinata per "
 "ampiezza. Il ritmo di avanzamento della frontiera domina; resa di "
 "cannibalizzazione e tasso di guasto contano meno una volta fissato il regime.", "5"),

("p",
 "La soglia $\\theta = 0{,}10$ è una convenzione, e la sua influenza è del "
 "tutto trasparente: entra nell'Eq. 5 solo attraverso il logaritmo, sicché "
 "dimezzarla allunga ogni $T_f$ di esattamente un tempo di raddoppio, circa "
 "cinque mesi, e raddoppiarla lo accorcia della stessa quantità, lasciando "
 "intatti ordinamento e distanze. Verificato numericamente: 42 / 36 / 31 mesi "
 "per $\\theta$ = 0,05 / 0,10 / 0,20 nel caso centrale cinese."),

("h2", "5.4  Dipendenza dal regime"),
("p",
 "La Figura 6 mostra le traiettorie nei diversi regimi di cannibalizzazione. I "
 f"valori di $\\kappa$ superiori a $\\kappa^{{*}} = {p2(ks['central'])}$, "
 "compreso il valore aeronautico di 10, un ipotetico acceleratore riparabile sul "
 "campo a 1, e il limite superiore dell'intervallo plausibile a 0,5, sono "
 "indistinguibili, perché tutti e tre sono oltre la saturazione e il flusso di "
 "guasti è già interamente assorbito. Solo il limite inferiore, 0,05, si colloca "
 "abbastanza sotto la soglia da incidere sul declino. Il sistema non risponde con "
 "continuità a $\\kappa$: satura."),
("fig", os.path.join(FIG, "fig6_regimi_kappa.png"),
 "Decadimento in quattro regimi di cannibalizzazione. Le tre curve pari o "
 "superiori alla resa critica coincidono perché tutte sono oltre la saturazione: "
 "il flusso di guasti è già assorbito e la capacità aggiuntiva resta inutilizzata.", "6"),

("h2", "5.5  Recisione parziale: che cosa compra davvero la dispersione"),
("p",
 "I controlli reali non sono né completi né istantanei. Sono permeabili, per "
 "dirottamento, rivendita e triangolazione via paesi terzi, e l'entità di questa "
 "dispersione è precisamente la grandezza che le politiche di enforcement "
 "contendono. Percorrendo il termine di dispersione su quattro ordini di "
 "grandezza si separano due effetti che di solito vengono discussi come uno solo."),
("p",
 "I due orizzonti rispondono alla dispersione con elasticità molto diverse. Su "
 f"un intervallo da zero al {LK['max_pct_of_c0_per_yr']:.0f}% del parco "
 f"installato all'anno, la soglia di sovranità sale dal "
 f"{LK['floor_at_zero']:.0f}% al {LK['floor_at_max']:.0f}% di $C_0$, un fattore "
 f"{LK['floor_at_max']/max(LK['floor_at_zero'],1e-9):.0f}, mentre l'uscita "
 f"dalla frontiera passa solo da {LK['tf_at_zero']:.0f} a "
 f"{LK['tf_at_max']:.0f} mesi, una variazione del "
 f"{100*(LK['tf_at_max']/LK['tf_at_zero']-1):.0f}%. L'asimmetria discende "
 "direttamente dalla forma analitica: la soglia è uno stato stazionario "
 "determinato dagli afflussi e scala linearmente in essi, mentre $T_f$ vi entra "
 "attraverso un logaritmo e un denominatore che cresce esponenzialmente. "
 f"Raggiungere una soglia del 100% di $C_0$ costa circa il "
 f"{LK['floor100']['leak_pct_of_C0_per_yr']:.0f}% del parco installato all'anno "
 f"e compra {LK['floor100']['t_frontier'] - LK['tf_at_zero']:.0f} mesi "
 "aggiuntivi alla frontiera."),
("table", "Recisione parziale. Effetto della dispersione sui due orizzonti.", "3",
 ["Regime di dispersione", "H100e / mese", "% di $C_0$ all'anno", "$T_f$ (mesi)",
  "$C_\\infty$ (% di $C_0$)"],
 [["Nessuna", "0", "0", f"{LK['tf_at_zero']:.0f}", f"{LK['floor_at_zero']:.0f}"],
  ["Soglia tenuta al 100%", n0(LK['floor100']['leak_per_month']),
   p1(LK['floor100']['leak_pct_of_C0_per_yr']),
   f"{LK['floor100']['t_frontier']:.0f}", "100"],
  ["Equivalente di mercato aperto", ", ", f"{LK['max_pct_of_c0_per_yr']:.0f}",
   f"{LK['tf_at_max']:.0f}", f"{LK['floor_at_max']:.0f}"]],
 "I tassi di dispersione sono espressi rispetto al flusso di dirottamento "
 "storicamente stimato. La soglia è molto elastica alla dispersione; l'orizzonte "
 "di frontiera non lo è."),
("fig", os.path.join(FIG, "fig8_dispersione.png"),
 "La dispersione alza ripidamente la soglia di sovranità muovendo pochissimo "
 "l'orizzonte di frontiera. Le due curve divergono perché la soglia è uno stato "
 "stazionario determinato dagli afflussi, mentre l'uscita dalla frontiera è "
 "governata dal tasso di crescita della frontiera stessa.", "7"),
("p",
 "**La dispersione compra capacità, non competitività.** Per il disegno "
 "dell'enforcement questo rovescia l'enfasi consueta. L'interdizione è "
 "relativamente efficace nel proteggere un vantaggio di frontiera, robusto alla "
 "dispersione perché determinato dal tasso di crescita della frontiera e non "
 "dallo stock dell'avversario. È quasi impotente nell'impedire a un avversario di "
 "mantenere una soglia sostanziale, perché la soglia risponde direttamente agli "
 "afflussi e l'afflusso richiesto è modesto. Un regime di controllo giustificato "
 "sul primo terreno e valutato sul secondo apparirà fallimentare quando non lo è "
 ", e viceversa."),

# ══ 6 ════════════════════════════════════════════════════════════════════════
("h1", "6  Il confronto aeronautico, e perché la calibrazione fallisce"),

("p",
 "Un modello di recisione si espone all'obiezione di essere infalsificabile, "
 "poiché nessuna giurisdizione è stata finora recisa integralmente dal calcolo "
 "per IA. La risposta naturale è calibrare sul caso osservato più prossimo. "
 "L'aviazione civile russa dopo il febbraio 2022 è l'unica recisione documentata "
 "di una flotta di capitale complessa e dipendente dai ricambi con una finestra "
 "di osservazione pluriennale: una flotta iniziale di circa 1.500-1.800 velivoli "
 "di costruzione occidentale, oltre un terzo dei quali risultava cannibalizzato "
 "entro l'ottobre 2025, una riduzione prevista superiore al 50% entro il 2026, e "
 "una prassi documentata di smontare circa un velivolo per tenerne in volo dieci."),
("p",
 "**Abbiamo tentato questa calibrazione e fallisce.** Stimando il rischio del "
 "modello come unico parametro libero con $\\kappa = 10$ fissato dalla prassi "
 "osservata, il migliore adattamento ottenibile raggiunge un errore quadratico "
 f"medio di {it(f'{av['rmse']:.3f}')} e lascia inspiegati "
 f"{av['unexplained_decline_share']*100:.0f} punti percentuali del declino "
 "osservato al mese 47, con il rischio stimato appiattito contro il limite "
 "superiore della griglia di ricerca."),
("fig", os.path.join(FIG, "fig5_confronto_aviazione.png"),
 "Flotta civile russa osservata contro il migliore adattamento ottenibile con il "
 "solo attrito dei ricambi. Il residuo ombreggiato è la quota di declino che "
 "l'attrito dei ricambi non può spiegare. Non è errore del modello: corrisponde a "
 "meccanismi privi di analogo nel calcolo.", "8"),
("p",
 "Il residuo è informativo, non imbarazzante. Due meccanismi determinano gran "
 "parte del declino osservato e non hanno corrispettivo nel calcolo: il sequestro "
 "da parte dei locatori dei velivoli di proprietà estera, che è uno shock una "
 "tantum sullo stock e non attrito, e il ritiro dell'idoneità al volo da parte "
 "dei regolatori, che rimuove velivoli efficienti per ragioni giuridiche anziché "
 "fisiche. Gli acceleratori sono di proprietà piena e nessun regolatore mette a "
 "terra un cluster degradato. Attribuire all'attrito dei ricambi l'intero declino "
 "russo sovrastimerebbe il rischio di circa un ordine di grandezza."),
("p",
 "Usiamo dunque l'aviazione per delimitare $\\kappa$ e per stabilire che la "
 "cannibalizzazione è un meccanismo reale, osservato e quantificato, non per "
 "calibrare il modello del calcolo. Riportare questo risultato negativo è "
 "importante per due ragioni. Impedisce che una calibrazione spuriamente precisa "
 "si propaghi nella letteratura, e individua esattamente ciò che un test empirico "
 "adeguato richiederebbe: telemetria di un parco sottoposto a un vincolo reale di "
 "riapprovvigionamento, che allo stato non esiste in forma pubblica."),
("p",
 "Un risultato qualitativo si trasferisce comunque. La frequenza degli incidenti "
 "riportata per la flotta russa è più che raddoppiata rispetto al 2019 ben prima "
 "che il numero dei velivoli si dimezzasse. Il degrado si manifesta come calo di "
 "affidabilità prima di manifestarsi come calo di inventario. Se lo stesso vale "
 "per il calcolo, la capacità effettiva scende più rapidamente di quanto il "
 "conteggio dei nodi suggerisca, e le nostre stime sono conservative."),

# ══ 7 ════════════════════════════════════════════════════════════════════════
("h1", "7  Discussione"),

("h2", "7.1  Che cosa fa guadagnare davvero la recisione"),
("p",
 "I risultati sostengono una riformulazione del dibattito sui controlli alle "
 "esportazioni. La grandezza rilevante non è quanto calcolo perda un avversario, "
 "ma quanto tempo impieghi a cadere fuori da una frontiera in movimento, e "
 "secondo le nostre stime tale intervallo è di circa due anni ed è notevolmente "
 "insensibile alla dimensione del parco installato. I controlli non devono "
 "distruggere capacità: devono soltanto mantenerla costante mentre la frontiera "
 "avanza. Per converso, una giurisdizione che si sia assicurata un ampio parco di "
 "acceleratori ha comprato meno tempo strategico di quanto la sua dimensione "
 "suggerisca, perché il vincolo operante è il tasso di crescita della frontiera "
 "e non il proprio hardware."),
("p",
 "Ne discende un'implicazione simmetrica e meno confortante. Se l'avanzamento "
 "della frontiera rallenta, per limiti di scala, vincoli energetici o ritiro di "
 "capitali, il valore dei controlli decade con esso. In questa lettura i "
 "controlli alle esportazioni sono una scommessa sulla prosecuzione del progresso "
 "esponenziale. Sono massimamente efficaci proprio quando meno servirebbero a "
 "stabilire un primato, e minimamente efficaci quando il progresso si arresta e "
 "gli stock installati conservano il proprio valore relativo."),

("h2", "7.2  La sovranità ha un numero, ed è ovunque basso"),
("p",
 "La soglia di sovranità esplicita qualcosa che la letteratura degli indici ha "
 "indicato senza quantificare, ma va letta con un'avvertenza che enunciamo "
 "prima del risultato, non dopo. L'Appendice A mostra che, dove la produzione "
 "interna è parametrizzata come frazione di copertura dello stock installato, "
 "come per Stati Uniti e Unione Europea, la soglia collassa in "
 "$\\mathrm{cov}\\,(1 + \\min(\\kappa, \\kappa^{*}))$, indipendente da $C_0$, "
 f"$\\lambda$ e $L$. Il dato statunitense del {p1(US['floor_med'])}% è dunque la "
 "banda di copertura assunta (15-35%) riscalata di un fattore compreso fra 1,0 e "
 "1,5, non un risultato indipendente. Lo riportiamo come **mappatura di "
 "scenario**: una copertura di 0,15 / 0,25 / 0,35 implica una soglia del 19 / 32 "
 "/ 45%, e chi contesta l'assunzione di copertura può sostituirvi la propria. La "
 f"soglia cinese ({p1(CN['floor_med'])}%) è di natura diversa, deriva da una "
 "stima di afflusso assoluto, non da una frazione di copertura, ed è l'unica "
 "delle tre a essere un esito del modello in senso proprio. Il suo intervallo va "
 f"allora preso sul serio: la banda al 90% corre dal {p1(CN['floor_p05'])}% al "
 f"{p1(CN['floor_p95'])}% del parco installato, attraversando la parità in alto. "
 "L'estremo superiore è mosso congiuntamente dal parametro di dipendenza dalle "
 "scorte, se l'output realizzato di Huawei nel 2025 sia sostenibile senza le "
 "scorte di die TSMC pre-controlli, e dall'ampia incertezza sullo stesso $C_0$. "
 "Il modello non autorizza quindi l'affermazione che la Cina non possa sostenere "
 "internamente il proprio parco: autorizza l'agnosticismo, e indica la misura "
 "che risolverebbe la questione, la quota di dipendenza dalle scorte, come il "
 "secondo bersaglio empirico di maggior valore dopo $\\kappa$."),
("p",
 "Con questa qualificazione il punto qualitativo regge, e non dipende dal "
 "parametro conteso. La litografia è olandese, la produzione all'avanguardia è "
 "taiwanese e la memoria ad alta banda è per circa il 90% coreana. Nessun "
 "partecipante a questo sistema può esserne reciso senza costi, e "
 "l'impostazione retorica per cui la sovranità sarebbe una proprietà che una "
 "parte possiede e l'altra no non è sostenuta da alcuna assunzione di copertura "
 "che consideriamo plausibile."),

("h2", "7.3  Previsioni verificabili"),
("p",
 "Il modello è falsificabile, e vale la pena essere precisi su come, perché un "
 "modello di recisione non verificabile è un saggio. Quattro previsioni ne "
 "discendono direttamente, ciascuna con l'osservazione che la smentirebbe."),
("bullets", [
 "**L'affidabilità degrada prima dell'inventario.** In qualunque parco di calcolo "
 "operante sotto un vincolo reale di riapprovvigionamento, il tasso di job falliti "
 "non recuperati dovrebbe crescere in modo misurabile prima che il numero di nodi "
 "operativi cali sensibilmente. Smentita osservando conteggi di nodi che calano in "
 "proporzione ai tassi di guasto, o prima di essi.",
 "**Lo sforzo di recupero mostra un punto di saturazione, non un gradiente.** Gli "
 "operatori che aumentano la capacità di cannibalizzazione oltre la soglia non "
 "dovrebbero registrare ulteriori miglioramenti di disponibilità. Smentita da una "
 "relazione regolare e non saturante fra sforzo di recupero e disponibilità.",
 "**L'uscita dalla frontiera scala logaritmicamente con lo stock.** Fra "
 "giurisdizioni, $T_f$ dovrebbe crescere di circa "
 "$T_{\\mathrm{ddp}}\\log_2(10) \\approx 17$ mesi per ogni aumento di dieci "
 "volte del calcolo installato, non proporzionalmente. Smentita da una relazione "
 "lineare o quasi. (Una versione precedente proponeva la previsione opposta, il "
 "disaccoppiamento dallo stock, che con la metrica allora implementata era "
 "infalsificabile per costruzione.)",
 "**Il dirottamento muove la soglia, non la frontiera.** Periodi di dirottamento "
 "accresciuto dovrebbero elevare sensibilmente la capacità di calcolo sostenuta di "
 "una giurisdizione, lasciando i suoi maggiori addestramenti all'incirca dove "
 "l'orologio della frontiera li colloca. Smentita da addestramenti di scala di "
 "frontiera che seguono i volumi di dirottamento.",
]),
("p",
 "La prima è la più immediatamente verificabile: richiede soltanto che un "
 "operatore sotto vincolo pubblichi la telemetria dei job falliti accanto ai "
 "conteggi dei nodi. Nessuna serie di questo tipo è oggi pubblica, ed è per questo "
 "che il §6 riporta una calibrazione fallita anziché una riuscita."),

("h2", "7.4  Limiti"),
("bullets", [
 "**Attribuzione giurisdizionale.** I migliori dati pubblici sugli stock "
 "risolvono la proprietà per impresa, non per paese. Percorriamo le quote anziché "
 "affermarle, ma nessun trattamento elimina del tutto questa debolezza. I "
 "risultati europei in particolare vanno letti come illustrazione di scenario.",
 "**$\\kappa$ non è misurata.** La resa di cannibalizzazione è delimitata da "
 "ragionamento architetturale, non da osservazione, e l'intervallo plausibile è a "
 "cavallo della soglia critica. È il parametro aperto più rilevante.",
 "**L'utilizzo è tenuto costante.** I vincoli energetici e di rete sono "
 "rappresentati da un tetto fisso. Diverse analisi recenti sostengono che in "
 "alcune giurisdizioni sia ormai l'energia, e non il silicio, a vincolare; "
 "endogenizzare $u(t)$ accorcerebbe verosimilmente gli orizzonti qui riportati.",
 "**La recisione è modellata come completa e istantanea.** I controlli reali "
 "sono parziali, graduali e permeabili. Il termine di dispersione ne cattura una "
 "parte; i regimi a fasce o a escalation non sono modellati.",
 "**La frontiera è esogena.** Trattiamo la crescita della frontiera come "
 "un'esponenziale esterna. In realtà l'uscita di una giurisdizione recisa dalla "
 "frontiera altera le dinamiche competitive e dunque la traiettoria della "
 "frontiera stessa.",
 "**Non esiste un caso empirico di recisione per il calcolo.** Il modello è "
 "falsificabile in linea di principio, prevede traiettorie di degrado specifiche "
 ", ma non può ancora essere verificato sull'osservazione, come stabilisce il §6.",
 "**Il ritiro è una scelta economica che il modello tratta come fisica.** La "
 "vita utile $L$ codifica il ritiro a fine vita contabile, ma un operatore in "
 "regime di recisione plausibilmente farebbe funzionare l'hardware fino al "
 "guasto. Rieseguendo i casi centrali con $L$ pari a quarant'anni, $T_f$ cresce "
 "solo di tre o quattro mesi, ogni $T_{1/2}$ si allunga e le soglie salgono in "
 "modo sostanziale: lo scenario di copertura statunitense dal 32% al 92% di "
 "$C_0$, la Cina dall'86% al 246%. Il funzionamento fino al guasto rafforza "
 "quindi i risultati sulla sovranità e sposta appena l'orologio della frontiera, "
 "ed è per questo che nei risultati principali riportiamo il caso conservativo "
 "con ritiro.",
 "**$T_f$ misura la posizione di calcolo, non la posizione di capacità.** "
 "L'efficienza algoritmica nei modelli linguistici ha storicamente dimezzato il "
 "calcolo necessario a prestazioni fisse circa ogni otto mesi (Ho et al., 2024). "
 "Nella misura in cui tali progressi sono pubblici, entrambe le parti ne "
 "beneficiano e l'ordinamento relativo si conserva, ma un parco congelato "
 "continua a guadagnare capacità assoluta, sicché attraversare $\\theta$ è più "
 "morbido in termini di capacità che in termini di FLOP. Nella misura in cui i "
 "progressi di frontiera restano proprietari, la parte recisa degrada più in "
 "fretta di quanto $T_f$ suggerisca. La misura è esatta sull'hardware e "
 "deliberatamente agnostica sul software.",
 "**L'accesso remoto è fuori dal modello per costruzione.** $N(t)$ conta gli "
 "acceleratori fisicamente installati e operati nella giurisdizione. Il calcolo "
 "noleggiato presso fornitori esteri non è in $N(t)$ e, a differenza del "
 "termine di dispersione, le cui unità entrano nel parco e poi decadono a "
 "$\\lambda$ e $\\delta$, la capacità in leasing è reintegrata dal locatore e "
 "non decade affatto. Ogni orizzonte qui riportato è dunque condizionato alla "
 "recisione hardware *e* all'interdizione effettiva dell'accesso remoto; contro "
 "la sola recisione hardware è un limite superiore dell'effetto. Una "
 "consolazione segue analiticamente: poiché il deflatore di frontiera è "
 "esponenziale, un leasing fisso di qualunque entità sposta $T_f$ solo di "
 "$T_{\\mathrm{ddp}}\\log_2(1 + A/C_0)$; la capacità noleggiata sconfigge il "
 "meccanismo solo se cresce essa stessa al ritmo della frontiera, "
 "$g^{*} = \\ln 2 / T_{\\mathrm{ddp}} \\approx 13\\%$ al mese.",
 "**La produzione interna è congelata al tasso del giorno della recisione.** Il "
 "modello non contiene un canale di sostituzione indotta, sicché $C_\\infty$ è "
 "definita solo per crescita nulla dell'indigenizzazione; per qualunque tasso "
 "positivo non esiste alcun asintoto. L'assunzione è contraddetta dalla "
 "tendenza più recente della serie stessa da cui il parametro è calibrato, gli "
 "obiettivi cinesi di produzione di acceleratori risultano circa raddoppiati fra "
 "2025 e 2026, benché, sotto la premessa di recisione completa del paper, con "
 "memoria coreana e litografia olandese entrambe ritirate, il tasso potrebbe "
 "plausibilmente avere entrambi i segni. $T_f$ è robusto a questo: si sposta di "
 "pochi mesi per tassi di crescita da $-30\\%$ a $+60\\%$ annui, perché nessun "
 "ritmo plausibile di indigenizzazione compete con una frontiera che raddoppia "
 "ogni 5,2 mesi.",
]),

# ══ 8 ════════════════════════════════════════════════════════════════════════
("h1", "8  Conclusioni"),
("p",
 "La capacità nazionale di IA è stata misurata come stock almeno undici volte e "
 "modellata come flusso nemmeno una. Abbiamo sostenuto che il flusso è la "
 "grandezza rilevante per le politiche, costruito un modello di decadimento dei "
 "parchi installati di acceleratori in regime di recisione, parametrizzato su "
 "telemetria pubblicata anziché su ipotesi, e riportato tre grandezze pensate per "
 "essere riutilizzate: l'emivita del calcolo, il tempo di uscita dalla frontiera "
 "e la soglia di sovranità."),
("p",
 "Quattro risultati si distinguono. Il recupero di componenti assorbe il flusso "
 f"di guasti solo fino a una resa di saturazione "
 f"$\\kappa^{{*}} = \\lambda L \\approx {p2(ks['central'])}$ e, poiché la memoria "
 "ad alta banda è integrata nello stesso package del die, l'intervallo plausibile "
 "per gli acceleratori è a cavallo di quella soglia, il che rende $\\kappa$ il "
 "parametro non misurato di maggior valore per il campo. L'uscita dalla frontiera "
 "avviene fra due e quattro anni e cresce solo logaritmicamente con il parco "
 "installato: un parco dieci volte più grande compra circa diciassette mesi in "
 "più, mentre il decadimento hardware pesa solo per il 13-14% dell'intervallo e "
 "l'orologio della frontiera per il resto. Alla mediana nessuna grande "
 "giurisdizione appare autosufficiente, benché per Stati Uniti e Unione Europea "
 "quel valore sia un'assunzione di copertura riscalata anziché un risultato "
 "indipendente, e l'intervallo cinese sia abbastanza ampio da attraversare la "
 "parità, lasciando lì la questione della sovranità genuinamente aperta. E la "
 "dispersione, quando è parziale, compra capacità anziché "
 "competitività: alza ripidamente la soglia di sovranità lasciando l'orizzonte di "
 "frontiera quasi dov'era."),
("p",
 "L'affermazione secondo cui i controlli alle esportazioni fanno guadagnare tempo "
 "è, in questa analisi, corretta nella forma e sostanzialmente errata nel "
 "meccanismo che di solito le si attribuisce. Ciò che si guadagna non è il "
 "degrado dell'hardware avversario, ma il congelamento della sua posizione "
 "rispetto a una frontiera che continua a muoversi. Si tratta di uno strumento "
 "diverso, con una diversa data di scadenza, e come tale andrebbe argomentato."),

("h1", "Appendice A  Derivazione della resa critica"),
("p",
 "Sia $P_t$ il bacino di recupero. In un periodo il bacino guadagna $\\kappa$ "
 "riparazioni per ogni unità che esce dal servizio, guasti non riparati "
 "$(F_t-\\rho_t)$ e ritiri $\\mathrm{Rit}_t$, e perde $\\rho_t$ per le "
 "riparazioni effettuate. Si consideri lo stato stazionario in cui ogni guasto "
 "viene riparato, cosicché $\\rho_t = F_t = N\\lambda$ e "
 "$\\mathrm{Rit}_t = N\\delta$. Il bilancio del bacino è"),
("eq", "\\Delta P \\;=\\; \\kappa N\\delta \\;-\\; N\\lambda", "A.1"),
("p",
 "non negativo precisamente quando $\\kappa \\geq \\lambda/\\delta$. Ponendo "
 "$\\delta = 1/L$ si ottiene $\\kappa^{*} = \\lambda L$. La dimensione della "
 "flotta $N$ si semplifica, dunque la soglia è indipendente dalla scala; "
 "l'afflusso $R$ non compare, dunque è anche indipendente dalle politiche. Al di "
 "sotto di $\\kappa^{*}$ il bacino si esaurisce in tempo finito e i guasti non "
 "riparati si accumulano; al di sopra il bacino cresce senza limite e il vincolo "
 "di riparazione cessa di operare, ed è per questo che le traiettorie per "
 "$\\kappa = 0,5$, $1$ e $10$ coincidono nella Figura 6."),
("p",
 "Si noti con attenzione ciò che questo *non* stabilisce. L'equazione A.1 governa "
 "il solo vincolo di riparazione. Il ritiro rimuove unità dal servizio "
 "indipendentemente dalla riparazione dei guasti, dunque $N$ declina anche al di "
 "sopra della soglia, al tasso $\\delta$, anziché a $\\delta$ più un termine di "
 "guasti non assorbiti. Una versione precedente di questo articolo affermava che "
 "il parco installato *persiste* al di sopra di $\\kappa^{*}$; la simulazione "
 "diretta la smentisce, e la lettura corretta, una soglia di saturazione che "
 "separa il decadimento limitato dai guasti da quello limitato dall'obsolescenza "
 ", è quella verificata numericamente al §5.1."),

("h2", "A.2  Forma chiusa della soglia di sovranità"),
("p",
 "Una versione precedente affermava che non esistesse una forma chiusa e "
 "riportava la soglia da un'integrazione a 900 mesi. Una forma chiusa esiste. "
 "Ponendo stazionario il bacino nell'Eq. 2 si ottiene "
 "$\\rho = \\kappa(F+\\mathrm{Rit})/(1+\\kappa)$, dunque un'attrito netto di "
 "$(\\lambda+\\delta)N/(1+\\min(\\kappa,\\kappa^{*}))$ e"),
("eq",
 r"\frac{C_\infty}{C_0} = \frac{R_{\mathrm{int}}+R_{\mathrm{disp}}}"
 r"{C_0\,(\lambda+\delta)}\,\left(1+\min(\kappa,\kappa^{*})\right)",
 "A.2"),
("p",
 "che riproduce esattamente i valori integrati. La conseguenza va detta "
 "chiaramente perché vincola la lettura di due delle nostre tre soglie. Dove la "
 "produzione interna è parametrizzata come frazione di copertura dello stock, "
 "$R_{\\mathrm{int}} = \\mathrm{cov}\\cdot C_0(\\lambda+\\delta)$, come "
 "trattiamo Stati Uniti e Unione Europea in assenza di dati di produzione "
 "risolti per giurisdizione, questa collassa in"),
("eq", r"\frac{C_\infty}{C_0} = \mathrm{cov}\,"
       r"\left(1+\min(\kappa,\lambda L)\right)", "A.3"),
("p",
 "indipendente da $C_0$, $\\lambda$ e $L$, con la parentesi limitata in "
 "$[1,0;\\,1,5]$ su tutti i valori considerati. Quelle due soglie sono dunque il "
 "riscalamento di un'assunzione, non una proprietà emergente del modello, e il "
 "§7.2 le riporta come mappatura di scenario. La soglia cinese, che deriva da "
 "una stima di afflusso assoluto, non è soggetta a questo collasso."),

("h1", "Appendice B  Riproducibilità"),
("p",
 "Tutti i risultati derivano da un unico script deterministico con seme casuale "
 "fissato (20260808). La sua esecuzione rigenera ogni figura, tabella e valore "
 "numerico di questo articolo, compresi quelli citati nell'abstract. Il modello "
 "consta di 200 righe di NumPy senza dipendenze da solutori esterni. Codice del "
 "modello, file dei parametri, output Monte Carlo e registro completo del "
 "reperimento delle fonti sono archiviati insieme a questo preprint; si veda "
 "*Disponibilità di dati e codice*."),
]

BACK = [
("h1", "Disponibilità di dati e codice"),
("p",
 "Codice del modello, definizioni dei parametri con attribuzione della fonte per "
 "ciascun valore, output Monte Carlo, tabelle elaborate e tutto il codice di "
 "generazione delle figure sono liberamente disponibili su "
 "github.com/diShine-digital-agency/The-Half-Life-of-Compute e sono "
 "archiviati con il deposito Zenodo di questo articolo. I dati sottostanti sono di terze parti e pubblicamente "
 "accessibili: Epoch AI pubblica dati su proprietà e vendite di acceleratori con "
 "metodologia documentata; le statistiche di guasto provengono da articoli "
 "pubblicati. Non sono stati utilizzati dati proprietari o sotto licenza."),

("h1", "Dichiarazioni"),
("p",
 "**Finanziamenti.** La ricerca non ha ricevuto finanziamenti esterni. "
 "**Conflitti di interesse.** L'autore è fondatore di diShine, società di "
 "consulenza attiva su adozione e governance dell'IA, ed è autore di un volume "
 "divulgativo sulla geopolitica della tecnologia citato una sola volta in questo "
 "articolo per un contributo di inquadramento. Nessuna delle due relazioni ha "
 "influenzato l'analisi, che poggia interamente su dati pubblici e su codice "
 "rilasciato. **Assistenza di IA.** Strumenti computazionali sono stati impiegati "
 "per il reperimento delle fonti, l'implementazione del modello e la preparazione "
 "del manoscritto; tutte le affermazioni analitiche, le scelte di parametrizzazione "
 "e le interpretazioni sono dell'autore, e ogni affermazione fattuale è stata "
 "verificata su una fonte primaria reperita."),

("h1", "Nota sulla versione"),
("p",
 "Questo articolo è la versione italiana di *The Half-Life of Compute: Modelling "
 "National AI Capacity Decay Under Supply Severance*. Le due versioni sono "
 "generate dal medesimo modello e condividono gli stessi risultati numerici. In "
 "caso di discrepanza fa fede la versione inglese, che è quella depositata su "
 "Zenodo."),

("h1", "Bibliografia"),
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
 "for a New American Security, aprile 2026.",
 "Cui, L., et al. (2025). Quantitative analysis of the U.S. chip embargo and "
 "China's export controls on Ga, Ge and graphite. *Computers & Industrial "
 "Engineering*, 7 gennaio 2025. ScienceDirect PII S0360835225000051.",
 "Dobbie, M. J., et al. (2013). Robustness and sensitivity of weighting and "
 "aggregation in constructing composite indices. *Ecological Indicators*.",
 "Epoch AI (2025). *Hardware failures won't limit AI scaling*. "
 "epoch.ai/blog/hardware-failures-wont-limit-ai-scaling",
 "Epoch AI (2026). *Data on AI Chip Owners* e *Data on AI Chip Sales*, con "
 "metodologia pubblicata. epoch.ai/data",

 "Epoch AI (2026). *Data on AI Models*: esecuzioni di addestramento di "
 "frontiera, fra cui Grok 3 a circa 3e26 FLOP e Grok 4 come la più grande "
 "dichiarata. epoch.ai/data/ai-models",
 "Escoda, K. (2026). *GEOPOLITECH*. Volume III di *The Architecture of the New "
 "World: From Code to Matter*., citato solo per l'inquadramento sui punti di "
 "strozzatura.",
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
 "China*. Epoch AI, 29 aprile 2026.",
 "Kelemen, A., et al. (2024). A sensitivity analysis of composite indicators: "
 "Min/max thresholds. *Environmental and Sustainability Indicators*.",
 "Kokolis, A., Kuchnik, M., Hoffman, J., Kumar, A., Malani, P., Ma, F., DeVito, "
 "Z., Sengupta, S., Saladi, K. & Wu, C.-J. (2025). Revisiting Reliability in "
 "Large-Scale Machine Learning Research Clusters. *IEEE HPCA 2025*. "
 "arXiv:2410.21680.",
 "Leavy, E. (2026). *Machinepower Index 2026*, edizione Q3 2026. "
 "machinepowerindex.org",
 "Lee, J.-D., Choi, S., Kim, K. & Si, S. (2024). *Empirical Measurement of "
 "Technology Sovereignty*. IFS Working Paper 2024-01, Institute for Future "
 "Strategy, Seoul National University. SSRN 5145685.",
 "Meng, W. (2025). Modeling the Path of Structural Strategic Deterrence: A Sand "
 "Table Simulation Based on Rare Earth Supply Disconnection. arXiv:2505.21579.",
 "Nardo, M., Saisana, M., Saltelli, A. & Tarantola, S. (2008). *Handbook on "
 "Constructing Composite Indicators: Methodology and User Guide*. OCSE / "
 "Commissione Europea JRC. JRC47008. ISBN 978-92-64-04346-6.",
 "Park, D.-J. & Liu, S. (2023). A Study on the Economic Effects of U.S. Export "
 "Controls on Semiconductors to China. *Korea International Trade Research "
 "Institute*. SSRN 4391187.",
 "Sherbrooke, C. C. (1968). METRIC: A Multi-Echelon Technique for Recoverable "
 "Item Control. *Operations Research*, 16(1), 122-141. doi:10.1287/opre.16.1.122. "
 "In precedenza RAND RM-5078.",

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
