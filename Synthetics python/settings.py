import random


PARAM = {

    'main_color_mean': 172.0,                   'main_color_std': 23, # Основной цвет фона

    'main_radius_gausse_blur': 4,               'main_sigma_gausse_blur': 1.5,  # радиус и размытие конечного изображения
    'main_min_gausse_noise_value': 6,          'main_max_gausse_noise_value': 15, # пределы для разброса нормального шума

    'axon_shell_color_mean': 57.0,              'axon_shell_color_std': 7.5, # Цвет оболочек аксона
    'axon_back_color_diff_mean': 50.0,          'axon_back_color_diff_std': 10.0, # Затемнение стандартной текстуры

    'membrane_thickness_mean': 3.0,             'membrane_thickness_std': 1.0, # Толщина линий
    'membrane_color_mean': 87.0,                'membrane_color_std': 10.0, # Цвет линий

    'mitohondrion_shell_color_mean': 88.0,      'mitohondrion_shell_color_std': 8, # Цвет оболочки митохондрии
    'mitohondrion_back_color_mean': 113.0,      'mitohondrion_back_color_std': 11.0, # Цвет заполнения митохондрии
    'mitohondrion_cristae_shell_color_mean': 80.0, 'mitohondrion_cristae_shell_color_std': 0.0, # Цвет оболочки крист
    'mitohondrion_cristae_color_mean': 125.0,   'mitohondrion_cristae_color_std': 40.0, # Цвет внутри крист

    'psd_back_color_mean': 60.0,                'psd_back_color_std': 7.5, # Цвет основной части PSD
    'psd_addcolor_mean': 65.0,                  'psd_addcolor_std': 10.0, # Цвет метелки PSD
    'psd_centerline_color_mean': 100.0,         'psd_centerline_color_std': 10.0, # Цвет нитки поверх PSD

    'vesicles_shell_color_mean': 87,          'vesicles_shell_color_std': 13.0, # Цвет оболочки везикул
    'vesicles_back_color_mean': 132.0,          'vesicles_back_color_std': 10.0, # Цвет внутри везикул

    'pearson_noise': 15, # интенсивность шума Пирсона
}


def uniform_float(mean, std):
    return random.uniform(mean - std, mean + std)


def uniform_int(mean, std):
    return int(random.uniform(mean - std, mean + std) + 0.5)
    
#def normal_random_float(mean, std):
#    return np.random.normal(mean, std)

#def normal_random_int(mean, std):
#    return int(round(np.random.normal(mean, std))