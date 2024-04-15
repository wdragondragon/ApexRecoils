def merge(time_points, x, y, step):
    current_step = 0
    current_step_num = current_step * step
    time_points_merge = []
    x_merge = []
    y_merge = []
    for i, time_point in enumerate(time_points):
        if time_point >= current_step_num:
            time_points_merge.append(current_step_num)
            x_merge.append(0)
            y_merge.append(0)
            current_step += 1
            current_step_num = current_step * step

        x_merge[current_step - 1] = x_merge[current_step - 1] + x[i]
        y_merge[current_step - 1] = y_merge[current_step - 1] + y[i]

    print(x_merge)
    print(y_merge)
    print(time_points_merge)


def merge_x_y(x, y, time_points_x, time_points_y):
    new_x = []
    new_y = []
    new_time_points = []

    x_length = len(time_points_x)
    y_length = len(time_points_y)

    xi = 0
    yi = 0
    while xi < x_length or yi < y_length:
        if xi >= x_length:
            new_y.append(y[yi])
            new_x.append(0)
            new_time_points.append(time_points_y[yi])
            yi += 1
            continue
        if yi >= y_length:
            new_x.append(x[xi])
            new_y.append(0)
            new_time_points.append(time_points_x[xi])
            xi += 1
            continue

        if time_points_x[xi] == time_points_y[yi]:
            new_x.append(x[xi])
            new_y.append(y[yi])
            new_time_points.append(time_points_x[xi])
            xi += 1
            yi += 1
        elif time_points_x[xi] < time_points_y[yi]:
            new_x.append(x[xi])
            new_y.append(0)
            new_time_points.append(time_points_x[xi])
            xi += 1
        elif time_points_x[xi] > time_points_y[yi]:
            new_y.append(y[yi])
            new_x.append(0)
            new_time_points.append(time_points_y[yi])
            yi += 1
    print(new_time_points)
    print(new_x)
    print(new_y)
    return new_time_points, new_x, new_y


time_points = [0, 3, 12, 16, 25, 28, 35, 41, 47, 58, 60, 67, 77, 82, 92, 99, 104, 112, 118, 129, 132, 142, 149, 154,
               162, 167, 171, 180, 185, 191, 197, 207, 216, 220, 233, 240, 244, 257, 264, 268, 277, 290, 295, 307, 313,
               319, 329, 337, 343, 354, 361, 375, 380, 387, 395, 404, 408, 417, 425, 434, 446, 450, 460, 466, 475, 490,
               494, 500, 514, 518, 528, 537, 542, 554, 561, 565, 575, 578, 586, 597, 601, 613, 623, 628, 635, 645, 654,
               658, 669, 678, 683, 695, 707, 718, 723, 733, 744, 747, 760, 770, 774, 785, 794, 802, 811, 819, 829, 835,
               848, 854, 871, 883, 890, 897, 913, 923, 928, 944, 954, 958, 972, 975, 988, 993, 1002, 1011, 1017, 1029,
               1036, 1041, 1054, 1060, 1068, 1082, 1087, 1094, 1106, 1121, 1123, 1129, 1143, 1160, 1164, 1170, 1179,
               1187, 1193, 1206, 1207, 1219, 1222, 1230, 1241, 1245, 1256, 1260, 1269, 1283, 1290, 1294, 1305, 1317,
               1331, 1346, 1351, 1357, 1361, 1372, 1383, 1388, 1396, 1402, 1412, 1418, 1428, 1430, 1448, 1451, 1462,
               1466, 1472, 1484, 1488, 1503, 1508, 1519, 1527, 1530, 1546, 1555, 1563, 1568, 1578, 1589, 1602, 1619,
               1637, 1638, 1660, 1669]
x = [-1, 0, -1, 0, -1, -1, -1, -1, -1, -1, -2, 1, 1, 1, 0, 2, 0, 1, 0, 0, 2, 1, 2, 1, 1, 2, 1, -1, 1, -3, 1, -2, -4, -2,
     -2, -2, -1, -1, -3, -2, -1, -1, -2, 0, -1, 0, -1, -1, -2, -1, -2, -2, -2, -2, -2, 0, -1, 0, 0, -2, -2, 2, -2, 4,
     -1, 5, 1, 2, 3, 2, 1, 4, 2, 2, 3, 2, 3, 2, 1, 3, 2, 2, 3, -1, 3, 1, -4, -1, -2, -5, -2, -2, -2, 2, -5, 2, 2, 3, 2,
     2, 2, -1, 1, -2, -2, -2, -3, -2, -2, -2, -2, -2, -2, 0, 0, 3, 1, 0, 3, -1, -2, 4, -2, 5, 1, 5, 2, 3, 6, 3, 4, 2, 3,
     2, -2, 1, -1, 2, 0, 2, 2, 2, -1, 4, 4, -2, 5, 1, 0, -2, 1, -1, -3, 0, -1, -6, -1, -2, -5, -2, -2, -2, -1, -5, -2,
     -4, -3, -4, -5, -3, 0, -3, -2, -2, -1, -2, -2, -1, -2, 0, -2, -2, -2, -2, 0, -2, 3, -2, -1, 1, 4, 1, 2, 2, 1, -1,
     -2, -2, -2, 1]
y = [-1, 0, -1, 3, -1, 7, 1, 7, 2, 2, 6, 2, 5, 2, 2, 6, 3, 2, 2, 2, 0, 2, 4, 2, 2, 3, 2, 1, 2, 6, 2, 4, 6, 4, 4, 2, 6,
     4, 12, 6, 6, 10, 6, 5, 3, 8, 6, 9, 6, 5, 6, 6, 3, 6, 5, 3, 4, 4, 3, 3, 4, 3, 5, -2, 6, 6, 4, 5, 6, 6, 5, 5, 5, 6,
     3, 6, -1, 6, 4, 3, 4, 4, 3, -2, 3, 2, 4, 2, 2, 2, 2, 2, 2, 3, 2, 3, 5, 4, 3, 3, 3, 4, -1, 4, -6, 3, -8, 3, -8, 3,
     3, -6, 3, 3, 3, -2, 3, 2, -1, 2, 2, -4, 2, 4, 2, 5, 2, 2, 3, 2, 1, -6, 1, 0, -8, 0, 0, 0, -4, 0, 0, 0, -2, 1, 1, 0,
     1, 1, 3, 2, 1, 1, 2, 1, 1, 0, 2, 1, 0, 1, 1, 1, 0, -2, 1, -4, 1, 1, -4, 2, -4, 0, -4, -1, -1, 0, 3, -1, 0, 4, -1,
     -1, 0, 0, -2, -2, -2, -2, -2, -2, -3, -2, -1, -2, 3, 4, -1, 4, 2, -2]
merge(time_points, x, y, 27.5)

t_x = [1, 3, 6]
x = [1, 3, 4]
t_y = []
y = []

merge_x_y(x, y, t_x, t_y)
