"""
Prog:   Lab2.py

Auth:   Oleksii Krutko, IO-z91

Desc:   Computer graphics Lab 3. 2020

"""

import time
import copy
import tkinter as tk
import numpy as np
from math import *
from threading import Thread


class Vector3(object):
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

    def neg(self):
        return Vector3(-self.x, -self.y, -self.z)


class MatrixAffine4x4(object):
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

        # m.data = m1.dot(m2).dot(MatrixAffine4x4.build_orthogonal_proj().data)
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
        s = axis.x + axis.y + axis.z
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
    def build_translation(dx, dy, dz):
        m = MatrixAffine4x4()
        m.data = np.array([[1.0, 0.0, 0.0, 0.0],
                           [0.0, 1.0, 0.0, 0.0],
                           [0.0, 0.0, 1.0, 0.0],
                           [dx, dy, dz, 1.0]])
        return m


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


class Vertex3d(Transformable):
    """
    Represents a single 3d vertex.
    """

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def transform(self, matrix):
        vector = np.array([self.x, self.y, self.z, 1.0])
        vector.dot(matrix.data, vector)
        self.x = vector[0] / vector[3]
        self.y = vector[1] / vector[3]
        self.z = vector[2] / vector[3]

    def get_transformed(self, matrix):
        vector = np.array([self.x, self.y, self.z, 1.0])
        vector.dot(matrix.data, vector)
        return Vertex3d(vector[0] / vector[3], vector[1] / vector[3], vector[2] / vector[3])


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
    def __init__(self, time_delay, color, transformation):
        self.time_delay = time_delay
        self.color = color
        self.transformation = transformation


class ScreenSaver(object):
    def __init__(self, engine, model, animation):
        self._engine = engine
        self._model = copy.deepcopy(model)
        self._animation = animation

        self._animation_thread = Thread(target=self._animate, daemon=True)

        self._engine.update()
        self._draw_frame()

    def _animate(self):
        while self.engine._is_animating.get() == 1:
            # self._draw_frame()
            # self._canvas.after(0, self._draw_frame())
            self._canvas.after(0, lambda: self._draw_frame())
            # self._canvas.update_idletasks()
            time.sleep(0.01)

    def _draw_frame(self):
        if self._model is not None:
            self._engine.clear()
            self._engine.draw_axes()

            rot = MatrixAffine4x4.build_rotation(2 * pi / 300, Vector3.unit_x())
            self._model.transform(rot)
            rot = MatrixAffine4x4.build_rotation(2 * pi / 300, Vector3.unit_z())
            # self._model.transform(rot)
            rot = MatrixAffine4x4.build_rotation(2 * pi / 300, Vector3.unit_y())
            # self._model.transform(rot)
            self._engine.draw_model(self._model, 3, "blue", False)
            self._engine.update_idletasks()
            # self._canvas.after(0, self._draw_frame())

    def start(self):
        self._animation_thread.start()
        pass

    def stop(self):
        pass


