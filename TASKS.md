# TASKS.md: Eläinäänten tunnistus CNN:llä

Projekti: neuroverkkokurssin loppuprojekti 4. Palautus **pe 11.12.2026**, tavoite arvosana 5.
Ryhmä 2: Elias, Miska, Veijo, Taif

## Ohjeet (ihmiselle ja Claudelle)

1. Lue koko tiedosto. Valitse ylimmältä rivi, jonka `tila` on `vapaa` ja jonka `vaatii`-tehtävät ovat kaikki `valmis`.
2. Kun otat tehtävän: kirjoita nimesi kohtaan `ottaja` ja vaihda `tila: vapaa` muotoon `tila: työn alla`.
3. Kun tehtävä on valmis: vaihda `tila: valmis` ja muuta ruutu `[ ]` muotoon `[x]`.
4. Älä muokkaa muiden `työn alla` -tehtäviä äläkä muuta tehtävien numeroita (`T01`...), koska `vaatii`-viittaukset käyttävät niitä.
5. Jos tehtävä paljastaa uuden työn, lisää rivi osion loppuun uudella numerolla ja `tila: vapaa`.
6. Kirjaa tekoälyn käyttö alla olevaan AI-lokiin heti, kun käytät sitä.

Claudelle: pysy tämän projektin suunnitelmassa (ESC-50:n 10 eläinluokkaa, Keras 3 + TensorFlow, mallit A, B, C1, C2). Älä ehdota uusia datasettejä tai kirjastoja ilman, että kysyt ensin. Tarkista aina: ei datavuotoa (normalisointi ja augmentaatio vain opetusdatalle, testifoldiin ei kosketa viritysvaiheessa), siemen 42, samat foldit kaikilla malleilla.

Tavoitteet: baseline (A) ≥ 70 %, paras malli ≥ 85 % tarkkuus ja makro-F1 ≥ 0,85, siirto-oppiminen vähintään 10 prosenttiyksikköä baselinea parempi. Nämä ovat arvioita ja tarkennetaan baseline-ajon jälkeen.

---

## Vaihe 1: Perusta (valmis to 26.11.)

Näiden pitää olla valmiina ennen kuin muut voivat ajaa malleja, koska kaikki käyttävät samaa dataa ja koodia.

- [ ] **T01** Luo GitHub-repo, kansiorakenne, `requirements.txt` ja jaettu Drive-kansio
  - vaatii: – · takaraja: to 26.11. · ottaja: – · tila: vapaa
- [ ] **T02** Lataa ESC-50, suodata eläinluokat (`target` < 10), tarkista 400 leikettä
  - vaatii: T01 · takaraja: to 26.11. · ottaja: – · tila: vapaa
- [ ] **T03** Fold-jako `split()` (testifoldi + validointifoldi + opetusfoldit, ks. `PLAN.md`) ja EDA (luokkajakauma, esimerkkispektrogrammit)
  - vaatii: T02 · takaraja: to 26.11. · ottaja: – · tila: vapaa
- [ ] **T04** Esikäsittely: `load_wave`, `log_mel`, `.npy`-välimuisti, normalisointi opetusdatan tilastoilla
  - vaatii: T02 · takaraja: to 26.11. · ottaja: – · tila: vapaa
- [ ] **T05** `PyDataset` ja augmentaatiot (aikasiirto, kohina, SpecAugment, mixup)
  - vaatii: T04 · takaraja: to 26.11. · ottaja: – · tila: vapaa
- [ ] **T06** Yhteinen koulutusfunktio (callbackit) ja tulosten tallennus `results/`-kansioon
  - vaatii: T01 · takaraja: to 26.11. · ottaja: – · tila: vapaa
- [ ] **T25** Luo `scripts/check_project.py` (tarkistaa tulostiedostot, tavoitteet ja palautettavat)
  - vaatii: T01 · takaraja: to 26.11. · ottaja: – · tila: vapaa

## Vaihe 2: Mallit (valmis ma 30.11. – to 3.12.)

- [ ] **T07** Malli A (baseline-CNN), ajo kiinteillä foldeilla
  - vaatii: T04, T06 · takaraja: ma 30.11. · ottaja: – · tila: vapaa
- [ ] **T08** Malli B (regularisoitu CNN), ensimmäinen ajo
  - vaatii: T05, T06 · takaraja: ma 30.11. · ottaja: – · tila: vapaa
