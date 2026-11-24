# CLAUDE.md: Eläinäänten tunnistus CNN:llä (Ryhmä 2)

Tämä tiedosto kertoo Claudelle, mitä projektissa tehdään ja miten. Lue se ja `TASKS.md` aina istunnon alussa.

## Projekti

Neuroverkkokurssin loppuprojekti 4 (oma aihe). Ryhmä 2: Elias, Miska, Veijo, Taif. Palautus **pe 11.12.2026**, tavoite arvosana 5.

Tehtävä: tunnista eläin 5 sekunnin äänileikkeestä konvoluutioverkolla. Data on ESC-50:n 10 eläinluokkaa (`target` 0–9, 400 leikettä, viralliset 5 foldia). Kehys on Keras 3 TensorFlow-backendillä.

Neljä mallia vertaillaan samalla datajaolla:
- **A**: baseline-CNN ilman augmentaatiota
- **B**: regularisoitu CNN (BatchNorm, Dropout, L2) augmentaatiolla
- **C1**: YAMNet-upotukset + pieni luokitin
- **C2**: EfficientNetB0 (ImageNet-painot), pää ensin ja sitten hienosäätö

Mitattavat tavoitteet ovat `PLAN.md`:ssä. Arviointi: tekninen toteutus 50 %, analyysi 30 %, esitys ja dokumentaatio 20 %.

## Pysy aiheessa

- Auta vain tässä projektissa. Älä ehdota uutta datasettiä, mallia, kirjastoa tai kehystä (esim. PyTorch) ilman, että kysyt ensin ryhmältä. Jos pyyntö on suunnitelman ulkopuolella, sano se ja viittaa `PLAN.md`:hen.
- Tee yksi pieni askel kerrallaan ja kerro, mihin tehtävään (`T01`...) se liittyy.
- Älä keksi tuloksia, lukuja tai lähteitä. Jos et tiedä, sano se. Älä väitä tavoitteen täyttyneen ennen kuin `python scripts/check_project.py` ja tulostiedostot sen osoittavat.

## Työnkulku

1. Istunnon alussa: lue `TASKS.md` ja `PLAN.md`, aja `python scripts/check_project.py` ja kerro lyhyesti tilanne. Skripti syntyy vasta tehtävässä T25. Kun sitä ei vielä ole, sano se äläkä väitä tarkistusta tehdyksi.
2. Ota tehtävä vain, jos sen `vaatii`-tehtävät ovat `valmis`. Kirjoita `ottaja` ja vaihda `tila: työn alla`.
3. Kun tehtävä on valmis: `tila: valmis`, `[x]`, ja aja tarkistusskripti uudelleen.
4. Älä muokkaa toisen `työn alla` -tehtävää äläkä muuta tehtävien numeroita.
5. Kirjaa tekoälyn käyttö `TASKS.md`:n AI-lokiin heti.

## Tekniset säännöt (tarkista aina)

- **Ei datavuotoa.** Käytä vain viralliseen foldiin perustuvaa `split(df, k)`-funktiota. Normalisointitilastot lasketaan vain opetusdatasta. Augmentaatio vain opetusdatalle. Testifoldiin ei kosketa viritysvaiheessa.
- **Siemen 42** jokaisessa ajossa: `keras.utils.set_random_seed(42)`.
- **Samat foldit ja sama esikäsittely** kaikilla malleilla, jotta vertailu on reilu. Poikkeus: C1 käyttää 16 kHz:n aaltomuotoa ja YAMNetin omaa esikäsittelyä (`PLAN.md`).
- **Validointi** on yksi kokonainen opetusfoldi, ei satunnaista osuutta. EarlyStopping, ReduceLROnPlateau ja KerasTuner käyttävät vain sitä, ei testifoldia.
- **Koodi jaettuihin moduuleihin** (`src/data.py`, `src/augment.py`, `src/models.py`), ei kopioina notebookeihin.
- **Tulokset yhteiseen muotoon**: `results/{malli}_fold{k}.json` (kentät `PLAN.md`:ssä). Mallit `models/{malli}_fold{k}.keras`.
- **Callbackit**: EarlyStopping (`restore_best_weights=True`), ModelCheckpoint, ReduceLROnPlateau, CSVLogger.
- **Keras 3**: `hub.KerasLayer` ei toimi, joten YAMNet ajetaan `hub.load`-funktiolla mallin ulkopuolella.
- Älä commitoi dataa tai isoja välimuistitiedostoja. Pidä `data/` ja `.npy`-tiedostot `.gitignore`ssa.

## Kurssin säännöt tekoälystä

Tekoälyn käyttö on sallittu myös dokumentaatiossa ja raportissa, mutta:
- ryhmän jäsenen pitää ymmärtää ja pystyä selittämään jokainen käytetty koodirivi, joten selitä koodi riveittäin pyydettäessä ja ennen kuin ehdotat isoa muutosta,
- sisällön, tulosten ja johtopäätösten on oltava oikeita ja ryhmän todentamia,
- tekoälyn käyttö kirjataan tarkasti AI-lokiin ja raportin liitteeseen.

## Kommunikointi

Vastaa suomeksi. Ole tiivis ja konkreettinen. Kun pyydetään "tarkistus", käy läpi: tehtävien tila aikatauluun nähden, tavoitteet joita ei ole vielä saavutettu ja puuttuvat palautettavat.
