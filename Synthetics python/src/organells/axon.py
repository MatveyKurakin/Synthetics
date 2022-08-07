import numpy as np
import cv2

import math

if __name__ == "__main__":
    import sys
    sys.path.append('.')

from src.container.spline import *
from src.container.subclass import *


class Axon:
    def __init__(self):
        self.type = "Axon"
    
        self.nowInnerBrush = None
        self.nowBubbleBrush = None
        self.innerTexture = None
        self.bubbleTexture = None
        
    
        self.color = (65, 65, 65)
        self.sizePen = np.random.randint(14, 18)
        self.sizeAddPen = np.random.randint(self.sizePen, 20)
        
        self.centerPoint = [0,0]
        self.input_radius = None
        self.angle = 0
        self.sublistNumber = 0
                
        self.pointNumber = 0
        self.Points = []
        self.PointsWithOffset = []

        self.nowPen = Pen(self.color, self.sizePen)
        self.nowAddPen = Pen(self.color, self.sizeAddPen)
        self.Create()
        
    def Create(self, min_r=0, max_r=0):
        
        self.Points = []

        self.pointNumber = np.random.randint(7, 14)
 
        if (min_r == 0):
            min_r = np.random.randint(30, 70)
        
        if (max_r == 0):
            max_r = min_r + np.random.randint(4, min_r);                                  # лучше поменять параметры
 
        max_increase_len = max_r - min_r
        
        # 2 типа генерации, если маленький просто оболочка, если большой, то с внутренней частью

        step_angle = 2.0 * math.pi / self.pointNumber

        for i in range(self.pointNumber):
            now_angle = step_angle * i
            r = min_r + np.random.randint(1, max_increase_len)
            
            now_point = [int(round(r * math.sin(now_angle))), int(round(r * math.cos(now_angle)))]
            self.Points.append(now_point)

        if min_r > 40:
            self.input_radius = np.random.randint(min_r/2, min_r-2, 2)
            self.angle = np.random.randint(0, 360)

        self.ChangePositionPoints()
        self.sublistNumber = np.random.randint(3, len(self.PointsWithOffset) - 3)

    def CreateNewTexture(self, image):
        self.innerTexture = image
        
        self.bubbleTexture = image.copy()
        t = 50
        
        self.bubbleTexture[self.bubbleTexture[:,:,0] > t] -= t
        
        # создание пятен        
        now_x = 10
        
        color1 = 168
        color2 = 100
        
        while now_x < image.shape[1] - 10:
            now_y = 10
            while now_y < image.shape[1] - 10:

                radius = np.random.randint(11,14,2)

                Brush((color1,color1,color1)).FullBrushEllipse(self.bubbleTexture, (now_x, now_y), radius)

                cv2.ellipse(img = self.bubbleTexture,
                           center = (now_x, now_y),
                           axes = radius,
                           color = (color2,color2,color2),
                           thickness = 4,
                           angle = 0,
                           startAngle = 0,
                           endAngle = 360)
                #step y
                step_y = np.random.randint(160, 201)
                now_y = now_y + step_y
                
            #step x
            step_x = np.random.randint(160,201)
            now_x += step_x
        
        self.nowInnerBrush = Brush(self.innerTexture, typeFull = "texture")
        self.nowBubbleBrush = Brush(self.bubbleTexture, typeFull = "texture")

    def ChangePositionPoints(self):
        self.PointsWithOffset = []

        for point in self.Points:
            self.PointsWithOffset.append([self.centerPoint[0]+point[0], self.centerPoint[1]+point[1]])

    def NewPosition(self, x, y):
        self.centerPoint[0] = x
        self.centerPoint[1] = y

        self.ChangePositionPoints()

    def Draw(self, image, layer_drawing = True):
        # Основная рисующая фукция
        draw_image = image.copy()

        if layer_drawing == True:
            self.CreateNewTexture(image)

        spline_line(draw_image, self.PointsWithOffset, self.nowPen.color, self.nowPen.sizePen)

        # для 2 типа генерации
        if (self.input_radius is not None):
            # дополнительное утолщение части границы
            sublist = self.PointsWithOffset[1: self.sublistNumber+1+1]
            
            small_spline_line(draw_image, sublist, self.nowAddPen.color, self.nowAddPen.sizePen)  

            #заполнение внутренности
            self.nowBubbleBrush.FullBrush(draw_image, self.PointsWithOffset)

            #очистить центральную внутренность 
            self.nowInnerBrush.FullBrushEllipse(draw_image, self.centerPoint, self.input_radius, self.angle)

            #внутренняя оболочка
            cv2.ellipse(img = draw_image,
                       center = (self.centerPoint[0], self.centerPoint[1]),
                       axes = self.input_radius,
                       color = self.nowPen.color,
                       thickness = 3,
                       angle = self.angle,
                       startAngle = 0,
                       endAngle = 360)

        else:
             #очистить центральную внутренность (и сделать границу тоньше в 2 раза)
             self.nowInnerBrush.FullBrush(draw_image, self.PointsWithOffset)

        return draw_image

    def DrawMask(self, image):
        #Смена цветов для рисования маски
        self.setMaskParam()
        mask = self.Draw(image, layer_drawing = False)
        self.setDrawParam()
        
        return mask

    def DrawUniqueArea(self, image, small_mode = False):
        # Функция создающая маску с немного большим отступом для алгорима случайного размещения новых органнел без пересечения 
        ret_image = image.copy()
        ret_image = ret_image.astype(int)
        
        draw_image = np.zeros(image.shape, np.uint8) 
        
        Brush((255,255,255)).FullBrush(draw_image, self.PointsWithOffset)
        spline_line(draw_image, self.PointsWithOffset, (255,255,255), self.nowPen.sizePen)
                    
        sublist = self.PointsWithOffset[1: self.sublistNumber+1+1]    
        spline_line(draw_image, sublist, (255,255,255), self.nowAddPen.sizePen, is_closed = False)  

        if small_mode == False:
            kernel = np.ones((5, 5), 'uint8')
            draw_image = cv2.dilate(draw_image,kernel,iterations = 2)
            
        ret_image = ret_image + draw_image
        ret_image[ret_image[:,:,:] > 255] = 255
        ret_image = ret_image.astype(np.uint8)
        
        return ret_image
        

    def setMaskParam(self):
        self.nowInnerBrush = Brush(brush = (0,0,0), typeFull = "full")
        self.nowBubbleBrush = Brush(brush = (255,255,255), typeFull = "full")

        self.nowPen.color = (255,255,255)
        self.nowAddPen.color = (255,255,255)

    def setDrawParam(self):
        self.nowInnerBrush = Brush(brush = self.innerTexture, typeFull = "texture")
        self.nowBubbleBrush = Brush(brush = self.bubbleTexture, typeFull = "texture")

        self.nowPen.color = self.color
        self.nowAddPen.color = self.color       


def testAxon():
        
    q = None


    print("Press button 'Q' or 'q' to exit")
    while q != ord('q') and q != ord("Q"):
        
        color = np.random.randint(182, 200)
        
        img = np.full((512,512,3), (color,color,color), np.uint8)
        
        for i in range(0, 512, 32):
            img[i:i+15,:,:] += 30
        
        axon = Axon()
        
        axon.NewPosition(256,256)
        
        print("centerPoint", axon.centerPoint)
        print("Points", axon.Points)
        print("PointsWithOffset", axon.PointsWithOffset)
        print("sublistNumber", axon.sublistNumber)
        
        img1 = axon.Draw(img)
        
        mask = np.zeros((512,512,3), np.uint8)
        
        tecnicalMask = np.zeros((512,512,3), np.uint8)
        
        mask = axon.DrawMask(mask)
        img2 = axon.Draw(img)
        tecnicalMask = axon.DrawUniqueArea(tecnicalMask)
        
        cv2.imshow("img", img1)
        cv2.imshow("mask", mask)
        cv2.imshow("img2", img2)
        cv2.imshow("tecnicalMask", tecnicalMask)
        
        q = cv2.waitKey()

if __name__ == "__main__":
    testAxon()


