import numpy as np
import cv2

from src.organells.axon import Axon, testAxon
from src.organells.PSD import PSD, testPSD
from src.organells.vesicles import Vesicles, testVesicles
from src.organells.mitohondrion import Mitohondrion, testMitohondrion
from src.organells.membrane import Membrane, testMembrane


from src.container.main_field import Form


#testAxon()
testPSD()
#testVesicles()
#testMitohondrion()
#testMembrane()



size_image = (256, 256)
forma = Form(size_image)

# количество элементов на изображении
max_count_PSD = 3
max_count_Axon = 1
max_count_Vesicles = 3
max_count_Mitohondrion = 3

number_generation = 100
ArrLayers = forma.StartGeneration(number_generation, max_count_PSD, max_count_Axon, max_count_Vesicles, max_count_Mitohondrion,\
                                  dir_save = "dataset/new/", startIndex = 0)
#ArrLayers = [[Img, MackPSD, MackAxon, MackMembrans, MackMito, MackMitoBoarder, MackVesicules], ...]


