import numpy as np

class Vertex:
    def __init__(self, vertex : tuple|list, normal : tuple|list = (0, 0, 0)):
        assert len(vertex) == 3
        assert len(normal) == 3

        # координата точки
        self.vertex = np.array(vertex)

        # вектор нормали
        self.normal =  np.array(normal)

    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return f"vertex: {self.vertex}, normal: {self.normal}"
