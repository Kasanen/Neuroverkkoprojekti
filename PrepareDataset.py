"""
Kuvadatan valmistelu: hakemistorakenne, esikäsittely ja jako train/val/test.

Odotettu lähtörakenne (yksi kansio per luokka):

    raw_images/
        luokka_1/  kuva1.jpg, kuva2.jpg, ...
        luokka_2/  ...
        ...

Tuloksena syntyvä rakenne:

    dataset/
        train/<luokka>/*.jpg
        val/<luokka>/*.jpg
        test/<luokka>/*.jpg
        stats.json            (train-datan keskiarvo ja keskihajonta per kanava)
        arrays/               (normalisoidut numpy-taulukot: X_train.npy, y_train.npy, ...)
        split_manifest.csv    (mikä kuva meni mihin joukkoon)

Käyttö:
    pip install pillow numpy
    python prepare_dataset.py --src raw_images --dst dataset --size 224
"""

import argparse
import csv
import json
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}


def list_images(class_dir: Path):
    return sorted(p for p in class_dir.iterdir() if p.suffix.lower() in IMAGE_EXTS)


def split_indices(n, train_frac, val_frac, rng):
    """Palauttaa (train, val, test) -indeksilistat yhdelle luokalle."""
    idx = list(range(n))
    rng.shuffle(idx)
    n_train = int(round(n * train_frac))
    n_val = int(round(n * val_frac))
    train = idx[:n_train]
    val = idx[n_train:n_train + n_val]
    test = idx[n_train + n_val:]
    return train, val, test


def preprocess(path: Path, size: int) -> Image.Image:
    """Avaa kuva, korjaa EXIF-kierto, rajaa neliöksi keskeltä ja skaalaa size x size."""
    img = Image.open(path)
    img = ImageOps.exif_transpose(img)
    img = img.convert("RGB")
    # fit = keskeltä rajaus kuvasuhteeseen 1:1 + koon muutos
    return ImageOps.fit(img, (size, size), method=Image.LANCZOS, centering=(0.5, 0.5))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="raw_images", help="lähdekansio (alikansio per luokka)")
    ap.add_argument("--dst", default="dataset", help="kohdekansio")
    ap.add_argument("--size", type=int, default=224, help="kuvan sivun pituus pikseleinä")
    ap.add_argument("--train", type=float, default=0.70)
    ap.add_argument("--val", type=float, default=0.15)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--no-arrays", action="store_true", help="älä tallenna normalisoituja .npy-tiedostoja")
    args = ap.parse_args()

    src, dst = Path(args.src), Path(args.dst)
    classes = sorted(d.name for d in src.iterdir() if d.is_dir())
    if not classes:
        raise SystemExit(f"Kansiosta {src} ei löytynyt luokkakansioita.")
    print(f"Luokat ({len(classes)}): {classes}")

    rng = random.Random(args.seed)

    # 1) Hakemistorakenne
    for split in ("train", "val", "test"):
        for c in classes:
            (dst / split / c).mkdir(parents=True, exist_ok=True)

    # 2) Esikäsittely + jako (stratifioitu: jako tehdään erikseen jokaisessa luokassa)
    manifest = []
    for c in classes:
        files = list_images(src / c)
        if len(files) < 50:
            print(f"  Varoitus: luokassa '{c}' on vain {len(files)} kuvaa (vaatimus >= 50)")
        tr, va, te = split_indices(len(files), args.train, args.val, rng)
        for split, ids in (("train", tr), ("val", va), ("test", te)):
            for i in ids:
                img = preprocess(files[i], args.size)
                out = dst / split / c / f"{files[i].stem}.jpg"
                img.save(out, quality=95)
                manifest.append((split, c, files[i].name, str(out)))
        print(f"  {c}: {len(files)} kuvaa -> train {len(tr)}, val {len(va)}, test {len(te)}")

    with open(dst / "split_manifest.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["split", "class", "original_file", "output_file"])
        w.writerows(manifest)

    # 3) Normalisointi: keskiarvo/keskihajonta lasketaan VAIN train-datasta
    class_to_idx = {c: i for i, c in enumerate(classes)}

    def load_split(split):
        X, y = [], []
        for c in classes:
            for p in sorted((dst / split / c).glob("*.jpg")):
                arr = np.asarray(Image.open(p), dtype=np.float32) / 255.0  # skaalaus [0, 1]
                X.append(arr)
                y.append(class_to_idx[c])
        return np.stack(X), np.array(y, dtype=np.int64)

    X_train, y_train = load_split("train")
    mean = X_train.mean(axis=(0, 1, 2))
    std = X_train.std(axis=(0, 1, 2))
    stats = {"mean": mean.tolist(), "std": std.tolist(),
             "classes": classes, "image_size": args.size}
    with open(dst / "stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    print(f"\nTrain-datan mean={mean.round(4)}, std={std.round(4)}")

    if not args.no_arrays:
        arr_dir = dst / "arrays"
        arr_dir.mkdir(exist_ok=True)
        for split in ("train", "val", "test"):
            X, y = (X_train, y_train) if split == "train" else load_split(split)
            X = (X - mean) / std  # standardointi train-tilastoilla
            np.save(arr_dir / f"X_{split}.npy", X.astype(np.float32))
            np.save(arr_dir / f"y_{split}.npy", y)
            print(f"  {split}: X{X.shape}, y{y.shape}")

    print(f"\nValmis. Data kansiossa: {dst.resolve()}")


if __name__ == "__main__":
    main()