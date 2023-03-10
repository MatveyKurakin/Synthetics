import numpy as np
import cv2

import math

if __name__ == "__main__":
    import sys
    sys.path.append('.')

from src.container.spline import *
from src.container.subclass import *
from src.organells.brushes import *
from settings import PARAM, uniform_int

class Mitohondrion:
    def __init__(self):
        self.type = "Mitohondrion"

        # COLORS
        color = uniform_int(
            PARAM['mitohondrion_shell_color_mean'],
            PARAM['mitohondrion_shell_color_std'])
        self.color = (color, color, color)
        self.nowPen = Pen(self.color, np.random.randint(PARAM['mitohondrion_border_w_min'], PARAM['mitohondrion_border_w_max']))    
        self.nowBrush = None
        self.texture = None

        # GEOMETRY
        self.angle = 0
        self.main_len = 0
        self.numberPoints = 0
        self.centerPoint = [0, 0]
        self.Points = []
        self.PointsWithOffset = []

        self.direction = [0,0]         # вектор смещения границы, для имитации косого среза
        self.dopSizeLine = 0

        self.addPoints = []            # точки с смещением для имитации косого среза
        self.addPointsWithOffset = []

        self.Create()

    def __copy__(self):
        new_mito = Mitohondrion()

        new_mito.color = self.color
        new_mito.nowPen  = self.nowPen.copy()

        if self.texture is not None:
            new_mito.nowBrush  = self.nowBrush.copy()
            new_mito.texture  = self.texture.copy()

        new_mito.angle = self.angle
        new_mito.main_len = self.main_len
        new_mito.numberPoints = self.numberPoints
        new_mito.centerPoint = self.centerPoint.copy()
        new_mito.Points = self.Points.copy()

        new_mito.direction  = self.direction.copy()
        new_mito.addPoints  = self.addPoints.copy()

        new_mito.dopSizeLine = self.dopSizeLine

        new_mito.setDrawParam()
        new_mito.setRandomAngle(0,0)

        return new_mito

    def copy(self):
        return self.__copy__()

    def Create(self):

        main_len = np.random.randint(PARAM["mit_len_min"], PARAM["mit_len_max"])
        self.main_len = main_len

        min_r = np.random.randint(5, 27)
        max_r = np.random.randint(27, 80)

        # минимум 6, максимум 10
        self.numberPoints = 2 + 2 * np.random.randint(2, 5)

        tPoints = []
        # Добавление первой главной точки
        startMPoint = [-main_len//2, 0]
        tPoints.append(startMPoint.copy())

        half_len = (self.numberPoints - 2)//2

        
        # заполнение иксов - поделили отрезок на half_len + 2 отрезков
        xes = np.linspace(-main_len//2, main_len//2, num = half_len + 2)[1:-1]
        # нам нужны эти точки дважды, для верхней и для нижней половин митохондрии
        xes = np.concatenate((xes, xes[::-1]))


        # во избежание создания крайне извилистой или вытянутой митохондрии 
        # вводится ограничение на изменение крутизны её извилистости
        step = main_len / (half_len+1)
        
        # игреки для верхней половины митохондрии
        start_y_value = np.random.randint(min(max(step, min_r),max_r)//2 , min(max_r, main_len//2)+1)
        yes = np.random.randint(-max_r//2, max_r//2 + 1, half_len)
        cumulative_sum = np.clip(np.cumsum(yes, axis = 0) + start_y_value, min_r, max_r)
        yes = np.array([start_y_value]) + cumulative_sum
        
        # игреки для нижней половины митохондрии
        start_y_value = np.random.randint(min(max(step, min_r),max_r)//2 , min(max_r, main_len//2)+1)
        yes2 = np.random.randint(-max_r//2, max_r//2 + 1, half_len)
        cumulative_sum =  np.clip(np.cumsum(yes2, axis = 0) + start_y_value, min_r, max_r)
        yes2 = np.array([start_y_value]) + cumulative_sum
        
        yes = np.concatenate((yes , (-1) * yes2[::-1]))


        list1 = xes.tolist()
        list2 = yes.tolist()
        self.Points = [[x, y] for x, y in zip(list1, list2)]

        # поворот митохондрии
        self.angle = np.random.randint(0, 90)

        #добавление доп. точек
        if np.random.random() < 0.5: 
            self.dopSizeLine = np.random.randint(3, 5)

            direction = np.random.randint(-4, 5, 2)

            len_dir = math.sqrt(direction[0]**2 + direction[1]**2)

            if len_dir != 0:
                self.direction = [direction[0]/len_dir, direction[1]/len_dir]


        self.setRandomAngle(0, 0)

    def ChangePositionPoints(self):
        self.PointsWithOffset = []
        #self.addPointsWithOffset = []

        for point in self.Points:
            self.PointsWithOffset.append([self.centerPoint[0]+point[0], self.centerPoint[1]+point[1]])

        #for point2 in self.addPoints:
        #    self.addPointsWithOffset.append([self.centerPoint[0]+point2[0], self.centerPoint[1]+point2[1]])

    def NewPosition(self, x, y):
        self.centerPoint[0] = x
        self.centerPoint[1] = y

        self.ChangePositionPoints()

    def setRandomAngle(self, min_angle = 0, max_angle = 90, is_singned_change = True):

        if np.random.random() < 0.5 and is_singned_change:
            sign = -1
        else:
            sign = 1

        new_angle = (self.angle + np.random.randint(min_angle, max_angle+1) * sign) %360
        change_angle = (new_angle - self.angle) * (math.pi/180)
        self.angle = new_angle

        tPoints = []
        for point in self.Points:
            x = int(round(point[0] * math.cos(change_angle) - point[1] * math.sin(change_angle)))
            y = int(round(point[0] * math.sin(change_angle) + point[1] * math.cos(change_angle)))
            tPoints.append([x,y])

        #tAddPoints = []
        #for point2 in self.addPoints:
        #    x = int(round(point2[0] * math.cos(change_angle) - point2[1] * math.sin(change_angle)))
        #    y = int(round(point2[0] * math.sin(change_angle) + point2[1] * math.cos(change_angle)))
        #    tAddPoints.append([x,y])

        self.Points = tPoints
        #self.addPoints = tAddPoints
        self.ChangePositionPoints()
   

    def Draw(self, image, layer_drawing = True):
        # Основная рисующая фукция
        if layer_drawing:
            self.texture, self.nowBrush = CreateTexture(image, self.main_len, self.angle)

        draw_image = image.copy()


        self.nowBrush.FullBrush(draw_image, self.PointsWithOffset)

        if self.dopSizeLine != 0 and  self.direction[0] != 0 and self.direction[1] != 0:
            for step in range(-self.dopSizeLine, self.dopSizeLine+1, self.nowPen.sizePen-1):

                temp_PointsWithOffset_for_boarder = []

                for point in self.PointsWithOffset:
                    temp_PointsWithOffset_for_boarder.append([point[0]+int(round(step*self.direction[0])), point[1] + int(round(step*self.direction[1]))])

                spline_line(draw_image, temp_PointsWithOffset_for_boarder, self.nowPen.color, self.nowPen.sizePen)


        # if len(self.addPointsWithOffset) != 0:
        #    fill_texture_2_poligons(draw_image, self.addPointsWithOffset[0:3], self.addPointsWithOffset[3:6], self.nowPen.color, self.nowPen.sizePen+1)
        #    fill_texture_2_poligons(draw_image, self.addPointsWithOffset[6:9], self.addPointsWithOffset[9:12], self.nowPen.color, self.nowPen.sizePen+1)
        else:
            spline_line(draw_image, self.PointsWithOffset, self.nowPen.color, self.nowPen.sizePen)

        return draw_image

    def DrawLayer(self, image):
        return self.Draw(image)

    def setDrawParam(self):
        self.nowPen.color = self.color
        self.nowBrush = Brush(brush = self.texture, typeFull = "texture")

    def setMaskParam(self):
        self.nowPen.color = (255,255,255)
        self.nowBrush = Brush((255,255,255))

    def setMaskBoarderParam(self):
        self.nowPen.color = (255,255,255)
        self.nowBrush =  Brush((0,0,0))

    def DrawMask(self, image):
        #Смена цветов для рисования маски
        self.setMaskParam()
        mask = self.Draw(image, layer_drawing = False)
        self.setDrawParam()

        return mask

    def DrawMaskBoarder(self, image):
        #Смена цветов для рисования маски
        self.setMaskBoarderParam()
        mask = self.Draw(image, layer_drawing = False)
        self.setDrawParam()

        return mask

    def DrawUniqueArea(self, image, small_mode = False):
        # Функция создающая маску с немного большим отступом для алгорима случайного размещения новых органнел без пересечения
        ret_image = image.copy()
        ret_image = ret_image.astype(int)
        # import matplotlib.pyplot as plt
        # plt.imshow(ret_image)
        # plt.show()

        draw_image = np.zeros(image.shape, np.uint8)
        draw_image = self.DrawMask(draw_image)
        # plt.imshow(draw_image)
        # plt.show()

        if small_mode == False:
            kernel = np.array([[0, 1, 0],
                               [1, 1, 1],
                               [0, 1, 0]], dtype=np.uint8)

            draw_image = cv2.dilate(draw_image,kernel,iterations = 5)

        ret_image = ret_image + draw_image
        ret_image[ret_image[:,:,:] > 255] = 255
        ret_image = ret_image.astype(np.uint8)

        return ret_image


def testMitohondrion():
    q = None

    print("Press button 'Q' or 'q' to exit")
    while q != ord('q') and q != ord("Q"):

        color = np.random.randint(182, 200)

        img = np.full((512,512,3), (color,color,color), np.uint8)

        for i in range(0, 512, 32):
            img[i:i+15,:,:] += 30

        mitohondrion = Mitohondrion()

        mitohondrion.NewPosition(256,256)

        print("centerPoint", mitohondrion.centerPoint)
        print("Points", mitohondrion.Points)
        print("PointsWithOffset", mitohondrion.PointsWithOffset)

        print("addPoints", mitohondrion.addPoints)
        print("addPointsWithOffset", mitohondrion.addPointsWithOffset)

        img1 = mitohondrion.Draw(img)

        mask = np.zeros((512,512,3), np.uint8)

        tecnicalMask = np.zeros((512,512,3), np.uint8)

        maskMito = mitohondrion.DrawMask(mask.copy())
        img2 = mitohondrion.Draw(img)
        tecnicalMask = mitohondrion.DrawUniqueArea(tecnicalMask)

        for point in mitohondrion.PointsWithOffset:
            cv2.circle(img1, point, 3, (0, 0, 255), 2)

        for point in mitohondrion.addPointsWithOffset:
            cv2.circle(img2, point, 3, (0, 255, 0), 2)

        Boarder = mitohondrion.DrawMaskBoarder(mask)

        cv2.imshow("img", img1)
        cv2.imshow("mask", maskMito)
        cv2.imshow("img2", img2)
        cv2.imshow("tecnicalMask", tecnicalMask)
        cv2.imshow("Boarder", Boarder)

        q = cv2.waitKey()

if __name__ == "__main__":
    testMitohondrion()
