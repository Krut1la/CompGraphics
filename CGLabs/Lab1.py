"""
Prog:   Lab1.py

Auth:   Oleksii Krutko, IO-z91

Desc:   Computer graphics Lab 1. 2020

"""

from math import *
import graphics as glib
import matplotlib.pyplot as plt
import turtle


def transform_point_perspective(point_original, perspective_center):
    point = [perspective_center[0] + (point_original[0] - perspective_center[0]) / (
            1 - point_original[2] / perspective_center[2]),
             perspective_center[1] + (point_original[1] - perspective_center[1]) / (
                     1 - point_original[2] / perspective_center[2])]

    return point


class SubWindow(object):
    def __init__(self):
        self.name = ''
        self.zero_point = (0.0, 0.0)
        self.width = 0.0
        self.height = 0.0
        self.x_axis_name = 'X'
        self.y_axis_name = 'Y'


class Engine(object):
    def __init__(self, window_width, window_height, background_color):
        self.x_scale = 1.0
        self.y_scale = 1.0
        self.window_width = window_width
        self.window_height = window_height
        self.background_color = background_color

        self.sub_windows = (SubWindow(), SubWindow(), SubWindow(), SubWindow())

    def setup_sub_window(self, sub_window_number, name, zero_point, width, height, x_axis_name, y_axis_name):
        self.sub_windows[sub_window_number - 1].name = name
        self.sub_windows[sub_window_number - 1].zero_point = zero_point
        self.sub_windows[sub_window_number - 1].width = width
        self.sub_windows[sub_window_number - 1].height = height
        self.sub_windows[sub_window_number - 1].x_axis_name = x_axis_name
        self.sub_windows[sub_window_number - 1].y_axis_name = y_axis_name

    def draw_points(self, sub_window, points, color):
        pass

    def draw_line(self, sub_window, points, color):
        pass

    def draw_polygon(self, sub_window, points, outline_color, fill_color):
        pass

    def draw_text(self, sub_window, text, position):
        pass

    def draw_titles(self):
        pass

    def draw_aux(self):
        pass

    def show(self):
        pass


