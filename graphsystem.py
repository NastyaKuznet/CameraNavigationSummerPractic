from plotly import graph_objs as go
import pandas as pd
import plotly.express as px
import plotly.colors as pcolors

import generator as gr


def draw_field(fig, field):
    """Отрисовывает на объекте fig прямоугольник. Field массив состоящий из двух массивов:
    первый - левая нижняя точка x, y, второй - правая верхняя точка x, y."""
    fig.add_shape(type="rect", x0=field[0][0], y0=field[0][1], x1=field[1][0], y1=field[1][1],
                  line=dict(color="black", width=2))
    fig.add_shape(type="rect", x0=field[0][0], y0=field[0][1], x1=field[1][0], y1=field[1][1],
                  fillcolor="lightblue",
                  line=dict(color="black", width=2), layer='below')


def draw_walls(fig, walls):
    """Отрисовывает стены. Walls массив состоящий из массивов длиной 2,
    где для i=0,n walls[i][0] = x, walls[i][1] = y."""
    for wall in walls:
        fig.add_trace(go.Scatter(x=wall[0], y=wall[1], mode='lines',
                                 showlegend=False, hoverinfo='none', line=dict(color='black', width=2)))


def draw_cameras(fig, cameras):
    """Отрисовывает камеры в виде синих точек. Cameras массив из двух подмассивов:
    первый - все x, второй - все y."""
    fig.add_trace(go.Scatter(x=cameras[0], y=cameras[1], mode='markers',
                             name='Camera', line=dict(color='blue')))


def draw_selected_field(fig, selected_fields):
    """Отрисовывает полупрозрачные секции оранжевого цвета. Selected_fields массив,
    состоящий из массивов, каждый из которых описывает одну секцию. Массив одной
    секции состоит из двух массивов: первый - левая нижняя точка [x, y],
    второй - правая верхняя [x, y]."""
    for selected_field in selected_fields:
        fig.add_shape(type="rect", x0=selected_field[0][0], y0=selected_field[0][1],
                      x1=selected_field[1][0], y1=selected_field[1][1], fillcolor="#eec896",
                      line=dict(color="#e0993c", width=2), opacity=0.5)


def draw_exits(fig, exits):
    """Отрисовывает указатель с надписью Вход/выход. Exits массив состоящий из массивов,
    каждый из которых содержит координаты x, y каждого входа."""
    for ex in exits:
        fig.add_annotation(x=ex[0], y=ex[1], text="Вход/выход",
                           showarrow=True, arrowhead=7, arrowsize=1, arrowcolor='black')


def draw_location(fig, field, walls=None, cameras=None, selected_fields=None, exits=None):
    """Отрисовывает поле, а также стены, камеры, выделенные поля, выходы, если они указаны."""
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
    """Отрисовывает сетку по полю ограниченному x0_field, y0_field, x1_field, y1_field.
    Ширина и высота ячейки сетки задается width, height."""
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


def draw_chessboard(fig, x0_field, x1_field, y0_field, y1_field, size_x, size_y):
    """Отрисовывает полупрозрачную шахматную доску оранжевым и зеленым цветом по
    полю ограниченному x0_field, x1_field, y0_field, y1_field, где ширина и длина
    клеток задается size_x, size_y"""
    last_step_y = y0_field
    step_y = y0_field + size_y
    count = True
    last_count = count
    while step_y <= y1_field:
        last_step_x = x0_field
        step_x = x0_field + size_x
        count = not last_count
        last_count = count
        while step_x <= x1_field:
            if count:
                fillc = "orange"
            else:
                fillc = "green"
            fig.add_shape(type="rect", x0=last_step_x, y0=last_step_y, x1=step_x,
                          y1=step_y, line=dict(color=fillc, width=2), opacity=0.1,
                          fillcolor=fillc)
            count = not count
            last_step_x = step_x
            step_x += size_x
        last_step_y = step_y
        step_y += size_y


