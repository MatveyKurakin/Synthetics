if __name__ == "__main__":
    import sys
    sys.path.append('.')

from src.organells.PSD import *
from src.organells.vesicles import *
from src.organells.membrane import *


class Vesicles_and_PSD():
    def __init__(self):
        super().__init__()
        self.type = "Vesicles_and_PSD"

        self.centerPoint = [0, 0]
        self.angle = 0

        self.PSD = PSD(isVesiclesAndPSD=True)
        self.vesicles = Vesicles()
        
        # координаты относительно centerPoint
        self.PSD_pos = None
        self.vesicles_pos = None
        
        self.SetPosition()

    def SetPosition(self, turnPSD=False):
        # вернуть в горизонтальное положение, так как угол генерируется случайно
        # и повернуть на 180, чтобы след был в противоположной стороне от везикул
        self.PSD.setAngle(-self.PSD.angle + 180)
        self.PSD.angle = 0
        
        change_90 = np.random.randint(0, 2)
        self.vesicles.setAngle(-self.vesicles.angle + 90 * change_90)
        self.vesicles.angle = 90 * change_90
        
        ##################################################################################### переделать чтобы и полоска размытия PSD генерировалась в сторону от везикул и чтобы генерация мембран от PSD не пересекала везикулы.
        # полоска с размытием находится снизу
        self.PSD_pos = [0, -5]
        self.vesicles_pos = [0, 5]

        distance = np.random.randint(0, 10)
        if(change_90 == 1):
            distance += self.vesicles.width
        else:
            distance += self.vesicles.height

        # раздвигать пока не будет пересечения
        while True:
            mask_psd = np.zeros((256,256,3), np.uint8)
            mask_vesicles = np.zeros((256,256,3), np.uint8)
            
            self.PSD.NewPosition(self.PSD_pos[0]+128, self.PSD_pos[1]+128)
            self.vesicles.NewPosition(self.vesicles_pos[0]+128, self.vesicles_pos[1]+128)
            
            mask_psd = self.PSD.DrawMask(mask_psd)
            mask_vesicles = self.vesicles.DrawMask(mask_vesicles)
            
            if ((mask_psd&mask_vesicles).sum() == 0 and math.dist(self.PSD.PointsWithOffset[1], self.vesicles.centerPoint) >= distance):
                break
            else:
                self.PSD_pos[1] -= 1
                self.vesicles_pos[1] += 1

        # повернуть всю конструкцию
        self.setRandomAngle(0, 180)

    def __copy__(self):
        new_class = Vesicles_and_PSD()
        new_class.centerPoint = self.centerPoint.copy()
        new_class.angle = self.angle
        new_class.PSD = self.PSD.copy()
        new_class.vesicles = self.vesicles.copy()
        new_class.PSD_pos = self.PSD_pos.copy()
        new_class.vesicles_pos = self.vesicles_pos.copy()
        return new_class

    def copy(self):
        return self.__copy__()

    def DrawLayer(self, image):
        image = self.PSD.DrawLayer(image)
        image = self.vesicles.DrawLayer(image)
        return image
        
    def DrawUniqueArea(self, image, small_mode = False):
        image = self.PSD.DrawUniqueArea(image, small_mode)
        image = self.vesicles.DrawUniqueArea(image, small_mode)
        cv2.line(image, self.PSD.PointsWithOffset[1], self.vesicles.centerPoint, (255, 255, 255), 1)
        return image
        
    def DrawMask(self, image):
        image = self.PSD.DrawMask(image)
        image = self.vesicles.DrawMask(image)
        return image

    def setAngle(self, angle):
        change_angle = math.radians(angle)

        PSD_pos_x = int(round(self.PSD_pos[0] * math.cos(change_angle) - self.PSD_pos[1] * math.sin(change_angle)))
        PSD_pos_y = int(round(self.PSD_pos[0] * math.sin(change_angle) + self.PSD_pos[1] * math.cos(change_angle)))
        self.PSD_pos = (PSD_pos_x, PSD_pos_y)
        
        vesicles_pos_x = int(round(self.vesicles_pos[0] * math.cos(change_angle) - self.vesicles_pos[1] * math.sin(change_angle)))
        vesicles_pos_y = int(round(self.vesicles_pos[0] * math.sin(change_angle) + self.vesicles_pos[1] * math.cos(change_angle)))
        self.vesicles_pos = (vesicles_pos_x, vesicles_pos_y)

        self.ChangePositionPoints()
        self.PSD.setAngle(angle)
        self.vesicles.setAngle(angle)
        self.PSD.angle += angle
        self.vesicles.angle += angle
        

    def setRandomAngle(self, min_angle = 0, max_angle = 90, is_singned_change = True):

        if np.random.random() < 0.5 and is_singned_change:
            sign = -1
        else:
            sign = 1

        new_angle = (self.angle + np.random.randint(min_angle, max_angle+1) * sign) %360
        change_angle = (new_angle - self.angle)
        self.angle = new_angle

        self.setAngle(change_angle)

    def ChangePositionPoints(self):
        self.PSD.NewPosition(self.centerPoint[0] + self.PSD_pos[0], self.centerPoint[1] + self.PSD_pos[1])
        self.vesicles.NewPosition(self.centerPoint[0] + self.vesicles_pos[0], self.centerPoint[1] + self.vesicles_pos[1])

    def NewPosition(self, x, y):
        self.centerPoint[0] = x
        self.centerPoint[1] = y
        self.ChangePositionPoints()
        

