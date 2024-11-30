import os
import numpy as np
import skimage
from skimage.feature import graycomatrix, graycoprops
from skimage import io, color
import matplotlib.pyplot as plt

# Функция для расчета GLCM и извлечения метрик для одного изображения
def calculate_glcm_metrics(image):
    
    distances = [1]
    angles = [0, np.pi/4, np.pi/2, 3*np.pi/4]
    glcm = graycomatrix(image, distances=distances, angles=angles, levels=256, symmetric=True, normed=True)
    
    contrast = graycoprops(glcm, 'contrast').mean()
    homogeneity = graycoprops(glcm, 'homogeneity').mean()
    energy = graycoprops(glcm, 'energy').mean()
    correlation = graycoprops(glcm, 'correlation').mean()
    
    return contrast, homogeneity, energy, correlation

# Путь к папке с изображениями
folder_path = '..//..//dataset//test_gen//original'

# Инициализация списка для хранения метрик всех изображений
all_contrast = []
all_homogeneity = []
all_energy = []
all_correlation = []

# Чтение всех изображений из папки
for filename in os.listdir(folder_path):
    if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
        image_path = os.path.join(folder_path, filename)
        image = io.imread(image_path)

        # Вычисление метрик для текущего изображения
        contrast, homogeneity, energy, correlation = calculate_glcm_metrics(image)
        
        # Добавление метрик в списки
        all_contrast.append(contrast)
        all_homogeneity.append(homogeneity)
        all_energy.append(energy)
        all_correlation.append(correlation)

# Преобразование списков в массивы NumPy для удобных расчетов
all_contrast = np.array(all_contrast)
all_homogeneity = np.array(all_homogeneity)
all_energy = np.array(all_energy)
all_correlation = np.array(all_correlation)

# Расчет средних значений и стандартных отклонений
mean_contrast = np.mean(all_contrast)
std_contrast = np.std(all_contrast)

mean_homogeneity = np.mean(all_homogeneity)
std_homogeneity = np.std(all_homogeneity)

mean_energy = np.mean(all_energy)
std_energy = np.std(all_energy)

mean_correlation = np.mean(all_correlation)
std_correlation = np.std(all_correlation)

# Вывод результатов
print(f"Контраст: {mean_contrast} +|- {std_contrast}")
print(f"Однородность: {mean_homogeneity} +|- {std_homogeneity}")
print(f"Энергия: {mean_energy} +|- {std_energy}")
print(f"Корреляция: {mean_correlation} +|- {std_correlation}")
