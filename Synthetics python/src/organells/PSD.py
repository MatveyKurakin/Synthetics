import numpy as np
import cv2

import math

if __name__ == "__main__":
    import sys
    sys.path.append('.')

from src.container.spline import *
from src.container.subclass import *

class PSD:
    def __init__(self):
        self.type = "PSD"
        
        self.color = (63, 63, 63)
        self.addColor = (90, 90, 90)
        
        input_color = np.random.randint(100, 131)
        self.addColor2 = (input_color, input_color, input_color)
        
        self.nowBrush = Brush(self.addColor)
        
        self.nowPen = Pen(self.color, 12)
        self.nowAddPen = Pen(self.addColor2, 2)
        
        self.centerPoint = [0, 0]
        
        self.Points = []
        self.PointsWithOffset = []

        self.lenPSD = 0;
        
        self.Create()
        
    def Create(self):
        
        min_r = 10
        max_r = 30
        
        # создание точки начала отрезка в 1 или 4 четвертях
        lenXPSD = np.random.randint(min_r, max_r)
        lenYPSD = np.random.randint(min_r, max_r)
        
        if np.random.randint(0,2) == 0:
            lenYPSD *= -1
            
        self.Points.append([int(lenXPSD), int(lenYPSD)])

        # вычисление нормали к вектору из (0, 0) до созданой точки
        eXnormal = 1.0
        eYnormal = -(lenXPSD/lenYPSD)
        lenNormal = math.sqrt(eXnormal * eXnormal + eYnormal * eYnormal)

        eXnormal /= lenNormal
        eYnormal /= lenNormal
        normal = (eXnormal, eYnormal)

    
        self.lenPSD = math.sqrt((4 * lenXPSD * lenXPSD) + (4 * lenYPSD * lenYPSD))

        # создание точки, для искривление отрезка PSD
        delta = 3;
        curveVal = np.random.randint(-delta, delta)
        curvedPoint = [int(round(normal[0] * curveVal)), int(round(normal[1] * curveVal))]
        self.Points.append(curvedPoint)


        # создание точки конца отрезка, симметрично относительно (0, 0)
        self.Points.append([int(-lenXPSD), int(-lenYPSD)])

        # смещение дополнительной полосы в выпуклую сторону (- значение) и в внутренюю сторону (+ значение)
        sizeOffset = -1
        
        Offset = [math.copysign(1, curveVal) * int(round(normal[0] * sizeOffset)), math.copysign(1, curveVal) * int(round(normal[1] * sizeOffset))]

        
        dirPSDX = lenXPSD/math.sqrt((lenXPSD * lenXPSD) + (lenYPSD * lenYPSD))
        dirPSDY = lenYPSD/math.sqrt((lenXPSD * lenXPSD) + (lenYPSD * lenYPSD))
        
        add_size = self.nowPen.sizePen//2+2

        p1_1 = [int(self.Points[0][0] + Offset[0] - dirPSDX * add_size), int(self.Points[0][1] + Offset[1] - dirPSDY * add_size)]
        c_1  = [int(self.Points[1][0] + Offset[0]), int(self.Points[1][1] + Offset[1])]
        p2_1 = [int(self.Points[2][0] + Offset[0] + dirPSDX * add_size), int(self.Points[2][1] + Offset[1] + dirPSDY * add_size)]

        self.Points.append(p1_1)
        self.Points.append(c_1)
        self.Points.append(p2_1)

        sizeOffset = -15
        Offset[0] = math.copysign(1, curveVal) * int(round(normal[0] * sizeOffset))
        Offset[1] = math.copysign(1, curveVal) * int(round(normal[1] * sizeOffset))

        self.Points.append(self.Points[0])
        c_2 = [int(self.Points[1][0] + Offset[0]), int(self.Points[1][1] + Offset[1])]
        
        self.Points.append(c_2)
        self.Points.append(self.Points[2])
        self.Points.append(self.Points[1])

        
        self.ChangePositionPoints()
        
    def ChangePositionPoints(self):
        self.PointsWithOffset = []

        for point in self.Points:
            self.PointsWithOffset.append([self.centerPoint[0]+point[0], self.centerPoint[1]+point[1]])


    def setDrawParam(self):
        self.nowPen.color = self.color
        self.nowAddPen.color = self.addColor2
 
        self.nowBrush.brush = self.addColor

    def setMaskParam(self):
        self.nowPen.color = (255,255,255)
        self.nowAddPen.color = (255,255,255)

        self.nowBrush.brush = (255,255,255)

    def NewPosition(self, x, y):
        self.centerPoint[0] = x
        self.centerPoint[1] = y

        self.ChangePositionPoints()

    def Draw(self, image, layer_drawing = True):
        # Основная рисующая фукция
        draw_image = image.copy()

        # затемнение фона позади PSD
        rangeList = self.PointsWithOffset[6:6+4]           

        #if layer_drawing == True:
        small_spline_line(draw_image, rangeList, self.nowAddPen.color, self.nowAddPen.sizePen)   
        self.nowBrush.FullBrush(draw_image, rangeList)
 
        
        #главная темная линия PSD
        #if layer_drawing == True:
        small_spline_line(draw_image, self.PointsWithOffset[3:3+3], self.nowPen.color, self.nowPen.sizePen)  
  
        # светлая полоска от границы на PSD 
        if np.random.random() < 0.5:
            small_spline_line(draw_image, self.PointsWithOffset[0:3], self.nowAddPen.color, self.nowAddPen.sizePen) 
        
        return draw_image
            
    def DrawUniqueArea(self, image, small_mode = False):
        # Функция создающая маску с немного большим отступом для алгорима случайного размещения новых органнел без пересечения 
        ret_image = image.copy()
        
        ret_image = ret_image.astype(int)
        
        draw_image = np.zeros(image.shape, np.uint8) 
        
        draw_image = self.DrawMask(draw_image)
        
        if small_mode == False:
            kernel = np.array([[0, 1, 0],
                               [1, 1, 1],
                               [0, 1, 0]], dtype=np.uint8)
            draw_image = cv2.dilate(draw_image,kernel,iterations = 4)
        else:
            kernel = np.array([[0, 1, 0],
                               [1, 1, 1],
                               [0, 1, 0]], dtype=np.uint8)
            draw_image = cv2.dilate(draw_image,kernel,iterations = 2)
            
            normal = [self.centerPoint[0] - self.PointsWithOffset[7][0], self.centerPoint[1] - self.PointsWithOffset[7][1]]
            
            sizeNormal = math.sqrt(normal[0]**2 + normal[1]**2)
            
            normal = [normal[0]/sizeNormal, normal[1]/sizeNormal]
            
            sizeInputOffset = -15
            
            poligon = [self.PointsWithOffset[0], [self.PointsWithOffset[1][0] + sizeInputOffset * normal[0], self.PointsWithOffset[1][1] + sizeInputOffset * normal[1]], self.PointsWithOffset[2]]
             
            int_poligon = []
            for x,y in poligon:
                int_poligon.append([np.array((int(round(x)),int(round(y))), dtype = np.int32)])

            contour = np.array(int_poligon, dtype = np.int32)

            cv2.drawContours(draw_image,[contour], 0,(255,255,255), -1)
            
            #cv2.imshow("sdad", draw_image)
            #cv2.waitKey()
            
        ret_image = ret_image + draw_image
        ret_image[ret_image[:,:,:] > 255] = 255
        ret_image = ret_image.astype(np.uint8)
        
        return ret_image
        
    def DrawMask(self, image):
        #Смена цветов для рисования маски
        self.setMaskParam()
        mask = self.Draw(image, layer_drawing = False)
        self.setDrawParam()
        
        return mask 
     
def testPSD():
    q = None

    print("Press button 'Q' or 'q' to exit")
    while q != ord('q') and q != ord("Q"):
        
        color = np.random.randint(182, 200)
        
        img = np.full((512,512,3), (color,color,color), np.uint8)
        
        for i in range(0, 512, 32):
            img[i:i+15,:,:] += 30
        
        psd = PSD()
        
        psd.NewPosition(256,256)
        
        print("centerPoint", psd.centerPoint)
        print("Points", psd.Points)
        print("PointsWithOffset", psd.PointsWithOffset)
        
        img1 = psd.Draw(img)
        
        mask = np.zeros((512,512,3), np.uint8)
        
        tecnicalMask = np.zeros((512,512,3), np.uint8)
        
        mask = psd.DrawMask(mask)
        img2 = psd.Draw(img)
        tecnicalMask = psd.DrawUniqueArea(tecnicalMask)
        
        cv2.imshow("img", img1)
        cv2.imshow("mask", mask)
        cv2.imshow("img2", img2)
        cv2.imshow("tecnicalMask", tecnicalMask)
        
        q = cv2.waitKey()

if __name__ == "__main__":
    testPSD()

