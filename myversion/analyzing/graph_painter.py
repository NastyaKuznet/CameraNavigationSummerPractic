import plotly.graph_objects as go

# Размер поля
m, n = 10, 10

# Создаем фигуру
fig = go.Figure()

# Добавляем прямоугольник, представляющий поле
fig.add_shape(
    type="rect",
    x0=0, y0=0, x1=n, y1=m,
    line=dict(width=0),
    fillcolor="#EFE4B0"
)

# Добавляем сетку
for i in range(m + 1):
    fig.add_shape(
        type="line",
        x0=0, y0=i, x1=n, y1=i,
        line=dict(color="black", width=1)
    )
    fig.add_shape(
        type="line",
        x0=i, y0=0, x1=i, y1=m,
        line=dict(color="black", width=1)
    )

# Функция для добавления красной линии
def add_red_line(x_start, y_start, x_end, y_end):
    fig.add_shape(
        type="line",
        x0=x_start, y0=y_start, x1=x_end, y1=y_end,
        line=dict(color="red", width=2)
    )

# Функция для добавления зеленого треугольника
def add_green_triangle(p1, p2, p3):
    fig.add_trace(go.Scatter(
        x=[p1[0], p2[0], p3[0], p1[0]],
        y=[p1[1], p2[1], p3[1], p1[1]],
        fill="toself",
        fillcolor="green",
        line=dict(color="green"),
        mode="lines"
    ))

# Примеры добавления красных линий
add_red_line(1, 1, 5, 5)
add_red_line(2, 8, 8, 2)

# Примеры добавления зеленых треугольников
add_green_triangle((1, 1), (2, 3), (3, 1))
add_green_triangle((6, 6), (7, 8), (8, 6))

# Настраиваем оси
fig.update_xaxes(range=[0, n], showgrid=False, zeroline=False)
fig.update_yaxes(range=[0, m], scaleanchor="x", scaleratio=1, showgrid=False, zeroline=False)

# Убираем рамки и фоны
fig.update_layout(
    paper_bgcolor='white',
    plot_bgcolor='white',
    xaxis=dict(showline=False),
    yaxis=dict(showline=False)
)

# Показываем фигуру
fig.show()


from CameraNavigationSummerPractic.myversion.general.DBHelper import DBHelper


class GraphPainter:
    def graph(self, loc_id, db_helper):
        # Размер поля
        m, n = 10, 10

        # Создаем фигуру
        fig = go.Figure()

        # Добавляем прямоугольник, представляющий поле
        fig.add_shape(
            type="rect",
            x0=0, y0=0, x1=n, y1=m,
            line=dict(width=0),
            fillcolor="#EFE4B0"
        )

        # Добавляем сетку
        for i in range(m + 1):
            fig.add_shape(
                type="line",
                x0=0, y0=i, x1=n, y1=i,
                line=dict(color="black", width=1)
            )
            fig.add_shape(
                type="line",
                x0=i, y0=0, x1=i, y1=m,
                line=dict(color="black", width=1)
            )

        # Добавляем стены и камеры
        walls = GraphPainter.get_walls(loc_id, db_helper)
        for wall in walls:
            GraphPainter.add_line(fig, wall[0][0], wall[0][1], wall[1][0], wall[1][1], "red")

        cameras = GraphPainter.get_cameras(loc_id, db_helper)
        vertexes = []
        for camera in cameras:
            vertexes.append(camera[3])
            GraphPainter.add_green_triangle(fig, camera[0], camera[1], camera[2])



        # Настраиваем оси
        fig.update_xaxes(range=[0, n], showgrid=False, zeroline=False)
        fig.update_yaxes(range=[0, m], scaleanchor="x", scaleratio=1, showgrid=False, zeroline=False)

        # Убираем рамки и фоны
        fig.update_layout(
            paper_bgcolor='white',
            plot_bgcolor='white',
            xaxis=dict(showline=False),
            yaxis=dict(showline=False)
        )

        return fig.to_html()

    @staticmethod
    def get_walls(loc_id, db_helper: DBHelper):
        db_helper.exec(f"""
        select coord_start, coord_end from walls where id_location = {loc_id}
        """)
        walls = []
        coord_start, coord_end = db_helper.fetch_one()
        while coord_start:
            walls.append((coord_start, coord_end))
        return walls

    # Возвращает все точки для каждой линии между всеми камерами
    @staticmethod
    def get_graph_edge(loc_id, db_helper: DBHelper):
        db_helper.exec(f"""
        select points from graph where id = {loc_id}
        """)
        lines = []
        line = db_helper.fetch_one()
        while line:
            lines.append(lines)
        return lines

    # Возвращает наборы из 4 точек. 1) Сама камера. 2 и 3 - определяют треугольник области видимости.
    # 4 - ближайшая целая точка к центру треугольника. Фактически вершина графа
    @staticmethod
    def get_cameras(loc_id, db_helper: DBHelper):
        db_helper.exec(f"""
        select points from camera where id_location = {loc_id}
        """)
        db_helper.exec(f"""
        select points from graph where id = {loc_id}
        """)
        camera_points = []
        points = db_helper.fetch_one()
        while points:
            camera_points.append(points)
        return camera_points

    @staticmethod
    # Функция для добавления красной линии
    def add_line(fig, x_start, y_start, x_end, y_end, color):
        fig.add_shape(
            type="line",
            x0=x_start, y0=y_start, x1=x_end, y1=y_end,
            line=dict(color=color, width=2)
        )

    @staticmethod
    # Функция для добавления зеленого треугольника
    def add_green_triangle(fig, p1, p2, p3):
        fig.add_trace(go.Scatter(
            x=[p1[0], p2[0], p3[0], p1[0]],
            y=[p1[1], p2[1], p3[1], p1[1]],
            fill="toself",
            fillcolor="green",
            line=dict(color="green"),
            mode="lines"
        ))

