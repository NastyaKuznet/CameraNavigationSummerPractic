from plotly import graph_objs as go

import database.db as db
import generator as gn
import graphsystem as gs

x0 = 0
y0 = 0
x1 = 20
y1 = 20
size_x = 1
size_y = 1
x_exit, y_exit = gn.generate_exit(x0, x1, y0, y1, size_x, size_y)
count_max_start = 0
count_max_end = 100
early_start = 10
early_end = 30
persons = db.get_all_person()
x_mas = []
y_mas = []
kit_mas = []
for i in range(len(persons)):
    x, y, state = gn.generation_trajectory(x_exit, y_exit, x0, x1, y0, y1, size_x, size_y, count_max_start, count_max_end,
                             early_start, early_end)
    photos = db.get_person_appearances(persons[i])
    kit = []
    for a in range(len(x)):
        kit.append(photos[i % len(photos)])
    x_mas.append(x)
    y_mas.append(y)
    kit_mas.append(kit)

#потом берется траетория из анализа

fig = go.Figure()
gs.draw_a_lot_trajectory_with_point(fig, x_mas, y_mas, None)
fig.to_html()




