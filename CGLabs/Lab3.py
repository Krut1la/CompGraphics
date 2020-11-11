"""
Prog:   Lab3.py

Auth:   Oleksii Krutko, IO-z91

Desc:   Computer graphics Lab 3. 2020

"""

import random
import copy
import tkinter as tk
import numpy as np
from math import *


class Transformable(object):
    """
    Interface for geometry objects that can be transformed.
    """

    def transform(self, matrix):
        """
        Uses matrix operations to transform.
        :param matrix: transformation matrix
        :return:
        """
        pass

    def get_transformed(self, matrix):
        """
        Uses matrix operations to transform.
        :param matrix: transformation matrix
        :return:
        """
        pass


class Vector3(Transformable):
    """
    Represents 3-vector with standard operations on it.
    """
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @staticmethod
    def unit_x():
        return Vector3(1.0, 0.0, 0.0)

    @staticmethod
    def unit_y():
        return Vector3(0.0, 1.0, 0.0)

    @staticmethod
    def unit_z():
        return Vector3(0.0, 0.0, 1.0)

    @staticmethod
    def zero():
        return Vector3(0.0, 0.0, 0.0)

    def dist(self, other):
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)

    def length(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self):
        length = self.length()
        if length == 0.0:
            raise
        return self*(1/length)

    def cross(self, vector):
        return Vector3(self.y * vector.z - self.z * vector.y,
                       self.z * vector.x - self.x * vector.z,
                       self.x * vector.y - self.y * vector.x)

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if isinstance(other, float):
            return Vector3(self.x * other, self.y * other, self.z * other)

    def neg(self):
        return Vector3(-self.x, -self.y, -self.z)

    def transform(self, matrix):
        vector4 = np.array([self.x, self.y, self.z, 1.0])
        vector4.dot(matrix.data, vector4)
        self.x = vector4[0] / vector4[3]
        self.y = vector4[1] / vector4[3]
        self.z = vector4[2] / vector4[3]

    def get_transformed(self, matrix):
        vector4 = np.array([self.x, self.y, self.z, 1.0])
        vector4.dot(matrix.data, vector4)
        return Vector3(vector4[0] / vector4[3], vector4[1] / vector4[3], vector4[2] / vector4[3])