def draw_trajectory(fig, x, y):
    """Отрисовывается траетория по массивам x, y."""

    fig.add_trace(go.Scatter(x=x, y=y, mode='lines',
                             showlegend=True, line=dict(color='red', width=2)))


def draw_trajectory_with_point(fig, x, y):
    """Отрисовывается траетория по массивам x, y с точкой показывающей передвижение."""
    fig = go.Figure(
        data=[go.Scatter(x=x, y=y,
                         mode="lines",
                         line=dict(width=2, color="green")),
              go.Scatter(x=x, y=y,
                         mode="lines",
                         line=dict(width=2, color="green"))],
        layout=go.Layout(
            xaxis=dict(range=[min(x), max(x)], autorange=False, zeroline=False),
            yaxis=dict(range=[min(y), max(y)], autorange=False, zeroline=False),
            title_text="Траектория движения", hovermode="closest",
            updatemenus=[dict(type="buttons",
                              buttons=[dict(label="Play",
                                            method="animate",
                                            args=[None])])]),
        frames=[go.Frame(
            data=[go.Scatter(
                x=[x[k]],
                y=[y[k]],
                mode="markers",
                marker=dict(color="red", size=10))])
            for k in range(len(x))]
    )


def draw_a_lot_trajectory_with_point(fig, x_mas, y_mas, times,
                                     colors_lines=pcolors.qualitative.Plotly,
                                     colors_points=pcolors.qualitative.Set1):
    """Отрисовывается траетории по массивам x_mas, y_mas с точками показывающими передвижение."""
    points_traces = []
    max_len = 0
    for i in range(len(x_mas)):
        fig.add_trace(go.Scatter(x=x_mas[i], y=y_mas[i],
                                 mode="lines",
                                 line=dict(width=2, color=colors_lines[i % len(colors_lines)])))
    for i in range(len(x_mas)):
        fig.add_trace(go.Scatter(x=x_mas[i], y=y_mas[i],
                                 mode="lines",
                                 text=times,
                                 hovertemplate='Время: %{text}<br>x: %{x:.2f}<br>y: %{y:.2f}<extra></extra>',
                                 line=dict(width=2, color=colors_lines[i % len(colors_lines)])))
        points_traces.append(go.Scatter(x=[x_mas[i][0]], y=[y_mas[i][0]], mode="markers",
                                        marker=dict(color=colors_points[i % len(colors_points)], size=10),
                                        name=f'Point {i}'))
        len_i = len(x_mas[i])
        if len_i > max_len:
            max_len = len_i
    fig.update_layout(go.Layout(title_text="Траектория движения", hovermode="closest",
                                updatemenus=[dict(type="buttons",
                                                  buttons=[dict(label="Play",
                                                                method="animate",
                                                                args=[None])])]))
    frames = []
    for k in range(max_len):
        frame_data = []
        for i in range(len(x_mas)):
            x_now = x_mas[i][-1] if k >= len(x_mas[i]) else x_mas[i][k]
            y_now = y_mas[i][-1] if k >= len(x_mas[i]) else y_mas[i][k]
            frame_data.append(go.Scatter(
                x=[x_now],
                y=[y_now],
                mode="markers",
                marker=dict(color=colors_points[i % len(colors_points)], size=10),
                name=f'Point {i}'
            ))
        frames.append(go.Frame(data=frame_data))
    fig.frames = frames


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
    # draw_test_location(0, 0, 10, 10, 1, 1, 600, 600)
    data0 = [
        {'date': '2023-03-01', 'time': '10:00', 'visitors': 10},
        {'date': '2023-03-01', 'time': '11:00', 'visitors': 15},
        {'date': '2023-03-01', 'time': '12:00', 'visitors': 20},
        {'date': '2023-03-02', 'time': '10:00', 'visitors': 12},
        {'date': '2023-03-02', 'time': '11:00', 'visitors': 18},
        {'date': '2023-03-02', 'time': '12:00', 'visitors': 25},
    ]
    # draw_heatmap_time_count_people(data0)

