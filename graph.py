from plotly import graph_objs as go
import plotly.express as px
import numpy as np

#алгоритм сортировки точек в нужном порядке для границ или каждая стена отдельно

# ввод координат левой нижней точки и правой верхней точки поля
field = [[0, 0], [30, 20]]
# ввод координат внутрених стен
  # представление [[x1, y1], [x2, y2]] => [[x1, x2,], [y1, y2]]
walls = [[[10, 10], [10, 20]],
          [[20, 0], [20, 10]]]
for i in range(len(walls)):
  walls[i] = np.array(walls[i]).transpose()
# ввод координат камер
cameras = np.array([[9, 15], [5, 1], [19, 5], [25, 19]]).transpose()
# ввод координат зон камер
selected_fields = [[[0, 10], [10, 20]],
                   [[0, 0], [10, 10]],
                   [[10, 0], [20, 10]],
                   [[20, 10], [30, 20]]]
# ввод траектории
  # сперва центральная точка, потом крайние
trajectory = [[[5, 15], [0, 15], [5, 10]],
              [[5, 5], [5, 10], [10, 5]],
              [[15, 5], [10, 5], [15, 10]],
              [[25, 15], [20, 15], [25, 10]]]
for i in range(len(trajectory)):
  trajectory[i] = np.array(trajectory[i]).transpose()

fig = go.Figure()
# вывод поля
fig.add_shape(type="rect",x0=field[0][0], y0=field[0][1], x1=field[1][0],
              y1=field[1][1], line=dict(color="black", width=2))
fig.add_shape(type="rect", x0=field[0][0], y0=field[0][1], x1=field[1][0],
    y1=field[1][1], fillcolor="lightblue",
    line=dict(color="black", width=2), layer = 'below')
# вывод внутрених стен
for wall in walls:
  fig.add_trace(go.Scatter(x=wall[0], y=wall[1], mode='lines',
    showlegend=False, hoverinfo='none', line=dict(color='black', width=2)))
# ввывод камер
fig.add_trace(go.Scatter(x=cameras[0], y=cameras[1], mode='markers',
    name='Camera', line=dict(color='blue')))
# ввывод зон камер
for selected_field in selected_fields:
  fig.add_shape(type="rect",x0=selected_field[0][0], y0=selected_field[0][1],
    x1=selected_field[1][0], y1=selected_field[1][1], fillcolor="#eec896",
    line=dict(color="#e0993c", width=2), opacity=0.5)
# ввывод траектории
for field in trajectory:
  for i in range(1, len(field) + 1):
    fig.add_trace(go.Scatter(x=[field[0][0], field[0][i]],
      y=[field[1][0], field[1][i]], mode='lines',
      showlegend=False, hoverinfo='none', line=dict(color='red', width=2)))
fig.show()