class MatrixAffine4x4(object):
    """
    Represents affine matrix with standard operations.
    """
    def __init__(self):
        self.data = np.array([[1.0, 0.0, 0.0, 0.0],
                              [0.0, 1.0, 0.0, 0.0],
                              [0.0, 0.0, 1.0, 0.0],
                              [0.0, 0.0, 0.0, 1.0]])

    def __mul__(self, other):
        new_matrix = MatrixAffine4x4()
        new_matrix.data = self.data.dot(other.data)
        return new_matrix

    @staticmethod
    def build_identity():
        m = MatrixAffine4x4()
        m.data = np.array([[1.0, 0.0, 0.0, 0.0],
                           [0.0, 1.0, 0.0, 0.0],
                           [0.0, 0.0, 1.0, 0.0],
                           [0.0, 0.0, 0.0, 1.0]])
        return m

    @staticmethod
    def build_xz_reflection():
        m = MatrixAffine4x4()
        m.data = np.array([[1.0, 0.0, 0.0, 0.0],
                           [0.0, -1.0, 0.0, 0.0],
                           [0.0, 0.0, 1.0, 0.0],
                           [0.0, 0.0, 0.0, 1.0]])
        return m

    @staticmethod
    def build_xy_reflection():
        m = MatrixAffine4x4()
        m.data = np.array([[1.0, 0.0, 0.0, 0.0],
                           [0.0, 1.0, 0.0, 0.0],
                           [0.0, 0.0, -1.0, 0.0],
                           [0.0, 0.0, 0.0, 1.0]])
        return m

    @staticmethod
    def build_xy_perspective_proj(p, q, r):
        m = MatrixAffine4x4()
        m.data = np.array([[1.0, 0.0, 0.0, p],
                           [0.0, 1.0, 0.0, q],
                           [0.0, 0.0, 0.0, r],
                           [0.0, 0.0, 0.0, 1.0]])
        return m

    @staticmethod
    def build_orthogonal_proj():
        m = MatrixAffine4x4()
        m.data = np.array([[1.0, 0.0, 0.0, 0.0],
                           [0.0, 1.0, 0.0, 0.0],
                           [0.0, 0.0, 0.0, 0.0],
                           [0.0, 0.0, 0.0, 1.0]])
        return m

    @staticmethod
    def build_axonometric_proj(phi, eta):
        m = MatrixAffine4x4()
        m1 = np.array([[cos(phi), 0.0, -sin(phi), 0.0],
                       [0.0, 1.0, 0.0, 0.0],
                       [sin(phi), 0.0, cos(phi), 0.0],
                       [0.0, 0.0, 0.0, 1.0]])

        m2 = np.array([[1.0, 0.0, 0.0, 0.0],
                       [0.0, cos(eta), sin(eta), 0.0],
                       [0.0, -sin(eta), cos(eta), 0.0],
                       [0.0, 0.0, 0.0, 1.0]])

        m.data = m1.dot(m2).dot(MatrixAffine4x4.build_orthogonal_proj().data)

        return m

    @staticmethod
    def build_xy_orthograph_proj():
        m = MatrixAffine4x4()
        m.data = np.array([[1.0, 0.0, 0.0, 0.0],
                           [0.0, 0.0, 0.0, 0.0],
                           [0.0, -1.0, 0.0, 0.0],
                           [0.0, 0.0, 0.0, 1.0]])
        return m

    @staticmethod
    def build_rotation(angle, axis):
        s = axis.x ** 2 + axis.y ** 2 + axis.z ** 2
        sq = sqrt(s)
        n1 = axis.x / sq
        n2 = axis.y / sq
        n3 = axis.z / sq

        m = MatrixAffine4x4()
        m.data = np.array(
            [[n1 * n1 + (1 - n1 * n1) * cos(angle), n1 * n2 * (1 - cos(angle)) - n3 * sin(angle),
              n1 * n3 * (1 - cos(angle)) + n2 * sin(angle), 0.0],
             [n1 * n2 * (1 - cos(angle)) + n3 * sin(angle), n2 * n2 + (1 - n2 * n2) * cos(angle),
              n2 * n3 * (1 - cos(angle)) - n1 * sin(angle), 0.0],
             [n1 * n3 * (1 - cos(angle)) - n2 * sin(angle), n2 * n3 * (1 - cos(angle)) + n1 * sin(angle),
              n3 * n3 + (1 - n3 * n3) * cos(angle), 0.0],
             [0.0, 0.0, 0.0, 1.0]])

        return m

    @staticmethod
    def build_scale(sx, sy, sz):
        m = MatrixAffine4x4()
        m.data = np.array([[sx, 0.0, 0.0, 0.0],
                           [0.0, sy, 0.0, 0.0],
                           [0.0, 0.0, sz, 0.0],
                           [0.0, 0.0, 1.0, 0.0]])
        return m

    @staticmethod
    def build_translation(point):
        m = MatrixAffine4x4()
        m.data = np.array([[1.0, 0.0, 0.0, 0.0],
                           [0.0, 1.0, 0.0, 0.0],
                           [0.0, 0.0, 1.0, 0.0],
                           [point.x, point.y, point.z, 1.0]])
        return m


