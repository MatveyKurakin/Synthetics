from Synthetic3D.src.hard.split_curve import split_half_curve
class Edge:
    def __init__(self, v1_index, v2_index):
        self.v1_index = v1_index
        self.v2_index = v2_index
        self.vertex_mean = None

        self.new_index_pair = None

def split_edge(list_of_vertex, list_of_edge, index_edge, list_of_half_edges):
    edge = list_of_edge[index_edge]

    if edge.vertex_mean is None:
        v1 = list_of_vertex[edge.v1_index]
        v2 = list_of_vertex[edge.v2_index]

        v3 = split_half_curve(v1, v2)
        new_index = len(list_of_vertex)
        list_of_vertex.append(v3)
        list_of_edge[index_edge].vertex_mean = new_index # перестраховка что запишется в нужное место

        new_index_half_edges = len(list_of_half_edges)

        list_of_edge[index_edge].new_index_pair = (new_index_half_edges, new_index_half_edges+1)
        list_of_half_edges.append(Edge(edge.v1_index, edge.vertex_mean))
        list_of_half_edges.append(Edge(edge.vertex_mean, edge.v2_index))

    return edge.v1_index, edge.vertex_mean, edge.v2_index, edge.new_index_pair[0], edge.new_index_pair[1]
