"""
Prog:   Lab2.py

Auth:   Oleksii Krutko, IO-z91

Desc:   Computer graphics Lab 2. 2020

"""

import time
import copy
import tkinter as tk
import numpy as np
from math import *


def build_identity():
    return np.array([[1.0, 0.0, 0.0],
                     [0.0, 1.0, 0.0],
                     [0.0, 0.0, 1.0]])


def build_rotation(angle):
    return np.array([[cos(angle), sin(angle), 0.0],
                     [-sin(angle), cos(angle), 0.0],
                     [0.0, 0.0, 1.0]])


def build_scale(sx, sy):
    return np.array([[sx, 0.0, 0.0],
                     [0.0, sy, 0.0],
                     [0.0, 0.0, 1.0]])


def build_translation(dx, dy):
    return np.array([[1.0, 0.0, 0.0],
                     [0.0, 1.0, 0.0],
                     [dx, dy, 1.0]])


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

    def transform_scalar(self, matrix):
        """
        Uses scalar operations to transform.
        :param matrix: transformation matrix
        :return:
        """
        pass


class Vertex2d(Transformable):
    """
    Represents a single 2d vertex.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def transform(self, matrix):
        vector = np.array([self.x, self.y, 1.0])
        vector.dot(matrix, vector)
        self.x = vector[0]
        self.y = vector[1]

    def transform_scalar(self, matrix):
        new_x = self.x*matrix[0][0] + self.y*matrix[1][0] + matrix[2][0]
        new_y = self.x*matrix[0][1] + self.y*matrix[1][1] + matrix[2][1]
        self.x = new_x
        self.y = new_y


class Edge(object):
    """
    Represents an edge between two vertices.
    """
    def __init__(self, vid_from, vid_to):
        self.vid_from = vid_from
        self.vid_to = vid_to


class Model(Transformable):
    """
    Represents 2d geometry objects.
    """
    def __init__(self):
        self._vertices = []
        self._edges = []

    def transform(self, matrix):
        for vertex in self._vertices:
            vertex.transform(matrix)

    def transform_scalar(self, matrix):
        for vertex in self._vertices:
            vertex.transform_scalar(matrix)

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


class GraphicsEngine2d(object):
    """
    Simple 2d graphics based on Tk.
    """
    def __init__(self, width, height, title):
        self.__root = tk.Tk()
        self.__root.title(title)
        self.__root.geometry(str(width) + "x" + str(height) + "+10+20")
        self._transform_callback = None
        self._show_trajectory = tk.BooleanVar(self.__root, True)
        self._use_scalar = tk.BooleanVar(self.__root, False)
        self.rotation_angle = 0.0
        self.scale_x = 1.0
        self.scale_y = 1.0
        self.trans_x = 0.0
        self.trans_y = 0.0

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
        rotation_label = tk.Label(sliders_frame, text="Rotation angle (deg)", bg="gray", fg="white",
                                  font=("Helvetica", 10))
        rotation_label.grid(row=0, column=0, sticky="n")
        self._rotation_slider = tk.Scale(sliders_frame, from_=-180, to=180, bg="gray", fg="white",
                                         font=("Helvetica", 10), orient=tk.HORIZONTAL)
        self._rotation_slider.set(0)
        self._rotation_slider.grid(row=1, column=0, sticky="new")
        scale_x_label = tk.Label(sliders_frame, text="Scale X (/10)", bg="gray", fg="white", font=("Helvetica", 10))
        scale_x_label.grid(row=2, column=0, sticky="n")
        self._scale_x_slider = tk.Scale(sliders_frame, from_=5, to=20, tickinterval=0.1, bg="gray", fg="white",
                                        font=("Helvetica", 10), orient=tk.HORIZONTAL)
        self._scale_x_slider.set(10)
        self._scale_x_slider.grid(row=3, column=0, sticky="new")
        scale_y_label = tk.Label(sliders_frame, text="Scale Y (/10)", bg="gray", fg="white", font=("Helvetica", 10))
        scale_y_label.grid(row=4, column=0, sticky="n")
        self._scale_y_slider = tk.Scale(sliders_frame, from_=5, to=20, tickinterval=0.1, bg="gray", fg="white",
                                        font=("Helvetica", 10), orient=tk.HORIZONTAL)
        self._scale_y_slider.set(10)
        self._scale_y_slider.grid(row=5, column=0, sticky="new")
        trans_x_label = tk.Label(sliders_frame, text="Trans X", bg="gray", fg="white", font=("Helvetica", 10))
        trans_x_label.grid(row=6, column=0, sticky="n")
        self._trans_x_slider = tk.Scale(sliders_frame, from_=-100, to=100, bg="gray", fg="white",
                                        font=("Helvetica", 10), orient=tk.HORIZONTAL)
        self._trans_x_slider.set(0)
        self._trans_x_slider.grid(row=7, column=0, sticky="new")
        trans_y_label = tk.Label(sliders_frame, text="Trans Y", bg="gray", fg="white", font=("Helvetica", 10))
        trans_y_label.grid(row=8, column=0, sticky="n")
        self._trans_y_slider = tk.Scale(sliders_frame, from_=-100, to=100, bg="gray", fg="white",
                                        font=("Helvetica", 10), orient=tk.HORIZONTAL)
        self._trans_y_slider.set(0)
        self._trans_y_slider.grid(row=9, column=0, sticky="new")
        trajectory_check = tk.Checkbutton(sliders_frame, text="Show trajectory", variable=self._show_trajectory)
        trajectory_check.grid(row=10, column=0, sticky="new")
        scalar_check = tk.Checkbutton(sliders_frame, text="Use scalar", variable=self._use_scalar)
        scalar_check.grid(row=11, column=0, sticky="new")
        buttons_frame = tk.Frame(control_frame, bg="gray")
        buttons_frame.grid(row=2, column=0, sticky="nsew")
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_rowconfigure(0, weight=1)
        buttons_frame.grid_rowconfigure(1, weight=1)
        buttons_frame.grid_rowconfigure(2, weight=1)
        buttons_frame.grid_rowconfigure(3, weight=1)
        self.__transform_scale_button = tk.Button(buttons_frame, fg="black", text="Scale",
                                                  command=self._transform_scale)
        self.__transform_scale_button.grid(row=0, column=0, sticky="sew")
        self.__transform_trans_rot_button = tk.Button(buttons_frame, fg="black", text="(Trans + Rot)",
                                                      command=self._transform_trans_rot)
        self.__transform_trans_rot_button.grid(row=1, column=0, sticky="sew")
        reset_button = tk.Button(buttons_frame, fg="black", text="Reset",
                                 command=self._reset)
        reset_button.grid(row=2, column=0, sticky="sew")
        quit_button = tk.Button(buttons_frame, fg="black", text="Quit", command=quit)
        quit_button.grid(row=3, column=0, sticky="sew")

    def _transform_scale(self):
        """
        According to Lab 2. Variant 10.
        Performs Scale operation. Sets other params to 0.0, so that only scale params have effect.

        :return:
        """
        if self.set_transform_callback is not None:
            self._transform_callback(0.0,
                                     self._scale_x_slider.get() / 10,
                                     self._scale_y_slider.get() / 10,
                                     0.0,
                                     0.0,
                                     self._show_trajectory.get(),
                                     self._use_scalar.get())

    def _transform_trans_rot(self):
        """
        According to Lab 2. Variant 10.
        Performs Translation+Rotation operation. Sets other params to 1.0,
        so that only rotation and transformation params have effect.

        :return:
        """
        if self.set_transform_callback is not None:
            self._transform_callback(self._rotation_slider.get(),
                                     1.0,
                                     1.0,
                                     self._trans_x_slider.get(),
                                     self._trans_y_slider.get(),
                                     self._show_trajectory.get(),
                                     self._use_scalar.get())

    def set_transform_callback(self, transform_callback):
        self._transform_callback = transform_callback

    def _reset(self):
        self._rotation_slider.set(0)
        self._scale_x_slider.set(10)
        self._scale_y_slider.set(10)
        self._trans_x_slider.set(0)
        self._trans_y_slider.set(0)

    def clear(self):
        self._canvas.delete("all")

    def draw_axes(self):
        self._canvas.update()
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()
        margin_x = width / 40
        margin_y = height / 40

        self._canvas.create_line(width / 2, 0, width / 2, height, width=1)
        self._canvas.create_line(0, height / 2, width, height / 2, width=1)
        self._canvas.create_text(width / 2 - margin_x, margin_y, text="X")
        self._canvas.create_text(width - margin_x, height / 2 - margin_y, text="Y")
        self._canvas.create_text(width / 2 - margin_x, height / 2 - margin_y, text="0.0")

    def draw_model(self, model, line_width, color, show_coords):
        self._canvas.update()
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()

        edges = model.get_edges()
        vertices = model.get_vertices()
        for edge in edges:
            self._canvas.create_line(vertices[edge.vid_from].x + width / 2,
                                     vertices[edge.vid_from].y + height / 2,
                                     vertices[edge.vid_to].x + width / 2,
                                     vertices[edge.vid_to].y + height / 2,
                                     width=line_width,
                                     fill=color)

        if show_coords:
            for vertex in vertices:
                self._canvas.create_text(vertex.x + width / 2, vertex.y + height / 2,
                                         text="{:.2f}".format(vertex.x) + ". " + "{:.2f}".format(vertex.y),
                                         font=("Helvetica", 7))

    def show(self):
        self.__root.mainloop()


def create_box_model(width, height):
    """
    According to Lab 2. Variant 10.
    Creates a box.

    :param width:
    :param height:
    :return:
    """
    model = Model()
    vid_1 = model.add_vertex(Vertex2d(-width / 2, -height / 2))
    vid_2 = model.add_vertex(Vertex2d(width / 2, -height / 2))
    vid_3 = model.add_vertex(Vertex2d(width / 2, height / 2))
    vid_4 = model.add_vertex(Vertex2d(-width / 2, height / 2))
    model.add_edge(Edge(vid_1, vid_2))
    model.add_edge(Edge(vid_2, vid_3))
    model.add_edge(Edge(vid_3, vid_4))
    model.add_edge(Edge(vid_4, vid_1))

    return model


def main():
    model = create_box_model(400.0, 200.0)

    engine2d = GraphicsEngine2d(1024, 768, "Lab 2. Variant 10.")

    engine2d.draw_axes()
    engine2d.draw_model(model, 3, "blue", True)

    def transform_callback(rotation_angle, scale_x, scale_y, trans_x, trans_y, show_trajectory, use_scalar):
        engine2d.clear()

        engine2d.draw_axes()

        scale_sequence = []
        rotation_sequence = []
        translation_sequence = []

        iterations_num = 10

        for i in range(1, iterations_num + 1):
            scale_sequence.append(build_scale(scale_x ** (1 / iterations_num), scale_y ** (1 / iterations_num)))

        for i in range(1, iterations_num + 1):
            rotation_sequence.append(build_rotation((rotation_angle * 2 * pi / 360) / iterations_num))

        for i in range(1, iterations_num + 1):
            translation_sequence.append(build_translation(trans_x / iterations_num, trans_y / iterations_num))

        transformations = []

        if show_trajectory:
            transformations.append(build_identity())

            for i in range(1, iterations_num + 1):
                intermediate_scale = build_identity()
                for j in range(0, i):
                    intermediate_scale = intermediate_scale.dot(scale_sequence[j])

                intermediate_rotation = build_identity()
                for j in range(0, i):
                    intermediate_rotation = intermediate_rotation.dot(rotation_sequence[j])

                intermediate_translation = build_identity()
                for j in range(0, i):
                    intermediate_translation = intermediate_translation.dot(translation_sequence[j])

                transformations.append(intermediate_scale.dot(intermediate_translation.dot(intermediate_rotation)))
        else:
            transformations.append(build_identity())

            final_scale = build_identity()
            for scale in scale_sequence:
                final_scale = final_scale.dot(scale)

            final_rotation = build_identity()
            for rotation in rotation_sequence:
                final_rotation = final_rotation.dot(rotation)

            final_translation = build_identity()
            for translation in translation_sequence:
                final_translation = final_translation.dot(translation)

            transformations.append(final_scale.dot(final_translation.dot(final_rotation)))

        for i in range(0, len(transformations)):
            model_transformed = copy.deepcopy(model)
            if use_scalar:
                model_transformed.transform_scalar(transformations[i])
            else:
                model_transformed.transform(transformations[i])

            line_width = 1
            color = "black"
            show_coord = False
            if i == 0 or i == len(transformations) - 1:
                line_width = 3
                show_coord = True

            if i == 0:
                color = "blue"

            if i == len(transformations) - 1:
                color = "red"

            engine2d.draw_model(model_transformed, line_width, color, show_coord)
            time.sleep(0.1)

    engine2d.set_transform_callback(transform_callback)

    engine2d.show()


main()