class GraphicsEngine2d(object):
    """
    Simple 3d graphics based on Tk.
    """

    def __init__(self, width, height, title):
        self.__root = tk.Tk()
        self.__root.title(title)
        self.__root.geometry(str(width) + "x" + str(height) + "+10+20")

        self._is_animating = tk.BooleanVar(self.__root, False)
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

        self.__init_ui()

    def __init_ui(self):
        """
        Simple test framework UI
        :return:
        """
        main_frame = tk.Frame(self.__root, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.grid_columnconfigure(0, weight=2)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        render_frame = tk.Frame(main_frame, bg="white")
        render_frame.grid(row=0, column=0, sticky="nsew")
        render_label = tk.Label(render_frame, text="Scene", bg="white", fg="gray", font=("Helvetica", 20))
        render_label.pack(side=tk.TOP)
        self._canvas = tk.Canvas(render_frame, bg="white")
        self._canvas.pack(fill=tk.BOTH, expand=True)
        control_frame = tk.Frame(main_frame, bg="gray")
        control_frame.grid(row=0, column=1, sticky="nsew")
        control_frame.grid_columnconfigure(0, weight=1)
        control_frame.grid_rowconfigure(0, weight=1)
        control_frame.grid_rowconfigure(1, weight=5)
        control_frame.grid_rowconfigure(2, weight=4)
        control_label = tk.Label(control_frame, text="Control", bg="gray", fg="white", font=("Helvetica", 20))
        control_label.grid(row=0, column=0, sticky="n")
        sliders_frame = tk.Frame(control_frame, bg="gray")
        sliders_frame.grid(row=1, column=0, sticky="nsew")
        sliders_frame.grid_columnconfigure(0, weight=1)
        sliders_frame.grid_rowconfigure(0, weight=1)
        sliders_frame.grid_rowconfigure(1, weight=1)
        sliders_frame.grid_rowconfigure(2, weight=1)
        sliders_frame.grid_rowconfigure(3, weight=1)
        sliders_frame.grid_rowconfigure(4, weight=1)
        sliders_frame.grid_rowconfigure(5, weight=1)
        sliders_frame.grid_rowconfigure(6, weight=1)
        sliders_frame.grid_rowconfigure(7, weight=1)
        sliders_frame.grid_rowconfigure(8, weight=1)
        sliders_frame.grid_rowconfigure(9, weight=1)
        sliders_frame.grid_rowconfigure(10, weight=1)
        sliders_frame.grid_rowconfigure(11, weight=1)

        views_label = tk.Label(sliders_frame, text="Views", bg="gray", fg="white", font=("Helvetica", 20))
        views_label.grid(row=0, column=0, sticky="n")

        view_front_radio = tk.Radiobutton(sliders_frame, text="Front", variable=self._view_type, value=0,
                                          indicatoron=0)
        view_front_radio.grid(row=1, column=0, sticky="new")
        view_back_radio = tk.Radiobutton(sliders_frame, text="Back", variable=self._view_type, value=1,
                                         indicatoron=0)
        view_back_radio.grid(row=2, column=0, sticky="new")
        view_up_radio = tk.Radiobutton(sliders_frame, text="Up", variable=self._view_type, value=2,
                                       indicatoron=0)
        view_up_radio.grid(row=3, column=0, sticky="new")
        view_down_radio = tk.Radiobutton(sliders_frame, text="Down", variable=self._view_type, value=3,
                                         indicatoron=0)
        view_down_radio.grid(row=4, column=0, sticky="new")
        view_left_radio = tk.Radiobutton(sliders_frame, text="Left", variable=self._view_type, value=4,
                                         indicatoron=0)
        view_left_radio.grid(row=5, column=0, sticky="new")
        view_right_radio = tk.Radiobutton(sliders_frame, text="Right", variable=self._view_type, value=5,
                                          indicatoron=0)
        view_right_radio.grid(row=6, column=0, sticky="new")

        projections_label = tk.Label(sliders_frame, text="Projections", bg="gray", fg="white", font=("Helvetica", 20))
        projections_label.grid(row=7, column=0, sticky="n")

        proj_orthogonal_radio = tk.Radiobutton(sliders_frame, text="Orthogonal", variable=self._projection_type,
                                               value=0, indicatoron=0)
        proj_orthogonal_radio.grid(row=8, column=0, sticky="new")

        axonometric_orthogonal_radio = tk.Radiobutton(sliders_frame, text="Axonometric", variable=self._projection_type,
                                                      value=1, indicatoron=0)
        axonometric_orthogonal_radio.grid(row=9, column=0, sticky="new")

        perspective_orthogonal_radio = tk.Radiobutton(sliders_frame, text="Perspective", variable=self._projection_type,
                                                      value=2, indicatoron=0)
        perspective_orthogonal_radio.grid(row=10, column=0, sticky="new")

        buttons_frame = tk.Frame(control_frame, bg="gray")
        buttons_frame.grid(row=2, column=0, sticky="nsew")
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_rowconfigure(0, weight=1)
        buttons_frame.grid_rowconfigure(1, weight=1)
        buttons_frame.grid_rowconfigure(2, weight=1)
        buttons_frame.grid_rowconfigure(3, weight=1)

        animation_on_check = tk.Checkbutton(buttons_frame, text="Animate", variable=self._is_animating,
                                            indicatoron=0, command=self._start_animation)
        animation_on_check.grid(row=0, column=0, sticky="new")

        reset_button = tk.Button(buttons_frame, fg="black", text="Reset",
                                 command=self._reset)
        reset_button.grid(row=2, column=0, sticky="sew")
        quit_button = tk.Button(buttons_frame, fg="black", text="Quit", command=quit)
        quit_button.grid(row=3, column=0, sticky="sew")

    def update(self):
        self._canvas.update()

    def clear(self):
        self._canvas.delete("all")

    def draw_axes(self):
        axis_len = 200.0

        model = Model()
        vid_zero = model.add_vertex(Vertex3d(0.0, 0.0, 0.0))
        vid_x = model.add_vertex(Vertex3d(axis_len, 0.0, 0.0))
        vid_y = model.add_vertex(Vertex3d(0.0, axis_len, 0.0))
        vid_z = model.add_vertex(Vertex3d(0.0, 0.0, axis_len))
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
            self._canvas.create_line(vertices2d[edge.vid_from].x + width / 2,
                                     vertices2d[edge.vid_from].y + height / 2,
                                     vertices2d[edge.vid_to].x + width / 2,
                                     vertices2d[edge.vid_to].y + height / 2,
                                     width=line_width,
                                     fill=color)

        if show_coord:
            for i in range(0, len(vertices)):
                self._canvas.create_text(vertices2d[i].x + width / 2, vertices2d[i].y + height / 2,
                                         text="{:.2f}".format(vertices[i].x) + ". " +
                                              "{:.2f}".format(vertices[i].y) + ". " +
                                              "{:.2f}".format(vertices[i].z),
                                         font=("Helvetica", 7))

    def show(self):
        self.__root.mainloop()


def create_box_model(width, height, depth):
    """
    According to Lab 3. Variant 10.
    Creates a box.

    :param width:
    :param height:
    :param depth:
    :return:
    """
    model = Model()
    vid_1 = model.add_vertex(Vertex3d(-width / 2, -height / 2, depth / 2))
    vid_2 = model.add_vertex(Vertex3d(width / 2, -height / 2, depth / 2))
    vid_3 = model.add_vertex(Vertex3d(width / 2, height / 2, depth / 2))
    vid_4 = model.add_vertex(Vertex3d(-width / 2, height / 2, depth / 2))
    vid_5 = model.add_vertex(Vertex3d(-width / 2, -height / 2, -depth / 2))
    vid_6 = model.add_vertex(Vertex3d(width / 2, -height / 2, -depth / 2))
    vid_7 = model.add_vertex(Vertex3d(width / 2, height / 2, -depth / 2))
    vid_8 = model.add_vertex(Vertex3d(-width / 2, height / 2, -depth / 2))
    model.add_edge(Edge(vid_1, vid_2))
    model.add_edge(Edge(vid_2, vid_3))
    model.add_edge(Edge(vid_3, vid_4))
    model.add_edge(Edge(vid_4, vid_1))
    model.add_edge(Edge(vid_5, vid_6))
    model.add_edge(Edge(vid_6, vid_7))
    model.add_edge(Edge(vid_7, vid_8))
    model.add_edge(Edge(vid_8, vid_5))
    model.add_edge(Edge(vid_1, vid_5))
    model.add_edge(Edge(vid_2, vid_6))
    model.add_edge(Edge(vid_3, vid_7))
    model.add_edge(Edge(vid_4, vid_8))

    return model


def main():
    model = create_box_model(300.0, 200.0, 100.0)
    engine2d = GraphicsEngine2d(1024, 768, "Lab 2. Variant 10.")
    animation = ()

    screen_saver = ScreenSaver(engine2d, model, animation)
    screen_saver.start()


main()