- [ ] **T09** YAMNet-upotukset kaikille leikkeille (16 kHz)
  - vaatii: T02 · takaraja: ma 30.11. · ottaja: – · tila: vapaa
- [ ] **T10** Malli C1: luokitin YAMNet-upotusten päälle
  - vaatii: T06, T09 · takaraja: to 3.12. · ottaja: – · tila: vapaa
- [ ] **T11** KerasTuner-haku mallille B (10–15 kokeilua)
  - vaatii: T08 · takaraja: to 3.12. · ottaja: – · tila: vapaa
- [ ] **T12** Malli C2: EfficientNetB0 (pää ensin, sitten hienosäätö)
  - vaatii: T04, T06 · takaraja: to 3.12. · ottaja: – · tila: vapaa

## Vaihe 3: Lopulliset ajot ja analyysi (valmis su 6.12., koodi jäädytetään)

- [ ] **T13** 5-fold-ajot: malli A
  - vaatii: T07 · takaraja: su 6.12. · ottaja: – · tila: vapaa
- [ ] **T14** 5-fold-ajot: malli B (paras konfiguraatio)
  - vaatii: T11 · takaraja: su 6.12. · ottaja: – · tila: vapaa
- [ ] **T15** 5-fold-ajot: malli C1
  - vaatii: T10 · takaraja: su 6.12. · ottaja: – · tila: vapaa
- [ ] **T16** 5-fold-ajot: malli C2
  - vaatii: T12 · takaraja: su 6.12. · ottaja: – · tila: vapaa
- [ ] **T17** Ablaatio mallille B (4 augmentaatioasetusta × 5 foldia)
  - vaatii: T05, T11 · takaraja: su 6.12. · ottaja: – · tila: vapaa
- [ ] **T18** Vertailunotebook: taulukot, confusion matrixit, oppimiskuvaajat
  - vaatii: T13, T14, T15, T16 · takaraja: su 6.12. · ottaja: – · tila: vapaa
- [ ] **T19** Virheanalyysi ja Grad-CAM
  - vaatii: T18 · takaraja: su 6.12. · ottaja: – · tila: vapaa

## Vaihe 4: Demo, raportti ja esitys (valmis ke 9.12.)

- [ ] **T20** Gradio-demo parhaalla mallilla (paras selviää T18:ssa)
  - vaatii: T18 · takaraja: ke 9.12. · ottaja: – · tila: vapaa
- [ ] **T21** Raportti (3–5 s): tavoite ja motivaatio, data ja esikäsittely, mallit ja perustelut, koulutus ja hyperparametrit, analyysi, haasteet ja epäonnistumiset, johtopäätökset ja jatkokehitysideat, työnjako
  - vaatii: T18, T19 · takaraja: ke 9.12. · ottaja: – · tila: vapaa
- [ ] **T22** Tekoälyn käytön dokumentointi (kirjaa koko ajan, viimeistele raporttiin)
  - vaatii: – · takaraja: ke 9.12. · ottaja: – · tila: vapaa
- [ ] **T23** Esitysdiat (10–15 min) ja harjoitusesitys, kaikki puhuvat
  - vaatii: T18 · takaraja: ke 9.12. · ottaja: – · tila: vapaa

## Vaihe 5: Puskuri ja palautus

- [ ] **T24** Notebookit `.ipynb`- ja `.html`-muodossa, uudelleenkoulutusohje ja palautuksen tarkistuslista
  - vaatii: kaikki · takaraja: to 10.12. (palautus pe 11.12.) · ottaja: – · tila: vapaa

---

## AI-loki

Kurssi vaatii tarkan kirjauksen siitä, miten ja missä tekoälyä on käytetty. Lisää rivi jokaisesta käytöstä.

| Päivä | Kuka | Tehtävä | Työkalu | Mitä pyydettiin | Mitä käytettiin ja muutettiin |
| --- | --- | --- | --- | --- | --- |
| 24.11.2026 | Veijo | Dokumentaation tarkistus | Claude Code | Vertaa CLAUDE.md, PLAN.md, TASKS.md ja INSTRUCTIONS-short.md tehtävänantoon ja korjaa 7 löydettyä puutetta | Käytettiin tarkistuksen tuloksia. Lisättiin validointifoldi, C1-poikkeus, T25, T17/T20/T21 muutokset ja raportin osiot. Ryhmän pitää tarkistaa muutokset |
