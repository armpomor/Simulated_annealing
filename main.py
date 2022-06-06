import plotly.graph_objs as go
from annealing import Annealing
from itertools import pairwise
from config import *


def f1(ann):
    """
    Строим график зависимости длины маршрута на итерации от номера итерации.
    """
    x1 = ann.run_invert()
    x = ann.run_greedy()

    fig = go.Figure()
    fig.update_layout(title=dict(text='Simulated annealing',
                      font=dict(size=20)), margin=dict(l=0, t=30, b=0, r=0))

    fig.add_trace(go.Scatter(y=x, mode='lines', line=dict(width=3, color='black'), name='Greedy'))
  
    fig.add_trace(go.Scatter(y=x1, mode='lines', line=dict(width=3, color='red'), name='Annealing'))

    fig.update_xaxes(title='Номер итерации')
    fig.update_yaxes(title='Длина маршрута на итерации')
    
    fig.show()


def f2(ann):
    """
    Последний маршрут.
    """
    route = ann.last_route
    # Список координат последнего маршрута
    coordinates = [ann.graph.node_coord(i) for i in route]
    x = [i[0] for i in coordinates]
    y = [i[1] for i in coordinates]
    
    fig = go.Figure()
    fig.update_layout(title=dict(text=f'Длина последнего маршрута {ann.graph.length_route(ann.last_route)} на {NUM_ITER} итерации.',
                                  font=dict(size=20)), margin=dict(l=0, t=30, b=0, r=0))

    fig.add_trace(go.Scatter(x=x, y=y, mode='markers', marker=dict(size=7, color='black', symbol="circle"),
                              name='City', text=[(route.index(i) + 1) for i in route], hoverinfo='text'))
    
    # Координаты ребер (пары координат)
    couple_x = pairwise(x)
    couple_y = pairwise(y)
    edges = zip(couple_x, couple_y)
    
    routes = [go.Scatter(x=i[0], y=i[1], mode='lines', line=dict(width=2)) for i in edges]
    for i in routes:
        fig.add_trace(i)

    fig.show()


ann = Annealing()
f1(ann)
f2(ann)




