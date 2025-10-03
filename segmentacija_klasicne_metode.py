
## FRST: https://github.com/ChristianGutowski/frst_python
## algoritam https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0070221&type=printable

# from frst import frst
import numpy as np
import skimage as ski
import cv2
import os
from PIL import Image
import matplotlib.pyplot as plt

def normalize01(x):
    rng = (x.max() - x.min())
    return (x - x.min()) / rng if rng != 0 else np.zeros_like(x)

def frst(img, radii, std):
    O_n = np.zeros_like(img, np.uint8)
    pad_val = np.max(radii)
    O_n = np.pad(O_n, pad_val)

    gx = ski.filters.sobel_h(img)
    gy = ski.filters.sobel_v(img)

    gnorms = np.sqrt( np.add( np.multiply(gx, gx) , np.multiply(gy, gy) ) )

    gpx = np.divide(gx, gnorms, out=np.zeros(gx.shape), where=gnorms!=0)
    gpx = np.stack([np.round(gpx * r).astype(int) for r in radii], axis=-1)

    gpy = np.divide(gy, gnorms, out=np.zeros(gy.shape), where=gnorms!=0)
    gpy = np.stack([np.round(gpy * r).astype(int) for r in radii], axis=-1)


    Ni, Nj = gnorms.shape

    for i in range(Ni):
        for j in range(Nj):
            if gnorms[i,j] > 0:
                ppve = (i+gpx[i,j], j + gpy[i,j])
                O_n[ppve] += 1
                
                pnve = (i-gpx[i,j], j - gpy[i,j])
                O_n[pnve] += 1
        


    
    if np.max(O_n) > 0:
        O_n =  O_n/ float(np.max(O_n))
    
    S = ski.filters.gaussian(O_n, std)

    S = S[:-2*pad_val, :-2*pad_val]
    return S


def morphological(h, n, panels):
    SE = ski.morphology.disk(n, decomposition='sequence'if n > 15 else None)

    seed = ski.morphology.erosion(h, SE)
    opening = ski.morphology.reconstruction(seed, h, 'dilation')

    seed2 = ski.morphology.dilation(opening, SE)
    closing = ski.morphology.reconstruction(seed2, opening, 'erosion')

    closing2 = ski.morphology.closing(closing, ski.morphology.disk(int(n/2)))

    # flipped for better visibility
    print(np.max(h))
    print(np.max(opening))
    print(np.max(closing))
    print(np.max(closing2))


    # negative for better visualisation
    panels[n] = [
        ("original", image, None),
        ("Hematoxylin", 1-h, 'gray'),
        ("Opening", 1-opening, 'gray'),
        ("Closing", 1-closing, 'gray'),
        (f"Closing2, n={n}", 1-closing2, 'gray'),
        ("mask", mask, 'tab20')
    ]
    res = ski.exposure.rescale_intensity(closing2, out_range=(0,255))
    return res, panels

def segment_nuclei(image, mask):
    hed = ski.color.rgb2hed(image)

    h = hed[:, :, 0]

    N = [5, 11, 15, 33]
    panels = {}

    for n in N:
        res, panels = morphological(h, n, panels)

        radii = np.array(range(n, 2*n))

        frst_res = frst(res, radii, std=0)

        panels[n].append(('frst', frst_res, 'gray'))
        

    fig, axes = plt.subplots(len(panels), len(panels[N[0]]), figsize=(2*len(panels[N[0]]), 2*len(panels)))
    for i, n in enumerate(N):
        for ax, (title, img, cmap) in zip(axes[i], panels[n]):
            if cmap == 'gray':
                # ax.imshow(img, cmap=cmap, vmin=0, vmax=1)
                ax.imshow(img, cmap=cmap)
            else:
                ax.imshow(img, cmap=cmap)
            ax.set_title(title, fontsize=10)
            ax.axis("off")
    plt.tight_layout()
    plt.show()




def fit_ellipse(masks_dir):
    mask_filenames = os.listdir(masks_dir)

    for filename in mask_filenames:

        file = os.path.join(masks_dir, filename)
        mask = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
        normalized = np.zeros_like(mask)
        cv2.normalize(mask, normalized, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

        # Threshold just in case (ensure binary)
        _, thresh = cv2.threshold(normalized, 127, 255, cv2.THRESH_BINARY)

        # Find contours (cv2.RETR_EXTERNAL for only outermost, use cv2.RETR_TREE if nested)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # Copy to visualize
        ellipse_img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

        for cnt in contours:
            if len(cnt) >= 5:  # fitEllipse needs at least 5 points
                cv2.drawContours(ellipse_img, [cnt], -1, (255, 0, 0), 2)
                # ellipse = cv2.fitEllipse(cnt)
                # cv2.ellipse(ellipse_img, ellipse, (0,255,0), 2)

        # Show result
        plt.figure(figsize=(10,5))
        plt.subplot(1,2,1); plt.title("Original mask"); plt.imshow(mask, cmap='gray')
        plt.subplot(1,2,2); plt.title("Fitted ellipses"); plt.imshow(ellipse_img[...,::-1])
        plt.show()
    



if __name__ == '__main__':
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

    # for img_file, mask_file in zip(image_files, mask_files):

    image = ski.io.imread(os.path.join(images_dir, 'img_Lung_2_00771.png'))

    mask = np.array(Image.open(os.path.join(masks_dir, 'sem_Lung_2_00771.png')))
    hed = ski.color.rgb2hed(image)

    segment_nuclei(image, mask)
    plt.show()

        # ==========test frst===============
        # frst_res = frst(mask, range(1, 7), 2)
        
        # panels = [
        #     ('image', image, None),
        #     ('mask', mask, 'tab20'),
        #     ('frst', frst_res, 'gray')

        # ]
   
        # fig, axes = plt.subplots(1, len(panels), figsize=(4*len(panels), 4))
        # for ax, (title, img, cmap) in zip(axes, panels):
        #     if cmap == 'gray':
        #         # ax.imshow(img, cmap=cmap, vmin=0, vmax=1)
        #         ax.imshow(img, cmap=cmap)
        #     else:
        #         ax.imshow(img, cmap=cmap)
        #     ax.set_title(title, fontsize=10)
        #     ax.axis("off")
        # plt.tight_layout()
        # plt.show()

    # fit_ellipse(masks_dir_inst)