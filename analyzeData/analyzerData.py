import os
import random

from plotly import graph_objs as go

import analyzeData.generator as gr
import analyzeData.graphsystem as gs
#import CameraNavigationSummerPractic.database.db as db
#import CameraNavigationSummerPractic.database.config as cf
from trash.recognizer import ReIdRecognizer
from DBHelper import DBHelper


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
    def analyze_trajectories(x_mas, y_mas, good_x_mas, good_y_mas, bad_x_mas, bad_y_mas, states_gen, states_an,
                             state_an, point_not_exit1, point_not_exit2, point_not_exit3):
        count_com = 0
        count_all = 0
        for i in range(len(x_mas)):
            count_all += len(x_mas[i])
        for i in range(len(good_x_mas)):
            count_com += len(good_x_mas[i])
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
                  f"Сколько НЕ вышло из здания (проанализировано): {len(states_an) - count_go_out_an}\n"]
        if not states_an[0]:
            answer.append(f"Последний раз человек 1 был замечен:{point_not_exit1}")
        if not states_an[1]:
            answer.append(f"Последний раз человек 2 был замечен:{point_not_exit2}")
        if not states_an[2]:
            answer.append(f"Последний раз человек 3 был замечен:{point_not_exit3}")
        answer.append(f"Процент совпадения: {proc_com}%\n")
        answer.append(f"Не совпавшие координаты: \n")
        for i in range(len(points)):
            answer.append(f"{i+1}: {points[i]}\n")
        return answer


    @staticmethod
    def get_generate_traj(x0, y0, x1, y1, size_x, size_y, start_time,
                          end_time, ex=None):
        if ex is None:
            ex = gr.Generator.generate_exit(x0, x1, y0, y1, size_x, size_y)
        times = gr.Generator.generate_times(start_time, end_time, 1,
                                            5, "2024-07-08",
                                            "2024-07-08")
        x, y, state = gr.Generator.generation_trajectory(ex[0], ex[1], x0, x1, y0, y1, size_x, size_y, len(times)-2)
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
        generator = rf.RecognizeFromFile(db_helper)
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

        x2 = [x[0]]
        y2 =[y[0]]
        times2 = []

        directory = r"D:\practice\1"
        file_paths = []
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_paths.append(file_path)
        bad_photo = []

        good_x = []; good_y = []; bad_x = []; bad_y = []
        for i in range(len(x)):
            if i == 0:
                continue
            r = random.randrange(1, 8, 1)
            if r != 1:
                x2.append(x[i])
                y2.append(y[i])
                times2.append(times[i])
                good_x.append(x[i])
                good_y.append(y[i])
            else:
                bad_x.append(x[i])
                bad_y.append(y[i])
                bad_photo.append(file_paths[i % len(file_paths)][len(directory):])


        state2 = x[-1] == x2[-1]
        #x2, y2, state2 = gr.Generator.generation_trajectory(ex[0], ex[1], x0_f, x1_f, y0_f, y1_f, s_x, s_y, len(times))
        #good_x = []; good_y = []; bad_x = []; bad_y = []
        '''
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
                bad_y.append(y[i])'''

        field = [[x0_f, y0_f], [x1_f, y1_f]]
        # генерация камер
        cam = gr.Generator.generate_cameras_all_cell(x0_f, x1_f, y0_f, y1_f, s_x, s_y)

        fig = go.Figure()
        gs.GraphSystem.draw_location(fig, field, exits=[ex])  # локация, выход, камеры
        gs.GraphSystem.draw_cameras_rect(fig, cam, 0.01)
        gs.GraphSystem.draw_chessboard(fig, x0_f, x1_f, y0_f, y1_f, s_x, s_y)  # разметка в виде шахматной доски
        gs.GraphSystem.draw_a_lot_trajectory_with_point(fig, [x, x2], [y, y2], [times, times2],
                                                        ["Сгенерированная траектория", "Проанализированная траектория"],
                                                        ["Сгенерированное движение", "Проанализированное движение"])  # траектории
        fig.update_layout(
            xaxis_range=[x0_f, x1_f],
            yaxis_range=[y0_f, y1_f],
            xaxis_autorange=False,
            yaxis_autorange=False,
            width=width_w,
            height=height_w,
        )  # настройки формата
        answ = AnalyzerData.analyze_trajectories([x], [y], [good_x], [good_y],
                                          [bad_x], [bad_y], [state], [state2], state2, (x2[-1], y2[-1]))
        return fig.to_html(), answ, bad_photo  # вывод

    @staticmethod
    def start_demo4(x0_f, y0_f, x1_f, y1_f, s_x, s_y, time_start, time_end, width_w, height_w):
        x, y, state, times, ex = AnalyzerData.get_generate_traj(x0_f, y0_f, x1_f, y1_f, s_x, s_y, time_start, time_end)
        x2, y2, state2, times2, ex2 = AnalyzerData.get_generate_traj(x0_f, y0_f, x1_f, y1_f, s_x, s_y, time_start, time_end, ex)
        x3, y3, state3, times3, ex3 = AnalyzerData.get_generate_traj(x0_f, y0_f, x1_f, y1_f, s_x, s_y, time_start, time_end, ex)
        directory = r'D:\Python\CameraNavigation\CameraNavigationSummerPractic\resources\sequences\babka\\'
        directory2 = r'D:\Python\CameraNavigation\CameraNavigationSummerPractic\resources\sequences\Muzhik\\'
        directory3 = r'D:\Python\CameraNavigation\CameraNavigationSummerPractic\resources\sequences\RedLady\\'

        good_x = []
        good_y = []
        bad_x = []
        bad_y = []
        good_x2 = []
        good_y2 = []
        bad_x2 = []
        bad_y2 = []
        good_x3 = []
        good_y3 = []
        bad_x3 = []
        bad_y3 = []

        field = [[x0_f, y0_f], [x1_f, y1_f]]
        # генерация камер
        cam = gr.Generator.generate_cameras_all_cell(x0_f, x1_f, y0_f, y1_f, s_x, s_y)

        x_a = []
        y_a = []
        times_a = []
        x_a2 = []
        y_a2 = []
        times_a2 = []
        x_a3 = []
        y_a3 = []
        times_a3 = []

        file_paths = []
        file_names = []
        for root, _, files in os.walk(directory):
            for file in files:
                # D:\Python\CameraNavigation\CameraNavigationSummerPractic\seq_1\\Screenshot_368.jpg
                file_path = os.path.join(root, file)
                file_paths.append(file_path)
                name = file_path.split('\\')[-3]
                print(file_path)
                file_names.append(name)
        file_paths2 = []
        file_names2 = []
        for root, _, files in os.walk(directory2):
            for file in files:
                # D:\Python\CameraNavigation\CameraNavigationSummerPractic\seq_1\\Screenshot_368.jpg
                file_path2 = os.path.join(root, file)
                file_paths2.append(file_path2)
                name = file_path2.split('\\')[-3]
                print(file_path2)
                file_names2.append(name)
        file_paths3 = []
        file_names3 = []
        for root, _, files in os.walk(directory3):
            for file in files:
                # D:\Python\CameraNavigation\CameraNavigationSummerPractic\seq_1\\Screenshot_368.jpg
                file_path3 = os.path.join(root, file)
                file_paths3.append(file_path3)
                name = file_path3.split('\\')[-3]
                print(file_path3)
                file_names3.append(name)
        print(file_names)
        reco = ReIdRecognizer()
        # Надо рандомно добавлять людей в процессе
        reco.entrance_recognize(r'D:\Python\CameraNavigation\CameraNavigationSummerPractic\resources\photos\entrance\babka.jpg', 'babka')
        reco.entrance_recognize(r'D:\Python\CameraNavigation\CameraNavigationSummerPractic\resources\photos\entrance\Muzhik.jpg',
                                'Muzhik')
        reco.entrance_recognize(r'D:\Python\CameraNavigation\CameraNavigationSummerPractic\resources\photos\entrance\RedLady.jpg',
                                'RedLady')


        bad_photo = []
        db_helper = DBHelper(database='big_brother', user='postgres', password='1111', host='localhost')

        for i in range(len(x)):
            id_p = reco.recognize(file_paths[i % len(file_paths)])
            print(file_names[i % len(file_paths)], id_p)
            if file_names[i % len(file_paths)] in id_p:
                x_a.append(x[i])
                y_a.append(y[i])
                times_a.append(times[i])
                good_x.append(x[i])
                good_y.append(y[i])
            else:
                bad_x.append(x[i])
                bad_y.append(y[i])
                bad_photo.append(file_paths[i % len(file_paths)][len(directory) + 1:])
                times_a.append('30')
                good_x.append('30')
                good_y.append('30')

        for i in range(len(x2)):
            id_p = reco.recognize(file_paths2[i % len(file_paths2)])
            print(file_names2[i % len(file_paths2)], id_p)
            if file_names2[i % len(file_paths2)] in id_p:
                x_a2.append(x2[i])
                y_a2.append(y2[i])
                times_a2.append(times2[i])
                good_x2.append(x2[i])
                good_y2.append(y2[i])
            else:
                bad_x2.append(x2[i])
                bad_y2.append(y2[i])
                bad_photo.append(file_paths2[i % len(file_paths2)][len(directory2) + 1:])
                times_a2.append('30')
                good_x2.append('30')
                good_y2.append('30')

        bias = 0
        for i in range(len(x3)):
            id_p = reco.recognize(file_paths3[i % len(file_paths3)])
            print(file_names3[i % len(file_paths3)], id_p)
            if file_names3[i % len(file_paths3)] in id_p:
                x_a3.append(x3[i])
                y_a3.append(y3[i])
                times_a3.append(times3[i])
                good_x3.append(x3[i])
                good_y3.append(y3[i])
                continue
            else:
                bad_x3.append(x3[i])
                bad_y3.append(y3[i])
                bad_photo.append(file_paths3[i % len(file_paths3)][len(directory3) + 1:])
                x_a3.append(30)
                y_a3.append(30)
                times_a3.append('30')
                good_x3.append('30')
                good_y3.append('30')
        reco.knn.plot_vectors()
        state_a = len(x_a) != 0 and x[-1] == x_a[-1] and y[-1] == y_a[-1]
        state_a2 = len(x_a2) != 0 and x2[-1] == x_a2[-1] and y2[-1] == y_a2[-1]
        state_a3 = len(x_a3) != 0 and x3[-1] == x_a3[-1] and y3[-1] == y_a3[-1]
        fig = go.Figure()
        gs.GraphSystem.draw_location(fig, field, exits=[ex])  # локация, выход, камеры
        gs.GraphSystem.draw_cameras_rect(fig, cam, 0.01)
        gs.GraphSystem.draw_chessboard(fig, x0_f, x1_f, y0_f, y1_f, s_x, s_y)  # разметка в виде шахматной доски
        gs.GraphSystem.draw_a_lot_trajectory_with_point(fig, [x, x_a, x2, x_a2, x3, x_a3], [y, y_a, y2, y_a2, y3, y_a3], [times, times_a, times2, times_a2, times3, times_a3],
                                                        ["Сгенерированная траектория 1", "Проанализированная траектория 1", "Сгенерированная траектория 2", "Проанализированная траектория 2", "Сгенерированная траектория 3", "Проанализированная траектория3"],
                                                        ["Сгенерированное движение 1", "Проанализированное движение 1", "Сгенерированное движение 2", "Проанализированное движение 2", "Сгенерированное движение 3", "Проанализированное движение 3"],
                                                        ['#0a3cc3', '#c31a0a', '#0a91c3', '#c3640a', '#550ac3', '#e7714a'],
                                                        ['#0a246b', '#6c0e05', '#094961', '#5c3007', '#29075c', '#c74b22'])  # траектории
        fig.update_layout(
            xaxis_range=[x0_f, x1_f],
            yaxis_range=[y0_f, y1_f],
            xaxis_autorange=False,
            yaxis_autorange=False,
            width=width_w,
            height=height_w,
        )  # настройки формата
        answ = AnalyzerData.analyze_trajectories([x, x2, x3], [y, y2, y3], [good_x, good_x2, good_x3], [good_y, good_y2, good_y3],
                                                 [bad_x, bad_x2, bad_x3], [bad_y, bad_y2, bad_y3], [state, state2, state3], [state_a, state_a2, state_a3], state2, (x_a[-1], y_a[-1]),
                                                 (x_a2[-1], y_a2[-1]), (x_a3[-1], y_a3[-1]))
        return fig.to_html(), answ, bad_photo   # вывод'''


if __name__ == "__main__":
    AnalyzerData.start_demo4(0, 0, 20, 20, 1, 1, '8:00', '12:00', 20, 20)