class BoundingBox(Transformable):
    """
    Represents bounding box.
    """
    def __init__(self, point_min, point_max):
        self.point_min = point_min
        self.point_max = point_max

    def is_point_in(self, point):
        return (self.point_min.x <= point.x) and \
               (self.point_max.x >= point.x) and \
               (self.point_min.y <= point.y) and \
               (self.point_max.y >= point.y) and \
               (self.point_min.z <= point.z) and \
               (self.point_max.z >= point.z)

    def get_model(self):
        model = Model()
        vid_1 = model.add_vertex(Vertex3d(Vector3(self.point_min.x, self.point_min.y, self.point_min.z)))
        vid_2 = model.add_vertex(Vertex3d(Vector3(self.point_min.x, self.point_min.y, self.point_max.z)))
        vid_3 = model.add_vertex(Vertex3d(Vector3(self.point_min.x, self.point_max.y, self.point_min.z)))
        vid_4 = model.add_vertex(Vertex3d(Vector3(self.point_min.x, self.point_max.y, self.point_max.z)))
        vid_5 = model.add_vertex(Vertex3d(Vector3(self.point_max.x, self.point_min.y, self.point_min.z)))
        vid_6 = model.add_vertex(Vertex3d(Vector3(self.point_max.x, self.point_min.y, self.point_max.z)))
        vid_7 = model.add_vertex(Vertex3d(Vector3(self.point_max.x, self.point_max.y, self.point_min.z)))
        vid_8 = model.add_vertex(Vertex3d(Vector3(self.point_max.x, self.point_max.y, self.point_max.z)))

        model.add_edge(Edge(vid_1, vid_2))
        model.add_edge(Edge(vid_2, vid_4))
        model.add_edge(Edge(vid_3, vid_4))
        model.add_edge(Edge(vid_3, vid_1))
        model.add_edge(Edge(vid_5, vid_6))
        model.add_edge(Edge(vid_6, vid_8))
        model.add_edge(Edge(vid_7, vid_8))
        model.add_edge(Edge(vid_7, vid_5))
        model.add_edge(Edge(vid_1, vid_5))
        model.add_edge(Edge(vid_2, vid_6))
        model.add_edge(Edge(vid_3, vid_7))
        model.add_edge(Edge(vid_4, vid_8))

        return model

    def transform(self, matrix):
        self.point_min.transform(matrix)
        self.point_max.transform(matrix)

    def get_transformed(self, matrix):
        point_min = self.point_min.get_transformed(matrix)
        point_max = self.point_max.get_transformed(matrix)
        return BoundingBox(point_min, point_max)


class Vertex3d(Transformable):
    """
    Represents a single 3d vertex.
    """

    def __init__(self, point):
        self.point = point

    def transform(self, matrix):
        self.point.transform(matrix)

    def get_transformed(self, matrix):
        point = self.point.get_transformed(matrix)
        return Vertex3d(point)


class Edge(object):
    """
    Represents an edge between two vertices.
    """

    def __init__(self, vid_from, vid_to):
        self.vid_from = vid_from
        self.vid_to = vid_to


class Model(Transformable):
    """
    Represents 3d geometry objects.
    """

    def __init__(self):
        self._vertices = []
        self._edges = []

    def transform(self, matrix):
        for vertex in self._vertices:
            vertex.transform(matrix)

    def add_vertex(self, vertex):
        self._vertices.append(vertex)
        return len(self._vertices) - 1

    def add_edge(self, edge):
        self._edges.append(edge)
        return len(self._edges) - 1

    def get_vertices(self):
        return self._vertices

    def get_edges(self):
        return self._edges

    def clear(self):
        self._vertices.clear()
        self._edges.clear()


class AnimationFrame(object):
    """
    Represents a single frame in an animation sequence.
    """
    def __init__(self, time_delay, color, transformation):
        self.time_delay = time_delay
        self.color = color
        self.transformation = transformation


class Animation(object):
    """
    Represents animation as a sequence of frames.
    """
    def __init__(self, cyclic, frames):
        self._cyclic = cyclic
        self._frames = frames
        self.position = 0

    def get_model(self):
        model = Model()
        prev_vid = -1
        prev_point = None
        for frame in self._frames:

            point = Vector3.zero()
            point.transform(frame.transformation)

            if prev_vid == -1:
                vid = model.add_vertex(Vertex3d(point))
                prev_point = copy.deepcopy(point)
                prev_vid = vid
            else:
                segment_dist = prev_point.dist(point)
                if segment_dist > 50.0:
                    vid = model.add_vertex(Vertex3d(point))
                    model.add_edge(Edge(prev_vid, vid))
                    prev_point = copy.deepcopy(point)
                    prev_vid = vid

        return model

    def get_frame(self):
        frame = self._frames[self.position]
        self.position = self.position + 1

        if self.position == len(self._frames):
            if self._cyclic:
                self.position = 0
            else:
                self.position = self.position - 1

        return frame


