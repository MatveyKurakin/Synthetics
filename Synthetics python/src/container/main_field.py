import numpy as np
import cv2
import os
import datetime
import math
from settings import PARAM, uniform_int
import skimage
import random

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

from src.container.output import SaveGeneration

from src.container.noises import PointsNoise, SpamComponents

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

    def AddNewElementWithoutOverlapWithMask(self, technicalMackAllcompanenst, newComponent):
        # максимальное количество попыток добавить
        max_iter = 300

        # small items should be not near the edge
        if newComponent.type == "PSD":
            step_from_edge = 32
        else:
            step_from_edge = 5

        # рисование маски нового элемента (первая попытка). Выбирается позиция, угол и рисуется.
        counter = 1
        checkNewImage = np.zeros((*self.sizeImage, 3), np.uint8)
        newComponent.NewPosition(np.random.randint(step_from_edge, self.sizeImage[1]-step_from_edge), np.random.randint(step_from_edge, self.sizeImage[0] - step_from_edge))
        newComponent.setRandomAngle(0, 90)
        checkNewImage = newComponent.DrawUniqueArea(checkNewImage)

        while self.CheckOverlapNewElement(technicalMackAllcompanenst, checkNewImage) and counter < max_iter:
            checkNewImage = np.zeros((*self.sizeImage, 3), np.uint8)
            newComponent.NewPosition(np.random.randint(step_from_edge, self.sizeImage[1]-step_from_edge), np.random.randint(step_from_edge, self.sizeImage[0] - step_from_edge))
            newComponent.setRandomAngle(0, 90)
            checkNewImage = newComponent.DrawUniqueArea(checkNewImage)

            counter += 1

        # Добавлено исключение чтобы элементы не накладывались друг на друга
        if counter == max_iter:
            raise Exception("Can't add unique position new element")

    def addNewElementIntoImage(self, compartmentsList, newComponent, technicalMackAllcompanenst = None):
        # защита от дурака)
        if newComponent is not None:
            # иключение на случай если не получилось добавить без пересечения или что-то пошло не так при попытке рисования масок
            try:
                # если не дали тех.маску текущих компонентов, то сделаем из списка компонентов
                if technicalMackAllcompanenst is None:
                    checkImage = np.zeros((*self.sizeImage, 3), np.uint8)
                    for component in compartmentsList:
                        checkImage = component.DrawUniqueArea(checkImage)

                # иначе используем тех.маску
                else:
                    checkImage = technicalMackAllcompanenst

                # нет смысла проверять мембраны, так как они касаются PSD и будет перекрытие
                if newComponent.type != "Membrane":
                    self.AddNewElementWithoutOverlapWithMask(checkImage, newComponent);

                compartmentsList.append(newComponent)
                checkImage = newComponent.DrawUniqueArea(checkImage) # рисуется новый элемент на тех.маску
                newComponent = None

                return checkImage

            except Exception as ex:
                print(ex)
                #print(f"{type(ex).__name__} at line {ex.__traceback__.tb_lineno} of {__file__}: {ex}")

        return technicalMackAllcompanenst

    def DrawBackround(self, img, color):
        draw_image = np.full(img.shape, color, np.uint8)

        p = PointsNoise(self.sizeImage)
        draw_image = p.Draw(draw_image)

        return draw_image
    
    def get_count(self, max_count):
        return np.random.randint(1, max_count + 1) if max_count > 0 else 0
    
    class_constructors = {
        "Axon": Axon,
        "Mitohondrion": Mitohondrion,
        "Vesicles": Vesicles,
        "PSD": PSD,
    }
    
    def generate_lists(self, element_dict, split = True):
        '''
        Generate list or lists of compartment which will be used as order to adding 
        this compartment into layer

        Parameters
        ----------
        element_dict : dictionary
            key: compartment type as string
            value: number of compartment in layer.
        split : bool
            Need we 2 lists or one. The default is True.

        Returns
        -------
        list
            List of lists of compartment order.
            For example: [["PSD","Axon", "PSD", "Mitohondrion", "Vesicles"], ["Mitohondrion", "Vesicles"]]
            "PSD" can be only in the first list

        '''
        if split:
            element_dict1 = {}
            element_dict2 = {}
            for key in element_dict:
                if key != "PSD":
                    element_dict1[key] = np.random.randint(0, element_dict[key] + 1)
                    element_dict2[key] = element_dict[key] - element_dict1[key]
            element_dict1["PSD"] = element_dict["PSD"]
             
            element_list1 = []
            for key in element_dict1:
                element_list1.extend([key] * element_dict1[key]) 
            element_list2 = []
            for key in element_dict2:
                element_list1.extend([key] * element_dict2[key]) 
            random.shuffle(element_list1)    
            random.shuffle(element_list2)    
            return [element_list1, element_list2]
        else:
            element_list = []
            for key in element_dict:
                element_list.extend([key] * element_dict[key])
            random.shuffle(element_list)  
            return [element_list]

    def createListGeneration(self, max_count_PSD = 0, max_count_Axon = 0, max_count_Vesicles = 0, max_count_Mitohondrion = 0):
        RetList = []
        
        count_PSD = self.get_count(max_count_PSD)
        count_Axon = self.get_count(max_count_Axon)
        count_Vesicles = self.get_count(max_count_Vesicles)
        count_Mitohondrion = self.get_count(max_count_Mitohondrion)  

        element_dict = {"Axon": count_Axon, "Mitohondrion" : count_Mitohondrion, 
                        "Vesicles": count_Vesicles, "PSD" : count_PSD}
        
        element_list = self.generate_lists(element_dict)

        # тех.маска уже добавленных элементов
        UnionMask = np.zeros((*self.sizeImage,3), np.uint8)
        
        # защита на случай если несуществует класса element
        try:
            # добавление элементов перед добавлением мембран
            for element in element_list[0]:
               if element in self.class_constructors:
                   newElement = self.class_constructors[element]()
                   UnionMask = self.addNewElementIntoImage(RetList, newElement, UnionMask)
               else:
                   raise Exception("No such class exist: " + element)
            
            #cv2.imshow("testMask", UnionMask)
            #cv2.waitKey()
            # DRAW MEMBRANES
            UnionMask = self.addNewElementIntoImage(RetList, Membrane(self.sizeImage, RetList), UnionMask)
    
            # добавление элементов после добавления мембран для более плотного расположения
            for element in element_list[1]:
               if element in self.class_constructors:
                   newElement = self.class_constructors[element]()
                   UnionMask = self.addNewElementIntoImage(RetList, newElement, UnionMask)
               else:
                   print("No such class exist: " + element)
                   raise Exception("No such class exist: " + element)
        except Exception as ex:
            print(ex)
            
        return RetList

    def createListGenerationWithStartMembrane(self, max_count_PSD = 0, max_count_Axon = 0, max_count_Vesicles = 0, max_count_Mitohondrion = 0):
        
        RetList = []
        
        count_PSD = self.get_count(max_count_PSD)
        count_Axon = self.get_count(max_count_Axon)
        count_Vesicles = self.get_count(max_count_Vesicles)
        count_Mitohondrion = self.get_count(max_count_Mitohondrion)  

        element_dict = {"Axon": count_Axon, "Mitohondrion" : count_Mitohondrion, 
                         "Vesicles": count_Vesicles, "PSD" : count_PSD}
         
        element_list = self.generate_lists(element_dict, False)

        # DRAW MEMBRANES
        UnionMask = self.addNewElementIntoImage(RetList, Membrane(self.sizeImage))

        try:
            for element in element_list[0]:
                if element in self.class_constructors:
                    newElement = self.class_constructors[element]()
                    UnionMask = self.addNewElementIntoImage(RetList, newElement)
                else:
                    raise Exception("No such class exist: " + element)
        except Exception as ex:
            print(ex)
            
        return RetList

    def fake_3_layers(self, ListGeneration, counter, dir_save, startIndex, size_overlap = 5):

        # список для хранения списков компонетнов предыдущего, текущего и следующего слоёв
        # нужен для того, чтобы 1 и тот же компонент был сдвинут по прямой
        ListListGeneration = []
        for i in range(-1, 2):
            ListListGeneration.append([])

        for k, component in enumerate(ListGeneration):
            # создание единичного случайного вектора для смещения
            x = np.random.random() * 2 - 1 # to -1:1
            y = np.random.random() * 2 - 1 # to -1:1
            len_direction = math.sqrt(x**2 + y**2)
            direction = [x/len_direction, y/len_direction]

            for index, i in enumerate(range(-1, 2)): # 1-индексация по массиву, 2-взвешанное направление по прямой
                if component.type != "Membrane":
                    copy_component = component.copy()
                    copy_component.NewPosition(component.centerPoint[0] + int(round(i * direction[0] * size_overlap)), component.centerPoint[1] + int(round(i * direction[1] * size_overlap)))
                    ListListGeneration[index].append(copy_component)
                else:
                    new_membrane = Membrane(self.sizeImage, ListListGeneration[index].copy())
                    new_membrane.copy_main_param(component)
                    ListListGeneration[index].append(new_membrane)

        for j, ListGenerationCopy in enumerate(ListListGeneration):
            fake_suffix = str(j)  # 0, 1, 2...

            draws_result = self.DrawsLayerAndMask(ListGenerationCopy)

            Img, MackPSD, MackAxon, MackMembrans, MackMito, MackMitoBoarder, MackVesicules = draws_result

            SaveGeneration(Img, MackPSD, MackAxon, MackMembrans, MackMito, MackMitoBoarder, MackVesicules, counter, dir_save, startIndex, fake_suffix)

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




    def StartGeneration(self, count_img = 100, count_PSD = 3, count_Axon = 1, count_Vesicles = 3, count_Mitohondrion = 3, dir_save = None, startIndex=0):
        # Цикличная генерация
        ArrLayers = []

        Noise = albu.Compose(albu.GaussNoise(var_limit = (PARAM['main_min_gausse_noise_value'], PARAM['main_max_gausse_noise_value']), per_channel = False, always_apply=True))

        for counter in range(count_img):
            print(f"{counter + 1} generation img for {count_img}")

            # создаю новый список для каждой генерации
            ListGeneration = self.createListGeneration(count_PSD, count_Axon, count_Vesicles, count_Mitohondrion, spam = 5)
            print(ListGeneration)

            color = uniform_int(
                PARAM['main_color_mean'],
                PARAM['main_color_std'])
            self.backgroundСolor = (color, color, color)

            # Рисование
            # рисование слоя и масок
          #  Img, MackPSD, MackAxon, MackMembrans, MackMito, MackMitoBoarder, MackVesicules = self.DrawsLayerAndMask(ListGeneration)

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
            for component in ListGeneration:
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
            
            # Img = cv2.blur(Img,(3,3))

            noisy = np.ones((*self.sizeImage, 3), np.uint8)
            noisy = np.random.poisson(noisy)*PARAM['poisson_noise'] - PARAM['poisson_noise']
            noisy = cv2.blur(noisy,(5,5))
            noisy2 = np.random.poisson(np.ones((*self.sizeImage, 3), np.uint8))*PARAM['poisson_noise'] - PARAM['poisson_noise']
            noisy = noisy + noisy2

            Img = Img + noisy
            Img[Img < 0] = 0
            Img[Img > 255] = 255
            Img = Img.astype(np.uint8)

            ArrLayers.append([Img, MackPSD, MackAxon, MackMembrans, MackMito, MackMitoBoarder, MackVesicules])

            SaveGeneration(Img, MackPSD, MackAxon, MackMembrans, MackMito, MackMitoBoarder, MackVesicules, counter, dir_save, startIndex)

        return ArrLayers

    def StartFake3LayerGeneration(self, count_img = 100, count_PSD = 3, count_Axon = 1, count_Vesicles = 3, count_Mitohondrion = 3, dir_save = None, startIndex=0):
        # Цикличная генерация
        ArrLayers = []

        Noise = albu.Compose(albu.GaussNoise(var_limit = (PARAM['main_min_gausse_noise_value'], PARAM['main_max_gausse_noise_value']), per_channel = False, always_apply=True))

        for counter in range(count_img):
            print(f"{counter + 1} generation img for {count_img}")

            # создаю новый список для каждой генерации
            ListGeneration = self.createListGeneration(count_PSD, count_Axon, count_Vesicles, count_Mitohondrion)

            color = uniform_int(
                PARAM['main_color_mean'],
                PARAM['main_color_std'])
            self.backgroundСolor = (color, color, color)

            self.fake_3_layers(ListGeneration, counter, dir_save, startIndex, 5)

        return ArrLayers
