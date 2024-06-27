from plotly import graph_objs as go
import pandas as pd
import plotly.express as px

import setting_location as sl
import database.db as db
import generator as gr


def draw_field(fig, field):
    fig.add_shape(type="rect", x0=field[0][0], y0=field[0][1], x1=field[1][0],
                  y1=field[1][1], line=dict(color="black", width=2))
    fig.add_shape(type="rect", x0=field[0][0], y0=field[0][1], x1=field[1][0],
                  y1=field[1][1], fillcolor="lightblue",
                  line=dict(color="black", width=2), layer='below')


def draw_walls(fig, walls):
    for wall in walls:
        fig.add_trace(go.Scatter(x=wall[0], y=wall[1], mode='lines',
                                 showlegend=False, hoverinfo='none', line=dict(color='black', width=2)))


def draw_cameras(fig, cameras):
    fig.add_trace(go.Scatter(x=cameras[0], y=cameras[1], mode='markers',
                             name='Camera', line=dict(color='blue')))


def draw_selected_field(fig, selected_fields):
    for selected_field in selected_fields:
        fig.add_shape(type="rect", x0=selected_field[0][0], y0=selected_field[0][1],
                      x1=selected_field[1][0], y1=selected_field[1][1], fillcolor="#eec896",
                      line=dict(color="#e0993c", width=2), opacity=0.5)


def draw_exits(fig, exits):
    for ex in exits:
        fig.add_annotation(x=ex[0], y=ex[1], text="Вход/выход",
                           showarrow=True, arrowhead=7, arrowsize=1, arrowcolor='black')


def draw_location(fig, field, walls=None, cameras=None, selected_fields=None, exits=None):
    draw_field(fig, field)
    if walls is not None:
        draw_walls(fig, walls)
    if cameras is not None:
        draw_cameras(fig, cameras)
    if selected_fields is not None:
        draw_selected_field(fig, selected_fields)
    if exits is not None:
        draw_exits(fig, exits)


def line_field(fig, width, height, x0_field, y0_field, x1_field, y1_field):
    x0 = x0_field
    while True:
        x0 = x0 + width
        if x0 >= x1_field:
            break
        fig.add_trace(go.Scatter(x=[x0, x0], y=[y0_field, y1_field], mode='lines',
                                 showlegend=False, hoverinfo='none', line=dict(color='orange', width=2)))
    y0 = y0_field
    while True:
        y0 = y0 + height
        if y0 >= y1_field:
            break
        fig.add_trace(go.Scatter(x=[x0_field, x1_field], y=[y0, y0], mode='lines',
                                 showlegend=False, hoverinfo='none', line=dict(color='orange', width=2)))


def draw_trajectory(fig, id_person): #переделать под новую бд
    trajectory = db.get_trajectory(id_person)
    cen = trajectory[0]
    bli = [a for i in trajectory[1] for a in i]
    ind = 0
    i = 0
    save = 0
    x = []
    y = []
    while True:
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


def draw_test_location(x0, y0, x1, y1, size_x, size_y, width_window, height_window):
    field = [[x0, y0], [x1, y1]]
    ex = gr.generate_exit(x0, x1, y0, y1, size_x, size_y)
    cam = gr.generate_cameras_all_cell(x0, x1, y0, y1, size_x, size_y)
    fig = go.Figure()
    draw_location(fig, field, exits=[ex], cameras=cam)
    line_field(fig, size_x, size_y, x0, y0, x1, y1)
    trajectory = gr.generation_trajectory(ex[0], ex[1], x0, x1, y0, y1, size_x, size_y,
                                          10, 40, 15, 20)
    fig.add_trace(go.Scatter(x=trajectory[0], y=trajectory[1], mode='lines', text='trajectory',
                             showlegend=True, line=dict(color='red', width=2)))
    fig.update_layout(
        xaxis_range=[x0, x1],
        yaxis_range=[y0, y1],
        xaxis_autorange=False,
        yaxis_autorange=False,
        width=width_window,
        height=height_window,
    )
    fig.show()


def draw_heatmap_time_count_people(data):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df['time'] = pd.to_datetime(df['time'], format='%H:%M').dt.time
    fig = px.density_heatmap(
        df,
        x='date',
        y='time',
        z='visitors',
        color_continuous_scale='Viridis',  # Выберите подходящую цветовую палитру
        title='Количество посетителей по дням и времени'
    )
    fig.update_layout(
        xaxis_title='Дата',
        yaxis_title='Время',
        coloraxis_colorbar_title='Количество посетителей',
    )
    fig.show()


if __name__ == "__main__":
    #draw_test_location(0, 0, 10, 10, 1, 1, 600, 600)
    data0 = [
        {'date': '2023-03-01', 'time': '10:00', 'visitors': 10},
        {'date': '2023-03-01', 'time': '11:00', 'visitors': 15},
        {'date': '2023-03-01', 'time': '12:00', 'visitors': 20},
        {'date': '2023-03-02', 'time': '10:00', 'visitors': 12},
        {'date': '2023-03-02', 'time': '11:00', 'visitors': 18},
        {'date': '2023-03-02', 'time': '12:00', 'visitors': 25},
    ]
    draw_heatmap_time_count_people(data0)
