import numpy as np
import matplotlib.pyplot as plt

def collect_images(dataset, model):
    class_names = dataset.class_names
    correct, wrong = [], []

    for images, labels in dataset:
        original_images = images.numpy().astype("uint8")

        preds = model.predict(images, verbose=0)
        pred_labels = np.argmax(preds, axis=1)
        true_labels = np.argmax(labels.numpy(), axis=1)

        for img, t, p in zip(original_images, true_labels, pred_labels):
            entry = (img, class_names[t], class_names[p])
            if t == p:
                correct.append(entry)
            else:
                wrong.append(entry)

    return correct, wrong

def plot_images(images_list, title, n=8):
    num = min(n, len(images_list))
    if num == 0:
        print(f"{title}: no images")
        return
    cols = 4
    rows = (num + cols - 1) // cols
    plt.figure(figsize=(cols*3, rows*3))

    for i in range(num):
        ax = plt.subplot(rows, cols, i+1)
        plt.imshow(images_list[i][0])
        plt.title(f"True: {images_list[i][1]}\nPred: {images_list[i][2]}", fontsize=10)
        plt.axis("off")

    plt.suptitle(title, fontsize=15)
    plt.tight_layout()
    plt.show()

def plot_confusion_matrix(entries, class_names, title="Confusion matrix (test set)"):
    """Piirtää virhematriisin collect_images-funktion palauttamista (kuva, tosi, ennuste) -riveistä
    ja tulostaa yleisimmät sekaannukset. Rivit = oikea luokka, sarakkeet = ennuste."""
    idx = {name: i for i, name in enumerate(class_names)}
    n = len(class_names)
    cm = np.zeros((n, n), dtype=int)
    for _, true, pred in entries:
        cm[idx[true], idx[pred]] += 1

    plt.figure(figsize=(5, 4.5))
    plt.imshow(cm, cmap="Blues")
    plt.colorbar()
    plt.xticks(range(n), class_names, rotation=45)
    plt.yticks(range(n), class_names)
    for i in range(n):
        for j in range(n):
            plt.text(j, i, cm[i, j], ha="center", va="center",
                     color="white" if cm[i, j] > cm.max() / 2 else "black")
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.title(title)
    plt.tight_layout()
    plt.show()

    print("Luokkakohtainen tarkkuus (recall):")
    for i, name in enumerate(class_names):
        total = cm[i].sum()
        print(f"  {name:6s} {cm[i, i]}/{total} = {cm[i, i] / total:.0%}")
    errors = [(cm[i, j], class_names[i], class_names[j])
              for i in range(n) for j in range(n) if i != j and cm[i, j] > 0]
    print("Sekaannukset (oikea -> ennuste):")
    for count, t, p in sorted(errors, reverse=True):
        print(f"  {t} -> {p}: {count}")
    return cm
