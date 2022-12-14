import random


PARAM = {
    
    'main_color_mean': 185.0,                   'main_color_std': 15, # Основной цвет фона
    'main_radius_gausse_blur': 5,               'main_sigma_gausse_blur': 2,  # радиус и размытие конечного изображения
    'main_min_gausse_noise_value': 6,          'main_max_gausse_noise_value': 15, # пределы для разброса нормального шума

    'axon_shell_color_mean': 65.0,              'axon_shell_color_std': 10.0, # Цвет оболочек аксона
    'axon_back_color_diff_mean': 50.0,          'axon_back_color_diff_std': 10.0, # Затемнение стандартной текстуры 

    'membrane_thickness_mean': 3.0,             'membrane_thickness_std': 1.0, # Толщина линий
    'membrane_color_mean': 95.0,                'membrane_color_std': 15.0, # Цвет линий
    
    'mitohondrion_shell_color_mean': 85.0,      'mitohondrion_shell_color_std': 5.0, # Цвет оболочки митохондрии
    'mitohondrion_back_color_mean': 120.0,      'mitohondrion_back_color_std': 20.0, # Цвет заполнения митохондрии
    'mitohondrion_cristae_shell_color_mean': 80.0, 'mitohondrion_cristae_shell_color_std': 0.0, # Цвет оболочки крист
    'mitohondrion_cristae_color_mean': 120.0,   'mitohondrion_cristae_color_std': 5.0, # Цвет внутри крист

    'psd_back_color_mean': 60.0,                'psd_back_color_std': 10.0, # Цвет основной части PSD
    'psd_addcolor_mean': 85.0,                  'psd_addcolor_std': 10.0, # Цвет метелки PSD
    'psd_centerline_color_mean': 115.0,            'psd_centerline_color_std': 15.0, # Цвет нитки поверс PSD 

    'vesicles_shell_color_mean': 80.0,          'vesicles_shell_color_std': 10.0, # Цвет оболочки везикул
    'vesicles_back_color_mean': 125.0,          'vesicles_back_color_std': 10.0, # Цвет внутри везикул
    
    'pearson_noise': 15, # интенсивность шума Пирсона
}


def uniform_float(mean, std):
    return random.uniform(mean - std, mean + std)


def uniform_int(mean, std):
    return int(random.uniform(mean - std, mean + std) + 0.5)