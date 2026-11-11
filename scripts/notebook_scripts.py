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