# Kotitalousesineiden kuvantunnistus kolmella eri mallilla

Neuroverkot-kurssin projektiraportti. Työkirjat: `CNN-Malli.ipynb`, `Esikoulutettu-Malli.ipynb`, `Hienosaadetty-malli.ipynb`.

## 1. Datasetin kuvaus

Tehtävänä oli luokitella kuvia viiteen luokkaan: **fork (haarukka), knife (veitsi), mug (muki), pen (kynä) ja plate (lautanen)**. Kuvat on otettu itse, ja niitä on **250 kappaletta, 50 jokaista luokkaa kohden**, joten aineisto on täysin tasapainoinen. Luokkien joukossa on tarkoituksella visuaalisesti samankaltaisia esineitä (haarukka, veitsi ja kynä ovat ohuita ja pitkänomaisia).

Aineisto esikäsiteltiin skriptillä `PrepareDataset.py`:
- EXIF-kierron korjaus, RGB-muunnos, keskeltä rajaus neliöön ja skaalaus kokoon **224 × 224 px** (VGG16:n syötekoko).
- **Stratifioitu jako** luokittain suhteessa 70 / 15 / 15 %, erillisiin hakemistoihin (`dataset/train`, `validation`, `test`). Kerasin `validation_split`-optiota ei käytetty.
- Satunnaissiemen 42, joten jako on toistettavissa. Jako on tallennettu tiedostoon `split_manifest.csv`.
- Normalisointitilastot (kanavakohtainen keskiarvo ja keskihajonta) laskettiin vain koulutusdatasta.

| Joukko | Kuvia / luokka | Kuvia yhteensä |
|---|---:|---:|
| Koulutus | 35 | 175 |
| Validointi | 8 | 40 |
| Testi | 7 | 35 |

Kaikki mallit käyttävät samaa jakoa, joten tulokset ovat vertailukelpoisia. Augmentointia käytettiin vain koulutusdatalle. Validointi- ja testidata pidettiin koskemattomina.

## 2. Mallit ja suorituskyvyn vertailu

**Malli 1: oma CNN.** Kolme konvoluutiolohkoa (16, 32 ja 64 suodatinta, MaxPooling, Dropout 0,2), GlobalAveragePooling, Dense(64), Dropout(0,5) ja softmax. Parametreja on noin 28 000. Koulutus tehtiin alusta alkaen Adam-optimoijalla, voimakkaalla augmentoinnilla ja EarlyStoppingilla (patience 5).

**Malli 2: VGG16 piirteenirrottajana.** ImageNet-painoilla esikoulutettu VGG16 (`include_top=False`) on jäädytetty. Piirteet (7×7×512) lasketaan kerran, ja niiden päälle koulutetaan pieni luokittelija (Flatten, Dense(128), Dropout 0,5, softmax) RMSpropilla 20 epochia.

**Malli 3: hienosäädetty VGG16.** Ensin koulutettiin luokittelija jäädytetyn VGG16:n päälle augmentoinnilla (3a). Sen jälkeen VGG16:n neljä viimeistä kerrosta avattiin ja koulutettiin oppimisnopeudella 1e-5 (3b). Koulutettavia parametreja oli noin 10,3 miljoonaa.

| Malli | Koulutettavia parametreja | Testitarkkuus | Oikein / 35 | Testihäviö |
|---|---:|---:|---:|---:|
| 1: oma CNN | ~28 tuhatta | 68,6 % | 24 | 0,83 |
| 2: VGG16, piirteiden irrotus | ~3,2 milj. | 97,1 % | 34 | 0,47 |
| 3a: VGG16 jäädytettynä + augmentointi | ~3,2 milj. | 97,1 % | 34 | 1,36 |
| 3b: hienosäädetty VGG16 | ~10,3 milj. | 97,1 % | 34 | 1,90 |

Keskeiset havainnot:
1. **Siirto-oppiminen paransi tulosta selvästi.** Esikoulutetut mallit olivat noin 28 prosenttiyksikköä tarkempia kuin tyhjästä koulutettu CNN, vaikka dataa oli vain 35 kuvaa luokkaa kohden.
2. **Mallien 2, 3a ja 3b välillä ei ole eroa tarkkuudessa.** Jokainen teki testijoukossa yhden virheen. Yksi kuva vastaa 2,9 prosenttiyksikköä, joten 35 kuvan testijoukolla ei voi väittää yhden mallin olevan toista parempi.
3. **Testihäviö kasvoi** mallista 2 malliin 3b (0,47 → 1,36 → 1,90), vaikka tarkkuus pysyi samana. Mallit ovat ylivarmoja virheissään, ja pelkkä tarkkuus antaa liian ruusuisen kuvan.
4. Väärin luokiteltuja kuvia ja virhematriisia on tarkasteltu työkirjoissa. Oletuksemme on, että sekaannukset syntyvät ohuiden, pitkänomaisten esineiden (haarukka, veitsi, kynä) välillä. Tämä tulee tarkistaa virhematriiseista.

