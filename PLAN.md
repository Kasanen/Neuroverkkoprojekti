# PLAN.md: Tavoitteet ja valmiin määritelmä (Ryhmä 2)

Tämä tiedosto kertoo, milloin projekti on valmis. Tehtävien tila on `TASKS.md`:ssä, ja `python scripts/check_project.py` tarkistaa osan tästä koneellisesti.

## Rajaus

- Data: ESC-50:n eläinluokat (koira, kukko, sika, lehmä, sammakko, kissa, kana, hyönteiset, lammas, varis), 400 leikettä, viralliset 5 foldia.
- Kehys: Keras 3 + TensorFlow-backend, Google Colab GPU.
- Mallit: A, B, C1, C2. Muiden mallien tai datasettien lisääminen vaatii koko ryhmän päätöksen ja merkinnän muutokseen alla.
- Datajako: testifoldi k on testi. Validointina on yksi kokonainen opetusfoldi (ei satunnaista osuutta, koska ESC-50:n samasta lähteestä tulevat leikkeet ovat samassa foldissa). Loput kaksi foldia ovat opetusta. EarlyStopping, ReduceLROnPlateau ja KerasTuner käyttävät vain validointifoldia, ja testifoldiin ei kosketa viritysvaiheessa.
- Poikkeus C1:lle: YAMNet käyttää 16 kHz:n aaltomuotoa ja omaa esikäsittelyään, joten C1 ei käytä samaa log-mel-esikäsittelyä kuin muut mallit. Fold-jako ja siemen 42 ovat samat. Poikkeus raportoidaan.
- Git-työnkulku: uusi repo (T01), yksi haara per tehtävä, pull request ja toisen jäsenen katselmointi. Tehtävän varaus pushataan mainiin ennen työn aloitusta (`TASKS.md`).
- Varadatasetti (Kaggle Animal Sound Dataset) otetaan käyttöön vain, jos ESC-50:n kanssa ilmenee estävä ongelma.

## Mitattavat tavoitteet

Luvut ovat 5-fold-ristiinvalidoinnin keskiarvoja. Ne ovat ryhmän omia arvioita, ja ne tarkennetaan baseline-ajon (T13) jälkeen.

| Tavoite | Kynnys |
| --- | --- |
| Malli A (baseline) tarkkuus | ≥ 70 % |
| Paras malli tarkkuus | ≥ 85 % |
| Paras malli makro-F1 | ≥ 0,85 |
| Siirto-oppiminen (C1 tai C2) verrattuna malliin A | vähintään +10 prosenttiyksikköä |
| Ablaatio mallille B | jokaisen augmentaation vaikutus keskiarvona ± keskihajontana |

## Tulostiedoston muoto

Jokainen ajo tallentaa tiedoston `results/{malli}_fold{k}.json`, jossa `malli` on `A`, `B`, `C1` tai `C2` ja `k` on 1–5:

```json
{
  "model": "B",
  "fold": 3,
  "seed": 42,
  "accuracy": 0.8625,
  "macro_f1": 0.858,
  "params": 123456,
  "train_seconds": 312.4,
  "y_true": [0, 3, 5],
  "y_pred": [0, 3, 6]
}
```

Ablaatioajot tallennetaan samalla tavalla nimellä `results/ablation_{asetus}_fold{k}.json`.

## Valmiin määritelmä (palautus pe 11.12.)

- [ ] Kaikki neljä mallia on ajettu jokaisella viidellä foldilla ja tulostiedostot ovat `results/`-kansiossa
- [ ] Tavoitteet on tarkistettu ja saavuttamatta jääneet on perusteltu raportissa
- [ ] Ablaatio on ajettu ja raportoitu
- [ ] Vertailunotebook sisältää taulukon, confusion matrixit ja oppimiskuvaajat
- [ ] Virheanalyysi ja Grad-CAM on tehty
- [ ] Gradio-demo toimii parhaalla mallilla
- [ ] Notebookit on tallennettu `.ipynb`- ja `.html`-muodossa
- [ ] Koulutetut mallit tai uudelleenkoulutusohje ovat mukana (`README.md`)
- [ ] Linkki ESC-50-datasettiin ja lataus-/suodatusohje ovat mukana
- [ ] Opettaja on hyväksynyt projektisuunnitelman (tehtävänanto: viikko 5), tila kirjattu muutoslokiin
- [ ] Raportti (3–5 s) sisältää kaikki vaaditut osiot (myös motivaatio, jatkokehitysideat, epäonnistumiset ja opitut asiat sekä työnjako)
- [ ] Tekoälyn käyttö on dokumentoitu (AI-loki ja raportin liite)
- [ ] Esitys (10–15 min) on harjoiteltu ja jokainen jäsen puhuu

## Kurssin arviointikriteerit

