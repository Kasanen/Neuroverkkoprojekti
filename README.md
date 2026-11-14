# Neuroverkot: kotitalousesineiden kuvantunnistus

Kuvantunnistusprojekti, jossa luokitellaan itse otetut kuvat viiteen luokkaan (**fork, knife, mug, pen, plate**) kolmella eri konvoluutioneuroverkkomenetelmällä. Menetelmät etenevät yksinkertaisesta vaativampaan.

## Tulokset

Testijoukossa on 35 kuvaa, joten yhden kuvan ero on noin 2,9 prosenttiyksikköä.

| Malli | Menetelmä | Testitarkkuus | Oikein / 35 |
|---|---|---:|---:|
| 1 | Oma CNN alusta alkaen | 68,6 % | 24 |
| 2 | VGG16 piirteenirrottajana + oma luokittelija | 97,1 % | 34 |
| 3a | VGG16 jäädytettynä + augmentointi | 97,1 % | 34 |
| 3b | VGG16, viimeiset 4 kerrosta hienosäädetty | 97,1 % | 34 |

Täydellinen vertailu, haasteet ja pohdinta ovat raportissa [RAPORTTI.md](RAPORTTI.md).

## Rakenne

```
images/                  alkuperäiset kuvat, alikansio per luokka (50 kpl / luokka)
dataset/
  train/<luokka>/        175 kuvaa (35 / luokka)
  validation/<luokka>/   40 kuvaa (8 / luokka)
  test/<luokka>/         35 kuvaa (7 / luokka)
  stats.json             train-datan keskiarvo ja keskihajonta per kanava
  split_manifest.csv     mikä kuva meni mihin joukkoon
  arrays/                normalisoidut .npy-taulukot (ei gitissä, luodaan skriptillä)
scripts/notebook_scripts.py   yhteiset apufunktiot (collect_images, plot_images, plot_confusion_matrix)
RAPORTTI.md             projektiraportti
PrepareDataset.py        datan esikäsittely ja jako
CNN-Malli.ipynb          Malli 1
Esikoulutettu-Malli.ipynb  Malli 2
Hienosaadetty-malli.ipynb  Malli 3
```

## Dataset

- 250 itse otettua kuvaa, 50 per luokka. Kohteet on kuvattu selkeästi esillä ja taustat pidetty yksinkertaisina.
- Esikäsittely ([PrepareDataset.py](PrepareDataset.py)): EXIF-kierron korjaus, rajaus neliöksi keskeltä, koon muutos 224×224 ja normalisointi. Normalisoinnin tilastot lasketaan vain train-datasta.
- Jako on stratifioitu 70 / 15 / 15 siemenluvulla 42 erillisiin hakemistoihin (Kerasin `validation_split`-optiota ei käytetä).
- Augmentaatiota käytetään vain harjoitusdatalle (malleissa 1 ja 3a). Malli 2 laskee piirteet etukäteen ilman augmentaatiota. Validointi- ja testidata pidetään koskemattomina.

## Ajaminen

Tarvitaan Python 3, `tensorflow` (Keras 3), `numpy`, `pillow` ja `matplotlib`.

```bash
python -m venv .venv && source .venv/bin/activate
pip install tensorflow numpy pillow matplotlib jupyter

# Dataset on valmiina kansiossa dataset/. Uudelleenluonti kuvista:
python PrepareDataset.py --src images --dst dataset --size 224

jupyter notebook
```

Aja työkirjat tässä järjestyksessä: `CNN-Malli.ipynb`, `Esikoulutettu-Malli.ipynb`, `Hienosaadetty-malli.ipynb`. Työkirjat käyttävät Kerasin taustana TensorFlow'ta ja ladataan VGG16:n ImageNet-painot ensimmäisellä ajolla (vaatii verkkoyhteyden).

Jokaisessa työkirjassa on oppimiskäyrät, väärin luokiteltujen kuvien tarkastelu ja testijoukon virhematriisi.
