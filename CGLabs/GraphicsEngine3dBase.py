"""
Prog:   GraphicsEngine3dBase.py

Auth:   Oleksii Krutko, IO-z91

Desc:   Computer graphics Labs. 2020

Simple 3d graphics based on Tk.

"""

import tkinter as tk
from math import pi

from graphics3d import MatrixAffine4x4, Vector3, Model, Vertex3d, Edge


class GraphicsEngine3dBase(object):
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

        vertices = model.get_vertices()
        for vertex in vertices:
            vertex.color = (127, 127, 127)

        self.draw_model(model, 1, True)

    def draw_model(self, model, line_width, show_coord):
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()

        facets = model.get_facets()
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
                            vertices2d[edge.vid_from].color,
                            vertices2d[edge.vid_to].color)

        for facet in facets:
            self._fill_facet(vertices2d[edge.vid_1].point.x + width / 2,
                             vertices2d[edge.vid_1].point.y + height / 2,
                             vertices2d[edge.vid_2].point.x + width / 2,
                             vertices2d[edge.vid_2].point.y + height / 2,
                             vertices2d[edge.vid_3].point.x + width / 2,
                             vertices2d[edge.vid_3].point.y + height / 2,
                             facet.color)

        if show_coord:
            for i in range(0, len(vertices)):
                self._draw_text(vertices2d[i].point.x + width / 2, vertices2d[i].point.y + height / 2,
                                "{:.2f}".format(vertices[i].point.x) + ". " +
                                "{:.2f}".format(vertices[i].point.y) + ". " +
                                "{:.2f}".format(vertices[i].point.z))

    def _draw_line(self, x_from, y_from, x_to, y_to, line_width, color_from, color_to):
        pass

    def _fill_facet(self, x_1, y_1, x_2, y_2, x_3, y_3, color):
        pass

    def _draw_text(self, x, y, text):
        pass

    def show(self):
        self.__root.mainloop()


def color_rgb(r, g, b):
    """
    r,g,b are intensities of red, green, and blue in range(256)
    Returns color specifier string for the resulting color
    """
    return "#%02x%02x%02x" % (r, g, b)
