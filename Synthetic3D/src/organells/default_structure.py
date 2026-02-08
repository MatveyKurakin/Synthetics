import numpy as np
from Synthetic3D.src.hard.edge import Edge
from Synthetic3D.src.hard.triangle import Triangle
from Synthetic3D.src.hard.vertex import Vertex

def create_octahedron_with_main_point(center_point, rx, ry, rz):

    normal_len_max = max(rx,ry,rz)

    v1 = Vertex(np.array(center_point) + (rx, 0, 0), (normal_len_max/rx, 0, 0))
    v2 = Vertex(np.array(center_point) - (rx, 0, 0), (-normal_len_max/rx, 0, 0))

    v3 = Vertex(np.array(center_point) + (0, ry, 0), (0, normal_len_max/ry, 0))
    v4 = Vertex(np.array(center_point) - (0, ry, 0), (0, -normal_len_max/ry, 0))

    v5 = Vertex(np.array(center_point) + (0, 0, rz), (0, 0, normal_len_max/rz))
    v6 = Vertex(np.array(center_point) - (0, 0, rz), (0, 0, -normal_len_max/rz))

    vertices = [v1, v2, v3, v4, v5, v6]

    ed1 = Edge(0, 2) # v1 v3
    ed2 = Edge(0, 3) # v1 v4
    ed3 = Edge(0, 4) # v1 v5
    ed4 = Edge(0, 5) # v1 v6
    ed5 = Edge(1, 2) # v2 v3
    ed6 = Edge(1, 3) # v2 v4
    ed7 = Edge(1, 4) # v2 v5
    ed8 = Edge(1, 5) # v2 v6
    ed9 = Edge(2, 4) # v3 v5
    ed10= Edge(2, 5) # v3 v6
    ed11= Edge(3, 4) # v4 v5
    ed12= Edge(3, 5) # v4 v6

    edges = [ed1, ed2, ed3, ed4, ed5, ed6, ed7, ed8, ed9, ed10, ed11, ed12]

    tr1 = Triangle((0, 2, 4), (0, 2, 8))  # v1 v3 v5
    tr2 = Triangle((0, 2, 5), (0, 3, 9))  # v1 v3 v6
    tr3 = Triangle((0, 3, 4), (1, 2, 10)) # v1 v4 v5
    tr4 = Triangle((0, 3, 5), (1, 3, 11)) # v1 v4 v6

    tr5 = Triangle((1, 2, 4), (4, 6, 8))  # v2 v3 v5
    tr6 = Triangle((1, 2, 5), (4, 7, 9))  # v2 v3 v6
    tr7 = Triangle((1, 3, 4), (5, 6, 10)) # v2 v4 v5
    tr8 = Triangle((1, 3, 5), (5, 7, 11)) # v2 v4 v6

    triangles = [tr1, tr2, tr3, tr4, tr5, tr6, tr7, tr8]

    return vertices, edges, triangles






