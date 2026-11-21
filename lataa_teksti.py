"""Lataa Sherlock Holmes -tekstin Project Gutenbergista ja siivoaa sen (sherlock_puhdas.txt)."""
import re
import urllib.request

# Arthur Conan Doyle: The Adventures of Sherlock Holmes (Project Gutenberg #1661)
# Doyle kuoli 1930, joten teos on tekijänoikeusvapaa.
URLS = [
    "https://gutenberg.pglaf.org/1/6/6/1661/1661-0.txt",
    "https://www.gutenberg.org/cache/epub/1661/pg1661.txt",
    "http://aleph.gutenberg.org/1/6/6/1661/1661-0.txt",
]
RAW_FILE = "sherlock_raw.txt"
TEXT_FILE = "sherlock_puhdas.txt"

for url in URLS:
    try:
        urllib.request.urlretrieve(url, RAW_FILE)
        print("Ladattu:", url)
        break
    except Exception as e:
        print("Epäonnistui:", url, e)
else:
    raise SystemExit(f"Lataa teksti selaimella (gutenberg.org/ebooks/1661, Plain Text UTF-8) ja tallenna nimellä {RAW_FILE}")

with open(RAW_FILE, "r", encoding="utf-8-sig") as f:
    raw = f.read().replace("\r\n", "\n")

# Poistetaan Project Gutenbergin lisenssiteksti alusta ja lopusta
alku = raw.index("*** START OF")
alku = raw.index("***", alku + 3) + 3   # otsikkorivi voi jatkua seuraavalle riville
loppu = raw.index("*** END OF")
text = raw[alku:loppu]
text = text[text.index("I. A SCANDAL IN BOHEMIA"):]   # hypätään sisällysluettelon yli

# Yhdistetään rivinvaihdolla katkaistut rivit kappaleiksi ja siivotaan tyhjät
text = text.replace("_", "")   # poistetaan kursiivimerkinnät
text = re.sub(r"\[Illustration[^\]]*\]", "", text)
text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)
text = re.sub(r"[ \t]+", " ", text)
text = re.sub(r"\n{3,}", "\n\n", text).strip()

with open(TEXT_FILE, "w", encoding="utf-8") as f:
    f.write(text)
print(f"{TEXT_FILE}: {len(text)} merkkiä ({len(text.encode('utf-8'))/1024:.0f} KB)")
