"""
Prog:   GraphicsEngine3dBase.py

Auth:   Oleksii Krutko, IO-z91

Desc:   Computer graphics Labs. 2020

Simple 3d graphics based on Tk.

"""

import math
import random
import numpy as np
import tkinter as tk
from math import pi
from PIL import Image, ImageTk

from Bezier import evaluate_bezier
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
            0: MatrixAffine4x4.build_identity(),
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

        self.draw_model(model, 1, True, 0.0)

    def draw_model(self, model, line_width, show_coord, transparency):
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()

        facets = model.get_facets()
        edges = model.get_edges()
        vertices = model.get_vertices()
        vertices2d = []
        z_coords = []

        transform = MatrixAffine4x4.build_xy_reflection() * \
                    MatrixAffine4x4.build_xz_reflection() * \
                    self._view_types[self._view_type.get()] * \
                    self._projection_types[self._projection_type.get()]

        proj = transform * MatrixAffine4x4.build_orthogonal_proj()

        for vertex in vertices:
            z_coords.append(vertex.get_transformed(transform))
            vertices2d.append(vertex.get_transformed(proj))

        view_dir = Vector3.unit_z().neg()

        for edge in edges:
            self._draw_line(vertices2d[edge.vid_from].point.x + width / 2,
                            vertices2d[edge.vid_from].point.y + height / 2,
                            vertices2d[edge.vid_to].point.x + width / 2,
                            vertices2d[edge.vid_to].point.y + height / 2,
                            z_coords[edge.vid_from].point.z,
                            z_coords[edge.vid_to].point.z,
                            line_width,
                            vertices2d[edge.vid_from].color,
                            vertices2d[edge.vid_to].color,
                            transparency)

        for facet in facets:
            normal = facet.normal.get_transformed(transform.extract_rotation())

            dot = view_dir.dot(normal)

            if dot <= 0.01:
                continue

            self._fill_facet(vertices2d[facet.vid_1].point.x + width / 2,
                             vertices2d[facet.vid_1].point.y + height / 2,
                             z_coords[facet.vid_1].point.z,
                             vertices2d[facet.vid_2].point.x + width / 2,
                             vertices2d[facet.vid_2].point.y + height / 2,
                             z_coords[facet.vid_2].point.z,
                             vertices2d[facet.vid_3].point.x + width / 2,
                             vertices2d[facet.vid_3].point.y + height / 2,
                             z_coords[facet.vid_3].point.z,
                             vertices2d[facet.vid_1].color,
                             vertices2d[facet.vid_2].color,
                             vertices2d[facet.vid_3].color,
                             transparency)

        if show_coord:
            for i in range(0, len(vertices)):
                self._draw_text(vertices2d[i].point.x + width / 2, vertices2d[i].point.y + height / 2,
                                "{:.2f}".format(vertices[i].point.x) + ". " +
                                "{:.2f}".format(vertices[i].point.y) + ". " +
                                "{:.2f}".format(vertices[i].point.z))

    def _draw_line(self, x_from, y_from, x_to, y_to, z_from, z_to, line_width, color_from, color_to, transparency):
        pass

    def _fill_facet(self, x_1, y_1, z_1, x_2, y_2, z_2, x_3, y_3, z_3, color_1, color_2, color_3, transparency):
        pass

    def _draw_text(self, x, y, text):
        pass

    def show(self):
        self.__root.mainloop()


