import networkx as nx
from random import sample
from math import dist
from config import *
from itertools import pairwise


class Graph:
    def __init__(self):
        self.graph = nx.complete_graph(range(NUM_NODES))
        self.add_coordinates()
        self.add_lengths()
            
    def add_coordinates(self):
        """
        Добавляем координаты к узлам графа
        """
        [self.graph.add_nodes_from([i], coord=sample(range(COORDINATES), 2)) for i in self.graph.nodes]
        
    def add_lengths(self):
        """
        Добавляем длины ребер
        """
        for i in self.graph.edges:
            self.graph.add_edge(*i, length=int(dist(self.graph.nodes[i[0]]['coord'], self.graph.nodes[i[1]]['coord'])))
            
    def list_nodes(self):
        """
        Список вершин
        """
        return list(self.graph.nodes)
                
    def node_coord(self, node):
        """
        Возвращает координаты узла
        """
        return self.graph.nodes[node]['coord']
    
    def edge_length(self, node1, node2):
        """
        Возвращает длину ребра
        """
        return self.graph.get_edge_data(node1, node2)['length']
    
    def length_route(self, nodes: list):
        """
        Принимает список вершин. Возвращает длину маршрута
        """
        length = 0
        route = pairwise(nodes)
        for i in route:
            length += self.edge_length(*i)
        return length
        

if __name__ == '__main__':
    g = Graph()
    print(g.list_nodes())
    print(g.graph.nodes(data=True))
    print(g.graph.edges(data=True))
    print(g.length_route(g.list_nodes() + [g.list_nodes()[0]]))
   
    