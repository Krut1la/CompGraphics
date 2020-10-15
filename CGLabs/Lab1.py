"""
Prog:   Lab1.py

Auth:   Oleksii Krutko, IO-z91

Desc:   Computer graphics Lab 1. 2020

"""

from math import *
import graphics as glib
import matplotlib.pyplot as plt
import turtle


class SubWindow(object):
    def __init__(self):
        self.name = ''
        self.zero_point = (0.0, 0.0)
        self.x_axis_name = ''
        self.y_axis_name = ''


class Engine(object):
    def __init__(self, window_width, window_height, background_color, perspective_depth):
        self.window_width = window_width
        self.window_height = window_height
        self.background_color = background_color

        self.sub_windows = (SubWindow(), SubWindow(), SubWindow(), SubWindow())

    def setup_sub_window(self, sub_window_number, name, zero_point, x_axis_name, y_axis_name):
        self.sub_windows[sub_window_number - 1].name = name
        self.sub_windows[sub_window_number - 1].zero_point = zero_point
        self.sub_windows[sub_window_number - 1].x_axis_name = x_axis_name
        self.sub_windows[sub_window_number - 1].y_axis_name = y_axis_name

    def transform_point_perspective(self, point_original, perspective_center):
        point = [perspective_center[0] + (point_original[0] - perspective_center[0]) / (
                1 - point_original[2] / perspective_center[2]),
                 perspective_center[1] + (point_original[1] - perspective_center[1]) / (
                         1 - point_original[2] / perspective_center[2])]

        return point

    def draw_points(self, sub_window, points, color):
        return 0

    def draw_line(self, sub_window, points, color):
        return 0

    def draw_polygon(self, sub_window, points, outline_color, fill_color):
        return 0

    def show(self):
        return 0


