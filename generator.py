import random


def generate_exit(x0, x1, y0, y1, size_cell_x, size_cell_y):
    coord_axis = random.randint(0, 1)
    wall = random.randint(0, 1)
    if coord_axis == 0:
        coord1 = random.randint(x0, x1 - 1) + size_cell_x / 2
        coord2 = y0 if wall == 0 else y1
    else:
        coord2 = random.randint(y0, y1 - 1) + size_cell_y / 2
        coord1 = x0 if wall == 0 else x1
    return [coord1, coord2]


def append_x_y(x, y, x_ap, y_ap):
    x.append(x_ap)
    y.append(y_ap)


def generation_trajectory(x_exit, y_exit, x0_loc, x1_loc, y0_loc, y1_loc,
                          size_cell_x, size_cell_y, count_max_start, count_max_end,
                          early_start, early_end):
    count_max = random.randint(count_max_start, count_max_end)
    early = random.randint(early_start, early_end)
    x = [x_exit]
    y = [y_exit]
    x_now, y_now = get_half_step(x, y, x_exit, y_exit, x0_loc, x1_loc,
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
        append_x_y(x, y, x_now, y_now)
        count += 1
        if x1_exit == x_now and y1_exit == y_now:
            out = random.randint(0, 1)  # пойти на выход или нет?
            if out == 0:
                state = True
                break

        if count == count_max - early:
            state = get_out(x, y, x_now, y_now, count, count_max, x_exit, y_exit, x1_exit, y1_exit,
                            x0_loc, x1_loc, y0_loc, y1_loc, size_cell_x, size_cell_y)
            break
        if count == count_max:
            break
    return x, y, state


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
    append_x_y(x, y, x_now, y_now)
    return x_now, y_now


def get_out(x, y, x_now, y_now, count, count_max, x_exit, y_exit, x1_exit, y1_exit,
            x0_loc, x1_loc, y0_loc, y1_loc, size_cell_x, size_cell_y):
    while count <= count_max:
        if y_exit == y0_loc:  # вход снизу
            return get_out_down(x, y, x_now, y_now, count, count_max, x1_exit,
                                y0_loc, size_cell_x, size_cell_y)

        elif y_exit == y1_loc:  # вход сверху
            return get_out_up(x, y, x_now, y_now, count, count_max, x1_exit,
                              y1_loc, size_cell_x, size_cell_y)

        elif x_exit == x0_loc:  # вход слева
            return get_out_left(x, y, x_now, y_now, count, count_max, y1_exit,
                                x0_loc, size_cell_x, size_cell_y)

        else:  # вход справа
            return get_out_right(x, y, x_now, y_now, count, count_max, y1_exit,
                                 x1_loc, size_cell_x, size_cell_y)


def get_out_down(x, y, x_now, y_now, count, count_max, x1_exit,
                 y0_loc, size_cell_x, size_cell_y):
    while True:  # идем до упора вниз
        step = y_now - size_cell_y
        if step <= y0_loc:
            break
        y_now = step
        count += 1
        append_x_y(x, y, x_now, y_now)
        if count == count_max:
            return False
    return get_out_after_x(x, y, x_now, y_now, count, count_max, x1_exit, size_cell_x)


def get_out_up(x, y, x_now, y_now, count, count_max, x1_exit,
               y1_loc, size_cell_x, size_cell_y):
    while True:  # идем до упора вверх
        step = y_now + size_cell_y
        if step >= y1_loc:
            break
        y_now = step
        count += 1
        append_x_y(x, y, x_now, y_now)
        if count == count_max:
            return False
    return get_out_after_x(x, y, x_now, y_now, count, count_max, x1_exit, size_cell_x)


def get_out_after_x(x, y, x_now, y_now, count, count_max, x1_exit,
                    size_cell_x):
    if x_now > x1_exit:  # если выход слева, то идем влево
        while True:
            step = x_now - size_cell_x
            if step == x1_exit:
                break
            x_now = step
            count += 1
            append_x_y(x, y, x_now, y_now)
            if count == count_max:
                return False
        return True
    elif x_now < x1_exit:  # если выход справа, то идем вправо
        while True:
            step = x_now + size_cell_x
            if step == x1_exit:
                break
            x_now = step
            count += 1
            append_x_y(x, y, x_now, y_now)
            if count == count_max:
                return False
        return True
    elif x_now == x1_exit:
        return True


def get_out_left(x, y, x_now, y_now, count, count_max, y1_exit,
                 x0_loc, size_cell_x, size_cell_y):
    while True:  # идем до упора влево
        step = x_now - size_cell_x
        if step <= x0_loc:
            break
        x_now = step
        count += 1
        append_x_y(x, y, x_now, y_now)
        if count == count_max:
            return False
    return get_out_after_y(x, y, x_now, y_now, count, count_max, y1_exit, size_cell_y)


def get_out_right(x, y, x_now, y_now, count, count_max, y1_exit,
                  x1_loc, size_cell_x, size_cell_y):
    while True:  # идем до упора вправо
        step = x_now + size_cell_x
        if step >= x1_loc:
            break
        x_now = step
        count += 1
        append_x_y(x, y, x_now, y_now)
        if count == count_max:
            return False
    return get_out_after_y(x, y, x_now, y_now, count, count_max, y1_exit, size_cell_y)


def get_out_after_y(x, y, x_now, y_now, count, count_max, y1_exit,
                    size_cell_y):
    if y_now > y1_exit:  # если выход снизу, то идем вниз
        while True:
            step = y_now - size_cell_y
            if step == y1_exit:
                break
            y_now = step
            count += 1
            append_x_y(x, y, x_now, y_now)
            if count == count_max:
                return False
        return True
    elif y_now < y1_exit:  # если выход сверху, то идем вверх
        while True:
            step = y_now + size_cell_y
            if step == y1_exit:
                break
            y_now = step
            count += 1
            append_x_y(x, y, x_now, y_now)
            if count == count_max:
                return False
        return True
    elif y_now == y1_exit:
        return True


if __name__ == '__main__':
    pass