import os
import cv2

# example of calculating the frechet inception distance
import numpy as np
from matplotlib import pyplot as plt

def calculate_mean(arr):
    summ = arr.sum()
    mean = 0
    for i, count in enumerate(arr):
        mean += i*count
    mean/=summ
    cov = 0
    for i, count in enumerate(arr):
        cov+= ((i-mean)**2)*count
    cov/=summ

    return mean, np.sqrt(cov)

def calcFIDbyHist(etal_hist, gen_hist):
    m1, s1 = calculate_mean(etal_hist)
    m2, s2 = calculate_mean(gen_hist)

    print(m1, m2, s1, s2)
    #cv2.imshow("etalon", etalon)
    #cv2.imshow("slice", slice)
    #cv2.waitKey()

    score = (m1-m2)**2 + (s1-s2)**2
    return score

def calcAllHist(imgs_path, img_names, mask_use):
    calc_hist = np.zeros(256, np.uint64)

    for img_name in img_names:
        img_path = os.path.join(imgs_path, 'original', img_name)
        img = cv2.imread(img_path, 0)
        img = np.expand_dims(img, -1)

        if mask_use is None:
            mask = None
        else:
            if not os.path.isdir(os.path.join(imgs_path, mask_use)):
                if mask_use == "mitochondrial_boundaries":
                    mask_use = "mitochondrial boundaries"
                else:
                    raise Exception(f"Don't find {mask_use}\nin {os.path.join(imgs_path, mask_use)}")

            path_mask = os.path.join(imgs_path, mask_use, img_name)
            mask = cv2.imread(path_mask, 0)
            mask[mask>127]=255
            mask[mask<128]=0

        hist = (np.array(cv2.calcHist([img], [0], mask, [256], [0,256]))).squeeze().squeeze().astype(np.uint64)
        calc_hist += hist

    return(calc_hist)

def viewHistPlot(etal_hist, gen_hist, name_plot, view = False):
    plt.plot(etal_hist / np.linalg.norm(etal_hist), color = 'g', label="Real data")
    plt.plot(gen_hist /  np.linalg.norm(gen_hist), color = 'r', label="Synthetic data")
    plt.title(f'Histograms of {name_plot}')
    plt.legend()

    if not view:
        plt.savefig("FID_HIST/"+ f'{name_plot}' +".png", dpi=600)
    plt.show()

etal_dir = "G:/Data/Unet_multiclass/data/original data"
gen_dir = "C:/Users/Sokol-PC/Synthetics/dataset/synthetic_dataset10"

mask_names = [None, "axon", "boundaries", "mitochondria", "mitochondrial_boundaries", "vesicles", "PSD"]

etal_names = [name for name in os.listdir(os.path.join(etal_dir, 'original')) if name.endswith(".png")]
gen_names =  [name for name in os.listdir(os.path.join(gen_dir, 'original'))  if name.endswith(".png")]

map_plot = {None: "All dataset",
            "axon": "Axon",
            "boundaries": "Membrane",
            "mitochondria": "Mitochondrion",
            "mitochondrial_boundaries": "Mitochondrial boundaries",
            "vesicles": "Vesicles",
            "PSD": "PSD"}


print(f"number etalons: {len(etal_names)}")
print(f"number gen: {len(gen_names)}")

assert(len(etal_names) > 0)
assert(len(gen_names) > 0)

Score_list = []

for mask_use in mask_names:
    print(f"calculate etal {map_plot[mask_use]}")

    print("\n\tcalculate etal")
    etal_hist = calcAllHist(etal_dir, etal_names, mask_use)
    print(etal_hist)

    print("\n\tcalculate gen")
    gen_hist = calcAllHist(gen_dir, gen_names, mask_use)
    print(gen_hist)

    score = calcFIDbyHist(etal_hist, gen_hist)
    print(f"\n\tcalculate FID: {score}\n")
    Score_list.append(score)

    viewHistPlot(etal_hist, gen_hist, map_plot[mask_use])


str_name = "| "
str_fid  = "| "

for i in range(len(Score_list)):
    print_name = map_plot[mask_names[i]]
    str_fid_now = f"{Score_list[i]:.4f}"

    len_name = len(print_name)
    len_score = len(str_fid_now)

    if len_name < len_score:
        str_name += f"{print_name}{' '*(len_score - len_name)} | "
        str_fid += f"{str_fid_now} | "
    else:
        str_name += f"{print_name} | "
        str_fid += f"{str_fid_now}{' '*(len_name - len_score)} | "

print(str_name)
print(str_fid)
