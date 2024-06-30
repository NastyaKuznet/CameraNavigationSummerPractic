from plotly import graph_objs as go

import generator as gr
import graphsystem as gs


class AnalyzerData:
    @staticmethod
    def compare_trajectories(x1, y1, times1, times2):
        good = []
        bad = []
        flag = False
        for i1 in range(len(times1)):
            for i2 in range(len(times2)):
                if times1[i1] == times2[i2]:
                    flag = True
                    break
            if flag:
                good.append((x1[i1], y1[i1]))
            else:
                bad.append((x1[i1], y1[i1]))
        return len(bad) == 0, good, bad

    @staticmethod
    def get_generate_traj(x0, y0, x1, y1, size_x, size_y, start_time,
                          end_time):
        ex = gr.generate_exit(x0, x1, y0, y1, size_x, size_y)
        times = gr.generate_times(start_time, end_time, 1,
                                  10, "2024-07-08",
                                  "2024-07-08")
        x, y, state = gr.generation_trajectory(ex[0], ex[1], x0, x1, y0, y1, size_x, size_y, len(times))
        if len(x) < len(times):
            times = times[:len(x)]
        return x, y, state, times, ex

    @staticmethod
    def get_graph_traj_with_points(x0_field, y0_field, x1_field, y1_field, size_x, size_y,
                                   width_window, height_window, times, ex, x1, y1, x2, y2):
        field = [[x0_field, y0_field], [x1_field, y1_field]]
        cam = gr.generate_cameras_all_cell(x0_field, x1_field, y0_field, y1_field, size_x, size_y)

        fig = go.Figure()
        gs.draw_location(fig, field, exits=[ex], cameras=cam)
        gs.draw_chessboard(fig, x0_field, x1_field, y0_field, y1_field, size_x, size_y)
        gs.draw_a_lot_trajectory_with_point(fig, [x1, x2], [y1, y2], times)
        fig.update_layout(
            xaxis_range=[x1, x2],
            yaxis_range=[y1, y2],
            xaxis_autorange=False,
            yaxis_autorange=False,
            width=width_window,
            height=height_window,
        )
        return fig.to_html()
