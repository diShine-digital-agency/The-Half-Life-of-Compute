# L'emivita del calcolo

**Un modello di decadimento della capacita nazionale di IA in regime di recisione delle forniture**

Kevin Escoda · diShine, Milano · agosto 2026
DOI dell'articolo: `10.5281/zenodo.21866487` (Zenodo) · [English version](README.md) · [Version francaise](README.fr.md)

I controlli sulle esportazioni di chip per l'IA sono giustificati da un'affermazione sul tempo: si dice che ne facciano guadagnare. Questo repository contiene il modello, i dati, la suite di verifica e i manoscritti completi della prima stima quantitativa di quanto, trattando il parco nazionale di acceleratori come capitale deperibile che si guasta, invecchia rispetto a una frontiera in movimento e puo essere riparato solo in parte per cannibalizzazione.

## Risultati principali

| Grandezza | Definizione | Risultato (mediana, Monte Carlo a 10.000 estrazioni) |
|---|---|---|
| Uscita dalla frontiera, T_f | mesi perche la capacita scenda sotto il 10% della scala di frontiera | UE 25 · Cina 41 · USA 49 |
| Legge analitica | T_f segue T_dbl x log2(C0 / (theta x F0)) | 10 volte lo stock compra circa 17 mesi |
| Emivita del calcolo, T1/2 | mesi al 50% della capacita iniziale | USA 51, UE 28; Cina censurata (">120" nel 58% delle estrazioni) |
| Soglia di sovranita, C_inf | capacita sostenibile con gli afflussi non recisi | USA 31% (scenario), UE 3% (scenario), Cina 53% con intervallo 22-156%: l'autosufficienza cinese e genuinamente indeterminata |
| Soglia di saturazione | kappa* = lambda x L = 0,38 | oltre, ulteriore sforzo di recupero non rende nulla |

Il decadimento hardware spiega solo il 13-14% dell'intervallo di uscita dalla frontiera. Il resto e l'orologio della frontiera: la recisione non deve distruggere il calcolo dell'avversario, basta congelarlo mentre la frontiera avanza.

## Mappa del repository

```
01-SUBMISSION/      PDF finali: articolo e sintesi in EN, IT, FR
02-DRAFT/model/     il modello (~200 righe di NumPy), suite di verifica, generatori di figure
02-DRAFT/figures*/  tutte le figure, per lingua (articoli e sintesi esecutive)
02-DATA/processed/  results.json, results_extended.json, tutte le tabelle CSV
03-AUDIT/           la cronologia completa delle correzioni, incluse le affermazioni ritirate
```

## Riprodurre tutto

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r 05-DRAFT/model/requirements.txt
cd 05-DRAFT/model
python3 compute_decay_model.py     # modello, Monte Carlo, figure, tabelle
python3 verify_and_extend.py       # ricalcolo indipendente; deve stampare ALL CHECKS PASSED
```

Seme fissato 20260808. Ogni numero di ogni manoscritto, abstract compresi, e letto da `results.json` in fase di build; nulla e digitato due volte.

## Una nota sull'onesta

L'articolo e stato sottoposto a revisione avversariale prima del rilascio, e il registro e pubblico in `01-AUDIT/`. Un'affermazione di punta di una bozza precedente (invarianza rispetto allo stock) e risultata un artefatto di normalizzazione ed e stata ritirata; il tempo di raddoppio della frontiera e stato ricalibrato sulla serie corretta; un tentativo di calibrazione sull'aviazione civile russa e fallito ed e riportato come fallimento; un'ipotesi allettante e stata verificata, respinta e documentata.

## Citazione

Si veda il blocco BibTeX nel README inglese. Licenza: codice MIT, manoscritti e figure CC BY 4.0.