| Osa | Paino | Mistä se tulee |
| --- | --- | --- |
| Tekninen toteutus | 50 % | oikea toteutus, laadukas esikäsittely, selkeä koodi, järkevä koulutus (hyperparametrit, regularisointi), tekniset haasteet |
| Analyysi ja arviointi | 30 % | systemaattinen arviointi, visualisoinnit, vertailu lähestymistapojen välillä, kriittinen pohdinta, perustellut havainnot |
| Esitys ja dokumentaatio | 20 % | selkeä loppuesitys, laadukas dokumentaatio, yhteistyö ja työnjako, haasteiden ja ratkaisujen kuvaus |

## Arvosana 5 -tarkistuslista

Kurssin tarkkaa arvosanarajausta ei tiedetä, joten lista seuraa tehtävänannon arviointikohtia. Jokaiselle kohdalle on tehtävä ja todiste. Merkitse `[x]`, kun todiste on olemassa ja ryhmä on tarkistanut sen.

| Arviointikohta (paino) | Todiste | Tehtävä | Valmis |
| --- | --- | --- | --- |
| Toimiva toteutus ja laadukas esikäsittely (50 %) | `src/data.py`, välimuisti, normalisointi vain opetusdatasta, ei datavuotoa | T04 | [ ] |
| Selkeä, dokumentoitu koodi (50 %) | Moduulit `src/`, katselmoidut PR:t, README | T01, T24 | [ ] |
| Järkevä koulutus: hyperparametrit ja regularisointi (50 %) | KerasTuner-haku, callbackit, perustelut raportissa | T06, T11 | [ ] |
| Tekniset haasteet ratkaistu (50 %) | Haasteet ja ratkaisut raportissa | T21 | [ ] |
| Systemaattinen arviointi (30 %) | 5-fold-tulokset, keskiarvo ± keskihajonta, ablaatio | T13–T17 | [ ] |
| Visualisoinnit (30 %) | Taulukko, confusion matrixit, oppimiskuvaajat | T18 | [ ] |
| Lähestymistapojen vertailu (30 %) | A, B, C1, C2 samalla jaolla | T18 | [ ] |
| Kriittinen pohdinta ja perustelut (30 %) | Virheanalyysi, Grad-CAM, saavuttamattomien tavoitteiden perustelu | T19, T21 | [ ] |
| Selkeä esitys (20 %) | Harjoiteltu 10–15 min esitys, demo | T20, T23 | [ ] |
| Dokumentaation laatu (20 %) | Raportti 3–5 s, notebookit `.ipynb` ja `.html` | T21, T24 | [ ] |
| Yhteistyö ja työnjako (20 %) | Git-historia, `ottaja`-kentät, työnjako raportissa | kaikki, T21 | [ ] |
| Haasteet ja epäonnistumiset kuvattu (20 %) | Oma osio raportissa | T21 | [ ] |
| Tekoälyn käyttö dokumentoitu | AI-loki ja raportin liite | T22 | [ ] |

## Välitavoitteet

| Päivä | Välitavoite |
| --- | --- |
| to 26.11. | Perusta valmis (T01–T06) |
| ma 30.11. | Mallit A ja B ajettu, YAMNet-upotukset laskettu |
| to 3.12. | C1, C2 ja KerasTuner-haku valmiit |
| su 6.12. | 5-fold-ajot, ablaatio ja analyysi valmiit, koodi jäädytetään |
| ke 9.12. | Raportti, demo ja esitys valmiit |
| to 10.12. | Puskuri ja viimeinen tarkistus |
| pe 11.12. | Palautus |

## Muutosloki

Kirjaa tähän kaikki suunnitelmaan tehdyt muutokset (päivä, mitä muuttui, miksi, kuka päätti).

| Päivä | Muutos | Syy | Päättäjä |
| --- | --- | --- | --- |
| 24.11.2026 | Validointijoukoksi yksi kokonainen opetusfoldi | Tehtävänanto vaatii train/validation/test-jaon, ja EarlyStopping ja KerasTuner tarvitsevat validointidataa ilman datavuotoa | Ryhmä (pyysi Veijo), toteutti Claude |
| 24.11.2026 | C1 saa poikkeuksen esikäsittelyyn (16 kHz, YAMNetin oma) | YAMNet ei käytä samaa log-melia kuin muut mallit | Ryhmä (pyysi Veijo), toteutti Claude |
| 24.11.2026 | Lisätty valmiin määritelmään suunnitelman hyväksyntä ja raportin lisäosiot | Tehtävänanto: hyväksyntä viikolla 5, raportin vaaditut osiot | Ryhmä (pyysi Veijo), toteutti Claude |
| 24.11.2026 | Uusi repo, haara per tehtävä ja PR toisen jäsenen katselmoinnilla; arvosana 5 -tarkistuslista | Neljän hengen yhteistyö ilman konflikteja ja arviointikohtien seuranta | Veijo valitsi Clauden ehdotuksista. Ryhmän pitää vahvistaa |
