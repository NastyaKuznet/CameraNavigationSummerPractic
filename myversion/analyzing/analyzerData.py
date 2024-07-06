from plotly import graph_objs as go
import inspect
import CameraNavigationSummerPractic.analyzeData.generator as gr
import CameraNavigationSummerPractic.analyzeData.graphsystem as gs
import CameraNavigationSummerPractic.database.db as db
import CameraNavigationSummerPractic.database.config as cf
import CameraNavigationSummerPractic.RecognizeFromFile as rf
from CameraNavigationSummerPractic.DBHelper import DBHelper
import joblib


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
    def analyze_trajectories(x_mas, y_mas, good_x_mas, good_y_mas, bad_x_mas, bad_y_mas, states_gen, states_an):
        count_com = 0
        count_all = 0
        for i in range(len(x_mas)):
            for j in range(len(x_mas[i])):
                for k in range(len(good_x_mas)):
                    if x_mas[i][j] == good_x_mas[i][k] and y_mas[i][j] == good_y_mas[i][k]:
                        count_com += 1
                        break
                count_all += len(x_mas[i])
        proc_com = round(count_com / count_all * 100, 2)
        count_go_out = 0
        for i in states_gen:
            if i:
                count_go_out += 1
        count_go_out_an = 0
        for i in states_an:
            if i:
                count_go_out_an += 1
        points = []
        for i in range(len(bad_x_mas)):
            points.append([])
            for j in range(len(bad_x_mas[i])):
                points[i].append((bad_x_mas[i][j], bad_y_mas[i][j]))

        answer = [f"Описание \n ",
                  f"Сколько вышло из здания (сгененрированно): {count_go_out}\n",
                  f"Сколько НЕ вышло из здания (сгененрированно): {len(states_gen) - count_go_out}\n",
                  f"Сколько вышло из здания (проанализировано): {count_go_out_an}\n",
                  f"Сколько НЕ вышло из здания (проанализировано): {len(states_an) - count_go_out_an}\n",
                  f"Процент совпадения: {proc_com}%\n",
                  f"Не совпавшие координаты: \n"]
        for i in range(len(points)):
            answer.append(f"{i+1}: {points[i]}\n")
        return answer





    @staticmethod
    def get_generate_traj(x0, y0, x1, y1, size_x, size_y, start_time,
                          end_time):
        ex = gr.Generator.generate_exit(x0, x1, y0, y1, size_x, size_y)
        times = gr.Generator.generate_times(start_time, end_time, 1,
                                            5, "2024-07-08",
                                            "2024-07-08")
        x, y, state = gr.Generator.generation_trajectory(ex[0], ex[1], x0, x1, y0, y1, size_x, size_y, len(times))
        if len(x) < len(times):
            times = times[:len(x)]
        return x, y, state, times, ex

    @staticmethod
    def get_graph_traj_with_points(x0_field, y0_field, x1_field, y1_field, size_x, size_y,
                                   width_window, height_window, times, ex, x1, y1, x2, y2):
        field = [[x0_field, y0_field], [x1_field, y1_field]]
        cam = gr.Generator.generate_cameras_all_cell(x0_field, x1_field, y0_field, y1_field, size_x, size_y)

        fig = go.Figure()
        gs.GraphSystem.draw_location(fig, field, exits=[ex], cameras=cam)
        gs.GraphSystem.draw_chessboard(fig, x0_field, x1_field, y0_field, y1_field, size_x, size_y)
        gs.GraphSystem.draw_a_lot_trajectory_with_point(fig, [x1, x2], [y1, y2], [times])
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
        #id_person = db.exec_query_first(f"""select id from {cf.schema_name}.person""","[INFO] Get first id_person")

        # берутся его "фото" и отправляются на анализ лиц и результат сохраняется в бд с тем временем,
        # что указано в times в таблице appearence

        #times2 = db.exec_query_all(f"""select data_time from {cf.schema_name}.appearence where id_person == {id_person}""", "[INFO] Get time from appearence")
        # по таблице appearence достаем time по id человека, которого мы взяли
        #state_compar, good_x, good_y, bad_x, bad_y = AnalyzerData.compare_trajectories(x, y, times, times2)

        #AnalyzerData.get_graph_traj_with_points(x0_f, y0_f, x1_f, y1_f, s_x, s_y, width_w, height_w, times, ex, x, y, good_x, good_y)

    @staticmethod
    def start_demo1():
        #id_person = db.exec_query_first(f"""select id from {cf.schema_name}.person""","[INFO] Get first id_person")
        #times_move = db.exec_query_all(f"""select data_time, coord from {cf.schema_name}.appearence as ap join {cf.schema_name}.camera as c on ap.id_camera = c.id where id_person == {id_person}""", "[INFO] Get time from appearence")
        x = []
        y = []
        times = []
        #for i in range(len(times_move)):
            #x.append(times_move[1][0])
           # y.append(times_move[1][1])
            #times.append(times_move[0])
        fig = go.Figure()
        gs.GraphSystem.draw_a_lot_trajectory_with_point(fig,[x], [y], times)
        fig.show()

    @staticmethod
    def start_demo2():
        #базовые настройки поля
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
        # генерация траектории
        x, y, state, times, ex = AnalyzerData.get_generate_traj(x0_f, y0_f, x1_f, y1_f, s_x, s_y, starttime, endtime)
        field = [[x0_f, y0_f], [x1_f, y1_f]]
        #генерация камер
        cam = gr.Generator.generate_cameras_all_cell(x0_f, x1_f, y0_f, y1_f, s_x, s_y)
        id_person = 1
        # переменные где будут сохраняться проанализированные траектории
        x_a = []
        y_a = []
        times_a = []
        # путь тебе надо будет поменять
        path = r"C:\Users\user\PycharmProjects\CameraNavigationSummerPractic\resources\photos\1"
        db_helper = DBHelper(database='big_brother', user='postgres', password='1111', host='localhost')
        '''
        generator = rf.RecognizeFromFile(__db_helper)
        count_photos = 10 # количество фото в папке
        for i in range(len(x)):
            path_ = path + str(i % count_photos)
            id_p = generator.recognize(path_)
            if id_p == id_person:
                x_a.append(x[i])
                y_a.append(y[i])
                times_a.append(times[i])
        #рисуем
        fig = go.Figure()
        gs.GraphSystem.draw_location(fig, field, exits=[ex], cameras=cam) # локация, выход, камеры
        gs.GraphSystem.draw_chessboard(fig, x0_f, x1_f, y0_f, y1_f, s_x, s_y) # разметка в виде шахматной доски
        gs.GraphSystem.draw_a_lot_trajectory_with_point(fig, [x, x_a], [y, y_a], [times, times_a]) # траектории
        fig.update_layout(
            xaxis_range=[x0_f, x1_f],
            yaxis_range=[y0_f, y1_f],
            xaxis_autorange=False,
            yaxis_autorange=False,
            width=width_w,
            height=height_w,
        ) # настройки формата
        fig.show() # вывод'''

    @staticmethod
    def start_demo3(x0_f, y0_f, x1_f, y1_f, s_x, s_y, time_start, time_end, width_w, height_w):
        x, y, state, times, ex = AnalyzerData.get_generate_traj(x0_f, y0_f, x1_f, y1_f, s_x, s_y, time_start, time_end)
        x2, y2, state2 = gr.Generator.generation_trajectory(ex[0], ex[1], x0_f, x1_f, y0_f, y1_f, s_x, s_y, len(times))
        good_x = []; good_y = []; bad_x = []; bad_y = []
        for i in range(len(x)):
            flag = False
            for j in range(len(x2)):
                if x[i] == x2[j] and y[i] == y2[j]:
                    good_x.append(x[i])
                    good_y.append(y[i])
                    flag = True
                    break
            if flag:
                bad_x.append(x[i])
                bad_y.append(y[i])

        field = [[x0_f, y0_f], [x1_f, y1_f]]
        # генерация камер
        cam = gr.Generator.generate_cameras_all_cell(x0_f, x1_f, y0_f, y1_f, s_x, s_y)

        fig = go.Figure()
        gs.GraphSystem.draw_location(fig, field, exits=[ex], cameras=cam)  # локация, выход, камеры
        gs.GraphSystem.draw_cameras_rect(fig, cam, 0.01)
        gs.GraphSystem.draw_chessboard(fig, x0_f, x1_f, y0_f, y1_f, s_x, s_y)  # разметка в виде шахматной доски
        gs.GraphSystem.draw_a_lot_trajectory_with_point(fig, [x, x2], [y, y2], [times, times])  # траектории
        fig.update_layout(
            xaxis_range=[x0_f, x1_f],
            yaxis_range=[y0_f, y1_f],
            xaxis_autorange=False,
            yaxis_autorange=False,
            width=width_w,
            height=height_w,
        )  # настройки формата
        answ = AnalyzerData.analyze_trajectories([x], [y], [good_x], [good_y],
                                          [bad_x], [bad_y], [state], [state2])
        return fig.to_html(), answ  # вывод

    @staticmethod
    def start_demo4(x0_f, y0_f, x1_f, y1_f, s_x, s_y, time_start, time_end, width_w, height_w):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        print('caller name:', calframe[1][3])
        x, y, state, times, ex = AnalyzerData.get_generate_traj(x0_f, y0_f, x1_f, y1_f, s_x, s_y, time_start, time_end)
        # x2, y2, state2 = gr.Generator.generation_trajectory(ex[0], ex[1], x0_f, x1_f, y0_f, y1_f, s_x, s_y, len(times))
        good_x = []
        good_y = []
        bad_x = []
        bad_y = []
        # for i in range(len(x)):
        #     flag = False
        #     for j in range(len(x2)):
        #         if x[i] == x2[j] and y[i] == y2[j]:
        #             good_x.append(x[i])
        #             good_y.append(y[i])
        #             flag = True
        #             break
        #     if flag:
        #         bad_x.append(x[i])
        #         bad_y.append(y[i])

        field = [[x0_f, y0_f], [x1_f, y1_f]]
        # генерация камер
        cam = gr.Generator.generate_cameras_all_cell(x0_f, x1_f, y0_f, y1_f, s_x, s_y)

        x_a = []
        y_a = []
        times_a = []

        id_person = 1
        path = [r"D:\Python\CameraNavigation\CameraNavigationSummerPractic\resources\faces\1\1.jpg",
                r"D:\Python\CameraNavigation\CameraNavigationSummerPractic\resources\faces\1\3.jpg"]
        db_helper = DBHelper(database='big_brother', user='postgres', password='1111', host='localhost')

        generator = rf.RecognizeFromFile(db_helper)
        for i in range(len(x)):
            id_p = generator.recognize(path[i % len(path)])
            if id_person in id_p:
                x_a.append(x[i])
                y_a.append(y[i])
                times_a.append(times[i])
        joblib.dump(generator, 'generator.pkl')
        joblib.dump(cam, 'cam.pkl')
        fig = go.Figure()
        gs.GraphSystem.draw_location(fig, field, exits=[ex], cameras=cam)  # локация, выход, камеры
        gs.GraphSystem.draw_cameras_rect(fig, cam, 0.01)
        gs.GraphSystem.draw_chessboard(fig, x0_f, x1_f, y0_f, y1_f, s_x, s_y)  # разметка в виде шахматной доски
        gs.GraphSystem.draw_a_lot_trajectory_with_point(fig, [x, x_a], [y, y_a], [times, times_a])  # траектории
        fig.update_layout(
            xaxis_range=[x0_f, x1_f],
            yaxis_range=[y0_f, y1_f],
            xaxis_autorange=False,
            yaxis_autorange=False,
            width=width_w,
            height=height_w,
        )  # настройки формата
        answ = AnalyzerData.analyze_trajectories([x], [y], [good_x], [good_y],
                                                 [bad_x], [bad_y], [state], [state])
        return fig.to_html(), answ  # вывод


if __name__ == "__main__":
    AnalyzerData.start_demo4(0, 0, 20, 20, 1, 1, '12:00', '18:00', 600, 600)
