import random


class Generator:
    @staticmethod
    def generate_exit(x0, x1, y0, y1, size_cell_x, size_cell_y):
        coord_axis = random.randint(0, 1)
        wall = random.randint(0, 1)
        if coord_axis == 0:
            coord1 = random.randrange(x0, x1 - size_cell_x, size_cell_x) + size_cell_x / 2
            coord2 = y0 if wall == 0 else y1
        else:
            coord2 = random.randrange(y0, y1 - size_cell_y, size_cell_y) + size_cell_y / 2
            coord1 = x0 if wall == 0 else x1
        return [coord1, coord2]

    @staticmethod
    def append_x_y(x, y, x_ap, y_ap):
        x.append(x_ap)
        y.append(y_ap)

    @staticmethod
    def generation_trajectory(x_exit, y_exit, x0_loc, x1_loc, y0_loc, y1_loc,
                              size_cell_x, size_cell_y, count_max):
        early = random.randint(count_max // 100, count_max // 2)
        x = [x_exit]
        y = [y_exit]
        x_now, y_now = Generator.get_half_step(x, y, x_exit, y_exit, x0_loc, x1_loc,
                                     y0_loc, y1_loc, size_cell_x, size_cell_y)
        x1_exit = x_now
        y1_exit = y_now
        # 0 - лево, 1 - вверх, 2 - право, 3 - вниз

        count = 0
        state = None
        while True:
            direction = random.randint(0, 3)
            match direction:
                case 0:
                    step = x_now - size_cell_x
                    if step <= x0_loc:
                        continue
                    x_now = step
                case 1:
                    step = y_now + size_cell_y
                    if step >= y1_loc:
                        continue
                    y_now = step
                case 2:
                    step = x_now + size_cell_x
                    if step >= x1_loc:
                        continue
                    x_now = step
                case 3:
                    step = y_now - size_cell_y
                    if step <= y0_loc:
                        continue
                    y_now = step
            Generator.append_x_y(x, y, x_now, y_now)
            count += 1
            if x1_exit == x_now and y1_exit == y_now:
                out = random.randint(0, 1)  # пойти на выход или нет?
                if out == 0:
                    state = True
                    break

            if count == count_max - early:
                state = Generator.get_out(x, y, x_now, y_now, count, count_max, x_exit, y_exit, x1_exit, y1_exit,
                                x0_loc, x1_loc, y0_loc, y1_loc, size_cell_x, size_cell_y)
                break
            if count == count_max:
                break
        if state:
            Generator.append_x_y(x, y, x_exit, y_exit)
        return x, y, state

    @staticmethod
    def get_half_step(x, y, x_exit, y_exit, x0_loc, x1_loc, y0_loc, y1_loc, size_cell_x, size_cell_y):
        if y_exit == y0_loc:  # вход снизу
            x_now = x_exit
            y_now = y_exit + size_cell_y / 2
        elif y_exit == y1_loc:  # вход сверху
            x_now = x_exit
            y_now = y_exit - size_cell_y / 2
        elif x_exit == x0_loc:  # вход слева
            x_now = x_exit + size_cell_x / 2
            y_now = y_exit
        else:  # вход справа
            x_now = x_exit - size_cell_x / 2
            y_now = y_exit
        Generator.append_x_y(x, y, x_now, y_now)
        return x_now, y_now

    @staticmethod
    def get_out(x, y, x_now, y_now, count, count_max, x_exit, y_exit, x1_exit, y1_exit,
                x0_loc, x1_loc, y0_loc, y1_loc, size_cell_x, size_cell_y):
        while count <= count_max:
            if y_exit == y0_loc:  # вход снизу
                return Generator.get_out_down(x, y, x_now, y_now, count, count_max, x1_exit,
                                    y0_loc, size_cell_x, size_cell_y)

            elif y_exit == y1_loc:  # вход сверху
                return Generator.get_out_up(x, y, x_now, y_now, count, count_max, x1_exit,
                                  y1_loc, size_cell_x, size_cell_y)

            elif x_exit == x0_loc:  # вход слева
                return Generator.get_out_left(x, y, x_now, y_now, count, count_max, y1_exit,
                                    x0_loc, size_cell_x, size_cell_y)

            else:  # вход справа
                return Generator.get_out_right(x, y, x_now, y_now, count, count_max, y1_exit,
                                     x1_loc, size_cell_x, size_cell_y)

    @staticmethod
    def get_out_down(x, y, x_now, y_now, count, count_max, x1_exit,
                     y0_loc, size_cell_x, size_cell_y):
        while True:  # идем до упора вниз
            step = y_now - size_cell_y
            if step <= y0_loc:
                break
            y_now = step
            count += 1
            Generator.append_x_y(x, y, x_now, y_now)
            if count == count_max:
                return False
        return Generator.get_out_after_x(x, y, x_now, y_now, count, count_max, x1_exit, size_cell_x)

    @staticmethod
    def get_out_up(x, y, x_now, y_now, count, count_max, x1_exit,
                   y1_loc, size_cell_x, size_cell_y):
        while True:  # идем до упора вверх
            step = y_now + size_cell_y
            if step >= y1_loc:
                break
            y_now = step
            count += 1
            Generator.append_x_y(x, y, x_now, y_now)
            if count == count_max:
                return False
        return Generator.get_out_after_x(x, y, x_now, y_now, count, count_max, x1_exit, size_cell_x)

    @staticmethod
    def get_out_after_x(x, y, x_now, y_now, count, count_max, x1_exit,
                        size_cell_x):
        if x_now > x1_exit:  # если выход слева, то идем влево
            while True:
                step = x_now - size_cell_x

                x_now = step
                count += 1
                Generator.append_x_y(x, y, x_now, y_now)
                if step == x1_exit:
                    break
                if count == count_max:
                    return False
            return True
        elif x_now < x1_exit:  # если выход справа, то идем вправо
            while True:
                step = x_now + size_cell_x

                x_now = step
                count += 1
                Generator.append_x_y(x, y, x_now, y_now)
                if step == x1_exit:
                    break
                if count == count_max:
                    return False
            return True
        elif x_now == x1_exit:
            return True

    @staticmethod
    def get_out_left(x, y, x_now, y_now, count, count_max, y1_exit,
                     x0_loc, size_cell_x, size_cell_y):
        while True:  # идем до упора влево
            step = x_now - size_cell_x
            if step <= x0_loc:
                break
            x_now = step
            count += 1
            Generator.append_x_y(x, y, x_now, y_now)
            if count == count_max:
                return False
        return Generator.get_out_after_y(x, y, x_now, y_now, count, count_max, y1_exit, size_cell_y)

    @staticmethod
    def get_out_right(x, y, x_now, y_now, count, count_max, y1_exit,
                      x1_loc, size_cell_x, size_cell_y):
        while True:  # идем до упора вправо
            step = x_now + size_cell_x
            if step >= x1_loc:
                break
            x_now = step
            count += 1
            Generator.append_x_y(x, y, x_now, y_now)
            if count == count_max:
                return False
        return Generator.get_out_after_y(x, y, x_now, y_now, count, count_max, y1_exit, size_cell_y)

    @staticmethod
    def get_out_after_y(x, y, x_now, y_now, count, count_max, y1_exit,
                        size_cell_y):
        if y_now > y1_exit:  # если выход снизу, то идем вниз
            while True:
                step = y_now - size_cell_y

                y_now = step
                count += 1
                Generator.append_x_y(x, y, x_now, y_now)
                if step == y1_exit:
                    break
                if count == count_max:
                    return False
            return True
        elif y_now < y1_exit:  # если выход сверху, то идем вверх
            while True:
                step = y_now + size_cell_y

                y_now = step
                count += 1
                Generator.append_x_y(x, y, x_now, y_now)
                if step == y1_exit:
                    break
                if count == count_max:
                    return False
            return True
        elif y_now == y1_exit:
            return True

    @staticmethod
    def generate_cameras_all_cell(x0_field, x1_field, y0_field,
                                  y1_field, size_cell_x, size_cell_y):
        x = []
        y = []
        koef = {0: [0.15, 0.5], 1: [0.5, 0.85], 2: [0.85, 0.5], 3: [0.5, 0.15],
                4: [0.15, 0.15], 5: [0.15, 0.85], 6: [0.85, 0.85], 7: [0.85, 0.15]}
        # 0<-,1/\,2->,3\/,4<-\/,5<-/\,6/\->,7->\/
        y_step = y0_field
        while y_step < y1_field:
            x_step = x0_field
            while x_step < x1_field:
                direction = random.randint(0, len(koef) - 1)
                x.append(x_step + size_cell_x * koef[direction][0])
                y.append(y_step + size_cell_y * koef[direction][1])
                x_step += size_cell_x
            y_step += size_cell_y
        return x, y

    @staticmethod
    def generate_times(start_time, end_time, inter_time_start, inter_time_end, start_date, end_date):
        """Нужно использовать формат 11:00, (минуты), 2023-03-01. Генерируется какое-то число
        и генерируются точки времени."""
        year_start, month_start, day_start = start_date.split("-")
        year_end, month_end, day_end = end_date.split("-")
        random_year = random.randint(int(year_start), int(year_end))
        random_month = random.randint(int(month_start), int(month_end))
        random_day = random.randint(int(day_start), int(day_end))
        random_date = str(random_year) + "-" + str(random_month) + "-" + str(random_day)
        hour_start, minute_start = start_time.split(":")
        hour_end, minute_end = end_time.split(":")
        hour_end = int(hour_end)
        minute_end = int(minute_end)
        hour_now = int(hour_start)
        minute_now = int(minute_start)
        times = []
        while True:
            if len(str(minute_now)) == 1:
                mn = "0" + str(minute_now)
            else:
                mn = str(minute_now)
            times.append(random_date + " " + str(hour_now) + ":" + mn)

            step = random.randint(inter_time_start, inter_time_end)
            hour_now += (minute_now + step) // 60
            minute_now = (minute_now + step) % 60
            if hour_now > hour_end and minute_now > minute_end:
                break
        return times


if __name__ == '__main__':
    # print(generate_times("11:00", "14:00", 1, 20, "2002-10-2", "2002-10-3"))
    pass
