from Synthetic3D.src.hard.edge import Edge, split_edge

class Triangle:
    def __init__(self, triple_vertex_index, triple_edge_indexes):
        assert len(triple_vertex_index) == 3
        assert len(triple_edge_indexes) == 3

        self.vertex_indexes = triple_vertex_index
        self.edge_indexes = triple_edge_indexes
    def get_vertices(self, vertex_list):
        return (vertex_list[self.vertex_indexes[0]],
                vertex_list[self.vertex_indexes[1]],
                vertex_list[self.vertex_indexes[2]])

    def get_edge(self, edge_list):
        return (edge_list[self.edge_indexes[0]],
                edge_list[self.edge_indexes[1]],
                edge_list[self.edge_indexes[2]])

    def partition_of_triangle(self, vertices, edges, new_half_edges):
        # тюрпл из 5 индексов
        split_edge_res_1 = split_edge(vertices, edges, self.edge_indexes[0], new_half_edges)
        split_edge_res_2 = split_edge(vertices, edges, self.edge_indexes[1], new_half_edges)
        split_edge_res_3 = split_edge(vertices, edges, self.edge_indexes[2], new_half_edges)

        new_edge_index = len(new_half_edges)
        # поиск общих вершин из первой
        if split_edge_res_1[0] == split_edge_res_2[0]:
            v1_1, v_mean1, v2_1, ed1_1, ed2_1 = split_edge_res_1
            v1_2, v_mean2, v2_2, ed1_2, ed2_2 = split_edge_res_2

            if v2_1 == split_edge_res_3[0]:
                v1_3, v_mean3, v2_3, ed1_3, ed2_3 = split_edge_res_3
            else:
                v2_3, v_mean3, v1_3, ed2_3, ed1_3 = split_edge_res_3


        elif split_edge_res_1[0] == split_edge_res_2[2]:
            v1_1, v_mean1, v2_1, ed1_1, ed2_1 = split_edge_res_1
            v2_2, v_mean2, v1_2, ed2_2, ed1_2 = split_edge_res_2

            if v2_1 == split_edge_res_3[0]:
                v1_3, v_mean3, v2_3, ed1_3, ed2_3 = split_edge_res_3
            else:
                v2_3, v_mean3, v1_3, ed2_3, ed1_3 = split_edge_res_3

        elif split_edge_res_1[0] == split_edge_res_3[0]:
            v1_1, v_mean1, v2_1, ed1_1, ed2_1 = split_edge_res_1
            v1_2, v_mean2, v2_2, ed1_2, ed2_2 = split_edge_res_3

            if v2_1 == split_edge_res_2[0]:
                v1_3, v_mean3, v2_3, ed1_3, ed2_3 = split_edge_res_2
            else:
                v2_3, v_mean3, v1_3, ed2_3, ed1_3 = split_edge_res_2

        else: # v1_1 == v2_3
            v1_1, v_mean1, v2_1, ed1_1, ed2_1 = split_edge_res_1
            v2_2, v_mean2, v1_2, ed2_2, ed1_2 = split_edge_res_3

            if v2_1 == split_edge_res_2[0]:
                v1_3, v_mean3, v2_3, (ed1_3, ed2_3) = split_edge_res_2
            else:
                v2_3, v_mean3, v1_3, (ed2_3, ed1_3) = split_edge_res_2

        new_half_edges.append(Edge(v_mean1, v_mean2))
        tr1 = Triangle((v1_1, v_mean1, v_mean2), (ed1_1, new_edge_index, ed1_2))

        new_half_edges.append(Edge(v_mean1, v_mean3))
        new_half_edges.append(Edge(v_mean2, v_mean3))

        tr2 = Triangle((v_mean1, v_mean2, v_mean3),
                       (new_edge_index, new_edge_index+1, new_edge_index+2))

        tr3 = Triangle((v2_1, v_mean1, v_mean3),
                       (new_edge_index+1, ed2_1, ed1_3))

        tr4 = Triangle((v_mean3, v_mean2, v2_2),
                       (new_edge_index+2, ed2_2, ed2_3))

        return [tr1, tr2, tr3, tr4]