class GraphicsEngine3dImage(GraphicsEngine3dBase):
    """
    Simple 3d graphics based on Tk.
    """

    def __init__(self, width, height, title):
        super(GraphicsEngine3dImage, self).__init__(width, height, title)

        self._canvas.update()
        self._image_width = self._canvas.winfo_width()
        self._image_height = self._canvas.winfo_height()

        self._background = Image.new("RGB", (self._image_width, self._image_height), "white")
        self._pixels = np.array(self._background)
        self._z_buffer = np.empty([self._image_height, self._image_width], dtype=float)

        self._image = ImageTk.PhotoImage(image=self._background)

        self._image_on_canvas = self._canvas.create_image((self._image_width / 2, self._image_height / 2),
                                                          image=self._image)

    def _init_ui(self):
        super(GraphicsEngine3dImage, self)._init_ui()

    def update(self):
        self._background = Image.fromarray(self._pixels, mode="RGB")
        self._image = ImageTk.PhotoImage(self._background)
        self._canvas.itemconfig(self._image_on_canvas, image=self._image)

        super(GraphicsEngine3dImage, self).update()

    def clear(self):
        self._canvas.delete("labels")

        self._pixels.fill(255)
        self._z_buffer.fill(-float("inf"))

    def _draw_line(self, x_from, y_from, x_to, y_to, z_from, z_to, line_width, color_from, color_to, transparency):
        """
        Draws a line using Bresenham algorithm
        :param x_from:
        :param y_from:
        :param x_to:
        :param y_to:
        :param line_width:
        :param color_from:
        :param color_to:
        :param transparency:
        :return:
        """
        x1, y1 = x_from, y_from
        x2, y2 = x_to, y_to
        dx = x2 - x1
        dy = y2 - y1

        is_steep = abs(dy) > abs(dx)

        if is_steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        swapped = False
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            swapped = True

        dx = x2 - x1
        dy = y2 - y1

        error = int(dx / 2.0)
        y_step = 1 if y1 < y2 else -1

        y = y1
        points = []
        for x in range(round(x1), round(x2) + 1):
            coord = (y, x) if is_steep else (x, y)
            points.append(coord)
            error -= abs(dy)
            if error < 0:
                y += y_step
                error += dx

        if swapped:
            points.reverse()

        for point in points:
            x = round(point[0])
            y = round(point[1])
            if 0 <= x < self._image.width() and 0 <= y < self._image.height():

                # Check Z-Buffer
                if math.isclose(y_to - y_from, 0.0, abs_tol=1e-6):
                    z = z_to
                else:
                    z = ((y - y_from) / (y_to - y_from)) * (z_to - z_from) + z_from

                if self._z_buffer[y, x] > -z:
                    continue

                self._z_buffer[y, x] = -z

                # Interpolate color between two vertices.

                sqr_dist = (x_to - x) ** 2 - (y_to - y) ** 2
                sqr_full_dist = (x_to - x_from) ** 2 - (y_to - y_from) ** 2
                if math.isclose(sqr_full_dist, 0.0, abs_tol=1e-6):
                    self._pixels[y, x] = color_from
                    continue

                fraction = sqr_dist/sqr_full_dist

                r_n = (color_from[0] - color_to[0]) * fraction + color_to[0]
                g_n = (color_from[1] - color_to[1]) * fraction + color_to[1]
                b_n = (color_from[2] - color_to[2]) * fraction + color_to[2]

                blend_r = 255 * transparency + r_n * (1 - transparency)
                blend_g = 255 * transparency + g_n * (1 - transparency)
                blend_b = 255 * transparency + b_n * (1 - transparency)

                self._pixels[y, x] = (blend_r, blend_g, blend_b)

    def _fill_facet(self, x_1, y_1, z_1, x_2, y_2, z_2, x_3, y_3, z_3, color_1, color_2, color_3, transparency):
        p1 = np.array([x_1, y_1, z_1])
        p2 = np.array([x_2, y_2, z_2])
        p3 = np.array([x_3, y_3, z_3])

        v1 = p3 - p1
        v2 = p2 - p1

        cp = np.cross(v1, v2)

        a, b, c = cp

        d = np.dot(cp, p3)

        """
        Fills a triangle using scan line algorithm,
        :param x_1:
        :param y_1:
        :param x_2:
        :param y_2:
        :param x_3:
        :param y_3:
        :param color_1:
        :param color_2:
        :param color_3:
        :param transparency:
        :return:
        """
        def draw_hor_line(x_from, x_to, y):
            """
            Fill single horizontal line.
            :param x_from:
            :param x_to:
            :param y:
            :return:
            """
            w = self._image.width()
            h = self._image.height()
            x_r_from = round(x_from)
            x_r_to = round(x_to) + 1
            for x in range(x_r_from, x_r_to):
                if 0 <= x < w and 0 <= y < h:

                    # Check Z-Buffer
                    z = (d - a * x - b * y) / c

                    if self._z_buffer[y, x] > -z:
                        continue

                    self._z_buffer[y, x] = -z

                    # Interpolate color between three vertices.

                    sqr_dist_1 = (x_1 - x) ** 2 + (y_1 - y) ** 2
                    sqr_dist_2 = (x_2 - x) ** 2 + (y_2 - y) ** 2
                    sqr_dist_3 = (x_3 - x) ** 2 + (y_3 - y) ** 2

                    sqr_sum_dist = sqr_dist_1 + sqr_dist_2 + sqr_dist_3

                    fraction_1 = sqr_dist_1 / sqr_sum_dist
                    fraction_2 = sqr_dist_2 / sqr_sum_dist
                    fraction_3 = sqr_dist_3 / sqr_sum_dist

                    r_n = (color_1[0] * fraction_1 + color_2[0] * fraction_2 + color_3[0] * fraction_3)
                    g_n = (color_1[1] * fraction_1 + color_2[1] * fraction_2 + color_3[1] * fraction_3)
                    b_n = (color_1[2] * fraction_1 + color_2[2] * fraction_2 + color_3[2] * fraction_3)

                    blend_r = 255 * transparency + r_n * (1 - transparency)
                    blend_g = 255 * transparency + g_n * (1 - transparency)
                    blend_b = 255 * transparency + b_n * (1 - transparency)

                    self._pixels[y, x] = (blend_r, blend_g, blend_b)

        def fill_top(top_x_1, top_y_1, top_x_2, top_y_2, top_x_3, top_y_3):
            """
            Fills top flat triangle.
            :param top_x_1:
            :param top_y_1:
            :param top_x_2:
            :param top_y_2:
            :param top_x_3:
            :param top_y_3:
            :return:
            """
            interpol_1 = (top_x_3 - top_x_1) / (top_y_3 - top_y_1)
            interpol_2 = (top_x_3 - top_x_2) / (top_y_3 - top_y_2)

            cur_x_1 = top_x_3
            cur_x_2 = top_x_3

            scan_y = top_y_3
            while scan_y > top_y_1:
                if cur_x_1 < cur_x_2:
                    draw_hor_line(cur_x_1, cur_x_2, scan_y)
                else:
                    draw_hor_line(cur_x_2, cur_x_1, scan_y)

                cur_x_1 = cur_x_1 - interpol_1
                cur_x_2 = cur_x_2 - interpol_2
                scan_y = scan_y - 1

        def fill_bottom(bottom_x_1, bottom_y_1, bottom_x_2, bottom_y_2, bottom_x_3, bottom_y_3):
            """
            Fills bottom flat triangle.
            :param bottom_x_1:
            :param bottom_y_1:
            :param bottom_x_2:
            :param bottom_y_2:
            :param bottom_x_3:
            :param bottom_y_3:
            :return:
            """
            interpol_1 = (bottom_x_2 - bottom_x_1) / (bottom_y_2 - bottom_y_1)
            interpol_2 = (bottom_x_3 - bottom_x_1) / (bottom_y_3 - bottom_y_1)

            cur_x_1 = bottom_x_1
            cur_x_2 = bottom_x_1

            for scan_y in range(bottom_y_1, bottom_y_2 + 1):
                if cur_x_1 < cur_x_2:
                    draw_hor_line(cur_x_1, cur_x_2, scan_y)
                else:
                    draw_hor_line(cur_x_2, cur_x_1, scan_y)

                cur_x_1 = cur_x_1 + interpol_1
                cur_x_2 = cur_x_2 + interpol_2

        vertices = sorted([(round(x_1), round(y_1)), (round(x_2), round(y_2)), (round(x_3), round(y_3))],
                          key=lambda v: v[1])

        if vertices[1][1] == vertices[2][1] and vertices[0][1] == vertices[2][1]:
            return
        if vertices[1][1] == vertices[2][1]:
            fill_bottom(vertices[0][0], vertices[0][1], vertices[1][0], vertices[1][1], vertices[2][0], vertices[2][1])
        elif vertices[0][1] == vertices[1][1]:
            fill_top(vertices[0][0], vertices[0][1], vertices[1][0], vertices[1][1], vertices[2][0], vertices[2][1])
        else:
            v_mid = (round(vertices[0][0] + ((vertices[1][1] - vertices[0][1]) / (vertices[2][1] - vertices[0][1])) *
                           (vertices[2][0] - vertices[0][0])), vertices[1][1])
            fill_bottom(vertices[0][0], vertices[0][1], vertices[1][0], vertices[1][1], v_mid[0], v_mid[1])
            fill_top(vertices[1][0], vertices[1][1], v_mid[0], v_mid[1], vertices[2][0], vertices[2][1])

    def _draw_text(self, x, y, text):
        self._canvas.create_text(x, y,
                                 tag="labels",
                                 text=text,
                                 font=("Helvetica", 7))


