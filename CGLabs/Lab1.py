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
    """
    Transforms a 3d point to a 2d using perspective transformation.
    :param point_original: point in 3d space
    :param perspective_center: center of perspective in 3d space
    :return: 2d point
    """
    point = [perspective_center[0] + (point_original[0] - perspective_center[0]) / (
            1 - point_original[2] / perspective_center[2]),
             perspective_center[1] + (point_original[1] - perspective_center[1]) / (
                     1 - point_original[2] / perspective_center[2])]

    return point


class SubWindow(object):
    """
    Represents a sub window in the main 2d window.
    """

    def __init__(self):
        self.name = ''
        self.zero_point = (0.0, 0.0)
        self.width = 0.0
        self.height = 0.0
        self.x_scale = 1.0
        self.y_scale = 1.0
        self.x_axis_name = 'X'
        self.y_axis_name = 'Y'
        self.title_area_height = 50


class Engine(object):
    """
    Base engine class for simple drawing
    """
    def __init__(self, window_width, window_height, background_color):
        self.title = 'Engine'
        self.window_width = window_width
        self.window_height = window_height
        self.background_color = background_color

        # always 4!
        self._sub_windows_num = 4
        self._title_area_height = 50

        self.sub_windows = []
        for i in range(0, self._sub_windows_num):
            sub_window = SubWindow()
            sub_window.name = 'Window ' + str(i + 1)
            sub_window.width = self.window_width / 2
            sub_window.height = (self.window_height - self._title_area_height) / 2
            sub_window.zero_point = ((i // 2) * self.window_width / 2,
                                     (i % 2) * sub_window.height + self._title_area_height)
            self.sub_windows.append(sub_window)

    def setup_sub_window(self, sub_window_number, name, x_axis_name, y_axis_name):
        """
        Sets sub window parameters.
        :param sub_window_number: sub window id
        :param name: new title
        :param x_axis_name: new x axis name
        :param y_axis_name: new y axis name
        :return:
        """
        self.sub_windows[sub_window_number - 1].name = name
        self.sub_windows[sub_window_number - 1].x_axis_name = x_axis_name
        self.sub_windows[sub_window_number - 1].y_axis_name = y_axis_name

    def draw_debug_info(self):
        """
        Draws elements that help to debug
        :return:
        """
        for i in range(1, self._sub_windows_num + 1):
            self.draw_line(i, ((0.0, 0.0),
                               (self.sub_windows[i - 1].width, 0.0)), 'gray')
            self.draw_line(i, ((self.sub_windows[i - 1].width, 0.0),
                               (self.sub_windows[i - 1].width, self.sub_windows[i - 1].height)), 'gray')
            self.draw_line(i, ((self.sub_windows[i - 1].width, self.sub_windows[i - 1].height),
                               (0.0, self.sub_windows[i - 1].height)), 'gray')
            self.draw_line(i, ((0.0, self.sub_windows[i - 1].height),
                               (0.0, 0.0)), 'gray')

    def draw_curve(self, sub_window, points, color):
        """
        Draws a curve.
        :param sub_window: sub window id
        :param points: set of points of the curve
        :param color: outline color
        :return:
        """
        pass

    def draw_line(self, sub_window, points, color):
        """
        Draws a line
        :param sub_window: sub window id
        :param points: points of the line
        :param color: color to draw with
        :return:
        """
        pass

    def draw_polygon(self, sub_window, points, outline_color, fill_color):
        """
        Draws a polygon.
        :param sub_window: sub window id
        :param points: points of the polygon
        :param outline_color: outline color
        :param fill_color: color to fill with
        :return:
        """
        pass

    def draw_text(self, sub_window, text, position):
        """
        Draws text in sub window coords.
        :param sub_window: sub window id
        :param text: text to write
        :param position: position of the text
        :return:
        """
        pass

    def draw_text_main(self, text, position):
        """
        Draws text in main window coords.
        :param text: text to write
        :param position: position of the text
        :return:
        """
        pass

    def draw_titles(self):
        """
        Draws main and sub windows titles.
        :return:
        """
        self.draw_text_main(self.title,
                            (self.window_width / 2, self._title_area_height / 2))

        for i in range(1, self._sub_windows_num + 1):
            self.draw_text(i, self.sub_windows[i - 1].name,
                           (self.sub_windows[i - 1].width / 2, self.sub_windows[i - 1].title_area_height / 2))

    def draw_aux(self):
        """
        Draws auxiliary elements.
        :return:
        """
        pass

    def show(self):
        """
        Performs needed actions to start rendering.
        :return:
        """
        pass


class MathPlotLibEngine(Engine):
    """
    Implements simple drawing using Mathplot lib.
    """
    def __init__(self, window_width, window_height, background_color):
        super(MathPlotLibEngine, self).__init__(window_width, window_height, background_color)
        self.__fig, self.__axs = plt.subplots(2, 2)
        self.__fig.canvas.set_window_title('Matplotlib engine')

    def setup_sub_window(self, sub_window_number, name, x_axis_name, y_axis_name):
        super(MathPlotLibEngine, self).setup_sub_window(sub_window_number, name, x_axis_name, y_axis_name)
        # self.__axs[(sub_window_number - 1) // 2, (sub_window_number - 1) % 2]\
        #    .axis([0.0, self.window_width, self.window_height, 0.0])
        self.__axs[(sub_window_number - 1) // 2, (sub_window_number - 1) % 2].set_title(name)
        self.__axs[(sub_window_number - 1) // 2, (sub_window_number - 1) % 2].set_aspect('equal')
        self.__axs[(sub_window_number - 1) // 2, (sub_window_number - 1) % 2].invert_yaxis()

    def draw_debug_info(self):
        pass

    def draw_titles(self):
        pass

    def draw_curve(self, sub_window, points, color):
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
    """
    Implements simple drawing using Graphics lib.
    """
    def __init__(self, window_width, window_height, background_color):
        super(GraphicsEngine, self).__init__(window_width, window_height, background_color)
        self.title = 'Graphics lib engine'
        self.win = glib.GraphWin("Lab 1. Task 1", window_width, window_height)
        self.win.setBackground(background_color)

    def draw_curve(self, sub_window, points, color):
        for point in points:
            p = glib.Point(
                self.sub_windows[sub_window - 1].zero_point[0] + point[0] * self.sub_windows[sub_window - 1].x_scale,
                self.sub_windows[sub_window - 1].zero_point[1] + point[1] * self.sub_windows[sub_window - 1].y_scale)
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

    def draw_text_main(self, text, position):
        label = glib.Text(
            glib.Point(position[0], position[1]), text)
        label.draw(self.win)

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
    """
    Implements simple drawing using Turtle lib.
    """
    def __init__(self, window_width, window_height, background_color):
        super(TurtleEngine, self).__init__(window_width, window_height, background_color)
        self.title = 'Turtle lib engine'

        turtle.screensize(self.window_width, self.window_height)
        turtle.speed(10)
        turtle.pensize(3)
        turtle.radians()
        turtle.penup()

    def draw_curve(self, sub_window, points, color):
        turtle.pencolor(color)
        turtle.goto(
            self.sub_windows[sub_window - 1].zero_point[0] + points[0][0] * self.sub_windows[sub_window - 1].x_scale +
             - self.window_width / 2,
            self.window_height / 2 - self.sub_windows[sub_window - 1].zero_point[1] - points[0][1] * self.sub_windows[
                sub_window - 1].x_scale)
        turtle.pendown()

        i = 1
        while i < len(points) - 1:
            turtle.goto(
                self.sub_windows[sub_window - 1].zero_point[0] + points[i][0] * self.sub_windows[
                    sub_window - 1].x_scale - self.window_width / 2,
                self.window_height / 2 - self.sub_windows[sub_window - 1].zero_point[1] - points[i + 1][
                    1] * self.sub_windows[sub_window - 1].x_scale)
            i = i + 1

        turtle.penup()

    def draw_line(self, sub_window, points, color):
        moved_point_from = [self.sub_windows[sub_window - 1].zero_point[0] + points[0][0] - self.window_width / 2,
                            self.window_height / 2 - self.sub_windows[sub_window - 1].zero_point[1] - points[0][1]]
        moved_point_to = [self.sub_windows[sub_window - 1].zero_point[0] + points[1][0] - self.window_width / 2,
                          self.window_height / 2 - self.sub_windows[sub_window - 1].zero_point[1] - points[1][1]]

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

    def draw_text_main(self, text, position):
        turtle.goto(position[0] - self.window_width / 2,
                    self.window_height / 2 - position[1])
        turtle.write(text)

    def draw_aux(self):
        i = 0
        while i < len(self.sub_windows):
            self.draw_line(i, ((0.0, 0.0), (self.window_width / 3, 0.0)), 'gray')
            self.draw_line(i, ((0.0, -self.window_height / 8), (0.0, self.window_height / 8)), 'gray')
            self.draw_text(i, 'X', (self.window_width / 3, 20.0))
            self.draw_text(i, 'Y', (-20.0, -self.window_height / 8))
            i = i + 1


def draw_task_one(engine):
    """
    Lab 1. Task 1. Draw squares and triangles using linear perspective transformation.
    :param engine: graphics engine to render with
    :return:
    """
    engine.setup_sub_window(1, "Triangle - polygon (-30)", "", "")
    engine.setup_sub_window(2, "Triangle - polygon  (-100)", "", "")
    engine.setup_sub_window(3, "Square - lines (-30)", "", "")
    engine.setup_sub_window(4, "Square - lines (-100)", "", "")

    engine.draw_debug_info()
    engine.draw_titles()

    # shift the zero point and the scale for better visualizing
    # in the engines that do not support auto scaling.
    for i in range(0, 4):
        engine.sub_windows[i].zero_point = (engine.sub_windows[i].zero_point[0] + 100,
                                            engine.sub_windows[i].zero_point[1] + 100)
        engine.sub_windows[i].x_scale = 10
        engine.sub_windows[i].y_scale = 10

    def draw_figure_two_with_perspective(sub_window_num, perspective_depth, width, height, depth_step, count,
                                         inner_color, outer_color):
        """
        Draws squares on given depth levels according given perspective.
        :param sub_window_num: sub window id
        :param perspective_depth: z-coord of perspective center point
        :param width: square side length
        :param height: square height
        :param depth_step: depth increment
        :param count: number of squares
        :param inner_color: color of inner squares
        :param outer_color: color of outer squares
        :return:
        """

        perspective_center = (width / 2, height / 2, perspective_depth)

        for i in range(0, count):
            # calc points for single depth level
            p_top_left = transform_point_perspective((0.0, 0.0, i * depth_step), perspective_center)
            p_top_right = transform_point_perspective((width, 0.0, i * depth_step), perspective_center)
            p_bottom_left = transform_point_perspective((0.0, height, i * depth_step), perspective_center)
            p_bottom_right = transform_point_perspective((width, height, i * depth_step), perspective_center)

            if i == 0 or i == count - 1:
                color = outer_color
            else:
                color = inner_color

            # draw using lines
            engine.draw_line(sub_window_num, [p_top_left, p_top_right], color)
            engine.draw_line(sub_window_num, [p_top_left, p_bottom_left], color)
            engine.draw_line(sub_window_num, [p_bottom_left, p_bottom_right], color)
            engine.draw_line(sub_window_num, [p_top_right, p_bottom_right], color)

    draw_figure_two_with_perspective(3, -30, 200.0, 200.0, 20.0, 5, 'green', 'blue')
    draw_figure_two_with_perspective(4, -100, 200.0, 200.0, 20.0, 5, 'green', 'blue')

    def draw_figure_one_with_perspective(sub_window_num, perspective_depth, width, height, depth_step, count,
                                         inner_color, outer_color):
        """
        Draws triangles on given depth levels according given perspective.
        :param sub_window_num: sub window id
        :param perspective_depth: z-coord of perspective center point
        :param width: triangle base length
        :param height: triangle height
        :param depth_step: depth increment
        :param count: number of triangles
        :param inner_color: color of inner triangles
        :param outer_color: color of outer triangles
        :return:
        """

        perspective_center = (width / 2, height / 2, perspective_depth)

        for i in range(0, count):
            # calc points for single depth level
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

            # draw using polygon
            engine.draw_polygon(sub_window_num, [p_top, p_bottom_left, p_bottom_right], color,
                                glib.color_rgb(255, 255, 190))

    draw_figure_one_with_perspective(1, -30, 300.0, 200.0, 20.0, 4, 'green', 'blue')
    draw_figure_one_with_perspective(2, -100, 300.0, 200.0, 20.0, 4, 'green', 'blue')


def draw_task_two(engine):
    """
    Lab 1. Task 2. Draw logo.
    :param engine: graphics engine to render with
    :return:
    """

    engine.setup_sub_window(1, "Monochrome-polygon", "", "")
    engine.setup_sub_window(2, "Monochrome-lines", "", "")
    engine.setup_sub_window(3, "Color-lines", "", "")
    engine.setup_sub_window(4, "Color-polygon", "", "")

    engine.draw_debug_info()
    engine.draw_titles()

    def with_options(sub_window, monochrome, lines):
        """
        Draws logo with appearance options.
        :param sub_window: sub window id
        :param monochrome: monochrome if true, in colors otherwise
        :param lines: use lines to draw if true, polygons otherwise
        :return:
        """
        def rotate_point(cx, cy, x, y, rot_angle):
            """
            Rotates 2d point around another point.
            :param cx: x of point to rotate around
            :param cy: y of point to rotate around
            :param x: x of point to rotate
            :param y: y of point to rotate
            :param rot_angle: rotation angle
            :return: rotated point
            """
            s = sin(rot_angle)
            c = cos(rot_angle)

            origin_x = x - cx
            origin_y = y - cy
            new_x = origin_x * c - origin_y * s
            new_y = origin_x * s + origin_y * c
            return new_x + cx, new_y + cy

        # setup size and colors
        width = 200.0
        height = 200.0

        outline_colors = [glib.color_rgb(0, 101, 182), glib.color_rgb(16, 171, 1), 'red', glib.color_rgb(255, 149, 1)]
        fill_colors = [glib.color_rgb(255, 149, 1), 'red', glib.color_rgb(16, 171, 1), glib.color_rgb(0, 101, 182)]

        # calc points
        # lets calc a single leaf the crescent and then rotate it four times

        center_point = (engine.window_width / 4, engine.window_height / 4)

        shift = height / 32

        angle = 0.0
        for i in range(0, 4):
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

    # draw with different options
    with_options(1, True, False)
    with_options(2, True, True)
    with_options(3, False, True)
    with_options(4, False, False)


def draw_task_three(engine):
    """
    Lab 1. Task 3. Simulate analogue amplifier signals.
    :param engine: graphics engine to render with
    :return:
    """
    engine.setup_sub_window(1, "Sin", "", "")
    engine.setup_sub_window(2, "Tan", "", "")
    engine.setup_sub_window(3, "Ctg", "", "")
    engine.setup_sub_window(4, "Sum", "", "")

    engine.draw_debug_info()
    engine.draw_titles()

    # shift the zero point and the scale for better visualizing
    # in the engines that do not support auto scaling.
    for i in range(0, 4):
        engine.sub_windows[i].zero_point = (engine.sub_windows[i].zero_point[0] + 50,
                                            engine.sub_windows[i].zero_point[1] + 150)
        engine.sub_windows[i].x_scale = 10
        engine.sub_windows[i].y_scale = 10

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

    # setup ranges
    x_min = 0.0
    x_max = 20.0
    y_abs_max = 2.0

    # calculate points of curves
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

    # draw
    engine.draw_curve(1, points_one, color_one)
    engine.draw_curve(2, points_two, color_two)
    engine.draw_curve(3, points_three, color_three)
    engine.draw_curve(4, points_one, color_one)
    engine.draw_curve(4, points_two, color_two)
    engine.draw_curve(4, points_three, color_three)


def main():
    """
    Here it can be chosen which task of Lab 1 to run and which engine to use.
    :return:
    """
    # engine = MathPlotLibEngine(1024, 768, 'white')
    # engine = GraphicsEngine(1024, 768, 'white')
    engine = TurtleEngine(1024, 768, 'white')

    # draw_task_one(engine)
    # draw_task_two(engine)
    draw_task_three(engine)

    engine.show()


main()
