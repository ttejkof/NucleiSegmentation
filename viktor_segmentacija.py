
## FRST: https://github.com/ChristianGutowski/frst_python
## algoritam https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0070221&type=printable

import frst
import numpy as np
import skimage as ski
import cv2
import os
from PIL import Image
import matplotlib.pyplot as plt

def normalize01(x):
    rng = (x.max() - x.min())
    return (x - x.min()) / rng if rng != 0 else np.zeros_like(x)



data_dir = "dataset/Lung"
images_dir = os.path.join(data_dir, "images")
masks_dir = os.path.join(data_dir, "sem_masks")
masks_dir_inst = os.path.join(data_dir, "inst_masks")

image_files = sorted(os.listdir(images_dir))[:6]
mask_files = sorted(os.listdir(masks_dir))[:6]
mask_files_inst = sorted(os.listdir(masks_dir_inst))[:6]


image_files = sorted(os.listdir(images_dir))
chosen = np.random.randint(0, len(image_files)-1, 6)
image_files = [image_files[i] for i in chosen]
mask_files = [sorted(os.listdir(masks_dir))[i] for i in chosen]
mask_files_inst = [sorted(os.listdir(masks_dir_inst))[i] for i in chosen]



def segment_nuclei(image, mask):
    hed = ski.color.rgb2hed(image)
    # h = ski.exposure.rescale_intensity(
    #     hed[:, :, 0],
    #     out_range=(0, 1),
    #     in_range=(0, np.percentile(hed[:, :, 0], 99)),
    # )
    h = hed[:, :, 0]
    # flip
    h = 1-h;

    N = [5, 11, 15, 21, 33]
    panels = {}

    for n in N:
        SE = ski.morphology.disk(n, decomposition='sequence'if n > 15 else None)

        seed = ski.morphology.erosion(h, SE)
        opening = ski.morphology.reconstruction(seed, h, 'dilation')

        seed2 = ski.morphology.dilation(opening, SE)
        closing = ski.morphology.reconstruction(seed2, opening, 'erosion')

        closing2 = ski.morphology.closing(closing, ski.morphology.disk(int(n/2)))

        panels[n] = [
            ("original", image, None),
            ("Hematoxylin", h, 'gray'),
            ("Opening", opening, 'gray'),
            ("Closing", closing, 'gray'),
            (f"Closing2, n={n}", closing2, 'gray'),
            ("mask", mask, 'tab20')
        ]

    fig, axes = plt.subplots(len(panels), len(panels[N[0]]), figsize=(2*len(panels[N[0]]), 2*len(panels)))
    for i, n in enumerate(N):
        for ax, (title, img, cmap) in zip(axes[i], panels[n]):
            ax.imshow(img, cmap=cmap)
            ax.set_title(title, fontsize=10)
            ax.axis("off")
    plt.tight_layout()
    plt.show()






for img_file, mask_file in zip(image_files, mask_files):
   
    image = ski.io.imread(os.path.join(images_dir, img_file))
    mask = np.array(Image.open(os.path.join(masks_dir, mask_file)))
    hed = ski.color.rgb2hed(image)

    segment_nuclei(image, mask)
