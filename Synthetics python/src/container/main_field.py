import numpy as np
import cv2
import os
import datetime
import math
from settings import PARAM, uniform_int

import albumentations as albu

if __name__ == "__main__":
    import sys
    sys.path.append('.')


from src.organells.axon import Axon
from src.organells.PSD import PSD
from src.organells.vesicles import Vesicles
from src.organells.mitohondrion import Mitohondrion
from src.organells.membrane import Membrane

from src.container.spline import *
from src.container.subclass import *

class PointsNoise:
    def __init__(self, size = (512,512)):
        # self.Points = []
        # self.PointsWithOffset = []
        self.sizeImage = size

    def Draw(self, image):
        draw_image = image.copy()
        # число линий
        count = np.random.randint(100, 400+1)
        # максимальная длина линий
        maxdist = np.random.randint(4, 40, 4)

        #  разбиваем область на 4 части в каждой будет свое направление линий
        xs = np.random.randint(0, self.sizeImage[0]/2, count)
        ys = np.random.randint(0, self.sizeImage[1]/2, count)

        xs[int(count/4):int(count/4) + int(count/4)] = np.random.randint(int(self.sizeImage[0]//2), self.sizeImage[0], int(count/4))
        xs[int(count*3/4):int(count*3/4) + int(count/4)] = np.random.randint(int(self.sizeImage[0]//2), self.sizeImage[0], int(count/4))
        ys[int(count/2): int(count/2) + int(count/2)] = np.random.randint(int(self.sizeImage[1]//2), self.sizeImage[1], int(count/2))

        #  направление линий
        vecx = np.random.rand(4)
        vecy = np.random.rand(4)*2 - 1

        #  забиваем дистанцию у каждой четверти свой максимум
        #  забиваем направления
        xd = np.ones(count)
        yd = np.ones(count)
        dist = np.ones(count)*2
        j = 0
        for i in range(0, int(count//4)*4, int(count//4)):
            a = np.asarray([vecx[j], vecy[j]])
            a = a/np.sqrt(a.dot(a))
            xd[i:i+int(count//4)] = a[0]
            yd[i:i+int(count//4)] = a[1]
            dist[i:i+int(count//4)] = np.random.randint(3, maxdist[j], int(count//4))
            j = j + 1

        xe = xs + xd * dist
        ye = ys + yd * dist

        xe = xe.astype(np.int)
        ye = ye.astype(np.int)

        xe[xe < 0] = 0
        ye[ye < 0] = 0

        xe[xe > self.sizeImage[0]] = self.sizeImage[0]
        ye[ye > self.sizeImage[1]] = self.sizeImage[1]

        #  толщина линий
        w = np.random.randint(1, 5, count)

        for i in range(0, count):    
            c = np.random.randint(95, 140)
            draw_image = cv2.line(draw_image, [xs[i], ys[i]], [xe[i], ye[i]], (c,c,c) , w[i])

        count = np.random.randint(200, 1000+1)
        # максимальная длина линий
        xs = np.random.randint(0, self.sizeImage[0], count)
        ys = np.random.randint(0, self.sizeImage[1], count)
        xd = np.random.randint(-5, 5, count)
        yd = np.random.randint(-5, 5, count)
        xe = np.minimum(np.ones(count) * self.sizeImage[0], np.maximum(np.zeros(count), xs + xd)).astype(np.int)
        ye = np.minimum(np.ones(count) * self.sizeImage[1], np.maximum(np.zeros(count),ys + yd)).astype(np.int)
        w = np.random.randint(1, 5, count)
        for i in range(0, count):    
            c = np.random.randint(100, 150)
            draw_image = cv2.line(draw_image, [xs[i], ys[i]], [xe[i], ye[i]], (c,c,c) , w[i])

        return draw_image

def AddGaussianNoise(image, noisePower = 16):
    mean = 0

    gaussian = np.random.normal(mean, noisePower, image.shape[0:2])

    noise_image = np.zeros(image.shape, np.float32)

    if len(image.shape) == 2:
        noise_image = image + gaussian
    else:
        noise_image[:, :, 0] = image[:, :, 0] + gaussian
        noise_image[:, :, 1] = image[:, :, 1] + gaussian
        noise_image[:, :, 2] = image[:, :, 2] + gaussian

    noise_image[noise_image[:,:,:] < 0] = 0
    noise_image[noise_image[:,:,:] > 255] = 255

    noise_image = noise_image.astype(np.uint8)

    return noise_image

class SpamComponents:
    def __init__(self, compartmentsList, numberSpam = 10):
        '''
        I say "hello"
        This class adds spam or junk to the input image. At the same time, garbage is not superimposed on classes.

        sizeOverlap - offset from masks
        numberSpam - amount of added spam

        возможно стоит сделать параметризованный по типам класс (типо точка, полосочка, и т.д. по типу органнел) чтобы на соседних слоях была та же картина
        '''
        self.type = "SpamComponents"
        self.sizeOverlap = 1
        self.numberSpam = numberSpam
        self.compartmentsList = compartmentsList

    def CreateLine(self, len_line, max_y = 10, len_segment_min = 10, len_segment_max = 20):
        now_pos = -len_line//2
        y_s =  np.random.randint(-max_y, max_y+1)
        # задание первой точки линии
        points_segment = [[now_pos, y_s]]

        # добавление промежуточных участков
        len_segment = np.random.randint(len_segment_min, len_segment_max + 1)
        while now_pos+len_segment_min+len_segment_max < len_line//2:
            x_s = now_pos + len_segment
            y_s =  np.random.randint(-max_y, max_y+1)
            points_segment.append([x_s, y_s])

            now_pos = x_s
            len_segment = np.random.randint(len_segment_min, len_segment_max + 1)

        # добавление конечной точки
        x_s = len_line//2 - now_pos
        y_s =  np.random.randint(-max_y, max_y+1)
        points_segment.append([x_s, y_s])

        # поворот вокруг центральной точки
        change_angle = math.radians(np.random.randint(0, 360))
        work_points = []
        for point in points_segment:
            x_s = int(round(point[0] * math.cos(change_angle) - point[1] * math.sin(change_angle)))
            y_s = int(round(point[0] * math.sin(change_angle) + point[1] * math.cos(change_angle)))
            work_points.append([x_s,y_s])

        return work_points

    def DrawType1(self, image, mask, color, size_line):
        # выбор центра для паттерна
        x = np.random.randint(15, image.shape[1] - 15)
        y = np.random.randint(15, image.shape[0] - 15)

        angle = np.random.randint(0, 180)

        radius = np.random.randint(7, 20, 2)

        cv2.ellipse(img = image,
                    center = (x, y),
                    axes = radius,
                    color = (color, color, color),
                    thickness = size_line,
                    angle = angle,
                    startAngle = 0,
                    endAngle = 360)

        cv2.ellipse(img = mask,
                    center = (x, y),
                    axes = radius,
                    color = (255, 255,255),
                    thickness = 2+1,
                    angle = angle,
                    startAngle = 0,
                    endAngle = 360)

        cv2.ellipse(img = mask,
                    center = (x, y),
                    axes = radius,
                    color = (255, 255,255),
                    thickness = -1,
                    angle = angle,
                    startAngle = 0,
                    endAngle = 360)
        return mask

    def DrawType2(self, image, mask, color, size_line):
        # выбор центра для паттерна
        x = np.random.randint(45, image.shape[1] - 45)
        y = np.random.randint(45, image.shape[0] - 45)

        # длина линии
        len_line = np.random.randint(20, 90 + 1)

        max_y = 10

        len_segment_max = 20
        len_segment_min = 10

        work_points = self.CreateLine(len_line, max_y, len_segment_min, len_segment_max)

        height_line = np.random.randint(3, 10+1)

        # смещение в центр паттерна
        out_list = np.array([[int(round(work_points[i][0] + x)), int(round(work_points[i][1] + y))] for i in range(len(work_points))])

        cv2.polylines(mask, [out_list], isClosed = False, color = (255,255,255), thickness = height_line + size_line, lineType = cv2.LINE_AA)
        cv2.polylines(mask, [out_list], isClosed = False, color = (0,0,0), thickness = height_line, lineType = cv2.LINE_AA)

        mask[mask[:,:,0] > 0] = (255,255,255)
        image[mask[:,:,0] == 255] = (color, color, color)

        kernel = np.array([[0, 1, 0],
                           [1, 1, 1],
                           [0, 1, 0]], dtype=np.uint8)
        mask = cv2.dilate(mask, kernel, iterations = 3)
        return mask

    def DrawType3(self, image, mask):
        # выбор центра для паттерна
        x = np.random.randint(35, image.shape[1] - 35)
        y = np.random.randint(35, image.shape[0] - 35)

        angle = np.random.randint(0, 180)

        radius = np.random.randint(3, 14+1)

        color = np.random.randint(44,70+1)

        cv2.ellipse(img = image,
                    center = (x, y),
                    axes = (radius,radius),
                    color = (color, color, color),
                    thickness = -1,
                    angle = angle,
                    startAngle = 0,
                    endAngle = 360)

        cv2.ellipse(img = mask,
                    center = (x, y),
                    axes = (radius,radius),
                    color = (255, 255,255),
                    thickness = -1,
                    angle = angle,
                    startAngle = 0,
                    endAngle = 360)

        return mask

    def DrawType4(self, image, mask, size_line):
        # выбор центра для паттерна
        x = np.random.randint(50, image.shape[1] - 50)
        y = np.random.randint(50, image.shape[0] - 50)

        color = np.random.randint(44,70+1)
        # длина линии
        len_line = np.random.randint(50, 100 + 1)

        max_y = 5

        len_segment_max = 20
        len_segment_min = 10

        work_points = self.CreateLine(len_line, max_y, len_segment_min, len_segment_max)

        # смещение в центр паттерна
        out_list = np.array([[int(round(work_points[i][0] + x)), int(round(work_points[i][1] + y))] for i in range(len(work_points))])

        cv2.polylines(mask, [out_list], isClosed = False, color = (255,255,255), thickness = size_line+1, lineType = cv2.LINE_AA)

        mask[mask[:,:,0] > 0] = (255,255,255)
        image[mask[:,:,0] == 255] = (color, color, color)

        kernel = np.array([[0, 1, 0],
                           [1, 1, 1],
                           [0, 1, 0]], dtype=np.uint8)
        mask = cv2.dilate(mask, kernel, iterations = 3)

        return mask

    def DrawAny(self, image, color, size_line):
        # маска для проверки на пересечение
        temp_mask = np.zeros(image.shape, np.uint8)

        random_val = np.random.randint(0, 25)
        # наиболее частые - это небольшие кружочки и полые полосочки
        # темные кружочки и линии - очень редкие
        if random_val < 10:
            type_pattern = 1    # type1 - small ellipse
        elif random_val < 20:
            type_pattern = 2    # type2 - line
        elif random_val == 20:
            type_pattern = 3    # type3 - black point
        else:
            type_pattern = 4    # type4 - black line

        # type1 - small ellipse
        if type_pattern == 1:
            temp_mask = self.DrawType1(image, temp_mask, color, size_line)
        # type2 - line
        elif type_pattern == 2:
            temp_mask = self.DrawType2(image, temp_mask, color, size_line)
        # type3 - black point
        elif type_pattern == 3:
            temp_mask = self.DrawType3(image, temp_mask)
        # type4 - black line
        elif type_pattern == 4:
            temp_mask = self.DrawType4(image, temp_mask, size_line)
        else:
            raise Exception("What's up in DrawAny from SpamComponents?")

        return image, temp_mask

    def DrawLayer(self, image):
        # создание маски для всех классов
        masks_classes = np.zeros(image.shape, np.uint8)

        kernel = np.array([[0, 1, 0],
                           [1, 1, 1],
                           [0, 1, 0]], dtype=np.uint8)
        # заполнение маски всеми классами
        for component in self.compartmentsList:
            if component.type != "SpamComponents" and\
               component.type != "Vesicles" and\
               component.type != "Axon" and\
               component.type != "PSD" and\
               component.type != "Membrane":
                masks_classes = component.DrawMask(masks_classes)

            elif component.type == "Vesicles" or component.type == "PSD":
                masks_classes_temp = np.zeros(image.shape, np.uint8)
                masks_classes_temp = component.DrawUniqueArea(masks_classes_temp) # не рисовать рядом (small_mode = False)
                masks_classes_temp = cv2.dilate(masks_classes_temp, kernel, iterations = 25) # вообще даже близко не рисовать
                masks_classes = masks_classes | masks_classes_temp

            elif component.type == "Axon":
                masks_classes = component.DrawUniqueArea(masks_classes, small_mode = True)    # не рисовать внутри, но можно рядом

            elif component.type == "Membrane":
                masks_classes = component.DrawUniqueArea(masks_classes)
                sizeLine = component.sizeLine

        # отступ от маски
        masks_classes = cv2.dilate(masks_classes, kernel, self.sizeOverlap)

        iter = 0
        max_iter = 10000
        count = 0

        while count < self.numberSpam and iter < max_iter:
            image_clone = image.copy()

            drawColor = uniform_int(PARAM['spam_color_mean'],
                                    PARAM['spam_color_std'])

            temp_image, temp_mask = self.DrawAny(image_clone, drawColor, sizeLine)

            if all(masks_classes[temp_mask[:,:,0] == 255, 0] == 0):
                masks_classes = masks_classes | temp_mask
                image = temp_image
                count += 1

            iter += 1

        if iter == max_iter:
            print("I can't create spam : only", count, "is",  self.numberSpam)

        return image

class Form:
    def __init__(self, size = (512, 512)):

        color = uniform_int(
            PARAM['main_color_mean'],
            PARAM['main_color_std'])
        self.backgroundСolor = (color, color, color) # выбор цвета фона

        self.nowViewType = 'layer'
        self.sizeImage = size

        #self.currView = np.zeros((*self.sizeImage, 3), np.uint8)
        #self.backgroundImg = np.zeros((*self.sizeImage, 3), np.uint8)

        #self.technicalMackAllcompanenst = np.zeros((*self.sizeImage, 3), np.uint8)

        self.compartmentsList = []

    def CheckOverlapNewElement(self, all_mask, check_mask):
        if any(all_mask[check_mask[:,:,0] != 0, 0] != 0):
            return True
        return False

    def AddNewElementWithoutOverlap(self, compartmentsList, newComponent):

        checkImage = np.zeros((*self.sizeImage, 3), np.uint8)

        for component in compartmentsList:
            checkImage = component.DrawUniqueArea(checkImage)

        max_iter = 300

        checkNewImage = np.zeros((*self.sizeImage, 3), np.uint8)

        if newComponent.type == "PSD":
            step_from_edge = 32
        else:
            step_from_edge = 5

        newComponent.NewPosition(np.random.randint(step_from_edge, self.sizeImage[1]-step_from_edge), np.random.randint(step_from_edge, self.sizeImage[0] - step_from_edge))
        newComponent.setRandomAngle(0, 90)
        checkNewImage = newComponent.DrawUniqueArea(checkNewImage)

        counter = 1

        while self.CheckOverlapNewElement(checkImage, checkNewImage) and counter < max_iter:
            checkNewImage = np.zeros((*self.sizeImage, 3), np.uint8)
            newComponent.NewPosition(np.random.randint(step_from_edge, self.sizeImage[1]-step_from_edge), np.random.randint(step_from_edge, self.sizeImage[0] - step_from_edge))
            newComponent.setRandomAngle(0, 90)
            checkNewImage = newComponent.DrawUniqueArea(checkNewImage)

            counter += 1

        #except Exception as ex:
        #    print(ex)
        #    print(newComponent.type)
        #    print(f"{type(ex).__name__} at line {ex.__traceback__.tb_lineno} of {__file__}: {ex}")

        # Добавлено исключение чтобы элементы не накладывались друг на друга
        if counter == max_iter:
            raise Exception("Can't add unique position new element")

    def AddNewElementWithoutOverlap_WithMask(self, technicalMackAllcompanenst, newComponent):
        max_iter = 200

        checkNewImage = np.zeros((*self.sizeImage, 3), np.uint8)

        if newComponent.type == "PSD":
            step_from_edge = 32
        else:
            step_from_edge = 5

        newComponent.NewPosition(np.random.randint(step_from_edge, self.sizeImage[1]-step_from_edge), np.random.randint(step_from_edge, self.sizeImage[0] - step_from_edge))
        newComponent.setRandomAngle(0, 90)
        checkNewImage = newComponent.DrawUniqueArea(checkNewImage)

        counter = 1

        while self.CheckOverlapNewElement(technicalMackAllcompanenst, checkNewImage) and counter < max_iter:
            checkNewImage = np.zeros((*self.sizeImage, 3), np.uint8)
            newComponent.NewPosition(np.random.randint(step_from_edge, self.sizeImage[1]-step_from_edge), np.random.randint(step_from_edge, self.sizeImage[0] - step_from_edge))
            newComponent.setRandomAngle(0, 90)
            checkNewImage = newComponent.DrawUniqueArea(checkNewImage)

            counter += 1

        # Добавлено исключение чтобы элементы не накладывались друг на друга
        if counter == max_iter:
            raise Exception("Can't add unique position new element")

    def addNewElementIntoImage(self, compartmentsList, newComponent):
        if newComponent is not None:
            try:
                # нет смысла проверять мембраны, так как они касаются PSD и будет перекрытие
                if newComponent.type != "Membrane":
                    self.AddNewElementWithoutOverlap(compartmentsList, newComponent);

                compartmentsList.append(newComponent)
                newComponent = None

            except Exception as ex:
                print(ex)
                #print(f"{type(ex).__name__} at line {ex.__traceback__.tb_lineno} of {__file__}: {ex}")

    def addNewElementIntoImage_WithMask(self, compartmentsList, technicalMackAllcompanenst, newComponent):
        if newComponent is not None:
            try:
                # нет смысла проверять мембраны, так как они касаются PSD и будет перекрытие
                if newComponent.type != "Membrane":
                    self.AddNewElementWithoutOverlap_WithMask(technicalMackAllcompanenst, newComponent);

                compartmentsList.append(newComponent)
                technicalMackAllcompanenst = newComponent.DrawUniqueArea(technicalMackAllcompanenst)
                newComponent = None

            except Exception as ex:
                print(ex)
                #print(f"{type(ex).__name__} at line {ex.__traceback__.tb_lineno} of {__file__}: {ex}")

        return technicalMackAllcompanenst

    def DrawBackround(self, img, color):
        draw_image = np.full(img.shape, color, np.uint8)

        p = PointsNoise(self.sizeImage)
        draw_image = p.Draw(draw_image)

        r = 3
        G = (2 * r + 1) / 3
        draw_image = cv2.GaussianBlur(draw_image,(r*2+1,r*2+1), G)

        return draw_image

    def createListGeneration(self, max_count_PSD = 0, max_count_Axon = 0, max_count_Vesicles = 0, max_count_Mitohondrion = 0, spam = 0):

        if max_count_PSD > 0:
            count_PSD = np.random.randint(1, max_count_PSD+1)
        else:
            count_PSD = 0

        if max_count_Axon > 0:
            count_Axon = np.random.randint(1, max_count_Axon+1)
        else:
            count_Axon = 0

        if max_count_Vesicles > 0:
            count_Vesicles = np.random.randint(1, max_count_Vesicles+1)
        else:
            count_Vesicles = 0

        if max_count_Mitohondrion > 0:
            count_Mitohondrion = np.random.randint(1, max_count_Mitohondrion+1)
        else:
            count_Mitohondrion = 0


        addAxonAfterMempbran         = np.random.randint(0, count_Axon+1)
        addMitohondrionAfterMempbran = np.random.randint(0, count_Mitohondrion+1)
        addVesiclesAfterMempbran     = np.random.randint(0, count_Vesicles+1)

        addAxonBeforeMempbran         = count_Axon         - addAxonAfterMempbran
        addMitohondrionBeforeMempbran = count_Mitohondrion - addMitohondrionAfterMempbran
        addVesiclesBeforeMempbran     = count_Vesicles     - addVesiclesAfterMempbran

        RetList = []

        ListMixingClass = [["Axon"        , addAxonBeforeMempbran],
                           ["Mitohondrion", addMitohondrionBeforeMempbran],
                           ["Vesicles"    , addVesiclesBeforeMempbran],
                           ["PSD"         , count_PSD]]

        while len(ListMixingClass) != 0:
            index = np.random.randint(0, len(ListMixingClass))

            if ListMixingClass[index][1] <= 0:
                ListMixingClass.pop(index)
            else:
                ListMixingClass[index][1] -= 1

                if ListMixingClass[index][0] == "Axon":
                    newElement = Axon()
                elif ListMixingClass[index][0] == "Mitohondrion":
                    newElement = Mitohondrion()
                elif ListMixingClass[index][0] == "Vesicles":
                    newElement = Vesicles()
                elif ListMixingClass[index][0] == "PSD":
                    newElement = PSD()
                else:
                    raise Exception("What's up ?")

                UnionMask = self.addNewElementIntoImage(RetList, newElement)

        #################################################
        UnionMask = self.addNewElementIntoImage(RetList, Membrane(self.sizeImage, RetList))
        #################################################

        ListMixingClass2 = [["Axon"        , addAxonAfterMempbran],
                            ["Mitohondrion", addMitohondrionAfterMempbran],
                            ["Vesicles"    , addVesiclesAfterMempbran]]

        while len(ListMixingClass2) != 0:
            index = np.random.randint(0, len(ListMixingClass2))

            if ListMixingClass2[index][1] <= 0:
                ListMixingClass2.pop(index)
            else:
                ListMixingClass2[index][1] -= 1
                try:
                    if ListMixingClass2[index][0] == "Axon":
                        newElement = Axon()
                    elif ListMixingClass2[index][0] == "Mitohondrion":
                        newElement = Mitohondrion()
                    elif ListMixingClass2[index][0] == "Vesicles":
                        newElement = Vesicles()
                    else:
                        raise Exception("What's up ?")

                    self.addNewElementIntoImage(RetList, newElement)
                except Exception as ex:
                    print(ex)
                    #print(f"{type(ex).__name__} at line {ex.__traceback__.tb_lineno} of {__file__}: {ex}")

        if spam != 0:
            RetList.append(SpamComponents(RetList.copy(), spam))

        return RetList

    def createListGenerationWithMask(self, max_count_PSD = 0, max_count_Axon = 0, max_count_Vesicles = 0, max_count_Mitohondrion = 0):

        if max_count_PSD > 0:
            count_PSD = np.random.randint(1, max_count_PSD+1)
        else:
            count_PSD = 0

        if max_count_Axon > 0:
            count_Axon = np.random.randint(1, max_count_Axon+1)
        else:
            count_Axon = 0

        if max_count_Vesicles > 0:
            count_Vesicles = np.random.randint(1, max_count_Vesicles+1)
        else:
            count_Vesicles = 0

        if max_count_Mitohondrion > 0:
            count_Mitohondrion = np.random.randint(1, max_count_Mitohondrion+1)
        else:
            count_Mitohondrion = 0


        addAxonAfterMempbran         = np.random.randint(0, count_Axon+1)
        addMitohondrionAfterMempbran = np.random.randint(0, count_Mitohondrion+1)
        addVesiclesAfterMempbran     = np.random.randint(0, count_Vesicles+1)

        addAxonBeforeMempbran         = count_Axon         - addAxonAfterMempbran
        addMitohondrionBeforeMempbran = count_Mitohondrion - addMitohondrionAfterMempbran
        addVesiclesBeforeMempbran     = count_Vesicles     - addVesiclesAfterMempbran

        RetList = []

        ListMixingClass = [["Axon"        , addAxonBeforeMempbran],
                           ["Mitohondrion", addMitohondrionBeforeMempbran],
                           ["Vesicles"    , addVesiclesBeforeMempbran],
                           ["PSD"         , count_PSD]]

        UnionMask = np.zeros((*self.sizeImage,3), np.uint8)

        while len(ListMixingClass) != 0:
            index = np.random.randint(0, len(ListMixingClass))

            if ListMixingClass[index][1] <= 0:
                ListMixingClass.pop(index)
            else:
                ListMixingClass[index][1] -= 1

                if ListMixingClass[index][0] == "Axon":
                    newElement = Axon()
                elif ListMixingClass[index][0] == "Mitohondrion":
                    newElement = Mitohondrion()
                elif ListMixingClass[index][0] == "Vesicles":
                    newElement = Vesicles()
                elif ListMixingClass[index][0] == "PSD":
                    newElement = PSD()
                else:
                    raise Exception("What's up ?")

                UnionMask = self.addNewElementIntoImage_WithMask(RetList, UnionMask, newElement)

        #cv2.imshow("testMask", UnionMask)
        #cv2.waitKey()
        #################################################
        UnionMask = self.addNewElementIntoImage_WithMask(RetList, UnionMask, Membrane(self.sizeImage, RetList))
        #################################################

        ListMixingClass2 = [["Axon"        , addAxonAfterMempbran],
                            ["Mitohondrion", addMitohondrionAfterMempbran],
                            ["Vesicles"    , addVesiclesAfterMempbran]]

        while len(ListMixingClass2) != 0:
            index = np.random.randint(0, len(ListMixingClass2))

            if ListMixingClass2[index][1] <= 0:
                ListMixingClass2.pop(index)
            else:
                ListMixingClass2[index][1] -= 1
                try:
                    if ListMixingClass2[index][0] == "Axon":
                        newElement = Axon()
                    elif ListMixingClass2[index][0] == "Mitohondrion":
                        newElement = Mitohondrion()
                    elif ListMixingClass2[index][0] == "Vesicles":
                        newElement = Vesicles()
                    else:
                        raise Exception("What's up ?")

                    UnionMask = self.addNewElementIntoImage_WithMask(RetList, UnionMask, newElement)
                except Exception as ex:
                    print(ex)
                    #print(f"{type(ex).__name__} at line {ex.__traceback__.tb_lineno} of {__file__}: {ex}")

        return RetList

    def createListGenerationWithStartMembrane(self, max_count_PSD = 0, max_count_Axon = 0, max_count_Vesicles = 0, max_count_Mitohondrion = 0):
        if max_count_PSD > 0:
            count_PSD = np.random.randint(1, max_count_PSD+1)
        else:
            count_PSD = 0

        if max_count_Axon > 0:
            count_Axon = np.random.randint(1, max_count_Axon+1)
        else:
            count_Axon = 0

        if max_count_Vesicles > 0:
            count_Vesicles = np.random.randint(1, max_count_Vesicles+1)
        else:
            count_Vesicles = 0

        if max_count_Mitohondrion > 0:
            count_Mitohondrion = np.random.randint(1, max_count_Mitohondrion+1)
        else:
            count_Mitohondrion = 0

        RetList = []

        ListMixingClass = [["Axon"        , count_Axon],
                           ["Mitohondrion", count_Mitohondrion],
                           ["Vesicles"    , count_Vesicles],
                           ["PSD"         , count_PSD]]

        #################################################
        UnionMask = self.addNewElementIntoImage(RetList, Membrane(self.sizeImage))
        #################################################

        while len(ListMixingClass) != 0:
            index = np.random.randint(0, len(ListMixingClass))

            if ListMixingClass[index][1] <= 0:
                ListMixingClass.pop(index)
            else:
                ListMixingClass[index][1] -= 1

                if ListMixingClass[index][0] == "Axon":
                    newElement = Axon()
                elif ListMixingClass[index][0] == "Mitohondrion":
                    newElement = Mitohondrion()
                elif ListMixingClass[index][0] == "Vesicles":
                    newElement = Vesicles()
                elif ListMixingClass[index][0] == "PSD":
                    newElement = PSD()
                else:
                    raise Exception("What's up ?")

                UnionMask = self.addNewElementIntoImage(RetList, newElement)

        return RetList

    def fake_3_layers(self, ListGeneration, counter, dir_save, startIndex, size_overlap = 5):
        for i in range(-1, 2):
            print("i:", i)
            ListGenerationCopy = []
            if i != 0:
                for component in ListGeneration:
                    # создание единичного случайного вектора для смещения
                    x = np.random.random() * 2 - 1 # to -1:1
                    y = np.random.random() * 2 - 1 # to -1:1
                    len_direction = math.sqrt(x**2 + y**2)
                    direction = [x/len_direction, y/len_direction]

                    if component.type != "Membrane":
                        copy_component = component.copy()
                        copy_component.NewPosition(copy_component.centerPoint[0] + int(round(i * direction[0] * size_overlap)), copy_component.centerPoint[1] + int(round(i * direction[1] * size_overlap)))
                        ListGenerationCopy.append(copy_component)
                    else:
                        new_membrane = Membrane(self.sizeImage, ListGenerationCopy)
                        new_membrane.copy_main_param(component)
                        ListGenerationCopy.append(new_membrane)
            else:
                ListGenerationCopy = ListGeneration

            print(ListGenerationCopy[0].angle)

            fake_suffix = str(i+ 1)  # 0, 1, 2...

            draws_result = self.DrawsLayerAndMask(ListGenerationCopy)

            Img, MackPSD, MackAxon, MackMembrans, MackMito, MackMitoBoarder, MackVesicules = draws_result

            self.SaveGeneration(Img, MackPSD, MackAxon, MackMembrans, MackMito, MackMitoBoarder, MackVesicules, counter, dir_save, startIndex, fake_suffix)

    def DrawsLayerAndMask(self, ListComponents):
        # рисование слоя и фона к нему
        Img = np.zeros((*self.sizeImage, 3), np.uint8)
        Img = self.DrawBackround(Img, self.backgroundСolor)

        # рисование маски и заполнение черным
        MackAxon = np.zeros((*self.sizeImage, 3), np.uint8)

        # рисование маски и заполнение черным
        MackPSD = np.zeros((*self.sizeImage, 3), np.uint8)

        # рисование маски и заполнение черным
        MackMito = np.zeros((*self.sizeImage, 3), np.uint8)

        # рисование маски и заполнение черным
        MackMitoBoarder = np.zeros((*self.sizeImage, 3), np.uint8)

        # рисование маски и заполнение черным
        MackMembrans = np.zeros((*self.sizeImage, 3), np.uint8)

        # рисование маски и заполнение черным
        MackVesicules = np.zeros((*self.sizeImage, 3), np.uint8)

        # рисовка в соответствующее изображение
        for component in ListComponents:
            Img = component.DrawLayer(Img)

            if component.type == "PSD":
                MackPSD = component.DrawMask(MackPSD)

            elif component.type == "Axon":
                MackAxon = component.DrawMask(MackAxon)

            elif component.type == "Membrane":
                MackMembrans = component.DrawMask(MackMembrans)

            elif component.type == "Mitohondrion":
                MackMito = component.DrawMask(MackMito)
                MackMitoBoarder = component.DrawMaskBoarder(MackMitoBoarder)

            elif component.type ==  "Vesicles":
                MackVesicules = component.DrawMask(MackVesicules)

            elif component.type == "SpamComponents":
                pass
            else:
                print(f"ERROR: no type {component.type}")

        # добавление шума
        #Img = AddGaussianNoise(Img, 40)

        r = PARAM["main_radius_gausse_blur"]
        G = PARAM["main_sigma_gausse_blur"]
        Img = cv2.GaussianBlur(Img,(r*2+1,r*2+1), G)

        noisy = np.ones(self.sizeImage, np.uint8)
        noisy = np.random.poisson(noisy)*PARAM['pearson_noise'] - PARAM['pearson_noise']/2

        Img = Img + cv2.merge([noisy, noisy, noisy])
        Img[Img < 0] = 0
        Img[Img > 255] = 255
        Img = Img.astype(np.uint8)

        return Img, MackPSD, MackAxon, MackMembrans, MackMito, MackMitoBoarder, MackVesicules

    def SaveGeneration(self, Img, MackPSD, MackAxon, MackMembrans, MackMito, MackMitoBoarder, MackVesicules, counter, dir_save = None, startIndex = 0, suffix_name = ""):
        if dir_save is not None:
            # Сохранение слоя и масок
            if not os.path.isdir(dir_save):
                print(f"create dir_save: {dir_save}")
                os.mkdir(dir_save)

            if not os.path.isdir(os.path.join(dir_save, "original")):
                print(f"create original: {os.path.join(dir_save, 'original')}")
                os.mkdir(os.path.join(dir_save, "original"))

            if not os.path.isdir(os.path.join(dir_save, "PSD")):
                print(f"create PSD: {os.path.join(dir_save, 'PSD')}")
                os.mkdir(os.path.join(dir_save, "PSD"))

            if not os.path.isdir(os.path.join(dir_save, "axon")):
                print(f"create axon: {os.path.join(dir_save, 'axon')}")
                os.mkdir(os.path.join(dir_save, "axon"))

            if not os.path.isdir(os.path.join(dir_save, "boundaries")):
                print(f"create boundaries: {os.path.join(dir_save, 'boundaries')}")
                os.mkdir(os.path.join(dir_save, "boundaries"))

            if not os.path.isdir(os.path.join(dir_save, "mitochondria")):
                print(f"create mitochondria: {os.path.join(dir_save, 'mitochondria')}")
                os.mkdir(os.path.join(dir_save, "mitochondria"))

            if not os.path.isdir(os.path.join(dir_save, "mitochondrial_boundaries")):
                print(f"create mitochondrial_boundaries: {os.path.join(dir_save, 'mitochondrial_boundaries')}")
                os.mkdir(os.path.join(dir_save, "mitochondrial_boundaries"))

            if not os.path.isdir(os.path.join(dir_save, "vesicles")):
                print(f"create vesicles: {os.path.join(dir_save, 'vesicles')}")
                os.mkdir(os.path.join(dir_save, "vesicles"))

            date = datetime.datetime.now().strftime(r'%Y_%m_%d')
            name = str(counter + startIndex) + "_" + date

            if len(suffix_name) > 0:
                name += "_" + suffix_name

            # coхранение слоя
            cv2.imwrite(os.path.join(dir_save, "original", name + ".png"), cv2.cvtColor(Img, cv2.COLOR_RGB2GRAY))
            # coхранение маски
            cv2.imwrite(os.path.join(dir_save, "PSD", name + ".png"), cv2.cvtColor(MackPSD, cv2.COLOR_RGB2GRAY))
            # coхранение маски
            cv2.imwrite(os.path.join(dir_save, "axon", name + ".png"), cv2.cvtColor(MackAxon, cv2.COLOR_RGB2GRAY))
            # coхранение маски
            cv2.imwrite(os.path.join(dir_save, "boundaries", name + ".png"), cv2.cvtColor(MackMembrans, cv2.COLOR_RGB2GRAY))
            # coхранение маски
            cv2.imwrite(os.path.join(dir_save, "mitochondria", name + ".png"), cv2.cvtColor(MackMito, cv2.COLOR_RGB2GRAY))
            # coхранение маски
            cv2.imwrite(os.path.join(dir_save, "vesicles", name + ".png"), cv2.cvtColor(MackVesicules, cv2.COLOR_RGB2GRAY))
            # coхранение маски
            cv2.imwrite(os.path.join(dir_save, "mitochondrial_boundaries", name + ".png"), cv2.cvtColor(MackMitoBoarder, cv2.COLOR_RGB2GRAY))


    def StartGeneration(self, count_img = 100, count_PSD = 3, count_Axon = 1, count_Vesicles = 3, count_Mitohondrion = 3, dir_save = None, startIndex=0):
        # Цикличная генерация
        ArrLayers = []

        Noise = albu.Compose(albu.GaussNoise(var_limit = (PARAM['main_min_gausse_noise_value'], PARAM['main_max_gausse_noise_value']), per_channel = False, always_apply=True))

        for counter in range(count_img):
            print(f"{counter + 1} generation img for {count_img}")

            # создаю новый список для каждой генерации
            ListGeneration = self.createListGeneration(count_PSD, count_Axon, count_Vesicles, count_Mitohondrion, spam = 5)
            #ListGeneration = self.createListGenerationWithStartMembrane(count_PSD, count_Axon, count_Vesicles, count_Mitohondrion)

            color = uniform_int(
                PARAM['main_color_mean'],
                PARAM['main_color_std'])
            self.backgroundСolor = (color, color, color)

            # Рисование
            # рисование слоя и масок
            Img, MackPSD, MackAxon, MackMembrans, MackMito, MackMitoBoarder, MackVesicules = self.DrawsLayerAndMask(ListGeneration)

            ArrLayers.append([Img, MackPSD, MackAxon, MackMembrans, MackMito, MackMitoBoarder, MackVesicules])

            self.SaveGeneration(Img, MackPSD, MackAxon, MackMembrans, MackMito, MackMitoBoarder, MackVesicules, counter, dir_save, startIndex)

        return ArrLayers

    def StartFake3LayerGeneration(self, count_img = 100, count_PSD = 3, count_Axon = 1, count_Vesicles = 3, count_Mitohondrion = 3, dir_save = None, startIndex=0):
        # Цикличная генерация
        ArrLayers = []

        Noise = albu.Compose(albu.GaussNoise(var_limit = (PARAM['main_min_gausse_noise_value'], PARAM['main_max_gausse_noise_value']), per_channel = False, always_apply=True))

        for counter in range(count_img):
            print(f"{counter + 1} generation img for {count_img}")

            # создаю новый список для каждой генерации
            ListGeneration = self.createListGeneration(count_PSD, count_Axon, count_Vesicles, count_Mitohondrion)
            #ListGeneration = self.createListGenerationWithStartMembrane(count_PSD, count_Axon, count_Vesicles, count_Mitohondrion)

            color = uniform_int(
                PARAM['main_color_mean'],
                PARAM['main_color_std'])
            self.backgroundСolor = (color, color, color)

            self.fake_3_layers(ListGeneration, counter, dir_save, startIndex, 5)

        return ArrLayers
