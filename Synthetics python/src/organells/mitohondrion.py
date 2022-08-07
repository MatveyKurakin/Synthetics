import numpy as np
import cv2

import math

if __name__ == "__main__":
    import sys
    sys.path.append('.')

from src.container.spline import *
from src.container.subclass import *

class Mitohondrion:
    def __init__(self):
        self.type = "Mitohondrion"

        self.color = (85, 85, 85)                   #/// подобрать цвета, сделать заливку текстурой
        
        addColor = np.random.randint(100, 141)                     # основной цвет текстуры
        self.addColor = (addColor, addColor, addColor)
        
        self.nowPen = Pen(self.color, 5)    
        self.nowBrush = None
        self.texture = None

        self.angle = 0
        self.main_len = 0
        self.numberPoints = 0     
        self.centerPoint = [0, 0]
        self.Points = []
        self.PointsWithOffset = []
        self.addPoints = []            # точки с смещением для имитации косоро среза
        self.addPointsWithOffset = []

        self.Create()

    def Create(self):
        
        min_len = 26
        max_len = 196
        
        main_len = np.random.randint(min_len, max_len)
        self.main_len = main_len
        
        min_r = np.random.randint(5, 27)
        max_r = np.random.randint(27, 80)

        self.numberPoints = 2 + 2 * np.random.randint(1, 3+1)
        
        tPoints = []
        # Добавление первой главной точки
        startMPoint = [-main_len//2, 0]
        tPoints.append(startMPoint.copy())
        
        half_len = (self.numberPoints - 2)//2
        step = main_len/ (half_len+1)
        
        # заполнение первой половины митохондрии
        for i in range(half_len):
           addPointX = startMPoint[0] + step * (i+1)
           addPointY = -np.random.randint(min_r, max_r)
           #print(addPointX, addPointY) 
           tPoints.append([addPointX, addPointY])
       
        # Добавление второй главной точки
        endMPoint = [main_len//2, 0]
        tPoints.append(endMPoint.copy())
        
        # заполнение второй половины митохондрии
        
        for j in range(half_len):
           addPointX = endMPoint[0] - step * (j+1)
           addPointY = np.random.randint(min_r, max_r)
           #print(addPointX, addPointY)
           tPoints.append([addPointX, addPointY])
        
        # поворот митохондрии
        self.angle = np.random.randint(0, 90) 
        
        angle = self.angle * (math.pi/180)
        
        #print(self.numberPoints, half_len, len(tPoints))
        for point in tPoints:
            x = int(round(point[0] * math.cos(angle) - point[1] * math.sin(angle)))
            y = int(round(point[0] * math.sin(angle) + point[1] * math.cos(angle)))
            
            self.Points.append([x,y])

        #добавление доп. точек
        
        if np.random.random() < 0.5:
            size_dop = main_len // 6 - 1
            
            overlap_size_dop = size_dop//4
            
            #print (main_len)
            #print (size_dop)
            #print (size_dop//2)
        
            startMPointWithOffset = [startMPoint[0] - size_dop, 0]
            
            tAddPoints1 = [startMPointWithOffset,
                           [tPoints[1][0] + overlap_size_dop, tPoints[1][1] - 2],
                           [tPoints[1][0] - overlap_size_dop, tPoints[1][1] + 2],
                           startMPoint,
                           [tPoints[-1][0] - overlap_size_dop, tPoints[-1][1] - 2],
                           [tPoints[-1][0] + overlap_size_dop   , tPoints[-1][1] + 2]]
            
            endMPointWithOffset = [endMPoint[0] + size_dop, 0]
            
            tAddPoints2 = [endMPointWithOffset,
                           [tPoints[half_len][0] - overlap_size_dop, tPoints[half_len][1] - 2],
                           [tPoints[half_len][0] + overlap_size_dop, tPoints[half_len][1] + 2],
                           endMPoint,
                           [tPoints[half_len+2][0] + overlap_size_dop, tPoints[half_len+2][1] - 2],
                           [tPoints[half_len+2][0] - overlap_size_dop, tPoints[half_len+2][1] + 2]]
            
            tAddPoints = tAddPoints1 + tAddPoints2
            
            for point2 in tAddPoints:
                x = int(round(point2[0] * math.cos(angle) - point2[1] * math.sin(angle)))
                y = int(round(point2[0] * math.sin(angle) + point2[1] * math.cos(angle)))
                
                self.addPoints.append([x,y]) 

        self.ChangePositionPoints()

    def ChangePositionPoints(self):
        self.PointsWithOffset = []
        self.addPointsWithOffset = []

        for point in self.Points:
            self.PointsWithOffset.append([self.centerPoint[0]+point[0], self.centerPoint[1]+point[1]])
            
        for point2 in self.addPoints:
            self.addPointsWithOffset.append([self.centerPoint[0]+point2[0], self.centerPoint[1]+point2[1]])

    def NewPosition(self, x, y):
        self.centerPoint[0] = x
        self.centerPoint[1] = y

        self.ChangePositionPoints()
       
    def CreateTexture(self, image):

        self.texture = np.full((*image.shape[0:2],3), self.addColor, np.uint8)
        #self.texture[:,:] = (0,0,255)
        
        color = 240 - self.addColor[0]
        
        now_x = 10
        
        color2 = (80,80,80)
        
        while now_x < image.shape[1] - 10:
            now_y = 10
            while now_y < image.shape[1] - 10:
                len_line = np.random.randint(0, self.main_len // 2)

                start_pos = [now_x + np.random.randint(-2,3), now_y]
                enf_pos = [now_x + np.random.randint(-2,3), now_y+len_line]
                
                self.texture = cv2.line(self.texture, start_pos, enf_pos, color2, 5)
                
                if len_line == 0: # генерация черной точки
                    if np.random.random() < 0.5: 
                        self.texture = cv2.line(self.texture, start_pos, enf_pos, (1,1,1), 5)
                        self.texture = cv2.line(self.texture, start_pos, enf_pos, (1,1,1), 2)
                    else:
                        self.texture = cv2.line(self.texture, start_pos, enf_pos, (color,color,color), 2)
                else:
                    self.texture = cv2.line(self.texture, start_pos, enf_pos, (color,color,color), 2)

                #step y
                step_y = np.random.randint(7,20)
                now_y = now_y + len_line + step_y
                
            #step x
            step_x = np.random.randint(12,18)
            now_x += step_x

        (h, w) = image.shape[:2]
        center = (int(w / 2), int(h / 2))
        rotation_matrix = cv2.getRotationMatrix2D(center, 90 - self.angle, 1.5)
        self.texture = cv2.warpAffine(self.texture, rotation_matrix, (w, h))
        
        #print(self.texture.shape)
        self.texture[self.texture[:,:,0] == 0] = self.addColor

        #cv2.imshow("texture", self.texture)
        #cv2.waitKey()
        self.nowBrush = Brush(brush = self.texture, typeFull = "texture")

    def Draw(self, image, layer_drawing = True):
        # Основная рисующая фукция
        if layer_drawing:
            self.CreateTexture(image)

        draw_image = image.copy()
                
        if len(self.addPointsWithOffset) != 0:
            Brush(self.nowPen.color).FullBrush(draw_image, self.addPointsWithOffset[0:6]) 
            Brush(self.nowPen.color).FullBrush(draw_image, self.addPointsWithOffset[6:12]) 
            
        #cv2.ellipse(img = draw_image,
        #           center = self.PointsWithOffset[0],
        #           axes = (5,5),
        #           color = (0,0,255),
        #           thickness =  self.nowPen.sizePen,
        #           angle = 0,
        #           startAngle = 0,
        #           endAngle = 360)
           
        #cv2.ellipse(img = draw_image,
        #           center = self.PointsWithOffset[len(self.PointsWithOffset)//2],
        #           axes = (5,5),
        #           color = (0,0,255),
        #           thickness =  self.nowPen.sizePen,
        #           angle = 0,
        #           startAngle = 0,
        #           endAngle = 360) 


            
        self.nowBrush.FullBrush(draw_image, self.PointsWithOffset)

        spline_line(draw_image, self.PointsWithOffset, self.nowPen.color, self.nowPen.sizePen) 

        return draw_image
        
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
        
        draw_image = np.zeros(image.shape, np.uint8) 
        draw_image = self.DrawMask(draw_image)
        
        if small_mode == False:
            kernel = np.array([[0, 1, 0],
                               [1, 1, 1],
                               [0, 1, 0]], dtype=np.uint8)
                               
            draw_image = cv2.dilate(draw_image,kernel,iterations = 4)     
                    
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
        
        mask = mitohondrion.DrawMask(mask)
        img2 = mitohondrion.Draw(img)
        tecnicalMask = mitohondrion.DrawUniqueArea(tecnicalMask)
        
        cv2.imshow("img", img1)
        cv2.imshow("mask", mask)
        cv2.imshow("img2", img2)
        cv2.imshow("tecnicalMask", tecnicalMask)
        
        q = cv2.waitKey()

if __name__ == "__main__":
    testMitohondrion()


