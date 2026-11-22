# Oppimisprojekti 3: Transformer-mallit

**Ryhmä 2:** Elias Eide, Miska Voutilainen, Taif Jalo ja Veijo Kasanen

Notebookit: `Tekstigeneraattori.ipynb` (osa 1) ja `Puheentunnistus.ipynb` (osa 2). Luvut ovat notebookien tulosteista, ja ajot tehtiin CPU:lla.

## 1. Tekstiaineisto

Aineistona on Arthur Conan Doylen *The Adventures of Sherlock Holmes* (Project Gutenberg #1661), 561 KB puhdasta englantia (163 000 tokenia). Doyle kuoli 1930, joten teos on tekijänoikeusvapaa. Valitsimme sen, koska narratiivinen proosa on tunnistettavaa ja aineistoa on riittävästi. Lisenssiteksti, sisällysluettelo ja kursiivimerkit poistettiin. Malli on kurssin Kalevala-pohjan mukainen decoder-only-transformer (upotus, sinimuotoinen paikkakoodaus, kausaalinen multi-head-attention, ff-verkko, Add & Norm) ja tokenisointi on SentencePiece BPE.

## 2. Generoitu teksti ja analyysi

Vertasimme malleja 8 epookin koulutuksella (validointi: tekstin viimeinen 10 %). Muodossa embed / kerrokset / päät:

| malli | rakenne | param. | aika | val loss | perplexity |
|---|---|---|---|---|---|
| minimi | 32 / 1 / 2 | 0,14 M | 3,4 min | 5,05 | 156 |
| pieni | 64 / 2 / 2 | 0,32 M | 4,7 min | 4,74 | 115 |
| keski | 128 / 3 / 4 | 0,91 M | 10,8 min | 4,52 | 92 |
| iso | 256 / 4 / 8 | 3,13 M | 29,6 min | 4,39 | 81 |
| pieni, seq 128 | 64 / 2 / 2 | 0,32 M | 11,8 min | 4,71 | 111 |
| pieni, seq 32 | 64 / 2 / 2 | 0,32 M | 2,2 min | 4,79 | 120 |

**Havainnot.** Loss paranee koon myötä, mutta hinta kasvaa nopeammin: `iso` on 22 kertaa suurempi ja 8,7 kertaa hitaampi kuin `minimi`, ja perplexity paranee 156:sta vain 81:een. `pieni` on hyvä kompromissi. Pidempi `seq_length` paransi vähän mutta maksoi 2,5-kertaisen ajan. Yksi kerros (val loss 4,72) oli yhtä hyvä kuin kaksi, neljä kerrosta huonompi (4,91) ja attention-päiden määrällä (2 vs 8) ei ollut vaikutusta. Kaikki mallit paransivat vielä viimeisellä epookilla, joten yksikään ei konvergoinut, ja vertailu on tasaisella epookkibudjetilla. Sanaston koon (1000 / 2000 / 4000) vertailu loss-arvolla johtaa harhaan, koska tokenin pituus muuttuu (3,0 / 3,4 / 3,9 merkkiä). Merkkiä kohti isompi sanasto oli parempi (noin 1,45 / 1,38 / 1,31 nat/merkki). Generointiin käytettiin pienimmän val lossin mallia (sanasto 1000), mikä on siis vertailuharha.

**Esimerkkejä** (aloitusteksti "Sherlock Holmes"):

- lämpötila 0,2: *Sherlock Holmes, and a lounight of the cably, and a little forested, and the floor of the move of the corner of the...*
- lämpötila 1,0: *Sherlock Holmes creed of them read from Can in sevate sister had seen his mindside to the ces of the sconeoust...*
- lämpötila 1,5: *Sherlock Holmes carhing their mads that comptcolonildfultm the for just hair. Ry every smark arile, lauard...*

Matala lämpötila tuottaa kieliopillisen oloista mutta toistuvaa tekstiä (toistuvia kolmen sanan jaksoja 11 % lämpötilassa 0,2, 2 % lämpötilassa 0,5 ja 0 % lämpötilassa 1,0 ja yli), ja korkea tuottaa keksittyjä sanoja. Isommat mallit tuottivat sujuvampia lauseita (`iso`: *"I knew that I should trust that this gentleman in our room..."*), mutta yksikään ei tuota johdonmukaista kerrontaa.

**Miksi alusta kouluttaminen on hidasta?** Kaikki parametrit alkavat satunnaisina ja kielen rakenne pitää oppia pienestä aineistosta. Silti 11 koulutusta vei noin 85 minuuttia, ja suurin malli (3,1 M parametria) 30 minuuttia ilman konvergenssia. Ulostulokerros laskee todennäköisyyden koko sanastolle, attention kasvaa sekvenssin pituuden neliönä ja hyperparametrien etsintä kertoo kustannuksen kokeiden määrällä. Osan 2 Whisper small (242 M parametria) on 77 kertaa suurempi kuin `iso`-mallimme, ja sen saa valmiiksi koulutettuna.

## 3. Puheentunnistuksen arviointi

Näytteet (alle 30 s, luettu käsikirjoituksesta, joka toimii viitetekstinä): selkeä suomi (`selkea_fi`), taustahälyssä luettu suomi (`haly_fi`), toinen puhuja samalla tekstillä (`puhuja2_fi`), puhekielinen suomi (`murre_fi`, ei alueellinen murre) ja englanti (`selkea_en`).

| näyte | WER tiny | WER base | WER small |
|---|---|---|---|
| selkea_fi | 0,74 | 0,56 | 0,32 |
| haly_fi | 0,77 | 0,65 | 0,26 |
| puhuja2_fi | 0,47 | 0,35 | 0,18 |
| murre_fi | 0,55 | 0,41 | 0,24 |
| selkea_en | 0,04 | 0,06 | 0,04 |
| **keskiarvo** (CER) | 0,51 (0,14) | 0,41 (0,09) | 0,21 (0,06) |
| nopeus (CPU, RTF) | 3,0 s (0,12) | 5,6 s (0,22) | 11,5 s (0,47) |

**Koko:** `small` on suomessa selvästi paras, mutta 4 kertaa hitaampi kuin `tiny`. WER on suomessa korkea myös hyvällä mallilla, koska yksi väärä kirjain tekee koko sanasta virheen (`tiny`, `selkea_fi`: WER 0,74 mutta CER 0,19). Englannissa jo `tiny` riittää (WER 0,04), eli pieni malli riittää helpolle kielelle. **Puhuja:** sama teksti toisen puhujan lukemana tunnistui paremmin (`small` 0,18 vs 0,32), mutta kahdella puhujalla syytä ei voi erottaa. **Kielentunnistus:** suomi tunnistettiin oikein kaikilla malleilla, mutta `base` luuli englantia latinaksi.

**Kohinakoe** (`selkea_fi` + keinotekoinen kohina, WER):

| SNR (dB) | puhdas | 20 | 10 | 5 | 0 | −5 |
|---|---|---|---|---|---|---|
| tiny | 0,74 | 0,85 | 0,97 | 1,06 | 6,47 | 3,32 |
| small | 0,32 | 0,35 | 0,53 | 0,68 | 0,74 | 0,85 |

`small` kestää kohinaa selvästi paremmin. Pienet mallit hallusinoivat noin 0 dB:n kohdalla (WER yli 1, esim. `tiny` −5 dB:ssä: *"jäämään jäämään jäämään..."*). Tulokset perustuvat viiteen näytteeseen ja yhteen puhujaan kutakin, joten ne ovat suuntaa-antavia.

## 4. Mel-spektrogrammi omin sanoin

Spektrogrammissa vaaka-akseli on aika ja pystyakseli äänen taajuus. Mel-asteikossa taajuus on venytetty ihmisen kuulon mukaiseksi: matalille taajuuksille tulee paljon tarkkuutta ja korkeille vähemmän. Väri kertoo äänen voimakkuuden desibeleinä, ja kirkas väri tarkoittaa voimakasta energiaa kyseisellä hetkellä ja taajuudella. Raaka äänisignaali on pitkä lukujono (16 000 arvoa sekunnissa), josta esimerkiksi vokaaleja ei voi lukea suoraan. Spektrogrammissa samat piirteet näkyvät kuvioina, joita verkko oppii tunnistamaan, ja esitys on huomattavasti lyhyempi. Whisper on transformer, kuten osan 1 generaattori: osassa 1 teksti pilkotaan tokeneiksi ja muutetaan upotuksiksi, ja Whisperissä spektrogrammin aikakehyksistä tulee vastaavat upotukset, joita attention vertailee. Dekooderi tuottaa tekstin token kerrallaan kuten generaattorimme, ja lämpötila vaikuttaa siihen samalla tavalla. Notebookin visualisointi käyttää 128 mel-kaistaa (librosa), kun Whisperin tiny–small käyttävät sisäisesti 80.

## 5. Pohdinta: transformerien vahvuudet ja rajoitukset

**Vahvuudet.** Attention tarkastelee koko sekvenssiä kerralla, ja sama arkkitehtuuri toimii tekstille ja äänelle. Esikoulutettu malli antaa hyvän tuloksen ilman omaa koulutusta: `small` tunnisti englannin lähes virheettömästi, kun oma pieni mallimme tuotti vain kielen näköistä tekstiä.

**Rajoitukset.** Alusta kouluttaminen vaatii paljon dataa ja laskentaa, ja isompi malli maksaa nopeasti enemmän kuin se tuo (`iso`: 8,7-kertainen aika, perplexity 156 → 81). Mallit hallusinoivat kohinassa, ovat huonompia pienemmillä kielillä (suomen WER oli englantia selvästi korkeampi) ja niiden tarkkuus riippuu koosta, jolloin nopeus ja laatu kilpailevat keskenään. Attentionin kustannus kasvaa sekvenssin pituuden neliönä.

## 6. Tekoälyn käyttö

Projektissa käytettiin Claudea (Claude Code) tekoälyavusteisena työkaluna. Sitä käytettiin seuraaviin tehtäviin:

- notebookien pohjien tekeminen kurssin tukimateriaalin (`Puheentunnistus.ipynb`, `Whisper_simple.ipynb` ja `LLM_Keras_Kalevala_pieni.ipynb`) pohjalta
- apukoodin kirjoittaminen: WER:n ja CER:n laskenta, kohinakoe, kielentunnistus, mallien vertailutaulukot ja kuvaajat sekä tekstin siivous
- koodivirheiden selvittäminen (puuttuvat kirjastot, kielentunnistuksen korjaus, tiedostopolut)

Tekoäly ei tuottanut projektin mittaustuloksia. Ryhmä äänitti ääninäytteet, ajoi notebookit ja koulutti mallit itse, ja kaikki luvut (WER, CER, koulutusajat, parametrimäärät ja validation loss) ovat notebookien omista tulosteista. Ryhmä vastaa itse tulosten tulkinnasta ja johtopäätöksistä.
