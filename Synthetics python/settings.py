import random


PARAM = {
    'axon_shell_color_mean': 65.0,              'axon_shell_color_std': 5.0,

    'membrane_thickness_mean': 3.0,             'membrane_thickness_std': 1.0,
    'membrane_color_mean': 80.0,                'membrane_color_std': 5.0,
    
    'mitohondrion_shell_color_mean': 85.0,      'mitohondrion_shell_color_std': 5.0,
    'mitohondrion_back_color_mean': 120.0,      'mitohondrion_back_color_std': 20.0,
    'mitohondrion_cristae_shell_color_mean': 80.0, 'mitohondrion_cristae_shell_color_std': 0.0,
    'mitohondrion_cristae_color_mean': 120.0,   'mitohondrion_cristae_color_std': 5.0,

    'psd_back_color_mean': 63.0,                'psd_back_color_std': 0.0,
    'psd_addcolor_mean': 90.0,                  'psd_addcolor_std': 5.0,
    'psd_topline_color_mean': 115.0,            'psd_topline_color_std': 15.0,

    'vesicles_shell_color_mean': 65.0,          'vesicles_shell_color_std': 5.0,
    'vesicles_back_color_mean': 130.0,          'vesicles_back_color_std': 5.0,
}


def uniform_float(mean, std):
    return random.uniform(mean - std, mean + std)


def uniform_int(mean, std):
    return int(random.uniform(mean - std, mean + std) + 0.5)