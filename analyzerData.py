from plotly import graph_objs as go

import generator as gr
import graphsystem as gs
import database.db as db
import database.config as cf


class AnalyzerData:
    @staticmethod
    def compare_trajectories(x1, y1, times1, times2):
        good_x = []
        good_y = []
        bad_x = []
        bad_y = []
        flag = False
        for i1 in range(len(times1)):
            for i2 in range(len(times2)):
                if times1[i1] == times2[i2]:
                    flag = True
                    break
            if flag:
                good_x.append(x1[i1])
                good_y.append(y1[i1])
            else:
                bad_x.append(x1[i1])
                bad_y.append(y1[i1])
        return len(bad_x) == 0, good_x, good_y, bad_x, bad_y

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
        fig.show()

    @staticmethod
    def start_demo():
        x0_f = 0
        y0_f = 0
        x1_f = 30
        y1_f = 30
        s_x = 1
        s_y = 1
        width_w = 700
        height_w = 700
        starttime = "12:00"
        endtime = "18:00"
        x, y, state, times, ex = AnalyzerData.get_generate_traj(x0_f, y0_f, x1_f, y1_f, s_x, s_y, starttime, endtime)
        # берем человека из бд
        id_person = db.exec_query_first(f"""select id from {cf.schema_name}.person""",
                                        "[INFO] Get first id_person")


        # берутся его "фото" и отправляются на анализ лиц и результат сохраняется в бд с тем временем,
        # что указано в times в таблице appearence


        times2 = db.exec_query_all(f"""select data_time from {cf.schema_name}.appearence
         where id_person == {id_person}""", "[INFO] Get time from appearence")
        # по таблице appearence достаем time по id человека, которого мы взяли
        state_compar, good_x, good_y, bad_x, bad_y = AnalyzerData.compare_trajectories(x, y, times, times2)

        AnalyzerData.get_graph_traj_with_points(x0_f, y0_f, x1_f, y1_f, s_x, s_y, width_w, height_w,times,
                                                ex, x, y, good_x, good_y)

