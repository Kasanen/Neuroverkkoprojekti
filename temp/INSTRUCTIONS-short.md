# Mitä teemme?

Rakennamme neuroverkon, joka tunnistaa eläimen sen äänestä. Syötteenä on 5 sekunnin äänileike, ja malli kertoo, onko kyseessä koira, kissa, kukko, sika, lehmä, sammakko, kana, hyönteiset, lammas vai varis. Data on ESC-50-datasetin 10 eläinluokkaa, yhteensä 400 leikettä.

# Miten se toimii?

Muutamme jokaisen äänen spektrogrammiksi eli kuvaksi, jossa näkyy, mitä taajuuksia äänessä on milloinkin. Sen jälkeen konvoluutioverkko käsittelee sitä kuin tavallista kuvaa.

# Mitä vertaamme?

Koulutamme neljä mallia ja katsomme, kuinka paljon kukin lisäys auttaa:

1. Yksinkertainen CNN, joka on vertailukohta.
2. Parempi CNN, jossa on regularisointi ja augmentaatio. Augmentaatiossa lisäämme dataan muunnoksia, kuten kohinaa ja peitettyjä kohtia spektrogrammissa.
3. YAMNet, jonka Google on valmiiksi opettanut tunnistamaan ääniä. Käytämme sitä siirto-oppimisella.
4. EfficientNet, joka on kuvamalli ja jonka hienosäädämme spektrogrammeille.

# Mitä lopuksi saamme?

Vertailun siitä, mikä lähestymistapa toimii parhaiten ja miksi. Mukana ovat myös virheanalyysi (mitkä eläimet sekoittuvat keskenään) ja toimiva demo, johon voi ladata äänen ja nähdä mallin arvauksen.

# Aikataulu

Aikataulu: palautus on 11.12.2026. Koodin pitäisi olla valmis noin 6.12. mennessä, jotta raportille ja esitykselle jää aikaa.
