import numpy as np
import cv2

from src.organells.axon import Axon, testAxon
from src.organells.PSD import PSD, testPSD
from src.organells.vesicles import Vesicles, testVesicles
from src.organells.mitohondrion import Mitohondrion, testMitohondrion

from src.container.main_field import Form


#testAxon()
#testPSD()
#testVesicles()
#testMitohondrion()

size_image = (256, 256)
forma = Form(size_image)

# количество элементов на изображении
count_PSD = 3
count_Axon = 1
count_Vesicles = 3
count_Mitohondrion = 2

number_generation = 1000
ArrLayers = forma.StartGeneration(number_generation, count_PSD, count_Axon, count_Vesicles, count_Mitohondrion,\
                                  dir_save = "small_Sintetic_generation_dataset test boarder/", startIndex = 2000)
#ArrLayers = [[Img, MackPSD, MackAxon, MackMembrans, MackMito, MackMitoBoarder, MackVesicules], ...]


