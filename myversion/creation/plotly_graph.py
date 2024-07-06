import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go

# Инициализация приложения Dash
app = dash.Dash(__name__)

# Начальные данные для графика
fig = go.Figure()

# Размер поля
m, n = 10, 10

# Создаем начальное поле
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

# Настраиваем оси
fig.update_xaxes(range=[0, n], showgrid=False, zeroline=False)
fig.update_yaxes(range=[0, m], scaleanchor="x", scaleratio=1, showgrid=False, zeroline=False)

# Убираем рамки и фоны
fig.update_layout(
    paper_bgcolor='white',
    plot_bgcolor='white',
    xaxis=dict(showline=False),
    yaxis=dict(showline=False),
    clickmode='event+select'  # Включаем режим кликов
)

# Определяем разметку приложения
app.layout = html.Div([
    dcc.Graph(
        id='interactive-graph',
        figure=fig
    ),
    html.Div(id='output')
])

# Хранение точек для линий и треугольников
points = []


# Коллбек для обработки кликов на графике
@app.callback(
    Output('interactive-graph', 'figure'),
    Input('interactive-graph', 'clickData'),
    State('interactive-graph', 'figure')
)
def update_graph(clickData, current_fig):
    if clickData is None:
        return current_fig

    # Получаем координаты клика
    x, y = clickData['points'][0]['x'], clickData['points'][0]['y']
    points.append((x, y))

    fig = go.Figure(current_fig)

    # Отрисовываем точки
    fig.add_trace(go.Scatter(
        x=[x], y=[y],
        mode='markers',
        marker=dict(color='black', size=10)
    ))

    # Если две точки, рисуем красную линию
    if len(points) % 2 == 0:
        x_start, y_start = points[-2]
        x_end, y_end = points[-1]
        fig.add_shape(
            type="line",
            x0=x_start, y0=y_start, x1=x_end, y1=y_end,
            line=dict(color="red", width=2)
        )

    # Если три точки, рисуем зеленый треугольник
    if len(points) % 3 == 0:
        p1, p2, p3 = points[-3], points[-2], points[-1]
        fig.add_trace(go.Scatter(
            x=[p1[0], p2[0], p3[0], p1[0]],
            y=[p1[1], p2[1], p3[1], p1[1]],
            fill="toself",
            fillcolor="green",
            line=dict(color="green"),
            mode="lines"
        ))

    return fig


# Запуск приложения
if __name__ == '__main__':
    app.run_server(debug=True)
