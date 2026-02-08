import os
import numpy as np
import skimage
from skimage.feature import graycomatrix, graycoprops
from skimage import io, color
import matplotlib.pyplot as plt



#folder_path = "D:/Data/Unet_multiclass/data/train slices"
#work_fun(folder_path)

#main_path = "D:/Projects/UnetClass/pytorch/diffusion/"

folders_real = [
    "D:/Data/Unet_multiclass/data/cutting data/original",
    "D:/Data/Unet_multiclass/data/cutting data mito all/original",
    "D:/Data/Unet_multiclass/data/train slices/",
    "D:/Data/Unet_multiclass/data/test",
    "D:/Data/Unet_multiclass/data/testTest",
    "D:/Data/данные с митохондриями/АС4/train",
    "D:/Data/данные с митохондриями/Kasthuri/Test_In",
    "D:/Data/данные с митохондриями/Kasthuri/Train_In",
    "D:/Data/данные с митохондриями/UroCell-master/data/fib1-0-0-0"
]

folder_geom = [
    "D:/Projects/Synthetics/dataset/synthetic_dataset10/original"
    ]

main_folder = "D:/Projects/UnetClass/pytorch/diffusion/"
folders_sint = [
    "result_t_dataset_5_slices_1_classes",
    "result_t_dataset_5_slices_5_classes",
    "result_t_dataset_5_slices_6_classes",
    "result_t_dataset_10_slices_1_classes",
    "result_t_dataset_10_slices_5_classes",
    "result_t_dataset_10_slices_6_classes",
    "result_t_dataset_15_slices_1_classes",
    "result_t_dataset_15_slices_5_classes",
    "result_t_dataset_15_slices_6_classes",
    "result_t_dataset_20_slices_1_classes",
    "result_t_dataset_20_slices_5_classes",
    "result_t_dataset_20_slices_6_classes",
    "result_t_dataset_30_slices_1_classes",
    "result_t_dataset_30_slices_5_classes",
    "result_t_dataset_30_slices_6_classes",
    "result_t_dataset_42_slices_1_classes",
    "result_t_dataset_42_slices_5_classes",
    "result_t_dataset_42_slices_6_classes",
    "result_t_dataset_100_slices_1_classes",
    "result_t_dataset_165_slices_1_classes"
]

folder_path_list = folders_real + folder_geom + [main_folder + folder + "/original" for folder in folders_sint]





def graycoprops_mods(P, prop='contrast'):
    """Calculate texture properties of a GLCM.

    Compute a feature of a gray level co-occurrence matrix to serve as
    a compact summary of the matrix. The properties are computed as
    follows:

    - 'contrast': :math:`\\sum_{i,j=0}^{levels-1} P_{i,j}(i-j)^2`
    - 'dissimilarity': :math:`\\sum_{i,j=0}^{levels-1}P_{i,j}|i-j|`
    - 'homogeneity': :math:`\\sum_{i,j=0}^{levels-1}\\frac{P_{i,j}}{1+(i-j)^2}`
    - 'ASM': :math:`\\sum_{i,j=0}^{levels-1} P_{i,j}^2`
    - 'energy': :math:`\\sqrt{ASM}`
    - 'correlation':
        .. math:: \\sum_{i,j=0}^{levels-1} P_{i,j}\\left[\\frac{(i-\\mu_i) \\
                  (j-\\mu_j)}{\\sqrt{(\\sigma_i^2)(\\sigma_j^2)}}\\right]

    """
    #check_nD(P, 4, 'P')

    (num_level, num_level2, num_dist, num_angle) = P.shape
    if num_level != num_level2:
        raise ValueError('num_level and num_level2 must be equal.')
    if num_dist <= 0:
        raise ValueError('num_dist must be positive.')
    if num_angle <= 0:
        raise ValueError('num_angle must be positive.')

    # normalize each GLCM
    P = P.astype(np.float64)
    glcm_sums = np.sum(P, axis=(0, 1), keepdims=True)
    glcm_sums[glcm_sums == 0] = 1
    P /= glcm_sums

    # create weights for specified property
    I, J = np.ogrid[0:num_level, 0:num_level]
    if prop == 'contrast':
        weights = (I - J) ** 2
    elif prop == 'dissimilarity':
        weights = np.abs(I - J)
    elif prop == 'homogeneity':
        weights = 1.0 / (1.0 + (I - J) ** 2)
    elif prop in ['ASM', 'energy', 'correlation', 'entropy']:
        pass
    else:
        raise ValueError(f'{prop} is an invalid property')

    # compute property for each GLCM
    if prop == 'energy':
        asm = np.sum(P**2, axis=(0, 1))
        results = np.sqrt(asm)
    elif prop == 'entropy':
        results = -np.sum(P*np.log(P, where=(P!=0)), axis=(0, 1))
    elif prop == 'ASM':
        results = np.sum(P**2, axis=(0, 1))
    elif prop == 'correlation':
        results = np.zeros((num_dist, num_angle), dtype=np.float64)
        I = np.array(range(num_level)).reshape((num_level, 1, 1, 1))
        J = np.array(range(num_level)).reshape((1, num_level, 1, 1))
        diff_i = I - np.sum(I * P, axis=(0, 1))
        diff_j = J - np.sum(J * P, axis=(0, 1))

        std_i = np.sqrt(np.sum(P * (diff_i) ** 2, axis=(0, 1)))
        std_j = np.sqrt(np.sum(P * (diff_j) ** 2, axis=(0, 1)))
        cov = np.sum(P * (diff_i * diff_j), axis=(0, 1))

        # handle the special case of standard deviations near zero
        mask_0 = std_i < 1e-15
        mask_0[std_j < 1e-15] = True
        results[mask_0] = 1

        # handle the standard case
        mask_1 = ~mask_0
        results[mask_1] = cov[mask_1] / (std_i[mask_1] * std_j[mask_1])
    elif prop in ['contrast', 'dissimilarity', 'homogeneity']:
        weights = weights.reshape((num_level, num_level, 1, 1))
        results = np.sum(P * weights, axis=(0, 1))

    return results


