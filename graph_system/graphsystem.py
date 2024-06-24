from plotly import graph_objs as go
from setting_location import field, walls, cameras, selected_fields
import database.db as db


def draw_location(fig):
    # вывод поля
    fig.add_shape(type="rect", x0=field[0][0], y0=field[0][1], x1=field[1][0],
                  y1=field[1][1], line=dict(color="black", width=2))
    fig.add_shape(type="rect", x0=field[0][0], y0=field[0][1], x1=field[1][0],
                  y1=field[1][1], fillcolor="lightblue",
                  line=dict(color="black", width=2), layer='below')
    # вывод внутрених стен
    for wall in walls:
        fig.add_trace(go.Scatter(x=wall[0], y=wall[1], mode='lines',
                                 showlegend=False, hoverinfo='none', line=dict(color='black', width=2)))
    # ввывод камер
    fig.add_trace(go.Scatter(x=cameras[0], y=cameras[1], mode='markers',
                             name='Camera', line=dict(color='blue')))
    # ввывод зон камер
    for selected_field in selected_fields:
        fig.add_shape(type="rect", x0=selected_field[0][0], y0=selected_field[0][1],
                      x1=selected_field[1][0], y1=selected_field[1][1], fillcolor="#eec896",
                      line=dict(color="#e0993c", width=2), opacity=0.5)


def draw_trajectory(fig, id_person):
    trajectory = db.get_trajectory(id_person)
    cen = trajectory[0]
    bli = [a for i in trajectory[1] for a in i]
    ind = 0
    i = 0
    save = 0
    x = []
    y = []
    while (True):
        if ind < len(bli) and cen[i][0] == bli[ind][4]:
            x.append(bli[ind][0])
            x.append(bli[ind][2])
            y.append(bli[ind][1])
            y.append(bli[ind][3])
            save = bli[ind][5]
            ind += 1
        else:
            if save != cen[i + 1][0]:
                x.append(cen[i][1][0])
                x.append(cen[i + 1][1][0])
                y.append(cen[i][1][1])
                y.append(cen[i + 1][1][1])
            i += 1
        if i == len(cen) - 1:
            break

    fig.add_trace(go.Scatter(x=x, y=y, mode='lines',
                             showlegend=True, line=dict(color='red', width=2)))


def draw():
    fig = go.Figure()
    draw_location(fig)
    draw_trajectory(fig, 3)
    fig.show()


if __name__ == "__main__":
    draw()
