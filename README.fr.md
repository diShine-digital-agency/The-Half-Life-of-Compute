# La demi-vie du calcul

**Modeliser le declin de la capacite nationale en IA en regime de rupture d'approvisionnement**

Kevin Escoda · diShine, Milan · aout 2026
DOI de l'article : `10.5281/zenodo.21866487` (Zenodo) · [English version](README.md) · [Versione italiana](README.it.md)

Les controles a l'exportation de puces d'IA sont justifies par une affirmation sur le temps : ils en feraient gagner. Ce depot contient le modele, les donnees, la suite de verification et les manuscrits complets de la premiere estimation quantitative de combien, en traitant le parc national d'accelerateurs comme un capital perissable qui tombe en panne, vieillit face a une frontiere mobile et ne peut etre repare que partiellement par cannibalisation.

## Resultats cles

| Grandeur | Definition | Resultat (mediane, Monte-Carlo a 10 000 tirages) |
|---|---|---|
| Sortie de la frontiere, T_f | mois avant de passer sous 10% de l'echelle de frontiere | UE 25 · Chine 41 · E.-U. 49 |
| Loi analytique | T_f suit T_dbl x log2(C0 / (theta x F0)) | 10 fois le stock achete environ 17 mois |
| Demi-vie du calcul, T1/2 | mois jusqu'a 50% de la capacite initiale | E.-U. 51, UE 28 ; Chine censuree (">120" dans 58% des tirages) |
| Plancher de souverainete, C_inf | capacite soutenable par les apports non rompus | E.-U. 31% (scenario), UE 3% (scenario), Chine 53% avec un intervalle de 22-156% : l'autosuffisance chinoise est veritablement indeterminee |
| Seuil de saturation | kappa* = lambda x L = 0,38 | au-dela, tout effort de recuperation supplementaire ne rapporte rien |

Le declin materiel n'explique que 13-14% de l'intervalle de sortie. Le reste est l'horloge de la frontiere : la rupture n'a pas besoin de detruire le calcul de l'adversaire, le figer suffit pendant que la frontiere avance.

## Plan du depot

```
01-SUBMISSION/      PDF finaux : article et synthese en EN, IT, FR
02-DRAFT/model/     le modele (~200 lignes de NumPy), suite de verification, generateurs de figures
02-DRAFT/figures*/  toutes les figures, par langue (articles et syntheses)
02-DATA/processed/  results.json, results_extended.json, toutes les tables CSV
03-AUDIT/           l'historique complet des corrections, y compris les affirmations retirees
```

## Tout reproduire

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r 05-DRAFT/model/requirements.txt
cd 05-DRAFT/model
python3 compute_decay_model.py     # modele, Monte-Carlo, figures, tables
python3 verify_and_extend.py       # recalcul independant ; doit afficher ALL CHECKS PASSED
```

Graine fixee 20260808. Chaque nombre de chaque manuscrit, resumes compris, est lu depuis `results.json` a la construction ; rien n'est saisi deux fois.

## Une note sur l'honnetete

L'article a ete soumis a une revue adversariale avant publication, et le registre est public dans `01-AUDIT/`. Une affirmation phare d'une version anterieure (invariance au stock) s'est revelee un artefact de normalisation et a ete retiree ; le temps de doublement de la frontiere a ete recale sur la bonne serie ; une tentative de calibration sur l'aviation civile russe a echoue et est rapportee comme un echec ; une hypothese seduisante a ete testee, rejetee et documentee.

## Citation

Voir le bloc BibTeX du README anglais. Licence : code MIT, manuscrits et figures CC BY 4.0.