class ScreenSaver(object):
    """
    Represents a simple screen saver according to Lab 3. Variant 10.
    """
    def __init__(self, engine, model, animation, boundary_box):
        self._engine = engine
        self._model = copy.deepcopy(model)
        self._boundary_box_model = boundary_box.get_model()
        self._trajectory_model = animation.get_model()
        self._animation = animation

        self._engine.update()
        self._draw_frame(self._animation.get_frame())

    def _animate(self):
        if self._engine.is_animating.get():
            self._draw_frame(self._animation.get_frame())

        self._engine.after(20, self._animate)

    def _draw_frame(self, frame):
        if self._model is not None:
            self._engine.clear()

            if self._engine.show_axes.get():
                self._engine.draw_axes()

            if self._engine.show_debug.get():
                self._engine.draw_model(self._boundary_box_model, 1, "gray", True)
                self._engine.draw_model(self._trajectory_model, 5, "red", True)

            model = copy.deepcopy(self._model)
            model.transform(frame.transformation)

            self._engine.draw_model(model, 3, frame.color,  self._engine.show_debug.get())
            self._engine.update()

    def start(self):
        self._engine.after(1, self._animate)
        self._engine.show()

    def stop(self):
        pass


class GraphicsEngine2dBase(object):
    """
    Base class for simple 3d graphics based on Tk.
    Supports basic projections and views.
    """

    def __init__(self, width, height, title):
        self.__root = tk.Tk()
        self.__root.title(title)
        self.__root.geometry(str(width) + "x" + str(height) + "+10+20")

        self.is_animating = tk.BooleanVar(self.__root, True)
        self.show_axes = tk.BooleanVar(self.__root, False)
        self.show_debug = tk.BooleanVar(self.__root, False)

        self._view_type = tk.IntVar(self.__root, 0)
        self._projection_type = tk.IntVar(self.__root, 0)

        self._projection_types = {
            0: MatrixAffine4x4.build_orthogonal_proj(),
            1: MatrixAffine4x4.build_axonometric_proj(pi / 6, pi / 4),
            2: MatrixAffine4x4.build_xy_perspective_proj(0.0, 0.0, 0.002)
        }

        self._view_types = {
            0: MatrixAffine4x4.build_identity(),
            1: MatrixAffine4x4.build_rotation(pi, Vector3.unit_y()),
            2: MatrixAffine4x4.build_rotation(-pi / 2, Vector3.unit_x()),
            3: MatrixAffine4x4.build_rotation(pi / 2, Vector3.unit_x()),
            4: MatrixAffine4x4.build_rotation(pi / 2, Vector3.unit_y()),
            5: MatrixAffine4x4.build_rotation(-pi / 2, Vector3.unit_y()),
        }

        self._init_ui()

    def _init_ui(self):
        """
        Simple test framework UI
        :return:
        """
        main_frame = tk.Frame(self.__root, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.grid_columnconfigure(0, weight=2)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        self._render_frame = tk.Frame(main_frame, bg="white")
        self._render_frame.grid(row=0, column=0, sticky="nsew")
        render_label = tk.Label(self._render_frame, text="Scene", bg="white", fg="gray", font=("Helvetica", 20))
        render_label.pack(side=tk.TOP)
        self._canvas = tk.Canvas(self._render_frame, bg="white")
        self._canvas.pack(fill=tk.BOTH, expand=True)
        control_frame = tk.Frame(main_frame, bg="gray")
        control_frame.grid(row=0, column=1, sticky="nsew")
        control_frame.grid_columnconfigure(0, weight=1)
        control_frame.grid_rowconfigure(0, weight=1)
        control_frame.grid_rowconfigure(1, weight=5)
        control_frame.grid_rowconfigure(2, weight=4)
        control_label = tk.Label(control_frame, text="Control", bg="gray", fg="white", font=("Helvetica", 20))
        control_label.grid(row=0, column=0, sticky="n")
        self._sliders_frame = tk.Frame(control_frame, bg="gray")
        self._sliders_frame.grid(row=1, column=0, sticky="nsew")
        self._sliders_frame.grid_columnconfigure(0, weight=1)
        self._sliders_frame.grid_rowconfigure(0, weight=1)
        self._sliders_frame.grid_rowconfigure(1, weight=1)
        self._sliders_frame.grid_rowconfigure(2, weight=1)
        self._sliders_frame.grid_rowconfigure(3, weight=1)
        self._sliders_frame.grid_rowconfigure(4, weight=1)
        self._sliders_frame.grid_rowconfigure(5, weight=1)
        self._sliders_frame.grid_rowconfigure(6, weight=1)
        self._sliders_frame.grid_rowconfigure(7, weight=1)
        self._sliders_frame.grid_rowconfigure(8, weight=1)
        self._sliders_frame.grid_rowconfigure(9, weight=1)
        self._sliders_frame.grid_rowconfigure(10, weight=1)
        self._sliders_frame.grid_rowconfigure(11, weight=1)

        views_label = tk.Label(self._sliders_frame, text="Views", bg="gray", fg="white", font=("Helvetica", 20))
        views_label.grid(row=0, column=0, sticky="n")

        view_front_radio = tk.Radiobutton(self._sliders_frame, text="Front", variable=self._view_type, value=0,
                                          indicatoron=0)
        view_front_radio.grid(row=1, column=0, sticky="new")
        view_back_radio = tk.Radiobutton(self._sliders_frame, text="Back", variable=self._view_type, value=1,
                                         indicatoron=0)
        view_back_radio.grid(row=2, column=0, sticky="new")
        view_up_radio = tk.Radiobutton(self._sliders_frame, text="Up", variable=self._view_type, value=2,
                                       indicatoron=0)
        view_up_radio.grid(row=3, column=0, sticky="new")
        view_down_radio = tk.Radiobutton(self._sliders_frame, text="Down", variable=self._view_type, value=3,
                                         indicatoron=0)
        view_down_radio.grid(row=4, column=0, sticky="new")
        view_left_radio = tk.Radiobutton(self._sliders_frame, text="Left", variable=self._view_type, value=4,
                                         indicatoron=0)
        view_left_radio.grid(row=5, column=0, sticky="new")
        view_right_radio = tk.Radiobutton(self._sliders_frame, text="Right", variable=self._view_type, value=5,
                                          indicatoron=0)
        view_right_radio.grid(row=6, column=0, sticky="new")

        projections_label = tk.Label(self._sliders_frame, text="Projections", bg="gray", fg="white",
                                     font=("Helvetica", 20))
        projections_label.grid(row=7, column=0, sticky="n")

        proj_orthogonal_radio = tk.Radiobutton(self._sliders_frame, text="Orthogonal", variable=self._projection_type,
                                               value=0, indicatoron=0)
        proj_orthogonal_radio.grid(row=8, column=0, sticky="new")

        axonometric_orthogonal_radio = tk.Radiobutton(self._sliders_frame, text="Axonometric",
                                                      variable=self._projection_type,
                                                      value=1, indicatoron=0)
        axonometric_orthogonal_radio.grid(row=9, column=0, sticky="new")

        perspective_orthogonal_radio = tk.Radiobutton(self._sliders_frame, text="Perspective",
                                                      variable=self._projection_type,
                                                      value=2, indicatoron=0)
        perspective_orthogonal_radio.grid(row=10, column=0, sticky="new")

        buttons_frame = tk.Frame(control_frame, bg="gray")
        buttons_frame.grid(row=2, column=0, sticky="nsew")
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_rowconfigure(0, weight=1)
        buttons_frame.grid_rowconfigure(1, weight=1)
        buttons_frame.grid_rowconfigure(2, weight=1)
        buttons_frame.grid_rowconfigure(3, weight=1)
        buttons_frame.grid_rowconfigure(4, weight=1)

        animation_on_check = tk.Checkbutton(buttons_frame, text="Animate", variable=self.is_animating,
                                            indicatoron=0)
        animation_on_check.grid(row=0, column=0, sticky="new")

        axes_button = tk.Checkbutton(buttons_frame, fg="black", text="Show axes", variable=self.show_axes,
                                     indicatoron=0)
        axes_button.grid(row=2, column=0, sticky="sew")

        debug_button = tk.Checkbutton(buttons_frame, fg="black", text="Show debug", variable=self.show_debug,
                                      indicatoron=0)
        debug_button.grid(row=3, column=0, sticky="sew")

        quit_button = tk.Button(buttons_frame, fg="black", text="Quit", command=quit)
        quit_button.grid(row=4, column=0, sticky="sew")

    def after(self, delay, func):
        self._canvas.after(delay, func)

    def update(self):
        self._canvas.update()

    def clear(self):
        self._canvas.delete("all")

    def draw_axes(self):
        axis_len = 200.0

        model = Model()
        vid_zero = model.add_vertex(Vertex3d(Vector3(0.0, 0.0, 0.0)))
        vid_x = model.add_vertex(Vertex3d(Vector3(axis_len, 0.0, 0.0)))
        vid_y = model.add_vertex(Vertex3d(Vector3(0.0, axis_len, 0.0)))
        vid_z = model.add_vertex(Vertex3d(Vector3(0.0, 0.0, axis_len)))
        model.add_edge(Edge(vid_zero, vid_x))
        model.add_edge(Edge(vid_zero, vid_y))
        model.add_edge(Edge(vid_zero, vid_z))

        self.draw_model(model, 1, "grey", True)

    def draw_model(self, model, line_width, color, show_coord):
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()

        edges = model.get_edges()
        vertices = model.get_vertices()
        vertices2d = []
        for vertex in vertices:
            transform = MatrixAffine4x4.build_xy_reflection() * \
                        MatrixAffine4x4.build_xz_reflection() * \
                        self._view_types[self._view_type.get()] * \
                        self._projection_types[self._projection_type.get()]

            vertices2d.append(vertex.get_transformed(transform))
        for edge in edges:
            self._draw_line(vertices2d[edge.vid_from].point.x + width / 2,
                            vertices2d[edge.vid_from].point.y + height / 2,
                            vertices2d[edge.vid_to].point.x + width / 2,
                            vertices2d[edge.vid_to].point.y + height / 2,
                            line_width,
                            color)

        if show_coord:
            for i in range(0, len(vertices)):
                self._draw_text(vertices2d[i].point.x + width / 2, vertices2d[i].point.y + height / 2,
                                "{:.2f}".format(vertices[i].point.x) + ". " +
                                "{:.2f}".format(vertices[i].point.y) + ". " +
                                "{:.2f}".format(vertices[i].point.z))

    def _draw_line(self, x_from, y_from, x_to, y_to, line_width, color):
        pass

    def _draw_text(self, x, y, text):
        pass

    def show(self):
        self.__root.mainloop()


class GraphicsEngine2dCanvas(GraphicsEngine2dBase):
    """
    Simple 3d graphics based on Tk.
    """

    def __init__(self, width, height, title):
        super(GraphicsEngine2dCanvas, self).__init__(width, height, title)

    def _init_ui(self):
        super(GraphicsEngine2dCanvas, self)._init_ui()

    def _draw_line(self, x_from, y_from, x_to, y_to, line_width, color):
        self._canvas.create_line(x_from,
                                 y_from,
                                 x_to,
                                 y_to,
                                 width=line_width,
                                 fill=color)

    def _draw_text(self, x, y, text):
        self._canvas.create_text(x, y,
                                 text=text,
                                 font=("Helvetica", 7))


def color_rgb(r, g, b):
    """
    r,g,b are intensities of red, green, and blue in range(256)
    Returns color specifier string for the resulting color
    """
    return "#%02x%02x%02x" % (r, g, b)


def build_animation(boundary_box):
    """

    :param boundary_box:
    :return:
    """
    frames = []

    start_point = Vector3(0.0, 0.0, 0.0)
    direction = Vector3(1.0, 1.0, 1.0)
    direction_inc = 1.0

    current_position = copy.deepcopy(start_point)

    for i in range(0, 2000):
        while True:
            new_position = current_position + direction * direction_inc

            if not boundary_box.is_point_in(new_position):
                ort_dir = Vector3(random.random(), random.random(), random.random())
                ort_dir = ort_dir.normalize()
                direction.transform(MatrixAffine4x4.build_rotation(random.random() * pi / 3 + pi, ort_dir))
            else:
                current_position = new_position
                break

        trans = MatrixAffine4x4.build_translation(current_position)
        rot = MatrixAffine4x4.build_rotation(2 * i * pi / 300, Vector3.unit_z())
        color = color_rgb(round(abs(sin(i / 100)) * 255), round(abs(sin(i / 100)) * 255), 255)
        time_delay = 100
        frame = AnimationFrame(time_delay, color, rot * trans)
        frames.append(frame)

    return Animation(True, frames)


def main():
    engine2d = GraphicsEngine2dCanvas(1024, 768, "Lab 2. Variant 10.")

    model = BoundingBox(Vector3(-150.0, -100.0, -50.0), Vector3(150.0, 100.0, 50.0))\
        .get_model()

    boundary_box = BoundingBox(Vector3(-250.0, -200.0, -150.0), Vector3(250.0, 200.0, 150.0))
    animation = build_animation(boundary_box)

    screen_saver = ScreenSaver(engine2d, model, animation, boundary_box)

    screen_saver.start()


main()
