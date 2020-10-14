"""
Prog:   Lab1.py

Auth:   Oleksii Krutko, IO-z91

Desc:   Computer graphics Lab 1. 2020

"""

from math import *
import graphics as grph
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import turtle
from matplotlib.widgets import Slider, Button, RadioButtons


class Engine(object):
    def __init__(self, window_width, window_height, background_color, perspective_depth):
        self.window_width = window_width
        self.window_height = window_height
        self.background_color = background_color
        self.perspective_depth = perspective_depth

    def __transform_point_perspective(self, point_original, perspective_center):
        point = [perspective_center[0] + (point_original[0] - perspective_center[0]) / (
                1 - point_original[2] / perspective_center[2]),
                 perspective_center[1] + (point_original[1] - perspective_center[1]) / (
                         1 - point_original[2] / perspective_center[2])]

        return point

    def _draw_point(self, point, color):
        return 0

    def _draw_line(self, points, color):
        return 0

    def _draw_polygon(self, points, outline_color, fill_color):
        return 0

    def draw_task_one_figure_one(self, width, height, depth_step, count, inner_color, outer_color):
        position_offset = [self.window_width / 4 - width / 2, self.window_height / 2 - height / 2]
        perspective_center = (position_offset[0] + width / 2, position_offset[1] + height / 2,
                              self.perspective_depth)

        for i in range(0, count):
            # set points

            p_top = self.__transform_point_perspective(
                (position_offset[0] + width / 2, position_offset[1], i * depth_step),
                perspective_center)
            p_bottom_left = self.__transform_point_perspective(
                (position_offset[0], position_offset[1] + height, i * depth_step), perspective_center)
            p_bottom_right = self.__transform_point_perspective(
                (position_offset[0] + width, position_offset[1] + height, i * depth_step), perspective_center)

            if i == 0 or i == count - 1:
                color = outer_color
            else:
                color = inner_color

            self._draw_polygon([p_top, p_bottom_left, p_bottom_right], color, color)

    def draw_task_one_figure_two(self, width, height, depth_step, count, inner_color, outer_color):

        position_offset = [3 * self.window_width / 4 - width / 2, self.window_height / 2 - height / 2]
        perspective_center = (position_offset[0] + width / 2, position_offset[1] + height / 2,
                              self.perspective_depth)

        for i in range(0, count):
            # set points

            p_top_left = self.__transform_point_perspective((position_offset[0], position_offset[1], i * depth_step),
                                                            perspective_center)
            p_top_right = self.__transform_point_perspective(
                (position_offset[0] + width, position_offset[1], i * depth_step), perspective_center)
            p_bottom_left = self.__transform_point_perspective(
                (position_offset[0], position_offset[1] + height, i * depth_step), perspective_center)
            p_bottom_right = self.__transform_point_perspective(
                (position_offset[0] + width, position_offset[1] + height, i * depth_step), perspective_center)

            if i == 0 or i == count - 1:
                color = outer_color
            else:
                color = inner_color

            self._draw_line([p_top_left, p_top_right], color)
            self._draw_line([p_top_left, p_bottom_left], color)
            self._draw_line([p_bottom_left, p_bottom_right], color)
            self._draw_line([p_top_right, p_bottom_right], color)

    def draw_task_two_logo(self, width, height, monochrome, lines):

        def rotate_point(cx, cy, x, y, rot_angle):
            s = sin(rot_angle)
            c = cos(rot_angle)

            origin_x = x - cx
            origin_y = y - cy
            new_x = origin_x * c - origin_y * s
            new_y = origin_x * s + origin_y * c
            return new_x + cx, new_y + cy

        outline_colors = ['blue', 'green', 'red', 'yellow']
        fill_colors = ['yellow', 'red', 'green', 'blue']

        center_point = (self.window_width / 2, self.window_height / 2)

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
                self._draw_line([center_point, point_left], outline_color)
                self._draw_line([point_left, point_right], outline_color)
                self._draw_line([point_right, center_point], outline_color)
            else:
                self._draw_polygon([center_point, point_left, point_right], outline_color, fill_color)

            angle = angle + pi / 2

    def draw_task_three_diagram(self, width, height):
        a = 10.0

        def func_one(x):
            return a*0.1*sin(x)

        def func_two(x):
            if x == pi/2 :
                return 10e+100
            return a * 0.1 * tan(x)

        def func_three(x):
            if x == 0:
                return 10e+100
            return a * 0.1 * cos(x)/sin(x)


    def show(self):
        return 0


class MathPlotLibEngine(Engine):
    def __init__(self, window_width, window_height, background_color, perspective_depth):
        super(MathPlotLibEngine, self).__init__(window_width, window_height, background_color, perspective_depth)
        plt.title('Lab1')
        plt.axis([0.0, self.window_width, self.window_height, 0.0])

    def _draw_point(self, point, color):
        return 0

    def _draw_line(self, points, color):
        plt.plot([points[0][0], points[1][0]], [points[0][1], points[1][1]], color=color)

        return 0

    def _draw_polygon(self, points, outline_color, fill_color):
        # polygon = plt.Polygon(points, True)
        x = []
        y = []
        for point in points:
            x.append(point[0])
        for point in points:
            y.append(point[1])

        plt.fill(x, y, facecolor=fill_color, edgecolor=outline_color)
        return 0

    def show(self):
        plt.show()
        return 0


class GraphicsEngine(Engine):
    def __init__(self, window_width, window_height, background_color, perspective_depth):
        super(GraphicsEngine, self).__init__(window_width, window_height, background_color, perspective_depth)
        self.win = grph.GraphWin("Lab 1. Task 1", window_width, window_height)
        self.win.setBackground(background_color)

    def _draw_line(self, points, color):
        line = grph.Line(grph.Point(points[0][0], points[0][1]), grph.Point(points[1][0], points[1][1]))
        line.setFill(color)
        line.setWidth(3)
        line.draw(self.win)

    def _draw_polygon(self, points, outline_color, fill_color):
        poly_points = []
        for p in points:
            poly_points.append(grph.Point(p[0], p[1]))

        polygon = grph.Polygon(poly_points)
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

    def _draw_line(self, points, color):
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

    def _draw_polygon(self, points, outline_color, fill_color):
        turtle.begin_fill()
        turtle.fillcolor(fill_color)

        i = 0
        while i < len(points) - 1:
            self._draw_line([points[i], points[i + 1]], outline_color)
            i = i + 1

        self._draw_line([points[i], points[0]], outline_color)

        turtle.end_fill()

    def show(self):
        # turtle.showturtle()
        return 0


def main():
    engine = MathPlotLibEngine(640, 480, grph.color_rgb(255, 255, 255), -30)
    # engine = GraphicsEngine(640, 480, grph.color_rgb(255, 255, 255), -30)
    # engine = TurtleEngine(640, 480, color_rgb(255, 255, 255), -30)

    # engine.draw_task_one_figure_one(300.0, 200.0, 20.0, 4, grph.color_rgb(0, 255, 0), grph.color_rgb(0, 0, 255))
    # engine.draw_task_one_figure_two(200.0, 200.0, 20.0, 5, color_rgb(0, 255, 0), color_rgb(0, 0, 255))
    engine.draw_task_two_logo(400.0, 400.0, False, False)
    engine.show()


main()
