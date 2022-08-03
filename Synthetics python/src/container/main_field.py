import numpy as np
import cv2
import os
import datetime


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
        self.Points = []
        self.PointsWithOffset = []
        self.sizeImage = size

    def Create(self, min_r_st = -20, max_r_st = 20):
        min_r = np.random.randint(min_r_st, 0)
        max_r = np.random.randint(0, max_r_st)

        for i in range(2):
            rx = np.random.randint(min_r, max_r)
            ry = np.random.randint(min_r, max_r)
            now_point = [rx, ry]
            self.Points.append(now_point)
            
    def  ChangePositionPoints(self):
        self.PointsWithOffset = []
        
        for i in range(0, len(self.Points), 2):
            x = np.random.randint(0, self.sizeImage[0])
            y = np.random.randint(0, self.sizeImage[1])
            
            self.PointsWithOffset.append([self.Points[i][0] + x, self.Points[i][1] + y])
            self.PointsWithOffset.append([self.Points[i + 1][0] + x, self.Points[i + 1][1] + y])

    def Draw(self, image):
        draw_image = image.copy()
    
        for i in range(500):
            self.Create()
        self.ChangePositionPoints()

        for i in range(0, len(self.PointsWithOffset), 2):
            c = np.random.randint(100, 159)
            w = np.random.randint(1, 10)
            
            draw_image = cv2.line(draw_image, self.PointsWithOffset[i],  self.PointsWithOffset[i+1], (c,c,c), w)
            
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

class Form:
    def __init__(self, size = (512, 512)):
        color = np.random.randint(175, 186)                        # выбор цвета фона
        self.backgroundСolor = (color, color, color)
        
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

        max_iter = 200
                
        checkNewImage = np.zeros((*self.sizeImage, 3), np.uint8)
        newComponent.NewPosition(np.random.randint(5, self.sizeImage[1]-5), np.random.randint(5, self.sizeImage[0] - 5))
        checkNewImage = newComponent.DrawUniqueArea(checkNewImage)

        counter = 1
        
        while self.CheckOverlapNewElement(checkImage, checkNewImage) and counter < max_iter:
            checkNewImage = np.zeros((*self.sizeImage, 3), np.uint8)
            newComponent.NewPosition(np.random.randint(5, self.sizeImage[1]-5), np.random.randint(5, self.sizeImage[0] - 5))
            checkNewImage = newComponent.DrawUniqueArea(checkNewImage)

            counter += 1
            
        # Добавлено исключение чтобы элементы не накладывались друг на друга
        if counter == max_iter:
            raise Exception("Can't add unique position new element")
            
    def AddNewElementWithoutOverlap_WithMask(self, technicalMackAllcompanenst, newComponent):
        max_iter = 200
                
        checkNewImage = np.zeros((*self.sizeImage, 3), np.uint8)
        newComponent.NewPosition(np.random.randint(5, self.sizeImage[1]-5), np.random.randint(5, self.sizeImage[0] - 5))
        checkNewImage = newComponent.DrawUniqueArea(checkNewImage)

        counter = 1
        
        while self.CheckOverlapNewElement(technicalMackAllcompanenst, checkNewImage) and counter < max_iter:
            checkNewImage = np.zeros((*self.sizeImage, 3), np.uint8)
            newComponent.NewPosition(np.random.randint(5, self.sizeImage[1]-5), np.random.randint(5, self.sizeImage[0] - 5))
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
 
        return technicalMackAllcompanenst

    def DrawBackround(self, img, color):
        draw_image = np.full(img.shape, color, np.uint8)
        
        p = PointsNoise(self.sizeImage)
        draw_image = p.Draw(draw_image)
            
        r = 7
        G = (2 * r + 1) / 3
        draw_image = cv2.GaussianBlur(draw_image,(r*2+1,r*2+1), G)

        return draw_image
        
    def createListGeneration(self, count_PSD = 0, count_Axon = 0, count_Vesicles = 0, count_Mitohondrion = 0):
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
                    raise Exception("Shlyapa")
                    
                UnionMask = self.addNewElementIntoImage(RetList, newElement)

        #################################################
        UnionMask = self.addNewElementIntoImage(RetList, Membrane(RetList, self.sizeImage))
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
                        raise Exception("Shlyapa")

                    self.addNewElementIntoImage(RetList, newElement)
                except Exception as ex:
                    print(ex)
        
        return RetList
        
    def createListGenerationWithMask(self, count_PSD = 0, count_Axon = 0, count_Vesicles = 0, count_Mitohondrion = 0):
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
                    raise Exception("Shlyapa")
                    
                UnionMask = self.addNewElementIntoImage_WithMask(RetList, UnionMask, newElement)

        #cv2.imshow("testMask", UnionMask)
        #cv2.waitKey()
        #################################################
        UnionMask = self.addNewElementIntoImage_WithMask(RetList, UnionMask, Membrane(RetList, self.sizeImage))
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
                        raise Exception("Shlyapa")

                    UnionMask = self.addNewElementIntoImage_WithMask(RetList, UnionMask, newElement)
                except Exception as ex:
                    print(ex)
        
        return RetList

    def StartGeneration(self, count_img = 100, count_PSD = 3, count_Axon = 1, count_Vesicles = 3, count_Mitohondrion = 3, dir_save = None):
        # Цикличная генерация
        ArrLayers = []

        Noise = albu.Compose(albu.GaussNoise(var_limit = (10,25), per_channel = False, always_apply=True))

        for counter in range(count_img):
            print(f"{counter + 1} generation img for {count_img}")

            # создаю новый список для каждой генерации
            ListGeneration = self.createListGeneration(count_PSD, count_Axon, count_Vesicles, count_Mitohondrion)
            
            # Рисование
            # рисование слоя и масок

            # рисование слоя и фона к нему
            Img = np.zeros((*self.sizeImage, 3), np.uint8)
            Img = self.DrawBackround(Img, self.backgroundСolor)
            
            # рисование маски и заплолнение черным
            MackAxon = np.zeros((*self.sizeImage, 3), np.uint8)

            # рисование маски и заплолнение черным
            MackPSD = np.zeros((*self.sizeImage, 3), np.uint8)

            # рисование маски и заплолнение черным
            MackMito = np.zeros((*self.sizeImage, 3), np.uint8)

            # рисование маски и заплолнение черным
            MackMitoBoarder = np.zeros((*self.sizeImage, 3), np.uint8)

            # рисование маски и заплолнение черным
            MackMembrans = np.zeros((*self.sizeImage, 3), np.uint8)

            # рисование маски и заплолнение черным
            MackVesicules = np.zeros((*self.sizeImage, 3), np.uint8)

            # рисовка в соответсвующее изображение
            for component in ListGeneration:
                Img = component.Draw(Img)

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

                else:
                    print(f"ERROR: no type {component.type}")

            # добавление шума
            #Img = AddGaussianNoise(Img, 40)

            r = 6
            G = 2
            Img = cv2.GaussianBlur(Img,(r*2+1,r*2+1), G)

            Img = Noise(image=Img)['image']

            ArrLayers.append([Img, MackPSD, MackAxon, MackMembrans, MackMito, MackMitoBoarder, MackVesicules])

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
                name = str(counter) + "_" + date
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
            
        return ArrLayers
        