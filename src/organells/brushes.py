# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 21:48:45 2023

@author: user
"""
import numpy as np
import cv2
import math

from src.container.spline import *
from src.container.subclass import *
from settings import PARAM, uniform_int

def points_generator(centre_x, centre_y, points_num):
    _points = list()
    middle = list()
    k = 1

    middle.append((centre_x, k * centre_y))
    for i in range(1, points_num + 1):
        r_x = np.random.randint(4, 10)

        x_coord_middle = middle[i - 1][0] + r_x
        y_coord_middle = k * middle[i - 1][1]
        new_point_middle = (x_coord_middle, y_coord_middle)
        middle.append(new_point_middle)
    for i in range(points_num + 1):
        sign = np.random.randint(0, 1)
        if not sign:
            sign = -1
            #  ыеличина волны
        delta = sign * np.random.randint(2, 5)
        _points.append( (middle[i][0] - delta, middle[i][1] - delta) )
    return _points


def fillInnerTextureSpline(inn_tex):
    cristae_color = uniform_int(
            PARAM['mitohondrion_cristae_color_mean'],
            PARAM['mitohondrion_cristae_color_std'])
    cristae_color = (cristae_color,cristae_color,cristae_color)
        
    forecolor = uniform_int(
            PARAM['mitohondrion_cristae_shell_color_mean'],
            PARAM['mitohondrion_cristae_shell_color_std'])        
    forecolor = (forecolor,forecolor,forecolor)
        
    points_x = np.random.randint(0, inn_tex.shape[0], int(inn_tex.shape[1]/2))
    points_y = np.random.randint(0, inn_tex.shape[1], int(inn_tex.shape[1]/2))
        
      #  print('len', len(points_y))
    for i in zip(points_x, points_y):
          #  print('centers', points_x, points_y)
          crista_len = np.random.randint(2, 5)
          points = points_generator(i[0], i[1], crista_len)
          crista_w = np.random.randint(4, 6)
          small_spline_line(inn_tex, points, nowPen.color, crista_w)
          small_spline_line(inn_tex, points, cristae_color, crista_w - 3)
            # spline_line(inn_tex, points, self.nowPen.color, 5, False)
    import matplotlib.pyplot as plt
    plt.imshow(inn_tex)
    plt.show()
    return inn_tex

        
def fillInnerTexture(inn_tex, mit_len):
    cristae_color = uniform_int(
            PARAM['mitohondrion_cristae_color_mean'],
            PARAM['mitohondrion_cristae_color_std'])
    cristae_color = (cristae_color,cristae_color,cristae_color)
        
    forecolor = uniform_int(
            PARAM['mitohondrion_cristae_shell_color_mean'],
            PARAM['mitohondrion_cristae_shell_color_std'])        
    forecolor = (forecolor,forecolor,forecolor)
    
    now_x = 10
    while now_x < inn_tex.shape[1] - 10:
        now_y = 10
        while now_y < inn_tex.shape[1] - 10:
            len_line = np.random.randint(0, mit_len // 2)

            start_pos = [now_x + np.random.randint(-2,3), now_y]
            enf_pos = [now_x + np.random.randint(-2,3), now_y+len_line]
                
            inn_tex = cv2.line(inn_tex, start_pos, enf_pos, forecolor, 5)
                
            if len_line == 0: # генерация черной точки
                if np.random.random() < 0.5: 
                    inn_tex = cv2.line(inn_tex, start_pos, enf_pos, (1,1,1), 5)
                    inn_tex = cv2.line(inn_tex, start_pos, enf_pos, (1,1,1), 2)
                else:
                    inn_tex = cv2.line(inn_tex, start_pos, enf_pos, (cristae_color), 2)
            else:
                inn_tex = cv2.line(inn_tex, start_pos, enf_pos, (cristae_color), 2)

                #step y
            step_y = np.random.randint(7,20)
            now_y = now_y + len_line + step_y
                
            #step x
        step_x = np.random.randint(12,18)
        now_x += step_x
            
        return inn_tex

        
def CreateTexture(image, mit_len, angle):

    addColor = uniform_int(
            PARAM['mitohondrion_back_color_mean'],
            PARAM['mitohondrion_back_color_std'])
        
    addColor = (addColor, addColor, addColor) # основной цвет текстуры.
    
    texture = np.full((*image.shape[0:2],3), addColor, np.uint8)
        #self.texture[:,:] = (0,0,255)

    cristae_color = uniform_int(
            PARAM['mitohondrion_cristae_color_mean'],
            PARAM['mitohondrion_cristae_color_std'])
    cristae_color = (cristae_color,cristae_color,cristae_color)

    forecolor = uniform_int(
            PARAM['mitohondrion_cristae_shell_color_mean'],
            PARAM['mitohondrion_cristae_shell_color_std'])
    forecolor = (forecolor,forecolor,forecolor)

        
# Kolya
    now_x = 10
    while now_x < image.shape[1] - 10:
        now_y = 10
        while now_y < image.shape[1] - 10:
            type_line = np.random.random()
            if type_line < 0.1:
                len_line = 0
            elif type_line < 0.55:
                len_line = np.random.randint(2, 5)
            else:
                len_line = np.random.randint(5, mit_len // 2)

            start_pos = [now_x + np.random.randint(-3,4), now_y]
            enf_pos = [now_x + np.random.randint(-3,4), now_y+len_line]

            texture = cv2.line(texture, start_pos, enf_pos, forecolor, 5)

            if len_line == 0: # генерация черной точки
                if np.random.random() < 0.5:
                    color_black_point = (20,20,20)
                    texture = cv2.line(texture, start_pos, enf_pos, color_black_point, 5)
                    texture = cv2.line(texture, start_pos, enf_pos, color_black_point, 2)
                else:
                    texture = cv2.line(texture, start_pos, enf_pos, (cristae_color), 2)
            else:
                texture = cv2.line(texture, start_pos, enf_pos, (cristae_color), 2)

                #step y
            step_y = np.random.randint(7,20)
            now_y = now_y + len_line + step_y

            #step x
        step_x = np.random.randint(12,18)
        now_x += step_x
    texture = fillInnerTexture(texture, mit_len)

    (h, w) = image.shape[:2]
    center = (int(w / 2), int(h / 2))
    rotation_matrix = cv2.getRotationMatrix2D(center, 90 - angle, 1.5)
    texture = cv2.warpAffine(texture, rotation_matrix, (w, h))

    #print(self.texture.shape)
    texture[texture[:,:,0] == 0] = addColor

    #cv2.imshow("texture", self.texture)
    #cv2.waitKey()
    nowBrush = Brush(brush = texture, typeFull = "texture")
    return texture, nowBrush