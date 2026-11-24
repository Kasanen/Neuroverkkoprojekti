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

Ryhmässä on 4 jäsentä, ja jokainen käyttää omaa Claude-istuntoaan. Claude ei muista edellisiä istuntoja, joten ajantasainen tila on aina gitissä: `TASKS.md`, `PLAN.md` ja git-historia.

**Istunnon alussa**
1. Aja `git pull` ja `git log -10 --oneline`, lue `TASKS.md` ja `PLAN.md`.
2. Kysy käyttäjän nimi (Elias, Miska, Veijo tai Taif), jos se ei ilmene. Git-käyttäjänimi ei kerro sitä. Käytä nimeä `ottaja`-kentässä ja AI-lokissa.
3. Aja `python scripts/check_project.py` ja kerro lyhyesti tilanne. Skripti syntyy vasta tehtävässä T25. Kun sitä ei vielä ole, sano se äläkä väitä tarkistusta tehdyksi.

**Tehtävän aikana**
4. Ota tehtävä vain, jos sen `vaatii`-tehtävät ovat `valmis` ja `tila` on `vapaa` pullin jälkeen. Varaus (`ottaja`, `tila: työn alla`) commitoidaan ja pushataan heti omana pienenä commitina mainiin. Vasta sitten luodaan haara `T07-malli-a` (tehtävän numero + lyhyt nimi).
5. Työ tehdään omassa haarassa, ja valmis työ tulee mainiin pull requestilla. Toinen jäsen katselmoi sen. Älä pushaa suoraan mainiin muuta kuin varausta.
6. Älä muokkaa toisen `työn alla` -tehtävää äläkä muuta tehtävien numeroita.

**Kun tehtävä on valmis**
7. Samassa PR:ssä: `tila: valmis`, `[x]`, AI-lokirivi ja tarvittaessa `PLAN.md`:n muutosloki. Aja tarkistusskripti uudelleen.
8. Kirjaa tekoälyn käyttö `TASKS.md`:n AI-lokiin heti, älä vasta lopuksi.
9. Lopuksi tarkista, ettei mikään jäänyt päivittämättä: tehtävän tila, AI-loki ja muutosloki.

**Suunnitelman muutokset**
10. Älä muuta `PLAN.md`:n tavoitteita, rajausta tai kynnyksiä itse. Ehdota muutos käyttäjälle, ja kirjaa se muutoslokiin vasta, kun ryhmä on päättänyt (päättäjä-sarake).

## Tekniset säännöt (tarkista aina)

- **Ei datavuotoa.** Käytä vain viralliseen foldiin perustuvaa `split(df, k)`-funktiota. Normalisointitilastot lasketaan vain opetusdatasta. Augmentaatio vain opetusdatalle. Testifoldiin ei kosketa viritysvaiheessa.
- **Siemen 42** jokaisessa ajossa: `keras.utils.set_random_seed(42)`.
- **Samat foldit ja sama esikäsittely** kaikilla malleilla, jotta vertailu on reilu. Poikkeus: C1 käyttää 16 kHz:n aaltomuotoa ja YAMNetin omaa esikäsittelyä (`PLAN.md`).
- **Validointi** on yksi kokonainen opetusfoldi, ei satunnaista osuutta. EarlyStopping, ReduceLROnPlateau ja KerasTuner käyttävät vain sitä, ei testifoldia.
- **Koodi jaettuihin moduuleihin** (`src/data.py`, `src/augment.py`, `src/models.py`), ei kopioina notebookeihin.
- **Tulokset yhteiseen muotoon**: `results/{malli}_fold{k}.json` (kentät `PLAN.md`:ssä). Mallit `models/{malli}_fold{k}.keras`.
- **Callbackit**: EarlyStopping (`restore_best_weights=True`), ModelCheckpoint, ReduceLROnPlateau, CSVLogger.
- **Keras 3**: `hub.KerasLayer` ei toimi, joten YAMNet ajetaan `hub.load`-funktiolla mallin ulkopuolella.
- Älä commitoi dataa tai isoja välimuistitiedostoja. Pidä `data/`, `models/` ja `.npy`-tiedostot `.gitignore`ssa. Ne jaetaan Drivessa. Pienet `results/*.json`-tiedostot commitoidaan.
- **Notebookit**: `.ipynb` ei yhdisty gitissä kunnolla. Logiikka on `src/`:ssä, notebookissa vain ajot, taulukot ja kuvat. Tyhjennä tulosteet ennen committia (lopulliset notebookit poikkeus). Yksi henkilö muokkaa samaa notebookia kerrallaan.

## Kurssin säännöt tekoälystä

Tekoälyn käyttö on sallittu myös dokumentaatiossa ja raportissa, mutta:
- ryhmän jäsenen pitää ymmärtää ja pystyä selittämään jokainen käytetty koodirivi, joten selitä koodi riveittäin pyydettäessä ja ennen kuin ehdotat isoa muutosta,
- sisällön, tulosten ja johtopäätösten on oltava oikeita ja ryhmän todentamia,
- tekoälyn käyttö kirjataan tarkasti AI-lokiin ja raportin liitteeseen.

## Kommunikointi

Vastaa suomeksi. Ole tiivis ja konkreettinen. Kun pyydetään "tarkistus", käy läpi: tehtävien tila aikatauluun nähden, tavoitteet joita ei ole vielä saavutettu, puuttuvat palautettavat ja `PLAN.md`:n arvosana 5 -tarkistuslista (merkitse puuttuvat todisteet). Älä väitä arvosanaa, koska kurssin tarkkaa arvosanarajausta ei tiedetä.
