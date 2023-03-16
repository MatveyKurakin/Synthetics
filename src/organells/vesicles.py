import numpy as np
import cv2

import math

if __name__ == "__main__":
    import sys
    sys.path.append('.')

from src.organells.location import *
from src.container.spline import *
from src.container.subclass import *
from settings import PARAM, DEBUG_MODE, uniform_int

class Vesicles(Location):
    def __init__(self):
        super().__init__()
        self.type = "Vesicles"

        self.sizeVesiculeMin = 5
        self.sizeVesiculeMax = 7

        self.listSizeVesiculs = []

        color = uniform_int(
            PARAM['vesicles_shell_color_mean'],
            PARAM['vesicles_shell_color_std'])
        self.color = (color, color, color) #/// подобрать цвета          
        self.nowPen = Pen(self.color, PARAM['vesicles_border_w'])
        backcolor = uniform_int(
            PARAM['vesicles_back_color_mean'],
            PARAM['vesicles_back_color_std'])
        self.addColor = (backcolor, backcolor, backcolor)

        self.nowBrush = Brush(self.addColor)

        self.varibleInputFilling = 0

        # 0 - normal mode, 1 - many small vesicles
        self.typeGen = 0            

        self.Create()

    def __copy__(self):
        new_vesic = Vesicles()

        new_vesic.sizeVesiculeMin = self.sizeVesiculeMin
        new_vesic.sizeVesiculeMax = self.sizeVesiculeMax
        new_vesic.listSizeVesiculs = self.listSizeVesiculs

        new_vesic.color = self.color
        new_vesic.nowPen  = self.nowPen.copy()
        new_vesic.addColor = self.addColor

        new_vesic.typeGen = self.typeGen
        new_vesic.varibleInputFilling = self.varibleInputFilling

        # copy location data
        new_vesic.centerPoint = self.centerPoint.copy()
        new_vesic.Points = self.Points.copy()
        new_vesic.angle = self.angle
        new_vesic.numberPoints = self.numberPoints

        new_vesic.setDrawParam()
        new_vesic.setRandomAngle(0,0)
        return new_vesic

    def copy(self):
        return self.__copy__()

    def Create(self):

        self.typeGen = np.random.randint(0, 2)

        if self.typeGen == 0:
            mainVesiculesSize = np.random.randint(5, 7)
        else:
            mainVesiculesSize = 4
            #не более 0.1 полностью заполненных, так как получается единое месиво
            self.varibleInputFilling = np.random.random() * 0.1                            

        self.sizeVesiculeMin = mainVesiculesSize - 1
        self.sizeVesiculeMax = mainVesiculesSize + 2

        # radiuses of vesicules area (ellipse)
        radius_x = np.random.randint(30, 96)
        radius_y = np.random.randint(30, 96)

        square = radius_y * radius_x

        sqrt_int_square = int(round(square / mainVesiculesSize**2))

        if self.typeGen == 0:
            self.numberPoints = np.random.randint(sqrt_int_square//4, sqrt_int_square//3+1)
        else:
            self.numberPoints = np.random.randint(2*sqrt_int_square//9, sqrt_int_square//2+1)

        MAX_ITERATION = 2000

        fail_counter = 0

        tPoints = []

        for i in range(self.numberPoints):
            counter = 0
            while True:
                now_point = self.getNewCoordVesicules(radius_x, radius_y)
                nowSizeCycle = np.random.randint(self.sizeVesiculeMin, self.sizeVesiculeMax)
                counter += 1
                
                if not self.CheckOverlap(tPoints, now_point, nowSizeCycle, 1):
                    # if we found the place for new vesicula 
                    self.listSizeVesiculs.append(nowSizeCycle)
                    tPoints.append(now_point)
                    break
                
                if counter >= MAX_ITERATION:
                    fail_counter += 1
                    break

        # поворот области везикул
        self.angle = np.random.randint(0, 90)

        angle = self.angle * (math.pi/180)

        #print(self.numberPoints, half_len, len(tPoints))
        for point in tPoints:
            x = int(round(point[0] * math.cos(angle) - point[1] * math.sin(angle)))
            y = int(round(point[0] * math.sin(angle) + point[1] * math.cos(angle)))
            self.Points.append([x,y])

        if DEBUG_MODE:
            if (fail_counter != 0):
                print(f"The number of vesicles that could not be generated at a unique position: {fail_counter} out of {self.numberPoints}")

        self.numberPoints = len(self.Points)

        self.ChangePositionPoints()


    def getNewCoordVesicules(self, radius_x, radius_y):

        #if self.typeForm == -1:
        #    now_point =  [np.random.randint(min_max_r_x[0], min_max_r_x[1]), np.random.randint(min_max_r_y[0], min_max_r_y[1])]

        #else:

        ## генерация эллипсом
        stop_gen = False
        while stop_gen == False:
            #x = np.random.randint(-radius_x, radius_x+1)
            #y = np.random.randint(-radius_y, radius_y+1)
            x, y = np.random.normal(loc=0.0, scale=0.2, size=2)

            x = int(round(x * radius_x))
            y = int(round(y * radius_y))

            if ((x**2) / (radius_x**2) + (y**2) / (radius_y**2)) <= 1:
                stop_gen = True
        now_point = [x,y]


        return now_point

    def CheckOverlap(self, Points, point, sizeVesicule, proportion):
        '''
        

        Parameters
        ----------
        Points : TYPE
            DESCRIPTION.
        point : TYPE
            DESCRIPTION.
        sizeVesicule : TYPE
            DESCRIPTION.
        proportion : TYPE
            DESCRIPTION.

        Returns
        -------
        bool
            True if new vesicula overlap old vesicules. False otherwise.

        '''
        for i in range(len(Points)):

            x_delt = abs(Points[i][0] - point[0])
            y_delt = abs(Points[i][1] - point[1])

            len_new_now = math.sqrt(x_delt**2 + y_delt**2)

            if len_new_now < self.listSizeVesiculs[i] + sizeVesicule + self.nowPen.sizePen + proportion:
                return True

        return False

    def Draw(self, image, small_mask_mode = False):
        # Основная рисующая фукция
        
        if small_mask_mode:
            minus_ves_size = 2
        else:
            minus_ves_size = 0

        draw_image = image.copy()

        for i in range(self.numberPoints):
        
            size_vesicule = self.listSizeVesiculs[i] - minus_ves_size

            if self.typeGen == 0:
                self.nowBrush.FullBrushEllipse(draw_image, self.PointsWithOffset[i], (self.listSizeVesiculs[i], self.listSizeVesiculs[i]))
            else:
                if np.random.random() < self.varibleInputFilling:
                    Brush(self.nowPen.color).FullBrushEllipse(draw_image, self.PointsWithOffset[i], (self.listSizeVesiculs[i], self.listSizeVesiculs[i]))
                else:
                    self.nowBrush.FullBrushEllipse(draw_image, self.PointsWithOffset[i], (self.listSizeVesiculs[i], self.listSizeVesiculs[i]))


            cv2.ellipse(img = draw_image,
                       center = self.PointsWithOffset[i],
                       axes = (size_vesicule, size_vesicule),
                       color = self.nowPen.color,
                       thickness = self.nowPen.sizePen + self.listSizeVesiculs[i] - self.sizeVesiculeMin,
                       angle = 0,
                       startAngle = 0,
                       endAngle = 360)

        return draw_image

    def DrawLayer(self, image):
        return self.Draw(image)

    def setDrawParam(self):
        self.nowPen.color = self.color
        self.nowBrush.brush = self.addColor

    def setMaskParam(self):
        self.nowPen.color = (255,255,255)
        self.nowBrush.brush = (255,255,255)

    def DrawMask(self, image):
        #Смена цветов для рисования маски
        self.setMaskParam()
        mask = self.Draw(image, small_mask_mode = True)
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

        print(vesicles.typeGen)
        if vesicles.typeGen==1:
           print(vesicles.varibleInputFilling)

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
