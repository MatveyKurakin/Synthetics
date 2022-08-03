import numpy as np
import cv2

import math

if __name__ == "__main__":
    import sys
    sys.path.append('.')

from src.container.spline import *
from src.container.subclass import *

class Membrane:
    def __init__(self, compartmentsList, sizeImage):
        self.type = "Membrane"

        self.sizeLine = 4 - 1

        self.color = (80, 80, 80)
        self.nowColor = self.color
        self.labels = None

        self.Points = []

        self.Create(compartmentsList.copy(), sizeImage)

    def Create(self, compartments, sizeImg):
    
        checkMask = np.zeros((*sizeImg,3), np.uint8)

        # Создание маски регионов и зпаолнение её
        for compartment in compartments:
            checkMask = compartment.DrawUniqueArea(checkMask, small_mode = True)

        # Сохранение общей маски
        #cv2.imwrite("Sintetic_generation/original/fileMask.png", checkMask)

        # Создание и инициализация 0 матрицы меток (или матрицы изображения меток)
        #labelImage = np.zeros(sizeImg, int)

        connectivity = 4
        retval, labels, stats, centroids = cv2.connectedComponentsWithStats(checkMask[:,:,0], connectivity, cv2.CV_32S)

        # retval - возвращает колличество меток (с 0 меткой для фона) кол-во объектов retval-1 [1:retval-1]
        #print(retval)
        #print(labels)
        #print(labels.max())

        # Сохранение маски меток
        #cv2.imwrite("Sintetic_generation/original/fileMaskLabels.png", labels.astype(np.uint8))

        labels = self.RegionExpansion(labels)

        # Сохранение маски разросшихся регионов
        #cv2.imwrite("Sintetic_generation/original/fileMaskLabelsEnd.png", (labels[:,:] + 1).astype(np.uint8))
        
        self.labels = self.ExpansionPSD(labels, compartments)
        
        #cv2.imwrite("Sintetic_generation/original/fileMaskLabelsEndWithPSD.png", (self.labels[:,:] + 2).astype(np.uint8))
        
    def RegionExpansion(self, input_labels):
        """
        Функция разрастания регионов итеративно расширяет границу 
        Также эта функия добавляет граничные пиксели в self.Points
        """
        labels = input_labels.copy()

        # инициализация цикла
        Work_points = []
        for y in range(labels.shape[0]):
            for x in range(labels.shape[1]):
                if labels[y,x] != 0:
                    if x > 0 and labels[y,x-1] == 0:
                        Work_points.append([x,y])
                    if x < labels.shape[1]-1 and labels[y,x+1] == 0:
                        Work_points.append([x,y])
                    
                    if y > 0 and labels[y-1,x] == 0:
                        Work_points.append([x,y])
                    if y < labels.shape[0]-1 and labels[y+1,x] == 0:
                        Work_points.append([x,y])
                    
        np.random.shuffle(Work_points)
         
        #print("iter 0", len(Work_points))
        counter = 0
         
        while len(Work_points) != 0:
            Work_points_iteration = []
            
            for (x,y) in Work_points:
                boarder = 0
                if x > 0:
                    if labels[y,x-1] == 0:
                        labels[y,x-1] = labels[y,x]
                        Work_points_iteration.append([x-1,y])
                    elif labels[y,x-1] != labels[y,x]:                      # граница в 2 пикселя
                        boarder += 1
                    
                if x < labels.shape[1]-1:
                    if labels[y,x+1] == 0:
                        labels[y,x+1] = labels[y,x]
                        Work_points_iteration.append([x+1,y])
                    elif labels[y,x+1] != labels[y,x]: 
                        boarder += 1 
                
                if y > 0:
                    if labels[y-1,x] == 0:
                        labels[y-1,x] = labels[y,x]
                        Work_points_iteration.append([x,y-1])
                    elif labels[y-1,x] != labels[y,x]:
                        boarder += 1 
                    
                    
                if y < labels.shape[0]-1:
                    if labels[y+1,x] == 0:
                        labels[y+1,x] = labels[y,x]
                        Work_points_iteration.append([x,y+1])
                    elif labels[y+1,x] != labels[y,x]:
                        boarder += 1
                        
                # Случайность заполнения исправляет образование очень толстых границ
                if boarder != 0:
                    if np.random.random() < 0.5:                               
                        labels[y,x] = -1                                       # Значение -1 обозначает границу 
                        self.Points.append([x,y])
                    else:
                        Work_points_iteration.append([x,y])
                
            np.random.shuffle(Work_points_iteration)
            Work_points = Work_points_iteration
            counter += 1
          
        print(f"Number region iteration: {counter}")
        return labels
                
    def ExpansionPSD(self, input_labels, compartments):
        labels = input_labels.copy()

        for compartment in compartments:
            if compartment.type == "PSD":
                center = compartment.centerPoint
                startPoint = compartment.PointsWithOffset[0]
                normalPoint = compartment.PointsWithOffset[1]
                endPoint = compartment.PointsWithOffset[2]

                # смещение разметки мембран так как в реальных данных PSD больше внутри 1 мембраны клетки
                if center[0] == normalPoint[0] and center[1] == normalPoint[1]:
                    # вычисление нормали к вектору из end to start
                    eDirX = 1;
                    eDirY = -((startPoint[0] - endPoint[0]) / (startPoint[1] - endPoint[1]))

                else:
                    eDirX = normalPoint[0] - center[0];
                    eDirY = normalPoint[1] - center[1];

                lenNormal = math.sqrt(eDirX * eDirX + eDirY * eDirY)
                eDirX /= lenNormal
                eDirY /= lenNormal

                addedX = int(round(eDirX * 2)) # 2 = (6 - 2) /2 - размер пера PSD минус размер пера мембран деленое на 2
                addedY = int(round(eDirY * 2)) # 2 = (6 - 2) /2 - размер пера PSD минус размер пера мембран деленое на 2 

                # добавление смещения
                offset_main_normal = 3
                offset_start_normal = -1
                
                self.AddingPSDDirection(labels, [normalPoint[0] + offset_main_normal * addedX, normalPoint[1] + offset_main_normal * addedY],
                                                [startPoint[0] + addedX * offset_start_normal, startPoint[1] + addedY * offset_start_normal])
                                                
                self.AddingPSDDirection(labels, [normalPoint[0] + offset_main_normal * addedX, normalPoint[1] + offset_main_normal * addedY],
                                                [endPoint[0] + addedX * offset_start_normal, endPoint[1] + addedY * offset_start_normal])

        return labels

    def AddingPSDDirection(self, labels, antiDir, startPoint, labelPrint = -2):
        #основная идея расширяться в направлении конца до тех пор, пока не упрёмся в границу или выйдем за поле

        # если край за полем видимости, то выходим
        height, width = labels.shape
        
        if (startPoint[0] < 0 or startPoint[0] >= width):
            return
            
        if (startPoint[1] < 0 or startPoint[1] >= height):
            return
            
        # вычисление направления движения
        directionX = startPoint[0] - antiDir[0]
        directionY = startPoint[1] - antiDir[1]
        
        lenDir = math.sqrt(directionX * directionX + directionY * directionY)
        directionX /= lenDir
        directionY /= lenDir
        
        #print(f"stPoint {startPoint}, antiDir {antiDir},  dir : {directionX}, {directionY}")
        
        nowPos = startPoint.copy()
        # Двигаемся, помечая границей labelPrint пока не выйдем за поле или рядом будет граница
        
        counter = 1
        repit_dir = True
        
        while repit_dir:
            
            #print(nowPos)
            flag_fing_boarder = False; # flag нахождения в окрестности границы

            if nowPos[0] > 0:
                if labels[nowPos[1], nowPos[0] - 1] == -1:
                    flag_fing_boarder = True

            if nowPos[0] < width - 1:
                if labels[nowPos[1], nowPos[0] + 1] == -1:
                    flag_fing_boarder = True

            if nowPos[1] > 0:
                if labels[nowPos[1] - 1, nowPos[0]] == -1:
                    flag_fing_boarder = True

            if nowPos[1] < height - 1:
                if labels[nowPos[1] + 1, nowPos[0]] == -1:
                    flag_fing_boarder = True

            if flag_fing_boarder == False:
                # Добавление граничного пикселя
                labels[nowPos[1], nowPos[0]] = labelPrint
                self.Points.append(nowPos.copy())

                # вычисление следующего шага
                nowPos[0] = startPoint[0] + int(round(directionX * counter))
                nowPos[1] = startPoint[1] + int(round(directionY * counter))
                
                counter += 1
                
                # проверка останова
                if nowPos[0] < 0 or nowPos[0] >= width:
                    repit_dir = False

                elif nowPos[1] < 0 or nowPos[1] >= height:
                    repit_dir = False
                    
                elif labels[nowPos[1], nowPos[0]] == -1:
                    repit_dir = False
               
            else:
                labels[nowPos[1], nowPos[0]] = labelPrint
                self.Points.append(nowPos.copy())
                repit_dir = False

        #raise Exception("my error")

    def Draw(self, image):
        # Основная рисующая фукция

        draw_image = image.copy()
        
        mask = np.zeros(draw_image.shape[0:2], np.uint8)
        mask[self.labels[:,:] == -1] = 255
       
        kernel = np.array([[0, 1, 0],
                           [1, 1, 1],
                           [0, 1, 0]], dtype=np.uint8)
                               
        mask = cv2.dilate(mask,kernel,iterations = self.sizeLine)
        
        maskPSD = np.zeros(draw_image.shape[0:2], np.uint8)
        maskPSD[self.labels[:,:] == -2] = 255
        maskPSD = cv2.dilate(maskPSD,kernel,iterations = 2)
        
        
        draw_image[mask[:,:] == 255] = self.nowColor  
        draw_image[maskPSD[:,:] == 255] = self.nowColor

        return draw_image
        
    def setDrawParam(self):
        self.nowColor = self.color 
        
    def setMaskParam(self):
        self.nowColor = (255,255,255)
        
    def DrawMask(self, image):
        self.setMaskParam()
        mask = self.Draw(image)
        self.setDrawParam()
        
        return mask             
            
    def DrawUniqueArea(self, image):
        # Функция создающая маску с немного большим отступом для алгорима случайного размещения новых органнел без пересечения
              
        draw_image = image.copy()
        
        draw_image = self.DrawMask(draw_image)
        
        kernel = np.array([[0, 1, 0],
                           [1, 1, 1],
                           [0, 1, 0]], dtype=np.uint8)
                           
        draw_image = cv2.dilate(draw_image,kernel,iterations = 2)
        
        return draw_image

