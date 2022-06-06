from graph import Graph
from config import *
from random import shuffle, sample, randint
from math import exp


class Annealing:
    def __init__(self):
        self.graph = Graph()
        self.cur_route = self.graph.list_nodes()
        shuffle(self.cur_route)                               # Перемешиваем список вершин
        self.cur_route = self.cur_route + [self.cur_route[0]] # Делаем маршрут замкнутым. Это первый маршрут.
        self.cur_route_greedy = self.cur_route[:]             # Первый маршрут для жадного алгоритма
        self.candidate_route = []                             # 2-ой маршрут, который будем сравнивать с первым.
        self.last_route = []                                  # Маршрут на последней итерации 
        self.temperature = 100                                
    
    def select_nodes_invert(self):
        """
        Выбираем случайным образом два узла маршрута, не включая старт и финиш, и 
        между выбранными узлами инвертируем узлы. Так мы меняем только два ребра в маршруте.
        Возвращаем новый маршрут self.candidate_route
        """
        self.candidate_route = self.cur_route[:]
        indexs = sorted(sample(range(1, len(self.candidate_route) - 1), 2))
        
        temp = self.candidate_route[indexs[0]:(indexs[1] + 1)]
        self.candidate_route = self.candidate_route[:indexs[0]] + temp[::-1] + self.candidate_route[indexs[1] + 1:]
        return self.candidate_route
        
    
    def probability(self, length_1: int, length_2: int):
        """
        Вычисляем вероятность принятия маршрута self.candidate_route
        """
        self.temperature = self.temperature * ALPHA
        # Устанавливаем ограничение на нижний предел температуры
        if self.temperature <= 0.4: 
            self.temperature = 0.4
            
        p = 100 * exp(-(length_2 - length_1) / self.temperature)
        return p
    
    def select_route(self):
        """
        Выбираем маршрут
        """
        if self.probability(self.graph.length_route(self.cur_route), 
                         self.graph.length_route(self.candidate_route)) > randint(1, 100):
            self.cur_route = self.candidate_route[:]
        return self.cur_route 
            
    def run_invert(self):
        """
        Запускаем итерации
        """
        length_paths = []  # Длины маршрутов на итерациях
        
        for _ in range(NUM_ITER):
            self.select_nodes_invert()
            self.select_route()
            length_paths.append(self.graph.length_route(self.cur_route))
     
        self.last_route = self.cur_route[:]    
        return length_paths
            
    def run_greedy(self):
        """
        Жадный алгоритм. На каждой итерации выбираем более короткий маршрут.
        """
        self.cur_route = self.cur_route_greedy[:]
        length_paths = []  # Длины маршрутов на итерациях
        
        for _ in range(NUM_ITER):
            self.select_nodes_invert()
            if self.graph.length_route(self.candidate_route) < self.graph.length_route(self.cur_route):
                self.cur_route = self.candidate_route[:]
            length_paths.append(self.graph.length_route(self.cur_route))
            
        return length_paths
                            
        

if __name__=='__main__':        
    ann = Annealing()
    print(ann.graph.length_route(ann.cur_route))
    ann.run_invert()
    print(ann.graph.length_route(ann.cur_route), 'Annealing')
    ann.run_greedy()
    print(ann.graph.length_route(ann.cur_route), 'Greedy')
  
    
 