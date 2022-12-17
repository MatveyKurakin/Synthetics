import numpy as np
import cv2
import os
import datetime
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
        count = 200
        # максимальная длина линий
        maxdist = np.random.randint(4, 40, 4)

        #  разбиваем область на 4 части в каждой будет свое направление линий
        xs = np.random.randint(0, self.sizeImage[0]/2, count)
        ys = np.random.randint(0, self.sizeImage[1]/2, count)

        xs[int(count/4):int(count/2)] = np.random.randint(int(self.sizeImage[0]/2), self.sizeImage[0], int(count/2)-int(count/4))
        xs[int(count*3/4):] = np.random.randint(int(self.sizeImage[0]/2), self.sizeImage[0], int(count/2)-int(count/4))
        ys[int(count/2):] = np.random.randint(int(self.sizeImage[1]/2), self.sizeImage[1], int(count/2))

        #  направление линий
        vecx = np.random.rand(4)
        vecy = np.random.rand(4)*2 - 1

        #  забиваем дистанцию у каждой четверти свой максимум
        #  забиваем направления
        xd = np.ones(count)
        yd = np.ones(count)
        dist = np.ones(count)*2
        j = 0
        for i in range(0, int(count/4)*4, int(count/4)):
            a = np.asarray([vecx[j], vecy[j]])
            a = a/np.sqrt(a.dot(a))
            xd[i:i+int(count/4)] = a[0]
            yd[i:i+int(count/4)] = a[1]
            dist[i:i+int(count/4)] = np.random.randint(3, maxdist[j], int(count/4))
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
            c = np.random.randint(100, 160)
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
        newComponent.NewPosition(np.random.randint(5, self.sizeImage[1]-5), np.random.randint(5, self.sizeImage[0] - 5))
        newComponent.setRandomAngle(0, 90)
        checkNewImage = newComponent.DrawUniqueArea(checkNewImage)

        counter = 1

        while self.CheckOverlapNewElement(checkImage, checkNewImage) and counter < max_iter:
            checkNewImage = np.zeros((*self.sizeImage, 3), np.uint8)
            newComponent.NewPosition(np.random.randint(5, self.sizeImage[1]-5), np.random.randint(5, self.sizeImage[0] - 5))
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
        newComponent.NewPosition(np.random.randint(5, self.sizeImage[1]-5), np.random.randint(5, self.sizeImage[0] - 5))
        newComponent.setRandomAngle(0, 90)
        checkNewImage = newComponent.DrawUniqueArea(checkNewImage)

        counter = 1

        while self.CheckOverlapNewElement(technicalMackAllcompanenst, checkNewImage) and counter < max_iter:
            checkNewImage = np.zeros((*self.sizeImage, 3), np.uint8)
            newComponent.NewPosition(np.random.randint(5, self.sizeImage[1]-5), np.random.randint(5, self.sizeImage[0] - 5))
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

    def createListGeneration(self, max_count_PSD = 0, max_count_Axon = 0, max_count_Vesicles = 0, max_count_Mitohondrion = 0):

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

    def StartGeneration(self, count_img = 100, count_PSD = 3, count_Axon = 1, count_Vesicles = 3, count_Mitohondrion = 3, dir_save = None, startIndex=0):
        # Цикличная генерация
        ArrLayers = []

        Noise = albu.Compose(albu.GaussNoise(var_limit = (PARAM['main_min_gausse_noise_value'], PARAM['main_max_gausse_noise_value']), per_channel = False, always_apply=True))

        for counter in range(count_img):
            print(f"{counter + 1} generation img for {count_img}")

            # создаю новый список для каждой генерации
            ListGeneration = self.createListGeneration(count_PSD, count_Axon, count_Vesicles, count_Mitohondrion)
            #ListGeneration = self.createListGenerationWithStartMembrane(count_PSD, count_Axon, count_Vesicles, count_Mitohondrion)


            # Рисование
            # рисование слоя и масок

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

            r = PARAM["main_radius_gausse_blur"]
            G = PARAM["main_sigma_gausse_blur"]
            Img = cv2.GaussianBlur(Img,(r*2+1,r*2+1), G)

            noisy = np.ones((*self.sizeImage, 3), np.uint8)
            noisy = np.random.poisson(noisy)*PARAM['pearson_noise'] - PARAM['pearson_noise']/2

            Img = Img + noisy
            Img[Img < 0] = 0
            Img[Img > 255] = 255
            Img = Img.astype(np.uint8)

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
                name = str(counter + startIndex) + "_" + date
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
