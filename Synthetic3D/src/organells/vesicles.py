from copy import deepcopy

import cv2

from Synthetic3D.src.hard.draw_triangle import draw_voxel_triangle

from default_structure import create_octahedron_with_main_point

from organell import Organell


class Vesicle(Organell):
    def __init__(self):
        super().__init__()
        self.comment = "Default one vesicle"

        self.CreateAlone()

    def Create(self):
        pass

    def CreateAlone(self):
        self.frame.points_list.append((0, 0, 0))

        v,e,p = create_octahedron_with_main_point(self.frame.points_list[0], 30, 60, 50)

        self.shell.vertex_list = v
        self.shell.edge_list = e
        self.shell.poligon_list = p

        self.__CalculateViewData()


    # Первая фунция пересчета с нуля №№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№
    def __CalculateViewData(self):
        # if self.view_poligon is None:
        self.view_shell = deepcopy(self.shell)
        self.Rotate(self.angle)
        self.ChangePosition(self.position)
        self.Partition_of_triangles(2)

    def ChangePosition(self, delta_position):
        for vertex in self.view_shell.vertex_list:
            vertex.vertex += delta_position
        self.position = np.array(self.position) + delta_position
    def Rotate(self, delta_angle):
        pass  # реализация функции поворота

    def Draw(self, data):
        for triangle in self.view_shell.poligon_list:
            v1, v2, v3 = triangle.get_vertices(self.view_shell.vertex_list)
            draw_voxel_triangle(data, v1.vertex, v2.vertex, v3.vertex, self.view_data.color, self.view_data.thickness)


class Vesicles():
    def __init__(self):
        self.comment = "Default vesicles cloud"

        self.list_of_vesicle = []

    ##################################### ТЕСТОВАЯ РЕАЛИЗАЦИЯ №№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№
    def CreateExsample(self):
        self.list_of_vesicle.append(Vesicle())
        self.list_of_vesicle.append(Vesicle())
        self.list_of_vesicle.append(Vesicle())
        self.list_of_vesicle.append(Vesicle())

        self.list_of_vesicle[1].position += (0, 10, 0)
        self.list_of_vesicle[2].position += (0, 0, 10)
        self.list_of_vesicle[3].position += (10, 0, 0)

    def ChangePosition(self, delta_position):
        for vesicle in self.list_of_vesicle:
            vesicle.ChangePosition(delta_position)

    def SetPosition(self, new_pos):  # фунцкия переноса в пространстве
        delta_pos = new_pos - self.position
        self.ChangePosition(delta_pos)

    ##################################################################################################################### не реализованна
    def Rotate(self, delta_angle):
        pass
        # @abc.abstractmethod

    def SetAngle(self, new_angle):  # реализация функции поворота
        delta_angle = new_angle - self.angle
        self.Rotate(delta_angle)

    def Draw(self, data):
        for triangle in self.view_poligon.poligon_list:
            v1, v2, v3 = triangle.get_vertices(self.view_poligon.vertex_list)
            draw_voxel_triangle(data, v1, v2, v3, self.view_data.color, self.view_data.thickness)




import numpy as np
from  Synthetic3D.src.hard.view_data import view_vtk_3D_data
def TestVesicles():
    test_data = np.zeros((128, 256, 512, 3), dtype=np.uint8)

    vesicle = Vesicle()
    vesicle.ChangePosition((256+127,127,64))

    print("len of triangles:", len(vesicle.view_shell.poligon_list))

    vesicle.Draw(test_data)

    for z in range(test_data.shape[0]):
        slice = test_data[z,:,:,:]
        cv2.imwrite(f"test/test_gen_vesicles/vesicules_slice_{z}.png", slice)

    print(vesicle.view_shell.vertex_list[1])

    view_vtk_3D_data(test_data, vesicle.view_shell.vertex_list, vesicle.position)# vesicle.view_shell.vertex_list[1].vertex)


if __name__ == "__main__":
    print("StartTestVesicles")
    TestVesicles()

