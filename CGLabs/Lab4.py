"""
Prog:   Lab4.py

Auth:   Oleksii Krutko, IO-z91

Desc:   Computer graphics Lab 4. 2020

"""

import numpy as np
from PIL import Image, ImageTk
from graphics3d import Vector3, BoundingBox
from GraphicsEngine3dBase import GraphicsEngine3dBase
from ScreenSaver import ScreenSaver, build_animation


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

    def _draw_line(self, x_from, y_from, x_to, y_to, line_width, color_from, color_to, transparency):
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
                # Interpolate color between two vertices.

                sqr_dist = (x_to - x) ** 2 - (y_to - y) ** 2
                sqr_full_dist = (x_to - x_from) ** 2 - (y_to - y_from) ** 2
                if sqr_full_dist == 0.0:
                    fraction = 1.0
                else:
                    fraction = sqr_dist/sqr_full_dist

                r_n = (color_from[0] - color_to[0]) * fraction + color_to[0]
                g_n = (color_from[1] - color_to[1]) * fraction + color_to[1]
                b_n = (color_from[2] - color_to[2]) * fraction + color_to[2]

                r = self._pixels[y, x][0]
                g = self._pixels[y, x][1]
                b = self._pixels[y, x][2]

                blend_r = r * transparency + r_n * (1 - transparency)
                blend_g = g * transparency + g_n * (1 - transparency)
                blend_b = b * transparency + b_n * (1 - transparency)

                self._pixels[y, x] = (blend_r, blend_g, blend_b)

    def _fill_facet(self, x_1, y_1, x_2, y_2, x_3, y_3, color_1, color_2, color_3, transparency):
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
            for x in range(round(x_from), round(x_to) + 1):
                if 0 <= x < self._image.width() and 0 <= y < self._image.height():

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

                    r = self._pixels[y, x][0]
                    g = self._pixels[y, x][1]
                    b = self._pixels[y, x][2]

                    blend_r = r * transparency + r_n * (1 - transparency)
                    blend_g = g * transparency + g_n * (1 - transparency)
                    blend_b = b * transparency + b_n * (1 - transparency)

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


def main():
    engine2d = GraphicsEngine3dImage(1024, 768, "Lab 4. Variant 10.")

    model = BoundingBox(Vector3(-150.0, -100.0, -50.0), Vector3(150.0, 100.0, 50.0)) \
        .get_model()

    boundary_box = BoundingBox(Vector3(-250.0, -200.0, -150.0), Vector3(250.0, 200.0, 150.0))
    animation = build_animation(boundary_box)

    screen_saver = ScreenSaver(engine2d, model, animation, boundary_box)

    screen_saver.start()


main()