class GraphicsEngine3dImageVector(GraphicsEngine3dImage):
    """
    Simple 3d graphics based on Tk.
    """

    def _draw_line(self, x_from, y_from, x_to, y_to, z_from, z_to, line_width, color_from, color_to, transparency):
        m = np.array([[x_from, y_from],
                       [(x_from + x_to)/2, (y_from + y_to)/2],
                         [x_to, y_to]])

        points = evaluate_bezier(m, 50)

        for point in points:
            x = round(point[0])
            y = round(point[1])
            if 0 <= x < self._image.width() and 0 <= y < self._image.height():
                self._pixels[y, x] = color_from


class GraphicsEngine3dImageVectorFractal(GraphicsEngine3dImageVector):
    """
    Simple 3d graphics based on Tk.
    """

    def __init__(self, width, height, title):
        super(GraphicsEngine3dImageVectorFractal, self).__init__(width, height, title)

        self._fractal_pixels = np.array(self._background)
        self._build_barnsley_fractal()
        self._build_sierpinsky_fractal()

    def _build_barnsley_fractal(self):
        """
        Draws several Barnsley ferns into _fractal_pixels.
        :return:
        """

        coeffs = np.array([[[0.0, 0.0, 0.0, 0.16, 0.0, 0.0, 1.0],
                            [0.85, 0.04, -0.04, 0.85, 0.0, 1.6, 85.0],
                            [0.2, -0.26, 0.23, 0.22, 0.0, 1.6, 7.0],
                            [-0.15, 0.28, 0.26, 0.24, 0.0, 0.44, 7.0]
                           ],
                           [[0.0, 0.0, 0.0, 0.25, 0.0, -0.14, 2.0],
                            [0.85, 0.02, -0.02, 0.83, 0.0, 1.0, 84.0],
                            [0.09, -0.28, 0.3, 0.11, 0.0, 0.6, 7.0],
                            [-0.09, 0.28, 0.3, 0.09, 0.0, 0.7, 7.0]
                            ],
                           [[0.0, 0.0, 0.0, 0.25, 0.0, -0.4, 2.0],
                            [0.95, 0.002, -0.002, 0.93, -0.002, 0.5, 84.0],
                            [0.035, -0.1, 0.27, 0.01, -0.05, 0.005, 7.0],
                            [-0.04, 0.11, 0.27, 0.01, 0.047, 0.06, 7.0]
                            ],
                           [[0.0, 0.0, 0.0, 0.2, 0.0, -0.12, 1.0],
                            [0.845, 0.035, -0.035, 0.82, 0.0, 1.6, 85.0],
                            [0.2, -0.31, 0.255, 0.245, 0.0, 0.29, 7.0],
                            [-0.15, 0.24, 0.25, 0.20, 0.0, 0.68, 7.0]
                            ]
                          ])

        for n in range(0, 4):
            x = []
            y = []

            x.append(coeffs[n, 0, 0])
            y.append(coeffs[n, 0, 1])

            current = 0

            for i in range(1, 50000):
                z = random.randint(1, 100)

                if 0 < z <= int(coeffs[n, 0, 6]):
                    x.append(coeffs[n, 0, 2])
                    y.append(coeffs[n, 0, 3] * (y[current]))

                if int(coeffs[n, 0, 6]) < z <= int(coeffs[n, 1, 6]) + int(coeffs[n, 0, 6]):
                    x.append(coeffs[n, 1, 0] * x[current] + coeffs[n, 1, 1] * y[current] + coeffs[n, 1, 4])
                    y.append(coeffs[n, 1, 2] * x[current] + coeffs[n, 1, 3] * y[current] + coeffs[n, 1, 5])

                if int(coeffs[n, 1, 6]) + int(coeffs[n, 0, 6]) < z <= int(coeffs[n, 2, 6]) + int(coeffs[n, 1, 6]) + int(coeffs[n, 0, 6]):
                    x.append(coeffs[n, 2, 0] * x[current] + coeffs[n, 2, 1] * y[current] + coeffs[n, 2, 4])
                    y.append(coeffs[n, 2, 2] * x[current] + coeffs[n, 2, 3] * y[current] + coeffs[n, 2, 5])

                if int(coeffs[n, 2, 6]) + int(coeffs[n, 1, 6]) + int(coeffs[n, 0, 6]) < z <= 100:
                    x.append(coeffs[n, 3, 0] * x[current] + coeffs[n, 3, 1] * y[current] + coeffs[n, 3, 4])
                    y.append(coeffs[n, 3, 2] * x[current] + coeffs[n, 3, 3] * y[current] + coeffs[n, 3, 5])

                current = current + 1

                p_x = int(x[i - 1] * 50 + (n + 1)*130)
                p_y = int(y[i - 1] * 40)

                if 0 <= p_x < self._image.width() and 0 <= p_y < self._image.height():
                    self._fractal_pixels[p_y, p_x] = (0, int(255 / (n + 1)), 0)

    def __draw_background_line(self, x_from, y_from, x_to, y_to, z_from, z_to, line_width, color_from,
                               color_to, transparency):
        m = np.array([[x_from, y_from],
                       [(x_from + x_to)/2, (y_from + y_to)/2],
                         [x_to, y_to]])

        points = evaluate_bezier(m, 50)

        for point in points:
            x = round(point[0])
            y = round(point[1])
            if 0 <= x < self._image.width() and 0 <= y < self._image.height():
                self._fractal_pixels[y, x] = color_from

    def _build_sierpinsky_fractal(self):
        """
        Draws several Sierpinsky's triangles into _fractal_pixels.
        :return:
        """

        def draw_sub_triangle(pt1_x, pt1_y, pt2_x, pt2_y, pt3_x, pt3_y, depth):
            if depth > 6:
                return

            self.__draw_background_line(pt1_x, pt1_y, pt2_x, pt2_y, 0.0, 0.0, 1.0,
                                        (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 0.0)
            self.__draw_background_line(pt2_x, pt2_y, pt3_x, pt3_y, 0.0, 0.0, 1.0,
                                        (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 0.0)
            self.__draw_background_line(pt3_x, pt3_y, pt1_x, pt1_y, 0.0, 0.0, 1.0,
                                        (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 0.0)

            pt_sub_1_x = (pt1_x + pt2_x) / 2
            pt_sub_1_y = (pt1_y + pt2_y) / 2
            pt_sub_2_x = pt2_x
            pt_sub_2_y = pt2_y
            pt_sub_3_x = (pt2_x + pt3_x) / 2
            pt_sub_3_y = (pt2_y + pt3_y) / 2

            draw_sub_triangle(pt_sub_1_x, pt_sub_1_y, pt_sub_2_x, pt_sub_2_y, pt_sub_3_x, pt_sub_3_y, depth + 1)

            pt_sub_1_x = (pt1_x + pt3_x) / 2
            pt_sub_1_y = (pt1_y + pt3_y) / 2
            pt_sub_2_x = pt3_x
            pt_sub_2_y = pt3_y
            pt_sub_3_x = (pt2_x + pt3_x) / 2
            pt_sub_3_y = (pt2_y + pt3_y) / 2

            draw_sub_triangle(pt_sub_1_x, pt_sub_1_y, pt_sub_2_x, pt_sub_2_y, pt_sub_3_x, pt_sub_3_y, depth + 1)

            pt_sub_1_x = (pt1_x + pt2_x) / 2
            pt_sub_1_y = (pt1_y + pt2_y) / 2
            pt_sub_2_x = pt1_x
            pt_sub_2_y = pt1_y
            pt_sub_3_x = (pt1_x + pt3_x) / 2
            pt_sub_3_y = (pt1_y + pt3_y) / 2

            draw_sub_triangle(pt_sub_1_x, pt_sub_1_y, pt_sub_2_x, pt_sub_2_y, pt_sub_3_x, pt_sub_3_y, depth + 1)

        w = self._image_width
        h = self._image_height

        draw_sub_triangle(0, h / 2, w / 4, h, w / 2, h / 2, 1)
        draw_sub_triangle(3 * w / 4, h / 2, w / 2, h, w, h, 1)

    def clear(self):
        self._canvas.delete("labels")

        self._pixels = self._fractal_pixels.copy()
        self._z_buffer.fill(-float("inf"))


def color_rgb(r, g, b):
    """
    r,g,b are intensities of red, green, and blue in range(256)
    Returns color specifier string for the resulting color
    """
    return "#%02x%02x%02x" % (r, g, b)
