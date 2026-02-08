import abc
from copy import deepcopy


######################################################################################## возможно класс избыточен и не нужен
class Shell:
    """
    Класс для хранения поверхностных точек
    """
    def __init__(self):
        self.vertex_list = []
        self.edge_list = []
        self.poligon_list = []

    def __deepcopy__(self, memo):
        new_shell = Shell
        new_shell.vertex_list = deepcopy(self.vertex_list, memo)
        new_shell.edge_list = deepcopy(self.edge_list, memo)
        new_shell.poligon_list = deepcopy(self.poligon_list, memo)
        return new_shell

######################################################################################## возможно класс избыточен и не нужен
class Frame:
    """
    Класс для хранения направляющих
    """

    def __init__(self):
        self.points_list = []


class ViewData:
    """
    Класс для хранения данных для отображения
    """

    def __init__(self):
        self.color = (255, 0, 0) # красный
        self.mask_color = (255, 255, 255)
        self.thickness = 0

class Organell(abc.ABC):
    """
    Общий класс для подвижных органелл.

    Arguments:
        comment     : str? - поле для комментария каждой конкретной органеллы для возможности
                    создания уникальных именованных объектов.
        frame       : list[point] - класс для хранения центральных точек органеллы (центры везикул, центральная линия
                    митохондрии, центральная линия аксона, центр ПСП и т.д.)
        shell       : list[point] - класс для хранения грубых данных оболочки (в первом приближении без сглаживания)
        view_poligon: list[triangle] - список треугольников для рисования в нужных координатах и ориентации

        angle       : (float, float, float) - текущий угол поворота органеллы, спроецированный по осям X, Y и Z.
        position    : (int, int, int) - текущая позиция органеллы в пространстве

    Methods: ################################################################################################################## нуждается в доработке обобщенных методов
        SetPosition(new_pos) - функция изменения положения в пространстве в положение new_pos (int, int, int).
                               *смещение положения должно вычисляеться как новое минус старое
        Rotate(angle_delta) - функция поворота органеллы на угол angle_delta, заданный как (float, float, float)

        Draw(data) - функция рисования органеллы в пространстве data

    """

    def __init__(self):
        self.comment = ""

        self.frame = Frame()
        self.shell = Shell()

        self.view_shell = None

        self.angle = (0, 0, 0)
        self.position = (0, 0, 0)

        self.view_data = ViewData()

    def __CalculateViewData(self): pass # создает треугольники в нужной ориентации для рисования

    def __Calculate_Shift(self): pass # смещает координаты точек

    def __Calculate_Turn(self): pass # поворачивает точки относительно центра

    ############################################################################################## В текущей реализации 1 треугольник дробится в 4
    def Partition_of_triangles(self, number_of_iteration):
        for i in range(number_of_iteration):
            new_shall = Shell()

            vertices = self.view_shell.vertex_list
            edges = self.view_shell.edge_list

            for triangle in self.view_shell.poligon_list:
                new_shall.poligon_list += triangle.partition_of_triangle(vertices, edges, new_shall.edge_list)

            new_shall.vertex_list = vertices
            self.view_shell = new_shall

    # @abc.abstractmethod
    def ChangePosition(self, delta_position): pass

    def SetPosition(self, new_pos): #фунцкия переноса в пространстве
        delta_pos = new_pos - self.position
        self.ChangePosition(delta_pos)

    #@abc.abstractmethod
    def Rotate(self, delta_angle): pass # реализация функции поворота

    def SetAngle(self, new_angle): # реализация функции поворота
        delta_angle = new_angle - self.angle
        self.Rotate(delta_angle)


    @abc.abstractmethod
    def Draw(self, data):   pass  # реализация функции отрисовки на входных данных