## 3. Kohtaamamme haasteet ja ratkaisut

| Haaste | Ratkaisu |
|---|---|
| **Pieni aineisto** (250 kuvaa): oman CNN:n ylisovittumisen riski on suuri. | Augmentointi (peilaus, kierto, zoom, siirto, kirkkaus, kontrasti), Dropout, pieni malli, EarlyStopping ja siirto-oppiminen. |
| **Pieni validointi- ja testijoukko** (40 ja 35 kuvaa): tulokset ovat kohinaisia, ja validointitarkkuus saavutti 100 %, jolloin se ei enää ohjannut koulutusta. | Tulokset tulkittiin varovasti: kuvamäärät raportoitiin prosenttien rinnalla, eikä pieniä eroja väitetty merkittäviksi. Parempi ratkaisu olisi ristiinvalidointi tai lisäkuvat. |
| **Toistettavuus ja datavuoto:** satunnaisjako voisi muuttua ajokerrasta toiseen. | Jako tehdään kiinteällä siemenellä (42), luokkakohtaisesti ja ennen normalisointia. Normalisointitilastot lasketaan vain koulutusdatasta. Lisäksi `keras.utils.set_random_seed(42)` kaikissa työkirjoissa. |
| **Yhtenäinen syöte:** kuvat olivat eri kokoisia ja suuntaisia (EXIF). | Yhteinen esikäsittely: EXIF-kierto, keskirajaus ja skaalaus 224×224:ään. Oma CNN skaalaa pikselit väliin [0, 1], ja VGG16 käyttää omaa `preprocess_input`-funktiotaan. |
| **Laskenta-aika:** VGG16:n hienosäätö on hidasta ilman GPU:ta (noin 20 s / epoch). | Mallissa 2 piirteet esilaskettiin kerran. Hienosäädössä avattiin vain neljä viimeistä kerrosta, ja EarlyStopping lopetti koulutuksen ajoissa. |
| **Epävakaa hienosäätö:** liian suuri oppimisnopeus voi tuhota esikoulutetut painot. | Luokittelija koulutettiin ensin jäädytetyn pohjan päälle, ja hienosäädössä käytettiin pientä oppimisnopeutta (1e-5). |
| **Toistuva koodi:** apufunktiot olivat kopioituina työkirjoissa. | Yhteiset funktiot (`collect_images`, `plot_images`, `plot_confusion_matrix`) siirrettiin tiedostoon `scripts/notebook_scripts.py`. |

## 4. Pohdinta: mallien soveltuvuus ongelmaan

**Oma CNN** on kevyt, nopea kouluttaa ja täysin ymmärrettävä, eikä se tarvitse ulkopuolisia malleja. Kun dataa on vain 35 kuvaa per luokka, sen on kuitenkin opittava kaikki tyhjästä, ja tulos jää noin 69 %:iin. Se sopisi paremmin tilanteeseen, jossa kuvia on tuhansia tai kuvat poikkeavat selvästi ImageNetistä (esim. lääketieteelliset kuvat).

**VGG16 piirteenirrottajana** osoittautui tähän ongelmaan parhaaksi kompromissiksi. Se sai korkeimman tarkkuuden (97,1 %) ja pienimmän testihäviön (0,47), ja koulutus on erittäin nopeaa, koska kuvat kulkevat VGG16:n läpi vain kerran. Haittoja ovat, ettei augmentointia voi käyttää esilasketuilla piirteillä, ja että malli on iso (14,7 milj. parametria) ja siksi raskas käyttää tuotannossa.

**Hienosäädetty VGG16** olisi teoriassa joustavin, koska se voi mukauttaa korkeamman tason piirteitä juuri näihin luokkiin. Tässä aineistossa se ei kuitenkaan parantanut tarkkuutta (97,1 % kuten ennen hienosäätöä), oli laskennallisesti kalliimpi ja kasvatti testihäviötä. Hienosäädöstä olisi todennäköisemmin hyötyä, jos kohdeluokat poikkeaisivat ImageNetin luokista tai aineisto olisi suurempi. Meidän luokkamme (haarukka, muki, lautanen jne.) ovat hyvin lähellä ImageNetin sisältöä.

**Johtopäätös:** tämän projektin ongelmaan (5 selkeää esineluokkaa, pieni aineisto) paras valinta on esikoulutettu VGG16 piirteenirrotuksella. Se on yksinkertaisin ratkaisu ja yhtä tarkka kuin monimutkaisempi hienosäädetty malli. Tärkeimmät jatkokehityskohteet ovat (1) enemmän ja monipuolisempia kuvia (taustat, valaistus, kuvakulmat), (2) ristiinvalidointi, (3) virhematriisien ja luokkakohtaisten mittareiden hyödyntäminen ja (4) kevyempi esikoulutettu malli (esim. MobileNet) mobiilikäyttöön.