class MathPlotLibEngine(Engine):
    def __init__(self, window_width, window_height, background_color):
        super(MathPlotLibEngine, self).__init__(window_width, window_height, background_color)
        self.__fig, self.__axs = plt.subplots(2, 2)

    def setup_sub_window(self, sub_window_number, name, zero_point, width, height, x_axis_name, y_axis_name):
        super(MathPlotLibEngine, self).setup_sub_window(sub_window_number, name, zero_point, width, height, x_axis_name, y_axis_name)
        self.__axs[(sub_window_number - 1) // 2, (sub_window_number - 1) % 2].set_title(name)
        self.__axs[(sub_window_number - 1) // 2, (sub_window_number - 1) % 2].set_aspect('equal')
        self.__axs[(sub_window_number - 1) // 2, (sub_window_number - 1) % 2].invert_yaxis()

    def draw_points(self, sub_window, points, color):
        x = []
        y = []
        for point in points:
            x.append(point[0])
        for point in points:
            y.append(point[1])

        self.__axs[(sub_window - 1) // 2, (sub_window - 1) % 2].plot(x, y, color=color)

    def draw_line(self, sub_window, points, color):
        self.__axs[(sub_window - 1) // 2, (sub_window - 1) % 2].plot([points[0][0], points[1][0]],
                                                                     [points[0][1], points[1][1]], color=color)

    def draw_polygon(self, sub_window, points, outline_color, fill_color):
        x = []
        y = []
        for point in points:
            x.append(point[0])
        for point in points:
            y.append(point[1])

        self.__axs[(sub_window - 1) // 2, (sub_window - 1) % 2].fill(x, y, facecolor=fill_color,
                                                                     edgecolor=outline_color)

    def show(self):
        plt.show()


class GraphicsEngine(Engine):
    def __init__(self, window_width, window_height, background_color):
        super(GraphicsEngine, self).__init__(window_width, window_height, background_color)
        self.win = glib.GraphWin("Lab 1. Task 1", window_width, window_height)
        self.win.setBackground(background_color)

    def draw_points(self, sub_window, points, color):
        for point in points:
            p = glib.Point(self.sub_windows[sub_window - 1].zero_point[0] + point[0] * self.x_scale,
                           self.sub_windows[sub_window - 1].zero_point[1] + point[1] * self.y_scale)
            p.setOutline(color)
            p.draw(self.win)

    def draw_line(self, sub_window, points, color):
        line = glib.Line(
            glib.Point(self.sub_windows[sub_window - 1].zero_point[0] + points[0][0],
                       self.sub_windows[sub_window - 1].zero_point[1] + points[0][1]),
            glib.Point(self.sub_windows[sub_window - 1].zero_point[0] + points[1][0],
                       self.sub_windows[sub_window - 1].zero_point[1] + points[1][1]))

        line.setOutline(color)
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

    def draw_text(self, sub_window, text, position):
        label = glib.Text(
            glib.Point(self.sub_windows[sub_window - 1].zero_point[0] + position[0],
                       self.sub_windows[sub_window - 1].zero_point[1] + position[1]), text)
        label.draw(self.win)

    def draw_titles(self):
        label = glib.Text(glib.Point(self.window_width/2, 10.0), 'Graphics lib')
        label.draw(self.win)

        i = 1
        while i <= len(self.sub_windows):
            self.draw_text(i, self.sub_windows[i - 1].name, (self.sub_windows[i - 1].width/3, 10.0))
            i = i + 1

    def draw_aux(self):
        i = 0
        while i < len(self.sub_windows):
            self.draw_line(i, ((0.0, 0.0), (self.window_width / 3, 0.0)), 'gray')
            self.draw_line(i, ((0.0, -self.window_height / 8), (0.0, self.window_height / 8)), 'gray')
            self.draw_text(i, 'X', (self.window_width / 3, 20.0))
            self.draw_text(i, 'Y', (-20.0, -self.window_height / 8))
            i = i + 1

    def show(self):
        self.win.getMouse()
        self.win.close()


class TurtleEngine(Engine):
    def __init__(self, window_width, window_height, background_color):
        super(TurtleEngine, self).__init__(window_width, window_height, background_color)

        turtle.screensize(self.window_width, self.window_height)
        turtle.pensize(3)
        turtle.radians()
        turtle.penup()

    def draw_points(self, sub_window, points, color):
        turtle.pencolor(color)
        turtle.goto(
            self.sub_windows[sub_window - 1].zero_point[0] + points[0][0] * self.x_scale - self.window_width / 2,
            self.window_height / 2 - self.sub_windows[sub_window - 1].zero_point[1] - points[0][1] * self.y_scale)
        turtle.pendown()
        i = 1
        while i < len(points) - 1:
            turtle.goto(
                self.sub_windows[sub_window - 1].zero_point[0] + points[i][0] * self.x_scale - self.window_width / 2,
                self.window_height / 2 - self.sub_windows[sub_window - 1].zero_point[1] - points[i + 1][
                    1] * self.y_scale)
            i = i + 1

        turtle.penup()

    def draw_line(self, sub_window, points, color):
        moved_point_from = [self.sub_windows[sub_window - 1].zero_point[0] + points[0][0] - self.window_width / 2,
                            self.window_height/2 - self.sub_windows[sub_window - 1].zero_point[1] - points[0][1]]
        moved_point_to = [self.sub_windows[sub_window - 1].zero_point[0] + points[1][0] - self.window_width / 2,
                          self.window_height/2 - self.sub_windows[sub_window - 1].zero_point[1] - points[1][1]]

        length = sqrt((moved_point_to[0] - moved_point_from[0]) * (moved_point_to[0] - moved_point_from[0])
                      + (moved_point_to[1] - moved_point_from[1]) * (moved_point_to[1] - moved_point_from[1]))
        angle = acos((moved_point_to[0] - moved_point_from[0]) / length)
        if moved_point_to[1] < moved_point_from[1]:
            angle = 2 * pi - angle

        turtle.goto(moved_point_from[0], moved_point_from[1])
        turtle.setheading(0)
        turtle.pencolor(color)
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

    def draw_text(self, sub_window, text, position):
        turtle.goto(self.sub_windows[sub_window - 1].zero_point[0] + position[0] - self.window_width / 2,
                    self.window_height / 2 - self.sub_windows[sub_window - 1].zero_point[1] - position[1])
        turtle.write(text)

    def draw_titles(self):
        turtle.goto(- self.window_width / 2, self.window_height / 2)
        turtle.write('Turtle lib')

        i = 1
        while i <= len(self.sub_windows):
            self.draw_text(i, self.sub_windows[i - 1].name, (self.window_width / 4, -self.window_height / 8))
            i = i + 1

    def draw_aux(self):
        i = 0
        while i < len(self.sub_windows):
            self.draw_line(i, ((0.0, 0.0), (self.window_width / 3, 0.0)), 'gray')
            self.draw_line(i, ((0.0, -self.window_height / 8), (0.0, self.window_height / 8)), 'gray')
            self.draw_text(i, 'X', (self.window_width / 3, 20.0))
            self.draw_text(i, 'Y', (-20.0, -self.window_height / 8))
            i = i + 1


def draw_task_one(engine):
    offset_x = 50.0
    offset_y = 100.0

    engine.setup_sub_window(1, "Triangle - filled", (offset_x, offset_y), "", "")
    engine.setup_sub_window(2, "Triangle - outlined", (offset_x + engine.window_width / 2, offset_y), "", "")
    engine.setup_sub_window(3, "Square - filled", (offset_x, offset_y + engine.window_height / 2), "", "")
    engine.setup_sub_window(4, "Square - outlined", (offset_x + engine.window_width / 2, offset_y + engine.window_height / 2), "", "")

    engine.draw_titles()

    def draw_figure_two_with_perspective(sub_window_num, perspective_depth, width, height, depth_step, count,
                                         inner_color, outer_color):

        perspective_center = (width / 2, height / 2, perspective_depth)

        for i in range(0, count):
            p_top_left = transform_point_perspective((0.0, 0.0, i * depth_step), perspective_center)
            p_top_right = transform_point_perspective((width, 0.0, i * depth_step), perspective_center)
            p_bottom_left = transform_point_perspective((0.0, height, i * depth_step), perspective_center)
            p_bottom_right = transform_point_perspective((width, height, i * depth_step), perspective_center)

            if i == 0 or i == count - 1:
                color = outer_color
            else:
                color = inner_color

            engine.draw_line(sub_window_num, [p_top_left, p_top_right], color)
            engine.draw_line(sub_window_num, [p_top_left, p_bottom_left], color)
            engine.draw_line(sub_window_num, [p_bottom_left, p_bottom_right], color)
            engine.draw_line(sub_window_num, [p_top_right, p_bottom_right], color)

    draw_figure_two_with_perspective(3, -30, 200.0, 200.0, 20.0, 5, 'green', 'blue')
    draw_figure_two_with_perspective(4, -100, 200.0, 200.0, 20.0, 5, 'green', 'blue')

    def draw_figure_one_with_perspective(sub_window_num, perspective_depth, width, height, depth_step, count,
                                         inner_color, outer_color):

        perspective_center = (width / 2, height / 2, perspective_depth)

        for i in range(0, count):
            p_top = transform_point_perspective(
                (width / 2, 0.0, i * depth_step), perspective_center)
            p_bottom_left = transform_point_perspective(
                (0.0, height, i * depth_step), perspective_center)
            p_bottom_right = transform_point_perspective(
                (width, height, i * depth_step), perspective_center)

            if i == 0 or i == count - 1:
                color = outer_color
            else:
                color = inner_color

            engine.draw_polygon(sub_window_num, [p_top, p_bottom_left, p_bottom_right], color,
                                glib.color_rgb(255, 255, 190))

    draw_figure_one_with_perspective(1, -30, 300.0, 200.0, 20.0, 4, 'green', 'blue')
    draw_figure_one_with_perspective(2, -100, 300.0, 200.0, 20.0, 4, 'green', 'blue')


def draw_task_two(engine):
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

        center_point = (engine.window_width / 4, engine.window_height / 4)

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

    engine.setup_sub_window(1, "Monochrome-polygon", (0.0, 0.0), "", "")
    engine.setup_sub_window(2, "Monochrome-lines", (engine.window_width / 2, 0.0), "", "")
    engine.setup_sub_window(3, "Color-lines", (0.0, engine.window_height / 2), "", "")
    engine.setup_sub_window(4, "Color-polygon", (engine.window_width / 2, engine.window_height / 2), "", "")

    engine.draw_titles()

    with_options(1, True, False)
    with_options(2, True, True)
    with_options(3, False, True)
    with_options(4, False, False)


def draw_task_three(engine):
    offset_x = 50.0
    offset_y = 100.0

    engine.setup_sub_window(1, "Sin", (offset_x, offset_y), "", "")
    engine.setup_sub_window(2, "Tan", (offset_x + engine.window_width / 2, offset_y), "", "")
    engine.setup_sub_window(3, "Ctg", (offset_x, offset_y + engine.window_height / 2), "", "")
    engine.setup_sub_window(4, "Sum", (offset_x + engine.window_width / 2, offset_y + engine.window_height / 2), "", "")

    engine.draw_titles()
    engine.draw_aux()

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

    engine.x_scale = 10.0
    engine.y_scale = 10.0
    engine.draw_points(1, points_one, color_one)
    engine.draw_points(2, points_two, color_two)
    engine.draw_points(3, points_three, color_three)
    engine.draw_points(4, points_one, color_one)
    engine.draw_points(4, points_two, color_two)
    engine.draw_points(4, points_three, color_three)


def main():
    # engine = MathPlotLibEngine(640, 480, 'white')
    engine = GraphicsEngine(1024, 768, 'white')
    # engine = TurtleEngine(640, 480, 'white')

    draw_task_one(engine)
    # draw_task_two(engine)
    # draw_task_three(engine)

    engine.show()


main()
