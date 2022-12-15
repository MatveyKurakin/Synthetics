import numpy as np
import cv2

import math

if __name__ == "__main__":
    import sys
    sys.path.append('.')

from src.container.spline import *
from src.container.subclass import *
from settings import PARAM, uniform_float, uniform_int


class PSD:
    def __init__(self, TreePoints = None):
        self.type = "PSD"
        
        """
        
        генерация PSD в 3 линии
        
        u - верхняя
        i - внутрення
        d - нижняя
        
        форма по слоям:
         uuuuu
        u     u
         
         iiiii
        i     i
        
         ddddd
        d     d
        """
        
        color = uniform_int(
            PARAM['psd_back_color_mean'],
            PARAM['psd_back_color_std'])
        self.color = (color, color, color)

        addcolor = uniform_int(
            PARAM['psd_addcolor_mean'],
            PARAM['psd_addcolor_std'])
        self.addColor = (addcolor, addcolor, addcolor)
        
        centerline_color = uniform_int(
            PARAM['psd_centerline_color_mean'],
            PARAM['psd_centerline_color_std'])
        self.centerline_color = (centerline_color, centerline_color, centerline_color)
     
        # карандаш для темной линии PSD
        self.nowPen = Pen(self.color)
        # карандаш для центральной линии
        self.nowAddPen = Pen(self.centerline_color)
        # заливка для затемненоой области
        self.nowBrush = Brush(self.addColor)
        
        
        self.centerPoint = [0, 0]
        
        self.Points = []
        self.PointsWithOffset = []

        self.lenPSD = 0
        
        self.typeGen = 0       # 0 - with line, 1 - full fill PSD
        self.angle = 0
        
        if TreePoints is None:
            self.Create()
        else:
            self.CreateTreePoints(TreePoints)
        
    def Create(self):
        
        min_len_05 = 15
        max_len_05 = 30
            
        lenPSD_05 = np.random.randint(min_len_05, max_len_05 + 1)
        lenPSD = 2 * lenPSD_05
        normal_y = abs(np.random.normal(loc=0.0, scale=0.5)) * min_len_05//2
        
        # Coздание первой основной точки
        point1 = [-lenPSD_05,0]
        # Coздание точки на нормали        
        normal = [0, normal_y]
        # Coздание третьей основной точки
        point2 = [lenPSD_05,0]
        
        self.CreateTreePoints([point1, normal, point2])
        
        self.setRandomAngle(0,360)  
        
    def CreateTreePoints(self, TreePoints):        
        # в 1 из 10 случаев полностью черная, в 9/10 с полосой внутри
        if np.random.randint(0,10) == 0:
            self.typeGen = 1
            self.centerline_color = self.color
            self.nowAddPen.color = self.centerline_color
            
                        
            self.mainUpSizeLinePSD = 2
            self.inputSizeLinePSD = np.random.randint(2, 3+1)
            self.mainDownSizeLinePSD = 2
        else:
            self.typeGen = 0
            
            self.mainUpSizeLinePSD = np.random.randint(2, 4+1)
            self.inputSizeLinePSD = np.random.randint(1, 2+1)
            self.mainDownSizeLinePSD = 2
            
        point1 = TreePoints[0]
        normal = TreePoints[1]
        point2 = TreePoints[2]
            
        # приведение входных точек в горизонтальный вид и в начало координат, с запоминанием исходного местоположения
        
        # центр - точка между краями
        self.centerPoint = [(point1[0] + point2[0])//2, (point1[1] + point2[1])//2]
            
        self.lenPSD = math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2) 

        vec = [point2[0] - self.centerPoint[0], point2[1] - self.centerPoint[1]]
        vec = [2*vec[0]/self.lenPSD, 2*vec[1]/self.lenPSD]

        if vec[0] != 0:
            self.angle = math.atan(vec[1]/vec[0]) * 180 / math.pi
        else:
            self.angle = math.copysign(1, vec[1]) * 90
        normal_y = math.sqrt((self.centerPoint[0] - normal[0])**2 + (self.centerPoint[1] - normal[1])**2) 
               
        ########### 0-2 main-line (цвет PSD или цвет межкеточный)
        # Добавление первой основной точки
        self.Points.append([-self.lenPSD//2,0])       
        # Добавление точки на нормали
        self.Points.append([0, normal_y])
        # Добавление третьей основной точки
        self.Points.append([self.lenPSD//2,0])
        ############
        
        
        ########### 3-7 PSD-line (цвет PSD под выпоклустью)
        # смещение 1 дополнительной полосы в выпуклую(внешнюю) сторону (+ значение) и в внутренюю сторону (- значение)
        sizeOffsetY_1 = - (self.mainDownSizeLinePSD + self.inputSizeLinePSD)+1
        #главная темная линия PSD
        p1_1 = [self.Points[0][0], int(self.Points[0][1] + sizeOffsetY_1+1)]
        c_1  = [self.Points[1][0], int(self.Points[1][1] + sizeOffsetY_1)]
        p2_1 = [self.Points[2][0], int(self.Points[2][1] + sizeOffsetY_1+1)]
        
        self.Points.append(p1_1)
        self.Points.append(c_1)
        self.Points.append(p2_1)
        #############

        ########### 8-12 PSD-line (цвет PSD над выпоклустью)
        # смещение 2 дополнительной полосы в выпуклую(внешнюю) сторону (+ значение) и в внутренюю сторону (- значение)
        sizeOffsetY_2 = (self.mainUpSizeLinePSD + self.inputSizeLinePSD)
        #главная темная линия PSD
        p1_2 = [self.Points[0][0], int(self.Points[0][1] + sizeOffsetY_2-1)]
        c_2  = [self.Points[1][0], int(self.Points[1][1] + sizeOffsetY_2)]
        p2_2 = [self.Points[2][0], int(self.Points[2][1] + sizeOffsetY_2-1)]
        
        self.Points.append(p1_2)
        self.Points.append(c_2)
        self.Points.append(p2_2)
        
        # Отрисовка замкнутой области для затемнения
        sizeOffset = 10
        sizeOffset2 = 5
        self.Points.append(self.Points[3])
        self.Points.append(self.Points[4])
        self.Points.append(self.Points[5])
        self.Points.append([self.Points[8][0], int(self.Points[8][1] + sizeOffset2)])
        self.Points.append([self.Points[7][0], int(self.Points[7][1] + sizeOffset)])
        self.Points.append([self.Points[6][0] , int(self.Points[6][1] + sizeOffset2)])
        
        self.setRandomAngle(0,0)        
        
    def ChangePositionPoints(self):
        self.PointsWithOffset = []

        for point in self.Points:
            self.PointsWithOffset.append([self.centerPoint[0]+point[0], self.centerPoint[1]+point[1]])

    def setRandomAngle(self, min_angle = 0, max_angle = 90, is_singned_change = True):  
       
        if np.random.random() < 0.5 and is_singned_change:
            sign = -1
        else:
            sign = 1
            
        self.angle = (self.angle + np.random.randint(min_angle, max_angle+1) * sign) %360
        
        change_angle = self.angle * (math.pi/180)
        
        tPoints = []
        for point in self.Points:
            x = int(round(point[0] * math.cos(change_angle) - point[1] * math.sin(change_angle)))
            y = int(round(point[0] * math.sin(change_angle) + point[1] * math.cos(change_angle)))
            tPoints.append([x,y])
       
        self.Points = tPoints
        self.ChangePositionPoints()


    def setDrawParam(self):
        self.nowPen.color = self.color
        self.nowAddPen.color = self.centerline_color
        self.nowBrush.brush = self.addColor

    def setMaskParam(self):
        self.nowPen.color = (255,255,255)
        self.nowAddPen.color = (255,255,255)
        self.nowBrush.brush = (255,255,255)

    def NewPosition(self, x, y):
        self.centerPoint[0] = x
        self.centerPoint[1] = y

        self.ChangePositionPoints()

    def Draw(self, image, layer_drawing = True):
        # Основная рисующая фукция
        
        draw_image = image.copy()
        
        # основной алгоритм - нарисовать пятно, нарисовать линии PSD (над и под), нарисовать внутреннюю линию
        
        # пятно
        rangeList = self.PointsWithOffset[9:9+6]
        self.nowBrush.FullBrush(draw_image, rangeList)

        # рисование нижней линии 
        rangeList_up = self.PointsWithOffset[3: 3+3]
        small_spline_line(draw_image, rangeList_up, self.nowPen.color, self.mainDownSizeLinePSD)        
        # рисование верхней линии 
        rangeList_down = self.PointsWithOffset[6: 6+3]
        small_spline_line(draw_image, rangeList_down, self.nowPen.color, self.mainUpSizeLinePSD)
        
        # рисование внутренней линии
        rangeList_input = self.PointsWithOffset[0: 0+3]
        small_spline_line(draw_image, rangeList_input, self.nowAddPen.color, self.inputSizeLinePSD)


         
        return draw_image
            
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
        else:
            kernel = np.array([[0, 1, 0],
                               [1, 1, 1],
                               [0, 1, 0]], dtype=np.uint8)
            draw_image = cv2.dilate(draw_image,kernel,iterations = 2)

            #cv2.imshow("sdad", draw_image)
            #cv2.waitKey()
            
        ret_image = ret_image + draw_image
        ret_image[ret_image[:,:,:] > 255] = 255
        ret_image = ret_image.astype(np.uint8)
        
        return ret_image
        
    def DrawMask(self, image):
        #Смена цветов для рисования маски
        self.setMaskParam()
        mask = self.Draw(image, layer_drawing = False)
        self.setDrawParam()
        
        return mask 
     
def testPSD():
    q = None

    print("1/2 Press button 'Q' or 'q' to exit")
    while q != ord('q') and q != ord("Q"):
        
        color = np.random.randint(182, 200)
        
        img = np.full((512,512,3), (color,color,color), np.uint8)
        
        for i in range(0, 512, 32):
            img[i:i+15,:,:] += 30
        
        psd = PSD()
        
        psd.NewPosition(256,256)
        
        print("centerPoint", psd.centerPoint)
        print("Points", psd.Points)
        print("PointsWithOffset", psd.PointsWithOffset)
        
        print("typeGen", psd.typeGen)
        
        img1 = psd.Draw(img)
        
        mask = np.zeros((512,512,3), np.uint8)
        
        tecnicalMask = np.zeros((512,512,3), np.uint8)
        
        mask = psd.DrawMask(mask)
        img2 = psd.Draw(img)
        tecnicalMask = psd.DrawUniqueArea(tecnicalMask)
        
        cv2.imshow("img", img1)
        cv2.imshow("mask", mask)
        cv2.imshow("img2", img2)
        cv2.imshow("tecnicalMask", tecnicalMask)
        
        q = cv2.waitKey()

    q = None

    print("2/2 Press button 'Q' or 'q' to exit")
    while q != ord('q') and q != ord("Q"):
        
        color = np.random.randint(182, 200)
        
        img = np.full((512,512,3), (color,color,color), np.uint8)
        
        for i in range(0, 512, 32):
            img[i:i+15,:,:] += 30
        
        tree_gen_temp = [np.random.randint(128,384,2) for i in range(2)]
        center = [(tree_gen_temp[0][0] + tree_gen_temp[1][0])//2, (tree_gen_temp[0][1] + tree_gen_temp[1][1])//2]
        
        dir = (tree_gen_temp[0][0] - center[0], tree_gen_temp[0][1] - center[1])
        
        if (dir[0] == 0):
            normal_x = 1
            normal_y = 0
        else:
            normal_y = 1
            normal_x = -dir[1]/dir[0]
            
            len_normal = math.sqrt(normal_y + normal_x**2)
            
            normal_y /= len_normal
            normal_x /= len_normal
        
        size_change = np.random.randint(0,128)
        norm_point = [int(round(center[0] + normal_x * size_change)), int(round(center[1] + normal_y * size_change))]
        
        tree_gen = [tree_gen_temp[0], norm_point, tree_gen_temp[1]]
        
        print(tree_gen)
        psd = PSD(tree_gen)
                
        print("centerPoint", psd.centerPoint)
        print("Points", psd.Points)
        print("PointsWithOffset", psd.PointsWithOffset)
        
        print("typeGen", psd.typeGen)
        
        img1 = psd.Draw(img)
        
        for point in tree_gen:
            cv2.circle(img1, point, 3, (0, 0, 255), 2)
            
        cv2.circle(img1, center, 3, (0, 255, 0), 2)
            
            
        
        mask = np.zeros((512,512,3), np.uint8)
        
        tecnicalMask = np.zeros((512,512,3), np.uint8)
        
        mask = psd.DrawMask(mask)
        img2 = psd.Draw(img)
        tecnicalMask = psd.DrawUniqueArea(tecnicalMask)
        
        cv2.imshow("img", img1)
        cv2.imshow("mask", mask)
        cv2.imshow("img2", img2)
        cv2.imshow("tecnicalMask", tecnicalMask)
        
        q = cv2.waitKey()

if __name__ == "__main__":
    testPSD()