def testUnion_PSD_ves(imgMembrane = False, imgVesEllipse = False):
    q = None

    print("1/2 Press button 'Q' or 'q' to exit")
    while q != ord('q') and q != ord("Q"):

        color = np.random.randint(182, 200)

        img = np.full((512,512,3), (color,color,color), np.uint8)

        for i in range(0, 512, 32):
            img[i:i+15,:,:] += 30

        union = Vesicles_and_PSD()

        union.NewPosition(256,256)

        #psd.setAngle(-psd.angle)

        print("centerPoint", union.centerPoint)
        print("centerPointPSD", union.PSD.centerPoint)
        print("centerPointVesicles", union.vesicles.centerPoint)
        
        print("angle", union.angle)
        print("anglePSD", union.PSD.angle)
        print("angleVesicles", union.vesicles.angle)

        print("widthVesicle", union.vesicles.width)
        print("heightVesicle", union.vesicles.height)

        img1 = union.DrawLayer(img)

        mask = np.zeros((512,512,3), np.uint8)

        tecnicalMask = np.zeros((512,512,3), np.uint8)

        mask = union.DrawMask(mask)
        img2 = union.DrawLayer(img)
        tecnicalMask = union.DrawUniqueArea(tecnicalMask)

        cv2.imshow("img", img1)
        cv2.imshow("mask", mask)
        cv2.imshow("img2", img2)
        cv2.imshow("tecnicalMask", tecnicalMask)

        if(imgVesEllipse):
            imgWithEllipse = np.copy(img1)
            psdCenter = union.PSD.centerPoint
            vesCenter = union.vesicles.centerPoint
            dir = [0, 0]
            dir[0] = psdCenter[0] - vesCenter[0]
            dir[1] = psdCenter[1] - vesCenter[1]
            dirNormal = math.sqrt(dir[0] * dir[0] + dir[1] * dir[1])
            dir[0] /= dirNormal
            dir[1] /= dirNormal
            a = union.vesicles.width
            b = union.vesicles.height
            vesAngle = (union.vesicles.angle) * math.pi / 180

            for theta in np.linspace(0, 2 * math.pi, 400):
                x = a * math.cos(theta)
                y = b * math.sin(theta)

                x_rot = x * math.sin(vesAngle) - y * math.cos(vesAngle)
                y_rot = y * math.sin(vesAngle) + x * math.cos(vesAngle)
                imgWithEllipse[int(round(x_rot + vesCenter[1])), int(round(y_rot + vesCenter[0]))] = 255

            cv2.imshow("imgWithEllipse", imgWithEllipse)

        if(imgMembrane):
            if(imgVesEllipse):
                imgWithMembrane = np.copy(imgWithEllipse)
            else:
                imgWithMembrane = np.copy(img1)
            membrane = Membrane((512, 512), [union])
            imgWithMembrane = membrane.Draw(imgWithMembrane)
            cv2.imshow("imgWithMembrane", imgWithMembrane)

        r = PARAM["main_radius_gausse_blur"]
        G = PARAM["main_sigma_gausse_blur"]
        Img = cv2.GaussianBlur(img1,(r*2+1,r*2+1), G)

        noisy = np.ones(img1.shape[:2], np.uint8)
        noisy = np.random.poisson(noisy)*PARAM['poisson_noise'] - PARAM['poisson_noise']/2

        Img = Img + cv2.merge([noisy, noisy, noisy])
        Img[Img < 0] = 0
        Img[Img > 255] = 255
        Img = Img.astype(np.uint8)

        cv2.imshow("add noise and blur", Img)

        q = cv2.waitKey()


if __name__ == "__main__":
    testUnion_PSD_ves()