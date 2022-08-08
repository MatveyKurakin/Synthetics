import numpy as np
import cv2

import math

if __name__ == "__main__":
    import sys
    sys.path.append('.')

from src.container.spline import *
from src.container.subclass import *
from settings import PARAM, uniform_int

class Vesicles:
    def __init__(self):
        self.type = "Vesicles"
        
        self.sizeVesiculeMin = 5
        self.sizeVesiculeMax = 7
         
        self.numberPoints = 0
        self.listSizeVesiculs = []

        color = uniform_int(
            PARAM['vesicles_shell_color_mean'],
            PARAM['vesicles_shell_color_std'])
        self.color = (color, color, color) #/// подобрать цвета          
        self.nowPen = Pen(self.color, 2)
        backcolor = uniform_int(
            PARAM['vesicles_back_color_mean'],
            PARAM['vesicles_back_color_std'])    
        self.addColor = (backcolor, backcolor, backcolor)

        self.nowBrush = Brush(self.addColor)
             
        self.centerPoint = [0, 0]
        self.Points = []
        self.PointsWithOffset = []
           
        self.Create()

    def Create(self, min_r = 0, max_r = 0):
    
        mainVesiculesSize = np.random.randint(4, 7)
    
        self.sizeVesiculeMin = mainVesiculesSize-1
        self.sizeVesiculeMax = mainVesiculesSize+2
    
        
        if (min_r == 0):                                                               #  /// сделать осмесленную форму генерации
            min_r = np.random.randint(-95, -30)
         
        if (max_r == 0):
            max_r = np.random.randint(30, 95)

        min_r_x = np.random.randint(-95, -30)
        max_r_x = np.random.randint(30, 95)
               
        min_r_y = np.random.randint(-95, -30)
        max_r_y = np.random.randint(30, 95)
        
        square = (max_r_y-min_r_y) * (max_r_x-min_r_x)
        
        sqrt_int_square = int(round(math.sqrt(square)))
        
        self.numberPoints = np.random.randint(sqrt_int_square//2 - 10, sqrt_int_square)
        
        max_iteration = 1000
        
        fail_counter = 0
        
        tPoints = []
        
        for i in range(self.numberPoints):
        
            now_point = [np.random.randint(min_r_x, max_r_x), np.random.randint(min_r_y, max_r_y)]
            nowSizeCycle = np.random.randint(self.sizeVesiculeMin, self.sizeVesiculeMax)
            counter = 1
            
            while (self.CheckOverlap(tPoints, now_point, nowSizeCycle, 1) and counter < max_iteration):
                now_point = [np.random.randint(min_r_x, max_r_x), np.random.randint(min_r_y, max_r_y)]
                nowSizeCycle = np.random.randint(self.sizeVesiculeMin, self.sizeVesiculeMax)
                counter += 1
            
            if (counter == max_iteration):
                fail_counter += 1
            
            self.listSizeVesiculs.append(nowSizeCycle)
            tPoints.append(now_point)
            
        # поворот везикул
        self.angle = np.random.randint(0, 90) 
        
        angle = self.angle * (math.pi/180)
        
        #print(self.numberPoints, half_len, len(tPoints))
        for point in tPoints:
            x = int(round(point[0] * math.cos(angle) - point[1] * math.sin(angle)))
            y = int(round(point[0] * math.sin(angle) + point[1] * math.cos(angle)))
            
            #x = point[0]
            #y = point[1]
            
            self.Points.append([x,y])

            
        if (fail_counter != 0):
            print(f"The number of vesicles that could not be generated at a unique position: {fail_counter} out of {self.numberPoints}")

        self.ChangePositionPoints()

    def ChangePositionPoints(self):
        self.PointsWithOffset = []

        for point in self.Points:
            self.PointsWithOffset.append([self.centerPoint[0]+point[0], self.centerPoint[1]+point[1]])

    def NewPosition(self, x, y):
        self.centerPoint[0] = x
        self.centerPoint[1] = y

        self.ChangePositionPoints()
    
    def CheckOverlap(self, Points, point, sizeVesicule, proportion):
        for i in range(len(Points)):
           
            x_delt = abs(Points[i][0] - point[0]);
            y_delt = abs(Points[i][1] - point[1]);

            if x_delt / ((self.listSizeVesiculs[i] + sizeVesicule)/2 + self.nowPen.sizePen * 2) < proportion and\
               y_delt / ((self.listSizeVesiculs[i] + sizeVesicule)/2 + self.nowPen.sizePen * 2) < proportion:
                return True

        return False

    def Draw(self, image):
        # Основная рисующая фукция

        draw_image = image.copy()
        
        for i in range(self.numberPoints):            
            self.nowBrush.FullBrushEllipse(draw_image, self.PointsWithOffset[i], (self.listSizeVesiculs[i], self.listSizeVesiculs[i]))

            cv2.ellipse(img = draw_image,
                       center = self.PointsWithOffset[i],
                       axes = (self.listSizeVesiculs[i], self.listSizeVesiculs[i]),
                       color = self.nowPen.color,
                       thickness = self.nowPen.sizePen + self.listSizeVesiculs[i] - self.sizeVesiculeMin,
                       angle = 0,
                       startAngle = 0,
                       endAngle = 360)

        return draw_image

    def setDrawParam(self):
        self.nowPen.color = self.color 
        self.nowBrush.brush = self.addColor
        
    def setMaskParam(self):
        self.nowPen.color = (255,255,255)
        self.nowBrush.brush = (255,255,255)

    def DrawMask(self, image):
        #Смена цветов для рисования маски
        self.setMaskParam()
        mask = self.Draw(image)
        self.setDrawParam()
        
        return mask             
            
    def DrawUniqueArea(self, image, small_mode = False):
        # Функция создающая маску с немного большим отступом для алгорима случайного размещения новых органнел без пересечения 
        ret_image = image.copy()
        ret_image = ret_image.astype(int)
        
        draw_image = np.zeros(image.shape, np.uint8) 

        hull = cv2.convexHull(np.array(self.PointsWithOffset).astype(int))
        hull = np.squeeze(hull)

        #for point in hull:
        #    point[1] += 5

        draw_image = cv2.drawContours(draw_image, [hull], -1, (255,255,255), -1)

        if small_mode == False:
            kernel = np.array([[0, 1, 0],
                               [1, 1, 1],
                               [0, 1, 0]], dtype=np.uint8)

            draw_image = cv2.dilate(draw_image, kernel, iterations = 10)
        else:
            kernel = np.array([[0, 1, 0],
                               [1, 1, 1],
                               [0, 1, 0]], dtype=np.uint8)

            draw_image = cv2.dilate(draw_image, kernel, iterations = 7)

                    
        ret_image = ret_image + draw_image
        ret_image[ret_image[:,:,:] > 255] = 255
        ret_image = ret_image.astype(np.uint8)
        
        return ret_image
    
def testVesicles():
    q = None

    print("Press button 'Q' or 'q' to exit")
    while q != ord('q') and q != ord("Q"):
        
        color = np.random.randint(182, 200)
        
        img = np.full((512,512,3), (color,color,color), np.uint8)
        
        for i in range(0, 512, 32):
            img[i:i+15,:,:] += 30
        
        vesicles = Vesicles()
        
        vesicles.NewPosition(256,256)
        
        print("centerPoint", vesicles.centerPoint)
        print("Points", vesicles.Points)
        print("PointsWithOffset", vesicles.PointsWithOffset)
        
        img1 = vesicles.Draw(img)
        
        mask = np.zeros((512,512,3), np.uint8)
        
        tecnicalMask = np.zeros((512,512,3), np.uint8)
        
        mask = vesicles.DrawMask(mask)
        img2 = vesicles.Draw(img)
        tecnicalMask = vesicles.DrawUniqueArea(tecnicalMask)
        
        smalltecnicalMask = np.zeros((512,512,3), np.uint8)
        
        smalltecnicalMask = vesicles.DrawUniqueArea(smalltecnicalMask, True)
        
        cv2.imshow("img", img1)
        cv2.imshow("mask", mask)
        cv2.imshow("img2", img2)
        cv2.imshow("tecnicalMask", tecnicalMask)
        
        cv2.imshow("tecnicalMaskZove", tecnicalMask - mask)
        
        cv2.imshow("tecnicalMaskSmall", smalltecnicalMask)
        cv2.imshow("tecnicalMaskZoveSmall", smalltecnicalMask - mask)
        
        q = cv2.waitKey()

if __name__ == "__main__":
    testVesicles()