# Функция для расчета GLCM и извлечения метрик для одного изображения
def calculate_glcm_metrics(image):

    distances = [1]
    angles = [0, np.pi/4, np.pi/2, 3*np.pi/4]
    glcm = graycomatrix(image, distances=distances, angles=angles, levels=256, symmetric=True, normed=True)

    contrast = graycoprops_mods(glcm, 'contrast').mean()
    homogeneity = graycoprops_mods(glcm, 'homogeneity').mean()
    energy = graycoprops_mods(glcm, 'energy').mean()
    correlation = graycoprops_mods(glcm, 'correlation').mean()
    entropy = graycoprops_mods(glcm, 'entropy').mean()
    return contrast, homogeneity, energy, correlation, entropy

# Путь к папке с изображениями
#folder_path = '..//..//dataset//synthetic_dataset10'
#folder_path = "D:/Data/Unet_multiclass/data/cutting data"
#folder_path = "D:/Data/Unet_multiclass/data/cutting data mito all"
#folder_path += "/original"
folder_path = "D:/Data/Unet_multiclass/data/testTest"


def work_fun(folder_path):

    # Инициализация списка для хранения метрик всех изображений
    all_contrast = []
    all_homogeneity = []
    all_energy = []
    all_correlation = []
    all_entropy = []

    # Чтение всех изображений из папки
    for filename in os.listdir(folder_path):
        if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
            image_path = os.path.join(folder_path, filename)
            image = io.imread(image_path)

            image = image if len(image.shape)==2 else color.rgb2gray(image[:,:,:3]).astype(np.uint8) if image.shape[2]>2 else image[:,:,0]

            # Вычисление метрик для текущего изображения
            contrast, homogeneity, energy, correlation, entropy = calculate_glcm_metrics(image)

            # Добавление метрик в списки
            all_contrast.append(contrast)
            all_homogeneity.append(homogeneity)
            all_energy.append(energy)
            all_correlation.append(correlation)
            all_entropy.append(entropy)

    # Преобразование списков в массивы NumPy для удобных расчетов
    all_contrast = np.array(all_contrast)
    all_homogeneity = np.array(all_homogeneity)
    all_energy = np.array(all_energy)
    all_correlation = np.array(all_correlation)
    all_entropy = np.array(all_entropy)

    # Расчет средних значений и стандартных отклонений
    mean_contrast = np.mean(all_contrast)
    std_contrast = np.std(all_contrast)

    mean_homogeneity = np.mean(all_homogeneity)
    std_homogeneity = np.std(all_homogeneity)

    mean_energy = np.mean(all_energy)
    std_energy = np.std(all_energy)

    mean_correlation = np.mean(all_correlation)
    std_correlation = np.std(all_correlation)

    mean_entropy = np.mean(all_entropy)
    std_entropy = np.std(all_entropy)

    # Вывод результатов
    print(f"Контраст: {mean_contrast} +|- {std_contrast}")
    print(f"Однородность: {mean_homogeneity} +|- {std_homogeneity}")
    print(f"Энергия: {mean_energy} +|- {std_energy}")
    print(f"Корреляция: {mean_correlation} +|- {std_correlation}")
    print(f"Энтропия: {mean_entropy} +|- {std_entropy}")


if __name__ == "__main__":
   for folder_path in folder_path_list:
        print(f"folder_path: {folder_path}")
        work_fun(folder_path)
        print()