class MathPlotLibEngine(Engine):
    def __init__(self, window_width, window_height, background_color, perspective_depth):
        super(MathPlotLibEngine, self).__init__(window_width, window_height, background_color, perspective_depth)
        # plt.axis([0.0, self.window_width, self.window_height, 0.0])

        self.__fig, self.__axs = plt.subplots(2, 2)

    def setup_sub_window(self, sub_window_number, name, zero_point, x_axis_name, y_axis_name):
        super(MathPlotLibEngine, self).setup_sub_window(sub_window_number, name, zero_point, x_axis_name, y_axis_name)
        self.__axs[(sub_window_number - 1) // 2, (sub_window_number - 1) % 2].set_title("test")

    def draw_points(self, sub_window, points, color):
        x = []
        y = []
        for point in points:
            x.append(point[0])
        for point in points:
            y.append(point[1])

        self.__axs[(sub_window - 1) // 2, (sub_window - 1) % 2].plot(x, y, color=color)

        return 0

    def draw_line(self, sub_window, points, color):
        self.__axs[(sub_window - 1) // 2, (sub_window - 1) % 2].plot([points[0][0], points[1][0]],
                                                                     [points[0][1], points[1][1]], color=color)

        return 0

    def draw_polygon(self, sub_window, points, outline_color, fill_color):
        # polygon = plt.Polygon(points, True)
        x = []
        y = []
        for point in points:
            x.append(point[0])
        for point in points:
            y.append(point[1])

        self.__axs[(sub_window - 1) // 2, (sub_window - 1) % 2].fill(x, y, facecolor=fill_color,
                                                                     edgecolor=outline_color)
        return 0

    def show(self):
        plt.show()
        return 0


class GraphicsEngine(Engine):
    def __init__(self, window_width, window_height, background_color, perspective_depth):
        super(GraphicsEngine, self).__init__(window_width, window_height, background_color, perspective_depth)
        self.win = glib.GraphWin("Lab 1. Task 1", window_width, window_height)
        self.win.setBackground(background_color)

    def draw_points(self, sub_window, points, color):
        for point in points:
            p = glib.Point(self.sub_windows[sub_window - 1].zero_point[0] + point[0],
                           self.sub_windows[sub_window - 1].zero_point[1] + point[1])
            p.draw(self.win)

    def draw_line(self, sub_window, points, color):
        line = glib.Line(
            glib.Point(self.sub_windows[sub_window - 1].zero_point[0] + points[0][0],
                       self.sub_windows[sub_window - 1].zero_point[1] + points[0][1]),
            glib.Point(self.sub_windows[sub_window - 1].zero_point[0] + points[1][0],
                       self.sub_windows[sub_window - 1].zero_point[1] + points[1][1]))

        line.setFill(color)
        line.setWidth(3)
        line.draw(self.win)

    def draw_polygon(self, sub_window, points, outline_color, fill_color):
        poly_points = []
        for p in points:
            poly_points.append(glib.Point(self.sub_windows[sub_window - 1].zero_point[0] + p[0],
                                          self.sub_windows[sub_window - 1].zero_point[1] + p[1]))

        polygon = glib.Polygon(poly_points)
        polygon.setOutline(outline_color)
        polygon.setFill(fill_color)
        polygon.setWidth(3)
        polygon.draw(self.win)

        return 0

    def show(self):
        self.win.getMouse()
        self.win.close()
        return 0


class TurtleEngine(Engine):
    def __init__(self, window_width, window_height, background_color, perspective_depth):
        super(TurtleEngine, self).__init__(window_width, window_height, background_color, perspective_depth)

        turtle.screensize(self.window_width, self.window_height)
        turtle.radians()
        turtle.penup()

    def draw_line(self, sub_window, points, color):
        moved_point_from = [points[0][0] - self.window_width / 2, points[0][1] - self.window_height / 2]
        moved_point_to = [points[1][0] - self.window_width / 2, points[1][1] - self.window_height / 2]

        length = sqrt((moved_point_to[0] - moved_point_from[0]) * (moved_point_to[0] - moved_point_from[0])
                      + (moved_point_to[1] - moved_point_from[1]) * (moved_point_to[1] - moved_point_from[1]))
        angle = acos((moved_point_to[0] - moved_point_from[0]) / length)
        if moved_point_to[1] < moved_point_from[1]:
            angle = 2 * pi - angle

        turtle.goto(moved_point_from[0], moved_point_from[1])
        turtle.setheading(0)
        turtle.color(color)
        turtle.pendown()
        turtle.left(angle)
        turtle.forward(length)
        turtle.penup()

    def draw_polygon(self, sub_window, points, outline_color, fill_color):
        turtle.begin_fill()
        turtle.fillcolor(fill_color)

        i = 0
        while i < len(points) - 1:
            self.draw_line(sub_window, [points[i], points[i + 1]], outline_color)
            i = i + 1

        self.draw_line(sub_window, [points[i], points[0]], outline_color)

        turtle.end_fill()

    def show(self):
        # turtle.showturtle()
        return 0


def draw_task_one_figure_one(engine, width, height, depth_step, count, inner_color, outer_color):
    def draw_with_perspective(sub_window_num, perspective_depth):
        engine.setup_sub_window(1, "Triangle - filled", (0.0, 0.0), "", "")
        engine.setup_sub_window(2, "Triangle - outlined", (engine.window_width/2, 0.0), "", "")
        engine.setup_sub_window(3, "Square - filled", (0.0, engine.window_height/2), "", "")
        engine.setup_sub_window(4, "Square - outlined", (engine.window_width/2, engine.window_height/2), "", "")

        perspective_center = (width / 2, height / 2, perspective_depth)

        for i in range(0, count):
            p_top = engine.transform_point_perspective(
                (width / 2, 0.0, i * depth_step), perspective_center)
            p_bottom_left = engine.transform_point_perspective(
                (0.0, height, i * depth_step), perspective_center)
            p_bottom_right = engine.transform_point_perspective(
                (width, height, i * depth_step), perspective_center)

            if i == 0 or i == count - 1:
                color = outer_color
            else:
                color = inner_color

            engine.draw_polygon(sub_window_num, [p_top, p_bottom_left, p_bottom_right], color,
                                glib.color_rgb(255, 255, 190))

    draw_with_perspective(1, -30)
    draw_with_perspective(2, -100)


def draw_task_one_figure_two(engine, width, height, depth_step, count, inner_color, outer_color):
    def draw_with_perspective(sub_window_num, perspective_depth):
        engine.setup_sub_window(1, "Triangle - filled", (0.0, 0.0), "", "")
        engine.setup_sub_window(2, "Triangle - outlined", (engine.window_width / 2, 0.0), "", "")
        engine.setup_sub_window(3, "Square - filled", (0.0, engine.window_height / 2), "", "")
        engine.setup_sub_window(4, "Square - outlined", (engine.window_width / 2, engine.window_height / 2), "", "")

        perspective_center = (width / 2, height / 2,
                              perspective_depth)

        for i in range(0, count):
            p_top_left = engine.transform_point_perspective((0.0, 0.0, i * depth_step), perspective_center)
            p_top_right = engine.transform_point_perspective((width, 0.0, i * depth_step), perspective_center)
            p_bottom_left = engine.transform_point_perspective((0.0, height, i * depth_step), perspective_center)
            p_bottom_right = engine.transform_point_perspective((width, height, i * depth_step), perspective_center)

            if i == 0 or i == count - 1:
                color = outer_color
            else:
                color = inner_color

            engine.draw_line(sub_window_num, [p_top_left, p_top_right], color)
            engine.draw_line(sub_window_num, [p_top_left, p_bottom_left], color)
            engine.draw_line(sub_window_num, [p_bottom_left, p_bottom_right], color)
            engine.draw_line(sub_window_num, [p_top_right, p_bottom_right], color)

    draw_with_perspective(3, -30)
    draw_with_perspective(4, -100)


def draw_task_two(engine):
    engine.setup_sub_window(1, "Sin", (0.0, 0.0), "", "")
    engine.setup_sub_window(2, "Tan", (engine.window_width / 2, 0.0), "", "")
    engine.setup_sub_window(3, "Ctan", (0.0, engine.window_height / 2), "", "")
    engine.setup_sub_window(4, "Sum", (engine.window_width / 2, engine.window_height / 2), "", "")

    def with_options(sub_window, monochrome, lines):
        def rotate_point(cx, cy, x, y, rot_angle):
            s = sin(rot_angle)
            c = cos(rot_angle)

            origin_x = x - cx
            origin_y = y - cy
            new_x = origin_x * c - origin_y * s
            new_y = origin_x * s + origin_y * c
            return new_x + cx, new_y + cy

        width = 200.0
        height = 200.0

        outline_colors = ['blue', 'green', 'red', 'yellow']
        fill_colors = ['yellow', 'red', 'green', 'blue']

        center_point = (engine.window_width / 2, engine.window_height / 2)

        shift = height / 32

        angle = 0.0
        for i in range(0, 4):
            # set points

            point_left = rotate_point(center_point[0], center_point[1], center_point[0] + width / 2,
                                      center_point[1] - shift + height / 5, angle)
            point_right = rotate_point(center_point[0], center_point[1], center_point[0] + width / 2,
                                       center_point[1] - shift - height / 5, angle)

            if monochrome:
                outline_color = 'black'
                fill_color = 'white'
            else:
                outline_color = outline_colors[i]
                fill_color = fill_colors[i]

            if lines:
                engine.draw_line(sub_window, [center_point, point_left], outline_color)
                engine.draw_line(sub_window, [point_left, point_right], outline_color)
                engine.draw_line(sub_window, [point_right, center_point], outline_color)
            else:
                engine.draw_polygon(sub_window, [center_point, point_left, point_right], outline_color, fill_color)

            angle = angle + pi / 2

    with_options(1, True, False)
    with_options(2, True, True)
    with_options(3, False, True)
    with_options(4, False, False)

def draw_task_three(engine, width, height):
    engine.setup_sub_window(1, "Sin", (0.0, 0.0), "", "")
    engine.setup_sub_window(2, "Tan", (engine.window_width / 2, 0.0), "", "")
    engine.setup_sub_window(3, "Ctan", (0.0, engine.window_height / 2), "", "")
    engine.setup_sub_window(4, "Sum", (engine.window_width / 2, engine.window_height / 2), "", "")

    # Student number
    a = 10.0

    def func_one(arg_x):
        return a * 0.1 * sin(arg_x)

    def func_two(arg_x):
        return a * 0.1 * tan(arg_x)

    def func_three(arg_x):
        return a * 0.1 * cos(arg_x) / sin(arg_x)

    color_one = 'red'
    color_two = 'green'
    color_three = 'blue'

    x_min = 0.0
    x_max = 20.0
    y_abs_max = 2.0

    x = x_min
    step = 0.01

    points_one = []
    points_two = []
    points_three = []

    while x <= x_max:
        points_one.append((x, func_one(x)))

        try:
            y = func_two(x)
            if abs(y) < y_abs_max:
                points_two.append((x, func_two(x)))
        except ZeroDivisionError:
            pass

        try:
            y = func_three(x)
            if abs(y) < y_abs_max:
                points_three.append((x, func_three(x)))
        except ZeroDivisionError:
            pass

        x = x + step

    engine.draw_points(1, points_one, color_one)
    engine.draw_points(2, points_two, color_two)
    engine.draw_points(3, points_three, color_three)
    engine.draw_points(4, points_one, color_one)
    engine.draw_points(4, points_two, color_two)
    engine.draw_points(4, points_three, color_three)


def main():
    # engine = MathPlotLibEngine(640, 480, glib.color_rgb(255, 255, 255), -30)
    engine = GraphicsEngine(640, 480, glib.color_rgb(255, 255, 255), -30)
    # engine = TurtleEngine(640, 480, glib.color_rgb(255, 255, 255), -30)

    # draw_task_one_figure_one(engine, 300.0, 200.0, 20.0, 4,
    #                         glib.color_rgb(0, 255, 0), glib.color_rgb(0, 0, 255))
    # draw_task_one_figure_two(engine, 200.0, 200.0, 20.0, 5, glib.color_rgb(0, 255, 0), glib.color_rgb(0, 0, 255))
    draw_task_two(engine)
    # draw_task_three(engine, 100, 100)
    engine.show()


main()
